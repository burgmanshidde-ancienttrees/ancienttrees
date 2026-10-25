// A place we have no trees for becomes an ask to add one (Hidde, 2026-10-25).
//
// Convention: Google Maps and Apple Maps answer a search for any real town,
// whatever their own data holds there, and AllTrails' empty area offers the
// nearest thing it has rather than a dead end. So search finds the town
// through Apple's own MKLocalSearch (MapKit, no third party, filtered to
// localities with MKAddressFilter), and where we hold nothing the answer is
// the grey card below, the ask to add the first tree, and the nearest tree we
// do hold. The website builds the same card from the same copy.
//
// Spacing is copied, not set by feel: the card is the map's arrival card
// (surfaceMuted, radius 14, padding 16, 16 in from the edges), the faint
// icon is the Want-to-visit ghost tile's (22 medium, inkSoft at 0.6), the
// button is the sheet button's 48 point capsule, and the row is MapSearch's
// row (14 between icon and words, a 24 point icon column, 56 tall).

import SwiftUI
import MapKit

/// A real town Apple knows, which may hold none of our trees.
struct RealPlace: Identifiable, Equatable {
    let name: String
    let country: String
    let lat: Double
    let lng: Double
    var id: String { "\(name)|\(country)|\(Int(lat * 100))|\(Int(lng * 100))" }
}

/// The map asked to look at a town from somewhere that is not the map
/// (Discover's search). Equatable so MapTab can watch it.
struct PlaceOnMap: Equatable {
    let name: String
    let lat: Double
    let lng: Double
}

enum EmptyPlace {
    /// Zoom 11 or so: a town and the country lanes around it.
    static let spanMetres: Double = 20_000

    /// Towns matching the query, Apple's answer, localities only. Empty on
    /// any failure (offline, throttled), which the caller reads as "nothing
    /// matches", the honest thing to say when nothing came back.
    static func lookup(_ query: String) async -> [RealPlace] {
        let req = MKLocalSearch.Request()
        req.naturalLanguageQuery = query
        req.resultTypes = .address
        req.addressFilter = MKAddressFilter(including: [.locality])
        guard let resp = try? await MKLocalSearch(request: req).start() else { return [] }
        var seen = Set<String>()
        var out: [RealPlace] = []
        for item in resp.mapItems {
            let pm = item.placemark
            guard let name = pm.locality ?? item.name else { continue }
            let country = pm.country ?? ""
            let key = "\(name)|\(country)"
            guard !seen.contains(key) else { continue }
            seen.insert(key)
            out.append(RealPlace(name: name, country: country,
                                 lat: pm.coordinate.latitude, lng: pm.coordinate.longitude))
        }
        return Array(out.prefix(5))
    }

    /// The nearest tree in our catalogue to a point, and how far.
    static func nearest(in catalogue: Catalogue, lat: Double, lng: Double) -> (tree: Tree, km: Double)? {
        var best: (tree: Tree, km: Double)?
        for t in catalogue.trees {
            let d = t.distanceKm(from: lat, lng)
            if best == nil || d < best!.km { best = (t, d) }
        }
        return best
    }

    /// "27 km", "3.4 km", "17 mi": whole numbers once the decimal stops
    /// meaning anything, in the reader's own unit.
    static func distance(_ km: Double, _ unit: DistanceUnit) -> String {
        let v = unit == .metric ? km : km * 0.621371
        let u = unit == .metric ? "km" : "mi"
        return v < 10 ? String(format: "%.1f %@", v, u) : "\(Int(v.rounded())) \(u)"
    }
}

/// The grey card: no trees here yet, and the ask.
struct EmptyPlaceCard: View {
    /// nil says "here"; a name says where.
    let place: String?
    @Environment(Navigator.self) private var navigator

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            VStack(alignment: .leading, spacing: 8) {
                Image(systemName: "tree")
                    .font(.system(size: 22, weight: .medium))
                    .foregroundStyle(Brand.inkSoft.opacity(0.6))
                    .accessibilityHidden(true)
                Text(place.map { "No trees mapped in \($0) yet" } ?? "No trees mapped here yet")
                    .font(.system(size: 16, weight: .semibold))
                    .foregroundStyle(Brand.ink)
                    .fixedSize(horizontal: false, vertical: true)
                Text("Know an old tree here? Add the first one.")
                    .font(.system(size: 14))
                    .foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
            }
            Button {
                // The same deed every other "Add a tree" asks for (Discover's
                // growing card): the root opens the camera flow.
                navigator.collectNearby = true
            } label: {
                Label("Add a tree", systemImage: "camera.fill")
                    .font(.system(size: 16, weight: .semibold))
                    .foregroundStyle(Brand.ink)
                    .frame(maxWidth: .infinity).frame(height: 48)
                    .background(Brand.surface, in: .capsule)
                    .contentShape(.capsule)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("empty-place-add")
        }
        .padding(16)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Brand.surfaceMuted, in: .rect(cornerRadius: 14))
        .accessibilityElement(children: .contain)
        .accessibilityIdentifier("empty-place-card")
    }
}

/// One row, MapSearch's shape: icon, name, a line under it.
struct EmptyPlaceRow: View {
    let name: String
    let sub: String
    let icon: String
    var inset: CGFloat = 16

    var body: some View {
        HStack(spacing: 14) {
            Image(systemName: icon)
                .font(.system(size: 17))
                .foregroundStyle(Brand.moss)
                .frame(width: 24)
            VStack(alignment: .leading, spacing: 2) {
                Text(name)
                    .font(.brand(16, .bold)).foregroundStyle(Brand.ink)
                    .lineLimit(1)
                Text(sub).font(.caption).foregroundStyle(Brand.inkSoft).lineLimit(1)
            }
            Spacer(minLength: 8)
        }
        .padding(.horizontal, inset).frame(minHeight: 56)
        .contentShape(.rect)
    }
}
