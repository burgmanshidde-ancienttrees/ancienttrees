// One species search for every screen that asks for a kind of tree.
//
// Hidde, 2026-10-31: "when adding a tree I often dont know the english name -
// some people might even prefer latin names can we make the specie database
// smarter and easier to search through on every occasion in the app possible".
//
// Three screens had each written their own filter (the map's species filter,
// the chooser for naming your own tree, map search), all answering to our
// English name and the Latin and nothing else. Somebody at a hornbeam who
// thinks "haagbeuk" found no row and typed a name of their own, which splits a
// species the way hard rule 9 exists to prevent.
//
// The names travel as data: `names` on /api/species.json, built by
// scripts/species_names.py from our own translations and Wikidata, and read by
// the website's search from the same file. This file only matches.
//
// Convention: iNaturalist's taxon autocomplete, which answers to the
// scientific name and every common name and returns `matched_term`, the name
// that matched, so the row can say why it answered (CONVENTIONS.md,
// "Searching a species by any of its names").
import Foundation

/// One row of the feed's species dictionary.
public struct SpeciesNameRow: Codable, Hashable, Sendable {
    /// Our common name, the one every screen prints (hard rule 9).
    public let c: String
    /// The Latin.
    public let l: String
    /// Every other name, in any of our languages. Search only.
    public let a: [String]?
    /// false: a species we have met in a lead and do not map yet.
    public let m: Bool?
    /// true: a genus, offered as "Oak (Quercus sp.)".
    public let g: Bool?

    public var isMapped: Bool { m != false && g != true }
    public var isGenus: Bool { g == true }

    /// What a reader's tree is called when they pick this row: the common
    /// name with the Latin, so it groups with the trees that carry it.
    public var species: String {
        isGenus ? "\(c) (\(l) sp.)" : "\(c) (\(l))"
    }
}

/// Why a species answered a query, best first.
public enum SpeciesHit: Equatable, Sendable, Comparable {
    case name
    case latin
    /// Another name of it, which the row shows so the answer makes sense.
    case other(String)
    /// One letter off, which on a phone keyboard is most typing.
    case nearly

    private var rank: Int {
        switch self {
        case .name: 0
        case .latin: 1
        case .other: 2
        case .nearly: 3
        }
    }
    public static func < (a: SpeciesHit, b: SpeciesHit) -> Bool { a.rank < b.rank }

    /// The name to print under the row, when it is not the one on top.
    public var via: String? {
        if case .other(let n) = self { return n }
        return nil
    }
}

public enum SpeciesSearch {
    /// Lower case, accents off, so "chene" finds Chêne and "fachen" Fächer.
    public static func fold(_ s: String) -> String {
        s.folding(options: [.caseInsensitive, .diacriticInsensitive], locale: nil)
            .trimmingCharacters(in: .whitespaces)
    }

    private static func words(_ folded: String) -> [Substring] {
        folded.split(whereSeparator: { $0 == " " || $0 == "-" || $0 == "(" || $0 == "'" })
    }

    /// Does the query start the name, or any word inside it? "oak" finds Holm
    /// Oak, "robur" Quercus robur, "eiche" Stiel-Eiche.
    public static func startsAWord(_ name: String, _ q: String) -> Bool {
        let n = fold(name)
        return n.hasPrefix(q) || words(n).contains { $0.hasPrefix(q) }
    }

    /// The query one letter off the start of a word: a swap, a slip, a
    /// missing or extra letter. Five letters at least, because below that one
    /// letter off matches half the list.
    public static func nearlyStartsAWord(_ name: String, _ q: String) -> Bool {
        guard q.count >= 5 else { return false }
        let qa = Array(q)
        return words(fold(name)).contains { w in
            let wa = Array(w)
            for len in [qa.count - 1, qa.count, qa.count + 1] where len > 0 && len <= wa.count {
                if editDistance(qa, Array(wa[0..<len]), limit: 1) <= 1 { return true }
            }
            return false
        }
    }

    private static func editDistance(_ a: [Character], _ b: [Character], limit: Int) -> Int {
        if abs(a.count - b.count) > limit { return limit + 1 }
        if a.isEmpty || b.isEmpty { return max(a.count, b.count) }
        var prev = Array(0...b.count)
        for i in 1...a.count {
            var cur = [i] + Array(repeating: 0, count: b.count)
            for j in 1...b.count {
                cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] == b[j - 1] ? 0 : 1))
            }
            prev = cur
        }
        return prev[b.count]
    }

    /// How a species answers a folded query, or nil.
    public static func hit(common: String, latin: String?, other: [String], _ q: String) -> SpeciesHit? {
        guard !q.isEmpty else { return .name }
        if startsAWord(common, q) { return .name }
        if let latin, startsAWord(latin, q) { return .latin }
        if let n = other.first(where: { startsAWord($0, q) }) { return .other(n) }
        if nearlyStartsAWord(common, q) { return .nearly }
        if let latin, nearlyStartsAWord(latin, q) { return .nearly }
        if let n = other.first(where: { nearlyStartsAWord($0, q) }) { return .other(n) }
        return nil
    }
}

extension Catalogue {
    /// How one of our species answers what somebody typed, or nil.
    public func speciesHit(_ common: String, query: String) -> SpeciesHit? {
        SpeciesSearch.hit(common: common, latin: scientificName(of: common),
                          other: otherNames(of: common), SpeciesSearch.fold(query))
    }

    /// Our species that answer the query, best match first; ties keep the
    /// order they came in, which is each screen's own (around you, then most).
    public func filterSpecies(_ commons: [String], query: String) -> [(name: String, hit: SpeciesHit)] {
        let q = SpeciesSearch.fold(query)
        let hits = commons.enumerated().compactMap { i, c -> (Int, String, SpeciesHit)? in
            guard let h = SpeciesSearch.hit(common: c, latin: scientificName(of: c),
                                            other: otherNames(of: c), q) else { return nil }
            return (i, c, h)
        }
        return hits.sorted { $0.2 == $1.2 ? $0.0 < $1.0 : $0.2 < $1.2 }.map { ($0.1, $0.2) }
    }

    /// Species and genera we do not map, for somebody naming their own tree.
    /// Only once something is typed: a list of 500 strangers is no help.
    public func unmappedSpecies(matching query: String, limit: Int = 8) -> [(row: SpeciesNameRow, hit: SpeciesHit)] {
        let q = SpeciesSearch.fold(query)
        guard q.count >= 2 else { return [] }
        let hits = speciesDirectory.enumerated().compactMap { i, r -> (Int, SpeciesNameRow, SpeciesHit)? in
            // A genus we already map ("Oak (Quercus sp.)") is a row above.
            guard !r.isMapped, trees(ofSpecies: r.c).isEmpty,
                  let h = SpeciesSearch.hit(common: r.c, latin: r.l, other: r.a ?? [], q) else { return nil }
            return (i, r, h)
        }
        // A genus first when it is what was typed ("eik" is Oak, not one oak).
        return hits.sorted {
            if $0.2 != $1.2 { return $0.2 < $1.2 }
            if $0.1.isGenus != $1.1.isGenus { return $0.1.isGenus }
            return $0.0 < $1.0
        }.prefix(limit).map { ($0.1, $0.2) }
    }
}
