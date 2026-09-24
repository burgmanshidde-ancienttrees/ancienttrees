import SwiftUI

struct ContributeView: View {
    /// Prefilled when it is opened from a tree, which is the case that matters:
    /// somebody standing at a pin that is wrong.
    var about: Tree?
    /// What they picked from the tree page's menu, seeded into `why` so the
    /// report says what kind of wrong it is without them typing a category.
    /// They can delete it; it is an opening line, not a label we impose.
    var opening: String?
    /// The Profile's feedback button (Hidde, 2026-08-26: a general feedback
    /// channel, "vertel ons welke features je zou willen toevoegen"). Same
    /// form, same pipeline, kind `feedback`; the picker and the Where fields
    /// disappear because there is no tree and no place, only the idea.
    var feedbackMode = false

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
                    // THE ACCOUNT IS ASKED FOR BEFORE THE TYPING (2026-09-24).
                    // Hidde, about the website and true here word for word:
                    // the person should be sent to sign in and told that they
                    // have to, in the flow rather than afterwards. This same
                    // sentence sat in a Section footer UNDER the send button,
                    // which is read after six fields, if at all.
                    //
                    // Google Maps will not show a signed-out person the
                    // Contribute tab at all and iNaturalist asks you to sign
                    // up before it hands you the observation form
                    // (CONVENTIONS.md, "Contributing when you are not signed
                    // in"). We keep the softer gate our own 2026-08-21 ruling
                    // chose, the form visible to anybody, and move the
                    // sentence to where it is met first.
                    if !account.isSignedIn {
                        Section {
                            Text("Sending needs a free account. It is how we thank you, ask a question if we need one, and tell you what your tip changed.")
                                .font(.footnote).foregroundStyle(Brand.inkSoft)
                            Button("Sign in") { signingIn = true }
                                .font(.callout.weight(.semibold))
                        }
                    }
                    // OPENED FROM A TREE: no picker and no blank Where. We
                    // know which tree, the kind is a correction by definition,
                    // and asking the two questions we can already answer is
                    // what made this read as the wrong screen (Hidde,
                    // 2026-08-25). Only the one field we cannot fill stays:
                    // where the tree really is.
                    if let t = about {
                        Section {
                            VStack(alignment: .leading, spacing: 3) {
                                Text(t.name).font(.callout.weight(.semibold))
                                Text(t.city).font(.footnote).foregroundStyle(.secondary)
                            }
                        } header: {
                            Text("About this tree")
                        }
                        Section {
                            TextField("Where is it really, if you can say",
                                      text: $draft.locationHint)
                        }
                    } else if !feedbackMode {
                        Section {
                            // Three choices as three rows with a tick, the way
                            // Settings lists a short choice. The menu style drew
                            // a 34 point button inside a 44 point row, and the
                            // layout gate measured the button.
                            Picker("This is", selection: $draft.kind) {
                                ForEach(Submission.Kind.allCases) { k in
                                    Text(k.label).tag(k)
                                }
                            }
                            .pickerStyle(.inline)
                            .labelsHidden()
                        }
                        Section("Where") {
                            TextField("Place or city", text: $draft.city)
                            TextField("Which tree", text: $draft.tree)
                            TextField("Where exactly, if you can say", text: $draft.locationHint)
                        }
                    }
                    Section {
                        TextField(feedbackMode ? "A feature you would like, or anything else"
                                               : "What should we know?",
                                  text: $draft.why, axis: .vertical)
                            .lineLimit(4...10)
                    } header: {
                        if feedbackMode { Text("Tell us what you would like") }
                    } footer: {
                        // Not "we never publish your name": the display name
                        // somebody chooses on their profile is shown beside a
                        // follow, so as a blanket promise that stopped being
                        // true when profiles arrived. What is true, and is the
                        // thing they are actually asking, is that nobody sees
                        // who sent THIS.
                        Text("Nobody else sees who sent this, and we do not ask for your name.")
                    }
                    Section {
                        // Visible to everyone; sending needs the account that
                        // lets us answer (2026-08-21, the Google Maps
                        // convention: the account is the reply channel).
                        Button {
                            guard account.isSignedIn else { signingIn = true; return }
                            Task {
                                sending = true
                                let ok = await Submission.send(draft, from: about?.url ?? (feedbackMode ? "app-profile" : nil),
                                                               token: await account.freshToken())
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
                    }
                }
            }
            .accessibilityElement(children: .contain)
            .accessibilityIdentifier("contribute-sheet")
            .navigationTitle(sent ? "Sent" : feedbackMode ? "Feedback" : "Tell us")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button(sent ? "Done" : "Cancel") { dismiss() }
                }
            }
            .task {
                if feedbackMode { draft.kind = .feedback }
                if let t = about {
                    draft.city = t.city
                    draft.tree = t.name
                    // A report about a tree we already publish is a correction,
                    // never an offer of a tree we are missing. It was already
                    // the default; setting it here means the screen and the row
                    // it sends cannot drift apart when that default changes.
                    draft.kind = .correction
                }
                if let opening, draft.why.isEmpty { draft.why = opening + "\n" }
                // AND THE SHEET ASKS BEFORE THE TYPING (Hidde, 2026-09-24:
                // "just open the login overlay if people go to the 'add tree
                // flow' from all direction", and about the line above it,
                // "that one sentence noone will read"). The website does the
                // same on arrival, which is the Google Maps convention taken
                // whole: the gate is at the entrance rather than at the send
                // button. The form stays behind it and the sheet is
                // dismissible, so nothing is hidden and nobody is trapped.
                //
                // A privacy request is not reachable from this screen, so
                // there is no exception to make here; on the website there is.
                if !account.isSignedIn { signingIn = true }
            }
            .sheet(isPresented: $signingIn) {
                SignInSheet(reason: .feedback, localCount: 0)
            }
        }
    }
}
