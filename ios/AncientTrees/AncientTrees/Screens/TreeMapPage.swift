// One tree, on a whole map, WITHOUT leaving the page you were reading.
//
// Hidde, 2026-08-26: "als je die wilt expanden, dan kom je weer terug op de
// mappagina ... ideaal expand je alleen de map van de locatie waar die boom
// staat, in een eigen subpagina met een backbutton terug naar de detailpagina,
// zodat je gewoon niet verdwijnt uit die detailpagina en door kan gaan met je
// zoektocht."
//
// The old expand set navigator.showOnMap, which switches to the Map tab and
// clears its stack. That answers "show me this on the map" and throws away
// everything else: the tree you were reading, the city page you came from, the
// search you did to get there. A pushed page answers the same question and
// keeps the trail, and Back is the way out, which is what a reader already
// knows.
//
// It shows the neighbours too, because "is it worth the trip on its own or are
// there three more round the corner" is the question somebody opening a map is
// actually asking.

import SwiftUI
import CoreLocation

struct TreeMapPage: View {
    let tree: Tree
    let catalogue: Catalogue

    @Environment(Navigator.self) private var navigator
    @Environment(Saved.self) private var saved
    /// The map wants somewhere to put a selection; this page has none, because
    /// a tap here opens a page rather than selecting a pin.
    @State private var selected: Tree?

    /// This tree and whatever else of ours stands within a walk of it.
    private var nearby: [Tree] {
        let others = catalogue.nearest(to: tree.lat, tree.lng, limit: 12, withinKm: 1.5)
            .map(\.tree).filter { $0.id != tree.id }
        return [tree] + others
    }

    var body: some View {
        TreeMap(trees: nearby,
                collected: Set(saved.collected.map(\.treeId)),
                onSelectTree: { id in
                    // A neighbour opens its own page, pushed on this same
                    // stack, so the trail keeps growing rather than resetting.
                    if id != tree.id { navigator.push = .tree(id) }
                },
                focus: CLLocationCoordinate2D(latitude: tree.lat, longitude: tree.lng),
                spanMeters: 600,
                selected: $selected)
            .ignoresSafeArea(edges: .bottom)
            .navigationTitle(tree.name)
            .navigationBarTitleDisplayMode(.inline)
            .accessibilityIdentifier("tree-map-page")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button { Directions.walk(to: tree) } label: {
                        Label("Take me there", systemImage: "arrow.turn.up.right")
                    }
                    .accessibilityLabel("Take me there")
                }
            }
    }
}
