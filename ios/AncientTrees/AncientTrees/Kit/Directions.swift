// Getting somebody walking, in the maps app they actually use.
//
// Hidde, 2026-08-21: "als ik Take Me There klik krijg ik de melding dat ik geen
// navigatie heb geinstalleerd, terwijl ik gewoon Google Maps heb." It was
// answered that day with a fallback chain, and on 2026-08-24 he got the same
// message again. The chain was right; the way it ASKED was not.
//
// canOpenURL is the trap. It answers only for schemes listed in
// LSApplicationQueriesSchemes, this app has no such list, and without one it
// returns false for every third-party scheme whether the app is installed or
// not. So the Google Maps branch could never be taken, and the person with
// Google Maps on their phone was told there was nothing to open.
//
// NO CUSTOM SCHEME, ANYWHERE. Fourth report of the same thing (Hidde,
// 2026-08-21, 08-24, 08-25 and 08-26: "hij zegt nog steeds geen navigatie app
// geinstalleerd"), and the three earlier fixes all kept asking `maps://` first
// and only argued about how to ask. That is the bug: iOS raises its own "no app
// installed" alert for an unclaimed scheme, and canOpenURL cannot be trusted to
// keep us away from it, because a phone that has had Apple Maps removed can
// still answer yes.
//
// Both destinations below are https UNIVERSAL LINKS, which is what Apple and
// Google publish for exactly this purpose. Google's own documentation: "On an
// iOS device: If Google Maps app for iOS is installed, the URL launches Google
// Maps in the Maps app and performs the requested action."
// (developers.google.com/maps/documentation/urls/get-started). A phone without
// the app opens the same route in Safari. There is no scheme to be unclaimed,
// so there is no alert to raise, and every path ends with a map on the screen.
//
// AND IT ASKS WHICH ONE, ONCE (Hidde, 2026-08-28: "als ik op de take me there
// knop druk waarom opent die niet mn google maps app, 90% van de mensen hebben
// die app"). Until then it always built the Apple link and the Google line under
// it was unreachable, so every tap landed in Apple Maps on every phone. iOS
// cannot answer this for us: the default-navigation-app setting added in iOS
// 18.4 is EU-only and governs Siri and Apple's own address taps, while a
// maps.apple.com link stays claimed by Apple Maps.
//
// Convention: an app that opens directions and cannot read the system default
// asks the person and remembers. WhatsApp prompts between Apple Maps, Google
// Maps and Waze on an address tap; the settings row that changes it afterwards
// is the standard half nobody sees until they want to switch. Recorded in
// CONVENTIONS.md.
//
// WAZE IS NOT IN THE LIST, deliberately. It publishes no https universal link,
// only `waze://`, and a custom scheme is the one thing this file exists to keep
// out. It goes in the day they publish one, and not before.
import Foundation
import MapKit
import UIKit

enum Directions {
    /// The maps apps we can open without a custom scheme.
    enum MapsApp: String, CaseIterable, Identifiable {
        case apple, google
        var id: String { rawValue }
        var label: String {
            switch self {
            case .apple: "Apple Maps"
            case .google: "Google Maps"
            }
        }
        func url(lat: Double, lng: Double) -> URL? {
            switch self {
            case .apple:
                URL(string: "https://maps.apple.com/?daddr=\(lat),\(lng)&dirflg=w")
            case .google:
                URL(string: "https://www.google.com/maps/dir/?api=1"
                    + "&destination=\(lat),\(lng)&travelmode=walking")
            }
        }
    }

    private static let key = "directions.app"

    /// The remembered answer, or nil while nobody has been asked yet.
    static var preferred: MapsApp? {
        get { UserDefaults.standard.string(forKey: key).flatMap(MapsApp.init(rawValue:)) }
        set {
            if let newValue { UserDefaults.standard.set(newValue.rawValue, forKey: key) }
            else { UserDefaults.standard.removeObject(forKey: key) }
        }
    }

    static func walk(to tree: Tree) { walk(lat: tree.lat, lng: tree.lng, name: tree.name) }

    /// Opens the remembered app, or asks first. The asking is presented from
    /// the root of the app rather than from the button, because these buttons
    /// live on a tree page, a pushed map and inside walk mode, and one dialog
    /// in one place cannot drift out of step with the other two.
    @MainActor
    static func walk(lat: Double, lng: Double, name: String? = nil) {
        if let chosen = preferred {
            open(chosen, lat: lat, lng: lng)
        } else {
            DirectionsAsk.shared.pending = DirectionsAsk.Pending(lat: lat, lng: lng, name: name)
        }
    }

    @MainActor
    static func open(_ app: MapsApp, lat: Double, lng: Double) {
        guard let url = app.url(lat: lat, lng: lng) else { return }
        UIApplication.shared.open(url, options: [:], completionHandler: nil)
    }
}

/// The one place a pending "which maps app" question lives, so the dialog can
/// be presented once at the root. Same shape as the root sheet: SwiftUI honours
/// one dialog per view, and three buttons in three screens asking separately is
/// how a control ends up behaving differently depending on where you tapped it.
@MainActor
@Observable
final class DirectionsAsk {
    static let shared = DirectionsAsk()

    struct Pending: Equatable {
        let lat: Double
        let lng: Double
        let name: String?
    }

    /// Set by Directions.walk when nothing is remembered yet. The debug
    /// argument is the sweep's way in: a dialog no argument can open is a
    /// screen that ships unlooked at, which is exactly how three sheets went
    /// unseen until 2026-08-28.
    var pending: Pending? = ProcessInfo.processInfo.arguments.contains("-directions")
        ? Pending(lat: 52.3676, lng: 4.9041, name: nil) : nil

    private init() {}

    func answer(_ app: Directions.MapsApp) {
        guard let p = pending else { return }
        Directions.preferred = app
        pending = nil
        Directions.open(app, lat: p.lat, lng: p.lng)
    }
}
