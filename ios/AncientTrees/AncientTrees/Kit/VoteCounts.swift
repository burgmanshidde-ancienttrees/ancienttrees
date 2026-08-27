// How many people said a tree was worth the visit, and how many said it was not.
//
// Hidde, 2026-08-27: "1 person keeps this tree is een hele rare zin, zet gewoon
// bij thumb hoeveel mensen thumb up of down hebben gedaan verder niet." A
// number beside each thumb, and nothing else: no sentence about it, and no
// number anywhere the thumbs are not.
//
// It cannot be counted on the phone, for a harder reason than saves. The
// submissions table has no select policy at all, so a vote is write-only from
// the client: this app has never been able to read back even its own. And the
// arithmetic is not a count of rows either. Undoing a vote writes a
// compensating "vote undone" row rather than deleting anything, so one person
// tapping up, down, up on one tree leaves three rows and one opinion. Only the
// last word counts, which is what supabase/vote-counts.sql works out.
//
// UNTIL THAT SQL IS RUN the call 404s, this holds nothing, and no number
// appears. The same honest-empty rule SaveCounts follows: a number we cannot
// stand behind is not shown.

import Foundation
import Observation

@MainActor
@Observable
public final class VoteCounts {
    public struct Tally: Sendable, Equatable {
        public var up: Int
        public var down: Int
    }

    private(set) var byTree: [String: Tally] = [:]
    private var loaded = false

    public init() {}

    /// One call for the whole catalogue, like SaveCounts and for the same
    /// reason: a request per tree page is a round trip somebody waits for.
    public func loadOnce() async {
        guard !loaded else { return }
        loaded = true
        var req = URLRequest(url: Submission.url
            .deletingLastPathComponent()
            .appendingPathComponent("rpc/tree_vote_counts"))
        req.httpMethod = "POST"
        req.setValue(Submission.key, forHTTPHeaderField: "apikey")
        req.setValue("Bearer \(Submission.key)", forHTTPHeaderField: "Authorization")
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        req.httpBody = Data("{}".utf8)
        struct Row: Decodable { let tree_id: String; let up: Int; let down: Int }
        do {
            let (data, response) = try await Net.data(for: req)
            guard (response as? HTTPURLResponse)?.statusCode == 200 else { return }
            let rows = try JSONDecoder().decode([Row].self, from: data)
            byTree = Dictionary(rows.map { ($0.tree_id, Tally(up: $0.up, down: $0.down)) },
                                uniquingKeysWith: { a, _ in a })
        } catch {
            // No network, or the function does not exist yet. Both mean the
            // same thing on screen: no number.
        }
    }

    /// nil rather than zero, so nothing renders "0" beside a thumb. A tree
    /// nobody has voted on says nothing about itself, which is the rule Hidde
    /// set for the save count on 2026-08-26 ("pas van 1 tellen") and it reads
    /// the same way here: a lone 0 under a tree we chose to publish is worse
    /// than no number at all.
    public func up(_ treeId: String) -> Int? { positive(byTree[treeId]?.up) }
    public func down(_ treeId: String) -> Int? { positive(byTree[treeId]?.down) }

    private func positive(_ n: Int?) -> Int? {
        guard let n, n >= 1 else { return nil }
        return n
    }

    /// Move the number the moment somebody taps, rather than on the next
    /// launch. A thumb that fills in while the count beside it stays at three
    /// reads as a control that did nothing, and the server will agree with this
    /// within the second: the vote is already on its way.
    ///
    /// Takes the vote it is replacing, because that is what the control does:
    /// tapping down while up is set removes an up and adds a down in one act.
    public func record(_ treeId: String, from old: String, to new: String) {
        var t = byTree[treeId] ?? Tally(up: 0, down: 0)
        if old == "up" { t.up = max(0, t.up - 1) }
        if old == "down" { t.down = max(0, t.down - 1) }
        if new == "up" { t.up += 1 }
        if new == "down" { t.down += 1 }
        byTree[treeId] = t
    }
}
