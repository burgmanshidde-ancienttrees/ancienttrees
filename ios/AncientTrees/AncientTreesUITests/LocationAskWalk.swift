// The first open asks for location by itself (Hidde, 2026-10-14).
//
// A reader wrote "Location not working on iOS, permissions for it not
// available in the options": the app only asked when somebody tapped the
// "Location off" chip, so a phone that never did had no Location row in
// Settings at all. This walk resets the answer, opens the app the way a
// stranger does (no -at origin, no flags), and requires the system's own
// question to appear without a single tap. It also requires the Location row
// in Profile, the second way to switch it on.
import XCTest

final class LocationAskWalk: XCTestCase {
    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    func testFirstOpenAsksForLocation() {
        let app = XCUIApplication()
        app.resetAuthorizationStatus(for: .location)
        app.launchArguments = ["-reset-collection", "-no-review-prompt"]
        app.launch()

        let springboard = XCUIApplication(bundleIdentifier: "com.apple.springboard")
        let alert = springboard.alerts.firstMatch
        XCTAssertTrue(alert.waitForExistence(timeout: 20),
                      "the first open did not ask for location by itself")
        let deny = alert.buttons["Don’t Allow"]
        XCTAssertTrue(deny.exists, "the location question has no Don't Allow button")
        deny.tap()

        // Refused, so the chip stays on the map and offers the way back.
        XCTAssertTrue(app.buttons["location-off-chip"].firstMatch.waitForExistence(timeout: 10)
                      || app.staticTexts["Location off"].firstMatch.waitForExistence(timeout: 5),
                      "after a refusal the map no longer says location is off")
    }

    func testProfileHasALocationRow() {
        let app = XCUIApplication()
        app.launchArguments = ["-no-location-ask", "-no-cover", "-open=profile:me"]
        app.launch()
        let row = app.buttons["profile-location"].firstMatch
        XCTAssertTrue(row.waitForExistence(timeout: 20), "Profile has no Location row")
    }
}
