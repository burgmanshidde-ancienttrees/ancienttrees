// SIGNED IN, FOR REAL: A WRITE REACHES THE SERVER AND COMES BACK (2026-11-08).
//
// Hidde: "waarom testen we in Gods naam alleen uitgelogd". Every signed-in UI
// test so far ran on -signed-in, a session with no token, so it could see a
// sheet open and never whether anything arrived. This one runs on the test
// account (scripts/test_session.py; CI hands the session over as
// AT_SESSION, xcodebuild strips the TEST_RUNNER_ prefix) and proves the round
// trip the way a person would notice it: save a tree, close the app, open it
// again, and the tree is still saved, which it can only be if the server kept
// it, because nothing a person does is kept on the device (hard rule 11).
// Then it removes the save again, and checks that too, so the account ends
// every run as it started.
//
// Without a session (a laptop, a fork) it skips rather than fails.

import XCTest

final class SignedInRoundTrip: XCTestCase {
    private var session: String = ""

    override func setUpWithError() throws {
        continueAfterFailure = false
        session = ProcessInfo.processInfo.environment["AT_SESSION"] ?? ""
        try XCTSkipIf(session.isEmpty, "no test-account session (AT_SESSION): CI only")
    }

    private func launch(_ args: [String]) -> XCUIApplication {
        let app = XCUIApplication()
        app.launchArguments = ["-no-location-ask"] + args
        app.launchEnvironment["AT_TEST_SESSION"] = session
        app.launch()
        _ = app.staticTexts.firstMatch.waitForExistence(timeout: 30)
        return app
    }

    /// THE TREE PAGE'S OWN HEART, not the first one in the tree. The page
    /// opens over the map, whose cards carry hearts with the same identifier;
    /// the first run (2026-11-08) took one of those, tapped the sheet lying on
    /// top of it and read "Save" sixteen times over. Signed out that never
    /// showed, because every heart asks to sign in. So: hittable, centre on
    /// screen, and the largest (the page's action-bar heart is 52 points, a
    /// card's 44).
    private func heart(_ app: XCUIApplication) -> XCUIElement {
        XCTAssertTrue(app.buttons["save-heart"].firstMatch.waitForExistence(timeout: 20),
                      "no save heart on the tree page")
        sleep(2)
        let screen = app.windows.firstMatch.frame
        let all = app.buttons.matching(identifier: "save-heart").allElementsBoundByIndex
        let reachable = all.filter { e in
            let f = e.frame
            return !f.isEmpty && screen.contains(CGPoint(x: f.midX, y: f.midY)) && e.isHittable
        }
        guard let best = reachable.max(by: { $0.frame.width < $1.frame.width }) else {
            XCTFail("\(all.count) save heart(s) on screen and none a finger can reach")
            return all.first ?? app.buttons["save-heart"].firstMatch
        }
        return best
    }

    /// Wait until the heart says what we expect; the account's saves arrive
    /// from the server a moment after launch.
    private func waitFor(_ h: XCUIElement, saved: Bool, _ what: String) {
        let want = saved ? "Saved " : "Save "
        let p = NSPredicate(format: "label BEGINSWITH %@", want)
        let ok = XCTWaiter().wait(for: [XCTNSPredicateExpectation(predicate: p, object: h)], timeout: 20) == .completed
        XCTAssertTrue(ok, "\(what): the heart reads \"\(h.label)\"")
    }

    func testASaveReachesTheServerAndComesBack() {
        // Start clean: if an earlier run left it saved, remove it first.
        var app = launch(["-tab=0", "-open=tree:ams_001"])
        var h = heart(app)
        sleep(5)
        if h.label.hasPrefix("Saved ") {
            h.tap()
            waitFor(h, saved: false, "clearing what an earlier run left")
            sleep(8)
        }
        app.terminate()

        // Save it. The first run (2026-11-08) saw the heart still reading
        // "Save" after the tap, which is one of two things: the app did not
        // take the test session (the tap then asks to sign in), or the save
        // landed and the account's own list, arriving from the server a moment
        // after launch, wrote over it, which a person tapping in the first
        // seconds would meet too. So the tap comes straight after launch, as a
        // person's would, and the test says which of the two it saw.
        app = launch(["-tab=0", "-open=tree:ams_001"])
        h = heart(app)
        waitFor(h, saved: false, "before saving")
        h.tap()
        var seen: [String] = []
        for _ in 0..<16 {
            seen.append(h.exists ? (h.label.hasPrefix("Saved ") ? "saved" : "save") : "gone")
            usleep(500_000)
        }
        let askedToSignIn = app.descendants(matching: .any)["signin-sheet"].exists
        XCTAssertFalse(askedToSignIn,
                       "the tap asked to sign in: the app did not take the test session (AT_TEST_SESSION)")
        XCTAssertFalse(seen.contains("saved") && seen.last == "save",
                       "the save showed and was then undone, every half second after the tap: \(seen.joined(separator: " "))")
        waitFor(h, saved: true, "right after the tap (every half second: \(seen.joined(separator: " ")))")
        sleep(8)   // let the write go out before the app is closed
        app.terminate()

        // A fresh launch reads the account from the server: still saved.
        app = launch(["-tab=0", "-open=tree:ams_001"])
        h = heart(app)
        waitFor(h, saved: true, "after closing and opening the app (the server kept it)")

        // And remove it, so the account ends as it began.
        h.tap()
        waitFor(h, saved: false, "right after removing")
        sleep(8)
        app.terminate()

        app = launch(["-tab=0", "-open=tree:ams_001"])
        h = heart(app)
        sleep(5)
        waitFor(h, saved: false, "after removing and reopening (the server forgot it)")
        app.terminate()
    }
}
