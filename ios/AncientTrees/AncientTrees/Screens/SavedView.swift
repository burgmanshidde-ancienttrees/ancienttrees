// Saved gets its own tab, which is what both references do and what we had
// wrong: AllTrails and Google Maps each split Opgeslagen from the profile,
// because you open your saved places weekly and your account almost never.

import SwiftUI

struct SavedView: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    @Environment(Saved.self) private var saved

    private var visited: [Tree] {
        saved.entries.values.filter { $0.visitedAt != nil }
            .sorted { ($0.visitedAt ?? .distantPast) > ($1.visitedAt ?? .distantPast) }
            .compactMap { catalogue.tree($0.treeId) }
    }
    private var wishlist: [Tree] {
        saved.entries.values.filter { $0.visitedAt == nil }
            .sorted { $0.savedAt > $1.savedAt }
            .compactMap { catalogue.tree($0.treeId) }
    }

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 14) {
                if visited.isEmpty && wishlist.isEmpty { empty }

                if !wishlist.isEmpty {
                    header("Want to see", wishlist.count)
                    ForEach(wishlist) { card($0) }
                }
                if !visited.isEmpty {
                    header("Stood in front of", visited.count)
                    ForEach(visited) { card($0) }
                }
                Color.clear.frame(height: 40)
            }
            .padding(.horizontal, 16).padding(.top, 8)
        }
        .background(Color(.systemGroupedBackground))
        .navigationTitle("Saved")
    }

    private func header(_ t: String, _ n: Int) -> some View {
        HStack {
            Text(t).font(.headline)
            Text("\(n)").font(.subheadline).foregroundStyle(.secondary).monospacedDigit()
            Spacer()
        }
        .padding(.top, 6)
    }

    private func card(_ t: Tree) -> some View {
        NavigationLink {
            TreeDetail(tree: t, catalogue: catalogue)
        } label: {
            TreeCard(tree: t, km: t.distanceKm(from: origin.lat, origin.lng))
        }
        .buttonStyle(.plain)
    }

    /// Shown at full size rather than hidden behind a message, the way
    /// AllTrails draws a progress chart with one bar on it. The shape of what
    /// you are about to fill in is the invitation.
    private var empty: some View {
        VStack(spacing: 14) {
            HStack(spacing: 22) {
                ForEach(["Silver Maple", "Ginkgo", "Cedar of Lebanon", "Pedunculate Oak"], id: \.self) { s in
                    SpeciesMark(species: s, color: .secondary.opacity(0.28))
                        .frame(width: 46, height: 46)
                }
            }
            .padding(.top, 30)
            Text("Nothing saved yet").font(.headline)
            Text("Tap the heart on a tree to keep it here, and tick it off once you have stood in front of it. There are \(catalogue.trees.count) to find.")
                .font(.footnote).foregroundStyle(.secondary)
                .multilineTextAlignment(.center).padding(.horizontal, 24)
        }
    }
}
