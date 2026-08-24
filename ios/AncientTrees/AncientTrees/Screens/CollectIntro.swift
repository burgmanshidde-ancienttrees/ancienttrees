// What the middle button is for, before you have used it once.
//
// Rebuilt 2026-08-22 on the shape AllTrails and Airbnb both use for a sheet
// that asks you to do something: a short title, one paragraph, a lot of air,
// and ONE primary button where a thumb already is. What went with it was a
// hand-drawn figure in the middle of the screen, which was decoration
// standing between somebody and the thing they came to do.
//
// The copy changed again on 2026-08-23, when add and collect became one act.
// It no longer explains two paths, because there are no longer two: it says
// what to do, and names the two things that can come back.

import SwiftUI

struct CollectIntro: View {
    var onStart: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text("Collect a tree")
                .font(.brand(28, .bold, relativeTo: .title))
                .foregroundStyle(Brand.ink)
                .fixedSize(horizontal: false, vertical: true)

            Text("You can collect a tree by photographing it while you stand in front of it. If it is one of ours, we tell you which and tick it off. If we do not have it, it is yours, and it reaches us too.")
                .font(.system(size: 17))
                .foregroundStyle(Brand.inkSoft)
                .lineSpacing(3)
                .fixedSize(horizontal: false, vertical: true)

            Spacer(minLength: 24)

            Button("Take a photo", action: onStart)
                .buttonStyle(BrandButtonStyle())
                .accessibilityIdentifier("add-start")
        }
        .frame(maxHeight: .infinity, alignment: .top)
        .padding(.top, 8)
    }
}
