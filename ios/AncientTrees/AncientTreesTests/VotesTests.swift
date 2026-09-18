// Your votes and reports, which live in the account and nowhere else.
//
// Hidde, 2026-09-18: "Stop saving stuff locally anywhere please make sure this
// happens nowhere always account related." The third time he has said it, which
// by this project's own ratchet is what turns a rule into a check. The check is
// scripts/localcheck.py; these are the tests for the thing it was written
// about.
//
// Until that day every worth-it vote and every report sat in three UserDefaults
// keys per tree. The account was read at launch and COPIED into them, so the
// views were reading a mirror rather than the account, and the mirror could
// disagree: nothing cleared it on sign-out, so a signed-out phone still showed
// the last person's votes, and a key written per tree cannot be enumerated to
// clear it.

import Testing
import Foundation
@testable import AncientTrees

@MainActor
struct VotesTests {

    /// "not worth it" CONTAINS "worth it", and the reader matched by contains,
    /// so the payoff screen's thumbs down came back as a green thumbs UP on the
    /// tree page. It could not be seen before, because no control ever read
    /// this value back; it was only ever written to the device.
    @Test func aThumbsDownDoesNotComeBackAsAThumbsUp() {
        let v = MyVotes()
        v.setVote("ams_001", "down")
        #expect(v.vote("ams_001") == "down")
        #expect(v.vote("ams_001") != "up", "a no came back as a yes")
    }

    /// The tree field is written as "id (name)" by both surfaces and every view
    /// reads the bare id.
    @Test func theTreeIdIsTakenFromTheRowsOwnFormat() {
        #expect(MyVotes.treeId("kyo_016 (Sudajii of Omiya Gate, Kyoto Gyoen)") == "kyo_016")
        #expect(MyVotes.treeId("ams_001") == "ams_001")
    }

    /// A report carries the reason, because the reason picks the one follow-up
    /// question worth asking. It used to be read from at_wrong_<id>.
    @Test func aReportRemembersWhichReasonWasGiven() {
        let v = MyVotes()
        #expect(!v.hasReported("lon_005"))
        v.markReported("lon_005", reason: "could not tell which tree")
        #expect(v.hasReported("lon_005"))
        #expect(v.reason("lon_005") == "could not tell which tree")
        #expect(!v.hasDetailed("lon_005"))
        v.markDetailed("lon_005")
        #expect(v.hasDetailed("lon_005"))
    }

    /// Signing out takes them off the screen, exactly as it takes the
    /// collection off. They live in the account and come back on the next
    /// sign-in; this is the part the old mirror could not do at all.
    @Test func signingOutTakesTheVotesOffTheScreen() {
        let v = MyVotes()
        v.setVote("ams_001", "up")
        v.markReported("lon_005", reason: "wrong location")
        v.markDetailed("lon_005")

        v.forgetLocally()

        #expect(v.vote("ams_001").isEmpty, "a signed-out phone still shows a vote")
        #expect(!v.hasReported("lon_005"))
        #expect(!v.hasDetailed("lon_005"))
    }

    /// And the keys the old mirror left on phones that already have them go,
    /// signed in or out. They cannot be enumerated any other way.
    @Test func theOldPerTreeKeysAreSweptOffThePhone() {
        let d = UserDefaults.standard
        d.set("up", forKey: "at_worthit_test_001")
        d.set("wrong location", forKey: "at_wrong_test_001")
        d.set(true, forKey: "at_wrong_detail_test_001")

        MyVotes.clearTheOldMirror()

        #expect(d.object(forKey: "at_worthit_test_001") == nil)
        #expect(d.object(forKey: "at_wrong_test_001") == nil)
        #expect(d.object(forKey: "at_wrong_detail_test_001") == nil)
    }
}
