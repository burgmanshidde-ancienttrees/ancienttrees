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
//
// AND ON 2026-08-28 IT STOPPED NAMING THEM. Hidde: "slaat collect nog wel
// ergens op want je hebt my trees... hoe leggen we makkelijk uit dat je fotos
// van bestaande bomen kan toevoegen en ze zo spaart en dat je nieuwe bomen kan
// toevoegen. Of is dat gewoon te complex."
//
// It is, and the reason is the one CollectSheet already wrote down: what
// separates the two cases is not something the person does, it is something
// only our database knows. Two lines teaching that distinction ask somebody to
// hold a difference that has no consequence for their next action, before
// anything has happened. Seek is the reference and does not do it: you point
// the camera and it tells you what you found.
//
// So one line, and it is the example PRODUCT_COPY.md's own rule 6 gives.
// "Your tree collection" rather than "your trees" is his (2026-08-28): the tab
// that holds them is called My trees, and somebody opening this screen for the
// first time has never seen it, so "your trees" points at nothing while a
// collection explains itself.
//
// The title says what you DO. "Collect a tree" was an outcome, and an outcome
// is the one thing this flow deliberately does not decide up front.

import SwiftUI

struct CollectIntro: View {
    var onStart: () -> Void
    /// The camera roll, added 2026-08-28. Convention: iNaturalist, where the
    /// gallery is an ordinary route and not a fallback, reachable both by long
    /// pressing the camera button and as a visible choice. A long press alone
    /// is invisible, so this is the visible half and the press is the shortcut.
    var onLibrary: () -> Void = {}

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text("Build your tree collection")
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

            // NO SENTENCE AT ALL, his call of 2026-08-28 between the two
            // honest options. Two lines that explained our side of the deal
            // went first (rule 6: not at the moment somebody is deciding to
            // act), and the one that replaced them repeated "tree collection"
            // under a title that had just said it, which is what he caught:
            // "de copy is still quite bad".
            //
            // So the title says what you get, the two buttons say how, and
            // there is nothing left that can go stale. The previous line could
            // and did: it promised we would tell you which tree it is, and
            // that stopped being true for a photograph off the camera roll
            // within the hour of it being written.

            Spacer(minLength: 24)

            VStack(spacing: 10) {
                Button("Take a photo", action: onStart)
                    .buttonStyle(BrandButtonStyle())
                    .accessibilityIdentifier("add-start")
                    // The shortcut iNaturalist puts on its camera button. It
                    // is a second way in and never the only one.
                    .onLongPressGesture(perform: onLibrary)

                // The label carries the frame and the shape, not the Button:
                // a plain Button reports its TEXT as the tappable thing, which
                // is how this shipped 18 points tall past a green build. The
                // layout gate measured it within the hour.
                Button(action: onLibrary) {
                    Text("Choose from your photos")
                        .font(.brand(16, .bold))
                        .foregroundStyle(Brand.moss)
                        .frame(maxWidth: .infinity, minHeight: 44)
                        .contentShape(.rect)
                }
                .buttonStyle(.plain)
                .accessibilityIdentifier("add-library")
            }
        }
        .frame(maxHeight: .infinity, alignment: .top)
        .padding(.top, 8)
    }
}
