// The app's own look, because it did not have one.
//
// Hidde, 2026-08-20, on running it: "it feels like im looking at apple
// settings". He is right and it is diagnosable rather than a matter of taste.
// Three things make an iOS app read as Settings, and this app was doing all
// three: `List` in its default inset-grouped style, `Color(.systemGroupedBackground)`
// as the ground, and San Francisco at system sizes for every word on screen.
// Those are Apple's defaults, they are excellent defaults, and they are why a
// screen built from them looks like a system screen rather than like a product.
//
// What replaces them comes from two places and nothing is invented here:
//
// THE SITE. ancienttrees.app already has an identity: cream ground, moss green,
// a warm near-black ink, a gold accent, and Gabarito as the typeface. The app
// was ignoring all of it, which is also why the two products did not look
// related. Gabarito ships in the bundle under its OFL licence, the same file
// the website serves.
//
// ALLTRAILS, for the structure rather than the colour, per the teardown: cards
// with the photograph doing the work, one filled green primary action and never
// two, a stat row with its units labelled underneath, and section headers that
// are large and bold rather than small and grey. Their green is theirs; ours is
// the moss the website has used since July.
//
// The body face stays San Francisco on purpose. Gabarito is a display face and
// a two hundred word story set in it is worse to read, so the pairing is
// Gabarito for anything you scan and the system face for anything you read.

import SwiftUI
import CoreText

// MARK: - Colour

public enum Brand {
    /// The ground. WHITE, ruled by Hidde 2026-08-20 evening: "ik heb nog nooit
    /// een app met een vieze achtergrond kleur gezien kijk aub af naar
    /// conventies en stop met dingen verzinnen." The site's cream is the
    /// site's; every reference app (AllTrails, Komoot, Airbnb, Google Maps)
    /// stands on white, and transplanting the web ground here read as dirty
    /// rather than warm. The identity lives in moss, gold, ink and Gabarito,
    /// not in tinting the page.
    public static let ground = Color(light: 0xFFFFFF, dark: 0x121410)
    /// A card, a sheet, anything sitting on the ground; on the white ground
    /// the card shadow does the separating, the AllTrails way.
    public static let surface = Color(light: 0xFFFFFF, dark: 0x1D211B)
    /// A quieter surface, for a row inside a card. Neutral grey, not cream,
    /// same ruling as the ground.
    public static let surfaceMuted = Color(light: 0xF2F2F2, dark: 0x262A24)
    public static let ink = Color(light: 0x26301E, dark: 0xECEFE4)
    public static let inkSoft = Color(light: 0x5C6350, dark: 0xA7AE9E)
    /// The one colour that means "press this".
    ///
    /// LIGHTER IN THE DARK, and that is the convention rather than a taste. A
    /// dark theme's accent is taken from the light end of a ramp (Material puts
    /// it at tone 200; Google's own dark products press in #8AB4F8 rather than
    /// in their daylight blue), because a mid-tone green on a near-black ground
    /// has too little contrast to read as a control.
    public static let moss = Color(light: 0x4A6B2A, dark: 0x96B863)
    /// The deeper green, and it goes DARKER in the dark where moss goes
    /// lighter, because the two are used for opposite jobs. Moss is a control
    /// and has to stand out; canopy is a fill behind white text (the "Seen"
    /// badge, an active filter, the tile a tree with no photograph wears) and
    /// has to sit back. It was lighter than the light value for a while and
    /// white on it measured 3.67:1.
    public static let canopy = Color(light: 0x3A5222, dark: 0x33491F)
    /// Reserved for the season badge, so "at its best now" stays scarce.
    public static let gold = Color(light: 0xD9A13F, dark: 0xE0B463)
    /// The same gold, WRITTEN rather than filled.
    ///
    /// Found by scripts/darkcheck.py on the day it was written, and it is a
    /// daylight fault rather than a dark one: the Plus chip and the season line
    /// set gold as text, and gold on white measures 2.30:1, half of what small
    /// text needs. In the dark the ordinary gold is already 8.5:1 on a card, so
    /// only the light value moves and the badge keeps the colour it has.
    public static let goldInk = Color(light: 0x8F6210, dark: 0xE0B463)
    public static let hairline = Color(light: 0xE6E6E6, dark: 0x363B31)
    /// What is WRITTEN on a filled moss control, which is not white in the dark.
    ///
    /// This is the other half of the rule above and the two only work together.
    /// A light accent takes dark text: white on the dark palette's moss measured
    /// 2.85:1, under half the 4.5:1 a body of text needs, and it looked it. It
    /// was the loudest thing on the tree page and on the camera sheet, a
    /// highlighter slab with pale text on it. Dark ink on the same green is
    /// 8.9:1. Material's dark FAB and Google Maps' own dark buttons both do
    /// exactly this: light fill, dark label.
    public static let onMoss = Color(light: 0xFFFFFF, dark: 0x10160A)
}

extension Color {
    /// One hex per appearance. UIColor rather than a colour set because the
    /// asset catalogue would put these somewhere nobody reads them, and the
    /// palette belongs next to the reasoning for it.
    init(light: UInt32, dark: UInt32) {
        self = Color(UIColor { $0.userInterfaceStyle == .dark
            ? UIColor(hex: dark) : UIColor(hex: light) })
    }
}

extension UIColor {
    convenience init(hex: UInt32) {
        self.init(red: CGFloat((hex >> 16) & 0xFF) / 255,
                  green: CGFloat((hex >> 8) & 0xFF) / 255,
                  blue: CGFloat(hex & 0xFF) / 255,
                  alpha: 1)
    }
}

// MARK: - Type

public enum BrandFont {
    /// Registered at launch rather than declared in Info.plist, because the
    /// project generates its plist from build settings and UIAppFonts has no
    /// build setting. Registering from the bundle is the ordinary way out.
    private static var registered = false

    /// Idempotent, because this is now called from two places: the app's init,
    /// which is where it has to happen for the FIRST frame to be set in the
    /// brand face, and configureAppearance, which is where it used to live
    /// alone. Registering the same file twice logs an error and does nothing
    /// useful, so it is asked once.
    public static func register() {
        guard !registered else { return }
        registered = true
        for name in ["Gabarito-Regular", "Gabarito-Medium", "Gabarito-Bold",
                     "Gabarito-ExtraBold", "Gabarito-Black"] {
            guard let url = Bundle.main.url(forResource: name, withExtension: "ttf") else { continue }
            CTFontManagerRegisterFontsForURL(url as CFURL, .process, nil)
        }
    }
}

extension Font {
    /// The display face, scaled by the reader's text size like any system font.
    static func brand(_ size: CGFloat, _ weight: Weight = .bold,
                      relativeTo style: TextStyle = .body) -> Font {
        let face: String
        switch weight {
        case .black: face = "Gabarito-Black"
        case .heavy: face = "Gabarito-ExtraBold"
        case .bold, .semibold: face = "Gabarito-Bold"
        case .medium: face = "Gabarito-Medium"
        default: face = "Gabarito-Regular"
        }
        return .custom(face, size: size, relativeTo: style)
    }

    /// A screen's own name, the biggest thing on it.
    static var screenTitle: Font { .brand(32, .bold, relativeTo: .largeTitle) }
    /// The header over a shelf of cards.
    static var shelfTitle: Font { .brand(21, .bold, relativeTo: .title2) }
    /// A card's name.
    static var cardTitle: Font { .brand(17, .bold, relativeTo: .headline) }
    /// A small uppercase label, the way the website sets its eyebrows.
    static var eyebrow: Font { .brand(11, .bold, relativeTo: .caption2) }
}

// MARK: - Pieces

/// The one filled control. AllTrails colours exactly one thing on any screen and
/// it is always the verb; this is that thing.
public struct BrandButtonStyle: ButtonStyle {
    var prominent = true

    public func makeBody(configuration: Configuration) -> some View {
        configuration.label
            // The system face at semibold, not the display face at black.
            // Gabarito Black is a poster weight: on a button it reads as
            // shouting, which is most of why the old control looked heavy
            // (Hidde, 2026-08-22).
            .font(.system(size: 16, weight: .semibold))
            .foregroundStyle(prominent ? Brand.onMoss : Brand.ink)
            .frame(maxWidth: .infinity)
            .frame(height: 54)
            // A ROUNDED RECTANGLE rather than a capsule. Airbnb, Booking and
            // every checkout on a phone use a 12 point radius; a full capsule
            // at this width is a lozenge, and a lozenge is the shape of an
            // advert.
            .background(prominent ? Brand.moss : Brand.surface,
                        in: .rect(cornerRadius: 12))
            .overlay {
                if !prominent {
                    RoundedRectangle(cornerRadius: 12)
                        .strokeBorder(Brand.ink.opacity(0.22), lineWidth: 1)
                }
            }
            .opacity(configuration.isPressed ? 0.85 : 1)
            .animation(.easeOut(duration: 0.12), value: configuration.isPressed)
    }
}

extension View {
    /// A card: a white surface on the cream ground, with a shadow soft enough to
    /// lift it rather than to announce itself.
    func brandCard(_ radius: CGFloat = 12) -> some View {
        // CLIPPED first, and it is the whole reason this line exists. A card
        // painted a rounded background and a rounded border and then let its
        // own content ignore both, so every card with a photograph at the top
        // had the photograph running square through the two top corners:
        // Explore's cards, the Home shelf, and the card for a tree you added
        // yourself (Hidde, 2026-08-25, who found all three at once and was
        // right that I should have caught it). One clip here fixes every card,
        // which is also why the bug reached three screens.
        self.clipShape(.rect(cornerRadius: radius))
            .background(Brand.surface, in: .rect(cornerRadius: radius))
            .overlay {
                RoundedRectangle(cornerRadius: radius)
                    .strokeBorder(Brand.hairline, lineWidth: 1)
            }
    }

    /// The ground under a whole screen.
    func brandGround() -> some View {
        self.background(Brand.ground.ignoresSafeArea())
    }
}

/// The tile a tree or a city with no photograph wears.
///
/// ONE gradient rather than one per screen, which is the shared-component rule
/// in CLAUDE.md applied to a thing that was written out three times: the card,
/// the city shelf and the tree page each had their own greens, and when the
/// dark palette arrived two of the three came out as a lit slab the size of a
/// photograph while the third had already been made neutral.
///
/// It stays GREEN in the dark rather than going grey, because in a shelf the
/// green tile with a species drawn on it is how a tree with no photograph is
/// told apart from one whose picture has not loaded yet. It is simply dark
/// enough to be a tile rather than the brightest thing on the page, which is
/// Material's dark-theme rule for decorative imagery.
public let leafTile = LinearGradient(colors: [Color(light: 0x3A5222, dark: 0x2A3A1C),
                            Color(light: 0x597A4D, dark: 0x1E2A16)],
                   startPoint: .topLeading, endPoint: .bottomTrailing)

/// The header over a shelf. Large and bold, with the count doing the work a
/// subtitle would: AllTrails writes "347 routes" and it tells you more than a
/// sentence would.
public struct ShelfHeader: View {
    let title: String
    var subtitle: String? = nil
    var trailing: String? = nil
    var action: (() -> Void)? = nil
    /// The "see all" behind the shelf. A value rather than a closure so a
    /// header can push onto the tab's own stack without every caller wiring
    /// navigation by hand.
    var more: Route? = nil

    /// The title and "See all" share ONE line, and a subtitle sits under the
    /// whole row rather than beside it.
    ///
    /// It used to nest the subtitle in a column next to the link, so a
    /// two-line sentence pushed "See all" off the title's baseline and the
    /// header stopped looking left-aligned (Hidde, 2026-08-22). Netflix,
    /// AllTrails and Airbnb all keep the row to one line and the subtitle
    /// short, which is also why the sentences here got shorter.
    public var body: some View {
        VStack(alignment: .leading, spacing: 2) {
            HStack(alignment: .firstTextBaseline) {
                Text(title)
                    .font(.shelfTitle)
                    .foregroundStyle(Brand.ink)
                    .fixedSize(horizontal: false, vertical: true)
                Spacer(minLength: 8)
                if let more {
                    NavigationLink(value: more) {
                        HStack(spacing: 3) {
                            Text("See all").font(.subheadline.weight(.semibold))
                            Image(systemName: "chevron.right").font(.caption2)
                        }
                        .foregroundStyle(Brand.moss)
                        .frame(minHeight: 44)
                        .contentShape(.rect)
                    }
                    .buttonStyle(.plain)
                }
                if let trailing, let action {
                    Button(trailing, action: action)
                        .font(.subheadline.weight(.semibold))
                        .foregroundStyle(Brand.moss)
                }
            }
            if let subtitle {
                Text(subtitle)
                    .font(.footnote)
                    .foregroundStyle(Brand.inkSoft)
                    .lineLimit(1)
            }
        }
        .padding(.horizontal, 16)
    }
}

/// A small pill. Used for a species, an age, a season badge.
public struct Chip: View {
    let text: String
    var tint: Color = Brand.inkSoft
    var filled = false

    public var body: some View {
        Text(text)
            .font(.brand(12, .medium, relativeTo: .caption))
            .foregroundStyle(filled ? .white : tint)
            .padding(.horizontal, 10).padding(.vertical, 5)
            .background(filled ? tint : tint.opacity(0.12), in: .capsule)
    }
}
