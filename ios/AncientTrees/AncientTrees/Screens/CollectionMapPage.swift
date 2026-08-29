// Your own trees, on a map you can actually move.
//
// The cover on My trees is a still picture, and it has to be: a map you can
// pan inside a scroll view means one finger choosing between the two, which is
// the fight that page just lost its sheet over. So the cover opens this, and
// this is a real map with nothing else on it.
//
// It is the same answer every reference gives. Airbnb's listing shows a static
// map that opens a full one, Google Maps' place card the same, Strava's
// activity the same. Back is the way out.

import SwiftUI
import CoreLocation

struct CollectionMapPage: View {
    let catalogue: Catalogue

    @Environment(Saved.self) private var saved
    @Environment(Sightings.self) private var sightings
    @Environment(Navigator.self) private var navigator
    @State private var selected: Tree?

    private var mine: [Tree] {
        saved.collected.compactMap { catalogue.tree($0.treeId) }
    }

    /// The middle of what you have, so the map opens on your collection rather
    /// than on wherever the phone happens to be.
    private var centre: CLLocationCoordinate2D? {
        let all = mine.map { (lat: $0.lat, lng: $0.lng) }
            + sightings.yoursOnly.map { (lat: $0.lat, lng: $0.lng) }
        guard !all.isEmpty else { return nil }
        return CLLocationCoordinate2D(
            latitude: all.map(\.lat).reduce(0, +) / Double(all.count),
            longitude: all.map(\.lng).reduce(0, +) / Double(all.count))
    }

    /// Far enough out to hold the spread, with a floor so one tree is a street
    /// rather than an infinite zoom.
    private var span: CLLocationDistance {
        let lats = mine.map(\.lat) + sightings.yoursOnly.map(\.lat)
        let lngs = mine.map(\.lng) + sightings.yoursOnly.map(\.lng)
        guard let loLat = lats.min(), let hiLat = lats.max(),
              let loLng = lngs.min(), let hiLng = lngs.max() else { return 4000 }
        let m = max((hiLat - loLat) * 111_000, (hiLng - loLng) * 111_000 * 0.62)
        return max(m * 1.3, 1200)
    }

    var body: some View {
        TreeMap(trees: mine,
                mine: sightings.yoursOnly.map { (id: $0.id, lat: $0.lat, lng: $0.lng, name: $0.name,
                                                 photo: sightings.image($0)) },
                collected: Set(saved.collected.map(\.treeId)),
                favourites: Set(saved.favourites.map(\.treeId)),
                onSelectMine: { navigator.push = .mine($0) },
                onSelectTree: { navigator.push = .tree($0) },
                focus: centre,
                spanMeters: span,
                fitsTrees: true,
                selected: $selected)
            .ignoresSafeArea(edges: .bottom)
            .navigationTitle("My trees")
            .navigationBarTitleDisplayMode(.inline)
            .accessibilityIdentifier("collection-map-page")
    }
}
