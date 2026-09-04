// A city or a country on a real map, WITHOUT leaving where you were.
//
// Hidde, 2026-08-27: "ik klik op een stad, zie de kaart, en er staat open de
// map. Dan wil je niet dat hij naar de mappagina gaat ... je wilt dat mensen in
// discovery blijven ... je gaat alleen naar de kaartkant als mensen dat in de
// menubar doen, nooit via dat."
//
// The preview used to hand you to the Map tab, and a tab is a different place
// with a different history: the city you were reading was gone and the back
// button belonged to something else. This is pushed on the stack you are
// already on, so back is back and the trail survives. The website has worked
// this way for a while; this is the app catching up.
//
// IT IS THE SAME COMPONENT AS THE OTHER TWO, which is the other half of what he
// asked for. MapWithSheet carries the arrangement, the drag arbitration, the
// content inset that lifts the camera above the sheet, and the room left for a
// floating bar (zero here, because a pushed page has no tab bar). Nothing about
// how the map and the list answer each other is written twice.

import SwiftUI
import CoreLocation

struct PlaceMapPage: View {
    let place: Route.Place
    let catalogue: Catalogue

    @Environment(Saved.self) private var saved
    @Environment(Sightings.self) private var sightings
    @Environment(Navigator.self) private var navigator

    @State private var sheetHeight: SheetHeight = .half
    @State private var selected: Tree?
    @State private var topCard: String?

    /// Photographs first, because this list is a browse and most of these
    /// trees have no picture yet. See Editorial.photographsFirst.
    private var trees: [Tree] {
        let all = switch place {
        case .city(let slug): catalogue.trees(inCity: slug)
        case .country(let name): catalogue.trees(inCountry: name)
        }
        return Editorial.photographsFirst(all, photo: { $0.photo != nil })
    }

    private var title: String {
        switch place {
        case .city(let slug): trees.first?.city ?? slug
        case .country(let name): name
        }
    }

    /// The middle of what is here, so the map opens on the place rather than on
    /// wherever the phone happens to be standing.
    private var centre: CLLocationCoordinate2D? {
        guard !trees.isEmpty else { return nil }
        return CLLocationCoordinate2D(
            latitude: trees.map(\.lat).reduce(0, +) / Double(trees.count),
            longitude: trees.map(\.lng).reduce(0, +) / Double(trees.count))
    }

    /// Wide enough to hold them all with a little air, and never so tight that
    /// a place with one tree opens on a doorstep.
    private var span: CLLocationDistance {
        let lats = trees.map(\.lat), lngs = trees.map(\.lng)
        guard let loLat = lats.min(), let hiLat = lats.max(),
              let loLng = lngs.min(), let hiLng = lngs.max() else { return 4000 }
        let m = max((hiLat - loLat) * 111_000, (hiLng - loLng) * 111_000 * 0.62)
        return max(m * 1.3, 1200)
    }

    var body: some View {
        MapWithSheet(height: $sheetHeight, topItem: $topCard) {
            TreeMap(trees: trees,
                    collected: Set(saved.collected.map(\.treeId)),
                    favourites: Set(saved.favourites.map(\.treeId)),
                    onSelectTree: { navigator.push = .tree($0) },
                    focus: centre,
                    spanMeters: span,
                    // The whole point of this page is these trees, so it frames
                    // them rather than a point near them. See fitsTrees.
                    fitsTrees: true,
                    selected: $selected)
                .accessibilityIdentifier("tree-map")
        } header: {
            Text(trees.count == 1 ? "1 tree in \(title)" : "\(trees.count) trees in \(title)")
                .font(.brand(16, .bold, relativeTo: .headline))
                .foregroundStyle(Brand.ink)
                .frame(maxWidth: .infinity)
                .padding(.bottom, 10)
        } content: {
            VStack(alignment: .leading, spacing: 18) {
                ForEach(trees) { t in
                    SheetLink(route: .tree(t.id)) { TreeCard(tree: t) }
                        .accessibilityIdentifier("tree-card")
                        .id(t.id)
                }
                Color.clear.frame(height: 24)
            }
            .padding(.horizontal, 20)
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .brandGround()
        .navigationTitle(title)
        .navigationBarTitleDisplayMode(.inline)
        .accessibilityIdentifier("place-map-page")
    }
}
