// A place's list in direction C (Hidde, 2026-11-05: "i like option c"):
// Highlights as a sideways shelf of photograph cards (Airbnb, AllTrails), then
// every tree as a compact row with a small square on the left (Google Maps'
// result rows). A tree without a photograph no longer fills the list with a
// 190 point green block that says its species twice: its square is the pale
// moss tint with the species drawn in it. The website draws the same two parts
// (TreeCard.astro, variant "row" and the highlights grid).

import SwiftUI

/// The short age a card can carry, or nil: a number, never a sentence and
/// never an empty string, so the meta line never ends in a lone dot.
func cardAge(_ tree: Tree) -> String? {
    if let s = tree.ageShort?.trimmingCharacters(in: .whitespaces), !s.isEmpty,
       s.rangeOfCharacter(from: .decimalDigits) != nil { return s }
    if let lo = tree.ageMin, lo > 0 {
        if let hi = tree.ageMax, hi > lo { return "\(lo)-\(hi) years" }
        return "\(lo) years"
    }
    return nil
}

/// "Silky Oak" or "Silky Oak · 100 years".
struct TreeMetaLine: View {
    let tree: Tree
    var body: some View {
        HStack(spacing: 5) {
            Text(tree.commonName)
            if let age = cardAge(tree) {
                Text("·").foregroundStyle(.tertiary)
                Text(age)
            }
        }
        .font(.system(size: 13))
        .foregroundStyle(Brand.inkSoft)
        .lineLimit(1)
    }
}

/// One tree in "All trees".
struct TreeRow: View {
    let tree: Tree
    @Environment(Saved.self) private var saved

    var body: some View {
        HStack(spacing: 12) {
            thumb.accessibilityHidden(true)
            VStack(alignment: .leading, spacing: 4) {
                Text(tree.name)
                    .font(.brand(16, .bold))
                    .foregroundStyle(Brand.ink)
                    .lineLimit(2)
                    .fixedSize(horizontal: false, vertical: true)
                TreeMetaLine(tree: tree)
            }
            Spacer(minLength: 4)
            SaveHeart(tree: tree, look: .plain)
        }
        .padding(.vertical, 10)
        .overlay(alignment: .bottom) { Rectangle().fill(Brand.hairline).frame(height: 1) }
        .contentShape(.rect)
    }

    @ViewBuilder private var thumb: some View {
        Group {
            if let url = tree.photo?.card {
                Color.clear.overlay {
                    TreePhoto(url: url) { Brand.mossTint }
                }
                .clipped()
            } else {
                ZStack {
                    Brand.mossTint
                    SpeciesMark(species: tree.species, color: Brand.moss)
                        .frame(width: 30, height: 30)
                }
            }
        }
        .frame(width: 64, height: 64)
        .clipShape(.rect(cornerRadius: 10))
        // Collected: the white tick of the Seen tag, small, on the square's
        // corner (SeenTag's look, TreeCard.swift).
        .overlay(alignment: .bottomTrailing) {
            if saved.isVisited(tree.id) {
                Image(systemName: "checkmark.circle.fill")
                    .font(.system(size: 18))
                    .foregroundStyle(Brand.canopy, .white)
                    .background(Circle().fill(.white).padding(2))
                    .offset(x: 4, y: 4)
                    .accessibilityIdentifier("tree-card-seen")
            }
        }
    }
}

/// One card on the Highlights shelf.
struct HighlightCard: View {
    let tree: Tree
    @Environment(Saved.self) private var saved

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Color.clear
                .frame(width: 220, height: 150)
                .overlay {
                    TreePhoto(url: tree.photo?.card) { leafTile }
                }
                .clipShape(.rect(cornerRadius: 12))
                .overlay(alignment: .topTrailing) { SaveHeart(tree: tree, look: .onPhoto).padding(2) }
                .overlay(alignment: .topLeading) {
                    if saved.isVisited(tree.id) { SeenTag().padding(8) }
                }
            Text(tree.name)
                .font(.brand(15, .bold))
                .foregroundStyle(Brand.ink)
                .lineLimit(2, reservesSpace: true)
                .padding(.top, 8)
            TreeMetaLine(tree: tree)
                .font(.system(size: 12))
                .padding(.top, 3)
        }
        .frame(width: 220, alignment: .leading)
        .contentShape(.rect)
    }
}

/// "Highlights", "All 58 trees": the list's section heads.
struct SheetSectionHead: View {
    let title: String
    var body: some View {
        Text(title)
            .font(.brand(19, .bold))
            .foregroundStyle(Brand.ink)
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.top, 6)
            .accessibilityAddTraits(.isHeader)
    }
}
