import SwiftUI

struct ContributeView: View {
    /// Prefilled when it is opened from a tree, which is the case that matters:
    /// somebody standing at a pin that is wrong.
    var about: Tree?

    @Environment(\.dismiss) private var dismiss
    @Environment(Account.self) private var account
    @State private var draft = Submission.Draft()
    @State private var sending = false
    @State private var sent = false
    @State private var failed = false
    @State private var signingIn = false

    var body: some View {
        NavigationStack {
            Form {
                if sent {
                    Section {
                        Label("Thank you", systemImage: "checkmark.seal.fill")
                            .font(.headline)
                        Text("Everything sent in is checked against independent sources before it goes live, and a wrong pin gets looked at the same day. You will hear what your tip changed.")
                            .font(.footnote).foregroundStyle(.secondary)
                    }
                } else {
                    Section {
                        Picker("This is", selection: $draft.kind) {
                            ForEach(Submission.Kind.allCases) { k in
                                Text(k.label).tag(k)
                            }
                        }
                    }
                    Section("Where") {
                        TextField("Place or city", text: $draft.city)
                        TextField("Which tree", text: $draft.tree)
                        TextField("Where exactly, if you can say", text: $draft.locationHint)
                    }
                    Section {
                        TextField("What should we know?", text: $draft.why, axis: .vertical)
                            .lineLimit(4...10)
                    } footer: {
                        Text("We never publish your name, and we do not ask for it.")
                    }
                    Section {
                        // Visible to everyone; sending needs the account that
                        // lets us answer (2026-08-21, the Google Maps
                        // convention: the account is the reply channel).
                        Button {
                            guard account.isSignedIn else { signingIn = true; return }
                            Task {
                                sending = true
                                let ok = await Submission.send(draft, from: about?.url,
                                                               token: account.session?.accessToken)
                                sending = false
                                if ok { sent = true } else { failed = true }
                            }
                        } label: {
                            HStack {
                                if sending { ProgressView().padding(.trailing, 6) }
                                Text(sending ? "Sending" : "Send")
                            }
                            .frame(maxWidth: .infinity)
                        }
                        .disabled(sending || draft.why.isEmpty)
                        if failed {
                            Text("That did not go through. Try again in a moment.")
                                .font(.footnote).foregroundStyle(.red)
                        }
                    } footer: {
                        if !account.isSignedIn {
                            Text("Sending needs a free account, one email and no password, so we can thank you, ask a question if we need to, and tell you what your tip changed.")
                        }
                    }
                }
            }
            .navigationTitle(sent ? "Sent" : "Tell us")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button(sent ? "Done" : "Cancel") { dismiss() }
                }
            }
            .task {
                if let t = about {
                    draft.city = t.city
                    draft.tree = t.name
                }
            }
            .sheet(isPresented: $signingIn) {
                SignInSheet(reason: .feedback, localCount: 0)
            }
        }
    }
}
