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
    /// Your newest photograph of this tree of ours, looked up once for the
    /// whole grid by the screen (Sightings.newestShotByTree).
    var ownShot: Sightings.Sighting? = nil
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
            if let ownShot {
                OwnThumb(sighting: ownShot, maxPixel: 500)
            } else if let url = t.photo?.card {
                TreePhoto(url: url) { Brand.surfaceMuted }
            } else {
                named(t.name)
            }
        case .mine(let s):
            if s.photo != nil {
                OwnThumb(sighting: s, maxPixel: 500)
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
        if let city, !city.isEmpty { TagPill(text: city) }
    }
}

/// THE tag (Hidde, 2026-10-10: "i really prefer the tags of white background
/// and green letters keep those"). One look for every tag on a photograph:
/// the collected grid, Discover's tiles and its season hero.
struct TagPill: View {
    let text: String
    var body: some View {
        Text(text)
            .font(.system(size: 10, weight: .semibold))
            .foregroundStyle(Brand.moss)
            .lineLimit(2)
            .padding(.horizontal, 6).padding(.vertical, 3)
            .background(Brand.surface, in: .rect(cornerRadius: 8))
    }
}

/// One of your own photographs, decoded off the main thread. The tile is drawn
/// at once on the muted ground and the picture arrives a moment later, the
/// way Photos and Instagram fill a grid, instead of the scroll waiting for it.
struct OwnThumb: View {
    let sighting: Sightings.Sighting
    let maxPixel: CGFloat
    @Environment(Sightings.self) private var sightings
    @State private var img: UIImage?

    var body: some View {
        ZStack {
            Brand.surfaceMuted
            if let img { Image(uiImage: img).resizable().scaledToFill() }
        }
        .task(id: sighting.id) {
            if let hit = sightings.cachedThumbnail(sighting, maxPixel: maxPixel) { img = hit; return }
            guard let url = sightings.photoURL(sighting) else { return }
            let px = maxPixel
            let made = await Task.detached(priority: .userInitiated) {
                Sightings.decodeThumbnail(url, maxPixel: px)
            }.value
            if let made {
                sightings.keepThumbnail(made, for: sighting, maxPixel: maxPixel)
                img = made
            }
        }
    }
}
