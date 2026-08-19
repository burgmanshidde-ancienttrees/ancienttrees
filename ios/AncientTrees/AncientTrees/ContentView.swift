// The four verbs, one tab each: find, walk, collect, season.
//
// The tab bar is the product's own doctrine rather than a copy of AllTrails',
// though theirs is the evidence that verbs work as tabs: Verkennen, Opgeslagen,
// Navigeer, Activiteit. Three of their four map onto ours almost exactly.

import SwiftUI
import CoreLocation
import MapKit

struct ContentView: View {
    @State private var store = CatalogueStore()
    @State private var saved = Saved()
    @State private var entitlement = Entitlement()
    @State private var location = LocationProvider()
    // Screenshotting each tab needs a way to open on one, because this Mac's
    // simulator panel is not available and simctl cannot tap. Debug only.
    @State private var tab = ProcessInfo.processInfo.arguments
        .first(where: { $0.hasPrefix("-tab=") })
        .flatMap { Int($0.dropFirst(5)) } ?? 0

    /// Debug only, same reason as the tab argument: this Mac cannot tap the
    /// simulator's location permission dialog, so screenshots would all be
    /// Amsterdam. `-at=38.11,13.36` starts somewhere else.
    private var debugOrigin: (lat: Double, lng: Double)? {
        guard let a = ProcessInfo.processInfo.arguments
                .first(where: { $0.hasPrefix("-at=") })?.dropFirst(4).split(separator: ","),
              a.count == 2, let la = Double(a[0]), let ln = Double(a[1]) else { return nil }
        return (lat: la, lng: ln)
    }

    private var origin: (lat: Double, lng: Double) {
        debugOrigin ?? location.coordinate ?? (lat: 52.3731, lng: 4.8922)   // Dam square
    }

    var body: some View {
        Group {
            if let cat = store.catalogue {
                TabView(selection: $tab) {
                    NavigationStack { MapTab(catalogue: cat, origin: origin,
                                             located: location.coordinate != nil || debugOrigin != nil) }
                        .tag(0)
                        .tabItem { Label("Map", systemImage: "map.fill") }

                    NavigationStack { ExploreView(catalogue: cat, origin: origin) }
                        .tag(1)
                        .tabItem { Label("Explore", systemImage: "square.grid.2x2") }

                    NavigationStack { SavedView(catalogue: cat, origin: origin) }
                        .tag(2)
                        .tabItem { Label("Saved", systemImage: "heart") }

                    NavigationStack { YouView(catalogue: cat) }
                        .tag(3)
                        .tabItem { Label("You", systemImage: "person.crop.circle") }
                }
                .environment(saved)
                .environment(entitlement)
                // Same debug scaffolding as -tab and -at: no simulator panel
                // here, so a screen that is only reachable by tapping cannot
                // otherwise be looked at before it ships.
                .sheet(isPresented: .constant(ProcessInfo.processInfo.arguments.contains("-paywall"))) {
                    PaywallView(feature: .walkBeyondFirst).environment(entitlement)
                }
            } else if let err = store.loadError {
                ContentUnavailableView("Something is wrong with the catalogue",
                                       systemImage: "exclamationmark.triangle",
                                       description: Text(err))
            } else {
                ProgressView()
            }
        }
        .task {
            store.loadBundled()
            location.request()
        }
    }
}

struct NothingNearby: View {
    let catalogue: Catalogue
    var body: some View {
        ContentUnavailableView {
            Label("No trees near you yet", systemImage: "tree")
        } description: {
            Text("We map \(catalogue.trees.count) trees in \(catalogue.citySlugs.count) places, and none is within fifty kilometres of here.")
        }
    }
}

@Observable
final class LocationProvider: NSObject, CLLocationManagerDelegate {
    private let manager = CLLocationManager()
    var coordinate: (lat: Double, lng: Double)?

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyHundredMeters
    }

    func request() {
        manager.requestWhenInUseAuthorization()
        manager.startUpdatingLocation()
    }

    func locationManager(_ m: CLLocationManager, didUpdateLocations locs: [CLLocation]) {
        guard let l = locs.last else { return }
        coordinate = (lat: l.coordinate.latitude, lng: l.coordinate.longitude)
    }

    func locationManager(_ m: CLLocationManager, didFailWithError error: Error) {}
}
