// The map is the product, so the tab called Map opens on a map.
//
// The model is Google Maps' rather than AllTrails', and Hidde is right about
// why: AllTrails is built for LINES and we show POINTS. A route has no location,
// it has a course, which is why they cluster into labels reading "2 routes". A
// tree is exactly what a pin wants to be, and Google Maps has been solving that
// one problem for twenty years.
//
// The piece worth copying is the sheet. It is always there, it has three
// heights, and it carries either the list or whatever pin you last tapped. That
// is what stops the map and the list being two destinations you have to choose
// between, which is what ours were.

import SwiftUI
import MapKit
import Combine

struct MapTab: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    let located: Bool
    /// iOS has been asked and said no. A different sentence from "not yet
    /// asked", because the only way out of this one is Settings.
    var locationDenied: Bool = false
    var onUseMyLocation: () -> Void = {}

    @State private var selected: Tree?
    /// Debug only, same family as -tab and -at: selecting a pin needs a tap and
    /// simctl cannot tap, so the one screen that only exists after a tap could
    /// not be looked at before it shipped.
    private var debugSelect: String? {
        ProcessInfo.processInfo.arguments.first { $0.hasPrefix("-select=") }.map { String($0.dropFirst(8)) }
    }
    /// Debug scaffolding, same family as -tab and -spot: the sheet opens at
    /// its peek and a test that wants a CARD would otherwise have to perform
    /// the raise gesture first, which makes every card test a gesture test as
    /// well and fails for reasons that have nothing to do with what it covers.
    /// The gesture itself is still asserted, by the test that is about it.
    @State private var sheetHeight: SheetHeight =
        ProcessInfo.processInfo.arguments.contains("-sheet=full") ? .full : .peek
    @State private var query = ""
    @State private var promptIndex = 0
    /// Debug scaffolding, same family as -spot: the search page is only
    /// reachable by tapping and simctl has no finger. `-search` opens it empty,
    /// `-search=lis` opens it with that typed.
    @State private var searching = ProcessInfo.processInfo.arguments
        .contains { $0 == "-search" || $0.hasPrefix("-search=") }
    private let promptTick = Timer.publish(every: 2.6, on: .main, in: .common).autoconnect()
    /// Where the map is looking. nil until it has been moved, so the first list
    /// is still the list of what is near you.
    @State private var mapRegion: MKCoordinateRegion?
    @State private var moveRequest: (token: UUID, region: MKCoordinateRegion)?
    @State private var filters = MapFilters()
    @State private var shownWalk: Walk?
    @Environment(Entitlement.self) private var entitlement
    @Environment(Saved.self) private var saved
    @Environment(Account.self) private var account
    @Environment(Nudge.self) private var nudge
    @Environment(Navigator.self) private var navigator

    /// EVERY tree, because the map is the whole map.
    ///
    /// This used to hand MapKit the nearest 400 within 200 km, which meant that
    /// zooming out from Amsterdam showed the Netherlands and then nothing: no
    /// Portugal, no Japan, no reason to believe there is a world here. The
    /// website has never done that, it clusters the whole set, and the app
    /// looking narrower than the website is the wrong way round.
    ///
    /// Cheap to do: 1,500 annotations is nothing for MKMapView, the pins carry
    /// a clusteringIdentifier so MapKit collapses them by zoom on its own, and
    /// the set never changes so updateUIView stops churning entirely.
    /// The walks the site planned, nearest first. The ORDER inside a city is
    /// left exactly as /api/walks.json delivers it, because that order is a
    /// decision rather than an accident: walk_planning.py sorts photographed
    /// walks ahead of bigger ones, on the grounds that somebody decides from the
    /// pictures whether an afternoon is worth it. Re-sorting here would throw
    /// that away.
    private var walksHere: [Walk] {
        catalogue.walks.compactMap { w -> (Walk, Double)? in
            guard let f = catalogue.trees(of: w).first else { return nil }
            return (w, f.distanceKm(from: focus.lat, focus.lng))
        }
        .filter { $0.1 < 60 }
        .sorted { $0.1 < $1.1 }
        .map(\.0)
    }

    private var walkRoute: [CLLocationCoordinate2D] {
        guard let w = shownWalk else { return [] }
        // The real routed line where route_walks.py cached one, and the order
        // the trees are visited where it did not. 78 of 179 have a real one.
        if let shape = w.shape, shape.count > 1 {
            return shape.map { CLLocationCoordinate2D(latitude: $0[1], longitude: $0[0]) }
        }
        return catalogue.trees(of: w).map { .init(latitude: $0.lat, longitude: $0.lng) }
    }

    private var mapTrees: [Tree] {
        guard filters.isOn else { return catalogue.trees }
        return catalogue.trees.filter {
            filters.keeps($0, month: month, collected: collectedIds)
                && filters.keepsDistance($0.distanceKm(from: focus.lat, focus.lng))
        }
    }

    private var month: Int { Calendar.current.component(.month, from: Date()) }
    /// The ids you have collected, worked out once per redraw rather than
    /// asked per tree while filtering fifteen hundred of them.
    private var collectedIds: Set<String> {
        Set(saved.entries.values.filter { $0.visitedAt != nil }.map(\.treeId))
    }
    /// The point the list is about: where the map is looking once it has been
    /// moved, and where you are standing until then.
    private var focus: (lat: Double, lng: Double) {
        guard let c = mapRegion?.center else { return origin }
        return (lat: c.latitude, lng: c.longitude)
    }

    /// How far to look, which has to follow the zoom. Half the visible height,
    /// floored at fifty kilometres so a street-level view still fills the list
    /// rather than showing the four trees actually on screen.
    private var reachKm: Double {
        guard let s = mapRegion?.span else { return 50 }
        return max(50, s.latitudeDelta * 111.0 / 2)
    }

    /// True when the map is still looking at roughly where you are standing, so
    /// the chip can stop saying "near you" the moment that stops being true.
    private var lookingAtYou: Bool {
        guard let c = mapRegion?.center else { return true }
        return CLLocation(latitude: c.latitude, longitude: c.longitude)
            .distance(from: CLLocation(latitude: origin.lat, longitude: origin.lng)) < 3000
    }

    /// Move the map somewhere a search result asked for. A region rather than
    /// a camera because that is what the sheet's list reads to decide what is
    /// "here", so setting one keeps the two in step.
    private func fly(to lat: Double, lng: Double, span metres: Double) {
        let r = MKCoordinateRegion(center: .init(latitude: lat, longitude: lng),
                                   latitudinalMeters: metres, longitudinalMeters: metres)
        moveRequest = (UUID(), r)
        mapRegion = r
    }

    /// How many trees are actually under the view, uncapped.
    ///
    /// The strip used to count `listed`, which stops at sixty because that is
    /// as many cards as anybody scrolls. So it read "60 trees you can see" over
    /// Amsterdam, over Lisbon and over half of Europe, which is a number that
    /// looks like information and is not.
    private var inReach: Int {
        // What the WORDS say: the trees inside the rectangle you are looking
        // at. It counted everything within fifty kilometres before, which is
        // a different and much larger claim than "you can see".
        guard let r = mapRegion else {
            return catalogue.trees.filter {
                filters.keeps($0, month: month, collected: collectedIds)
                    && $0.distanceKm(from: focus.lat, focus.lng) <= 6
            }.count
        }
        let latMin = r.center.latitude - r.span.latitudeDelta / 2
        let latMax = r.center.latitude + r.span.latitudeDelta / 2
        let lngMin = r.center.longitude - r.span.longitudeDelta / 2
        let lngMax = r.center.longitude + r.span.longitudeDelta / 2
        return catalogue.trees.filter {
            $0.lat >= latMin && $0.lat <= latMax && $0.lng >= lngMin && $0.lng <= lngMax
                && filters.keeps($0, month: month, collected: collectedIds)
        }.count
    }

    private var listed: [(tree: Tree, km: Double)] {
        let near = catalogue.nearest(to: focus.lat, focus.lng, limit: 60, withinKm: reachKm)
            .filter { filters.keeps($0.tree, month: month, collected: collectedIds) && filters.keepsDistance($0.km) }
        guard !query.isEmpty else {
            return Editorial.leadWithAPhotograph(near, photo: { $0.tree.photo != nil })
        }
        let q = query.lowercased()
        return catalogue.trees
            .filter { $0.name.lowercased().contains(q) || $0.city.lowercased().contains(q)
                      || $0.species.lowercased().contains(q) }
            .filter { filters.keeps($0, month: month, collected: collectedIds)
                        && filters.keepsDistance($0.distanceKm(from: focus.lat, focus.lng)) }
            .prefix(40)
            .map { ($0, $0.distanceKm(from: focus.lat, focus.lng)) }
    }

    var body: some View {
        ZStack(alignment: .bottom) {
            TreeMap(trees: shownWalk.map { catalogue.trees(of: $0) } ?? mapTrees,
                    focus: .init(latitude: origin.lat, longitude: origin.lng),
                    route: walkRoute,
                    routeIsReal: (shownWalk?.shape?.count ?? 0) > 1,
                    showsRecentre: true,
                    region: $mapRegion,
                    moveTo: moveRequest,
                    selected: $selected)
                .ignoresSafeArea(edges: [.top, .horizontal])
                .accessibilityIdentifier("tree-map")
            .onReceive(promptTick) { _ in
                withAnimation(.easeInOut(duration: 0.25)) { promptIndex = (promptIndex + 1) % Self.searchWords.count }
            }
            BottomSheet(height: $sheetHeight) {
                // The arbitration between dragging the sheet and scrolling what
                // is inside it, which is the whole interaction and was wrong.
                //
                // The convention, and Apple Maps, Google Maps and Airbnb all do
                // exactly this: the finger does ONE thing at a time, and which
                // one is decided by the sheet's height rather than by where the
                // finger landed. Below full height the sheet moves and the list
                // does not scroll, so dragging up over the trees raises the
                // sheet instead of scrolling past them. At full height the list
                // scrolls, and the grabber at the top stays outside the scroll
                // view so there is always a way back down.
                sheet
            }
        }
        // The title used to float over the map as bare text with nothing behind
        // it, and worse, "Near Amsterdam" was a statement of a problem with no
        // way to fix it. It is a chip now, and when we do not know where you
        // are it is the button that finds out.
        // The chips float over the map rather than sitting in the sheet, which
        // is where Google Maps puts them and for the reason this needed moving:
        // inside the sheet they were below the peek height, so the one control
        // that changes what the whole screen shows was invisible until you
        // dragged. A filter you cannot see is a filter nobody uses.
        .overlay(alignment: .top) {
            VStack(spacing: 8) {
                searchField
                whereChip
                filterRow
            }
        }
        .overlay(alignment: .bottom) {
            if sheetHeight == .full {
                Button {
                    withAnimation(.spring(duration: 0.28)) { sheetHeight = .peek }
                } label: {
                    Label("Map", systemImage: "map.fill")
                        .font(.brand(15, .bold))
                        .padding(.horizontal, 18).frame(minHeight: 44)
                        .background(Capsule().fill(Brand.ink))
                        .foregroundStyle(Brand.ground)
                }
                .buttonStyle(.plain)
                // Just above the tab bar, which is where AllTrails and Komoot
                // both float it. At 104 it sat in the MIDDLE of the list and
                // swallowed taps meant for the card underneath it.
                .padding(.bottom, 14)
                .transition(.opacity)
                .accessibilityIdentifier("back-to-map")
            }
        }
        .task {
            if let id = debugSelect, let t = catalogue.tree(id) {
                selected = t
                sheetHeight = .half
            }
        }
        .onChange(of: navigator.showOnMap) { _, new in
            guard let id = new, let t = catalogue.tree(id) else { return }
            selected = t
            sheetHeight = .half
            navigator.showOnMap = nil
        }
        .fullScreenCover(isPresented: $searching) {
            MapSearch(catalogue: catalogue, origin: origin) { hit in
                switch hit {
                case .city(_, _, let lat, let lng):
                    fly(to: lat, lng: lng, span: 6000)
                case .country(let name):
                    // A country has no single point, so go to its biggest city
                    // rather than to the middle of the sea.
                    let ts = catalogue.trees.filter { $0.country == name }
                    if let c = Dictionary(grouping: ts, by: \.citySlug)
                        .max(by: { $0.value.count < $1.value.count })?.value {
                        var la = 0.0, ln = 0.0
                        for t in c { la += t.lat; ln += t.lng }
                        fly(to: la / Double(c.count), lng: ln / Double(c.count), span: 14000)
                    }
                case .species(let name):
                    filters.species = name
                case .tree(let t):
                    fly(to: t.lat, lng: t.lng, span: 1200)
                    selected = t
                }
            }
        }
        .toolbar(.hidden, for: .navigationBar)
        .onChange(of: selected) { _, new in
            // Tapping a pin raises the sheet to that tree, the way Google Maps
            // turns the sheet into the place you tapped.
            if new != nil { sheetHeight = .half }
        }
    }

    /// Close enough to see it. Beyond this the honest thing is to point rather
    /// than to offer a tick, because a tick you can press from your sofa is
    /// worth nothing to collect.
    private let arrivedKm = 0.12

    private var arrived: Tree? {
        guard query.isEmpty, selected == nil,
              let first = listed.first, first.km <= arrivedKm else { return nil }
        return first.tree
    }

    /// What the pager pages over. The tapped tree first if the list does not
    /// already contain it, which happens when somebody taps a pin outside the
    /// sixty the list shows.

    @ViewBuilder private var sheet: some View {
        if selected != nil {
            selectedCard
        } else {
            VStack(spacing: 0) {
                countStrip
                if shownWalk != nil && sheetHeight != .peek { walkCard }
                if let t = arrived, sheetHeight != .peek { arrivalCard(t) }
                list
            }
        }
    }

    /// What the sheet says when it is only a lip: how many trees are under the
    /// map you are looking at. Komoot's "511 hardlooproutes", which Hidde asked
    /// to copy on 2026-08-22, and it does three jobs at once: it says there is
    /// a list down here, it says how big it is, and being unTAPPABLE it makes
    /// the lip a handle rather than a row of half-visible cards a thumb keeps
    /// opening by accident.
    private var countStrip: some View {
        Text(inReach == 0
             ? "No trees in view"
             : "\(inReach) \(inReach == 1 ? "tree" : "trees") you can see")
            .font(.brand(16, .bold))
            .foregroundStyle(Brand.inkSoft)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 10)
            .accessibilityIdentifier("map-count")
    }

    /// The moment the whole product exists for, surfaced where the user already
    /// is instead of in a tab that would sit dead the rest of the month.
    private func arrivalCard(_ t: Tree) -> some View {
        VStack(spacing: 10) {
            Text("You are standing in front of").font(.caption).foregroundStyle(.secondary)
            Text(t.name).font(.title3.bold()).multilineTextAlignment(.center)
            Button {
                saved.toggleVisited(t.id)
                if saved.isVisited(t.id) {
                    nudge.ticked(treeName: t.name,
                                 signedIn: account.isSignedIn,
                                 total: saved.visitedCount)
                }
            } label: {
                Label(saved.isVisited(t.id) ? "Ticked off" : "I have seen this one",
                      systemImage: saved.isVisited(t.id) ? "checkmark.seal.fill" : "checkmark.seal")
                    .font(.subheadline.weight(.semibold))
                    .frame(maxWidth: .infinity).padding(.vertical, 13)
            }
            .buttonStyle(.borderedProminent)
            .tint(saved.isVisited(t.id) ? .gray : Color(red: 0.20, green: 0.35, blue: 0.20))
            .sensoryFeedback(.success, trigger: saved.isVisited(t.id)) { _, now in now }
        }
        .padding(16)
        .background(Color(.secondarySystemBackground), in: .rect(cornerRadius: 14))
        .padding(.horizontal, 16).padding(.bottom, 6)
    }

    private var list: some View {
        LazyVStack(spacing: 12) {
                ForEach(listed, id: \.tree.id) { hit in
                    NavigationLink(value: Route.tree(hit.tree.id)) {
                        TreeCard(tree: hit.tree)
                    }
                    .buttonStyle(.plain)
                    .accessibilityIdentifier("tree-card")
                }
                if listed.isEmpty {
                    Text(query.isEmpty
                         ? (lookingAtYou
                            ? "No tree of ours within fifty kilometres."
                            : "No tree of ours in view. Try moving the map.")
                         : "Nothing matches “\(query)”.")
                        .font(.footnote).foregroundStyle(.secondary).padding(.top, 30)
                }
            }
        .padding(.horizontal, 16)
        .padding(.bottom, 110)      // clear of the floating tab bar
    }

    /// Only the ASK survives here. "Near you" and "Trees in this area" spent
    /// the best strip on the screen telling somebody looking at a map that
    /// they were looking at a map (Hidde, 2026-08-21: "that's the whole app,
    /// so don't waste that space"). When we do not have a location there is
    /// something real to say, so that half stays.
    @ViewBuilder private var whereChip: some View {
        if located {
            EmptyView()
        } else {
            Button {
                if locationDenied {
                    if let u = URL(string: UIApplication.openSettingsURLString) {
                        UIApplication.shared.open(u)
                    }
                } else {
                    onUseMyLocation()
                }
            } label: {
                HStack(spacing: 6) {
                    Image(systemName: "location.slash")
                    Text("Near Amsterdam")
                    Text("·").foregroundStyle(.secondary)
                    Text(locationDenied ? "Turn on location" : "Use my location")
                        .foregroundStyle(Color(red: 0.20, green: 0.35, blue: 0.20))
                }
                .font(.subheadline.weight(.semibold))
                .padding(.horizontal, 14).padding(.vertical, 8)
                .background(.regularMaterial, in: .capsule)
                .shadow(color: .black.opacity(0.12), radius: 6, y: 2)
                .padding(.top, 10)
            }
            .buttonStyle(.plain)
        }
    }

    /// Four filters and no more, deliberately. The map is the one screen where
    /// every control added takes something away from the thing it is for, and
    /// Two chips, and Hidde cut it to two on 2026-08-21: "walking routes make
    /// sense, and species. That's it for the filter for now." What went: at
    /// their best (season is a pulse on the pins, not a filter), with a photo
    /// (the editorial order already leads with pictures) and within 2 km (the
    /// list is distance-ordered anyway). Restoring one is a single line, so
    /// the cost of being wrong here is nothing.
    private var filterRow: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                walkChip
                FilterChip(label: "Collected", icon: "checkmark.seal",
                           on: filters.collectedOnly) { filters.collectedOnly.toggle() }

                Menu {
                    Button("Any species") { filters.species = nil }
                    Divider()
                    ForEach(topSpecies, id: \.self) { sp in
                        Button(sp) { filters.species = sp }
                    }
                } label: {
                    FilterChipLabel(label: filters.species ?? "Species",
                                    icon: "leaf", on: filters.species != nil)
                }

                if filters.isOn {
                    Button {
                        filters = MapFilters()
                    } label: {
                        FilterChipLabel(label: "Clear", icon: "xmark", on: false)
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.horizontal, 14)
        }
        .scrollClipDisabled()
    }

    /// One walk free, the rest behind Plus, which is the rule Entitlement.swift
    /// already states: nobody buys a thing they have never felt. So the nearest
    /// walk draws itself on the map for anybody, and asking for the next one is
    /// what opens the ask.
    @ViewBuilder private var walkChip: some View {
        if !walksHere.isEmpty {
            Button {
                if shownWalk == nil {
                    shownWalk = walksHere.first
                    sheetHeight = .peek
                } else {
                    shownWalk = nil
                }
            } label: {
                FilterChipLabel(label: shownWalk == nil ? "See walking routes" : "Hide the walk",
                                icon: "figure.walk", on: shownWalk != nil)
            }
            .buttonStyle(.plain)
        }
    }

    /// What the map is showing, said in the sheet, with the one thing a walk
    /// needs pinned under it. Begin rather than Directions, and it is the only
    /// coloured control on the screen, per the AllTrails teardown's first
    /// finding.
    @ViewBuilder private var walkCard: some View {
        if let w = shownWalk {
            VStack(alignment: .leading, spacing: 12) {
                HStack(alignment: .firstTextBaseline) {
                    VStack(alignment: .leading, spacing: 2) {
                        Text(w.name).font(.brand(19, .heavy, relativeTo: .title3))
                            .foregroundStyle(Brand.ink)
                        Text(w.city).font(.footnote).foregroundStyle(Brand.inkSoft)
                    }
                    Spacer()
                    Button { shownWalk = nil } label: {
                        Image(systemName: "xmark.circle.fill")
                            .font(.title3).foregroundStyle(Brand.inkSoft)
                    }
                    .buttonStyle(.plain)
                }
                HStack(spacing: 0) {
                    walkStat("\(w.count)", "trees")
                    Divider().frame(height: 26)
                    walkStat(String(format: "%.1f", w.km), "km")
                    Divider().frame(height: 26)
                    walkStat("\(w.minutes)", "min")
                }
                if (w.shape?.count ?? 0) <= 1 {
                    // The same honesty the website prints, and the same reason:
                    // a solid line between trunks claims a path nobody checked.
                    Label("The line shows the order, not the streets. Only about half our walks have a checked route yet.",
                          systemImage: "info.circle")
                        .font(.caption).foregroundStyle(Brand.inkSoft)
                        .fixedSize(horizontal: false, vertical: true)
                }
                Button {
                    navigator.beginWalk = .init(city: w.citySlug, name: w.name)
                } label: {
                    Label("Begin", systemImage: "location.fill")
                }
                .buttonStyle(BrandButtonStyle())
                .accessibilityIdentifier("walk-begin")

                if walksHere.count > 1 {
                    LockedRow(feature: .walkBeyondFirst) {
                        HStack {
                            Text("\(walksHere.count - 1) more walks near here")
                                .font(.subheadline).foregroundStyle(Brand.ink)
                            Spacer()
                            Chip(text: "Plus", tint: Brand.gold)
                        }
                    }
                }
            }
            .padding(16)
            .brandCard()
            .padding(.horizontal, 16).padding(.bottom, 4)
        }
    }

    private func walkStat(_ value: String, _ unit: String) -> some View {
        VStack(spacing: 1) {
            Text(value).font(.brand(17, .bold, relativeTo: .headline))
                .foregroundStyle(Brand.ink).monospacedDigit()
            Text(unit).font(.caption2).foregroundStyle(Brand.inkSoft)
        }
        .frame(maxWidth: .infinity)
    }

    private var topSpecies: [String] {
        Array(Dictionary(grouping: catalogue.trees, by: \.commonName)
            .sorted { $0.value.count > $1.value.count }
            .prefix(14).map(\.key))
    }

    private var searchField: some View {
        Button { searching = true } label: {
            HStack(spacing: 8) {
                Image(systemName: "magnifyingglass")
                    .font(.system(size: 17, weight: .semibold))
                    .foregroundStyle(Brand.ink)
                // The whole sentence rather than one rotating noun (Hidde,
                // 2026-08-22). A word that changes under your eyes is a nice
                // trick on a field you are typing in and a distraction on a
                // button you are only reading.
                Text("Search a city, country or tree")
                    .font(.system(size: 16, weight: .medium))
                    .foregroundStyle(Brand.inkSoft)
                Spacer(minLength: 0)
            }
            .padding(.horizontal, 16).frame(height: 50)
            .background(Brand.surface, in: .capsule)
            .overlay { Capsule().strokeBorder(Brand.hairline, lineWidth: 1) }
            .shadow(color: .black.opacity(0.10), radius: 8, y: 2)
            .padding(.horizontal, 16)
            .padding(.top, 6)
            .contentShape(.capsule)
        }
        .buttonStyle(.plain)
        .accessibilityIdentifier("map-search-field")
    }

    /// The four things a person actually looks for here, one at a time.
    private static let searchWords = ["tree", "city", "park", "country"]
    private var searchWord: String { Self.searchWords[promptIndex] }

    /// One tapped pin, shown in the sheet over the map rather than pushed onto
    /// a page, so the map stays visible behind the decision.
    ///
    /// Cut back to just the card on 2026-08-21. What went, and why: the
    /// sideways PAGER between neighbouring trees (Hidde: "als ik op een boom
    /// sta is het echt onmogelijk om links of rechts te swipen... ik vind het
    /// raar"), the line advertising that gesture, and the close CROSS ("waarom
    /// kan ik op mijn kruisje drukken?"). Google Maps has none of the three:
    /// you tap another pin to switch and drag the sheet down to be rid of it.
    /// The button under the card went too, because a card that opens when you
    /// tap it does not need a label saying it opens when you tap it.
    @ViewBuilder private var selectedCard: some View {
        if let t = selected {
            VStack(spacing: 0) {
                NavigationLink(value: Route.tree(t.id)) {
                    TreeCard(tree: t)
                }
                .buttonStyle(.plain)
                .accessibilityIdentifier("tree-card")
                Color.clear.frame(height: 100)      // clear of the floating tab bar
            }
            .padding(.horizontal, 16)
        }
    }
}
