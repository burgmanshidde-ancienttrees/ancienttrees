// Everything the app knows, held in memory. Getting on for two thousand trees
// is a few megabytes of JSON, which is small enough to keep whole rather than
// to page out of a database, and that is what makes the app work with no
// signal: there is no query that needs the network once this is loaded.
//
// The struct is built once per load and is where the app's derived lookups
// live, so nothing downstream has to scan the list. See the indexes below.

import Foundation

public struct Catalogue: Sendable {
    public let version: String
    public let trees: [Tree]
    public let walks: [Walk]
    public let species: [Species]
    /// The website's hand-curated collections, which Explore is built out of.
    public let collections: [TreeCollection]
    /// The city, country, species and park facets from /api/browse.json, with
    /// the intro the website wrote and the face it shows.
    public let facets: BrowseFacets

    private let byId: [String: Tree]
    private let walksByCity: [String: [Walk]]

    // GROUPED ONCE HERE RATHER THAN IN EVERY SCREEN.
    //
    // byId and walksByCity have been built here since the start; the three
    // below had not, so `Dictionary(grouping: trees, by: \.citySlug)` and its
    // siblings were written out again in Home, MapSearch, IndexPages, Collect,
    // SpeciesChooser and SpeciesPicker, and `trees.filter { $0.country == x }`
    // in three more. A computed property on a View re-runs on every body pass,
    // so MapSearch rebuilt three of these on every keystroke while somebody was
    // typing. It is milliseconds rather than a freeze, and the real cost was
    // the copies: six places deciding separately what "the trees of a city"
    // means is six places to keep in step.
    //
    // This is the cheapest possible moment to pay for it. A Catalogue is built
    // when the app loads one and never again, so the work happens once per
    // launch instead of once per frame.
    private let byCity: [String: [Tree]]
    private let byCountry: [String: [Tree]]
    private let bySpecies: [String: [Tree]]

    /// Every common name we carry, once each, sorted. The search field asked
    /// for this by building a Set and sorting it, per keystroke.
    public let speciesNames: [String]

    public init(trees: [Tree], walks: [Walk], species: [Species],
                collections: [TreeCollection] = [],
                facets: BrowseFacets = .empty, version: String) {
        self.trees = trees
        self.walks = walks
        self.species = species
        self.collections = collections
        self.facets = facets
        self.version = version
        self.byId = Dictionary(trees.map { ($0.id, $0) }, uniquingKeysWith: { a, _ in a })
        self.walksByCity = Dictionary(grouping: walks, by: { $0.citySlug })
        self.byCity = Dictionary(grouping: trees, by: { $0.citySlug })
        self.byCountry = Dictionary(grouping: trees, by: { $0.country })
        let bySpecies = Dictionary(grouping: trees, by: { $0.commonName })
        self.bySpecies = bySpecies
        // Sorted here so it is stable everywhere it is shown. An empty common
        // name is a tree whose species nobody has established yet, which is a
        // real state on this site (the publish-and-ask rule) and not a species.
        self.speciesNames = bySpecies.keys.filter { !$0.isEmpty }.sorted()
    }

    public func tree(_ id: String) -> Tree? { byId[id] }

    /// The trees of one city, country or species. Order is the catalogue's own,
    /// which is what every caller filtering the whole list used to get.
    public func trees(inCity slug: String) -> [Tree] { byCity[slug] ?? [] }
    public func trees(inCountry name: String) -> [Tree] { byCountry[name] ?? [] }
    public func trees(ofSpecies commonName: String) -> [Tree] { bySpecies[commonName] ?? [] }

    /// Every city, country and species with its trees, for the pages that show
    /// all of them. A view of the index rather than a fresh grouping.
    public var citiesWithTrees: [String: [Tree]] { byCity }
    public var countriesWithTrees: [String: [Tree]] { byCountry }
    public var speciesWithTrees: [String: [Tree]] { bySpecies }

    // MARK: - card faces
    //
    // WHICH PHOTOGRAPH FRONTS A CARD IS NOT THIS APP'S DECISION (2026-08-25).
    // It used to be, by accident: a city card took the first tree in the list
    // with a photograph, so the same city wore one face on the website and
    // another on the phone, and the website's pin (hero_tree_id, face_tree_id)
    // reached the app not at all. Hidde, on a species card fronted by a
    // fountain: "do you save the thumbnails between app and web and make sure we
    // use the same ones?"
    //
    // The answer travels in the feed as a tree id. When it is missing (an old
    // snapshot), fall back to the best photograph we can judge locally rather
    // than to the first one, which is the same ranking the website uses: enough
    // pixels, then landscape, then widest.

    /// The tree whose photograph fronts this city.
    public func face(city slug: String) -> Tree? {
        facets.face(city: slug).flatMap { byId[$0] } ?? bestFace(trees(inCity: slug))
    }

    /// The tree whose photograph fronts this country.
    public func face(country name: String) -> Tree? {
        facets.face(country: name).flatMap { byId[$0] } ?? bestFace(trees(inCountry: name))
    }

    /// The tree whose photograph fronts this species.
    public func face(species commonName: String) -> Tree? {
        facets.face(species: commonName).flatMap { byId[$0] } ?? bestFace(trees(ofSpecies: commonName))
    }

    /// The website's introduction to a species, where it wrote one.
    public func intro(species commonName: String) -> String? {
        facets.intro(species: commonName)
    }

    /// The best photograph in a set for a letterbox, mirroring bestFaceTree()
    /// in site/src/lib/images.ts. Only ever a fallback: a photograph's SUBJECT
    /// is a person's judgement, and that judgement arrives as a face id.
    private func bestFace(_ set: [Tree]) -> Tree? {
        set.filter { $0.photo != nil }
           .max { a, b in
               let pa = a.photo!, pb = b.photo!
               let bigA = (pa.width ?? 0) == 0 || (pa.width ?? 0) >= 540
               let bigB = (pb.width ?? 0) == 0 || (pb.width ?? 0) >= 540
               if bigA != bigB { return bigB }
               let landA = (pa.width ?? 0) > 0 && (pa.height ?? 0) > 0 && (pa.width ?? 0) >= (pa.height ?? 0)
               let landB = (pb.width ?? 0) > 0 && (pb.height ?? 0) > 0 && (pb.width ?? 0) >= (pb.height ?? 0)
               if landA != landB { return landB }
               return (pa.width ?? 0) < (pb.width ?? 0)
           }
    }

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

    public var citySlugs: [String] { byCity.keys.sorted() }
}
