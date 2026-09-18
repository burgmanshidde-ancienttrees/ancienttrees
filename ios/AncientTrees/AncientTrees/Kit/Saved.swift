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

/// Main-actor isolated, like every store the root holds. See Account.swift for
/// why: SwiftUI already reads these from the main actor, so the annotation
/// costs nothing at runtime and makes a background write a compiler error
/// instead of a data race nobody can reproduce.
@MainActor
@Observable
public final class Saved {
    /// TWO LISTS THAT SHARE A ROW, never one list wearing two hats. Hidde,
    /// 2026-08-26: "je kunt niet bomen uit je collected halen door ze te
    /// ontfavorieten, die dingen zijn twee verschillende lijsten en hebben
    /// niks met elkaar te maken."
    ///
    /// He is describing a real bug rather than a preference. `toggleSaved`
    /// used to delete the whole row, so taking the heart off a tree you had
    /// photographed threw away the fact that you had stood in front of it,
    /// which is the one thing in this app that cannot be recovered by tapping
    /// again. Favouriting is a wish and collecting is a memory.
    ///
    /// So a row is a tree you have SOME relationship with, and it carries both
    /// independently: `favourite` for the heart, `visitedAt` for the standing
    /// in front of. A row with neither is deleted, because it means nothing.
    public struct Entry: Codable, Hashable, Sendable {
        public let treeId: String
        public let visitedAt: Date?      // nil means not yet stood in front of
        public let savedAt: Date
        public var favourite: Bool

        public init(treeId: String, visitedAt: Date?, savedAt: Date,
                    favourite: Bool) {
            self.treeId = treeId
            self.visitedAt = visitedAt
            self.savedAt = savedAt
            self.favourite = favourite
        }

        /// Rows written before `favourite` existed were all hearts by
        /// definition, since the only way to make one was to save it. Reading
        /// them as true keeps every collection anybody already has.
        public init(from decoder: Decoder) throws {
            let c = try decoder.container(keyedBy: CodingKeys.self)
            treeId = try c.decode(String.self, forKey: .treeId)
            visitedAt = try c.decodeIfPresent(Date.self, forKey: .visitedAt)
            savedAt = try c.decode(Date.self, forKey: .savedAt)
            favourite = try c.decodeIfPresent(Bool.self, forKey: .favourite) ?? true
        }
    }

    private let key = "saved.entries.v1"

    /// Where the collection is written. UserDefaults.standard everywhere in the
    /// app; a throwaway suite in a unit test, so a test about losing trees
    /// cannot lose the trees of the simulator it runs on, and two tests cannot
    /// read each other's collection.
    private let defaults: UserDefaults

    public private(set) var entries: [String: Entry] = [:]

    /// Called with every deliberate change so the cloud half can follow, set by
    /// ContentView because this type has no business knowing about an account.
    /// A nil entry means the tree was removed.
    public var onMutate: ((String, Entry?) -> Void)?

    public init(defaults: UserDefaults = .standard) {
        self.defaults = defaults
        load()
    }

    /// Take a row that came back from the account. Deliberately does NOT fire
    /// onMutate: this is the server telling us something, and echoing it
    /// straight back would be a write for no reason.
    ///
    /// `favourite` says which list the row arrived from, and until 2026-09-18
    /// it could not be said at all: every adopted row became a favourite,
    /// because the only table that existed when this was written was `saves`.
    /// A row from `saves` IS a heart and passes true; a row from `visited` is
    /// a tree somebody stood in front of and passes nil, which keeps whatever
    /// this phone already knew and makes a brand new row a plain visit. Pass
    /// nil rather than false to leave the heart alone.
    public func adopt(treeId: String, visitedAt: Date?, savedAt: Date,
                      favourite: Bool? = nil) {
        let existing = entries[treeId]
        entries[treeId] = Entry(treeId: treeId,
                                visitedAt: visitedAt ?? existing?.visitedAt,
                                savedAt: min(savedAt, existing?.savedAt ?? savedAt),
                                favourite: favourite ?? existing?.favourite ?? false)
        persist()
    }

    public func isSaved(_ id: String) -> Bool { entries[id]?.favourite == true }
    public func isVisited(_ id: String) -> Bool { entries[id]?.visitedAt != nil }

    /// Debug scaffolding, same family as -tab and -select: mark trees as
    /// collected at launch so the collected PIN can be photographed. simctl
    /// cannot tap, and a pin state that only exists after a tap is a pin state
    /// that ships unlooked at.
    public func seedFromLaunchArguments() {
        guard let arg = ProcessInfo.processInfo.arguments
            .first(where: { $0.hasPrefix("-collected=") }) else { return }
        let now = Date()
        for id in arg.dropFirst(11).split(separator: ",") {
            adopt(treeId: String(id), visitedAt: now, savedAt: now)
        }
    }


    public var savedCount: Int { entries.values.filter { $0.favourite }.count }
    public var visitedCount: Int { entries.values.filter { $0.visitedAt != nil }.count }

    /// The two lists, each in the order somebody would expect to read it:
    /// newest first, because the last thing you did is the thing you are
    /// looking for.
    public var favourites: [Entry] {
        entries.values.filter { $0.favourite }.sorted { $0.savedAt > $1.savedAt }
    }
    public var collected: [Entry] {
        entries.values.filter { $0.visitedAt != nil }
            .sorted { ($0.visitedAt ?? .distantPast) > ($1.visitedAt ?? .distantPast) }
    }

    /// THE ONE-OFF REPAIR of 2026-09-18, and the only place the truth about it
    /// still exists. CloudSync used to push EVERY entry to `saves`, ticked
    /// ones included, so that table stopped meaning "hearted" and started
    /// meaning "in your collection at all". The website reads it for the
    /// Favourites list, so Favourites became a superset of My trees and the
    /// two lanes showed one list twice (Hidde, 2026-09-18: "als ik klik op My
    /// Trees op Favorites, dan krijg ik dezelfde lijst").
    ///
    /// A stray row cannot be told from a real heart in the database, because
    /// `saves` carries no flag saying which it was. It CAN be told apart here:
    /// this phone recorded every tap, so an entry it holds with the heart off
    /// and a visit on is exactly the row that should never have been pushed.
    /// Those rows are deleted once, before the first pull of the fixed
    /// version, and the flag below makes sure it happens once and never again.
    ///
    /// The honest cost, written down rather than glossed: a tree hearted on
    /// the WEBSITE that this phone happens to hold as ticked-only is deleted
    /// with them. That is one tap to put back and it is bounded to this one
    /// migration, against a Favourites list that is otherwise wrong forever.
    public var strayHearts: [Entry] {
        entries.values.filter { !$0.favourite && $0.visitedAt != nil }
    }

    private let repairKey = "saved.saves_are_hearts_v1"

    public var savesRepaired: Bool {
        get { defaults.bool(forKey: repairKey) }
        set { defaults.set(newValue, forKey: repairKey) }
    }

    /// The heart, and ONLY the heart. Taking it off a tree you have collected
    /// leaves the collection alone; the row only goes when nothing is left in
    /// it to keep.
    public func toggleSaved(_ id: String) {
        if let e = entries[id] {
            if e.favourite && e.visitedAt == nil {
                entries[id] = nil
            } else {
                entries[id] = Entry(treeId: id, visitedAt: e.visitedAt,
                                    savedAt: e.savedAt, favourite: !e.favourite)
            }
        } else {
            entries[id] = Entry(treeId: id, visitedAt: nil, savedAt: Date(),
                                favourite: true)
        }
        persist()
        // ON only. Taking a heart off again is a correction, not a verb.
        if entries[id]?.favourite == true { Measure.event("tree_saved", ["tree": id]) }
        onMutate?(id, entries[id])
    }

    /// Ticking a tree off is the point of the whole verb, so it also saves it:
    /// nobody should have to save a tree before they are allowed to say they
    /// stood in front of it.
    /// Standing in front of it, and only that. It no longer hearts the tree as
    /// a side effect: the two lists are independent, so collecting one does
    /// not put it in the other (Hidde, 2026-08-26). Untick the last thing on
    /// a row that was never a favourite and the row goes.
    public func toggleVisited(_ id: String) {
        let existing = entries[id]
        let fav = existing?.favourite ?? false
        if existing?.visitedAt != nil {
            if fav {
                entries[id] = Entry(treeId: id, visitedAt: nil,
                                    savedAt: existing?.savedAt ?? Date(), favourite: true)
            } else {
                entries[id] = nil
            }
        } else {
            entries[id] = Entry(treeId: id, visitedAt: Date(),
                                savedAt: existing?.savedAt ?? Date(), favourite: fav)
        }
        persist()
        if entries[id]?.visitedAt != nil { Measure.event("tree_visited", ["tree": id]) }
        onMutate?(id, entries[id])
    }

    /// Everything this phone holds, forgotten, WITHOUT telling the server.
    ///
    /// Signing out empties the collection on this phone (Hidde, 2026-08-29:
    /// "de favourites en seen moet ook leeg wanneer niet ingelogd"). Saving is
    /// already gated behind an account, so a filled heart on a signed-out phone
    /// is the leftovers of somebody else's session showing through, and the
    /// ticks and hearts on every card said the app still knew who you were.
    ///
    /// It deliberately does NOT fire `onMutate`. That is the channel that
    /// deletes a row from the account, and this is not a deletion: the
    /// collection lives in the account and comes straight back on the next
    /// sign-in. Emptying a phone must never empty a person's account.
    public func forgetLocally() {
        entries = [:]
        persist()
    }

    private func persist() {
        if let d = try? JSONEncoder().encode(Array(entries.values)) {
            defaults.set(d, forKey: key)
        }
    }

    /// Debug scaffolding, same family as -tab and -spot: a UI test that is
    /// ABOUT the empty state cannot depend on running before the tests that
    /// fill it. One walk test ticking a tree used to fail Collect's day-zero
    /// test, and only when the clones happened to share a simulator.
    private var wipeRequested: Bool {
        ProcessInfo.processInfo.arguments.contains("-reset-collection")
    }

    private func load() {
        if wipeRequested {
            defaults.removeObject(forKey: key)
            return
        }
        guard let d = defaults.data(forKey: key),
              let list = try? JSONDecoder().decode([Entry].self, from: d) else { return }
        entries = Dictionary(list.map { ($0.treeId, $0) }, uniquingKeysWith: { a, _ in a })
    }
}
