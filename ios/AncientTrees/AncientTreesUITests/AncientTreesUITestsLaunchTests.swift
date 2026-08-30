//
//  AncientTreesUITestsLaunchTests.swift
//  AncientTreesUITests
//
//  Created by Hidde on 19/08/2026.
//

import XCTest

final class AncientTreesUITestsLaunchTests: XCTestCase {

    override class var runsForEachTargetApplicationUIConfiguration: Bool {
        true
    }

    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    override func tearDownWithError() throws {
        // Leave the simulator the way the other tests expect it; see
        // AncientTreesUITests.setUpWithError.
        XCUIDevice.shared.orientation = .portrait
        XCUIDevice.shared.appearance = .light
    }

    @MainActor
    func testLaunch() throws {
        let app = XCUIApplication()
        // The same fixed origin as every other test, so the launch never
        // raises the location dialog on the shared simulator.
        app.launchArguments = ["-at=52.3731,4.8922", "-reset-collection", "-no-cover"]
        app.launch()

        // Insert steps here to perform after app launch but before taking a screenshot,
        // such as logging into a test account or navigating somewhere in the app
        // XCUIAutomation Documentation
        // https://developer.apple.com/documentation/xcuiautomation

        let attachment = XCTAttachment(screenshot: app.screenshot())
        attachment.name = "Launch Screen"
        attachment.lifetime = .keepAlways
        add(attachment)
    }
}
