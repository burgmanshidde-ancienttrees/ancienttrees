// You: what you have collected, and where it is kept.
//
// Rebuilt twice on 2026-08-20. First from a settings list whose top row was the
// dead text "Signed in ... not yet", and then again off `List` entirely, because
// a screen made of inset-grouped rows IS the Settings app however good the copy
// on it is.
//
// The shape now is AllTrails' Activity tab, which their teardown describes
// exactly: a stats card, then Parkstempels drawn as illustrated badges, then the
// log. Ours are species rather than national parks, and drawing them is the one
// idea in that teardown we had listed as "what we take" and had not taken.
//
// The stamps are the point, and the non-obvious rule about them comes straight
// from watching their app: THE UNCOLLECTED ONES ARE DRAWN TOO. AllTrails shows
// its progress chart with a single bar on it rather than hiding the chart until
// there is data, and an empty grid of outlines does more work than any sentence
// saying you have not collected anything: the shape of what you are about to
// fill in is the invitation. Every user of this app on its first day has zero,
// so this screen has to be worth looking at at zero.

import SwiftUI

struct YouView: View {
    let catalogue: Catalogue
    @Environment(Saved.self) private var saved
    @Environment(Account.self) private var account

    @State private var signingIn = false
    @State private var confirmingDelete = false
    @State private var deleteFailed = false

    private var visited: [Tree] {
        saved.entries.values.filter { $0.visitedAt != nil }.compactMap { catalogue.tree($0.treeId) }
    }
    private var countries: Int { Set(visited.map(\.country)).count }
    private var cities: Int { Set(visited.map(\.citySlug)).count }
    private var collectedSpecies: Set<String> { Set(visited.map(\.commonName)) }

    /// The set to fill in: the species we map most, so the grid is worth
    /// completing rather than arbitrary.
    private var stampSpecies: [String] {
        Dictionary(grouping: catalogue.trees, by: \.commonName)
            .sorted { $0.value.count > $1.value.count }
            .prefix(18).map(\.key)
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 26) {
                statsCard
                stampCard
                if account.isSignedIn { signedInCard } else { signedOutCard }
                linksCard
                plusCard
                Color.clear.frame(height: 80)
            }
            .padding(.horizontal, 16)
            .padding(.top, 6)
        }
        .brandGround()
        .navigationTitle("You")
        .sheet(isPresented: $signingIn) {
            SignInSheet(reason: saved.savedCount > 0 ? .keepCollection(saved.savedCount) : .general,
                        localCount: saved.savedCount)
                .environment(account).environment(saved)
        }
        .alert("Delete your account?", isPresented: $confirmingDelete) {
            Button("Cancel", role: .cancel) {}
            Button("Delete", role: .destructive) {
                Task { deleteFailed = !(await account.deleteAccount()) }
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

    // MARK: - the numbers

    private var statsCard: some View {
        VStack(spacing: 14) {
            HStack(spacing: 0) {
                tile("\(visited.count)", "Trees")
                Divider().frame(height: 42)
                tile("\(cities)", cities == 1 ? "Place" : "Places")
                Divider().frame(height: 42)
                tile("\(collectedSpecies.count)", "Species")
                Divider().frame(height: 42)
                tile("\(countries)", countries == 1 ? "Country" : "Countries")
            }
            Text("Out of \(catalogue.trees.count.formatted(.number.locale(Locale(identifier: "en_US")))) trees we map in \(Set(catalogue.trees.map(\.country)).count) countries.")
                .font(.caption).foregroundStyle(Brand.inkSoft)
        }
        .padding(.vertical, 18).padding(.horizontal, 8)
        .frame(maxWidth: .infinity)
        .brandCard()
    }

    private func tile(_ value: String, _ label: String) -> some View {
        VStack(spacing: 3) {
            Text(value)
                .font(.brand(26, .black, relativeTo: .title))
                .foregroundStyle(Brand.ink).monospacedDigit()
            Text(label).font(.caption2).foregroundStyle(Brand.inkSoft)
        }
        .frame(maxWidth: .infinity)
    }

    // MARK: - the stamps

    private var stampCard: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack(alignment: .firstTextBaseline) {
                Text("Species collected").font(.brand(19, .heavy, relativeTo: .title3))
                    .foregroundStyle(Brand.ink)
                Spacer()
                Text("\(collectedSpecies.count) of \(stampSpecies.count)")
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(Brand.inkSoft).monospacedDigit()
            }
            LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: 10), count: 6),
                      spacing: 14) {
                ForEach(stampSpecies, id: \.self) { s in
                    let got = collectedSpecies.contains(s)
                    SpeciesMark(species: s, color: got ? Brand.moss : Brand.inkSoft.opacity(0.28))
                        .frame(height: 34)
                        .accessibilityLabel(got ? "\(s), collected" : "\(s), not yet")
                }
            }
            Text(collectedSpecies.isEmpty
                 ? "Tick a tree off and its species fills in here."
                 : "The eighteen species we map most. Rarer ones count too, they are just not drawn here yet.")
                .font(.caption).foregroundStyle(Brand.inkSoft)
        }
        .padding(18)
        .frame(maxWidth: .infinity, alignment: .leading)
        .brandCard()
    }

    // MARK: - the account

    private var signedOutCard: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(spacing: 10) {
                SpeciesMark(species: "Pedunculate Oak", color: Brand.moss)
                    .frame(width: 34, height: 34)
                Text(saved.savedCount == 0
                     ? "Your collection lives on this phone"
                     : "\(saved.savedCount) collected, on this phone only")
                    .font(.brand(18, .bold, relativeTo: .headline))
                    .foregroundStyle(Brand.ink)
            }
            Text(saved.savedCount == 0
                 ? "Start ticking trees off and they are kept here. An account keeps them if this phone is lost or replaced, and puts them on the website too."
                 : "Lose this phone, replace it, or reinstall, and they are gone. An account keeps them, and puts them on the website too.")
                .font(.footnote).foregroundStyle(Brand.inkSoft)
            Button("Keep my trees") { signingIn = true }
                .buttonStyle(BrandButtonStyle())
            Text("One tap with Apple, or one email. No password, and nothing else stored.")
                .font(.caption2).foregroundStyle(Brand.inkSoft)
                .frame(maxWidth: .infinity, alignment: .center)
        }
        .padding(18)
        .frame(maxWidth: .infinity, alignment: .leading)
        .brandCard()
    }

    private var signedInCard: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label("Your trees are backed up", systemImage: "checkmark.icloud.fill")
                .font(.brand(17, .bold, relativeTo: .headline))
                .foregroundStyle(Brand.moss)
            Text(account.email ?? "Signed in")
                .font(.footnote).foregroundStyle(Brand.inkSoft)
            Text("Your trees are kept under this address. Sign in on ancienttrees.app with the same one and your collection is there too; a different one starts a separate collection.")
                .font(.caption).foregroundStyle(Brand.inkSoft)
            Divider()
            Button("Sign out") { account.signOut() }
                .font(.subheadline.weight(.semibold)).foregroundStyle(Brand.moss)
            Button("Delete account") { confirmingDelete = true }
                .font(.subheadline).foregroundStyle(.red)
        }
        .padding(18)
        .frame(maxWidth: .infinity, alignment: .leading)
        .brandCard()
    }

    // MARK: - the quiet rows

    private var linksCard: some View {
        VStack(spacing: 0) {
            link("The website", "safari", "https://ancienttrees.app")
            Divider().padding(.leading, 48)
            link("Suggest a tree", "plus.circle", "https://ancienttrees.app/contribute")
            Divider().padding(.leading, 48)
            link("Privacy", "lock", "https://ancienttrees.app/privacy")
        }
        .brandCard()
    }

    private func link(_ title: String, _ icon: String, _ url: String) -> some View {
        Link(destination: URL(string: url)!) {
            HStack(spacing: 12) {
                Image(systemName: icon).frame(width: 20).foregroundStyle(Brand.moss)
                Text(title).font(.callout).foregroundStyle(Brand.ink)
                Spacer()
                Image(systemName: "arrow.up.right")
                    .font(.caption).foregroundStyle(Brand.inkSoft.opacity(0.6))
            }
            .padding(.horizontal, 16).padding(.vertical, 14)
        }
    }

    /// Last on the screen on purpose. Selling three locked features to somebody
    /// with nothing collected is asking for money before anything has been felt.
    private var plusCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Coming with Plus").font(.eyebrow).textCase(.uppercase)
                .foregroundStyle(Brand.inkSoft).tracking(0.8)
            VStack(spacing: 0) {
                LockedRow(feature: .badges) { plusRow("Badges", "rosette") }
                Divider().padding(.leading, 48)
                LockedRow(feature: .offlineDownload) { plusRow("Offline maps", "arrow.down.circle") }
                Divider().padding(.leading, 48)
                LockedRow(feature: .seasonAlerts) { plusRow("Season alerts", "bell") }
            }
            .brandCard()
            Text("Every tree, story and location stays free, here and on the website.")
                .font(.caption).foregroundStyle(Brand.inkSoft)
        }
    }

    private func plusRow(_ title: String, _ icon: String) -> some View {
        HStack(spacing: 12) {
            Image(systemName: icon).frame(width: 20).foregroundStyle(Brand.inkSoft)
            Text(title).font(.callout).foregroundStyle(Brand.ink)
        }
        .padding(.horizontal, 16).padding(.vertical, 14)
    }
}
