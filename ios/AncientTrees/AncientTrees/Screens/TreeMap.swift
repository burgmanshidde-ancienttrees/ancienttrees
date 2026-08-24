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
    var mine: [(id: UUID, lat: Double, lng: Double, name: String)] = []
    /// Ours that you have already stood in front of. Only changes the pin.
    var collected: Set<String> = []
    /// Tapping a tree of your own opens its page, the same as one of ours.
    /// A callback because this view knows nothing about navigation.
    var onSelectMine: ((UUID) -> Void)? = nil
    var focus: CLLocationCoordinate2D?
    /// A walk's line. Real when route_walks.py cached a routed shape, otherwise
    /// the order the trees are visited, which is NOT the path a walker takes.
    var route: [CLLocationCoordinate2D] = []
    var routeIsReal = true
    /// Off on a walk's map, where the camera belongs to the route.
    var showsRecentre = false
    /// How tall the sheet in front of this map is, so the recentre control can
    /// sit ABOVE it. It was pinned 120 points off the bottom, which was clear
    /// of the sheet's peek and behind every other stop it has: the button has
    /// been invisible since the sheet grew (Hidde, 2026-08-24: "de knop mist
    /// waar je naar je locatie gaat").
    var sheetLift: SheetHeight = .peek
    /// How wide the first look is. Four kilometres suits "what is near me"; a
    /// tree's own page wants the street it stands in, and at four kilometres the
    /// tree itself disappears into a cluster bubble.
    var spanMeters: CLLocationDistance = 4000
    /// Off on a tree's own page. Clustering is right when the question is "what
    /// is around here" and wrong when the answer is already known: the subject
    /// of the page was disappearing into a bubble marked 11.
    var clusters = true
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
        let map = MLNMapView(frame: .zero, styleURL: MapStyle.url)
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
        map.compassView.isHidden = true
        map.attributionButton.tintColor = UIColor(white: 0.45, alpha: 1)

        // Taps are read off the STYLE LAYERS rather than from annotation views,
        // because clustering lives on the source and a cluster is a feature, not
        // a view. One recogniser, three questions, in the order a finger means
        // them: a cluster first, then a tree, then nothing.
        let tap = UITapGestureRecognizer(target: context.coordinator,
                                         action: #selector(Coordinator.handleTap(_:)))
        for existing in map.gestureRecognizers ?? [] where existing is UITapGestureRecognizer {
            tap.require(toFail: existing)     // let a double tap zoom in peace
        }
        map.addGestureRecognizer(tap)

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

        if let focus {
            map.setCenter(focus, zoomLevel: Self.zoom(forMeters: spanMeters), animated: false)
        }
        return map
    }

    func updateUIView(_ map: MLNMapView, context: Context) {
        context.coordinator.parent = self
        // Keep the recentre control just above the sheet, whatever stop the
        // sheet is at. 12 points of air, and never lower than the old 120 so a
        // map with no sheet in front of it looks the same as before.
        if let lift = context.coordinator.recentreLift, map.bounds.height > 0 {
            let want = -(sheetLift.points(in: map.bounds.height) + 12)
            let clamped = min(want, -120)
            if abs(lift.constant - clamped) > 1 { lift.constant = clamped }
        }

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
                              mine: [(id: UUID, lat: Double, lng: Double, name: String)],
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
            MapLayers.mapRef = map
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
                  mine: [(id: UUID, lat: Double, lng: Double, name: String)],
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
            let wantTrees = Set(trees.map(\.id)).union(
                parent.collected.intersection(trees.map(\.id)).map { "c:" + $0 })
            let wantMine = Set(mine.map { $0.id.uuidString })
            MainActor.assumeIsolated {
            if wantTrees != drawnTreeIDs {
                drawnTreeIDs = wantTrees
                MapLayers.setTrees(trees, on: style, clustered: clusters,
                                   collected: parent.collected)
            }
            if wantMine != drawnMineIDs {
                drawnMineIDs = wantMine
                MapLayers.setMine(mine, on: style)
            }
            if route.count != drawnRoute {
                drawnRoute = route.count
                MapLayers.setRoute(route, real: routeIsReal, on: style)
            }
            }
        }

        // MARK: interaction

        @objc func handleTap(_ g: UITapGestureRecognizer) {
            guard let map = g.view as? MLNMapView else { return }
            let point = g.location(in: map)
            // A finger is wider than a pixel. Ask over a small square so a tap
            // near a pin counts as a tap on it, which is what every map does.
            let box = CGRect(x: point.x - 22, y: point.y - 22, width: 44, height: 44)

            let clusterHits = map.visibleFeatures(in: box,
                                                  styleLayerIdentifiers: [MapLayers.clusterLayer])
            if let cluster = clusterHits.first {
                // Tapping a pile zooms into it rather than opening anything,
                // which is what Google Maps does and what a pile of pins needs.
                map.setCenter(cluster.coordinate,
                              zoomLevel: min(map.zoomLevel + 2.0, 17),
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
                parent.selected = tree
            }
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
    static let mineSource = "at-mine"
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
    /// Which pin images this style already carries. See setTrees for why this
    /// is not a question asked of MLNStyle.
    private static var registered: Set<String> = []
    /// Clustering options, set by install() and used by setTrees when it builds
    /// the source. They cannot be applied later: a source is clustered or not
    /// from birth.
    private static var treeOptions: [MLNShapeSourceOption: Any] = [:]
    private static var writeCount = 0
    /// The identifier the live tree source currently carries. See apply().
    private static var liveSourceID = treeSource
    /// The map itself, so clustering can read the current zoom. Weak: the
    /// style outlives nothing here, and a strong reference would keep a dead
    /// map view alive.
    static weak var mapRef: MLNMapView?

    static func install(on style: MLNStyle, clustered: Bool) {
        registered.removeAll()
        style.setImage(pin(colour: moss, glyph: nil), forName: "at-pin-default")
        style.setImage(minePin(), forName: "at-pin-mine")

        var options: [MLNShapeSourceOption: Any] = [:]
        if clustered {
            // NSNumber, explicitly. These cross into Objective-C and a Swift Int
            // or Bool does not always arrive as the number the clusterer expects;
            // a mis-read radius is indistinguishable from "everything is one
            // cluster", which is exactly what the map was showing.
            options[.clustered] = NSNumber(value: true)
            options[.clusterRadius] = NSNumber(value: 44)
            // Past this the pile has to open, or the subject of a tree page
            // disappears into a bubble marked 11.
            options[.maximumZoomLevelForClustering] = NSNumber(value: 15)
        }
        // The source is NEVER given MapLibre's own clustering options. They do
        // not work: see the note on cluster() below. We cluster ourselves and
        // hand this source the result, so from its point of view it is a plain
        // collection of points.
        // No tree source here. apply() is the only place one is ever made,
        // because a source that has already existed under this identifier does
        // not load: see the note there.
        _ = options
        liveSourceID = treeSource
        let mine = MLNShapeSource(identifier: mineSource, shape: nil, options: nil)
        style.addSource(mine)
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

        let minePins = MLNSymbolStyleLayer(identifier: mineLayer, source: mine)
        minePins.iconImageName = NSExpression(forConstantValue: "at-pin-mine")
        minePins.iconAllowsOverlap = NSExpression(forConstantValue: true)
        style.addLayer(minePins)

    }

    static func setTrees(_ trees: [Tree], on style: MLNStyle, clustered: Bool,
                         collected: Set<String> = []) {
        let month = Calendar.current.component(.month, from: Date())
        var features: [MLNPointFeature] = []
        for t in trees {
            let f = MLNPointFeature()
            f.coordinate = .init(latitude: t.lat, longitude: t.lng)
            f.title = t.name
            let peaking = t.peak?.isNow(month) ?? false
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
            let name = imageName(species: t.commonName, peaking: peaking, colour: colour)
                + (seen ? "-c" : "")
            // Our own register of what has been added, rather than asking the
            // style whether it already has the image. That check drew exactly
            // ONE pin for eleven trees: whatever style.image(forName:) returns
            // for a name it has never seen, it is not reliably nil, so after the
            // first species every later icon name pointed at nothing and
            // MapLibre silently drew nothing. Found in a screenshot, not in a log.
            if !registered.contains(name) {
                registered.insert(name)
                style.setImage(pin(colour: colour,
                                   glyph: SpeciesGlyph.image(for: t.commonName),
                                   collected: seen),
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
        leaves = features
        cluster(on: style, zoom: mapRef?.zoomLevel ?? 12, clustered: clustered, force: true)
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
        writeCount += 1
        let file = FileManager.default.temporaryDirectory
            .appendingPathComponent("at-trees-\(writeCount).geojson")
        guard (try? data.write(to: file)) != nil else { return }

        for id in [clusterCount, clusterLayer, peakLayer, haloLayer, treeLayer] {
            if let layer = style.layer(withIdentifier: id) { style.removeLayer(layer) }
        }
        // A NEW identifier as well as a new file. Re-adding a source under an
        // identifier the style has just seen leaves it holding nothing: the
        // file is read, no error is raised, and `features(matching:)` returns
        // zero. Measured, 2026-08-24. The layer identifiers stay fixed, which
        // is what the tap handler reads, so nothing downstream notices.
        if let old = style.source(withIdentifier: liveSourceID) { style.removeSource(old) }
        liveSourceID = "\(treeSource)-\(writeCount)"
        let source = MLNShapeSource(identifier: liveSourceID, url: file, options: [:])
        style.addSource(source)
        addTreeLayers(on: style, source: source, clustered: clustered)
        // Yesterday's file is no longer read once the new source is in.
        let stale = FileManager.default.temporaryDirectory
            .appendingPathComponent("at-trees-\(writeCount - 1).geojson")
        try? FileManager.default.removeItem(at: stale)
    }

    /// Every tree as a point feature, kept so clustering can be recomputed on a
    /// zoom change without rebuilding any of this.
    private static var leaves: [MLNPointFeature] = []
    private static var lastBucket: Int = .min
    private static var lastClustered = true

    /// Past this there is nothing left to pile up, and the subject of a tree
    /// page should not disappear into a bubble marked 11.
    private static let clusterMaxZoom = 15.0
    /// How close two pins have to be, in points, before they become one bubble.
    private static let clusterCellPoints = 60.0

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
        let bucket = clustered && zoom < clusterMaxZoom ? Int(floor(zoom)) : 99
        if !force && bucket == lastBucket && clustered == lastClustered { return }
        lastBucket = bucket
        lastClustered = clustered

        if bucket == 99 {
            apply(leaves, on: style, clustered: clustered)
            return
        }

        // Normalised web mercator, both axes in 0...1, so the cell is a plain
        // fraction of the world and no trigonometry is needed per tree.
        let worldPoints = 512.0 * pow(2.0, zoom)
        let cell = clusterCellPoints / worldPoints
        var cells: [Int64: [MLNPointFeature]] = [:]
        for f in leaves {
            let x = (f.coordinate.longitude + 180.0) / 360.0
            let lat = min(max(f.coordinate.latitude, -85.05), 85.05) * .pi / 180.0
            let y = (1.0 - log(tan(lat) + 1.0 / cos(lat)) / .pi) / 2.0
            let key = Int64(floor(x / cell)) &* 100_000 &+ Int64(floor(y / cell))
            cells[key, default: []].append(f)
        }

        var out: [MLNPointFeature] = []
        out.reserveCapacity(cells.count)
        for (_, group) in cells {
            if group.count == 1 {
                out.append(group[0])
                continue
            }
            let shown = min(group.count, 99)
            let icon = "at-cluster-\(shown)"
            if !registered.contains(icon), let style = mapRef?.style {
                registered.insert(icon)
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
        insertUnderMine(pins, on: style)

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
        insertUnderMine(halo, on: style)

        let peak = MLNSymbolStyleLayer(identifier: peakLayer, source: trees)
        peak.iconImageName = NSExpression(forKeyPath: "icon")
        peak.iconAllowsOverlap = NSExpression(forConstantValue: true)
        peak.iconAnchor = NSExpression(forConstantValue: "center")
        peak.predicate = NSPredicate(format: "at_kind == 'tree' AND peaking == YES")
        insertUnderMine(peak, on: style)
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
    }

    /// Tree pins belong under a person's own pins, which is where they sat
    /// before the source started being rebuilt.
    private static func insertUnderMine(_ layer: MLNStyleLayer, on style: MLNStyle) {
        if let mine = style.layer(withIdentifier: mineLayer) {
            style.insertLayer(layer, below: mine)
        } else {
            style.addLayer(layer)
        }
    }

    static func setMine(_ mine: [(id: UUID, lat: Double, lng: Double, name: String)],
                        on style: MLNStyle) {
        guard let source = style.source(withIdentifier: mineSource) as? MLNShapeSource else { return }
        let features = mine.map { m -> MLNPointFeature in
            let f = MLNPointFeature()
            f.coordinate = .init(latitude: m.lat, longitude: m.lng)
            f.title = m.name
            f.attributes = [idKey: m.id.uuidString]
            return f
        }
        source.shape = MLNShapeCollectionFeature(shapes: features)
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
    private static func pin(colour: UIColor, glyph: UIImage?, collected: Bool = false) -> UIImage {
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
