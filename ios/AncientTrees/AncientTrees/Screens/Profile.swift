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
    @Environment(Units.self) private var units

    @State private var signingIn = false
    @State private var confirmingDelete = false
    @State private var confirmingSignOut = false
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
                // The same title as Explore and Collection wear, now that this
                // is a tab beside them rather than a page pushed from a small
                // avatar (Hidde, 2026-08-24). An inline navigation title on one
                // of three sibling tabs and a big screen title on the other two
                // is the kind of difference nobody can name and everybody
                // feels.
                Text("Profile")
                    .font(.screenTitle)
                    .foregroundStyle(Brand.ink)
                    .padding(.bottom, 2)
                identity
                contributeCard
                plusCard
                settingsCard
                aboutCard
                version
                signOutRow
                Color.clear.frame(height: 80)
            }
            .padding(.horizontal, 16).padding(.top, 6)
        }
        .brandGround()
        .toolbar(.hidden, for: .navigationBar)
        .sheet(isPresented: $contributing) { ContributeView() }
        .sheet(isPresented: $plusPitch) { PaywallView(feature: .seasonAlerts) }
        .sheet(isPresented: $showingAccount) { accountSheet }
        .sheet(isPresented: $signingIn) {
            SignInSheet(reason: saved.savedCount > 0 ? .keepCollection(saved.savedCount) : .general,
                        localCount: saved.savedCount)
                .environment(account).environment(saved)
        }
        // Signing out went through on the first tap, while deleting the
        // account two rows above asked first. Every app asks (Hidde,
        // 2026-08-24: "dit is raar"), and here it matters more than usual: what
        // it looks like you are about to lose is your collection.
        .confirmationDialog("Sign out?", isPresented: $confirmingSignOut,
                            titleVisibility: .visible) {
            Button("Sign out", role: .destructive) { account.signOut() }
            Button("Cancel", role: .cancel) {}
        } message: {
            Text("Your collection stays in your account. Sign in again on any phone and it comes back.")
        }
        .alert("Delete your account?", isPresented: $confirmingDelete) {
            Button("Cancel", role: .cancel) {}
            Button("Delete", role: .destructive) {
                Task { deleteFailed = !(await account.deleteAccount()) }
            }
        } message: {
            Text("We delete your email address and your collection. This cannot be undone.")
        }
        .alert("That did not work", isPresented: $deleteFailed) {
            Button("OK", role: .cancel) {}
        } message: {
            Text("Nothing was deleted. Try again, or write to info@ancienttrees.app and we will do it by hand.")
        }
    }

    // MARK: - who you are

    private var identity: some View {
        // A BUTTON, not a tap gesture on a card. onTapGesture on a large view
        // inside a ScrollView competes with the scroll's own recogniser, so a
        // tap that moves a millimetre is swallowed and the control feels slow
        // and unreliable, which is exactly what Hidde reported (2026-08-24:
        // "de sign in knop op profielpagina werkt langzaam en soms niet").
        // A Button coordinates with the scroll view instead of racing it.
        Button {
            if account.isSignedIn { navigator.selectTab = 3 } else { signingIn = true }
        } label: {
            identityRow
        }
        .buttonStyle(.plain)
        .accessibilityIdentifier("profile-signin")
    }

    private var identityRow: some View {
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
                Text("See what's included")
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
            // Short, because the card only has one thing to say (Hidde,
            // 2026-08-24: "niet meer tekst, meer inzetten op helderheid, minder
            // poespas"). How you add a tree here is by standing in front of it,
            // and everything else that used to be in this paragraph was us
            // explaining ourselves.
            Text("You can add a tree by taking a photograph of it and filling in what you know.")
                .font(.footnote).foregroundStyle(Brand.inkSoft)
            Button { navigator.collectNearby = true } label: {
                Text("Add a tree")
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

    // MARK: - settings

    /// The two settings a map app is expected to have and ours did not. No
    /// website row and no top-level privacy row any more (Hidde, 2026-08-21):
    /// privacy belongs under About, which is where every app people already
    /// use keeps it and where the App Store expects to find it.
    private var settingsCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Settings").font(.eyebrow).textCase(.uppercase)
                .foregroundStyle(Brand.inkSoft).tracking(0.8)
                .padding(.leading, 4)
            VStack(spacing: 0) {
                // The WHOLE ROW opens the menu, which is what a settings row
                // does everywhere and what this one did not: the control was
                // the width of the word "Kilometres", and the row directly
                // under it is the locked Plus row, so a tap that fell short
                // opened the paywall instead of the units (Hidde, 2026-08-24:
                // "distance km veranderen verwijst naar plus, dat moet gewoon
                // zonder plus naar miles kunnen"). Units were never gated in
                // the code; the target was.
                Menu {
                    Picker("", selection: Binding(get: { units.unit },
                                                  set: { units.unit = $0 })) {
                        ForEach(DistanceUnit.allCases) { u in Text(u.label).tag(u) }
                    }
                } label: {
                    HStack(spacing: 12) {
                        Image(systemName: "ruler").frame(width: 20).foregroundStyle(Brand.moss)
                        Text("Distances").font(.callout).foregroundStyle(Brand.ink)
                        Spacer()
                        Text(units.unit.label).font(.callout).foregroundStyle(Brand.inkSoft)
                        Image(systemName: "chevron.up.chevron.down")
                            .font(.caption2).foregroundStyle(Brand.inkSoft)
                    }
                    .padding(.horizontal, 16).frame(height: 48)
                    .contentShape(.rect)
                }
                .buttonStyle(.plain)
                Divider().padding(.leading, 48)
                LockedRow(feature: .seasonAlerts) {
                    HStack(spacing: 12) {
                        Image(systemName: "bell").frame(width: 20).foregroundStyle(Brand.moss)
                        Text("Season alerts").font(.callout).foregroundStyle(Brand.ink)
                        Spacer()
                        Chip(text: "Plus", tint: Brand.gold)
                    }
                    .padding(.horizontal, 16).frame(height: 48)
                }
            }
            .brandCard()
        }
    }

    // MARK: - about

    private var aboutCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("About").font(.eyebrow).textCase(.uppercase)
                .foregroundStyle(Brand.inkSoft).tracking(0.8)
                .padding(.leading, 4)
            VStack(spacing: 0) {
                link("Privacy", "lock", "https://ancienttrees.app/privacy")
                Divider().padding(.leading, 48)
            }
            .brandCard()
        }
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
                Text("We keep your collection under this address. Sign in on ancienttrees.app with the same one and it is there too.")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
                Text("We hold your email address and the trees you have saved and collected. Nothing else.")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
                Text("To use a different address, write to info@ancienttrees.app and we will move your collection across.")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
                Spacer()
                Button { confirmingDelete = true } label: {
                    Text("Delete account")
                        .font(.callout).foregroundStyle(.red)
                        .frame(maxWidth: .infinity).frame(height: 48)
                        .contentShape(.rect)
                }
                .buttonStyle(.plain)
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

    // MARK: - the one that goes last

    /// Sign out, and nothing else. Deleting an account is not something you
    /// should be able to do by mis-tapping the bottom of a profile page, so it
    /// moved one layer in, under Account (Hidde, 2026-08-21: "most of the time
    /// they put the click further down").
    @ViewBuilder private var signOutRow: some View {
        if account.isSignedIn {
            Button { confirmingSignOut = true } label: {
                HStack {
                    Text("Sign out").font(.callout).foregroundStyle(Brand.ink)
                    Spacer()
                }
                .padding(.horizontal, 16).frame(height: 48)
                .contentShape(.rect)
            }
            .brandCard()
        }
    }
}
