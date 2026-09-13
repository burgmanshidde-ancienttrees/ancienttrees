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
// and cannot draw a sphere; MapKit renders the Earth as one, with no texture to
// license and no library to add, since it is a system framework. That is the
// only reason for the second engine, and it is confined to this one view.
//
// IT HAS TO BE A FLYOVER CONFIGURATION, and that is the bug Hidde photographed
// on 2026-09-13: "de weergave van my trees gaat helemaal slecht, volgens mij
// moet dit een wereldbol zijn omdat ik in meerdere landen heb". He was right on
// both halves. The globe branch WAS firing (two countries, signed in, and the
// Dutch continent label proves the picture is Apple's map rather than ours,
// since our own style has no continent layer and asks for name:latin). It was
// simply never a globe.
//
// "far enough out" was the wrong model. MapKit only renders the Earth as a
// SPHERE in the flyover configurations; with a standard configuration it
// refuses to zoom out past a certain point and stays flat however large a
// camera altitude you hand it, which is why 26,000 km produced a clamped flat
// map over central Asia. Apple's own developer forums say exactly this:
// MKMapRectWorld gives a spherical view under SatelliteFlyover and
// HybridFlyover, and "will zoom out the map only to a certain extent" under
// Standard, Satellite, Hybrid and Muted Standard.
// https://developer.apple.com/forums/thread/104352
//
// So this is MKImageryMapConfiguration with realistic elevation, which is the
// modern spelling of satellite flyover. It is also the closer match to the
// reference: Polarsteps' globe is a photographed Earth, not a road map.
//
// NOTHING HAD EVER LOOKED AT THIS SCREEN, which is the real reason it shipped
// like that. It needs a signed-in account whose collection spans two countries,
// which no simulator can produce, so it was in no screen list, had no launch
// argument, and appeared in no UI test. -globe forces the branch for exactly
// the reason -collect-place and -collect-identify exist.
//
// It stops turning when it is off screen. A 3D map animating behind a page
// nobody is looking at is a battery bill for nothing.

import SwiftUI
import MapKit

struct GlobeMap: UIViewRepresentable {
    let points: [(lat: Double, lng: Double)]
    /// Kilometres from the surface. Far enough that MapKit draws the planet
    /// rather than a country, which it will only do at all under the flyover
    /// configuration set below.
    private let altitude: CLLocationDistance = 26_000_000

    /// WHERE THE GLOBE STARTS TURNING FROM: the MEDIAN of your trees, never
    /// the mean.
    ///
    /// The mean is what shipped, and it is wrong in exactly the case this view
    /// exists for. A collection only reaches the globe when it spans countries,
    /// so it is usually two clusters far apart, and the mean of two clusters is
    /// the empty space between them: the Netherlands plus Japan averages to
    /// Kazakhstan, which is what Hidde's screenshot opened on, an ocean of land
    /// with not one of his trees on it. The median lands inside whichever
    /// cluster holds most of them, which is a place he has actually been.
    ///
    /// Latitude is held inside 35 degrees so the planet stays centred in the
    /// frame rather than showing a pole. Longitude is taken as a plain median,
    /// which is wrong for a collection straddling the antimeridian and is not
    /// worth solving: it turns a full circle every few minutes anyway, so the
    /// cost is one imperfect opening frame.
    static func opening(for points: [(lat: Double, lng: Double)]) -> (lat: Double, lng: Double) {
        guard !points.isEmpty else { return (20, 0) }
        func median(_ xs: [Double]) -> Double {
            let s = xs.sorted()
            return s.count % 2 == 1 ? s[s.count / 2]
                                    : (s[s.count / 2 - 1] + s[s.count / 2]) / 2
        }
        return (min(max(median(points.map(\.lat)), -35), 35), median(points.map(\.lng)))
    }

    /// Two dots on opposite sides of the planet, for -globe alone. A forced
    /// globe with an empty collection is a bare Earth, which photographs the
    /// projection and nothing else; the whole question this screen raises is
    /// what a collection spanning two countries looks like on it.
    static let somewhereToLookAt: [(lat: Double, lng: Double)] = [
        (52.37, 4.90),    // Amsterdam
        (34.68, 135.83),  // Nara
    ]

    func makeUIView(context: Context) -> MKMapView {
        let map = MKMapView()
        map.isUserInteractionEnabled = false      // a cover, not a control
        map.showsCompass = false
        map.showsScale = false
        map.pointOfInterestFilter = .excludingAll
        // Imagery, not standard. See the note at the top: a standard
        // configuration cannot be a sphere at any altitude. Imagery carries no
        // points of interest to filter, so there is nothing to set on it.
        map.preferredConfiguration = MKImageryMapConfiguration(elevationStyle: .realistic)
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

        /// Starts over your trees, so the first thing on screen is your own
        /// collection rather than the Pacific.
        func start(from points: [(lat: Double, lng: Double)]) {
            if !points.isEmpty {
                let opening = GlobeMap.opening(for: points)
                latitude = opening.lat
                longitude = opening.lng
            }
            place()
            // A twentieth of a degree thirty times a second is a full turn in
            // four minutes: a drift you notice only if you watch it, which is
            // what the reference does. (This said six minutes and the
            // arithmetic says four.)
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
