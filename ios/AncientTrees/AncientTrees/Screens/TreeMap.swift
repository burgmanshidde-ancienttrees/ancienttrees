// The map, built on MKMapView rather than SwiftUI's Map for one reason:
// clustering. Our own website stacks about ten Amsterdam pins into an
// unreadable pile at city zoom, which is the single biggest visible gap between
// Google Maps' map and ours, and MKMapView gives real zoom-dependent clustering
// for free while SwiftUI's Map does not.
//
// MapKit rather than MapLibre deliberately. MapLibre would be a third-party
// dependency in the product, which needs Hidde's yes under hard rule 5; MapKit
// ships with iOS, needs no key and no account, and the stack here is
// deliberately boring. The cost is that the app's map does not look like the
// website's Positron, and that is a trade worth naming rather than hiding.

import SwiftUI
import MapKit

final class TreeAnnotation: NSObject, MKAnnotation {
    let tree: Tree
    var coordinate: CLLocationCoordinate2D { .init(latitude: tree.lat, longitude: tree.lng) }
    var title: String? { tree.name }
    var subtitle: String? { tree.commonName }
    init(_ t: Tree) { tree = t }
}

struct TreeMap: UIViewRepresentable {
    let trees: [Tree]
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
    /// can be a list of what you are looking at. Optional because a walk's map
    /// does not want it.
    var region: Binding<MKCoordinateRegion?>? = nil
    /// Somewhere to GO, as opposed to `region`, which is where the map has
    /// been. Carries its own token so the same request cannot be applied twice
    /// and a finger can pan away from it afterwards.
    var moveTo: (token: UUID, region: MKCoordinateRegion)? = nil
    @Binding var selected: Tree?

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    func makeUIView(context: Context) -> MKMapView {
        let map = MKMapView()
        map.delegate = context.coordinator
        map.showsUserLocation = true
        map.pointOfInterestFilter = .excludingAll   // our pins are the point
        TreePinView.clusteringEnabled = clusters
        map.register(TreePinView.self,
                     forAnnotationViewWithReuseIdentifier: MKMapViewDefaultAnnotationViewReuseIdentifier)
        map.register(ClusterView.self,
                     forAnnotationViewWithReuseIdentifier: MKMapViewDefaultClusterAnnotationViewReuseIdentifier)
        map.addAnnotations(trees.map(TreeAnnotation.init))
        context.coordinator.setRoute(route, real: routeIsReal, on: map)
        // MKUserTrackingButton rather than a button of our own. It is Apple's
        // control, it already knows the three states (off, following, heading)
        // and every iOS user has used it in Maps. The convention rule says take
        // the one people are trained on. Without it there was no way back to
        // yourself at all once you had panned away, which on a map whose whole
        // premise is "near you" is the one control you cannot leave out.
        if showsRecentre {
            let recentre = MKUserTrackingButton(mapView: map)
            recentre.translatesAutoresizingMaskIntoConstraints = false
            recentre.backgroundColor = UIColor.systemBackground.withAlphaComponent(0.92)
            recentre.layer.cornerRadius = 10
            recentre.layer.shadowColor = UIColor.black.cgColor
            recentre.layer.shadowOpacity = 0.15
            recentre.layer.shadowRadius = 5
            recentre.layer.shadowOffset = CGSize(width: 0, height: 2)
            map.addSubview(recentre)
            NSLayoutConstraint.activate([
                recentre.trailingAnchor.constraint(equalTo: map.safeAreaLayoutGuide.trailingAnchor, constant: -12),
                // 208 = the sheet's peek height plus a hair, so the button
                // sits just above the lip of the sheet rather than behind it.
                recentre.bottomAnchor.constraint(equalTo: map.bottomAnchor, constant: -120),
                recentre.widthAnchor.constraint(equalToConstant: 44),
                recentre.heightAnchor.constraint(equalToConstant: 44),
            ])
        }
        if let focus {
            map.setRegion(MKCoordinateRegion(center: focus,
                                             latitudinalMeters: spanMeters,
                                             longitudinalMeters: spanMeters), animated: false)
        }
        return map
    }

    func updateUIView(_ map: MKMapView, context: Context) {
        context.coordinator.parent = self

        if let move = moveTo, context.coordinator.moved != move.token {
            context.coordinator.moved = move.token
            map.setRegion(move.region, animated: true)
        }

        // Paging through the sheet moves the map with you, which is the whole
        // point of staying on the map rather than opening a page.
        if let sel = selected, context.coordinator.centred != sel.id {
            context.coordinator.centred = sel.id
            map.setRegion(MKCoordinateRegion(center: .init(latitude: sel.lat, longitude: sel.lng),
                                             latitudinalMeters: 900, longitudinalMeters: 900),
                          animated: true)
        } else if selected == nil {
            context.coordinator.centred = nil
        }

        let have = Set((map.annotations.compactMap { $0 as? TreeAnnotation }).map(\.tree.id))
        let want = Set(trees.map(\.id))
        guard have != want else { return }
        map.removeAnnotations(map.annotations.filter { $0 is TreeAnnotation })
        map.addAnnotations(trees.map(TreeAnnotation.init))
        context.coordinator.setRoute(route, real: routeIsReal, on: map)
    }

    final class Coordinator: NSObject, MKMapViewDelegate {
        /// var, not let, and reassigned on every updateUIView. A coordinator is
        /// made once and keeps whatever struct it was born with, so a delegate
        /// method reading `parent.selected` was reading the value from launch
        /// forever. That is why the map did not follow the pager and why the
        /// region kept reporting itself while a tree was selected.
        var parent: TreeMap
        private var drawn = 0
        /// Which tree the camera was last moved to, so paging does not fight
        /// itself by re-centring on every redraw.
        var centred: String?
        var moved: UUID?
        init(_ p: TreeMap) { parent = p }

        func setRoute(_ pts: [CLLocationCoordinate2D], real: Bool, on map: MKMapView) {
            guard pts.count != drawn else { return }
            drawn = pts.count
            map.removeOverlays(map.overlays)
            guard pts.count > 1 else { return }
            let line = MKPolyline(coordinates: pts, count: pts.count)
            line.title = real ? "real" : "guessed"
            map.addOverlay(line)
        }

        func mapView(_ map: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
            let r = MKPolylineRenderer(overlay: overlay)
            r.strokeColor = UIColor(red: 0.20, green: 0.35, blue: 0.20, alpha: 0.9)
            r.lineWidth = 5
            r.lineCap = .round
            // A dashed line where we do not have a routed shape, because a solid
            // line between trunks claims a path nobody checked. 78 of 179 walks
            // carry a real route; the rest only carry an order.
            if (overlay.title ?? "") == "guessed" {
                r.lineDashPattern = [2, 10]
                r.lineWidth = 4
                r.strokeColor = UIColor(red: 0.20, green: 0.35, blue: 0.20, alpha: 0.55)
            }
            return r
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
        func mapView(_ map: MKMapView, regionDidChangeAnimated animated: Bool) {
            // While a tree is selected the camera is being driven by the pager,
            // so reporting the region back would rebuild the list under the
            // pager and shuffle what you are swiping through.
            guard parent.selected == nil, let binding = parent.region else { return }
            let c = map.region.center
            if let last = binding.wrappedValue {
                let a = CLLocation(latitude: last.center.latitude, longitude: last.center.longitude)
                let b = CLLocation(latitude: c.latitude, longitude: c.longitude)
                guard a.distance(from: b) > 300
                        || abs(last.span.latitudeDelta - map.region.span.latitudeDelta) > 0.01
                else { return }
            }
            binding.wrappedValue = map.region
        }

        func mapView(_ map: MKMapView, didSelect view: MKAnnotationView) {
            if let a = view.annotation as? TreeAnnotation {
                parent.selected = a.tree
            } else if let c = view.annotation as? MKClusterAnnotation {
                // Tapping a cluster zooms into it rather than opening anything,
                // which is what Google Maps does and what a pile of pins needs.
                let rect = c.memberAnnotations.reduce(MKMapRect.null) { r, a in
                    r.union(MKMapRect(origin: MKMapPoint(a.coordinate), size: .init(width: 1, height: 1)))
                }
                map.setVisibleMapRect(rect, edgePadding: .init(top: 80, left: 60, bottom: 260, right: 60),
                                      animated: true)
                // Without this the cluster stays selected, so tapping the same
                // pile a second time does nothing and it reads as a dead pin.
                map.deselectAnnotation(c, animated: false)
            }
        }
    }
}

/// One tree. The website's pins are illustrated species silhouettes and are
/// better than AllTrails' single brown marker, so the app keeps the idea: the
/// pin says what KIND of tree it is before you tap it.
final class TreePinView: MKMarkerAnnotationView {
    /// Set by whichever map is being built. A static because MKMapView makes
    /// these itself and there is nowhere to hand it an argument.
    static var clusteringEnabled = true

    override var annotation: MKAnnotation? {
        didSet {
            clusteringIdentifier = Self.clusteringEnabled ? "tree" : nil
            // .required, deliberately, and it was briefly changed away from on
            // 2026-08-20 to let MapKit cull colliding labels. Reverted: it made
            // no visible difference in Paris, and what it buys in tidiness it
            // pays for by allowing MapKit to hide a PIN, not just a label. On a
            // map whose entire job is showing where the trees are, a vanished
            // tree is a worse bug than two names that overlap.
            displayPriority = .required
            canShowCallout = false

            // A tree having its moment right now is gold and it breathes
            // (Hidde, 2026-08-20: "als ze in bloei staan, zie je ze een beetje
            // pulseren"). This is where the season verb lives now that it is not
            // a tab: not a badge you have to go and look at, but the map itself
            // telling you which of these is worth today rather than any day.
            //
            // It has to stay SCARCE to mean anything, and the data makes that
            // true on its own: 571 of 1,535 trees carry a best_time at all, and
            // only the ones whose month is this month pulse, so a screen full of
            // pins has a handful breathing on it rather than all of them.
            let now = Calendar.current.component(.month, from: Date())
            let tree = (annotation as? TreeAnnotation)?.tree
            let peak = tree?.peak
            let peaking = peak?.isNow(now) ?? false

            // The glyph is the SPECIES, always, not a generic tree icon. That is
            // what the website's pins have always been and what the app was
            // missing: a ginkgo pin looks like a ginkgo before you tap it. It
            // works for every tree, because every tree carries a species while
            // only a quarter carry a photograph.
            glyphImage = tree.map { SpeciesGlyph.image(for: $0.commonName) }
                ?? UIImage(systemName: "tree.fill")

            // And when the species is having its moment, the pin takes the
            // colour of that moment rather than one shared gold. A ginkgo goes
            // butter yellow in November, a cherry pink in spring, a beech
            // copper in October. The colour comes from the feed, computed once
            // on the server, so this pin and the website's light up the same
            // tree on the same day.
            markerTintColor = peaking
                ? (UIColor(hex: peak?.colour) ?? UIColor(red: 0.85, green: 0.63, blue: 0.25, alpha: 1))
                : UIColor(red: 0.20, green: 0.35, blue: 0.20, alpha: 1)
            setPulsing(peaking, effect: peak?.effect)
        }
    }

    private static let pulseKey = "at.pulse"

    /// A slow breath rather than a blink. Reduce Motion turns it off, because a
    /// map covered in animation is exactly what that setting exists for.
    ///
    /// The strength follows the moment, matching the website's stylesheet. A
    /// crown turning gold in three days is a display; acorns landing is a sound
    /// in the background, so a fruiting pin breathes at less than half the
    /// amplitude and takes half again as long over it (Hidde, 2026-08-20: "de
    /// vrucht animatie kan dan wat subtieler").
    private func setPulsing(_ on: Bool, effect: String?) {
        layer.removeAnimation(forKey: Self.pulseKey)
        guard on, !UIAccessibility.isReduceMotionEnabled else { return }
        let quiet = effect == "fruit-drop" || effect == "catkins"
        let pulse = CABasicAnimation(keyPath: "transform.scale")
        pulse.fromValue = 1.0
        pulse.toValue = quiet ? 1.07 : 1.18
        pulse.duration = quiet ? 1.7 : 1.1
        pulse.autoreverses = true
        pulse.repeatCount = .infinity
        pulse.timingFunction = CAMediaTimingFunction(name: .easeInEaseOut)
        layer.add(pulse, forKey: Self.pulseKey)
    }
}

/// The species silhouettes as pin glyphs. SwiftUI draws them, ImageRenderer
/// turns them into the UIImage MapKit wants, and the result is cached because
/// a map redraws its annotations constantly and there are only fifteen shapes.
/// @MainActor because ImageRenderer is, and because the only caller is a
/// MapKit annotation view's didSet, which MapKit already runs on the main
/// thread. The local Debug build accepted the nonisolated version and the iOS
/// CI job did not: strict concurrency catches what a permissive local build
/// waves through, which is the whole reason that job exists.
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

/// A pile of trees, drawn as a count. This is the thing our website map is
/// missing entirely.
final class ClusterView: MKAnnotationView {
    override var annotation: MKAnnotation? {
        didSet {
            guard let c = annotation as? MKClusterAnnotation else { return }
            displayPriority = .required
            collisionMode = .circle
            image = Self.circle(count: c.memberAnnotations.count)
        }
    }

    private static func circle(count: Int) -> UIImage {
        let d: CGFloat = count < 10 ? 38 : (count < 100 ? 44 : 50)
        return UIGraphicsImageRenderer(size: .init(width: d, height: d)).image { _ in
            UIColor(red: 0.20, green: 0.35, blue: 0.20, alpha: 1).setFill()
            UIBezierPath(ovalIn: .init(x: 0, y: 0, width: d, height: d)).fill()
            UIColor.white.setStroke()
            let ring = UIBezierPath(ovalIn: .init(x: 1.5, y: 1.5, width: d - 3, height: d - 3))
            ring.lineWidth = 3; ring.stroke()
            let s = "\(count)" as NSString
            let f = UIFont.systemFont(ofSize: count < 100 ? 16 : 14, weight: .bold)
            let size = s.size(withAttributes: [.font: f])
            s.draw(at: .init(x: (d - size.width) / 2, y: (d - size.height) / 2),
                   withAttributes: [.font: f, .foregroundColor: UIColor.white])
        }
    }
}
