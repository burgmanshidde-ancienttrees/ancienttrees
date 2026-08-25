// One place that says what is free and what is not, and why.
//
// Written as a freemium funnel rather than as a feature list, because the two
// give different answers. The rules below are the ones AllTrails actually
// follows, read off their own app rather than off a blog post:
//
// 1. NEVER GATE THE CORE LOOP. Their whole map, every trail, every photo and
//    every description is free; Plus sells offline, weather and conditions.
//    If the loop is gated there is no habit to charge for later. Ours is find,
//    walk, tick, and all three stay free.
// 2. GATE ON INTENT, NOT ON TIME OR COUNT. Their paywall appears the moment you
//    tap "download for offline", when you have already decided you want it. It
//    does not appear on launch, and there is no "3 free trails this month".
// 3. THE ASK NAMES WHAT YOU WERE DOING. "Download Palermo" converts; "Go Plus"
//    does not.
// 4. ONE REAL TASTE. The first walk is free, so the thing being sold has been
//    felt rather than described.
//
// Hidde's line, DECISIONS.md 2026-08-18: EUR 19.95 a year with a 7-day trial,
// and four things behind it, Season Radar alerts, curated walks, a personal log
// with badges and photo upload, and full offline. Every tree, story and location
// stays free. The one judgement inside that which is mine, and it is flagged in
// the app for him to flip in a line: TICKING AND SAVING ARE FREE. If the whole
// log is paid then a free user cannot collect anything, and collecting is the
// only reason to come back. Badges, photo upload and the alerts are the paid
// half of it.

import Foundation
import Observation

public enum Feature: String, Sendable {
    case offlineDownload
    case walkBeyondFirst
    case badges
    case photoUpload
    case seasonAlerts
    /// Not a feature: paying because you want this to exist.
    ///
    /// Hidde asked for it on 2026-08-25, alongside turning Plus off for the
    /// MVP: "we could add a button that just says Sponsor this project, and
    /// that would lead to an in-app purchase of 20 euro a year". The button is
    /// here and THE PURCHASE IS NOT, and that is hard rule 2 rather than an
    /// oversight: money is his alone. What it does today is what the rest of
    /// this screen does, which is count who says yes to a real number, and
    /// that number is the one worth having before any processor is wired.
    case sponsor

    /// What the upsell says when this one is reached for. It names the thing the
    /// person was doing, never the plan.
    public var ask: String {
        switch self {
        case .offlineDownload: "Keep this city in your pocket"
        case .walkBeyondFirst: "Unlock every walk"
        case .badges: "Earn badges as you collect"
        case .photoUpload: "Add your own photographs"
        case .seasonAlerts: "Be told when a tree near you peaks"
        case .sponsor: "Keep this project going"
        }
    }

    public var detail: String {
        switch self {
        case .offlineDownload:
            "Every tree, story and map tile stored on your phone, so it works with no signal at all."
        case .walkBeyondFirst:
            "Hand-picked routes that string the best trees of a city into one afternoon."
        case .badges:
            "A drawn badge for every species, city and country you have stood in front of."
        case .photoUpload:
            "Photograph a tree nobody has photographed yet, and put it on its page."
        case .seasonAlerts:
            "A quiet nudge in the week a tree near you is at its best."
        case .sponsor:
            "Around 20 euro a year, from the people who want the trees mapped, whether or not they ever use a paid feature."
        }
    }
}

@Observable
public final class Entitlement {
    /// No payment exists yet and none is built: the price and the processor are
    /// Hidde's alone under hard rule 2. What the paywall does today is MEASURE,
    /// which is the honest phase-1 move and the answer to hard rule 6: it puts
    /// a real price in front of a real intention and counts who says yes.
    public private(set) var isPlus = false
    public private(set) var interestedIn: Set<String> = []

    private let key = "entitlement.interest.v1"

    public init() {
        interestedIn = Set(UserDefaults.standard.stringArray(forKey: key) ?? [])
    }

    public func allows(_ f: Feature) -> Bool { isPlus }

    /// Recorded locally as well as sent, so the funnel is legible on the device
    /// during testing and not only in the database.
    public func registerInterest(_ f: Feature) {
        interestedIn.insert(f.rawValue)
        UserDefaults.standard.set(Array(interestedIn), forKey: key)
    }
}
