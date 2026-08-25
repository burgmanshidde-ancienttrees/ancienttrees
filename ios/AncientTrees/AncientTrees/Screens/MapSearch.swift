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
        .onAppear { focused = true }
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
        let near = Editorial.suggestions(catalogue: catalogue, origin: origin, excluding: [], limit: 4)
        if !near.isEmpty {
            head("Near you")
            ForEach(near) { t in
                row(t.name, "\(t.commonName) · \(t.city)", "tree") { onPick(.tree(t)); dismiss() }
            }
        }
        head("Places worth a trip")
        ForEach(biggestCities.prefix(6), id: \.slug) { c in
            row(c.name, "\(c.country) · \(c.count) trees", "building.2") {
                onPick(.city(slug: c.slug, name: c.name, lat: c.lat, lng: c.lng)); dismiss()
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

        if empty {
            Text(lane == .top
                 ? "Nothing matches that yet."
                 : "Nothing under \(lane.label.lowercased()). Try Top results.")
                .font(.subheadline).foregroundStyle(Brand.inkSoft)
                .padding(.horizontal, 20).padding(.top, 24)
        }
        if showPlaces && !r.places.isEmpty {
            if lane == .top { head("Places") }
            ForEach(r.places, id: \.id) { p in
                row(p.name, p.sub, p.icon) { onPick(p.hit); dismiss() }
            }
        }
        if showSpecies && !r.species.isEmpty {
            if lane == .top { head("Species") }
            ForEach(r.species, id: \.self) { s in
                row(s, speciesSub(s), "leaf") { onPick(.species(s)); dismiss() }
            }
        }
        if showTrees && !r.trees.isEmpty {
            if lane == .top { head("Trees") }
            ForEach(r.trees) { t in
                row(t.name, "\(t.commonName) · \(t.city)", "tree") { onPick(.tree(t)); dismiss() }
            }
        }
    }

    private struct Place {
        let id: String
        let name: String
        let sub: String
        let icon: String
        let hit: Hit
    }

    /// The website's hierarchy, in Swift. Countries whose name starts with the
    /// query come first, then cities, then species, and trees only once the
    /// query is four characters or more and matches the start of a word.
    private var ranked: (places: [Place], species: [String], trees: [Tree]) {
        let q = Self.fold(query)
        guard q.count >= 2 else { return ([], [], []) }

        var places: [Place] = []
        for c in countries where Self.fold(c.name).hasPrefix(q) {
            places.append(Place(id: "k:" + c.name, name: c.name,
                                sub: "\(c.count) trees in \(c.cities) places",
                                icon: "globe.europe.africa", hit: .country(c.name)))
        }
        for c in biggestCities {
            let n = Self.fold(c.name)
            if Self.startsAWord(n, q) || Self.fold(c.country).hasPrefix(q) || n.contains(q) {
                places.append(Place(id: "c:" + c.slug, name: c.name,
                                    sub: "\(c.country) · \(c.count) trees",
                                    icon: "building.2",
                                    hit: .city(slug: c.slug, name: c.name, lat: c.lat, lng: c.lng)))
            }
        }
        // Word-start rather than string-start, so "oak" finds Holm Oak and
        // Pedunculate Oak. The website matches the head of the name only,
        // which is right for a keyboard-and-mouse dropdown and wrong on a
        // phone, where nobody types "pedunculate".
        let species = allSpecies.filter { Self.startsAWord(Self.fold($0), q) }

        var trees: [Tree] = []
        if q.count >= 4 || lane == .trees {
            trees = catalogue.trees.filter {
                let n = Self.fold($0.name)
                return n.hasPrefix(q) || n.contains(" " + q)
            }
            trees = Editorial.rank(trees, origin: origin)
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
                    Text(sub).font(.caption).foregroundStyle(Brand.inkSoft).lineLimit(1)
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

    private func speciesSub(_ s: String) -> String {
        let n = catalogue.trees.filter { $0.commonName == s }.count
        return "\(n) \(n == 1 ? "tree" : "trees")"
    }

    /// Does the query start the name, or start any word inside it?
    private static func startsAWord(_ name: String, _ q: String) -> Bool {
        name.hasPrefix(q) || name.contains(" " + q)
    }

    /// Case and accents folded, so Cadiz finds Cádiz and Zurich finds Zürich.
    private static func fold(_ s: String) -> String {
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

    private var biggestCities: [CityRow] {
        var out: [CityRow] = []
        for (slug, ts) in Dictionary(grouping: catalogue.trees, by: \.citySlug) {
            let n = Double(ts.count)
            var la = 0.0, ln = 0.0
            for t in ts { la += t.lat; ln += t.lng }
            out.append(CityRow(slug: slug, name: ts[0].city, country: ts[0].country,
                               count: ts.count, lat: la / n, lng: ln / n))
        }
        return out.sorted { $0.count > $1.count }
    }

    private var countries: [(name: String, count: Int, cities: Int)] {
        Dictionary(grouping: catalogue.trees, by: \.country).map {
            (name: $0.key, count: $0.value.count, cities: Set($0.value.map(\.citySlug)).count)
        }
        .sorted { $0.count > $1.count }
    }

    private var allSpecies: [String] {
        Array(Set(catalogue.trees.map(\.commonName))).sorted()
    }
}
