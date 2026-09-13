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

/// WHERE THE GLOBE OPENS. Hidde, 2026-09-13, on a screenshot of My trees
/// showing a flat map parked over central Asia: "de weergave van my trees gaat
/// helemaal slecht, volgens mij moet dit een wereldbol zijn omdat ik in
/// meerdere landen heb."
///
/// Two faults in that one picture. It was not a sphere, which is a
/// configuration and is not arithmetic, so it is not tested here. And it was
/// pointed at nowhere, which IS arithmetic: the opening centre was the MEAN of
/// his trees, and this view exists precisely for collections made of two
/// clusters far apart, whose mean is the empty space between them.
struct TheGlobeOpensOverYourOwnTrees {

    private let netherlands = (lat: 52.37, lng: 4.90)
    private let japan = (lat: 34.68, lng: 135.83)

    /// THE BUG. Most of the collection in Japan, a few trees at home, and the
    /// mean lands in Kazakhstan with not one of his trees under it.
    @Test func doesNotOpenOnTheEmptySpaceBetweenTwoCountries() {
        let points = Array(repeating: japan, count: 20)
            + Array(repeating: netherlands, count: 7)
        let opening = GlobeMap.opening(for: points)
        #expect(opening.lng == japan.lng)
        // The mean of that collection is about 101 E, which is western China.
        let mean = points.map(\.lng).reduce(0, +) / Double(points.count)
        #expect(abs(mean - japan.lng) > 30)
    }

    /// And the other way round, because the median follows whichever cluster
    /// actually holds the trees rather than a hardcoded preference.
    @Test func followsWhicheverCountryHoldsMostOfThem() {
        let points = Array(repeating: netherlands, count: 20)
            + Array(repeating: japan, count: 7)
        #expect(GlobeMap.opening(for: points).lng == netherlands.lng)
    }

    /// A pole fills the frame with ice and no trees, so the camera stays in the
    /// band where the planet reads as a planet.
    @Test func staysOutOfThePoles() {
        #expect(GlobeMap.opening(for: [(lat: 78.2, lng: 15.6)]).lat == 35)
        #expect(GlobeMap.opening(for: [(lat: -77.8, lng: 166.7)]).lat == -35)
    }

    /// An empty collection cannot reach the globe in the app, but -globe forces
    /// it, so it still has to be somewhere rather than nowhere.
    @Test func hasAnAnswerForNothingAtAll() {
        let opening = GlobeMap.opening(for: [])
        #expect(opening.lat == 20)
        #expect(opening.lng == 0)
    }

    /// One tree is one tree: its longitude exactly, and its latitude held
    /// inside the band, which for Amsterdam at 52 N means the clamp does the
    /// work. That is deliberate and it is why the pole test above passes: the
    /// globe looks at the planet, not straight down at where you stand.
    @Test func opensOnTheOnlyTreeYouHave() {
        let amsterdam = GlobeMap.opening(for: [netherlands])
        #expect(amsterdam.lng == netherlands.lng)
        #expect(amsterdam.lat == 35)

        let nara = GlobeMap.opening(for: [japan])
        #expect(nara.lng == japan.lng)
        #expect(nara.lat == japan.lat)
    }
}

/// STANDING IN FRONT OF IT IS A CLAIM ABOUT YOU, not about the camera.
///
/// Hidde, 2026-09-13, in Fukuoka, reading a card that told him he was standing
/// in front of a cherry in Kyoto Gyoen: "dit moet je alleen suggereren als gps
/// heel erg in de buurt is toch."
///
/// The 120 metre threshold was never the fault. The card measured from the
/// map's centre, so panning to any tree on earth and waiting for it to be the
/// only one in view made the app say you were in front of it and offer to tick
/// it off, which writes a visit that never happened into the collection.
struct YouAreOnlyInFrontOfATreeYouAreInFrontOf {

    /// Built through the feed's own decoder, so this breaks the day its shape
    /// does. Same approach as MyTreesTests.
    private static func tree(_ id: String, _ lat: Double, _ lng: Double) -> Tree {
        let json = """
        {"id":"\(id)","name":"\(id)","species":"Cherry","age":null,
         "age_min":null,"age_max":null,"lat":\(lat),"lng":\(lng),
         "city":"Kyoto","city_slug":"kyoto","country":"Japan","neighbourhood":null,
         "access":"","transport":null,"precision":"confirmed","best_time":null,
         "peak":null,"story":"","how_to_recognise":null,"url":"","photo":null}
        """
        return try! JSONDecoder().decode(Tree.self, from: Data(json.utf8))
    }

    private static let kyotoGyoen = (lat: 35.0254, lng: 135.7621)
    private static let fukuoka    = (lat: 33.5904, lng: 130.4017)

    private func arrival(_ trees: [Tree], _ origin: (lat: Double, lng: Double),
                         located: Bool = true) -> Tree? {
        MapTab.arrival(among: trees, origin: origin, located: located, within: 0.12)
    }

    /// THE BUG, and the distance is 517 kilometres.
    @Test func aTreeInAnotherCityIsNeverAnArrival() {
        let cherry = Self.tree("kyo_020", Self.kyotoGyoen.lat, Self.kyotoGyoen.lng)
        #expect(arrival([cherry], Self.fukuoka) == nil)
    }

    /// And it still works when you really are there.
    @Test func standingAtItIsAnArrival() {
        let cherry = Self.tree("kyo_020", Self.kyotoGyoen.lat, Self.kyotoGyoen.lng)
        #expect(arrival([cherry], Self.kyotoGyoen)?.id == "kyo_020")
        // 50 metres north, comfortably inside the 120.
        #expect(arrival([cherry], (lat: Self.kyotoGyoen.lat + 0.00045,
                                   lng: Self.kyotoGyoen.lng))?.id == "kyo_020")
    }

    /// A street away is not in front of it.
    @Test func aCoupleOfHundredMetresIsNotArrival() {
        let cherry = Self.tree("kyo_020", Self.kyotoGyoen.lat, Self.kyotoGyoen.lng)
        // About 220 metres north.
        #expect(arrival([cherry], (lat: Self.kyotoGyoen.lat + 0.002,
                                   lng: Self.kyotoGyoen.lng)) == nil)
    }

    /// NO FIX, NO CLAIM. `origin` falls back to a remembered place and then to
    /// Dam square, so without this the card comes back pointed at wherever the
    /// phone was last the moment location is off.
    @Test func withoutARealFixItSaysNothingAtAll() {
        let cherry = Self.tree("kyo_020", Self.kyotoGyoen.lat, Self.kyotoGyoen.lng)
        #expect(arrival([cherry], Self.kyotoGyoen, located: false) == nil)
    }

    /// Two in range, and it is the nearer one you are in front of.
    @Test func theNearerOfTwoWins() {
        let far  = Self.tree("kyo_021", Self.kyotoGyoen.lat + 0.0009, Self.kyotoGyoen.lng)
        let near = Self.tree("kyo_022", Self.kyotoGyoen.lat + 0.0002, Self.kyotoGyoen.lng)
        #expect(arrival([far, near], Self.kyotoGyoen)?.id == "kyo_022")
        #expect(arrival([near, far], Self.kyotoGyoen)?.id == "kyo_022")
    }

    /// An empty catalogue is not a crash.
    @Test func nothingNearbyIsSimplyNothing() {
        #expect(arrival([], Self.kyotoGyoen) == nil)
    }
}
