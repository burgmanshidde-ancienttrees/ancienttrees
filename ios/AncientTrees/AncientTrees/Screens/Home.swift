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

struct HomeView: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    @Environment(CatalogueStore.self) private var store
    @State private var search = ""
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
        var atTheirBest: [Tree] = []
        var oldest: [Tree] = []
        var countries: [(name: String, count: Int, cities: Int, photo: Tree?)] = []
        var cities: [(slug: String, name: String, country: String, count: Int)] = []
        var walksNear: [Walk] = []
        var species: [(name: String, count: Int)] = []
    }

    private var month: Int { Calendar.current.component(.month, from: Date()) }
    private var monthName: String { DateFormatter().monthSymbols[month - 1] }

    private var atTheirBest: [Tree] { deck.atTheirBest }
    private var cities: [(slug: String, name: String, country: String, count: Int)] { deck.cities }
    private var walksNear: [Walk] { deck.walksNear }
    private var oldest: [Tree] { deck.oldest }

    /// Rebuilt when the catalogue changes under us, which it now does, or when
    /// the map has moved somewhere far enough to change what is near.
    private func buildShelves() {
        var s = Shelves()
        s.atTheirBest = catalogue.atTheirBest(inMonth: month, near: origin.lat, origin.lng, withinKm: 150)
        s.cities = Dictionary(grouping: catalogue.trees, by: \.citySlug)
            .map { (slug: $0.key, name: $0.value[0].city,
                    country: $0.value[0].country, count: $0.value.count) }
            .sorted { $0.count > $1.count }
        s.walksNear = catalogue.walks.compactMap { w -> (Walk, Double)? in
            guard let f = catalogue.trees(of: w).first else { return nil }
            return (w, f.distanceKm(from: origin.lat, origin.lng))
        }
        .sorted { $0.1 < $1.1 }.prefix(8).map(\.0)
        // Oldest by the LOW end of the range, so a tree claiming 200 to 800
        // years does not outrank one solidly dated at 900. A photograph is
        // required, because a shelf about the most spectacular thing we have
        // cannot be a row of placeholders.
        s.oldest = catalogue.trees
            .filter { $0.photo != nil && ($0.ageMin ?? 0) > 0 }
            .sorted { ($0.ageMin ?? 0) > ($1.ageMin ?? 0) }
            .prefix(12).map { $0 }
        s.countries = Dictionary(grouping: catalogue.trees, by: \.country)
            .map { (name: $0.key,
                    count: $0.value.count,
                    cities: Set($0.value.map(\.citySlug)).count,
                    photo: $0.value.first { $0.photo != nil }) }
            .sorted { $0.count > $1.count }
        s.species = Dictionary(grouping: catalogue.trees, by: \.commonName)
            .map { (name: $0.key, count: $0.value.count) }
            .sorted { $0.count > $1.count }
            .prefix(18).map { $0 }
        deck = s
    }

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 30) {
                if search.isEmpty { shelves } else { results }
                Color.clear.frame(height: 90)        // clear of the floating tab bar
            }
            .padding(.top, 6)
        }
        .brandGround()
        // Explore's list face, named the way its map face is ("explore-map"),
        // so a test can tell which face is showing without depending on a
        // shelf that sits below the fold on a small phone.
        .accessibilityIdentifier("explore-home")
        // No literal tab-label heading: the content is the heading. The empty
        // inline title keeps the bar (searchable lives in it) without the word
        // "Home" shouting over the hero.
        .navigationTitle("")
        .navigationBarTitleDisplayMode(.inline)
        .searchable(text: $search, prompt: "Search a place, a tree or a species")
        .refreshable { await store.refresh() }
        .task(id: catalogue.version) { buildShelves() }
    }

    /// The website leads with one tree rather than with a grid, and so does
    /// this: its "Tree of the month" block, which is the app's equivalent of a
    /// hero photo you cannot have on a phone without eating the whole screen.
    /// Picks the nearest tree that is at its best right now AND has a
    /// photograph, because a hero without a picture is a headline.
    @ViewBuilder private var hero: some View {
        if let t = atTheirBest.first(where: { $0.photo != nil }) {
            NavigationLink(value: Route.tree(t.id)) {
                VStack(alignment: .leading, spacing: 0) {
                    ZStack(alignment: .bottomLeading) {
                        if let p = t.photo, let url = Photos.thumb(p.url, width: 900) {
                            AsyncImage(url: url) { img in
                                img.resizable().aspectRatio(contentMode: .fill)
                            } placeholder: {
                                LinearGradient(colors: [Brand.canopy, Brand.moss],
                                               startPoint: .topLeading, endPoint: .bottomTrailing)
                            }
                            .frame(height: 260).clipped()
                        }
                        LinearGradient(colors: [.clear, .black.opacity(0.75)],
                                       startPoint: .center, endPoint: .bottom)
                        VStack(alignment: .leading, spacing: 6) {
                            Chip(text: "At its best now", tint: Brand.gold, filled: true)
                            Text(t.name)
                                .font(.brand(26, .black, relativeTo: .title))
                                .foregroundStyle(.white)
                                .multilineTextAlignment(.leading)
                            if let b = t.bestTime {
                                Text(b.label).font(.subheadline)
                                    .foregroundStyle(.white.opacity(0.9))
                                    .lineLimit(2)
                            }
                        }
                        .padding(16)
                    }
                    .frame(height: 260)
                }
                .clipShape(.rect(cornerRadius: 16))
                .shadow(color: .black.opacity(0.10), radius: 10, y: 4)
                .padding(.horizontal, 16)
            }
            .buttonStyle(.plain)
        }
    }

    /// Vertically, because a species is a WORD. Side by side they were a row
    /// of small labels you had to scroll sideways to read, and reading is the
    /// whole job of a list of names (Hidde, 2026-08-21).
    private var speciesShelf: some View {
        VStack(alignment: .leading, spacing: 8) {
            ShelfHeader(title: "By species",
                        subtitle: "\(Set(catalogue.trees.map(\.commonName)).count) kinds of tree on the map.",
                        more: .index(.species))
                .padding(.horizontal, 16)
            ForEach(topSpeciesHere.prefix(6), id: \.name) { sp in
                NavigationLink(value: Route.species(sp.name)) {
                    HStack(spacing: 12) {
                        SpeciesMark(species: sp.name, color: Brand.moss)
                            .frame(width: 28, height: 28)
                        Text(sp.name)
                            .font(.brand(16, .bold, relativeTo: .subheadline))
                            .foregroundStyle(Brand.ink).lineLimit(1)
                        Spacer(minLength: 8)
                        Text("\(sp.count)")
                            .font(.subheadline).foregroundStyle(Brand.inkSoft).monospacedDigit()
                        Image(systemName: "chevron.right")
                            .font(.caption).foregroundStyle(Brand.inkSoft.opacity(0.6))
                    }
                    .padding(.horizontal, 16).frame(minHeight: 52)
                    .brandCard(12)
                }
                .buttonStyle(.plain)
                .padding(.horizontal, 16)
            }
        }
    }

    private var topSpeciesHere: [(name: String, count: Int)] { deck.species }

    // MARK: - the browse state

    /// The feed, as Hidde cut it on 2026-08-21. What went: season (it is the
    /// map's pulse, not a browse row) and every curated collection (they stay
    /// on the website, which is where they earn their traffic). What stayed:
    /// cities, species, walks. What is new: the oldest trees we map, and the
    /// countries, because both are ways of showing the same database that a
    /// map cannot.
    @ViewBuilder private var shelves: some View {
        if !walksNear.isEmpty { walkShelf }

        cityShelf

        if !oldest.isEmpty {
            shelf(title: "The oldest trees we map",
                  subtitle: "Every one of these was already standing before your country looked the way it does.",
                  trees: oldest,
                  season: false,
                  more: .index(.oldest))
        }

        countryShelf
        speciesShelf
    }

    private var countryShelf: some View {
        VStack(alignment: .leading, spacing: 12) {
            ShelfHeader(title: "Tree countries",
                        subtitle: "\(deck.countries.count) of them, and the count is what we have mapped rather than what is there.",
                        more: .index(.countries))
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(alignment: .top, spacing: 12) {
                    ForEach(deck.countries.prefix(14), id: \.name) { c in
                        NavigationLink(value: Route.country(c.name)) { countryCard(c) }
                            .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal, 16).padding(.bottom, 4)
            }
        }
    }

    private func countryCard(_ c: (name: String, count: Int, cities: Int, photo: Tree?)) -> some View {
        VStack(alignment: .leading, spacing: 0) {
            Color.clear
                .frame(width: 150, height: 100)
                .overlay {
                    if let t = c.photo, let p = t.photo, let url = Photos.thumb(p.url, width: 400) {
                        AsyncImage(url: url) { img in
                            img.resizable().aspectRatio(contentMode: .fill)
                        } placeholder: { Brand.surfaceMuted }
                    } else {
                        Brand.surfaceMuted
                    }
                }
                .clipped()
            VStack(alignment: .leading, spacing: 2) {
                Text(c.name).font(.brand(15, .bold, relativeTo: .subheadline))
                    .foregroundStyle(Brand.ink).lineLimit(1)
                Text("\(c.count) trees · \(c.cities) \(c.cities == 1 ? "place" : "places")")
                    .font(.caption2).foregroundStyle(Brand.inkSoft)
            }
            .padding(.horizontal, 10).padding(.vertical, 9)
            .frame(width: 150, alignment: .leading)
        }
        .brandCard(12)
    }

    private func shelf(title: String, subtitle: String?, trees: [Tree],
                       season: Bool, more: Route? = nil) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            ShelfHeader(title: title, subtitle: subtitle, more: more)
                .padding(.horizontal, 16)

            ScrollView(.horizontal, showsIndicators: false) {
                HStack(alignment: .top, spacing: 12) {
                    ForEach(trees) { t in
                        NavigationLink(value: Route.tree(t.id)) {
                            VStack(alignment: .leading, spacing: 6) {
                                TreeCard(tree: t)
                                if season, let b = t.bestTime {
                                    Text(b.label)
                                        .font(.caption).foregroundStyle(Brand.inkSoft)
                                        .lineLimit(2).fixedSize(horizontal: false, vertical: true)
                                        .padding(.horizontal, 2)
                                }
                            }
                            .frame(width: 260)
                        }
                        .buttonStyle(.plain)
                        .accessibilityIdentifier("tree-card")
                    }
                }
                .padding(.horizontal, 16).padding(.bottom, 4)
            }
        }
    }

    /// Walks get their own card shape: the four facts with their units under
    /// them, which is the one thing from the AllTrails teardown that transfers
    /// wholesale, and the lock said plainly rather than as a bare padlock.
    private var walkShelf: some View {
        VStack(alignment: .leading, spacing: 12) {
            ShelfHeader(title: "Walks near you",
                        subtitle: "The nearest one is open to everyone. The others come with Plus, which is not open yet.")
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(alignment: .top, spacing: 12) {
                    ForEach(Array(walksNear.enumerated()), id: \.element.name) { i, w in
                        if i == 0 {
                            NavigationLink(value: Route.walk(city: w.citySlug, name: w.name)) {
                                walkCard(w, locked: false)
                            }
                            .buttonStyle(.plain)
                        } else {
                            LockedRow(feature: .walkBeyondFirst) { walkCard(w, locked: true) }
                        }
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
                if locked { Chip(text: "Plus", tint: Brand.gold) }
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

    /// The website's own homepage shelf, which this screen was missing: the
    /// places, with a photograph, rather than a list of names and counts.
    private var cityShelf: some View {
        VStack(alignment: .leading, spacing: 12) {
            ShelfHeader(title: "Our favourite tree cities",
                        subtitle: "\(cities.count) places, and every one of them is a good afternoon.",
                        more: .index(.cities))
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(alignment: .top, spacing: 12) {
                    ForEach(cities.prefix(14), id: \.slug) { c in
                        NavigationLink(value: Route.city(c.slug)) { cityCard(c) }
                            .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal, 16).padding(.bottom, 4)
            }
        }
    }

    private func cityCard(_ c: (slug: String, name: String, country: String, count: Int)) -> some View {
        // Cheap because it stops at the first hit, but it is still a scan of
        // every tree per card, so it only runs for the fourteen cards drawn.
        let cover = catalogue.trees.first { $0.citySlug == c.slug && $0.photo != nil }
        return VStack(alignment: .leading, spacing: 0) {
            ZStack(alignment: .bottomLeading) {
                if let p = cover?.photo, let url = Photos.thumb(p.url, width: 400) {
                    AsyncImage(url: url) { img in
                        img.resizable().aspectRatio(contentMode: .fill)
                    } placeholder: {
                        LinearGradient(colors: [Brand.canopy, Brand.moss],
                                       startPoint: .topLeading, endPoint: .bottomTrailing)
                    }
                    .frame(width: 172, height: 120).clipped()
                } else {
                    ZStack {
                        LinearGradient(colors: [Brand.canopy, Brand.moss],
                                       startPoint: .topLeading, endPoint: .bottomTrailing)
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
                    Text(c.name).font(.brand(16, .bold, relativeTo: .headline))
                        .foregroundStyle(.white).lineLimit(1)
                    Text("\(c.count) trees").font(.caption2).foregroundStyle(.white.opacity(0.85))
                }
                .padding(10)
            }
        }
        .frame(width: 172)
        .clipShape(.rect(cornerRadius: 14))
        .shadow(color: .black.opacity(0.07), radius: 8, y: 3)
    }

    // MARK: - the search state

    @ViewBuilder private var results: some View {
        let q = search.lowercased()
        let places = cities.filter {
            $0.name.lowercased().contains(q) || $0.country.lowercased().contains(q)
        }
        let trees = catalogue.trees.filter {
            $0.name.lowercased().contains(q) || $0.species.lowercased().contains(q)
        }.prefix(30)

        if places.isEmpty && trees.isEmpty {
            Text("Nothing matches “\(search)”.")
                .font(.footnote).foregroundStyle(Brand.inkSoft)
                .padding(.horizontal, 16).padding(.top, 30)
        }
        if !places.isEmpty {
            VStack(alignment: .leading, spacing: 12) {
                ShelfHeader(title: places.count == 1 ? "1 place" : "\(places.count) places")
                VStack(spacing: 0) {
                    ForEach(places.prefix(20), id: \.slug) { c in
                        NavigationLink(value: Route.city(c.slug)) {
                            HStack {
                                VStack(alignment: .leading, spacing: 1) {
                                    Text(c.name).font(.cardTitle).foregroundStyle(Brand.ink)
                                    Text(c.country).font(.caption).foregroundStyle(Brand.inkSoft)
                                }
                                Spacer()
                                Text("\(c.count)").font(.subheadline).foregroundStyle(Brand.inkSoft)
                                    .monospacedDigit()
                                Image(systemName: "chevron.right")
                                    .font(.caption).foregroundStyle(Brand.inkSoft.opacity(0.6))
                            }
                            .padding(.horizontal, 14).padding(.vertical, 12)
                        }
                        .buttonStyle(.plain)
                        if c.slug != places.prefix(20).last?.slug {
                            Divider().padding(.leading, 14)
                        }
                    }
                }
                .brandCard()
                .padding(.horizontal, 16)
            }
        }
        if !trees.isEmpty {
            VStack(alignment: .leading, spacing: 12) {
                ShelfHeader(title: "\(trees.count) trees")
                ForEach(trees) { t in
                    NavigationLink(value: Route.tree(t.id)) {
                        TreeCard(tree: t)
                            .padding(.horizontal, 16)
                    }
                    .buttonStyle(.plain)
                }
            }
        }
    }
}

/// One collection, opened from its shelf: the editor's own introduction, then
/// every tree in it.
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

    private var trees: [Tree] { catalogue.trees.filter { $0.citySlug == slug } }

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 14) {
                let walks = catalogue.walks(inCity: slug)
                if !walks.isEmpty {
                    ShelfHeader(title: walks.count == 1 ? "1 walk" : "\(walks.count) walks")
                    VStack(spacing: 0) {
                        ForEach(walks, id: \.name) { w in
                            NavigationLink(value: Route.walk(city: w.citySlug, name: w.name)) {
                                HStack {
                                    VStack(alignment: .leading, spacing: 1) {
                                        Text(w.name).font(.cardTitle).foregroundStyle(Brand.ink)
                                        Text("\(w.count) trees · \(w.duration)")
                                            .font(.caption).foregroundStyle(Brand.inkSoft)
                                    }
                                    Spacer()
                                    Image(systemName: "chevron.right")
                                        .font(.caption).foregroundStyle(Brand.inkSoft.opacity(0.6))
                                }
                                .padding(.horizontal, 12).padding(.vertical, 12)
                                .frame(minHeight: 44)
                                .contentShape(.rect)
                            }
                            .buttonStyle(.plain)
                            if w.name != walks.last?.name { Divider().padding(.leading, 12) }
                        }
                    }
                    .brandCard()
                    .padding(.horizontal, 16)
                }

                ShelfHeader(title: "\(trees.count) trees")
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
        .navigationBarTitleDisplayMode(.inline)
    }
}
