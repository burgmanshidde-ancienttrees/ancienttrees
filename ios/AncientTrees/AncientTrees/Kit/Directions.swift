// Getting somebody walking, on whatever maps app they actually have.
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
// open(_:options:completionHandler:) needs no list at all: it either launches
// the app or reports that it could not. So this asks by TRYING, in order, and
// the last link is an https one that no phone can fail to open.
import Foundation
import MapKit
import UIKit

enum Directions {
    static func walk(to tree: Tree) { walk(lat: tree.lat, lng: tree.lng, name: tree.name) }

    static func walk(lat: Double, lng: Double, name: String? = nil) {
        // NO CUSTOM SCHEME, ANYWHERE. Fourth report of the same thing (Hidde,
        // 2026-08-21, 08-24, 08-25 and 08-26: "hij zegt nog steeds geen
        // navigatie app geinstalleerd"), and the three earlier fixes all kept
        // asking `maps://` first and only argued about how to ask. That is the
        // bug: iOS raises its own "no app installed" alert for an unclaimed
        // scheme, and canOpenURL cannot be trusted to keep us away from it,
        // because a phone that has had Apple Maps removed can still answer yes.
        // A fix that depends on a predicate being right is not a fix when the
        // predicate is the thing failing.
        //
        // Both of these are https UNIVERSAL LINKS, which is what Apple and
        // Google publish for exactly this purpose. An installed Apple Maps
        // takes maps.apple.com and an installed Google Maps takes
        // google.com/maps; a phone with neither opens the same route in
        // Safari. There is no scheme to be unclaimed, so there is no alert to
        // raise, and every path ends with a map on the screen.
        let apple = URL(string:
            "https://maps.apple.com/?daddr=\(lat),\(lng)&dirflg=w")
        let web = URL(string:
            "https://www.google.com/maps/dir/?api=1&destination=\(lat),\(lng)&travelmode=walking")
        if let apple {
            UIApplication.shared.open(apple, options: [:], completionHandler: nil)
        } else if let web {
            UIApplication.shared.open(web, options: [:], completionHandler: nil)
        }
    }
}
