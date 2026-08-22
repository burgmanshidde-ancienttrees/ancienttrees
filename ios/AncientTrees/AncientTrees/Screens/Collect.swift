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
    @Environment(Sightings.self) private var sightings

    @State private var signingIn = false
    @State private var lane: Lane = .want

    enum Lane: Hashable { case want, seen, mine }

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

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 22) {
                HStack(alignment: .center) {
                    Text("Collect")
                        .font(.screenTitle)
                        .foregroundStyle(Brand.ink)
                    Spacer(minLength: 8)
                    ProfileButton()
                }
                .padding(.top, 4)

                // Day zero opens with a MISSION, not with the score. Four
                // zeros and eighteen grey ghosts were Hidde's own evidence
                // that the app leads with what you do not have ("Collect is
                // vier nullen plus achttien grijze spookjes"); the shape-of-
                // the-grid argument in stampCard's comment below holds once
                // there is one stamp in it, so the score renders from the
                // first tick, never before.
                if allVisited.isEmpty {
                    mission
                } else {
                    statsCard
                    stampCard
                }
                if !account.isSignedIn && saved.savedCount > 0 { backupBar }

                // Want and had are one idea in two states, so they are two
                // segments rather than two tabs (Hidde, 2026-08-21: Saved as
                // its own tab was a second empty room, and "collect is
                // natuurlijk eigenlijk gewoen een beetje hetzelfde").
                if !saved.entries.isEmpty || !sightings.yoursOnly.isEmpty {
                    Picker("", selection: $lane) {
                        Text("Want to see").tag(Lane.want)
                        Text("Collected").tag(Lane.seen)
                        Text("Yours").tag(Lane.mine)
                    }
                    .pickerStyle(.segmented)
                    .accessibilityIdentifier("collect-lane")

                    if lane == .mine {
                        // Trees only YOU have: photographed, kept, and still
                        // yours whether or not we take them for the map.
                        if sightings.yoursOnly.isEmpty {
                            Text("Trees you find that we do not map yet appear here. Photograph one with the Spot button.")
                                .font(.subheadline).foregroundStyle(Brand.inkSoft)
                                .padding(.top, 4)
                        } else {
                            ForEach(sightings.yoursOnly) { sightingCard($0) }
                        }
                    } else {
                        let list = lane == .want ? wishlist : visited
                        if list.isEmpty {
                            Text(lane == .want
                                 ? "Nothing on your list. Tap a heart anywhere to put a tree here."
                                 : "Nothing collected yet. Stand before a tree and use the Spot button.")
                                .font(.subheadline).foregroundStyle(Brand.inkSoft)
                                .padding(.top, 4)
                        } else {
                            ForEach(list) { card($0) }
                        }
                    }
                }
                Color.clear.frame(height: 80)
            }
            .padding(.horizontal, 16).padding(.top, 6)
        }
        .brandGround()
        // No literal tab-label heading; the mission or the score leads.
        .toolbar(.hidden, for: .navigationBar)
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
                 : "The eighteen species we map most. Rarer ones count too; they are simply not drawn here yet.")
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
            TreeCard(tree: t)
        }
        .buttonStyle(.plain)
        .accessibilityIdentifier("tree-card")
        .contextMenu {
            Button(role: .destructive) { saved.toggleSaved(t.id) } label: {
                Label("Remove from saved", systemImage: "heart.slash")
            }
            if saved.isVisited(t.id) {
                Button { saved.toggleVisited(t.id) } label: {
                    Label("I have not seen this one after all", systemImage: "arrow.uturn.backward")
                }
            }
        }
    }

    /// One of your own finds: your photograph, what you called it, and where
    /// the suggestion stands if you offered it. The status is the honest half
    /// of asking somebody to do work for us (Hidde, 2026-08-21).
    private func sightingCard(_ s: Sightings.Sighting) -> some View {
        VStack(alignment: .leading, spacing: 0) {
            if let img = sightings.image(s) {
                Image(uiImage: img)
                    .resizable().aspectRatio(contentMode: .fill)
                    .frame(height: 170).frame(maxWidth: .infinity)
                    .clipped()
            }
            VStack(alignment: .leading, spacing: 5) {
                Text(s.name)
                    .font(.cardTitle).foregroundStyle(Brand.ink)
                    .lineLimit(2).multilineTextAlignment(.leading)
                HStack(spacing: 6) {
                    Text(s.date.formatted(date: .abbreviated, time: .omitted))
                    if s.status != .mine {
                        Text("·")
                        Text(s.status.label)
                            .foregroundStyle(s.status == .published ? Brand.moss : Brand.inkSoft)
                    }
                }
                .font(.caption).foregroundStyle(Brand.inkSoft)
            }
            .padding(.horizontal, 14).padding(.vertical, 12)
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .brandCard()
    }

    /// The passive half of the account ask, and probably the one that does most
    /// of the work. It interrupts nobody and it states a fact rather than a
    /// pitch. A prompt has to be well timed; this only has to be true.
    private var backupBar: some View {
        Button { signingIn = true } label: {
            HStack(spacing: 12) {
                Image(systemName: "person.crop.circle")
                    .font(.title3).foregroundStyle(Brand.moss)
                VStack(alignment: .leading, spacing: 2) {
                    Text("Sign in")
                        .font(.brand(16, .bold, relativeTo: .subheadline))
                        .foregroundStyle(Brand.ink)
                    Text("Your collection follows you to the website and to any phone.")
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

    // MARK: - day zero: a mission, not a score

    /// The nearest tree worth walking to: your nearest heart if you have one,
    /// the best suggestion nearby if you do not.
    private var missionTree: Tree? {
        wishlist.min { $0.distanceKm(from: origin.lat, origin.lng)
                     < $1.distanceKm(from: origin.lat, origin.lng) }
        ?? Editorial.suggestions(catalogue: catalogue, origin: origin,
                                 excluding: Set(saved.entries.keys), limit: 1).first
    }

    private func distanceLabel(_ t: Tree) -> String {
        let km = t.distanceKm(from: origin.lat, origin.lng)
        return km < 1 ? "\(Int(km * 1000)) m" : String(format: "%.1f km", km)
    }

    @ViewBuilder private var mission: some View {
        if let t = missionTree {
            VStack(alignment: .leading, spacing: 12) {
                Text("Your first tree is \(distanceLabel(t)) away")
                    .font(.brand(24, .heavy, relativeTo: .title))
                    .foregroundStyle(Brand.ink)
                Text("Stand before it and tick it off with the Spot button. Trees, species and places fill your collection, and the years they have seen add up.")
                    .font(.subheadline).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
                NavigationLink(value: Route.tree(t.id)) {
                    TreeCard(tree: t)
                }
                .buttonStyle(.plain)
                NavigationLink(value: Route.tree(t.id)) {
                    HStack { Spacer()
                        Label("Show the way", systemImage: "arrow.turn.up.right")
                            .font(.brand(17, .bold))
                        Spacer() }
                        .padding(.vertical, 15)
                        .background(Brand.moss, in: .rect(cornerRadius: 15))
                        .foregroundStyle(.white)
                }
                .buttonStyle(.plain)
            }
            .accessibilityElement(children: .contain)
            .accessibilityIdentifier("collect-mission")
        } else {
            // Nowhere near any tree we map: honest, and it still points out.
            VStack(alignment: .leading, spacing: 10) {
                Text("Nothing collected yet")
                    .font(.brand(24, .heavy, relativeTo: .title)).foregroundStyle(Brand.ink)
                Text("There are \(catalogue.trees.count.formatted(.number.locale(Locale(identifier: "en_US")))) trees to find in \(Set(catalogue.trees.map(\.country)).count) countries. Explore the map, save the ones you want, and tick them off as you stand before them.")
                    .font(.subheadline).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
    }
}
