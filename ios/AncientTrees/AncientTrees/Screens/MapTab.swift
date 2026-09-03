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

struct MapTab: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    let located: Bool
    /// iOS has been asked and said no. A different sentence from "not yet
    /// asked", because the only way out of this one is Settings.
    var locationDenied: Bool = false
    var onUseMyLocation: () -> Void = {}

    /// The recovery sheet, nil when shut. See PermissionRecovery.
    @State private var refused: Permission?
    /// Debug scaffolding, same family as -spot: the sheet only exists after a
    /// refusal the simulator cannot produce on demand, so appsweep can open it.
    @State private var debugRefused =
        ProcessInfo.processInfo.arguments.contains("-refused")

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
        // -sheet=half as well as -sheet=full, since 2026-08-27: the App Store
        // screenshot of the map wants the shape a person actually uses, a card
        // you can read over a map you can see, and peek shows a sliver of one
        // photograph.
        ProcessInfo.processInfo.arguments.contains("-sheet=full") ? .full
            : (ProcessInfo.processInfo.arguments.contains("-sheet=half") ? .half
               : (ProcessInfo.processInfo.arguments.contains("-sheet=card") ? .card : .peek))
    @State private var query = ""
    /// When the map was last moved on purpose, so the list's own settling
    /// cannot move it back. See fly().
    @State private var flewAt: Date?
    @State private var askingPlus = false
    /// Debug scaffolding, same family as -spot: the search page is only
    /// reachable by tapping and simctl has no finger. `-search` opens it empty,
    /// `-search=lis` opens it with that typed.
    /// Debug scaffolding, same family as -tab, -select and -collected: simctl
    /// cannot tap, and a sheet that only exists after a tap is a sheet that
    /// ships unlooked at. It shipped that way once and froze the app.
    /// The card at the top of the list, reported by the sheet as you scroll.
    @State private var topCard: String?
    @State private var pickingSpecies = ProcessInfo.processInfo.arguments.contains("-species")
    @State private var searching = ProcessInfo.processInfo.arguments
        .contains { $0 == "-search" || $0.hasPrefix("-search=") }
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
    @Environment(Sightings.self) private var sightings

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
        guard Launch.walks else { return [] }
        return catalogue.walks.compactMap { w -> (Walk, Double)? in
            // NEAREST STOP, not the first one. Judging a walk by its first tree
            // made it flicker in and out while the list was scrolled, because
            // scrolling the list moves the map, and a walk whose first stop
            // left the view vanished while four of its other stops were still
            // on screen (Hidde, 2026-08-25, in The Hague: "als ik hem naar
            // beneden scrolle, zie ik geen walking route, als ik hem naar boven
            // scrolle wel, dus dat gaat fout"). A walk is here when any part of
            // it is here, which is also what somebody looking at the map means.
            let stops = catalogue.trees(of: w)
            guard !stops.isEmpty else { return nil }
            let nearest = stops.map { $0.distanceKm(from: focus.lat, focus.lng) }.min()!
            return (w, nearest)
        }
        // Within the VIEW, not within sixty kilometres. Standing in Amsterdam
        // that radius swept up the whole Randstad and the shelf said "23 walks
        // here", which is not a count of anything a person can see (Hidde,
        // 2026-08-24: "dat zijn er veel te veel"). Floored so a street-level
        // view still finds the walk you are standing on.
        .filter { $0.1 < max(reachKm, 3) }
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
            filters.keeps($0, month: month, collected: collectedIds, favourites: favouriteIds)
                && filters.keepsDistance($0.distanceKm(from: focus.lat, focus.lng))
        }
    }

    private var month: Int { Calendar.current.component(.month, from: Date()) }
    /// The ids you have collected, worked out once per redraw rather than
    /// asked per tree while filtering fifteen hundred of them.
    private var collectedIds: Set<String> {
        Set(saved.entries.values.filter { $0.visitedAt != nil }.map(\.treeId))
    }
    private var favouriteIds: Set<String> {
        Set(saved.favourites.map(\.treeId))
    }
    /// The point the list is about: where the map is looking once it has been
    /// moved, and where you are standing until then.
    private var focus: (lat: Double, lng: Double) {
        guard let c = mapRegion?.center else { return origin }
        return (lat: c.latitude, lng: c.longitude)
    }

    /// How far the list looks: WHAT IS ON SCREEN.
    ///
    /// It used to be `max(50, ...)`, a fifty kilometre floor whatever the zoom,
    /// so panning across a city changed nothing and the list quietly described
    /// the province (Hidde, 2026-08-24: "als ik op de kaart ga swipen of zoek
    /// of mijn view verander moeten de bomen meeveranderen naar degene die in
    /// mijn view staan"). The floor was there for a real reason, that a street
    /// level view holds four trees and a list of four looks broken, and that
    /// reason is answered in `listed` by topping up rather than by lying about
    /// where the list is looking.
    /// The map's own rectangle, a little generous at the edges so a pin half
    /// under the sheet still counts as on screen.
    private struct Box {
        let minLat, maxLat, minLng, maxLng: Double
        func contains(_ lat: Double, _ lng: Double) -> Bool {
            lat >= minLat && lat <= maxLat && lng >= minLng && lng <= maxLng
        }
    }

    private var visibleBox: Box {
        guard let r = mapRegion else {
            // No region yet: a small box around where we think we are, rather
            // than the whole world, so the first draw is not the entire map.
            return Box(minLat: origin.lat - 0.05, maxLat: origin.lat + 0.05,
                       minLng: origin.lng - 0.08, maxLng: origin.lng + 0.08)
        }
        let dLat = r.span.latitudeDelta / 2
        let dLng = r.span.longitudeDelta / 2
        return Box(minLat: r.center.latitude - dLat, maxLat: r.center.latitude + dLat,
                   minLng: r.center.longitude - dLng, maxLng: r.center.longitude + dLng)
    }

    private var reachKm: Double {
        guard let s = mapRegion?.span else { return 5 }
        return max(0.5, s.latitudeDelta * 111.0 / 2)
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
        // AND CUT THE BACK-CHANNEL for a moment. Scrolling the list moves the
        // map to whatever card reaches the top, which is his own 2026-08-24 ask
        // and which fights a deliberate move: flying to an olive tree in Sicily
        // re-laid the list, the scroll view settled on whatever card it still
        // held, that card reported itself as the top one, and the map was pulled
        // straight back to Baarn (Hidde, 2026-08-25: "waarom staat de lijst nog
        // steeds Kantonspark en Trees uit Baarn... die lijst moet meebewegen met
        // de content op de map"). The list follows the map; the map does not
        // follow the list's own settling.
        topCard = nil
        flewAt = Date()
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
                filters.keeps($0, month: month, collected: collectedIds, favourites: favouriteIds)
                    && $0.distanceKm(from: focus.lat, focus.lng) <= 6
            }.count
        }
        let latMin = r.center.latitude - r.span.latitudeDelta / 2
        let latMax = r.center.latitude + r.span.latitudeDelta / 2
        let lngMin = r.center.longitude - r.span.longitudeDelta / 2
        let lngMax = r.center.longitude + r.span.longitudeDelta / 2
        return catalogue.trees.filter {
            $0.lat >= latMin && $0.lat <= latMax && $0.lng >= lngMin && $0.lng <= lngMax
                && filters.keeps($0, month: month, collected: collectedIds, favourites: favouriteIds)
        }.count
    }

    private var listed: [(tree: Tree, km: Double)] {
        // WHAT IS ON SCREEN, and nothing else (Hidde, 2026-08-26, twice in a
        // row: "zodra je scrolt in je map moet je resultaat goed meescrollen"
        // and then "ook moet je alleen de bomen zien die in je beeld staan, hij
        // scrolt nu naar allemaal bomen door die ik helemaal niet zie").
        //
        // Two things were wrong and the second was the one he could feel. The
        // list asked for a RADIUS around the centre, so the corners of the
        // screen were never in it and a strip beyond the top and bottom edges
        // always was. And when a close view held fewer than eight trees it
        // widened that radius to eight times the view or fifty kilometres,
        // whichever was larger, which is a list of a province wearing the
        // heading of a street. That top-up was written to stop a street level
        // view reading as an empty app, and it bought that at the price of the
        // list telling the truth. An honest short list is the better trade: it
        // says "there are two trees here", which is a fact somebody can act on
        // by zooming out.
        //
        // The rectangle comes from the map's own region, so panning and
        // zooming change it by definition and the list cannot drift away from
        // what the eye sees.
        let box = visibleBox
        let near = catalogue.trees
            .filter { box.contains($0.lat, $0.lng) }
            .filter { filters.keeps($0, month: month, collected: collectedIds, favourites: favouriteIds) }
            .map { ($0, $0.distanceKm(from: focus.lat, focus.lng)) }
            .filter { filters.keepsDistance($0.1) }
            .sorted { $0.1 < $1.1 }
            .prefix(60)
            .map { (tree: $0.0, km: $0.1) }
        guard !query.isEmpty else {
            return Editorial.leadWithAPhotograph(near, photo: { $0.tree.photo != nil })
        }
        let q = query.lowercased()
        return catalogue.trees
            .filter { $0.name.lowercased().contains(q) || $0.city.lowercased().contains(q)
                      || $0.species.lowercased().contains(q) }
            .filter { filters.keeps($0, month: month, collected: collectedIds, favourites: favouriteIds)
                        && filters.keepsDistance($0.distanceKm(from: focus.lat, focus.lng)) }
            .prefix(40)
            .map { ($0, $0.distanceKm(from: focus.lat, focus.lng)) }
    }

    var body: some View {
        // THE SHARED COMPONENT (Hidde, 2026-08-26: "je wilt deze interactie als
        // component hebben en overal hetzelfde hebben"). This screen is where
        // the arrangement was argued out; My trees now uses the same one, and
        // it only stays the same if there is one of it.
        MapWithSheet(height: $sheetHeight, topItem: $topCard) {
            TreeMap(trees: shownWalk.map { catalogue.trees(of: $0) } ?? mapTrees,
                    mine: mineShown.map { (id: $0.id, lat: $0.lat, lng: $0.lng, name: $0.name,
                                           photo: sightings.image($0)) },
                    collected: collectedIds,
                    favourites: favouriteIds,
                    onLocationRefused: { refused = .location },
                    onSelectMine: { navigator.push = .mine($0) },
                    onSelectTree: { navigator.push = .tree($0) },
                    focus: .init(latitude: origin.lat, longitude: origin.lng),
                    // So the map can tell a fix from Dam square and retake its
                    // opening shot when the phone finally answers. See
                    // TreeMap.focusIsFix.
                    focusIsFix: located,
                    route: walkRoute,
                    routeIsReal: (shownWalk?.shape?.count ?? 0) > 1,
                    // Not while the sheet covers the map. It is a control on a
                    // surface nobody can see at that height, and it climbed up
                    // among the chips trying to stay above the sheet.
                    showsRecentre: sheetHeight != .full,
                    // Off while a walk is on screen, for the same reason as on
                    // the walk page itself: its stops must stay countable.
                    clusters: shownWalk == nil,
                    region: $mapRegion,
                    moveTo: moveRequest,
                    selected: $selected)
                .accessibilityIdentifier("tree-map")
        } header: {
                // The count is the header now, outside the scroll view: it stays
                // visible while the list scrolls and it is the handle that makes
                // the sheet draggable again once it has (2026-08-25).
                countStrip
        } content: {
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
        // AT FULL HEIGHT ONLY, which is his own correction within the minute:
        // "de map floating knop op de map pagina is overbodig" and then, having
        // pulled the list all the way up, "de knop maakt sense als je de lijst
        // helemaal naar boven trekt, hou hem dan maar de rest niet" (2026-08-25).
        // Both readings are right about their own case: at peek, card and half
        // the map is there to be tapped, and at full there are 124 points of it
        // left behind a chip row.
        //
        // What today's other fix bought stays bought: it used to sit at 14
        // points off the bottom, entirely behind the tab bar, existing and
        // invisible and swallowing the tap meant for the sheet.
        .overlay(alignment: .bottom) {
            if sheetHeight == .full {
                Button {
                    withAnimation(.spring(duration: 0.28)) { sheetHeight = .peek }
                } label: {
                    Label("Map", systemImage: "map.fill")
                        .font(.brand(15, .bold))
                        .padding(.horizontal, 18).frame(minHeight: 44)
                        // THE SAME MATERIAL THE TAB BAR WEARS, not an inverted
                        // fill. It was Brand.ink filled with Brand.ground text,
                        // which in daylight is a dark pill on a pale sheet and
                        // in the dark is a WHITE one: the brightest thing on
                        // the screen, and it is a secondary control. A material
                        // is what every map app floats over content, because it
                        // blurs whatever it lands on and therefore separates
                        // from a photograph and from the sheet alike.
                        .background(Capsule().fill(.regularMaterial))
                        .foregroundStyle(Brand.ink)
                        .shadow(color: .black.opacity(0.18), radius: 8, y: 2)
                }
                .buttonStyle(.plain)
                .padding(.bottom, 70)
                .transition(.opacity)
                .accessibilityIdentifier("back-to-map")
            }
        }
        .task {
            if let id = debugSelect, let t = catalogue.tree(id) {
                selected = t
                sheetHeight = .card
            }
        }
        // Scrolling the list moves the map to whatever you have reached, so
        // reading down the list is the same gesture as walking along it.
        //
        // Guarded against its own tail: moving the map changes what is in view,
        // which changes the list, which could change the top card and move the
        // map again. It only flies when the tree is genuinely off-centre, which
        // a small correction never is.
        .onChange(of: topCard) { _, new in
            // Not while a deliberate move is still settling. A scroll view
            // re-laid under a new list reports a top item that nobody chose.
            if let flewAt, Date().timeIntervalSince(flewAt) < 2.0 { return }
            guard let id = new, let t = catalogue.tree(id) else { return }
            let span = mapRegion?.span.latitudeDelta ?? 0.02
            guard Geo.km(focus, (t.lat, t.lng)) > span * 111.0 * 0.25 else { return }
            moveRequest = (token: UUID(),
                           region: MKCoordinateRegion(
                               center: .init(latitude: t.lat, longitude: t.lng),
                               span: mapRegion?.span
                                   ?? MKCoordinateSpan(latitudeDelta: 0.02, longitudeDelta: 0.02)))
        }
        .onChange(of: navigator.showCityOnMap) { _, new in
            guard let slug = new else { return }
            let here = catalogue.trees.filter { $0.citySlug == slug }
            navigator.showCityOnMap = nil
            guard !here.isEmpty else { return }
            // The city's own frame, the same arithmetic the city page's preview
            // uses: the middle of its trees, wide enough to hold them all.
            let lats = here.map(\.lat), lngs = here.map(\.lng)
            let centre = CLLocationCoordinate2D(
                latitude: (lats.min()! + lats.max()!) / 2,
                longitude: (lngs.min()! + lngs.max()!) / 2)
            let span = MKCoordinateSpan(
                latitudeDelta: max(lats.max()! - lats.min()!, 0.01) * 1.4,
                longitudeDelta: max(lngs.max()! - lngs.min()!, 0.01) * 1.4)
            selected = nil
            shownWalk = nil
            filters = MapFilters()
            query = ""
            sheetHeight = .peek
            moveRequest = (token: UUID(), region: MKCoordinateRegion(center: centre, span: span))
        }
        .onChange(of: navigator.showOnMap) { _, new in
            guard let id = new, let t = catalogue.tree(id) else { return }
            selected = t
            sheetHeight = .card
            navigator.showOnMap = nil
        }
        .sheet(isPresented: $askingPlus) {
            PaywallView(feature: .walkBeyondFirst)
        }
        .sheet(item: $refused) { PermissionRecovery(permission: $0) }
        .onAppear { if debugRefused { debugRefused = false; refused = .location } }
        .sheet(isPresented: $pickingSpecies) {
            SpeciesPicker(catalogue: catalogue,
                          nearby: Array(Set(mapTrees.map(\.commonName))),
                          selection: Binding(get: { filters.species },
                                             set: { new in
                                                 filters = MapFilters()
                                                 filters.species = new
                                                 if new != nil { shownWalk = nil }
                                             }))
        }
        .fullScreenCover(isPresented: $searching) {
            MapSearch(catalogue: catalogue, origin: origin) { hit in
                switch hit {
                case .city(let slug, _, let lat, let lng):
                    // STAY ON THE MAP (Hidde, 2026-08-24: "dan moet je niet een
                    // stadspagina openen in een nieuw venster, dat moet juist
                    // gewoon een overlay zijn op de kaart... je moet net als bij
                    // web niet het gevoel hebben dat je naar een andere pagina
                    // gaat"). I had made this push the city page an hour
                    // earlier, which answered a different complaint and broke
                    // this one. The map holds its place and simply looks at the
                    // city; its trees and its walks arrive in the sheet
                    // underneath, which is what a city IS here.
                    let ts = catalogue.trees.filter { $0.citySlug == slug }
                    if let first = ts.first {
                        var minLat = first.lat, maxLat = first.lat
                        var minLng = first.lng, maxLng = first.lng
                        for t in ts {
                            minLat = min(minLat, t.lat); maxLat = max(maxLat, t.lat)
                            minLng = min(minLng, t.lng); maxLng = max(maxLng, t.lng)
                        }
                        let cLat = (minLat + maxLat) / 2, cLng = (minLng + maxLng) / 2
                        let latM = (maxLat - minLat) * 111_320
                        let lngM = (maxLng - minLng) * 111_320 * cos(cLat * .pi / 180)
                        fly(to: cLat, lng: cLng,
                            span: max(1_500, min(max(latM, lngM) * 1.35, 60_000)))
                    } else {
                        fly(to: lat, lng: lng, span: 6000)
                    }
                case .country(let name):
                    // The COUNTRY in view, not its biggest city. It used to fly
                    // to whichever city had the most trees, so searching Spain
                    // showed you Barcelona and nothing else: a country is a
                    // question about spread, and the answer is the whole
                    // spread.
                    let ts = catalogue.trees.filter { $0.country == name }
                    if let first = ts.first {
                        var minLat = first.lat, maxLat = first.lat
                        var minLng = first.lng, maxLng = first.lng
                        for t in ts {
                            minLat = min(minLat, t.lat); maxLat = max(maxLat, t.lat)
                            minLng = min(minLng, t.lng); maxLng = max(maxLng, t.lng)
                        }
                        let cLat = (minLat + maxLat) / 2, cLng = (minLng + maxLng) / 2
                        let latM = (maxLat - minLat) * 111_320
                        let lngM = (maxLng - minLng) * 111_320 * cos(cLat * .pi / 180)
                        fly(to: cLat, lng: cLng,
                            span: max(20_000, min(max(latM, lngM) * 1.25, 2_500_000)))
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
            // Tapping a pin raises the sheet and puts that tree at the top of
            // the list, rather than making it the only thing in it.
            if let t = new {
                if sheetHeight == .peek { sheetHeight = .half }
                topCard = t.id
            }
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

    /// ONE sheet, always the list.
    ///
    /// Tapping a pin used to REPLACE the list with that single card, so the
    /// other trees in view disappeared and there was nothing to scroll (Hidde,
    /// 2026-08-24: "je wilt naar beneden kunnen scrollen om de rest van de
    /// bomen te zien in je beeld, en dat de kaart mee hovert naar die andere
    /// boom als je door de lijst gaat"). The list now scrolls TO the tapped
    /// tree instead, and scrolling it moves the map, which is the vertical
    /// version of the sideways pager he had removed on 2026-08-21 and the
    /// arrangement Google Maps and Apple Maps both use.
    @ViewBuilder private var sheet: some View {
        VStack(spacing: 0) {
            if shownWalk != nil && sheetHeight != .peek { walkCard }
            if let t = arrived, sheetHeight != .peek { arrivalCard(t) }
            list
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
                // Ticking is collecting, and collecting needs the account
                // (Hidde, 2026-08-25, on hearts working while signed out:
                // "all these functionalities of saving stuff should only be
                // available when you sign in"). Gating the heart and leaving
                // this open would be the same bug with a different button.
                guard account.isSignedIn else {
                    nudge.require(.keepTree(t.name))
                    return
                }
                saved.toggleVisited(t.id)
            } label: {
                Label(saved.isVisited(t.id) ? "Ticked off" : "I have seen this one",
                      systemImage: saved.isVisited(t.id) ? "checkmark.seal.fill" : "checkmark.seal")
                    .font(.subheadline.weight(.semibold))
                    .frame(maxWidth: .infinity).padding(.vertical, 13)
            }
            .buttonStyle(.borderedProminent)
            .tint(saved.isVisited(t.id) ? Color(Brand.inkSoft) : Brand.canopy)
            .sensoryFeedback(.success, trigger: saved.isVisited(t.id)) { _, now in now }
        }
        .padding(16)
        .background(Brand.surfaceMuted, in: .rect(cornerRadius: 14))
        .padding(.horizontal, 16).padding(.bottom, 6)
    }

    /// Yours, through the same filters ours go through.
    ///
    /// The pins and the list read this one property, because the bug it fixes
    /// was exactly two places reading the store direct and neither of them
    /// asking `filters` anything (2026-08-27).
    private var mineShown: [Sightings.Sighting] {
        sightings.yoursOnly.filter {
            filters.keeps($0, favourites: favouriteIds)
                && filters.keepsDistance(Geo.km(focus, ($0.lat, $0.lng)))
        }
    }

    /// Yours, near where the map is looking. They live on their own layer on
    /// the map and were missing from the list entirely, which made them feel
    /// like decoration rather than trees.
    private var minesInView: [Sightings.Sighting] {
        mineShown
            .filter { Geo.km(focus, ($0.lat, $0.lng)) <= reachKm }
            .sorted { Geo.km(focus, ($0.lat, $0.lng)) < Geo.km(focus, ($1.lat, $1.lng)) }
    }

    /// Put a walk on screen whole.
    ///
    /// Hidde, 2026-08-25: "if I press walking routes on the map screen, it would
    /// make sense that the map zooms out to place that walk exactly in the
    /// middle of your screen." It drew the line and left the camera wherever it
    /// happened to be, so a walk two streets away was a green thread leaving the
    /// corner of the screen. The bottom inset the camera now carries means the
    /// middle it aims for is the middle of the part you can SEE, not the middle
    /// of the map behind the sheet.
    private func frame(_ w: Walk) {
        let stops = catalogue.trees(of: w)
        guard !stops.isEmpty else { return }
        let lats = stops.map(\.lat), lngs = stops.map(\.lng)
        let centre = CLLocationCoordinate2D(latitude: (lats.min()! + lats.max()!) / 2,
                                            longitude: (lngs.min()! + lngs.max()!) / 2)
        // A fifth of air around it, and a floor so a walk of one street does not
        // arrive at maximum zoom.
        let span = MKCoordinateSpan(
            latitudeDelta: max((lats.max()! - lats.min()!) * 1.4, 0.004),
            longitudeDelta: max((lngs.max()! - lngs.min()!) * 1.4, 0.004))
        moveRequest = (token: UUID(), region: MKCoordinateRegion(center: centre, span: span))
    }

    /// The walks where the map is looking, as the shelf a city page uses.
    ///
    /// The sheet used to hold trees and nothing else, so a walk existed only
    /// behind a chip that drew a line. After searching a city you want what the
    /// city HAS, which is its walks and its trees, and that is the same shape
    /// the city page and the website both carry.
    @ViewBuilder private var walkShelf: some View {
        // Shown even while a walk is drawn, because choosing a DIFFERENT one
        // was impossible otherwise: the chip picks the first and the shelf
        // vanished the moment it did (Hidde, 2026-08-25: "je moet namelijk de
        // walking kunnen selecteren"). Amsterdam has three.
        if query.isEmpty, walksHere.count > 1 || shownWalk == nil, !walksHere.isEmpty {
            VStack(alignment: .leading, spacing: 8) {
                Text(walksHere.count == 1 ? "1 walk here" : "\(walksHere.count) walks here")
                    .font(.brand(17, .bold, relativeTo: .headline))
                    .foregroundStyle(Brand.ink)
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(alignment: .top, spacing: 12) {
                        ForEach(walksHere.prefix(6), id: \.name) { w in
                            // Tapping SELECTS: it draws that walk on the map
                            // and puts its card in the sheet. Free, because
                            // looking at a route is how anybody decides whether
                            // it is worth having, and Begin on the card below is
                            // where Plus still stands (Hidde, 2026-08-25: make
                            // the route available in the list, "en weer achter
                            // plus gooien"). Before this, every card here went
                            // straight to the paywall, so with three walks in
                            // Amsterdam you could see the first one and no other.
                            Button {
                                filters = MapFilters()
                                shownWalk = w
                                frame(w)
                                if sheetHeight == .peek { sheetHeight = .card }
                            } label: {
                                CityWalkCard(walk: w, locked: true,
                                             selected: shownWalk?.name == w.name)
                            }
                            .buttonStyle(.plain)
                        }
                    }
                    .padding(.bottom, 2)
                }
            }
            .padding(.bottom, 4)
        }
    }

    private var list: some View {
        LazyVStack(spacing: 12) {
                // Not at peek. The lip is a HANDLE (see countStrip): at 168
                // points the walks row and the tops of its cards were the only
                // thing visible, so the sheet looked like a row of controls,
                // and a tap on one of them raised the sheet instead of opening
                // it, which is the "one tap does nothing, the second opens the
                // tree underneath" Hidde reported on 2026-08-25. It also ate
                // the whole photograph the lip is meant to show.
                if sheetHeight != .peek { walkShelf }
                // Yours first: there are few of them and nobody else has them.
                if query.isEmpty {
                    ForEach(minesInView) { s in
                        SheetLink(route: .mine(s.id)) { MineCard(sighting: s) }
                    }
                }
                ForEach(listed, id: \.tree.id) { hit in
                    // SheetLink, not NavigationLink: see BottomSheet.swift. A
                    // link inside a sheet opens on release even when the drag
                    // that released it was raising the sheet.
                    SheetLink(route: .tree(hit.tree.id)) { TreeCard(tree: hit.tree) }
                        .accessibilityIdentifier("tree-card")
                        .id(hit.tree.id)
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
                // Not straight to Settings any more. Apple Maps puts a sheet
                // in between, and that sheet is the one chance to say what you
                // are missing to somebody who has already said no once. See
                // PermissionRecovery and CONVENTIONS.md.
                if locationDenied {
                    refused = .location
                } else {
                    onUseMyLocation()
                }
            } label: {
                HStack(spacing: 6) {
                    Image(systemName: "location.slash")
                    // No place name. It said "Near Amsterdam", which was true
                    // of the old hardcoded fallback and is not true now that
                    // the map opens on the last fix this phone had (Hidde in
                    // Baarn, 2026-08-25). Naming the wrong town is worse than
                    // naming none, and the useful half of this chip was always
                    // the action beside it.
                    Text("Location off")
                    Text("·").foregroundStyle(.secondary)
                    Text(locationDenied ? "Turn on location" : "Use my location")
                        // Brand.moss, which lightens in the dark. It was a
                        // fixed dark green, and this chip sits on a material:
                        // in the dark that is dark green on dark grey, which is
                        // the one word on the chip you are meant to tap.
                        .foregroundStyle(Brand.moss)
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
                // ONE chip. Collected and Yours stood next to each other here
                // and meant almost the same thing; adding a tree collects it,
                // so they are one set. The word is the state a pin is in,
                // which is what a filter chip is for; the tab keeps the word
                // Yours, which is a place.
                // It said "Your trees" for an hour this afternoon, to match a
                // tab called Yours. That tab is called Collection now, so the
                // word follows it: collect (the deed, which has no word at
                // all), collected (the state a pin is in), collection (the
                // place they live). One root, three forms, no "yours" left
                // anywhere. Hidde asked for "your trees" when the tab still
                // said Yours; this follows the reason rather than the word.
                // BOTH OF THESE ARE ABOUT A COLLECTION, so signed out they
                // ask for the account rather than filtering to nothing (Hidde,
                // 2026-08-29: "als je uitgelogd op favourites of my trees
                // filter klikt moet er ook een inlog scherm opkomen"). The
                // filter is not broken while you are signed out, it is empty,
                // and a control that quietly empties the map is worse than one
                // that says what it needs. Same gate as the heart and the
                // camera, through the same nudge.
                FilterChip(label: "Favourites", icon: "heart",
                           on: filters.favouritesOnly) {
                    guard account.isSignedIn else {
                        nudge.require(.general)
                        return
                    }
                    let want = !filters.favouritesOnly
                    filters = MapFilters()
                    filters.favouritesOnly = want
                }
                // "My trees" here too, so the map and the page agree about
                // what the word means (Hidde, 2026-08-26). One root, one word.
                FilterChip(label: "My trees", icon: "checkmark.seal",
                           on: filters.collectedOnly) {
                    guard account.isSignedIn else {
                        nudge.require(.general)
                        return
                    }
                    let want = !filters.collectedOnly
                    filters = MapFilters()
                    filters.collectedOnly = want
                    if want { shownWalk = nil }
                }

                // A chip, so it behaves like the chips beside it: off, tap to
                // choose; on, tap to clear; tap again to choose afresh (Hidde,
                // 2026-08-25). It used to reopen the sheet whatever state it
                // was in, which is a menu wearing a filter's clothes, and it
                // left clearing a filter to a Clear chip that is now gone.
                Button {
                    if filters.species != nil {
                        filters.species = nil
                    } else {
                        pickingSpecies = true
                    }
                } label: {
                    FilterChipLabel(label: filters.species ?? "Species",
                                    icon: "leaf", on: filters.species != nil)
                }
                .buttonStyle(.plain)
                .accessibilityLabel(filters.species == nil
                                    ? "Filter by species"
                                    : "Species: \(filters.species!). Tap to clear")

                // No Clear chip. It appeared the moment any filter went on,
                // which read as a cross growing out of the chip you had just
                // tapped (Hidde, 2026-08-25: "dat kruisje is niet nodig, ik
                // kan gewoon selecteren en deselecteren"). Every filter here
                // turns itself off: the chips toggle, and the species sheet
                // carries "Any species".
            }
            // 16, like the search field above it and the cards below it.
            // It was 14, and appfit had been reporting exactly that for hours
            // ("starts at x=14 while 3 other things on this screen start at
            // x=16") while I read past it. The check was not the thing that
            // failed here.
            .padding(.horizontal, 16)
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
                    // ONE of the three at a time (Hidde, 2026-08-24). Not
                    // tidiness: a walk shown WHILE the map is filtered to the
                    // trees you have collected loses the stops you have not,
                    // so the route on screen is not the route. Every
                    // combination of these three is either that or a filter
                    // nobody asked for.
                    filters = MapFilters()
                    shownWalk = walksHere.first
                    if let w = walksHere.first { frame(w) }
                    // .card, not .peek. It drew a route on the map and then
                    // shrank the sheet to a lip, so the walk existed as a line
                    // and nowhere else: "ik heb nu op walking routes geklikt op
                    // de map, dan zie ik dus een walking route in Amsterdam,
                    // maar dan zie ik hem vervolgens niet in de lijst eronder"
                    // (Hidde, 2026-08-25). The list has to represent what the
                    // map is showing, and .card is exactly the height of one
                    // card, which is what this is.
                    sheetHeight = .card
                } else {
                    shownWalk = nil
                }
            } label: {
                // One label in both states (Hidde, 2026-08-25: "ik denk dat
                // het filter eigenlijk walking routes moet heten... en je
                // hoeft ook niet hide walking routes"). It said "See walking
                // routes" and then "Hide walking routes", which is a verb a
                // filter chip does not need: the chip is already filled when
                // it is on, and every filter row in every app anybody has used
                // works that way. What the 08-24 note above was right about
                // was the PLURAL, and that survives.
                FilterChipLabel(label: "Walking routes",
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
                    // The fraction is a fact and facts move: 48 more walks got
                    // a checked route on 2026-08-25, which took it from about a
                    // half to about three quarters. Begin fetches a live route
                    // for the rest, so this line is about the preview above it.
                    Label("The line shows the order, not the streets. About three quarters of our walks have a checked route; Begin works one out for the rest.",
                          systemImage: "info.circle")
                        .font(.caption).foregroundStyle(Brand.inkSoft)
                        .fixedSize(horizontal: false, vertical: true)
                }
                // PREVIEW FREE, WALKING BEHIND PLUS (Hidde, 2026-08-25: "het is
                // goed als je een preview geeft van de wandeling maar daarna als
                // je klikt niet naar google maps gaan maar naar plus, coming soon
                // verwijzen"). Seeing the route on the map is how anybody decides
                // whether it is worth having; walking it is the thing his own
                // pricing sells. Begin used to open our walk mode, whose way to
                // the next tree is a hand-off to a maps app, so the paid feature
                // ended in somebody else's product.
                Button { askingPlus = true } label: {
                    Label("Begin", systemImage: "location.fill")
                }
                .buttonStyle(BrandButtonStyle())
                .accessibilityIdentifier("walk-begin")

                if walksHere.count > 1 {
                    LockedRow(feature: .walkBeyondFirst, lockGlyph: false) {
                        HStack {
                            Text("\(walksHere.count - 1) more "
                                 + (walksHere.count == 2 ? "walk" : "walks")
                                 + " near here")
                                .font(.subheadline).foregroundStyle(Brand.ink)
                            Spacer()
                            Chip(text: "Plus", tint: Brand.goldInk)
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
                Text(Search.placeholder)
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

}
