// The map, on MapLibre since 2026-08-23, and the reason is offline rather than
// looks. The paywall sells "Download interactive maps and routes to explore with
// confidence, even deep in the woods", Entitlement.swift already carries
// Feature.offlineDownload with the ask "Keep this city in your pocket", and
// MapKit has no API for any of it: Apple's tiles cannot be pre-downloaded and
// their terms do not permit caching them. MapLibre can, and it renders the same
// style file the website does, from the same OpenFreeMap tiles.
//
// Hidde approved the dependency knowing it is the app's first (2026-08-23). It
// costs nothing: BSD-2-Clause, a binary xcframework, no key and no account.
//
// The public interface of TreeMap is deliberately UNCHANGED from the MapKit
// version, MKCoordinateRegion included. That struct is just a centre and a span,
// it ships with iOS, and keeping it meant MapTab, WalkMode and TreeDetail did
// not have to be touched at all. Only the rendering moved.
//
// Clustering is why MKMapView was chosen in the first place, so it is the thing
// to check first on any change here: MapLibre clusters on the SOURCE, with the
// same configuration the website's map uses, which is one behaviour for both
// surfaces instead of two.

import SwiftUI
import MapKit      // MKCoordinateRegion only, as the coordinate-exchange type
import MapLibre

struct TreeMap: UIViewRepresentable {
    let trees: [Tree]
    /// Trees only THIS person has: photographed by them, ours or not. Drawn as
    /// their own pins so the two layers are legible as two layers, which is
    /// Hidde's own distinction (2026-08-21).
    var mine: [(id: UUID, lat: Double, lng: Double, name: String, photo: UIImage?)] = []
    /// Ours that you have already stood in front of. Only changes the pin.
    var collected: Set<String> = []
    /// The trees you have hearted, so a favourite is visible on the map itself
    /// rather than only in a list (Hidde, 2026-08-27: "kun je de bomen die je
    /// gefavoriet hebt een hartje icoon geven zoals de ticket op de map").
    var favourites: Set<String> = []
    /// Tapping a tree of your own opens its page, the same as one of ours.
    /// A callback because this view knows nothing about navigation.
    var onSelectMine: ((UUID) -> Void)? = nil
    /// Tapping one of OURS, when the caller wants the page rather than a
    /// selection (Hidde, 2026-08-25: "im not able to click on a tree on the map,
    /// it should open the deeper tree page"). A pin tap used to select the tree,
    /// which raised the sheet and put its card at the top of the list, so
    /// reaching the page took a second tap on a card that had just moved. His
    /// own trees already opened straight away, so the two kinds of pin behaved
    /// differently for no reason a reader could see.
    ///
    /// It stays a callback rather than becoming the default because SELECTION is
    /// still what the search result and the debug argument want: those move the
    /// camera and leave you on the map, which is his 2026-08-24 ruling.
    var onSelectTree: ((String) -> Void)? = nil
    var focus: CLLocationCoordinate2D?
    /// A walk's line. Real when route_walks.py cached a routed shape, otherwise
    /// the order the trees are visited, which is NOT the path a walker takes.
    var route: [CLLocationCoordinate2D] = []
    var routeIsReal = true
    /// The control that puts the map back: you in the middle, north at the top.
    ///
    /// ON BY DEFAULT since 2026-08-29, and that is the whole rule (Hidde: "die
    /// moet overal waar je de kaart gebruikt aanwezig zijn"). It used to be off
    /// by default and switched on by hand, so it existed on the map tab and the
    /// walk and on none of the other eight maps in this app: the tree's own map,
    /// a city's, a country's, My trees, the collection map and the pin picker
    /// all shipped with no way back to yourself once you had panned away. That
    /// is the second time this control has gone missing (the first was
    /// 2026-08-24, "de knop mist waar je naar je locatie gaat"), which is why
    /// the default is the one that is right nearly everywhere and the exception
    /// has to be typed out.
    ///
    /// Pass false only where the map is a PICTURE rather than a map: the city
    /// and country page previews take no taps at all and open the real map when
    /// you tap them, so a control on top of one would be a button inside a
    /// button. The map tab passes false at full sheet height for the same kind
    /// of reason, which is that there is no map on screen to recentre.
    var showsRecentre = true
    /// How tall the sheet in front of this map is, so the recentre control can
    /// sit ABOVE it. It was pinned 120 points off the bottom, which was clear
    /// of the sheet's peek and behind every other stop it has: the button has
    /// been invisible since the sheet grew (Hidde, 2026-08-24: "de knop mist
    /// waar je naar je locatie gaat").
    /// nil on every map with no sheet in front of it, which is all of them but
    /// the map tab. It used to default to `.peek`, so a full-screen map applied
    /// a 168 point bottom inset for a sheet that was not there and centred its
    /// subject well above the middle of the screen: the pin-moving screen drew
    /// its crosshair at the view's centre and the map put the tree 118 points
    /// above it, which on that screen is not a cosmetic fault but a wrong
    /// coordinate (2026-08-25).
    /// Set by hand on a map that is not inside a MapWithSheet. Everything that
    /// IS inside one inherits it from the sheet itself, which is the whole
    /// point: see SheetLiftKey in BottomSheet.swift.
    var sheetLift: SheetHeight? = nil
    @Environment(\.sheetLift) private var inheritedLift

    /// How much of this map the sheet in front of it is covering.
    private var sheetCoverage: SheetHeight? { sheetLift ?? inheritedLift }
    /// How wide the first look is. Four kilometres suits "what is near me"; a
    /// tree's own page wants the street it stands in, and at four kilometres the
    /// tree itself disappears into a cluster bubble.
    var spanMeters: CLLocationDistance = 4000
    /// Off on a tree's own page. Clustering is right when the question is "what
    /// is around here" and wrong when the answer is already known: the subject
    /// of the page was disappearing into a bubble marked 11.
    var clusters = true

    /// FIT THESE TREES rather than aim at a point, for a map whose whole job is
    /// showing a set: a city, a country, a walk, your own collection.
    ///
    /// `focus` and `spanMeters` cannot do it and Aarhus is the arithmetic.
    /// Focus is the MEAN of the trees, which four trees at Moesgard drag south
    /// of the two in the north, and the span is the widest extent fitted to the
    /// map's WIDTH, which says nothing about a viewport whose usable height is
    /// now a 360 point strip above a sheet. Seven trees, four on screen.
    ///
    /// A bounding box with padding answers both at once, on both axes, and it
    /// is the primitive every map has for exactly this question. Off by
    /// default: the Map tab opens on YOU and a tree's own page opens on the
    /// tree, and neither wants to be reframed around whatever else is nearby.
    var fitsTrees = false
    /// What the map is currently looking at, reported back so the list under it
    /// can be a list of what you are looking at.
    var region: Binding<MKCoordinateRegion?>? = nil
    /// Somewhere to GO, as opposed to `region`, which is where the map has
    /// been. Carries its own token so the same request cannot be applied twice
    /// and a finger can pan away from it afterwards.
    var moveTo: (token: UUID, region: MKCoordinateRegion)? = nil
    @Binding var selected: Tree?

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    func makeUIView(context: Context) -> MLNMapView {
        let map = LaidOutMapView(frame: .zero, styleURL: MapStyle.url)
        // AIM WHEN THE VIEW HAS A SIZE, not when SwiftUI feels like updating.
        //
        // This is the whole of the "map is not centred" bug, and it is general
        // rather than per screen (Hidde, 2026-08-29, on Krakow: "deze view is
        // ook niet mooi gecentraliseerd kunnen we die kennis overal toepassen
        // waar een kaart toont?").
        //
        // updateUIView held the code that applies the sheet's content inset and
        // then aims the camera into the strip a person can actually see. On
        // this screen it ran three times, every one of them with
        // `map.bounds.height == 0`, so neither ever happened: SwiftUI updates a
        // representable when its inputs change, and layout comes afterwards.
        // The Map tab escapes it by accident, because its `region` binding
        // fires on every camera move and drags a later update along behind it.
        // Nothing else in the app has one, so every other map has been showing
        // makeUIView's naive first paint: the trees centred in the whole view,
        // half of which is behind the sheet.
        //
        // A view knows when it has been laid out. Asking it is one override and
        // it fixes every map at once.
        map.onLayout = { [weak map] in
            guard let map else { return }
            context.coordinator.settle(map)
        }
        map.delegate = context.coordinator
        map.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        // Only once somebody has ALREADY said yes. MapLibre asks the system for
        // authorisation the moment this is set, which put the location dialog
        // over the map on first launch and took the ask away from
        // LocationPrimer, whose whole job is to explain why before the system
        // asks. MapKit happened not to prompt here, so this is a difference the
        // port introduced rather than inherited, found by looking at the
        // screenshot (2026-08-23).
        let status = CLLocationManager().authorizationStatus
        map.showsUserLocation = (status == .authorizedWhenInUse || status == .authorizedAlways)
        map.logoView.isHidden = true          // our own attribution sits in the sheet
        // Hidden AND out of the accessibility tree. isHidden alone left both
        // controls in the tree, so the layout gate kept reporting a 40 by 40
        // compass and a 26 by 26 info button against Apple's 44, on every
        // screen that carries a map.
        // NO ROTATION. Hidde, 2026-08-25: "ik heb het idee dat de map te snel
        // draait als ik uit probeer te zoomen, wat is convention in this
        // interaction?" The convention is split: Google and Apple Maps both
        // allow a two-finger twist, and both put a compass on screen the moment
        // the map is off north so you can put it back. We hid the compass on
        // purpose (our recentre control resets north), which leaves the worst of
        // both: a map that rotates by accident during a pinch and no way to see
        // or undo it. Rotation buys nothing here either, because every label on
        // it is a place name meant to be read.
        map.allowsRotating = false
        // OUR INSET, NOT UIKIT'S. MapLibre offers to keep contentInset in step
        // with whatever bars sit over it, and this map is under a sheet rather
        // than a bar, so its idea of the covered area is wrong and it overwrites
        // ours on a layout pass. MapLibre prints a warning about the deprecated
        // form of this on every launch; turning it off is what the warning asks
        // for and what settle() needs to be the only writer.
        map.automaticallyAdjustsContentInset = false
        map.compassView.isHidden = true
        map.compassView.isAccessibilityElement = false
        map.attributionButton.isHidden = true
        map.attributionButton.isAccessibilityElement = false
        // No floating credit control on the map. Mine sat at the map's bottom
        // edge, which is behind the sheet on every screen that has one, so it
        // was invisible, and MapLibre's own is 26 by 26 against Apple's 44.
        // The credit is not optional: OpenFreeMap serve these tiles from
        // OpenStreetMap data and ask to be named. It is named once, in About on
        // the Profile tab, where there is room to read it and where iOS apps
        // conventionally keep this.
        if showsRecentre {
            let recentre = RecentreButton(map: map)
            recentre.translatesAutoresizingMaskIntoConstraints = false
            map.addSubview(recentre)
            let lift = recentre.bottomAnchor.constraint(equalTo: map.bottomAnchor, constant: -120)
            context.coordinator.recentreLift = lift
            NSLayoutConstraint.activate([
                recentre.trailingAnchor.constraint(equalTo: map.safeAreaLayoutGuide.trailingAnchor, constant: -12),
                lift,
                recentre.widthAnchor.constraint(equalToConstant: 44),
                recentre.heightAnchor.constraint(equalToConstant: 44),
            ])
        }

        // THE TAP RECOGNISER, WHICH WAS NEVER INSTALLED.
        //
        // handleTap() has been written, commented and maintained since the
        // MapLibre port and nothing ever called it: no UITapGestureRecognizer
        // was created anywhere in this file. So tapping a pin has done nothing
        // at all, and neither has tapping a cluster, for as long as the port has
        // existed. Hidde reported it three times in one evening and I "fixed" it
        // once by wiring a callback into a function nobody calls (2026-08-25:
        // "ik heb de laatste build en kan nog steeds niet op een boom klikken of
        // een getal dat ie ze dan opent").
        //
        // MapLibre installs its own single tap recogniser, which deselects
        // annotations. Ours gets first refusal: if the tap lands on one of our
        // features we handle it, and if it does not, theirs proceeds. That is
        // the recipe Mapbox and MapLibre both document, and doing it the other
        // way round delays every tap by the other recogniser's timeout.
        let tap = UITapGestureRecognizer(target: context.coordinator,
                                         action: #selector(Coordinator.handleTap(_:)))
        for existing in map.gestureRecognizers ?? [] where existing is UITapGestureRecognizer {
            existing.require(toFail: tap)
        }
        map.addGestureRecognizer(tap)

        // A first paint so the map never shows the Atlantic while it lays out.
        // It is deliberately NOT the final word: at this moment the view has no
        // height, so there is no content inset yet and this centres the
        // collection in the whole map, half of which is about to be covered by
        // the sheet. updateUIView sets it again the moment the inset is real.
        if let focus {
            map.setCenter(focus, zoomLevel: Self.zoom(forMeters: spanMeters), animated: false)
        }
        return map
    }

    func updateUIView(_ map: MLNMapView, context: Context) {
        context.coordinator.parent = self
        // Asserted on every update, not once at creation: MapLibre brings its
        // own compass and info button back after a style or a layout pass, so
        // setting them in makeUIView held for a moment and the layout gate kept
        // reporting a 40 by 40 compass and a 26 by 26 button on every map
        // screen. Ours is beside them at 44.
        map.compassView.isHidden = true
        map.compassView.isAccessibilityElement = false
        map.compassView.accessibilityElementsHidden = true
        map.attributionButton.isHidden = true
        map.attributionButton.isAccessibilityElement = false
        map.attributionButton.accessibilityElementsHidden = true
        context.coordinator.settle(map)

        if let move = moveTo, context.coordinator.moved != move.token {
            context.coordinator.moved = move.token
            map.setVisibleCoordinateBounds(Self.bounds(move.region), animated: true)
        }

        // Paging through the sheet moves the map with you, which is the whole
        // point of staying on the map rather than opening a page.
        if let sel = selected, context.coordinator.centred != sel.id {
            context.coordinator.centred = sel.id
            map.setCenter(.init(latitude: sel.lat, longitude: sel.lng),
                          zoomLevel: Self.zoom(forMeters: 900), animated: true)
        } else if selected == nil {
            context.coordinator.centred = nil
        }

        context.coordinator.sync(trees: trees, mine: mine, route: route,
                                 routeIsReal: routeIsReal, clusters: clusters, on: map)
    }

    // MARK: camera arithmetic

    /// MapKit thinks in metres across, MapLibre in zoom levels. One conversion,
    /// in one place, so every caller keeps speaking metres.
    /// `width` is how wide the thing showing the map is, in points. It defaults
    /// to the narrow phone because that is what a full-screen map is; a 72 point
    /// thumbnail that borrows the 375 figure opens five times too close, which
    /// turns an inset meant to show a SETTING into a picture of tarmac.
    static func zoom(forMeters m: CLLocationDistance, latitude: Double = 52,
                     width: Double = 375) -> Double {
        // 512, not 256. MapLibre's zoom is defined against 512-point tiles, and
        // using the 256 figure from the web slippy-map convention put every
        // camera one whole level too close: asking for four kilometres gave
        // about two, so the map opened on a single tree where the old MapKit
        // version showed the city and its clusters. It looked like clustering
        // was broken and it was arithmetic.
        let metresPerPointAtZoomZero = (40_075_017.0 / 512.0) * cos(latitude * .pi / 180)
        return max(1, min(20, log2(metresPerPointAtZoomZero * width / max(m, 1))))
    }

    /// The smallest box holding every one of these, or nil when there are none.
    static func box(of points: [CLLocationCoordinate2D]) -> MLNCoordinateBounds? {
        guard !points.isEmpty else { return nil }
        let lats = points.map(\.latitude), lngs = points.map(\.longitude)
        return MLNCoordinateBounds(
            sw: .init(latitude: lats.min()!, longitude: lngs.min()!),
            ne: .init(latitude: lats.max()!, longitude: lngs.max()!))
    }

    static func bounds(_ r: MKCoordinateRegion) -> MLNCoordinateBounds {
        MLNCoordinateBounds(
            sw: .init(latitude: r.center.latitude - r.span.latitudeDelta / 2,
                      longitude: r.center.longitude - r.span.longitudeDelta / 2),
            ne: .init(latitude: r.center.latitude + r.span.latitudeDelta / 2,
                      longitude: r.center.longitude + r.span.longitudeDelta / 2))
    }

    static func region(_ b: MLNCoordinateBounds) -> MKCoordinateRegion {
        MKCoordinateRegion(
            center: .init(latitude: (b.sw.latitude + b.ne.latitude) / 2,
                          longitude: (b.sw.longitude + b.ne.longitude) / 2),
            span: .init(latitudeDelta: abs(b.ne.latitude - b.sw.latitude),
                        longitudeDelta: abs(b.ne.longitude - b.sw.longitude)))
    }

    // MARK: coordinator

    final class Coordinator: NSObject, MLNMapViewDelegate {
        /// var, not let, and reassigned on every updateUIView. A coordinator is
        /// made once and keeps whatever struct it was born with, so a delegate
        /// method reading `parent.selected` was reading the value from launch
        /// forever. That is why the map did not follow the pager and why the
        /// region kept reporting itself while a tree was selected.
        var parent: TreeMap
        var centred: String?
        var moved: UUID?

        private var styleReady = false
        private var pending: (trees: [Tree],
                              mine: [(id: UUID, lat: Double, lng: Double, name: String, photo: UIImage?)],
                              route: [CLLocationCoordinate2D],
                              routeIsReal: Bool,
                              clusters: Bool)?
        private var drawnTreeIDs: Set<String> = []
        private var drawnMineIDs: Set<String> = []
        private var drawnRoute = 0
        private var breath: Timer?
        /// The constraint that keeps the recentre control above the sheet.
        var recentreLift: NSLayoutConstraint?

        init(_ p: TreeMap) { parent = p }
        deinit { breath?.invalidate() }

        // MARK: style

        func mapView(_ map: MLNMapView, didFinishLoading style: MLNStyle) {
            // MapLibre calls its delegate on the main thread, but the protocol
            // is an Objective-C one and therefore nonisolated, so the compiler
            // cannot know that. assumeIsolated states it once rather than
            // hopping through a Task, which would let a frame render before the
            // layers exist. Strict concurrency only fails in the CI job; the
            // local Debug build waves this through, which is the whole reason
            // that job exists.
            MainActor.assumeIsolated {
            MapLayers.install(on: style, clustered: parent.clusters)
            styleReady = true
            if let p = pending {
                pending = nil
                sync(trees: p.trees, mine: p.mine, route: p.route,
                     routeIsReal: p.routeIsReal, clusters: p.clusters, on: map)
            }
            startBreathing(on: style)
            }
        }

        /// A tree having its moment right now is gold and it breathes (Hidde,
        /// 2026-08-20: "als ze in bloei staan, zie je ze een beetje pulseren").
        ///
        /// On MapKit each pin was its own view and carried its own CALayer scale
        /// animation. A style layer cannot: iconScale is a LAYOUT property in
        /// MapLibre and layout properties do not animate, only paint ones do. So
        /// the pin holds still and a soft halo breathes around it instead, on
        /// circleRadius and circleOpacity, which are paint and transition
        /// properly. It is arguably the better answer anyway, because the pin
        /// stays exactly as readable while it happens.
        ///
        /// All the peaking pins breathe TOGETHER, since the animation belongs to
        /// the layer rather than to each feature. On a screen with a handful of
        /// them that reads as a tide rather than as noise.
        ///
        /// Reduce Motion turns it off, because a map covered in animation is
        /// exactly what that setting exists for.
        private func startBreathing(on style: MLNStyle) {
            breath?.invalidate()
            guard !UIAccessibility.isReduceMotionEnabled,
                  let halo = style.layer(withIdentifier: MapLayers.haloLayer) as? MLNCircleStyleLayer
            else { return }
            var out = true
            breath = Timer.scheduledTimer(withTimeInterval: 1.15, repeats: true) { [weak halo] _ in
                guard let halo else { return }
                halo.circleRadius = NSExpression(forConstantValue: out ? 27 : 20)
                halo.circleOpacity = NSExpression(forConstantValue: out ? 0.0 : 0.38)
                out.toggle()
            }
            breath?.fire()
        }

        // MARK: data

        func sync(trees: [Tree],
                  mine: [(id: UUID, lat: Double, lng: Double, name: String, photo: UIImage?)],
                  route: [CLLocationCoordinate2D],
                  routeIsReal: Bool,
                  clusters: Bool,
                  on map: MLNMapView) {
            guard styleReady, let style = map.style else {
                pending = (trees, mine, route, routeIsReal, clusters)
                return
            }
            // The collected set joins the identity of what is drawn: without
            // it, ticking a tree off changes no id and the pins never redraw.
            let wantTrees = Set(trees.map(\.id))
                .union(parent.collected.intersection(trees.map(\.id)).map { "c:" + $0 })
                .union(parent.favourites.intersection(trees.map(\.id)).map { "f:" + $0 })
            let wantMine = Set(mine.map { $0.id.uuidString })
            MainActor.assumeIsolated {
            if wantTrees != drawnTreeIDs {
                drawnTreeIDs = wantTrees
                MapLayers.setTrees(trees, on: style, clustered: clusters,
                                   zoom: map.zoomLevel,
                                   collected: parent.collected,
                                   favourites: parent.favourites)
            }
            if wantMine != drawnMineIDs {
                drawnMineIDs = wantMine
                MapLayers.setMine(mine, on: style, clustered: clusters, zoom: map.zoomLevel)
            }
            if route.count != drawnRoute {
                drawnRoute = route.count
                MapLayers.setRoute(route, real: routeIsReal, on: style)
            }
            }
        }

        // MARK: interaction

        /// @MainActor because MapLayers is, and this now calls into it for the
        /// cluster's members. Exactly the trap SpeciesGlyph records further down
        /// this file: the local Debug build waved the nonisolated version
        /// through and the iOS CI job did not. A gesture recogniser only ever
        /// fires on the main thread, so this states what was already true.
        @MainActor
        @objc func handleTap(_ g: UITapGestureRecognizer) {
            guard let map = g.view as? MLNMapView, let style = map.style else { return }
            let point = g.location(in: map)
            // A finger is wider than a pixel. Ask over a small square so a tap
            // near a pin counts as a tap on it, which is what every map does.
            let box = CGRect(x: point.x - 22, y: point.y - 22, width: 44, height: 44)

            let clusterHits = map.visibleFeatures(in: box,
                                                  styleLayerIdentifiers: [MapLayers.clusterLayer])
            if let cluster = clusterHits.first {
                // Tapping a pile zooms into it rather than opening anything,
                // which is what Google Maps does and what a pile of pins needs.
                //
                // ONE TAP HAS TO BE ENOUGH (Hidde, 2026-08-26: "ik vind dat als
                // je een keer op het getal klikt, je in een keer zover moet
                // inzoomen dat alles uitklapt"). This used to add a fixed two
                // zoom levels, which has nothing to do with how far apart the
                // trees in that particular pile stand: a bubble marked 2 over
                // two trees fifty metres apart took three taps to come apart,
                // and a bubble over a whole province came apart on the first.
                // A fixed step cannot be right for both.
                //
                // So the pile says where to go. We cluster ourselves, so the
                // members are known exactly, and the target is the zoom that
                // fits their spread on screen. That guarantees separation: a
                // spread filling the viewport puts its members hundreds of
                // points apart, against the sixty that makes them one bubble.
                let members = MapLayers.clusterMembers(at: cluster.coordinate, on: style)
                map.setCenter(Coordinator.centre(of: members) ?? cluster.coordinate,
                              zoomLevel: Coordinator.zoomToSplit(members, in: map),
                              animated: true)
                return
            }
            // Yours first: they are drawn on top, so a tap that lands on one
            // meant that one. They were not in this list at all, which is why
            // they could not be opened.
            let mineHits = map.visibleFeatures(in: box,
                                               styleLayerIdentifiers: [MapLayers.mineLayer])
            if let hit = mineHits.first,
               let raw = hit.attribute(forKey: MapLayers.idKey) as? String,
               let id = UUID(uuidString: raw) {
                parent.onSelectMine?(id)
                return
            }

            let treeHits = map.visibleFeatures(in: box,
                                               styleLayerIdentifiers: [MapLayers.treeLayer,
                                                                       MapLayers.peakLayer])
            if let hit = treeHits.first,
               let id = hit.attribute(forKey: MapLayers.idKey) as? String,
               let tree = parent.trees.first(where: { $0.id == id }) {
                if let open = parent.onSelectTree {
                    open(tree.id)
                } else {
                    parent.selected = tree
                }
            }
        }

        /// The mean of a pile, so the camera lands on the trees rather than on
        /// the bubble's own drawn position.
        static func centre(of members: [CLLocationCoordinate2D]) -> CLLocationCoordinate2D? {
            guard !members.isEmpty else { return nil }
            var lat = 0.0, lon = 0.0
            for c in members { lat += c.latitude; lon += c.longitude }
            return .init(latitude: lat / Double(members.count),
                         longitude: lon / Double(members.count))
        }

        /// The zoom at which a pile actually comes apart, rather than a step.
        ///
        /// Works in the same normalised web mercator the clusterer uses, so the
        /// arithmetic here and the arithmetic that built the bubble agree by
        /// construction. Three cases, and the last one is the reason for the
        /// ceiling: trees on ONE coordinate never separate at any zoom, which
        /// is not hypothetical here (a register rounding to two decimals put
        /// six Kalopa trees on one grid point). Chasing that split would zoom
        /// to infinity, so it stops somewhere useful instead.
        static func zoomToSplit(_ members: [CLLocationCoordinate2D],
                                in map: MLNMapView) -> Double {
            let hardMax = 17.0
            guard members.count > 1 else { return min(map.zoomLevel + 2.0, hardMax) }
            func merc(_ c: CLLocationCoordinate2D) -> (x: Double, y: Double) {
                let x = (c.longitude + 180.0) / 360.0
                let lat = min(max(c.latitude, -85.05), 85.05) * .pi / 180.0
                return (x, (1.0 - log(tan(lat) + 1.0 / cos(lat)) / .pi) / 2.0)
            }
            let pts = members.map(merc)
            let dx = (pts.map(\.x).max() ?? 0) - (pts.map(\.x).min() ?? 0)
            let dy = (pts.map(\.y).max() ?? 0) - (pts.map(\.y).min() ?? 0)
            // Room to breathe, so the outermost pins are not on the bezel.
            let pad = 96.0
            let w = Swift.max(Double(map.bounds.width) - pad, 80.0)
            let h = Swift.max(Double(map.bounds.height) - pad, 80.0)
            var world = Double.greatestFiniteMagnitude
            if dx > 0 { world = Swift.min(world, w / dx) }
            if dy > 0 { world = Swift.min(world, h / dy) }
            guard world < .greatestFiniteMagnitude else { return hardMax }
            let z = log2(world / 512.0)
            // Never go backwards, and always move enough to feel like something
            // happened, even when the pile is already nearly apart.
            return Swift.min(Swift.max(z, map.zoomLevel + 1.0), hardMax)
        }

        /// Pan the map and the list follows. Google Maps, Apple Maps and Airbnb
        /// all do a version of this, because a list that keeps describing where
        /// you were standing while you look at Paris is answering a question
        /// nobody is asking any more.
        ///
        /// Throttled by distance rather than by time: a pan fires this a lot,
        /// and re-sorting fifteen hundred trees for every three metres would be
        /// work nobody can see. Three hundred metres is under one screen at
        /// street zoom, so the list still feels live.
        /// Whether the opening shot has been taken with a real content inset.
        var aimed = false
        /// The sheet coverage the opening shot was taken with, so a shot taken
        /// before the sheet had reported its height can be retaken once and
        /// only once. See settle().
        var aimedCoverage: CGFloat = -1
        /// Set the moment a finger moves the camera. After that the map belongs
        /// to whoever is holding the phone and nothing here aims it again.
        var userMoved = false

        /// EVERYTHING THAT NEEDS THE VIEW TO HAVE A SIZE, in one place, called
        /// from layoutSubviews as well as from updateUIView.
        ///
        /// It used to live in updateUIView alone, guarded on a non-zero height,
        /// and on every screen but the Map tab that guard was never once true.
        /// See the note in makeUIView.
        @MainActor
        func settle(_ map: MLNMapView) {
            guard map.bounds.height > 0 else { return }
            let coverage = parent.sheetCoverage?.points(in: map.bounds.height) ?? 0

            // Keep the recentre control just above the sheet, whatever stop the
            // sheet is at. 12 points of air, and never lower than the old 120 so
            // a map with no sheet in front of it looks the same as before.
            if let lift = recentreLift {
                // Never higher than mid-screen. At full height the sheet is 86
                // percent of the phone, so "just above the sheet" put the
                // recentre control up among the search field and the filter
                // chips, three controls deep in the same 120 points (seen
                // 2026-08-25, on the map-full screen the first time it was
                // photographed).
                let clamped = max(min(-(coverage + 12), -120), -(map.bounds.height * 0.55))
                if abs(lift.constant - clamped) > 1 { lift.constant = clamped }
            }

            // AND THE CAMERA HAS TO KNOW ABOUT THE SHEET TOO, which until
            // 2026-08-25 only the recentre button did. Tapping a tree centred it
            // in the map VIEW, and the bottom half of that view is behind the
            // sheet, so the pin you just tapped settled at the sheet's top edge
            // or under it (Hidde: "als ik op Muntje klik, pakt hij niet goed het
            // midden van Muntje van de kaart"). A content inset is what this is
            // for: MapLibre then treats the uncovered strip as the map, so every
            // camera move, the selection, the recentre and a search result all
            // land in the middle of what a person can actually see.
            //
            // Clamped at 55 percent, because at full height the sheet leaves a
            // sliver and an inset that large gives the camera almost no viewport
            // to aim into.
            let bottom = min(coverage, map.bounds.height * 0.55)
            if abs(map.contentInset.bottom - bottom) > 1 {
                map.contentInset = UIEdgeInsets(top: 0, left: 0, bottom: bottom, right: 0)
            }

            // AND NOW AIM, with an inset that is finally real.
            //
            // ONCE, and once more only if the first shot was taken before the
            // sheet had said anything. The sheet reports its height through the
            // environment while it is still settling, so the first layout pass
            // can arrive with no coverage at all and the real answer land a
            // frame later; aiming strictly once would take whichever came
            // first.
            //
            // It is NOT "aim until a finger moves the map", which is what this
            // said for an hour. Dragging the SHEET is not moving the map, so
            // every drag re-framed the camera under somebody's thumb, and a map
            // that jumps while you are reading the list under it is worse than
            // a map that opened slightly wrong.
            guard !userMoved, !aimed || abs(coverage - aimedCoverage) > 1 && aimedCoverage <= 0
            else { return }
            aimedCoverage = coverage

            // The set, when the caller asked for the set. Padding on three
            // sides for air, and the sheet's own coverage under it so nothing
            // is fitted into the part nobody can see.
            if parent.fitsTrees,
               let box = TreeMap.box(of: parent.trees.map { CLLocationCoordinate2D(latitude: $0.lat, longitude: $0.lng) }
                                     + parent.mine.map { CLLocationCoordinate2D(latitude: $0.lat, longitude: $0.lng) }) {
                aimed = true
                // AIR ONLY. MapLibre's own header: "Camera edge insets are
                // formed as accumulation of map view's content insets and the
                // edge padding passed to the method." The sheet is already in
                // contentInset above, so adding it here again asked for 734
                // points of padding on a 667 point phone and pushed every pin
                // into a corner. This is the margin round the box and nothing
                // else; the top is deeper because the back button and the
                // title sit there.
                map.setVisibleCoordinateBounds(
                    box,
                    edgePadding: UIEdgeInsets(top: 76, left: 44, bottom: 44, right: 44),
                    animated: false)
                // A single tree fits to a box with no size, which MapLibre
                // answers with the deepest zoom it has: a doorstep. Back off to
                // the same opening shot every other one-tree map takes.
                if map.zoomLevel > 16.5 {
                    map.setCenter(map.centerCoordinate, zoomLevel: 15.5, animated: false)
                }
                return
            }

            guard let focus = parent.focus else { return }
            aimed = true
            map.setCenter(focus,
                          zoomLevel: TreeMap.zoom(forMeters: parent.spanMeters),
                          animated: false)
        }

        /// A finger on the map ends the aiming. `reason` tells us it was a
        /// person rather than one of our own setCenter calls, which is the
        /// whole distinction: without it the map would stop aiming the instant
        /// it aimed itself.
        func mapView(_ map: MLNMapView, regionWillChangeWith reason: MLNCameraChangeReason,
                     animated: Bool) {
            let byHand: MLNCameraChangeReason = [
                .gesturePan, .gesturePinch, .gestureRotate, .gestureZoomIn,
                .gestureZoomOut, .gestureOneFingerZoom, .gestureTilt,
            ]
            if !reason.intersection(byHand).isEmpty { userMoved = true }
        }

        func mapView(_ map: MLNMapView, regionDidChangeAnimated animated: Bool) {
            // Our own clustering regroups on a change of zoom level and does
            // nothing on a pan, which is what makes a pan free.
            if let style = map.style {
                MainActor.assumeIsolated {
                    MapLayers.cluster(on: style, zoom: map.zoomLevel, clustered: parent.clusters)
                }
            }
            // While a tree is selected the camera is being driven by the pager,
            // so reporting the region back would rebuild the list under the
            // pager and shuffle what you are swiping through.
            guard parent.selected == nil, let binding = parent.region else { return }
            let now = TreeMap.region(map.visibleCoordinateBounds)
            if let last = binding.wrappedValue {
                let a = CLLocation(latitude: last.center.latitude, longitude: last.center.longitude)
                let b = CLLocation(latitude: now.center.latitude, longitude: now.center.longitude)
                // Proportional to what you can SEE, not a flat 300 metres.
                // At street zoom 300 metres is most of the screen, so a pan
                // that visibly changed everything reported nothing and the list
                // stood still (Hidde, 2026-08-24).
                let visible = now.span.latitudeDelta * 111_000
                guard a.distance(from: b) > max(60, visible * 0.15)
                        || abs(last.span.latitudeDelta - now.span.latitudeDelta)
                            > now.span.latitudeDelta * 0.2
                else { return }
            }
            binding.wrappedValue = now
        }
    }
}

/// A map view that says when it has been laid out.
///
/// One override, and it is the difference between a camera that aims at the
/// trees and one that aims at the middle of a view half covered by a sheet. See
/// the note in makeUIView: a SwiftUI representable is updated when its inputs
/// change, and on most of these screens nothing changes after the first pass,
/// so `updateUIView` only ever sees a view with no size yet.
final class LaidOutMapView: MLNMapView {
    var onLayout: (() -> Void)?

    override func layoutSubviews() {
        super.layoutSubviews()
        onLayout?()
    }
}

/// Where the style comes from. The same file the website renders, so a change to
/// the palette lands on both surfaces at once, which is the whole reason the map
/// moved off MapKit's closed basemap.
enum MapStyle {
    static let url = URL(string: "https://ancienttrees.app/assets/map-style.json")!
}

/// Everything the map draws, in one place: the sources, the layers and the
/// images. Kept out of the SwiftUI wrapper because it is style plumbing rather
/// than view logic, and because the offline work will need to call it too.
@MainActor
enum MapLayers {
    static let treeSource = "at-trees"
    static let routeSource = "at-route"
    static let treeLayer = "at-trees-pin"
    static let peakLayer = "at-trees-peak"
    static let haloLayer = "at-trees-halo"
    static let clusterLayer = "at-cluster"
    static let clusterCount = "at-cluster-count"
    static let mineLayer = "at-mine-pin"
    static let routeLayer = "at-route-line"
    static let idKey = "at_id"
    /// How many trees a bubble stands for. NOT "point_count", which is
    /// MapLibre's own reserved cluster property: a feature carrying it makes
    /// the WHOLE source load as empty, silently, valid GeoJSON and all. That
    /// single word cost most of 2026-08-24. Proof: the same 974 features with
    /// the bubbles emitted as ordinary points render; with `point_count` on
    /// 284 of them, the source reports zero features and no error anywhere.
    static let countKey = "at_count"
    /// Tree or cluster, as a STRING. Every layer selects on this rather than on
    /// a number: with `at_count > 1` the bubbles never painted, and the same
    /// features with the same keys painted the moment the count was 1, which
    /// puts the fault in the numeric comparison rather than in the data.
    static let kindKey = "at_kind"
    // Every feature carries it, 1 for a single tree and n for a bubble, so no
    // layer ever has to ask whether a property is absent. `at_count == nil`
    // draws nothing at all: MapLibre gives its own `point_count` special
    // treatment in that comparison and an ordinary key none.

    private static let moss = UIColor(red: 0.20, green: 0.35, blue: 0.20, alpha: 1)
    /// Brand.ink, for the ring around a tree you added yourself. Every other
    /// colour on this map is spoken for: moss is ours, white is the ring every
    /// pin wears, blue is a ticket and gold is Plus. See photoPin.
    private static let ink = UIColor(red: 0.15, green: 0.19, blue: 0.12, alpha: 1)
    /// EVERYTHING THIS FILE REMEMBERS IS PER STYLE, and that is a correctness
    /// fix rather than tidiness. This app has several map views alive at once:
    /// the Map tab, My trees, a tree page's map, the pin picker.
    ///
    /// The image register learned this on 2026-08-28 and the rest of the state
    /// did not, so the same class of bug stayed live in five other statics
    /// until 2026-08-29 (Hidde, both days: "de kaart verliest nog steeds z'n
    /// pin als ik uitzoom"). Two ways it went wrong, both silent.
    ///
    /// `leaves` held "the trees", so opening a tree page, whose map draws one
    /// tree, replaced it for every map in the app. Going back and zooming out
    /// re-clustered the Map tab from that single tree, and the map emptied.
    /// Nothing redraws it, because the coordinator thinks it has already drawn
    /// what it was asked for.
    ///
    /// `writeCount` numbered the GeoJSON files, and each write deletes the one
    /// before it. Two maps sharing the counter therefore delete each other's
    /// file while the other's source is still reading it.
    ///
    /// A weak-keyed table rather than a dictionary of ObjectIdentifier: a
    /// dealloced style's key can be reused by a new object, and inheriting a
    /// dead map's cluster state is the same bug pointing the other way.
    final class StyleState {
        var registered: Set<String> = []
        /// Every tree of OURS as a point feature, kept so clustering can be
        /// recomputed on a zoom change without rebuilding any of this.
        var leaves: [MLNPointFeature] = []
        /// And every tree the person added themselves. Kept apart only so a
        /// change to one does not mean rebuilding the other; they cluster
        /// together, which is the whole point.
        var mine: [MLNPointFeature] = []
        var lastBucket: Int = .min
        /// The zoom the pins were last built for. See the hysteresis in cluster().
        var lastClusterZoom: Double = -99
        var lastClustered = true
        /// The identifier the live tree source currently carries. See apply().
        var liveSourceID = treeSource
        var writeCount = 0
        /// This style's own slot in the temporary directory.
        let seq: Int
        init(seq: Int) { self.seq = seq }
    }

    private static let states = NSMapTable<MLNStyle, StyleState>.weakToStrongObjects()
    private static var seq = 0

    private static func state(for style: MLNStyle) -> StyleState {
        if let s = states.object(forKey: style) { return s }
        seq += 1
        let s = StyleState(seq: seq)
        states.setObject(s, forKey: style)
        return s
    }

    private static func hasImage(_ name: String, on style: MLNStyle) -> Bool {
        state(for: style).registered.contains(name)
    }

    private static func noteImage(_ name: String, on style: MLNStyle) {
        state(for: style).registered.insert(name)
    }
    // There was a `mapRef` here, one shared weak pointer to "the map", and it
    // was removed on 2026-08-28 with the last thing that read it. A single
    // static naming one of four live map views is a bug waiting to be written
    // again: whoever loaded last won, and everything done through it was done
    // to the wrong map. Everything that needs a style is handed the style it
    // is drawing.

    static func install(on style: MLNStyle, clustered: Bool) {
        // A FRESH state for this style. A style loads once per map view, so
        // this is where a map starts remembering, and starting clean is what
        // keeps one map from inheriting another's.
        seq += 1
        states.setObject(StyleState(seq: seq), forKey: style)
        style.setImage(pin(colour: moss, glyph: nil), forName: "at-pin-default")
        style.setImage(minePin(), forName: "at-pin-mine")

        // The source is NEVER given MapLibre's own clustering options. They do
        // not work: see the note on cluster() below. We cluster ourselves and
        // hand this source the result, so from its point of view it is a plain
        // collection of points.
        //
        // No tree source here, and since 2026-08-29 no separate source for the
        // trees somebody added themselves either. They are features in the same
        // source now, so they land in the same grid and join the same counts
        // (Hidde: "zelfgemaakte bomen moeten gewoon mee clusteren met de
        // getallen als je uitzoomt"). A second source could never do that: a
        // clusterer only ever sees the points it was handed.
        //
        // apply() is the only place a source is ever made, because a source
        // that has already existed under this identifier does not load: see the
        // note there.
        let route = MLNShapeSource(identifier: routeSource, shape: nil, options: nil)
        style.addSource(route)

        // The walk goes UNDER the pins: a line drawn over a trunk hides the
        // thing the line exists to join up.
        let line = MLNLineStyleLayer(identifier: routeLayer, source: route)
        line.lineColor = NSExpression(forConstantValue: moss.withAlphaComponent(0.9))
        line.lineWidth = NSExpression(forConstantValue: 5)
        line.lineCap = NSExpression(forConstantValue: "round")
        line.lineJoin = NSExpression(forConstantValue: "round")
        // A dashed line where we do not have a routed shape, because a solid
        // line between trunks claims a path nobody checked. 78 of 179 walks
        // carry a real route; the rest only carry an order.
        line.predicate = NSPredicate(format: "real == YES")
        style.addLayer(line)

        let guessed = MLNLineStyleLayer(identifier: routeLayer + "-guessed", source: route)
        guessed.lineColor = NSExpression(forConstantValue: moss.withAlphaComponent(0.55))
        guessed.lineWidth = NSExpression(forConstantValue: 4)
        guessed.lineCap = NSExpression(forConstantValue: "round")
        guessed.lineDashPattern = NSExpression(forConstantValue: [0.5, 2.5])
        guessed.predicate = NSPredicate(format: "real == NO")
        style.addLayer(guessed)

    }

    /// `zoom` is the zoom the map is ACTUALLY at, handed in by the caller,
    /// which always has the map in scope.
    ///
    /// It used to ask a stored reference and fall back to 12 when that was not
    /// set yet, which is street level. So when the catalogue arrived before the
    /// map had finished attaching, every tree in the world was grouped into
    /// cells sized for a street while somebody was looking at a continent, and
    /// almost every pin fell on top of another and vanished. Hidde saw three
    /// clusters over Europe above a sheet reading "1,356 trees you can see"
    /// (2026-08-28), and it healed the moment he dragged the map, because a
    /// region change recomputes at the real zoom. That is exactly the shape of
    /// a wrong guess that corrects itself, which is the kind nobody can report
    /// and everybody sees.
    static func setTrees(_ trees: [Tree], on style: MLNStyle, clustered: Bool,
                         zoom: Double,
                         collected: Set<String> = [], favourites: Set<String> = []) {
        let month = Calendar.current.component(.month, from: Date())
        var features: [MLNPointFeature] = []
        for t in trees {
            let f = MLNPointFeature()
            f.coordinate = .init(latitude: t.lat, longitude: t.lng)
            f.title = t.name
            let peaking = Launch.season && (t.peak?.isNow(month) ?? false)
            // The glyph is the SPECIES, always, not a generic tree icon: a
            // ginkgo pin looks like a ginkgo before you tap it. It works for
            // every tree, because every tree carries a species while only a
            // quarter carry a photograph. And when the species is having its
            // moment, the pin takes the colour of that moment rather than one
            // shared gold, computed on the server so this pin and the website's
            // light up the same tree on the same day.
            let colour = peaking
                ? (UIColor(hex: t.peak?.colour) ?? UIColor(red: 0.85, green: 0.63, blue: 0.25, alpha: 1))
                : moss
            let seen = collected.contains(t.id)
            let ticket = t.paidEntry
            let loved = favourites.contains(t.id)
            let name = imageName(species: t.commonName, peaking: peaking, colour: colour)
                + (seen ? "-c" : "") + (ticket ? "-t" : "") + (loved ? "-f" : "")
            // Our own register of what has been added, rather than asking the
            // style whether it already has the image. That check drew exactly
            // ONE pin for eleven trees: whatever style.image(forName:) returns
            // for a name it has never seen, it is not reliably nil, so after the
            // first species every later icon name pointed at nothing and
            // MapLibre silently drew nothing. Found in a screenshot, not in a log.
            if !hasImage(name, on: style) {
                noteImage(name, on: style)
                style.setImage(pin(colour: colour,
                                   glyph: SpeciesGlyph.image(for: t.commonName),
                                   collected: seen, ticket: ticket, favourite: loved),
                               forName: name)
            }
            // Attributes must be values GeoJSON can hold: strings, numbers,
            // booleans. A UIColor in here made every feature invalid and the
            // map drew ONE pin for fourteen hundred trees, silently. The peak
            // colour still reaches the eye where it matters, baked into the pin
            // image itself; the halo underneath takes one warm tone for all of
            // them, which reads as a season rather than as a paint chart.
            f.attributes = [idKey: t.id, "icon": name, "peaking": peaking,
                            countKey: 1, kindKey: "tree", "at_label": ""]
            features.append(f)
        }
        state(for: style).leaves = features
        cluster(on: style, zoom: zoom, clustered: clustered, force: true)
    }

    /// Hand the style a fresh source built from these points.
    ///
    /// Two things here are not the obvious call, and both were measured on
    /// 2026-08-24 rather than reasoned about.
    ///
    /// First, the points go in as real GeoJSON, not as an
    /// MLNShapeCollectionFeature. Second, and this is the one that cost the
    /// afternoon, the source is CREATED from a file URL rather than having its
    /// `shape` assigned. Assigning `shape` draws nothing at all on this build:
    /// 974 features went in, all eight layers were present in the style, and
    /// `visibleFeatures` returned zero. The same 974 features handed to
    /// `MLNShapeSource(identifier:url:options:)` draw. No error is logged in
    /// either case.
    ///
    /// The file name is new every time because MapLibre caches a source's URL:
    /// rewriting the same path leaves the previous contents in place.
    private static func apply(_ features: [MLNPointFeature], on style: MLNStyle, clustered: Bool) {
        let st = state(for: style)
        var out: [[String: Any]] = []
        out.reserveCapacity(features.count)
        for f in features {
            let geom: [String: Any] = ["type": "Point",
                                       "coordinates": [f.coordinate.longitude, f.coordinate.latitude]]
            let props: [String: Any] = f.attributes
            out.append(["type": "Feature", "geometry": geom, "properties": props])
        }
        let doc: [String: Any] = ["type": "FeatureCollection", "features": out]
        guard let data = try? JSONSerialization.data(withJSONObject: doc) else { return }
        st.writeCount += 1
        // NAMED AFTER THIS STYLE. The counter used to be shared, so two live
        // maps numbered their files from one sequence and each deleted the
        // other's the moment it wrote its own, while the other's source was
        // still reading it.
        let file = FileManager.default.temporaryDirectory
            .appendingPathComponent("at-trees-\(st.seq)-\(st.writeCount).geojson")
        guard (try? data.write(to: file)) != nil else { return }

        for id in [clusterCount, clusterLayer, peakLayer, haloLayer, treeLayer, mineLayer] {
            if let layer = style.layer(withIdentifier: id) { style.removeLayer(layer) }
        }
        // A NEW identifier as well as a new file. Re-adding a source under an
        // identifier the style has just seen leaves it holding nothing: the
        // file is read, no error is raised, and `features(matching:)` returns
        // zero. Measured, 2026-08-24. The layer identifiers stay fixed, which
        // is what the tap handler reads, so nothing downstream notices.
        if let old = style.source(withIdentifier: st.liveSourceID) { style.removeSource(old) }
        st.liveSourceID = "\(treeSource)-\(st.seq)-\(st.writeCount)"
        let source = MLNShapeSource(identifier: st.liveSourceID, url: file, options: [:])
        style.addSource(source)
        addTreeLayers(on: style, source: source, clustered: clustered)
        // Yesterday's file is no longer read once the new source is in.
        let stale = FileManager.default.temporaryDirectory
            .appendingPathComponent("at-trees-\(st.seq)-\(st.writeCount - 1).geojson")
        try? FileManager.default.removeItem(at: stale)
    }

    /// WHERE THE PILING STOPS, and both numbers are the convention rather than
    /// a guess (Hidde, 2026-08-29: "de pinnen lijken wat te snel te clusteren,
    /// het zou in dit geval nicer zijn als ze wel gewoon apart te zien zijn wat
    /// zijn hier conventies in?"). He was looking at two trees a couple of
    /// streets apart in Baarn drawn as a bubble marked 2.
    ///
    /// What the references do, recorded in CONVENTIONS.md: MapLibre and Mapbox
    /// cluster on a radius in PIXELS, defaulting to 50; the supercluster
    /// library underneath them defaults to 40; MapKit does not take a number at
    /// all and clusters when two annotation views would OVERLAP. All three
    /// answer the same question, which is whether the pins would collide, not
    /// whether the trees are near each other.
    ///
    /// Ours are 38 points across, so 44 is a pin's width plus a hair: two that
    /// would touch become one bubble and two that would not stay two. It was
    /// 60, which is a thumb rather than a pin, and it piled up trees that were
    /// comfortably far apart on screen.
    private static let clusterCellPoints = 44.0
    /// And past this nothing piles up at all. Left at 15 deliberately: raising
    /// it makes pins cluster for LONGER, which is the opposite of what was
    /// asked, and lowering it drops a whole city's worth of overlapping pins on
    /// the map at a zoom where they cannot be told apart.
    private static let clusterMaxZoom = 15.0

    /// WHICH GRID CELL A POINT FALLS IN, as one number.
    ///
    /// Pulled out and rewritten 2026-08-28, because the old expression was
    /// `column * 100_000 + row` and the row index outgrows 100,000 partway up
    /// the range this is actually used in. The grid is `worldPoints / 60`
    /// cells wide, `worldPoints` is `512 * 2^zoom`, so the largest index is
    /// `8.53 * 2^zoom`: it passes 100,000 at zoom 13.5 and reaches about
    /// 280,000 at zoom 15, which is where clustering stops. Between 13.5 and 15
    /// two cells a long way apart therefore shared a key, and a bubble was
    /// drawn at the MEAN of both groups, which is a pile of trees standing
    /// somewhere none of them are.
    ///
    /// A shift rather than a bigger multiplier, because a multiplier is a
    /// number somebody has to keep checking against a zoom range. Both indices
    /// are non-negative and fit in 32 bits at any zoom this map can reach, so
    /// this cannot collide at all.
    nonisolated static func cellKey(x: Double, y: Double, cell: Double) -> Int64 {
        (Int64(floor(x / cell)) << 32) | Int64(floor(y / cell))
    }

    /// WHICH POINTS FALL TOGETHER, as groups of indices into what was handed in.
    ///
    /// Pure and nonisolated on purpose: it is the whole of the clustering
    /// decision, so a test can ask the question that cannot be asked of a map
    /// (does a tree somebody added themselves join the pile beside it) without
    /// a simulator, a style or a single pixel.
    nonisolated static func groups(of coords: [CLLocationCoordinate2D],
                                   cell: Double) -> [[Int]] {
        var cells: [Int64: [Int]] = [:]
        for (i, c) in coords.enumerated() {
            let x = (c.longitude + 180.0) / 360.0
            let lat = min(max(c.latitude, -85.05), 85.05) * .pi / 180.0
            let y = (1.0 - log(tan(lat) + 1.0 / cos(lat)) / .pi) / 2.0
            cells[cellKey(x: x, y: y, cell: cell), default: []].append(i)
        }
        return Array(cells.values)
    }

    /// OUR OWN CLUSTERING, 2026-08-24, because MapLibre's does not work here.
    ///
    /// Ten hypotheses were tested across two days. With
    /// `MLNShapeSourceOptionClustered` set, the source yields exactly one
    /// feature whatever it is given: as an MLNShapeCollectionFeature, as an
    /// MLNShape parsed from real GeoJSON, and as a file URL, which is the path
    /// MapLibre's own clustering example uses. Options were stripped to
    /// `.clustered` alone, then varied one at a time (radius, maximum cluster
    /// zoom, source zoom range, buffer). The proof that it is not our data:
    /// six bare points around Amsterdam with no properties at all, handed to a
    /// clustered source, rendered NOTHING, while the same six unclustered
    /// render six. MapLibre logs no error in any of these cases.
    ///
    /// So the source is left plain and this does the work. A grid in world
    /// space, sized so a cell is about sixty points on screen at the current
    /// zoom, which is what a thumb covers. Cells holding one tree emit that
    /// tree; cells holding more emit one bubble carrying `at_count`, which
    /// is the same attribute MapLibre's own clusters carry, so the layers and
    /// the tap handler did not have to change at all.
    ///
    /// Deliberately in WORLD space rather than screen space: clusters then stay
    /// put while you pan and only regroup when you zoom, which is how every map
    /// that does this behaves. Recomputed once per whole zoom level, so a pan
    /// costs nothing and a pinch costs one pass over the trees.
    static func cluster(on style: MLNStyle, zoom: Double, clustered: Bool, force: Bool = false) {
        let st = state(for: style)
        // OURS AND YOURS IN ONE PASS (Hidde, 2026-08-29: "zelfgemaakte bomen
        // moeten gewoon mee clusteren met de getallen als je uitzoomt"). They
        // used to live in a source of their own, which cannot cluster with
        // anything: a grid only sees the points it is handed. So a city of
        // forty trees collapsed to one bubble marked 40 with your own pin
        // hanging beside it at full size, saying nothing except that it had
        // been left out of the arithmetic.
        let all = st.leaves + st.mine
        let bucket = clustered && zoom < clusterMaxZoom ? Int(floor(zoom)) : 99
        if !force && bucket == st.lastBucket && clustered == st.lastClustered { return }
        // HYSTERESIS, or the pins blink out while you pan (Hidde, 2026-08-24:
        // "de iconen verdwijnen als ik over de map scroll"). A pan wobbles the
        // zoom by hundredths, and a wobble across a whole-number boundary used
        // to count as a new bucket: rebuilding the source means removing the
        // layers, writing a file and letting MapLibre load it, and for that
        // moment there are no pins at all. A real zoom change moves far more
        // than this; a pan never does.
        if !force && bucket != 99 && abs(zoom - st.lastClusterZoom) < 0.45 { return }
        st.lastBucket = bucket
        st.lastClustered = clustered
        st.lastClusterZoom = zoom

        if bucket == 99 {
            apply(all, on: style, clustered: clustered)
            return
        }

        // Normalised web mercator, both axes in 0...1, so the cell is a plain
        // fraction of the world and no trigonometry is needed per tree.
        let worldPoints = 512.0 * pow(2.0, zoom)
        let cell = clusterCellPoints / worldPoints
        var out: [MLNPointFeature] = []
        for indices in groups(of: all.map(\.coordinate), cell: cell) {
            let group = indices.map { all[$0] }
            if group.count == 1 {
                out.append(group[0])
                continue
            }
            let shown = min(group.count, 99)
            let icon = "at-cluster-\(shown)"
            // ON THE STYLE BEING DRAWN, not on mapRef's. mapRef is whichever
            // map loaded last, which with several maps alive is regularly not
            // this one.
            if !hasImage(icon, on: style) {
                noteImage(icon, on: style)
                style.setImage(clusterPin(count: shown), forName: icon)
            }
            let bubble = MLNPointFeature()
            var lonSum = 0.0, latSum = 0.0
            for g in group {
                lonSum += g.coordinate.longitude
                latSum += g.coordinate.latitude
            }
            bubble.coordinate = .init(latitude: latSum / Double(group.count),
                                      longitude: lonSum / Double(group.count))
            // The SAME keys as a leaf, every one of them. A feature carrying
            // a subset of the others' properties made the whole source load as
            // empty: 974 features in, zero out, no error. Measured 2026-08-24
            // by emitting the bubbles as ordinary leaves, which rendered, and
            // then putting them back, which did not.
            bubble.attributes = [countKey: group.count, idKey: "",
                                 "peaking": false,
                                 kindKey: "cluster", "at_label": String(group.count),
                                 "icon": icon]
            out.append(bubble)
        }
        apply(out, on: style, clustered: clustered)
    }

    /// The trees inside the bubble drawn at `coordinate`.
    ///
    /// Recomputed with the same grid that built the bubble rather than carried
    /// on the feature, and that is not tidiness: every feature in this source
    /// must carry exactly the SAME attribute keys or the whole source loads as
    /// empty, 974 features in and zero out with no error (see cluster()). So
    /// four bounding-box keys on a bubble would mean four dead keys on all
    /// 1,800 leaves. Regrouping costs one pass over the trees, on a tap.
    static func clusterMembers(at coordinate: CLLocationCoordinate2D,
                               on style: MLNStyle) -> [CLLocationCoordinate2D] {
        let st = state(for: style)
        guard st.lastBucket != 99 else { return [] }
        let worldPoints = 512.0 * pow(2.0, st.lastClusterZoom)
        let cell = clusterCellPoints / worldPoints
        let coords = (st.leaves + st.mine).map(\.coordinate)
        // A bubble is drawn at its group's mean, so the nearest mean is it.
        // Matching on the cell the tap fell in would be wrong at low zoom: we
        // average LATITUDE while the grid divides MERCATOR y, and those two
        // part company as cells get tall.
        var best: [CLLocationCoordinate2D] = []
        var bestDistance = Double.greatestFiniteMagnitude
        for indices in groups(of: coords, cell: cell) where indices.count > 1 {
            let group = indices.map { coords[$0] }
            var lat = 0.0, lon = 0.0
            for c in group { lat += c.latitude; lon += c.longitude }
            let dLat = lat / Double(group.count) - coordinate.latitude
            let dLon = lon / Double(group.count) - coordinate.longitude
            let d = dLat * dLat + dLon * dLon
            if d < bestDistance { bestDistance = d; best = group }
        }
        return best
    }

    /// Everything drawn from the tree source. Separate from install() because
    /// the source itself is now born in setTrees, and these have to be rebuilt
    /// with it.
    private static func addTreeLayers(on style: MLNStyle, source trees: MLNShapeSource,
                                      clustered: Bool) {
        let pins = MLNSymbolStyleLayer(identifier: treeLayer, source: trees)
        pins.iconImageName = NSExpression(forKeyPath: "icon")
        pins.iconAllowsOverlap = NSExpression(forConstantValue: true)
        pins.iconAnchor = NSExpression(forConstantValue: "center")
        pins.predicate = NSPredicate(format: "at_kind == 'tree' AND peaking != YES")
        style.addLayer(pins)

        // The halo goes UNDER the peaking pin and is the thing that breathes.
        // Its colour follows the moment, same as the pin: a ginkgo's gold, a
        // cherry's pink, from the same server-computed value the website uses.
        let halo = MLNCircleStyleLayer(identifier: haloLayer, source: trees)
        halo.predicate = NSPredicate(format: "at_kind == 'tree' AND peaking == YES")
        halo.circleColor = NSExpression(forConstantValue:
            UIColor(red: 0.85, green: 0.63, blue: 0.25, alpha: 1))
        halo.circleRadius = NSExpression(forConstantValue: 20)
        halo.circleOpacity = NSExpression(forConstantValue: 0.38)
        halo.circleRadiusTransition = MLNTransition(duration: 1.1, delay: 0)
        halo.circleOpacityTransition = MLNTransition(duration: 1.1, delay: 0)
        style.addLayer(halo)

        let peak = MLNSymbolStyleLayer(identifier: peakLayer, source: trees)
        peak.iconImageName = NSExpression(forKeyPath: "icon")
        peak.iconAllowsOverlap = NSExpression(forConstantValue: true)
        peak.iconAnchor = NSExpression(forConstantValue: "center")
        peak.predicate = NSPredicate(format: "at_kind == 'tree' AND peaking == YES")
        style.addLayer(peak)
        if clustered {
            // A SYMBOL layer with a rendered image, not a circle layer plus a
            // text layer. Two days went into the circle-and-text pair and it
            // never painted a single bubble; worse, once any feature matched
            // it, the whole source stopped rendering, leaves included, with no
            // error anywhere. Symbol layers reading `icon` are the one thing on
            // this map that has always worked, so the count is drawn into the
            // image and there is nothing left to go wrong at layer level.
            let bubble = MLNSymbolStyleLayer(identifier: clusterLayer, source: trees)
            bubble.predicate = NSPredicate(format: "at_kind == 'cluster'")
            bubble.iconImageName = NSExpression(forKeyPath: "icon")
            bubble.iconAllowsOverlap = NSExpression(forConstantValue: true)
            bubble.iconAnchor = NSExpression(forConstantValue: "center")
            style.addLayer(bubble)
        }

        // YOURS, LAST, so a tree you added sits on top of ours where they
        // overlap. It reads the same `icon` key as everything else on this
        // source: PER FEATURE, not one image for all of them, because a tree
        // you added wears YOUR photograph (Hidde, 2026-08-27: "kunnen we my
        // trees de foto in het icoontje geven aangezien je m alleen kan
        // toevoegen door een foto"). It is the only pin on this map that can
        // be a picture of the actual tree rather than a drawing of its species.
        //
        // A feature only reaches this layer when the clusterer left it
        // standing alone; inside a pile it is one of the numbers instead.
        let minePins = MLNSymbolStyleLayer(identifier: mineLayer, source: trees)
        minePins.predicate = NSPredicate(format: "at_kind == 'mine'")
        minePins.iconImageName = NSExpression(forKeyPath: "icon")
        minePins.iconAllowsOverlap = NSExpression(forConstantValue: true)
        minePins.iconAnchor = NSExpression(forConstantValue: "center")
        style.addLayer(minePins)
    }

    static func setMine(_ mine: [(id: UUID, lat: Double, lng: Double, name: String, photo: UIImage?)],
                        on style: MLNStyle, clustered: Bool, zoom: Double) {
        let features = mine.map { m -> MLNPointFeature in
            let f = MLNPointFeature()
            f.coordinate = .init(latitude: m.lat, longitude: m.lng)
            f.title = m.name
            // One image per sighting when it has a photograph, and the shared
            // drawn pin when it does not. Registered under the sighting's own
            // id, so replacing a photograph replaces the pin.
            var icon = "at-pin-mine"
            if let photo = m.photo {
                icon = "at-pin-mine-" + m.id.uuidString
                if !hasImage(icon, on: style) {
                    noteImage(icon, on: style)
                    style.setImage(photoPin(photo), forName: icon)
                }
            }
            // EXACTLY THE SAME KEYS AS EVERY OTHER FEATURE ON THIS SOURCE.
            // Not a style rule: a feature carrying a subset of the others'
            // properties makes the whole source load as empty, 974 features in
            // and zero out with no error anywhere (see cluster()). That is why
            // a tree of yours carries `peaking` and `at_count` it has no use
            // for, and it is why moving these into the shared source was a
            // one-line change away from emptying the entire map.
            f.attributes = [idKey: m.id.uuidString, "icon": icon,
                            "peaking": false, countKey: 1,
                            kindKey: "mine", "at_label": ""]
            return f
        }
        state(for: style).mine = features
        cluster(on: style, zoom: zoom, clustered: clustered, force: true)
    }

    static func setRoute(_ pts: [CLLocationCoordinate2D], real: Bool, on style: MLNStyle) {
        guard let source = style.source(withIdentifier: routeSource) as? MLNShapeSource else { return }
        guard pts.count > 1 else {
            source.shape = MLNShapeCollectionFeature(shapes: [])
            return
        }
        var coords = pts
        let line = MLNPolylineFeature(coordinates: &coords, count: UInt(coords.count))
        line.attributes = ["real": real]
        source.shape = MLNShapeCollectionFeature(shapes: [line])
    }

    private static func imageName(species: String, peaking: Bool, colour: UIColor) -> String {
        var r: CGFloat = 0, g: CGFloat = 0, b: CGFloat = 0, a: CGFloat = 0
        colour.getRed(&r, green: &g, blue: &b, alpha: &a)
        let hex = String(format: "%02X%02X%02X", Int(r * 255), Int(g * 255), Int(b * 255))
        return "at-pin-\(peaking ? "peak-" : "")\(hex)-\(species.replacingOccurrences(of: " ", with: "_"))"
    }

    /// One pin, drawn once per species-and-colour and then cached by the style.
    /// A filled circle with a white ring and the species silhouette knocked out
    /// of it in white, which is the website's pin translated into a bitmap.
    /// A pin, and whether you have already stood in front of that tree.
    ///
    /// Three states existed on this map and only two of them looked different:
    /// a tree you added yourself has always had its own pin, and one of OURS
    /// that you had collected was drawn exactly like one you had never seen
    /// (Hidde, 2026-08-24: "mss met een ander pin vertoning voor collected en
    /// toegevoegd"). The mark is a small white disc with a check, bottom right,
    /// which is where Google Maps hangs its saved-place flag and what the
    /// Collected control in this app already uses as its symbol.
    private static func pin(colour: UIColor, glyph: UIImage?, collected: Bool = false,
                            ticket: Bool = false, favourite: Bool = false) -> UIImage {
        let d: CGFloat = 38
        return UIGraphicsImageRenderer(size: .init(width: d, height: d)).image { _ in
            colour.setFill()
            UIBezierPath(ovalIn: .init(x: 2, y: 2, width: d - 4, height: d - 4)).fill()
            UIColor.white.setStroke()
            let ring = UIBezierPath(ovalIn: .init(x: 2.5, y: 2.5, width: d - 5, height: d - 5))
            ring.lineWidth = 3
            ring.stroke()
            if let glyph {
                let s: CGFloat = 20
                glyph.withTintColor(.white, renderingMode: .alwaysOriginal)
                    .draw(in: .init(x: (d - s) / 2, y: (d - s) / 2, width: s, height: s))
            }
            if ticket {
                // A TICKET, bottom left, a little bigger than the collected
                // tick (Hidde, 2026-08-24: "een ticket icoon op de boom zoals
                // de vink als je m hebt gezien maar iets groter"). Blue, not
                // gold: gold is the Plus colour everywhere else in this app,
                // and sharing it made a ticket read as one of our paid
                // features (Hidde, 2026-08-25: "omdat je die ticket nu
                // dezelfde kleur hebt gegeven als plus, lijkt het alsof dat
                // samenhoort... ik wil die tickets licht donkerblauw of zo").
                // What the 08-24 note above was right about stands: it is a
                // condition on the visit rather than a thing you have done,
                // so it is not moss either. Left, so a tree can wear both.
                //
                // APPLE'S OWN GLYPH, not one of ours. The first version was a
                // hand-drawn stub with a notch out of each side, and Hidde's
                // verdict was the right one: "het ticket icoon silhouet zelf
                // is niet goed, kies een andere meer standaard benchmark
                // convention, nobody understands this" (2026-08-25). A symbol
                // invented for a 17 point circle is a symbol nobody has been
                // trained on, and this project's own rule is to take the
                // published asset wherever one exists. `ticket.fill` is what
                // Wallet and every Apple surface use for exactly this, so it
                // arrives already learned.
                let b: CGFloat = 17
                let r = CGRect(x: 1, y: d - b - 1, width: b, height: b)
                UIColor.white.setFill()
                UIBezierPath(ovalIn: r).fill()
                let blue = UIColor(red: 0.18, green: 0.42, blue: 0.66, alpha: 1)
                if let glyph = UIImage(systemName: "ticket.fill")?
                    .withConfiguration(UIImage.SymbolConfiguration(pointSize: 9,
                                                                   weight: .bold))
                    .withTintColor(blue, renderingMode: .alwaysOriginal) {
                    let s = glyph.size
                    glyph.draw(in: CGRect(x: r.midX - s.width / 2,
                                          y: r.midY - s.height / 2,
                                          width: s.width, height: s.height))
                } else {
                    blue.setFill()
                    UIBezierPath(ovalIn: r.insetBy(dx: 4, dy: 4)).fill()
                }
            }
            if favourite {
                // TOP RIGHT, because the other two corners are taken: the
                // ticket sits bottom left and the collected tick bottom right,
                // and a tree can wear all three at once. Red rather than moss:
                // a heart is red in every app anybody has used, and the heart
                // on our own cards is already red, so the map agrees with the
                // list.
                let b: CGFloat = 15
                let r = CGRect(x: d - b - 1, y: 1, width: b, height: b)
                UIColor.white.setFill()
                UIBezierPath(ovalIn: r).fill()
                let red = UIColor(red: 0.85, green: 0.20, blue: 0.24, alpha: 1)
                if let heart = UIImage(systemName: "heart.fill")?
                    .withConfiguration(UIImage.SymbolConfiguration(pointSize: 8,
                                                                   weight: .bold))
                    .withTintColor(red, renderingMode: .alwaysOriginal) {
                    let sz = heart.size
                    heart.draw(in: CGRect(x: r.midX - sz.width / 2,
                                          y: r.midY - sz.height / 2,
                                          width: sz.width, height: sz.height))
                } else {
                    red.setFill()
                    UIBezierPath(ovalIn: r.insetBy(dx: 4, dy: 4)).fill()
                }
            }
            if collected {
                let b: CGFloat = 15
                let r = CGRect(x: d - b - 1, y: d - b - 1, width: b, height: b)
                UIColor.white.setFill()
                UIBezierPath(ovalIn: r).fill()
                let tick = UIBezierPath()
                tick.move(to: .init(x: r.minX + 4.0, y: r.midY))
                tick.addLine(to: .init(x: r.midX - 0.6, y: r.maxY - 4.4))
                tick.addLine(to: .init(x: r.maxX - 3.6, y: r.minY + 4.6))
                tick.lineWidth = 2.2
                tick.lineCapStyle = .round
                tick.lineJoinStyle = .round
                colour.setStroke()
                tick.stroke()
            }
        }
    }

    /// A cluster bubble with its number already drawn in. Moss, white ring,
    /// white figure, and it grows a little with the count so a pile of forty
    /// reads as bigger than a pair.
    private static func clusterPin(count: Int) -> UIImage {
        let d: CGFloat = count >= 25 ? 46 : (count >= 10 ? 40 : 34)
        let size = CGSize(width: d, height: d)
        return UIGraphicsImageRenderer(size: size).image { ctx in
            let rect = CGRect(origin: .zero, size: size).insetBy(dx: 2, dy: 2)
            moss.setFill()
            UIColor.white.setStroke()
            let path = UIBezierPath(ovalIn: rect)
            path.lineWidth = 3
            path.fill()
            path.stroke()
            let text = "\(count)"
            let font = UIFont.systemFont(ofSize: d * 0.42, weight: .bold)
            let attrs: [NSAttributedString.Key: Any] = [
                .font: font, .foregroundColor: UIColor.white,
            ]
            let bounds = (text as NSString).size(withAttributes: attrs)
            (text as NSString).draw(
                at: CGPoint(x: (size.width - bounds.width) / 2,
                            y: (size.height - bounds.height) / 2),
                withAttributes: attrs)
            _ = ctx
        }
    }

    /// A tree of your own: the same pin as ours, INVERTED.
    ///
    /// It used to be a white disc with a moss dot in it, which is the shape
    /// every map uses for "a point" and says nothing about trees (Hidde,
    /// 2026-08-24: "het icoontje van een zelf toegevoegde boom is ook gek").
    /// Same size, same ring, same silhouette as ours; white where ours is moss
    /// and moss where ours is white. One family, and you can see at a glance
    /// which ones are yours without a badge explaining it.
    /// YOUR photograph, in the pin, behind a dark ring.
    ///
    /// NOT GOLD, and that was a real mistake rather than a preference. Gold
    /// means paid-by-us everywhere in this app (DECISIONS.md, 2026-08-25, which
    /// is also why the ticket mark left gold for blue), so a gold ring around
    /// somebody's own free contribution says the opposite of what it means. The
    /// fresh-eyes reviewer caught it the same day it shipped; Hidde's answer
    /// was "doe maar een andere kleur, als het maar herkenbaar is".
    ///
    /// Ink, because every other colour on this map is spoken for: moss is ours,
    /// white is the ring every pin wears, blue is a ticket, gold is Plus, red is
    /// the heart. A dark ring also reads as a frame around a photograph, which
    /// is what this is.
    ///
    /// The picture is drawn as a circle rather than a square, so it reads as a
    /// pin at a glance rather than as a photograph pasted on the map, which is
    /// what Google Maps does with a contributed image and Strava with a segment
    /// photograph.
    private static func photoPin(_ image: UIImage) -> UIImage {
        // THE SAME GEOMETRY AS pin(), rectangle for rectangle, and that is
        // the third time this has been asked for (Hidde, 2026-08-28: "het icoon
        // van mijn boom met de foto is groter dan de rest", and again on
        // 08-29). The first answer only matched the CANVAS: both images are
        // 38 points, and inside them ours drew a 34 point disc while this one
        // filled the whole 38, so on screen a tree of yours still stood a
        // couple of points wider than every tree beside it. A canvas nobody can
        // see is not the size anybody was talking about.
        //
        // So the numbers below are pin()'s numbers and nothing else: the same
        // (2, 2, 34, 34) body, the same ring stroked at (2.5, 2.5, 33, 33) with
        // the same width, which puts the outer edge of both at exactly the same
        // radius. Change one and change the other.
        let d: CGFloat = 38
        let body = CGRect(x: 2, y: 2, width: d - 4, height: d - 4)
        return UIGraphicsImageRenderer(size: .init(width: d, height: d)).image { ctx in
            // A white disc under the photograph, so one with a pale edge still
            // has a rim against a pale map.
            UIColor.white.setFill()
            UIBezierPath(ovalIn: body).fill()

            ctx.cgContext.saveGState()
            UIBezierPath(ovalIn: body).addClip()
            // ASPECT FILL, so a portrait photograph is not squeezed into a
            // circle: scale by the SHORT side and centre what is left over.
            let scale = max(body.width / image.size.width, body.height / image.size.height)
            let w = image.size.width * scale, h = image.size.height * scale
            image.draw(in: CGRect(x: body.midX - w / 2, y: body.midY - h / 2, width: w, height: h))
            ctx.cgContext.restoreGState()

            // Ink where ours is white, which is the whole of how you tell them
            // apart now that they are the same size.
            ink.setStroke()
            let ring = UIBezierPath(ovalIn: .init(x: 2.5, y: 2.5, width: d - 5, height: d - 5))
            ring.lineWidth = 3
            ring.stroke()
        }
    }

    private static func minePin() -> UIImage {
        let d: CGFloat = 38
        return UIGraphicsImageRenderer(size: .init(width: d, height: d)).image { _ in
            UIColor.white.setFill()
            UIBezierPath(ovalIn: .init(x: 2, y: 2, width: d - 4, height: d - 4)).fill()
            moss.setStroke()
            let ring = UIBezierPath(ovalIn: .init(x: 2.5, y: 2.5, width: d - 5, height: d - 5))
            ring.lineWidth = 3
            ring.stroke()
            if let glyph = SpeciesGlyph.image(for: "") {
                let sz: CGFloat = 20
                glyph.withTintColor(moss, renderingMode: .alwaysOriginal)
                    .draw(in: .init(x: (d - sz) / 2, y: (d - sz) / 2, width: sz, height: sz))
            }
        }
    }
}

/// Back to yourself. MKUserTrackingButton was Apple's control and every iOS user
/// had used it in Maps; MapLibre has no equivalent, so this is the same idea in
/// the same place, drawn to match. Without it there is no way back to yourself
/// once you have panned away, which on a map whose whole premise is "near you"
/// is the one control you cannot leave out.
final class RecentreButton: UIButton {
    private weak var map: MLNMapView?

    init(map: MLNMapView) {
        self.map = map
        super.init(frame: .zero)
        backgroundColor = UIColor.systemBackground.withAlphaComponent(0.92)
        layer.cornerRadius = 10
        layer.shadowColor = UIColor.black.cgColor
        layer.shadowOpacity = 0.15
        layer.shadowRadius = 5
        layer.shadowOffset = CGSize(width: 0, height: 2)
        tintColor = UIColor(red: 0.20, green: 0.35, blue: 0.20, alpha: 1)
        setImage(UIImage(systemName: "location.fill"), for: .normal)
        accessibilityLabel = "Back to my location"
        accessibilityIdentifier = "map-recentre"
        addTarget(self, action: #selector(recentre), for: .touchUpInside)
    }

    required init?(coder: NSCoder) { fatalError("init(coder:) has not been implemented") }

    /// Back to you, AND north back to the top.
    ///
    /// Both, on one button, because that is what Hidde asked for and because
    /// they are the same wish: a map you have wandered and turned, put back the
    /// way it started. It used to TOGGLE tracking, so a second press left you
    /// wherever you had scrolled to and a turned map stayed turned.
    @objc private func recentre() {
        guard let map else { return }
        let status = CLLocationManager().authorizationStatus
        guard status == .authorizedWhenInUse || status == .authorizedAlways else { return }
        map.showsUserLocation = true
        map.setUserTrackingMode(.follow, animated: true)
        if map.direction != 0 { map.setDirection(0, animated: true) }
    }
}

/// The species silhouettes as pin glyphs. SwiftUI draws them, ImageRenderer
/// turns them into a UIImage, and the result is cached because there are only
/// fifteen shapes and a map asks for them constantly.
/// @MainActor because ImageRenderer is. The local Debug build accepted the
/// nonisolated version and the iOS CI job did not: strict concurrency catches
/// what a permissive local build waves through, which is the whole reason that
/// job exists.
@MainActor
enum SpeciesGlyph {
    private static var cache: [String: UIImage] = [:]

    static func image(for commonName: String) -> UIImage? {
        if let hit = cache[commonName] { return hit }
        let renderer = ImageRenderer(content:
            SpeciesMark(species: commonName, color: .white)
                .frame(width: 22, height: 22))
        renderer.scale = UIScreen.main.scale
        guard let img = renderer.uiImage?.withRenderingMode(.alwaysTemplate) else { return nil }
        cache[commonName] = img
        return img
    }
}

extension UIColor {
    /// #RRGGBB from the feed. Returns nil rather than black on anything it does
    /// not understand, so a bad colour falls back to the default rather than
    /// painting a pin the colour of a hole in the map.
    convenience init?(hex: String?) {
        guard var h = hex?.trimmingCharacters(in: .whitespaces) else { return nil }
        if h.hasPrefix("#") { h.removeFirst() }
        guard h.count == 6, let v = UInt32(h, radix: 16) else { return nil }
        self.init(red: CGFloat((v >> 16) & 0xFF) / 255,
                  green: CGFloat((v >> 8) & 0xFF) / 255,
                  blue: CGFloat(v & 0xFF) / 255, alpha: 1)
    }
}
