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

    // -sheet=full opens the sheet as the page, so the screen sweep can
    // photograph the Polarsteps transition here as well as on the map tab
    // (Hidde, 2026-10-02: "this transition should also be on the map page and
    // the my trees page"; it is one component, so it is).
    @State private var sheetHeight: SheetHeight =
        ProcessInfo.processInfo.arguments.contains("-sheet=full") ? .full : .half
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

    /// The mainland, when this is a country the website names one for.
    private var mainland: (sw: CLLocationCoordinate2D, ne: CLLocationCoordinate2D)? {
        guard case .country(let name) = place,
              let f = catalogue.facets.focus(country: name) else { return nil }
        return (sw: CLLocationCoordinate2D(latitude: f.sw.lat, longitude: f.sw.lng),
                ne: CLLocationCoordinate2D(latitude: f.ne.lat, longitude: f.ne.lng))
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

    /// The opening frame. A country frames its mainland; a city with day
    /// trips frames its OWN trees, so Copenhagen opens on Copenhagen and not
    /// on Dyrehaven as well (Hidde, 2026-10-06, the website does the same).
    /// The day-trip pins are still on the map, a pinch away.
    private var openingBox: (sw: CLLocationCoordinate2D, ne: CLLocationCoordinate2D)? {
        if let m = mainland { return m }
        guard isCity, !away.isEmpty, inTown.count >= 2 else { return nil }
        let lats = inTown.map(\.lat), lngs = inTown.map(\.lng)
        let pad = 0.004
        return (sw: CLLocationCoordinate2D(latitude: lats.min()! - pad, longitude: lngs.min()! - pad),
                ne: CLLocationCoordinate2D(latitude: lats.max()! + pad, longitude: lngs.max()! + pad))
    }

    private var isCity: Bool { if case .city = place { true } else { false } }

    /// The list's first part: everything that is not a day trip.
    private var inTown: [Tree] { isCity ? trees.filter { $0.dayTrip == nil } : trees }

    /// The day trips, one group per place, nearest first.
    private var away: [(trip: Tree.DayTrip, trees: [Tree])] {
        guard isCity else { return [] }
        var groups: [String: (trip: Tree.DayTrip, trees: [Tree])] = [:]
        for t in trees { if let d = t.dayTrip { groups[d.line, default: (d, [])].trees.append(t) } }
        return groups.values.sorted { $0.trip.km < $1.trip.km }
    }


    private func card(_ t: Tree) -> some View {
        SheetLink(route: .tree(t.id)) { TreeCard(tree: t) }
            .accessibilityIdentifier("tree-card")
            .id(t.id)
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
                    fitBox: openingBox,
                    selected: $selected)
                .accessibilityIdentifier("tree-map")
        } header: {
            Text("\(treesLabel(trees.count)) in \(title)")
                .font(.brand(16, .bold, relativeTo: .headline))
                .foregroundStyle(Brand.ink)
                .frame(maxWidth: .infinity)
                .padding(.bottom, 10)
        } content: {
            VStack(alignment: .leading, spacing: 18) {
                // Who looks after this city, komoot's person row, above the
                // trees as the website prints it under the intro.
                if case .city(let slug) = place {
                    let named = catalogue.facets.ambassadors(city: slug)
                    ForEach(named, id: \.self) { a in
                        AmbassadorRow(name: a.name, place: title, affiliation: a.affiliation)
                    }
                    // Nobody named: the open seat, as the website draws it.
                    if named.isEmpty { AmbassadorWantedRow(place: title) }
                }
                ForEach(inTown) { t in card(t) }
                // A DAY TRIP AWAY, on the website's word (Hidde approved the
                // Copenhagen mockup 2026-09-27, and found it missing here on
                // 2026-10-01). The city's own trees first, then one group per
                // place, nearest first. Cities only: a country page is all
                // day trips by definition.
                if !away.isEmpty {
                    Divider().padding(.top, 10)
                    Text("A day trip away")
                        .font(.brand(20, .bold, relativeTo: .title3))
                        .foregroundStyle(Brand.ink)
                        .accessibilityAddTraits(.isHeader)
                    ForEach(away, id: \.trip.line) { g in
                        (Text(g.trip.place).bold().foregroundStyle(Brand.ink)
                         + Text(String(g.trip.line.dropFirst(g.trip.place.count))).foregroundStyle(Brand.inkSoft))
                            .font(.subheadline)
                        ForEach(g.trees) { t in card(t) }
                    }
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
