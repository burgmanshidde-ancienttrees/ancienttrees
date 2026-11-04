// Two small guards from the 2026-11-04 audit.
//
// Loading the account runs once at a time (Kit/SingleFlight.swift): at a cold
// launch the launch task and the scene turning active both started it, so the
// two merges ran side by side. And a share link is built without a force
// unwrap (WebLink.site), so an odd slug shares the home page, never a crash.

import Testing
import Foundation
@testable import AncientTrees

@MainActor
struct LoadingTheAccountRunsOnce {

    @MainActor final class Count { var n = 0 }

    @Test func aSecondCallerWaitsForTheFirst() async {
        let flight = SingleFlight()
        let runs = Count()
        let first = Task { @MainActor in
            await flight.run {
                runs.n += 1
                try? await Task.sleep(for: .milliseconds(80))
            }
        }
        let second = Task { @MainActor in
            await flight.run {
                runs.n += 1
                try? await Task.sleep(for: .milliseconds(80))
            }
        }
        await first.value
        await second.value
        #expect(runs.n == 1, "two loads ran at once")
        #expect(!flight.isRunning)
    }

    @Test func aLaterCallRunsAgain() async {
        let flight = SingleFlight()
        let runs = Count()
        await flight.run { runs.n += 1 }
        await flight.run { runs.n += 1 }
        #expect(runs.n == 2, "a finished load blocked the next one")
    }
}

@MainActor
struct AShareLinkNeverCrashes {

    @Test func aCityAndItsWalks() {
        #expect(WebLink.site("lisbon").absoluteString == "https://ancienttrees.app/lisbon")
        #expect(WebLink.site("lisbon/walks").absoluteString == "https://ancienttrees.app/lisbon/walks")
    }

    @Test func anOddSlugIsEscapedNotFatal() {
        let url = WebLink.site("são paulo")
        #expect(url.host == "ancienttrees.app")
        #expect(url.absoluteString.hasPrefix("https://ancienttrees.app/"))
    }
}
