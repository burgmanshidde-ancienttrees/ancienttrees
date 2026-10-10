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
    @Environment(Navigator.self) private var navigator
    @State private var confirmingRemove = false

    private var isSaved: Bool { saved.isSaved(tree.id) }

    var body: some View {
        Button(action: tap) { glyph }
            .buttonStyle(.plain)
            .accessibilityIdentifier("save-heart")
            .accessibilityLabel(isSaved ? "Saved \(tree.name). Tap to remove"
                                        : "Save \(tree.name)")
            .sensoryFeedback(.selection, trigger: isSaved)
            .sheet(isPresented: $confirmingRemove) {
                BrandSheet(
                    title: "Remove \(tree.name) from Want to visit?",
                    buttons: [
                        .destructive("Remove", id: "want-remove-confirm") {
                            confirmingRemove = false
                            saved.toggleSaved(tree.id)
                        },
                        .secondary("Keep it") { confirmingRemove = false },
                    ])
            }
    }

    private func tap() {
        guard account.isSignedIn else {
            // Replayed only if it is not already there. Signing in merges what
            // the account holds, which can include this very tree kept on
            // another device, and a blind toggle would then UN-save it.
            nudge.require(.keepTree(tree.name)) {
                if !saved.isSaved(tree.id) { saved.toggleSaved(tree.id); confirmAdded() }
            }
            return
        }
        if isSaved {
            confirmingRemove = true
        } else {
            saved.toggleSaved(tree.id)
            confirmAdded()
        }
    }

    private func confirmAdded() {
        withAnimation(.easeOut(duration: 0.2)) {
            navigator.snack = .init(text: "Added to Want to visit", viewWantToVisit: true)
        }
    }

    @ViewBuilder private var glyph: some View {
        switch look {
        case .onPhoto:
            Image(systemName: isSaved ? "bookmark.fill" : "bookmark")
                .font(.system(size: 15, weight: .semibold))
                .foregroundStyle(.white)
                .padding(9)
                .background(.black.opacity(0.38), in: .circle)
                // The CIRCLE stays 35 points because a bigger one would sit on
                // the photograph; the TAP TARGET is 44, which is Apple's
                // minimum and was being missed by nine points on every card in
                // the app. Measured by scripts/appfit.py, not noticed by eye.
                .frame(width: 44, height: 44)
                .contentShape(.rect)
        case .inBar:
            Image(systemName: isSaved ? "bookmark.fill" : "bookmark")
                .font(.title3)
                .foregroundStyle(isSaved ? Brand.moss : Brand.inkSoft)
                .frame(width: 52, height: 52)
                .background(Brand.surface, in: .circle)
                .overlay { Circle().strokeBorder(Brand.hairline, lineWidth: 1) }
        }
    }
}

/// The confirmation line itself, drawn once by the root over every screen.
/// Above the floating tab bar and the tree page's action bar alike.
struct SnackBar: View {
    @Environment(Navigator.self) private var navigator

    var body: some View {
        if let s = navigator.snack {
            HStack(spacing: 12) {
                Image(systemName: s.symbol).foregroundStyle(Brand.moss)
                Text(s.text)
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(Brand.ink)
                    .lineLimit(2)
                Spacer(minLength: 8)
                if s.viewWantToVisit {
                    Button("View") {
                        navigator.snack = nil
                        navigator.openWantToVisit = true
                        navigator.selectTab = 2
                    }
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(Brand.moss)
                    .frame(minWidth: 44, minHeight: 44)
                    .accessibilityIdentifier("snack-view")
                }
            }
            .padding(.leading, 16).padding(.trailing, 8)
            .frame(minHeight: 52)
            .background(Brand.surface, in: .rect(cornerRadius: 14))
            .overlay { RoundedRectangle(cornerRadius: 14).strokeBorder(Brand.hairline, lineWidth: 1) }
            .shadow(color: .black.opacity(0.16), radius: 14, y: 4)
            .padding(.horizontal, 16)
            .padding(.bottom, 92)
            .transition(.move(edge: .bottom).combined(with: .opacity))
            .accessibilityElement(children: .contain)
            .accessibilityIdentifier("snack")
            .task(id: s.id) {
                try? await Task.sleep(for: .seconds(4))
                if navigator.snack?.id == s.id {
                    withAnimation(.easeIn(duration: 0.2)) { navigator.snack = nil }
                }
            }
        }
    }
}
