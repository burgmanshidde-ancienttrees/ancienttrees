// The tests that do not need a screen.
//
// The first one exists because a UI test failed on 2026-08-20 saying no
// collection shelf rendered, and there are two very different reasons that can
// happen: the feed did not decode, or the swipe did not reach. A test that only
// decodes tells you which, in a second, instead of thirty.

import Testing
import Foundation
@testable import AncientTrees

struct EditorialSuggestions {

    /// The day-zero suggestion picker behind Saved and Collect: photographs
    /// first, nearest first, never a tree the person already has, capped.
    @Test func suggestionsPreferPhotosExcludeOwnedAndStayOrdered() throws {
        let store = CatalogueStore()
        store.loadBundled()
        let cat = try #require(store.catalogue, "the bundled catalogue did not load")
        let origin = (lat: 52.3731, lng: 4.8922)   // Dam square

        let all = Editorial.suggestions(catalogue: cat, origin: origin, excluding: [])
        #expect(all.count == 6)
        #expect(all.allSatisfy { $0.photo != nil },
                "a day-zero suggestion led with a photo-less tree")

        let owned = Set(all.prefix(2).map(\.id))
        let rest = Editorial.suggestions(catalogue: cat, origin: origin, excluding: owned)
        #expect(!rest.contains { owned.contains($0.id) },
                "a suggestion offered a tree the person already has")

        let distances = all.map { Geo.km(origin, ($0.lat, $0.lng)) }
        #expect(distances == distances.sorted(),
                "photo-carrying suggestions are not nearest-first")
    }
}

struct SpotSplit {

    /// The sheet's one decision: what is close enough to be the tree the
    /// person is standing before. At the Wertheimpark gate the wingnut leads;
    /// in a town we do not map, nothing is near and the add-path is the story.
    @Test func nearbyLeadsWithTheNearestAndFarFindsNothing() throws {
        let store = CatalogueStore()
        store.loadBundled()
        let cat = try #require(store.catalogue, "the bundled catalogue did not load")

        let atWertheimpark = (lat: 52.3667, lng: 4.9086)
        let near = CollectSheet.nearby(origin: atWertheimpark, trees: cat.trees)
        #expect(near.first?.id == "ams_004", "the wingnut is not first at its own gate")
        #expect(near.count <= 5)

        let farField = (lat: 52.03, lng: 5.91)
        #expect(CollectSheet.nearby(origin: farField, trees: cat.trees).isEmpty,
                "an empty field claims a nearby tree")
    }
}

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
