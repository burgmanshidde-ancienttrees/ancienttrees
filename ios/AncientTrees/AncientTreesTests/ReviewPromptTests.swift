// The review-ask restraint, tested the same way Saved's and Account's
// UserDefaults-backed state is: a scratch suite per test so nothing leaks
// into the real one, and every test cleans up after itself.

import Testing
import Foundation
@testable import AncientTrees

@MainActor
@Suite(.serialized)
struct ReviewPromptTests {

    private struct Scratch {
        let name = "test.reviewPrompt." + UUID().uuidString
        var defaults: UserDefaults { UserDefaults(suiteName: name)! }
        func clean() { UserDefaults.standard.removePersistentDomain(forName: name) }
    }

    // MARK: - the pure decision

    @Test func staysQuietBeforeTheFirstMilestone() {
        let name = ReviewPrompt.milestone(for: 2, fired: [], last: nil, now: Date(),
                                           maxAsks: 3, quietDays: 7)
        #expect(name == nil)
    }

    @Test func firesOnceAtTheThirdTree() {
        let name = ReviewPrompt.milestone(for: 3, fired: [], last: nil, now: Date(),
                                           maxAsks: 3, quietDays: 7)
        #expect(name == "first")
    }

    @Test func doesNotRepeatAnAlreadyFiredMilestone() {
        let name = ReviewPrompt.milestone(for: 3, fired: ["first"], last: nil, now: Date(),
                                           maxAsks: 3, quietDays: 7)
        #expect(name == nil)
    }

    @Test func holdsOffUntilTheQuietPeriodPasses() {
        let now = Date()
        let sixDaysAgo = now.addingTimeInterval(-6 * 86_400)
        let name = ReviewPrompt.milestone(for: 10, fired: ["first"], last: sixDaysAgo, now: now,
                                           maxAsks: 3, quietDays: 7)
        #expect(name == nil)
    }

    @Test func firesAgainOnceTheQuietPeriodHasPassed() {
        let now = Date()
        let eightDaysAgo = now.addingTimeInterval(-8 * 86_400)
        let name = ReviewPrompt.milestone(for: 10, fired: ["first"], last: eightDaysAgo, now: now,
                                           maxAsks: 3, quietDays: 7)
        #expect(name == "second")
    }

    @Test func stopsAfterTheLifetimeCap() {
        let now = Date()
        let longAgo = now.addingTimeInterval(-365 * 86_400)
        let name = ReviewPrompt.milestone(for: 999, fired: ["first", "second", "third"],
                                           last: longAgo, now: now, maxAsks: 3, quietDays: 7)
        #expect(name == nil)
    }

    // MARK: - the instance, and its persistence

    @Test func consideringPersistsTheMilestoneSoItDoesNotAskTwice() {
        let s = Scratch(); defer { s.clean() }
        let prompt = ReviewPrompt(defaults: s.defaults)
        let now = Date()

        #expect(prompt.consider(ticked: 3, now: now) == true)
        #expect(prompt.consider(ticked: 3, now: now) == false)
    }

    @Test func neverFiresUnderXCTest() {
        // This test itself runs under XCTest, so the real environment guard
        // inside `consider` should refuse regardless of the milestone data.
        // That guard is what keeps a UI test from ever popping a real
        // system dialog, so it is worth asserting directly rather than
        // trusting the pure function alone.
        let s = Scratch(); defer { s.clean() }
        let prompt = ReviewPrompt(defaults: s.defaults)
        #expect(prompt.consider(ticked: 3) == false)
    }
}
