// Google's own sign-in button, to Google's own specification.
//
// The first version of this was a plain bordered pill with the words "Continue
// with Google" and no mark, which Hidde recognised immediately as something he
// had never seen: "deze knop ben ik nog nooit tegengekomen". He is right, and
// the reason I built it that way was a bad trade. I was avoiding drawing
// somebody else's logo badly, and the conclusion I drew from that worry was to
// invent a button instead. Inventing is the worse of the two: a sign-in button
// is the single most convention-bound control in any app, because its whole job
// is to be recognised in a tenth of a second by somebody who has seen it a
// thousand times elsewhere.
//
// His ruling, and it is now a rule rather than a note: "altijd conventies
// volgen geen eigen ideeen."
//
// So this is Google's published button: white ground, a one point #747775
// border, #1F1F1F label, the unaltered four-colour G, and Roboto Medium where it
// exists. Using their mark on a button that signs people into Google is exactly
// what their guidelines are for; drawing a worse one of my own was never the
// safer option, only the more timid one.
//
// Where it departs from their spec, and why, is the note inside body: this
// button never stands alone, it stands under Apple's, and Apple's cannot be
// told where to put anything.

import SwiftUI

/// The four-colour G, as four paths in an 18x18 box. These are Google's own
/// asset geometry rather than a redrawing by eye.
private enum GoogleG {
    static let blue = "M17.64 9.2045c0-.6381-.0573-1.2518-.1636-1.8409H9v3.4814h4.8436c-.2086 1.125-.8427 2.0782-1.7959 2.7164v2.2581h2.9087c1.7018-1.5668 2.6836-3.874 2.6836-6.615z"
    static let green = "M9 18c2.43 0 4.4673-.806 5.9564-2.1805l-2.9087-2.2581c-.8059.54-1.8368.859-3.0477.859-2.344 0-4.3282-1.5831-5.036-3.7104H.9574v2.3318C2.4382 15.9832 5.4818 18 9 18z"
    static let yellow = "M3.964 10.71c-.18-.54-.2822-1.1168-.2822-1.71s.1023-1.17.2823-1.71V4.9582H.9573A8.9965 8.9965 0 0 0 0 9c0 1.4523.3477 2.8268.9573 4.0418L3.964 10.71z"
    static let red = "M9 3.5795c1.3214 0 2.5077.4541 3.4405 1.346l2.5813-2.5814C13.4632.8918 11.426 0 9 0 5.4818 0 2.4382 2.0168.9573 4.9582L3.964 7.29C4.6718 5.1627 6.656 3.5795 9 3.5795z"
}

struct GoogleMark: View {
    var side: CGFloat = 18

    var body: some View {
        Canvas { ctx, size in
            let s = size.width / 18
            let t = CGAffineTransform(scaleX: s, y: s)
            for (d, colour) in [(GoogleG.blue, Color(red: 0.259, green: 0.522, blue: 0.957)),
                                (GoogleG.green, Color(red: 0.204, green: 0.659, blue: 0.325)),
                                (GoogleG.yellow, Color(red: 0.984, green: 0.737, blue: 0.020)),
                                (GoogleG.red, Color(red: 0.918, green: 0.263, blue: 0.208))] {
                ctx.fill(SVG.path("<path d=\"\(d)\"/>").applying(t), with: .color(colour))
            }
        }
        .frame(width: side, height: side)
        .accessibilityHidden(true)
    }
}

struct GoogleSignInButton: View {
    var title = "Continue with Google"
    let action: () -> Void

    @Environment(\.colorScheme) private var scheme

    var body: some View {
        Button(action: action) {
            // MARK AND LABEL AS ONE CENTRED GROUP, because the button beside
            // this one draws itself that way and cannot be told otherwise.
            // SignInWithAppleButton is Apple's own control: it centres its mark
            // and its words together as a unit, and its type size is derived
            // from the button's height. Ours is the only one of the two that
            // can move.
            //
            // Google's guidelines describe a mark at the leading edge with 16
            // points of padding on iOS, and that is what this used to do. It is
            // right in isolation and wrong here, because the result was one
            // mark at the left edge and another near the middle, one line of
            // large type and one of small, on two controls stacked 14 points
            // apart (Hidde, 2026-09-01: "dan moet het apple logo en google logo
            // wel op dezelfde plek uitlijnen en continue met google en apple
            // hetzelfde grote lettertype"). The second time he has had to say
            // these two do not agree; the first was 2026-08-24, when only the
            // label was centred and the mark was left where it is now.
            //
            // What Google's rules actually forbid is altering their mark: "You
            // can't change the size or color of the Google 'G' logo. It must be
            // the standard color version." The four-colour G is untouched, at
            // its own aspect ratio, on white. What moves is our layout around
            // it, which is the part their spec treats as guidance for a button
            // standing on its own rather than one paired with Apple's.
            HStack(spacing: 8) {
                // 15, MEASURED AGAINST THE MARK ABOVE IT rather than taken
                // from Google's own ratio, which would put it at about 26 for
                // a 20 point label. Apple draws its mark 11 points wide here;
                // Google's G at 20 was 19 and read as the heavier of the two
                // buttons, which is the thing being fixed. At 15 it measures 14
                // and the pair reads as a pair. Photographed at 20 and at 15
                // and chosen from the pictures (Hidde, 2026-09-01: "onderste").
                //
                // The mark itself is untouched, which is what Google's rules
                // actually protect: standard four colours, own aspect ratio, on
                // white.
                GoogleMark(side: 15)
                Text(title)
                    // 20 point, matching what Apple's control draws at this
                    // height, rather than Google's web figure of 14. Two labels
                    // at different sizes read as two different kinds of button.
                    // Roboto Medium is Google's face; the system one at the same
                    // weight is the honest substitute rather than shipping a
                    // font download for one label.
                    .font(.system(size: 20, weight: .medium))
            }
            .frame(maxWidth: .infinity)
            .padding(.horizontal, 12)
            .frame(maxWidth: .infinity, minHeight: 52)
            .foregroundStyle(scheme == .dark ? Color(white: 0.89) : Color(red: 0.12, green: 0.12, blue: 0.12))
            .background(scheme == .dark ? Color(red: 0.075, green: 0.086, blue: 0.098) : .white,
                        in: .capsule)
            .overlay {
                Capsule().strokeBorder(scheme == .dark
                                       ? Color(red: 0.54, green: 0.56, blue: 0.58)
                                       : Color(red: 0.455, green: 0.463, blue: 0.459),
                                       lineWidth: 1)
            }
        }
        .buttonStyle(.plain)
    }
}
