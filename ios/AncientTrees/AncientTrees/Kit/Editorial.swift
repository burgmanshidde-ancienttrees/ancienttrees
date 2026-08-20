// The editorial hand: open with the best we have, never with the first row
// the database returns.
//
// The app's version of what city pages do on the website. A shelf, a sheet or
// a suggestion list that happens to lead with a photo-less winter tree reads
// as poverty even when the data behind it is rich, so anything that picks
// "which trees do we show first" goes through here rather than sorting by raw
// distance at its own call site.

import Foundation

public enum Editorial {

    /// Best-first: a photograph beats no photograph, nearness breaks the tie.
    public static func rank(_ trees: [Tree],
                            origin: (lat: Double, lng: Double)) -> [Tree] {
        trees.sorted { a, b in
            let ap = a.photo != nil, bp = b.photo != nil
            if ap != bp { return ap }
            return Geo.km(origin, (a.lat, a.lng)) < Geo.km(origin, (b.lat, b.lng))
        }
    }

    /// What Saved and Collect open with before anyone has saved or ticked a
    /// thing: the nearest trees worth wanting, photographs first, never one
    /// the person already has.
    public static func suggestions(catalogue: Catalogue,
                                   origin: (lat: Double, lng: Double),
                                   excluding: Set<String>,
                                   limit: Int = 6) -> [Tree] {
        let candidates = catalogue.trees.filter {
            !excluding.contains($0.id)
                && Geo.km(origin, ($0.lat, $0.lng)) <= 100
        }
        return Array(rank(candidates, origin: origin).prefix(limit))
    }
}
