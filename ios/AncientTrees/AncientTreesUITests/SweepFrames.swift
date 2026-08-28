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
    /// Every screen is measured from a clean collection; Saved's -reset-collection.
    private static let clean = "-reset-collection"
    /// And the blocked list, for the same reason: a block left by one screen
    /// silently removes a person from the next one.
    private static let unblocked = "-reset-blocks"

    /// name -> the launch arguments that open it.
    /// Name, launch arguments, and for a screen that is a sheet or an overlay,
    /// the identifier of its root. A sheet's measurements used to include the
    /// whole screen behind it, so the paywall was judged against Explore's
    /// hero chip and the contribute form against the profile under it, and
    /// both "drifted" from things nobody could see (2026-08-21).
    private static let screens: [(String, [String], String?)] = [
        ("map",          ["-tab=0"], nil),
        // The map with the sheet all the way up, which is a different screen
        // and was never measured: the way BACK from it is a floating button
        // that exists in the tree whether or not it is on top of the sheet
        // (2026-08-25).
        ("map-full",     ["-tab=0", "-sheet=full"], nil),
        ("explore",      ["-tab=1"], nil),
        ("collect-intro", ["-collect"], "spot-sheet"),
        ("collect-away", ["-collect", "-at=52.03,5.91"], "spot-sheet"),
        ("collect-place", ["-collect", "-collect-place"], "collect-place"),
        ("walk-begin",   ["-begin=amsterdam|Plantage"], "walk-mode"),
        ("search",       ["-search=lis"], nil),
        // "collection-tab", matching appsweep.py. It said "yours" here and
        // "collection" there, for the same tab, which is how these two lists
        // drift apart: CLAUDE.md says they are one list and on 2026-08-25 they
        // were not, and over there the duplicate name meant this screen was
        // never photographed at all.
        ("collection-tab", ["-tab=2"], nil),
        ("profile",      ["-tab=2", "-settings"], nil),
        ("tree",         ["-tab=0", "-open=tree:ath_004"], nil),
        ("tree-nophoto", ["-tab=0", "-open=tree:vln_010"], nil),
        ("city",         ["-tab=0", "-open=city:aarhus"], nil),
        ("city-map",     ["-tab=0", "-open=citymap:aarhus"], nil),
        ("species",      ["-tab=0", "-open=species:Aleppo Pine"], nil),
        ("collection",   ["-tab=0", "-open=collection:ancient-oaks-of-europe"], nil),
        ("walk",         ["-tab=0", "-open=walk:aarhus|Moesgård / Højbjerg"], nil),
        ("place-pin",    ["-tab=0", "-open=tree:ath_004", "-placepin"], nil),
        ("signin",       ["-tab=0", "-signin"], "signin-sheet"),
        ("paywall",      ["-tab=0", "-paywall"], "paywall-sheet"),
        ("primer",       ["-tab=0", "-primer"], "primer"),
        ("contribute",   ["-tab=2", "-settings", "-contribute"], "contribute-sheet"),
        ("feedback",     ["-tab=2", "-settings", "-feedback"], "contribute-sheet"),
        ("sponsor",      ["-tab=2", "-settings", "-sponsor"], "sponsor-sheet"),
        ("profile-edit", ["-tab=2", "-profile-edit"], nil),
        ("people",       ["-tab=2", "-signed-in", "-people", "-people-demo"], "people-sheet"),
    ]

    /// The file appfit.py goes looking for.
    static let dumpName = "appfit-frames.txt"

    @MainActor
    func testDumpEveryScreensFrames() throws {
        continueAfterFailure = true
        // Portrait: the launch tests may have left the simulator on its side.
        XCUIDevice.shared.orientation = .portrait
        XCUIDevice.shared.appearance = .light
        var dump = ""
        for (name, extra, root) in Self.screens {
            let app = XCUIApplication()
            app.launchArguments = [Self.origin, Self.clean, Self.unblocked] + extra
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
            // And let a sheet finish arriving. A sheet zooms in over about
            // half a second, and a frame read during that is the frame times
            // 0.957: the Spot sheet's 44 point close button measured 42.1 and
            // the gate called it small (2026-08-21).
            if let root {
                // ASSERTED, not awaited and forgotten. The result used to be
                // discarded, so a screen whose launch argument had died still
                // measured and still produced a picture: it was the screen
                // underneath, wearing the missing screen's name. Three of them
                // were doing exactly that on 2026-08-28, from the day Settings
                // stopped being a tab. A screen that cannot be opened has to
                // say so out loud, or the sweep reports coverage it does not
                // have.
                XCTAssertTrue(app.descendants(matching: .any)[root].waitForExistence(timeout: 10),
                              "\(name): nothing with identifier \(root) appeared, so this "
                              + "screenshot is of whatever was underneath. Fix the launch "
                              + "argument rather than the assertion.")
            }
            Thread.sleep(forTimeInterval: 1.5)

            let size = app.frame.size
            // The root's name travels in the header and appfit.py keeps only
            // what sits under it: an element's own debugDescription prints
            // the whole application anyway.
            dump += "<<<SWEEP \(name) \(size.width)x\(size.height)"
            if let root { dump += " root=\(root)" }
            dump += "\n"
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
