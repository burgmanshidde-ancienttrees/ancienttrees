// RECENT SEARCHES under the empty search field (Hidde, 2026-11-04: "i like all
// your proposals please build", design section 2 of drafts/design-2026-11-04).
// Google Maps, Instagram and Apple Maps all list recent picks under an empty
// field, a cross per row and a way to clear them all, tied to the account.
//
// Only what a person PICKED is recorded (a city, country, species, tree or a
// real town), never half-typed text. Signed in only, and on the server only:
// table recent_searches (supabase/recent-searches.sql), the website reads the
// same rows. Nothing is kept on the phone beyond this screen's memory (hard
// rule 11), so signed out the section simply is not there.
//
// If the table is not there yet (the SQL waits for Hidde's paste) PostgREST
// answers 404 (or 400): `rows` stays empty and no section is drawn, the way
// TreeNotes handles a missing function.
import Foundation
import Observation

@Observable
@MainActor
public final class RecentSearches {
    public struct Entry: Hashable, Identifiable, Sendable {
        /// city | country | species | tree | place
        public let kind: String
        /// city slug, country name, species common name, tree id, or
        /// "lat,lng" for a real town (four decimals, as the website writes it).
        public let ref: String
        public let label: String
        public let sub: String
        public var id: String { kind + "|" + ref }
    }

    /// At most five, newest first, none older than 90 days.
    public private(set) var rows: [Entry] = []

    public static let limit = 5
    public static let days = 90

    public init() {}

    public func load(token: String?) async {
        guard let token, !token.isEmpty else { rows = []; return }
        let since = ISO8601DateFormatter().string(from: Date().addingTimeInterval(-86400 * Double(Self.days)))
        let path = "/rest/v1/recent_searches?select=kind,key,label,sub"
            + "&searched_at=gte.\(since)&order=searched_at.desc&limit=\(Self.limit)"
        let got = await Supa.rows(path, token: token)
        rows = got.compactMap { r in
            guard let k = r["kind"] as? String, let ref = r["key"] as? String else { return nil }
            return Entry(kind: k, ref: ref, label: r["label"] as? String ?? "", sub: r["sub"] as? String ?? "")
        }
    }

    /// The `-recentdemo` launch argument: rows to screenshot the section with,
    /// supplied by the screen because only it knows what the catalogue holds.
    public func demo(_ entries: [Entry]) { rows = Array(entries.prefix(Self.limit)) }

    /// A pick: to the top here at once, then upserted with searched_at = now.
    public func record(_ e: Entry, token: String?) async {
        rows.removeAll { $0.id == e.id }
        rows.insert(e, at: 0)
        if rows.count > Self.limit { rows.removeLast(rows.count - Self.limit) }
        guard let token, !token.isEmpty else { return }
        let now = ISO8601DateFormatter().string(from: Date())
        await Supa.post("/rest/v1/recent_searches?on_conflict=user_id,kind,key", token: token,
                        body: ["kind": e.kind, "key": e.ref, "label": e.label, "sub": e.sub,
                               "searched_at": now])
    }

    public func remove(_ e: Entry, token: String?) async {
        rows.removeAll { $0.id == e.id }
        guard let token, !token.isEmpty else { return }
        let k = Self.encode(e.kind), r = Self.encode(e.ref)
        await Supa.delete("/rest/v1/recent_searches?kind=eq.\(k)&key=eq.\(r)", token: token)
    }

    public func clear(token: String?) async {
        rows = []
        guard let token, !token.isEmpty else { return }
        // RLS limits the delete to this person's own rows; PostgREST refuses a
        // DELETE with no filter at all, so the filter is one every row meets.
        await Supa.delete("/rest/v1/recent_searches?kind=not.is.null", token: token)
    }

    private static func encode(_ s: String) -> String {
        var allowed = CharacterSet.urlQueryAllowed
        allowed.remove(charactersIn: "&=+?#,")
        return s.addingPercentEncoding(withAllowedCharacters: allowed) ?? s
    }
}
