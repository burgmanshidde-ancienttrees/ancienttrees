// Search, over the map, taking the whole screen.
//
// Komoot's shape, which Hidde asked for by name on 2026-08-22: the field lifts
// out of the sheet and the results own the page, so a search is a place you
// are rather than a dropdown you are fighting for room with.
//
// THE RANKING IS THE WEBSITE'S, ported rather than reinvented (site/src/lib/
// search-form.ts). Its rule is a hierarchy instead of one flat relevance list,
// which is what every search-led map product does: places first and always,
// then species, and an individual TREE only once the query is specific enough
// to be asking for one. Two letters give you cities; four give you trees.

import SwiftUI
import MapKit

struct MapSearch: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    var onPick: (Hit) -> Void
    @Environment(\.dismiss) private var dismiss
    @State private var query = ProcessInfo.processInfo.arguments
        .first { $0.hasPrefix("-search=") }.map { String($0.dropFirst(8)) } ?? ""
    @FocusState private var focused: Bool
    @State private var lane: Lane = .top
    /// Real towns Apple knows for the query, and which query they answer, so
    /// a stale answer is never shown under a newer one (EmptyPlace.swift).
    @State private var realPlaces: [RealPlace] = []
    @State private var answered: String?
    @Environment(Units.self) private var units
    @Environment(Account.self) private var account
    /// What this person picked lately, read from the account each time the
    /// screen opens (Kit/RecentSearches.swift). Signed out it stays empty.
    @State private var recent = RecentSearches()

    enum Lane: String, CaseIterable, Identifiable {
        case top, places, species, trees
        var id: String { rawValue }
        var label: String {
            switch self {
            case .top: "Top results"
            case .places: "Places"
            case .species: "Species"
            case .trees: "Trees"
            }
        }
    }

    enum Hit {
        case city(slug: String, name: String, lat: Double, lng: Double)
        case country(String)
        case species(String)
        case tree(Tree)
        /// A real town with none of our trees (2026-10-25).
        case place(name: String, lat: Double, lng: Double)
    }

    var body: some View {
        VStack(spacing: 0) {
            field
            if query.count >= 2 { lanes }
            Divider()
            ScrollView {
                LazyVStack(alignment: .leading, spacing: 0) {
                    if query.count < 2 { empty } else { results }
                }
                .padding(.bottom, 24)
            }
            .scrollDismissesKeyboard(.immediately)
        }
        .brandGround()
        .accessibilityIdentifier("map-search")
        // `-searchblur` (debug, with -search=) keeps the keyboard down so a
        // screenshot shows the whole result list; simctl cannot dismiss it.
        .onAppear { focused = !ProcessInfo.processInfo.arguments.contains("-searchblur") }
        // Recent searches: the account's newest five, signed in only.
        // `-recentdemo` (debug) fills three rows so the section can be looked
        // at on a simulator, which cannot sign in.
        .task {
            if ProcessInfo.processInfo.arguments.contains("-recentdemo") {
                recent.demo(demoRecent)
                return
            }
            guard account.isSignedIn else { return }
            await recent.load(token: await account.freshToken())
        }
        // Apple's towns, a beat after the last keystroke so typing "Bern" is
        // one lookup and not four. Not asked when one of OUR places carries
        // the name typed: "Lisbon" is ours, and Apple has nothing to add.
        .task(id: query) {
            let q = query.trimmingCharacters(in: .whitespaces)
            guard q.count >= 2, !oursIsNamed(q) else { realPlaces = []; answered = nil; return }
            try? await Task.sleep(for: .milliseconds(300))
            guard !Task.isCancelled else { return }
            let found = await EmptyPlace.lookup(q)
            guard !Task.isCancelled else { return }
            realPlaces = found
            answered = query
        }
    }

    /// One of our cities or countries carries exactly this name, in English or
    /// in another language browse.json knows.
    private func oursIsNamed(_ raw: String) -> Bool {
        let q = Self.fold(raw)
        if countries.contains(where: { Self.fold($0.name) == q }) { return true }
        return biggestCities.contains { c in
            Self.fold(c.name) == q || catalogue.facets.aka(city: c.slug).contains { Self.fold($0) == q }
        }
    }

    /// The town the empty card is about, or nil for no card.
    ///
    /// When nothing of ours matches, Apple's first town. When some of ours
    /// match only in passing ("Bern" finds Brno through its Albanian name
    /// Bërno, and Oberndorf through the middle of a word), a town Apple knows
    /// by EXACTLY the name typed still gets its card: somebody who typed a
    /// town's whole name was asking for that town (Hidde's mockup, 2026-10-25,
    /// is Bern). Our passing place matches are then dropped; our species and
    /// trees stay listed under it.
    private var cardTown: RealPlace? {
        guard answered == query, !realPlaces.isEmpty else { return nil }
        // NEVER "NO TREES" FOR A PLACE OF OURS (2026-11-04): Apple answered
        // "CadizCadiz" with Cádiz, and the card said nothing was mapped there.
        let towns = realPlaces.filter { !oursIsNamed($0.name) }
        guard !towns.isEmpty else { return nil }
        let r = ranked
        if r.places.isEmpty && r.species.isEmpty && r.trees.isEmpty { return towns[0] }
        let q = Self.fold(query.trimmingCharacters(in: .whitespaces))
        // OUR PLACES FIRST WHEN THE NAME BEGINS WITH WHAT WAS TYPED (Hidde,
        // 2026-11-04: "barce" found a town called Barce and hid Barcelona).
        // A place that matched only in passing (Brno through Bërno) still
        // gives way to a town typed in full, the Bern case above.
        if r.places.contains(where: { Self.fold($0.name).hasPrefix(q) }) { return nil }
        return towns.first { Self.fold($0.name) == q }
    }

    // MARK: - the field

    private var field: some View {
        HStack(spacing: 10) {
            Button { dismiss() } label: {
                Image(systemName: "arrow.left")
                    .font(.system(size: 17, weight: .semibold))
                    .foregroundStyle(Brand.ink)
                    .frame(width: 44, height: 44)
                    .contentShape(.rect)
            }
            .buttonStyle(.plain)
            .accessibilityLabel("Back to the map")

            TextField(Search.placeholder, text: $query)
                .textFieldStyle(.plain)
                .font(.system(size: 17, weight: .medium))
                .autocorrectionDisabled()
                .textInputAutocapitalization(.never)
                .focused($focused)
                .submitLabel(.search)

            if !query.isEmpty {
                Button { query = "" } label: {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundStyle(Brand.inkSoft)
                        .frame(width: 44, height: 44)
                        .contentShape(.rect)
                }
                .buttonStyle(.plain)
            }
        }
        .padding(.horizontal, 6)
        .frame(height: 54)
        .background(Brand.surface, in: .capsule)
        .overlay { Capsule().strokeBorder(Brand.hairline, lineWidth: 1) }
        .shadow(color: .black.opacity(0.06), radius: 6, y: 2)
        .padding(.horizontal, 16).padding(.top, 6).padding(.bottom, 10)
    }

    /// The chips under the field, which is the piece of Komoot's search that
    /// does the most work: the hierarchy is a good default and a bad prison,
    /// and somebody who wants only places should be able to say so.
    private var lanes: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                ForEach(Lane.allCases) { l in
                    let on = lane == l
                    Button { withAnimation(.snappy) { lane = l } } label: {
                        Text(l.label)
                            .font(.system(size: 14, weight: .semibold))
                            .foregroundStyle(on ? .white : Brand.ink)
                            .padding(.horizontal, 14)
                            .frame(height: 36)
                            .background(on ? Brand.canopy : Brand.surface, in: .capsule)
                            .overlay {
                                if !on { Capsule().strokeBorder(Brand.hairline, lineWidth: 1) }
                            }
                            .frame(height: 44)
                            .contentShape(.rect)
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.horizontal, 16)
        }
        .padding(.bottom, 6)
    }

    // MARK: - what an empty field shows

    /// Not nothing. An empty field asks the visitor to already know what we
    /// hold, and nobody arriving knows we have Cadiz. The website answers this
    /// the same way and for the same reason.
    @ViewBuilder private var empty: some View {
        let mine = recentRows
        if !mine.isEmpty {
            recentHead
            ForEach(mine, id: \.entry.id) { r in
                recentRow(r)
            }
            Divider().padding(.top, 10)
        }
        let near = Editorial.suggestions(catalogue: catalogue, origin: origin, excluding: [], limit: 4)
        if !near.isEmpty {
            head("Near you")
            ForEach(near) { t in
                row(t.name, "\(t.commonName) · \(t.city)", "tree") { pick(.tree(t)) }
            }
        }
        head("Places worth a trip")
        ForEach(biggestCities.prefix(6), id: \.slug) { c in
            row(c.name, "\(c.country) · \(treesLabel(c.count))", "building.2") {
                pick(.city(slug: c.slug, name: c.name, lat: c.lat, lng: c.lng))
            }
        }
    }

    // MARK: - what a query shows

    @ViewBuilder private var results: some View {
        let r = ranked
        let showPlaces = lane == .top || lane == .places
        let showSpecies = lane == .top || lane == .species
        let showTrees = lane == .top || lane == .trees
        let empty = (!showPlaces || r.places.isEmpty)
            && (!showSpecies || r.species.isEmpty)
            && (!showTrees || r.trees.isEmpty)

        // NOTHING OF OURS, BUT A REAL TOWN (Hidde, 2026-10-25): the ask to
        // add the first tree, the towns themselves, and the nearest tree we
        // do hold. On Top results and Places, the lanes a town belongs in.
        let ours = r.places.isEmpty && r.species.isEmpty && r.trees.isEmpty
        let asksForPlaces = lane == .top || lane == .places
        let town = asksForPlaces ? cardTown : nil
        if let town {
            notMappedYet(town)
        } else if ours && asksForPlaces && answered == query {
            // The 16 every row on this screen starts at.
            Text("Nothing matches “\(query)”. Check the spelling, or try a town nearby.")
                .font(.subheadline).foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
                .padding(.horizontal, 16).padding(.top, 24)
        } else if empty && !(ours && asksForPlaces) {
            Text("Nothing under \(lane.label.lowercased()). Try Top results.")
                .font(.subheadline).foregroundStyle(Brand.inkSoft)
                .padding(.horizontal, 16).padding(.top, 24)
        }
        if town == nil && showPlaces && !r.places.isEmpty {
            if lane == .top { head("Places") }
            ForEach(r.places, id: \.id) { p in
                row(p.name, p.sub, p.icon) { pick(p.hit) }
            }
        }
        if showSpecies && !r.species.isEmpty {
            if lane == .top { head("Species") }
            ForEach(r.species, id: \.self) { s in
                row(s, speciesSub(s), "leaf") { pick(.species(s)) }
            }
        }
        if showTrees && !r.trees.isEmpty {
            if lane == .top { head("Trees") }
            ForEach(r.trees) { t in
                row(t.name, "\(t.commonName) · \(t.city)", "tree") { pick(.tree(t)) }
                    .accessibilityIdentifier("search-result-tree")
            }
        }
    }

    /// The grey card for the town, Apple's towns (that one first), and the
    /// nearest tree. Our own places that matched only in passing (Brno via
    /// "Bërno") are left out, as on the website; species and trees follow.
    @ViewBuilder private func notMappedYet(_ top: RealPlace) -> some View {
        EmptyPlaceCard(place: top.name)
            .padding(.horizontal, 16).padding(.top, 18)
        head("Places")
        ForEach([top] + realPlaces.filter { $0 != top }) { p in
            Button { pick(.place(name: p.name, lat: p.lat, lng: p.lng)) } label: {
                EmptyPlaceRow(name: p.name,
                              sub: p.country.isEmpty ? "Show on the map" : "\(p.country) · show on the map",
                              icon: "mappin.and.ellipse")
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("empty-place-town")
        }
        if let n = EmptyPlace.nearest(in: catalogue, lat: top.lat, lng: top.lng) {
            head("Nearest tree")
            Button { pick(.tree(n.tree)) } label: {
                EmptyPlaceRow(name: n.tree.name,
                              sub: "\(EmptyPlace.distance(n.km, units.unit)) from \(top.name) · \(n.tree.city)",
                              icon: "tree")
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("empty-place-nearest")
        }
    }

    struct Place {
        let id: String
        let name: String
        let sub: String
        let icon: String
        let hit: Hit
    }

    /// The website's hierarchy, in Swift. Countries whose name starts with the
    /// query come first, then cities, then species, and trees only once the
    /// query is four characters or more and matches the start of a word.
    /// Worked out once per query and lane, and read back by every place that
    /// asks (the result list and the town card) until either changes.
    private var ranked: (places: [Place], species: [String], trees: [Tree]) {
        let idx = index   // first: a new catalogue clears the remembered result
        let key = RankedKey(query: query, lane: lane, lat: origin.lat, lng: origin.lng)
        if cache.rankedKey == key { return cache.ranked }
        let out = rank(idx)
        cache.rankedKey = key
        cache.ranked = out
        return out
    }

    private func rank(_ idx: SearchIndex) -> (places: [Place], species: [String], trees: [Tree]) {
        let q = Self.fold(query)
        guard q.count >= 2 else { return ([], [], []) }

        var places: [Place] = []
        for c in countries where Self.fold(c.name).hasPrefix(q) {
            places.append(Place(id: "k:" + c.name, name: c.name,
                                sub: "\(treesLabel(c.count)) in \(c.cities) \(c.cities == 1 ? "place" : "places")",
                                icon: "globe.europe.africa", hit: .country(c.name)))
        }
        for c in biggestCities {
            let n = Self.fold(c.name)
            // Sevilla finds Seville: the other-language names travel in
            // browse.json, the same list the website's search reads.
            let other = catalogue.facets.aka(city: c.slug).contains { Self.startsAWord(Self.fold($0), q) }
            if Self.startsAWord(n, q) || Self.fold(c.country).hasPrefix(q) || n.contains(q) || other {
                places.append(Place(id: "c:" + c.slug, name: c.name,
                                    sub: "\(c.country) · \(treesLabel(c.count))",
                                    icon: "building.2",
                                    hit: .city(slug: c.slug, name: c.name, lat: c.lat, lng: c.lng)))
            }
        }
        // Word-start rather than string-start, so "oak" finds Holm Oak and
        // Pedunculate Oak. The website matches the head of the name only,
        // which is right for a keyboard-and-mouse dropdown and wrong on a
        // phone, where nobody types "pedunculate".
        // And the scientific name, word-start too, so "quercus" and "robur"
        // both find Pedunculate Oak (2026-10-03). iNaturalist's autocomplete
        // answers to either name; the website's search does the same.
        // And every other name it goes by, in any of our languages, one
        // letter off included (2026-10-31): the one matcher every species
        // list uses, Kit/SpeciesSearch.swift.
        let species = catalogue.filterSpecies(allSpecies, query: query).map(\.name)

        var trees: [Tree] = []
        if q.count >= 4 || lane == .trees {
            trees = Editorial.rank(idx.treesNamed(q), origin: origin)
        }
        // Eight rows, the website's budget: places first, two species, and
        // trees only in whatever room is left.
        // On TOP RESULTS the budget is eight rows, and each kind takes more of
        // them when the others leave room: two species is right when six
        // places matched and absurd when the query was "oak". Ask for one kind
        // by name and the budget goes away, because a lane called Species that
        // shows two of eleven is a lie about what we have.
        guard lane == .top else {
            return (Array(places.prefix(40)), Array(species.prefix(40)), Array(trees.prefix(40)))
        }
        let p = Array(places.prefix(6))
        let s = Array(species.prefix(p.isEmpty ? 6 : 2))
        let room = max(0, 8 - p.count - s.count)
        return (p, s, Array(trees.prefix(min(room, p.isEmpty ? 5 : 2))))
    }

    // MARK: - recent searches

    /// Every pick goes through here: recorded on the account (signed in only,
    /// what was picked and never what was typed), then handed to the caller.
    /// The upsert is its own task so it outlives this screen's dismissal.
    private func pick(_ hit: Hit) {
        if account.isSignedIn, let e = entry(for: hit) {
            let store = recent, acct = account
            Task { await store.record(e, token: await acct.freshToken()) }
        }
        onPick(hit)
        dismiss()
    }

    private func entry(for hit: Hit) -> RecentSearches.Entry? {
        switch hit {
        case .city(let slug, let name, _, _):
            let c = index.cityBySlug[slug]
            return .init(kind: "city", ref: slug, label: name,
                         sub: c.map { "\($0.country) · \(treesLabel($0.count))" } ?? "")
        case .country(let name):
            return .init(kind: "country", ref: name, label: name,
                         sub: countries.first { $0.name == name }.map(countrySub) ?? "")
        case .species(let s):
            return .init(kind: "species", ref: s, label: s,
                         sub: treesLabel(catalogue.trees(ofSpecies: s).count))
        case .tree(let t):
            return .init(kind: "tree", ref: t.id, label: t.name, sub: "\(t.commonName) · \(t.city)")
        case .place(let name, let lat, let lng):
            return .init(kind: "place", ref: String(format: "%.4f,%.4f", lat, lng), label: name,
                         sub: "Show on the map")
        }
    }

    private func countrySub(_ c: (name: String, count: Int, cities: Int)) -> String {
        "\(treesLabel(c.count)) in \(c.cities) \(c.cities == 1 ? "place" : "places")"
    }

    private struct RecentRow {
        let entry: RecentSearches.Entry
        let name: String
        let sub: Text
        let hit: Hit
    }

    /// The account's rows, each read against today's catalogue so the sub
    /// line is today's (the same line the result rows draw). A row whose city,
    /// tree or species is no longer ours is left out.
    private var recentRows: [RecentRow] {
        guard !recent.rows.isEmpty else { return [] }
        return recent.rows.compactMap { e in
            switch e.kind {
            case "city":
                guard let c = index.cityBySlug[e.ref] else { return nil }
                return RecentRow(entry: e, name: c.name, sub: Text("\(c.country) · \(treesLabel(c.count))"),
                                 hit: .city(slug: c.slug, name: c.name, lat: c.lat, lng: c.lng))
            case "country":
                guard let c = countries.first(where: { $0.name == e.ref }) else { return nil }
                return RecentRow(entry: e, name: c.name, sub: Text(countrySub(c)), hit: .country(c.name))
            case "species":
                guard allSpecies.contains(e.ref) else { return nil }
                return RecentRow(entry: e, name: e.ref, sub: speciesSub(e.ref), hit: .species(e.ref))
            case "tree":
                guard let t = catalogue.tree(e.ref) else { return nil }
                return RecentRow(entry: e, name: t.name, sub: Text("\(t.commonName) · \(t.city)"), hit: .tree(t))
            case "place":
                let p = e.ref.split(separator: ",").compactMap { Double($0) }
                guard p.count == 2 else { return nil }
                return RecentRow(entry: e, name: e.label, sub: Text(e.sub.isEmpty ? "Show on the map" : e.sub),
                                 hit: .place(name: e.label, lat: p[0], lng: p[1]))
            default:
                return nil
            }
        }
    }

    /// The section head, as head() draws it, with Clear all at the right end
    /// (Google Maps' and Instagram's place for it). The tap area is 44 tall
    /// without making the head any taller.
    private var recentHead: some View {
        HStack(alignment: .firstTextBaseline) {
            Text("Recent")
                .font(.eyebrow).textCase(.uppercase).tracking(0.8)
                .foregroundStyle(Brand.inkSoft)
            Spacer(minLength: 8)
            Button {
                let store = recent, acct = account
                Task { await store.clear(token: await acct.freshToken()) }
            } label: {
                Text("Clear all")
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundStyle(Brand.moss)
                    .padding(.vertical, 12).padding(.leading, 12)
                    .contentShape(.rect)
                    .padding(.vertical, -12).padding(.leading, -12)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("recent-clear")
        }
        .padding(.horizontal, 16).padding(.top, 18).padding(.bottom, 6)
    }

    /// row()'s numbers exactly (14 between icon and text, the 24-wide icon at
    /// 17, 2 between name and sub, 16 in, 56 tall), with the clock in the
    /// grey of history and a cross at the end that removes this one.
    private func recentRow(_ r: RecentRow) -> some View {
        HStack(spacing: 0) {
            Button { pick(r.hit) } label: {
                HStack(spacing: 14) {
                    Image(systemName: "clock.arrow.circlepath")
                        .font(.system(size: 17))
                        .foregroundStyle(Brand.inkSoft)
                        .frame(width: 24)
                    VStack(alignment: .leading, spacing: 2) {
                        Text(r.name).fontWeight(.bold)
                            .font(.brand(16, .regular)).foregroundStyle(Brand.ink)
                            .lineLimit(1)
                        r.sub.font(.caption).foregroundStyle(Brand.inkSoft).lineLimit(1)
                    }
                    Spacer(minLength: 8)
                }
                .padding(.leading, 16).frame(minHeight: 56)
                .contentShape(.rect)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("recent-row")
            Button {
                let store = recent, acct = account, e = r.entry
                Task { await store.remove(e, token: await acct.freshToken()) }
            } label: {
                Image(systemName: "xmark")
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundStyle(Brand.inkSoft)
                    .frame(width: 44, height: 44)
                    .contentShape(.rect)
            }
            .buttonStyle(.plain)
            .padding(.trailing, 2)
            .accessibilityLabel("Remove \(r.name) from recent")
        }
    }

    /// Three rows for `-recentdemo`, from what the catalogue holds: a country,
    /// a city and a tree in it, the mock's Canada, Lisbon and a Lisbon tree.
    private var demoRecent: [RecentSearches.Entry] {
        var out: [RecentSearches.Entry] = []
        if let k = countries.first(where: { $0.name == "Canada" }) ?? countries.first,
           let e = entry(for: .country(k.name)) { out.append(e) }
        let cities = biggestCities
        if let c = cities.first(where: { $0.slug == "lisbon" }) ?? cities.first,
           let e = entry(for: .city(slug: c.slug, name: c.name, lat: c.lat, lng: c.lng)) {
            out.append(e)
            let ts = catalogue.trees.filter { $0.citySlug == c.slug }
            if let t = ts.first(where: { $0.name.localizedCaseInsensitiveContains("dragon") }) ?? ts.first,
               let e2 = entry(for: .tree(t)) { out.append(e2) }
        }
        return out
    }

    // MARK: - the pieces

    private func head(_ t: String) -> some View {
        Text(t)
            .font(.eyebrow).textCase(.uppercase).tracking(0.8)
            .foregroundStyle(Brand.inkSoft)
            // 16, matching the field above and every card in the app. It was
            // 20 here and in the rows below, so this screen carried two left
            // margins four points apart, which is the drift appfit exists to
            // name and which it only saw once it was pointed at a large phone
            // (2026-08-25).
            .padding(.horizontal, 16).padding(.top, 18).padding(.bottom, 6)
    }

    private func row(_ name: String, _ sub: String, _ icon: String,
                     _ act: @escaping () -> Void) -> some View {
        row(name, Text(sub), icon, act)
    }

    private func row(_ name: String, _ sub: Text, _ icon: String,
                     _ act: @escaping () -> Void) -> some View {
        Button(action: act) {
            HStack(spacing: 14) {
                Image(systemName: icon)
                    .font(.system(size: 17))
                    .foregroundStyle(Brand.moss)
                    .frame(width: 24)
                VStack(alignment: .leading, spacing: 2) {
                    highlighted(name)
                        .font(.brand(16, .regular)).foregroundStyle(Brand.ink)
                        .lineLimit(1)
                    sub.font(.caption).foregroundStyle(Brand.inkSoft).lineLimit(1)
                }
                Spacer(minLength: 8)
            }
            .padding(.horizontal, 16).frame(minHeight: 56)
            .contentShape(.rect)
        }
        .buttonStyle(.plain)
    }

    /// The letters you typed, in bold, wherever they sit in the name. Komoot
    /// does this and it is the difference between reading a list and seeing
    /// why each row is in it.
    private func highlighted(_ name: String) -> Text {
        let q = Self.fold(query)
        guard q.count >= 2, let r = Self.fold(name).range(of: q) else {
            return Text(name).fontWeight(.bold)
        }
        let lo = Self.fold(name).distance(from: Self.fold(name).startIndex, to: r.lowerBound)
        let hi = lo + q.count
        let chars = Array(name)
        guard hi <= chars.count else { return Text(name).fontWeight(.bold) }
        return Text(String(chars[0..<lo]))
            + Text(String(chars[lo..<hi])).fontWeight(.black)
            + Text(String(chars[hi...])).fontWeight(.bold)
    }

    /// The scientific name in italics before the count, iNaturalist's row:
    /// common name on top, Latin beneath. It is also how somebody who typed
    /// "robur" sees why Pedunculate Oak answered.
    private func speciesSub(_ s: String) -> Text {
        var count = Text(treesLabel(catalogue.trees(ofSpecies: s).count))
        if let sci = catalogue.scientificName(of: s) { count = scientificNameText(sci) + Text(" · ") + count }
        // The name that answered, when it was not the one on top: somebody
        // who typed "stieleiche" sees Stieleiche over Pedunculate Oak.
        guard let via = catalogue.speciesHit(s, query: query)?.via else { return count }
        return Text(via) + Text(" · ") + count
    }

    /// Does the query start the name, or start any word inside it?
    private static func startsAWord(_ name: String, _ q: String) -> Bool {
        name.hasPrefix(q) || name.contains(" " + q)
    }

    /// Case and accents folded, so Cadiz finds Cádiz and Zurich finds Zürich.
    static func fold(_ s: String) -> String {
        s.folding(options: [.diacriticInsensitive, .caseInsensitive], locale: .current)
    }

    /// A named struct rather than a six-part tuple: the tuple version put the
    /// type-checker over its budget in one expression.
    struct CityRow: Identifiable {
        let slug: String
        let name: String
        let country: String
        let count: Int
        let lat: Double
        let lng: Double
        var id: String { slug }
    }

    // BUILT ONCE PER CATALOGUE, not once per read (2026-11-04). These were
    // computed properties, so every keystroke rebuilt a centre for every city
    // and sorted them several times over (the ranking, the exact-name check,
    // the recent rows and the empty state each asked), and from four letters
    // folded every tree name again. The search screen now builds them the
    // first time it is drawn and reads them back after.
    private var biggestCities: [CityRow] { index.cities }
    private var countries: [(name: String, count: Int, cities: Int)] { index.countries }
    private var allSpecies: [String] { catalogue.speciesNames }

    private var index: SearchIndex { cache.index(for: catalogue) }

    /// Everything the search reads from the catalogue that does not depend
    /// on what was typed.
    struct SearchIndex {
        let cities: [CityRow]
        let cityBySlug: [String: CityRow]
        let countries: [(name: String, count: Int, cities: Int)]
        /// Every tree with its name folded, in catalogue order.
        let foldedNames: [(tree: Tree, folded: String)]

        init(_ catalogue: Catalogue) {
            var out: [CityRow] = []
            for (slug, ts) in catalogue.citiesWithTrees {
                let n = Double(ts.count)
                var la = 0.0, ln = 0.0
                for t in ts { la += t.lat; ln += t.lng }
                out.append(CityRow(slug: slug, name: ts[0].city, country: ts[0].country,
                                   count: ts.count, lat: la / n, lng: ln / n))
            }
            // The most VISITED first, as the website sorts it (Hidde, 2026-09-26:
            // "niet met de meeste bomen maar de meest bezochte pagina's"). The
            // figure is the website's, sent in browse.json; tree count breaks ties.
            let pop = { (slug: String) in catalogue.facets.popularity(city: slug) }
            cities = out.sorted { (pop($0.slug), $0.count) > (pop($1.slug), $1.count) }
            cityBySlug = Dictionary(cities.map { ($0.slug, $0) }, uniquingKeysWith: { a, _ in a })
            countries = catalogue.countriesWithTrees.map {
                (name: $0.key, count: $0.value.count, cities: Set($0.value.map(\.citySlug)).count)
            }
            .sorted { $0.count > $1.count }
            foldedNames = catalogue.trees.map { (tree: $0, folded: MapSearch.fold($0.name)) }
        }

        /// Trees whose name starts with the query or has a word that does,
        /// in catalogue order. `q` is already folded.
        func treesNamed(_ q: String) -> [Tree] {
            foldedNames.filter { $0.folded.hasPrefix(q) || $0.folded.contains(" " + q) }.map(\.tree)
        }
    }

    /// A class, so filling it while drawing changes nothing SwiftUI watches
    /// (the map's TreesMemo pattern).
    final class SearchCache {
        private var built: SearchIndex?
        private var builtFor: (version: String, count: Int)?
        var rankedKey: RankedKey?
        var ranked: (places: [Place], species: [String], trees: [Tree]) = ([], [], [])

        func index(for catalogue: Catalogue) -> SearchIndex {
            if let b = built, let k = builtFor,
               k.version == catalogue.version, k.count == catalogue.trees.count { return b }
            let b = SearchIndex(catalogue)
            built = b
            builtFor = (catalogue.version, catalogue.trees.count)
            rankedKey = nil
            return b
        }
    }
    struct RankedKey: Equatable {
        let query: String, lane: Lane, lat: Double, lng: Double
    }
    @State private var cache = SearchCache()
}
