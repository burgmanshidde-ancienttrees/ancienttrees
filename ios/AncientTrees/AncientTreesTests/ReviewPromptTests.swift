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

    // MARK: - counting the trees somebody has looked at

    @Test func countsEachTreeOnce() {
        // Three trees means three DIFFERENT trees. Opening one yew three
        // times is the case this guards, and it is the common one: back,
        // reopen, back.
        let s = Scratch(); defer { s.clean() }
        let prompt = ReviewPrompt(defaults: s.defaults, suppressed: false)
        prompt.saw("lon_001"); prompt.saw("lon_001"); prompt.saw("lon_001")
        #expect(prompt.seenCount == 1)
        #expect(prompt.consider() == false)
    }

    @Test func asksAtTheThirdDifferentTree() {
        let s = Scratch(); defer { s.clean() }
        let prompt = ReviewPrompt(defaults: s.defaults, suppressed: false)
        prompt.saw("lon_001"); prompt.saw("lon_002")
        #expect(prompt.consider() == false)
        #expect(prompt.pending == false)

        prompt.saw("lon_003")
        #expect(prompt.consider() == true)
        #expect(prompt.pending == true)
    }

    @Test func stopsRecordingPastTheLastMilestone() {
        // Nothing above the highest threshold can change a decision, so the
        // set must not grow forever in UserDefaults.
        let s = Scratch(); defer { s.clean() }
        let prompt = ReviewPrompt(defaults: s.defaults, suppressed: false)
        for i in 0..<60 { prompt.saw("tree_\(i)") }
        #expect(prompt.seenCount == ReviewPrompt.milestones.last!.count)
    }

    // MARK: - the instance, and its persistence

    @Test func consideringPersistsTheMilestoneSoItDoesNotAskTwice() {
        // suppressed: false bypasses the XCTest environment guard, which is
        // otherwise always on during any xcodebuild test run (see
        // ReviewPrompt.swift's `suppressedOverride`). This test is about
        // the persistence logic, not the guard. neverFiresUnderXCTest
        // below covers the guard itself. The second call is 8 days later,
        // past the quiet period, so a `false` there proves "first" is
        // recorded as fired rather than merely proving the quiet period
        // blocked a same-instant repeat (which holdsOffUntilTheQuietPeriodPasses
        // already covers on the pure function).
        let s = Scratch(); defer { s.clean() }
        let prompt = ReviewPrompt(defaults: s.defaults, suppressed: false)
        let now = Date()
        let eightDaysLater = now.addingTimeInterval(8 * 86_400)
        prompt.saw("a"); prompt.saw("b"); prompt.saw("c")

        #expect(prompt.consider(now: now) == true)
        #expect(prompt.consider(now: eightDaysLater) == false)
    }

    @Test func remembersTheTreesSeenAcrossLaunches() {
        // The counter has to survive the app being closed, or a person who
        // looks at two trees a day never reaches three.
        let s = Scratch(); defer { s.clean() }
        let first = ReviewPrompt(defaults: s.defaults, suppressed: false)
        first.saw("a"); first.saw("b")

        let second = ReviewPrompt(defaults: s.defaults, suppressed: false)
        #expect(second.seenCount == 2)
        second.saw("c")
        #expect(second.consider() == true)
    }

    @Test func neverFiresUnderXCTest() {
        // This test itself runs under XCTest, so the real environment guard
        // inside `consider` should refuse regardless of the milestone data.
        // That guard is what keeps a UI test from ever popping a real
        // system dialog, so it is worth asserting directly rather than
        // trusting the pure function alone.
        let s = Scratch(); defer { s.clean() }
        let prompt = ReviewPrompt(defaults: s.defaults)
        prompt.saw("a"); prompt.saw("b"); prompt.saw("c")
        #expect(prompt.consider() == false)
        #expect(prompt.pending == false)
    }
}
