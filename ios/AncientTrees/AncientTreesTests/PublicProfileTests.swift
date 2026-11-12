// public_profile()'s answer, with and without the two lists of
// supabase/approved-on-profiles.sql (2026-11-12). The SQL is Hidde's paste,
// so the app meets both shapes: a profile without `approved` and `own` must
// still open, with empty lists, never as "This profile is private".
import XCTest
@testable import AncientTrees

final class PublicProfileTests: XCTestCase {
    private let before = """
    {"user_id":"u1","display_name":"Marieke","avatar_url":null,"country":"NL",
     "created_at":"2026-09-01","followers":3,"following":1,"ambassador":[],
     "visited":["brn_001","brn_002"],"saves":["brn_003"]}
    """

    private let after = """
    {"user_id":"u1","display_name":"Marieke","avatar_url":null,"country":"NL",
     "created_at":"2026-09-01","followers":3,"following":1,"ambassador":["Baarn"],
     "visited":["brn_001","brn_002"],"saves":["brn_003"],
     "approved":["brn_001"],
     "own":[{"id":"6f1a2b3c-4d5e-4f60-8a71-92b3c4d5e6f7","name":"","species":"Pedunculate Oak (Quercus robur)",
             "photo":"u1/6F1A2B3C-4D5E-4F60-8A71-92B3C4D5E6F7.jpg","lat":52.21,"lng":5.28},
            {"id":"not-a-uuid","name":"Lime","species":null,"photo":null,"lat":null,"lng":null}]}
    """

    private func decode(_ s: String) throws -> Profiles.PublicProfile {
        try JSONDecoder().decode(Profiles.PublicProfile.self, from: Data(s.utf8))
    }

    func testWithoutTheNewKeysTheListsAreEmpty() throws {
        let p = try decode(before)
        XCTAssertEqual(p.visited, ["brn_001", "brn_002"])
        XCTAssertEqual(p.approved, [])
        XCTAssertEqual(p.own, [])
    }

    func testWithTheNewKeysApprovedAndOwnDecode() throws {
        let p = try decode(after)
        XCTAssertEqual(p.approved, ["brn_001"])
        XCTAssertEqual(p.own.count, 2)
        let oak = p.own[0]
        XCTAssertEqual(oak.title, "Pedunculate Oak")          // empty name falls back to the species
        XCTAssertEqual(oak.uuid?.uuidString, "6F1A2B3C-4D5E-4F60-8A71-92B3C4D5E6F7")
        XCTAssertEqual(oak.photoURL?.absoluteString,
                       Supa.url + "/storage/v1/object/public/shared-sightings/u1/6F1A2B3C-4D5E-4F60-8A71-92B3C4D5E6F7.jpg")
        XCTAssertEqual(oak.lat, 52.21)
        let lime = p.own[1]
        XCTAssertEqual(lime.title, "Lime")
        XCTAssertNil(lime.uuid)                                // the grid skips a row it cannot open
        XCTAssertNil(lime.photoURL)
    }

    func testAMalformedOwnListNeverHidesTheProfile() throws {
        let p = try decode(before.replacingOccurrences(of: "\"saves\":[\"brn_003\"]",
                                                       with: "\"saves\":[\"brn_003\"],\"own\":\"oops\",\"approved\":null"))
        XCTAssertEqual(p.own, [])
        XCTAssertEqual(p.approved, [])
    }
}
