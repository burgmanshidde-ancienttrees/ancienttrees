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

    func load(account: Account) async {
        guard let token = await account.freshToken() else { byTree = [:]; return }
        let r = Supa.request("/rest/v1/submissions?select=tree,kind,why&kind=eq.feedback",
                             method: "GET", token: token)
        guard let (data, _) = try? await Net.data(for: r),
              let rows = try? JSONSerialization.jsonObject(with: data) as? [[String: Any]]
        else { return }
        var found: [String: String] = [:]
        for row in rows {
            guard let tree = row["tree"] as? String, let why = row["why"] as? String else { continue }
            // An undo is a compensating row rather than a deletion, so the
            // last word on a tree is the one that counts.
            if why.hasPrefix("vote undone") { found[tree] = nil }
            else if why.contains("worth it") { found[tree] = "up" }
            else { found[tree] = "down" }
        }
        byTree = found
    }
}

struct WorthItView: View {
    let tree: Tree

    @Environment(Account.self) private var account
    @Environment(VoteCounts.self) private var counts
    @AppStorage private var vote: String
    @State private var whyOpen = false
    @State private var reported: Bool
    @State private var detail = ""
    @State private var detailSent: Bool
    @State private var signingIn = false

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

    init(tree: Tree, showsVote: Bool = true) {
        self.tree = tree
        self.showsVote = showsVote
        _vote = AppStorage(wrappedValue: "", "at_worthit_\(tree.id)")
        _reported = State(initialValue:
            UserDefaults.standard.string(forKey: "at_wrong_\(tree.id)") != nil)
        _detailSent = State(initialValue:
            UserDefaults.standard.bool(forKey: "at_wrong_detail_\(tree.id)"))
    }

    /// THE VOTE LEFT THIS BLOCK (Hidde, 2026-09-04: "de worth the visit tekst
    /// mag helemaal weg, zet die thumb omhoog gewoon naast de stadsnaam zoals
    /// ontworpen en dat je hem kan aanklikken om er een toe te voegen").
    ///
    /// The thumb is now the compact button in the line under the tree's name,
    /// where it is a control rather than a question, and the question itself is
    /// gone: a heading that asks whether you have been here is a sentence spent
    /// on a thing the thumb says by being a thumb. What is left here is the
    /// report entry, which he asked to keep and to put lower down.
    var showsVote: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            if showsVote {
                HStack(spacing: 10) {
                    Text("Been here? Worth the visit?")
                        .font(.subheadline.weight(.semibold))
                    Spacer(minLength: 0)
                    WorthItButton(tree: tree)
                }
            }
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
                        UserDefaults.standard.set(true, forKey: "at_wrong_detail_\(tree.id)")
                        detailSent = true
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

    private var reason: String {
        UserDefaults.standard.string(forKey: "at_wrong_\(tree.id)") ?? ""
    }

    private func chip(_ label: String, _ reason: String) -> some View {
        Button(label) {
            guard account.isSignedIn else { signingIn = true; return }
            UserDefaults.standard.set(reason, forKey: "at_wrong_\(tree.id)")
            reported = true
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
/// copies read the same `at_worthit_<id>` key.
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
    @AppStorage private var vote: String
    @State private var signingIn = false

    init(tree: Tree, compact: Bool = false) {
        self.tree = tree
        self.compact = compact
        _vote = AppStorage(wrappedValue: "", "at_worthit_\(tree.id)")
    }

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
            vote = ""
            return
        }
        counts.record(tree.id, from: vote, to: "up")
        vote = "up"
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
            content.frame(minHeight: 44).contentShape(.rect)
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
