// The early-adopter badge: every account opened before the paid tier goes live.
//
// Hidde, 2026-10-16: "Build it like this on web and app, with the one-time
// sheet. Cutoff: the day the paid tier goes live." The website's twin is
// site/src/lib/early-adopter.ts and profile-js.ts; the rule is written once,
// there, and travels to the app as data: /api/version.json carries
// early_adopter_until (null while the window is open).
//
// WHO HAS IT is two facts from the server and none from the phone (hard rule
// 11): the account's created_at, as /auth/v1/user returns it, and the cutoff
// in the feed. The one-time sheet is remembered on the ACCOUNT, in the auth
// user's own metadata (early_adopter_seen), the same flag the website writes,
// so whichever surface shows it first, the other one does not repeat it.
import Foundation

public enum EarlyAdopter {
    public struct Status: Sendable, Equatable {
        public var hasBadge: Bool
        public var seenSheet: Bool
    }

    /// Nil when the server could not be asked: then the badge stays off
    /// rather than guessing, and the sheet never opens on a guess.
    public static func status(token: String) async -> Status? {
        async let user = whoAmI(token: token)
        async let cutoff = feedCutoff()
        guard let u = await user, let created = u.createdAt else { return nil }
        let until = await cutoff
        // ISO dates compare as strings: "2026-08-14T10:02:11Z" < "2027-03-01".
        let has: Bool
        switch until {
        case .none: return nil
        case .some(.none): has = true
        case .some(.some(let day)): has = created < day
        }
        return Status(hasBadge: has, seenSheet: u.seen)
    }

    /// Closing the sheet, from either surface, writes this once. Best effort:
    /// a failure only means the sheet may show once more.
    public static func markSeen(token: String) async {
        let r = Supa.request("/auth/v1/user", method: "PUT", token: token,
                             body: ["data": ["early_adopter_seen": true]])
        _ = try? await Net.data(for: r)
    }

    private static func whoAmI(token: String) async -> (createdAt: String?, seen: Bool)? {
        let r = Supa.request("/auth/v1/user", method: "GET", token: token)
        guard let (data, resp) = try? await Net.data(for: r),
              let http = resp as? HTTPURLResponse, (200..<300).contains(http.statusCode),
              let j = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return nil }
        let md = j["user_metadata"] as? [String: Any]
        return (j["created_at"] as? String, (md?["early_adopter_seen"] as? Bool) ?? false)
    }

    /// .some(nil) is "the window is open", .some(day) is a cutoff, nil is
    /// "the feed could not be read".
    private static func feedCutoff() async -> String?? {
        guard let (data, _) = try? await Net.data(from: Feed.version),
              let j = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return nil }
        // A feed from before 2026-10-16 has no key at all: treat it as open,
        // which is what the website says for the same moment.
        return .some(j["early_adopter_until"] as? String)
    }
}
