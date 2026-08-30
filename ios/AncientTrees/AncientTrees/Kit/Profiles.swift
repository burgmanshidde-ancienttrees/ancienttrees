// Who you are, and who you follow.
//
// Hidde cleared the gate on 2026-08-26 ("extra persoonsgegevens moet gewoon"),
// which is the explicit yes the accounts rule asks for before anything new
// about a person is stored. What is stored is in supabase/profiles.sql and
// nowhere else: a display name, an avatar url, and rows saying one account
// follows another. Everything cascades off auth.users, so deleting an account
// still takes all of it, which was the condition of opening accounts at all.
//
// UNTIL THAT SQL IS RUN every call here fails quietly and the app shows the
// same page it showed yesterday: a name you can set locally and no followers.
// That is the honest-empty rule the rest of this project follows, and it means
// this can ship before the database catches up.

import Foundation
import Observation

@MainActor
@Observable
public final class Profiles {
    public struct Profile: Codable, Sendable, Hashable {
        public let user_id: String
        public var display_name: String
        public var avatar_url: String?
        /// "km" or "mi", or nil when they never chose and the phone's own
        /// locale is still deciding. A preference rather than data, and one
        /// more thing that should not stay behind on an old phone.
        public var units: String?
    }

    public private(set) var me: Profile?
    public private(set) var followers = 0
    public private(set) var following = 0

    public init() {
        // Debug scaffolding, the same family as -collected=, -mine-demo and
        // -signed-in: give the signed-in demo account a name.
        //
        // Without it the name falls back to the local part of the fake
        // session's address and every screenshot of My trees is headed "test",
        // which is how a store screenshot announces that it is a test build.
        // Found by looking at the five App Store screenshots on 2026-08-28,
        // which is what the script that makes them tells you to do.
        if let arg = ProcessInfo.processInfo.arguments
            .first(where: { $0.hasPrefix("-as=") }) {
            let name = String(arg.dropFirst(4))
            if !name.isEmpty {
                me = Profile(user_id: "00000000-0000-0000-0000-0000000000ab",
                             display_name: name, avatar_url: nil, units: nil)
            }
        }
    }

    /// SUPA.REQUEST, not a builder of our own.
    ///
    /// This was one, and the comment it carried is worth keeping because it
    /// names the bug: appendingPathComponent percent-encodes a "?" into %3F, so
    /// "profiles?on_conflict=user_id" became a TABLE NAME with a question mark
    /// in it and PostgREST refused the lot. Saving a name or a picture had
    /// never once worked, follower counts were always zero, and a report or a
    /// block only ever happened on the phone. Nothing said so: the refusal was
    /// swallowed. Supa.request has always concatenated, which is exactly why
    /// saves, visited and sightings were fine all along, and is the argument
    /// for there being one builder rather than seven.
    private func request(_ path: String, _ method: String, token: String?,
                         body: Data? = nil, prefer: String? = nil) -> URLRequest {
        Supa.request("/rest/v1/" + path, method: method, token: token,
                     body: body, prefer: prefer)
    }

    /// Your own row, and the two counts beside it.
    public func load(userId: String?, token: String?) async {
        guard let userId, let token else { me = nil; followers = 0; following = 0; return }
        if let data = try? await send(request(
            "profiles?select=user_id,display_name,avatar_url,units&user_id=eq.\(userId)",
            "GET", token: token)),
           let rows = try? JSONDecoder().decode([Profile].self, from: data) {
            me = rows.first
        }
        struct Counts: Decodable { let followers: Int; let following: Int }
        if let data = try? await send(request("rpc/follow_counts", "POST", token: token,
                                              body: try? JSONEncoder().encode(["uid": userId]))),
           let rows = try? JSONDecoder().decode([Counts].self, from: data),
           let c = rows.first {
            followers = c.followers
            following = c.following
        }
    }

    /// Who you were, forgotten on this phone. Called on sign-out, so the
    /// picture and the name go with the session rather than sitting over a
    /// signed-out settings page (Hidde, 2026-08-29: "profielfoto moet weg als
    /// je uitlogt"). Nothing is deleted anywhere else: this row is the
    /// account's and it comes back with the next sign-in.
    public func forgetLocally() {
        me = nil
        followers = 0
        following = 0
    }

    /// Set or change what people see. The name is the only thing required; an
    /// avatar is optional and stays optional.
    public func save(name: String, avatarURL: String?, userId: String, token: String) async -> Bool {
        struct Row: Encodable { let user_id: String; let display_name: String; let avatar_url: String? }
        let body = try? JSONEncoder().encode([Row(user_id: userId,
                                                  display_name: name,
                                                  avatar_url: avatarURL)])
        let ok = (try? await send(request("profiles?on_conflict=user_id", "POST",
                                          token: token, body: body,
                                          prefer: "resolution=merge-duplicates"))) != nil
        if ok { me = Profile(user_id: userId, display_name: name, avatar_url: avatarURL) }
        return ok
    }

    public func follow(_ other: String, me userId: String, token: String) async {
        struct Row: Encodable { let follower: String; let followee: String }
        _ = try? await send(request("follows", "POST", token: token,
                                    body: try? JSONEncoder().encode([Row(follower: userId,
                                                                         followee: other)])))
        await load(userId: userId, token: token)
    }

    public func unfollow(_ other: String, me userId: String, token: String) async {
        _ = try? await send(request("follows?follower=eq.\(userId)&followee=eq.\(other)",
                                    "DELETE", token: token))
        await load(userId: userId, token: token)
    }

    /// People, by the name they chose. The only way to find somebody, which is
    /// deliberate: there is no browsing of everybody who ever signed up.
    public func search(_ query: String, token: String?) async -> [Profile] {
        let q = query.trimmingCharacters(in: .whitespaces)
        guard q.count >= 2 else { return [] }
        let escaped = q.addingPercentEncoding(withAllowedCharacters: .alphanumerics) ?? q
        guard let data = try? await send(request(
            "profiles?select=user_id,display_name,avatar_url,units&display_name=ilike.*\(escaped)*&limit=25",
            "GET", token: token)) else { return [] }
        return (try? JSONDecoder().decode([Profile].self, from: data)) ?? []
    }

    /// Names and pictures for a set of ids. The blocked list keeps ids and
    /// nothing else, and a screen that lists ids is a screen nobody can use.
    public func byIds(_ ids: [String], token: String?) async -> [Profile] {
        guard !ids.isEmpty else { return [] }
        let list = ids.joined(separator: ",")
        guard let data = try? await send(request(
            "profiles?select=user_id,display_name,avatar_url,units&user_id=in.(\(list))",
            "GET", token: token)) else { return [] }
        return (try? JSONDecoder().decode([Profile].self, from: data)) ?? []
    }

    /// Which units they read distances in, kept with the profile because it is
    /// the row that already belongs to them. Its own call, so changing a unit
    /// does not rewrite a name and a picture.
    public func saveUnits(_ units: String, userId: String, token: String) async {
        struct Row: Encodable { let user_id: String; let units: String }
        let body = try? JSONEncoder().encode([Row(user_id: userId, units: units)])
        _ = try? await send(request("profiles?on_conflict=user_id", "POST", token: token,
                                    body: body, prefer: "resolution=merge-duplicates"))
        me?.units = units
    }

    private func send(_ r: URLRequest) async throws -> Data {
        let (data, response) = try await Net.data(for: r)
        let code = (response as? HTTPURLResponse)?.statusCode ?? 0
        guard (200..<300).contains(code) else {
            throw NSError(domain: "profiles", code: code)
        }
        return data
    }
}
