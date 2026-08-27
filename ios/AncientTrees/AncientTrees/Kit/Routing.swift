// A pedestrian route over the streets, fetched once for the screen that needs it.
//
// The website has had real routes since 2026-08-08: scripts/route_walks.py asks
// FOSSGIS's public Valhalla for each city walk, caches the shape in the repo, and
// the build draws it. That is still the right arrangement for a walk, because a
// walk's stops never move, so the answer can be computed once for everybody and
// no visitor's browser ever calls a routing service.
//
// What it cannot cover is the case Hidde asked about on 2026-08-25: "take me
// there zou gewoon een route moeten tonen van waar ik nu ben naar die boom". A
// route that starts where the person is standing cannot be precomputed, because
// the start is different every time. So this is the small live half of the same
// thing, and it is deliberately narrow:
//
//   ONE call, when a walk screen opens without a cached shape. Never per tap,
//   never while walking, never on the map tab. That is the scope Hidde approved
//   on 2026-08-24 ("ik vind die afhankelijkheid van die partij geen probleem
//   voor een betere ervaring"), one call per walk, and it is also what is fair
//   to a community instance that costs nobody anything.
//
//   FAILING IS FINE. No route, no error, no retry: the caller keeps the dashed
//   straight line it was already drawing and the honest note that goes with it.
//   A walk must work on a train with no signal.
//
//   AND IT IS SANITY CHECKED, with the same two rules the script uses. A routed
//   line more than 2.5x the crow flies usually means a path is missing from
//   OpenStreetMap inside a park, and one shorter than 0.4x means the router
//   snapped every stop to the same node, which is how Oahu came back as eight
//   copies of one coordinate. Both are worse than the honest schematic.

import CoreLocation
import Foundation

enum Routing {
    private static let url = URL(string: "https://valhalla1.openstreetmap.de/route")!
    private static let agent = "AncientTrees/1.0 (https://ancienttrees.app; iOS)"
    private static let maxDetour = 2.5
    private static let minPlausible = 0.4

    /// The stops, in order, including where the person is standing.
    /// Returns nil rather than throwing: every failure here is the same failure.
    static func pedestrian(through stops: [CLLocationCoordinate2D]) async -> [CLLocationCoordinate2D]? {
        guard stops.count >= 2 else { return nil }
        let body: [String: Any] = [
            "locations": stops.map { ["lat": $0.latitude, "lon": $0.longitude] },
            "costing": "pedestrian",
            "directions_options": ["units": "kilometers"],
        ]
        var r = URLRequest(url: url)
        r.httpMethod = "POST"
        r.timeoutInterval = 8
        r.setValue("application/json", forHTTPHeaderField: "Content-Type")
        r.setValue(agent, forHTTPHeaderField: "User-Agent")
        r.httpBody = try? JSONSerialization.data(withJSONObject: body)

        guard let (data, resp) = try? await Net.data(for: r),
              let http = resp as? HTTPURLResponse, (200..<300).contains(http.statusCode),
              let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let trip = json["trip"] as? [String: Any],
              let legs = trip["legs"] as? [[String: Any]]
        else { return nil }

        var shape: [CLLocationCoordinate2D] = []
        for leg in legs {
            guard let s = leg["shape"] as? String else { return nil }
            shape.append(contentsOf: decode(s))
        }
        guard shape.count > 1 else { return nil }

        // The two sanity checks, against the straight line through the stops.
        let straight = zip(stops, stops.dropFirst()).reduce(0.0) {
            $0 + Geo.km(($1.0.latitude, $1.0.longitude), ($1.1.latitude, $1.1.longitude))
        }
        let routed = zip(shape, shape.dropFirst()).reduce(0.0) {
            $0 + Geo.km(($1.0.latitude, $1.0.longitude), ($1.1.latitude, $1.1.longitude))
        }
        if straight > 0.01 {
            let ratio = routed / straight
            if ratio > maxDetour || ratio < minPlausible { return nil }
        }
        return shape
    }

    /// Valhalla's encoded polyline, precision 6.
    private static func decode(_ s: String) -> [CLLocationCoordinate2D] {
        var out: [CLLocationCoordinate2D] = []
        var lat = 0, lng = 0
        var chars = Array(s.utf8).map { Int($0) - 63 }
        var i = 0
        while i < chars.count {
            var deltas = [0, 0]
            for which in 0..<2 {
                var shift = 0, result = 0
                while i < chars.count {
                    let b = chars[i]
                    i += 1
                    result |= (b & 0x1F) << shift
                    shift += 5
                    if b < 0x20 { break }
                }
                deltas[which] = (result & 1) != 0 ? ~(result >> 1) : (result >> 1)
            }
            lat += deltas[0]
            lng += deltas[1]
            out.append(.init(latitude: Double(lat) / 1e6, longitude: Double(lng) / 1e6))
        }
        chars = []
        return out
    }
}
