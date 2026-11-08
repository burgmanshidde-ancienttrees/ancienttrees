// EVERY BUTTON ANSWERS A FINGER (2026-11-08).
//
// Hidde, after Discover's ambassador seat ignored his tap on build 40 and no
// test had noticed: "Hebben we überhaupt een test proces dat de app helemaal
// langs loopt of zitten we allemaal van dit soort gaten in", then "Ja" to a
// walk that taps every button. The website has had this since 2026-10-07
// (smoke.yml clicks every control on every page type); the app had walks that
// asked whether there was a way back (FlowWalk) and whether a gated control
// asked for an account (SignedOutWalk), and nothing that asked whether a
// control DOES anything.
//
// So this opens each screen, signed out and signed in, finds every button a
// finger can reach on it (scrolling down a few times), and for each one:
// launches the screen fresh, waits for it to stand still, taps the button the
// way a finger does (on its centre, no accessibility action), and
// asserts that SOMETHING CHANGED: a new screen, a sheet, a different label, a
// snackbar, or the app handing over to Safari, Maps or the share sheet. A
// button after which the screen reads exactly as before is a dead button, and
// every dead button is named in one failure per screen.
//
// What is compared is the element tree's text, frames rounded to whole points,
// once the screen has stood still, so a sheet that lowers counts as an answer
// and a map still drawing does not. The tap lands on the button's centre as a
// finger would, whatever lies on top of it. A button that rightly changes nothing a test
// can read goes in `quiet` with its reason; a button that would do harm with
// a fake session (delete, sign out, block) is never tapped (`neverTap`).
//
// It is slow (a fresh launch per button), so it does not run in ios.yml's
// suite: .github/workflows/buttonwalk.yml runs it once a day and on dispatch.
// A new screen joins `screens` here, as it joins SweepFrames' list.

import XCTest

final class ButtonWalk: XCTestCase {

    /// Amsterdam unless a screen names its own place: the app reads the FIRST
    /// -at=, so the default is added only when a screen has none.
    private static let base = ["-no-location-ask", "-reset-collection", "-reset-blocks", "-no-cover"]
    private static let origin = "-at=52.3731,4.8922"

    /// name, launch arguments. Each is walked signed out and signed in.
    private static let screens: [(String, [String])] = [
        ("map",           ["-tab=0"]),
        ("map-full",      ["-tab=0", "-sheet=full"]),
        ("map-pin",       ["-tab=0", "-select=ath_004"]),
        ("discover",      ["-tab=1"]),
        // Discover where a city has an open ambassador seat: Cadiz.
        ("discover-cadiz", ["-tab=1", "-at=36.5297,-6.2925"]),
        ("my-trees",      ["-tab=2"]),
        ("profile",       ["-tab=2", "-settings"]),
        ("tree",          ["-tab=0", "-open=tree:ath_004"]),
        ("tree-nophoto",  ["-tab=0", "-open=tree:vln_010"]),
        ("city",          ["-tab=0", "-open=city:cadiz"]),
        ("city-full",     ["-tab=0", "-open=city:cadiz", "-sheet=full"]),
        ("species",       ["-tab=0", "-open=species:Aleppo Pine"]),
        ("collection",    ["-tab=0", "-open=collection:ancient-oaks-of-europe"]),
    ]

    /// Words in a button's identifier or label that mean it must not be
    /// tapped by a machine, even with the fake session.
    private static let neverTap = ["delete", "sign out", "signout", "log out", "logout",
                                   "block", "remove", "unfollow"]

    /// Buttons that rightly change nothing this walk can read, with why.
    /// Keyed "<screen>|<identifier or label>": the same button can be quiet on
    /// one screen and must answer on another. Every entry carries its reason;
    /// a new one needs a person to agree with it.
    private static let quiet: [String: String] = [
        // Your own tab, tapped while you are on it at the top, does nothing in
        // every app with a tab bar (first walk, 2026-11-08).
        "map|tab-map": "already on the map tab",
        "map-full|tab-map": "already on the map tab",
        "map-pin|tab-map": "already on the map tab",
        "city|tab-map": "already on the map tab",
        "city-full|tab-map": "already on the map tab",
        "discover|tab-discover": "already on Discover, at the top",
        "discover-cadiz|tab-discover": "already on Discover, at the top",
        "my-trees|tab-my-trees": "already on My trees",
        // The test pins the location with -at=, and the camera opens on it:
        // re-centring on where it already stands moves nothing.
        "map|map-recentre": "the camera already stands on the test's location",
        "my-trees|map-recentre": "the camera already stands on the test's location",
    ]

    override func setUpWithError() throws {
        continueAfterFailure = true
        XCUIDevice.shared.orientation = .portrait
    }

    private func launch(_ args: [String]) -> XCUIApplication {
        let app = XCUIApplication()
        let at = args.contains { $0.hasPrefix("-at=") } ? [] : [Self.origin]
        app.launchArguments = Self.base + at + args
        app.launch()
        _ = app.staticTexts.firstMatch.waitForExistence(timeout: 30)
        return app
    }

    /// The screen as text: every element's type, identifier, label and value,
    /// WITH its frame, rounded to whole points. The first walk took frames
    /// out so that motion would not count as an answer, and then flagged
    /// every control whose answer IS motion (a sheet that lowers, a list that
    /// jumps) as dead. Settling first (two equal readings a second apart)
    /// keeps a map that is still drawing from counting as an answer.
    private func signature(_ app: XCUIApplication) -> String {
        if app.state != .runningForeground { return "<left the app>" }
        var s = app.debugDescription
        s = s.replacingOccurrences(of: #"(\d+)\.\d+"#, with: "$1", options: .regularExpression)
        s = s.replacingOccurrences(of: #"0x[0-9a-fA-F]+"#, with: "", options: .regularExpression)
        s = s.replacingOccurrences(of: #"pid: \d+"#, with: "", options: .regularExpression)
        return s
    }

    /// Wait until two readings a second apart agree (the catalogue loading,
    /// a sheet arriving), at most eight seconds; return the last reading.
    private func settled(_ app: XCUIApplication) -> String {
        var last = signature(app)
        for _ in 0..<8 {
            sleep(1)
            let now = signature(app)
            if now == last { return now }
            last = now
        }
        return last
    }

    private struct Target: Hashable { let id: String; let label: String }

    private func key(_ t: Target) -> String { t.id.isEmpty ? t.label : t.id }

    /// Every button in one snapshot of the screen, with its frame. A snapshot
    /// cannot fail halfway the way asking element by element did: the first
    /// walk died twice on a tree card that went away between two questions
    /// ("Failed to get matching snapshot", "Activation point invalid").
    private func buttons(_ app: XCUIApplication) -> [(Target, CGRect)] {
        guard let root = try? app.snapshot() else { return [] }
        var out: [(Target, CGRect)] = []
        var stack: [XCUIElementSnapshot] = [root]
        while let n = stack.popLast() {
            if n.elementType == .button, n.isEnabled, !n.frame.isEmpty {
                out.append((Target(id: n.identifier, label: n.label), n.frame))
            }
            stack.append(contentsOf: n.children)
        }
        return out
    }

    /// Where a finger would land on this button now, if its centre is on the
    /// screen. Tapping that point is exactly what a finger does, including
    /// meeting whatever lies on top of it (a sheet over a filter row).
    private func spot(_ app: XCUIApplication, _ t: Target) -> CGPoint? {
        let screen = app.windows.firstMatch.frame
        for (b, f) in buttons(app) where b == t {
            let c = CGPoint(x: f.midX, y: f.midY)
            if screen.insetBy(dx: 1, dy: 1).contains(c) { return c }
        }
        return nil
    }

    private func tap(_ app: XCUIApplication, at p: CGPoint) {
        app.coordinate(withNormalizedOffset: .zero).withOffset(CGVector(dx: p.x, dy: p.y)).tap()
    }

    /// Every button whose centre is on screen, scrolling down a few times.
    private func targets(_ app: XCUIApplication) -> [Target] {
        var seen: [Target] = []
        let screen = app.windows.firstMatch.frame
        for pass in 0..<4 {
            for (t, f) in buttons(app) where screen.contains(CGPoint(x: f.midX, y: f.midY)) {
                if t.id.isEmpty && t.label.isEmpty { continue }
                if !seen.contains(t) { seen.append(t) }
            }
            if pass < 3 { app.swipeUp() }
        }
        return seen
    }

    private func walk(_ name: String, _ screen: String, _ args: [String]) {
        let first = launch(args)
        _ = settled(first)
        let list = targets(first).filter { t in
            let k = (t.id + " " + t.label).lowercased()
            return !Self.neverTap.contains { k.contains($0) } && Self.quiet["\(screen)|\(key(t))"] == nil
        }
        first.terminate()
        XCTAssertFalse(list.isEmpty, "\(name): no buttons found at all; did the screen open?")

        var dead: [String] = []
        var unreachable: [String] = []
        for t in list {
            let app = launch(args)
            // Reach it first (scrolling is not the answer we are looking for),
            // then read the screen, then tap where a finger would.
            var p = spot(app, t)
            var tries = 0
            while p == nil && tries < 5 { app.swipeUp(); tries += 1; p = spot(app, t) }
            guard p != nil else { unreachable.append(key(t)); app.terminate(); continue }
            let before = settled(app)
            guard let at = spot(app, t) else { unreachable.append(key(t)); app.terminate(); continue }
            tap(app, at: at)
            let after = settled(app)
            if after == before { dead.append(key(t)) }
            app.terminate()
        }
        XCTAssertTrue(dead.isEmpty,
                      "\(name): \(dead.count) button(s) changed nothing when tapped: \(dead.joined(separator: ", "))")
        if !unreachable.isEmpty {
            // Found once and then not again is a flaky screen, not a dead
            // button: said, not failed.
            print("ButtonWalk \(name): could not reach again: \(unreachable.joined(separator: ", "))")
        }
    }

    func testEveryButtonAnswersSignedOut() {
        for (name, args) in Self.screens { walk(name + " (signed out)", name, args) }
    }

    func testEveryButtonAnswersSignedIn() {
        for (name, args) in Self.screens { walk(name + " (signed in)", name, args + ["-signed-in"]) }
    }
}
