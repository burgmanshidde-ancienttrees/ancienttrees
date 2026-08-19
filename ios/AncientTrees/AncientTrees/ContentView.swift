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
    @State private var location = LocationProvider()
    // Screenshotting each tab needs a way to open on one, because this Mac's
    // simulator panel is not available and simctl cannot tap. Debug only.
    @State private var tab = ProcessInfo.processInfo.arguments
        .first(where: { $0.hasPrefix("-tab=") })
        .flatMap { Int($0.dropFirst(5)) } ?? 0

    private var origin: (lat: Double, lng: Double) {
        location.coordinate ?? (lat: 52.3731, lng: 4.8922)   // Dam square, until we know better
    }

    var body: some View {
        Group {
            if let cat = store.catalogue {
                TabView(selection: $tab) {
                    NavigationStack { MapTab(catalogue: cat, origin: origin,
                                             located: location.coordinate != nil) }
                        .tag(0)
                        .tabItem { Label("Map", systemImage: "map.fill") }

                    NavigationStack { ExploreView(catalogue: cat, origin: origin) }
                        .tag(1)
                        .tabItem { Label("Explore", systemImage: "square.grid.2x2") }

                    NavigationStack { HereView(catalogue: cat, origin: origin,
                                               located: location.coordinate != nil) }
                        .tag(2)
                        .tabItem { Label("Here", systemImage: "dot.viewfinder") }

                    NavigationStack { YouView(catalogue: cat) }
                        .tag(3)
                        .tabItem { Label("You", systemImage: "person.crop.circle") }
                }
                .environment(saved)
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

/// The map IS the product, and the list is a view of it rather than a
/// separate destination. AllTrails' floating pill is the convention: one
/// control, always in the same place, so nobody has to decide which page to be
/// on. Walks live on this map too rather than in a tab of their own, because a
/// walk is a way of finding trees and two map tabs is one too many.
/// destinations. AllTrails' floating Kaart pill is the convention and it means
/// nobody has to decide which page to be on.
struct MapTab: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    let located: Bool

    @State private var showMap = false
    @State private var selected: Tree?

    private var near: [(tree: Tree, km: Double)] {
        catalogue.nearest(to: origin.lat, origin.lng, limit: 60, withinKm: 50)
    }

    var body: some View {
        ZStack(alignment: .bottom) {
            if showMap {
                TreeMap(trees: near.map(\.tree),
                        focus: .init(latitude: origin.lat, longitude: origin.lng),
                        selected: $selected)
                    .ignoresSafeArea(edges: .bottom)
            } else if near.isEmpty {
                NothingNearby(catalogue: catalogue)
            } else {
                List(near, id: \.tree.id) { hit in
                    NavigationLink {
                        TreeDetail(tree: hit.tree, catalogue: catalogue)
                    } label: {
                        TreeRow(tree: hit.tree, km: hit.km)
                    }
                }
                .listStyle(.plain)
            }

            Button {
                showMap.toggle()
            } label: {
                Label(showMap ? "List" : "Map", systemImage: showMap ? "list.bullet" : "map.fill")
                    .font(.subheadline.weight(.semibold))
                    .padding(.horizontal, 18).padding(.vertical, 11)
            }
            .buttonStyle(.borderedProminent)
            .tint(Color(red: 0.20, green: 0.35, blue: 0.20))
            .clipShape(.capsule)
            .padding(.bottom, 14)
        }
        .navigationTitle(located ? "Near you" : "Near Amsterdam")
        .navigationDestination(item: $selected) { t in
            TreeDetail(tree: t, catalogue: catalogue)
        }
    }
}

struct TreeRow: View {
    let tree: Tree
    let km: Double

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack(alignment: .firstTextBaseline) {
                Text(tree.name).font(.headline)
                Spacer()
                Text(distance).font(.subheadline).foregroundStyle(.secondary).monospacedDigit()
            }
            Text(tree.commonName).font(.subheadline).foregroundStyle(.secondary)
            HStack(spacing: 10) {
                if let age = tree.age { Label(age, systemImage: "clock") }
                if tree.precision.needsWarning { Label("pin is approximate", systemImage: "scope") }
            }
            .font(.caption).foregroundStyle(.secondary).labelStyle(.titleAndIcon)
        }
        .padding(.vertical, 4)
    }

    /// Metres under a kilometre: "0.3 km" reads as further than "330 m".
    private var distance: String {
        km < 1 ? "\(Int((km * 1000).rounded())) m" : String(format: "%.1f km", km)
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
