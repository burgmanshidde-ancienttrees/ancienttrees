// Profile: the account and the admin, and nothing else.
//
// New on 2026-08-20 out of the old You tab, which was doing three jobs: the
// score, the account and the settings shelf. The score went to Collect where the
// game is, and what is left here is what Hidde asked for in one line: "hier zijn
// al je persoonlijke dingen in ... je accountinstellingen, en weet ik veel alles
// wat je bij een account zoekt, vindt".
//
// A quiet screen on purpose. This is the tab people open twice a year, which is
// exactly why it should not be competing for attention: AllTrails and Google
// Maps both keep the profile boring and put the collection somewhere else.
//
// Suggest a tree lives here as its FIXED home, and that is the whole of the
// decision not to give it a fifth tab. The moments that actually produce a
// submission are contextual and already exist elsewhere in the app: standing at
// a tree with no photograph, the "something here is wrong" button, an empty
// search. Those ask where somebody has just noticed the gap themselves. This is
// only the place it can be found when somebody goes looking for it.

import SwiftUI

struct ProfileView: View {
    let catalogue: Catalogue
    @Environment(Saved.self) private var saved
    @Environment(Account.self) private var account

    @State private var signingIn = false
    @State private var confirmingDelete = false
    @State private var deleteFailed = false

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 22) {
                if account.isSignedIn { signedInCard } else { signedOutCard }
                contributeCard
                linksCard
                plusCard
                version
                Color.clear.frame(height: 80)
            }
            .padding(.horizontal, 16).padding(.top, 6)
        }
        .brandGround()
        .navigationTitle("Profile")
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
            Text("One tap with Apple or Google, or one email. No password, and nothing else stored.")
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
            // Named because Apple hands out a private relay address and Google
            // does not, so two sign-ins can be two accounts. Somebody who can
            // read the address can work that out; somebody who cannot just
            // thinks we lost their trees.
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

    // MARK: - contributing

    private var contributeCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Know a tree we are missing?")
                .font(.brand(18, .bold, relativeTo: .headline)).foregroundStyle(Brand.ink)
            Text("We map \(catalogue.trees.count.formatted(.number.locale(Locale(identifier: "en_US")))) and there are a great many more. If you know a good one, or a whole city worth mapping, tell us.")
                .font(.footnote).foregroundStyle(Brand.inkSoft)
            Link(destination: URL(string: "https://ancienttrees.app/contribute")!) {
                Text("Suggest a tree")
                    .font(.brand(17, .bold, relativeTo: .headline))
                    .foregroundStyle(Brand.moss)
                    .frame(maxWidth: .infinity).padding(.vertical, 14)
                    .background(Brand.surface, in: .capsule)
                    .overlay { Capsule().strokeBorder(Brand.moss.opacity(0.35), lineWidth: 1.5) }
            }
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
                LockedRow(feature: .photoUpload) { plusRow("Your photo on the tree's page", "camera") }
                Divider().padding(.leading, 48)
                LockedRow(feature: .badges) { plusRow("Badges and the visited seal", "rosette") }
                Divider().padding(.leading, 48)
                LockedRow(feature: .walkBeyondFirst) { plusRow("Every walk", "figure.walk") }
                Divider().padding(.leading, 48)
                LockedRow(feature: .offlineDownload) { plusRow("Offline maps", "arrow.down.circle") }
                Divider().padding(.leading, 48)
                LockedRow(feature: .seasonAlerts) { plusRow("Season alerts", "bell") }
            }
            .brandCard()
            Text("Ticking trees off, your list and every tree, story and location stay free, here and on the website.")
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

    private var version: some View {
        Text("\(catalogue.trees.count.formatted(.number.locale(Locale(identifier: "en_US")))) trees, updated whenever you open the app.")
            .font(.caption2).foregroundStyle(Brand.inkSoft.opacity(0.8))
            .frame(maxWidth: .infinity, alignment: .center)
    }
}
