// A species answers to every name it goes by (2026-10-31, Hidde: "when
// adding a tree I often dont know the english name"). Built the way
// LatinNameTests builds its catalogue, through the feed's own decoder.
import XCTest
@testable import AncientTrees

final class SpeciesSearchTests: XCTestCase {
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

    private var catalogue: Catalogue {
        let names = """
        [{"c":"Pedunculate Oak","l":"Quercus robur","a":["Zomereik","Stieleiche","Chêne pédonculé"]},
         {"c":"European Yew","l":"Taxus baccata","a":["Taxus","Eibe"]},
         {"c":"European Hornbeam","l":"Carpinus betulus","a":["Haagbeuk","Hainbuche"],"m":false},
         {"c":"Oak","l":"Quercus","a":["Eik","Eiche"],"g":true}]
        """
        let dir = try! JSONDecoder().decode([SpeciesNameRow].self, from: Data(names.utf8))
        return Catalogue(trees: [tree("lon_001", species: "Pedunculate Oak (Quercus robur)"),
                                 tree("lon_002", species: "European Yew (Taxus baccata)")],
                         walks: [], species: [], speciesDirectory: dir, version: "t")
    }

    func testAnOtherLanguageFindsOurSpeciesAndSaysWhich() {
        let hits = catalogue.filterSpecies(["Pedunculate Oak", "European Yew"], query: "zomer")
        XCTAssertEqual(hits.map(\.name), ["Pedunculate Oak"])
        XCTAssertEqual(hits.first?.hit.via, "Zomereik")
    }

    func testAccentsAndHyphensDoNotMatter() {
        XCTAssertNotNil(catalogue.speciesHit("Pedunculate Oak", query: "chene"))
        XCTAssertNotNil(catalogue.speciesHit("Pedunculate Oak", query: "pedoncule"))
    }

    func testTheLatinStillAnswers() {
        XCTAssertEqual(catalogue.speciesHit("Pedunculate Oak", query: "robur"), .latin)
    }

    func testOneLetterOffStillFinds() {
        XCTAssertEqual(catalogue.speciesHit("Pedunculate Oak", query: "pedunculte"), .nearly)
        XCTAssertNil(catalogue.speciesHit("European Yew", query: "pedunculte"))
    }

    func testTheOwnNameRanksAboveAnotherName() {
        // "taxus" is the Yew's Latin; nothing else here starts with it.
        let hits = catalogue.filterSpecies(["Pedunculate Oak", "European Yew"], query: "taxus")
        XCTAssertEqual(hits.first?.hit, .latin)
    }

    func testATreeWeDoNotMapIsOfferedWithItsLatin() {
        let offered = catalogue.unmappedSpecies(matching: "haagbeuk")
        XCTAssertEqual(offered.first?.row.species, "European Hornbeam (Carpinus betulus)")
    }

    func testAGenusWordOffersTheGenus() {
        let offered = catalogue.unmappedSpecies(matching: "eik")
        XCTAssertEqual(offered.first?.row.species, "Oak (Quercus sp.)")
    }

    func testAnOldFeedWithoutNamesStillDecodes() {
        let json = #"{"version":"v","count":0,"species":[]}"#
        let feed = try! JSONDecoder().decode(SpeciesFeed.self, from: Data(json.utf8))
        XCTAssertNil(feed.names)
    }
}
