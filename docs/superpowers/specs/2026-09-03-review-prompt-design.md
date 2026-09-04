# Asking for an App Store review

Written 2026-09-03 for Hidde, who asked to research the convention for
app-review flows and build it.

## The convention, and where it was read

Apple's own guidance (developer.apple.com, read 2026-09-03): use
`SKStoreReviewController` (in SwiftUI, the `.requestReview` environment
action), never a custom dialog. Ask "at the end of a sequence of events the
user has successfully completed," never from a button, never on launch.
App Store Review Guideline 5.6.1 forbids a custom "are you enjoying the
app?" gate in front of the native prompt (satisfaction gating) and forbids
wiring the call to a "Rate us" button. iOS itself throttles the actual
popup to at most 3 times per 365 days regardless of how often the app calls
the API, but well-behaved apps still self-limit to genuine milestones.

Sources:
- https://developer.apple.com/documentation/storekit/requesting-app-store-reviews
- https://www.avanderlee.com/swift/skstorereviewcontroller-app-ratings/
- https://criticalmoments.io/blog/skstorereviewcontroller_guide_with_examples

AllTrails-style outdoor apps (the reference product this codebase names for
walk-shaped interactions) ask after completing a full trail, the clearest
"successfully completed" moment they have. Our closest equivalent, finishing
a curated Walk, exists (`WalkMode.swift`'s `finishedCard`) but is used by few
people this early, so it would rarely fire. Hidde chose the tree-tick moment
instead (see Decision below).

## The moment already in this codebase that matches

`Kit/Nudge.swift` already runs exactly this shape of ask, for a different
purpose (sign-in): named moments, fired at most once each, a lifetime cap,
and a quiet period between asks. Reusing that architecture for the review
prompt is following our own established convention, which is stronger than
importing an external one from scratch.

`CollectSheet.swift`'s `tickedState` view ("You found \(t.name)") is
explicitly commented as "the payoff... the app's job at that exact second is
to tell them what it is" — the genuine successfully-completed moment Apple's
guidance asks for.

## Decision, confirmed with Hidde

- **Trigger: ticking a tree only**, not walk completion. Reasoning: works for
  everyone regardless of whether they use the Walks feature, which is still
  lightly used.
- **Milestones: the 3rd, 10th and 25th tree ticked** (by `saved.visitedCount`
  at the moment of a tick), each asked at most once, at least 7 days apart,
  capped at 3 asks ever. The count "3" echoes the existing "third save...
  starts to look like a collection" reasoning already in Nudge.swift. 10 and
  25 are this design's own choice (Apple sets no specific numbers), approved
  by Hidde alongside the rest of the design.

## What gets built

**`Kit/ReviewPrompt.swift`**, mirroring `Nudge.swift`'s shape:
- `@MainActor @Observable final class ReviewPrompt`
- UserDefaults-backed `fired: Set<String>` (`reviewPrompt.fired.v1`) and
  `last: Date?` (`reviewPrompt.last.v1`), independent of Nudge's own keys.
- `milestones: [(name: String, count: Int)]` = `[("first", 3), ("second", 10),
  ("third", 25)]`.
- `func consider(ticked total: Int) -> Bool` — called after a successful
  tick. Returns `true` (and marks the moment fired, records `last`) the
  first time `total` reaches an unfired milestone, provided the quiet period
  and lifetime cap allow it. Returns `false` otherwise, including whenever
  running under XCTest.
- Test suppression: the `XCTestConfigurationFilePath` environment guard
  reliably covers unit tests, but does NOT reliably cover UI tests (the app
  under test runs as a separate process from the XCTest runner, and that
  variable is set in the runner's environment, not necessarily the app's).
  UI tests therefore rely on the explicit `-no-review-prompt` launch
  argument, which the shared launch-argument helper in every UI test file
  that can reach a tick now passes.

**Wiring:**
- `ContentView.swift` gains `@State fileprivate var reviewPrompt =
  ReviewPrompt()` beside the existing `nudge`, injected the same way
  (`.environment(root.reviewPrompt)`).
- `CollectSheet.swift` (the `View` struct itself, `tickedState` is just a
  private func on it) gains `@Environment(ReviewPrompt.self) private var
  reviewPrompt` and `@Environment(\.requestReview) private var
  requestReview` (StoreKit's SwiftUI action), mirroring how it already holds
  `@Environment(Nudge.self) private var nudge`.
- At the point a tick succeeds (`withAnimation(.snappy) { stage =
  .ticked(t.id) }`, `CollectSheet.swift:422`), call `reviewPrompt.consider
  (ticked: saved.visitedCount)`; if it returns `true`, call
  `requestReview()`. Nothing else about the tick flow changes.

**`CONVENTIONS.md`**: a new entry recording the interaction, the Apple
guideline it follows, why no custom gate is shown, and the sources above —
satisfying `scripts/conventioncheck.py` and the standing rule that a lookup
gets written down once.

## What this deliberately does not do

- No custom "enjoying the app?" screen. The native call is the whole UI.
- No trigger tied to walk completion, session count, or days-since-install.
  Those are real conventions too, but Hidde chose the single tick-based
  trigger for this build; a future pass can add another moment the same way
  Nudge has two.
- No app-version gating. Nudge doesn't have it either, and the quiet-period
  plus lifetime cap already does the restraining this small a user base
  needs.

## Testing

- A unit-style check that `ReviewPrompt.consider` returns `true` exactly once
  per milestone, respects the 7-day quiet gate, and stops after 3 asks.
- Confirm `ProcessInfo` env guard: running under the existing UI test target
  (`XCTestConfigurationFilePath` is always set there) means `consider` always
  returns `false`, so no existing UI test needs to be touched to stay safe
  from an unexpected system dialog.
- `appfit`/`appsweep` are unaffected (no new screen, no layout).
