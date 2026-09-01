// The app after somebody has tapped "Don't Allow".
//
// Location refused is not a rare state. It is what you get from anybody who
// has been burned by an app before, anybody handing their phone to a child,
// and anybody who tapped the wrong button once, months ago, and never went
// back. This app is ABOUT where you are standing, so it is the state most
// likely to make it look broken.
//
// Every other UI test here launches with -at=, a fixed location that always
// works. That is the right default for testing everything else and it means
// this state had never been entered once.
//
// The launch arguments are deliberately absent here: no -at=, because the
// whole point is what happens with nothing to fall back on. scripts/refused.py
// revokes the permission on the simulator before running these, so the app's
// real Core Location code takes its real refused branch.

import XCTest

final class RefusedWalk: XCTestCase {

    override func setUpWithError() throws {
        continueAfterFailure = false
        XCUIDevice.shared.orientation = .portrait
        XCUIDevice.shared.appearance = .light
    }

    private func launch(_ args: [String] = []) -> XCUIApplication {
        let app = XCUIApplication()
        app.launchArguments = ["-reset-collection", "-reset-blocks", "-no-nudge", "-no-cover"] + args
        app.launch()
        return app
    }

    /// The map still has trees on it and still says where it is. What it must
    /// never do is pretend it knows where you are.
    func testTheMapStillWorksWithLocationRefused() throws {
        let app = launch(["-tab=0"])

        XCTAssertTrue(app.buttons["tab-map"].waitForExistence(timeout: 20),
                      "the app did not finish launching with location refused")
        let count = app.staticTexts["map-count"]
        XCTAssertTrue(count.waitForExistence(timeout: 12),
                      "the map drew no trees at all with location refused")
        XCTAssertFalse(count.label.hasPrefix("0 "),
                       "the map is empty without a location: \(count.label)")
    }

    /// And it SAYS so. A map that quietly centres somewhere else without a word
    /// is the one unforgivable error in this product: telling somebody they are
    /// somewhere they are not.
    func testTheMapAdmitsItDoesNotKnowWhereYouAre() throws {
        let app = launch(["-tab=0"])
        XCTAssertTrue(app.buttons["tab-map"].waitForExistence(timeout: 20))

        let chip = app.buttons.matching(
            NSPredicate(format: "label CONTAINS[c] 'Location off'")).firstMatch
        XCTAssertTrue(chip.waitForExistence(timeout: 12),
                      "with location refused the map said nothing about it")
        // And it offers the only thing that can actually fix it. Not read the
        // instant the chip exists: CLLocationManager's very first
        // authorizationStatus read on a cold launch can still say
        // .notDetermined for a moment, before locationd's own callback
        // delivers the real .denied a beat later, so the chip's first paint
        // can briefly say "Use my location" before correcting itself. Wait
        // for the corrected text rather than failing on the flash.
        let saysTurnOn = NSPredicate(format: "label CONTAINS[c] 'turn on'")
        let stabilised = expectation(for: saysTurnOn, evaluatedWith: chip)
        let result = XCTWaiter().wait(for: [stabilised], timeout: 8)
        XCTAssertEqual(result, .completed,
                      "the chip does not offer a way out: '\(chip.label)'")
    }

    /// Every tab has to survive it, not only the map. Discover and My trees
    /// both sort by distance from you, and neither had ever been opened
    /// without a distance to sort by.
    func testEveryTabSurvivesHavingNoLocation() throws {
        let app = launch(["-tab=0"])
        XCTAssertTrue(app.buttons["tab-map"].waitForExistence(timeout: 20))

        for tab in ["tab-discover", "tab-my-trees", "tab-map"] {
            let button = app.buttons[tab]
            XCTAssertTrue(button.waitForExistence(timeout: 10), "\(tab) is not there")
            button.tap()
            XCTAssertEqual(app.state, .runningForeground,
                           "the app stopped running on \(tab) with no location")
        }
    }

    /// The one screen that is entirely about where you are standing. It cannot
    /// tell you which tree is in front of you, and it has to say that rather
    /// than show an empty list or a spinner.
    func testCollectSaysWhatItCannotDoRatherThanShowingNothing() throws {
        let app = launch(["-collect"])

        let sheet = app.otherElements["spot-sheet"]
        XCTAssertTrue(sheet.waitForExistence(timeout: 20),
                      "the collect sheet never opened with location refused")
        XCTAssertEqual(app.state, .runningForeground)
        // Something readable, not an empty box. Whatever the wording, the
        // screen has to carry words.
        XCTAssertGreaterThan(app.staticTexts.count, 1,
                             "the collect sheet is blank when it does not know where you are")
    }
}
