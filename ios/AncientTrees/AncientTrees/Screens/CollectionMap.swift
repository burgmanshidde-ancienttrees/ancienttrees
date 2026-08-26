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
    /// The size the picture in hand was drawn for, so a rotation or a new
    /// sheet height redraws rather than stretching what is there.
    @State private var rendered: CGSize = .zero

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
        // MEASURED, then rendered at that size. It used to ask the snapshotter
        // for a 190 point strip because that is what the old card was, and the
        // page now shows it full screen: a 190 point image stretched over 800
        // is the blur Hidde saw ("die kaart ziet er helemaal kak en pixelig
        // uit"), and the pins drawn over it landed nowhere near their trees
        // because the frame they were placed in was not the frame on screen.
        GeometryReader { geo in
            ZStack {
                if let image, rendered == geo.size {
                    Image(uiImage: image).resizable().aspectRatio(contentMode: .fill)
                } else {
                    Brand.surfaceMuted
                }
                ForEach(Array(points.enumerated()), id: \.offset) { _, p in
                    Circle()
                        .fill(Brand.moss)
                        .overlay(Circle().strokeBorder(.white, lineWidth: 1.5))
                        .frame(width: 11, height: 11)
                        .position(place(p, in: geo.size))
                }
            }
            .frame(width: geo.size.width, height: geo.size.height)
            .clipped()
            .task(id: "\(geo.size.width)x\(geo.size.height)x\(points.count)") {
                let f = frame
                let shot = await MapThumb.snapshot(lat: f.lat, lng: f.lng,
                                                   size: geo.size, meters: f.meters)
                if shot != nil { rendered = geo.size }
                image = shot
            }
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
