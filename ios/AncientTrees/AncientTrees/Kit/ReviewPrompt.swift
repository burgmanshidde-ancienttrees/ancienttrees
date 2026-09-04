// Asking for an App Store review, the same restraint as Nudge.swift but for
// a different ask.
//
// Convention: Apple's own developer guidance (developer.apple.com, read
// 2026-09-03) says to use the native SKStoreReviewController prompt only,
// never a custom "are you enjoying this?" gate in front of it (App Store
// Review Guideline 5.6.1 forbids that), and to ask at the end of a sequence
// the person has just completed successfully, never from a button and
// never on launch. See CONVENTIONS.md.
//
// The moment we use is ticking a tree: CollectSheet's own comment already
// calls that "the payoff... the app's job at that exact second is to tell
// them what it is", which is exactly Apple's "successfully completed"
// moment. Three escalating milestones, each asked at most once, at least a
// week apart, three asks in the phone's lifetime: the same shape as
// Nudge's own restraint, and the count 3 echoes Nudge's own "third save...
// starts to look like a collection" reasoning.

import Foundation
import Observation

@MainActor
@Observable
public final class ReviewPrompt {
    private let defaults: UserDefaults
    private let firedKey = "reviewPrompt.fired.v1"
    private let lastKey = "reviewPrompt.last.v1"
    private let maxAsks = 3
    private let quietDays = 7.0
    private let suppressedOverride: Bool?

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

    /// `suppressedOverride` exists only for ReviewPromptTests: production
    /// code (and every other caller) leaves it `nil` and gets the safe
    /// default below, which cannot be forgotten. A unit test that needs to
    /// exercise `consider()`'s actual decision-making (rather than confirm
    /// it is suppressed) passes `suppressed: false` explicitly, because the
    /// XCTest environment guard is otherwise ALWAYS true for any
    /// `xcodebuild test` invocation, individual or full-suite alike — there
    /// is no environment state in which a test could observe `consider()`
    /// returning `true` without this seam.
    public init(defaults: UserDefaults = .standard, suppressed: Bool? = nil) {
        self.defaults = defaults
        self.suppressedOverride = suppressed
        if ProcessInfo.processInfo.arguments.contains("-reset-collection") {
            defaults.removeObject(forKey: firedKey)
            defaults.removeObject(forKey: lastKey)
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

    /// The pure decision, kept apart from `suppressed` so its milestone,
    /// quiet-period and lifetime-cap logic can be unit tested without the
    /// XCTest guard silencing every call.
    static func milestone(for total: Int, fired: Set<String>, last: Date?, now: Date,
                           maxAsks: Int, quietDays: Double) -> String? {
        guard fired.count < maxAsks else { return nil }
        if let last, now.timeIntervalSince(last) < quietDays * 86_400 { return nil }
        return milestones.first { total >= $0.count && !fired.contains($0.name) }?.name
    }

    /// Called after a tree is ticked. Returns `true` the moment a new
    /// milestone is reached and conditions allow it; the caller then, and
    /// only then, calls SwiftUI's `\.requestReview` action.
    @discardableResult
    public func consider(ticked total: Int, now: Date = Date()) -> Bool {
        guard !suppressed else { return false }
        guard let name = Self.milestone(for: total, fired: fired, last: last, now: now,
                                         maxAsks: maxAsks, quietDays: quietDays) else {
            return false
        }
        var f = fired
        f.insert(name)
        fired = f
        last = now
        return true
    }
}
