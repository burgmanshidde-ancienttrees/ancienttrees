// The map, its search and My trees stopped redoing work on every redraw
// (2026-11-04). What a person sees must not change, so each shortcut is held
// here against the computation it replaced: the same trees, in the same order.
import XCTest
@testable import AncientTrees

@MainActor
final class RedrawMemoTests: XCTestCase {
    private func tree(_ id: String, name: String, city: String, slug: String,
                      country: String, lat: Double, lng: Double) -> Tree {
        let json = """
        {"id":"\(id)","name":"\(name)","species":"Pedunculate Oak (Quercus robur)","age":null,
         "age_min":null,"age_max":null,"lat":\(lat),"lng":\(lng),
         "city":"\(city)","city_slug":"\(slug)","country":"\(country)","neighbourhood":null,
         "access":"","transport":null,"precision":"confirmed","best_time":null,
         "peak":null,"story":"","how_to_recognise":null,"url":"","photo":null}
        """
        return try! JSONDecoder().decode(Tree.self, from: Data(json.utf8))
    }

    /// Interleaved on purpose, so an index that lost the catalogue's order
    /// would show.
    private var catalogue: Catalogue {
        Catalogue(trees: [
            tree("lis_001", name: "The Dragon Tree", city: "Lisbon", slug: "lisbon",
                 country: "Portugal", lat: 38.71, lng: -9.14),
            tree("por_001", name: "Old Cork Oak", city: "Porto", slug: "porto",
                 country: "Portugal", lat: 41.15, lng: -8.61),
            tree("lon_001", name: "Major Oak of the Park", city: "London", slug: "london",
                 country: "United Kingdom", lat: 51.5, lng: -0.1),
            tree("lis_002", name: "Fig of Príncipe Real", city: "Lisbon", slug: "lisbon",
                 country: "Portugal", lat: 38.72, lng: -9.15),
            tree("lon_002", name: "Plane at Berkeley Square", city: "London", slug: "london",
                 country: "United Kingdom", lat: 51.51, lng: -0.14),
            tree("lis_003", name: "Oak by the river", city: "Lisbon", slug: "lisbon",
                 country: "Portugal", lat: 38.70, lng: -9.16),
        ], walks: [], species: [], version: "t")
    }

    /// MapTab's place header now reads the index instead of filtering.
    func testTheCityAndCountryIndexMatchFilteringTheWholeList() {
        let c = catalogue
        for slug in ["lisbon", "porto", "london", "nowhere"] {
            XCTAssertEqual(c.trees(inCity: slug).map(\.id),
                           c.trees.filter { $0.citySlug == slug }.map(\.id), slug)
        }
        for name in ["Portugal", "United Kingdom", "Nowhere"] {
            XCTAssertEqual(c.trees(inCountry: name).map(\.id),
                           c.trees.filter { $0.country == name }.map(\.id), name)
        }
    }

    /// The map reads these sets several times per redraw; the store keeps
    /// them and must forget them on every change.
    func testTheStoredIdSetsFollowEveryChange() {
        let suite = "redraw-memo-\(UUID().uuidString)"
        let saved = Saved(defaults: UserDefaults(suiteName: suite)!)
        defer { UserDefaults().removePersistentDomain(forName: suite) }

        func check(_ step: String) {
            XCTAssertEqual(saved.collectedIds,
                           Set(saved.entries.values.filter { $0.visitedAt != nil }.map(\.treeId)), step)
            XCTAssertEqual(saved.favouriteIds, Set(saved.favourites.map(\.treeId)), step)
        }
        check("empty")
        saved.toggleSaved("lis_001"); check("hearted")
        saved.toggleVisited("lis_002"); check("collected")
        saved.toggleVisited("lis_001"); check("hearted and collected")
        saved.toggleSaved("lis_001"); check("heart off")
        saved.adopt(treeId: "lon_001", visitedAt: Date(), savedAt: Date(), favourite: true)
        check("adopted")
        saved.toggleVisited("lis_002"); check("uncollected")
        saved.forgetLocally(); check("forgotten")
    }

    /// The search folds every tree name once, then answers each query from
    /// that; the answer must be the old per-keystroke filter's.
    func testSearchingFoldedNamesMatchesFoldingPerKeystroke() {
        let c = catalogue
        let idx = MapSearch.SearchIndex(c)
        for raw in ["oak", "OAK", "drag", "princ", "plane", "of", "zzzz", "fig of"] {
            let q = MapSearch.fold(raw)
            let old = c.trees.filter {
                let n = MapSearch.fold($0.name)
                return n.hasPrefix(q) || n.contains(" " + q)
            }
            XCTAssertEqual(idx.treesNamed(q).map(\.id), old.map(\.id), raw)
        }
        XCTAssertEqual(Set(idx.cities.map(\.slug)), ["lisbon", "porto", "london"])
        XCTAssertEqual(idx.cityBySlug["lisbon"]?.count, 3)
        XCTAssertEqual(idx.countries.first?.name, "Portugal")
    }
}
