import XCTest
@testable import AncientTrees

/// A tree's photographs, and the rule that decides which ones the phone shows
/// (2026-09-12, when trees gained more than one).
///
/// The website is the only thing that decides the SET and its ORDER. This is
/// the app's half of that contract, and the three cases below are the three
/// states a feed can actually be in: a tree with one photograph, a tree with
/// several, and a catalogue written by a version of the app that had never
/// heard of the field. The third is the one that breaks everybody at once if
/// it is wrong, which is UpgradeTests' whole subject: a phone that has synced
/// before meets a release where a model changed, and a single missing
/// non-optional field rejects the entire file rather than one tree.
final class PhotoSetTests: XCTestCase {

    private func tree(_ photoJSON: String, photos: String? = nil) throws -> Tree {
        let extra = photos.map { ",\"photos\":\($0)" } ?? ""
        let json = """
        {"id":"kyo_006","name":"The Camphor of Munakata Shrine",
         "species":"Camphor Tree (Cinnamomum camphora)","age":null,
         "age_min":null,"age_max":null,"lat":35.019452,"lng":135.760783,
         "city":"Kyoto","city_slug":"kyoto","country":"Japan",
         "neighbourhood":null,"access":"","transport":null,
         "precision":"confirmed","best_time":null,"peak":null,"story":"",
         "how_to_recognise":null,"url":"","photo":\(photoJSON)\(extra)}
        """
        return try JSONDecoder().decode(Tree.self, from: Data(json.utf8))
    }

    private func photo(_ name: String) -> String {
        """
        {"url":"https://ancienttrees.app/photos/\(name).jpg","license":"x",
         "attribution":null,"width":1600,"height":1200,
         "thumb":"https://ancienttrees.app/photos/\(name)-500.jpg",
         "hero":"https://ancienttrees.app/photos/\(name).jpg",
         "credit_required":false,"attribution_short":null,"credit_line":null}
        """
    }

    /// The ordinary tree, which is 3,054 of them: no `photos` key at all.
    func testOnePhotographIsASetOfOne() throws {
        let t = try tree(photo("wide"))
        XCTAssertNil(t.photos)
        XCTAssertEqual(t.shots.count, 1)
        XCTAssertEqual(t.shots.first?.url, t.photo?.url)
    }

    /// The feed sends the WHOLE set, lead first, so the phone joins nothing.
    func testTheSetArrivesLeadFirstAndIsNotReordered() throws {
        let t = try tree(photo("wide"),
                         photos: "[\(photo("wide")),\(photo("closeup"))]")
        XCTAssertEqual(t.shots.count, 2)
        XCTAssertTrue(t.shots[0].url.hasSuffix("wide.jpg"))
        XCTAssertTrue(t.shots[1].url.hasSuffix("closeup.jpg"))
        // The lead is still the lead: cards, the map and the share card read
        // `photo` and must not start seeing a different picture.
        XCTAssertEqual(t.photo?.url, t.shots[0].url)
    }

    /// A tree with no photograph at all shows none, rather than an empty box
    /// standing in for one.
    func testNoPhotographIsAnEmptySet() throws {
        let t = try tree("null")
        XCTAssertTrue(t.shots.isEmpty)
    }

    /// An empty array is not "no photographs", it is a feed that sent the key
    /// and nothing in it. Falling back to the lead is the honest read, and it
    /// is what stops a malformed feed blanking a picture we already have.
    func testAnEmptyArrayFallsBackToTheLead() throws {
        let t = try tree(photo("wide"), photos: "[]")
        XCTAssertEqual(t.shots.count, 1)
        XCTAssertTrue(t.shots[0].url.hasSuffix("wide.jpg"))
    }

    /// OLD BYTES, NEW CODE. A catalogue written before the field existed must
    /// decode, because the alternative is an empty map on every phone that has
    /// ever synced. `photos` is optional with a default for exactly this.
    func testACatalogueWrittenBeforeTheFieldStillDecodes() throws {
        let t = try tree(photo("wide"))
        XCTAssertEqual(t.shots.count, 1)
        XCTAssertNoThrow(try JSONEncoder().encode(t))
    }
}
