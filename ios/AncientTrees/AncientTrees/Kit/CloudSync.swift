// The collection's cloud half: the same two tables the website writes to.
//
// supabase/saves.sql and supabase/visited.sql already exist, are already
// row-level-secured per user, and already cascade off auth.users so deleting an
// account really does take the collection with it. Nothing new is stored here
// and no new column is added, which matters because a new column holding
// personal data needs Hidde's yes (DECISIONS.md 2026-08-14).
//
// One caveat, measured against the live database on 2026-08-20 rather than
// assumed: public.saves exists and public.visited DOES NOT. visited.sql was
// written on 2026-08-18 and never pasted into the Supabase dashboard, which only
// Hidde can do. So until he runs it, every write to visited returns a 404 and is
// swallowed here. Nothing is lost by that: pushAll writes every entry to saves
// including the ticked ones, so a collection still survives a new phone, and the
// day the table exists the visited dates start following too.
//
// The merge rule is UNION, and only on the way in. When somebody signs in on a
// phone that already has six ticked trees, and their account already has four
// from the website, the answer is ten. Anything else silently destroys work
// somebody did, and a collection that eats your entries is worse than no
// collection. Deletes are only ever sent for a tree the person just untapped,
// never inferred from what is missing on one side.

import Foundation

public enum CloudSync {
    /// Called once when a session appears: pull what the account holds, fold it
    /// into what this phone holds, then push the union back.
    @discardableResult
    public static func merge(account: Account, saved: Saved) async -> Int {
        guard let s = await account.freshSession() else { return 0 }

        let remoteSaves = await Supa.rows("/rest/v1/saves?select=tree_id,created_at", token: s.accessToken)
        let remoteVisited = await Supa.rows("/rest/v1/visited?select=tree_id,visited_at", token: s.accessToken)

        var pulled = 0
        for row in remoteSaves {
            guard let id = row["tree_id"] as? String else { continue }
            if saved.entries[id] == nil {
                saved.adopt(treeId: id, visitedAt: nil,
                            savedAt: date(row["created_at"]) ?? Date())
                pulled += 1
            }
        }
        for row in remoteVisited {
            guard let id = row["tree_id"] as? String else { continue }
            let when = date(row["visited_at"]) ?? Date()
            if saved.entries[id]?.visitedAt == nil {
                saved.adopt(treeId: id, visitedAt: when,
                            savedAt: saved.entries[id]?.savedAt ?? when)
                pulled += 1
            }
        }

        await pushAll(account: account, saved: saved)
        return pulled
    }

    /// Upsert every local entry. Cheap at these sizes and it is the one call
    /// that makes a phone's existing collection survive a first sign-in.
    public static func pushAll(account: Account, saved: Saved) async {
        guard let s = await account.freshSession() else { return }
        let entries = Array(saved.entries.values)
        guard !entries.isEmpty else { return }

        let saveRows = entries.map { ["user_id": s.userId, "tree_id": $0.treeId] }
        await Supa.post("/rest/v1/saves?on_conflict=user_id,tree_id", token: s.accessToken, body: saveRows)

        let visitRows = entries.compactMap { e -> [String: Any]? in
            guard let v = e.visitedAt else { return nil }
            return ["user_id": s.userId, "tree_id": e.treeId, "visited_at": day(v)]
        }
        if !visitRows.isEmpty {
            await Supa.post("/rest/v1/visited?on_conflict=user_id,tree_id", token: s.accessToken, body: visitRows)
        }
    }

    /// One tree changed. Fire and forget: a failed write is retried by the next
    /// pushAll rather than shown to anybody, because the local copy is already
    /// correct and the person is standing under a tree.
    public static func push(account: Account, entry: Saved.Entry?, treeId: String) async {
        guard let s = await account.freshSession() else { return }
        guard let entry else {
            await Supa.delete("/rest/v1/saves?tree_id=eq.\(treeId)", token: s.accessToken)
            await Supa.delete("/rest/v1/visited?tree_id=eq.\(treeId)", token: s.accessToken)
            return
        }
        await Supa.post("/rest/v1/saves?on_conflict=user_id,tree_id", token: s.accessToken,
                   body: [["user_id": s.userId, "tree_id": treeId]])
        if let v = entry.visitedAt {
            await Supa.post("/rest/v1/visited?on_conflict=user_id,tree_id", token: s.accessToken,
                       body: [["user_id": s.userId, "tree_id": treeId, "visited_at": day(v)]])
        } else {
            await Supa.delete("/rest/v1/visited?tree_id=eq.\(treeId)", token: s.accessToken)
        }
    }

    // MARK: - plumbing

    // rows / post / delete live on Supa: they were identical here and in
    // SightingSync, and a second copy of "did it work" is a second answer
    // waiting to happen.

    private static let dayFormatter: DateFormatter = {
        let f = DateFormatter()
        f.dateFormat = "yyyy-MM-dd"
        f.timeZone = TimeZone(identifier: "UTC")
        f.locale = Locale(identifier: "en_US_POSIX")
        return f
    }()

    private static func day(_ d: Date) -> String { dayFormatter.string(from: d) }

    private static func date(_ any: Any?) -> Date? {
        guard let s = any as? String else { return nil }
        if let d = dayFormatter.date(from: String(s.prefix(10))) { return d }
        return ISO8601DateFormatter().date(from: s)
    }
}
