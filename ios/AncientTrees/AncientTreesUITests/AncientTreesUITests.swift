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

    /// Tapping the tab you are already on goes back to the top of it. This is
    /// the reason every NavigationLink in the app became a value on 2026-08-20,
    /// so it is the thing that has to be asserted rather than assumed.
    @MainActor
    func testTappingTheActiveTabGoesBackToTheTop() throws {
        let app = launch(["-tab=0"])

        let firstCard = app.buttons.containing(
            NSPredicate(format: "label CONTAINS[c] 'km' OR label CONTAINS[c] 'years'")
        ).firstMatch
        XCTAssertTrue(firstCard.waitForExistence(timeout: 10))
        firstCard.tap()
        XCTAssertTrue(app.buttons["Take me there"].waitForExistence(timeout: 5),
                      "a tree page did not open")

        app.buttons["Map"].tap()
        XCTAssertTrue(app.staticTexts["Near you"].waitForExistence(timeout: 5),
                      "tapping the active tab did not return to the map")
    }

    /// Panning the map has to move the list under it, which is the one thing in
    /// this app that cannot be checked from a screenshot: it only happens after
    /// a finger has dragged something.
    @MainActor
    func testPanningTheMapMovesTheList() throws {
        let app = launch(["-tab=0"])
        XCTAssertTrue(app.staticTexts["Near you"].waitForExistence(timeout: 10),
                      "the map did not open on the user")

        // Drag the map itself, well above the sheet, several times so the centre
        // clears the three kilometres that separates "near you" from "this area".
        let map = app.otherElements.firstMatch
        for _ in 0..<4 {
            map.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.22))
               .press(forDuration: 0.05,
                      thenDragTo: map.coordinate(withNormalizedOffset: CGVector(dx: 0.1, dy: 0.22)))
        }

        XCTAssertTrue(app.staticTexts["Trees in this area"].waitForExistence(timeout: 6),
                      "the map was panned away and the list still claims to be near you")
    }

    /// Explore is built out of the website's own collections, which reach the
    /// app through /api/browse.json. If that feed ever stops carrying them the
    /// screen quietly loses most of itself, and a screenshot of the top of it
    /// would not show that at all.
    @MainActor
    func testExploreCarriesTheCollections() throws {
        let app = launch(["-tab=1"])
        XCTAssertTrue(app.staticTexts["Our favourite tree cities"].waitForExistence(timeout: 12),
                      "the places shelf is missing")

        // Down past the season shelf, the walks and the cities.
        var found = false
        for _ in 0..<8 where !found {
            app.swipeUp(velocity: .fast)
            // A collection heading is inside its own NavigationLink, so
            // accessibility flattens it into the button's label rather than
            // leaving it as loose text. Check both.
            for name in ["Trees Planted by Kings and Their Gardeners",
                         "The Ginkgos Worth a November Trip",
                         "The Great Planes of Europe",
                         "Europe's Most Remarkable Yews"] {
                if app.buttons[name].exists || app.staticTexts[name].exists { found = true }
            }
        }
        XCTAssertTrue(found, "no curated collection shelf rendered on Explore")
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
