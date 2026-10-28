// A provider's full name becomes a first name and an initial, never a published
// surname, for every shape a provider sends.
import XCTest
@testable import AncientTrees

final class NameTests: XCTestCase {
    func testFirstNameAndInitial() {
        XCTAssertEqual(Profiles.shortName(from: "Hidde Burgmans"), "Hidde B.")
        XCTAssertEqual(Profiles.shortName(from: "Jan van der Berg"), "Jan B.")
        XCTAssertEqual(Profiles.shortName(from: "Giulia"), "Giulia")
        XCTAssertEqual(Profiles.shortName(from: "  "), "")
    }

    /// The server's starting name gives way to Apple's; a name a person
    /// chose never does.
    func testAGeneratedNameIsRecognised() {
        XCTAssertTrue(Profiles.isGeneratedName("Mossy Linden 4821"))
        XCTAssertTrue(Profiles.isGeneratedName("Evergreen Sequoia 0007"))
        XCTAssertFalse(Profiles.isGeneratedName("Hidde B."))
        XCTAssertFalse(Profiles.isGeneratedName("Miguel Portugal"))
        XCTAssertFalse(Profiles.isGeneratedName("Oak Lover 2024 fan"))
    }

    /// A profile fetch that never answered (offline, a test with no server)
    /// is not a person without a name. The first flow walk after the name
    /// change opened the editor over every launch and the app trapped.
    @MainActor
    func testNoAnswerFromTheServerAsksNobody() async {
        let p = Profiles()
        let fine = await p.ensureName(userId: "x", token: "t", providerName: nil)
        XCTAssertTrue(fine, "no answer yet, so nothing to ask")
    }
}
