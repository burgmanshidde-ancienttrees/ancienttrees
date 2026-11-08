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
// way a finger does (no coordinate fallback, no accessibility action), and
// asserts that SOMETHING CHANGED: a new screen, a sheet, a different label, a
// snackbar, or the app handing over to Safari, Maps or the share sheet. A
// button after which the screen reads exactly as before is a dead button, and
// every dead button is named in one failure per screen.
//
// What is compared is the element tree's text with its frames and addresses
// taken out, so scrolling or an animation does not count as an answer and a
// map settling does not either. A button that rightly changes nothing a test
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
    /// Keyed "<identifier or label>".
    /// It starts empty on purpose and grows only with a reason a person agreed to.
    private static let quiet: [String: String] = [:]

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
    /// without frames or memory addresses, so movement is not a change.
    private func signature(_ app: XCUIApplication) -> String {
        if app.state != .runningForeground { return "<left the app>" }
        var s = app.debugDescription
        s = s.replacingOccurrences(of: #"\{\{[^}]*\}, \{[^}]*\}\}"#, with: "", options: .regularExpression)
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

    private func element(_ app: XCUIApplication, _ t: Target) -> XCUIElement {
        if !t.id.isEmpty { return app.buttons[t.id].firstMatch }
        return app.buttons.matching(NSPredicate(format: "label == %@", t.label)).firstMatch
    }

    /// Can a finger reach it: its centre on the screen, then XCTest's own
    /// hittable. Asking isHittable of an element whose centre is off screen
    /// does not return false, it FAILS the test ("Activation point invalid",
    /// the clipped highlight-card, 2026-11-08 first run), so the centre is
    /// checked first.
    private func reachable(_ e: XCUIElement, _ app: XCUIApplication) -> Bool {
        guard e.exists else { return false }
        let f = e.frame
        let screen = app.windows.firstMatch.frame
        guard !f.isEmpty, screen.contains(CGPoint(x: f.midX, y: f.midY)) else { return false }
        return e.isHittable
    }

    /// Every hittable button on the screen, scrolling down a few times.
    private func targets(_ app: XCUIApplication) -> [Target] {
        var seen: [Target] = []
        for pass in 0..<4 {
            for b in app.buttons.allElementsBoundByIndex where reachable(b, app) {
                let t = Target(id: b.identifier, label: b.label)
                if t.id.isEmpty && t.label.isEmpty { continue }
                if !seen.contains(t) { seen.append(t) }
            }
            if pass < 3 { app.swipeUp() }
        }
        return seen
    }

    /// Scroll until the button can be tapped by a finger, then tap it.
    private func reachAndTap(_ app: XCUIApplication, _ t: Target) -> Bool {
        let e = element(app, t)
        for _ in 0..<5 {
            if reachable(e, app) { e.tap(); return true }
            app.swipeUp()
        }
        return false
    }

    private func walk(_ name: String, _ args: [String]) {
        let first = launch(args)
        _ = settled(first)
        let list = targets(first).filter { t in
            let k = (t.id + " " + t.label).lowercased()
            return !Self.neverTap.contains { k.contains($0) } && Self.quiet[key(t)] == nil
        }
        first.terminate()
        XCTAssertFalse(list.isEmpty, "\(name): no buttons found at all; did the screen open?")

        var dead: [String] = []
        var unreachable: [String] = []
        for t in list {
            let app = launch(args)
            // Reach it first (scrolling is not the answer we are looking for),
            // then read the screen, then tap.
            let e = element(app, t)
            var tries = 0
            while !reachable(e, app) && tries < 5 { app.swipeUp(); tries += 1 }
            guard reachable(e, app) else { unreachable.append(key(t)); app.terminate(); continue }
            let before = settled(app)
            guard reachAndTap(app, t) else { unreachable.append(key(t)); app.terminate(); continue }
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
        for (name, args) in Self.screens { walk(name + " (signed out)", args) }
    }

    func testEveryButtonAnswersSignedIn() {
        for (name, args) in Self.screens { walk(name + " (signed in)", args + ["-signed-in"]) }
    }
}
