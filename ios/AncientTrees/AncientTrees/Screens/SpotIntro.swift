// What the centre button is for, before you use it.
//
// Rebuilt 2026-08-22 on the shape AllTrails and Airbnb both use for a sheet
// that asks you to do something: a short title, one paragraph, a lot of air,
// and ONE primary button where a thumb already is. What went with it was a
// hand-drawn figure in the middle of the screen, which was decoration
// standing between somebody and the thing they came to do.
//
// The button is the app's own BrandButtonStyle rather than a pill built here,
// so the one green control looks the same everywhere it appears.

import SwiftUI

struct AddIntro: View {
    var onStart: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text("Add a tree we do not have")
                .font(.brand(28, .bold, relativeTo: .title))
                .foregroundStyle(Brand.ink)
                .fixedSize(horizontal: false, vertical: true)

            Text("Photograph any tree you want to keep and it joins your own trees. If it is a remarkable old one, tell us: we check every tree, and it can join the map everybody sees.")
                .font(.system(size: 17))
                .foregroundStyle(Brand.inkSoft)
                .lineSpacing(3)
                .fixedSize(horizontal: false, vertical: true)

            Spacer(minLength: 24)

            Button("Add a tree", action: onStart)
                .buttonStyle(BrandButtonStyle())
                .accessibilityIdentifier("add-start")
        }
        .frame(maxHeight: .infinity, alignment: .top)
        .padding(.top, 8)
    }
}
