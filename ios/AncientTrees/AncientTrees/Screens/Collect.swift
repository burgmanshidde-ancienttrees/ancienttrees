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
import CoreLocation

struct CollectView: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    @Environment(Saved.self) private var saved
    @Environment(Account.self) private var account
    @Environment(Sightings.self) private var sightings
    @Environment(Navigator.self) private var navigator

    @State private var signingIn = false
    @State private var showAllStamps = false
    /// OPENS ON YOUR OWN TREES, not on the wishlist (Hidde, 2026-08-26: "ik
    /// zou daar op openen, niet op favourites"). The page is called My trees
    /// and the trees that are yours are the ones you photographed; a list of
    /// things you have not seen yet is the second question, not the first.
    @State private var lane: Lane = .seen
    /// Debug scaffolding, the same family as -tab and -contribute: the sweep
    /// cannot tap a gear, and a screen no argument can open is a screen that
    /// ships unlooked at.
    @State private var openSettings = ProcessInfo.processInfo.arguments.contains("-settings")
    @State private var editingProfile = ProcessInfo.processInfo.arguments.contains("-profile-edit")
    @State private var findingPeople = ProcessInfo.processInfo.arguments.contains("-people")
    @State private var sheetHeight: SheetHeight = .half
    @State private var selectedTree: Tree?
    @Environment(Profiles.self) private var profiles

    // TWO lanes, not three. "Collected" and "Added by you" were separate until
    // 2026-08-24, when Hidde gave the rule that dissolves the split: "je
    // collect de bomen die er zijn en je collect automatisch een boom als je
    // die toevoegt." A tree you added is collected by definition, so it belongs
    // in the same list as the ones you ticked off, newest first, with its own
    // photograph on it.
    enum Lane: Hashable { case want, seen }

    private var visited: [Tree] {
        saved.collected.compactMap { catalogue.tree($0.treeId) }
    }
    /// EVERY favourite, whether or not it has been stood in front of. The two
    /// lanes are independent lists and a tree may be in both (Hidde,
    /// 2026-08-26: "die dingen zijn twee verschillende lijsten en hebben niks
    /// met elkaar te maken"). This used to exclude anything visited, which is
    /// what made the heart and the collection look like one list in two
    /// states: photograph a tree you had hearted and it silently left your
    /// favourites.
    private var wishlist: [Tree] {
        saved.favourites.compactMap { catalogue.tree($0.treeId) }
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
        // THE SAME COMPONENT THE MAP SCREEN USES (Hidde, 2026-08-26: "ik wil
        // gewoon dezelfde interactie als op home ... je wilt deze interactie
        // als component hebben en overal hetzelfde hebben"). Everything about
        // how the map and the sheet behave together lives in MapWithSheet, so
        // this page cannot get it subtly different.
        MapWithSheet(height: $sheetHeight) {
            coverMap
        } header: {
            sheetHeader
        } content: {
            sheetBody
        } floating: {
            settingsButton.frame(maxWidth: .infinity, alignment: .trailing)
        }
        .brandGround()
        .toolbar(.hidden, for: .navigationBar)
        .task {
            if openSettings { openSettings = false; navigator.push = .profile }
        }
        .sheet(isPresented: $editingProfile) { ProfileEditor() }
        .sheet(isPresented: $findingPeople) { PeopleView() }
        .sheet(isPresented: $signingIn) {
            SignInSheet(reason: .keepCollection(saved.savedCount), localCount: saved.savedCount)
                .environment(account).environment(saved)
        }
    }

    /// Face and name, and NOTHING YOU CAN TAP. This is the grab handle, and a
    /// handle with controls in it is a handle you fight.
    ///
    /// It carried the numbers and the Add-a-tree button too, which put a
    /// 52-point green target and a tappable name in the one place this page is
    /// dragged from. Hidde has now reported that twice, first as the editor
    /// opening on a drag (2026-08-27: "als ik de slider gebruik opent het
    /// bewerken van je profiel veel te makkelijk") and then, after only the
    /// name was left tappable, as the same fault: "nog steeds kan ik niet
    /// lekker de lijst openen op my trees - de naam wijzigen knop overheerst".
    ///
    /// The convention answers it rather than another tuning pass. Polarsteps,
    /// Instagram and Strava all edit a profile from an EXPLICIT control, a gear
    /// or an Edit button, and none of them make the name itself the door. Ours
    /// is the gear in the corner, whose Settings screen has carried "Your name
    /// and picture" all along. So the name is text again, everything else moved
    /// into the list below, and the whole width of this row is grab.
    private var sheetHeader: some View {
        whoYouAre
            .padding(.horizontal, 20)
            .padding(.bottom, 12)
    }

    /// Your trees, and the picker that chooses which list.
    @ViewBuilder private var sheetBody: some View {
        VStack(alignment: .leading, spacing: 18) {
            // The numbers and the one thing you make scroll WITH the list, the
            // way they do on the page this is copied from. They sat in the
            // header, where they were both a wall between the name and the
            // list and a row of tap targets in the drag area.
            statsRow
            actionRow
            // YOUR OWN TREES COUNT AS HAVING STARTED. This asked only about
            // ours, so somebody whose whole collection is trees they
            // photographed themselves was told "your first tree is 1.3 km
            // away" directly under a row saying they have two (seen the moment
            // the map could show an own tree at all, 2026-08-27).
            if allVisited.isEmpty && saved.favourites.isEmpty
                && sightings.yoursOnly.isEmpty { mission }
            if !saved.entries.isEmpty || !sightings.yoursOnly.isEmpty {
                lanePicker
                laneContent
            }
            if !account.isSignedIn && saved.savedCount > 0 { backupBar }
            // The floating bar's own room is kept by the sheet now
            // (BottomSheet), so this is air at the end of a list rather than a
            // hole the size of a tab bar.
            Color.clear.frame(height: 24)
        }
        .padding(.horizontal, 20)
        .frame(maxWidth: .infinity, alignment: .leading)
    }

    /// The map under the sheet, and it MOVES: the same live map the map screen
    /// draws, not a snapshot, so panning and zooming work as they do
    /// everywhere else.
    @ViewBuilder private var coverMap: some View {
        let points = allVisited.map { (lat: $0.lat, lng: $0.lng) }
            + sightings.yoursOnly.map { (lat: $0.lat, lng: $0.lng) }
        if countries > 1 {
            GlobeMap(points: points)
        } else {
            TreeMap(trees: allVisited,
                    mine: sightings.yoursOnly.map {
                        (id: $0.id, lat: $0.lat, lng: $0.lng, name: $0.name,
                         photo: sightings.image($0)) },
                    collected: Set(saved.collected.map(\.treeId)),
                    favourites: Set(saved.favourites.map(\.treeId)),
                    onSelectMine: { navigator.push = .mine($0) },
                    onSelectTree: { navigator.push = .tree($0) },
                    focus: centreOfYours,
                    spanMeters: spanOfYours,
                    selected: $selectedTree)
        }
    }

    /// The middle of what you have, so the map opens on your collection.
    private var centreOfYours: CLLocationCoordinate2D? {
        let all = allVisited.map { (lat: $0.lat, lng: $0.lng) }
            + sightings.yoursOnly.map { (lat: $0.lat, lng: $0.lng) }
        // WHERE YOU ARE when you have nothing yet. Handing the map no focus
        // opened it on the whole Atlantic, which is a picture of nowhere; the
        // point of this map on an empty page is that it shows the streets your
        // first tree will appear in.
        guard !all.isEmpty else {
            return CLLocationCoordinate2D(latitude: origin.lat, longitude: origin.lng)
        }
        return CLLocationCoordinate2D(
            latitude: all.map(\.lat).reduce(0, +) / Double(all.count),
            longitude: all.map(\.lng).reduce(0, +) / Double(all.count))
    }

    private var spanOfYours: CLLocationDistance {
        let lats = allVisited.map(\.lat) + sightings.yoursOnly.map(\.lat)
        let lngs = allVisited.map(\.lng) + sightings.yoursOnly.map(\.lng)
        guard let loLat = lats.min(), let hiLat = lats.max(),
              let loLng = lngs.min(), let hiLng = lngs.max() else { return 3000 }
        let m = max((hiLat - loLat) * 111_000, (hiLng - loLng) * 111_000 * 0.62)
        return max(m * 1.4, 1200)
    }

    private var settingsButton: some View {
        Button { navigator.push = .profile } label: {
            Image(systemName: "gearshape")
                .font(.system(size: 18, weight: .medium))
                .foregroundStyle(Brand.ink)
                .frame(width: 44, height: 44)
                .background(.regularMaterial, in: .circle)
        }
        .buttonStyle(.plain)
        .padding(.trailing, 16)
        .accessibilityLabel("Settings")
        .accessibilityIdentifier("mytrees-settings")
    }

    /// The row Polarsteps runs under the numbers: the thing you make, wide and
    /// filled, and the way to find people beside it (Hidde, 2026-08-26: "doe
    /// voeg boom toe ook maar op dezelfde plek als bij polarsteps en daar dan
    /// naast die vriend uitnodigen knop").
    ///
    /// Theirs is a trip and ours is a tree, which is the same sentence: the
    /// one thing this page is a record of. The person button moved here out of
    /// the name row, where it had been sitting beside a pencil that has since
    /// gone, so the name row is now just the name.
    private var actionRow: some View {
        HStack(spacing: 12) {
            Button { navigator.collectNearby = true } label: {
                Label("Add a tree", systemImage: "camera.fill")
                    .font(.callout.weight(.semibold))
                    // A THREE WORD BUTTON MUST NOT BECOME "Add a tr...".
                    // Same cap as the counts and the stat row above, plus a
                    // little shrink, because a control that cannot say what it
                    // does is worse than one drawn slightly small.
                    .dynamicTypeSize(...DynamicTypeSize.accessibility1)
                    .lineLimit(1).minimumScaleFactor(0.7)
                    .foregroundStyle(Brand.ground)
                    .frame(maxWidth: .infinity)
                    .frame(height: 52)
                    .background(Brand.moss, in: .capsule)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("mytrees-add-tree")

            if account.isSignedIn {
                Button { findingPeople = true } label: {
                    Image(systemName: "person.badge.plus")
                        .font(.system(size: 18, weight: .medium))
                        .foregroundStyle(Brand.ink)
                        .frame(width: 52, height: 52)
                        .background(Brand.surface, in: .capsule)
                        .overlay { Capsule().strokeBorder(Brand.hairline, lineWidth: 1) }
                }
                .buttonStyle(.plain)
                .accessibilityLabel("Find people")
                .accessibilityIdentifier("mytrees-find-people")
            }
        }
    }






    private var oldBody: some View {
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
                    // "My trees", the same words as the tab, since 2026-08-26.
                    Text("My trees")
                        .font(.screenTitle)
                        .foregroundStyle(Brand.ink)
                    Spacer(minLength: 8)
                    // SETTINGS BEHIND A GEAR, top right, which is where
                    // Polarsteps puts it on the page about you and where iOS
                    // puts it everywhere (Hidde, 2026-08-26: "de my page
                    // krijgt zoals bij polarsteps een icoon rechtsboven voor
                    // je instellingen"). Profile stopped being a tab the same
                    // day: an account is something you visit twice a year, and
                    // a slot in a bar of three is the most expensive place in
                    // the app.
                    Button { navigator.push = .profile } label: {
                        Image(systemName: "gearshape")
                            .font(.system(size: 20, weight: .regular))
                            .foregroundStyle(Brand.ink)
                            .frame(width: 44, height: 44)
                            .contentShape(.rect)
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel("Settings")
                    .accessibilityIdentifier("mytrees-settings")
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
                    // YOUR OWN MAP, at the top, which is the shape Hidde asked
                    // for (2026-08-26: "de my trees pagina opbouwen als de my
                    // pagina van polarsteps"). Polarsteps opens the page about
                    // you with the globe carrying your own photographs, and
                    // the numbers sit under it: the picture answers "where
                    // have I been" before any figure does, and it is the only
                    // thing on the screen that is yours rather than ours.
                    //
                    // Ours is flat rather than a globe, because our collection
                    // is a walk across a city rather than a flight across the
                    // world, and a globe showing four trees in one park is a
                    // dot.
                    yourMap
                    whoYouAre
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
        .task {
            if openSettings { openSettings = false; navigator.push = .profile }
        }
        .sheet(isPresented: $editingProfile) {
            ProfileEditor()
        }
        .sheet(isPresented: $findingPeople) {
            PeopleView()
        }
        .sheet(isPresented: $signingIn) {
            SignInSheet(reason: .keepCollection(saved.savedCount), localCount: saved.savedCount)
                .environment(account).environment(saved)
        }
    }

    /// The lane picker, pinned. Opaque, because a pinned header with a clear
    /// background has the list sliding visibly underneath it.
    private var lanePicker: some View {
        Picker("", selection: $lane) {
            // "Favourites", not "Want to see" (Hidde, 2026-08-26: "dat zou ik
            // niet eens want to see noemen, ik zou het gewoon favorite trees
            // maken"). A heart is not a plan: people heart a tree they have
            // already seen and want to keep, which is exactly why the two
            // lists are independent now.
            // "My trees", not "Collected" (Hidde, 2026-08-26: "collected als
            // woord wordt my trees, en je voegt een boom toe aan je trees door
            // er een foto van te maken"). Collected described the mechanism;
            // his word describes what you end up with, and it is the same word
            // the tab wears, which is the point rather than a clash: this list
            // IS the page.
            Text("My trees").tag(Lane.seen)
            Text("Favourites").tag(Lane.want)
        }
        .pickerStyle(.segmented)
        .accessibilityIdentifier("collect-lane")
        .padding(.vertical, 10)
        // NO FILL BEHIND IT. It needed one while it was a pinned header on a
        // full-page scroller, with live content sliding under it. Inside the
        // sheet it is an ordinary row in the list, and the opaque ground
        // painted a white band across the sheet's own material.
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
                    SheetLink(route: .mine(s.id)) { MineCard(sighting: s) }
                }
            }
            let list = lane == .want ? wishlist : visited
            if list.isEmpty {
                Text(lane == .want
                     ? "No favourites yet. Tap a heart anywhere to keep a tree here."
                     : "You add a tree here by photographing it. Tap the camera and stand in front of one.")
                    .font(.subheadline).foregroundStyle(Brand.inkSoft)
                    .padding(.top, 4)
            } else {
                ForEach(list) { card($0, heart: lane == .want) }
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .id(lane)
    }

    // MARK: - the score

    /// The Polarsteps shape: the map of what you have done, then WHO, then the
    /// numbers (Hidde, 2026-08-26: "dat je daarboven een foto doet met de
    /// naam, precies zoals polarsteps opbouwt basically").
    ///
    /// WITH ONE HONEST GAP, and it is his rule rather than a limitation: an
    /// account here stores an email address and saves and NOTHING else, and a
    /// new column holding personal data needs his explicit yes (DECISIONS.md
    /// 2026-08-14). A profile photograph and a display name are both exactly
    /// that. So this is the shape with what we may hold: the initial of the
    /// address they signed in with, and the address itself, which is theirs
    /// and shown only back to them. The day he wants a real photograph and a
    /// name, it is a column, a bucket and a deletion duty, and it is his call.
    ///
    /// Followers are the other half of that reference and are not built:
    /// following is other people's data about each other, which is a bigger
    /// yes than this file may assume.
    @ViewBuilder private var whoYouAre: some View {
        HStack(spacing: 14) {
            let editable = account.isSignedIn
            // ONLY THE NAME IS TAPPABLE (Hidde, 2026-08-27: "als ik de slider
            // gebruik opent het bewerken van je profiel veel te makkelijk,
            // maak alleen de tekst van mijn naam klikbaar, want sliden doe je
            // veel vaker dan je naam bewerken").
            //
            // He is right about the ratio, and that is the whole argument: a
            // sixty-two point avatar plus a name plus two counts is most of the
            // width of the sheet's grab area, and it sat under the one gesture
            // this page gets constantly. A control's tap area should be
            // proportional to how often it is wanted, and this one is wanted
            // rarely.
            HStack(spacing: 14) {
                ZStack {
                    Circle().fill(Brand.moss.opacity(0.12))
                    if let url = profiles.me?.avatar_url, let u = URL(string: url) {
                        AsyncImage(url: u) { img in
                            img.resizable().aspectRatio(contentMode: .fill)
                        } placeholder: { Color.clear }
                        .clipShape(.circle)
                    } else if let e = profiles.me?.display_name ?? account.email, let first = e.first {
                        Text(String(first).uppercased())
                            .font(.brand(24, .black, relativeTo: .title2))
                            .foregroundStyle(Brand.moss)
                    } else {
                        Image(systemName: "person.fill")
                            .font(.system(size: 22))
                            .foregroundStyle(Brand.moss.opacity(0.6))
                    }
                }
                .frame(width: 62, height: 62)
    
                VStack(alignment: .leading, spacing: 0) {
                    // The part before the @ rather than the whole address
                    // truncated in the middle, which rendered as "burgma...ail.com"
                    // on his own phone and reads as a bug rather than as a name.
                    // Signed out it says what the page is.
                    // TAPPABLE, and inert while you drag. Not a Button: see
                    // tapUnlessDragged in BottomSheet.swift, which borrows what
                    // UIScrollView does for every row in iOS. A Button here
                    // fires on release even after a 40 point drag, because the
                    // row is the width of the sheet and the finger never
                    // leaves its bounds, and that is the whole complaint.
                    Text(editable
                         ? (profiles.me?.display_name
                            ?? account.email?.split(separator: "@").first.map(String.init)
                            ?? "Your trees")
                         : "Your trees")
                        .font(.brand(19, .bold, relativeTo: .title3))
                        .foregroundStyle(Brand.ink)
                        .lineLimit(1).truncationMode(.middle)
                        // A NAME IS 23 POINTS TALL and Apple's floor is 44.
                        .frame(minHeight: 44, alignment: .leading)
                        .tapUnlessDragged {
                            if editable { editingProfile = true } else { signingIn = true }
                        }
                        .accessibilityIdentifier("mytrees-edit-profile")
                        .accessibilityAddTraits(.isButton)
                        .accessibilityLabel(editable ? "Edit your profile" : "Sign in")
                    if account.isSignedIn {
                        // The two numbers Polarsteps runs beside the name. They
                        // are here from the first day rather than added later, so
                        // the page does not change shape on somebody the week
                        // following opens.
                        HStack(spacing: 14) {
                            Text("\(profiles.followers) followers")
                            Text("\(profiles.following) following")
                        }
                        .font(.caption).foregroundStyle(Brand.inkSoft)
                        // CAPPED, because two counts side by side cannot grow
                        // to five times their size and stay two counts. At the
                        // largest accessibility setting this read "0 followe...
                        // 0 follo..." (2026-08-27, found by running the whole
                        // app at that size). Capping a glanceable figure is
                        // what Apple does in its own compact stat rows; the
                        // stories and the page copy below scale all the way,
                        // which is where reading actually happens.
                        .dynamicTypeSize(...DynamicTypeSize.accessibility1)
                    } else {
                        Text("Sign in and your collection follows you.")
                            .font(.caption).foregroundStyle(Brand.inkSoft)
                    }
                }
            }
            Spacer(minLength: 0)
        }
        .accessibilityIdentifier("mytrees-who")
    }

    /// Every tree you have stood in front of, framed together.
    @ViewBuilder private var yourMap: some View {
        let points = allVisited.map { (lat: $0.lat, lng: $0.lng) }
            + sightings.yoursOnly.map { (lat: $0.lat, lng: $0.lng) }
        if !points.isEmpty {
            Button { navigator.selectTab = 0 } label: {
                CollectionMap(points: points)
                    .frame(height: 190)
                    .clipShape(.rect(cornerRadius: 16))
                    .overlay(alignment: .bottomLeading) {
                        Text(points.count == 1 ? "1 tree" : "\(points.count) trees")
                            .font(.caption.weight(.semibold))
                            .foregroundStyle(Brand.ink)
                            .padding(.horizontal, 10).padding(.vertical, 6)
                            .background(.regularMaterial, in: .capsule)
                            .padding(12)
                    }
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("mytrees-map")
            .accessibilityLabel("Your trees on the map")
        }
    }

    /// The numbers as the reference has them: bare on the sheet, separated by
    /// hairlines, no card around them (Hidde, 2026-08-26: "kijk goed naar die
    /// pagina van polarsteps en maak m na"). A card here made them read as a
    /// widget sitting ON your page; without it they read as facts ABOUT you,
    /// which is what they are and what Polarsteps gets right.
    private var statsRow: some View {
        VStack(spacing: 10) {
            HStack(spacing: 0) {
                tile("\(collectedCount)", "Trees")
                Divider().frame(height: 34)
                tile("\(collectedSpecies.count)", "Species")
                Divider().frame(height: 34)
                tile("\(countries)", countries == 1 ? "Country" : "Countries")
            }
            // Three figures across one row is a shape that cannot survive
            // unlimited growth: at the largest setting the labels became
            // "Specie" and "Coun-try" with the dividers gone and the list
            // pushed off the screen entirely. Same reasoning as the counts
            // above, same cap.
            .dynamicTypeSize(...DynamicTypeSize.accessibility1)
            // NO SENTENCE UNDER THE NUMBERS (Hidde, 2026-08-27: "delete out of
            // 1846 we map in 39 countries, it looks weird and the stat honestly
            // doesn't make much sense"). He is right twice: it measured US
            // rather than him, which is the wrong subject on the one page that
            // is about him, and a paragraph under a stat row is not what a stat
            // row is for. Polarsteps runs three numbers and nothing else.
        }
    }

    private var statsCard: some View {
        VStack(spacing: 14) {
            // THREE NUMBERS WITH DIVIDERS, which is the row Polarsteps runs
            // under the name (Hidde, 2026-08-26: "bij polarsteps heb je 51
            // landen en 21 volgers, daar zou je ook species collected kunnen
            // maken als een van die getallen", and then "na willen maken exact
            // zoals polarsteps dat doet").
            //
            // Cities left the row and kept its place in the sentence below.
            // Four numbers made each one small; the reference runs three and
            // that is why theirs reads at a glance. Species is in it on his
            // ask, and it is the right one to keep: a collector counts kinds,
            // not visits.
            //
            // FOLLOWERS BELONG IN THIS ROW and are not in it yet. Storing a
            // display name, a profile photograph and a follow graph is new
            // personal data about people, which is his explicit yes under the
            // accounts rule (DECISIONS.md 2026-08-14), and a followers count
            // that reads zero for a year makes an app look dead rather than
            // social. The row is built to take a fourth number the day both
            // of those change.
            HStack(spacing: 0) {
                tile("\(collectedCount)", "Trees")
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
            // One line that shrinks a little rather than a word broken across
            // two with a hyphen, which is what "Coun-try" was.
            Text(label).font(.caption2).foregroundStyle(Brand.inkSoft)
                .lineLimit(1).minimumScaleFactor(0.7)
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

    private func card(_ t: Tree, heart: Bool = true) -> some View {
        // SheetLink, not NavigationLink: this list lives in a sheet, and a
        // link there opens on release even when the drag that released it was
        // raising the sheet. See BottomSheet.swift.
        SheetLink(route: .tree(t.id)) {
            TreeCard(tree: t, showHeart: heart)
        }
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
                SheetLink(route: .tree(t.id)) { TreeCard(tree: t) }
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
