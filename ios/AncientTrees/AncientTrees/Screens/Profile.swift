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
    @Environment(Moderation.self) private var moderation
    @Environment(Sightings.self) private var sightings



    @State private var signingIn = false
    @State private var confirmingDelete = false
    @State private var confirmingSignOut = false
    @State private var deleteFailed = false
    @State private var showingAccount = false
    @State private var showingLegal = false
    /// The maps app Take me there opens, empty while nobody has answered. Same
    /// key Directions reads; @AppStorage so the row redraws when it changes.
    @AppStorage("directions.app") private var directionsApp: String = ""
    /// Debug scaffolding, same family as -tab and -open in ContentView: the
    /// screenshot sweep cannot tap, and this sheet is otherwise only reachable
    /// by tapping a card on this screen.
    @State private var contributing = ProcessInfo.processInfo.arguments.contains("-contribute")
    @State private var givingFeedback = ProcessInfo.processInfo.arguments.contains("-feedback")
    @State private var editingProfile = false
    /// Same debug scaffolding as -contribute and -feedback: the sweep cannot
    /// tap, so every screen needs an argument or it ships unlooked-at.

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 18) {
                // NO SCREEN TITLE. It carried one from the days this was a
                // tab beside Explore and Collection, where a big title was
                // right and there was no bar to hold one. It is a pushed page
                // now, the bar says Settings, and a page whose bar and body
                // disagree about its own name is the "title twice" fault the
                // tree page already fixed once.
                identity
                contributeCard
                // No Plus card. It was the loudest thing on the page and it
                // sold a tier that does not open yet (Hidde, 2026-08-25: "you
                // can delete the whole see what's included button from profile
                // right now, but you can add it under settings, like season
                // alerts"). An upgrade card belongs at the top of a profile in
                // any app that HAS an upgrade; ours is a promise, and a promise
                // belongs in a settings row.
                settingsCard
                aboutCard
                version
                signOutRow
                Color.clear.frame(height: 80)
            }
            .padding(.horizontal, 16).padding(.top, 6)
        }
        .brandGround()
        // A BAR, so there is a way back (Hidde, 2026-08-26: "als je op
        // instellingen drukt moet er een vorige button komen dat je weer terug
        // kan naar je me pagina"). This screen hid the navigation bar from the
        // days it was a tab, where there was nothing to go back to; it is
        // pushed from the gear on My trees now, and a pushed page without a
        // back button is a room with the door painted over.
        .navigationTitle("Settings")
        .navigationBarTitleDisplayMode(.inline)
        .sheet(isPresented: $contributing) { ContributeView() }
        .sheet(isPresented: $givingFeedback) { ContributeView(feedbackMode: true) }
        .sheet(isPresented: $editingProfile) { ProfileEditor() }
        // The paywall still opens, from the locked rows themselves; it no
        // longer has a row of its own (2026-08-25).
        .sheet(isPresented: $showingAccount) { accountSheet }
        .sheet(isPresented: $showingLegal) { legalSheet }
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
            // THE EDITOR, not a tab. This asked for tab 3, which stopped
            // existing when the bar went to three tabs on 2026-08-26: the
            // TabView then had a selection matching no tag, so it showed the
            // map with the tab bar gone and no way back (Hidde, 2026-08-27:
            // "kom je op het mapscherm zonder floating menu"). Tapping your own
            // card in a settings screen opens your account everywhere else,
            // which is the same room the row further down opens.
            if account.isSignedIn { editingProfile = true } else { signingIn = true }
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
                    Text(SignInReason.prompt)
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

    // The upgrade card lived here until 2026-08-25. Its two rows are in
    // Settings now, next to Season alerts, which is where he put them.

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
                // No inset. It put SETTINGS and ABOUT at 20 while every card
                // under them sits at 16, which appfit reads as a drift and a
                // reader reads as sloppy without being able to name it.
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
                // WHICH MAPS APP Take me there opens. It is asked once, on the
                // first tap, and this is where somebody changes their mind
                // (Hidde, 2026-08-28: "waarom opent die niet mn google maps
                // app, 90% van de mensen hebben die app"). Same row shape as
                // Distances above it, because it is the same kind of choice.
                // "Ask again" rather than a third app: it clears the answer, so
                // the next Take me there asks.
                // @AppStorage, not Directions.preferred directly: that reads
                // UserDefaults and SwiftUI has no way to know it changed, so
                // the row would keep printing the old answer until something
                // else redrew the screen.
                // The two apps and nothing else. "Ask again" was a third
                // option here and it is gone (Hidde, 2026-08-29: "directions
                // ask again optie is niet nodig"). A default-app setting lists
                // the apps; putting the question itself in the list of answers
                // is a control that undoes the choice it exists to make, and
                // the ask is not something anybody wants back.
                Menu {
                    Picker("", selection: $directionsApp) {
                        ForEach(Directions.MapsApp.allCases) { a in
                            Text(a.label).tag(a.rawValue)
                        }
                    }
                } label: {
                    HStack(spacing: 12) {
                        Image(systemName: "arrow.turn.up.right")
                            .frame(width: 20).foregroundStyle(Brand.moss)
                        Text("Directions").font(.callout).foregroundStyle(Brand.ink)
                        Spacer()
                        Text(Directions.MapsApp(rawValue: directionsApp)?.label ?? "Ask each time")
                            .font(.callout).foregroundStyle(Brand.inkSoft)
                        Image(systemName: "chevron.up.chevron.down")
                            .font(.caption2).foregroundStyle(Brand.inkSoft)
                    }
                    .padding(.horizontal, 16).frame(height: 48)
                    .contentShape(.rect)
                }
                .buttonStyle(.plain)
                if Launch.plus {
                Divider().padding(.leading, 48)
                LockedRow(feature: .seasonAlerts, lockGlyph: false) {
                    HStack(spacing: 12) {
                        Image(systemName: "bell").frame(width: 20).foregroundStyle(Brand.moss)
                        Text("Season alerts").font(.callout).foregroundStyle(Brand.ink)
                        Spacer()
                        // "Coming soon" beside the tier, because the tier is not
                        // open (Hidde, 2026-08-25: "bij offline maps en season
                        // alerts mag je coming soon plus zetten"). A bare Plus
                        // chip on a row that cannot be bought reads as a thing
                        // you are missing out on rather than a thing being built.
                        Text("Coming soon").font(.caption).foregroundStyle(Brand.inkSoft)
                        Chip(text: "Plus", tint: Brand.gold)
                    }
                    .padding(.horizontal, 16).frame(height: 48)
                }
                Divider().padding(.leading, 48)
                // Offline sits under Plus with the alerts, which is where he
                // put it on 2026-08-25 ("je zou offline maps bij season alert
                // kunnen zetten, dat het ook onder plus valt"). It is a row
                // rather than a switch because there is nothing to switch on
                // yet: tapping says so and counts that you asked.
                LockedRow(feature: .offlineDownload, lockGlyph: false) {
                    HStack(spacing: 12) {
                        Image(systemName: "arrow.down.circle")
                            .frame(width: 20).foregroundStyle(Brand.moss)
                        Text("Offline maps").font(.callout).foregroundStyle(Brand.ink)
                        Spacer()
                        Text("Coming soon").font(.caption).foregroundStyle(Brand.inkSoft)
                        Chip(text: "Plus", tint: Brand.gold)
                    }
                    .padding(.horizontal, 16).frame(height: 48)
                }
                }
                // The "What Plus will be" row is gone (Hidde, 2026-08-25: "je
                // mag de what is plus sectie in het profiel weghalen"). It was
                // a page whose whole content was a list of things that do not
                // exist yet, one tap from two rows that say the same in three
                // words each.
                Divider().padding(.leading, 48)
                // The Sponsor row is GONE, and so is the in-app purchase
                // behind it (Hidde, 2026-08-29: "haal er maar uit tenzij we
                // naar de website mogen verwijzen om het daar te doen"). We
                // may not: guideline 3.1.1 does not let an app link out to
                // ko-fi for a tip, the registered-nonprofit exception is not
                // ours, and the places where linking out IS allowed are one
                // storefront (US) and one paid entitlement (EU), which is not
                // one button shipped worldwide. The website keeps /sponsor.
                // HIS ASK, 2026-08-26: a general feedback button, and under
                // it specifically the features people would want. The open
                // answers are the material the Plus line gets designed from,
                // which beats any list we invent (drafts/PLUS_THINKING.md).
                // The same editor the name on My trees opens. Two doors to
                // one room, and he asked for both ("ook op profielpagina moet
                // je je profielfoto etc aan kunnen passen, prima als dat dubbel
                // is"): settings is where somebody looks for a thing about
                // themselves, and the name on the page is where somebody
                // notices it is wrong.
                Button { editingProfile = true } label: {
                    HStack(spacing: 12) {
                        Image(systemName: "person.crop.circle").frame(width: 20)
                            .foregroundStyle(Brand.moss)
                        Text("Your name and picture").font(.callout)
                            .foregroundStyle(Brand.ink)
                        Spacer()
                        Image(systemName: "chevron.right")
                            .font(.caption).foregroundStyle(Brand.inkSoft.opacity(0.6))
                    }
                    .padding(.horizontal, 16).frame(height: 48)
                    .contentShape(.rect)
                }
                .buttonStyle(.plain)
                .accessibilityIdentifier("settings-edit-profile")
                Divider().padding(.leading, 48)
                Button { givingFeedback = true } label: {
                    HStack(spacing: 12) {
                        Image(systemName: "bubble.left.fill").frame(width: 20)
                            .foregroundStyle(Brand.moss)
                        Text("Send feedback").font(.callout)
                            .foregroundStyle(Brand.ink)
                        Spacer()
                        Image(systemName: "chevron.right")
                            .font(.caption).foregroundStyle(Brand.inkSoft.opacity(0.6))
                    }
                    .padding(.horizontal, 16).frame(height: 48)
                    .contentShape(.rect)
                }
                .buttonStyle(.plain)
                .accessibilityIdentifier("profile-feedback")
            }
            .brandCard()
        }
    }

    // MARK: - about

    private var aboutCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("About").font(.eyebrow).textCase(.uppercase)
                .foregroundStyle(Brand.inkSoft).tracking(0.8)
                // No inset. It put SETTINGS and ABOUT at 20 while every card
                // under them sits at 16, which appfit reads as a drift and a
                // reader reads as sloppy without being able to name it.
            VStack(spacing: 0) {
                link("Privacy", "lock", "https://ancienttrees.app/privacy")
                Divider().padding(.leading, 48)
                // The map credit lives one level down now (Hidde, 2026-08-25:
                // "zet het in de legal rij zo ver mogelijk weg"). It used to
                // be a row of its own, the same weight as Privacy, which is
                // more than a tile credit has ever earned on anybody's profile
                // screen.
                //
                // It cannot simply go: OpenFreeMap serve these tiles from
                // OpenStreetMap data and the ODbL asks for the credit. What
                // the licence wants is that somebody looking for it finds it,
                // which is exactly what Apple Maps' Legal Notices and every
                // Mapbox app's info button do. A Legal row is the convention
                // and the furthest away this can honestly sit.
                Button { showingLegal = true } label: {
                    HStack(spacing: 12) {
                        Image(systemName: "doc.text").frame(width: 20)
                            .foregroundStyle(Brand.moss)
                        Text("Legal").font(.callout).foregroundStyle(Brand.ink)
                        Spacer()
                        Image(systemName: "chevron.right")
                            .font(.caption).foregroundStyle(Brand.inkSoft.opacity(0.6))
                    }
                    .padding(.horizontal, 16).frame(height: 48)
                    .contentShape(.rect)
                }
                .buttonStyle(.plain)
                Divider().padding(.leading, 48)
            }
            .brandCard()
        }
    }

    /// The credits, in the same words the website's own footer uses, because a
    /// person who checks both should not find two different answers about who
    /// made the map.
    private var legalSheet: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 18) {
                    VStack(alignment: .leading, spacing: 6) {
                        Text("The map").font(.cardTitle).foregroundStyle(Brand.ink)
                        Text("Map © OpenFreeMap, OpenMapTiles, OpenStreetMap contributors. Walking routes by Valhalla via FOSSGIS, on OpenStreetMap data.")
                            .font(.footnote).foregroundStyle(Brand.inkSoft)
                            .fixedSize(horizontal: false, vertical: true)
                        Link("OpenStreetMap copyright",
                             destination: URL(string: "https://www.openstreetmap.org/copyright")!)
                            .font(.footnote.weight(.semibold))
                            .foregroundStyle(Brand.moss)
                    }
                    VStack(alignment: .leading, spacing: 6) {
                        Text("Photographs").font(.cardTitle).foregroundStyle(Brand.ink)
                        Text("Every photograph carries its own credit and open licence, named on the tree's own page.")
                            .font(.footnote).foregroundStyle(Brand.inkSoft)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                    VStack(alignment: .leading, spacing: 6) {
                        Text("The rest").font(.cardTitle).foregroundStyle(Brand.ink)
                        Link("Terms", destination: URL(string: "https://ancienttrees.app/terms")!)
                            .font(.footnote.weight(.semibold)).foregroundStyle(Brand.moss)
                        Link("Privacy", destination: URL(string: "https://ancienttrees.app/privacy")!)
                            .font(.footnote.weight(.semibold)).foregroundStyle(Brand.moss)
                    }
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(20)
            }
            .brandGround()
            .navigationTitle("Legal")
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { showingLegal = false }
                }
            }
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

    /// The build, said out loud.
    ///
    /// It costs one line and it ends a whole class of wasted work. Twice now a
    /// morning has gone on bugs that were already fixed, because the phone in
    /// his hand was running the build he installed hours earlier and nothing on
    /// any screen said so (LOG.md 2026-08-25: "three of tonight's reports were
    /// things fixed thirty minutes earlier"). A report is only worth as much as
    /// the version it came from, and until now nobody could name that version.
    private var buildLine: String {
        let info = Bundle.main.infoDictionary
        let v = info?["CFBundleShortVersionString"] as? String ?? "?"
        let b = info?["CFBundleVersion"] as? String ?? "?"
        // The DATE is the part that does the work. CFBundleVersion is 1 and
        // stays 1 until somebody remembers to bump it, so on its own the line
        // would read "Version 1.0 (1)" on every build ever made and answer
        // nothing. The executable's own modification time changes every single
        // compile without anybody maintaining it.
        var when = ""
        if let exe = Bundle.main.executableURL,
           let at = try? FileManager.default.attributesOfItem(atPath: exe.path),
           let date = at[.modificationDate] as? Date {
            let f = DateFormatter()
            f.locale = Locale(identifier: "en_GB")
            f.dateFormat = "d MMM HH:mm"
            when = " · built " + f.string(from: date)
        }
        return "Version \(v) (\(b))" + when
    }

    private var version: some View {
        VStack(spacing: 2) {
            Text("\(catalogue.trees.count.formatted(.number.locale(Locale(identifier: "en_US")))) trees, updated whenever you open the app.")
            Text(buildLine).accessibilityIdentifier("build-line")
        }
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
                // "Nothing else" until 2026-08-28, and by then it was wrong on
                // four counts: a display name, a profile picture, who you
                // follow, and every tree you have photographed with the place
                // it stands. Hidde asked for a sweep of old promises after
                // catching the location one, and this was the worst of them,
                // because it stands on the screen where somebody decides
                // whether to trust us with any of it.
                Text("We hold your email address, the name and picture you chose, and the trees you have saved, collected and photographed. You can delete all of it from this screen.")
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
            // ON THE BUTTON, not on the page. iOS anchors a confirmation to
            // whatever it is attached to, so attaching this to the whole screen
            // put it up near the top with an arrow pointing at nothing (Hidde,
            // 2026-08-27: "het scherm zit op een random plek, wat is conventie?
            // je zou m eerder bij de knop zelf doen"). The convention is that a
            // confirmation belongs to the control it came from, which is also
            // how the ellipsis on a person already behaves.
            //
            // Signing out went through on the first tap, while deleting the
            // account two rows above asked first. Every app asks (Hidde,
            // 2026-08-24: "dit is raar"), and here it matters more than usual:
            // what it looks like you are about to lose is your collection.
            // CANCEL WITHOUT THE CANCEL ROLE, and that is not a style choice.
            //
            // Anchored to a control, iOS 26 draws this as a popover, and a
            // popover DROPS every button carrying `role: .cancel`, because
            // tapping outside is meant to do that job. So the Cancel declared
            // here never drew and the only control on a destructive
            // confirmation was the red one: somebody who opened it by mistake
            // had nothing to tap. Found on 2026-08-27 by the flow walk, which
            // had been failing on exactly this for days while nothing read its
            // verdict. A plain button says the same word and survives.
            .confirmationDialog("Sign out?", isPresented: $confirmingSignOut,
                                titleVisibility: .visible) {
                Button("Sign out", role: .destructive) {
                    // THE QUEUE GOES UP BEFORE THE DOOR SHUTS. Signing out is
                    // the last moment a valid token exists, and anything not
                    // yet at the account is about to become the only copy
                    // there is. Pushing here is what makes the clearing that
                    // follows lossless rather than merely tidy.
                    Task {
                        await SightingSync.pushAll(account: account, sightings: sightings)
                        account.signOut()
                    }
                }
                Button("Cancel") { confirmingSignOut = false }
            } message: {
                Text("Your collection stays in your account. Sign in again on any phone and it comes back.")
            }
        }
    }
}
