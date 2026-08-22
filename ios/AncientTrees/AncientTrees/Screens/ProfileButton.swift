// The way to your profile, in the corner rather than in the bar.
//
// Hidde, 2026-08-22, with two Komoot screenshots: they keep a small pill top
// right holding a bell and an avatar, and their bar is four tabs. Ours was
// five, and the fifth was the screen people open twice a year. Four tabs is
// more focus on the things that are the product.

import SwiftUI

struct ProfileButton: View {
    @Environment(Account.self) private var account

    var body: some View {
        NavigationLink(value: Route.profile) {
            ZStack {
                Circle().fill(Brand.surfaceMuted)
                if account.isSignedIn {
                    Text(String((account.email ?? "?").prefix(1)).uppercased())
                        .font(.brand(15, .bold)).foregroundStyle(Brand.moss)
                } else {
                    Image(systemName: "person")
                        .font(.system(size: 15, weight: .medium))
                        .foregroundStyle(Brand.inkSoft)
                }
            }
            .frame(width: 32, height: 32)
            .frame(width: 44, height: 44)
            .contentShape(.rect)
        }
        .accessibilityLabel("Your profile")
        .accessibilityIdentifier("profile-button")
    }
}
