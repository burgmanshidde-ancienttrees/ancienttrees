// A species answers to its scientific name as well as its common one
// (2026-10-03, a reader's request). The name is read off the record the feed
// already carries, so these are decoded through the feed's own decoder, the
// same way MapAimTests builds a tree.
import XCTest
@testable import AncientTrees

final class LatinNameTests: XCTestCase {
    private func tree(_ id: String, species: String) -> Tree {
        let json = """
        {"id":"\(id)","name":"\(id)","species":"\(species)","age":null,
         "age_min":null,"age_max":null,"lat":51.5,"lng":-0.1,
         "city":"London","city_slug":"london","country":"United Kingdom","neighbourhood":null,
         "access":"","transport":null,"precision":"confirmed","best_time":null,
         "peak":null,"story":"","how_to_recognise":null,"url":"","photo":null}
        """
        return try! JSONDecoder().decode(Tree.self, from: Data(json.utf8))
    }

    func testTheLatinIsTheParenthetical() {
        XCTAssertEqual(Tree.scientificName(of: "European Yew (Taxus baccata)"), "Taxus baccata")
        XCTAssertEqual(Tree.scientificName(of: "Oak (Quercus sp.)"), "Quercus sp.")
        XCTAssertNil(Tree.scientificName(of: "species not established"))
        XCTAssertNil(Tree.scientificName(of: "Ficus organensis"))
        XCTAssertEqual(Tree.commonName(of: "European Yew (Taxus baccata)"), "European Yew")
    }

    /// The feed's own field wins; the trees' parenthetical fills in for a
    /// species the facets do not carry.
    func testTheCatalogueAnswersFromTheFeedThenTheTrees() {
        let yew = tree("lon_001", species: "European Yew (Taxus baccata)")
        let oak = tree("lon_002", species: "Pedunculate Oak (Quercus robur)")
        let facets = BrowseFacets(cities: [], countries: [],
                                  species: [BrowseFacet(slug: "european-yew", name: "European Yew",
                                                        trees: nil, count: 1, intro: nil, face: nil,
                                                        scientific: "Taxus baccata L.", aka: nil,
                                                        focus: nil, popularity: nil)],
                                  parks: [])
        let cat = Catalogue(trees: [yew, oak], walks: [], species: [], facets: facets, version: "t")
        XCTAssertEqual(cat.scientificName(of: "European Yew"), "Taxus baccata L.")
        XCTAssertEqual(cat.scientificName(of: "Pedunculate Oak"), "Quercus robur")
        XCTAssertNil(cat.scientificName(of: "Nothing"))
    }
}
