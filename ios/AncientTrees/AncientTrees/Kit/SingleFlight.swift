// One run of a piece of work at a time; a second caller waits for the first.
//
// Loading the account (the collection, your trees and their photographs) was
// started from two places at a cold launch: the launch task, and the scene
// becoming active while the profile had not arrived yet, which at launch it
// never has. Both ran CloudSync.merge and SightingSync.merge at once, so the
// same photographs downloaded twice and two merges wrote the same rows (audit,
// 2026-11-04). The shape is Account.refreshTask's: the running task is kept,
// a caller that finds one awaits it, and the task clears itself when done.

import Foundation

@MainActor
final class SingleFlight {
    private var running: Task<Void, Never>?

    /// Whether a run is under way right now.
    var isRunning: Bool { running != nil }

    /// Run `work`, or, when a run is already under way, wait for that one
    /// instead of starting a second.
    func run(_ work: @escaping @MainActor () async -> Void) async {
        if let running { return await running.value }
        let task = Task { @MainActor in
            defer { self.running = nil }
            await work()
        }
        running = task
        await task.value
    }
}
