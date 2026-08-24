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
    @Environment(Navigator.self) private var navigator

    @State private var signingIn = false
    @State private var lane: Lane = .want

    // TWO lanes, not three. "Collected" and "Added by you" were separate until
    // 2026-08-24, when Hidde gave the rule that dissolves the split: "je
    // collect de bomen die er zijn en je collect automatisch een boom als je
    // die toevoegt." A tree you added is collected by definition, so it belongs
    // in the same list as the ones you ticked off, newest first, with its own
    // photograph on it.
    enum Lane: Hashable { case want, seen }

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
    /// Every tree you have, ours and your own. Places, species and countries
    /// stay on `allVisited` because a sighting carries a name and a position
    /// and nothing else: counting a tree we cannot name a country for would be
    /// inventing the country.
    private var collectedCount: Int { allVisited.count + sightings.yoursOnly.count }

    private var countries: Int { Set(allVisited.map(\.country)).count }
    private var cities: Int { Set(allVisited.map(\.citySlug)).count }
    private var collectedSpecies: Set<String> { Set(allVisited.map(\.commonName)) }
    /// Have you collected anything OUTSIDE the eighteen drawn above.
    private var restCollected: Bool { !collectedSpecies.subtracting(stampSpecies).isEmpty }

    /// The set to fill in: the species we map most, so the grid is worth
    /// completing rather than arbitrary.
    private var stampSpecies: [String] {
        Dictionary(grouping: catalogue.trees, by: \.commonName)
            .sorted { $0.value.count > $1.value.count }
            .prefix(18).map(\.key)
    }

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 28) {
                HStack(alignment: .firstTextBaseline) {
                    Text("Your trees")
                        .font(.screenTitle)
                        .foregroundStyle(Brand.ink)
                    Spacer(minLength: 8)
                    // Aligned on the TITLE'S CAP HEIGHT, not on its
                    // line box. A 34 point line box carries descender
                    // room that "Explore" never uses, so centring the
                    // circle against it put the circle a couple of
                    // points high, which is exactly the sort of drift
                    // that reads as sloppy without being nameable
                    // (Hidde, 2026-08-22). Cap height on Gabarito
                    // Black at 34 is about 24 points, so the circle's
                    // centre belongs 12 above the baseline.
                    .alignmentGuide(.firstTextBaseline) { d in
                        d[VerticalAlignment.center] + 12
                    }
                }
                .padding(.top, 4)

                // The BUTTON went and the sentence came back (Hidde,
                // 2026-08-24: "je hebt nu de hele collect a tree knop
                // weggehaald maar ik vond die verwijzing en uitleg bovenaan
                // collection wel goed"). He is right about both halves: a
                // full-width button here repeated the camera that sits two
                // centimetres below it in the middle of the bar, while the
                // explanation was doing real work, because nothing else on
                // this screen says HOW a tree gets here.
                HStack(spacing: 10) {
                    Image(systemName: "camera")
                        .font(.footnote).foregroundStyle(Brand.moss)
                    Text("Photograph a tree with the camera below and it is yours, ours or not.")
                        .font(.footnote).foregroundStyle(Brand.inkSoft)
                        .fixedSize(horizontal: false, vertical: true)
                }
                .padding(.bottom, 2)

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
                    }
                    .pickerStyle(.segmented)
                    .accessibilityIdentifier("collect-lane")

                    if lane == .seen, !sightings.yoursOnly.isEmpty {
                        // Yours first, because they are the ones nobody else
                        // has. Still marked as yours on the card, so the
                        // distinction survives where it is useful (this one is
                        // not on the map everybody sees) and disappears where
                        // it was only in the way.
                        ForEach(sightings.yoursOnly) { s in
                            NavigationLink(value: Route.mine(s.id)) { MineCard(sighting: s) }
                                .buttonStyle(.plain)
                        }
                    }
                    Group {
                        let list = lane == .want ? wishlist : visited
                        if list.isEmpty {
                            Text(lane == .want
                                 ? "Nothing on your list. Tap a heart anywhere to put a tree here."
                                 : "Nothing collected yet. Photograph a tree with the button above, ours or one only you know.")
                                .font(.subheadline).foregroundStyle(Brand.inkSoft)
                                .padding(.top, 4)
                        } else {
                            ForEach(list) { card($0) }
                        }
                    }
                }
                Color.clear.frame(height: 80)
            }
            .padding(.horizontal, 20).padding(.top, 8)
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
                tile("\(collectedCount)", "Trees")
                Divider().frame(height: 42)
                tile("\(cities)", cities == 1 ? "Place" : "Places")
                Divider().frame(height: 42)
                tile("\(collectedSpecies.count)", "Species")
                Divider().frame(height: 42)
                tile("\(countries)", countries == 1 ? "Country" : "Countries")
            }
            // The sentence has to survive your own trees being in the count
            // above, because they are not among the ones we map and "12 of
            // 1,842" would quietly be false.
            Text(sightings.yoursOnly.isEmpty
                 ? "Out of \(catalogue.trees.count.formatted(.number.locale(Locale(identifier: "en_US")))) trees we map in \(Set(catalogue.trees.map(\.country)).count) countries."
                 : "\(allVisited.count) from the map we keep, \(sightings.yoursOnly.count) only you have.")
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
                Text("\(collectedSpecies.count) of \(stampSpecies.count + 1)")
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
                // The nineteenth mark: everything else we map. Without it the
                // grid quietly dropped every rarer species you had collected,
                // and the card needed a sentence at the bottom explaining that
                // it was doing so (Hidde, 2026-08-24: "haal die zin weg en
                // zorg gewoon dat er ook een rest icoon is zodat alles eronder
                // valt"). A drawing that counts everything needs no footnote.
                SpeciesMark(species: "", color: restCollected ? Brand.moss : Brand.inkSoft.opacity(0.28))
                    .frame(height: 34)
                    .accessibilityLabel(restCollected
                                        ? "Other species, collected"
                                        : "Other species, not yet")
            }
            if collectedSpecies.isEmpty {
                Text("Collect a tree and its species fills in here.")
                    .font(.caption).foregroundStyle(Brand.inkSoft)
            }
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
                    .font(.brand(24, .bold, relativeTo: .title))
                    .foregroundStyle(Brand.ink)
                Text("Take a photo of it while you are standing there and it is yours. Trees, species and places fill your collection, and the years they have seen add up.")
                    .font(.subheadline).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
                NavigationLink(value: Route.tree(t.id)) {
                    TreeCard(tree: t)
                }
                .buttonStyle(.plain)
                NavigationLink(value: Route.tree(t.id)) {
                    Label("Show the way", systemImage: "arrow.turn.up.right")
                }
                // SECONDARY, because the filled green control on this screen
                // is the one that collects. AllTrails colours exactly one
                // thing per screen and this app's own style rule says the
                // same; two green pills was the screen shouting twice.
                .buttonStyle(BrandButtonStyle(prominent: false))
            }
            .accessibilityElement(children: .contain)
            .accessibilityIdentifier("collect-mission")
        } else {
            // Nowhere near any tree we map: honest, and it still points out.
            VStack(alignment: .leading, spacing: 10) {
                Text("No trees yet")
                    .font(.brand(24, .bold, relativeTo: .title)).foregroundStyle(Brand.ink)
                Text("Take a photo of a tree to start your collection. There are \(catalogue.trees.count.formatted(.number.locale(Locale(identifier: "en_US")))) of ours to find in \(Set(catalogue.trees.map(\.country)).count) countries, and any tree you photograph is yours whether we map it or not.")
                    .font(.subheadline).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
    }
}
