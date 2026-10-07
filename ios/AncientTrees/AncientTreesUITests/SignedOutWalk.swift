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

    /// Scroll until the control exists (a lazy list keeps what is below the
    /// fold out of the tree entirely), then tap it; a control that exists but
    /// reads as not hittable (the bar's heart, behind the sheet's hit test) is
    /// tapped at its centre, which is what a finger does.
    private func tap(_ app: XCUIApplication, _ id: String, file: StaticString = #filePath, line: UInt = #line) {
        let b = app.descendants(matching: .any)[id].firstMatch
        var tries = 0
        while !b.waitForExistence(timeout: 4) && tries < 8 { app.swipeUp(); tries += 1 }
        XCTAssertTrue(b.exists, "no control \(id) on screen", file: file, line: line)
        if b.isHittable { b.tap() }
        else { b.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5)).tap() }
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
        // The tree page's own vote is WorthItButton; the thumbs pair
        // (worth-the-trip-up) lives on the payoff screen after a tick.
        let app = launch(["-tree=ams_001"])
        tap(app, "worthit-button"); expectSignIn(app, after: "worthit-button")
    }

    func testSeenTickAsks() {
        // -select opens the map's sheet at its peek; raise it the way
        // FlowWalk does so the card's buttons are in reach.
        let app = launch(["-tab=0", "-select=ams_001"])
        app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.88)).tap()
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
        // -contribute is read by the Collection tab's screen (Profile.swift),
        // so that tab has to be the one on screen.
        let app = launch(["-tab=2", "-contribute"])
        expectSignIn(app, after: "-contribute")
    }
}
