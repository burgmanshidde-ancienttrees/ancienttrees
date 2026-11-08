// THE AMBASSADOR SEAT ANSWERS A FINGER, WHEREVER IT STANDS (2026-11-08).
//
// Hidde, on build 40, Discover in Den Bosch: "Ik kan het niet klikken", then
// "Hoezo vind jou test deze fout niet". SignedOutWalk tapped the seat only in
// the map's sheet and only signed out, and its tap helper falls back to a
// coordinate tap when the control is not hittable, so a seat that ignored a
// real tap on Discover passed every run. This walk closes those three gaps:
//
//   - the seat on DISCOVER (the city you are standing in, -at= Cadiz, which
//     has no ambassador), not only on the city's sheet;
//   - SIGNED IN (-signed-in): the tap must open the apply sheet with its
//     "Apply" button, not only the sign-in sheet;
//   - NO COORDINATE FALLBACK: the seat must be hittable and answer a plain
//     tap, as a finger would, or the test fails.
import XCTest

final class AmbassadorAskWalk: XCTestCase {
    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    /// Cadiz: no ambassador, trees within 30 km, the same city SignedOutWalk uses.
    private let cadiz = "-at=36.5297,-6.2925"

    private func launch(_ args: [String]) -> XCUIApplication {
        let app = XCUIApplication()
        app.launchArguments = ["-no-location-ask"] + args
        app.launch()
        _ = app.staticTexts.firstMatch.waitForExistence(timeout: 30)
        return app
    }

    /// Scroll until the seat exists, then tap it the way a finger does. No
    /// coordinate fallback: a seat that is not hittable is the bug.
    private func tapSeat(_ app: XCUIApplication, file: StaticString = #filePath, line: UInt = #line) {
        let seat = app.descendants(matching: .any)["ambassador-wanted"].firstMatch
        var tries = 0
        while !(seat.exists && seat.isHittable) && tries < 14 {
            if seat.waitForExistence(timeout: 2) && seat.isHittable { break }
            app.swipeUp(); tries += 1
        }
        XCTAssertTrue(seat.exists, "no ambassador seat on screen", file: file, line: line)
        XCTAssertTrue(seat.isHittable, "the ambassador seat is on screen but cannot be tapped", file: file, line: line)
        seat.tap()
    }

    private func expect(_ app: XCUIApplication, _ id: String, _ what: String,
                        file: StaticString = #filePath, line: UInt = #line) {
        let el = app.descendants(matching: .any)[id].firstMatch
        XCTAssertTrue(el.waitForExistence(timeout: 10),
                      "tapping the ambassador seat did not open \(what)", file: file, line: line)
    }

    func testDiscoverSeatAsksSignedOut() {
        let app = launch(["-tab=1", cadiz])
        tapSeat(app)
        expect(app, "signin-sheet", "the sign-in sheet")
    }

    func testDiscoverSeatOpensApplySignedIn() {
        let app = launch(["-tab=1", cadiz, "-signed-in"])
        tapSeat(app)
        expect(app, "ambassador-apply", "the apply sheet")
    }

    func testCitySheetSeatOpensApplySignedIn() {
        let app = launch(["-tab=0", "-open=city:cadiz", "-signed-in"])
        tapSeat(app)
        expect(app, "ambassador-apply", "the apply sheet")
    }

    func testFullCitySheetSeatOpensApplySignedIn() {
        let app = launch(["-tab=0", "-open=city:cadiz", "-sheet=full", "-signed-in"])
        tapSeat(app)
        expect(app, "ambassador-apply", "the apply sheet")
    }
}
