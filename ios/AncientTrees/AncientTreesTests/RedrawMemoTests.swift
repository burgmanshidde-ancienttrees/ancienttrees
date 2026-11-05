// The map, its search and My trees stopped redoing work on every redraw
// (2026-11-04). What a person sees must not change, so each shortcut is held
// here against the computation it replaced: the same trees, in the same order.
//
// SWIFT TESTING, NOT XCTEST (2026-11-05). Written first as an XCTestCase, the
// stored-sets test crashed in CI and on the iOS 18.6 simulator with SIGABRT
// when its Saved went away: "pointer being freed was not allocated" inside
// swift_task_deinitOnExecutorMainActorBackDeploy, called from
// Saved.__deallocating_deinit. That is the Swift runtime's back-deployed
// main-actor deinit failing under an XCTest invocation; the crash took the
// city/country test in the same process down with it. Every other test that
// builds a Saved (CollectionTests, FailureTests, UpgradeTests) is a Swift
// Testing suite and lets it go without trouble, so this file follows them.
// The app itself never releases its one Saved, so no person can hit it.
import Testing
import Foundation
@testable import AncientTrees

@MainActor
struct RedrawMemo {
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
    @Test func theCityAndCountryIndexMatchFilteringTheWholeList() {
        let c = catalogue
        for slug in ["lisbon", "porto", "london", "nowhere"] {
            #expect(c.trees(inCity: slug).map(\.id)
                    == c.trees.filter { $0.citySlug == slug }.map(\.id), "\(slug)")
        }
        for name in ["Portugal", "United Kingdom", "Nowhere"] {
            #expect(c.trees(inCountry: name).map(\.id)
                    == c.trees.filter { $0.country == name }.map(\.id), "\(name)")
        }
    }

    /// The map reads these sets several times per redraw; the store keeps
    /// them and must forget them on every change.
    @Test func theStoredIdSetsFollowEveryChange() {
        let suite = "redraw-memo-\(UUID().uuidString)"
        defer { UserDefaults.standard.removePersistentDomain(forName: suite) }
        let saved = Saved(defaults: UserDefaults(suiteName: suite)!)

        func check(_ step: String) {
            #expect(saved.collectedIds
                    == Set(saved.entries.values.filter { $0.visitedAt != nil }.map(\.treeId)),
                    "\(step)")
            #expect(saved.favouriteIds == Set(saved.favourites.map(\.treeId)), "\(step)")
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
    @Test func searchingFoldedNamesMatchesFoldingPerKeystroke() {
        let c = catalogue
        let idx = MapSearch.SearchIndex(c)
        for raw in ["oak", "OAK", "drag", "princ", "plane", "of", "zzzz", "fig of"] {
            let q = MapSearch.fold(raw)
            let old = c.trees.filter {
                let n = MapSearch.fold($0.name)
                return n.hasPrefix(q) || n.contains(" " + q)
            }
            #expect(idx.treesNamed(q).map(\.id) == old.map(\.id), "\(raw)")
        }
        #expect(Set(idx.cities.map(\.slug)) == ["lisbon", "porto", "london"])
        #expect(idx.cityBySlug["lisbon"]?.count == 3)
        #expect(idx.countries.first?.name == "Portugal")
    }
}
