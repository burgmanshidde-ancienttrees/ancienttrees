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
        // Portrait, every time. The launch tests run once per UI
        // configuration, landscape included, and since the suite runs on one
        // simulator rather than throwaway clones (2026-08-21) the last
        // orientation stays: a sheet test then found no search field and a
        // walk's tick landed beside its button, on the SE only.
        XCUIDevice.shared.orientation = .portrait
        // And light, for the same reason: the dark configuration sticks too,
        // and every screenshot a failure leaves behind should look like the
        // app Hidde sees.
        XCUIDevice.shared.appearance = .light
    }

    /// At peek the sheet takes no taps, by design since 2026-08-21: a finger
    /// there belongs to the sheet so a swipe up raises it instead of opening
    /// whatever card it started on. So a test that wants a card raises the
    /// sheet first, exactly as a person does.
    private func launch(_ args: [String] = []) -> XCUIApplication {
        let app = XCUIApplication()
        // A fixed origin keeps the test off the location permission dialog and
        // makes the list deterministic: Amsterdam always has trees near it.
        // And a clean collection, because serial testing shares one simulator
        // across every test and a tick left by one would greet the next.
        app.launchArguments = ["-at=52.3731,4.8922", "-reset-collection"] + args
        app.launch()
        return app
    }

    /// Hiding the map's navigation bar must not hide the pushed page's.
    @MainActor
    func testTreePageFromTheMapHasAWayBack() throws {
        let app = launch(["-map", "-sheet=full"])

        // The sheet's first card, whatever tree it happens to be today.
        let firstCard = app.buttons.matching(identifier: "tree-card").firstMatch
        XCTAssertTrue(firstCard.waitForExistence(timeout: 10), "no tree card in the map sheet")
        firstCard.tap()

        // Whatever it is called, there has to be something that goes back.
        let back = app.navigationBars.buttons.firstMatch
        XCTAssertTrue(back.waitForExistence(timeout: 5),
                      "a tree opened from the map has no back button, so the person is trapped")
        back.tap()
        XCTAssertTrue(app.tabBars.buttons["Map"].waitForExistence(timeout: 5),
                      "back did not return to the map tab")
    }

    /// Collecting is something you do standing in front of the tree, so the
    /// tree PAGE cannot do it (Hidde, 2026-08-21: "die collect-knop die ik
    /// zomaar aan kan klikken, die moet daar weg"). The page keeps the heart,
    /// which is a wish rather than a claim; the tick lives in Spot, where
    /// being near is what puts a tree in front of you.
    @MainActor
    func testATreePageCannotCollectForYou() throws {
        let app = launch(["-map", "-sheet=full"])
        let firstCard = app.buttons.matching(identifier: "tree-card").firstMatch
        XCTAssertTrue(firstCard.waitForExistence(timeout: 12))
        firstCard.tap()
        XCTAssertTrue(app.buttons["Take me there"].waitForExistence(timeout: 6),
                      "a tree page did not open")

        XCTAssertFalse(app.buttons["I have stood in front of this tree"].exists,
                       "the tree page still collects for you")
        XCTAssertTrue(app.buttons.matching(
            NSPredicate(format: "label BEGINSWITH 'Save '")).firstMatch.exists,
                      "the heart went with the tick; it should not have")
    }

    /// Panning the map has to move the list under it, which is the one thing in
    /// this app that cannot be checked from a screenshot: it only happens after
    /// a finger has dragged something.
    ///
    /// Asserted on the COUNT since 2026-08-22, because the count IS the list's
    /// visible state at the sheet's lip and it leaves the map uncovered for the
    /// drag. Earlier versions read the first card, which needed the sheet open,
    /// which covered the map the test had to drag.
    @MainActor
    func testPanningTheMapMovesTheList() throws {
        let app = launch(["-map"])
        let count = app.staticTexts["map-count"]
        XCTAssertTrue(count.waitForExistence(timeout: 12), "no count under the map")
        let before = count.label

        // The map BY NAME. app.otherElements.firstMatch used to be the map and
        // is not any more now that a search field and a chip row float over it,
        // so the drag was landing on whatever the query tree happened to list
        // first.
        let map = app.descendants(matching: .any)["tree-map"]
        XCTAssertTrue(map.waitForExistence(timeout: 6), "no map to pan")
        for _ in 0..<6 {
            map.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.35))
               .press(forDuration: 0.05,
                      thenDragTo: map.coordinate(withNormalizedOffset: CGVector(dx: 0.05, dy: 0.35)))
        }

        let changed = NSPredicate(format: "label != %@", before)
        expectation(for: changed, evaluatedWith: count)
        waitForExpectations(timeout: 12) { err in
            XCTAssertNil(err, "the map was panned away and the count still says \(before)")
        }
    }

    /// The sheet and the list handing the gesture back and forth, which is the
    /// one interaction in this app that cannot be seen in a screenshot and that
    /// Hidde found broken three times in a row.
    ///
    /// Anchored on the COUNT STRIP since 2026-08-22, which is the whole of the
    /// sheet at its lowest: Komoot's layout put the search field at the top of
    /// the map and left the lip saying only how many trees are under the view.
    /// That is also why this now cannot fail the way it kept failing: at peek
    /// there is nothing tappable in the sheet at all.
    @MainActor
    func testTheSheetAndTheListTakeTurns() throws {
        let app = launch(["-map"])
        let count = app.staticTexts["map-count"]
        XCTAssertTrue(count.waitForExistence(timeout: 12), "no count on the sheet's lip")

        let screen = app.frame.height
        let peekY = settledY(of: count)
        XCTAssertGreaterThan(peekY, screen * 0.6,
                             "the sheet did not open at its lip: the count sits at "
                             + "y=\(peekY) on a \(screen) point screen")

        count.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
             .press(forDuration: 0.35,
                    thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.12)))
        let openY = settledY(of: count)
        XCTAssertLessThan(openY, screen * 0.35,
                          "dragging the lip up did not raise the sheet: the count went from "
                          + "y=\(peekY) to y=\(openY) on a \(screen) point screen")

        // And the way back down, which is a button now rather than only a drag.
        let back = app.buttons["back-to-map"]
        if back.waitForExistence(timeout: 3) {
            back.tap()
        } else {
            count.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
                 .press(forDuration: 0.35,
                        thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.92)))
        }
        let downY = settledY(of: count)
        XCTAssertGreaterThan(downY, screen * 0.6,
                             "the sheet did not go back down: the count went from "
                             + "y=\(openY) to y=\(downY) on a \(screen) point screen")
    }

    /// The frame of something that may still be springing. Every gesture in
    /// these tests starts from a SETTLED frame: the sheet animates for 0.28
    /// seconds, and a press aimed at where an element was a frame ago lands on
    /// whatever has moved under it.
    private func settledY(of el: XCUIElement, timeout: TimeInterval = 6) -> CGFloat {
        let end = Date().addingTimeInterval(timeout)
        var last: CGFloat = -1
        while Date() < end {
            guard el.exists else { return -1 }
            let y = el.frame.origin.y
            if y == last { return y }
            last = y
            RunLoop.current.run(until: Date().addingTimeInterval(0.4))
        }
        return el.exists ? el.frame.origin.y : -1
    }

    /// Searching for somewhere has to MOVE the map. It did not: `region` is a
    /// binding the map fills in when a finger moves it, and nothing ever read
    /// it back, so picking Barcelona set a number in SwiftUI and left the map
    /// over Amsterdam (Hidde, 2026-08-22, who typed exactly that).
    @MainActor
    func testSearchingForATreeMovesTheMapToIt() throws {
        let app = launch(["-map", "-search=beethoven"])
        let row = app.buttons.matching(
            NSPredicate(format: "label CONTAINS[c] 'Beethoven'")).firstMatch
        XCTAssertTrue(row.waitForExistence(timeout: 12), "search found no Beethoven Plane")
        row.tap()

        // The map selects it, and the sheet shows that tree rather than
        // whatever was nearest where we started.
        XCTAssertTrue(app.staticTexts["The Beethoven Plane"].waitForExistence(timeout: 8)
                      || app.buttons.matching(
                          NSPredicate(format: "label CONTAINS[c] 'Beethoven'")).firstMatch
                          .waitForExistence(timeout: 8),
                      "picking a tree in search did not take the map to it")
    }

    /// The bar: four slots, and the middle one is a BUTTON rather than a
    /// place. Restored on 2026-08-22 after a careless block replacement took
    /// this and two others out with it, which nothing noticed because a
    /// deleted test does not fail.
    @MainActor
    func testFourSlotBar() throws {
        let app = launch()
        for label in ["Map", "Explore", "Collect", "Yours"] {
            XCTAssertTrue(app.tabBars.buttons[label].waitForExistence(timeout: 12),
                          "tab \(label) is missing from the bar")
        }
        XCTAssertFalse(app.tabBars.buttons["Profile"].exists,
                       "Profile is a tab again; it belongs in the corner")

        app.tabBars.buttons["Collect"].tap()
        XCTAssertTrue(app.descendants(matching: .any)["spot-sheet"].waitForExistence(timeout: 6),
                      "selecting Collect did not present the sheet")
        app.buttons["spot-close"].tap()
        XCTAssertTrue(app.tabBars.buttons["Map"].waitForExistence(timeout: 6))
        XCTAssertTrue(app.tabBars.buttons["Map"].isSelected,
                      "Collect took the selection with it; the bar must stay where it was")
    }

    /// ONE act, and the app decides what it was (Hidde, 2026-08-23: "add en
    /// collect zijn wel moeilijk uit te leggen"). The centre button never
    /// asks which kind of tree you are pointing at, because that is the one
    /// question the person holding the phone cannot answer. It opens on the
    /// camera, and the words add and collect appear only afterwards, as
    /// outcomes.
    @MainActor
    func testCollectAsksForAPhotographRatherThanAChoice() throws {
        let app = XCUIApplication()
        app.launchArguments = ["-at=52.3667,4.9086", "-reset-collection", "-collect"]
        app.launch()
        XCTAssertTrue(app.staticTexts["Collect a tree"].waitForExistence(timeout: 12),
                      "the centre button does not open on the collect intro")
        XCTAssertTrue(app.buttons["add-start"].exists,
                      "no way into the camera")
        XCTAssertFalse(app.staticTexts["Add a tree we do not have"].exists,
                       "the add/collect choice is back on the way in")
    }

    /// The fourth tab's day zero is a mission naming one real tree, never four
    /// zeros and a grid of grey ghosts.
    @MainActor
    func testCollectDayZeroShowsMission() throws {
        let app = launch(["-tab=3"])
        XCTAssertTrue(app.otherElements["collect-mission"].waitForExistence(timeout: 12),
                      "no mission on the collection's day zero")
        XCTAssertFalse(app.staticTexts["Species collected"].exists,
                       "the empty stamp grid renders before the first tick")
        XCTAssertTrue(app.buttons["collect-a-tree"].exists,
                      "Your trees has no way to collect a tree")
    }

    /// Explore is the feed, and the feed is the rows Hidde settled on
    /// 2026-08-21: cities, the oldest trees, countries, species, walks. The
    /// curated collections left with the season shelf; they stay on the
    /// website, which is where they earn their traffic.
    @MainActor
    func testExploreCarriesTheFeed() throws {
        let app = launch(["-tab=1"])
        XCTAssertTrue(app.staticTexts["Our favourite tree cities"].waitForExistence(timeout: 12),
                      "the cities shelf is missing")

        var found = Set<String>()
        let wanted = ["The oldest trees we map", "Tree countries", "By species"]
        for _ in 0..<10 where found.count < wanted.count {
            for w in wanted where app.staticTexts[w].exists { found.insert(w) }
            app.swipeUp(velocity: .fast)
        }
        XCTAssertEqual(found.count, wanted.count,
                       "Explore is missing \(Set(wanted).subtracting(found))")
    }

    /// Begin is the walk verb actually happening: full screen, the route, and
    /// a tick that advances to the next tree. It used to hand the person to
    /// Apple Maps, which ended our part of the afternoon.
    @MainActor
    func testBeginWalksTheWalk() throws {
        let app = XCUIApplication()
        // Clean, like every launch: on the shared simulator a tick from an
        // earlier test otherwise starts this walk at "1 of 14".
        // -no-nudge because this test is about the WALK, not about the
        // sign-in ask that a first tick correctly raises over it.
        app.launchArguments = ["-at=52.3667,4.9086", "-reset-collection", "-no-nudge",
                               "-begin=amsterdam|Plantage"]
        app.launch()

        XCTAssertTrue(app.otherElements["walk-mode"].waitForExistence(timeout: 12),
                      "Begin did not open the walk")
        // By the words on it. An identifier on a Button whose label is an
        // HStack of Spacers does not always survive into the query tree, and a
        // test that cannot find the button it is about proves nothing.
        let tick = app.buttons.matching(
            NSPredicate(format: "label CONTAINS 'standing before it'")).firstMatch
        XCTAssertTrue(tick.waitForExistence(timeout: 6), "no tick in the walk")

        // Ticking has to MOVE the walk on: the counter climbs and the card
        // names a different tree. A tick that only lit up would be a screen
        // pretending to be a walk.
        let progress = app.staticTexts.matching(NSPredicate(format: "label CONTAINS 'of 14 ticked off'")).firstMatch
        XCTAssertTrue(progress.waitForExistence(timeout: 6))
        let before = Int(progress.label.components(separatedBy: " ").first ?? "") ?? 0
        tick.tap()
        // The exact next count, not "a label without the old digit": the
        // runner started at 1, the tick took it to "2 of 14", and "14"
        // contains a 1, so the old predicate could never be satisfied.
        XCTAssertTrue(app.staticTexts["\(before + 1) of 14 ticked off"].waitForExistence(timeout: 6),
                      "ticking a tree did not advance the walk from \(before) of 14")

        app.buttons["walk-close"].tap()
        XCTAssertTrue(app.tabBars.buttons["Map"].waitForExistence(timeout: 6),
                      "leaving the walk did not return to the app")
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
