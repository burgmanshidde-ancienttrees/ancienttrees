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

    /// One person looking after one place (supabase/ambassadors.sql). The
    /// badge is the whole of it: komoot's Pioneer shape, per place, beside the
    /// name (CONVENTIONS.md 2026-10-02). `public` is consent to be NAMED on the
    /// website; the app shows the badge to signed-in readers either way,
    /// because a profile is already public here.
    public struct Ambassador: Codable, Sendable, Hashable {
        public let user_id: String
        public let place_slug: String
        public let place_name: String
        public let `public`: Bool
    }

    public private(set) var me: Profile?
    /// True once the server has answered about your own row. A fetch that
    /// failed (offline, a test with no server) leaves `me` nil and this false,
    /// and nobody is asked for a name on the strength of a missing answer.
    public private(set) var meLoaded = false
    public private(set) var followers = 0
    public private(set) var following = 0
    /// The places you are the ambassador of, usually none.
    public private(set) var myPlaces: [Ambassador] = []
    /// Your country, an ISO two-letter code you picked in Edit profile, for
    /// the flag after your name (supabase/profiles.sql, 2026-10-16). Read on
    /// its own rather than in the profile select, so a database without the
    /// column yet costs the flag and never the name.
    public private(set) var myCountry: String?
    /// You chose "Don't show" (profiles.flag_hidden, 2026-10-20), so the
    /// default flag never comes back. False until the server says otherwise.
    public private(set) var myFlagHidden = false
    /// Other people's badges, by user id, filled as lists load.
    public private(set) var placesByUser: [String: [Ambassador]] = [:]
    /// Whether your profile is open to anybody (profiles.public, 2026-10-19;
    /// supabase/public-profiles.sql). Nil until the server answers, and nil
    /// for good on a database without the column, so the Public profile
    /// switch in Settings shows only when it can store something.
    public private(set) var myPublic: Bool?

    /// Somebody's profile as anybody may see it, from public_profile(): only
    /// while its owner made it public, never the day a tree was ticked.
    public struct PublicProfile: Decodable, Sendable, Hashable {
        public let user_id: String
        public let display_name: String
        public let avatar_url: String?
        public let country: String?
        public let created_at: String?
        public let followers: Int
        public let following: Int
        public let ambassador: [String]
        public let visited: [String]
        public let saves: [String]
    }

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
        // -people-demo: the first demo person wears a badge, so the People
        // list is photographed with one in it.
        if DemoPeople.on, let first = DemoPeople.all.first {
            placesByUser[first.user_id] = [Ambassador(user_id: first.user_id, place_slug: "amsterdam",
                                                      place_name: "Amsterdam", public: true)]
        }
        // -ambassador=Paris: the badge on the demo account, so the screen
        // sweep photographs it (a screen no argument can open ships unseen).
        if let arg = ProcessInfo.processInfo.arguments
            .first(where: { $0.hasPrefix("-ambassador=") }) {
            let place = String(arg.dropFirst(12))
            if !place.isEmpty {
                myPlaces = [Ambassador(user_id: me?.user_id ?? "00000000-0000-0000-0000-0000000000ab",
                                       place_slug: place.lowercased(), place_name: place, public: false)]
            }
        }
        // -public=off / -public=on: the Public profile switch on the demo
        // account, for the sweep (2026-10-19).
        if let arg = ProcessInfo.processInfo.arguments
            .first(where: { $0.hasPrefix("-public=") }) {
            myPublic = arg == "-public=on"
        }
        // -country=NL: the flag on the demo account, for the sweep.
        if let arg = ProcessInfo.processInfo.arguments
            .first(where: { $0.hasPrefix("-country=") }) {
            myCountry = String(arg.dropFirst(9)).uppercased()
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
        // Signed out clears; a token we could not renew does NOT (2026-10-08).
        // The old guard wiped the avatar and the follow counts on every launch
        // where the refresh found no signal, although the person was still
        // signed in. Without a token the reads go out on the publishable key,
        // which the profile and count reads accept.
        guard let userId else { me = nil; meLoaded = false; followers = 0; following = 0; return }
        if let data = try? await send(request(
            "profiles?select=user_id,display_name,avatar_url,units&user_id=eq.\(userId)",
            "GET", token: token)),
           let rows = try? JSONDecoder().decode([Profile].self, from: data) {
            me = rows.first
            meLoaded = true
        }
        if let data = try? await send(request(
            "ambassadors?select=user_id,place_slug,place_name,public&user_id=eq.\(userId)",
            "GET", token: token)),
           let rows = try? JSONDecoder().decode([Ambassador].self, from: data) {
            myPlaces = rows
            placesByUser[userId] = rows
        }
        // Unchosen, your flag is the phone's region (Hidde, 2026-10-20: "bij
        // polarsteps heb ik de vlag zonder ooit actief nederland te hebben
        // aangevinkt"), written once to a profile row that exists. A database
        // without flag_hidden yet reads the country alone and fills nothing.
        struct FlagRow: Decodable { let country: String?; let flag_hidden: Bool }
        struct CountryRow: Decodable { let country: String? }
        if let data = try? await send(request(
            "profiles?select=country,flag_hidden&user_id=eq.\(userId)", "GET", token: token)),
           let rows = try? JSONDecoder().decode([FlagRow].self, from: data) {
            myCountry = rows.first?.country
            myFlagHidden = rows.first?.flag_hidden ?? false
            if rows.first != nil, myCountry == nil, !myFlagHidden, let token,
               let guess = Self.countryGuess() {
                _ = await saveCountry(guess, userId: userId, token: token)
            }
        } else if let data = try? await send(request(
            "profiles?select=country&user_id=eq.\(userId)", "GET", token: token)),
           let rows = try? JSONDecoder().decode([CountryRow].self, from: data) {
            myCountry = rows.first?.country
        }
        struct PublicRow: Decodable { let `public`: Bool }
        if let data = try? await send(request(
            "profiles?select=public&user_id=eq.\(userId)", "GET", token: token)),
           let rows = try? JSONDecoder().decode([PublicRow].self, from: data) {
            myPublic = rows.first?.public ?? false
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
        meLoaded = false
        followers = 0
        following = 0
        myPlaces = []
        myCountry = nil
        myFlagHidden = false
        myPublic = nil
    }

    /// The badges of the people in a list, one request for the whole list.
    /// Fails quietly into "no badges", the honest-empty rule, until the table
    /// exists.
    public func loadAmbassadors(for ids: [String], token: String?) async {
        let wanted = Array(Set(ids)).filter { placesByUser[$0] == nil }
        guard !wanted.isEmpty, let token else { return }
        let list = wanted.joined(separator: ",")
        guard let data = try? await send(request(
            "ambassadors?select=user_id,place_slug,place_name,public&user_id=in.(\(list))",
            "GET", token: token)),
              let rows = try? JSONDecoder().decode([Ambassador].self, from: data) else {
            for id in wanted { placesByUser[id] = [] }
            return
        }
        for id in wanted { placesByUser[id] = [] }
        for r in rows { placesByUser[r.user_id, default: []].append(r) }
    }

    /// Set or change what people see. The name is the only thing required; an
    /// avatar is optional and stays optional.
    /// "Hidde Burgmans" -> "Hidde B.", which is how Strava and Polarsteps show a
    /// name taken from a provider in a list: a first name, and no surname
    /// published for somebody who never typed one. Pure, for the test.
    nonisolated public static func shortName(from full: String) -> String {
        let parts = full.split(separator: " ").map(String.init).filter { !$0.isEmpty }
        guard let first = parts.first else { return "" }
        if parts.count == 1 { return String(first.prefix(40)) }
        return String("\(first) \(parts[parts.count - 1].prefix(1)).".prefix(40))
    }

    /// Give a profile its first name from what the provider said, once.
    /// True when a name exists afterwards, from before or from this call;
    /// false means the person has to be asked (ProfileEditor).
    public func ensureName(userId: String, token: String, providerName: String?) async -> Bool {
        if let me, !me.display_name.isEmpty { return true }
        // No answer from the server is not "no name": asking would open the
        // editor over every offline launch, and did, in the flow walk.
        guard meLoaded else { return true }
        guard let providerName else { return false }
        let short = Self.shortName(from: providerName)
        guard !short.isEmpty else { return false }
        return await save(name: short, avatarURL: me?.avatar_url, userId: userId, token: token)
    }

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

    /// True when the account accepted it. A refusal (offline, a revoked
    /// token, following yourself) used to be swallowed here and the button
    /// in People stayed on the state the finger asked for (2026-10-02).
    @discardableResult
    public func follow(_ other: String, me userId: String, token: String) async -> Bool {
        struct Row: Encodable { let follower: String; let followee: String }
        let ok = (try? await send(request("follows", "POST", token: token,
                                          body: try? JSONEncoder().encode([Row(follower: userId,
                                                                               followee: other)])))) != nil
        await load(userId: userId, token: token)
        return ok
    }

    @discardableResult
    public func unfollow(_ other: String, me userId: String, token: String) async -> Bool {
        let ok = (try? await send(request("follows?follower=eq.\(userId)&followee=eq.\(other)",
                                          "DELETE", token: token))) != nil
        await load(userId: userId, token: token)
        return ok
    }

    /// WHO FOLLOWS YOU, and who you follow (Hidde, 2026-09-04: "ik zie ook dat
    /// ik twee followers heb, opzich nice als ik daar op kan klikken en volg
    /// terug kan doen"). The numbers have been on the profile since the first
    /// day and led nowhere, which makes them decoration rather than people.
    ///
    /// Two calls rather than a join, because the follows table holds ids and
    /// the names live in profiles: ask who, then ask who they are. Somebody who
    /// has signed up and never chosen a display name has no profile row at all,
    /// so they come back as an id with no name; the screen says so rather than
    /// inventing one. Two of the three accounts on this database are in exactly
    /// that state today.
    public func followerIds(of userId: String, token: String?) async -> [String] {
        await ids("follows?select=follower&followee=eq.\(userId)&limit=200", key: "follower", token: token)
    }

    public func followingIds(of userId: String, token: String?) async -> [String] {
        await ids("follows?select=followee&follower=eq.\(userId)&limit=200", key: "followee", token: token)
    }

    private func ids(_ path: String, key: String, token: String?) async -> [String] {
        guard let data = try? await send(request(path, "GET", token: token)) else { return [] }
        guard let rows = try? JSONSerialization.jsonObject(with: data) as? [[String: Any]] else { return [] }
        return rows.compactMap { $0[key] as? String }
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

    /// Your country, or nil for "Don't show", which is remembered so the
    /// default never returns. Its own call, like units, so it never rewrites a
    /// name and a picture. Returns whether the server took it.
    public func saveCountry(_ code: String?, userId: String, token: String) async -> Bool {
        struct Row: Encodable { let user_id: String; let country: String?; let flag_hidden: Bool }
        struct Plain: Encodable { let user_id: String; let country: String? }
        let body = try? JSONEncoder().encode([Row(user_id: userId, country: code, flag_hidden: code == nil)])
        var ok = (try? await send(request("profiles?on_conflict=user_id", "POST", token: token,
                                          body: body, prefer: "resolution=merge-duplicates"))) != nil
        if !ok {
            // A database without flag_hidden yet: the country alone.
            let plain = try? JSONEncoder().encode([Plain(user_id: userId, country: code)])
            ok = (try? await send(request("profiles?on_conflict=user_id", "POST", token: token,
                                          body: plain, prefer: "resolution=merge-duplicates"))) != nil
        }
        if ok { myCountry = code; myFlagHidden = code == nil }
        return ok
    }

    /// Where the phone says you are: Settings, General, Language & Region.
    public static func countryGuess() -> String? {
        guard let code = Locale.current.region?.identifier, code.count == 2,
              Locale.Region.isoRegions.contains(where: { $0.identifier == code }) else { return nil }
        return code
    }

    /// The Public profile switch: `on` makes the
    /// profile public. Returns whether the server took it.
    public func savePublic(_ on: Bool, userId: String, token: String) async -> Bool {
        let body = try? JSONEncoder().encode(["public": on])
        let ok = (try? await send(request("profiles?user_id=eq.\(userId)", "PATCH", token: token,
                                          body: body, prefer: "return=minimal"))) != nil
        if ok { myPublic = on }
        return ok
    }

    /// Somebody's public profile, or nil when it is private, unknown, or the
    /// server cannot say. All three read the same on screen.
    public func publicProfile(_ userId: String, token: String?) async -> PublicProfile? {
        if let demo = DemoPeople.publicProfile(userId) { return demo }
        guard let data = try? await send(request("rpc/public_profile", "POST", token: token,
                                                 body: try? JSONEncoder().encode(["uid": userId])))
        else { return nil }
        return try? JSONDecoder().decode(PublicProfile.self, from: data)
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
