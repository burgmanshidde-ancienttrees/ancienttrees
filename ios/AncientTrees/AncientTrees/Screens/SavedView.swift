// The Saved tab: what you want, before you have been.
//
// The bank-to-street bridge: save Sevilla's fig in January, walk to it in May.
// Day zero opens with suggestions rather than zeros, per Hidde ("we moeten wel
// zorgen dat de middelste 3 opties niet als leeg voelt als je nog niks hebt
// dus daar moeten suggesties in staan iig in saved"): the screen shows the
// nearest trees worth wanting, hearts live, so the first act of using this tab
// is the act that fills it.

import SwiftUI

struct SavedView: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    @Environment(Saved.self) private var saved

    /// Hearts not yet visited, nearest first: the list you walk with.
    private var toVisit: [Tree] {
        saved.entries.keys
            .filter { !saved.isVisited($0) }
            .compactMap { catalogue.tree($0) }
            .sorted { $0.distanceKm(from: origin.lat, origin.lng)
                    < $1.distanceKm(from: origin.lat, origin.lng) }
    }

    private var suggestions: [Tree] {
        Editorial.suggestions(catalogue: catalogue, origin: origin,
                              excluding: Set(saved.entries.keys))
    }

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 16) {
                Text("Trees you want to stand before")
                    .font(.brand(24, .heavy))
                    .foregroundStyle(Brand.ink)
                    .padding(.top, 14)

                if toVisit.isEmpty {
                    Text("Nothing saved yet. Start with these, and tap the heart to keep one for later.")
                        .font(.body)
                        .foregroundStyle(Brand.inkSoft)
                    cards(suggestions)
                } else {
                    cards(toVisit)
                    if !suggestions.isEmpty {
                        Text("Worth adding")
                            .font(.brand(20, .bold))
                            .foregroundStyle(Brand.ink)
                            .padding(.top, 10)
                        cards(Array(suggestions.prefix(3)))
                    }
                }
                Color.clear.frame(height: 90)        // clear of the floating tab bar
            }
            .padding(.horizontal, 20)
            .padding(.top, 6)
        }
        .brandGround()
        .toolbar(.hidden, for: .navigationBar)
    }

    private func cards(_ trees: [Tree]) -> some View {
        ForEach(trees) { t in
            NavigationLink(value: Route.tree(t.id)) {
                TreeCard(tree: t, km: t.distanceKm(from: origin.lat, origin.lng))
            }
            .buttonStyle(.plain)
        }
    }
}
