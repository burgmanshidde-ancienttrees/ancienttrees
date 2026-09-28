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
    /// The tree somebody tapped the camera on, when they came from one
    /// (Hidde, 2026-09-04: "als je vanuit een boom op de camera knop klikt is
    /// de boodschap iets anders dan wil je iets zeggen als voeg deze boom toe
    /// aan je collectie door er een foto van te maken").
    ///
    /// He is right that the general line is wrong there. "Build your tree
    /// collection" is an invitation, which is what somebody pressing the middle
    /// button needs; somebody who tapped the camera on Old Tjikko has already
    /// accepted the invitation and wants to know what this button does to THIS
    /// tree. Same sheet, same flow, different first sentence.
    var about: String? = nil
    /// Came in from the tree's missing photograph: the sheet is about adding
    /// a photo, so it says that and nothing about collecting.
    var addsPhoto = false
    var onStart: () -> Void
    /// The camera roll, added 2026-08-28. Convention: iNaturalist, where the
    /// gallery is an ordinary route and not a fallback, reachable both by long
    /// pressing the camera button and as a visible choice. A long press alone
    /// is invisible, so this is the visible half and the press is the shortcut.
    var onLibrary: () -> Void = {}
    /// The sheet's close button, drawn on the title row (Hidde, 2026-09-28:
    /// "the x is placed wrongly"). Apple Maps and the iOS 26 system sheets put
    /// the close control at the trailing end of the TITLE, on the content's
    /// own margin, never in a row of its own above it.
    var close: AnyView? = nil

    var body: some View {
        VStack(alignment: .leading, spacing: 24) {
            // THE TITLE SAYS WHAT YOU ARE DOING, and nothing else (Hidde,
            // 2026-09-27: "I'm really not happy with the copy here"). The
            // buttons that open this sheet say "Add a tree", and a sheet that
            // answers them with "Build your tree collection" and a sentence
            // about collections talks past the person who pressed it.
            HStack(alignment: .center, spacing: 12) {
                Text(addsPhoto ? "Add a photo"
                     : about == nil ? "Add a tree"
                     : "Add this tree")
                    .font(.brand(28, .bold, relativeTo: .title))
                    .foregroundStyle(Brand.ink)
                    .fixedSize(horizontal: false, vertical: true)
                    .frame(maxWidth: .infinity, alignment: .leading)
                close
            }

            // ONE LINE, AND IT IS BACK ON PURPOSE (Hidde, 2026-08-29: "ik denk
            // dat deze toch een onderregel nodig heeft om wat meer uit te
            // leggen wat je gaat doen").
            //
            // It was removed on 2026-08-28, on his call, and the reason it went
            // is the reason this one is worded the way it is. The line before it
            // promised we would tell you WHICH tree it is, and that stopped
            // being true for a photograph off the camera roll within the hour.
            // The one before that explained our side of the deal, which rule 6
            // of PRODUCT_COPY.md forbids at the moment somebody is deciding to
            // act.
            //
            // So this says the one thing that is true of both routes and cannot
            // stop being true: you take a picture, and it is yours. It is the
            // file's own worked example, not a new sentence.
            // Named, and the reader is the subject joined with "by", which is
            // PRODUCT_COPY.md's own shape. The general line stays exactly as it
            // was for every other way in.
            // No second line: the two buttons below say how.

            // 24 between the title and the buttons, fixed rather than a
            // Spacer: the sheet is sized to fit, so a Spacer only ever grew
            // into the gap Hidde saw on 2026-09-28 ("the vertical spacing in
            // the pop-up seems off").
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

                // No footnote about whose photographs we can use (Hidde,
                // 2026-09-27: "do we need to say it otherwise less is more").
                // It told an honest person something they already do and
                // stopped nobody else; the viewing pass checks every picture.
            }
        }
    }
}
