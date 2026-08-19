// The map is the product, so the tab called Map opens on a map.
//
// The model is Google Maps' rather than AllTrails', and Hidde is right about
// why: AllTrails is built for LINES and we show POINTS. A route has no location,
// it has a course, which is why they cluster into labels reading "2 routes". A
// tree is exactly what a pin wants to be, and Google Maps has been solving that
// one problem for twenty years.
//
// The piece worth copying is the sheet. It is always there, it has three
// heights, and it carries either the list or whatever pin you last tapped. That
// is what stops the map and the list being two destinations you have to choose
// between, which is what ours were.

import SwiftUI
import MapKit

struct MapTab: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    let located: Bool

    @State private var selected: Tree?
    @State private var sheetHeight: SheetHeight = .peek
    @State private var query = ""

    /// A wide net for the map itself: pins the user can pan to matter, and
    /// MapKit clusters whatever it is given.
    private var mapTrees: [Tree] {
        catalogue.nearest(to: origin.lat, origin.lng, limit: 400, withinKm: 200).map(\.tree)
    }
    private var listed: [(tree: Tree, km: Double)] {
        let near = catalogue.nearest(to: origin.lat, origin.lng, limit: 60, withinKm: 50)
        guard !query.isEmpty else { return near }
        let q = query.lowercased()
        return catalogue.trees
            .filter { $0.name.lowercased().contains(q) || $0.city.lowercased().contains(q)
                      || $0.species.lowercased().contains(q) }
            .prefix(40)
            .map { ($0, $0.distanceKm(from: origin.lat, origin.lng)) }
    }

    var body: some View {
        ZStack(alignment: .bottom) {
            TreeMap(trees: mapTrees,
                    focus: .init(latitude: origin.lat, longitude: origin.lng),
                    selected: $selected)
                .ignoresSafeArea(edges: [.top, .horizontal])
            BottomSheet(height: $sheetHeight) {
                sheet
            }
        }
        .navigationTitle(located ? "Near you" : "Near Amsterdam")
        .navigationBarTitleDisplayMode(.inline)
        .onChange(of: selected) { _, new in
            // Tapping a pin raises the sheet to that tree, the way Google Maps
            // turns the sheet into the place you tapped.
            if new != nil { sheetHeight = .half }
        }
    }

    @ViewBuilder private var sheet: some View {
        if let t = selected { selectedTree(t) } else { list }
    }

    private var list: some View {
        ScrollView {
            LazyVStack(spacing: 12) {
                searchField
                ForEach(listed, id: \.tree.id) { hit in
                    NavigationLink {
                        TreeDetail(tree: hit.tree, catalogue: catalogue)
                    } label: {
                        TreeCard(tree: hit.tree, km: hit.km)
                    }
                    .buttonStyle(.plain)
                }
                if listed.isEmpty {
                    Text(query.isEmpty
                         ? "No tree of ours within fifty kilometres."
                         : "Nothing matches “\(query)”.")
                        .font(.footnote).foregroundStyle(.secondary).padding(.top, 30)
                }
            }
            .padding(.horizontal, 16)
            .padding(.bottom, 24)
        }
    }

    private var searchField: some View {
        HStack(spacing: 8) {
            Image(systemName: "magnifyingglass").foregroundStyle(.secondary)
            TextField("Search a tree, species or place", text: $query)
                .textFieldStyle(.plain)
                .autocorrectionDisabled()
                .onTapGesture { sheetHeight = .full }
            if !query.isEmpty {
                Button { query = "" } label: {
                    Image(systemName: "xmark.circle.fill").foregroundStyle(.secondary)
                }
                .buttonStyle(.plain)
            }
        }
        .padding(.horizontal, 12).padding(.vertical, 10)
        .background(Color(.secondarySystemBackground), in: .capsule)
        .padding(.top, 6)
    }

    /// One tapped pin, shown in the sheet rather than pushed onto a page, so the
    /// map stays visible behind the decision.
    private func selectedTree(_ t: Tree) -> some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 12) {
                HStack {
                    Spacer()
                    Button { selected = nil } label: {
                        Image(systemName: "xmark.circle.fill")
                            .font(.title3).foregroundStyle(.secondary)
                    }
                    .buttonStyle(.plain)
                }
                TreeCard(tree: t, km: t.distanceKm(from: origin.lat, origin.lng))
                NavigationLink {
                    TreeDetail(tree: t, catalogue: catalogue)
                } label: {
                    Label("Read why it is worth the walk", systemImage: "book")
                        .font(.subheadline.weight(.semibold))
                        .frame(maxWidth: .infinity).padding(.vertical, 13)
                }
                .buttonStyle(.borderedProminent)
                .tint(Color(red: 0.20, green: 0.35, blue: 0.20))
            }
            .padding(.horizontal, 16).padding(.bottom, 24)
        }
    }
}
