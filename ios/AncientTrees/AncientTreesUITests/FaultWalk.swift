// The app with the network taken away, which is where it is actually used.
//
// Every other UI test here runs the path where everything works. The complaints
// after a launch do not come from there. They come from a wood with no signal,
// a hotel wifi that accepts a connection and then says nothing, and a Supabase
// answering 500 for ten minutes. Faults.swift makes each of those reachable
// with one launch argument; these are the five answers that matter.
//
// The promise being tested is one sentence: a person standing under a tree with
// no bars can still read about the tree they are standing under. Everything the
// app needs for that is in the bundle already. What is being checked is that
// nothing in front of it waits for a network that is not coming.

import XCTest

final class FaultWalk: XCTestCase {

    override func setUpWithError() throws {
        continueAfterFailure = false
        XCUIDevice.shared.orientation = .portrait
        XCUIDevice.shared.appearance = .light
    }

    private func launch(_ args: [String]) -> XCUIApplication {
        let app = XCUIApplication()
        app.launchArguments = ["-at=52.3731,4.8922", "-reset-collection", "-reset-blocks", "-no-cover"] + args
        app.launch()
        return app
    }

    /// Day one of the whole product: no signal, and the map still has trees on
    /// it, because they ship inside the app.
    @MainActor
    func testTheAppOpensWithNoSignalAtAll() throws {
        let app = launch(["-fault=offline", "-tab=0"])

        XCTAssertTrue(app.buttons["tab-map"].waitForExistence(timeout: 15),
                      "with no network the app never finished launching")
        let count = app.staticTexts["map-count"]
        XCTAssertTrue(count.waitForExistence(timeout: 10),
                      "the map showed no trees at all without a network")
        XCTAssertFalse(count.label.hasPrefix("0 "),
                       "the map is empty offline: \(count.label)")
    }

    /// And the tree page itself, which is the thing somebody actually walked to.
    @MainActor
    func testATreeCanStillBeReadWithNoSignal() throws {
        let app = launch(["-fault=offline", "-map", "-sheet=full"])

        let card = app.buttons.matching(identifier: "tree-card").firstMatch
        XCTAssertTrue(card.waitForExistence(timeout: 15), "no tree card offline")
        card.tap()

        XCTAssertTrue(app.buttons["Take me there"].waitForExistence(timeout: 8),
                      "a tree page could not open without a network")
        XCTAssertTrue(app.navigationBars.buttons.firstMatch.exists,
                      "offline, the tree page has no way back")
    }

    /// The hotel wifi case, and the one a screenshot can never catch: the
    /// network accepts the connection and then says nothing for eight seconds.
    /// If any fetch is blocking, the app is frozen for those eight seconds and
    /// this test finds it. Nothing here waits for the network on purpose.
    @MainActor
    func testAStalledConnectionDoesNotFreezeTheApp() throws {
        let app = launch(["-fault=slow", "-tab=0"])

        XCTAssertTrue(app.buttons["tab-discover"].waitForExistence(timeout: 15),
                      "the app never drew a tab bar while the network stalled")
        // Tapped while the stall is still running: eight seconds is longer than
        // this takes, so a frozen app fails here rather than passing slowly.
        app.buttons["tab-discover"].tap()
        XCTAssertTrue(app.staticTexts["explore-home"].waitForExistence(timeout: 5)
                      || app.otherElements["explore-home"].waitForExistence(timeout: 1),
                      "the app would not change tab while a request hung")
    }

    /// A 500 has to end in a sentence somebody can read, and it has to end. A
    /// form left on its spinner is the worst version of this: nothing to read,
    /// nothing to do, and no way to know it failed.
    @MainActor
    func testABrokenServerDoesNotLeaveTheSignInFormSpinning() throws {
        // -show-email: this test drives the typed email route on purpose, and
        // that route is hidden by default since 2026-08-30 (Launch.emailSignIn,
        // commit 6658e94a).
        let app = launch(["-fault=server", "-tab=0", "-signin", "-show-email"])

        XCTAssertTrue(app.otherElements["signin-sheet"].waitForExistence(timeout: 10)
                      || app.staticTexts["Keep your trees"].waitForExistence(timeout: 5),
                      "the sign-in sheet did not open")

        let field = app.textFields["you@example.com"]
        XCTAssertTrue(field.waitForExistence(timeout: 8), "no email field on the sign-in sheet")
        field.tap()
        field.typeText("walker@ancienttrees.app")

        // BY NAME, not by a loose predicate. The first version of this asked for
        // a button whose label contained "code" or "continue" and took the first
        // match, which is "Continue with Apple": the test spent thirty seconds
        // in Apple's own system sheet and then reported that a 500 had left the
        // form with nothing to read. The app had been right the whole time
        // (2026-08-27). A sign-in sheet is full of buttons that sound alike, so
        // this one is named.
        let send = app.buttons["Email me a code"]
        XCTAssertTrue(send.waitForExistence(timeout: 5), "nothing to submit the address with")
        XCTAssertEqual(field.value as? String, "walker@ancienttrees.app",
                       "the address never reached the field, so this tests the wrong failure")
        send.tap()

        // A readable sentence within a few seconds. Not a status code, and not
        // a spinner that never stops.
        //
        // matching(), not containing(). containing() asks for elements that HOLD
        // a descendant matching the predicate, and a static text holds nothing,
        // so it can never match and the test fails whatever the app does. That
        // cost the first run of this file (2026-08-27).
        let message = app.staticTexts.matching(
            NSPredicate(format: "label CONTAINS[c] 'could not' OR label CONTAINS[c] 'try again'")
        ).firstMatch
        XCTAssertTrue(message.waitForExistence(timeout: 15),
                      "a 500 left the sign-in form with nothing to read")
        XCTAssertTrue(field.exists, "the form vanished instead of reporting the failure")
    }

    /// A feed that answers with broken JSON must leave the bundled copy alone.
    /// Reading it as an empty answer would empty the app.
    @MainActor
    func testGarbageFromTheFeedDoesNotEmptyTheApp() throws {
        let app = launch(["-fault=garbage", "-tab=0"])

        let count = app.staticTexts["map-count"]
        XCTAssertTrue(count.waitForExistence(timeout: 15),
                      "a broken feed stopped the map drawing at all")
        XCTAssertFalse(count.label.hasPrefix("0 "),
                       "a broken feed emptied the map: \(count.label)")
    }
}
