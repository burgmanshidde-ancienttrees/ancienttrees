// The shapes the app reads, decoded straight from what ancienttrees.app already
// serves. Nothing here is invented: every field and every nullability below was
// measured against the live feed on 2026-08-19 (1377 trees, 175 walks).
//
// The one rule this file encodes rather than documents: an unknown or missing
// `precision` decodes to .approximate, never to .confirmed. A wrong pin is the
// single error a reader cannot forgive, because they are already standing in the
// wrong place before any correction reaches them, so the failure has to fall on
// the side of admitting we are unsure.

import Foundation

public enum Precision: String, Codable, Sendable {
    case confirmed
    case approximate

    public init(from decoder: Decoder) throws {
        let raw = try decoder.singleValueContainer().decode(String.self)
        self = Precision(rawValue: raw) ?? .approximate
    }

    /// What the map should say next to the directions button.
    public var needsWarning: Bool { self == .approximate }
}

public struct Photo: Codable, Hashable, Sendable {
    public let url: String
    public let license: String?
    public let attribution: String?
    public let width: Int?
    public let height: Int?

    /// CC BY and BY-SA oblige a visible credit and that is the licence's price,
    /// never something to strip. Anything else may render without one.
    public var creditRequired: Bool {
        guard let license else { return true }
        let l = license.uppercased()
        return l.contains("BY")
    }
}

public struct BestTime: Codable, Hashable, Sendable {
    public let months: [Int]
    public let label: String
    public let kind: String?

    public func isNow(_ month: Int) -> Bool { months.contains(month) }
}

/// The species' one moment of the year worth a trip, and what this pin should
/// do about it. Computed on the server from data/phenology and already shifted
/// for the tree's latitude, so the app never has to know that a Melbourne
/// ginkgo turns in May. The same field drives the website's map, which is the
/// point: one calculation, two surfaces, the same tree lighting up on the same
/// day (Hidde, 2026-08-21).
public struct Peak: Codable, Hashable, Sendable {
    public let months: [Int]
    public let effect: String
    public let colour: String

    /// Is this tree having its moment in the given month?
    public func isNow(_ month: Int) -> Bool { months.contains(month) }
}

public struct Tree: Codable, Identifiable, Hashable, Sendable {
    public let id: String
    public let name: String
    public let species: String
    public let age: String?
    /// Numeric bounds, where a city file has them. 1,159 of 1,406 trees do.
    public let ageMin: Int?
    public let ageMax: Int?
    public let lat: Double
    public let lng: Double
    public let city: String
    public let citySlug: String
    public let country: String
    // NULLABLE IN THE FEED, and non-optional here is how the whole catalogue
    // stopped decoding on 2026-08-24: "Expected value of type String but found
    // null instead. Path: trees[93].neighbourhood". 45 trees carry a null
    // neighbourhood and 59 a null transport, and one bad field rejects the
    // entire file, so the app fell back to the copy bundled with it. That copy
    // was five days old, which is the only reason nobody had seen this: the
    // staleness was hiding the breakage.
    //
    // Stored optional, read non-optional, so no call site changes and Codable
    // stays synthesised. Every string a city file may leave empty belongs in
    // this shape.
    let neighbourhoodRaw: String?
    public var neighbourhood: String { neighbourhoodRaw ?? "" }
    public let access: String
    let transportRaw: String?
    public var transport: String { transportRaw ?? "" }
    public let story: String
    public let url: String
    public let precision: Precision
    public let photo: Photo?
    public let bestTime: BestTime?
    public let peak: Peak?

    enum CodingKeys: String, CodingKey {
        case id, name, species, age, lat, lng, city, country
        case neighbourhoodRaw = "neighbourhood"
        case transportRaw = "transport"
        case ageMin = "age_min"
        case ageMax = "age_max"
        case access, story, url, precision, photo, peak
        case citySlug = "city_slug"
        case bestTime = "best_time"
    }

    /// The common name only, without the Latin in parentheses. Map pins and
    /// cards have no room for the binomial.
    public var commonName: String {
        guard let i = species.firstIndex(of: "(") else { return species }
        return species[..<i].trimmingCharacters(in: .whitespaces)
    }
}

public struct Walk: Codable, Hashable, Sendable {
    public let city: String
    public let citySlug: String
    public let name: String
    public let trees: [String]
    public let count: Int
    public let km: Double        // the feed sends this as int or double; Double takes both
    public let minutes: Int
    public let duration: String
    public let combined: Bool
    /// GeoJSON order, [lng, lat], present on 78 of 179 walks where
    /// scripts/route_walks.py cached a real routed line.
    public let shape: [[Double]]?

    enum CodingKeys: String, CodingKey {
        case city, name, trees, count, km, minutes, duration, combined, shape
        case citySlug = "city_slug"
    }
}

public struct Species: Codable, Hashable, Sendable {
    public let commonName: String
    public let habit: String?
    public let leaf: [Int]
    public let flowers: [Int]
    public let fruit: [Int]
    public let colour: [Int]
    public let bare: [Int]

    enum CodingKeys: String, CodingKey {
        case habit, leaf, flowers, fruit, colour, bare
        case commonName = "common_name"
    }
}

// The feed envelopes.
public struct TreeFeed: Codable, Sendable {
    public let version: String
    public let count: Int
    public let trees: [Tree]
}

/// Identity for the places SwiftUI needs one: presenting Begin as a
/// fullScreenCover, mostly. City slug plus name, which is what makes a walk
/// unique in the feed as well.
extension Walk: Identifiable {
    public var id: String { citySlug + "|" + name }
}

public struct WalkFeed: Codable, Sendable {
    public let version: String
    public let count: Int
    public let walks: [Walk]
}

public struct SpeciesFeed: Codable, Sendable {
    public let version: String
    public let count: Int
    public let species: [Species]
}

/// One hand-curated collection: the website's own, not derived here. Thirteen of
/// them exist and they are the most inspiring thing this project owns, which is
/// why Explore is built out of them rather than out of a list of cities.
public struct TreeCollection: Codable, Hashable, Sendable, Identifiable {
    public let slug: String
    public let title: String
    public let intro: String?
    public let trees: [String]

    public var id: String { slug }
}

/// A named park, country or species with the trees in it. Decoded loosely on
/// purpose: /api/browse.json carries four facets and the app uses what it can.
public struct BrowseFacet: Codable, Hashable, Sendable, Identifiable {
    public let slug: String?
    public let name: String
    public let trees: [String]?
    public let count: Int?

    public var id: String { slug ?? name }
}

public struct BrowseFeed: Codable, Sendable {
    public let version: String
    public let collections: [TreeCollection]
}

/// `/api/version.json`, the cheap call that says whether anything changed.
public struct VersionInfo: Codable, Sendable {
    public let version: String
    public let trees: Int
    public let cities: Int
}
