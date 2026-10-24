// NOTES FROM VISITORS on a tree page (2026-10-24; CONVENTIONS.md, "Notes from
// visitors on a tree page"). The web's tree-notes-js.ts, in Swift: one note
// per person per tree, dated, no replies, no likes, live for everyone the
// moment it is written (Hidde: "zet gewoon live en we kunnen altijd
// wegmodereren later"); the night run reads it afterwards (scripts/tree_notes.py).
// Table and function: supabase/tree-notes.sql.
//
// Reads every note on this tree AND its nearest neighbours in one call
// (tree_notes_for, anon-readable; a name and picture only from a public
// profile), so an empty block can borrow the nearest tree's real note as its
// example (Airbnb's "this host has N reviews"). Signed in, reads your own row
// too (RLS: own rows only), so your note shows as "Your note" whatever your
// profile's setting, and the sheet reopens prefilled to edit it.
//
// If the table is not there yet (the SQL waits for Hidde's paste) the function
// answers 404 and `gone` hides the section rather than show a broken block.
import Foundation
import Observation

@Observable
@MainActor
public final class TreeNotes {
    public struct Note: Decodable, Hashable, Identifiable, Sendable {
        public let tree_id: String
        public let body: String
        public let created_at: String
        public let author_name: String?
        public let author_avatar: String?
        public var id: String { tree_id + "|" + created_at + "|" + String(body.prefix(24)) }
        public var date: Date { TreeNotes.date(created_at) }
    }
    public struct Mine: Decodable, Hashable, Sendable {
        public let body: String
        public let created_at: String
        public var date: Date { TreeNotes.date(created_at) }
    }

    public private(set) var all: [Note] = []
    public private(set) var mine: Mine?
    /// The function is not on the server yet: draw nothing.
    public private(set) var gone = false
    public private(set) var loaded = false

    public init() {}

    static func date(_ iso: String) -> Date {
        let f = ISO8601DateFormatter()
        f.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
        if let d = f.date(from: iso) { return d }
        f.formatOptions = [.withInternetDateTime]
        return f.date(from: iso) ?? Date()
    }

    /// Every note on this tree, newest first, your own taken out (it is drawn
    /// separately as "Your note").
    public func here(_ tree: String) -> [Note] {
        all.filter { $0.tree_id == tree && !isMine($0) }
    }

    public func isMine(_ n: Note) -> Bool {
        guard let m = mine else { return false }
        return abs(n.date.timeIntervalSince(m.date)) < 2
    }

    /// The nearest neighbour's newest note, when this tree has none.
    public func borrowed(near ids: [String]) -> Note? {
        for id in ids {
            if let n = all.first(where: { $0.tree_id == id }) { return n }
        }
        return nil
    }

    public func load(tree: String, near: [String], token: String?) async {
        // Debug scaffolding for the sweep and for looking at the block before
        // the table exists: -notesdemo (two notes here), -notesdemo=borrowed
        // (none here, one on the nearest tree), -notesdemo=none (nothing).
        if let arg = ProcessInfo.processInfo.arguments.first(where: { $0.hasPrefix("-notesdemo") }) {
            let mode = arg.contains("=") ? String(arg.split(separator: "=").last ?? "here") : "here"
            let iso = ISO8601DateFormatter().string(from: Date().addingTimeInterval(-86400 * 12))
            all = []
            if mode == "here" {
                all = [Note(tree_id: tree, body: "Full gold this week. Stand on the north side around four, the sun comes through the leaves.", created_at: iso, author_name: "Rita M.", author_avatar: nil),
                       Note(tree_id: tree, body: "My grandfather used to bring me here on Sundays. It was already big then.", created_at: iso, author_name: nil, author_avatar: nil)]
            } else if mode == "borrowed", let n = near.first {
                all = [Note(tree_id: n, body: "I spent whole afternoons under this tree with my grandparents when I was small. It still smells the same.", created_at: iso, author_name: nil, author_avatar: nil)]
            }
            mine = nil; gone = false; loaded = true
            return
        }
        let ids = [tree] + near
        let r = Supa.request("/rest/v1/rpc/tree_notes_for", body: ["ids": ids])
        if let (data, resp) = try? await Net.data(for: r), let http = resp as? HTTPURLResponse {
            if http.statusCode == 404 { gone = true }
            else if (200..<300).contains(http.statusCode),
                    let rows = try? JSONDecoder().decode([Note].self, from: data) {
                all = rows
            }
        }
        if let token {
            let rows = await Supa.rows("/rest/v1/tree_notes?select=body,created_at&tree_id=eq.\(tree)", token: token)
            if let first = rows.first, let body = first["body"] as? String,
               let created = first["created_at"] as? String {
                mine = Mine(body: body, created_at: created)
            } else {
                mine = nil
            }
        } else {
            mine = nil
        }
        loaded = true
    }

    /// Writes or rewrites your one note on this tree. Returns whether it landed.
    public func save(tree: String, body: String, token: String) async -> Bool {
        let now = ISO8601DateFormatter().string(from: Date())
        let ok = await Supa.post("/rest/v1/tree_notes?on_conflict=user_id,tree_id", token: token,
                                 body: ["tree_id": tree, "body": body, "updated_at": now])
        if ok { mine = Mine(body: body, created_at: mine?.created_at ?? now) }
        return ok
    }

    public func delete(tree: String, token: String) async -> Bool {
        let ok = await Supa.delete("/rest/v1/tree_notes?tree_id=eq.\(tree)", token: token)
        if ok {
            if let m = mine { all.removeAll { abs($0.date.timeIntervalSince(m.date)) < 2 && $0.tree_id == tree } }
            mine = nil
        }
        return ok
    }
}
