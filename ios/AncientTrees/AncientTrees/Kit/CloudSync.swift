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
//
// WHAT `saves` MEANS, corrected 2026-09-18, because this file had been writing
// the wrong thing into it since the cloud half shipped. `saves` is the HEART
// and nothing else, which is what the table was designed for and what the
// website has always read it as. This file pushed every entry into it instead,
// ticked-only trees included, on the reasonable-sounding ground that a
// collection should survive a new phone. `visited` exists now and carries that
// half, so the shortcut has no argument left and it had a real cost: the two
// lanes are independent lists (Hidde, 2026-08-26) and the website drew them
// from these two tables, so Favourites came back as a superset of My trees and
// the two lists read as one (Hidde, 2026-09-18: "dat kan niet kloppen").
//
// So, in one line each: a heart goes to `saves` and only a heart, a tick goes
// to `visited` and only a tick, and taking a heart off a tree you have
// collected deletes its `saves` row while the visit stays. Saved.strayHearts
// carries the one-off repair of what the old rule left behind.

import Foundation

public enum CloudSync {
    /// Called once when a session appears: pull what the account holds, fold it
    /// into what this phone holds, then push the union back.
    @discardableResult
    public static func merge(account: Account, saved: Saved) async -> Int {
        guard let s = await account.freshSession() else { return 0 }

        // BEFORE the pull, never after: once a stray row has been read back as
        // a heart there is nothing left that knows it was not one.
        await repairStrayHearts(session: s, saved: saved)

        let remoteSaves = await Supa.rows("/rest/v1/saves?select=tree_id,created_at", token: s.accessToken)
        let remoteVisited = await Supa.rows("/rest/v1/visited?select=tree_id,visited_at", token: s.accessToken)

        var pulled = 0
        for row in remoteSaves {
            guard let id = row["tree_id"] as? String else { continue }
            if saved.entries[id] == nil { pulled += 1 }
            // Adopted even when this phone already holds the tree, because the
            // heart is the fact the row carries: somebody who hearts a tree on
            // the website must find it hearted here, and without this the next
            // push would delete a save the person had just made. Skipped when
            // the heart is already on, so a pull is not a few hundred writes
            // of a collection that has not changed.
            guard saved.entries[id]?.favourite != true else { continue }
            saved.adopt(treeId: id, visitedAt: nil,
                        savedAt: date(row["created_at"]) ?? Date(),
                        favourite: true)
        }
        for row in remoteVisited {
            guard let id = row["tree_id"] as? String else { continue }
            let when = date(row["visited_at"]) ?? Date()
            if saved.entries[id]?.visitedAt == nil {
                // favourite stays nil: a visit says nothing about the heart,
                // and a tree that arrives only from this table is not one.
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

        // HEARTS ONLY. This line used to map every entry, which is what filled
        // the website's Favourites list with trees nobody had hearted.
        let saveRows = entries.filter(\.favourite).map { ["user_id": s.userId, "tree_id": $0.treeId] }
        if !saveRows.isEmpty {
            await Supa.post("/rest/v1/saves?on_conflict=user_id,tree_id", token: s.accessToken, body: saveRows)
        }

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
        if entry.favourite {
            await Supa.post("/rest/v1/saves?on_conflict=user_id,tree_id", token: s.accessToken,
                       body: [["user_id": s.userId, "tree_id": treeId]])
        } else {
            // The heart came off a tree that is still collected: the row goes
            // from saves and the visit below stays, which is exactly what
            // toggleSaved does locally.
            await Supa.delete("/rest/v1/saves?tree_id=eq.\(treeId)", token: s.accessToken)
        }
        if let v = entry.visitedAt {
            await Supa.post("/rest/v1/visited?on_conflict=user_id,tree_id", token: s.accessToken,
                       body: [["user_id": s.userId, "tree_id": treeId, "visited_at": day(v)]])
        } else {
            await Supa.delete("/rest/v1/visited?tree_id=eq.\(treeId)", token: s.accessToken)
        }
    }

    /// Delete the `saves` rows the old push rule created, once per phone.
    /// See Saved.strayHearts for why this phone is the only place that can
    /// still tell one from a real heart, and what it costs.
    private static func repairStrayHearts(session s: Session, saved: Saved) async {
        guard !saved.savesRepaired else { return }
        // Nothing local to judge from, so judge nothing and keep the chance:
        // signing out empties this phone, and burning the flag on an empty
        // store would spend the repair on a collection it cannot see.
        guard !saved.entries.isEmpty else { return }
        let strays = saved.strayHearts.map(\.treeId)
        if !strays.isEmpty {
            // One request rather than one per tree: this runs at launch, and a
            // person with a hundred ticked trees should not pay a hundred
            // round trips for a repair they will never see.
            let list = strays.joined(separator: ",")
            await Supa.delete("/rest/v1/saves?tree_id=in.(\(list))", token: s.accessToken)
        }
        saved.savesRepaired = true
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
