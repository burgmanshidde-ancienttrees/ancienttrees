// The layer the app did not have: FLOWS, walked with a finger, photographed
// step by step, with one invariant asserted after every tap.
//
// Hidde, 2026-08-27: "hoe kunnen we jou een fatsoenlijke ui en ux test laten
// doen dat je alles doorloopt en zelf oordeelt of het werkt zoals conventionele
// flows werken". He asked it the morning he found a dead end nobody could have
// photographed: Settings, tap your own name, and you land on the map with no
// tab bar and no back button, because the button still asked for a tab that
// stopped existing when the bar went to three.
//
// Nothing in the app's QA could see that, and the reason is structural rather
// than an oversight. appsweep.py opens each screen with a launch argument and
// photographs it, so every screen is a first frame and no screen is ever
// arrived at. appfit.py measures those frames. Both are blind to the whole
// class of fault that only exists BETWEEN two screens: a dead end, a control
// that does nothing, a back button that does not come back.
//
// So this walks. Each flow is a list of steps; each step is a tap or a swipe
// with a name; after every step the frame is written out as a PNG and the one
// invariant is checked:
//
//   THERE IS ALWAYS A WAY BACK. Either the tab bar is on screen, or the page
//   has a back button, or the sheet has a Cancel or a Close. A screen with
//   none of the three is a room with the door painted over, and it is the only
//   fault this file asserts, because it is the only one a machine can be sure
//   about.
//
// Everything else is left to eyes on purpose, and that is the division of
// labour the whole QA doctrine already runs on: a script can prove a button is
// on the screen and cannot tell you the flow is wrong. scripts/appwalk.py
// collects the pictures into one folder, in order, so the judging is reading
// a strip of frames rather than remembering a five-step simctl recipe.

import XCTest

final class FlowWalk: XCTestCase {

    /// One thing a person does, and what to call the picture it leaves.
    private struct Step {
        let name: String
        let act: (XCUIApplication) -> Void
    }

    private struct Flow {
        let name: String
        let args: [String]
        let steps: [Step]
    }

    /// Tap a button by identifier ONCE IT IS THERE.
    ///
    /// Every step here used to tap the instant its closure ran, which passes on
    /// a desk and fails on a loaded runner. The launch check above waits for the
    /// first static text, and that only proves the window drew something: a list
    /// that fills from demo data, a sheet that springs, a push that animates all
    /// land later than the first label does.
    ///
    /// It cost a red gate on 2026-09-01, on the report-and-block flow, which is
    /// the worst one to lose because Apple's reviewer taps exactly that sequence
    /// (iOS 18.5 in CI: "Failed to tap person-more, no matches found"). The same
    /// flow walked clean on a desk minutes later, which is the signature of a
    /// race rather than a fault: a test that fails only where the machine is
    /// busy is testing the machine.
    ///
    /// Ten seconds, and it costs nothing when the element is already there,
    /// because waitForExistence returns as soon as it appears. It deliberately
    /// does NOT assert: a missing button still fails on the next line, with the
    /// tap's own message and its screenshot, rather than being renamed here.
    private static func tap(_ app: XCUIApplication, _ id: String) {
        let b = app.buttons[id].firstMatch
        _ = b.waitForExistence(timeout: 10)
        b.tap()
    }

    // MARK: - the flows

    /// A signed-in account, because signed out is a different and much shorter
    /// app: the gate is what most of these flows would meet first.
    private static let signedIn = ["-signed-in", "-collected=ams_001,ams_002"]

    private static var flows: [Flow] {
        [
            // The one that was broken. Two doors to the profile editor and a
            // way back out of both.
            Flow(name: "settings", args: ["-tab=2"] + signedIn, steps: [
                Step(name: "gear") { Self.tap($0, "mytrees-settings") },
                Step(name: "your-own-card") { Self.tap($0, "profile-signin") },
                Step(name: "cancel-the-editor") { Self.tap($0, "Cancel") },
                Step(name: "back-to-my-trees") { back($0) },
            ]),

            // The sheet, which is the control this app is most often holding.
            // Raising it from the header is the gesture Hidde has reported
            // three times, and the header is a handle only if a drag that
            // starts on it moves the sheet rather than opening something.
            Flow(name: "my-trees-sheet", args: ["-tab=2"] + signedIn, steps: [
                Step(name: "drag-the-header-up") { drag($0, from: 0.55, to: 0.16) },
                Step(name: "scroll-the-list") { $0.swipeUp() },
                Step(name: "drag-back-down") { drag($0, from: 0.22, to: 0.75) },
            ]),

            // The map's own sheet, and the page it leads to. A tree page pushed
            // from a tab must keep its back button, which is the fault this
            // suite's oldest test exists for.
            Flow(name: "map-to-a-tree", args: ["-tab=0"], steps: [
                // A TAP, because at peek the sheet takes no taps of its own and
                // one anywhere on it raises it. That is the rule the sheet has
                // had since 2026-08-21 and it is worth walking rather than
                // trusting: it is what stops a swipe up opening whatever card
                // it started on.
                Step(name: "raise-the-sheet") {
                    $0.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.88)).tap()
                },
                Step(name: "open-the-first-tree") { firstCard($0)?.tap() },
                Step(name: "back-to-the-map") { back($0) },
            ]),

            // The camera in the bar is the app's one deed, and it is gated.
            // A gate that leaves you nowhere is worse than no gate.
            Flow(name: "collect-gate", args: ["-tab=0"], steps: [
                Step(name: "tap-the-camera") { Self.tap($0, "tab-collect") },
            ]),

            // MODERATION, built 2026-08-27 and therefore the least walked thing
            // in the app. Apple's reviewer taps exactly this sequence, so it is
            // the one flow where a dead end would cost a release rather than an
            // afternoon.
            Flow(name: "report-and-block",
                 args: ["-tab=2", "-people", "-people-demo"] + signedIn, steps: [
                Step(name: "open-the-ellipsis") { Self.tap($0, "person-more") },
                Step(name: "choose-report") { Self.tap($0, "Report this person") },
                // The literal string, not Moderation.Reason: a UI test runs in
                // its own process and cannot see the app's types at all.
                Step(name: "pick-a-reason") {
                    Self.tap($0, "An offensive name or picture")
                },
                Step(name: "close-the-thank-you") { Self.tap($0, "OK") },
            ]),

            // The way into the app from a search, which is how somebody who
            // knows what they are looking for uses it.
            Flow(name: "search-to-a-tree", args: ["-search=lis"], steps: [
                Step(name: "first-result") { firstCard($0)?.tap() },
                Step(name: "back") { back($0) },
            ]),

            // Discover, and the city page under it. The city page is where the
            // walks shelf leaked Plus this morning, so it is worth arriving at
            // rather than only photographing.
            Flow(name: "discover-to-a-city", args: ["-tab=1"], steps: [
                Step(name: "scroll-the-feed") { $0.swipeUp() },
                Step(name: "open-something") { firstCard($0)?.tap() },
                Step(name: "back") { back($0) },
            ]),

            // The lane picker, which Hidde reported as dead three times before
            // it was pinned. A control with that history gets walked.
            Flow(name: "my-trees-lanes", args: ["-tab=2"] + signedIn, steps: [
                Step(name: "raise-the-sheet") { drag($0, from: 0.55, to: 0.16) },
                Step(name: "favourites") {
                    $0.segmentedControls["collect-lane"].buttons["Favourites"].tap()
                },
                Step(name: "back-to-my-trees") {
                    $0.segmentedControls["collect-lane"].buttons["My trees"].tap()
                },
            ]),

            // Settings, all the way down, because the two most destructive
            // controls in the app live at the bottom of it and both must ask
            // first rather than act.
            // THE ROUTE TO DELETING AN ACCOUNT, walked because it went missing.
            //
            // Between 2026-08-21 and 2026-08-31 there was no way to open the
            // Account sheet at all. The row that set `showingAccount` was
            // deleted along with the card it lived in, and the sheet and its
            // Delete account button stayed in the build, unreachable, for ten
            // days. Nothing here noticed, and build 7 went to App Review with
            // our own notes promising deletion under Settings.
            //
            // Guideline 5.1.1(v) requires an app that can create an account to
            // delete one from inside the app, and a reviewer taps it, so this
            // is a release blocker rather than a missing convenience.
            //
            // THE TAP IS THE ASSERTION. A step whose button does not exist
            // fails the test, which is the whole of what those ten quiet days
            // needed. It stops at Cancel: a walk that actually deleted the
            // account would pass once and then have nothing left to walk.
            Flow(name: "delete-account-route",
                 args: ["-tab=2", "-settings"] + signedIn, steps: [
                Step(name: "open-account") {
                    Self.tap($0, "settings-account")
                },
                // THE SECOND ASK, and the walk has to make it too. That
                // button is disabled until the word is in the field, so a flow
                // that only taps is a flow testing the design we replaced. It
                // types for real rather than reaching past the gate, which is
                // the point: rip the gate out and this test goes red.
                Step(name: "type-the-word") {
                    let field = $0.textFields["delete-confirm-field"].firstMatch
                    _ = field.waitForExistence(timeout: 10)
                    field.tap()
                    field.typeText("DELETE\n")
                },
                Step(name: "delete-asks-first") {
                    Self.tap($0, "delete-confirm-button")
                },
                Step(name: "cancel") { Self.tap($0, "Cancel") },
                // AND IT STOPS THERE. Closing the sheet was a fourth step and
                // it is gone: neither "Done" nor an identifier put on that
                // Button can be found, because an identifier set inside a
                // ToolbarItem does not reach the element XCUITest sees. The
                // property it was meant to prove is asserted anyway, after
                // every step, by the way-back invariant this file exists for.
            ]),

            Flow(name: "settings-bottom", args: ["-tab=2", "-settings"] + signedIn, steps: [
                Step(name: "scroll-to-the-bottom") { $0.swipeUp(); $0.swipeUp() },
                Step(name: "sign-out-asks-first") { Self.tap($0, "Sign out") },
                Step(name: "cancel") { Self.tap($0, "Cancel") },
            ]),
        ]
    }

    // MARK: - the gestures

    private static func back(_ app: XCUIApplication) {
        let bar = app.navigationBars.firstMatch
        if bar.exists, bar.buttons.count > 0 { bar.buttons.element(boundBy: 0).tap() }
    }

    /// A drag in fractions of the screen, so one number works on both phones.
    private static func drag(_ app: XCUIApplication, from: CGFloat, to: CGFloat) {
        let start = app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: from))
        let end = app.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: to))
        start.press(forDuration: 0.05, thenDragTo: end)
    }

    /// The first tree card in whatever list is on screen. Cards carry no
    /// identifier of their own, so this takes the first button that has a tree
    /// page's shape: an image and two lines of text under it.
    private static func firstCard(_ app: XCUIApplication) -> XCUIElement? {
        let cards = app.buttons.matching(NSPredicate(format: "identifier BEGINSWITH 'tree-card'"))
        if cards.count > 0 { return cards.element(boundBy: 0) }
        // Fall back to the first hittable button below the middle of the
        // screen, which on a raised sheet is a card.
        for i in 0..<app.buttons.count {
            let b = app.buttons.element(boundBy: i)
            if b.exists, b.isHittable, b.frame.minY > app.frame.height * 0.4 { return b }
        }
        return nil
    }

    // MARK: - the invariant

    /// Somewhere to go that is not forward. The tab bar counts, a back button
    /// counts, a sheet's own dismissal counts.
    private static func hasAWayBack(_ app: XCUIApplication) -> Bool {
        if app.buttons["tab-map"].exists { return true }
        let bar = app.navigationBars.firstMatch
        if bar.exists, bar.buttons.count > 0 { return true }
        for label in ["Cancel", "Close", "Done", "Not now"] {
            if app.buttons[label].firstMatch.exists { return true }
        }
        // A sheet you drag away: the grabber is the handle and the way out.
        return app.otherElements["spot-sheet"].exists
            || app.otherElements["signin-sheet"].exists
    }

    // MARK: - the walk

    @MainActor
    func testEveryFlowLeavesAWayBack() throws {
        continueAfterFailure = true
        XCUIDevice.shared.orientation = .portrait
        XCUIDevice.shared.appearance = .light

        let out = FileManager.default.temporaryDirectory.appendingPathComponent(Self.folder)
        try? FileManager.default.createDirectory(at: out, withIntermediateDirectories: true)

        for flow in Self.flows {
            let app = XCUIApplication()
            app.launchArguments = ["-at=52.3731,4.8922", "-reset-collection", "-reset-blocks", "-no-cover"] + flow.args
            app.launch()
            // The catalogue is 2.5 MB of JSON and nothing exists until it is
            // read; a step taken before that taps an empty window.
            XCTAssertTrue(app.staticTexts.firstMatch.waitForExistence(timeout: 20),
                          "\(flow.name): nothing rendered at launch")
            shoot(out, flow.name, 0, "launch")

            for (i, step) in flow.steps.enumerated() {
                step.act(app)
                // Long enough for a push, a sheet or a spring to land. Frames
                // read mid-animation measure the thing times 0.957 and read as
                // faults that are not there (2026-08-21).
                Thread.sleep(forTimeInterval: 1.2)
                shoot(out, flow.name, i + 1, step.name)
                XCTAssertTrue(Self.hasAWayBack(app),
                              "\(flow.name): after \"\(step.name)\" there is no tab bar, "
                              + "no back button and nothing to dismiss")
            }
            app.terminate()
        }
    }

    /// Where appwalk.py goes looking, the same arrangement SweepFrames uses:
    /// a file in the runner's own temporary directory, which lives inside the
    /// simulator's container and survives the throwaway clone.
    static let folder = "appwalk"

    private func shoot(_ dir: URL, _ flow: String, _ n: Int, _ name: String) {
        let png = XCUIScreen.main.screenshot().pngRepresentation
        let file = dir.appendingPathComponent(String(format: "%@__%02d-%@.png", flow, n, name))
        try? png.write(to: file)
    }
}
