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
// MKMapSnapshotter rather than a live map view, because a card is a thumbnail
// and putting a real MKMapView in a scrolling list is how you make a list stutter.
// Snapshots are cached in memory by coordinate, so scrolling back up costs
// nothing, and they need the network: with no signal there is simply no inset,
// which is the same honest degradation as a photograph that will not load.

import SwiftUI
import MapKit

/// One at a time, and never more than two.
///
/// MKMapSnapshotter is not a thumbnail generator, it is a map render, and Home
/// puts dozens of cards on screen at once across its shelves. Firing one per
/// card froze the app on the home screen: Hidde could not scroll at all. A
/// gate is the fix rather than a smaller image, because the cost is per render
/// and not per pixel.
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

    static func cached(_ key: String) -> UIImage? { cache.object(forKey: key as NSString) }

    static func snapshot(lat: Double, lng: Double, size: CGSize,
                         dark: Bool, meters: CLLocationDistance = 500) async -> UIImage? {
        let key = "\(lat),\(lng),\(Int(size.width)),\(Int(size.height)),\(dark)"
        if let hit = cached(key) { return hit }

        let options = MKMapSnapshotter.Options()
        options.region = MKCoordinateRegion(center: .init(latitude: lat, longitude: lng),
                                            latitudinalMeters: meters, longitudinalMeters: meters)
        options.size = size
        options.pointOfInterestFilter = .excludingAll
        options.traitCollection = UITraitCollection(userInterfaceStyle: dark ? .dark : .light)

        await SnapshotGate.shared.enter()
        defer { Task { await SnapshotGate.shared.leave() } }
        guard let shot = try? await MKMapSnapshotter(options: options).start() else { return nil }

        // The dot is drawn on rather than left to the snapshotter, which has no
        // annotations. Centre of the image is the tree by construction.
        let out = UIGraphicsImageRenderer(size: size).image { ctx in
            shot.image.draw(at: .zero)
            let c = CGPoint(x: size.width / 2, y: size.height / 2)
            let r: CGFloat = 5
            ctx.cgContext.setFillColor(UIColor.white.cgColor)
            ctx.cgContext.fillEllipse(in: CGRect(x: c.x - r - 2, y: c.y - r - 2,
                                                 width: (r + 2) * 2, height: (r + 2) * 2))
            ctx.cgContext.setFillColor(UIColor(red: 0.20, green: 0.35, blue: 0.20, alpha: 1).cgColor)
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

    @Environment(\.colorScheme) private var scheme
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
        .task(id: scheme) {
            // A card that scrolls past in half a second should never have cost
            // a map render. Anything still on screen after this is worth one.
            try? await Task.sleep(for: .milliseconds(400))
            if Task.isCancelled { return }
            let w = side ?? UIScreen.main.bounds.width - 40
            image = await MapThumb.snapshot(lat: lat, lng: lng,
                                            size: CGSize(width: w * 2, height: (side ?? height) * 2),
                                            dark: scheme == .dark,
                                            meters: side == nil ? 700 : 500)
        }
        .accessibilityHidden(true)      // the card already says where the tree is
    }
}
