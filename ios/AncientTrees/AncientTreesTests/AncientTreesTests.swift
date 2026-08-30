// The tests that do not need a screen.
//
// The first one exists because a UI test failed on 2026-08-20 saying no
// collection shelf rendered, and there are two very different reasons that can
// happen: the feed did not decode, or the swipe did not reach. A test that only
// decodes tells you which, in a second, instead of thirty.

import Testing
import Foundation
@testable import AncientTrees

// The stores are main-actor isolated (see Account.swift), so a suite that
// builds one asks on the main actor.
@MainActor
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

// The stores are main-actor isolated (see Account.swift), so a suite that
// builds one asks on the main actor.
@MainActor
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

// The stores are main-actor isolated (see Account.swift), so a suite that
// builds one asks on the main actor.
@MainActor
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

// MARK: - the indexes say the same thing the scan said

/// AN INDEX IS ONLY WORTH HAVING IF IT ANSWERS IDENTICALLY.
///
/// Home, MapSearch, IndexPages, Collect, Country, Species and PlaceMapPage each
/// worked out "the trees of this city" for themselves, by filtering or grouping
/// the whole list inside a computed property that re-runs on every body pass.
/// Catalogue groups them once at load instead. The refactor is only safe if
/// every one of those call sites gets exactly what it used to get, so this asks
/// the old question and the new one of the real bundled catalogue and compares
/// them, for every city, every country and every species we ship.
// The stores are main-actor isolated (see Account.swift), so a suite that
// builds one asks on the main actor.
@MainActor
struct TheIndexesMatchTheScan {

    private func bundled() throws -> Catalogue {
        let store = CatalogueStore()
        store.loadBundled()
        return try #require(store.catalogue, "the bundled catalogue did not load")
    }

    @Test func everyCityHoldsWhatFilteringWouldHaveFound() throws {
        let cat = try bundled()
        let cities = Set(cat.trees.map(\.citySlug))
        #expect(cities.count > 100, "the bundled catalogue looks wrong, not the index")
        for slug in cities {
            #expect(cat.trees(inCity: slug).map(\.id)
                    == cat.trees.filter { $0.citySlug == slug }.map(\.id),
                    "the index and the scan disagree about \(slug)")
        }
        #expect(cat.trees(inCity: "nowhere-at-all").isEmpty,
                "an unknown city returned something")
    }

    @Test func everyCountryAndSpeciesDoTheSame() throws {
        let cat = try bundled()
        for name in Set(cat.trees.map(\.country)) {
            #expect(cat.trees(inCountry: name).map(\.id)
                    == cat.trees.filter { $0.country == name }.map(\.id),
                    "the index and the scan disagree about \(name)")
        }
        for name in Set(cat.trees.map(\.commonName)) {
            #expect(cat.trees(ofSpecies: name).map(\.id)
                    == cat.trees.filter { $0.commonName == name }.map(\.id),
                    "the index and the scan disagree about \(name)")
        }
    }

    /// The search field built this per keystroke. It must still be every common
    /// name, once each, in the same order, and it must not offer an empty row
    /// for a tree whose species nobody has established yet.
    @Test func theSpeciesListIsTheSameListSortedTheSameWay() throws {
        let cat = try bundled()
        let scanned = Array(Set(cat.trees.map(\.commonName))).sorted().filter { !$0.isEmpty }
        #expect(cat.speciesNames == scanned)
        #expect(!cat.speciesNames.contains(""))
    }

    /// citySlugs used to build a Set and sort it. Same answer, or the index
    /// pages come out in a different order than they always have.
    @Test func theCitySlugsAreUnchanged() throws {
        let cat = try bundled()
        #expect(cat.citySlugs == Array(Set(cat.trees.map(\.citySlug))).sorted())
    }
}

// MARK: - one builder, and the URLs it must still produce

/// SEVEN FILES BUILT THEIR OWN REQUEST. NOW ONE DOES.
///
/// Waitlist, Submissions, VoteCounts, Profiles, Moderation, Diagnostics and
/// ProfileEditor each assembled a URLRequest by hand, four of them by walking
/// back up from the submissions table with deletingLastPathComponent and
/// counting the steps in a comment. Two of them got it wrong in a way that
/// failed silently for weeks.
///
/// This locks the addresses down, because the failure mode of getting one
/// wrong is not a crash: PostgREST answers 404 or 400, the app swallows it, and
/// a feature simply never works while looking as though it does. Each expected
/// string below is what the OLD hand-built code produced.
@Test func everyEndpointStillPointsWhereItPointed() {
    func url(_ r: URLRequest) -> String { r.url?.absoluteString ?? "" }
    let root = "https://caimvxiyrtifilimlkqw.supabase.co"

    #expect(url(Supa.request(Waitlist.path)) == root + "/rest/v1/waitlist")
    #expect(url(Supa.request(Submission.path)) == root + "/rest/v1/submissions")
    #expect(url(Supa.request("/rest/v1/rpc/tree_vote_counts"))
            == root + "/rest/v1/rpc/tree_vote_counts")
    #expect(url(Supa.request("/rest/v1/diagnostics")) == root + "/rest/v1/diagnostics")

    // The query survives. This is the one that had actually shipped broken:
    // appendingPathComponent turns the "?" into %3F and the whole query becomes
    // part of the table name.
    #expect(url(Supa.request("/rest/v1/profiles?on_conflict=user_id"))
            == root + "/rest/v1/profiles?on_conflict=user_id")
    #expect(url(Supa.request("/rest/v1/blocks?select=blocked&blocker=eq.abc"))
            == root + "/rest/v1/blocks?select=blocked&blocker=eq.abc")

    // Storage sits beside /rest, not under it. Three deletingLastPathComponent
    // calls used to get here, with the count load-bearing.
    #expect(url(Supa.request("/storage/v1/object/avatars/abc/avatar.jpg"))
            == root + "/storage/v1/object/avatars/abc/avatar.jpg")
}

/// Every call now carries a timeout, which is the point of having one builder
/// and was the practical cost of not having one: five of the seven set none at
/// all, so they ran on the system default of sixty seconds. A minute of
/// somebody under a tree watching nothing happen, in an app for being outside.
@Test func everyRequestGivesUpBeforeAMinute() {
    #expect(Supa.request("/rest/v1/submissions").timeoutInterval == 20)
    #expect(Supa.request("/rest/v1/diagnostics").timeoutInterval < 30)
}

/// A body that is already encoded must not be encoded again. Profiles and
/// Moderation hand over Data from JSONEncoder; everything else hands over a
/// dictionary. Getting this wrong would post the base64 of a JSON document.
@Test func anAlreadyEncodedBodyPassesThrough() {
    let raw = Data(#"{"display_name":"Hidde"}"#.utf8)
    #expect(Supa.request("/rest/v1/profiles", body: raw).httpBody == raw)
    let dict = Supa.request("/rest/v1/submissions", body: ["kind": "feedback"]).httpBody
    #expect(dict.flatMap { String(data: $0, encoding: .utf8) } == #"{"kind":"feedback"}"#)
}

// MARK: - the query that vanished

/// A REQUEST URL KEEPS ITS QUERY.
///
/// appendingPathComponent percent-encodes a "?" into %3F, which turns
/// "profiles?on_conflict=user_id" into a table name with a question mark in it.
/// PostgREST refuses that, quietly, so saving a name or a picture had never
/// once worked, follower counts were always zero, and a report or a block only
/// ever happened on the phone. Nothing anywhere said so.
///
/// The cheapest possible guard against it coming back: the fault is entirely in
/// how a string becomes a URL, so catching it needs no network and no simulator.
@Test func aRequestURLKeepsItsQuery() {
    let base = URL(string: "https://x.supabase.co/rest/v1/")!

    // The trap, asserted so nobody has to rediscover it.
    #expect(base.appendingPathComponent("profiles?on_conflict=user_id")
        .absoluteString.contains("%3F"))

    // And the way this app builds them, which survives.
    let built = URL(string: base.absoluteString + "profiles?on_conflict=user_id")!
    #expect(built.query == "on_conflict=user_id")
    #expect(built.path == "/rest/v1/profiles")
}
