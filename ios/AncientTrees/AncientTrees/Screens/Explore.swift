// Browse, for when you are not going anywhere right now.
//
// Season lives here as a shelf rather than as its own tab. 546 of 1377 trees
// carry a best_time at all, and near one person in one month that is often a
// handful or nothing, so a whole tab would stand empty a lot of the time. As a
// shelf it appears when it has something and stays quiet when it does not.

import SwiftUI

struct ExploreView: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    @Environment(Saved.self) private var saved

    private var month: Int { Calendar.current.component(.month, from: Date()) }
    private var monthName: String { DateFormatter().monthSymbols[month - 1] }
    private var atTheirBest: [Tree] {
        catalogue.atTheirBest(inMonth: month, near: origin.lat, origin.lng, withinKm: 150)
    }
    private var cities: [(slug: String, name: String, count: Int)] {
        Dictionary(grouping: catalogue.trees, by: \.citySlug)
            .map { (slug: $0.key, name: $0.value[0].city, count: $0.value.count) }
            .sorted { $0.count > $1.count }
    }
    private var walksNear: [Walk] {
        catalogue.walks.compactMap { w -> (Walk, Double)? in
            guard let f = catalogue.trees(of: w).first else { return nil }
            return (w, f.distanceKm(from: origin.lat, origin.lng))
        }
        .sorted { $0.1 < $1.1 }.prefix(8).map(\.0)
    }

    var body: some View {
        List {
            if !atTheirBest.isEmpty {
                Section {
                    ForEach(atTheirBest.prefix(5)) { t in
                        NavigationLink { TreeDetail(tree: t, catalogue: catalogue) } label: {
                            VStack(alignment: .leading, spacing: 3) {
                                Text(t.name).font(.subheadline.weight(.medium))
                                if let b = t.bestTime {
                                    Text(b.label).font(.caption).foregroundStyle(.secondary)
                                }
                            }
                        }
                    }
                } header: {
                    Text("At their best in \(monthName)")
                } footer: {
                    Text("A tree only gets this if its moment is genuinely worth crossing town for.")
                }
            }

            Section("Walks near you") {
                ForEach(walksNear, id: \.name) { w in
                    NavigationLink { WalkDetail(walk: w, catalogue: catalogue) } label: {
                        VStack(alignment: .leading, spacing: 3) {
                            Text(w.name).font(.subheadline.weight(.medium))
                            Text("\(w.city) · \(w.count) trees · \(w.duration)")
                                .font(.caption).foregroundStyle(.secondary)
                        }
                    }
                }
            }

            Section("Places") {
                ForEach(cities.prefix(30), id: \.slug) { c in
                    NavigationLink {
                        CityView(slug: c.slug, name: c.name, catalogue: catalogue, origin: origin)
                    } label: {
                        HStack {
                            Text(c.name)
                            Spacer()
                            Text("\(c.count)").font(.caption).foregroundStyle(.secondary)
                                .monospacedDigit()
                        }
                    }
                }
            }
        }
        .navigationTitle("Explore")
    }
}

struct CityView: View {
    let slug: String
    let name: String
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)

    private var trees: [Tree] { catalogue.trees.filter { $0.citySlug == slug } }

    var body: some View {
        List {
            let walks = catalogue.walks(inCity: slug)
            if !walks.isEmpty {
                Section("Walks") {
                    ForEach(walks, id: \.name) { w in
                        NavigationLink { WalkDetail(walk: w, catalogue: catalogue) } label: {
                            Text("\(w.name) · \(w.count) trees · \(w.duration)")
                                .font(.subheadline)
                        }
                    }
                }
            }
            Section("\(trees.count) trees") {
                ForEach(trees) { t in
                    NavigationLink { TreeDetail(tree: t, catalogue: catalogue) } label: {
                        VStack(alignment: .leading, spacing: 2) {
                            Text(t.name).font(.subheadline.weight(.medium))
                            Text(t.commonName).font(.caption).foregroundStyle(.secondary)
                        }
                    }
                }
            }
        }
        .navigationTitle(name)
    }
}
