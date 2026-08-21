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
    @MainActor
    private func raiseSheet(_ app: XCUIApplication) {
        // Tap, then WAIT for the cards to become touchable rather than
        // assuming the animation finished. Under a parallel test run the
        // 0.28 second spring can still be moving when the next tap lands,
        // which made this the suite's one flaky test.
        let card = app.buttons.matching(identifier: "tree-card").firstMatch
        for _ in 0..<3 {
            app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.88)).tap()
            if card.waitForExistence(timeout: 4), card.isHittable { return }
        }
    }

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
        let app = launch(["-map"])
        raiseSheet(app)

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
        let app = launch(["-map"])
        raiseSheet(app)
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
    /// Asserted on the LIST rather than on a chip. The "Trees in this area"
    /// chip used to be the tell, and it was deleted on 2026-08-21 for spending
    /// the best strip of the screen saying what the screen already is.
    @MainActor
    func testPanningTheMapMovesTheList() throws {
        let app = launch(["-map"])
        let firstCard = app.buttons.matching(identifier: "tree-card").firstMatch
        XCTAssertTrue(firstCard.waitForExistence(timeout: 12), "no list under the map")
        let before = firstCard.label

        let map = app.otherElements.firstMatch
        for _ in 0..<5 {
            map.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.22))
               .press(forDuration: 0.05,
                      thenDragTo: map.coordinate(withNormalizedOffset: CGVector(dx: 0.05, dy: 0.22)))
        }

        let changed = NSPredicate(format: "label != %@", before)
        expectation(for: changed, evaluatedWith: firstCard)
        waitForExpectations(timeout: 10) { err in
            XCTAssertNil(err, "the map was panned away and the list did not follow")
        }
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

        let screen = app.frame.height
        // The sheet opens at its peek, which is the lower part of the screen.
        // Asserted outright, because the CI's only record of this test on
        // 2026-08-21 was "70.5 is not less than 43.0": the field had been
        // read at y=176 on a 667 point phone before anything was dragged, and
        // a relative assertion turned that into a riddle. If the sheet ever
        // opens high again, this line says so in words.
        let peekY = settledY(of: field)
        XCTAssertGreaterThan(peekY, screen * 0.45,
                             "the sheet did not open at its peek: the search field sits at "
                             + "y=\(peekY) on a \(screen) point screen")

        // Anchored on the search field rather than on a point in the list: a
        // drag that starts on a tree card can be taken as a tap and open the
        // tree, which is what happened the first time this was written. The
        // field is inside the same scrolling content, so it tests the same
        // thing and cannot navigate anywhere.
        //
        // And a long press before the drag, so nothing is read as a flick.
        //
        // Every gesture starts from a SETTLED frame (settledY above and
        // below). The sheet springs for 0.28 seconds after a drag, and a press
        // aimed at where the field was a frame ago lands on the card that has
        // moved under it, which opens the tree and ends the test on a page
        // with no search field at all (the SE, 2026-08-21).
        field.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
             .press(forDuration: 0.35,
                    thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.12)))
        let openY = settledY(of: field)
        XCTAssertLessThan(openY, screen * 0.3,
                          "dragging up over the list did not raise the sheet: the field went from "
                          + "y=\(peekY) to y=\(openY) on a \(screen) point screen")

        // And back down from the top of the list, which is the half that was
        // still missing.
        field.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
             .press(forDuration: 0.35,
                    thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.92)))
        let downY = settledY(of: field)
        XCTAssertGreaterThan(downY, screen * 0.45,
                             "dragging down from the top of the list did not lower the sheet: the field "
                             + "went from y=\(openY) to y=\(downY) on a \(screen) point screen")
    }

    /// The element's y once it has stopped moving: two reads 0.4 seconds
    /// apart that agree. Returns -1 when the element is gone, so a caller's
    /// assertion fails with a number rather than with "no matching snapshot",
    /// which is what reading the frame of a vanished element produces.
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
        app.launchArguments = ["-at=52.3667,4.9086", "-reset-collection", "-begin=amsterdam|Plantage"]
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
        let app = launch(["-tab=4", "-signin"])
        XCTAssertTrue(app.staticTexts["That one is yours"].waitForExistence(timeout: 10),
                      "the sign-in sheet did not present")
        XCTAssertTrue(app.buttons["Email me a code"].exists,
                      "the email route is missing from the sign-in sheet")
    }
}
