// Privacy settings: whether anybody can open your profile.
//
// Reference: AllTrails (support.alltrails.com, "Your account privacy options"):
// Profile, the gear, then the row "Privacy Settings", which opens a screen of
// its own; Polarsteps keeps its switch one level down too, under Settings,
// "Account type". CONVENTIONS.md, "A public profile, and the private switch".
// Hidde, 2026-10-19, asking whether the switch belonged at the top of
// Settings: it does not, so Settings carries one row and this is the screen.
//
// One switch, "Public profile", ON is public (Hidde: "Private profile is heel
// negatief"). Turning it on asks first with the one sheet and says what
// becomes visible; turning it off is one tap and asks nothing.

import SwiftUI

struct PrivacySettingsView: View {
    @Environment(Profiles.self) private var profiles
    @Environment(Account.self) private var account
    @Environment(Navigator.self) private var navigator
    @State private var confirmingPublic = false   // -publicask: launchSheet below
    @State private var editingProfile = false

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 8) {
                let isPublic = profiles.myPublic ?? false
                Toggle(isOn: Binding(
                    get: { isPublic },
                    set: { wantPublic in
                        if !wantPublic { setPublic(false) }
                        // A public profile shows a name, and no profile row
                        // exists until somebody sets one, so the name first.
                        else if profiles.me?.display_name.isEmpty ?? true { editingProfile = true }
                        else { confirmingPublic = true }
                    })) {
                    HStack(spacing: 12) {
                        Image(systemName: "globe.europe.africa").frame(width: 20).foregroundStyle(Brand.moss)
                        Text("Public profile").font(.callout).foregroundStyle(Brand.ink)
                    }
                }
                .tint(Brand.moss)
                .padding(.horizontal, 16).frame(minHeight: 48)
                .brandCard()
                .accessibilityIdentifier("profile-public")
                Text(isPublic ? "Anyone can see your profile and your trees." : "Only you see your profile.")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .padding(.horizontal, 16)
                if isPublic, let uid = account.session?.userId {
                    Button("See your public profile") { navigator.push = .person(uid) }
                        .font(.footnote.weight(.semibold)).foregroundStyle(Brand.moss)
                        .padding(.horizontal, 16)
                        .frame(minHeight: 44)
                        .accessibilityIdentifier("profile-public-open")
                }
            }
            .padding(.horizontal, 16).padding(.top, 6)
        }
        .brandGround()
        .navigationTitle("Privacy settings")
        .navigationBarTitleDisplayMode(.inline)
        .launchSheet("-publicask", isPresented: $confirmingPublic)
        .sheet(isPresented: $confirmingPublic) {
            BrandSheet(
                icon: "globe.europe.africa",
                title: "Make your profile public?",
                message: "Anyone can then open it, with or without an account.",
                points: ["Your name and picture",
                         "The trees you collected and want to visit",
                         "Your badges"],
                buttons: [
                    .primary("Make public", id: "public-yes") {
                        confirmingPublic = false
                        setPublic(true)
                    },
                    .quiet("Not now", id: "public-no") { confirmingPublic = false },
                ])
        }
        .sheet(isPresented: $editingProfile) { ProfileEditor() }
    }

    private func setPublic(_ on: Bool) {
        guard let uid = account.session?.userId else { return }
        Task {
            guard let t = await account.freshToken() else { return }
            _ = await profiles.savePublic(on, userId: uid, token: t)
        }
    }
}
