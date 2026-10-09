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

    var body: some View {
        // The website's quiet pill, laid out like every button in the sheet:
        // see SignInPill. The four-colour G is untouched, which is what
        // Google's rules protect.
        Button(action: action) {
            SignInPill(title: title, loud: false) { GoogleMark(side: 18) }
        }
        .buttonStyle(.plain)
    }
}

/// ONE LAYOUT FOR EVERY SIGN-IN BUTTON, the website's (.oauth-btn in
/// style.css): 48 tall, the mark 18 wide at the leading edge 22 in, the label
/// centred in the space after it, bold. Hidde, 2026-10-09: "the logos of
/// apple, google and mail are no longer aligned, follow the website design
/// for this and skip the mail logo". They drifted because Apple's stock
/// control centres its mark and words as a unit while ours did not; with one
/// view drawing all three, the marks share a column by construction.
struct SignInPill<Mark: View>: View {
    let title: String
    let loud: Bool
    @ViewBuilder let mark: () -> Mark

    var body: some View {
        HStack(spacing: 10) {
            if Mark.self != EmptyView.self {
                mark().frame(width: 18, height: 18)
            }
            Text(title)
                .font(.brand(17, .bold, relativeTo: .headline))
                .lineLimit(1).minimumScaleFactor(0.8)
                .frame(maxWidth: .infinity)
        }
        .padding(.horizontal, 22)
        .frame(maxWidth: .infinity, minHeight: 48)
        // The website's loud pill is #1B2416; in the dark it turns white,
        // which is also what Apple's own rules ask of its button there.
        .foregroundStyle(loud ? Color(light: 0xFFFFFF, dark: 0x000000) : Brand.ink)
        .background(loud ? Color(light: 0x1B2416, dark: 0xFFFFFF) : Brand.creamDark,
                    in: .capsule)
        .contentShape(.capsule)
    }
}

extension SignInPill where Mark == EmptyView {
    /// No mark at all: the label centres in the whole pill, as the website's
    /// email button does.
    init(title: String, loud: Bool) {
        self.init(title: title, loud: loud) { EmptyView() }
    }
}
