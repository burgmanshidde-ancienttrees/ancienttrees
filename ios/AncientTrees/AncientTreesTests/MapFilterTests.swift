// The map's filters, asked about a tree only you have.
//
// Hidde, 2026-08-27: "de boom die ik zelf heb toegevoegd blijft altijd op de map
// staan welke filter ik ook aanzet, terwijl het geen ginkgo is of niet mijn
// favoriet." He was right and the cause was structural rather than a slip:
// MapFilters answered for the catalogue, the mine layer was passed to the map
// and to the sheet straight from the store, and nothing in between ever asked a
// filter anything. So the fix ships with the tests that make it unshippable
// again, per the ratchet in CLAUDE.md.

import Testing
import Foundation
@testable import AncientTrees

struct YourOwnTreesObeyTheFilters {

    /// A sighting with whatever the test cares about and nothing else.
    private func mine(species: String? = nil, photo: String? = "shot.jpg",
                      lat: Double = 52.3731, lng: Double = 4.8922) -> Sightings.Sighting {
        Sightings.Sighting(treeId: nil, name: "The oak on my street",
                           species: species, lat: lat, lng: lng, photo: photo)
    }

    @Test func noFilterKeepsIt() {
        #expect(MapFilters().keeps(mine()))
    }

    @Test func aSpeciesFilterHidesATreeOfAnotherSpecies() {
        var f = MapFilters(); f.species = "Ginkgo"
        #expect(!f.keeps(mine(species: "Pedunculate Oak")))
        #expect(f.keeps(mine(species: "Ginkgo")))
    }

    /// The Latin you may have typed after it is not part of the comparison,
    /// the same way it is not for ours.
    @Test func aSpeciesFilterIgnoresTheLatinYouTyped() {
        var f = MapFilters(); f.species = "Ginkgo"
        #expect(f.keeps(mine(species: "Ginkgo (Ginkgo biloba)")))
    }

    /// A species nobody filled in cannot answer "is it a ginkgo", and an
    /// unanswerable question is a no. Keeping it would be the filter lying.
    @Test func aSpeciesFilterHidesATreeWithNoSpeciesYet() {
        var f = MapFilters(); f.species = "Ginkgo"
        #expect(!f.keeps(mine(species: nil)))
    }

    @Test func favouritesOnlyHidesOneYouHaveNotHearted() {
        var f = MapFilters(); f.favouritesOnly = true
        let s = mine()
        #expect(!f.keeps(s, favourites: []))
        #expect(f.keeps(s, favourites: [s.treeKey]),
                "the heart on your tree's page saves under treeKey, so the filter must ask with it")
    }

    /// Nothing records that YOUR tree peaks this month, and ours with no
    /// best_time are hidden by this filter too.
    @Test func atTheirBestHidesYours() {
        var f = MapFilters(); f.peakingNow = true
        #expect(!f.keeps(mine()))
    }

    /// The photograph is a file on the phone, so it is read off the sighting.
    /// Asking the adapted tree would hide every tree you own.
    @Test func withAPhotoKeepsTheOnesThatHaveOne() {
        var f = MapFilters(); f.withPhoto = true
        #expect(f.keeps(mine(photo: "shot.jpg")))
        #expect(!f.keeps(mine(photo: nil)))
    }

    /// You collect a tree by adding it, so there is nothing to look up.
    @Test func collectedOnlyKeepsYours() {
        var f = MapFilters(); f.collectedOnly = true
        #expect(f.keeps(mine()))
    }

    /// The id the heart saves under and the id the adapted tree carries are one
    /// string, written once. If they ever part, favouritesOnly goes silently
    /// wrong on your own trees and nothing else notices.
    @Test func theAdaptedTreeCarriesTheSameIdAsTheHeart() {
        let store = Sightings()
        let s = mine()
        #expect(store.asTree(s).id == s.treeKey)
    }
}
