// Joining the waitlist from inside the app, which is what the paywall's button
// actually does until payment exists. Same table the website's app page writes
// to, same publishable key, so the number Hidde reads in the digest counts app
// intent alongside web intent rather than splitting it into two places nobody
// compares.

import Foundation

public enum Waitlist {
    static let url = URL(string: "https://caimvxiyrtifilimlkqw.supabase.co/rest/v1/waitlist")!
    static let key = "sb_publishable_qOTuw-LCejk2VhO2J6aXGQ_6X2O2mgb"

    /// The email address is the whole point and it was missing until 2026-08-20.
    ///
    /// The button said "Tell me when this opens" and the screen answered "We
    /// will tell you the day it opens", and the row that reached the database
    /// carried a source and a note and no way to reach anybody. That is a
    /// promise we could not keep, which is the one thing the never-cuttable list
    /// forbids outright. It now sends the address of the account the person is
    /// signed in with, and the paywall does not offer the button until there is
    /// one.
    @discardableResult
    public static func join(reason: String, email: String) async -> Bool {
        var r = URLRequest(url: url)
        r.httpMethod = "POST"
        r.timeoutInterval = 20
        r.setValue(key, forHTTPHeaderField: "apikey")
        r.setValue("application/json", forHTTPHeaderField: "Content-Type")
        r.setValue("return=minimal", forHTTPHeaderField: "Prefer")
        // Only the columns the table actually has. It was posting a "note"
        // field, waitlist has no such column, and PostgREST rejects the whole
        // row with a 400. So the paywall button had never written a single row
        // in its life while telling everyone who pressed it that we would be in
        // touch. The reason rides along in source instead.
        r.httpBody = try? JSONSerialization.data(withJSONObject: [
            "source": "ios-app:" + reason,
            "email": email,
        ])
        guard let (_, resp) = try? await URLSession.shared.data(for: r),
              let http = resp as? HTTPURLResponse else { return false }
        return (200..<300).contains(http.statusCode)
    }
}
