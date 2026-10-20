// A tapped pin, in the map's own sheet.
//
// Reference: Apple Maps, recorded by hand in the iOS 26 simulator on
// 2026-10-18 (CONVENTIONS.md, "Tapping a pin on a map that has a list in a
// sheet"). A tap grows the pin and the SAME sheet becomes that place. Its top
// is one row: a share circle on the left, the name and its kind centred, a
// cross circle on the right, both circles centred on the two lines of text.
// Everything under it starts on the same edge as the circles.
//
// Measured off that recording and copied here: circles about 38 points,
// glyphs dark on a pale fill; about 11 points from the grip to the row; one
// 16 point edge for the circles and for the photograph under them.
//
// Hidde, 2026-10-19 and 10-20, over four rendered rounds: the list card
// rising "makes sense"; a cross on the photograph "seems unconventional"; a
// lone cross over the card was "really sloppy ... benchmark conventions and
// alignment". So the name moves up into Apple's row and the card below keeps
// its photograph, heart and tags (TreeCard showText: false), so nothing is
// said twice and every edge lines up.
//
// The whole photograph opens the tree page, as every card does.

import SwiftUI

struct TreePlaceHeader: View {
    let tree: Tree
    let onClose: () -> Void

    /// Species and age, the card's own line.
    private var meta: String {
        var parts = [tree.commonName]
        if let short = tree.ageShort, !short.isEmpty {
            parts.append(short)
        } else if let lo = tree.ageMin, lo > 0 {
            parts.append(tree.ageMax.map { $0 > lo ? "\(lo)-\($0) years" : "\(lo) years" } ?? "\(lo) years")
        }
        return parts.joined(separator: " · ")
    }

    var body: some View {
        HStack(alignment: .center, spacing: 12) {
            ShareLink(item: URL(string: "https://ancienttrees.app" + tree.url)!,
                      subject: Text(tree.name)) {
                PlaceCircle(symbol: "square.and.arrow.up")
            }
            .buttonStyle(.plain)
            .accessibilityLabel("Share \(tree.name)")
            .accessibilityIdentifier("place-share")

            VStack(spacing: 2) {
                Text(tree.name)
                    .font(.brand(20, .bold, relativeTo: .title3))
                    .foregroundStyle(Brand.ink)
                    .lineLimit(2)
                Text(meta)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                    .lineLimit(1)
            }
            .multilineTextAlignment(.center)
            .frame(maxWidth: .infinity)

            Button(action: onClose) { PlaceCircle(symbol: "xmark") }
                .buttonStyle(.plain)
                .accessibilityLabel("Close")
                .accessibilityIdentifier("place-close")
        }
        .padding(.horizontal, 16)
        // The sheet's header slot already sits 16 below the grip; Apple Maps'
        // row starts about 11 under it (measured 2026-10-20), so pull it up.
        .padding(.top, -14)
        .padding(.bottom, 16)
        .accessibilityIdentifier("place-header")
    }
}

/// Apple Maps' header circle: 38 drawn, a dark glyph on a pale fill, 44 to
/// hit. Pale ink rather than surfaceMuted, which is the sheet's own ground and
/// made the circle vanish (2026-10-19).
private struct PlaceCircle: View {
    let symbol: String
    var body: some View {
        Image(systemName: symbol)
            .font(.system(size: 15, weight: .semibold))
            .foregroundStyle(Brand.ink)
            .frame(width: 38, height: 38)
            .background(Brand.ink.opacity(0.08), in: .circle)
            .frame(width: 44, height: 44)
            .contentShape(.rect)
            // The 44 hit box sits 3 points wider each side than the circle;
            // pulling it back puts the drawn circle on the 16 point edge.
            .padding(.horizontal, -3)
    }
}

/// How a map screen's sheet answers a tapped pin, written once for the Map
/// tab, a city's map and My trees: a tap opens the sheet to its card stop,
/// sized to one tree rather than half the screen; letting go (the cross, a tap on empty map)
/// puts the list back at the height it had; swiping the sheet down to its lip
/// lets the tree go.
struct PinSelection: ViewModifier {
    @Binding var selected: Tree?
    @Binding var height: SheetHeight
    @State private var before: SheetHeight?

    func body(content: Content) -> some View {
        content
            // The card stop takes the tree's own height while one is chosen.
            .environment(\.sheetCardFits, selected != nil)
            .onChange(of: selected) { old, new in
                if new != nil {
                    if old == nil { before = height }
                    // THE CARD STOP, not half (Hidde, 2026-10-20: "er is veel
                    // leegte tussen menu en de boom kaart"). Half held one
                    // photograph and a band of empty sheet under it, which he
                    // ruled out on 2026-08-24 and is why .card exists.
                    withAnimation(.spring(duration: 0.3)) { height = .card }
                } else if let b = before {
                    withAnimation(.spring(duration: 0.3)) { height = b }
                    before = nil
                }
            }
            .onChange(of: height) { _, new in
                if new == .peek, selected != nil {
                    before = nil
                    selected = nil
                }
            }
    }
}

extension View {
    func pinSelection(_ selected: Binding<Tree?>, height: Binding<SheetHeight>) -> some View {
        modifier(PinSelection(selected: selected, height: height))
    }
}

struct TreePlaceBody: View {
    let tree: Tree
    let onOpen: () -> Void

    var body: some View {
        Button(action: onOpen) { TreeCard(tree: tree, showText: false) }
            .buttonStyle(.plain)
            .accessibilityIdentifier("place-card")
            .padding(.horizontal, 16)
    }
}
