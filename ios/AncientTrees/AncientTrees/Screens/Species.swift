// One species, and every tree of it we map.
//
// The website has a page per species and the app had no way to reach one, which
// left a whole layer of the site with no equivalent here. PRODUCT_IA.md calls
// this the compact directory: present for the determined, invisible as
// furniture, and never occupying the living room.

import SwiftUI

struct SpeciesView: View {
    let commonName: String
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)

    /// Photographed first, then nearest.
    ///
    /// Hidde, 2026-08-25: "when I click on a species from Explore, I think you
    /// should put the ones that have a photo on top." He is right for the
    /// reason the whole editorial order on this app already runs on: a page of
    /// silhouettes is a page nobody scrolls, and only a fifth of our trees
    /// carry a photograph, so nearest-first can open on five drawings in a row.
    /// Distance still decides inside each group, so the nearest photographed
    /// tree leads and the list stays useful where you are standing.
    private var trees: [Tree] {
        catalogue.trees.filter { $0.commonName == commonName }
            .sorted {
                let a = $0.photo != nil, b = $1.photo != nil
                if a != b { return a }
                return $0.distanceKm(from: origin.lat, origin.lng)
                     < $1.distanceKm(from: origin.lat, origin.lng)
            }
    }

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 14) {
                HStack(spacing: 12) {
                    SpeciesMark(species: commonName, color: Brand.moss)
                        .frame(width: 44, height: 44)
                    VStack(alignment: .leading, spacing: 2) {
                        Text(commonName).font(.brand(20, .heavy, relativeTo: .title3))
                            .foregroundStyle(Brand.ink)
                        Text("\(trees.count) on the map, photographed first")
                            .font(.footnote).foregroundStyle(Brand.inkSoft)
                    }
                }
                .padding(.horizontal, 16).padding(.top, 4)

                ForEach(trees) { t in
                    NavigationLink(value: Route.tree(t.id)) {
                        TreeCard(tree: t)
                            .padding(.horizontal, 16)
                    }
                    .buttonStyle(.plain)
                    .accessibilityIdentifier("tree-card")
                }
                Color.clear.frame(height: 90)
            }
            .padding(.top, 6)
        }
        .brandGround()
        .navigationTitle(commonName)
        .navigationBarTitleDisplayMode(.inline)
    }
}
