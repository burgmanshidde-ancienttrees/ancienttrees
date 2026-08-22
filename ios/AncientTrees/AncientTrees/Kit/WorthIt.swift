// "Worth the visit?" on the app, born with the toggle design the web control
// got the same day (Hidde, 2026-08-21): press selects and counts, press again
// undoes, a down-vote offers the optional why-chips. Same Supabase rows as
// the web control, so the pipeline behind it cannot tell the surfaces apart.
// Undo writes a compensating "vote undone" row rather than deleting anything.
// And gated the same way as the web control, same day's ruling: the options
// are visible to everyone, acting opens the sign-in sheet, because the
// account is the reply channel (the Google Maps convention).
import SwiftUI

struct WorthItView: View {
    let tree: Tree

    @Environment(Account.self) private var account
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

    init(tree: Tree) {
        self.tree = tree
        _vote = AppStorage(wrappedValue: "", "at_worthit_\(tree.id)")
        _reported = State(initialValue:
            UserDefaults.standard.string(forKey: "at_wrong_\(tree.id)") != nil)
        _detailSent = State(initialValue:
            UserDefaults.standard.bool(forKey: "at_wrong_detail_\(tree.id)"))
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack(spacing: 10) {
                Text("Been here? Worth the visit?")
                    .font(.subheadline.weight(.semibold))
                thumb("up", "hand.thumbsup")
                thumb("down", "hand.thumbsdown")
            }
            if !vote.isEmpty {
                Text("Thanks, counted. Tap again to undo.")
                    .font(.footnote).foregroundStyle(.secondary)
            }
            if whyOpen && !reported {
                Text("Care to say why? (optional)")
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

    private func thumb(_ dir: String, _ icon: String) -> some View {
        Button {
            // Visible to everyone; voting needs the account that lets us
            // answer (2026-08-21, the Google Maps convention).
            guard account.isSignedIn else { signingIn = true; return }
            if vote == dir {
                send("vote undone", vote == "up" ? "worth it" : "not worth it")
                vote = ""
                whyOpen = false
                return
            }
            if !vote.isEmpty {
                send("vote undone", vote == "up" ? "worth it" : "not worth it")
            }
            vote = dir
            send(dir == "up" ? "worth it" : "not worth it", nil)
            whyOpen = (dir == "down")
        } label: {
            Image(systemName: vote == dir ? icon + ".fill" : icon)
                .frame(minWidth: 44, minHeight: 44)
        }
        .buttonStyle(.bordered)
        .tint(vote == dir ? Brand.moss : .secondary)
        .accessibilityLabel(dir == "up"
            ? "Yes, \(tree.name) was worth the visit"
            : "No, \(tree.name) was not worth the visit")
        .accessibilityAddTraits(vote == dir ? .isSelected : [])
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

    private func send(_ verdict: String, _ reason: String?) {
        let why = reason.map { "\(verdict): \($0)" } ?? verdict
        let token = account.session?.accessToken
        Task {
            _ = await Submission.sendFeedback(city: tree.city,
                                              tree: "\(tree.id) (\(tree.name))",
                                              why: why,
                                              token: token)
        }
    }
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
