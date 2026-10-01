// A small grey "done" panel in the middle of the screen, gone by itself.
//
// Convention: Apple's own. Music's "Added to Library" and Photos' "Saved" are
// a rounded material square, a checkmark over one or two words, centred, for
// about a second and a half, and nothing to tap. Hidde, 2026-10-01, on saving
// a tree he had just added: "since you barely see a difference between add
// the tree and final tree page some confirmation of tree saved makes sense. I
// believe apple uses a small gray overlay for this type of interaction."
//
// It confirms an act; it never carries a choice. Anything with an undo is a
// Google Maps snackbar at the bottom instead, which is a different control.

import SwiftUI

struct DoneHUD: View {
    let text: String

    var body: some View {
        VStack(spacing: 10) {
            Image(systemName: "checkmark")
                .font(.system(size: 34, weight: .semibold))
            Text(text)
                .font(.subheadline.weight(.semibold))
                .multilineTextAlignment(.center)
        }
        .foregroundStyle(.secondary)
        .padding(.horizontal, 22).padding(.vertical, 20)
        .frame(minWidth: 140, minHeight: 120)
        .background(.regularMaterial, in: .rect(cornerRadius: 18))
        .accessibilityElement(children: .combine)
        .accessibilityIdentifier("done-hud")
    }
}

extension View {
    /// Shows `DoneHUD` while `text` is set, then clears it after 1.5 s.
    func doneHUD(_ text: Binding<String?>) -> some View {
        overlay {
            if let t = text.wrappedValue {
                DoneHUD(text: t)
                    .transition(.opacity.combined(with: .scale(scale: 0.92)))
                    .task(id: t) {
                        UIAccessibility.post(notification: .announcement, argument: t)
                        try? await Task.sleep(for: .seconds(1.5))
                        withAnimation(.easeOut(duration: 0.25)) { text.wrappedValue = nil }
                    }
                    .allowsHitTesting(false)
            }
        }
        .animation(.snappy, value: text.wrappedValue)
    }
}
