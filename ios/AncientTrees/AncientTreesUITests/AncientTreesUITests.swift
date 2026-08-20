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
        let app = launch(["-map"])

        // The sheet's first card, whatever tree it happens to be today.
        let firstCard = app.buttons.matching(identifier: "tree-card").firstMatch
        XCTAssertTrue(firstCard.waitForExistence(timeout: 10), "no tree card in the map sheet")
        firstCard.tap()

        // Whatever it is called, there has to be something that goes back.
        let back = app.navigationBars.buttons.firstMatch
        XCTAssertTrue(back.waitForExistence(timeout: 5),
                      "a tree opened from the map has no back button, so the person is trapped")
        back.tap()
        // Explore is still in map mode, so the pill offers the way to the list.
        XCTAssertTrue(app.buttons["List"].waitForExistence(timeout: 5),
                      "back did not return to Explore's map")
    }

    /// Ticking a tree off is the product's own verb and the moment the account
    /// is asked for, so it must survive the tap rather than only compile.
    ///
    /// Asserted unconditionally. The first version wrapped everything in
    /// `if tick.waitForExistence`, so when the button could not be found the
    /// test passed while proving nothing, and it sat green through a day in
    /// which the thing it covers was never once exercised.
    @MainActor
    func testTickingATreeKeepsIt() throws {
        let app = launch(["-map"])

        let firstCard = app.buttons.matching(identifier: "tree-card").firstMatch
        XCTAssertTrue(firstCard.waitForExistence(timeout: 12))
        firstCard.tap()

        // By the label the button actually carries, not by the symbol's name.
        let tick = app.buttons["I have stood in front of this tree"]
        XCTAssertTrue(tick.waitForExistence(timeout: 6), "no tick button on the tree page")
        tick.tap()

        XCTAssertTrue(app.buttons["Ticked off. Tap to undo"].waitForExistence(timeout: 5)
                      || app.staticTexts["That one is yours"].waitForExistence(timeout: 5),
                      "ticking a tree left no visible trace")
    }

    /// Tapping the tab you are already on goes back to the top of it. This is
    /// the reason every NavigationLink in the app became a value on 2026-08-20,
    /// so it is the thing that has to be asserted rather than assumed.
    @MainActor
    func testTappingTheActiveTabGoesBackToTheTop() throws {
        let app = launch(["-map"])

        let firstCard = app.buttons.matching(identifier: "tree-card").firstMatch
        XCTAssertTrue(firstCard.waitForExistence(timeout: 10))
        firstCard.tap()
        XCTAssertTrue(app.buttons["Take me there"].waitForExistence(timeout: 5),
                      "a tree page did not open")

        app.tabBars.buttons["Explore"].tap()
        XCTAssertTrue(app.staticTexts["Near you"].waitForExistence(timeout: 5),
                      "tapping the active tab did not return to the map")
    }

    /// Panning the map has to move the list under it, which is the one thing in
    /// this app that cannot be checked from a screenshot: it only happens after
    /// a finger has dragged something.
    @MainActor
    func testPanningTheMapMovesTheList() throws {
        let app = launch(["-map"])
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

    /// The sheet and the list handing the gesture back and forth, which is the
    /// one interaction in this app that cannot be seen in a screenshot and that
    /// Hidde found broken twice in a row: first dragging up scrolled the trees
    /// instead of raising the sheet, then dragging down scrolled instead of
    /// lowering it. Measured by where the search field sits: high on the screen
    /// means the sheet is open, low means it is back at its peek.
    @MainActor
    func testTheSheetAndTheListTakeTurns() throws {
        let app = launch(["-map"])
        let field = app.textFields.firstMatch
        XCTAssertTrue(field.waitForExistence(timeout: 12), "no search field in the sheet")

        let peekY = field.frame.origin.y
        let screen = app.frame.height

        // Anchored on the search field rather than on a point in the list: a
        // drag that starts on a tree card can be taken as a tap and open the
        // tree, which is what happened the first time this was written. The
        // field is inside the same scrolling content, so it tests the same
        // thing and cannot navigate anywhere.
        //
        // And a long press before the drag, so nothing is read as a flick.
        field.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
             .press(forDuration: 0.35,
                    thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.12)))
        let openY = field.frame.origin.y
        XCTAssertLessThan(openY, peekY - screen * 0.2,
                          "dragging up over the list did not raise the sheet")

        // And back down from the top of the list, which is the half that was
        // still missing.
        field.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
             .press(forDuration: 0.35,
                    thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.92)))
        XCTAssertGreaterThan(field.frame.origin.y, openY + screen * 0.2,
                             "dragging down from the top of the list did not lower the sheet")
    }

    /// Home is built out of the website's own collections, which reach the
    /// app through /api/browse.json. If that feed ever stops carrying them the
    /// screen quietly loses most of itself, and a screenshot of the top of it
    /// would not show that at all.
    @MainActor
    func testHomeCarriesTheCollections() throws {
        let app = launch(["-tab=0"])
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

    /// The bar Hidde set on 2026-08-20, evening: five slots, and the middle one
    /// is a button rather than a place. Selecting Spot must present the sheet
    /// and leave the bar exactly where it was, because a "tab" that steals the
    /// selection strands the person on a screen that does not exist.
    @MainActor
    func testFiveSlotBar() throws {
        let app = launch()
        for label in ["Explore", "Saved", "Spot", "Collect", "Profile"] {
            XCTAssertTrue(app.tabBars.buttons[label].waitForExistence(timeout: 10),
                          "tab \(label) is missing from the bar")
        }
        app.tabBars.buttons["Spot"].tap()
        XCTAssertTrue(app.otherElements["spot-sheet"].waitForExistence(timeout: 5),
                      "selecting Spot did not present the sheet")
        app.swipeDown(velocity: .fast)
        XCTAssertTrue(app.tabBars.buttons["Explore"].waitForExistence(timeout: 5))
        XCTAssertTrue(app.tabBars.buttons["Explore"].isSelected,
                      "Spot took the selection with it; the bar must stay where it was")
    }

    /// Spot's whole design is that it never has a dead state: near our trees
    /// it offers ticking WITH the add-path beneath; in the middle of nowhere
    /// it offers the add-form as the headline.
    @MainActor
    func testSpotAlwaysOffersBothOutcomes() throws {
        let app = XCUIApplication()
        app.launchArguments = ["-at=52.3667,4.9086", "-spot"]   // Wertheimpark gate
        app.launch()
        XCTAssertTrue(app.staticTexts["Which tree did you find?"].waitForExistence(timeout: 10),
                      "no tick list next to a tree we map")
        XCTAssertTrue(app.staticTexts["Standing before a tree we miss?"].exists,
                      "the add-path is missing from the tick list")

        let far = XCUIApplication()
        far.launchArguments = ["-at=52.03,5.91", "-spot"]       // a field near Arnhem
        far.launch()
        XCTAssertTrue(far.staticTexts["No tree on our map here"].waitForExistence(timeout: 10),
                      "the add-form is not the headline where we map nothing")
        XCTAssertTrue(far.buttons["Send it in"].exists)
    }

    /// The pill is the only door between Explore's two faces, so it has to
    /// actually swap them: shelves to map, and back.
    @MainActor
    func testPillSwapsListAndMap() throws {
        let app = launch(["-tab=0"])
        let pill = app.buttons["explore-pill"]
        XCTAssertTrue(pill.waitForExistence(timeout: 10), "no pill on Explore")
        pill.tap()
        XCTAssertTrue(app.staticTexts["Near you"].waitForExistence(timeout: 8),
                      "the pill did not open the map")
        XCTAssertTrue(app.buttons["List"].exists, "the pill did not relabel to List")
        app.buttons["List"].tap()
        XCTAssertTrue(app.staticTexts["Our favourite tree cities"].waitForExistence(timeout: 8),
                      "the pill did not return to the shelves")
    }

    /// The sheet the whole account funnel runs through. If it does not present,
    /// nothing downstream of it can work, and it presented from a launch
    /// argument rather than a tap so that failure would be invisible.
    @MainActor
    func testTheSignInSheetPresents() throws {
        let app = launch(["-tab=4", "-signin"])
        XCTAssertTrue(app.staticTexts["That one is yours"].waitForExistence(timeout: 10),
                      "the sign-in sheet did not present")
        XCTAssertTrue(app.buttons["Email me a code"].exists,
                      "the email route is missing from the sign-in sheet")
    }
}
