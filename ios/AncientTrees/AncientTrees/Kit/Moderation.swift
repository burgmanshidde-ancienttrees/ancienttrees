// Reporting somebody, and blocking them.
//
// The moment one person can see a name and a photograph another person chose,
// this stops being optional. App Store guideline 1.2 asks for a way to report
// content, a way to block a user, published contact details and terms nobody
// can miss, and the review team checks the first two by tapping. Hidde ruled
// the social half into 1.0 on 2026-08-27 ("sociale deel gaat mee") and answered
// the objection in the same breath: "maak gewoon die melden optie, zo moeilijk
// is het niet toch". It is not hard. It is just required.
//
// The schema is supabase/reports.sql. Until it is run, every call here fails
// quietly and the controls still work as far as the person can see, minus the
// part that needs a server: blocking still hides somebody on this phone. That
// is the same honest-empty rule Profiles follows, and it means the app can ship
// ahead of the database.
//
// WHY A BLOCK IS BOTH PLACES. On the server so it survives a reinstall, follows
// you to a second phone, and can break the follow rows in both directions; in
// UserDefaults so it applies the instant you tap it and holds on a launch with
// no network. The server is the truth and the local copy is the echo, so a
// reinstall reads the server and catches up.

import Foundation
import Observation

@MainActor
@Observable
public final class Moderation {

    /// Everybody this account has blocked, by user id.
    public private(set) var blocked: Set<String> = []

    private static let key = "blocked-accounts"

    public init() {
        let args = ProcessInfo.processInfo.arguments
        // Test scaffolding, the same family as -reset-collection. Without it a
        // block made by one test survives into every test after it on the same
        // simulator, which is how a flow walk photographed a person missing
        // from a list for no reason anybody could see (2026-08-27).
        if args.contains("-reset-blocks") {
            UserDefaults.standard.removeObject(forKey: Self.key)
        }
        blocked = Set(UserDefaults.standard.stringArray(forKey: Self.key) ?? [])
        // One already blocked, so the unblock can be photographed: it only
        // appears on somebody you have blocked, and nothing on a simulator has.
        if args.contains("-blocked-demo") {
            blocked.insert(DemoPeople.all[0].user_id)
        }
    }

    /// Whether somebody's name, picture and rows should be kept off this screen.
    public func hides(_ userId: String) -> Bool { blocked.contains(userId) }

    // MARK: - the two acts

    /// Send a report. Insert-only by policy: nothing reads these back through
    /// the app, not even your own, because a queue the reported person can read
    /// is a way to find out who reported them.
    public func report(subject: String, reason: String,
                       reporter: String, token: String) async -> Bool {
        struct Row: Encodable { let reporter: String; let subject: String; let reason: String }
        let body = try? JSONEncoder().encode([Row(reporter: reporter,
                                                  subject: subject,
                                                  reason: reason)])
        return await post("reports", body: body, token: token)
    }

    /// Block somebody. The local set moves first, so the list they were in
    /// redraws under the finger rather than after a round trip.
    public func block(_ userId: String, me: String, token: String?) async {
        blocked.insert(userId)
        persist()
        guard let token else { return }
        struct Row: Encodable { let blocker: String; let blocked: String }
        let body = try? JSONEncoder().encode([Row(blocker: me, blocked: userId)])
        _ = await post("blocks?on_conflict=blocker,blocked", body: body, token: token,
                       prefer: "resolution=merge-duplicates")
    }

    public func unblock(_ userId: String, me: String, token: String?) async {
        blocked.remove(userId)
        persist()
        guard let token else { return }
        _ = await post("blocks?blocker=eq.\(me)&blocked=eq.\(userId)",
                       body: nil, token: token, method: "DELETE")
    }

    /// Read the server's list at sign-in, so a new phone starts where the last
    /// one left off. The local set is replaced rather than merged: an unblock
    /// on the other phone has to be able to travel too.
    public func load(me: String?, token: String?) async {
        guard let me, let token else { return }
        struct Row: Decodable { let blocked: String }
        // See Profiles.request: appending a path component encodes the "?" and
        // the whole query becomes part of the table name.
        var r = URLRequest(url: URL(string: Submission.url.deletingLastPathComponent()
            .absoluteString + "blocks?select=blocked&blocker=eq.\(me)")!)
        r.setValue(Submission.key, forHTTPHeaderField: "apikey")
        r.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        guard let (data, resp) = try? await Net.data(for: r),
              let http = resp as? HTTPURLResponse, (200..<300).contains(http.statusCode),
              let rows = try? JSONDecoder().decode([Row].self, from: data) else { return }
        blocked = Set(rows.map(\.blocked))
        persist()
    }

    // MARK: - plumbing

    private func persist() {
        UserDefaults.standard.set(Array(blocked), forKey: Self.key)
    }

    private func post(_ path: String, body: Data?, token: String,
                      method: String = "POST", prefer: String? = nil) async -> Bool {
        var r = URLRequest(url: URL(string: Submission.url.deletingLastPathComponent()
            .absoluteString + path)!)
        r.httpMethod = method
        r.setValue(Submission.key, forHTTPHeaderField: "apikey")
        r.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        r.setValue("application/json", forHTTPHeaderField: "Content-Type")
        r.setValue(prefer ?? "return=minimal", forHTTPHeaderField: "Prefer")
        r.httpBody = body
        guard let (_, resp) = try? await Net.data(for: r),
              let http = resp as? HTTPURLResponse else { return false }
        return (200..<300).contains(http.statusCode)
    }

    /// The reasons somebody picks from. Short, concrete and in the order a
    /// person meets them: what is actually wrong with a name or a picture,
    /// then the catch-all. Apple's own report sheets read the same way.
    public enum Reason: String, CaseIterable, Identifiable, Sendable {
        case offensive = "An offensive name or picture"
        case impersonation = "Pretending to be somebody else"
        case spam = "Spam or advertising"
        case other = "Something else"
        public var id: String { rawValue }
    }
}
