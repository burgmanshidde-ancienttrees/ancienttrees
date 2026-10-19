// A TAP THAT LANDS ON A SCREEN STILL ARRIVING IS LOST (2026-10-19).
//
// On a busy CI runner a sheet or a system alert takes seconds to finish
// presenting, and XCUITest taps the moment the element exists. UIKit ignores
// touches while a presentation transition runs, so the tap vanishes without a
// word and the test fails on whatever it expected next: UndoWalk's "removing
// did not offer Undo" (run 39214058571, the sheet still dimming in under the
// tap, the frame XCTest read a second earlier "negative or non-finite").
// LocationAskWalk found the same with the location alert on 2026-10-15.
//
// So: wait until the element can be hit and its frame holds still between
// two looks a quarter second apart, then tap. A wider timeout would not help;
// the tap was never going to count.
import XCTest

extension XCUIElement {
    /// True once the element is hittable and its frame has stopped moving.
    @discardableResult
    func waitUntilSettled(timeout: TimeInterval = 10) -> Bool {
        var last = CGRect.null
        let end = Date().addingTimeInterval(timeout)
        while Date() < end {
            let now = exists ? frame : .null
            if !now.isNull, now == last, isHittable { return true }
            last = now
            Thread.sleep(forTimeInterval: 0.25)
        }
        return false
    }

    /// Taps once the element has settled (see waitUntilSettled).
    func tapWhenSettled(timeout: TimeInterval = 10) {
        waitUntilSettled(timeout: timeout)
        tap()
    }
}
