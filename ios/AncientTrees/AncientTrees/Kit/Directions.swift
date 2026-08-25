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
        // Apple Maps first, because it is the default on this platform and the
        // person who deleted it is exactly the person who has something else.
        // As a URL rather than MKMapItem.openInMaps, so a missing Maps app
        // fails quietly here instead of raising a system alert.
        let apple = URL(string: "maps://?daddr=\(lat),\(lng)&dirflg=w")
        // The https link, not comgooglemaps://. Google Maps claims
        // google.com/maps as a universal link, so an installed Google Maps takes
        // this and a phone without it gets the same route in a browser. Either
        // way something opens and nothing has to be guessed at.
        let web = URL(string:
            "https://www.google.com/maps/dir/?api=1&destination=\(lat),\(lng)&travelmode=walking")

        // ASK BEFORE TRYING, and only about Apple's own scheme.
        //
        // Third time on this bug (2026-08-21, 08-24, and 08-25: "hij geeft nog
        // steeds de melding geen navigatie app geinstalleerd terwijl hij wel
        // google maps opent"). The chain of attempts fixed the outcome and not
        // the noise: iOS itself puts up an alert when asked to open a scheme no
        // installed app claims, BEFORE the completion handler reports the
        // failure. So a phone without Apple Maps got the system's own "no app
        // installed" alert, our code moved on, and Google Maps opened behind it.
        // He saw both and was right to report it twice.
        //
        // canOpenURL is accurate for maps://, tel://, mailto: and the other
        // system schemes without any LSApplicationQueriesSchemes list; it is
        // only third-party schemes it lies about, which is why there is no
        // longer a third-party scheme here.
        if let apple, UIApplication.shared.canOpenURL(apple) {
            UIApplication.shared.open(apple, options: [:], completionHandler: nil)
            return
        }
        if let web {
            UIApplication.shared.open(web, options: [:], completionHandler: nil)
        }
    }
}
