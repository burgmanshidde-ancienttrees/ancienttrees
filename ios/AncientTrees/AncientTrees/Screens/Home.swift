// Home: the website's homepage, on a phone.
//
// Renamed from Explore on 2026-08-20 (Hidde: "Home - this is the explore page -
// based on our homepage on the website ... really try and recreate the web
// homepage experience here"). It is the second tab, not the first, and that is
// the one thing of his proposal I did not take: the website opens on
// inspiration because it does not know where you are, and the app does. Opening
// on anything but the map would be copying the website onto a device that can
// do better. PRODUCT_IA.md's own reason for moving the map OFF the homepage was
// that a sparse WORLD map advertises incompleteness, and that reason does not
// transfer to a map that opens on your street.
//
// The order follows PRODUCT_IA.md's homepage order, with one deliberate
// omission. The website's second block is the four verbs explained as sections;
// in the app the verbs ARE the tab bar, so repeating them here is exactly the
// duplication that document warns about ("tighten, never duplicate").
//
// Browse, rebuilt on 2026-08-20 as shelves rather than as a settings list.
//
// It was a `List`: season rows, walk rows, city rows, all in Apple's default
// inset-grouped style, which is the look of the Settings app and reads as a
// database with a nice font. Hidde's two notes were the same note twice: "it
// feels like im looking at apple settings", and "in explore please use rows
// like our favourite cities, best tree islands, stuff like that to inspire".
//
// So the screen is now shelves, the way AllTrails, Netflix and every browse
// screen worth the name is built: a horizontal row of cards under a large bold
// heading, where the pictures do the persuading and the heading says why these
// things are together.
//
// The headings are not invented here, which is the part that matters. The
// website has thirteen hand-curated collections with titles like "Trees Planted
// by Kings and Their Gardeners" and "The Ginkgos Worth a November Trip", and
// /api/browse.json has served them since 2026-08-19 to nobody at all. Writing
// new ones in the app would have meant inventing groupings with no editing
// behind them; using these means every shelf on this screen was decided by
// somebody looking at the trees.

import SwiftUI
import CoreLocation

struct HomeView: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    /// Whether `origin` is a fix or a fallback. See LocationOff.swift.
    @Environment(\.locationState) private var location
    @Environment(CatalogueStore.self) private var store
    @Environment(Navigator.self) private var navigator
    @Environment(Saved.self) private var saved
    @State private var searching = false
    /// Worked out once rather than on every redraw.
    ///
    /// These were computed properties, and each of them groups or sorts all
    /// 1,535 trees: the cities, the top species, the walks, what is at its best.
    /// SwiftUI re-evaluates a body constantly while a finger is on the screen,
    /// so scrolling Home meant re-grouping fifteen hundred trees per frame and
    /// the screen locked up. Hidde: "de app doet niks loop vast op homescherm
    /// kan niet scrollen."
    @State private var deck = Shelves()

    struct Shelves {
        /// The season where you stand: its word, the photographed tree at its
        /// best nearest to you, how many trees on your half of the world are at
        /// their best this month, and how many of those are within 20 km.
        var season: (word: String, hero: Tree, count: Int, near: Int)? = nil
        /// At their best now, photographed, nearest first, the hero left out.
        var best: [Tree] = []
        var cities: [(slug: String, name: String, country: String, count: Int)] = []
        /// The city you are standing in, for the ambassador row.
        var here: (slug: String, name: String)? = nil
        var countries: [(name: String, count: Int, photo: Tree?)] = []
        var islands: [(slug: String, name: String, country: String, count: Int)] = []
        var species: [(name: String, count: Int, photo: Tree?)] = []
        var records: [(label: String, tree: Tree, route: Route)] = []
        var lists: [(collection: TreeCollection, face: Tree)] = []
        var walksNear: [Walk] = []
        /// Every photographed tree not already on the page, nearest first:
        /// the stream at the bottom that keeps going.
        var tail: [Tree] = []
    }

    private var month: Int { Calendar.current.component(.month, from: Date()) }

    private var cities: [(slug: String, name: String, country: String, count: Int)] { deck.cities }
    private var walksNear: [Walk] { deck.walksNear }

    /// The season's word on your half of the world (Hidde, 2026-10-09: "wat
    /// doen we met het feit dat sommige landen niet tegelijk herfst hebben").
    static func seasonWord(month: Int, south: Bool) -> String {
        let m = south ? (month + 5) % 12 + 1 : month
        switch m {
        case 3...5: return "Spring"
        case 6...8: return "Summer"
        case 9...11: return "Autumn"
        default: return "Winter"
        }
    }

    /// Rebuilt when the catalogue changes under us, or when the map has moved
    /// somewhere far enough to change what is near.
    private func buildShelves() {
        var s = Shelves()
        // THE WEBSITE'S SHELF, in the website's order (feed `favourites`,
        // lib/favourites.ts), never every city by count (Hidde, 2026-10-02:
        // "Don't promote cities like Leeuwarden if they don't have a single
        // photo"). An older snapshot falls back to the cities that HAVE a face.
        let byCity = catalogue.citiesWithTrees
        func card(_ slug: String) -> (slug: String, name: String, country: String, count: Int)? {
            guard let trees = byCity[slug], let first = trees.first else { return nil }
            return (slug: slug, name: first.city, country: first.country, count: trees.count)
        }
        let favourites = catalogue.facets.favourites.compactMap(card)
        s.cities = !favourites.isEmpty ? favourites
            : byCity.keys.compactMap(card)
                .filter { catalogue.face(city: $0.slug) != nil }
                .sorted { $0.count > $1.count }
        s.walksNear = catalogue.walks.compactMap { w -> (Walk, Double)? in
            guard let f = catalogue.trees(of: w).first else { return nil }
            return (w, f.distanceKm(from: origin.lat, origin.lng))
        }
        .sorted { $0.1 < $1.1 }.prefix(8).map(\.0)

        // Distance once per tree, not once per comparison.
        let ranked = catalogue.trees
            .map { (tree: $0, km: $0.distanceKm(from: origin.lat, origin.lng)) }
            .sorted { $0.km < $1.km }

        // THE SEASON WHERE YOU ARE, the hero (Hidde, 2026-10-10: "season h1 is
        // good"). Without a fix the north is assumed, the half where most of
        // the map is.
        let south = location.known && origin.lat < 0
        let atBest = ranked.filter {
            ($0.tree.bestTime?.months ?? []).contains(month) && ($0.tree.lat < 0) == south
        }
        let bestPhotographed = atBest.filter { $0.tree.photo != nil }.map(\.tree)
        if let hero = bestPhotographed.first {
            let near = location.known ? atBest.filter { $0.km <= 20 }.count : 0
            s.season = (Self.seasonWord(month: month, south: south), hero, atBest.count, near)
            s.best = Array(bestPhotographed.dropFirst().prefix(6))
        }

        // The city you are standing in, for its open ambassador seat. Only with
        // a real fix: the fallback is not anybody's city.
        if location.known, let t = catalogue.nearest(to: origin.lat, origin.lng, limit: 1, withinKm: 30).first?.tree {
            s.here = (t.citySlug, t.city)
        }

        s.countries = catalogue.countriesWithTrees
            .map { (name: $0.key, count: $0.value.count, photo: catalogue.face(country: $0.key)) }
            .filter { $0.photo?.photo != nil }
            .sorted { $0.count > $1.count }
        s.islands = catalogue.facets.islands.compactMap(card)
            .filter { catalogue.face(city: $0.slug)?.photo != nil }
        s.species = catalogue.speciesWithTrees
            .map { (name: $0.key, count: $0.value.count, photo: catalogue.face(species: $0.key)) }
            .filter { $0.photo?.photo != nil }
            .sorted { $0.count > $1.count }
            .prefix(8).map { $0 }

        // THE RECORDS: the oldest, the thickest and the tallest, one tile each,
        // opening the full list. Oldest by the LOW end of the range, so a tree
        // claiming 200 to 800 years does not outrank one dated at 900.
        if let t = catalogue.trees.filter({ $0.photo != nil && ($0.ageMin ?? 0) > 0 })
            .max(by: { ($0.ageMin ?? 0) < ($1.ageMin ?? 0) }) {
            s.records.append((t.ageShort.map { "Oldest · \($0)" } ?? "Oldest", t, .index(.oldest)))
        }
        func first(_ slug: String) -> (TreeCollection, Tree)? {
            guard let c = catalogue.collections.first(where: { $0.slug == slug }),
                  let t = catalogue.trees(of: c).first(where: { $0.photo != nil }) else { return nil }
            return (c, t)
        }
        if let r = first("thickest-trees") {
            let (c, t) = r
            let label = t.girthCm.map { g -> String in
                let m = Double(g) / 100
                return "Thickest · " + (m >= 10 ? String(format: "%.0f m", m) : String(format: "%.1f m", m))
            } ?? "Thickest"
            s.records.append((label, t, .collection(c.slug)))
        }
        if let r = first("tallest-trees") { s.records.append(("Tallest", r.1, .collection(r.0.slug))) }

        // LISTS WITH AN OPINION: the hand-made collections, the ones in season
        // first. The generated rankings are already The records.
        let generated: Set<String> = ["tallest-trees", "thickest-trees", "trees-older-than-400-years",
                                      "the-oldest-tree-in-every-country-we-map"]
        s.lists = catalogue.collections.enumerated()
            .filter { !generated.contains($0.element.slug) }
            .compactMap { pair -> (Int, TreeCollection, Tree)? in
                let (i, c) = pair
                guard let id = c.face, let t = catalogue.tree(id), t.photo != nil else { return nil }
                return (i, c, t)
            }
            .sorted { a, b in
                let ia = (a.1.months ?? []).contains(month), ib = (b.1.months ?? []).contains(month)
                return ia == ib ? a.0 < b.0 : ia
            }
            // One face per photograph: two lists fronted by the same yew side by
            // side read as a mistake, so a list whose face is taken is skipped.
            .reduce(into: [(collection: TreeCollection, face: Tree)]()) { out, l in
                if out.count < 6, !out.contains(where: { $0.face.id == l.2.id }) {
                    out.append((collection: l.1, face: l.2))
                }
            }

        // MORE TREES NEAR YOU, the stream that keeps going (Hidde, 2026-10-10:
        // "more trees near you at the end is perfect"): every photographed tree
        // not already on the page, nearest first.
        var shown = Set(s.best.map(\.id))
        if let h = s.season?.hero { shown.insert(h.id) }
        s.tail = ranked.map(\.tree).filter { $0.photo != nil && !shown.contains($0.id) }
        deck = s
    }

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 30) {
                seasonHero
                shelves
                growingCard
                tailShelf
                Color.clear.frame(height: 90)        // clear of the floating tab bar
            }
            .padding(.top, 6)
        }
        // PINNED WITH safeAreaInset, not with a pinned Section (Hidde,
        // 2026-08-26: "stikcy search bovenaan op explore on scroll"). The
        // Section version compiled and then took the whole screen down on
        // launch, which the sweep caught as a photograph of the home screen;
        // this is the mechanism iOS uses for its own pinned bars, it does not
        // touch the shelves at all, and the scroll view gets the inset for
        // free so nothing hides under it.
        .safeAreaInset(edge: .top, spacing: 0) {
            VStack(alignment: .leading, spacing: 20) {
                    HStack(alignment: .firstTextBaseline) {
                        Text("Discover")
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
                    Button { searching = true } label: {
                        HStack(spacing: 10) {
                            Image(systemName: "magnifyingglass")
                                .font(.system(size: 17, weight: .semibold))
                                .foregroundStyle(Brand.ink)
                            Text(Search.placeholder)
                                .font(.system(size: 16, weight: .medium))
                                .foregroundStyle(Brand.inkSoft)
                            Spacer(minLength: 0)
                        }
                        .padding(.horizontal, 16).frame(height: 50)
                        .background(Brand.surface, in: .capsule)
                        .overlay { Capsule().strokeBorder(Brand.hairline, lineWidth: 1) }
                        .shadow(color: .black.opacity(0.06), radius: 6, y: 2)
                        .contentShape(.capsule)
                    }
                    .buttonStyle(.plain)
                    .accessibilityIdentifier("explore-search")
            }
            .padding(.horizontal, 16)
            .padding(.top, 4)
            .padding(.bottom, 10)
            // Opaque, or the shelves show through it as ghost text.
            .background(Brand.ground)
        }
        .brandGround()
        // Explore's list face, named the way its map face is ("explore-map"),
        // so a test can tell which face is showing without depending on a
        // shelf that sits below the fold on a small phone.
        .accessibilityIdentifier("explore-home")
        // No literal tab-label heading: the content is the heading. The empty
        // inline title keeps the bar (searchable lives in it) without the word
        // "Home" shouting over the hero.
        .toolbar(.hidden, for: .navigationBar)
        .fullScreenCover(isPresented: $searching) {
            MapSearch(catalogue: catalogue, origin: origin) { hit in
                // On the FEED a result is a page, not a camera move.
                switch hit {
                case .city(let slug, _, _, _): navigator.push = .city(slug)
                case .country(let name): navigator.push = .country(name)
                case .species(let name): navigator.push = .species(name)
                case .tree(let t): navigator.push = .tree(t.id)
                }
            }
        }
        .refreshable { await store.refresh() }
        // Rebuilt when the catalogue changes, and when a fix arrives or moves a
        // long way, because two shelves (walks, best in your country) depend
        // on where you are. A tenth of a degree is about ten kilometres.
        .task(id: "\(catalogue.version)|\(location.known)|\(Int(origin.lat * 10))|\(Int(origin.lng * 10))") { buildShelves() }
    }

    /// The website leads with one tree rather than with a grid, and so does
    /// this: its "Tree of the month" block, which is the app's equivalent of a
    /// hero photo you cannot have on a phone without eating the whole screen.
    /// Picks the nearest tree that is at its best right now AND has a
    /// photograph, because a hero without a picture is a headline.
    /// THE MAP IS NOT FINISHED, said out loud, at the end of the browsing.
    ///
    /// Hidde, 2026-08-29: "ik wil meer mensen duidelijk maken dat we nog aan
    /// het verbeteren zijn en ze kunnen helpen." It sat on the App Store panel
    /// for one build and he took it off there, which is right: a store frame
    /// sells the promise, and this is a different job.
    ///
    /// At the END of Discover on purpose. Somebody who has scrolled past the
    /// cities, the oldest trees, the countries and the species has just seen
    /// how much there is, which is the moment the gap is worth naming: they
    /// know what a good entry looks like and they can tell whether their own
    /// tree belongs. At the top it would be an apology before anybody had seen
    /// anything.
    ///
    /// The wording follows PRODUCT_COPY.md rather than the corpus's own voice:
    /// the reader acts, no machinery is named, and there is no summary line
    /// after it.
    private var growingCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("The map is still growing")
                .font(.brand(19, .bold, relativeTo: .headline))
                .foregroundStyle(Brand.ink)
            // NOT "some of the best ones came from readers", which is what this
            // said for one build. Two trees have been sent in so far and
            // neither is published, so that sentence was flattery dressed as a
            // fact, which is the one thing this project does not do to its own
            // readers. What is left is true: trees go on every week, and the
            // map has gaps.
            Text("New trees go on every week, and there are still cities where we have only a handful. You can add one by photographing it and filling in what you know.")
                .font(.subheadline).foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
            Button {
                // THE CAMERA IS NOT A TAB (Hidde, 2026-09-04: "add a tree knop
                // in discover onderaan doet het nog steeds niet").
                //
                // This asked for TabBar.collectTag, which was a real tab until
                // the bar went to three destinations and a separate camera
                // disc on 2026-08-26. Since then ContentView's guard has
                // silently dropped any selection outside 0...2, because a
                // selection matching no tag leaves the TabView on its first
                // page with no bar and no way back. The guard was right and
                // this call site was the second one it was quietly saving:
                // Profile's identity row was the first, found a week earlier.
                //
                // So it does what every other entry to the camera does, which
                // is ask for the deed rather than for a place.
                navigator.collectNearby = true
            } label: {
                Label("Add a tree", systemImage: "camera.fill")
            }
            .buttonStyle(BrandButtonStyle(prominent: false))
        }
        .padding(16)
        .frame(maxWidth: .infinity, alignment: .leading)
        .brandCard()
        .padding(.horizontal, 16)
    }

    /// A photograph and the promise, a different one every time the app is
    /// opened (Kit/Heroes.swift). It is the website's own hero moved onto the
    /// phone, so somebody arriving from ancienttrees.app meets the same thing.
    ///
    /// It scrolls AWAY rather than pinning, which is the whole reason it is
    /// allowed to be this big: the search field above it is pinned and stays,
    /// so a picture at the top costs a scroll and never a control.
    ///
    /// No tree name on it, deliberately. These are stock photographs and a
    /// name beside one would say we hold that tree, which we do not.
    @ViewBuilder private var heroBand: some View {
        // No photograph, no band. A gradient with a slogan on it is worse than
        // nothing, and that is exactly what shipped for one build: Image("name")
        // asks the asset catalogue, these files are loose in the bundle, and a
        // missing image is not a build error. See Kit/Heroes.swift.
        if let photo = Heroes.image {
        ZStack(alignment: .bottomLeading) {
            Image(uiImage: photo)
                .resizable()
                .aspectRatio(contentMode: .fill)
                .frame(height: 260)
                .clipped()
            LinearGradient(colors: [.clear, .black.opacity(0.62)],
                           startPoint: .center, endPoint: .bottom)
                .frame(height: 260)
            VStack(alignment: .leading, spacing: 2) {
                Text("Trees worth the walk,")
                    .foregroundStyle(.white)
                Text("wherever you are.")
                    .foregroundStyle(Brand.gold)
            }
            .font(.brand(26, .bold, relativeTo: .title2))
            .shadow(color: .black.opacity(0.35), radius: 8, y: 2)
            .padding(16)
        }
        .frame(height: 260)
        .clipShape(.rect(cornerRadius: 16))
        .padding(.horizontal, 16)
        .accessibilityElement(children: .combine)
        .accessibilityLabel("Trees worth the walk, wherever you are")
        }
    }

    // MARK: - Discover, redesigned 2026-10-10
    //
    // Convention: AllTrails, komoot and Pinterest build a browse screen as a
    // short curated top and then a stream that keeps going; the trees are
    // Instagram's 3:4 grid, the same tile as My trees (CONVENTIONS.md
    // 2026-10-06, "The browse / Discover screen, benchmarked"). Every row is
    // skipped when it has nothing for where you are. The designs Hidde chose
    // are board D3 of the Discover canvas.

    private let threeAcross = Array(repeating: GridItem(.flexible(), spacing: 8), count: 3)

    /// THE GRIDS STAY INSIDE THE PAGE'S MARGIN (Hidde, 2026-10-10: "het
    /// klopt weer niet op de discover pagina"). Edge to edge with square tiles
    /// is for a page that IS a grid, your own collection: Instagram's profile,
    /// the library in Apple Photos, our My trees. A page made of shelves keeps
    /// one left edge and rounds what floats in it: the App Store, Airbnb,
    /// AllTrails' Explore, the collections under Photos' grid
    /// (CONVENTIONS.md, "Corners", corrected the same day). Bleeding three
    /// grids out of the margin between rounded shelves made Discover's left
    /// edge jump in and out down the page.
    private func grid<Content: View>(@ViewBuilder _ content: () -> Content) -> some View {
        LazyVGrid(columns: threeAcross, spacing: 8, content: content)
            .padding(.horizontal, 16)
    }
    private static let tileShape = RoundedRectangle(cornerRadius: 12, style: .continuous)

    /// The tag on a tree tile: its city, and the distance when it is within a
    /// day trip of you (Hidde, 2026-10-10: "the first trees can be city · 1.2km").
    private func tag(_ t: Tree) -> String {
        guard location.known else { return t.city }
        let d = t.distanceKm(from: origin.lat, origin.lng)
        guard d <= 30 else { return t.city }
        return "\(t.city) · " + (d < 10 ? String(format: "%.1f km", d) : "\(Int(d.rounded())) km")
    }

    /// Three across inside the margin, rounded: see grid().
    private func tileGrid(_ trees: [Tree]) -> some View {
        grid {
            ForEach(trees) { t in
                NavigationLink(value: Route.tree(t.id)) { CollectedTile(kind: .ours(t), city: tag(t)).clipShape(Self.tileShape) }
                    .buttonStyle(.plain)
                    .accessibilityIdentifier("tree-card")
            }
        }
    }

    /// A tile that opens somewhere other than its own tree: an island, a
    /// record, a list. The tag says what it opens.
    private func tile(_ tree: Tree, _ label: String, to route: Route) -> some View {
        NavigationLink(value: route) { CollectedTile(kind: .ours(tree), city: label).clipShape(Self.tileShape) }
            .buttonStyle(.plain)
    }

    /// THE SEASON (hero H1). One photographed tree at its best near you, the
    /// season's word for your half of the world, and a real count. Falls back
    /// to the stock hero in the rare month nothing on your half peaks.
    @ViewBuilder private var seasonHero: some View {
        if let s = deck.season, let url = s.hero.photo?.full ?? s.hero.photo?.card {
            NavigationLink(value: Route.tree(s.hero.id)) {
                ZStack(alignment: .bottomLeading) {
                    Color.clear.frame(height: 240)
                        .overlay { TreePhoto(url: url) { Brand.surfaceMuted } }
                        .clipped()
                    LinearGradient(colors: [.clear, .black.opacity(0.62)],
                                   startPoint: .center, endPoint: .bottom)
                    VStack(alignment: .leading, spacing: 4) {
                        Text("\(s.word) is here")
                            .font(.brand(26, .bold, relativeTo: .title2))
                            .foregroundStyle(.white)
                        Text("\(treesLabel(s.count)) at their best this month"
                             + (s.near > 0 ? " · \(s.near) within 20 km of you" : ""))
                            .font(.subheadline.weight(.medium))
                            .foregroundStyle(.white.opacity(0.88))
                            .fixedSize(horizontal: false, vertical: true)
                    }
                    .shadow(color: .black.opacity(0.3), radius: 6, y: 1)
                    .padding(16)
                }
                .frame(height: 240)
                .overlay(alignment: .topLeading) { TagPill(text: "At its best now").padding(12) }
                .clipShape(.rect(cornerRadius: 14))
                .contentShape(.rect)
                // One element, as the stock hero was: the photograph is wider
                // than the card before the clip, and VoiceOver reads the card.
                .accessibilityElement(children: .ignore)
                .accessibilityLabel("\(s.word) is here. \(s.hero.name), at its best now.")
            }
            .buttonStyle(.plain)
            .padding(.horizontal, 16)
            .accessibilityIdentifier("discover-season")
        } else {
            heroBand
        }
    }

    private var wantTrees: [Tree] {
        saved.favourites.compactMap { catalogue.tree($0.treeId) }
            .sorted { $0.distanceKm(from: origin.lat, origin.lng) < $1.distanceKm(from: origin.lat, origin.lng) }
    }

    /// WANT TO VISIT, with trees: yours, under the hero, because they are
    /// yours (Netflix's My List, Spotify's Jump back in). Read live from Saved,
    /// so a bookmark tapped on a tree page is here when you come back.
    @ViewBuilder private var wantToVisitFull: some View {
        let mine = wantTrees
        if !mine.isEmpty {
            VStack(alignment: .leading, spacing: 12) {
                ShelfHeader(title: "Want to visit", seeAll: {
                    navigator.openWantToVisit = true
                    navigator.selectTab = 2
                })
                tileGrid(Array(mine.prefix(3)))
            }
        }
    }

    /// WANT TO VISIT, empty: the row's own shape waiting to be filled, one
    /// line saying what the bookmark does, and the way to find a tree. Lower
    /// on the page, so a first visit meets trees before an empty box.
    @ViewBuilder private var wantToVisitEmpty: some View {
        if wantTrees.isEmpty {
            VStack(alignment: .leading, spacing: 12) {
                ShelfHeader(title: "Want to visit")
                grid {
                    ForEach(0..<3, id: \.self) { i in
                        Brand.surfaceMuted
                            .aspectRatio(3.0 / 4.0, contentMode: .fit)
                            .clipShape(Self.tileShape)
                            .overlay {
                                if i == 0 {
                                    Image(systemName: "bookmark")
                                        .font(.system(size: 22, weight: .semibold))
                                        .foregroundStyle(Brand.inkSoft.opacity(0.45))
                                }
                            }
                    }
                }
                .accessibilityHidden(true)
                Text("You can keep a tree for later by tapping the bookmark on its page.")
                    .font(.subheadline).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
                    .padding(.horizontal, 16)
                Button { navigator.selectTab = 0 } label: {
                    Label("Find trees near you", systemImage: "map")
                }
                .buttonStyle(BrandButtonStyle(prominent: false))
                .padding(.horizontal, 16)
            }
            .accessibilityElement(children: .contain)
            .accessibilityIdentifier("discover-favourites-empty")
        }
    }

    private func section<Content: View>(_ title: String, more: Route? = nil,
                                        @ViewBuilder _ content: () -> Content) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            ShelfHeader(title: title, more: more)
            content()
        }
    }

    private func placeRow<Item, Card: View>(_ items: [Item], id: KeyPath<Item, String>,
                                            @ViewBuilder _ card: @escaping (Item) -> Card) -> some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(alignment: .top, spacing: 12) {
                ForEach(items, id: id) { card($0) }
            }
            .padding(.horizontal, 16).padding(.bottom, 4)
        }
    }

    private func speciesPill(_ sp: (name: String, count: Int, photo: Tree?)) -> some View {
        NavigationLink(value: Route.species(sp.name)) {
            HStack(spacing: 8) {
                Color.clear.frame(width: 34, height: 34)
                    .overlay {
                        if let url = sp.photo?.photo?.card { TreePhoto(url: url) { Brand.surfaceMuted } }
                    }
                    .clipShape(.circle)
                Text(sp.name)
                    .font(.brand(14, .bold, relativeTo: .subheadline))
                    .foregroundStyle(Brand.ink).lineLimit(1)
                Text("\(sp.count)")
                    .font(.system(size: 13)).foregroundStyle(Brand.inkSoft).monospacedDigit()
            }
            .padding(.leading, 5).padding(.trailing, 12)
            .frame(height: 44)
            .background(Brand.surface, in: .capsule)
            .overlay { Capsule().strokeBorder(Brand.hairline, lineWidth: 1) }
            .contentShape(.capsule)
        }
        .buttonStyle(.plain)
    }

    @ViewBuilder private var shelves: some View {
        wantToVisitFull

        if deck.best.count >= 3 {
            section("At their best now") { tileGrid(deck.best) }
        }

        cityShelf

        // The open seat of the city you are standing in, under the cities and
        // well away from "Add a tree" (Hidde, 2026-10-10: "dont put ambassador
        // cta and add tree cta below each other").
        if let h = deck.here, catalogue.facets.ambassadors(city: h.slug).isEmpty,
           !catalogue.facets.seated(city: h.slug) {
            AmbassadorWantedRow(place: h.name).padding(.horizontal, 16)
        }

        if !deck.countries.isEmpty {
            section("Tree countries", more: .index(.countries)) {
                placeRow(Array(deck.countries.prefix(14)), id: \.name) { c in
                    NavigationLink(value: Route.country(c.name)) {
                        placeCard(c.name, treesLabel(c.count), cover: c.photo)
                    }
                    .buttonStyle(.plain)
                }
            }
        }

        wantToVisitEmpty

        if deck.islands.count >= 3 {
            section("Tree islands") {
                grid {
                    ForEach(deck.islands.prefix(6), id: \.slug) { c in
                        if let face = catalogue.face(city: c.slug) { tile(face, c.name, to: .city(c.slug)) }
                    }
                }
            }
        }

        if !deck.species.isEmpty {
            section("By species", more: .index(.species)) {
                FlowRow(spacing: 8) {
                    ForEach(deck.species, id: \.name) { speciesPill($0) }
                }
                .padding(.horizontal, 16)
            }
        }

        if deck.records.count == 3 {
            section("The records") {
                grid {
                    ForEach(deck.records, id: \.label) { r in tile(r.tree, r.label, to: r.route) }
                }
            }
        }

        if deck.lists.count >= 3 {
            section("Lists with an opinion") {
                grid {
                    ForEach(deck.lists, id: \.collection.slug) { l in
                        tile(l.face, l.collection.title, to: .collection(l.collection.slug))
                    }
                }
            }
        }

        if Launch.walks, !walksNear.isEmpty, location.known { walkShelf }
    }

    /// The stream at the bottom: every photographed tree, nearest first,
    /// loading as you scroll (LazyVGrid draws only what is on screen).
    @ViewBuilder private var tailShelf: some View {
        if !deck.tail.isEmpty {
            section(location.known ? "More trees near you" : "More trees") { tileGrid(deck.tail) }
        }
    }

    static func withArticle(_ country: String) -> String {
        let the: Set<String> = ["United States", "United Kingdom", "Netherlands",
                                "Czech Republic", "Philippines", "Bahamas"]
        return the.contains(country) ? "the \(country)" : country
    }

    private var walkShelf: some View {
        VStack(alignment: .leading, spacing: 12) {
            // EVERY walk behind Plus (Hidde, 2026-08-24: "ik zou alle
            // wandelingen achter plus zetten"). His own pricing names curated
            // walks as a paid feature; the free first one was my softening of
            // it, and the subtitle promising it goes with it.
            ShelfHeader(title: "Walks near you")
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(alignment: .top, spacing: 12) {
                    ForEach(walksNear, id: \.name) { w in
                        LockedRow(feature: .walkBeyondFirst, lockGlyph: false) { walkCard(w, locked: true) }
                    }
                }
                .padding(.horizontal, 16).padding(.bottom, 4)
            }
        }
    }

    private func walkCard(_ w: Walk, locked: Bool) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                Text(w.name).font(.cardTitle).foregroundStyle(Brand.ink).lineLimit(2)
                Spacer(minLength: 6)
                if locked { Chip(text: "Plus", tint: Brand.goldInk) }
            }
            Text(w.city).font(.footnote).foregroundStyle(Brand.inkSoft)
            Spacer(minLength: 0)
            HStack(spacing: 0) {
                stat("\(w.count)", "trees")
                Divider().frame(height: 26)
                stat(String(format: "%.1f", w.km), "km")
                Divider().frame(height: 26)
                stat("\(w.minutes)", "min")
            }
        }
        .padding(14)
        .frame(width: 230, height: 168, alignment: .topLeading)
        .brandCard()
    }

    private func stat(_ value: String, _ unit: String) -> some View {
        VStack(spacing: 1) {
            Text(value).font(.brand(17, .bold, relativeTo: .headline))
                .foregroundStyle(Brand.ink).monospacedDigit()
            Text(unit).font(.caption2).foregroundStyle(Brand.inkSoft)
        }
        .frame(maxWidth: .infinity)
    }

    // NO SUBTITLES under the shelf titles (Hidde, 2026-10-04: "maybe less is
    // more"). AllTrails, Airbnb, Netflix and Spotify put a title and a See all
    // on a browse row and nothing under it; the cards do the persuading. The
    // counts that sat here ("31 countries, as far as we have mapped") were
    // the lead-with-a-count habit PITCH_VOICE.md names. CONVENTIONS.md
    // 2026-10-04.

    /// The website's own homepage shelf, which this screen was missing: the
    /// places, with a photograph, rather than a list of names and counts.
    private var cityShelf: some View {
        section("Our favourite tree cities", more: .index(.cities)) {
            placeRow(Array(cities.prefix(14)), id: \.slug) { c in
                NavigationLink(value: Route.city(c.slug)) {
                    placeCard(c.name, treesLabel(c.count), cover: catalogue.face(city: c.slug))
                }
                .buttonStyle(.plain)
            }
        }
    }

    /// A place: a city, a country. Wide, because a place is a landscape, and
    /// small, so two show with a third peeking (Airbnb's destination row).
    private func placeCard(_ name: String, _ sub: String, cover: Tree?) -> some View {
        ZStack(alignment: .bottomLeading) {
            if let url = cover?.photo?.card {
                TreePhoto(url: url) { leafTile }
                    .frame(width: 172, height: 120).clipped()
            } else {
                ZStack {
                    leafTile
                    SpeciesMark(species: cover?.species ?? "Pedunculate Oak",
                                color: .white.opacity(0.85))
                        .frame(width: 46, height: 46)
                }
                .frame(width: 172, height: 120)
            }
            LinearGradient(colors: [.clear, .black.opacity(0.55)],
                           startPoint: .center, endPoint: .bottom)
                .frame(width: 172, height: 120)
            VStack(alignment: .leading, spacing: 1) {
                Text(name).font(.brand(16, .bold, relativeTo: .headline))
                    .foregroundStyle(.white).lineLimit(1)
                Text(sub).font(.caption2).foregroundStyle(.white.opacity(0.85))
            }
            .padding(10)
        }
        .frame(width: 172, height: 120)
        .clipShape(.rect(cornerRadius: 14))
    }

}

struct CollectionView: View {
    let collection: TreeCollection
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 14) {
                if let intro = collection.intro, !intro.isEmpty {
                    Text(intro)
                        .font(.callout)
                        .foregroundStyle(Brand.inkSoft)
                        .padding(.horizontal, 16).padding(.top, 4)
                }
                ForEach(catalogue.trees(of: collection)) { t in
                    NavigationLink(value: Route.tree(t.id)) {
                        TreeCard(tree: t)
                            .padding(.horizontal, 16)
                    }
                    .buttonStyle(.plain)
                }
                Color.clear.frame(height: 90)
            }
            .padding(.top, 6)
        }
        .brandGround()
        .navigationTitle(collection.title)
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct CityView: View {
    let slug: String
    let name: String
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    @Environment(Navigator.self) private var navigator

    /// PHOTOGRAPHED FIRST (Hidde, 2026-08-29: "moeten we de app niet zo maken
    /// dat de bomen met fotos boven aan de lijst staan?").
    ///
    /// Here yes, because this list had no order at all: it was whatever the
    /// feed happened to hold, so nobody can be surprised by a different one,
    /// and a city page that opens on pictures is a city page somebody scrolls.
    /// Roughly a fifth of our trees carry a photograph, so an unsorted city
    /// opened on grey more often than not.
    ///
    /// NOT on the map's "trees you can see", and that boundary is the whole
    /// answer to his question. That list is sorted by distance and the
    /// distance IS the promise: a photographed tree three kilometres away
    /// climbing above the oak across the street would be the one lie this
    /// product cannot tell. Same for the season radar and for nearest().
    ///
    /// Stable within each half: enumerated() keeps the feed's own order among
    /// the photographed and among the rest, so this only ever lifts, never
    /// shuffles.
    private var trees: [Tree] {
        catalogue.trees(inCity: slug)
            .enumerated()
            .sorted { a, b in
                let pa = a.element.photo?.card != nil, pb = b.element.photo?.card != nil
                return pa == pb ? a.offset < b.offset : pa
            }
            .map(\.element)
    }

    /// Where the map opens: the middle of this city's trees, wide enough to
    /// hold them all with a little air.
    private var frame: (centre: (lat: Double, lng: Double), meters: Double) {
        guard let first = trees.first else { return (origin, 4000) }
        var minLat = first.lat, maxLat = first.lat
        var minLng = first.lng, maxLng = first.lng
        for t in trees {
            minLat = min(minLat, t.lat); maxLat = max(maxLat, t.lat)
            minLng = min(minLng, t.lng); maxLng = max(maxLng, t.lng)
        }
        let centre = ((minLat + maxLat) / 2, (minLng + maxLng) / 2)
        let latM = (maxLat - minLat) * 111_320
        let lngM = (maxLng - minLng) * 111_320 * cos(centre.0 * .pi / 180)
        return (centre, max(1200, min(max(latM, lngM) * 1.4, 40_000)))
    }

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 14) {
                // THE MAP FIRST, because a city is a view of the map before it
                // is a list (Hidde, 2026-08-24: "als ik op een stad klik zoals
                // barcelona verwacht ik daarboven de kaart met de bomen erop en
                // dan de bomen in de lijst eronder... dezelfde logica doen we
                // op web"). The website's city page has had exactly this shape
                // all along; the app's had a list and no map at all.
                // A PICTURE OF THE MAP, and the whole picture is the way to
                // the real one. It carried allowsHitTesting(false) and nothing
                // else, so it read as a dead control (Hidde, 2026-08-25: "dan
                // kan ik niet op de kaart klikken... ik zou hem eigenlijk dan
                // daarheen verwijzen"). Hit testing stays off on the map itself
                // so a finger dragging past it still scrolls the page, which is
                // what Airbnb and AllTrails do with a preview: the map does not
                // pan, the button over it opens the map that does.
                // PUSHED, never a jump to the Map tab (Hidde, 2026-08-27).
                // A tab is a different place with a different history: it threw
                // away the city somebody was reading and gave them a back
                // button belonging to something else. This keeps the trail.
                NavigationLink(value: Route.placeMap(.city(slug))) {
                    ZStack(alignment: .bottomTrailing) {
                        TreeMap(trees: trees,
                                focus: .init(latitude: frame.centre.lat,
                                             longitude: frame.centre.lng),
                                // A picture, so no recentre control: it cannot
                                // be panned and the whole thing is one link.
                                showsRecentre: false,
                                spanMeters: frame.meters,
                                fitsTrees: true,
                                selected: .constant(nil))
                            .allowsHitTesting(false)
                        // A solid capsule, not a material one: over a pale map
                        // the blur was invisible and the words floated on the
                        // tiles, which reads as a label rather than a control.
                        // What it does, rather than where it goes. "Open the
                        // map" described a destination and the destination was
                        // wrong; this says what you get.
                        Label("Expand map", systemImage: "arrow.up.left.and.arrow.down.right")
                            .font(.caption.weight(.semibold))
                            .foregroundStyle(Brand.ink)
                            .padding(.horizontal, 12).padding(.vertical, 8)
                            .background(Brand.surface, in: .capsule)
                            .overlay { Capsule().strokeBorder(Brand.hairline, lineWidth: 1) }
                            .shadow(color: .black.opacity(0.10), radius: 4, y: 1)
                            .padding(10)
                    }
                    .frame(height: 260)
                    .clipShape(.rect(cornerRadius: 16))
                    .contentShape(.rect)
                }
                .buttonStyle(.plain)
                .accessibilityIdentifier("city-open-map")
                .padding(.horizontal, 16)

                // WHO LOOKS AFTER THIS CITY, under the map as the website
                // prints it under the intro (AmbassadorLine.astro): the named
                // ambassadors, else the open seat with its one tap. It stood
                // only on the pushed map page until 2026-10-07, so the page a
                // person actually lands on from Discover and from a link never
                // showed it, and the signed-out walk could not find it there.
                let named = catalogue.facets.ambassadors(city: slug)
                ForEach(named, id: \.self) { a in
                    AmbassadorRow(name: a.name, place: name, affiliation: a.affiliation)
                        .padding(.horizontal, 16)
                }
                if named.isEmpty && !catalogue.facets.seated(city: slug) {
                    AmbassadorWantedRow(place: name).padding(.horizontal, 16)
                }

                // BEHIND THE LAUNCH FLAG, like every other walk surface
                // (Kit/Launch.swift). This one was not, so the app launched
                // free with no reference to Plus anywhere except here: a shelf
                // of gold Plus chips on every city page (Hidde, 2026-08-27:
                // "ik zie walks en plus op de stadspagina's staan"). Explore
                // and the map both read Launch.walks; the city page was
                // written from the same shelf and never got the check.
                let walks = Launch.walks ? catalogue.walks(inCity: slug) : []
                if !walks.isEmpty {
                    ShelfHeader(title: walks.count == 1 ? "1 walk" : "\(walks.count) walks")
                    // The same shelf Explore uses: swipe sideways, the first
                    // open to everyone and the rest behind Plus. It was a
                    // stacked list here and a shelf there, which is two designs
                    // for one object (Hidde, 2026-08-24).
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(alignment: .top, spacing: 12) {
                            // EVERY walk behind Plus (Hidde, 2026-08-24: "ik
                            // zou alle wandelingen achter plus zetten"), not
                            // just the ones past the first. His own pricing
                            // names curated walks as a paid feature; the free
                            // first one was my softening of it.
                            ForEach(walks, id: \.name) { w in
                                LockedRow(feature: .walkBeyondFirst, lockGlyph: false) {
                                    CityWalkCard(walk: w, locked: true)
                                }
                            }
                        }
                        .padding(.horizontal, 16).padding(.bottom, 4)
                    }
                }

                ShelfHeader(title: treesLabel(trees.count))
                ForEach(trees) { t in
                    NavigationLink(value: Route.tree(t.id)) {
                        TreeCard(tree: t)
                            .padding(.horizontal, 16)
                    }
                    .buttonStyle(.plain)
                }
                Color.clear.frame(height: 90)
            }
            .padding(.top, 6)
        }
        .brandGround()
        .navigationTitle(name)
        .toolbar {
            ShareTo(url: URL(string: "https://ancienttrees.app/\(slug)")!,
                    subject: name,
                    message: "Ancient trees in \(name).",
                    label: "Share this city")
        }
        .navigationBarTitleDisplayMode(.inline)
    }
}

/// A walk, as a card on a shelf. Shared by Explore and by a city, because the
/// two had drifted into different shapes for the same object.
struct CityWalkCard: View {
    let walk: Walk
    let locked: Bool
    /// Drawn on the map right now. The map's shelf lets you switch between a
    /// city's walks, and a shelf you can choose from has to say which one is
    /// chosen (2026-08-25).
    var selected: Bool = false

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                Text(walk.name).font(.cardTitle).foregroundStyle(Brand.ink).lineLimit(2)
                Spacer(minLength: 6)
                if locked { Chip(text: "Plus", tint: Brand.goldInk) }
            }
            Text("\(treesLabel(walk.count)) · \(walk.duration)")
                .font(.caption).foregroundStyle(Brand.inkSoft)
        }
        .padding(14)
        .frame(width: 220, alignment: .leading)
        .brandCard()
        .overlay {
            if selected {
                RoundedRectangle(cornerRadius: 12)
                    .strokeBorder(Brand.moss, lineWidth: 2)
            }
        }
    }
}
