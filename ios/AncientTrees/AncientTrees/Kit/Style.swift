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
    public static let ground = Color(light: 0xFFFFFF, dark: 0x14180F)
    /// A card, a sheet, anything sitting on the ground; on the white ground
    /// the card shadow does the separating, the AllTrails way.
    public static let surface = Color(light: 0xFFFFFF, dark: 0x1E241A)
    /// A quieter surface, for a row inside a card. Neutral grey, not cream,
    /// same ruling as the ground.
    public static let surfaceMuted = Color(light: 0xF2F2F2, dark: 0x262D20)
    public static let ink = Color(light: 0x26301E, dark: 0xECEFE4)
    public static let inkSoft = Color(light: 0x5C6350, dark: 0xA3AC93)
    /// The one colour that means "press this".
    public static let moss = Color(light: 0x4A6B2A, dark: 0x86A34D)
    public static let canopy = Color(light: 0x3A5222, dark: 0x5B7F35)
    /// Reserved for the season badge, so "at its best now" stays scarce.
    public static let gold = Color(light: 0xD9A13F, dark: 0xE0B463)
    public static let hairline = Color(light: 0xE6E6E6, dark: 0x333B29)
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
    public static func register() {
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
    static var screenTitle: Font { .brand(34, .black, relativeTo: .largeTitle) }
    /// The header over a shelf of cards.
    static var shelfTitle: Font { .brand(22, .heavy, relativeTo: .title2) }
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
            .font(.brand(17, .bold, relativeTo: .headline))
            .foregroundStyle(prominent ? Color.white : Brand.moss)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 15)
            .background(prominent ? Brand.moss : Brand.surface, in: .capsule)
            .overlay {
                if !prominent { Capsule().strokeBorder(Brand.moss.opacity(0.35), lineWidth: 1.5) }
            }
            .opacity(configuration.isPressed ? 0.82 : 1)
            .scaleEffect(configuration.isPressed ? 0.985 : 1)
            .animation(.easeOut(duration: 0.12), value: configuration.isPressed)
    }
}

extension View {
    /// A card: a white surface on the cream ground, with a shadow soft enough to
    /// lift it rather than to announce itself.
    func brandCard(_ radius: CGFloat = 16) -> some View {
        self.background(Brand.surface, in: .rect(cornerRadius: radius))
            .shadow(color: .black.opacity(0.07), radius: 8, y: 3)
    }

    /// The ground under a whole screen.
    func brandGround() -> some View {
        self.background(Brand.ground.ignoresSafeArea())
    }
}

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

    public var body: some View {
        HStack(alignment: .firstTextBaseline) {
            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.shelfTitle)
                    .foregroundStyle(Brand.ink)
                if let subtitle {
                    Text(subtitle)
                        .font(.footnote)
                        .foregroundStyle(Brand.inkSoft)
                }
            }
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
