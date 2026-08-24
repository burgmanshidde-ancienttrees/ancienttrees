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
        let google = URL(string: "comgooglemaps://?daddr=\(lat),\(lng)&directionsmode=walking")
        let web = URL(string:
            "https://www.google.com/maps/dir/?api=1&destination=\(lat),\(lng)&travelmode=walking")
        openFirst([apple, google, web])
    }

    /// Open the first of these that actually launches something.
    private static func openFirst(_ urls: [URL?]) {
        var queue = urls.compactMap { $0 }
        func next() {
            guard !queue.isEmpty else { return }
            let url = queue.removeFirst()
            UIApplication.shared.open(url, options: [:]) { ok in
                if !ok { next() }
            }
        }
        next()
    }
}
