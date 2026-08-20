// Everything the app knows, held in memory. 1377 trees is 2.5 MB of JSON, which
// is small enough to keep whole rather than to page out of a database, and that
// is what makes the app work with no signal: there is no query that needs the
// network once this is loaded.

import Foundation

public struct Catalogue: Sendable {
    public let version: String
    public let trees: [Tree]
    public let walks: [Walk]
    public let species: [Species]
    /// The website's hand-curated collections, which Explore is built out of.
    public let collections: [TreeCollection]

    private let byId: [String: Tree]
    private let walksByCity: [String: [Walk]]

    public init(trees: [Tree], walks: [Walk], species: [Species],
                collections: [TreeCollection] = [], version: String) {
        self.trees = trees
        self.walks = walks
        self.species = species
        self.collections = collections
        self.version = version
        self.byId = Dictionary(trees.map { ($0.id, $0) }, uniquingKeysWith: { a, _ in a })
        self.walksByCity = Dictionary(grouping: walks, by: { $0.citySlug })
    }

    public func tree(_ id: String) -> Tree? { byId[id] }

    /// A collection's trees, skipping any id the feed no longer carries, so a
    /// collection that lost a tree still works.
    public func trees(of collection: TreeCollection) -> [Tree] {
        collection.trees.compactMap { byId[$0] }
    }

    public func walks(inCity slug: String) -> [Walk] { walksByCity[slug] ?? [] }

    /// The trees of one walk, in the order the walk lists them, skipping any id
    /// the feed no longer carries. A walk that lost a tree still works.
    public func trees(of walk: Walk) -> [Tree] { walk.trees.compactMap { byId[$0] } }

    /// The home screen: what is near me, nearest first.
    ///
    /// `within` exists so the answer can be honestly empty. Most of the world has
    /// no tree of ours within an hour, and showing somebody the 12th nearest at
    /// 400 km is worse than saying there is nothing here yet.
    public func nearest(to lat: Double, _ lng: Double,
                        limit: Int = 10,
                        withinKm: Double = 50) -> [(tree: Tree, km: Double)] {
        trees.map { (tree: $0, km: $0.distanceKm(from: lat, lng)) }
             .filter { $0.km <= withinKm }
             .sorted { $0.km < $1.km }
             .prefix(limit)
             .map { $0 }
    }

    /// The Season Radar: trees whose one good moment is this month.
    public func atTheirBest(inMonth month: Int,
                            near lat: Double? = nil, _ lng: Double? = nil,
                            withinKm: Double = 50) -> [Tree] {
        let hits = trees.filter { $0.bestTime?.isNow(month) == true }
        guard let lat, let lng else { return hits }
        return hits.filter { $0.distanceKm(from: lat, lng) <= withinKm }
                   .sorted { $0.distanceKm(from: lat, lng) < $1.distanceKm(from: lat, lng) }
    }

    public var citySlugs: [String] { Array(Set(trees.map(\.citySlug))).sorted() }
}
