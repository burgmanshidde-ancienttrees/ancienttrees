# App Store Review Prompt Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ask the native App Store review dialog after somebody ticks their 3rd, 10th and 25th tree, following Apple's own SKStoreReviewController convention and this codebase's existing Nudge.swift restraint pattern.

**Architecture:** One new `@Observable` class, `ReviewPrompt`, holds a pure static milestone-decision function plus a thin UserDefaults-backed wrapper. It is injected as a root environment object exactly like `Nudge`, and called from the one place a tick actually succeeds, `CollectSheet.claim(_:image:at:)`. Both places that present `CollectSheet` (the shared `appObjects` extension and `WalkMode`'s hand-rolled sheet) must carry the new environment object, or the app crashes at that sheet.

**Tech Stack:** Swift, SwiftUI (`@Observable`/`@Environment`), StoreKit (`\.requestReview`), Swift Testing (`@Test`/`#expect`), Xcode project with file-system-synchronized groups (new files under `Kit/` and test files under `AncientTreesTests/` are picked up automatically, no `.pbxproj` edit needed).

## Global Constraints

- Trigger: only ticking a tree (via `CollectSheet.claim`). Never walk completion, never a button, never app launch.
- Milestones: the 3rd, 10th and 25th tree ticked, counted by `saved.visitedCount` at the moment of a successful tick.
- Each milestone fires at most once; at least 7 days between any two asks; at most 3 asks in the phone's lifetime.
- The only UI is the native `\.requestReview` SwiftUI environment action (StoreKit). No custom "are you enjoying the app?" screen — App Store Review Guideline 5.6.1 forbids gating the native prompt.
- Always suppressed when running under XCTest (`ProcessInfo.processInfo.environment["XCTestConfigurationFilePath"] != nil`), regardless of any launch argument, so no test can forget to guard against a real system dialog. Additionally suppressed by an explicit `-no-review-prompt` launch argument, for symmetry with `-no-nudge`.
- Record the interaction in `CONVENTIONS.md` with its sources, per the standing "a lookup you have to repeat is a lookup that gets skipped" rule.
- Spec: `docs/superpowers/specs/2026-09-03-review-prompt-design.md`.

---

### Task 1: `ReviewPrompt` core logic and its tests

**Files:**
- Create: `ios/AncientTrees/AncientTrees/Kit/ReviewPrompt.swift`
- Create: `ios/AncientTrees/AncientTreesTests/ReviewPromptTests.swift`

**Interfaces:**
- Produces: `@MainActor @Observable public final class ReviewPrompt`
  - `public init(defaults: UserDefaults = .standard)`
  - `static let milestones: [(name: String, count: Int)]` = `[("first", 3), ("second", 10), ("third", 25)]`
  - `static func milestone(for total: Int, fired: Set<String>, last: Date?, now: Date, maxAsks: Int, quietDays: Double) -> String?` — pure decision, no I/O.
  - `@discardableResult public func consider(ticked total: Int, now: Date = Date()) -> Bool` — the instance entry point CollectSheet calls.

- [ ] **Step 1: Write the failing tests**

Create `ios/AncientTrees/AncientTreesTests/ReviewPromptTests.swift`:

```swift
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
```

- [ ] **Step 2: Run the tests to verify they fail to compile**

```bash
xcodebuild test \
  -project ios/AncientTrees/AncientTrees.xcodeproj \
  -scheme AncientTrees \
  -destination "platform=iOS Simulator,name=iPhone 17 Pro" \
  -only-testing:AncientTreesTests/ReviewPromptTests \
  CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO CODE_SIGN_IDENTITY="" \
  2>&1 | grep -E "error:|BUILD"
```

Expected: `error: cannot find 'ReviewPrompt' in scope` (or similar), `** BUILD FAILED **`.

- [ ] **Step 3: Write the implementation**

Create `ios/AncientTrees/AncientTrees/Kit/ReviewPrompt.swift`:

```swift
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

    public init(defaults: UserDefaults = .standard) {
        self.defaults = defaults
    }

    /// Off whenever a test runner is attached, so no UI test can forget to
    /// suppress a real system dialog, plus an explicit flag for symmetry
    /// with Nudge's `-no-nudge`.
    private var suppressed: Bool {
        ProcessInfo.processInfo.environment["XCTestConfigurationFilePath"] != nil
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
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
xcodebuild test \
  -project ios/AncientTrees/AncientTrees.xcodeproj \
  -scheme AncientTrees \
  -destination "platform=iOS Simulator,name=iPhone 17 Pro" \
  -only-testing:AncientTreesTests/ReviewPromptTests \
  CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO CODE_SIGN_IDENTITY="" \
  2>&1 | grep -E "Test case|error:|\*\* (TEST|BUILD)"
```

Expected: eight `Test case ... passed`, `** TEST SUCCEEDED **`.

- [ ] **Step 5: Commit**

```bash
git add ios/AncientTrees/AncientTrees/Kit/ReviewPrompt.swift \
        ios/AncientTrees/AncientTreesTests/ReviewPromptTests.swift
git commit -m "$(cat <<'EOF'
Add ReviewPrompt: the milestone logic for the App Store review ask

Pure static decision (milestone/quiet-period/lifetime-cap) plus a thin
UserDefaults-backed wrapper, same shape as Nudge.swift. Not wired into
any screen yet.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Wire it into the tick flow

**Files:**
- Modify: `ios/AncientTrees/AncientTrees/ContentView.swift:38` (add root state), `:926` (add to `appObjects`)
- Modify: `ios/AncientTrees/AncientTrees/Screens/CollectSheet.swift:55-57` (import), `:70` (environment properties), `:418-423` (`claim`)
- Modify: `ios/AncientTrees/AncientTrees/Screens/WalkMode.swift:46` (environment property), `:181-190` (its own `CollectSheet` sheet)

**Interfaces:**
- Consumes: `ReviewPrompt` from Task 1 (`init(defaults:)`, `consider(ticked:now:)`).
- Produces: nothing further downstream; this is the leaf that calls `requestReview()`.

**Why three files, not one:** `CollectSheet` is presented as a `.sheet` from two places, and a SwiftUI sheet does not inherit environment objects from the view that presents it — that exact trap is called out in `ContentView.swift`'s `appObjects` doc comment ("trapped the app twice in two days") and again in `WalkMode.swift`'s own comment on the same subject. Missing either injection site produces a crash the moment that sheet's `CollectSheet` reads `@Environment(ReviewPrompt.self)`, not a compile error.

- [ ] **Step 1: Add the root state object in `ContentView.swift`**

Find (`ContentView.swift:38`):

```swift
    @State fileprivate var nudge = Nudge()
```

Replace with:

```swift
    @State fileprivate var nudge = Nudge()
    @State fileprivate var reviewPrompt = ReviewPrompt()
```

- [ ] **Step 2: Add it to the shared `appObjects` extension in `ContentView.swift`**

Find (`ContentView.swift:926`):

```swift
            .environment(root.nudge)
```

Replace with:

```swift
            .environment(root.nudge)
            .environment(root.reviewPrompt)
```

- [ ] **Step 3: Import StoreKit and add the two environment properties in `CollectSheet.swift`**

Find (`CollectSheet.swift:55-57`):

```swift
import CoreLocation
import Photos
import SwiftUI
```

Replace with:

```swift
import CoreLocation
import Photos
import StoreKit
import SwiftUI
```

Find (`CollectSheet.swift:70`):

```swift
    @Environment(Nudge.self) private var nudge
```

Replace with:

```swift
    @Environment(Nudge.self) private var nudge
    @Environment(ReviewPrompt.self) private var reviewPrompt
    @Environment(\.requestReview) private var requestReview
```

- [ ] **Step 4: Call it from the one place a tick actually succeeds, in `CollectSheet.swift`**

Find (`CollectSheet.swift:418-423`):

```swift
    private func claim(_ t: Tree, image: UIImage, at here: (lat: Double, lng: Double)) {
        if !saved.isVisited(t.id) { saved.toggleVisited(t.id) }
        sightings.record(treeId: t.id, name: t.name, lat: t.lat, lng: t.lng,
                         image: image, date: taken ?? Date())
        withAnimation(.snappy) { stage = .ticked(t.id) }
    }
```

Replace with:

```swift
    private func claim(_ t: Tree, image: UIImage, at here: (lat: Double, lng: Double)) {
        if !saved.isVisited(t.id) { saved.toggleVisited(t.id) }
        sightings.record(treeId: t.id, name: t.name, lat: t.lat, lng: t.lng,
                         image: image, date: taken ?? Date())
        withAnimation(.snappy) { stage = .ticked(t.id) }
        // "You found \(t.name)" below is the payoff moment; see
        // ReviewPrompt.swift and CONVENTIONS.md for why this is where the
        // native ask belongs and nowhere else.
        if reviewPrompt.consider(ticked: saved.visitedCount) {
            requestReview()
        }
    }
```

- [ ] **Step 5: Add the environment property in `WalkMode.swift`**

Find (`WalkMode.swift:46`):

```swift
    @Environment(Nudge.self) private var nudge
```

Replace with:

```swift
    @Environment(Nudge.self) private var nudge
    @Environment(ReviewPrompt.self) private var reviewPrompt
```

- [ ] **Step 6: Pass it into WalkMode's own `CollectSheet` sheet**

Find (`WalkMode.swift:181-190`):

```swift
        .sheet(isPresented: $photographing) {
            CollectSheet(catalogue: catalogue, origin: origin, mode: .collect)
                .environment(saved)
                .environment(account)
                .environment(nudge)
                .environment(sightings)
                .environment(navigator)
                .environment(units)
                .environment(entitlement)
        }
```

Replace with:

```swift
        .sheet(isPresented: $photographing) {
            CollectSheet(catalogue: catalogue, origin: origin, mode: .collect)
                .environment(saved)
                .environment(account)
                .environment(nudge)
                .environment(reviewPrompt)
                .environment(sightings)
                .environment(navigator)
                .environment(units)
                .environment(entitlement)
        }
```

- [ ] **Step 7: Verify the app still builds and the existing UI tests that tick trees are unaffected**

```bash
xcodebuild test \
  -project ios/AncientTrees/AncientTrees.xcodeproj \
  -scheme AncientTrees \
  -destination "platform=iOS Simulator,name=iPhone 17 Pro" \
  -only-testing:AncientTreesTests \
  -only-testing:AncientTreesUITests/FlowWalk \
  CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO CODE_SIGN_IDENTITY="" \
  2>&1 | grep -E "Test case|error:|\*\* (TEST|BUILD)"
```

Expected: `** BUILD SUCCEEDED **`, no new failures. (`FlowWalk` exercises the tick flow through `CollectSheet` via the map, not via `WalkMode`; running it confirms the environment wiring in `ContentView.swift` did not regress. `WalkMode`'s own sheet is exercised by `RefusedWalk`/`StressWalk`, which already run in CI on schedule per `ios.yml` and don't need a separate local run here.)

- [ ] **Step 8: Run `netcheck` and `conventioncheck` since a Screens file changed**

```bash
python3 scripts/netcheck.py
python3 scripts/conventioncheck.py ios/AncientTrees/AncientTrees/Screens/CollectSheet.swift ios/AncientTrees/AncientTrees/Screens/WalkMode.swift
```

Expected: both exit 0. (Neither script gates `Kit/ReviewPrompt.swift`: `netcheck` is about network calls bypassing `Kit/Net.swift`, which this feature makes none of, and `conventioncheck` only gates *new* files under `Screens/`, and both edited files here are modifications, not new files.)

- [ ] **Step 9: Commit**

```bash
git add ios/AncientTrees/AncientTrees/ContentView.swift \
        ios/AncientTrees/AncientTrees/Screens/CollectSheet.swift \
        ios/AncientTrees/AncientTrees/Screens/WalkMode.swift
git commit -m "$(cat <<'EOF'
Wire ReviewPrompt into the tick flow

CollectSheet.claim is the one place a tick actually succeeds, reached
both from the map and from WalkMode's own sheet, so both of that
sheet's environment injections needed the new object or the walk path
would have crashed on first tick.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Record the convention

**Files:**
- Modify: `CONVENTIONS.md`

**Interfaces:**
- Consumes: nothing (documentation only).
- Produces: nothing (documentation only).

- [ ] **Step 1: Append the entry**

Add to the end of `CONVENTIONS.md`, following the file's own format (interaction, reference, what it does, source, date):

```markdown
---

## Asking for an App Store review

**Reference: Apple's own SKStoreReviewController guidance**, not a specific
third-party app. Use the native `.requestReview` SwiftUI environment action
only; never a custom "are you enjoying this?" screen in front of it, which
App Store Review Guideline 5.6.1 forbids as satisfaction gating. Never wire
it to a "Rate us" button. Ask at the end of a sequence the person has just
completed successfully, never on launch and never mid-task.

**Where we ask: ticking a tree**, `CollectSheet.claim`, the moment already
described in that file's own comment as "the payoff... the app's job at
that exact second is to tell them what it is." AllTrails-style outdoor
apps ask after completing a whole trail; our closest equivalent is
finishing a curated Walk, but that feature is still lightly used, so the
ask is tied to the tick itself, which works for everyone. See
`Kit/ReviewPrompt.swift` and DECISIONS.md-shaped reasoning in
`docs/superpowers/specs/2026-09-03-review-prompt-design.md`.

**Milestones, our own choice (Apple sets no specific numbers):** the 3rd,
10th and 25th tree ticked, each asked once, at least 7 days apart, 3 asks
in the phone's lifetime. The 3 echoes `Nudge.swift`'s own "third save...
starts to look like a collection" reasoning, reused here as the same
restraint pattern applied to a different ask.

Read 2026-09-03:
- https://developer.apple.com/documentation/storekit/requesting-app-store-reviews
- https://www.avanderlee.com/swift/skstorereviewcontroller-app-ratings/
```

- [ ] **Step 2: Commit**

```bash
git add CONVENTIONS.md
git commit -m "$(cat <<'EOF'
CONVENTIONS.md: record the App Store review-ask convention

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

## Self-review notes (for whoever executes this plan)

- **Spec coverage:** trigger (Task 2 Step 4), milestones and cap (Task 1), native-only call (Task 2 Steps 3-4), test suppression (Task 1, asserted directly in `neverFiresUnderXCTest`), CONVENTIONS.md entry (Task 3). Nothing in the spec is left unaddressed.
- **Two sheet-presentation sites:** this was the one non-obvious gap a fresh implementer would likely miss — `WalkMode.swift` re-injects environment objects by hand rather than using `appObjects`, and skipping it would not fail any build, only crash at runtime the first time someone ticks a tree from inside a Walk. Task 2 Steps 5-6 exist because of that.
- **`saved.visitedCount` semantics:** it counts distinct trees with a `visitedAt` date, already correct for "how many has this person ticked in total" regardless of which screen the tick came from, so no separate counter is needed.
