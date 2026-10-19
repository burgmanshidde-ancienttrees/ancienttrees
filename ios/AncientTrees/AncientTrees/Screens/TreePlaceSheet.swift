// A tapped pin, in the map's own sheet.
//
// Reference: Apple Maps, recorded by hand in the iOS 26 simulator on
// 2026-10-18 (CONVENTIONS.md, "Tapping a pin on a map that has a list in a
// sheet"). A tap grows the pin in place and the SAME sheet becomes that place:
// share on the left, the name in the middle, the cross on the right, the main
// action under it, then the photographs. The cross puts the list back as it
// was. No card floats over the list and no page is pushed.
//
// Hidde, 2026-10-18, asking for it after seeing the recording; until then a
// pin tap pushed the whole tree page (2026-08-25, when a tap did nothing at
// all), which threw the map away for every tree somebody wanted to compare.
//
// Built from parts that already exist: SheetCloseButton (BrandSheet), the
// tree page's green BrandButtonStyle capsule and SaveHeart in its bar look,
// TreePhoto as the card draws it.

import SwiftUI

/// The sheet's fixed top while a tree is selected: share, name, cross.
struct TreePlaceHeader: View {
    let tree: Tree
    let onClose: () -> Void

    var body: some View {
        ZStack(alignment: .top) {
            VStack(spacing: 3) {
                Text(tree.name)
                    .font(.brand(20, .bold, relativeTo: .title3))
                    .foregroundStyle(Brand.ink)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)
                Text(TreePlaceHeader.meta(tree))
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                    .lineLimit(1)
            }
            .padding(.horizontal, 64)
            .padding(.top, 10)
            .frame(maxWidth: .infinity)

            HStack {
                ShareLink(item: URL(string: "https://ancienttrees.app" + tree.url)!,
                          subject: Text(tree.name)) {
                    Image(systemName: "square.and.arrow.up")
                        .font(.system(size: 13, weight: .bold))
                        .foregroundStyle(.secondary)
                        .frame(width: 30, height: 30)
                        .background(Brand.surfaceMuted, in: .circle)
                        .frame(width: 48, height: 48)
                        .contentShape(.rect)
                }
                .buttonStyle(.plain)
                .padding(.top, 8)
                .padding(.leading, 10)
                .accessibilityLabel("Share \(tree.name)")
                .accessibilityIdentifier("place-share")
                Spacer()
                SheetCloseButton(action: onClose)
            }
        }
        .padding(.bottom, 12)
        .accessibilityIdentifier("place-header")
    }

    /// Species and age, the card's own line.
    static func meta(_ t: Tree) -> String {
        var parts = [t.commonName]
        if let short = t.ageShort, !short.isEmpty {
            parts.append(short)
        } else if let lo = t.ageMin, lo > 0 {
            parts.append(t.ageMax.map { $0 > lo ? "\(lo)-\($0) years" : "\(lo) years" } ?? "\(lo) years")
        }
        return parts.joined(separator: " · ")
    }
}

/// What the sheet holds under that header.
struct TreePlaceBody: View {
    let tree: Tree
    /// From a real fix only, like the tree page: no distance from a guess.
    let km: Double?
    let onOpen: () -> Void

    private var takeLabel: String {
        guard let d = km else { return "Take me there" }
        let far = d < 1 ? "\(Int((d * 1000 / 50).rounded() * 50)) m"
            : d < 10 ? String(format: "%.1f km", d) : "\(Int(d.rounded())) km"
        return "Take me there · " + far
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack(spacing: 12) {
                Button { Directions.walk(lat: tree.lat, lng: tree.lng) } label: {
                    Label(takeLabel, systemImage: "arrow.turn.up.right").lineLimit(1)
                }
                .buttonStyle(BrandButtonStyle())
                .accessibilityIdentifier("place-take-me-there")
                SaveHeart(tree: tree, look: .inBar)
            }

            // The photograph, as wide as the sheet; the tree page is one tap
            // on it, the same way Apple Maps opens a place's pictures.
            Button(action: onOpen) {
                Color.clear
                    .frame(height: 200)
                    .overlay {
                        if let url = tree.photo?.card {
                            TreePhoto(url: url) { leafTile }
                        } else {
                            leafTile
                        }
                    }
                    .clipShape(.rect(cornerRadius: 16, style: .continuous))
                    .contentShape(.rect(cornerRadius: 16))
            }
            .buttonStyle(.plain)
            .accessibilityLabel("Open \(tree.name)")
            .accessibilityIdentifier("place-photo")

            // Pulled up, the sheet reads like the page it leads to.
            Text(tree.storyText)
                .font(.body)
                .foregroundStyle(Brand.ink)
                .lineSpacing(3)

            Button(action: onOpen) {
                Label("Open the tree page", systemImage: "chevron.right")
                    .labelStyle(.titleOnly)
            }
            .buttonStyle(SheetButtonStyle(kind: .secondary))
            .accessibilityIdentifier("place-open")

            Color.clear.frame(height: 24)
        }
        .padding(.horizontal, 20)
    }
}
