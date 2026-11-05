// SWITCHES FROM THE SERVER (Hidde, 2026-11-05: "kunnen we deze vragenlijst uit
// de app halen zonder een release"). Firebase's Remote Config does this; ours
// is one file, data/app-switches.json, sent in /api/version.json as
// `switches`, the call this app already makes on launch (EarlyAdopter reads
// the same feed). Asked again every time the app comes back to the front, so a
// switch turned off reaches a phone within one return.
//
// Nothing is kept on the device (hard rule 11 asks it for what a person does;
// a server's switch is not that, and keeping it would only add a way to be
// stale): until the feed answers, everything is ON, as the website is when the
// file has no key.
import Foundation
import Observation

@MainActor @Observable
public final class AppSwitches {
    public static let shared = AppSwitches()

    /// The Ancient Trees Plus question: the row on a city and in Settings.
    public private(set) var plusAsk = true

    public func refresh() async {
        // -plusoff draws the app as a switched-off feed would, for a look
        // without touching the server.
        if ProcessInfo.processInfo.arguments.contains("-plusoff") { plusAsk = false; return }
        guard let (data, _) = try? await Net.data(from: Feed.version),
              let j = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let s = j["switches"] as? [String: Any] else { return }
        plusAsk = (s["plus_ask"] as? Bool) ?? true
    }
}
