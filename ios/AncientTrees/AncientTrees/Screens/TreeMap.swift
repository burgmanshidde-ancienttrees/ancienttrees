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
    @Binding var selected: Tree?

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    func makeUIView(context: Context) -> MKMapView {
        let map = MKMapView()
        map.delegate = context.coordinator
        map.showsUserLocation = true
        map.pointOfInterestFilter = .excludingAll   // our pins are the point
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
                recentre.topAnchor.constraint(equalTo: map.safeAreaLayoutGuide.topAnchor, constant: 56),
                recentre.widthAnchor.constraint(equalToConstant: 44),
                recentre.heightAnchor.constraint(equalToConstant: 44),
            ])
        }
        if let focus {
            map.setRegion(MKCoordinateRegion(center: focus,
                                             latitudinalMeters: 4000,
                                             longitudinalMeters: 4000), animated: false)
        }
        return map
    }

    func updateUIView(_ map: MKMapView, context: Context) {
        let have = Set((map.annotations.compactMap { $0 as? TreeAnnotation }).map(\.tree.id))
        let want = Set(trees.map(\.id))
        guard have != want else { return }
        map.removeAnnotations(map.annotations.filter { $0 is TreeAnnotation })
        map.addAnnotations(trees.map(TreeAnnotation.init))
        context.coordinator.setRoute(route, real: routeIsReal, on: map)
    }

    final class Coordinator: NSObject, MKMapViewDelegate {
        let parent: TreeMap
        private var drawn = 0
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
            }
        }
    }
}

/// One tree. The website's pins are illustrated species silhouettes and are
/// better than AllTrails' single brown marker, so the app keeps the idea: the
/// pin says what KIND of tree it is before you tap it.
final class TreePinView: MKMarkerAnnotationView {
    override var annotation: MKAnnotation? {
        didSet {
            clusteringIdentifier = "tree"
            displayPriority = .required
            markerTintColor = UIColor(red: 0.20, green: 0.35, blue: 0.20, alpha: 1)
            glyphImage = UIImage(systemName: "tree.fill")
            canShowCallout = false
        }
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
