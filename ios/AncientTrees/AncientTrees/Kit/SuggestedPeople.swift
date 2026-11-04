// Who Find people suggests under an empty field (Hidde, 2026-11-04: "i like
// all your proposals please build", drafts/design-2026-11-04 section 3).
//
// Convention (CONVENTIONS.md, "The empty Find people screen", 2026-11-03):
// Strava, AllTrails and Instagram fill the space under an empty people search
// with suggested people. Ours suggests only names that are already public, so
// no contacts and no Facebook (hard list 1):
//   1. ambassadors whose profile is public, from the feed (the website settles
//      consent: BrowseFacet.ambassadors, `profile` only while public), the
//      places you saved or collected first;
//   2. public profiles who photographed trees in those places, from
//      suggested_photographers() (supabase/suggested-people.sql).
// Never you, never somebody you blocked, and people you already follow go to
// the end rather than the top. Pure, so the order has a test.

import Foundation

public struct SuggestedPerson: Hashable, Sendable {
    public var profile: Profiles.Profile
    /// One line under the name: "Lisbon ambassador", "Photographed 4 trees in Utrecht".
    public let reason: String
    public let ambassador: Bool
}

public enum SuggestedPeople {
    /// At most this many rows: a page of suggestions, not a directory.
    public static let limit = 12

    /// Your places, most trees first: the city slugs of the trees you saved
    /// or collected.
    public static func places(of treeIds: [String], city: (String) -> String?) -> [String] {
        var count: [String: Int] = [:]
        for id in treeIds { if let c = city(id) { count[c, default: 0] += 1 } }
        return count.sorted { $0.value != $1.value ? $0.value > $1.value : $0.key < $1.key }.map(\.key)
    }

    public static func reason(photographed n: Int, in place: String) -> String {
        n == 1 ? "Photographed 1 tree in \(place)" : "Photographed \(n) trees in \(place)"
    }

    public static func reason(ambassadorOf place: String) -> String { "\(place) ambassador" }

    /// One ambassador from the feed: their profile id and the place's name.
    public struct Ambassador: Hashable, Sendable {
        public let userId: String
        public let name: String
        public let placeSlug: String
        public let placeName: String
        public init(userId: String, name: String, placeSlug: String, placeName: String) {
            self.userId = userId; self.name = name; self.placeSlug = placeSlug; self.placeName = placeName
        }
    }

    /// Every ambassador the feed names with a public profile.
    public static func ambassadors(in cities: [BrowseFacet]) -> [Ambassador] {
        cities.flatMap { c -> [Ambassador] in
            guard let slug = c.slug else { return [] }
            return (c.ambassadors ?? []).compactMap { a in
                a.profile.map { Ambassador(userId: $0, name: a.name, placeSlug: slug, placeName: c.name) }
            }
        }
    }

    /// The list, in order: ambassadors of your places, people who photographed
    /// trees there, then the other ambassadors; one row per person; never
    /// you or a blocked person; anybody you follow moved to the end.
    public static func build(ambassadors: [Ambassador],
                             photographers: [Profiles.Photographer],
                             yourPlaces: [String],
                             placeName: (String) -> String,
                             me: String?,
                             blocked: (String) -> Bool,
                             following: Set<String>) -> [SuggestedPerson] {
        let rank = Dictionary(uniqueKeysWithValues: yourPlaces.enumerated().map { ($1, $0) })
        let mine = ambassadors.filter { rank[$0.placeSlug] != nil }
            .sorted { rank[$0.placeSlug]! < rank[$1.placeSlug]! }
        let others = ambassadors.filter { rank[$0.placeSlug] == nil }
        func row(_ a: Ambassador) -> SuggestedPerson {
            SuggestedPerson(profile: .init(user_id: a.userId, display_name: a.name, avatar_url: nil),
                            reason: reason(ambassadorOf: a.placeName), ambassador: true)
        }
        let shots = photographers.sorted {
            let l = rank[$0.place] ?? Int.max, r = rank[$1.place] ?? Int.max
            return l != r ? l < r : $0.trees > $1.trees
        }.map {
            SuggestedPerson(profile: .init(user_id: $0.user_id, display_name: $0.display_name,
                                           avatar_url: $0.avatar_url),
                            reason: reason(photographed: $0.trees, in: placeName($0.place)),
                            ambassador: false)
        }
        var seen = Set<String>()
        var out: [SuggestedPerson] = []
        for p in mine.map(row) + shots + others.map(row) {
            let id = p.profile.user_id
            guard id != me, !blocked(id), !p.profile.display_name.isEmpty, seen.insert(id).inserted else { continue }
            out.append(p)
        }
        let fresh = out.filter { !following.contains($0.profile.user_id) }
        let followed = out.filter { following.contains($0.profile.user_id) }
        return Array((fresh + followed).prefix(limit))
    }
}
