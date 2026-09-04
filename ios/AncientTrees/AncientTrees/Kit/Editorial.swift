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

    /// Never LEAD with a tree nobody has photographed. The list keeps its own
    /// order (on a map, nearest-first is what a reader expects); only the first
    /// card is promoted, and only to the nearest one that carries a picture
    /// from the head of the list. Hidde's finding, 2026-08-20: "de sheet op de
    /// kaart pakte gewoon de dichtstbijzijnde boom, die toevallig fotoloos is."
    public static func leadWithAPhotograph<T>(_ list: [T],
                                              photo: (T) -> Bool,
                                              lookahead: Int = 12) -> [T] {
        guard let first = list.first, !photo(first) else { return list }
        guard let i = list.prefix(lookahead).firstIndex(where: photo) else { return list }
        var out = list
        let winner = out.remove(at: i)
        out.insert(winner, at: 0)
        return out
    }

    /// PHOTOGRAPHS FIRST, in any list of a place's trees (Hidde, 2026-09-04,
    /// looking at Italy's 327: "kun je bij dit soort land of stad of whatever
    /// overzichten bomen met foto's bovenaan zetten").
    ///
    /// `leadWithAPhotograph` above only promotes ONE, so the first card is a
    /// picture and the second is a green placeholder, which is exactly what he
    /// was looking at. That one is right where only the opening card is being
    /// staged; this one is right where the list is a browse and 82 percent of
    /// the trees have no photograph yet.
    ///
    /// A stable partition rather than a sort, deliberately: whatever order the
    /// caller already had inside each group is kept, so a list sorted by
    /// distance stays sorted by distance and this adds one rule rather than
    /// replacing the caller's.
    ///
    /// Likes join this as the second key when there are any to sort by (his
    /// "en in de toekomst met likes"). Deliberately not yet: a list ordered by
    /// a number that is zero on every row is the same list with a slower sort.
    public static func photographsFirst<T>(_ list: [T], photo: (T) -> Bool) -> [T] {
        list.filter(photo) + list.filter { !photo($0) }
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
