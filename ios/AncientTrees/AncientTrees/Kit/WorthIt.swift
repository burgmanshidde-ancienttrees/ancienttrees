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
    @State private var showForm = false
    @State private var signingIn = false

    init(tree: Tree) {
        self.tree = tree
        _vote = AppStorage(wrappedValue: "", "at_worthit_\(tree.id)")
        _reported = State(initialValue:
            UserDefaults.standard.string(forKey: "at_wrong_\(tree.id)") != nil)
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
        }
        .sheet(isPresented: $showForm) { ContributeView(about: tree) }
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
            chip("Couldn't reach it", "could not reach it")
            Button("Something else") { showForm = true }
                .buttonStyle(.bordered).controlSize(.small)
        }
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
