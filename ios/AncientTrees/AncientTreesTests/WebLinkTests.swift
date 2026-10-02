// Every shape of web address the association file hands to the app, parsed
// without a catalogue (WebLink.Lookup is closures), so this runs on a machine
// with no feed and fails the moment a path shape stops resolving.
import XCTest
@testable import AncientTrees

final class WebLinkTests: XCTestCase {
    private let lookup = WebLink.Lookup(
        treeId: { path in ["/paris/turkey-oak-of-square-rene-le-gall": "par_033",
                           "/lisbon/dragon-tree-of-quinta-conde-dos-arcos": "lis_030"][path] },
        isCity: { ["paris", "lisbon", "the-hague"].contains($0) },
        countryName: { ["netherlands": "Netherlands", "united-kingdom": "United Kingdom"][$0] },
        speciesName: { ["london-plane": "London Plane", "pedunculate-oak": "Pedunculate Oak"][$0] })

    private func parse(_ url: String) -> WebLink.Target {
        WebLink.parse(URLComponents(string: url)!, lookup: lookup)
    }

    func testATreePageOpensTheTree() {
        XCTAssertEqual(parse("https://ancienttrees.app/paris/turkey-oak-of-square-rene-le-gall"), .route(.tree("par_033")))
    }

    func testATranslatedTreePageOpensTheSameTree() {
        XCTAssertEqual(parse("https://ancienttrees.app/fr/paris/turkey-oak-of-square-rene-le-gall"), .route(.tree("par_033")))
        XCTAssertEqual(parse("https://ancienttrees.app/ja/lisbon/dragon-tree-of-quinta-conde-dos-arcos"), .route(.tree("lis_030")))
    }

    func testACityPageOpensTheCity() {
        XCTAssertEqual(parse("https://ancienttrees.app/paris"), .route(.city("paris")))
        XCTAssertEqual(parse("https://ancienttrees.app/de/paris/"), .route(.city("paris")))
    }

    func testTheQuestionPageFallsBackToItsCity() {
        XCTAssertEqual(parse("https://ancienttrees.app/paris/oldest-tree"), .route(.city("paris")))
        XCTAssertEqual(parse("https://ancienttrees.app/de/paris/aeltester-baum"), .route(.city("paris")))
    }

    func testCountrySpeciesAndCollectionPages() {
        XCTAssertEqual(parse("https://ancienttrees.app/netherlands"), .route(.country("Netherlands")))
        XCTAssertEqual(parse("https://ancienttrees.app/species/london-plane"), .route(.species("London Plane")))
        XCTAssertEqual(parse("https://ancienttrees.app/collections/oldest-trees"), .route(.collection("oldest-trees")))
    }

    func testExploreIsTheMapAndTheIndexesAreNothing() {
        XCTAssertEqual(parse("https://ancienttrees.app/explore"), .map)
        XCTAssertEqual(parse("https://ancienttrees.app/nl/explore"), .map)
        XCTAssertEqual(parse("https://ancienttrees.app/"), .none)
        XCTAssertEqual(parse("https://ancienttrees.app/species"), .none)
        XCTAssertEqual(parse("https://ancienttrees.app/collections"), .none)
        XCTAssertEqual(parse("https://ancienttrees.app/nowhere-we-publish"), .none)
    }

    func testASharedSightingStillOpens() {
        let id = UUID()
        XCTAssertEqual(parse("https://ancienttrees.app/t?id=\(id.uuidString)"), .route(.shared(id)))
        XCTAssertEqual(parse("https://ancienttrees.app/t?id=garbage"), .none)
    }

    func testSlugsMatchTheWebsite() {
        XCTAssertEqual(WebLink.slugify("London Plane"), "london-plane")
        XCTAssertEqual(WebLink.slugify("The Hague"), "hague")
        XCTAssertEqual(WebLink.slugify("Tilleul d'Henri IV"), "tilleul-dhenri-iv")
        XCTAssertEqual(WebLink.slugify("Pedunculate Oak (Quercus robur)"), "pedunculate-oak-quercus-robur")
    }
}
