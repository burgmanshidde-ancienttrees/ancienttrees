// Joining the waitlist from inside the app, which is what the paywall's button
// actually does until payment exists. Same table the website's app page writes
// to, same publishable key, so the number Hidde reads in the digest counts app
// intent alongside web intent rather than splitting it into two places nobody
// compares.

import Foundation

public enum Waitlist {
    static let url = URL(string: "https://caimvxiyrtifilimlkqw.supabase.co/rest/v1/waitlist")!
    static let key = "sb_publishable_qOTuw-LCejk2VhO2J6aXGQ_6X2O2mgb"

    @discardableResult
    public static func join(reason: String) async -> Bool {
        var r = URLRequest(url: url)
        r.httpMethod = "POST"
        r.setValue(key, forHTTPHeaderField: "apikey")
        r.setValue("application/json", forHTTPHeaderField: "Content-Type")
        r.setValue("return=minimal", forHTTPHeaderField: "Prefer")
        r.httpBody = try? JSONSerialization.data(withJSONObject: [
            "source": "ios-app",
            "note": reason,
        ])
        guard let (_, resp) = try? await URLSession.shared.data(for: r),
              let http = resp as? HTTPURLResponse else { return false }
        return (200..<300).contains(http.statusCode)
    }
}
