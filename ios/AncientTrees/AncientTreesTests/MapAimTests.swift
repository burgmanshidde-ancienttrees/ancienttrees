// The opening shot, and the one case it never retook.
//
// Hidde, 2026-09-03: "op de eerste open toen ik mn locatie had gedeeld bleef ik
// op Amsterdam staan. Maar na re-open opende de app wel mooi op Leuven."
//
// A cold first launch has no fix yet, so `origin` falls through to Dam square
// and the map takes its single shot there. The fix lands a second or two later
// and the camera never moved, because settle() aims once. The next launch works
// because LocationProvider.remembered now holds the real place, so the single
// shot is taken at the right one.
//
// The decision is tested rather than the situation, which is the same shape as
// the camera-permission fix: a simulator cannot hand a map a late fix, and it
// does not have to, because what went wrong is a boolean.

import Testing
import Foundation
@testable import AncientTrees

struct TheMapAimsAtTheRealPlace {

    /// The state a cold launch starts in.
    private func aim(userMoved: Bool = false, aimed: Bool = true, selecting: Bool = false,
                     coverage: CGFloat = 168, aimedCoverage: CGFloat = 168,
                     hasFix: Bool = false, aimedWithFix: Bool = false) -> Bool {
        TreeMap.shouldAim(userMoved: userMoved, aimed: aimed, selecting: selecting,
                          coverage: coverage, aimedCoverage: aimedCoverage,
                          hasFix: hasFix, aimedWithFix: aimedWithFix)
    }

    @Test func aimsWhenItNeverHas() {
        #expect(aim(aimed: false))
    }

    /// THE BUG. Aimed at the fallback, then the phone answers.
    @Test func aimsAgainWhenTheGuessBecomesAnAnswer() {
        #expect(aim(hasFix: true, aimedWithFix: false))
    }

    /// And exactly once: walking must not drag the camera about.
    @Test func doesNotChaseYouOnceItHasAimedAtAFix() {
        #expect(!aim(hasFix: true, aimedWithFix: true))
    }

    /// A finger on the map ends the aiming, fix or no fix.
    @Test func aHandOnTheMapEndsIt() {
        #expect(!aim(userMoved: true, hasFix: true, aimedWithFix: false))
        #expect(!aim(userMoved: true, aimed: false))
    }

    /// The camera belongs to the pager while a tree is open.
    @Test func doesNotYankTheCameraOffASelectedTree() {
        #expect(!aim(selecting: true, hasFix: true, aimedWithFix: false))
    }

    /// Still no fix, nothing to retake.
    @Test func staysPutWhileNothingHasChanged() {
        #expect(!aim())
    }

    /// The retake settle() already had: a shot taken before the sheet had
    /// reported its height, retaken once the inset is real.
    @Test func retakesAShotTakenBeforeTheSheetSpoke() {
        #expect(aim(coverage: 168, aimedCoverage: 0))
        #expect(!aim(coverage: 168, aimedCoverage: 166))
    }
}
