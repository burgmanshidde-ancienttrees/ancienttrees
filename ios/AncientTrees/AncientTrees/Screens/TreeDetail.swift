// One tree, and the two actions that matter under it.
//
// The action bar is pinned to the bottom and does not scroll away, which is the
// sharpest thing the AllTrails teardown found: their `Begin` is not merely under
// the elevation chart, it is fixed to the bottom of the phone everywhere the
// route exists. `directions` fired zero times on our website, where the button
// lives at the end of a story somebody has to scroll through.

import SwiftUI
import MapKit

struct TreeDetail: View {
    let tree: Tree
    /// Set when this page is showing a tree only YOU have. The same page, with
    /// the fields you have not filled in yet open for you to fill (Hidde,
    /// 2026-08-24: "het is dezelfde boom pagina als onze bomen alleen dan dat
    /// de eindgebruiker de velden kan invullen"). A second screen for your own
    /// trees would drift from this one inside a week.
    var mine: Sightings.Sighting? = nil
    let catalogue: Catalogue
    /// Where the phone thinks it is, for the walking view. Defaults to the
    /// tree itself, which is honest when nobody has given us a location: the
    /// line is then zero long rather than wrong.
    var origin: (lat: Double, lng: Double)? = nil
    @Environment(Saved.self) private var saved
    @Environment(Sightings.self) private var sightings
    @Environment(\.dismiss) private var dismiss
    @State private var editing: EditableField?
    @Environment(Account.self) private var account
    @Environment(Nudge.self) private var nudge
    @State private var reporting = false
    /// What the menu item they chose says, seeded into the report.
    @State private var reportOpening: String?
    @State private var placing = false

    private func report(_ opening: String) {
        reportOpening = opening
        reporting = true
    }
    @State private var removing = false
    @Environment(Navigator.self) private var navigator
    /// The hero shows the map instead of the photograph. A swap rather than a
    /// jump to the Map tab, so the reader keeps their place.
    @State private var showingMap = false
    @Environment(SaveCounts.self) private var saveCounts

    var body: some View {
        ZStack(alignment: .bottom) {
            ScrollView {
                // A RHYTHM, not one gap repeated (Hidde, 2026-08-26: "de
                // spacing op een detailpagina is helemaal vreselijk, kijk daar
                // eens naar conventies hoe je zo'n pagina opbouwt").
                //
                // It was a single VStack at 16 points, so the space between a
                // name and its species was the same as the space between two
                // unrelated sections, and a page where everything is equally
                // far apart has no hierarchy at all: the eye cannot tell what
                // belongs to what.
                //
                // Every reference builds one the same way. Airbnb's listing,
                // AllTrails' trail and Apple Maps' place all run the hero edge
                // to edge with no margin, group what belongs together tightly,
                // and put real air between sections. So: 28 between sections,
                // 10 inside a group, and the picture full bleed.
                VStack(alignment: .leading, spacing: 0) {
                    hero
                    VStack(alignment: .leading, spacing: 28) {
                    header
                    facts
                    // A TICKET IS THE FIRST THING TO KNOW (Hidde, 2026-08-26:
                    // "dat betaald is dermate belangrijk dat die informatie
                    // met datzelfde ticketje bovenaan moet staan, boven been
                    // here worth to visit"). It decides whether somebody sets
                    // off at all, so it belongs above the question of whether
                    // the tree was worth it, in the same warning shape the
                    // approximate pin uses. The access line further down keeps
                    // the detail and the transport stays where it is.
                    //
                    // The same blue as the pin's ticket mark, and not gold:
                    // gold means paid-by-us everywhere in this app, and
                    // sharing it made a garden's entrance fee read as one of
                    // our own tiers (2026-08-25).
                    if mine == nil, tree.paidEntry { ticketNote }
                    if tree.precision.needsWarning { approximateNote }
                    // High on the page, under the facts, because it is a
                    // question about the thing the facts just described
                    // (Hidde, 2026-08-21).
                    // Not on your own tree: a vote on whether YOUR tree is
                    // worth the visit is a question to nobody, and the access
                    // and transport lines are ours to research, not blanks for
                    // you to fill about a tree you already stood at.
                    if mine == nil { WorthItView(tree: tree) }
                    story
                    if mine == nil { accessBlock }
                    // The "Nobody has photographed this one" card is gone
                    // (Hidde, 2026-08-26: "die mag helemaal weg"). It was a
                    // paragraph explaining a control that now exists: the
                    // camera in the photograph's corner says the same thing by
                    // being a camera, on every tree, whether or not there is
                    // already a picture.
                    if mine != nil { mineFooter }
                    // "Report a problem" used to sit here and open the generic
                    // contribute form, which greeted somebody who wanted to
                    // report a wrong pin with a picker whose first row reads "A
                    // tree we are missing" and three empty fields asking which
                    // place and which tree (Hidde, 2026-08-25: "die flow loopt
                    // totaal niet"). It was also the second report control on
                    // one page: WorthItView above already carries "Something's
                    // wrong" and the five chips that name what is actually
                    // wrong, which is the flow the website runs and the one a
                    // run can act on. One page, one way to say it.
                    // Last line on the page, and only where the licence asks
                    // for it. CC BY and BY-SA oblige a credit; CC0 and public
                    // domain do not and get none. Moving it here is allowed
                    // ("in any reasonable manner"), removing it is not.
                    // WHERE TO GO NEXT, as the same facets Explore already
                    // browses by (Hidde, 2026-08-26: "onderaam de boom detail
                    // pagina discover more in city, park or country,
                    // verschillende knoppen, kijk naar deze conventie,
                    // categorien die je ook op explore hebt staan").
                    //
                    // The convention is a row of chips rather than a list of
                    // links: AllTrails closes a trail page with "Nearby trails"
                    // and its own facet pills, Google Maps closes a place with
                    // "More places nearby". A reading page that simply stops is
                    // a dead end, and this page had one.
                    if mine == nil { discoverMore }
                    if let p = tree.photo, let c = Photos.credit(p) {
                        Text(c)
                            .font(.system(size: 10))
                            .foregroundStyle(Brand.inkSoft.opacity(0.45))
                            .lineLimit(1)
                    }
                    Color.clear.frame(height: 90)   // room for the pinned bar
                    }
                    .padding(.horizontal, 20)
                    .padding(.top, 20)
                }
            }
            actionBar
        }
        .brandGround()
        // The name renders once, in the body's own heading; a second copy in
        // the bar was the "title twice" mess from the findings list.
        .navigationTitle("")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            // Only ours can be shared: a tree only you have has no address on
            // the web to send anybody to, and inventing one would send them to
            // a 404. It gets a share button the day these get a page.
            if mine == nil {
                    ShareTo(url: URL(string: "https://ancienttrees.app" + tree.url)!,
                        subject: tree.name,
                        message: "\(tree.name), \(tree.city).",
                        label: "Share this tree")
                // THE SAME ELLIPSIS ON OUR TREES (Hidde, 2026-08-26: "we hadden
                // daar rechtsboven drie puntjes bedacht waar je eigenlijk alle
                // feedback kon geven... goed om die ook te herhalen op de
                // algehele boompagina's die wij maken").
                //
                // The menu existed only on a tree you added yourself, so the
                // 1,840 trees where our own facts might be wrong had no way to
                // say so beyond a thumbs down. That is backwards: readers are
                // the correction layer on this whole project, and the pages
                // that most need correcting are ours.
                //
                // Same glyph, same place, different verbs. Nothing here edits
                // anything, because these are not the reader's trees to edit:
                // every item opens the report we already have, prefilled with
                // this tree, which is the channel Step 0b already processes.
                // A GAP THAT SPLITS THE GLASS. iOS 26 gathers trailing toolbar
                // items into one capsule, so share and report shared a pill
                // while the back button and the camera on the photograph each
                // wore their own circle. Three controls on one screen drawn
                // two different ways is the inconsistency he saw. A
                // ToolbarSpacer is the platform's own way to break the group,
                // and it lands on the convention every reference uses over a
                // hero image: one round button per control, evenly spaced.
                // Guarded, because this app runs from iOS 18 and the spacer
                // arrived in 26. On 18 there is nothing to split: that older
                // toolbar draws no glass around a group, so the two controls
                // already read as two.
                // TWO GUARDS, not one, and the second is the one that was
                // missing. `#available` decides whether a device may RUN this;
                // the symbol still has to EXIST when it compiles, and the SDK
                // that has it ships with Xcode 26. This desk has that and the
                // CI runner has Xcode 16.4, so the gate could not build what
                // was written here (2026-08-26).
                #if compiler(>=6.2)
                if #available(iOS 26.0, *) {
                    ToolbarSpacer(.fixed, placement: .topBarTrailing)
                }
                #endif
                ToolbarItem(placement: .topBarTrailing) {
                    Menu {
                        Button { report("Something here is wrong:") } label: {
                            Label("Something is wrong here", systemImage: "exclamationmark.bubble")
                        }
                        Button { report("The pin is in the wrong place.") } label: {
                            Label("The pin is in the wrong place", systemImage: "mappin.slash")
                        }
                        Button { report("I could not tell which tree it was.") } label: {
                            Label("I could not tell which tree", systemImage: "questionmark.circle")
                        }
                        Button { report("This tree is gone.") } label: {
                            Label("This tree is gone", systemImage: "xmark.seal")
                        }
                    } label: {
                        // A REPORT ICON, not three dots (Hidde, 2026-08-26:
                        // "de drie puntjes moeten een report icoon worden").
                        // He is right that the glyph was lying about the menu:
                        // an ellipsis promises "more of the usual" and every
                        // item under this one is a way of telling us something
                        // is wrong. Apple's own Report a Concern uses this
                        // symbol, so it is the convention rather than a pick.
                        // The menu on a tree somebody added themselves keeps
                        // its ellipsis, because that one really is edit and
                        // remove.
                        // Sized by the toolbar, not by us: see ShareTo.swift
                        // for why a hand-rolled 44 point box inside a toolbar
                        // item is what pushed these two apart.
                        Image(systemName: "exclamationmark.bubble")
                            .font(.system(size: 17, weight: .semibold))
                    }
                    .accessibilityIdentifier("ours-menu")
                    .accessibilityLabel("Report a problem")
                }
            } else {
                // AN ELLIPSIS, TOP RIGHT, which he asked me to check rather
                // than assume (Hidde, 2026-08-25: "is het niet meer conventie om
                // 3 puntjes rechtsboven te doen en dan allerlei aanpas en
                // verwijder opties te geven? not sure check it please").
                //
                // It is. Photos, Notes, Files and Apple Maps all keep "what else
                // can I do to this thing" behind `ellipsis.circle` in the
                // navigation bar, and all of them put the destructive item last
                // and marked, behind a confirmation. So this is that menu and
                // nothing invented: the three fields you can fill, then Remove.
                //
                // Removing was not possible at all before this. A tree you added
                // could be edited and never taken back, which for a photograph
                // of your own garden is the wrong way round.
                ToolbarItem(placement: .topBarTrailing) {
                    Menu {
                        Button { editing = .name } label: {
                            Label("Change the name", systemImage: "pencil")
                        }
                        Button { editing = .species } label: {
                            Label("Change the species", systemImage: "leaf")
                        }
                        Button { editing = .age } label: {
                            Label("Change the age", systemImage: "calendar")
                        }
                        Button { placing = true } label: {
                            Label("Move the pin", systemImage: "mappin.and.ellipse")
                        }
                        Divider()
                        Button(role: .destructive) { removing = true } label: {
                            Label("Remove this tree", systemImage: "trash")
                        }
                    } label: {
                        Image(systemName: "ellipsis.circle")
                            .font(.system(size: 17, weight: .semibold))
                    }
                    .accessibilityIdentifier("mine-menu")
                    .accessibilityLabel("More")
                }
            }
        }
        .confirmationDialog("Remove \(tree.name) from your trees?",
                            isPresented: $removing, titleVisibility: .visible) {
            Button("Remove", role: .destructive) {
                if let m = mine {
                    sightings.remove(m.id)
                    dismiss()
                }
            }
            Button("Keep it", role: .cancel) {}
        } message: {
            Text("Your photograph goes with it. What you have already sent us stays sent.")
        }
        .sheet(isPresented: $reporting) {
            ContributeView(about: tree, opening: reportOpening)
        }
        .fullScreenCover(isPresented: $placing) {
            // Full screen, because the job is to find one trunk on a map and a
            // sheet would give it half a phone to do it in.
            PlacePin(tree: tree, catalogue: catalogue)
                .environment(account)
        }
        .sheet(item: $editing) { editor($0) }
        .task {
            // Debug scaffolding, same family as -tab, -select and -collected:
            // simctl cannot tap, and a screen that only exists after a tap is a
            // screen that ships unlooked at.
            // A screen no argument can open is a screen that ships unseen
            // (CLAUDE.md), so the pin picker gets its argument in the same
            // commit as the picker.
            if ProcessInfo.processInfo.arguments.contains("-placepin") { placing = true }
        }
    }

    /// The photograph, or the species drawn, edge to edge. AllTrails leads every
    /// route with a picture and it is most of why their pages feel like an
    /// invitation rather than a database record.
    ///
    /// The credit sits UNDER it rather than painted across it.
    ///
    /// This is the only place the attribution appears now, which is deliberate:
    /// cards stopped carrying it on 2026-08-20 because a dark chip over the
    /// trunk is the one thing on a card that is not the tree. A CC BY or BY-SA
    /// licence obliges a credit and this is it, in the ordinary place a caption
    /// goes, which is also what every image search and Wikipedia's own apps do.
    @ViewBuilder private var hero: some View {
        if showingMap {
            // The swap's other face: the same box, the same corners, the map
            // where the photograph was, and the photograph's own thumbnail in
            // the corner to swap back. One control, two directions.
            Color.clear
                .frame(height: 300)
                .overlay {
                    MapInset(lat: tree.lat, lng: tree.lng, side: nil, height: 240)
                }
                .clipped()
                .overlay(alignment: .bottomTrailing) {
                    // THE SAME CONTROL, POINTING THE OTHER WAY (Hidde,
                    // 2026-08-26: "dan wil je die actie om terug te gaan naar
                    // de foto precies dezelfde UI geven als hoe de map wordt
                    // getoond op de foto, en dan met een preview van de foto
                    // als je die hebt"). A rounded thumbnail in the corner
                    // going one way and a round icon coming back is two
                    // controls for one swap; the same shape both ways says
                    // "these two trade places", which is the whole idea.
                    Button { withAnimation(.easeInOut(duration: 0.22)) { showingMap = false } } label: {
                        photoInset.padding(10)
                    }
                    .buttonStyle(.plain)
                    .accessibilityIdentifier("tree-photo-swap")
                    .accessibilityLabel("Show the photograph again")
                }
                .overlay(alignment: .topTrailing) {
                    // The way to the FULL map is still here, because seeing it
                    // in the corner of a page and standing on it are different
                    // needs.
                    Button { navigator.push = .treeMap(tree.id) } label: {
                        Image(systemName: "arrow.up.left.and.arrow.down.right")
                            .font(.system(size: 14, weight: .semibold))
                            .foregroundStyle(Brand.ink)
                            .frame(width: 44, height: 44)
                            .background(.regularMaterial, in: .circle)
                            .padding(10)
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel("Open the full map")
                }
        } else if let m = mine, let shot = sightings.image(m) {
            // Your own photograph, from Documents rather than the network. The
            // same empty box with the picture laid over it as below, for the
            // same reason: an unbounded image drags the whole page sideways.
            Color.clear
                .frame(height: 300)
                .overlay {
                    Image(uiImage: shot).resizable().aspectRatio(contentMode: .fill)
                }
                .clipped()
        } else if let p = tree.photo, let url = p.full {
            VStack(alignment: .leading, spacing: 6) {
                // AN EMPTY BOX WITH THE PHOTOGRAPH LAID OVER IT, not a
                // photograph with a height. A .fill image asks for the width
                // its own picture wants (a landscape shot 240 points tall asks
                // for about 410) and everything around it grows to match: on a
                // 375 point phone the whole tree page sat 19.5 points to the
                // left, the photograph against the left edge and the heart
                // button hanging off the right. One unbounded image moved every
                // element on the screen, and adding maxWidth did not fix it,
                // because a frame's maximum still yields to the image's ideal.
                // An overlay never takes part in layout at all, which is the
                // only version that cannot do this again.
                Color.clear
                    .frame(height: 300)
                    .overlay {
                        AsyncImage(url: url) { img in
                            img.resizable().aspectRatio(contentMode: .fill)
                        } placeholder: {
                            heroFallback
                        }
                    }
                    .clipped()
                    // The way to the map, in the corner a card already trained
                    // people to look at. It replaces the 150 point map card
                    // that used to sit between the facts and the story and
                    // pushed the whole story below the fold.
                    .overlay(alignment: .bottomTrailing) {
                        // THE TWO SWAP PLACES (Hidde, 2026-08-26: "als je de
                        // kleine map icoon aantikt dan wordt de grote foto de
                        // map, en dan kan je dit heen en weer klikken"). It
                        // used to leave the page for the Map tab, which threw
                        // away where you were reading; a swap keeps you on the
                        // tree and answers the same question. Airbnb does this
                        // exact thing with its photo and its map.
                        Button { withAnimation(.easeInOut(duration: 0.22)) { showingMap.toggle() } } label: {
                            MapInset(lat: tree.lat, lng: tree.lng).padding(10)
                        }
                        .buttonStyle(.plain)
                        .accessibilityIdentifier("tree-map-swap")
                        .accessibilityLabel("Show this tree on the map")
                    }
                    .overlay(alignment: .topLeading) { addPhotoButton }

            }
        } else {
            // The whole empty frame is the door to the camera, on a tree of
            // ours that nobody has photographed (Hidde, 2026-08-26). The map
            // inset stays on top of it and keeps its own tap, so the corner
            // still goes to the map rather than to the camera.
            Button {
                if mine == nil { navigator.collectNearby = true }
            } label: {
                heroFallback.frame(height: 300)
            }
            .buttonStyle(.plain)
            .disabled(mine != nil)
            .accessibilityIdentifier("tree-empty-photo")
            .accessibilityLabel(mine == nil ? "Add a photograph of this tree" : "No photograph")
            .overlay(alignment: .bottomTrailing) {
                // SWAPS IN PLACE, the same as on a tree that has a photograph
                // (Hidde, 2026-08-26: "nu is de interactie weer dat je van dat
                // kaartje naar de map pagina gaat, maar je wilt dat je in
                // discover blijft maar wel een kaartje opent"). This one still
                // handed you to the Map tab, which is the behaviour the other
                // branch lost an hour ago; a photograph-less tree is not a
                // reason to throw away where somebody was reading.
                Button { withAnimation(.easeInOut(duration: 0.22)) { showingMap.toggle() } } label: {
                    MapInset(lat: tree.lat, lng: tree.lng).padding(10)
                }
                .buttonStyle(.plain)
                .accessibilityLabel("Show this tree on the map")
            }
            .overlay(alignment: .topLeading) { addPhotoButton }
        }
    }

    /// The way onward, in the reader's own widening circles: this city, the
    /// park it stands in when it has one, its species, its country. Every one
    /// of these is a page Explore already offers, so nothing new is invented
    /// and nothing is a dead end.
    @ViewBuilder private var discoverMore: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Discover more")
                .font(.brand(18, .bold, relativeTo: .headline))
                .foregroundStyle(Brand.ink)
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 8) {
                    discoverChip(tree.city, "building.2") { navigator.push = .city(tree.citySlug) }
                    // No park chip: a tree carries no park and Route has no
                    // park case, so the parks facet lives on the website only.
                    // Inventing one here would mean guessing which park a set
                    // of coordinates sits in, which is the kind of bridge
                    // claim this project has a rule against.
                    // The species chip moved up into the facts row on
                    // 2026-08-26; what is left here are the wider circles.
                    ForEach(collectionsWithThisTree, id: \.slug) { c in
                        discoverChip(c.title, "square.stack") {
                            navigator.push = .collection(c.slug)
                        }
                    }
                    if !tree.country.isEmpty {
                        discoverChip(tree.country, "globe.europe.africa") {
                            navigator.push = .country(tree.country)
                        }
                    }
                }
            }
        }
        .padding(.top, 4)
    }

    /// The curated lists this tree is actually in (Hidde, 2026-08-26: "in
    /// Discover More kan je dus ook collecties toevoegen, zoals de oudste
    /// bomen waar die in toegevoegd is"). Read from the website's own
    /// collections rather than worked out here, so a tree appears in the list
    /// the site says it is in and nowhere else.
    private var collectionsWithThisTree: [TreeCollection] {
        catalogue.collections.filter { $0.trees.contains(tree.id) }
    }

    private func discoverChip(_ title: String, _ symbol: String,
                              _ go: @escaping () -> Void) -> some View {
        Button(action: go) {
            HStack(spacing: 6) {
                Image(systemName: symbol).font(.caption)
                Text(title).font(.subheadline.weight(.medium)).lineLimit(1)
            }
            .foregroundStyle(Brand.ink)
            .padding(.horizontal, 14)
            .frame(height: 44)
            .background(Capsule().fill(Brand.moss.opacity(0.10)))
            .contentShape(.capsule)
        }
        .buttonStyle(.plain)
    }

    /// The tree, and whatever else of ours is within a few streets, because the
    /// second most useful thing after "where is it" is "is it worth the trip on
    /// its own or are there three more round the corner".
    private var nearbyTrees: [Tree] {
        catalogue.nearest(to: tree.lat, tree.lng, limit: 8, withinKm: 0.5).map(\.tree)
    }

    /// The empty photograph, and it is deliberately QUIET (Hidde, 2026-08-26:
    /// "deze manier van een plaatje tonen en een knop is compleet weird").
    ///
    /// It was a green gradient carrying white text and a floating map inset,
    /// which is a poster where a placeholder belongs. Every reference does the
    /// dull thing: Google Maps, Apple Maps and Yelp all show a neutral grey
    /// panel with one small glyph, and the way to add a picture is the camera
    /// button in the corner rather than a sentence in the middle.
    private var heroFallback: some View {
        ZStack {
            Brand.surfaceMuted
            VStack(spacing: 10) {
                SpeciesMark(species: tree.species, color: Brand.inkSoft.opacity(0.35))
                    .frame(width: 64, height: 64)
                // TAPPABLE, because the empty frame is the most obvious place
                // to offer one (Hidde, 2026-08-26: "als er geen foto is kan je
                // uberhaupt de hele foto aanklikken in de detail pagina en
                // vanuit daar het veranderen"). The words say so rather than
                // leaving it to be discovered.
                // Two short lines rather than one long one, and kept clear of
                // the map inset that sits in the bottom right corner: at 375
                // points the single sentence ran straight under it and read as
                // "Tap to add you" (seen on the sweep, 2026-08-26).
                Text("No photograph yet")
                    .font(.caption).foregroundStyle(Brand.inkSoft)
            }
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(tree.name)
                .font(.brand(30, .bold, relativeTo: .largeTitle))
                .foregroundStyle(Brand.ink)
            if tree.species.isEmpty, mine != nil {
                blank("What kind of tree is it?", .species)
            } else {
                // The FULL name, botanical and all, stays here as the caption
                // it always was; the short common name is the tappable fact
                // in the row below, since 2026-08-26. Two doors to the same
                // page a centimetre apart is one door too many, and the
                // caption is the one that carries the Latin.
                Text(tree.species).font(.subheadline).foregroundStyle(Brand.inkSoft)
            }
            // HOW MANY PEOPLE KEPT IT, and only once somebody has (Hidde,
            // 2026-08-26: "aantal likes tellen en terug geven, pas van 1
            // tellen"). A zero on a page is worse than nothing: it says
            // nobody wanted this, about a tree we chose to publish. The count
            // comes from the server, because a phone can only see its own
            // saves; until the SQL behind it exists there is simply no number.
            if mine == nil, let n = saveCounts.count(tree.id) {
                Label(n == 1 ? "1 person keeps this tree"
                             : "\(n) people keep this tree",
                      systemImage: "heart.fill")
                    .font(.caption)
                    .foregroundStyle(Brand.inkSoft)
                    .accessibilityIdentifier("tree-save-count")
            }
            // WHERE it is, with the width of the page to say it in.
            //
            // It used to be the middle column of the stat row, where "Plantage,
            // Amsterdam-Centrum" became "Plantage, Amsterdam-C..." A stat row
            // holds numbers: AllTrails puts length, ascent and time in theirs,
            // and a place name is a phrase, not a number.
            if mine != nil {
                // Where YOU stood. No district, no city, because nobody has
                // told us one and inventing it is the one thing a location
                // field may never do.
                Text("Where you photographed it")
                    .font(.subheadline).foregroundStyle(Brand.inkSoft)
            } else {
                Text(place).font(.subheadline).foregroundStyle(Brand.inkSoft)
                    .lineLimit(1)
            }
        }
    }

    private var place: String {
        let n = tree.neighbourhood.trimmingCharacters(in: .whitespaces)
        guard !n.isEmpty else { return tree.city }
        // Many registers write the district as "Amsterdam-Centrum", so adding
        // the city gives "Plantage, Amsterdam-Centrum, Amsterdam".
        return n.localizedCaseInsensitiveContains(tree.city) ? n : "\(n), \(tree.city)"
    }

    /// Four facts with their units labelled, the way AllTrails does it and the
    /// way our own website already does on a tree page.
    /// The number, where the feed has one, so the row holds a figure rather
    /// than a hedged sentence. The full wording is in the story.
    private var shortAge: String {
        if let lo = tree.ageMin, lo > 0 {
            if let hi = tree.ageMax, hi > lo { return "\(lo)-\(hi) years" }
            return "\(lo) years"
        }
        return tree.age ?? (mine != nil ? "Add it" : "not recorded")
    }

    private var facts: some View {
        HStack(alignment: .top, spacing: 0) {
            if mine != nil, tree.age == nil {
                Button { editing = .age } label: { fact("Add it", "Age") }
                    .buttonStyle(.plain)
            } else {
                fact(shortAge, "Age")
            }
            Divider().frame(height: 34)
            // THE SPECIES SITS WITH THE FACTS (Hidde, 2026-08-26: "die Wild
            // Olive, die dermate belangrijk is, onderdeel maken van helemaal
            // bovenin, naast hoe oud die is en of de pin exact is"). It was a
            // chip at the bottom among the ways onward, which is where you
            // put a thing somebody might browse to next; what kind of tree it
            // is belongs with how old it is, because it is the same kind of
            // answer. It stays tappable, so it is still the door to the
            // species page.
            Button { navigator.push = .species(tree.commonName) } label: {
                fact(tree.commonName, "Species", chevron: true)
            }
            .buttonStyle(.plain)
            // On the BUTTON, not on its label: the label's own frame does not
            // give the button a hit area, which is why the gate still read
            // 42 by 34 after the first attempt.
            .frame(minHeight: 44)
            .contentShape(.rect)
            .accessibilityIdentifier("tree-species-fact")
            Divider().frame(height: 34)
            fact(tree.precision == .confirmed ? "Exact" : "Approximate", "Pin")
        }
        .padding(.vertical, 14)
        .frame(maxWidth: .infinity)
        .brandCard(14)
    }

    private func fact(_ value: String, _ label: String,
                      chevron: Bool = false) -> some View {
        // Leading, not centred: a centred value starts wherever its width
        // puts it, so "up to 1,500 years" sat seven points right of the card
        // edge and the layout gate read it as a drift. The fourteen matches
        // the card's own inset elsewhere on the page.
        VStack(alignment: .leading, spacing: 3) {
            HStack(spacing: 3) {
                Text(value).font(.brand(14, .bold, relativeTo: .footnote))
                    .foregroundStyle(Brand.ink).multilineTextAlignment(.leading)
                    .lineLimit(2).minimumScaleFactor(0.8)
                if chevron {
                    Image(systemName: "chevron.right")
                        .font(.system(size: 9, weight: .semibold))
                        .foregroundStyle(Brand.inkSoft)
                }
            }
            Text(label).font(.caption2).foregroundStyle(Brand.inkSoft)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(.horizontal, 14)
    }

    // oneTreeWalk() went with the in-app walk to a single tree (2026-08-25).
    // WalkMode still takes `only:` for a caller that holds its own stops, which
    // is how a walk to a tree somebody added themselves would work.

    /// One sheet for every blank, because four sheets that differ by a
    /// placeholder is four places for them to drift apart.
    private func editor(_ field: EditableField) -> some View {
        FieldEditor(field: field,
                    initial: current(field),
                    onSave: { text in
                        guard let m = mine else { return }
                        switch field {
                        case .name: sightings.update(m.id, name: text)
                        case .species: sightings.update(m.id, species: text)
                        case .age: sightings.update(m.id, age: text)
                        case .story: sightings.update(m.id, note: text)
                        }
                        editing = nil
                    },
                    onCancel: { editing = nil })
    }

    private func current(_ field: EditableField) -> String {
        switch field {
        case .name: tree.name
        case .species: tree.species
        case .age: tree.age ?? ""
        case .story: tree.story
        }
    }

    /// A field on your own tree that nobody has filled in yet.
    enum EditableField: String, Identifiable {
        case name, species, age, story
        var id: String { rawValue }

        var prompt: String {
            switch self {
            case .name: "What do you call it?"
            case .species: "What kind of tree is it?"
            case .age: "How old is it, roughly?"
            case .story: "What makes it worth the walk?"
            }
        }

        /// Long answers get room; a species or an age is one line.
        var long: Bool { self == .story }
    }

    /// An empty field, offered rather than hidden. The green says it is
    /// yours to fill; a grey dash would read as missing data on our side.
    private func blank(_ label: String, _ field: EditableField) -> some View {
        Button { editing = field } label: {
            HStack(spacing: 5) {
                Image(systemName: "plus.circle")
                Text(label)
            }
            .font(.subheadline)
            .foregroundStyle(Brand.moss)
            .frame(minHeight: 44)
            .contentShape(.rect)
        }
        .buttonStyle(.plain)
    }

    /// The one warning this product must never soften. An approximate pin that
    /// says so sends somebody to the right park knowing they will have to look;
    /// one that pretends to be exact sends them to a spot where the tree is not.
    /// The blue the pin's own ticket mark wears.
    private static let ticketBlue = Color(red: 0.18, green: 0.42, blue: 0.66)

    private var ticketNote: some View {
        Label {
            VStack(alignment: .leading, spacing: 3) {
                Text("You need a ticket to see this tree")
                    .font(.footnote.weight(.semibold))
                if !tree.access.isEmpty {
                    Text(tree.access).font(.footnote)
                }
            }
        } icon: {
            Image(systemName: "ticket.fill")
                .foregroundStyle(Self.ticketBlue)
        }
        .foregroundStyle(Brand.ink)
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(12)
        .background(Self.ticketBlue.opacity(0.10), in: .rect(cornerRadius: 12))
        .accessibilityIdentifier("tree-ticket-note")
    }

    private var approximateNote: some View {
        VStack(alignment: .leading, spacing: 8) {
            Label {
                Text("This pin marks the area, not the trunk. You may have to look around once you are there.")
            } icon: {
                Image(systemName: "scope")
            }
            .font(.footnote)
            // The ask belongs here rather than three screens away: the person
            // reading this line is the one person who can answer it, and
            // location is the field this project cannot afford to get wrong.
            // THE MAP, not a form (Hidde, 2026-08-25: "help us place this tree
            // opens a form, but i guess the easiest would be if you open the
            // map and let someone drop / move a pin"). It used to open the
            // contribute sheet, which asked the one person who can see the
            // trunk to describe its position in a sentence.
            Button { placing = true } label: {
                Text("Show us where it is")
                    .font(.footnote.weight(.semibold))
                    .foregroundStyle(Brand.moss)
                    .frame(minHeight: 44)
                    .contentShape(.rect)
            }
            .buttonStyle(.plain)
        }
        .padding(12)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color.orange.opacity(0.12), in: .rect(cornerRadius: 10))
    }

    /// Whole, always. It used to stop at six lines behind a "read the whole
    /// story" button, which is a paywall made of nothing: the story IS the
    /// page, and with the map card gone there is room for it (Hidde,
    /// 2026-08-21: "your text can go up, so you can put the whole story there
    /// instead of putting that behind the button").
    private var story: some View {
        Group {
            if tree.story.isEmpty, mine != nil {
                blank("What makes it worth the walk?", .story)
            } else {
                Text(tree.story)
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
    }

    /// What happens to a tree you added, said plainly on its own page.
    ///
    /// There is no CHOICE about it any more (Hidde, 2026-08-24: "hij komt
    /// uberhaupt automatisch bij ons terecht of ze het willen of niet en dan
    /// kiezen wij of die het waard is"), so the honest thing is to say so here
    /// rather than to ask twice.
    @ViewBuilder private var mineFooter: some View {
        if let m = mine {
            HStack(alignment: .top, spacing: 8) {
                Image(systemName: m.status == .published ? "checkmark.seal" : "leaf")
                    .foregroundStyle(Brand.moss)
                Text(m.status == .published
                     ? "This one made the map everybody sees."
                     // His own sentence, verbatim (2026-08-25). What it
                     // replaced said "This tree is yours. We have it too",
                     // which reads as a boast about our own database at the
                     // moment somebody has just given us something, and it
                     // never said what happens next. The reader is the subject
                     // here and the next step is named.
                     : "You've added this tree. We're taking a look at it, and once it's verified, we will add it to our map.")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
            }
            .padding(.top, 2)
        }
    }

    private var accessBlock: some View {
        VStack(alignment: .leading, spacing: 10) {
            Label(tree.access, systemImage: "figure.walk")
            Label(tree.transport, systemImage: "tram.fill")
        }
        .font(.footnote)
        .foregroundStyle(.secondary)
    }

    /// The highest-intent moment there is for this feature: you are on a tree
    /// with no photograph, and 1077 of our 1435 trees are in that state. Asking
    /// here beats a row in settings, and it measures demand for the feature
    /// exactly where somebody would use it.
    /// The photograph as a thumbnail, drawn exactly as MapInset draws the map:
    /// 72 points, a 10 point radius, a white edge and a soft shadow. When
    /// there is no photograph it shows the species mark on the muted surface,
    /// which is what the page shows full size in that case.
    @ViewBuilder private var photoInset: some View {
        Group {
            if let m = mine, let shot = sightings.image(m) {
                Image(uiImage: shot).resizable().aspectRatio(contentMode: .fill)
            } else if let p = tree.photo, let url = p.card {
                AsyncImage(url: url) { img in
                    img.resizable().aspectRatio(contentMode: .fill)
                } placeholder: { Brand.surfaceMuted }
            } else {
                ZStack {
                    Brand.surfaceMuted
                    SpeciesMark(species: tree.species, color: Brand.inkSoft.opacity(0.5))
                        .frame(width: 30, height: 30)
                }
            }
        }
        .frame(width: 72, height: 72)
        .clipShape(.rect(cornerRadius: 10))
        .overlay { RoundedRectangle(cornerRadius: 10).strokeBorder(.white.opacity(0.9), lineWidth: 2) }
        .shadow(color: .black.opacity(0.18), radius: 4, y: 2)
    }

    /// The camera, in the corner of the photograph, on every tree of ours and
    /// in the same place whether or not there is a picture already (Hidde,
    /// 2026-08-26: "die knop moet overal gelijk zijn"). Google Maps and Apple
    /// Maps both hang it on a place's image header exactly like this; a
    /// control that moves or disappears is one nobody learns to look for.
    @ViewBuilder private var addPhotoButton: some View {
        // ONLY WHERE THERE IS NO PHOTOGRAPH (Hidde, 2026-08-26: "de camera-
        // actie links bovenin die foto moet alleen staan als er nog geen foto
        // is"). On a tree that already has one it was a second camera two
        // centimetres from the one in the bar, and the bar is where he wants
        // the act promoted.
        if mine == nil, tree.photo == nil {
            Button { navigator.collectNearby = true } label: {
                Image(systemName: "camera.fill")
                    .font(.system(size: 15, weight: .semibold))
                    .foregroundStyle(Brand.ink)
                    .frame(width: 44, height: 44)
                    .background(.regularMaterial, in: .circle)
                    .padding(10)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("tree-add-photo")
            .accessibilityLabel("Add a photograph of this tree")
        }
    }

    private var actionBar: some View {
        HStack(spacing: 10) {
            // The hand-off, and it is a REVERSAL of 2026-08-24, when this
            // button was pointed at our own walk screen because "waarom stuurt
            // ie je dan naar een andere app als je in de app kan navigeren".
            // Both readings are his and the second one is about the case rather
            // than the principle: a walk of nine stops is ours to run, a single
            // tree is a destination and maps apps do destinations.
            // STRAIGHT TO MAPS for a single tree (Hidde, 2026-08-25: "just let
            // people open google maps directly for now, as mvp its fine until we
            // build the whole location for ourselves"). It opened our own walk
            // screen, which is right for a walk of nine stops in a city and
            // absurd for one tree seventeen kilometres away: a route with one
            // destination and nothing to string together is what every maps app
            // already does better than we will for a long time.
            //
            // Our walk screen keeps the multi-stop case, which is where the live
            // routing built earlier today belongs anyway.
            // "Take me there" while it is alone, "Take me" once the photo
            // button stands beside it: three controls at 375 points wrapped
            // the label onto two lines, which reads as a layout fault rather
            // than as a short word (seen on the sweep, 2026-08-26).
            Button { Directions.walk(lat: tree.lat, lng: tree.lng) } label: {
                Label("Take me there", systemImage: "arrow.turn.up.right")
                    .lineLimit(1)
            }
            .buttonStyle(BrandButtonStyle())

            // NO photo button here. It lived beside "Take me there" for an
            // hour and only on trees without a picture, and Hidde was right
            // about both halves (2026-08-26: "add a photo staat nu bij bomen
            // die geen foto hebben, maar dat moet hetzelfde zijn als bomen die
            // wel een foto hebben, die knop moet overal gelijk zijn"). A
            // control that appears and disappears is a control nobody learns,
            // and anybody may photograph any tree.
            //
            // It sits on the photograph instead, in the corner, always. That
            // is the convention rather than a choice: Google Maps and Apple
            // Maps both hang the camera on the image header of a place, in the
            // same corner, whether the place has pictures or not.
            // THE MAIN ACT, on every tree page (Hidde, 2026-08-26: "op alle
            // detailpagina's moet rechts van het hartje die camera staan, want
            // de main actie die we overal willen promoten is dat mensen foto's
            // maken"). Same circle as the heart, same size, same border: two
            // things you can do to a tree, drawn as two of the same control.
            if mine == nil {
                Button { navigator.collectNearby = true } label: {
                    Image(systemName: "camera")
                        .font(.title3)
                        .foregroundStyle(Brand.moss)
                        .frame(width: 52, height: 52)
                        .background(Brand.surface, in: .circle)
                        .overlay { Circle().strokeBorder(Brand.hairline, lineWidth: 1) }
                }
                .buttonStyle(.plain)
                .accessibilityIdentifier("tree-add-photo-bar")
                .accessibilityLabel("Photograph this tree")
            }
            SaveHeart(tree: tree, look: .inBar)
        }
        // The same 20 as the page's content above it; at 16 the bar began
        // four points left of every paragraph, which is the drift the layout
        // gate exists to catch.
        .padding(.horizontal, 20)
        .padding(.bottom, 8)
        .padding(.top, 10)
        // Opaque, with a short fade above it. At 96 percent the story showed
        // through the bar as ghost text, which reads as a rendering fault
        // rather than as translucency.
        .background(alignment: .top) {
            VStack(spacing: 0) {
                LinearGradient(colors: [Brand.ground.opacity(0), Brand.ground],
                               startPoint: .top, endPoint: .bottom)
                    .frame(height: 18)
                Brand.ground
            }
            .ignoresSafeArea(edges: .bottom)
        }
    }
}

/// The one editor behind every blank on a tree of your own.
///
/// Deliberately dull: a title, a field, Cancel and Save. Nothing here is a new
/// interaction, because filling in a text field is the most settled thing in
/// software and inventing a version of it would be the third time in one day.
struct FieldEditor: View {
    let field: TreeDetail.EditableField
    let initial: String
    let onSave: (String) -> Void
    let onCancel: () -> Void

    @State private var text: String = ""
    @FocusState private var focused: Bool

    var body: some View {
        NavigationStack {
            VStack(alignment: .leading, spacing: 12) {
                if field.long {
                    TextField(field.prompt, text: $text, axis: .vertical)
                        .lineLimit(4...10)
                        .focused($focused)
                } else {
                    TextField(field.prompt, text: $text)
                        .focused($focused)
                }
                Spacer()
            }
            .padding(16)
            .navigationTitle(field.prompt)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { onCancel() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        onSave(text.trimmingCharacters(in: .whitespacesAndNewlines))
                    }
                }
            }
        }
        .presentationDetents(field.long ? [.medium, .large] : [.height(220)])
        .onAppear { text = initial; focused = true }
    }
}
