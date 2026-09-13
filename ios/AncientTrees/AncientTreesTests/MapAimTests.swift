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

/// THE RECENTRE CONTROL, which has been reported four times and fixed by eye
/// three times. Hidde, 2026-09-13: "het lukt me nog steeds het centre knopje
/// weg te slepen bij map als ik de lijst naar beneden en boven sleep."
///
/// The regression each time was the same shape: the control's relationship to
/// the sheet is arithmetic nobody could see except by dragging a list on a
/// phone. So the arithmetic is a function now and these are the properties it
/// has to keep. The one that broke on 2026-09-04 is `staysOutOfTheChipsAtEveryHeight`.
struct TheRecentreControlRidesTheSheet {

    /// Both phones the sweep photographs, because `card` is a fixed 400 points
    /// and `half` is a fraction: which of the two is taller flips between them,
    /// and a clamp written as a percentage was wrong on the small one.
    static let phones: [(name: String, height: CGFloat)] = [("SE", 667), ("large", 852)]

    private func place(_ coverage: CGFloat, _ mapHeight: CGFloat) -> (lift: CGFloat, alpha: CGFloat) {
        TreeMap.recentrePlacement(coverage: coverage, mapHeight: mapHeight)
    }

    /// A map with no sheet in front of it looks exactly as it always has.
    @Test func sitsWhereItAlwaysDidWithNoSheet() {
        for phone in Self.phones {
            #expect(place(0, phone.height).lift == -120)
            #expect(place(0, phone.height).alpha == 1)
        }
    }

    /// 12 points of air above the sheet, which is the whole point of it moving.
    @Test func ridesTwelvePointsAboveTheSheet() {
        for phone in Self.phones {
            let peek = SheetHeight.peek.points(in: phone.height)
            #expect(place(peek, phone.height).lift == -(peek + 12))
            #expect(place(peek, phone.height).alpha == 1)
        }
    }

    /// THE 2026-09-13 BUG. With no ceiling the button follows the sheet the
    /// whole way up, across the map and over the search field and the chips.
    /// Nothing it is copied from does that, so it stops instead.
    @Test func staysOutOfTheChipsAtEveryHeight() {
        for phone in Self.phones {
            // Anywhere the sheet can be, including the over-drag past full.
            for coverage in stride(from: CGFloat(0), through: phone.height, by: 10) {
                let lift = place(coverage, phone.height).lift
                // A quarter of the screen is the region the search field and
                // the filter row occupy. The control never reaches it.
                #expect(-lift < phone.height * 0.75,
                        "coverage \(coverage) on \(phone.name) lifted it \(-lift)")
            }
        }
    }

    /// And it is fully covered rather than parked in view, at every stop that
    /// is taller than where it stops riding.
    @Test func theSheetSwallowsItAtFullHeight() {
        for phone in Self.phones {
            let full = SheetHeight.full.points(in: phone.height)
            #expect(place(full, phone.height).alpha == 0)
        }
    }

    /// The stops it must still ride to, which is the half of this that the
    /// clamp broke the first time it existed: on an SE the card stop is taller
    /// than the half stop, and a 55 percent clamp froze the button under it.
    @Test func ridesAllTheWayToEveryStopBelowFull() {
        for phone in Self.phones {
            for stop in [SheetHeight.peek, .card, .half] {
                let h = stop.points(in: phone.height)
                let p = place(h, phone.height)
                #expect(p.alpha == 1, "\(stop) on \(phone.name) was already fading")
                #expect(p.lift <= -(h + 12) + 0.001,
                        "\(stop) on \(phone.name) sat below the sheet")
            }
        }
    }

    /// It never dives below where a sheetless map puts it, whatever the sheet
    /// does underneath.
    @Test func neverSitsLowerThanTheFloor() {
        for phone in Self.phones {
            for coverage in stride(from: CGFloat(0), through: phone.height, by: 10) {
                #expect(place(coverage, phone.height).lift <= -120)
            }
        }
    }
}
