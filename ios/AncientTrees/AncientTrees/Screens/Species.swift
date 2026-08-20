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

    private var trees: [Tree] {
        catalogue.trees.filter { $0.commonName == commonName }
            .sorted { $0.distanceKm(from: origin.lat, origin.lng) < $1.distanceKm(from: origin.lat, origin.lng) }
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
                        Text("\(trees.count) on the map, nearest first")
                            .font(.footnote).foregroundStyle(Brand.inkSoft)
                    }
                }
                .padding(.horizontal, 16).padding(.top, 4)

                ForEach(trees) { t in
                    NavigationLink(value: Route.tree(t.id)) {
                        TreeCard(tree: t, km: t.distanceKm(from: origin.lat, origin.lng))
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
