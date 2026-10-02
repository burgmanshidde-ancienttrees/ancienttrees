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
