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
    var focus: CLLocationCoordinate2D?
    /// A walk's line. Real when route_walks.py cached a routed shape, otherwise
    /// the order the trees are visited, which is NOT the path a walker takes.
    var route: [CLLocationCoordinate2D] = []
    var routeIsReal = true
    /// Off on a walk's map, where the camera belongs to the route.
    var showsRecentre = false
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
            NSLayoutConstraint.activate([
                recentre.trailingAnchor.constraint(equalTo: map.safeAreaLayoutGuide.trailingAnchor, constant: -12),
                // 120 puts it just above the lip of the sheet rather than behind it.
                recentre.bottomAnchor.constraint(equalTo: map.bottomAnchor, constant: -120),
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
    static func zoom(forMeters m: CLLocationDistance, latitude: Double = 52) -> Double {
        // 512, not 256. MapLibre's zoom is defined against 512-point tiles, and
        // using the 256 figure from the web slippy-map convention put every
        // camera one whole level too close: asking for four kilometres gave
        // about two, so the map opened on a single tree where the old MapKit
        // version showed the city and its clusters. It looked like clustering
        // was broken and it was arithmetic.
        let metresPerPointAtZoomZero = (40_075_017.0 / 512.0) * cos(latitude * .pi / 180)
        let width = 375.0                       // the narrow phone, our reference
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

        init(_ p: TreeMap) { parent = p }
        deinit { breath?.invalidate() }

        // MARK: style

        func mapView(_ map: MLNMapView, didFinishLoading style: MLNStyle) {
            MapLayers.install(on: style, clustered: parent.clusters)
            styleReady = true
            if let p = pending {
                pending = nil
                sync(trees: p.trees, mine: p.mine, route: p.route,
                     routeIsReal: p.routeIsReal, clusters: p.clusters, on: map)
            }
            startBreathing(on: style)
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
            let wantTrees = Set(trees.map(\.id))
            let wantMine = Set(mine.map { $0.id.uuidString })
            if wantTrees != drawnTreeIDs {
                drawnTreeIDs = wantTrees
                MapLayers.setTrees(trees, on: style)
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
            // While a tree is selected the camera is being driven by the pager,
            // so reporting the region back would rebuild the list under the
            // pager and shuffle what you are swiping through.
            guard parent.selected == nil, let binding = parent.region else { return }
            let now = TreeMap.region(map.visibleCoordinateBounds)
            if let last = binding.wrappedValue {
                let a = CLLocation(latitude: last.center.latitude, longitude: last.center.longitude)
                let b = CLLocation(latitude: now.center.latitude, longitude: now.center.longitude)
                guard a.distance(from: b) > 300
                        || abs(last.span.latitudeDelta - now.span.latitudeDelta) > 0.01
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

    private static let moss = UIColor(red: 0.20, green: 0.35, blue: 0.20, alpha: 1)
    /// Which pin images this style already carries. See setTrees for why this
    /// is not a question asked of MLNStyle.
    private static var registered: Set<String> = []

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
        let trees = MLNShapeSource(identifier: treeSource, shape: nil, options: options)
        style.addSource(trees)
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

        let pins = MLNSymbolStyleLayer(identifier: treeLayer, source: trees)
        pins.iconImageName = NSExpression(forKeyPath: "icon")
        pins.iconAllowsOverlap = NSExpression(forConstantValue: true)
        pins.iconAnchor = NSExpression(forConstantValue: "center")
        pins.predicate = NSPredicate(format: "point_count == nil AND peaking != YES")
        style.addLayer(pins)

        // The halo goes UNDER the peaking pin and is the thing that breathes.
        // Its colour follows the moment, same as the pin: a ginkgo's gold, a
        // cherry's pink, from the same server-computed value the website uses.
        let halo = MLNCircleStyleLayer(identifier: haloLayer, source: trees)
        halo.predicate = NSPredicate(format: "point_count == nil AND peaking == YES")
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
        peak.predicate = NSPredicate(format: "point_count == nil AND peaking == YES")
        style.addLayer(peak)

        let minePins = MLNSymbolStyleLayer(identifier: mineLayer, source: mine)
        minePins.iconImageName = NSExpression(forConstantValue: "at-pin-mine")
        minePins.iconAllowsOverlap = NSExpression(forConstantValue: true)
        style.addLayer(minePins)

        if clustered {
            let bubble = MLNCircleStyleLayer(identifier: clusterLayer, source: trees)
            bubble.predicate = NSPredicate(format: "point_count > 0")
            bubble.circleColor = NSExpression(forConstantValue: moss)
            bubble.circleStrokeColor = NSExpression(forConstantValue: UIColor.white)
            bubble.circleStrokeWidth = NSExpression(forConstantValue: 3)
            // A step expression on point_count was the first attempt and drew
            // nothing at all: a malformed expression does not throw, the layer
            // simply never paints, so eleven trees showed as one lone pin and
            // no bubbles. Found by looking at the screenshot rather than by any
            // error. Plain numbers, and the bubble grows by zoom instead.
            bubble.circleRadius = NSExpression(forConstantValue: 20)
            style.addLayer(bubble)

            let count = MLNSymbolStyleLayer(identifier: clusterCount, source: trees)
            count.predicate = NSPredicate(format: "point_count > 0")
            count.text = NSExpression(forKeyPath: "point_count")
            count.textColor = NSExpression(forConstantValue: UIColor.white)
            count.textFontSize = NSExpression(forConstantValue: 15)
            count.textFontNames = NSExpression(forConstantValue: ["Noto Sans Bold", "Noto Sans Regular"])
            count.textAllowsOverlap = NSExpression(forConstantValue: true)
            style.addLayer(count)
        }
    }

    static func setTrees(_ trees: [Tree], on style: MLNStyle) {
        guard let source = style.source(withIdentifier: treeSource) as? MLNShapeSource else { return }
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
            let name = imageName(species: t.commonName, peaking: peaking, colour: colour)
            // Our own register of what has been added, rather than asking the
            // style whether it already has the image. That check drew exactly
            // ONE pin for eleven trees: whatever style.image(forName:) returns
            // for a name it has never seen, it is not reliably nil, so after the
            // first species every later icon name pointed at nothing and
            // MapLibre silently drew nothing. Found in a screenshot, not in a log.
            if !registered.contains(name) {
                registered.insert(name)
                style.setImage(pin(colour: colour, glyph: SpeciesGlyph.image(for: t.commonName)),
                               forName: name)
            }
            // Attributes must be values GeoJSON can hold: strings, numbers,
            // booleans. A UIColor in here made every feature invalid and the
            // map drew ONE pin for fourteen hundred trees, silently. The peak
            // colour still reaches the eye where it matters, baked into the pin
            // image itself; the halo underneath takes one warm tone for all of
            // them, which reads as a season rather than as a paint chart.
            f.attributes = [idKey: t.id, "icon": name, "peaking": peaking]
            features.append(f)
        }
        // Handed over as real GeoJSON rather than as an MLNShapeCollectionFeature.
        // That type works perfectly for an unclustered source and is invisible
        // to the clusterer: with clustering on, the whole collection arrived as
        // ONE thing, so fourteen hundred trees drew as a single pin and it
        // looked like the cluster layers were broken. They were not. Proven by
        // turning clustering off, at which point every pin appeared.
        let json: [String: Any] = [
            "type": "FeatureCollection",
            "features": features.map { f -> [String: Any] in
                [
                    "type": "Feature",
                    "geometry": ["type": "Point",
                                 "coordinates": [f.coordinate.longitude, f.coordinate.latitude]],
                    "properties": f.attributes,
                ]
            },
        ]
        if let data = try? JSONSerialization.data(withJSONObject: json),
           let shape = try? MLNShape(data: data, encoding: String.Encoding.utf8.rawValue) {
            source.shape = shape
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
    private static func pin(colour: UIColor, glyph: UIImage?) -> UIImage {
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
        }
    }

    private static func minePin() -> UIImage {
        let d: CGFloat = 30
        return UIGraphicsImageRenderer(size: .init(width: d, height: d)).image { _ in
            UIColor.white.setFill()
            UIBezierPath(ovalIn: .init(x: 1, y: 1, width: d - 2, height: d - 2)).fill()
            moss.setStroke()
            let ring = UIBezierPath(ovalIn: .init(x: 2, y: 2, width: d - 4, height: d - 4))
            ring.lineWidth = 3
            ring.stroke()
            moss.setFill()
            UIBezierPath(ovalIn: .init(x: d / 2 - 4, y: d / 2 - 4, width: 8, height: 8)).fill()
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

    @objc private func recentre() {
        guard let map else { return }
        let status = CLLocationManager().authorizationStatus
        guard status == .authorizedWhenInUse || status == .authorizedAlways else { return }
        map.showsUserLocation = true
        map.setUserTrackingMode(map.userTrackingMode == .none ? .follow : .none, animated: true)
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
