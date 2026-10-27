// The catch-up after sign-in sends only what changed.
//
// Until 2026-10-27 `SightingSync.pushAll` re-sent every sighting on the phone
// whenever a session appeared, and every send stamped the row as freshly
// saved. Nothing was lost or doubled, but the server could no longer tell a
// new photograph from an old one: the Tangier fig came back on Hidde's digest
// as new, and one person's thirteen trees were "saved" in the same minute.
//
// These tests pin the rule that decides, `Sightings.needsPush`, and the two
// marks that feed it. The network half is not here: it is the same `push` as
// before, now called for fewer rows.

import Testing
import Foundation
@testable import AncientTrees

@MainActor
struct SyncOnlyChangedTests {

    private func folder() -> URL {
        let url = FileManager.default.temporaryDirectory
            .appendingPathComponent("sync-print-" + UUID().uuidString)
        try? FileManager.default.createDirectory(at: url, withIntermediateDirectories: true)
        return url
    }

    /// One tree on a fresh phone, the way a merge leaves it, without firing
    /// the send hook other tests listen to.
    private func one(in s: Sightings) -> Sightings.Sighting {
        s.adopt(Sightings.Sighting(name: "The fig", note: "Enormous.", lat: 35.78, lng: -5.81), image: nil)
        return s.all[0]
    }

    @Test func aTreeTheAccountHasNeverConfirmedIsSent() {
        let dir = folder(); defer { try? FileManager.default.removeItem(at: dir) }
        let s = Sightings(folder: dir)
        var fig = one(in: s)
        fig.syncedAt = nil
        fig.sentPrint = nil
        #expect(Sightings.needsPush(fig), "a tree the account never confirmed was skipped")
    }

    @Test func anUnchangedTreeIsNotSentAgain() {
        let dir = folder(); defer { try? FileManager.default.removeItem(at: dir) }
        let s = Sightings(folder: dir)
        let fig = one(in: s)
        s.markSynced(fig.id, sent: fig)
        #expect(!Sightings.needsPush(s.all[0]),
                "the catch-up re-sent a tree with nothing new in it")
    }

    @Test func anEditAfterTheLastSendIsSent() {
        let dir = folder(); defer { try? FileManager.default.removeItem(at: dir) }
        let s = Sightings(folder: dir)
        let fig = one(in: s)
        s.markSynced(fig.id, sent: fig)

        var edited = s.all[0]
        edited.note = "Enormous, and the roots run out across the grass."
        #expect(Sightings.needsPush(edited), "a changed note never reached the account")

        var moved = s.all[0]
        moved.treeId = "tng_001"
        #expect(Sightings.needsPush(moved), "a tree filed under one of ours stayed unfiled")

        var unshared = s.all[0]
        unshared.shared = false
        #expect(Sightings.needsPush(unshared), "stop sharing never reached the account")
    }

    /// What the phone keeps for itself is not a change the account cares about.
    @Test func lookingAtATreeDoesNotMakeItChanged() {
        let dir = folder(); defer { try? FileManager.default.removeItem(at: dir) }
        let s = Sightings(folder: dir)
        let fig = one(in: s)
        s.markSynced(fig.id, sent: fig)

        var looked = s.all[0]
        looked.place = "Tangier"
        looked.syncedAt = Date().addingTimeInterval(3600)
        #expect(!Sightings.needsPush(looked), "a local-only field made the tree look edited")
    }

    /// A send that started and never landed is sent again, even when the
    /// fingerprint would match: a photograph replaced under the same file name
    /// changes nothing the fingerprint can see.
    @Test func aSendThatNeverLandedIsSentAgain() {
        let dir = folder(); defer { try? FileManager.default.removeItem(at: dir) }
        let s = Sightings(folder: dir)
        let fig = one(in: s)
        s.markSynced(fig.id, sent: fig)
        s.markUnsent(fig.id)
        #expect(Sightings.needsPush(s.all[0]), "a failed send was forgotten")
    }

    @Test func aDraftIsNeverSent() {
        let dir = folder(); defer { try? FileManager.default.removeItem(at: dir) }
        let s = Sightings(folder: dir)
        var fig = one(in: s)
        fig.draft = true
        fig.syncedAt = nil
        #expect(!Sightings.needsPush(fig), "a draft went up before Save was pressed")
    }

    /// The fingerprint survives the phone's own file, or every launch would
    /// look like a change.
    @Test func theFingerprintSurvivesARelaunch() {
        let dir = folder(); defer { try? FileManager.default.removeItem(at: dir) }
        let s = Sightings(folder: dir)
        let fig = one(in: s)
        s.markSynced(fig.id, sent: fig)

        let again = Sightings(folder: dir)
        #expect(again.all.count == 1)
        #expect(!Sightings.needsPush(again.all[0]), "a relaunch made every tree look changed")
    }
}
