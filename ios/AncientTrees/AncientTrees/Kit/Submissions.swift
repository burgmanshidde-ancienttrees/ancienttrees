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
        case tree, city, correction, feedback
        public var id: String { rawValue }
        public var label: String {
            switch self {
            case .tree: "A tree we are missing"
            case .city: "A place we should map"
            case .correction: "Report a problem"
            case .feedback: "An idea for the app"
            }
        }
    }

    /// The project and the key live on Supa; this is just the table.
    static let path = "/rest/v1/submissions"

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

    /// A TREE YOU SENT US THROUGH THE FORM, read back.
    ///
    /// The app's camera writes to `sightings` and the website's form writes
    /// here, and for a long time only the first of the two came back to
    /// anybody. The website fixed its half on 2026-09-23, after the first
    /// contributor from outside sent one oak fourteen times: the thank-you
    /// mail tells people to look at their account, and what they had sent was
    /// in a table nothing read. This is the same fix on this surface, because
    /// a person who types a tree on a laptop and opens the app the next day is
    /// one person.
    ///
    /// RLS does the access control: the policy on submissions is
    /// `auth.uid() = user_id` (supabase/own-data.sql) and there is none for
    /// anybody else, so this returns your rows and nobody else's.
    public struct Sent: Identifiable, Sendable, Hashable {
        public var id: Int
        public var tree: String
        public var city: String
        public var outcome: String?
        public var reply: String?
        public var sentAt: Date?
        /// How many times this same tree was sent. There is no way to edit a
        /// tip, so refining one means sending it again, and a row each would
        /// read as a tree each.
        public var times: Int = 1

        /// The app's own vocabulary, so one state is never described in two
        /// ways across the two surfaces.
        var status: Sightings.Status {
            switch outcome {
            case "changed": .published
            case "holds", "open_question": .checking
            default: .sent
            }
        }

        public var title: String { tree.isEmpty ? city : tree }
    }

    /// Yours, newest first, one entry per tree rather than per row.
    public static func mine(token: String?) async -> [Sent] {
        guard let token else { return [] }
        // NOT the rows this app writes beside a sighting of its own. Adding
        // a tree here posts a submissions row carrying the sighting's uuid
        // (CollectSheet.swift, from: "app:collect"), and the sighting is
        // already the record of that tree, so counting the row as well puts
        // one tree on the lane twice.
        let rows = await Supa.rows(path + "?select=id,kind,city,tree,outcome,"
                                   + "reply_text,created_at,page&kind=in.(tree,city)"
                                   + "&order=created_at.desc", token: token)
        let iso = ISO8601DateFormatter()
        iso.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
        var order: [String] = []
        var byKey: [String: Sent] = [:]
        for row in rows {
            if ((row["page"] as? String) ?? "").hasPrefix("app") { continue }
            let tree = (row["tree"] as? String) ?? ""
            let city = (row["city"] as? String) ?? ""
            let key = (tree + "|" + city).lowercased()
                .filter { $0.isLetter || $0.isNumber || $0 == "|" }
            let outcome = row["outcome"] as? String
            if var have = byKey[key] {
                have.times += 1
                // The only outcome we ever set is on one row, so an answered
                // tip keeps its answer whichever row we answered.
                if have.outcome == nil, outcome != nil {
                    have.outcome = outcome
                    have.reply = row["reply_text"] as? String
                }
                byKey[key] = have
                continue
            }
            order.append(key)
            byKey[key] = Sent(id: (row["id"] as? Int) ?? 0,
                              tree: tree, city: city, outcome: outcome,
                              reply: row["reply_text"] as? String,
                              sentAt: (row["created_at"] as? String).flatMap { iso.date(from: $0) })
        }
        return order.compactMap { byKey[$0] }
    }

    private static func post(_ body: [String: Any], token: String?) async -> Bool {
        // No token is not an error here: a submission is accepted on the
        // publishable key, and Supa.request falls back to it.
        await Supa.post(path, token: token, body: body, prefer: "return=minimal")
    }
}
