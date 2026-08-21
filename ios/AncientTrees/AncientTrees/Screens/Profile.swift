// Profile: the account and the admin, in the order every app people already
// use puts them.
//
// Rebuilt 2026-08-21. It opened with sign out and delete account, which is the
// two most destructive controls in the app greeting somebody who came to look
// at their own page. Hidde, on finding them: "my first button I see is to sign
// out or delete accounts. Can you please look at conventional profile pages
// and just create one of those, because this doesn't make any sense at all?"
//
// So the conventional order, the one AllTrails, Komoot, Airbnb and Strava all
// share: WHO you are, then the UPGRADE, then what you can DO, then the quiet
// links, and only at the very bottom, after everything else, sign out and
// delete.
//
// And no fear anywhere. The old cards told people their trees were "on this
// phone only" and would be "gone" if they lost it, which is scaring somebody
// into an account. Hidde: "that's a really weird sort of thing... if that
// said, then just ask people to sign in. Don't say those things."
//
// Suggest a tree keeps its fixed home here, which is the whole of the decision
// not to give it a fifth tab: the moments that actually produce a submission
// are contextual and live elsewhere (the Spot button, a tree with no
// photograph, "something here is wrong"). This is where it can be FOUND.

import SwiftUI

struct ProfileView: View {
    let catalogue: Catalogue
    @Environment(Saved.self) private var saved
    @Environment(Account.self) private var account
    @Environment(Navigator.self) private var navigator

    @State private var signingIn = false
    @State private var confirmingDelete = false
    @State private var deleteFailed = false
    @State private var plusPitch = false
    @State private var showingAccount = false
    /// Debug scaffolding, same family as -tab and -open in ContentView: the
    /// screenshot sweep cannot tap, and this sheet is otherwise only reachable
    /// by tapping a card on this screen.
    @State private var contributing = ProcessInfo.processInfo.arguments.contains("-contribute")

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 18) {
                identity
                contributeCard
                plusCard
                linksCard
                version
                accountControls
                Color.clear.frame(height: 80)
            }
            .padding(.horizontal, 16).padding(.top, 6)
        }
        .brandGround()
        .navigationTitle("Profile")
        .navigationBarTitleDisplayMode(.inline)
        .sheet(isPresented: $contributing) { ContributeView() }
        .sheet(isPresented: $plusPitch) { PaywallView(feature: .seasonAlerts) }
        .sheet(isPresented: $showingAccount) { accountSheet }
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
            Text("Your email address and your collection are removed from our database and cannot be recovered.")
        }
        .alert("That did not work", isPresented: $deleteFailed) {
            Button("OK", role: .cancel) {}
        } message: {
            Text("Nothing was deleted. Try again, or write to info@ancienttrees.app and we will do it by hand.")
        }
    }

    // MARK: - who you are

    private var identity: some View {
        HStack(spacing: 14) {
            ZStack {
                Circle().fill(Brand.surfaceMuted)
                if account.isSignedIn {
                    Text(String((account.email ?? "?").prefix(1)).uppercased())
                        .font(.brand(24, .bold)).foregroundStyle(Brand.moss)
                } else {
                    Image(systemName: "person").font(.system(size: 24))
                        .foregroundStyle(Brand.inkSoft)
                }
            }
            .frame(width: 60, height: 60)

            VStack(alignment: .leading, spacing: 3) {
                if account.isSignedIn {
                    Text(account.email ?? "Signed in")
                        .font(.brand(18, .bold, relativeTo: .headline))
                        .foregroundStyle(Brand.ink).lineLimit(1)
                    // A count is a promise that the things counted are
                    // somewhere; this is the way there (Hidde, 2026-08-21).
                    Text("\(saved.visitedCount) collected · \(saved.savedCount) saved")
                        .font(.footnote).foregroundStyle(Brand.moss)
                } else {
                    Text("Sign in")
                        .font(.brand(18, .bold, relativeTo: .headline))
                        .foregroundStyle(Brand.ink)
                    Text("Your collection follows you to the website and to any phone.")
                        .font(.footnote).foregroundStyle(Brand.inkSoft)
                        .fixedSize(horizontal: false, vertical: true)
                }
            }
            Spacer(minLength: 0)
            if !account.isSignedIn {
                Image(systemName: "chevron.right")
                    .font(.footnote).foregroundStyle(Brand.inkSoft.opacity(0.6))
            }
        }
        .padding(16)
        .frame(maxWidth: .infinity, alignment: .leading)
        .brandCard()
        // The WHOLE row is the control when signed out, which is how every
        // profile page with a sign-in prompt does it. A pill button beside the
        // text squeezed the sentence into a four-line column.
        .contentShape(.rect)
        .onTapGesture {
            if account.isSignedIn { navigator.selectTab = 3 } else { signingIn = true }
        }
        .accessibilityIdentifier("profile-signin")
    }

    // MARK: - the upgrade

    /// Near the top, because on a profile page in any app that has one, the
    /// upgrade is what the page is FOR. What it replaced was five locked rows
    /// at the very bottom: a features table read as a list of things you
    /// cannot have.
    private var plusCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack(spacing: 10) {
                Image(systemName: "leaf.fill").font(.title3).foregroundStyle(Brand.gold)
                Text("Plus")
                    .font(.brand(19, .heavy, relativeTo: .headline)).foregroundStyle(Brand.ink)
            }
            Text("Season alerts, curated walks, your own photographs and badges, and the whole map offline.")
                .font(.footnote).foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
            Button { plusPitch = true } label: {
                Text("See what is in it")
                    .font(.brand(16, .bold))
                    .foregroundStyle(.white)
                    .frame(maxWidth: .infinity).frame(height: 48)
                    .background(Brand.moss, in: .capsule)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("profile-plus")
            Text("Every tree, story and location stays free, here and on the website.")
                .font(.caption2).foregroundStyle(Brand.inkSoft)
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
            Button { contributing = true } label: {
                Text("Suggest a tree")
                    .font(.brand(16, .bold))
                    .foregroundStyle(Brand.moss)
                    .frame(maxWidth: .infinity).frame(height: 48)
                    .background(Brand.surface, in: .capsule)
                    .overlay { Capsule().strokeBorder(Brand.moss.opacity(0.35), lineWidth: 1.5) }
            }
            .buttonStyle(.plain)
        }
        .padding(18)
        .frame(maxWidth: .infinity, alignment: .leading)
        .brandCard()
    }

    // MARK: - the quiet rows

    private var linksCard: some View {
        VStack(spacing: 0) {
            if account.isSignedIn {
                Button { showingAccount = true } label: {
                    HStack(spacing: 12) {
                        Image(systemName: "envelope").frame(width: 20).foregroundStyle(Brand.moss)
                        Text("Account").font(.callout).foregroundStyle(Brand.ink)
                        Spacer()
                        Image(systemName: "chevron.right")
                            .font(.caption).foregroundStyle(Brand.inkSoft.opacity(0.6))
                    }
                    .padding(.horizontal, 16).frame(height: 48)
                    .contentShape(.rect)
                }
                Divider().padding(.leading, 48)
            }
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
            .padding(.horizontal, 16).frame(height: 48)
            .contentShape(.rect)
        }
    }

    private var version: some View {
        Text("\(catalogue.trees.count.formatted(.number.locale(Locale(identifier: "en_US")))) trees, updated whenever you open the app.")
            .font(.caption2).foregroundStyle(Brand.inkSoft.opacity(0.8))
            .frame(maxWidth: .infinity, alignment: .center)
            .padding(.top, 4)
    }

    /// What we hold, in one screen, because "where do I change my email
    /// address" deserves an answer rather than a missing row (Hidde,
    /// 2026-08-21). Changing the address itself is not built: it needs a
    /// verified swap on the server and it moves somebody's whole collection,
    /// so it is Hidde's to open rather than mine.
    private var accountSheet: some View {
        NavigationStack {
            VStack(alignment: .leading, spacing: 16) {
                Text("Signed in as")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                Text(account.email ?? "Signed in")
                    .font(.brand(20, .bold)).foregroundStyle(Brand.ink)
                Text("Your collection is kept under this address. Sign in on ancienttrees.app with the same one and it is there too.")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
                Text("We hold your email address and the trees you have saved and collected. Nothing else.")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
                Text("To use a different address, write to info@ancienttrees.app and we will move your collection across.")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
                Spacer()
            }
            .padding(20)
            .frame(maxWidth: .infinity, alignment: .leading)
            .brandGround()
            .navigationTitle("Account")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Done") { showingAccount = false }
                }
            }
        }
    }

    // MARK: - the two that go last

    @ViewBuilder private var accountControls: some View {
        if account.isSignedIn {
            VStack(spacing: 0) {
                Button { account.signOut() } label: {
                    HStack {
                        Text("Sign out").font(.callout).foregroundStyle(Brand.ink)
                        Spacer()
                    }
                    .padding(.horizontal, 16).frame(height: 48)
                    .contentShape(.rect)
                }
                Divider().padding(.leading, 16)
                Button { confirmingDelete = true } label: {
                    HStack {
                        Text("Delete account").font(.callout).foregroundStyle(.red)
                        Spacer()
                    }
                    .padding(.horizontal, 16).frame(height: 48)
                    .contentShape(.rect)
                }
            }
            .brandCard()
        }
    }
}
