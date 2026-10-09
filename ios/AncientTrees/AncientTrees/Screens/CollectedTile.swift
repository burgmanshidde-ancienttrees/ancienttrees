// One tree in the Collected grid: a photograph in a 3:4 tile, nothing else.
//
// Convention: Instagram's profile grid, three columns of 3:4 portrait tiles a
// hairline apart (since January 2025), and iNaturalist's Me screen, whose Grid
// view is the photo-first way to look at your own observations (CONVENTIONS.md
// 2026-10-09, "Your collection as a grid"). Hidde, 2026-10-09: "the cards are
// not like instagram - like 9 trees in rows of 3 i think that would be better".
//
// The name lives on the tree's page, as it does on Instagram; the only words
// on a tile are its city, because that is the one fact the photograph cannot
// say.
import SwiftUI

struct CollectedTile: View {
    enum Kind { case ours(Tree), mine(Sightings.Sighting), sent(Submission.Sent) }
    let kind: Kind
    /// Where the tree stands, worked out by the screen (a tree you added is
    /// placed by the nearest tree we map).
    var city: String? = nil
    @Environment(Sightings.self) private var sightings

    var body: some View {
        Color.clear
            .aspectRatio(3.0 / 4.0, contentMode: .fit)
            .overlay { picture }
            .overlay(alignment: .bottomLeading) { tag.padding(6) }
            .clipped()
            .contentShape(.rect)
    }

    @ViewBuilder private var picture: some View {
        switch kind {
        case .ours(let t):
            if let own = sightings.ofTree(t.id).first.flatMap({ sightings.thumbnail($0, maxPixel: 500) }) {
                Image(uiImage: own).resizable().scaledToFill()
            } else if let url = t.photo?.card {
                TreePhoto(url: url) { Brand.surfaceMuted }
            } else {
                named(t.name)
            }
        case .mine(let s):
            if let img = sightings.thumbnail(s, maxPixel: 500) {
                Image(uiImage: img).resizable().scaledToFill()
            } else {
                named(s.name)
            }
        case .sent(let t):
            named(t.title)
        }
    }

    /// A tree with no photograph still gets its square: its name on the
    /// muted ground, so the grid has no holes.
    private func named(_ name: String) -> some View {
        ZStack {
            Brand.surfaceMuted
            Text(name)
                .font(.brand(12, .bold, relativeTo: .caption))
                .foregroundStyle(Brand.inkSoft)
                .multilineTextAlignment(.center)
                .lineLimit(4)
                .padding(8)
        }
    }

    /// THE CITY, on every tile (Hidde, 2026-10-09: "de your tree tags slaan
    /// eigenlijk nergens meer op gebruik die tags toch maar om aan te geven
    /// welke stad"). In a grid of trunks the photograph does not say where it
    /// is, and that is the question a collection of trees across countries
    /// raises first.
    @ViewBuilder private var tag: some View {
        if let city, !city.isEmpty { pill(city, icon: nil, filled: false) }
    }

    private func pill(_ text: String, icon: String?, filled: Bool) -> some View {
        HStack(spacing: 3) {
            if let icon { Image(systemName: icon) }
            Text(text)
        }
        .font(.system(size: 10, weight: .semibold))
        .foregroundStyle(filled ? .white : Brand.moss)
        .padding(.horizontal, 6).padding(.vertical, 3)
        .background(filled ? AnyShapeStyle(Brand.moss) : AnyShapeStyle(Brand.surface), in: .capsule)
    }
}
