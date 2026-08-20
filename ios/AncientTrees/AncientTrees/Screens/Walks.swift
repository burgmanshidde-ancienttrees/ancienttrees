// The walk verb. A walk is the thing that turns a list of trees into an
// afternoon, which is the whole value proposition, so it gets its own tab.

import SwiftUI
import MapKit
import CoreLocation

struct WalksView: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)

    /// Nearest walks first, by the distance to their first tree. A walk on the
    /// other side of Europe is not a suggestion, it is noise.
    private var walks: [(walk: Walk, km: Double)] {
        catalogue.walks.compactMap { w in
            guard let first = catalogue.trees(of: w).first else { return nil }
            return (w, first.distanceKm(from: origin.lat, origin.lng))
        }
        .sorted { $0.km < $1.km }
    }

    var body: some View {
        List(walks.prefix(40), id: \.walk.name) { item in
            NavigationLink(value: Route.walk(city: item.walk.citySlug, name: item.walk.name)) {
                VStack(alignment: .leading, spacing: 5) {
                    Text(item.walk.name).font(.headline)
                    Text(item.walk.city).font(.subheadline).foregroundStyle(.secondary)
                    HStack(spacing: 12) {
                        Label("\(item.walk.count) trees", systemImage: "tree")
                        Label(item.walk.duration, systemImage: "clock")
                        Label(String(format: "%.1f km", item.walk.km), systemImage: "figure.walk")
                    }
                    .font(.caption).foregroundStyle(.secondary)
                }
                .padding(.vertical, 3)
            }
        }
        .listStyle(.plain)
        .navigationTitle("Walks")
    }
}

struct WalkDetail: View {
    let walk: Walk
    let catalogue: Catalogue
    @State private var selected: Tree?

    private var trees: [Tree] { catalogue.trees(of: walk) }

    /// The cached routed shape when there is one, otherwise the order the trees
    /// are visited. The map draws the second dashed so nobody reads it as a path.
    private var routeLine: [CLLocationCoordinate2D] {
        if let shape = walk.shape, shape.count > 1 {
            return shape.compactMap { p in
                p.count == 2 ? CLLocationCoordinate2D(latitude: p[1], longitude: p[0]) : nil
            }
        }
        return trees.map { .init(latitude: $0.lat, longitude: $0.lng) }
    }

    var body: some View {
        ZStack(alignment: .bottom) {
            VStack(spacing: 0) {
                TreeMap(trees: trees,
                        focus: trees.first.map { .init(latitude: $0.lat, longitude: $0.lng) },
                        route: routeLine,
                        routeIsReal: walk.shape != nil,
                        selected: $selected)
                    .frame(maxHeight: .infinity)
                List {
                    ForEach(Array(trees.enumerated()), id: \.element.id) { i, t in
                        NavigationLink(value: Route.tree(t.id)) {
                            HStack(spacing: 12) {
                                Text("\(i + 1)")
                                    .font(.caption.bold()).foregroundStyle(.white)
                                    .frame(width: 24, height: 24)
                                    .background(Color(red: 0.20, green: 0.35, blue: 0.20), in: .circle)
                                VStack(alignment: .leading, spacing: 2) {
                                    Text(t.name).font(.subheadline.weight(.medium))
                                    Text(t.commonName).font(.caption).foregroundStyle(.secondary)
                                }
                            }
                        }
                    }
                }
                .listStyle(.plain)
                .frame(height: 240)
            }
            VStack(spacing: 0) {
                if walk.shape == nil {
                    Text("The line shows the order, not the route: nobody has walked this one for us yet.")
                        .font(.caption2).foregroundStyle(.secondary)
                        .padding(.horizontal, 16).padding(.vertical, 6)
                        .frame(maxWidth: .infinity)
                        .background(.bar)
                }
                beginBar
            }
        }
        .navigationTitle(walk.name)
        .navigationBarTitleDisplayMode(.inline)
    }

    /// `Begin` pinned to the bottom, first in the bar and the only coloured
    /// thing in it. This is the teardown's sharpest finding applied.
    private var beginBar: some View {
        HStack(spacing: 12) {
            Button {
                if let first = trees.first {
                    let url = URL(string: "maps://?daddr=\(first.lat),\(first.lng)&dirflg=w")!
                    UIApplication.shared.open(url)
                }
            } label: {
                Label("Begin", systemImage: "location.fill")
                    .font(.headline).frame(maxWidth: .infinity).padding(.vertical, 14)
            }
            .buttonStyle(.borderedProminent)
            .tint(Color(red: 0.20, green: 0.35, blue: 0.20))

            VStack(alignment: .trailing, spacing: 1) {
                Text(walk.duration).font(.subheadline.weight(.semibold))
                Text(String(format: "%.1f km", walk.km)).font(.caption).foregroundStyle(.secondary)
            }
        }
        .padding(.horizontal, 16).padding(.vertical, 10)
        .background(.bar)
    }
}
