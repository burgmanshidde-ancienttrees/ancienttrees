// The first screen: what is near me, nearest first.
//
// Deliberately the whole promise in one list rather than a home screen that
// links to one. The website's own value proposition is "see the remarkable old
// trees near you", and every layer of navigation between opening the app and
// that list is a layer that made `directions` fire zero times on the website.

import SwiftUI
import CoreLocation

struct ContentView: View {
    @State private var store = CatalogueStore()
    @State private var location = LocationProvider()

    private var origin: (lat: Double, lng: Double) {
        location.coordinate ?? (lat: 52.3731, lng: 4.8922)   // Dam square, until we know better
    }

    var body: some View {
        NavigationStack {
            Group {
                if let cat = store.catalogue {
                    let near = cat.nearest(to: origin.lat, origin.lng, limit: 25, withinKm: 50)
                    if near.isEmpty {
                        NothingNearby(catalogue: cat)
                    } else {
                        List(near, id: \.tree.id) { hit in
                            TreeRow(tree: hit.tree, km: hit.km)
                        }
                        .listStyle(.plain)
                    }
                } else if let err = store.loadError {
                    ContentUnavailableView("Something is wrong with the catalogue",
                                           systemImage: "exclamationmark.triangle",
                                           description: Text(err))
                } else {
                    ProgressView()
                }
            }
            .navigationTitle(location.coordinate == nil ? "Near Amsterdam" : "Near you")
            .navigationBarTitleDisplayMode(.large)
        }
        .task {
            store.loadBundled()
            location.request()
        }
    }
}

private struct TreeRow: View {
    let tree: Tree
    let km: Double

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack(alignment: .firstTextBaseline) {
                Text(tree.name).font(.headline)
                Spacer()
                Text(distance).font(.subheadline).foregroundStyle(.secondary)
                    .monospacedDigit()
            }
            Text(tree.commonName).font(.subheadline).foregroundStyle(.secondary)
            HStack(spacing: 10) {
                if let age = tree.age { Label(age, systemImage: "clock") }
                if tree.precision.needsWarning {
                    Label("pin is approximate", systemImage: "scope")
                }
            }
            .font(.caption)
            .foregroundStyle(.secondary)
            .labelStyle(.titleAndIcon)
        }
        .padding(.vertical, 4)
    }

    /// Metres under a kilometre, because "0.3 km" reads as further than "330 m".
    private var distance: String {
        km < 1 ? "\(Int((km * 1000).rounded())) m" : String(format: "%.1f km", km)
    }
}

/// Most of the world has no tree of ours within an hour, and the honest answer
/// is to say so rather than to offer the twelfth nearest at four hundred km.
private struct NothingNearby: View {
    let catalogue: Catalogue

    var body: some View {
        ContentUnavailableView {
            Label("No trees near you yet", systemImage: "tree")
        } description: {
            Text("We map \(catalogue.trees.count) trees in \(catalogue.citySlugs.count) places, and none of them is within fifty kilometres of here.")
        }
    }
}

/// Location, asked for once and never insisted upon. A refusal is a normal
/// answer: the app falls back to a city and keeps working.
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

#Preview { ContentView() }
