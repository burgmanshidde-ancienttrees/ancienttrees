// A tapped pin, in the map's own sheet.
//
// References, both recorded rather than remembered (CONVENTIONS.md, "Tapping a
// pin on a map that has a list in a sheet"): Apple Maps in the iOS 26
// simulator on 2026-10-18, where a tap grows the pin and the SAME sheet
// becomes that place, the cross giving the list back; and Airbnb's map card,
// which Hidde sent on 2026-10-19: the listing's own card with save and a cross
// on its photograph.
//
// So the sheet holds the tree's own card, the one the list already shows,
// with save and a cross on the photograph exactly where the website's map card
// has them. Hidde, 2026-10-19, on the first
// version (a title row, a separate photo and the story): "the app design does
// not look good"; the website's card was "kind of ok", so this is that card.
//
// Built from parts that already exist: TreeCard and SaveHeart's on-photo look.

import SwiftUI

struct TreePlaceBody: View {
    let tree: Tree
    /// From a real fix only, like the tree page: no distance from a guess.
    let km: Double?
    let onOpen: () -> Void
    let onClose: () -> Void

    var body: some View {
        VStack(spacing: 12) {
            ZStack(alignment: .topTrailing) {
                // The whole card opens the tree page, as every card does.
                Button(action: onOpen) { TreeCard(tree: tree, showHeart: false) }
                    .buttonStyle(.plain)
                    .accessibilityIdentifier("place-card")
                HStack(spacing: 0) {
                    SaveHeart(tree: tree, look: .onPhoto)
                    Button(action: onClose) {
                        // SaveHeart's on-photo circle, so the two read as a pair.
                        Image(systemName: "xmark")
                            .font(.system(size: 14, weight: .bold))
                            .foregroundStyle(.white)
                            .frame(width: 35, height: 35)
                            .background(.black.opacity(0.38), in: .circle)
                            .frame(width: 44, height: 44)
                            .contentShape(.rect)
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel("Close")
                    .accessibilityIdentifier("place-close")
                }
                .padding(6)
            }
            // No "Take me there" here: Airbnb's card and the website's carry
            // none, and at half height it sat against the floating tab bar
            // (behind it on the SE). The tree page, one tap on the card, has it.
        }
        .padding(.horizontal, 16)
        .padding(.top, 4)
    }
}
