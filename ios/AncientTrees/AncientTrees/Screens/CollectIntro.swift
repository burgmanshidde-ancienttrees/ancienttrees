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
                // 22 under the title, not 14 (Hidde, 2026-08-25: "the spacing
                // between collect a tree title and the rest is too little,
                // please verify whats convention"). It is: Apple's own sheets
                // set a large title and then leave roughly 20 to 24 points
                // before the body, which is about the title's own cap height.
                // 14 is the spacing BETWEEN two paragraphs, and using it here
                // made the title read as the first line of the text.
                .padding(.bottom, 8)

            // TWO THINGS, each with its own mark, which is his own structure
            // (Hidde, 2026-08-25, giving both sentences): one paragraph had to
            // carry collecting a tree we map AND adding one we do not, and the
            // second half arrived as a clause tacked onto the first ("if we do
            // not have it, it is yours, and it reaches us too"). They are two
            // different things somebody might be about to do.
            //
            // PRODUCT_COPY.md governs the wording: the reader is the subject,
            // the method is joined with "by", and there is no summary line. His
            // own draft said "if review succesfully added to the database for
            // all", and rule 5 is why that is not what it says here: nobody
            // needs the word database, they need to know it joins the map
            // everybody sees.
            VStack(alignment: .leading, spacing: 18) {
                line("checkmark.seal",
                     "You can collect a tree by photographing it while you stand in front of it. We tell you which one it is and tick it off.")
                line("plus.circle",
                     "If it is a tree we do not have, you can add it. It appears on your own map straight away, and once we have checked it, it joins the map everybody sees.")
            }

            Spacer(minLength: 24)

            Button("Take a photo", action: onStart)
                .buttonStyle(BrandButtonStyle())
                .accessibilityIdentifier("add-start")
        }
        .frame(maxHeight: .infinity, alignment: .top)
        .padding(.top, 8)
    }

    private func line(_ icon: String, _ text: String) -> some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 19))
                .foregroundStyle(Brand.moss)
                .frame(width: 24)
            Text(text)
                .font(.system(size: 17))
                .foregroundStyle(Brand.inkSoft)
                .lineSpacing(3)
                .fixedSize(horizontal: false, vertical: true)
        }
    }
}
