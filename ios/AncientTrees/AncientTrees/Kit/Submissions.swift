// Sending something back. Readers are the correction layer on this project, not
// a nice-to-have: the whole publishing standard rests on shipping what verifies,
// flagging what does not, and letting people who are standing in front of the
// tree tell us what is wrong.
//
// The app is where that matters most. Somebody at a pin that points at the wrong
// trunk is the one person who can say so, and until now they had to go and find
// the website to do it.
//
// The key below is the same publishable key the website already ships in its own
// JavaScript, so it is public by design and protected by row-level security
// rather than by secrecy. It is not a new dependency either: Supabase is already
// in the product.

import Foundation

public enum Submission {
    public enum Kind: String, CaseIterable, Identifiable, Sendable {
        case tree, city, correction
        public var id: String { rawValue }
        public var label: String {
            switch self {
            case .tree: "A tree we are missing"
            case .city: "A place we should map"
            case .correction: "Something here is wrong"
            }
        }
    }

    static let url = URL(string: "https://caimvxiyrtifilimlkqw.supabase.co/rest/v1/submissions")!
    static let key = "sb_publishable_qOTuw-LCejk2VhO2J6aXGQ_6X2O2mgb"

    public struct Draft: Sendable {
        public var kind: Kind = .correction
        public var city = ""
        public var tree = ""
        public var locationHint = ""
        public var why = ""
        public init() {}
    }

    /// Sends it, or says plainly that it did not go. No name field: we never
    /// publish a submitter's name and asking for one we will not use is worse
    /// than not asking. Sending needs the signed-in account (2026-08-21, the
    /// Google Maps convention): the token stamps the row with the sender, and
    /// the account's email is how the thank-you and the answer reach them.
    public static func send(_ d: Draft, from page: String?, token: String?) async -> Bool {
        await post([
            "kind": d.kind.rawValue,
            "city": d.city,
            "tree": d.tree,
            "location_hint": d.locationHint,
            "why": d.why,
            "page": page as Any,
        ], token: token)
    }

    /// The worth-it control's channel: kind 'feedback', same shape as the
    /// web control's rows, so the pipeline cannot tell the surfaces apart.
    public static func sendFeedback(city: String, tree: String, why: String,
                                    token: String?) async -> Bool {
        await post([
            "kind": "feedback",
            "city": city,
            "tree": tree,
            "why": why,
            "page": "app" as Any,
        ], token: token)
    }

    private static func post(_ body: [String: Any], token: String?) async -> Bool {
        var r = URLRequest(url: url)
        r.httpMethod = "POST"
        r.setValue(key, forHTTPHeaderField: "apikey")
        if let token { r.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization") }
        r.setValue("application/json", forHTTPHeaderField: "Content-Type")
        r.setValue("return=minimal", forHTTPHeaderField: "Prefer")
        r.httpBody = try? JSONSerialization.data(withJSONObject: body)
        guard let (_, resp) = try? await URLSession.shared.data(for: r),
              let http = resp as? HTTPURLResponse else { return false }
        return (200..<300).contains(http.statusCode)
    }
}
