// SIGNED OUT, EVERY ACCOUNT CONTROL ASKS (2026-10-07).
//
// Hidde, after a week of finding one gate after another: "how do we make sure
// we dont have more gaps and this doesnt happen in the future". The website
// got a sweep that clicks every button on every page type with no session and
// fails on any that writes, flips or stores. The app cannot click everything
// (a tap on the wrong thing hands you to Safari or Maps), so this walks the
// controls that touch the account, by identifier, with no session, and
// asserts one thing after each tap: THE SIGN-IN SHEET IS ON SCREEN. Nothing
// else is asserted, because nothing else is certain from outside.
//
// The list here is kept honest by scripts/gatecheck.py: every Swift file that
// gates on the account (nudge.require, signingIn = true) must carry an
// identifier that appears in this file, or name its reason for not being
// walked. Adding a gate without a step here fails the push.
import XCTest

final class SignedOutWalk: XCTestCase {
    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    private func launch(_ args: [String]) -> XCUIApplication {
        let app = XCUIApplication()
        app.launchArguments = args
        app.launch()
        _ = app.staticTexts.firstMatch.waitForExistence(timeout: 30)
        return app
    }

    /// Scroll until the control is there and hittable, then tap it.
    private func tap(_ app: XCUIApplication, _ id: String, file: StaticString = #filePath, line: UInt = #line) {
        let b = app.descendants(matching: .any)[id].firstMatch
        XCTAssertTrue(b.waitForExistence(timeout: 20), "no control \(id) on screen", file: file, line: line)
        var tries = 0
        while !b.isHittable && tries < 5 { app.swipeUp(); tries += 1 }
        XCTAssertTrue(b.isHittable, "\(id) is on screen but cannot be tapped", file: file, line: line)
        b.tap()
    }

    private func expectSignIn(_ app: XCUIApplication, after id: String, file: StaticString = #filePath, line: UInt = #line) {
        let sheet = app.descendants(matching: .any)["signin-sheet"].firstMatch
        XCTAssertTrue(sheet.waitForExistence(timeout: 10),
                      "tapping \(id) signed out did not open the sign-in sheet", file: file, line: line)
    }

    func testHeartAsks() {
        let app = launch(["-tree=ams_001"])
        tap(app, "save-heart"); expectSignIn(app, after: "save-heart")
    }

    func testVoteAsks() {
        let app = launch(["-tree=ams_001"])
        tap(app, "worth-the-trip-up"); expectSignIn(app, after: "worth-the-trip-up")
    }

    func testSeenTickAsks() {
        let app = launch(["-tab=0", "-select=ams_001"])
        tap(app, "seen-tick"); expectSignIn(app, after: "seen-tick")
    }

    func testFavouritesChipAsks() {
        let app = launch(["-tab=0"])
        tap(app, "filter-favourites"); expectSignIn(app, after: "filter-favourites")
    }

    func testMyTreesChipAsks() {
        let app = launch(["-tab=0"])
        tap(app, "filter-mine"); expectSignIn(app, after: "filter-mine")
    }

    func testCameraAsks() {
        let app = launch(["-tab=0"])
        tap(app, "tab-collect"); expectSignIn(app, after: "tab-collect")
    }

    func testAmbassadorSeatAsks() {
        // Amsterdam has no ambassador, so its page shows the open seat.
        let app = launch(["-open=city:amsterdam"])
        tap(app, "ambassador-wanted"); expectSignIn(app, after: "ambassador-wanted")
    }

    func testContributeAsks() {
        // The form opens sign-in by itself for anybody without an account.
        let app = launch(["-contribute"])
        expectSignIn(app, after: "-contribute")
    }
}
