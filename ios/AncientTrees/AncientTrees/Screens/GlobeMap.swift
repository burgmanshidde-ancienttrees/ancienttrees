// The globe, for a collection that has left one country.
//
// Hidde asked for the Polarsteps globe (2026-08-26) and then agreed the
// threshold before it was built: "opzich was de oplossing dat je dat pas hebt
// bij meer dan een land een goeie". That threshold is the whole design. Their
// globe sings because the person looking at it has been to fifty countries;
// two trees in one city on a whole planet is a dot on an empty sphere, which
// looks sadder than a map of your own street. So the page shows the globe the
// day your collection stops being local, and the flat cover until then. It
// rewards the thing we actually want, which is going somewhere.
//
// MAPKIT RATHER THAN OUR OWN MAP. MapLibre draws every other map in this app
// and cannot draw a sphere; MapKit renders the Earth as one once the camera is
// far enough out, with no texture to license and no library to add, since it
// is a system framework. That is the only reason for the second engine, and it
// is confined to this one view.
//
// It stops turning when it is off screen. A 3D map animating behind a page
// nobody is looking at is a battery bill for nothing.

import SwiftUI
import MapKit

struct GlobeMap: UIViewRepresentable {
    let points: [(lat: Double, lng: Double)]
    /// Kilometres from the surface. Far enough that MapKit draws the planet
    /// rather than a country.
    private let altitude: CLLocationDistance = 26_000_000

    func makeUIView(context: Context) -> MKMapView {
        let map = MKMapView()
        map.isUserInteractionEnabled = false      // a cover, not a control
        map.showsCompass = false
        map.showsScale = false
        map.pointOfInterestFilter = .excludingAll
        let config = MKStandardMapConfiguration(elevationStyle: .realistic)
        config.pointOfInterestFilter = .excludingAll
        map.preferredConfiguration = config
        map.addAnnotations(points.map { p in
            let a = MKPointAnnotation()
            a.coordinate = CLLocationCoordinate2D(latitude: p.lat, longitude: p.lng)
            return a
        })
        map.delegate = context.coordinator
        context.coordinator.map = map
        context.coordinator.start(from: points)
        return map
    }

    func updateUIView(_ map: MKMapView, context: Context) {}

    static func dismantleUIView(_ map: MKMapView, coordinator: Coordinator) {
        coordinator.stop()
    }

    func makeCoordinator() -> Coordinator { Coordinator(altitude: altitude) }

    final class Coordinator: NSObject, MKMapViewDelegate {
        weak var map: MKMapView?
        private var timer: Timer?
        private var longitude: Double = 0
        private var latitude: Double = 20
        private let altitude: CLLocationDistance

        init(altitude: CLLocationDistance) { self.altitude = altitude }

        /// Starts over the middle of what you have, so the first thing on
        /// screen is your own trees rather than the Pacific.
        func start(from points: [(lat: Double, lng: Double)]) {
            if !points.isEmpty {
                longitude = points.map(\.lng).reduce(0, +) / Double(points.count)
                latitude = min(max(points.map(\.lat).reduce(0, +) / Double(points.count), -35), 35)
            }
            place()
            // A degree every tick is a full turn in six minutes: a drift you
            // notice only if you watch it, which is what the reference does.
            timer = Timer.scheduledTimer(withTimeInterval: 1.0 / 30.0, repeats: true) { [weak self] _ in
                guard let self else { return }
                longitude += 0.05
                if longitude > 180 { longitude -= 360 }
                place()
            }
        }

        func stop() { timer?.invalidate(); timer = nil }

        private func place() {
            guard let map else { return }
            let camera = MKMapCamera(
                lookingAtCenter: CLLocationCoordinate2D(latitude: latitude, longitude: longitude),
                fromDistance: altitude, pitch: 0, heading: 0)
            map.setCamera(camera, animated: false)
        }

        func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
            let id = "tree"
            let view = mapView.dequeueReusableAnnotationView(withIdentifier: id)
                ?? MKAnnotationView(annotation: annotation, reuseIdentifier: id)
            view.annotation = annotation
            view.image = Coordinator.dot
            view.canShowCallout = false
            return view
        }

        /// One drawn dot, reused for every tree: a marker per annotation would
        /// be a hundred layers on a view nobody taps.
        static let dot: UIImage = {
            let side: CGFloat = 12
            return UIGraphicsImageRenderer(size: CGSize(width: side, height: side)).image { ctx in
                let r = CGRect(x: 1, y: 1, width: side - 2, height: side - 2)
                UIColor.white.setStroke()
                UIColor(red: 0.20, green: 0.35, blue: 0.20, alpha: 1).setFill()
                let path = UIBezierPath(ovalIn: r)
                path.lineWidth = 2
                path.fill()
                path.stroke()
            }
        }()
    }
}
