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
    static let items = [
        Item(title: "Map", symbol: "map"),
        Item(title: "Explore", symbol: "magnifyingglass"),
        Item(title: "", symbol: "camera.fill", action: true),
        Item(title: "Collection", symbol: "checkmark.circle"),
        Item(title: "Profile", symbol: "person"),
    ]

    let selected: Int
    let select: (Int) -> Void

    var body: some View {
        HStack(spacing: 0) {
            ForEach(Array(Self.items.enumerated()), id: \.offset) { i, item in
                Button {
                    select(i)
                } label: {
                    VStack(spacing: 2) {
                        ZStack {
                            if item.action {
                                // The highlight he asked for: a filled disc,
                                // the only one in the bar, so the deed reads as
                                // a button among places rather than a fifth
                                // destination. It never shows a selected state,
                                // because you never arrive here.
                                Circle()
                                    .fill(Brand.moss)
                                    .frame(width: 44, height: 44)
                                Image(systemName: item.symbol)
                                    .font(.system(size: 20, weight: .semibold))
                                    .foregroundStyle(Brand.ground)
                            } else {
                                // The selected item is said by a FILLED symbol
                                // and a bolder, darker word, not by a pill
                                // behind it (Hidde, 2026-08-24). That reverses
                                // the pill copied off his AllTrails frame this
                                // morning, and it is worth naming as a flip
                                // rather than a drift: this is what iOS does
                                // in its own bars, so it is the plainer of the
                                // two conventions rather than a preference.
                                Image(systemName: item.symbol)
                                    .font(.system(size: 22, weight: .regular))
                                    .foregroundStyle(i == selected ? Brand.ink : Brand.inkSoft)
                                    .environment(\.symbolVariants, i == selected ? .fill : .none)
                            }
                        }
                        // The ACTION needs 44 for its disc; a labelled item
                        // needs only its glyph, and giving it 44 too put air
                        // above and below the icon so the word floated away
                        // from it (Hidde, 2026-08-24: "de afstand tussen de
                        // tekst map explore etc en het icon erboven is wat te
                        // groot"). iOS sits its own icon and label about two
                        // points apart and so does the reference. The tap
                        // target is the whole 50 point row at full item width,
                        // so nothing here is smaller than Apple's floor.
                        .frame(height: item.action ? 44 : 26)
                        if !item.title.isEmpty {
                            Text(item.title)
                                .font(.system(size: 11,
                                              weight: i == selected ? .bold : .regular))
                                .foregroundStyle(i == selected ? Brand.ink : Brand.inkSoft)
                        }
                    }
                    .frame(maxWidth: .infinity)
                    // The row is 50 tall and every item fills the width it is
                    // given, so each target clears Apple's 44 in both
                    // directions even where the label is missing.
                    .frame(height: 50)
                    .contentShape(.rect)
                }
                .buttonStyle(.plain)
                .accessibilityLabel(item.action ? "Collect a tree" : item.title)
                .accessibilityAddTraits(i == selected ? [.isSelected, .isButton] : .isButton)
            }
        }
        .padding(.top, 6)
        .background(alignment: .top) {
            ZStack(alignment: .top) {
                Brand.ground
                Rectangle().fill(Brand.hairline).frame(height: 0.5)
            }
            .ignoresSafeArea(edges: .bottom)
        }
    }
}
