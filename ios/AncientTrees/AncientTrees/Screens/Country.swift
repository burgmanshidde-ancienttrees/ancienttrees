// One country: the places in it, and the trees worth the trip.
//
// New on 2026-08-21 with Explore's rebuild (Hidde: "I would make a list of
// best countries"). The website has had country pages since August; the app
// could not reach the idea at all, which is the sort of gap the whole-page
// check exists to catch.

import SwiftUI

struct CountryView: View {
    let country: String
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)

    private var trees: [Tree] { catalogue.trees.filter { $0.country == country } }

    private var cities: [(slug: String, name: String, count: Int)] {
        Dictionary(grouping: trees, by: \.citySlug)
            .map { (slug: $0.key, name: $0.value[0].city, count: $0.value.count) }
            .sorted { $0.count > $1.count }
    }

    /// Photographs first, then the oldest: the same editorial hand the rest of
    /// the app uses, so no page anywhere opens on what we do not have.
    private var best: [Tree] {
        trees.filter { $0.photo != nil }
            .sorted { ($0.ageMin ?? 0) > ($1.ageMin ?? 0) }
            .prefix(10).map { $0 }
    }

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 22) {
                Text("\(trees.count) trees in \(cities.count) \(cities.count == 1 ? "place" : "places")")
                    .font(.subheadline).foregroundStyle(Brand.inkSoft)
                    .padding(.horizontal, 20)

                if !best.isEmpty {
                    Text("Worth the trip")
                        .font(.brand(20, .heavy)).foregroundStyle(Brand.ink)
                        .padding(.horizontal, 20)
                    ForEach(best) { t in
                        NavigationLink(value: Route.tree(t.id)) {
                            TreeCard(tree: t, km: t.distanceKm(from: origin.lat, origin.lng))
                        }
                        .buttonStyle(.plain)
                        .padding(.horizontal, 20)
                    }
                }

                Text("Places")
                    .font(.brand(20, .heavy)).foregroundStyle(Brand.ink)
                    .padding(.horizontal, 20)
                ForEach(cities, id: \.slug) { c in
                    NavigationLink(value: Route.city(c.slug)) {
                        HStack {
                            Text(c.name).font(.brand(16, .bold)).foregroundStyle(Brand.ink)
                            Spacer()
                            Text("\(c.count)").font(.subheadline)
                                .foregroundStyle(Brand.inkSoft).monospacedDigit()
                            Image(systemName: "chevron.right")
                                .font(.caption).foregroundStyle(Brand.inkSoft.opacity(0.6))
                        }
                        .padding(.vertical, 12).padding(.horizontal, 16)
                        .brandCard(12)
                        .padding(.horizontal, 20)
                    }
                    .buttonStyle(.plain)
                }
                Color.clear.frame(height: 80)
            }
            .padding(.top, 8)
        }
        .brandGround()
        .navigationTitle(country)
        .navigationBarTitleDisplayMode(.inline)
    }
}
