// When to ask, which is the whole design and not a detail.
//
// Hidde's ruling on 2026-08-20 was the soft wall: saving and ticking work
// straight away with no account, and the ask arrives once there is something to
// lose. The reasoning is that AllTrails can put a wall in front of you because
// you already came looking for a named trail and they have a million reviews to
// stand on. We have neither, so a wall before anybody has felt anything buys a
// bounce rather than an account.
//
// Three rules, and they are all about restraint:
//
// 1. NEVER ON LAUNCH. An app that asks who you are before it has shown you
//    anything is asking for a favour it has not earned.
// 2. ASK AT THE MOMENT THE THING BECOMES WORTH KEEPING. That is the first time
//    somebody ticks a tree off, because a tick is a memory rather than a
//    bookmark, and again at the third save, because three is when a list starts
//    to look like a collection.
// 3. ASK AT MOST THREE TIMES, EVER, AND NEVER TWICE IN A WEEK. A prompt that
//    keeps coming back does not convert better, it teaches people to dismiss
//    things without reading them, and then the one honest warning we ever need
//    to show gets dismissed too.
//
// Everything else is passive: a row on You and a line on Saved that state
// plainly where the collection lives. Those are always there, cost nothing, and
// are the surface most people will actually sign in from.

import Foundation
import Observation

/// Main-actor isolated, like every store the root holds. See Account.swift for
/// why: SwiftUI already reads these from the main actor, so the annotation
/// costs nothing at runtime and makes a background write a compiler error
/// instead of a data race nobody can reproduce.
@MainActor
@Observable
public final class Nudge {
    private let firedKey = "nudge.fired.v1"     // which moments have been used
    private let lastKey = "nudge.last.v1"       // when we last asked
    private let maxAsks = 3
    private let quietDays = 7.0

    private var fired: Set<String> {
        get { Set(UserDefaults.standard.stringArray(forKey: firedKey) ?? []) }
        set { UserDefaults.standard.set(Array(newValue), forKey: firedKey) }
    }
    private var last: Date? {
        get { UserDefaults.standard.object(forKey: lastKey) as? Date }
        set { UserDefaults.standard.set(newValue, forKey: lastKey) }
    }

    /// Set when a moment qualifies; the view presents a sheet off it.
    public var pending: SignInReason?

    public init() {
        // -reset-collection wipes Saved and Sightings, and until 2026-08-23 it
        // left THIS behind, which made every test that ticks a tree depend on
        // whatever an earlier run had already fired. On a simulator that had
        // asked once, `quiet` was true and no sheet appeared; on a freshly
        // erased one the first tick raised the sign-in sheet over the walk and
        // the walk test could no longer read its own counter. It failed for
        // days, on main, for a reason that had nothing to do with walks.
        //
        // The product behaviour is untouched: the nudge still fires for a real
        // person on their first tick, which is the whole point of it.
        if ProcessInfo.processInfo.arguments.contains("-reset-collection") {
            UserDefaults.standard.removeObject(forKey: firedKey)
            UserDefaults.standard.removeObject(forKey: lastKey)
        }
    }

    private var quiet: Bool {
        // A test that ticks a tree is not testing the nudge, and until this
        // existed it was silently at the mercy of one: on a simulator that had
        // already been asked, no sheet appeared and the walk test passed; on a
        // freshly erased one the first tick raised the sign-in sheet over the
        // walk and the counter behind it could not be read. Same code, same
        // walk, opposite result, decided by leftover UserDefaults.
        if ProcessInfo.processInfo.arguments.contains("-no-nudge") { return true }
        if fired.count >= maxAsks { return true }
        if let last, Date().timeIntervalSince(last) < quietDays * 86_400 { return true }
        return false
    }

    /// Somebody just ticked a tree off. The strongest moment there is, because
    /// they are standing in front of it and have just made a record of that.
    public func ticked(treeName: String, signedIn: Bool, total: Int) {
        guard !signedIn, !quiet, !fired.contains("first-tick") else { return }
        mark("first-tick")
        pending = .keepTree(treeName)
    }

    /// The list has started to look like a collection.
    public func saved(count: Int, signedIn: Bool) {
        guard !signedIn, !quiet, count >= 3, !fired.contains("third-save") else { return }
        mark("third-save")
        pending = .keepCollection(count)
    }

    /// A GATE rather than a nudge, and the difference is the whole reason this
    /// method is separate from the two above it.
    ///
    /// Hidde reversed his own soft-wall ruling on 2026-08-25, having signed out
    /// and found he could still heart a tree: "all these functionalities of
    /// saving stuff should only be available when you sign in, and when you try
    /// to do it, you should get a message saying you need to sign in." So the
    /// ask is no longer a suggestion at a good moment, it is the answer to a
    /// tap that cannot go through, and none of the restraint rules apply: not
    /// the three-asks cap, not the quiet week, not the once-per-moment mark.
    /// Suppressing this one would leave a heart that does nothing and says
    /// nothing, which is worse than either wall.
    ///
    /// The comment at the top of this file is the argument he overruled. It is
    /// left standing because it is still the reasoning, and if signups fall
    /// after this it is the first thing to read.
    public func require(_ reason: SignInReason) {
        pending = reason
    }

    private func mark(_ moment: String) {
        var f = fired
        f.insert(moment)
        fired = f
        last = Date()
    }
}
