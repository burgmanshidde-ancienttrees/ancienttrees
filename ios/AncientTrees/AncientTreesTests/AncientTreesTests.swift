// The tests that do not need a screen.
//
// The first one exists because a UI test failed on 2026-08-20 saying no
// collection shelf rendered, and there are two very different reasons that can
// happen: the feed did not decode, or the swipe did not reach. A test that only
// decodes tells you which, in a second, instead of thirty.

import Testing
import Foundation
@testable import AncientTrees

struct CatalogueDecoding {

    @Test func theBundledBrowseFeedCarriesTheCollections() throws {
        let url = try #require(Bundle.main.url(forResource: "browse", withExtension: "json"),
                               "browse.json is not in the app bundle")
        let feed = try JSONDecoder().decode(BrowseFeed.self, from: Data(contentsOf: url))
        #expect(feed.collections.count >= 10)
        #expect(feed.collections.allSatisfy { !$0.trees.isEmpty })
    }

    /// The collections point at tree ids, and a shelf only draws when at least
    /// three of them resolve. If the bundled trees and the bundled browse feed
    /// were built from different days this is where it shows.
    @Test func collectionsResolveAgainstTheBundledTrees() throws {
        let store = CatalogueStore()
        store.loadBundled()
        let cat = try #require(store.catalogue, "the bundled catalogue did not load")
        #expect(cat.collections.count >= 10)
        for c in cat.collections {
            #expect(cat.trees(of: c).count >= 3,
                    "collection \(c.slug) resolved only \(cat.trees(of: c).count) trees")
        }
    }
}
