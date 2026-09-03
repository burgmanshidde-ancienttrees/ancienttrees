// The little map in the corner of the photograph.
//
// Straight out of the AllTrails frames Hidde recorded, and the teardown already
// called it "the cheapest good idea in the whole app": every route card carries
// a small rounded map in the bottom corner of its picture with the route drawn
// on it, so you can see what shape a walk is without opening anything.
//
// A tree is a point rather than a course, so what the inset shows is not a shape
// but a SETTING, and that turns out to be the more useful of the two here. It
// answers the question a photograph of a trunk cannot: is this thing in the
// middle of a park, on a canal, or on a street corner between two buildings.
// That is most of what decides whether you feel like walking there today.
//
// A snapshot rather than a live map view, because a card is a thumbnail and
// putting a real map in a scrolling list is how you make a list stutter.
// Snapshots are cached in memory by coordinate, so scrolling back up costs
// nothing, and they need the network: with no signal there is simply no inset,
// which is the same honest degradation as a photograph that will not load.
//
// MLNMapSnapshotter, not MKMapSnapshotter, since 2026-08-24. This was the last
// piece of Apple's map left in the app, and it showed: a tree page carried our
// own map at the top and an Apple one in the corner of the same photograph. It
// also mattered beyond looks, because Apple's snapshots always need the network
// and their terms forbid caching the tiles, so an offline tree page could never
// have had one.

import SwiftUI
import CoreLocation
import MapLibre

/// One at a time, and never more than two.
///
/// A snapshot is not a thumbnail generator, it is a map render, and Home puts
/// dozens of cards on screen at once across its shelves. Firing one per card
/// froze the app on the home screen: Hidde could not scroll at all. A gate is
/// the fix rather than a smaller image, because the cost is per render and not
/// per pixel.
actor SnapshotGate {
    static let shared = SnapshotGate()
    private var running = 0
    private var waiting: [CheckedContinuation<Void, Never>] = []

    func enter() async {
        if running < 2 { running += 1; return }
        await withCheckedContinuation { waiting.append($0) }
        running += 1
    }

    func leave() {
        running -= 1
        if !waiting.isEmpty { waiting.removeFirst().resume() }
    }
}

@MainActor
enum MapThumb {
    private static let cache = NSCache<NSString, UIImage>()
    /// The snapshotter has to outlive the call that starts it. Left to a local,
    /// it is released the moment the function returns and the callback never
    /// fires, which looks exactly like a map that will not load.
    private static var inFlight: [MLNMapSnapshotter] = []

    static func cached(_ key: String) -> UIImage? { cache.object(forKey: key as NSString) }

    /// How much of the rendered image is the snapshotter's own attribution bar.
    private static let attributionStrip: CGFloat = 24

    /// `size` is in POINTS. The snapshotter renders at screen scale itself,
    /// which is why nothing here doubles anything: the MapKit version used to,
    /// because its size meant something different.
    static func snapshot(lat: Double, lng: Double, size: CGSize,
                         meters: CLLocationDistance = 500) async -> UIImage? {
        // THE APPEARANCE IS PART OF THE KEY. Without it the first thumbnail
        // rendered wins for the rest of the launch, so a phone that goes dark at
        // sunset keeps a cream stamp in the corner of every dark tree page, and
        // one that starts dark keeps a dark one all morning.
        let dark = UITraitCollection.current.userInterfaceStyle == .dark
        let key = "\(lat),\(lng),\(Int(size.width)),\(Int(size.height)),\(dark ? "d" : "l")"
        if let hit = cached(key) { return hit }

        let centre = CLLocationCoordinate2D(latitude: lat, longitude: lng)
        let camera = MLNMapCamera(lookingAtCenter: centre, altitude: 0, pitch: 0, heading: 0)
        // Rendered TALLER than it is shown, and the extra strip is cropped off
        // below. The snapshotter burns its attribution into the bottom of the
        // image, which on a 72 point thumbnail is an unreadable clipped word
        // sitting across the map. Attribution for these tiles lives on the map
        // screen itself, where there is room to read it.
        let full = CGSize(width: size.width, height: size.height + attributionStrip)
        let options = MLNMapSnapshotOptions(
            styleURL: MapStyle.url(for: dark ? .dark : .light), camera: camera, size: full)
        // The same conversion the live map uses, told how wide THIS view is: a
        // thumbnail borrowing the full-screen width opens five times too close.
        options.zoomLevel = TreeMap.zoom(forMeters: meters, latitude: lat,
                                         width: Double(size.width))

        await SnapshotGate.shared.enter()
        defer { Task { await SnapshotGate.shared.leave() } }

        let shot: UIImage? = await withCheckedContinuation { cont in
            let snapshotter = MLNMapSnapshotter(options: options)
            inFlight.append(snapshotter)
            snapshotter.start { snap, _ in
                inFlight.removeAll { $0 === snapshotter }
                cont.resume(returning: snap?.image)
            }
        }
        guard let shot else { return nil }

        // The dot is drawn on rather than left to the snapshotter, which has no
        // annotations. Centre of the image is the tree by construction.
        let out = UIGraphicsImageRenderer(size: size).image { ctx in
            // Drawn full height into a shorter box, so the attribution strip
            // falls off the bottom rather than being squashed into view.
            shot.draw(in: CGRect(x: 0, y: 0, width: size.width,
                                 height: size.height + attributionStrip))
            let c = CGPoint(x: size.width / 2, y: size.height / 2)
            let r: CGFloat = 5
            // The ring is white on the daylight map and the map's own ground in
            // the dark, for the same reason the live map's pins wear a white
            // ring: the ring exists to separate the dot from the map under it,
            // and a white ring on a near-black map is a bright speck rather
            // than a separator.
            // 0x0D0F0C is the dark map's own ground, from
            // scripts/map_style_dark.py. It is the one colour here that belongs
            // to the map rather than to the palette.
            ctx.cgContext.setFillColor(dark ? UIColor(hex: 0x0D0F0C).cgColor
                                            : UIColor.white.cgColor)
            ctx.cgContext.fillEllipse(in: CGRect(x: c.x - r - 2, y: c.y - r - 2,
                                                 width: (r + 2) * 2, height: (r + 2) * 2))
            ctx.cgContext.setFillColor(UIColor(dark ? Brand.moss : Brand.canopy).cgColor)
            ctx.cgContext.fillEllipse(in: CGRect(x: c.x - r, y: c.y - r, width: r * 2, height: r * 2))
        }
        cache.setObject(out, forKey: key as NSString)
        return out
    }
}

struct MapInset: View {
    let lat: Double
    let lng: Double
    /// A square thumbnail in a card's corner, or nil for the wide strip the
    /// tree page uses as its way to the map.
    var side: CGFloat? = 72
    var height: CGFloat = 72

    @State private var image: UIImage?

    var body: some View {
        Group {
            if let image {
                Image(uiImage: image).resizable()
            } else {
                // Nothing rather than a grey box: an empty corner reads as no
                // inset, a grey square reads as a broken one.
                Color.clear
            }
        }
        .frame(width: side, height: side ?? height)
        .frame(maxWidth: side == nil ? .infinity : nil)
        .clipShape(.rect(cornerRadius: side == nil ? 0 : 10))
        .overlay {
            if image != nil, side != nil {
                RoundedRectangle(cornerRadius: 10).strokeBorder(.white.opacity(0.9), lineWidth: 2)
            }
        }
        .shadow(color: .black.opacity(side == nil ? 0 : 0.18), radius: 4, y: 2)
        .task {
            // A card that scrolls past in half a second should never have cost
            // a map render. Anything still on screen after this is worth one.
            try? await Task.sleep(for: .milliseconds(400))
            if Task.isCancelled { return }
            let w = side ?? UIScreen.main.bounds.width - 40
            image = await MapThumb.snapshot(lat: lat, lng: lng,
                                            size: CGSize(width: w, height: side ?? height),
                                            meters: side == nil ? 700 : 500)
        }
        .accessibilityHidden(true)      // the card already says where the tree is
    }
}
