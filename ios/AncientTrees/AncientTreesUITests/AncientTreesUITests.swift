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
        app.launchArguments = ["-at=52.3731,4.8922", "-reset-collection", "-reset-blocks"] + args
        app.launch()
        return app
    }

    /// Every map you can pan carries the control that puts it back: you in the
    /// middle, north at the top.
    ///
    /// This is a ratchet rather than a nicety. The control has now gone missing
    /// twice, once by sitting behind the sheet (2026-08-24, "de knop mist waar
    /// je naar je locatie gaat") and once by defaulting to off, which left it on
    /// the map tab and the walk mode and on none of the other eight maps here
    /// (2026-08-29, "die moet overal waar je de kaart gebruikt aanwezig zijn").
    /// Both times it was invisible to every other gate we have, because a
    /// missing control breaks no build, fails no layout rule and photographs
    /// as a perfectly good map.
    ///
    /// The two previews left out of this list are left out on purpose: the city
    /// and country pages draw a map that takes no taps and opens the real one.
    @MainActor
    func testEveryPannableMapCarriesTheRecentreControl() throws {
        let screens: [(String, [String])] = [
            ("the map tab", ["-tab=0"]),
            ("a city's map", ["-tab=0", "-open=citymap:aarhus"]),
            ("a tree's own map", ["-tab=0", "-open=treemap:ath_004"]),
            ("a walk", ["-tab=0", "-open=walk:aarhus|Moesg\u{00e5}rd / H\u{00f8}jbjerg"]),
            ("the pin picker", ["-tab=0", "-open=tree:ath_004", "-placepin"]),
        ]
        for (what, args) in screens {
            let app = launch(args)
            let recentre = app.buttons["map-recentre"]
            XCTAssertTrue(recentre.waitForExistence(timeout: 20),
                          "no way back to your own location on \(what)")
            app.terminate()
        }
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
        // The bar is a SwiftUI view, so `app.tabBars` finds nothing (2026-08-25).
        XCTAssertTrue(app.buttons["Map"].waitForExistence(timeout: 5),
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

        // And the way back down, which is the DRAG again: the floating Map
        // button was removed on 2026-08-25 ("de map floating knop op de map
        // pagina is overbodig"), so the gesture is the only way and therefore
        // the thing worth asserting. The list has to be at its top for the
        // sheet to take the drag, which it is here because nothing scrolled it.
        count.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
             .press(forDuration: 0.35,
                    thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.92)))
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

    /// The bar: THREE destinations, and the camera is a separate BUTTON beside
    /// it rather than a slot inside it.
    ///
    /// This asserted five slots (Map, Explore, camera, Collection, Profile)
    /// until 2026-08-26, when Hidde pulled the camera out onto its own disc,
    /// Polarsteps-style, and folded Profile into the Collection tab as "My
    /// trees" (TabBar.swift). Explore became Discover the same day. The old
    /// five-slot assertion had been failing against an app that was right,
    /// caught only when the app's own CI run was read rather than assumed
    /// green.
    @MainActor
    func testThreeTabsAndCollectButton() throws {
        let app = launch(["-signed-in"])
        for label in ["Map", "Discover", "My trees"] {
            XCTAssertTrue(app.buttons[label].waitForExistence(timeout: 12),
                          "tab \(label) is missing from the bar")
        }
        XCTAssertTrue(app.buttons["Collect a tree"].exists,
                      "the camera button beside the bar is gone")

        app.buttons["Collect a tree"].tap()
        XCTAssertTrue(app.descendants(matching: .any)["spot-sheet"].waitForExistence(timeout: 6),
                      "the camera button did not present the collect sheet")
        app.buttons["spot-close"].tap()
        XCTAssertTrue(app.buttons["Map"].waitForExistence(timeout: 6))
        XCTAssertTrue(app.buttons["Map"].isSelected,
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
        XCTAssertTrue(app.staticTexts["Build your tree collection"].waitForExistence(timeout: 12),
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
        let app = launch(["-tab=2"])
        XCTAssertTrue(app.otherElements["collect-mission"].waitForExistence(timeout: 12),
                      "no mission on the collection's day zero")
        XCTAssertFalse(app.staticTexts["Species collected"].exists,
                       "the empty stamp grid renders before the first tick")
        // The camera in the middle of the bar, which is the way to collect a
        // tree from anywhere in the app. The screen's own line about
        // photographing was removed on 2026-08-25 at Hidde's ask, and asserting
        // a button he deleted would keep a removed thing alive in a test.
        XCTAssertTrue(app.buttons["Collect a tree"].exists,
                      "there is no way to collect a tree from the collection")
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
    ///
    /// WHAT THE TICK DOES CHANGED on 2026-08-25: it opens the camera rather
    /// than ticking off a tap, because Hidde ruled that standing in front of a
    /// tree is claimed with a photograph or not at all. A simulator has no
    /// camera, so the test asserts the two halves separately: the counter reads
    /// the collection it was given, and the control opens the collect sheet.
    @MainActor
    func testBeginWalksTheWalk() throws {
        let app = XCUIApplication()
        // Clean, like every launch: on the shared simulator a tick from an
        // earlier test otherwise starts this walk at "1 of 7".
        // -no-nudge because this test is about the WALK, not about the
        // sign-in ask, and -signed-in because since 2026-08-25 collecting
        // without an account opens that sheet instead.
        // ams_018 is the Plantage walk's first stop, seeded as collected so the
        // counter has something true to say.
        app.launchArguments = ["-at=52.3667,4.9086", "-reset-collection", "-no-nudge",
                               "-signed-in", "-collected=ams_018",
                               "-begin=amsterdam|Plantage"]
        app.launch()

        XCTAssertTrue(app.otherElements["walk-mode"].waitForExistence(timeout: 14),
                      "Begin did not open the walk")

        // The counter is the walk's visible state and it has to read the
        // collection rather than a number somebody typed. The total is read,
        // not written down: it said 14 for two days after Amsterdam lost five
        // trees to the ticket ruling.
        let progress = app.staticTexts.matching(
            NSPredicate(format: "label CONTAINS 'ticked off'")).firstMatch
        XCTAssertTrue(progress.waitForExistence(timeout: 8), "the walk shows no progress line")
        let parts = progress.label.components(separatedBy: " ")
        XCTAssertEqual(parts.first, "1",
                       "the walk ignored the tree it was told is collected: \(progress.label)")
        let total = Int(parts.count > 2 ? parts[2] : "") ?? 0
        XCTAssertTrue(total > 1, "could not read the walk's total from \(progress.label)")

        // By the words on it. An identifier on a Button whose label is an
        // HStack of Spacers does not always survive into the query tree, and a
        // test that cannot find the button it is about proves nothing.
        let tick = app.buttons.matching(
            NSPredicate(format: "label CONTAINS 'standing before it'")).firstMatch
        XCTAssertTrue(tick.waitForExistence(timeout: 8), "no tick in the walk")
        tick.tap()
        XCTAssertTrue(app.descendants(matching: .any)["spot-sheet"].waitForExistence(timeout: 8),
                      "standing before a tree did not open the camera")
        app.buttons["spot-close"].tap()

        app.buttons["walk-close"].tap()
        XCTAssertTrue(app.buttons["Map"].waitForExistence(timeout: 8),
                      "leaving the walk did not return to the app")
    }

    /// A PIN OPENS ITS TREE, asserted by tapping the map.
    ///
    /// This is the test that should have existed from the day the map was
    /// ported: `handleTap` was written and never installed, so tapping a pin or
    /// a cluster did nothing for weeks and every check we had went green,
    /// because a gesture that is never recognised leaves no trace in a
    /// screenshot or in an element tree (2026-08-25).
    ///
    /// It taps down the map's centre column rather than at one computed pixel:
    /// the camera sits above the view's centre by whatever the sheet's inset is,
    /// and pinning this test to that arithmetic would make it fail the next time
    /// the sheet's heights change. Somewhere on that column is the tree the map
    /// was told to centre on.
    @MainActor
    func testTappingAPinOpensItsTree() throws {
        let app = launch(["-map", "-select=ams_002"])
        let map = app.otherElements["tree-map"]
        XCTAssertTrue(map.waitForExistence(timeout: 14), "no map")
        // Let the tiles and the pins arrive. Where the camera ends up does not
        // matter to this test any more; that it has drawn pins does.
        Thread.sleep(forTimeInterval: 5)

        // A GRID, not a column, and the reason is worth writing down because
        // the column version cost an hour on 2026-08-27.
        //
        // Its premise was that the camera has settled on the selected tree, so
        // the tree is somewhere down the middle. A screenshot taken from inside
        // the test showed that premise is not reliable: the map was still wide
        // open with Diemen and Amstelveen in frame, and the middle column ran
        // between the clusters. Meanwhile tapping a pin by hand opened its tree
        // perfectly, which is what this test is actually about.
        //
        // So it no longer cares where the camera is. It sweeps the visible map
        // and passes when a pin opens a tree: what is asserted is that a pin is
        // a control, not that the camera framed one particular trunk. A tap on
        // a cluster zooms in instead, which only makes the next rows likelier
        // to land.
        for row in 0...10 {
            for dx in [0.5, 0.28, 0.72] {
                let dy = 0.16 + Double(row) * 0.03
                map.coordinate(withNormalizedOffset: CGVector(dx: dx, dy: dy)).tap()
                if app.buttons["Take me there"].waitForExistence(timeout: 0.5) {
                    return
                }
            }
        }
        let shot = XCTAttachment(screenshot: XCUIScreen.main.screenshot())
        shot.name = "the-map-that-would-not-open-a-tree"
        shot.lifetime = .keepAlways
        add(shot)
        XCTFail("sweeping the visible map opened no tree at all")
    }

    /// THE MAP, DRIVEN, several times over, because he asked for exactly that.
    ///
    /// Hidde, 2026-08-25: "oprecht er gaat zoveel mis als je scrolt klikt en de
    /// lijst omhoog en naar beneden klikt, ik weet niet zo goed waar ik moet
    /// beginnen, kan je deze interactie zelf een paar keer doorlopen testen?"
    ///
    /// Every other test here checks one thing once. This one does the sequence a
    /// person actually performs, twice, and asserts after every step: raise the
    /// sheet, scroll the list, drag it back down, open a card, come back, raise
    /// it again. The bugs he keeps finding live in the SECOND lap, where a
    /// gesture leaves state behind that the first lap never saw.
    @MainActor
    func testTheMapSurvivesBeingUsed() throws {
        let app = launch(["-map", "-signed-in"])
        let count = app.staticTexts["map-count"]
        XCTAssertTrue(count.waitForExistence(timeout: 14), "no count on the sheet")
        let screen = app.frame.height

        for lap in 1...2 {
            // START LOW. Coming back from a tree page leaves the sheet where you
            // left it, which is right (Google Maps does the same) and means lap
            // two does not start where lap one did. The lap has to put it back
            // rather than assume.
            if settledY(of: count) < screen * 0.6 {
                count.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
                     .press(forDuration: 0.35,
                            thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.95)))
            }
            // UP, by dragging the lip.
            let low = settledY(of: count)
            XCTAssertGreaterThan(low, screen * 0.6,
                                 "lap \(lap): the sheet did not start at its lip")
            count.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
                 .press(forDuration: 0.35,
                        thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.12)))
            let high = settledY(of: count)
            XCTAssertLessThan(high, low - 40,
                              "lap \(lap): dragging the lip up did not raise the sheet "
                              + "(\(low) to \(high) on \(screen))")

            // SCROLL the list, which is the state that used to trap the sheet.
            let firstCard = app.buttons.matching(identifier: "tree-card").firstMatch
            XCTAssertTrue(firstCard.waitForExistence(timeout: 8),
                          "lap \(lap): no card in the raised sheet")
            app.swipeUp()

            // DOWN AGAIN, from the header, which is the grip that has to work
            // whatever the list is doing.
            count.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
                 .press(forDuration: 0.35,
                        thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.95)))
            let backDown = settledY(of: count)
            XCTAssertGreaterThan(backDown, high + 40,
                                 "lap \(lap): the sheet would not come down after the list "
                                 + "had been scrolled (\(high) to \(backDown) on \(screen))")

            // AND A CARD STILL OPENS, from the raised sheet.
            count.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
                 .press(forDuration: 0.35,
                        thenDragTo: app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.12)))
            let card = app.buttons.matching(identifier: "tree-card").firstMatch
            XCTAssertTrue(card.waitForExistence(timeout: 8), "lap \(lap): no card to open")
            card.tap()
            XCTAssertTrue(app.buttons["Take me there"].waitForExistence(timeout: 8),
                          "lap \(lap): tapping a card did not open the tree")
            app.navigationBars.buttons.firstMatch.tap()
            XCTAssertTrue(count.waitForExistence(timeout: 8),
                          "lap \(lap): coming back from a tree lost the map's sheet")
        }
    }

    /// The lane picker on Collection, tapped both ways.
    ///
    /// Hidde has now reported twice that he cannot get back to the first lane
    /// once he is on the second (2026-08-24 and again 2026-08-25). The first
    /// fix was made without a finger to test it with, which is how a fix ships
    /// that does not fix anything. This is the finger. The labels became "My
    /// trees" and "Favourites" on 2026-08-26 (Collect.swift); the switching
    /// bug they were guarding against is unchanged.
    @MainActor
    func testTheCollectionLanePickerSwitchesBothWays() throws {
        let app = launch(["-tab=2", "-signed-in", "-collected=ams_001,ams_002"])
        let picker = app.segmentedControls["collect-lane"]
        XCTAssertTrue(picker.waitForExistence(timeout: 12), "no lane picker on Collection")

        let seen = picker.buttons["My trees"]
        let want = picker.buttons["Favourites"]
        XCTAssertTrue(want.exists && seen.exists, "the two lanes are not both there")

        seen.tap()
        XCTAssertTrue(seen.isSelected, "tapping My trees did not select it")

        want.tap()
        XCTAssertTrue(want.isSelected,
                      "tapping Favourites from My trees did not select it")
        // And the tap must not have opened a tree instead, which is the other
        // half of what he described.
        XCTAssertFalse(app.buttons["Take me there"].exists,
                       "the lane tap opened a tree page underneath it")
    }

    /// The sheet the whole account funnel runs through. If it does not present,
    /// nothing downstream of it can work, and it presented from a launch
    /// argument rather than a tap so that failure would be invisible.
    @MainActor
    func testTheSignInSheetPresents() throws {
        let app = launch(["-tab=2", "-signin"])
        XCTAssertTrue(app.staticTexts["That one is yours"].waitForExistence(timeout: 10),
                      "the sign-in sheet did not present")
        XCTAssertTrue(app.buttons["Email me a code"].exists,
                      "the email route is missing from the sign-in sheet")
    }

    /// A DRAG THAT STARTS ON A CARD MOVES THE SHEET AND OPENS NOTHING.
    ///
    /// This is UIScrollView's rule, which every list in iOS has followed since
    /// 2007: the moment a touch becomes a drag, the control under it stops
    /// being pressed. Our sheet has its own drag gesture, so it does not come
    /// free, and a NavigationLink fires on release however far the finger
    /// travelled, because a card is two hundred points tall and the finger
    /// never leaves it.
    ///
    /// Hidde found it twice: first on the name row in the header, then, when
    /// only that was fixed, with the question that mattered ("heb je dit
    /// doorgevoerd overal waar dit component wordt gebruikt, dat is meer dan 1
    /// plek"). It is asserted here because the first attempted fix, turning off
    /// hit testing during the drag, looked right and did nothing at all: a
    /// press SwiftUI has already begun is not cancelled by refusing later
    /// touches.
    @MainActor
    func testDraggingFromACardRaisesTheSheetRatherThanOpeningIt() throws {
        let app = launch(["-tab=0"])
        XCTAssertTrue(app.staticTexts.firstMatch.waitForExistence(timeout: 20))
        // Raise it off peek, where the sheet takes no taps at all.
        app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.88)).tap()
        Thread.sleep(forTimeInterval: 1.0)

        // .descendants rather than .otherElements: a SheetLink is a plain view
        // with a tap on it, so what type XCUITest files it under is not ours
        // to assume.
        let card = app.descendants(matching: .any)
            .matching(identifier: "tree-card").firstMatch
        XCTAssertTrue(card.waitForExistence(timeout: 10), "no card in the sheet to drag from")
        // A real drag, starting on the card: down the middle of it and well
        // past the sheet's own 18 point threshold.
        card.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
            .press(forDuration: 0.05,
                   thenDragTo: card.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: -1.5)))
        Thread.sleep(forTimeInterval: 1.2)

        XCTAssertFalse(app.buttons["Take me there"].exists,
                       "dragging the sheet by a card opened the tree underneath it")
    }

    /// THE LAUNCH PROMISE: the app ships free with no reference to Plus
    /// anywhere (DECISIONS.md 2026-08-26, held by Kit/Launch.swift).
    ///
    /// Hidde, 2026-08-27, having found a shelf of gold Plus chips on every
    /// city page: "kun je een sweep doen dat je 100% zeker bent dat plus in
    /// deze build niet wordt meegenomen". A flag is only as good as the
    /// screens that read it, and that one did not: Explore and the map both
    /// checked Launch.walks and the city page, written from the same shelf,
    /// never got the check. Nothing could catch it, because the screenshot
    /// sweep photographs a city page and the shelf sat below the fold.
    ///
    /// So it is asserted rather than remembered, on every screen a person can
    /// reach, and it fails the build in CI. Flipping the flag for real users is
    /// the Plus introduction and is Hidde's call; this test is what makes the
    /// flag mean something in between.
    @MainActor
    func testNothingInTheAppSaysPlus() throws {
        let screens: [[String]] = [
            ["-tab=0"],
            ["-tab=1"],
            ["-tab=2", "-signed-in", "-collected=ams_001,ams_002"],
            ["-tab=2", "-settings"],
            ["-tab=0", "-open=city:amsterdam"],
            ["-tab=0", "-open=tree:ath_004"],
            ["-tab=0", "-open=collection:ancient-oaks-of-europe"],
            ["-tab=0", "-open=species:Aleppo Pine"],
        ]
        for args in screens {
            let app = launch(args)
            // Wait for the catalogue: 2.5 MB of JSON, and until it is read
            // there is nothing on screen to find, so an unwaited assertion
            // would pass on an empty window.
            XCTAssertTrue(app.staticTexts.firstMatch.waitForExistence(timeout: 20),
                          "nothing rendered for \(args)")
            XCTAssertFalse(app.staticTexts["Plus"].exists,
                           "a Plus chip is on screen with \(args)")
            app.terminate()
        }
    }
}
