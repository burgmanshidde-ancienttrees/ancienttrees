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
    @State private var showAllStamps = false
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
    // restCount went with the line that printed it (2026-08-25).

    /// Yours first, then the rest, both in the grid's own order.
    ///
    /// The point of the grid is what you have and what is left, and eighteen
    /// unsorted marks made you hunt for your own (Hidde, same message:
    /// "degene die je verzameld hebt zet die bovenaan").
    private var orderedStamps: [String] {
        let got = stampSpecies.filter { collectedSpecies.contains($0) }
        return got + stampSpecies.filter { !collectedSpecies.contains($0) }
    }

    /// The set to fill in: the species we map most, so the grid is worth
    /// completing rather than arbitrary.
    private var stampSpecies: [String] {
        // THE NAME BREAKS THE TIE, and without it this grid was not a set.
        //
        // Hidde filmed it on 2026-08-25: "the amount of species collected jumps
        // and changes the screen every 2 seconds". Four species sit on exactly
        // 20 trees, which is the count at eighteenth place, so which of them
        // made the cut was decided by a Dictionary's unordered iteration and an
        // unstable sort. Every time the view was rebuilt the grid could hold a
        // different eighteen, so the contents shuffled and "collected of
        // eighteen" jumped, and the view was being rebuilt constantly because
        // it reads `origin` and the location provider published every GPS tick.
        // Both halves are fixed; this is the half that made the number lie.
        // Written in named steps, each with its type, because as one chained
        // expression it compiled here and timed out on the CI runner ("the
        // compiler is unable to type-check this expression in reasonable time",
        // 2026-08-25). A ternary inside a sort closure over a Dictionary makes
        // the type checker try a great many overloads, and how many it gets
        // through depends on the machine, which is the worst kind of red: green
        // on the desk that wrote it, red on the gate.
        let byName: [String: [Tree]] = Dictionary(grouping: catalogue.trees, by: \.commonName)
        let ranked: [(key: String, value: [Tree])] = byName.sorted { a, b in
            if a.value.count != b.value.count { return a.value.count > b.value.count }
            return a.key < b.key
        }
        return ranked.prefix(18).map(\.key)
    }

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 28, pinnedViews: [.sectionHeaders]) {
                HStack(alignment: .firstTextBaseline) {
                    // "Collection", the same word as the tab. It said "Your
                    // trees" while the tab said Yours, which was a deliberate
                    // pair; the tab was renamed on 2026-08-24 and this title
                    // was not, so the bar and the screen have disagreed since.
                    // Nobody caught it because appsweep gave this screen and
                    // the curated collection page the same filename, so the
                    // page overwrote the tab and the tab was never looked at
                    // (found 2026-08-25, the first time it was photographed).
                    // The ruling it follows is MapTab's: collect the deed,
                    // collected the state, collection the place. One root.
                    Text("Collection")
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
                // The "Every tree you photograph joins your collection" line is
                // gone (Hidde, 2026-08-25: "haal die hele every tree you
                // photograph functie boven aan collection maar weg"). It had
                // been a sentence, then a button an hour earlier on his own ask,
                // and both versions were explaining the app on the screen that
                // should be showing what you have. The camera in the middle of
                // the tab bar is two centimetres below it and says the same
                // thing by being a camera.

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
                //
                // PINNED, since 2026-08-25, and that is the fix for the thing
                // he has now reported three times: "ik kan nog steeds niet op
                // want to see klikken in collection". The control was not dead.
                // It sat in the scrolling content directly above a list that is
                // rebuilt wholesale on every switch, so the moment it was
                // tapped the content under it changed height and the picker
                // moved out from under the finger; on a fast Mac the tap landed
                // anyway and on a phone, or on the CI runner, it did not. The
                // app's own CI had been failing on exactly this since it was
                // written, which is the first time that gate has caught
                // something my machine could not reproduce.
                //
                // A section header is also the convention: Photos, Files and
                // the App Store all pin a segmented control rather than let it
                // scroll away from the list it governs.
                if !saved.entries.isEmpty || !sightings.yoursOnly.isEmpty {
                    Section {
                        laneContent
                    } header: {
                        lanePicker
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

    /// The lane picker, pinned. Opaque, because a pinned header with a clear
    /// background has the list sliding visibly underneath it.
    private var lanePicker: some View {
        Picker("", selection: $lane) {
            Text("Want to see").tag(Lane.want)
            Text("Collected").tag(Lane.seen)
        }
        .pickerStyle(.segmented)
        .accessibilityIdentifier("collect-lane")
        .padding(.vertical, 10)
        .background(Brand.ground)
    }

    /// Everything the picker switches, rebuilt rather than reshuffled.
    ///
    /// Switching lanes used to leave the previous lane's NavigationLinks in the
    /// stack's hit-test geometry, so a tap on the picker opened whichever card
    /// had been under it (Hidde, 2026-08-24: "als ik op collected klik en weer
    /// op want to see dan opent die de boom eronder"). The `.id(lane)` below is
    /// that fix and it stays; what changed on 08-25 is that the picker no
    /// longer moves when this rebuild changes the content's height.
    @ViewBuilder private var laneContent: some View {
        VStack(alignment: .leading, spacing: 28) {
            if lane == .seen, !sightings.yoursOnly.isEmpty {
                // Yours first, because they are the ones nobody else has. Still
                // marked as yours on the card, so the distinction survives
                // where it is useful (this one is not on the map everybody
                // sees) and disappears where it was only in the way.
                ForEach(sightings.yoursOnly) { s in
                    NavigationLink(value: Route.mine(s.id)) { MineCard(sighting: s) }
                        .buttonStyle(.plain)
                }
            }
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
        .frame(maxWidth: .infinity, alignment: .leading)
        .id(lane)
    }

    // MARK: - the score

    private var statsCard: some View {
        VStack(spacing: 14) {
            HStack(spacing: 0) {
                tile("\(collectedCount)", "Trees")
                Divider().frame(height: 42)
                // It counts distinct cities, so it says cities (Hidde, 2026-08-24:
                // "je bedoelt me place city?"). "Place" was vaguer than the
                // truth, and vaguer reads as evasive rather than as roomy.
                tile("\(cities)", cities == 1 ? "City" : "Cities")
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
    /// One mark with its name under it. Collected is moss and named in full
    /// ink; the rest are dimmed, which reads as "not yet" rather than as
    /// "missing".
    private func stamp(_ name: String, got: Bool) -> some View {
        VStack(spacing: 5) {
            SpeciesMark(species: name == "Anything else" ? "" : name,
                        color: got ? Brand.moss : Brand.inkSoft.opacity(0.28))
                .frame(height: 32)
            Text(name)
                .font(.caption2)
                .foregroundStyle(got ? Brand.ink : Brand.inkSoft)
                .multilineTextAlignment(.center)
                .lineLimit(2)
                .frame(maxWidth: .infinity)
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel(got ? "\(name), collected" : "\(name), not yet")
    }

    private var stampCard: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack(alignment: .firstTextBaseline) {
                Text("Species collected").font(.brand(19, .heavy, relativeTo: .title3))
                    .foregroundStyle(Brand.ink)
                Spacer()
                // The GRID's score, so it counts the grid. It read
                // "collected of eighteen plus one" while the numerator counted
                // every species you own, which could pass the denominator.
                Text("\(collectedSpecies.intersection(Set(stampSpecies)).count) of \(stampSpecies.count)")
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(Brand.inkSoft).monospacedDigit()
            }
            // NAMES under the marks, and three columns rather than six.
            //
            // Sixteen drawings cover forty species here, so five of the
            // eighteen most-mapped ones share the generic broadleaf: Horse
            // Chestnut, both beeches, Hackberry and Common Lime are all a dome
            // on a trunk, and no silhouette separates them. Oak, plane, fig and
            // cedar each cover two more. A grid of unlabelled marks therefore
            // could not be read whatever it was drawn like, which is the real
            // fault rather than the drawings.
            LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: 10), count: 3),
                      spacing: 16) {
                // NINE, three rows of three, until you ask for the rest
                // (Hidde, 2026-08-25: "dit is veel te veel"). Eighteen marks
                // is a page of homework on a screen that is meant to show you
                // what you have.
                ForEach(showAllStamps ? orderedStamps : Array(orderedStamps.prefix(9)),
                        id: \.self) { sp in
                    stamp(sp, got: collectedSpecies.contains(sp))
                }
            }
            if orderedStamps.count > 9 {
                Button {
                    withAnimation(.snappy) { showAllStamps.toggle() }
                } label: {
                    Text(showAllStamps ? "Show fewer"
                                       : "Show all \(orderedStamps.count)")
                        .font(.footnote.weight(.semibold))
                        .foregroundStyle(Brand.moss)
                        .frame(maxWidth: .infinity, minHeight: 44)
                        .contentShape(.rect)
                }
                .buttonStyle(.plain)
                .accessibilityIdentifier("stamps-more")
            }
            // The "and one more species outside this set" line is gone (Hidde,
            // 2026-08-25: "please delete that line, why would you say that").
            // He is right: it was bookkeeping about our own eighteen-species
            // grid, addressed to somebody who never asked what the grid is.
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
        // NO context menu. It carried two tidy-up actions and it cost the tap:
        // a context menu installs a long-press recogniser over the whole card,
        // which delays every tap on it and makes a light one do nothing at all
        // (Hidde, 2026-08-25: "ik moet echt hard klikken om op a tree I found
        // te komen wat is dat probleem"). Both actions are reachable without
        // it: the heart removes a tree and now asks first, and un-ticking is
        // what the tree's own page is for. A hidden menu is a poor trade for a
        // card that does not respond to being touched.
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
                Text("You can collect it by photographing it while you stand there. Trees, species and places fill your collection, and the years they have seen add up.")
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
                Text("You can start your collection by photographing any tree. There are \(catalogue.trees.count.formatted(.number.locale(Locale(identifier: "en_US")))) of ours to find in \(Set(catalogue.trees.map(\.country)).count) countries, and any tree you photograph is yours whether we map it or not.")
                    .font(.subheadline).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
    }
}
