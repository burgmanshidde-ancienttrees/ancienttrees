// Getting somebody walking, on whatever maps app they actually have.
//
// This used to be one line: MKMapItem.openInMaps, which is Apple Maps and
// nothing else. Hidde, 2026-08-21, on his own phone: "als ik Take Me There
// klik krijg ik de melding dat ik geen navigatie heb geinstalleerd, terwijl ik
// gewoon Google Maps heb." Apple Maps can be deleted, and a person who deleted
// it is exactly the person who has something else.
//
// So: Apple Maps if it is there, then Google Maps if it is installed, then the
// universal Google web link, which every phone opens with whatever it uses for
// maps. The last one cannot fail, which is the point.

import Foundation
import MapKit
import UIKit

enum Directions {
    static func walk(to tree: Tree) { walk(lat: tree.lat, lng: tree.lng, name: tree.name) }

    static func walk(lat: Double, lng: Double, name: String? = nil) {
        let item = MKMapItem(placemark: .init(coordinate: .init(latitude: lat, longitude: lng)))
        item.name = name
        let opened = item.openInMaps(launchOptions:
            [MKLaunchOptionsDirectionsModeKey: MKLaunchOptionsDirectionsModeWalking])
        guard !opened else { return }

        let app = UIApplication.shared
        if let g = URL(string: "comgooglemaps://?daddr=\(lat),\(lng)&directionsmode=walking"),
           app.canOpenURL(g) {
            app.open(g)
            return
        }
        if let web = URL(string:
            "https://www.google.com/maps/dir/?api=1&destination=\(lat),\(lng)&travelmode=walking") {
            app.open(web)
        }
    }
}
