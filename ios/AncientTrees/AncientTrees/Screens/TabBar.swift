// The bottom bar, copied from AllTrails rather than designed.
//
// Hidde, 2026-08-24, twice: "kun je deze meer precies zoals alltrails maken"
// and then, after I drew a make-button of my own invention, "please verzin geen
// eigen dingen maar zoek het mooiste voorbeeld en maak het zoveel mogelijk als
// alltrails". So this is his own screenshot, read off:
//
//   - four items, evenly spaced, full width, a hairline along the top
//   - one outline weight for every symbol, nothing filled, nothing heavier
//   - the selected item wears a PILL BEHIND THE ICON ONLY, and its symbol
//     inverts to sit dark on the bright fill
//   - the word sits under the pill, outside it, and is never inside it
//
// iOS draws its own capsule around icon AND label, which is the one thing that
// cannot be reached with the native bar however it is configured, and it is
// also the most visible difference between our bar and his screenshot. Hence a
// bar of our own: not because a custom control is nicer, but because copying
// the reference exactly is what was asked and the native one cannot.

import SwiftUI

struct TabBar: View {
    struct Item {
        /// Empty on the action, which carries no word: see `items`.
        let title: String
        let symbol: String
        /// The one slot that is a DEED rather than a place.
        var action: Bool = false
    }

    /// Same order as the TabView's tags.
    ///
    /// FIVE slots, with the deed in the MIDDLE and no word under it (Hidde,
    /// 2026-08-24: "toch profiel als 5e tab en dan de camera in het midden
    /// zonder tekst eronder omdat het een andere actie is - maar dan wel met
    /// een aparte visuele highlight").
    ///
    /// This is the same control I drew that morning and he rejected, and he was
    /// right then and right now: Instagram, TikTok and YouTube all put it in
    /// the centre of a bar of FIVE, and with four slots there is no centre, so
    /// what was left was an invention wearing a reference as an excuse. The
    /// pattern only transfers with its preconditions, and the fifth tab is the
    /// precondition.
    ///
    /// A camera and never a plus (Hidde, 2026-08-23): a plus promises a row in
    /// a list, a camera says what you are about to do.
    /// THREE PLACES, and the deed is not one of them (Hidde, 2026-08-26:
    /// "Map, discover, my trees en een camera button zoals bij polarsteps los
    /// ... dus 3 iconen samen en dan de camera los want dat is geen pagina
    /// maar een actie").
    ///
    /// The reference is his own Polarsteps screen: a rounded bar holding the
    /// destinations, and a SEPARATE circular button floating beside it. That
    /// separation is the whole argument. A camera in a row of tabs says "a
    /// fourth place to go"; a camera on its own disc says "do this now", and
    /// it is the only control in the app that makes something.
    ///
    /// This replaces the five-slot bar of 2026-08-24, which put the deed in
    /// the middle because Instagram, TikTok and YouTube do. That pattern was
    /// read correctly and its precondition is a bar of five; with three
    /// destinations there is no middle to sit in, and Polarsteps answers the
    /// same problem by taking the button out of the bar entirely.
    static let items = [
        Item(title: "Map", symbol: "map"),
        Item(title: "Discover", symbol: "magnifyingglass"),
        Item(title: "My trees", symbol: "leaf"),
    ]

    /// The tag the camera carries in the TabView, intercepted rather than
    /// shown. It stays 2 so every launch argument and every caller that says
    /// -tab=2 still opens the collect sheet.
    static let collectTag = 3

    let selected: Int
    let select: (Int) -> Void
    /// The pill has to be ONE view that moves, not a different view appearing
    /// in each item, or the change happens by fading two rectangles in and out
    /// (Hidde, 2026-08-26: "de animatie is gek als je over de floating bar van
    /// selectiepagina wisselt, dat heeft volgens mij een standaard ios
    /// animatie die je niet gebruikt"). He is right that there is a standard
    /// one: iOS slides the selection between segments, and matchedGeometry is
    /// how SwiftUI does exactly that.
    @Namespace private var pill
    /// The deed, handed in rather than assumed, because it is not a tab.
    var collect: () -> Void = {}

    var body: some View {
        HStack(spacing: 10) {
            HStack(spacing: 4) {
                ForEach(Array(Self.items.enumerated()), id: \.offset) { i, item in
                    Button {
                        // The slide, and nothing else animated: a tab change
                        // itself is instant on iOS and always has been.
                        withAnimation(.snappy(duration: 0.28)) { select(i) }
                    } label: {
                        VStack(spacing: 3) {
                            Image(systemName: item.symbol)
                                .font(.system(size: 21, weight: .regular))
                                .environment(\.symbolVariants, i == selected ? .fill : .none)
                                .frame(height: 24)
                            Text(item.title)
                                .font(.system(size: 11,
                                              weight: i == selected ? .semibold : .regular))
                                .lineLimit(1)
                        }
                        // MONOCHROME, and that is the reference rather than a
                        // preference (Hidde, 2026-08-26: "flikker op met dat
                        // hele groen, maak het gewoon zwart-wit en zoals zij
                        // doen met dat grijze overlay").
                        .foregroundStyle(i == selected ? Brand.ink : Brand.inkSoft.opacity(0.8))
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        // THE SECOND COLOUR, which is the part he asked for by
                        // name (2026-08-26: "ze hebben een tweede kleur extra
                        // die om het icoon zit naast de fill om aan te geven
                        // waar je zit"). Polarsteps says the selected tab
                        // twice: the glyph fills AND a lighter pill sits
                        // behind the whole item. Filling alone is a small
                        // difference at a glance on a bar this size, and the
                        // pill is what makes it readable without looking.
                        .background {
                            if i == selected {
                                Capsule()
                                    .fill(Brand.ground.opacity(0.92))
                                    .shadow(color: .black.opacity(0.06), radius: 3, y: 1)
                                    .matchedGeometryEffect(id: "tab-pill", in: pill)
                            }
                        }
                        .contentShape(.rect)
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel(item.title)
                    .accessibilityIdentifier("tab-\(item.title.lowercased().replacingOccurrences(of: " ", with: "-"))")
                    .accessibilityAddTraits(i == selected ? [.isSelected, .isButton] : .isButton)
                }
            }
            .padding(4)
            // A GREY BAR, not a white one. `.regularMaterial` alone renders
            // nearly white over a pale map, so the pill behind the selected
            // item had nothing to stand out against; the reference bar is
            // visibly grey and its selected pill is the light thing on it.
            // A thin wash of ink over the material gives that without
            // hardcoding a colour that would be wrong in the dark.
            .background {
                Capsule().fill(.regularMaterial)
                Capsule().fill(Brand.ink.opacity(0.06))
            }
            .overlay(Capsule().strokeBorder(.white.opacity(0.25), lineWidth: 0.5))
            .shadow(color: .black.opacity(0.10), radius: 10, y: 3)

            // The deed, on its own disc, the same height as the bar so the two
            // read as one row rather than as a bar with something stuck beside
            // it. Same glass, same grey, same edge.
            Button(action: collect) {
                Image(systemName: "camera.fill")
                    .font(.system(size: 21, weight: .semibold))
                    .foregroundStyle(Brand.ink)
                    .frame(width: 58, height: 58)
                    .background {
                        Circle().fill(.regularMaterial)
                        Circle().fill(Brand.ink.opacity(0.06))
                    }
                    .overlay(Circle().strokeBorder(.white.opacity(0.25), lineWidth: 0.5))
                    .shadow(color: .black.opacity(0.10), radius: 10, y: 3)
            }
            .buttonStyle(.plain)
            .accessibilityLabel("Collect a tree")
            .accessibilityIdentifier("tab-collect")
        }
        .padding(.horizontal, 12)
        .padding(.bottom, 4)
    }
}
