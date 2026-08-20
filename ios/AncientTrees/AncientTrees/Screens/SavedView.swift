// Saved gets its own tab, which is what both references do and what we had
// wrong: AllTrails and Google Maps each split Opgeslagen from the profile,
// because you open your saved places weekly and your account almost never.

import SwiftUI

struct SavedView: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    @Environment(Saved.self) private var saved
    @Environment(Account.self) private var account
    @State private var signingIn = false
    @State private var search = ""

    private let brand = Color(red: 0.20, green: 0.35, blue: 0.20)

    private var visited: [Tree] {
        matching(saved.entries.values.filter { $0.visitedAt != nil }
            .sorted { ($0.visitedAt ?? .distantPast) > ($1.visitedAt ?? .distantPast) }
            .compactMap { catalogue.tree($0.treeId) })
    }
    private var wishlist: [Tree] {
        matching(saved.entries.values.filter { $0.visitedAt == nil }
            .sorted { $0.savedAt > $1.savedAt }
            .compactMap { catalogue.tree($0.treeId) })
    }

    /// A collection is meant to grow, and a few hundred entries is a lot to
    /// scroll past to find the oak you meant.
    private func matching(_ list: [Tree]) -> [Tree] {
        guard !search.isEmpty else { return list }
        let q = search.lowercased()
        return list.filter {
            $0.name.lowercased().contains(q) || $0.city.lowercased().contains(q)
                || $0.species.lowercased().contains(q)
        }
    }

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 14) {
                if visited.isEmpty && wishlist.isEmpty { empty }

                if !account.isSignedIn && !(visited.isEmpty && wishlist.isEmpty) { backupBar }

                if !wishlist.isEmpty {
                    header("Want to see", wishlist.count)
                    ForEach(wishlist) { card($0) }
                }
                if !visited.isEmpty {
                    header("Stood in front of", visited.count)
                    ForEach(visited) { card($0) }
                }
                Color.clear.frame(height: 96)   // clear of the floating tab bar
            }
            .padding(.horizontal, 16).padding(.top, 8)
        }
        .brandGround()
        .navigationTitle("Saved")
        .searchable(text: $search, prompt: "Search your trees")
        .sheet(isPresented: $signingIn) {
            SignInSheet(reason: .keepCollection(saved.savedCount), localCount: saved.savedCount)
                .environment(account)
                .environment(saved)
        }
    }

    /// The passive half of the account ask, and probably the one that does most
    /// of the work. It interrupts nobody, it states a fact rather than a pitch,
    /// and it sits on the screen people open when they already care about what
    /// is on it. A prompt has to be timed; this only has to be true.
    private var backupBar: some View {
        Button { signingIn = true } label: {
            HStack(spacing: 12) {
                Image(systemName: "exclamationmark.icloud")
                    .font(.title3).foregroundStyle(Brand.moss)
                VStack(alignment: .leading, spacing: 2) {
                    Text("Kept on this phone only")
                        .font(.brand(16, .bold, relativeTo: .subheadline))
                        .foregroundStyle(Brand.ink)
                    Text("Sign in and they follow you to a new phone and to the website.")
                        .font(.caption).foregroundStyle(.secondary)
                        .fixedSize(horizontal: false, vertical: true)
                }
                Spacer(minLength: 4)
                Image(systemName: "chevron.right").font(.caption).foregroundStyle(.tertiary)
            }
            .padding(14)
            .brandCard(12)
        }
        .buttonStyle(.plain)
    }

    private func header(_ t: String, _ n: Int) -> some View {
        HStack(alignment: .firstTextBaseline) {
            Text(t).font(.shelfTitle).foregroundStyle(Brand.ink)
            Text("\(n)").font(.subheadline.weight(.semibold))
                .foregroundStyle(Brand.inkSoft).monospacedDigit()
            Spacer()
        }
        .padding(.top, 8)
    }

    private func card(_ t: Tree) -> some View {
        NavigationLink(value: Route.tree(t.id)) {
            TreeCard(tree: t, km: t.distanceKm(from: origin.lat, origin.lng))
        }
        .buttonStyle(.plain)
        // The way out. A heart on the card toggles it too, but a card is not a
        // row and there is nothing to swipe, so the long press carries the
        // destructive action the way it does on a Home Screen icon.
        .contextMenu {
            Button(role: .destructive) {
                saved.toggleSaved(t.id)
            } label: {
                Label("Remove from saved", systemImage: "heart.slash")
            }
            if saved.isVisited(t.id) {
                Button {
                    saved.toggleVisited(t.id)
                } label: {
                    Label("Not stood in front of it after all", systemImage: "arrow.uturn.backward")
                }
            }
        }
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
            Text("Nothing saved yet").font(.brand(20, .heavy, relativeTo: .title3))
                .foregroundStyle(Brand.ink)
            Text("Tap the heart on a tree to keep it here, and tick it off once you have stood in front of it. There are \(catalogue.trees.count) to find.")
                .font(.footnote).foregroundStyle(.secondary)
                .multilineTextAlignment(.center).padding(.horizontal, 24)
        }
    }
}
