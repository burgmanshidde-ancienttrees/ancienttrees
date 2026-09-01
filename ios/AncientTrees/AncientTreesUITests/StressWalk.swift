// Tapping at random until something breaks.
//
// Every other test here checks something somebody thought of. This one is for
// what nobody thought of: the tap on a card while the sheet is still animating,
// the back button pressed twice, the filter opened during a map move. Those are
// the crashes that arrive in the first week of a release, because a thousand
// people find in an afternoon what one author never tries.
//
// THE SEED IS FIXED, and that is the whole difference between this and noise. A
// monkey test that cannot repeat its own failure is a test that turns the gate
// red and teaches nobody anything, which is worse than no test. With a seed,
// "it died on action 91" is a thing you can run again and watch.
//
// WHAT IT ASSERTS, deliberately only one thing: the app is still running. Not
// what is on screen, not where it ended up, because after ninety random taps
// there is no correct answer to either. A monkey test that asserts about
// content is a flaky test wearing a lab coat.
//
// WHAT IT AVOIDS: anything that leaves the app or destroys something. A random
// finger that finds "Delete" and confirms it teaches us nothing except that
// destructive buttons work.

import XCTest

final class StressWalk: XCTestCase {

    /// Reproducible randomness. Not for cryptography, for a finger.
    private struct Fixed: RandomNumberGenerator {
        var state: UInt64
        mutating func next() -> UInt64 {
            state ^= state << 13
            state ^= state >> 7
            state ^= state << 17
            return state
        }
    }

    /// Labels a random finger must not press. Two families: things that leave
    /// the app, and things that throw something away.
    private static let avoid = [
        "delete", "sign out", "remove", "block", "report",
        "privacy", "terms", "legal",            // these open Safari
        "continue with apple", "continue with google",
        "take me there",                        // hands over to Maps
    ]

    override func setUpWithError() throws {
        continueAfterFailure = false
        XCUIDevice.shared.orientation = .portrait
        XCUIDevice.shared.appearance = .light
    }

    @MainActor
    func testNinetyRandomActionsDoNotKillTheApp() throws {
        let app = XCUIApplication()
        app.launchArguments = ["-at=52.3731,4.8922", "-reset-collection", "-no-cover",
                               "-reset-blocks", "-signed-in", "-no-nudge"]
        app.launch()
        XCTAssertTrue(app.buttons["tab-map"].waitForExistence(timeout: 20),
                      "the app did not finish launching")

        var rng = Fixed(state: 20_260_827)
        var lastAction = "launch"

        for step in 1...90 {
            // Four moves, weighted the way a person moves: mostly taps, some
            // scrolling, and now and then a tab change to get out of a corner
            // the finger has painted itself into.
            switch Int.random(in: 0..<10, using: &rng) {
            case 0...5:
                // ONE element, resolved late. Filtering the whole list by
                // isHittable asks the app about every button in turn, and the
                // screen moves while it answers: the first version of this died
                // on "no matches found for element at index 15" after fifteen
                // actions, which is the test being stale rather than the app
                // being broken. Pick an index, resolve it, check it, tap it.
                let buttons = app.buttons
                let count = buttons.count
                guard count > 0 else { lastAction = "nothing to tap"; break }
                let pick = buttons.element(boundBy: Int.random(in: 0..<count, using: &rng))
                // ONE THROWING snapshot, and it is the only call here that can
                // be caught. .exists answers safely, but .frame and .label are
                // plain properties: when the element has gone since the count
                // was read they do not return, they fail the test outright, and
                // this test exists precisely to survive a screen moving under
                // it. The comment above records the same death at index 15;
                // this is index 20, on iOS 18.5 in CI on 2026-09-01, and
                // resolving later only ever narrows that window rather than
                // closing it. snapshot() throws, so `try?` turns a red gate
                // into the "gone before the tap" this loop already knows how to
                // handle.
                guard pick.exists, let snap = try? pick.snapshot() else {
                    lastAction = "gone before the tap"
                    break
                }
                // NOT isHittable. It throws rather than answering false for an
                // element scrolled out of view ("activation point invalid and no
                // suggested hit points"), and a row far down a list is exactly
                // what a random index keeps picking. So the frame is asked
                // instead and the tap goes to a coordinate inside it, which
                // needs no hittability question at all.
                let box = snap.frame
                let screen = app.frame
                guard box.width > 1, box.height > 1,
                      screen.contains(CGPoint(x: box.midX, y: box.midY)) else {
                    lastAction = "off screen"
                    break
                }
                let label = snap.label.lowercased()
                guard !Self.avoid.contains(where: { label.contains($0) }) else {
                    lastAction = "left '\(pick.label)' alone"
                    break
                }
                lastAction = "tap '\(pick.label)'"
                pick.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5)).tap()
            case 6, 7:
                lastAction = "swipe up"
                app.swipeUp()
            case 8:
                lastAction = "swipe down"
                app.swipeDown()
            default:
                let tabs = ["tab-map", "tab-discover", "tab-my-trees"]
                let name = tabs[Int.random(in: 0..<tabs.count, using: &rng)]
                lastAction = "go to \(name)"
                let tab = app.buttons[name]
                if tab.exists, tab.isHittable { tab.tap() }
            }

            // The one assertion, and it is the point of the whole file.
            XCTAssertEqual(app.state, .runningForeground,
                           "the app stopped running at action \(step), after \(lastAction). "
                           + "Re-run this test to watch it happen again: the seed is fixed.")

            // A random finger can still reach a system sheet or a share sheet
            // that no filter predicted. Come back rather than failing: being
            // handed to another app is not a crash, and the test has 90 actions
            // to get through.
            if app.state != .runningForeground { app.activate() }
        }

        XCTAssertEqual(app.state, .runningForeground)
    }
}
