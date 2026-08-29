// One country: the places in it, and the trees worth the trip.
//
// New on 2026-08-21 with Explore's rebuild (Hidde: "I would make a list of
// best countries"). The website has had country pages since August; the app
// could not reach the idea at all, which is the sort of gap the whole-page
// check exists to catch.

import SwiftUI
import CoreLocation

struct CountryView: View {
    let country: String
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)

    private var trees: [Tree] { catalogue.trees.filter { $0.country == country } }

    /// Where the preview opens: the middle of the country's own trees, which is
    /// not the middle of the country and is the more useful of the two.
    private var centre: CLLocationCoordinate2D? {
        guard !trees.isEmpty else { return nil }
        return CLLocationCoordinate2D(
            latitude: trees.map(\.lat).reduce(0, +) / Double(trees.count),
            longitude: trees.map(\.lng).reduce(0, +) / Double(trees.count))
    }

    private var span: CLLocationDistance {
        let lats = trees.map(\.lat), lngs = trees.map(\.lng)
        guard let loLat = lats.min(), let hiLat = lats.max(),
              let loLng = lngs.min(), let hiLng = lngs.max() else { return 400_000 }
        let m = max((hiLat - loLat) * 111_000, (hiLng - loLng) * 111_000 * 0.62)
        return max(m * 1.25, 4000)
    }

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
                // THE MAP FIRST, the same as a city page (Hidde, 2026-08-27:
                // "als er op een landpagina komt, staat de kaart daar, klik je
                // op de kaart, open het die kaart, maar niet in de kaartsectie
                // ... zodat je altijd op vorige kan blijven klikken"). A
                // country had no map at all until now, which made it the one
                // page in this flow that could not show you where anything is.
                //
                // A picture that opens the real thing, pushed, exactly as the
                // city page does it. The map itself takes no taps, so a finger
                // dragging past it still scrolls the page.
                NavigationLink(value: Route.placeMap(.country(country))) {
                    ZStack(alignment: .bottomTrailing) {
                        TreeMap(trees: trees,
                                focus: centre,
                                // Same as the city page: a picture, not a map.
                                showsRecentre: false,
                                spanMeters: span,
                                fitsTrees: true,
                                selected: .constant(nil))
                            .allowsHitTesting(false)
                        Label("Expand map",
                              systemImage: "arrow.up.left.and.arrow.down.right")
                            .font(.caption.weight(.semibold))
                            .foregroundStyle(Brand.ink)
                            .padding(.horizontal, 12).padding(.vertical, 8)
                            .background(Brand.surface, in: .capsule)
                            .overlay { Capsule().strokeBorder(Brand.hairline, lineWidth: 1) }
                            .shadow(color: .black.opacity(0.10), radius: 4, y: 1)
                            .padding(10)
                    }
                    .frame(height: 260)
                    .clipShape(.rect(cornerRadius: 16))
                    .contentShape(.rect)
                }
                .buttonStyle(.plain)
                .accessibilityIdentifier("country-open-map")
                .padding(.horizontal, 16)

                Text("\(trees.count) trees in \(cities.count) \(cities.count == 1 ? "place" : "places")")
                    .font(.subheadline).foregroundStyle(Brand.inkSoft)
                    .padding(.horizontal, 20)

                if !best.isEmpty {
                    Text("Worth the trip")
                        .font(.brand(20, .heavy)).foregroundStyle(Brand.ink)
                        .padding(.horizontal, 20)
                    ForEach(best) { t in
                        NavigationLink(value: Route.tree(t.id)) {
                            TreeCard(tree: t)
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
