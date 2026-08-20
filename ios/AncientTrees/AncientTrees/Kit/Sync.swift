// Keeping the catalogue current without downloading 2.5 MB to find out nothing
// changed. /api/version.json is a few dozen bytes and carries the same hash the
// tree feed carries, so the check costs one small request.

import Foundation

public enum Feed {
    public static let base = URL(string: "https://ancienttrees.app")!
    public static var version: URL { base.appending(path: "/api/version.json") }
    public static var trees: URL { base.appending(path: "/api/trees.json") }
    public static var walks: URL { base.appending(path: "/api/walks.json") }
    public static var species: URL { base.appending(path: "/api/species.json") }
    /// The facets the website already had and the app ignored for a day:
    /// collections, parks, countries, species counts.
    public static var browse: URL { base.appending(path: "/api/browse.json") }
}

public struct Sync: Sendable {
    public enum Outcome: Sendable, Equatable {
        case upToDate(version: String)
        case updated(from: String?, to: String)
        case offline          // no signal: whatever is on disk stays valid
    }

    /// Ask the cheap endpoint whether the local copy is stale.
    ///
    /// Returns .offline rather than throwing, because the whole point of holding
    /// the catalogue on disk is that the app works with no signal. A failed sync
    /// is a non-event, not an error to show anybody.
    public static func check(localVersion: String?,
                             fetch: (URL) async throws -> Data) async -> Outcome {
        do {
            let data = try await fetch(Feed.version)
            let info = try JSONDecoder().decode(VersionInfo.self, from: data)
            if info.version == localVersion { return .upToDate(version: info.version) }
            return .updated(from: localVersion, to: info.version)
        } catch {
            return .offline
        }
    }
}
