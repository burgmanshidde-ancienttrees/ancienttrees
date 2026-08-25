// The heart, once.
//
// It was written twice, on the card and in the tree page's action bar, and the
// two drifted the moment the rules behind it changed: signing out left both of
// them saving happily into a collection nobody was signed in to keep (Hidde,
// 2026-08-25). Two looks, one decision, which is the pattern CLAUDE.md already
// asks for after the same lesson on hearts, the sign-in dialog and the vote
// control.
//
// Two rules live here now.
//
// SIGNED OUT MEANS NO SAVING. His reversal of the soft wall, same day: "all
// these functionalities of saving stuff should only be available when you sign
// in, and when you try to do it, you should get a message saying you need to
// sign in to be able to do this." The tap opens the sign-in sheet instead of
// filling a collection that would evaporate.
//
// REMOVING ASKS FIRST. "I think you should say, are you sure you want to delete
// this tree from your collection, because this goes too quickly. You could
// accidentally hit that heart button pretty easily." He is right and the card
// is where it is worst: the heart sits on the photograph, a thumb away from the
// tap that opens the tree.
import SwiftUI

struct SaveHeart: View {
    /// Where it is drawn. The two looks are unchanged from the code they
    /// replaced, down to the tap target and the colours.
    enum Look {
        case onPhoto     // over a card's picture, white on a dark scrim
        case inBar       // in the tree page's action bar, a bordered circle
    }

    let tree: Tree
    var look: Look = .onPhoto

    @Environment(Saved.self) private var saved
    @Environment(Account.self) private var account
    @Environment(Nudge.self) private var nudge
    @State private var confirmingRemove = false

    private var isSaved: Bool { saved.isSaved(tree.id) }

    var body: some View {
        Button(action: tap) { glyph }
            .buttonStyle(.plain)
            .accessibilityLabel(isSaved ? "Saved \(tree.name). Tap to remove"
                                        : "Save \(tree.name)")
            .sensoryFeedback(.selection, trigger: isSaved)
            .confirmationDialog("Remove \(tree.name) from your collection?",
                                isPresented: $confirmingRemove,
                                titleVisibility: .visible) {
                Button("Remove", role: .destructive) { saved.toggleSaved(tree.id) }
                Button("Keep it", role: .cancel) {}
            }
    }

    private func tap() {
        guard account.isSignedIn else {
            nudge.require(.keepTree(tree.name))
            return
        }
        if isSaved {
            confirmingRemove = true
        } else {
            saved.toggleSaved(tree.id)
        }
    }

    @ViewBuilder private var glyph: some View {
        switch look {
        case .onPhoto:
            Image(systemName: isSaved ? "heart.fill" : "heart")
                .font(.system(size: 15, weight: .semibold))
                .foregroundStyle(isSaved ? .pink : .white)
                .padding(9)
                .background(.black.opacity(0.38), in: .circle)
                // The CIRCLE stays 35 points because a bigger one would sit on
                // the photograph; the TAP TARGET is 44, which is Apple's
                // minimum and was being missed by nine points on every card in
                // the app. Measured by scripts/appfit.py, not noticed by eye.
                .frame(width: 44, height: 44)
                .contentShape(.rect)
        case .inBar:
            Image(systemName: isSaved ? "heart.fill" : "heart")
                .font(.title3)
                .foregroundStyle(isSaved ? .pink : Brand.inkSoft)
                .frame(width: 52, height: 52)
                .background(Brand.surface, in: .circle)
                .overlay { Circle().strokeBorder(Brand.hairline, lineWidth: 1) }
        }
    }
}
