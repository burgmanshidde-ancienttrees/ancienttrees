// The tree page's big button follows the distance with a band, not a line
// (Hidde, 2026-11-04): Collect within 200 m, Take me there again only past
// 250 m, so a wandering fix cannot swap it back and forth.

import Testing
@testable import AncientTrees

@MainActor
struct TheBigButtonHoldsNearTheLine {

    @Test func comingInItSwapsAt200() {
        #expect(!TreeDetail.staysNear(was: false, km: 0.21))
        #expect(TreeDetail.staysNear(was: false, km: 0.2))
    }

    @Test func goingOutItHoldsTo250() {
        #expect(TreeDetail.staysNear(was: true, km: 0.24))
        #expect(TreeDetail.staysNear(was: true, km: 0.25))
        #expect(!TreeDetail.staysNear(was: true, km: 0.26))
    }

    @Test func driftAroundTheLineDoesNotFlip() {
        var near = false
        for d in [0.19, 0.22, 0.18, 0.24, 0.21] { near = TreeDetail.staysNear(was: near, km: d) }
        #expect(near)
    }

    @Test func noFixMeansNotNear() {
        #expect(!TreeDetail.staysNear(was: true, km: nil))
    }
}
