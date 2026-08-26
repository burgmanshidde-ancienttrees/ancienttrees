// How many people have saved a tree.
//
// Hidde, 2026-08-26: "aantal likes tellen en terug geven, pas van 1 tellen."
//
// It cannot be counted on the phone. The saves table is row-level-secured per
// user, so a client query returns that person's own rows and nothing else; a
// count from here would always read one or zero and be wrong in a way nobody
// would notice. So the server counts, through the function in
// supabase/like-counts.sql, which returns COUNTS ONLY and never a user id: the
// app learns that eleven people saved this tree and nothing about any of them.
//
// UNTIL HIDDE RUNS THAT SQL the call 404s, this returns nothing, and every
// count is simply absent. That is the same honest-empty rule the website's
// sponsor link follows: a number we cannot stand behind is not shown, and a
// tree with no saves has no number either, which is what "pas van 1 tellen"
// asks for.

import Foundation
import Observation

@MainActor
@Observable
public final class SaveCounts {
    public private(set) var counts: [String: Int] = [:]
    private var loaded = false

    public init() {}

    /// One call for the whole catalogue rather than one per tree. The result is
    /// a few thousand short rows at most, and a per-tree request would be a
    /// network round trip inside a scrolling list.
    public func loadOnce() async {
        guard !loaded else { return }
        loaded = true
        var req = URLRequest(url: Submission.url
            .deletingLastPathComponent()
            .appendingPathComponent("rpc/tree_save_counts"))
        req.httpMethod = "POST"
        req.setValue(Submission.key, forHTTPHeaderField: "apikey")
        req.setValue("Bearer \(Submission.key)", forHTTPHeaderField: "Authorization")
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        req.httpBody = Data("{}".utf8)
        struct Row: Decodable { let tree_id: String; let saves: Int }
        do {
            let (data, response) = try await URLSession.shared.data(for: req)
            guard (response as? HTTPURLResponse)?.statusCode == 200 else { return }
            let rows = try JSONDecoder().decode([Row].self, from: data)
            counts = Dictionary(rows.map { ($0.tree_id, $0.saves) },
                                uniquingKeysWith: { a, _ in a })
        } catch {
            // No network, or the function does not exist yet. Both mean the
            // same thing on screen: no number.
        }
    }

    /// nil rather than zero, so a caller cannot accidentally render "0 saves".
    public func count(_ treeId: String) -> Int? {
        guard let n = counts[treeId], n >= 1 else { return nil }
        return n
    }
}
