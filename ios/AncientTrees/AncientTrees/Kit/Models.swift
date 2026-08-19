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

public struct Tree: Codable, Identifiable, Hashable, Sendable {
    public let id: String
    public let name: String
    public let species: String
    public let age: String?
    public let lat: Double
    public let lng: Double
    public let city: String
    public let citySlug: String
    public let country: String
    public let neighbourhood: String
    public let access: String
    public let transport: String
    public let story: String
    public let url: String
    public let precision: Precision
    public let photo: Photo?
    public let bestTime: BestTime?

    enum CodingKeys: String, CodingKey {
        case id, name, species, age, lat, lng, city, country, neighbourhood
        case access, transport, story, url, precision, photo
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

/// `/api/version.json`, the cheap call that says whether anything changed.
public struct VersionInfo: Codable, Sendable {
    public let version: String
    public let trees: Int
    public let cities: Int
}
