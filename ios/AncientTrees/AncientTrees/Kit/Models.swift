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
    /// Card size and full-width size, already resolved by the feed. Optional
    /// only because a snapshot bundled before 2026-08-25 does not carry them,
    /// and one missing non-optional field rejects the whole catalogue.
    let thumbRaw: String?
    let heroRaw: String?
    /// Does the LICENCE oblige us to name somebody. Answered on the server, by
    /// the same function the website's figcaptions use.
    let creditRequiredRaw: Bool?
    /// The photographer's name as it should be printed, host already dropped.
    /// The trimming used to happen here, which meant the same photograph was
    /// credited one way on the phone and another on the website until Hidde
    /// picked the short one (2026-08-26: "ingekort natuurlijk").
    let attributionShort: String?
    /// The finished credit, name and terms in one string, built by the same
    /// function the website's figcaptions use. It exists because joining those
    /// two here was wrong for a photograph somebody GAVE us: the licence field
    /// then reads "Provided by Paulo V. Araujo (Dias com Arvores), all rights
    /// reserved", so the phone printed his name twice and told a reader the
    /// photograph he had donated was all rights reserved.
    let creditLine: String?

    enum CodingKeys: String, CodingKey {
        case url, license, attribution, width, height
        case thumbRaw = "thumb"
        case heroRaw = "hero"
        case creditRequiredRaw = "credit_required"
        case attributionShort = "attribution_short"
        case creditLine = "credit_line"
    }

    /// The name to print. Falls back to the untrimmed one only for a snapshot
    /// bundled before the feed carried this, where a credit that is too long is
    /// still a correct credit.
    public var name: String? { attributionShort ?? attribution }

    /// The url for a card or a list row.
    public var card: URL? { thumbRaw.flatMap { URL(string: $0) } ?? Photos.thumb(url, width: 500) }
    /// The url for a full-width hero.
    public var full: URL? { heroRaw.flatMap { URL(string: $0) } ?? Photos.thumb(url, width: 960) }

    /// CC BY and BY-SA oblige a visible credit and that is the licence's price,
    /// never something to strip. Anything else may render without one.
    ///
    /// The feed answers this now. The fallback below is the app's old rule and
    /// it was wrong in a way worth remembering: it asked whether the licence
    /// string contains "BY", so "Provided by the Fundacao Mata do Bucaco, all
    /// rights reserved" printed a credit the website did not, on four live
    /// photographs. A substring is not a licence.
    public var creditRequired: Bool {
        if let creditRequiredRaw { return creditRequiredRaw }
        guard let license else { return true }
        return license.uppercased().contains("BY")
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
    /// Getting to this tree needs a ticket. Written by scripts/paid_entry.py
    /// from the access prose and only where that prose is unambiguous.
    let paidEntryRaw: Bool?
    public var paidEntry: Bool { paidEntryRaw ?? false }
    let transportRaw: String?
    public var transport: String { transportRaw ?? "" }

    /// Whether there is anything to put in the access block at all. A tree
    /// with neither line gets no block rather than an empty one holding its
    /// own spacing (Hidde, 2026-08-29: "als er geen ov info beschikbaar is dan
    /// ook geen icon tonen").
    public var hasAccessInfo: Bool {
        !access.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
            || !transport.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
    }
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
        case paidEntryRaw = "paid_entry"
        case citySlug = "city_slug"
        case bestTime = "best_time"
    }

    /// The common name only, without the Latin in parentheses. Map pins and
    /// cards have no room for the binomial.
    public var commonName: String { Tree.commonName(of: species) }

    /// The same trim, reachable without a tree, because a tree somebody added
    /// themselves has a species they typed and no Tree to ask (see
    /// MapFilters.keeps(_ sighting:)). One implementation, so the species
    /// filter cannot come to two answers about the same words.
    public static func commonName(of species: String) -> String {
        guard let i = species.firstIndex(of: "(") else { return species }
        return String(species[..<i]).trimmingCharacters(in: .whitespaces)
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

/// A named city, park, country or species with the trees in it. Decoded loosely
/// on purpose: /api/browse.json carries five facets and the app uses what it can.
public struct BrowseFacet: Codable, Hashable, Sendable, Identifiable {
    public let slug: String?
    public let name: String
    public let trees: [String]?
    public let count: Int?
    /// The website's own hand-written introduction to this facet. It has been in
    /// the feed since 2026-08-19 and nothing here decoded it.
    public let intro: String?
    /// The id of the tree whose photograph fronts this facet, decided once on
    /// the server (site/src/lib/images.ts) so the app shows the same picture the
    /// website shows and a hand-set pin reaches both.
    public let face: String?

    public var id: String { slug ?? name }
}

public struct BrowseFeed: Codable, Sendable {
    public let version: String
    public let collections: [TreeCollection]
    /// All optional: a snapshot bundled before 2026-08-25 carries neither the
    /// cities array nor any face, and one missing field must not cost the app
    /// its collections.
    public let cities: [BrowseFacet]?
    public let countries: [BrowseFacet]?
    public let species: [BrowseFacet]?
    public let parks: [BrowseFacet]?
}

/// The browse facets as the app holds them: keyed for lookup, answering only
/// what the feed actually said. Nothing is decided here on purpose. A facet's
/// face and its intro are the website's judgement, and the whole point of
/// carrying them is that the two surfaces cannot disagree.
public struct BrowseFacets: Sendable {
    public static let empty = BrowseFacets(cities: [], countries: [], species: [], parks: [])

    public let cities: [BrowseFacet]
    public let countries: [BrowseFacet]
    public let species: [BrowseFacet]
    public let parks: [BrowseFacet]

    private let cityBySlug: [String: BrowseFacet]
    private let countryByName: [String: BrowseFacet]
    private let speciesByName: [String: BrowseFacet]

    public init(cities: [BrowseFacet], countries: [BrowseFacet],
                species: [BrowseFacet], parks: [BrowseFacet]) {
        self.cities = cities
        self.countries = countries
        self.species = species
        self.parks = parks
        self.cityBySlug = Dictionary(cities.compactMap { f in f.slug.map { ($0, f) } },
                                     uniquingKeysWith: { a, _ in a })
        self.countryByName = Dictionary(countries.map { ($0.name, $0) },
                                        uniquingKeysWith: { a, _ in a })
        self.speciesByName = Dictionary(species.map { ($0.name, $0) },
                                        uniquingKeysWith: { a, _ in a })
    }

    public init(feed: BrowseFeed?) {
        self.init(cities: feed?.cities ?? [], countries: feed?.countries ?? [],
                  species: feed?.species ?? [], parks: feed?.parks ?? [])
    }

    public func face(city slug: String) -> String? { cityBySlug[slug]?.face }
    public func face(country name: String) -> String? { countryByName[name]?.face }
    public func face(species commonName: String) -> String? { speciesByName[commonName]?.face }
    public func intro(species commonName: String) -> String? { speciesByName[commonName]?.intro }
    public func intro(country name: String) -> String? { countryByName[name]?.intro }
}

/// `/api/version.json`, the cheap call that says whether anything changed.
public struct VersionInfo: Codable, Sendable {
    public let version: String
    public let trees: Int
    public let cities: Int
}
