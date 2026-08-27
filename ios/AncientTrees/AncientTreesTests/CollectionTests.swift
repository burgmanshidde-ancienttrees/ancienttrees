// The collection, tested, because it is the one thing in this app a person
// cannot get back.
//
// A wrong pin is an edit and a missing photo is a gap. A collection that eats an
// entry is somebody's afternoon deleted, and they will not tell us, they will
// just stop opening it. Saved was 181 lines carrying two independent lists and
// had never had a test.
//
// Every test here uses its own throwaway UserDefaults suite, so a test about
// losing trees cannot lose the simulator's trees and two tests cannot read each
// other's collection.

import Testing
import Foundation
@testable import AncientTrees

/// A collection that belongs to one test and is thrown away after it.
private struct Scratch {
    let name = "test.saved." + UUID().uuidString
    var defaults: UserDefaults { UserDefaults(suiteName: name)! }
    func clean() { UserDefaults.standard.removePersistentDomain(forName: name) }
}

struct TheTwoLists {

    /// Hidde, 2026-08-26: "je kunt niet bomen uit je collected halen door ze te
    /// ontfavorieten, die dingen zijn twee verschillende lijsten." This is that
    /// sentence as a test, so the next refactor of Saved cannot quietly undo it.
    @Test func takingTheHeartOffACollectedTreeKeepsTheCollection() {
        let s = Scratch(); defer { s.clean() }
        let saved = Saved(defaults: s.defaults)

        saved.toggleVisited("ams_001")          // stood in front of it
        saved.toggleSaved("ams_001")            // and hearted it
        #expect(saved.isVisited("ams_001"))
        #expect(saved.isSaved("ams_001"))

        saved.toggleSaved("ams_001")            // heart off again
        #expect(!saved.isSaved("ams_001"))
        #expect(saved.isVisited("ams_001"),
                "unhearting a tree threw away the fact that you had stood in front of it")
        #expect(saved.collected.count == 1)
        #expect(saved.favourites.isEmpty)
    }

    /// And the same thing pointing the other way.
    @Test func untickingATreeYouAlsoHeartedKeepsTheHeart() {
        let s = Scratch(); defer { s.clean() }
        let saved = Saved(defaults: s.defaults)

        saved.toggleSaved("ams_002")
        saved.toggleVisited("ams_002")
        saved.toggleVisited("ams_002")          // untick

        #expect(!saved.isVisited("ams_002"))
        #expect(saved.isSaved("ams_002"), "unticking a visit took the heart with it")
    }

    /// A row with nothing left in it means nothing and goes, or the collection
    /// grows forever with trees nobody has any relationship with.
    @Test func aRowWithNothingLeftInItIsRemoved() {
        let s = Scratch(); defer { s.clean() }
        let saved = Saved(defaults: s.defaults)

        saved.toggleSaved("ams_003")
        saved.toggleSaved("ams_003")
        #expect(saved.entries["ams_003"] == nil)

        saved.toggleVisited("ams_004")
        saved.toggleVisited("ams_004")
        #expect(saved.entries["ams_004"] == nil)
    }

    /// Ticking a tree is no longer allowed to heart it as a side effect.
    @Test func collectingDoesNotHeart() {
        let s = Scratch(); defer { s.clean() }
        let saved = Saved(defaults: s.defaults)

        saved.toggleVisited("ams_005")
        #expect(saved.isVisited("ams_005"))
        #expect(!saved.isSaved("ams_005"), "collecting a tree put it in the other list too")
    }

    /// The cloud half tells Saved about a change through onMutate, and a removal
    /// has to arrive as one. If a removal did not fire, the tree would come
    /// straight back on the next sign-in.
    @Test func removingATreeIsReportedAsARemoval() {
        let s = Scratch(); defer { s.clean() }
        let saved = Saved(defaults: s.defaults)

        var reported: [(String, Bool)] = []
        saved.onMutate = { id, entry in reported.append((id, entry != nil)) }

        saved.toggleSaved("ams_006")
        saved.toggleSaved("ams_006")

        #expect(reported.map(\.0) == ["ams_006", "ams_006"])
        #expect(reported.map(\.1) == [true, false],
                "the removal was not reported, so the account would keep the tree")
    }
}

struct TheCollectionSurvives {

    /// Day thirty, and the second launch. UserDefaults is the whole reason the
    /// app can promise this where the website could not.
    @Test func aCollectionIsStillThereWhenTheAppIsOpenedAgain() {
        let s = Scratch(); defer { s.clean() }

        let first = Saved(defaults: s.defaults)
        first.toggleVisited("ams_001")
        first.toggleSaved("ams_002")

        let reopened = Saved(defaults: s.defaults)
        #expect(reopened.isVisited("ams_001"))
        #expect(reopened.isSaved("ams_002"))
        #expect(reopened.entries.count == 2)
    }

    /// A row written before `favourite` existed was a heart by definition.
    /// Reading it as anything else would empty the favourites list of everybody
    /// who collected before 2026-08-26.
    @Test func anOldRowWithoutTheFavouriteFieldIsStillAHeart() throws {
        let json = Data("""
        [{"treeId":"ams_009","savedAt":770000000}]
        """.utf8)
        let decoded = try JSONDecoder().decode([Saved.Entry].self, from: json)
        #expect(decoded.first?.favourite == true,
                "an upgrade emptied everybody's favourites")
    }

    /// What the account sends back must not overwrite what the phone knows. The
    /// visit is the fact worth most and the earlier save date is the true one.
    @Test func adoptingARowKeepsTheVisitAndTheEarlierDate() {
        let s = Scratch(); defer { s.clean() }
        let saved = Saved(defaults: s.defaults)

        saved.toggleVisited("ams_007")                 // visited, today
        let mine = saved.entries["ams_007"]?.savedAt

        let older = Date(timeIntervalSince1970: 700_000_000)
        saved.adopt(treeId: "ams_007", visitedAt: nil, savedAt: older)

        #expect(saved.isVisited("ams_007"), "a row from the account erased a visit")
        #expect(saved.entries["ams_007"]?.savedAt == older,
                "the earlier of the two save dates did not win")
        #expect(mine != nil)
    }
}
