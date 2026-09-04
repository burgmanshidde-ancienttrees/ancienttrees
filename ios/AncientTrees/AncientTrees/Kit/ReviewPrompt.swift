// Asking for an App Store review, the same restraint as Nudge.swift but for
// a different ask.
//
// Convention: Apple's own developer guidance (developer.apple.com, read
// 2026-09-03) says to use the native SKStoreReviewController prompt only,
// never a custom "are you enjoying this?" gate in front of it (App Store
// Review Guideline 5.6.1 forbids that), and to ask once somebody has shown
// engagement, at a pause rather than in the middle of something. Never from
// a button and never on launch. See CONVENTIONS.md.
//
// WHAT COUNTS AS ENGAGEMENT CHANGED ON 2026-09-04, on Hidde's ruling:
// "afgevinkte bomen is wel te lang - ik denk naar 3 bomen bekeken in de
// app". The first version counted trees TICKED OFF, which is the strongest
// signal there is and also the rarest: a tick means somebody stood in front
// of a trunk with a camera, so three of them is weeks of walking, and the
// ask would have reached almost nobody. Three trees LOOKED AT is a bar
// every interested person clears in one sitting, and it is still engagement
// rather than a launch counter.
//
// Two moments ask, because the counter and the moment are different things.
// Closing a tree page is the pause: the reader finished something and is
// back on a list. Ticking a tree off is the payoff, described in
// CollectSheet's own comment as "the app's job at that exact second".
// Whichever comes first wins, and both share one lifetime cap.
//
// Three escalating milestones, each asked at most once, at least a week
// apart, three asks in the phone's lifetime.

import Foundation
import Observation

@MainActor
@Observable
public final class ReviewPrompt {
    private let defaults: UserDefaults
    // v2: the milestone numbers used to mean trees ticked and now mean trees
    // seen, so an early tester's fired set would silence an ask it never
    // actually made under the new rule.
    private let firedKey = "reviewPrompt.fired.v2"
    private let lastKey = "reviewPrompt.last.v2"
    private let seenKey = "reviewPrompt.seen.v1"
    private let maxAsks = 3
    private let quietDays = 7.0
    private let suppressedOverride: Bool?

    /// Set the moment a milestone is reached; the ROOT view watches this and
    /// performs the system ask. It lives there rather than in the screen that
    /// noticed, because the screen that notices is usually the one going
    /// away: a tree page asks on the way out, and a view that is leaving the
    /// hierarchy is a bad place from which to present anything.
    public var pending = false

    /// Ordered so the first unfired, met threshold wins. Named rather than
    /// indexed so a milestone stays stable if the list ever grows.
    static let milestones: [(name: String, count: Int)] = [
        ("first", 3), ("second", 10), ("third", 25),
    ]

    private var fired: Set<String> {
        get { Set(defaults.stringArray(forKey: firedKey) ?? []) }
        set { defaults.set(Array(newValue), forKey: firedKey) }
    }
    private var last: Date? {
        get { defaults.object(forKey: lastKey) as? Date }
        set { defaults.set(newValue, forKey: lastKey) }
    }

    /// The trees this phone has opened, by id. A SET rather than a tally
    /// because "three trees" means three different ones: opening the same
    /// yew three times is one tree looked at three times, and a counter
    /// cannot tell those apart.
    private var seen: Set<String> {
        get { Set(defaults.stringArray(forKey: seenKey) ?? []) }
        set { defaults.set(Array(newValue), forKey: seenKey) }
    }

    public var seenCount: Int { seen.count }

    public init(defaults: UserDefaults = .standard, suppressed: Bool? = nil) {
        self.defaults = defaults
        self.suppressedOverride = suppressed
        if ProcessInfo.processInfo.arguments.contains("-reset-collection") {
            defaults.removeObject(forKey: firedKey)
            defaults.removeObject(forKey: lastKey)
            defaults.removeObject(forKey: seenKey)
        }
    }

    /// Off whenever a test runner is attached, so no UI test can forget to
    /// suppress a real system dialog, plus an explicit flag for symmetry
    /// with Nudge's `-no-nudge`.
    private var suppressed: Bool {
        if let suppressedOverride { return suppressedOverride }
        return ProcessInfo.processInfo.environment["XCTestConfigurationFilePath"] != nil
            || ProcessInfo.processInfo.arguments.contains("-no-review-prompt")
    }

    /// Record that a tree page was opened. Stops recording once the last
    /// milestone is behind us, so this never grows past ~25 ids in defaults:
    /// nothing above the highest threshold can change any decision.
    public func saw(_ treeId: String) {
        guard let ceiling = Self.milestones.last?.count, seen.count < ceiling else { return }
        var s = seen
        s.insert(treeId)
        seen = s
    }

    /// The pure decision, kept apart from `suppressed` so its milestone,
    /// quiet-period and lifetime-cap logic can be unit tested without the
    /// XCTest guard silencing every call.
    static func milestone(for total: Int, fired: Set<String>, last: Date?, now: Date,
                           maxAsks: Int, quietDays: Double) -> String? {
        guard fired.count < maxAsks else { return nil }
        if let last, now.timeIntervalSince(last) < quietDays * 86_400 { return nil }
        return milestones.first { total >= $0.count && !fired.contains($0.name) }?.name
    }

    /// Called at a pause: a tree page closing, or a tree just ticked off.
    /// Sets `pending` when a new milestone is reached and conditions allow
    /// it, which is the root's cue to make the system ask. Returns the same
    /// answer for a caller that wants to know.
    @discardableResult
    public func consider(now: Date = Date()) -> Bool {
        guard !suppressed else { return false }
        guard let name = Self.milestone(for: seen.count, fired: fired, last: last, now: now,
                                         maxAsks: maxAsks, quietDays: quietDays) else {
            return false
        }
        var f = fired
        f.insert(name)
        fired = f
        last = now
        pending = true
        return true
    }
}
