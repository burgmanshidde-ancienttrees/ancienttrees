// What the app does when the network does not work.
//
// This is the half that had never been tested, and it is the half a walking app
// meets most: no signal in a wood, a hotel wifi that accepts a connection and
// then says nothing, a Supabase answering 500, a session left alone for three
// weeks. Faults.swift makes each of those reachable; these are the answers.
//
// SERIALIZED, and it has to be. Swift Testing runs tests side by side by
// default and the fault state is one global, so two tests arming it at once
// would give each other's answers and the failure would look like a bug in the
// app.

import Testing
import Foundation
@testable import AncientTrees

// The stores are main-actor isolated (see Account.swift), so a suite that
// builds one asks on the main actor.
@MainActor
/// ONE serialized suite around both, and the nesting is the point rather than
/// tidiness. They were two top-level suites for an afternoon, each marked
/// serialized, and Swift Testing still ran the two of them side by side: the
/// stalled-connection test armed the eight second fault globally and a merge
/// test running in the next lane got the stall meant for it. The failure looked
/// exactly like a bug in CloudSync. A serialized parent is what actually stops
/// two tests sharing one global.
@Suite(.serialized)
struct WithTheNetworkTakenAway {

    // Nested types do not inherit the enclosing suite's actor, so this says
    // it again: Account and Saved are main-actor isolated.
    @MainActor
    struct WhenTheNetworkFails {

        private func session(freshness: TimeInterval) -> Session {
            Session(accessToken: "access", refreshToken: "refresh",
                    expiresAt: Date().addingTimeInterval(freshness),
                    userId: "00000000-0000-0000-0000-0000000000ab",
                    email: "walker@ancienttrees.app")
        }

        /// The bug this whole exercise found on its first day, kept as the test that
        /// stops it coming back.
        ///
        /// Every failed refresh took one branch and that branch was signOut(), so
        /// opening the app an hour after signing in, in a wood with no bereik,
        /// cleared the Keychain and asked the person to sign in again. In the exact
        /// place the app is for.
        @Test func noSignalDoesNotSignYouOut() async {
            Faults.reset(); defer { Faults.reset() }
            Faults.mode = .offline

            let account = Account(restoring: session(freshness: 60))   // stale: needs a refresh
            let ok = await account.refreshIfNeeded()

            #expect(ok == false, "it cannot have refreshed with no network")
            #expect(account.isSignedIn,
                    "no signal signed the person out and took the Keychain with it")
        }

        /// A stall is not a refusal, and it used to be treated as one too. Eight
        /// seconds of nothing has to end the same way: still signed in.
        @Test func aStalledConnectionDoesNotSignYouOutEither() async {
            Faults.reset(); defer { Faults.reset() }
            Faults.mode = .slow

            let account = Account(restoring: session(freshness: 60))
            _ = await account.refreshIfNeeded()

            #expect(account.isSignedIn, "a stalled connection signed the person out")
        }

        /// The other half, and it must still work: when the server ANSWERS and the
        /// answer is no, that is a real sign-out. A revoked token left in place
        /// shows an account screen that cannot save anything.
        @Test func arefusedTokenIsARealSignOut() async {
            Faults.reset(); defer { Faults.reset() }
            Faults.mode = .expired                                  // 401 on everything

            let account = Account(restoring: session(freshness: 60))
            let ok = await account.refreshIfNeeded()

            #expect(ok == false)
            #expect(!account.isSignedIn, "a refused refresh token left a dead session in place")
        }

        /// And a server having a bad ten minutes is not a verdict on your token
        /// either. A 5xx that signed people out would be the same bug as the one
        /// above, arriving through a different door.
        @Test func aBrokenServerDoesNotSignYouOut() async {
            Faults.reset(); defer { Faults.reset() }
            Faults.mode = .server                               // 500 on everything

            let account = Account(restoring: session(freshness: 60))
            let ok = await account.refreshIfNeeded()

            #expect(ok == false)
            #expect(account.isSignedIn, "a 500 from the server signed the person out")
        }

        /// TWO ASKS AT ONCE MUST BE ONE REQUEST, and the reason is not thrift.
        ///
        /// Launch asks three times over: refreshIfNeeded() directly, and
        /// freshToken() from the profiles load and the moderation load. All
        /// three used to see the same stale session and post the SAME refresh
        /// token, and Supabase rotates it. Its reuse window covers a fast
        /// network and nothing else, so on a slow one the second answer is a
        /// refusal, and a refusal here is a real sign-out that empties the
        /// Keychain. A perfectly good session thrown away because the app asked
        /// politely twice, which is the shape of every "ik was ineens
        /// uitgelogd" that nobody can reproduce.
        @Test func twoRefreshesAtOnceOnlyAskOnce() async {
            Faults.reset(); defer { Faults.reset() }
            Faults.mode = .server                   // answers, and is not a sign-out

            let account = Account(restoring: session(freshness: 60))
            async let first = account.refreshIfNeeded()
            async let second = account.refreshIfNeeded()
            _ = await (first, second)

            #expect(Faults.sent(to: "grant_type=refresh_token").count == 1,
                    "two callers spent the same refresh token twice")
            #expect(account.isSignedIn, "the second ask signed the person out")
        }

        /// A token good for another hour must not cost a request. This is on every
        /// launch, so getting it wrong is a round trip before the first frame.
        @Test func aFreshSessionAsksNobody() async {
            Faults.reset(); defer { Faults.reset() }
            Faults.mode = .offline

            let account = Account(restoring: session(freshness: 3600))
            let ok = await account.refreshIfNeeded()

            #expect(ok, "a session with an hour left refused to be used")
            #expect(Faults.seen.isEmpty, "a fresh session went to the network anyway")
        }

        /// Plain words on the screen, never a status code. The sign-in form is where
        /// somebody meets a 500, and "HTTP 500" has never helped anybody.
        @Test func aBrokenServerSaysSomethingAPersonCanRead() async {
            Faults.reset(); defer { Faults.reset() }
            Faults.mode = .server                                   // 500 on everything

            let account = Account(restoring: nil)
            await account.sendCode(to: "walker@ancienttrees.app")

            #expect(account.state == .signedOut, "the form was left spinning on working")
            let problem = account.problem ?? ""
            #expect(!problem.isEmpty, "a failed sign-in said nothing at all")
            #expect(!problem.contains("500"), "a status code reached the screen")
        }
    }

    @MainActor
    @Suite(.serialized)
    struct WhenSigningInOnAPhoneThatAlreadyHasTrees {

        private struct Scratch {
            let name = "test.saved." + UUID().uuidString
            var defaults: UserDefaults { UserDefaults(suiteName: name)! }
            func clean() { UserDefaults.standard.removePersistentDomain(forName: name) }
        }

        private func signedIn() -> Account {
            Account(restoring: Session(accessToken: "access", refreshToken: "refresh",
                                       expiresAt: .distantFuture,
                                       userId: "00000000-0000-0000-0000-0000000000ab",
                                       email: "walker@ancienttrees.app"))
        }

        /// The merge rule is UNION, and this is the moment it matters: six trees on
        /// the phone, four in the account, and the answer has to be ten. Anything
        /// else silently destroys work somebody did on an afternoon out.
        @Test func bothHalvesSurviveRatherThanOneReplacingTheOther() async {
            Faults.reset(); defer { Faults.reset() }
            let s = Scratch(); defer { s.clean() }

            let saved = Saved(defaults: s.defaults)
            saved.toggleSaved("ams_001")                            // this phone's tree
            saved.toggleVisited("ams_002")

            Faults.stub("/rest/v1/saves", json: [["tree_id": "lon_005", "created_at": "2026-07-01"]])
            Faults.stub("/rest/v1/visited", json: [["tree_id": "par_003", "visited_at": "2026-06-14"]])

            let pulled = await CloudSync.merge(account: signedIn(), saved: saved)

            #expect(pulled == 2, "the account's trees did not arrive")
            #expect(saved.entries["ams_001"] != nil, "signing in threw away this phone's tree")
            #expect(saved.entries["ams_002"] != nil)
            #expect(saved.entries["lon_005"] != nil)
            #expect(saved.isVisited("par_003"), "a visit from the account came back as a plain save")
        }

        /// And the union goes back UP, which is what makes a collection survive a
        /// new phone. Asserted on what was actually posted rather than on a return
        /// value, because the return value cannot tell you the body was empty.
        @Test func thePhonesOwnTreesArePushedToTheAccount() async {
            Faults.reset(); defer { Faults.reset() }
            let s = Scratch(); defer { s.clean() }

            let saved = Saved(defaults: s.defaults)
            saved.toggleSaved("ams_001")
            saved.toggleVisited("ams_002")

            Faults.stub("/rest/v1/saves", json: [])
            Faults.stub("/rest/v1/visited", json: [])

            await CloudSync.merge(account: signedIn(), saved: saved)

            let pushed = Faults.sent(to: "/rest/v1/saves").filter { $0.method == "POST" }
            #expect(pushed.count == 1, "nothing was pushed, so a new phone would start empty")
            let body = pushed.first?.text ?? ""
            #expect(body.contains("ams_001"))
            #expect(body.contains("ams_002"))
        }

        /// The phone is the copy that is already right. A sync that cannot reach
        /// anybody must leave it exactly as it was rather than emptying it to match
        /// a server it never spoke to.
        @Test func aSyncThatReachesNobodyLeavesThePhoneAlone() async {
            Faults.reset(); defer { Faults.reset() }
            let s = Scratch(); defer { s.clean() }

            let saved = Saved(defaults: s.defaults)
            saved.toggleVisited("ams_001")
            saved.toggleSaved("ams_002")

            Faults.mode = .offline
            await CloudSync.merge(account: signedIn(), saved: saved)

            #expect(saved.entries.count == 2, "a failed sync changed the collection")
            #expect(saved.isVisited("ams_001"))
            #expect(saved.isSaved("ams_002"))
        }

        /// Broken JSON from the account must not be read as an empty account.
        @Test func garbageFromTheAccountIsNotReadAsAnEmptyAccount() async {
            Faults.reset(); defer { Faults.reset() }
            let s = Scratch(); defer { s.clean() }

            let saved = Saved(defaults: s.defaults)
            saved.toggleSaved("ams_001")

            Faults.mode = .garbage
            let pulled = await CloudSync.merge(account: signedIn(), saved: saved)

            #expect(pulled == 0)
            #expect(saved.entries.count == 1, "unreadable JSON emptied the collection")
        }
    }
}
