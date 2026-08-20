// The chip row's one control, in two pieces: a button and a bare label, because
// a Menu needs the label without a button wrapped round it.

import SwiftUI

struct FilterChipLabel: View {
    let label: String
    let icon: String
    let on: Bool

    var body: some View {
        HStack(spacing: 5) {
            Image(systemName: icon).font(.caption2.weight(.semibold))
            Text(label).font(.brand(13, .medium, relativeTo: .caption))
        }
        .foregroundStyle(on ? .white : Brand.ink)
        .padding(.horizontal, 12).padding(.vertical, 8)
        .background(on ? Brand.moss : Brand.surface, in: .capsule)
        .overlay {
            if !on { Capsule().strokeBorder(Brand.hairline, lineWidth: 1) }
        }
        .shadow(color: .black.opacity(on ? 0 : 0.05), radius: 3, y: 1)
    }
}

struct FilterChip: View {
    let label: String
    let icon: String
    let on: Bool
    let tap: () -> Void

    var body: some View {
        Button(action: tap) { FilterChipLabel(label: label, icon: icon, on: on) }
            .buttonStyle(.plain)
            .accessibilityAddTraits(on ? [.isSelected] : [])
    }
}
