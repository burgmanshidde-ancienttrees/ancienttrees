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
        let title: String
        let symbol: String
    }

    /// Same order as the TabView's tags.
    static let items = [
        Item(title: "Map", symbol: "map"),
        Item(title: "Explore", symbol: "magnifyingglass"),
        // A camera and never a plus (Hidde, 2026-08-23): a plus promises a row
        // in a list, a camera says what you are about to do. It carries a word
        // like the other three, because in the reference every item does.
        Item(title: "Collect", symbol: "camera"),
        Item(title: "Yours", symbol: "checkmark.circle"),
    ]

    let selected: Int
    let select: (Int) -> Void

    var body: some View {
        HStack(spacing: 0) {
            ForEach(Array(Self.items.enumerated()), id: \.offset) { i, item in
                Button {
                    select(i)
                } label: {
                    VStack(spacing: 3) {
                        ZStack {
                            if i == selected {
                                RoundedRectangle(cornerRadius: 16, style: .continuous)
                                    .fill(Brand.moss)
                                    .frame(width: 62, height: 32)
                            }
                            Image(systemName: item.symbol)
                                .font(.system(size: 20, weight: .regular))
                                // Dark on the bright pill, the way the
                                // reference inverts its selected symbol.
                                .foregroundStyle(i == selected ? Brand.ground : Brand.ink)
                                .environment(\.symbolVariants, .none)
                        }
                        .frame(height: 32)
                        Text(item.title)
                            .font(.system(size: 11))
                            .foregroundStyle(i == selected ? Brand.ink : Brand.inkSoft)
                    }
                    .frame(maxWidth: .infinity)
                    // 49 plus the label keeps every item over Apple's 44.
                    .frame(height: 50)
                    .contentShape(.rect)
                }
                .buttonStyle(.plain)
                .accessibilityLabel(item.title)
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
