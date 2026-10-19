// A tapped pin, in the map's own sheet.
//
// References, both recorded rather than remembered (CONVENTIONS.md, "Tapping a
// pin on a map that has a list in a sheet"): Apple Maps in the iOS 26
// simulator on 2026-10-18, where a tap grows the pin and the SAME sheet
// becomes that place; and Airbnb's map card, which Hidde sent on 2026-10-19.
//
// Hidde chose it on 2026-10-19 after three rendered rounds: the tree's own
// list card rises in the sheet ("using the card in the list and make it come
// up makes sense"), and no cross ON the card ("the cross seems
// unconventional"): the cross sits in the sheet's corner, where Apple Maps has
// it. The list also comes back when the sheet is swiped down or the empty map
// is tapped (MapTab, `selected`).
//
// It IS the list's card, heart and all, so a tree looks the same wherever it
// is shown. The whole card opens the tree page, as every card does.

import SwiftUI

struct TreePlaceBody: View {
    let tree: Tree
    let onOpen: () -> Void

    var body: some View {
        Button(action: onOpen) { TreeCard(tree: tree) }
            .buttonStyle(.plain)
            .accessibilityIdentifier("place-card")
            .padding(.horizontal, 16)
    }
}
