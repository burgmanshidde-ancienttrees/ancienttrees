// Joining the waitlist from inside the app, which is what the paywall's button
// actually does until payment exists. Same table the website's app page writes
// to, same publishable key, so the number Hidde reads in the digest counts app
// intent alongside web intent rather than splitting it into two places nobody
// compares.

import Foundation

public enum Waitlist {
    /// The project and the key live on Supa. They were written out here as
    /// well, and in Submissions, so the same publishable key sat in three
    /// files: three places to edit the day it rotates, and two of them easy to
    /// miss.
    static let path = "/rest/v1/waitlist"

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
        // Only the columns the table actually has. It was posting a "note"
        // field, waitlist has no such column, and PostgREST rejects the whole
        // row with a 400. So the paywall button had never written a single row
        // in its life while telling everyone who pressed it that we would be in
        // touch. The reason rides along in source instead.
        return await Supa.post(path, body: ["source": "ios-app:" + reason,
                                            "email": email],
                               prefer: "return=minimal")
    }
}
