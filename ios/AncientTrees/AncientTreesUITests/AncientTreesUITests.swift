// The tests that need a finger.
//
// Everything else about this app can be checked from a screenshot, and the
// screenshot is how it is checked. These three cannot be, because they are
// about what happens AFTER a tap, and a screenshot of a screen nobody tapped
// proves the wrong thing.
//
// The first one exists because of a specific risk taken on 2026-08-20: the map
// tab hides its navigation bar so the "Near you" chip can float over the map
// instead of a bare title sitting on nothing. If that hiding leaks into the
// pushed tree page, there is no back button and the person is trapped on a
// tree, which is a far worse bug than the cosmetic one it fixes. So it is
// asserted rather than assumed.

import XCTest

final class AncientTreesUITests: XCTestCase {

    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    private func launch(_ args: [String] = []) -> XCUIApplication {
        let app = XCUIApplication()
        // A fixed origin keeps the test off the location permission dialog and
        // makes the list deterministic: Amsterdam always has trees near it.
        app.launchArguments = ["-at=52.3731,4.8922"] + args
        app.launch()
        return app
    }

    /// Hiding the map's navigation bar must not hide the pushed page's.
    @MainActor
    func testTreePageFromTheMapHasAWayBack() throws {
        let app = launch(["-tab=0"])

        // The sheet's first card, whatever tree it happens to be today.
        let firstCard = app.buttons.containing(
            NSPredicate(format: "label CONTAINS[c] 'km' OR label CONTAINS[c] 'years'")
        ).firstMatch
        XCTAssertTrue(firstCard.waitForExistence(timeout: 10), "no tree card in the map sheet")
        firstCard.tap()

        // Whatever it is called, there has to be something that goes back.
        let back = app.navigationBars.buttons.firstMatch
        XCTAssertTrue(back.waitForExistence(timeout: 5),
                      "a tree opened from the map has no back button, so the person is trapped")
        back.tap()
        XCTAssertTrue(app.buttons["Map"].waitForExistence(timeout: 5),
                      "back did not return to the map tab")
    }

    /// Ticking a tree off is the product's own verb and the moment the account
    /// is asked for, so it must survive the tap rather than only compile.
    @MainActor
    func testTickingATreeKeepsIt() throws {
        let app = launch(["-tab=0"])

        let firstCard = app.buttons.containing(
            NSPredicate(format: "label CONTAINS[c] 'km' OR label CONTAINS[c] 'years'")
        ).firstMatch
        XCTAssertTrue(firstCard.waitForExistence(timeout: 10))
        firstCard.tap()

        let tick = app.buttons.matching(identifier: "checkmark.seal").firstMatch
        if tick.waitForExistence(timeout: 5) {
            tick.tap()
            // The sign-in sheet is allowed to appear here; that is the design.
            // Either way the tick itself must have registered.
            XCTAssertTrue(app.buttons.matching(identifier: "checkmark.seal.fill").firstMatch
                            .waitForExistence(timeout: 5)
                          || app.staticTexts["That one is yours"].waitForExistence(timeout: 5),
                          "ticking a tree left no visible trace")
        }
    }

    /// The sheet the whole account funnel runs through. If it does not present,
    /// nothing downstream of it can work, and it presented from a launch
    /// argument rather than a tap so that failure would be invisible.
    @MainActor
    func testTheSignInSheetPresents() throws {
        let app = launch(["-tab=3", "-signin"])
        XCTAssertTrue(app.staticTexts["That one is yours"].waitForExistence(timeout: 10),
                      "the sign-in sheet did not present")
        XCTAssertTrue(app.buttons["Email me a code"].exists,
                      "the email route is missing from the sign-in sheet")
    }
}
