// The Ancient Trees Plus question's two writes (Hidde, 2026-11-04).
//
// supabase/plus-answers.sql: plus_answers is ANONYMOUS (the publishable key,
// never the session, so no account rides along), plus_waitlist holds the
// account that pressed "Tell me". The website writes the same rows
// (site/src/components/PlusAsk.astro); scripts/plus_answers.py reads both.

import Foundation

public enum PlusAnswers {
    /// The four options, keyed as the database stores them.
    public static let options: [(key: String, label: String)] = [
        ("walks", "Recommended tree walks for a city trip"),
        ("offline", "Download offline maps"),
        ("season", "Seasonal alerts when trees are at their best"),
        ("log", "A richer log of every tree you've collected"),
    ]

    /// One answer, without an account. Fire and forget: a lost answer to a
    /// question costs nobody anything, a spinner would.
    public static func answer(choices: [String], idea: String, other: String = "", shownOrder: [String],
                              city: String, openedFrom: String) async {
        let build = Bundle.main.infoDictionary?["CFBundleVersion"] as? String ?? ""
        var body: [String: Any] = [
            "surface": "app",
            "lang": "en",
            "city": String(city.prefix(80)),
            "opened_from": openedFrom,
            "choices": choices,
            "idea": String(idea.trimmingCharacters(in: .whitespacesAndNewlines).prefix(600)),
            "shown_order": shownOrder.joined(separator: ","),
            "build": build,
        ]
        // Sent only with "Something else", so an answer without it never
        // depends on the column (supabase/plus-answers.sql, 2026-11-05).
        let said = other.trimmingCharacters(in: .whitespacesAndNewlines)
        if choices.contains("other") { body["other_text"] = String(said.prefix(300)) }
        await Supa.post("/rest/v1/plus_answers", token: nil, body: body, prefer: "return=minimal")
    }

    /// "Tell me": this account on the list, once. A second press from another
    /// device is the same answer, so a duplicate is ignored rather than refused.
    public static func joinWaitlist(token: String) async -> Bool {
        await Supa.post("/rest/v1/plus_waitlist", token: token, body: [String: Any](),
                        prefer: "resolution=ignore-duplicates,return=minimal")
    }
}
