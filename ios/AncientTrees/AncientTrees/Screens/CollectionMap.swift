// The map of what YOU have, on My trees.
//
// Polarsteps opens the page about you with a globe carrying your own
// photographs, and Hidde asked for that shape (2026-08-26: "de my trees pagina
// opbouwen als de my pagina van polarsteps"). The picture answers "where have I
// been" before any number does, and it is the only thing on that screen that is
// yours rather than ours.
//
// It renders through the same snapshotter every card corner already uses, so it
// costs one image and no live map, and it frames every point rather than
// centring on one: a collection is a spread, and a collection map that shows
// the first tree at street level is a map of one tree.

import SwiftUI
import CoreLocation

struct CollectionMap: View {
    let points: [(lat: Double, lng: Double)]

    @State private var image: UIImage?

    /// The middle of everything you have, and how far apart the furthest two
    /// are, which together decide the frame.
    private var frame: (lat: Double, lng: Double, meters: CLLocationDistance) {
        guard !points.isEmpty else { return (52.37, 4.89, 4000) }
        let lats = points.map(\.lat), lngs = points.map(\.lng)
        let midLat = (lats.min()! + lats.max()!) / 2
        let midLng = (lngs.min()! + lngs.max()!) / 2
        // Degrees to metres, latitude only: it is the axis that does not lie
        // with distance from the equator, and a square-ish frame is enough for
        // a picture nobody navigates by.
        let spanM = max((lats.max()! - lats.min()!) * 111_000,
                        (lngs.max()! - lngs.min()!) * 111_000
                            * cos(midLat * .pi / 180))
        // A floor, so one tree is a street rather than an infinite zoom, and
        // a fifth of headroom so nothing sits on the edge.
        return (midLat, midLng, max(spanM * 1.2, 900))
    }

    var body: some View {
        // AN EMPTY BOX WITH THE PICTURE LAID OVER IT, never a bare .fill
        // image. A resizable image set to fill reports the size it wants
        // rather than the size it is given, so it drags whatever holds it
        // sideways: here it made the sheet lying over this map about three
        // screens wide, and My trees arrived on Hidde's phone with its stats
        // row off both edges ("de mytrees pagina is helemaal stuk").
        //
        // TreeDetail's hero already carries this same note from the same
        // trap. An overlay takes no part in layout at all, which is the only
        // version that cannot do it again.
        Color.clear
            .overlay {
                if let image {
                    Image(uiImage: image).resizable().aspectRatio(contentMode: .fill)
                } else {
                    Brand.surfaceMuted
                }
            }
            .clipped()
        .overlay {
            // The pins, drawn over the snapshot rather than into it, because
            // the snapshotter draws our own style and not our own trees.
            GeometryReader { geo in
                ForEach(Array(points.enumerated()), id: \.offset) { _, p in
                    Circle()
                        .fill(Brand.moss)
                        .overlay(Circle().strokeBorder(.white, lineWidth: 1.5))
                        .frame(width: 10, height: 10)
                        .position(place(p, in: geo.size))
                }
            }
        }
        .task(id: points.count) {
            let w = UIScreen.main.bounds.width - 40
            let f = frame
            image = await MapThumb.snapshot(lat: f.lat, lng: f.lng,
                                            size: CGSize(width: w, height: 190),
                                            meters: f.meters)
        }
    }

    /// Where a point lands on the snapshot. The same flat approximation the
    /// frame uses, which holds at the scale of a city and is honest at the
    /// scale of a country: this is a picture, not a route.
    private func place(_ p: (lat: Double, lng: Double), in size: CGSize) -> CGPoint {
        let f = frame
        let halfM = f.meters / 2
        let dyM = (p.lat - f.lat) * 111_000
        let dxM = (p.lng - f.lng) * 111_000 * cos(f.lat * .pi / 180)
        let x = size.width / 2 + CGFloat(dxM / halfM) * size.width / 2
        let y = size.height / 2 - CGFloat(dyM / halfM) * size.height / 2
        return CGPoint(x: min(max(x, 6), size.width - 6),
                       y: min(max(y, 6), size.height - 6))
    }
}
