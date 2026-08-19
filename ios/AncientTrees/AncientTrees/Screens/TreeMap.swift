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
    }

    final class Coordinator: NSObject, MKMapViewDelegate {
        let parent: TreeMap
        init(_ p: TreeMap) { parent = p }

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
