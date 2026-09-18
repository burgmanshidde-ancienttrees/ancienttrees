// "Worth the visit?" on the app, born with the toggle design the web control
// got the same day (Hidde, 2026-08-21): press selects and counts, press again
// undoes, a down-vote offers the optional why-chips. Same Supabase rows as
// the web control, so the pipeline behind it cannot tell the surfaces apart.
// Undo writes a compensating "vote undone" row rather than deleting anything.
// And gated the same way as the web control, same day's ruling: the options
// are visible to everyone, acting opens the sign-in sheet, because the
// account is the reply channel (the Google Maps convention).
import SwiftUI

/// Which trees this account has already voted on, read from the account rather
/// than from this phone.
///
/// The vote itself has always gone to the server; what lived only on the device
/// was the memory of having cast it, so a new phone showed every tree unvoted
/// and let the same person say the same thing twice. Hidde, 2026-08-27: "niks
/// moet lokaal opgeslagen zijn."
///
/// Read once at launch, because it is one small request and the alternative is
/// one per tree page.
@MainActor
@Observable
final class MyVotes {
    private(set) var byTree: [String: String] = [:]
    /// The trees this account has already reported something about, and the
    /// ones it also typed a detail for. The website has read these out of the
    /// same rows since the chips were built; the app only ever remembered them
    /// on the phone that tapped them, so a second phone offered the report
    /// again as though nothing had been said (2026-09-11).
    /// Keyed by tree rather than a bare set, because the report's REASON picks
    /// the follow-up question and that reason lives in the row's `why` too.
    private(set) var reports: [String: String] = [:]
    private(set) var detailed: Set<String> = []

    // WHAT A VIEW ASKS. Until 2026-09-18 every one of them asked UserDefaults
    // instead, off a mirror written at launch, which is the shape Hidde has
    // now ruled against three times ("niks moet lokaal opgeslagen zijn",
    // 2026-08-27; "alles wat wordt opgeslagen moet op je account zijn",
    // 2026-09-02; "stop saving stuff locally anywhere", 2026-09-18). A mirror
    // is a second source of truth: nothing cleared those keys on sign-out, so
    // a signed-out phone still showed the last person's votes, and a key
    // written per tree could never be enumerated to clear them.
    func vote(_ treeId: String) -> String { byTree[treeId] ?? "" }
    func hasReported(_ treeId: String) -> Bool { reports[treeId] != nil }
    func reason(_ treeId: String) -> String { reports[treeId] ?? "" }
    func hasDetailed(_ treeId: String) -> Bool { detailed.contains(treeId) }

    /// Painted at once and sent straight after, the same way the heart works:
    /// the account decides, the screen only reports. A failed send is corrected
    /// by the next launch, which reloads from the account.
    func setVote(_ treeId: String, _ value: String) {
        if value.isEmpty { byTree[treeId] = nil } else { byTree[treeId] = value }
    }
    func markReported(_ treeId: String, reason: String) { reports[treeId] = reason }
    func markDetailed(_ treeId: String) { detailed.insert(treeId) }

    /// Signing out takes them off the screen, exactly as it takes the
    /// collection off (CONVENTIONS.md, "What signing out takes with it"). They
    /// live in the account and come straight back on the next sign-in.
    func forgetLocally() { byTree = [:]; reports = [:]; detailed = [] }

    /// Take the old per-tree keys off phones that already carry them.
    ///
    /// Unconditional rather than behind a migration flag, and idempotent: it
    /// costs one pass over UserDefaults at launch, nothing writes these any
    /// more, and a flag would be one more thing stored on the device to track
    /// a thing being removed from the device. They cannot be enumerated any
    /// other way, which is half of why keys built per tree were the wrong
    /// shape to begin with.
    static func clearTheOldMirror() {
        let d = UserDefaults.standard
        for key in d.dictionaryRepresentation().keys
        where key.hasPrefix("at_worthit_") || key.hasPrefix("at_wrong_") {
            d.removeObject(forKey: key)
        }
    }

    /// The `tree` column is written as "id (name)" by both surfaces, and what
    /// every view asks about is the BARE id. Keying on the whole string meant
    /// a vote cast on one phone never appeared on another however faithfully
    /// it was stored, because it was filed under "kyo_016 (Sudajii of Omiya
    /// Gate, Kyoto Gyoen)" and looked up under "kyo_016".
    static func treeId(_ field: String) -> String {
        String(field.split(separator: " ", maxSplits: 1)[0])
    }

    func load(account: Account) async {
        guard let token = await account.freshToken() else {
            forgetLocally(); return
        }
        // OLDEST FIRST, because the loop below lets the last row on a tree win
        // and an undo only works if it arrives after the vote it cancels. The
        // order used to be whatever PostgREST felt like returning.
        let r = Supa.request("/rest/v1/submissions?select=tree,kind,why&kind=eq.feedback"
                             + "&order=created_at.asc", method: "GET", token: token)
        guard let (data, _) = try? await Net.data(for: r),
              let rows = try? JSONSerialization.jsonObject(with: data) as? [[String: Any]]
        else { return }
        var found: [String: String] = [:]
        var said: [String: String] = [:], saidMore: Set<String> = []
        for row in rows {
            guard let field = row["tree"] as? String, let why = row["why"] as? String else { continue }
            let tree = Self.treeId(field)
            // A REPORT IS NOT A VOTE. Everything that was not "worth it" used
            // to be read back as a thumb down, so reporting a wrong pin left
            // the tree looking voted on the next launch, on a page whose thumb
            // down was removed on 2026-09-04.
            if why.hasPrefix("report detail") { saidMore.insert(tree); continue }
            if why.hasPrefix("report") {
                // "report: wrong location" -> "wrong location", which is the
                // key the follow-up question is looked up under.
                said[tree] = why.contains(": ")
                    ? String(why.split(separator: ":", maxSplits: 1)[1])
                        .trimmingCharacters(in: .whitespaces)
                    : ""
                continue
            }
            // An undo is a compensating row rather than a deletion, so the
            // last word on a tree is the one that counts.
            if why.hasPrefix("vote undone") { found[tree] = nil }
            // MATCHED WHOLE, never by contains: "not worth it" contains
            // "worth it", so the payoff screen's thumbs DOWN came back as a
            // green thumbs up on the tree page at the next launch. Found while
            // moving these views off the device (2026-09-18); it could not
            // have been found before, because nothing ever read this value
            // back into the control that draws it.
            else if why == "worth it" { found[tree] = "up" }
            else if why == "not worth it" { found[tree] = "down" }
        }
        byTree = found
        reports = said
        detailed = saidMore
    }
}

struct WorthItView: View {
    let tree: Tree

    @Environment(Account.self) private var account
    @Environment(VoteCounts.self) private var counts
    @Environment(MyVotes.self) private var votes
    @State private var whyOpen = false
    @State private var detail = ""
    @State private var signingIn = false

    private var reported: Bool { votes.hasReported(tree.id) }
    private var detailSent: Bool { votes.hasDetailed(tree.id) }

    /// The one question whose answer lets a run close the case, per reason
    /// (Hidde, 2026-08-21: "i want them to tell us which of the two elms it
    /// is"). Asked inline, never by sending people to the form.
    private static let asks: [String: (String, String)] = [
        "dead or gone": ("What did you find there? (optional)",
                         "A stump, a fallen trunk, or nothing at all, and when you were there"),
        "wrong location": ("Where is it really? (optional)",
                           "A street corner, a landmark, or a maps pin"),
        "could not tell which tree": ("Which one did you look at? (optional)",
                                      "The thicker trunk, the one nearest the path, by the bench"),
        "could not reach it": ("What stopped you? (optional)",
                               "A locked gate, a fence, opening hours, private land"),
        "something else": ("Tell us in a line.",
                           "What we got wrong, or what we are missing"),
    ]

    /// Only the report entry lives here now. The vote is the compact thumb
    /// beside the place name (WorthItButton), since 2026-09-04, and the
    /// "Been here? Worth the visit?" heading that used to open this block went
    /// dead that day behind a switch nobody set; removed 2026-09-11 when the
    /// parity check caught it still sitting in the source.

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            if !reported {
                // ITS OWN ENTRY, never nested under the vote (2026-08-16:
                // "je kunt een boom niet leuk vinden of niet de moeite vinden
                // zonder dat er iets mis is"). With the thumbs down gone this
                // is the only way in, which is what the website has done all
                // along.
                Button { whyOpen.toggle() } label: {
                    Text("Something's wrong")
                        .font(.footnote.weight(.semibold))
                        .foregroundStyle(Brand.inkSoft)
                        .underline()
                        .frame(minHeight: 44)
                        .contentShape(.rect)
                }
                .buttonStyle(.plain)
                .accessibilityIdentifier("worthit-report")
            }
            if whyOpen && !reported {
                Text("What's wrong? (optional)")
                    .font(.footnote.weight(.semibold))
                chipRow
            }
            if reported {
                Text(detailSent ? "Thanks, that helps." : "Thanks, we'll check it.")
                    .font(.footnote).foregroundStyle(.secondary)
                if !detailSent, let ask = Self.asks[reason] {
                    Text(ask.0).font(.footnote.weight(.semibold))
                    TextField(ask.1, text: $detail, axis: .vertical)
                        .lineLimit(2...4)
                        .textFieldStyle(.roundedBorder)
                    Button("Send") {
                        guard account.isSignedIn else { signingIn = true; return }
                        let text = detail.trimmingCharacters(in: .whitespacesAndNewlines)
                        guard !text.isEmpty else { return }
                        send("report detail", String(text.prefix(1000)))
                        votes.markDetailed(tree.id)
                    }
                    .buttonStyle(.bordered).controlSize(.small)
                    .disabled(detail.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                }
            }
        }
        .sheet(isPresented: $signingIn) {
            SignInSheet(reason: .feedback, localCount: 0)
        }
    }

    private var chipRow: some View {
        FlowChips {
            chip("It's dead or gone", "dead or gone")
            chip("Wrong location", "wrong location")
            chip("Couldn't tell which tree", "could not tell which tree")
            chip("Couldn't reach it", "could not reach it")
            chip("Something else", "something else")
        }
    }

    private var reason: String { votes.reason(tree.id) }

    private func chip(_ label: String, _ reason: String) -> some View {
        Button(label) {
            guard account.isSignedIn else { signingIn = true; return }
            votes.markReported(tree.id, reason: reason)
            whyOpen = false
            send("report", reason)
        }
        .buttonStyle(.bordered).controlSize(.small)
    }

    /// A TOKEN THAT IS STILL GOOD, asked for inside the Task rather than read
    /// out of the session here.
    ///
    /// This read `session?.accessToken` straight, and those live an hour, so
    /// every vote and every report from anybody signed in longer than that came
    /// back 401 and vanished. The control still filled in, because it does not
    /// wait for the answer, so there was nothing to see: the thumb went green
    /// and the row never arrived. That is the same bug ProfileEditor had with
    /// the profile picture and the launch task had with the profile itself, and
    /// this was the third copy of it.
    ///
    /// Worse than sending nothing, which is why it is not merely untidy: a
    /// submission is accepted on the publishable key, so `nil` would have
    /// worked. An EXPIRED bearer makes PostgREST refuse the whole call.
    private func send(_ verdict: String, _ reason: String?) {
        let why = reason.map { "\(verdict): \($0)" } ?? verdict
        Task {
            _ = await Submission.sendFeedback(city: tree.city,
                                              tree: "\(tree.id) (\(tree.name))",
                                              why: why,
                                              token: await account.freshToken())
        }
    }
}

/// THE ONE VOTE, drawn twice on a tree page and always in step, because both
/// copies read the same MyVotes, which is the account's own answer.
///
/// One direction only (Hidde, 2026-09-04: "i agree that we dont need a thumb
/// down"). Every reference offers a single positive act and routes the
/// negative to a report: Strava's kudos, Instagram's like, Reddit's upvote,
/// YouTube's like. This page already carries the negative twice, in the
/// toolbar's report menu and in the chips under this control.
///
/// The number sits ON the control, which is the other half of the same
/// convention and the answer to Hidde's question ("how does someone add a
/// thumb up by clicking the 17"): nobody anywhere draws a count that is only a
/// count beside a separate button that casts. So the small one in the summary
/// line is not a label, it is this button.
struct WorthItButton: View {
    let tree: Tree
    /// The small one, for the line under the name.
    var compact = false

    @Environment(Account.self) private var account
    @Environment(VoteCounts.self) private var counts
    @Environment(MyVotes.self) private var votes
    @State private var signingIn = false

    private var vote: String { votes.vote(tree.id) }
    private var cast: Bool { vote == "up" }

    var body: some View {
        Button(action: tap) {
            HStack(spacing: compact ? 4 : 6) {
                Image(systemName: cast ? "hand.thumbsup.fill" : "hand.thumbsup")
                    .font(.system(size: compact ? 13 : 16, weight: .semibold))
                if let n = counts.up(tree.id) {
                    Text("\(n)")
                        .font(compact ? .subheadline : .brand(15, .semibold, relativeTo: .subheadline))
                        .monospacedDigit()
                        .underline(compact)
                }
            }
            .foregroundStyle(cast ? Brand.moss : (compact ? Brand.ink : Brand.ink))
            .modifier(WorthItShape(compact: compact, cast: cast))
        }
        .buttonStyle(.plain)
        .accessibilityIdentifier(compact ? "worthit-count" : "worthit-button")
        .accessibilityLabel(cast
            ? "You found \(tree.name) worth the visit. Tap to undo"
            : "Yes, \(tree.name) was worth the visit")
        .accessibilityAddTraits(cast ? .isSelected : [])
        .sheet(isPresented: $signingIn) {
            SignInSheet(reason: .feedback, localCount: 0)
        }
    }

    private func tap() {
        // Visible to everyone; voting needs the account that lets us answer
        // (2026-08-21, the Google Maps convention).
        guard account.isSignedIn else { signingIn = true; return }
        if cast {
            send("vote undone", "worth it")
            counts.record(tree.id, from: "up", to: "")
            votes.setVote(tree.id, "")
            return
        }
        counts.record(tree.id, from: vote, to: "up")
        votes.setVote(tree.id, "up")
        send("worth it", nil)
    }

    private func send(_ verdict: String, _ reason: String?) {
        let why = reason.map { "\(verdict): \($0)" } ?? verdict
        Task {
            _ = await Submission.sendFeedback(city: tree.city,
                                              tree: "\(tree.id) (\(tree.name))",
                                              why: why,
                                              token: await account.freshToken())
        }
    }
}

/// A capsule after the story, plain text in the summary line. The tap target
/// stays 44 points in both, which is the whole reason the small one is
/// allowed to be small.
private struct WorthItShape: ViewModifier {
    let compact: Bool
    let cast: Bool

    func body(content: Content) -> some View {
        if compact {
            // LEADING, so the glyph sits a normal gap after the dot beside the
            // place name and the 44-point target runs to the right of it.
            // Centred, a 13-point thumb in a 44-point frame left twice the gap
            // after the dot that stood before it (Hidde, 2026-09-11: "de
            // spacing van de duim opeens heel raar").
            content.frame(minWidth: 44, minHeight: 44, alignment: .leading)
                .contentShape(.rect)
        } else {
            content
                .padding(.horizontal, 14)
                .frame(height: 44)
                .background(cast ? Brand.moss.opacity(0.12) : Brand.surface,
                            in: .capsule)
                .overlay { Capsule().strokeBorder(Brand.hairline, lineWidth: 1) }
        }
    }
}

/// The count under the name. Same button, small.
struct WorthItCount: View {
    let tree: Tree
    var body: some View { WorthItButton(tree: tree, compact: true) }
}

/// A wrapping row for the chips, so they fit a 375 point screen.
struct FlowChips<Content: View>: View {
    @ViewBuilder var content: Content
    var body: some View {
        ViewThatFits(in: .horizontal) {
            HStack(spacing: 6) { content }
            VStack(alignment: .leading, spacing: 6) { content }
        }
    }
}


/// WAS IT WORTH THE TRIP? Asked once, at the end of the flow, only about a
/// tree we already map.
///
/// Hidde, 2026-09-08: "zou ik de flow willen eindigen met de vraag was het
/// worth the trip met thumbs up en down (gelinkt aan de thumbs up die we al
/// hebben) zodat we langzaam leren of bomen echt de moeite zijn."
///
/// THE DOWN THUMB IS BACK HERE AND ONLY HERE, and that is not a reversal of
/// his 2026-09-04 ruling that removed it. He drew the line himself the same
/// day he asked for this: "ik wilde duim naar beneden weg op de boom pagina
/// maar in deze flow is die bruikbaar - het is info voor ons niet voor de
/// gebruiker. Thumbs up tonen we wel." On a tree PAGE a thumbs-down is
/// ambiguous, because somebody browsing has not been and "not worth it" and
/// "something is wrong" get confused, which is why that page routes the
/// negative to a report. Here the person has just stood in front of it, so the
/// answer is unambiguous, and it is the only moment we can ever ask it
/// honestly. What does not change: the up is public and the down is ours.
///
/// CONVENTION (CONVENTIONS.md 2026-09-08). AllTrails prompts for a rating
/// after a recorded activity, and only when the activity attaches to a
/// verified trail and you have not rated it recently; Google Maps asks "How
/// was X? Help others know what to expect" after the visit rather than during
/// it; Apple's HIG says to ask at a natural pause, never mid-task, and warns
/// that repeated asks turn people against the app. So: on the payoff screen,
/// inline rather than modal, no dismiss button because not answering IS the
/// dismissal, and never shown twice for the same tree.
struct WorthTheTripAsk: View {
    let tree: Tree

    @Environment(Account.self) private var account
    @Environment(VoteCounts.self) private var counts
    @Environment(MyVotes.self) private var votes
    @State private var signingIn = false

    private var vote: String { votes.vote(tree.id) }

    var body: some View {
        Group {
            if vote.isEmpty {
                VStack(alignment: .leading, spacing: 10) {
                    Text("Was it worth the trip?")
                        .font(.subheadline.weight(.semibold))
                        .foregroundStyle(Brand.ink)
                    HStack(spacing: 10) {
                        thumb("hand.thumbsup", "up", "Yes, worth the trip")
                        thumb("hand.thumbsdown", "down", "No, not worth the trip")
                    }
                }
                .accessibilityIdentifier("worth-the-trip")
            } else {
                // Acknowledged where it happened rather than by a toast, which
                // leaves no trace for somebody coming back (CONVENTIONS.md,
                // landing after you have added something). No thanks-for-the-
                // negative variant: the same line either way, because a
                // different one would read as us minding.
                Text("Noted, that helps.")
                    .font(.footnote)
                    .foregroundStyle(Brand.inkSoft)
            }
        }
        .sheet(isPresented: $signingIn) { SignInSheet(reason: .feedback, localCount: 0) }
    }

    private func thumb(_ icon: String, _ value: String, _ label: String) -> some View {
        Button {
            guard account.isSignedIn else { signingIn = true; return }
            votes.setVote(tree.id, value)
            if value == "up" { counts.record(tree.id, from: "", to: "up") }
            let why = value == "up" ? "worth it" : "not worth it"
            Task {
                _ = await Submission.sendFeedback(city: tree.city,
                                                  tree: "\(tree.id) (\(tree.name))",
                                                  why: why,
                                                  token: await account.freshToken())
            }
        } label: {
            Image(systemName: icon)
                .font(.system(size: 20, weight: .semibold))
                .frame(width: 64, height: 44)
                .background(Brand.surfaceMuted, in: .rect(cornerRadius: 12))
                .foregroundStyle(Brand.ink)
        }
        .buttonStyle(.plain)
        .accessibilityLabel(label)
        .accessibilityIdentifier("worth-the-trip-\(value)")
    }
}
