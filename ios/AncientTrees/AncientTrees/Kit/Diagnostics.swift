// Crash reporting, without a third party in the product.
//
// Hidde, 2026-08-27, on being told the app has none: "crash reporting zullen we
// daar eens mee beginnen dan." The day after launch, an app with no crash
// reporting is an app whose author finds out from a one-star review.
//
// WHY NOT SENTRY OR CRASHLYTICS. Hard rule 5: nothing new ships inside the
// product without his yes, and each one is an SDK, a privacy label, an account
// and something that can break the app while nobody is looking. Apple has
// shipped the boring version since iOS 13 and it needs no dependency at all.
//
// WHAT METRICKIT ACTUALLY DOES, said plainly, because it is not a live crash
// reporter and treating it as one would be a lie in a comment. The system
// gathers diagnostics and hands them over AT MOST ONCE A DAY, on the next
// launch after the crash, and only on a real device: nothing arrives in the
// simulator, ever. So this is "what has been going wrong this week", not "tell
// me the moment somebody crashes". For the second thing you would need a third
// party, and that is a decision with a bill attached.
//
// It also carries hangs, which is the more useful half here. Every performance
// complaint Hidde has made about this app was a stutter rather than a crash,
// and MXHangDiagnostic is exactly that, measured on the phone it happened on.
//
// WHAT WE SEND: the payload's own JSON, the app version and the OS version. No
// user id, no email, no location. A crash does not need to know who you are,
// and not linking it is what keeps this out of the "data linked to you" half of
// the privacy label.

import Foundation
#if canImport(MetricKit)
import MetricKit
#endif

public final class Diagnostics: NSObject {
    public static let shared = Diagnostics()

    /// Anything bigger than this is dropped rather than posted. A payload with
    /// a thousand stack frames is not more useful than one with fifty, and a
    /// megabyte of JSON on somebody's cellular data to tell us about a crash
    /// they already lived through is a poor trade.
    private static let cap = 256 * 1024

    public func start() {
        #if canImport(MetricKit) && !targetEnvironment(simulator)
        MXMetricManager.shared.add(self)
        #endif
    }

    private func post(_ json: Data, kind: String) {
        guard json.count <= Self.cap else { return }
        let version = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "?"
        let build = Bundle.main.infoDictionary?["CFBundleVersion"] as? String ?? "?"
        let body: [String: Any] = [
            "kind": kind,
            "app_version": "\(version) (\(build))",
            "os_version": ProcessInfo.processInfo.operatingSystemVersionString,
            // The payload travels as text and is cast to jsonb by the column,
            // so a payload Apple changes the shape of cannot fail the insert.
            "payload": String(data: json, encoding: .utf8) ?? "",
        ]
        var r = URLRequest(url: Submission.url.deletingLastPathComponent()
            .appendingPathComponent("diagnostics"))
        r.httpMethod = "POST"
        r.setValue(Submission.key, forHTTPHeaderField: "apikey")
        r.setValue("Bearer \(Submission.key)", forHTTPHeaderField: "Authorization")
        r.setValue("application/json", forHTTPHeaderField: "Content-Type")
        r.setValue("return=minimal", forHTTPHeaderField: "Prefer")
        r.httpBody = try? JSONSerialization.data(withJSONObject: body)
        // Fire and forget. A diagnostic that fails to send is not worth a retry
        // queue, a backoff or a line of state: the next payload comes tomorrow.
        URLSession.shared.dataTask(with: r).resume()
    }
}

#if canImport(MetricKit) && !targetEnvironment(simulator)
extension Diagnostics: MXMetricManagerSubscriber {
    /// Crashes and hangs. The other payloads (disk writes, launch time, cellular
    /// conditions) are deliberately not sent: they are interesting and nobody
    /// here would read them, and every one is somebody's data on somebody's
    /// connection.
    public func didReceive(_ payloads: [MXDiagnosticPayload]) {
        for p in payloads {
            let json = p.jsonRepresentation()
            let kind: String
            if !(p.crashDiagnostics?.isEmpty ?? true) { kind = "crash" }
            else if !(p.hangDiagnostics?.isEmpty ?? true) { kind = "hang" }
            else { continue }
            post(json, kind: kind)
        }
    }

    /// Required by the protocol and deliberately empty: the metric payloads are
    /// aggregate performance figures, not faults, and sending them would be
    /// collecting data nobody has asked a question of.
    public func didReceive(_ payloads: [MXMetricPayload]) {}
}
#endif
