import SwiftUI

struct ContributeView: View {
    /// Prefilled when it is opened from a tree, which is the case that matters:
    /// somebody standing at a pin that is wrong.
    var about: Tree?

    @Environment(\.dismiss) private var dismiss
    @State private var draft = Submission.Draft()
    @State private var sending = false
    @State private var sent = false
    @State private var failed = false

    var body: some View {
        NavigationStack {
            Form {
                if sent {
                    Section {
                        Label("Thank you", systemImage: "checkmark.seal.fill")
                            .font(.headline)
                        Text("Everything sent in is checked against independent sources before it goes live, and a wrong pin gets looked at the same day.")
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
                        TextField("Email, if you want to hear back", text: $draft.email)
                            .keyboardType(.emailAddress)
                            .textInputAutocapitalization(.never)
                            .autocorrectionDisabled()
                    } footer: {
                        Text("Optional. Leave it so we can ask a question if we need to, and tell you what your tip changed. We use it for nothing else.")
                    }
                    Section {
                        Button {
                            Task {
                                sending = true
                                let ok = await Submission.send(draft, from: about?.url)
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
        }
    }
}
