// You: what you have collected, and where it is kept.
//
// Rewritten 2026-08-20. What stood here was a settings list whose first row read
// "Signed in ... not yet", as a LabeledContent, which is to say a piece of text
// that states a problem and offers nothing. There was no way to make an account
// anywhere in the app, so the honest answer to "how do we get more accounts"
// was that we could not get any.
//
// The shape now follows AllTrails' Activity tab and Google Maps' profile, which
// agree with each other on the thing that matters: the top of this screen is
// either who you are or an invitation to be somebody, and it is never a status
// label. Below that sits the collection, and the paid things sit at the bottom
// where they belong, because selling three locked features to a person with
// zero collected trees is asking for money before anything has been felt.
//
// The stat row stays even at zero, deliberately, which is the one non-obvious
// thing the teardown found: AllTrails draws its progress chart with a single bar
// on it rather than hiding it. The shape of what you are about to fill in is the
// invitation.

import SwiftUI

struct YouView: View {
    let catalogue: Catalogue
    @Environment(Saved.self) private var saved
    @Environment(Account.self) private var account
    @Environment(Nudge.self) private var nudge

    @State private var signingIn = false
    @State private var confirmingDelete = false
    @State private var deleteFailed = false

    private let brand = Color(red: 0.20, green: 0.35, blue: 0.20)

    private var visited: [Tree] {
        saved.entries.values.filter { $0.visitedAt != nil }.compactMap { catalogue.tree($0.treeId) }
    }
    private var countries: Int { Set(visited.map(\.country)).count }
    private var cities: Int { Set(visited.map(\.citySlug)).count }
    private var species: Int { Set(visited.map(\.commonName)).count }

    var body: some View {
        List {
            Section {
                HStack(spacing: 0) {
                    tile("\(visited.count)", "Trees")
                    Divider().frame(height: 40)
                    tile("\(cities)", cities == 1 ? "Place" : "Places")
                    Divider().frame(height: 40)
                    tile("\(species)", "Species")
                    Divider().frame(height: 40)
                    tile("\(countries)", countries == 1 ? "Country" : "Countries")
                }
                .padding(.vertical, 10)
                .listRowInsets(.init(top: 0, leading: 0, bottom: 0, trailing: 0))
            } footer: {
                Text("Out of \(catalogue.trees.count.formatted(.number.locale(Locale(identifier: "en_US")))) trees we map in \(Set(catalogue.trees.map(\.country)).count) countries.")
            }

            if account.isSignedIn { signedInSection } else { signedOutSection }

            Section {
                Link("The website", destination: URL(string: "https://ancienttrees.app")!)
                Link("Suggest a tree", destination: URL(string: "https://ancienttrees.app/contribute")!)
                Link("Privacy", destination: URL(string: "https://ancienttrees.app/privacy")!)
            }

            Section {
                LockedRow(feature: .badges) { Text("Badges") }
                LockedRow(feature: .offlineDownload) { Text("Offline maps") }
                LockedRow(feature: .seasonAlerts) { Text("Season alerts") }
            } header: {
                Text("Coming with Plus")
            } footer: {
                Text("Every tree, story and location stays free, here and on the website.")
            }
        }
        .navigationTitle("You")
        .sheet(isPresented: $signingIn) {
            SignInSheet(reason: reasonForButton, localCount: saved.savedCount)
                .environment(account)
                .environment(saved)
        }
        .alert("Delete your account?", isPresented: $confirmingDelete) {
            Button("Cancel", role: .cancel) {}
            Button("Delete", role: .destructive) {
                Task {
                    let ok = await account.deleteAccount()
                    deleteFailed = !ok
                }
            }
        } message: {
            Text("Your email address and your collection are removed from our database and cannot be recovered. The trees you ticked stay on this phone.")
        }
        .alert("That did not work", isPresented: $deleteFailed) {
            Button("OK", role: .cancel) {}
        } message: {
            Text("Nothing was deleted. Try again, or write to info@ancienttrees.app and we will do it by hand.")
        }
    }

    /// The whole point of this screen when nobody is signed in. A card rather
    /// than a row, because a row is something you scroll past.
    private var signedOutSection: some View {
        Section {
            VStack(alignment: .leading, spacing: 12) {
                HStack(spacing: 10) {
                    SpeciesMark(species: "Pedunculate Oak", color: brand)
                        .frame(width: 34, height: 34)
                    Text(saved.savedCount == 0
                         ? "Your collection lives on this phone"
                         : "\(saved.savedCount) collected, on this phone only")
                        .font(.headline)
                }
                Text(saved.savedCount == 0
                     ? "Start ticking trees off and they are kept here. An account keeps them if this phone is lost or replaced, and puts them on the website too."
                     : "Lose this phone, replace it, or reinstall, and they are gone. An account keeps them, and puts them on the website too.")
                    .font(.footnote).foregroundStyle(.secondary)
                Button {
                    signingIn = true
                } label: {
                    Text("Keep my trees")
                        .font(.headline).frame(maxWidth: .infinity).padding(.vertical, 13)
                }
                .buttonStyle(.borderedProminent).tint(brand).clipShape(.capsule)
                Text("One tap with Apple, or one email. No password, and nothing else stored.")
                    .font(.caption2).foregroundStyle(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
            }
            .padding(.vertical, 6)
        }
    }

    private var signedInSection: some View {
        Section {
            LabeledContent("Signed in", value: account.email ?? "yes")
            HStack {
                Label("Your trees are backed up", systemImage: "checkmark.icloud")
                    .font(.footnote).foregroundStyle(.secondary)
            }
            Button("Sign out") { account.signOut() }
            Button("Delete account", role: .destructive) { confirmingDelete = true }
        } header: {
            Text("Account")
        } footer: {
            Text("Signed in on ancienttrees.app with the same address and your collection is there too.")
        }
    }

    private var reasonForButton: SignInReason {
        saved.savedCount > 0 ? .keepCollection(saved.savedCount) : .general
    }

    private func tile(_ value: String, _ label: String) -> some View {
        VStack(spacing: 4) {
            Text(value).font(.title2.bold()).monospacedDigit()
            Text(label).font(.caption2).foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity)
    }
}
