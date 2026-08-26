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
    /// The deed, handed in rather than assumed, because it is not a tab.
    var collect: () -> Void = {}

    var body: some View {
        HStack(spacing: 12) {
            HStack(spacing: 0) {
                ForEach(Array(Self.items.enumerated()), id: \.offset) { i, item in
                    Button { select(i) } label: {
                        VStack(spacing: 3) {
                            Image(systemName: item.symbol)
                                .font(.system(size: 22, weight: .regular))
                                .environment(\.symbolVariants, i == selected ? .fill : .none)
                                .frame(height: 26)
                            Text(item.title)
                                .font(.system(size: 11,
                                              weight: i == selected ? .semibold : .regular))
                        }
                        // MONOCHROME, and that is the reference rather than a
                        // preference (Hidde, 2026-08-26: "flikker op met dat
                        // hele groen, maak het gewoon zwart-wit en zoals zij
                        // doen met dat grijze overlay"). Polarsteps' bar has
                        // no brand colour in it at all: the selected item is
                        // simply darker and filled, and everything else is
                        // grey. A green tab in a glass bar was our colour
                        // asking for attention the bar does not need, and the
                        // green is still doing its job two centimetres away on
                        // the camera.
                        .foregroundStyle(i == selected ? Brand.ink : Brand.inkSoft.opacity(0.75))
                        .frame(maxWidth: .infinity)
                        .frame(height: 52)
                        .contentShape(.rect)
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel(item.title)
                    .accessibilityIdentifier("tab-\(item.title.lowercased().replacingOccurrences(of: " ", with: "-"))")
                    .accessibilityAddTraits(i == selected ? [.isSelected, .isButton] : .isButton)
                }
            }
            // GLASS, not a painted capsule. Polarsteps floats a frosted bar
            // over the content and lets what is behind it show through, which
            // is why the bar reads as hovering rather than as a floor. iOS
            // gives us the same material its own bars use.
            .background(.regularMaterial, in: .capsule)
            .overlay(Capsule().strokeBorder(.white.opacity(0.35), lineWidth: 0.5))
            .shadow(color: .black.opacity(0.12), radius: 12, y: 3)

            // The deed, on its own disc beside the bar, in the same glass. It
            // is separated by distance rather than by colour, which is how the
            // reference does it: a button that makes something does not belong
            // in a row of places.
            Button(action: collect) {
                Image(systemName: "camera.fill")
                    .font(.system(size: 21, weight: .semibold))
                    .foregroundStyle(Brand.ink)
                    .frame(width: 58, height: 58)
                    .background(.regularMaterial, in: .circle)
                    .overlay(Circle().strokeBorder(.white.opacity(0.35), lineWidth: 0.5))
                    .shadow(color: .black.opacity(0.14), radius: 12, y: 3)
            }
            .buttonStyle(.plain)
            .accessibilityLabel("Collect a tree")
            .accessibilityIdentifier("tab-collect")
        }
        .padding(.horizontal, 14)
        .padding(.bottom, 4)
    }
}
