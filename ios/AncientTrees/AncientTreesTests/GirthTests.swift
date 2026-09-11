import XCTest
@testable import AncientTrees

/// Girth as somebody types it standing in front of the trunk (2026-09-11).
/// The web form carries the same rule in contribute.astro; both must agree.
final class GirthTests: XCTestCase {

    func testEveryWayOfWritingTheSameTrunk() {
        XCTAssertEqual(Sightings.girthCm(parsing: "4.2"), 420)
        XCTAssertEqual(Sightings.girthCm(parsing: "4,2"), 420)
        XCTAssertEqual(Sightings.girthCm(parsing: "4.2 m"), 420)
        XCTAssertEqual(Sightings.girthCm(parsing: "4.2m"), 420)
        XCTAssertEqual(Sightings.girthCm(parsing: "420 cm"), 420)
        XCTAssertEqual(Sightings.girthCm(parsing: "420"), 420)
        XCTAssertEqual(Sightings.girthCm(parsing: "1.5"), 150)
    }

    func testNonsenseIsRefusedRatherThanStored() {
        XCTAssertNil(Sightings.girthCm(parsing: ""))
        XCTAssertNil(Sightings.girthCm(parsing: "big"))
        XCTAssertNil(Sightings.girthCm(parsing: "0"))
        // Outside the database's own check, so it would be refused there too.
        XCTAssertNil(Sightings.girthCm(parsing: "9000"))
        XCTAssertNil(Sightings.girthCm(parsing: "5 cm"))
    }

    func testMetresReadBack() {
        XCTAssertEqual(Sightings.metres(420), "4.2")
        XCTAssertEqual(Sightings.metres(415), "4.15")
        XCTAssertEqual(Sightings.metres(400), "4")
    }

    /// A phone that saved its trees before girth existed must still open them.
    func testASightingWrittenBeforeGirthStillDecodes() throws {
        let json = """
        [{"id":"6F1A2B3C-0000-4000-8000-000000000001","name":"The oak","note":"",
          "lat":52.1,"lng":5.1,"date":0,"status":"mine"}]
        """
        let rows = try JSONDecoder().decode([Sightings.Sighting].self, from: Data(json.utf8))
        XCTAssertEqual(rows.count, 1)
        XCTAssertNil(rows[0].girthCm)
    }
}
