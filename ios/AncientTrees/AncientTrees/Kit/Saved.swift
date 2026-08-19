// The collection, and why it is lists rather than badges to begin with.
//
// The two references disagree about what collecting IS. Google Maps keeps
// lists: user-named, infinite, useful from the first save. AllTrails awards
// badges: a closed designed set that only pays off when it is completed. Hidde's
// own Google Maps holds 158 favourites, 257 starred and 279 in "want to go", and
// he collects no badges anywhere, so lists come first and badges arrive when
// there are enough trees for a set to be worth closing.
//
// Storage is UserDefaults on purpose for now. The website's own history is the
// argument: a passport in LocalStorage that Safari wipes after seven days was
// the failure that made accounts necessary. On iOS UserDefaults is not wiped, so
// this is safe locally, and the cloud sync that already exists for the website
// (Supabase, saves table) is the next step rather than a rewrite.

import Foundation
import Observation

@Observable
public final class Saved {
    public struct Entry: Codable, Hashable, Sendable {
        public let treeId: String
        public let visitedAt: Date?      // nil means saved but not yet stood in front of
        public let savedAt: Date
    }

    private let key = "saved.entries.v1"
    public private(set) var entries: [String: Entry] = [:]

    public init() { load() }

    public func isSaved(_ id: String) -> Bool { entries[id] != nil }
    public func isVisited(_ id: String) -> Bool { entries[id]?.visitedAt != nil }

    public var savedCount: Int { entries.count }
    public var visitedCount: Int { entries.values.filter { $0.visitedAt != nil }.count }

    public func toggleSaved(_ id: String) {
        if entries[id] != nil { entries[id] = nil }
        else { entries[id] = Entry(treeId: id, visitedAt: nil, savedAt: Date()) }
        persist()
    }

    /// Ticking a tree off is the point of the whole verb, so it also saves it:
    /// nobody should have to save a tree before they are allowed to say they
    /// stood in front of it.
    public func toggleVisited(_ id: String) {
        let existing = entries[id]
        if existing?.visitedAt != nil {
            entries[id] = Entry(treeId: id, visitedAt: nil, savedAt: existing?.savedAt ?? Date())
        } else {
            entries[id] = Entry(treeId: id, visitedAt: Date(), savedAt: existing?.savedAt ?? Date())
        }
        persist()
    }

    private func persist() {
        if let d = try? JSONEncoder().encode(Array(entries.values)) {
            UserDefaults.standard.set(d, forKey: key)
        }
    }

    private func load() {
        guard let d = UserDefaults.standard.data(forKey: key),
              let list = try? JSONDecoder().decode([Entry].self, from: d) else { return }
        entries = Dictionary(list.map { ($0.treeId, $0) }, uniquingKeysWith: { a, _ in a })
    }
}
