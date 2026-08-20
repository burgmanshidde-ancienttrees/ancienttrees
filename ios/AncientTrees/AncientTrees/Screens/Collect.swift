// Collect: the game, and the only tab that is about you rather than about trees.
//
// New on 2026-08-20, from Hidde's own division of the app: "collect is een
// functie die je wilt aanbieden voor de echte nichegebruikers die het tof
// vinden om naar bomen toe te wandelen ... en daarmee vereeuwig je dat je daar
// bent aan de hand van een foto".
//
// It merges what used to be two tabs, Saved and You, and the reason those had
// to merge is that neither was a verb. Saved held the lists and You held the
// score, so the two halves of one idea sat in different places and the profile
// was doing three jobs at once. Now the game is here and the admin is in
// Profile, which is the split AllTrails and Google Maps both make.
//
// WHAT IS FREE HERE AND WHAT IS NOT, because this is where the paywall actually
// touches the product. Ticking a tree off, seeing your own list and your own
// count are free, and they stay free: PRODUCT_IA.md's law 3 is the converged
// finding of a nine-product benchmark rather than an opinion, and it says the
// free account captures the keep-verbs while the paid tier sells in-the-field
// convenience. If collecting itself were paid, a free user would have a map and
// some photographs and no reason to come back, so the habit never forms and
// there is nothing left to convert.
//
// What is sold is the PROOF: your own photograph on the tree's page, the seal
// that says you were standing there, and the badges. That is the same three
// things Hidde's own paywall copy of 2026-08-18 names, and it keeps his
// intention while leaving the hook free.

import SwiftUI

struct CollectView: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    @Environment(Saved.self) private var saved
    @Environment(Account.self) private var account

    @State private var signingIn = false
    @State private var search = ""

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
    private var allVisited: [Tree] {
        saved.entries.values.filter { $0.visitedAt != nil }.compactMap { catalogue.tree($0.treeId) }
    }

    private var countries: Int { Set(allVisited.map(\.country)).count }
    private var cities: Int { Set(allVisited.map(\.citySlug)).count }
    private var collectedSpecies: Set<String> { Set(allVisited.map(\.commonName)) }

    /// The set to fill in: the species we map most, so the grid is worth
    /// completing rather than arbitrary.
    private var stampSpecies: [String] {
        Dictionary(grouping: catalogue.trees, by: \.commonName)
            .sorted { $0.value.count > $1.value.count }
            .prefix(18).map(\.key)
    }

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
            LazyVStack(alignment: .leading, spacing: 22) {
                statsCard
                stampCard
                if !account.isSignedIn && saved.savedCount > 0 { backupBar }

                if saved.entries.isEmpty { empty }

                if !wishlist.isEmpty {
                    header("Want to see", wishlist.count)
                    ForEach(wishlist) { card($0) }
                }
                if !visited.isEmpty {
                    header("Stood in front of", visited.count)
                    ForEach(visited) { card($0) }
                }
                Color.clear.frame(height: 80)
            }
            .padding(.horizontal, 16).padding(.top, 6)
        }
        .brandGround()
        .navigationTitle("Collect")
        .searchable(text: $search, prompt: "Search your trees")
        .sheet(isPresented: $signingIn) {
            SignInSheet(reason: .keepCollection(saved.savedCount), localCount: saved.savedCount)
                .environment(account).environment(saved)
        }
    }

    // MARK: - the score

    private var statsCard: some View {
        VStack(spacing: 14) {
            HStack(spacing: 0) {
                tile("\(allVisited.count)", "Trees")
                Divider().frame(height: 42)
                tile("\(cities)", cities == 1 ? "Place" : "Places")
                Divider().frame(height: 42)
                tile("\(collectedSpecies.count)", "Species")
                Divider().frame(height: 42)
                tile("\(countries)", countries == 1 ? "Country" : "Countries")
            }
            Text("Out of \(catalogue.trees.count.formatted(.number.locale(Locale(identifier: "en_US")))) trees we map in \(Set(catalogue.trees.map(\.country)).count) countries.")
                .font(.caption).foregroundStyle(Brand.inkSoft)
        }
        .padding(.vertical, 18).padding(.horizontal, 8)
        .frame(maxWidth: .infinity)
        .brandCard()
    }

    private func tile(_ value: String, _ label: String) -> some View {
        VStack(spacing: 3) {
            Text(value).font(.brand(26, .black, relativeTo: .title))
                .foregroundStyle(Brand.ink).monospacedDigit()
            Text(label).font(.caption2).foregroundStyle(Brand.inkSoft)
        }
        .frame(maxWidth: .infinity)
    }

    // MARK: - the stamps

    /// Drawn at zero, deliberately. AllTrails shows its progress chart with a
    /// single bar on it rather than hiding it, and every user of this app on its
    /// first day has nothing: the shape of what you are about to fill in does
    /// more than any sentence saying you have not started.
    private var stampCard: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack(alignment: .firstTextBaseline) {
                Text("Species collected").font(.brand(19, .heavy, relativeTo: .title3))
                    .foregroundStyle(Brand.ink)
                Spacer()
                Text("\(collectedSpecies.count) of \(stampSpecies.count)")
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(Brand.inkSoft).monospacedDigit()
            }
            LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: 10), count: 6),
                      spacing: 14) {
                ForEach(stampSpecies, id: \.self) { s in
                    let got = collectedSpecies.contains(s)
                    SpeciesMark(species: s, color: got ? Brand.moss : Brand.inkSoft.opacity(0.28))
                        .frame(height: 34)
                        .accessibilityLabel(got ? "\(s), collected" : "\(s), not yet")
                }
            }
            Text(collectedSpecies.isEmpty
                 ? "Tick a tree off and its species fills in here."
                 : "The eighteen species we map most. Rarer ones count too, they are just not drawn here yet.")
                .font(.caption).foregroundStyle(Brand.inkSoft)
        }
        .padding(18)
        .frame(maxWidth: .infinity, alignment: .leading)
        .brandCard()
    }

    // MARK: - the lists

    private func header(_ t: String, _ n: Int) -> some View {
        HStack(alignment: .firstTextBaseline) {
            Text(t).font(.shelfTitle).foregroundStyle(Brand.ink)
            Text("\(n)").font(.subheadline.weight(.semibold))
                .foregroundStyle(Brand.inkSoft).monospacedDigit()
            Spacer()
        }
        .padding(.top, 6)
    }

    private func card(_ t: Tree) -> some View {
        NavigationLink(value: Route.tree(t.id)) {
            TreeCard(tree: t, km: t.distanceKm(from: origin.lat, origin.lng))
        }
        .buttonStyle(.plain)
        .contextMenu {
            Button(role: .destructive) { saved.toggleSaved(t.id) } label: {
                Label("Remove from saved", systemImage: "heart.slash")
            }
            if saved.isVisited(t.id) {
                Button { saved.toggleVisited(t.id) } label: {
                    Label("Not stood in front of it after all", systemImage: "arrow.uturn.backward")
                }
            }
        }
    }

    /// The passive half of the account ask, and probably the one that does most
    /// of the work. It interrupts nobody and it states a fact rather than a
    /// pitch. A prompt has to be well timed; this only has to be true.
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
                        .font(.caption).foregroundStyle(Brand.inkSoft)
                        .fixedSize(horizontal: false, vertical: true)
                }
                Spacer(minLength: 4)
                Image(systemName: "chevron.right").font(.caption).foregroundStyle(Brand.inkSoft.opacity(0.6))
            }
            .padding(14)
            .brandCard(12)
        }
        .buttonStyle(.plain)
    }

    private var empty: some View {
        VStack(spacing: 12) {
            Text("Nothing collected yet")
                .font(.brand(20, .heavy, relativeTo: .title3)).foregroundStyle(Brand.ink)
            Text("Tap the heart on a tree to keep it, and tick it off once you have stood in front of it. There are \(catalogue.trees.count.formatted(.number.locale(Locale(identifier: "en_US")))) to find.")
                .font(.footnote).foregroundStyle(Brand.inkSoft)
                .multilineTextAlignment(.center).padding(.horizontal, 20)
        }
        .frame(maxWidth: .infinity)
        .padding(.top, 20)
    }
}
