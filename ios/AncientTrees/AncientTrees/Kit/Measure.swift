// What people actually do in this app.
//
// Written 2026-08-30 on Hidde's yes to a measurement tool, after the honest
// answer to "do we have analytics at all" turned out to be no. Crashes were
// covered (Diagnostics.swift) and behaviour was not, so nothing here could say
// whether anybody opens the map, taps Take me there, or ever comes back.
//
// Convention: PostHog, the tool the benchmark apps use a paid version of. See
// CONVENTIONS.md, "Measuring what people do in the app", for what AllTrails,
// Strava, Komoot, Polarsteps and iNaturalist actually ship and why this one
// won. EU cloud, so the rows sit in Frankfurt rather than the United States.
//
// NO SDK, AND THAT IS DELIBERATE. PostHog publishes a Swift package and this
// file does not use it, because the package brings its own networking and would
// go round Net.swift, which is the one door every call in this app goes through
// (netcheck.py fails the build on anything that does not). Losing that would
// mean the fault injection could no longer take the network away from it, on
// the one code path most likely to misbehave in a wood with no signal. What the
// package would buy us is session replay and feature flags, and we want neither
// today. What is left is one HTTP POST of a JSON object, which is what an
// analytics SDK is underneath.
//
// WHAT WE SEND: an event name, the app version, the major OS version, and an
// install id that is a random UUID made on this phone. No email, no account id,
// no coordinates, no advertising identifier, nothing Apple would call linked to
// a person. `$process_person_profile: false` tells PostHog not to build a
// profile behind the id, which is both the private option and the cheap one.
//
// WHY IT IS UNLINKED even though we know who is signed in: linking behaviour to
// an account is a different promise to the person and a different privacy
// label, and it is not needed to answer any question phase 1 asks. It can be
// added later on purpose. It cannot be unsent.

import Foundation

public enum Measure {

    /// Write-only and public by design: it can send events in and cannot read
    /// anything out, which is why it sits in the repo like the Supabase
    /// publishable key and the Cloudflare token do.
    private static let key = "phc_nSwWiqWesJZmLMypTZDaeR3MDpcpBwcMpWRy7eUSUpTm"
    private static let host = "https://eu.i.posthog.com/i/v0/e/"

    /// Only the real app measures, the same rule the website runs on: its
    /// beacon checks the hostname so the smoke test's headless Chrome is not
    /// counted as a visitor.
    ///
    /// THE LINE IS THE SIMULATOR, NOT THE BUILD, and the first version of this
    /// file got that wrong within the hour. It gated on DEBUG, which is right
    /// about CI and wrong about the one phone that matters: Xcode installs a
    /// Debug build on a real device, so Hidde walking around with the app in
    /// his hand would have sent nothing at all and it would have looked like a
    /// broken integration rather than a rule working as written.
    ///
    /// What actually needs excluding is the machine: every screenshot sweep, UI
    /// test and CI run happens on a simulator, and no real person is ever on
    /// one. So a simulator stays silent unless `-measure` says otherwise, and a
    /// real device measures whatever way it was built.
    private static var enabled: Bool {
        #if targetEnvironment(simulator)
        return ProcessInfo.processInfo.arguments.contains("-measure")
        #else
        return true
        #endif
    }

    /// A random id per install. Not a device id: it is made here, it is ours
    /// alone, it goes when the app does, and it identifies nobody. Renaming
    /// this key costs no data, only a discontinuity in the numbers, which is
    /// why it is not in UpgradeTests beside the keys that do lose things.
    private static let idKey = "measure.install.v1"
    private static var installId: String {
        if let s = UserDefaults.standard.string(forKey: idKey) { return s }
        let s = UUID().uuidString
        UserDefaults.standard.set(s, forKey: idKey)
        return s
    }

    /// Events that could not be sent, kept for the next launch. THE REASON THIS
    /// EXISTS, and it is not tidiness: this app is used outdoors, so the moment
    /// somebody is most likely to tap Take me there is the moment they are least
    /// likely to have signal. Dropping those would not make the data thinner, it
    /// would make it WRONG, biased towards people standing in city centres with
    /// four bars, which is the opposite of the audience. Capped, because a queue
    /// that grows without limit on a phone that never comes back online is a bug.
    private static let queueKey = "measure.queue.v1"
    private static let queueCap = 50

    /// Record one thing somebody did. Never blocks, never retries in the moment,
    /// never surfaces an error: a measurement that costs somebody a spinner has
    /// cost more than it is worth.
    public static func event(_ name: String, _ props: [String: String] = [:]) {
        guard enabled else { return }
        let version = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "?"
        var p: [String: Any] = props
        p["$process_person_profile"] = false
        p["app_version"] = version
        p["os"] = "iOS \(ProcessInfo.processInfo.operatingSystemVersion.majorVersion)"
        let body: [String: Any] = [
            "api_key": key,
            "event": name,
            "distinct_id": installId,
            // Sent explicitly so an event that waited in the queue overnight is
            // filed under the moment it happened rather than the moment it
            // finally got through.
            "timestamp": ISO8601DateFormatter().string(from: Date()),
            "properties": p,
        ]
        guard let data = try? JSONSerialization.data(withJSONObject: body) else { return }
        send(data)
    }

    private static func send(_ data: Data) {
        guard let url = URL(string: host) else { return }
        var r = URLRequest(url: url)
        r.httpMethod = "POST"
        r.timeoutInterval = 20
        r.setValue("application/json", forHTTPHeaderField: "Content-Type")
        r.httpBody = data
        Net.session.uploadTask(with: r, from: data) { _, response, error in
            let ok = (response as? HTTPURLResponse).map { (200..<300).contains($0.statusCode) } ?? false
            if !ok || error != nil { enqueue(data) }
        }.resume()
    }

    private static func enqueue(_ data: Data) {
        guard let s = String(data: data, encoding: .utf8) else { return }
        var q = UserDefaults.standard.stringArray(forKey: queueKey) ?? []
        q.append(s)
        // The OLDEST go first when the cap is reached. A phone that has been
        // offline for a week should keep this morning rather than last Tuesday.
        if q.count > queueCap { q = Array(q.suffix(queueCap)) }
        UserDefaults.standard.set(q, forKey: queueKey)
    }

    /// Called once at launch. Empties the queue before anything is added to it,
    /// so a failure now simply queues again rather than looping.
    public static func flush() {
        guard enabled else { return }
        let q = UserDefaults.standard.stringArray(forKey: queueKey) ?? []
        guard !q.isEmpty else { return }
        UserDefaults.standard.removeObject(forKey: queueKey)
        for s in q {
            if let d = s.data(using: .utf8) { send(d) }
        }
    }
}
