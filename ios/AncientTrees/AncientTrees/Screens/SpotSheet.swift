// The centre button's sheet: you are standing before a tree.
//
// One screen, both outcomes, GPS only orders them (DECISIONS.md 2026-08-20
// evening): trees we map within reach are there to tick off, and beneath them,
// always, the second way: a tree we miss can be sent in. The button never has
// a dead state, because anywhere on earth one of the two applies.
//
// This file is the stub that gives the sheet its place and its identifier;
// the real flow is plan task 4.

import SwiftUI

struct SpotSheet: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text("Standing before a tree?")
                .font(.brand(24, .heavy))
                .foregroundStyle(Brand.ink)
            Text("Tick it off if we map it, or send it in if we miss it.")
                .font(.body)
                .foregroundStyle(Brand.inkSoft)
            Spacer()
        }
        .padding(20)
        .frame(maxWidth: .infinity, alignment: .leading)
        .brandGround()
        .accessibilityElement(children: .contain)
        .accessibilityIdentifier("spot-sheet")
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
    }
}
