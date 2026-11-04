// Who Find people suggests, and in what order (Kit/SuggestedPeople.swift).
import XCTest
@testable import AncientTrees

@MainActor
final class SuggestedPeopleTests: XCTestCase {
    private let amb = [
        SuggestedPeople.Ambassador(userId: "a-paris", name: "Loic S.", placeSlug: "paris", placeName: "Paris"),
        SuggestedPeople.Ambassador(userId: "a-lisbon", name: "Hugo V.", placeSlug: "lisbon", placeName: "Lisbon"),
        SuggestedPeople.Ambassador(userId: "me", name: "Me", placeSlug: "baarn", placeName: "Baarn"),
    ]
    private let shots = [
        Profiles.Photographer(place: "utrecht", user_id: "p-tom", display_name: "Tom", avatar_url: nil, trees: 2),
        Profiles.Photographer(place: "lisbon", user_id: "p-marieke", display_name: "Marieke", avatar_url: nil, trees: 4),
        Profiles.Photographer(place: "lisbon", user_id: "a-lisbon", display_name: "Hugo V.", avatar_url: nil, trees: 9),
        Profiles.Photographer(place: "lisbon", user_id: "p-blocked", display_name: "B", avatar_url: nil, trees: 3),
    ]

    private func build(following: Set<String> = []) -> [SuggestedPerson] {
        SuggestedPeople.build(ambassadors: amb, photographers: shots,
                              yourPlaces: ["lisbon", "utrecht"],
                              placeName: { ["lisbon": "Lisbon", "utrecht": "Utrecht"][$0] ?? $0 },
                              me: "me", blocked: { $0 == "p-blocked" }, following: following)
    }

    func testYourPlacesAmbassadorFirstThenPhotographersThenOthers() {
        XCTAssertEqual(build().map(\.profile.user_id), ["a-lisbon", "p-marieke", "p-tom", "a-paris"])
    }

    func testNeverYouNeverBlockedOnePerPerson() {
        let ids = build().map(\.profile.user_id)
        XCTAssertFalse(ids.contains("me"))
        XCTAssertFalse(ids.contains("p-blocked"))
        XCTAssertEqual(ids.filter { $0 == "a-lisbon" }.count, 1)
    }

    func testPeopleYouFollowGoToTheEnd() {
        XCTAssertEqual(build(following: ["a-lisbon"]).map(\.profile.user_id).last, "a-lisbon")
    }

    func testReasons() {
        let r = build().map(\.reason)
        XCTAssertEqual(r[0], "Lisbon ambassador")
        XCTAssertEqual(r[1], "Photographed 4 trees in Lisbon")
        XCTAssertEqual(SuggestedPeople.reason(photographed: 1, in: "Baarn"), "Photographed 1 tree in Baarn")
    }

    func testPlacesMostTreesFirst() {
        let city = ["t1": "baarn", "t2": "utrecht", "t3": "utrecht"]
        XCTAssertEqual(SuggestedPeople.places(of: ["t1", "t2", "t3", "x"]) { city[$0] }, ["utrecht", "baarn"])
    }
}
