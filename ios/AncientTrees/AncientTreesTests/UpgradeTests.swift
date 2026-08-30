// The day the app updates, with somebody's data already on the phone.
//
// This is the failure Hidde has already lived through once, and it is the one
// kind of bug that arrives for EVERYBODY at the same moment: an update ships,
// and the data written by the version before it no longer fits. Nobody is
// doing anything unusual. They just opened the app.
//
// Nothing here installs one build over another, and it does not need to. What
// an upgrade actually IS, from the code's point of view, is old bytes meeting
// new code, and old bytes can simply be written down. That also makes it
// repeatable, which a real install-over-install is not.
//
// The salvage tests in MyTreesTests cover the same question for your own
// trees. These cover the catalogue and the collection.

import Testing
import Foundation
@testable import AncientTrees

// The stores are main-actor isolated (see Account.swift), so a suite that
// builds one asks on the main actor.
@MainActor
@Suite(.serialized)
struct WhenTheAppUpdatesUnderneathYou {

    private struct Downloads {
        let url: URL
        init() {
            url = FileManager.default.temporaryDirectory
                .appendingPathComponent("catalogue-test-" + UUID().uuidString)
            try? FileManager.default.createDirectory(at: url, withIntermediateDirectories: true)
        }
        func clean() { try? FileManager.default.removeItem(at: url) }
        func put(_ name: String, _ text: String) {
            try? Data(text.utf8).write(to: url.appendingPathComponent("\(name).json"))
        }
        var exists: Bool { FileManager.default.fileExists(atPath: url.path) }
    }

    /// THE ONE THAT WOULD HAVE HIT EVERYBODY. A phone that has ever synced
    /// holds a downloaded trees.json. The moment an update ships where that
    /// file no longer decodes, the app used to end up with no catalogue at all:
    /// an empty map, an empty Discover, and no way out but delete and reinstall.
    /// The bundled copy was sitting right there the whole time.
    @Test func aDownloadFromAnOlderAppFallsBackToTheBundledCopy() {
        let d = Downloads(); defer { d.clean() }
        // What a model gaining a required field looks like from here.
        d.put("trees", #"{"version":"old","count":1,"trees":[{"nonsense":true}]}"#)

        let store = CatalogueStore(downloads: d.url)
        store.loadBundled()

        #expect(store.catalogue != nil,
                "a stale download emptied the whole app: \(store.loadError ?? "no error given")")
        #expect((store.catalogue?.trees.count ?? 0) > 500,
                "the app came up with almost no trees")
        #expect(store.loadError == nil, "it recovered and still reported an error")
    }

    /// And it throws the stale copy away. Leaving it means paying that failure
    /// on every single launch, because refresh() asks whether the VERSION
    /// changed and it has not: the phone believes it is up to date with a file
    /// it can no longer read.
    @Test func theStaleDownloadIsNotKeptForever() {
        let d = Downloads(); defer { d.clean() }
        d.put("trees", "not json at all")

        let store = CatalogueStore(downloads: d.url)
        store.loadBundled()

        #expect(store.catalogue != nil)
        #expect(!d.exists, "the unreadable download was kept, so every launch pays for it again")
    }

    /// Half a download is the other shape of this: trees synced, browse.json
    /// added in a later release and never fetched. Falling back per file is
    /// what makes a new feed work on an old download the first time it is
    /// asked for, and it must keep working.
    @Test func aDownloadMissingANewerFeedStillWorks() {
        let d = Downloads(); defer { d.clean() }
        // Nothing at all in the download directory: every file comes from the
        // bundle, which is a fresh install and also the oldest possible upgrade.
        let store = CatalogueStore(downloads: d.url)
        store.loadBundled()

        #expect(store.catalogue != nil)
        #expect((store.catalogue?.collections.count ?? 0) >= 5,
                "collections went missing when nothing had been downloaded")
    }
}

/// The names on disk are an interface with the past, and renaming one is a
/// silent data loss that no compiler and no test would otherwise notice: the
/// old rows simply stop being found and the app looks empty on a phone that
/// had everything.
///
/// These are deliberately literal. If one of them has to change, this test is
/// where somebody is told to write a migration first.
// The stores are main-actor isolated (see Account.swift), so a suite that
// builds one asks on the main actor.
@MainActor
@Suite(.serialized)
struct TheNamesOnDiskDoNotMove {

    @Test func theCollectionIsStillWhereEveryPreviousVersionPutIt() {
        let suite = "upgrade." + UUID().uuidString
        let defaults = UserDefaults(suiteName: suite)!
        defer { UserDefaults.standard.removePersistentDomain(forName: suite) }

        let saved = Saved(defaults: defaults)
        saved.toggleSaved("ams_001")

        #expect(defaults.data(forKey: "saved.entries.v1") != nil,
                "the collection moved to another key, so every existing phone reads empty")
    }

    @Test func theLastKnownPositionIsStillWhereItWas() {
        // Read rather than written, because it is what a previous version left
        // behind that has to keep being found.
        UserDefaults.standard.set([52.37, 4.89], forKey: "ancienttrees.last_fix")
        defer { UserDefaults.standard.removeObject(forKey: "ancienttrees.last_fix") }

        let remembered = LocationProvider.remembered
        #expect(remembered?.lat == 52.37,
                "the remembered position key moved, so every phone forgets where it was")
    }

    /// Your own trees live in a folder rather than in UserDefaults, and its name
    /// is the same kind of promise.
    @Test func yourOwnTreesAreStillInTheSameFolder() {
        #expect(Sightings.defaultFolder.lastPathComponent == "sightings",
                "the folder holding everybody's own photographs was renamed")
    }
}
