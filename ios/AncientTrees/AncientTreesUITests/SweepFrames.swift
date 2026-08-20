// The measuring half of the screenshot sweep.
//
// scripts/appsweep.py photographs every screen so somebody can LOOK at it.
// This dumps the same screens as numbers, because a pair of eyes reading
// fourteen screenshots will not notice that a card starts at x=16 and the
// heading above it at x=20, and that four-point difference is exactly what
// Hidde has been seeing on his telephone and calling "uitlijning".
//
// It asserts nothing about layout on purpose. It prints the element tree with
// its frames between markers, and scripts/appfit.py does the judging: a
// threshold argued about in Python is a threshold anyone can change, while one
// buried in an XCTAssert is a threshold nobody dares touch.
//
// The screen list is the same list as appsweep.py's, and it has to stay that
// way. If you add a screen to one, add it to the other, or the app grows a
// screen that is photographed but never measured.

import XCTest

final class SweepFrames: XCTestCase {

    /// Same origin as the sweep: fixed, so the location dialog never appears
    /// and "near you" is the same trees every time.
    private static let origin = "-at=52.3731,4.8922"

    /// name -> the launch arguments that open it.
    private static let screens: [(String, [String])] = [
        ("home",         ["-tab=0"]),
        ("map",          ["-tab=1"]),
        ("collect",      ["-tab=2"]),
        ("profile",      ["-tab=3"]),
        ("tree",         ["-tab=0", "-open=tree:ath_004"]),
        ("tree-nophoto", ["-tab=0", "-open=tree:vln_010"]),
        ("city",         ["-tab=0", "-open=city:aarhus"]),
        ("species",      ["-tab=0", "-open=species:Aleppo Pine"]),
        ("collection",   ["-tab=0", "-open=collection:ancient-oaks-of-europe"]),
        ("signin",       ["-tab=0", "-signin"]),
        ("paywall",      ["-tab=0", "-paywall"]),
        ("primer",       ["-tab=0", "-primer"]),
        ("contribute",   ["-tab=3", "-contribute"]),
    ]

    /// The file appfit.py goes looking for.
    static let dumpName = "appfit-frames.txt"

    @MainActor
    func testDumpEveryScreensFrames() throws {
        continueAfterFailure = true
        var dump = ""
        for (name, extra) in Self.screens {
            let app = XCUIApplication()
            app.launchArguments = [Self.origin] + extra
            app.launch()

            // The catalogue is 2.5 MB of JSON, so nothing exists for a moment
            // after launch. Waiting on a real element rather than sleeping
            // means a slow machine does not produce an empty measurement that
            // then reads as a clean screen.
            // Any piece of text will do: there is none until the catalogue is
            // read, and every one of these screens has some once it is. A
            // predicate on `hittable` looks like the right thing to wait for
            // and is not: XCUIElementQuery cannot filter on it, and the test
            // fails on the first screen with "invalid key path".
            _ = app.staticTexts.firstMatch.waitForExistence(timeout: 20)

            let size = app.frame.size
            dump += "<<<SWEEP \(name) \(size.width)x\(size.height)\n"
            dump += app.debugDescription
            dump += "\nSWEEP>>>\n"
            app.terminate()
        }

        // A FILE, not print(). The first version printed the measurements and
        // the test passed while producing nothing a script could read: XCTest
        // does not forward a test's standard output to xcodebuild, so every
        // line of it went into the result bundle and nowhere else. Written into
        // the runner's own temporary directory, which appfit.py then finds
        // under the simulator's data directory.
        let out = FileManager.default.temporaryDirectory
            .appendingPathComponent(Self.dumpName)
        try dump.write(to: out, atomically: true, encoding: .utf8)
        print("wrote \(out.path)")
    }
}
