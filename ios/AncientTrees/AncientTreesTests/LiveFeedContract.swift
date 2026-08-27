// The website can break every installed app, and nothing noticed.
//
// The app reads five feeds off ancienttrees.app and the website deploys several
// times a day. Until 2026-08-27 nothing anywhere checked that what the website
// publishes still fits what the app can read. The only test that came close
// decoded the copy BUNDLED in the app, which is by definition the version that
// already worked.
//
// WHY THE SILENCE IS THE WORST PART. The app fails safe, which sounds good and
// hides this completely. A broken trees or walks feed makes refresh() return
// early and the app keeps whatever it had; a broken species or browse feed is
// swallowed by a `try?` and the app quietly loses its phenology or its
// collections. Nobody crashes, so nobody reports anything, and every phone in
// the world stops updating at the same moment while we see nothing at all.
//
// This test uses the app's OWN decoder and its own models, which is the only
// honest way to ask the question: a second description of the feed shape kept
// in another language would drift from the real one, and then we would be
// testing the copy instead of the app.
//
// It decodes all four STRICTLY, including the two the app forgives, because a
// feature disappearing without a word is exactly what we want to hear about.

import Testing
import Foundation
@testable import AncientTrees

@Suite(.serialized)
struct TheLiveFeedsStillFitTheApp {

    /// A plain session: this must ask the real website, and it must not be
    /// reachable by the fault injector, which exists to take the network away.
    private static func fetch(_ url: URL) async throws -> Data {
        var request = URLRequest(url: url)
        request.timeoutInterval = 30
        request.cachePolicy = .reloadIgnoringLocalCacheData
        let (data, response) = try await URLSession(configuration: .ephemeral)
            .data(for: request)
        guard let http = response as? HTTPURLResponse else {
            throw Failure.unreachable(url, "no HTTP response")
        }
        guard (200..<300).contains(http.statusCode) else {
            throw Failure.unreachable(url, "HTTP \(http.statusCode)")
        }
        return data
    }

    enum Failure: Error, CustomStringConvertible {
        case unreachable(URL, String)

        var description: String {
            switch self {
            case .unreachable(let url, let why):
                // Said this plainly so a red log answers the first question a
                // human asks: is the website down, or did the shape change?
                return "COULD NOT REACH \(url.path) (\(why)). This is a reachability "
                     + "problem, not a decoding one: either the site is down or this "
                     + "runner cannot leave the building."
            }
        }
    }

    @Test func theTreeFeedDecodes() async throws {
        let data = try await Self.fetch(Feed.trees)
        let feed = try JSONDecoder().decode(TreeFeed.self, from: data)
        #expect(feed.trees.count > 500,
                "the live tree feed carries \(feed.trees.count) trees, which is not a feed")
        #expect(!feed.version.isEmpty, "the feed has no version, so no phone can tell it changed")

        // A tree with no position is a tree no phone can draw, and it would go
        // unnoticed until somebody opened the map.
        let placeless = feed.trees.filter { $0.lat == 0 && $0.lng == 0 }
        #expect(placeless.isEmpty,
                "\(placeless.count) live trees have no position: \(placeless.prefix(3).map(\.id))")
    }

    @Test func theWalkFeedDecodes() async throws {
        let data = try await Self.fetch(Feed.walks)
        let feed = try JSONDecoder().decode(WalkFeed.self, from: data)
        #expect(!feed.walks.isEmpty, "the live walk feed is empty")
    }

    /// STRICTLY, even though the app forgives this one. A `try?` in
    /// CatalogueStore means a broken species feed costs every season chart in
    /// the app without a word being said anywhere.
    @Test func theSpeciesFeedDecodes() async throws {
        let data = try await Self.fetch(Feed.species)
        let feed = try JSONDecoder().decode(SpeciesFeed.self, from: data)
        #expect(!feed.species.isEmpty, "the live species feed is empty, so no tree has a season")
    }

    /// Same again: the app swallows a broken browse feed and simply shows no
    /// collections, which looks like a design decision rather than a fault.
    @Test func theBrowseFeedDecodes() async throws {
        let data = try await Self.fetch(Feed.browse)
        let feed = try JSONDecoder().decode(BrowseFeed.self, from: data)
        #expect(feed.collections.count >= 5,
                "the live browse feed carries \(feed.collections.count) collections")
    }

    /// The cheap endpoint every launch asks first. If this one changes shape,
    /// no phone ever learns that anything else changed either.
    @Test func theVersionFeedDecodes() async throws {
        let data = try await Self.fetch(Feed.version)
        let json = try JSONSerialization.jsonObject(with: data) as? [String: Any]
        let version = json?["version"] as? String
        #expect(version?.isEmpty == false,
                "version.json has no version string, so nothing will ever refresh")
    }
}
