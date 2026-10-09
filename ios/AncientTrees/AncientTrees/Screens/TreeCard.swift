// The card, built to the AllTrails shape: a photograph you can read at a glance,
// a heart on it, and a meta line of facts with no prose.
//
// The difference is what happens when there is no photograph, which is three
// quarters of the time. AllTrails never has that problem. Our website's answer
// is a species silhouette and a plain sentence saying nobody has published one,
// and that is strictly better than a grey rectangle: it still tells you what
// kind of tree it is, and it invites the reader to send one.

import SwiftUI

struct TreeCard: View {
    let tree: Tree
    var km: Double?
    /// Off in the collected lane, where a heart means the OTHER list (Hidde,
    /// 2026-08-26: "bij de collected lijst in my trees moet er geen hartje
    /// staan op de collected, dat heeft niks met hartje te maken"). The two
    /// lists are independent, so a heart drawn over a tree you photographed
    /// invites somebody to think it controls the thing they are looking at.
    var showHeart: Bool = true
    /// Your own photograph of this tree, which the card wears instead of ours
    /// in your own collection (2026-09-11): a list of the trees you stood in
    /// front of should show the trees as you saw them.
    var ownPhoto: UIImage? = nil
    /// Where your photograph of this tree stands, when you sent one
    /// (Sightings.Sighting.photoState). Drawn as the "Your photograph" tag.
    var ownState: String? = nil
    /// ONE HEIGHT FOR EVERY CARD IN A ROW, for a card that sits in a
    /// horizontal shelf.
    ///
    /// A name takes one, two or three lines, so in a shelf the cards ended at
    /// three different heights and the bottoms were ragged: that is most of
    /// what reads as "de verticale spacing is heel random" on Discover (Hidde,
    /// 2026-08-29). Netflix, AllTrails and the App Store all clamp a shelf
    /// card's title to a fixed number of lines for exactly this reason; a
    /// shelf is scanned sideways and a ragged bottom edge has nothing to line
    /// up against.
    ///
    /// Two lines reserved rather than three, because three would leave an
    /// empty line under most cards, and a longer name truncates, which is what
    /// the reference products do. Off by default: in a vertical list nothing
    /// is beside the card, so reserving space there would only add a blank
    /// line under every short name.
    var uniformTitle: Bool = false
    @Environment(Saved.self) private var saved

    private let corner: CGFloat = 14
    /// The picture grows with the reader's text size. A fixed 190 next to text
    /// set three sizes larger reads as a stamp rather than as a photograph, and
    /// the name under it was clipped at two lines besides.
    @ScaledMetric(relativeTo: .headline) private var imageHeight: CGFloat = 190

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            ZStack(alignment: .topTrailing) {
                image
                if showHeart { SaveHeart(tree: tree, look: .onPhoto).padding(6) }
                tagRow
                // No "Your photograph" tag (Hidde, 2026-10-09: "die mag ook
                // weg laten we dit consistent over web en app trekken").
            }
            VStack(alignment: .leading, spacing: 5) {
                Text(tree.name).font(.cardTitle).foregroundStyle(Brand.ink)
                    .lineLimit(uniformTitle ? 2 : 3, reservesSpace: uniformTitle)
                meta
            }
            .padding(.horizontal, 12).padding(.vertical, 10)
        }
        .background(Brand.surface)
        .clipShape(.rect(cornerRadius: corner))
        // The hairline belongs to the CARD, not to the screen behind it.
        // Hidde, 2026-08-27: "de kaart van de boom heeft de ene keer een lijn
        // eromheen en de andere keer niet." There was never a line: the card
        // fills Brand.surface, which is white in light mode, so it read as a
        // card on any screen whose background differed and dissolved into the
        // page on any screen that was also white. Ten call sites, ten
        // different backgrounds, one card that could not decide what it was.
        // Drawing it here makes the tile look the same everywhere by
        // construction rather than by every caller remembering.
        .overlay {
            RoundedRectangle(cornerRadius: corner, style: .continuous)
                .strokeBorder(Brand.hairline, lineWidth: 1)
        }
        // The tap area is the visible card and nothing more. The photograph
        // is drawn with .fill inside a 190 point box and .clipped() clips the
        // DRAWING only: the image still measured 33 points above and below
        // the card for hit-testing, so the first card in the map's sheet was
        // tappable through the lower half of the search field above it, and
        // a press on the field opened the tree (the SE, 2026-08-21, found by
        // a UI test that kept landing on a tree page it never asked for).
        .contentShape(.rect(cornerRadius: corner))
    }

    @ViewBuilder private var image: some View {
        if let own = ownPhoto {
            Color.clear
                .frame(height: imageHeight)
                .overlay { Image(uiImage: own).resizable().aspectRatio(contentMode: .fill) }
                .clipped()
                .accessibilityHidden(true)
        } else if let p = tree.photo, let url = p.card {
            // The same empty box with the photograph laid over it as the tree
            // page's hero, and for the same reason: a .fill image proposes the
            // width its own picture wants, and a card that does that makes the
            // page it sits on wider than the phone.
            Color.clear
                .frame(height: imageHeight)
                .overlay {
                    TreePhoto(url: url) {
                        placeholder.overlay(ProgressView().tint(.white))
                    }
                }
                .clipped()
            // The little map in the corner, from the AllTrails frames. On a
            // route it shows the shape; on a tree it shows the SETTING, and that
            // answers the thing a photograph of a trunk cannot: park, canal or
            // street corner.
            // Decorative, and its overflow is what made the card's measured
            // frame taller than the card; the name and meta carry the label.
            .accessibilityHidden(true)
            // No credit painted over the photograph (Hidde, 2026-08-20: "please
            // dont refer to wikicommons or whatever with an overlay on the tree,
            // put it somwhere small on the deeper page"). A card is a thumbnail
            // that exists to make somebody tap it, and a dark chip over the
            // trunk is the one thing on it that is not the tree.
            //
            // The attribution is not dropped, it MOVED: the tree page carries it
            // under the photograph, one tap away, which is how Wikipedia's own
            // apps and every image search do it. What is never allowed is a
            // CC BY or BY-SA picture with no credit anywhere at all, which is
            // what shipped once before and is the reason this comment exists.
        } else {
            noPhoto.frame(height: imageHeight)
        }
    }

    /// See leafTile in Style.swift: one tile for every card in the app that has
    /// to stand in for a photograph.
    private var placeholder: some View { leafTile }

    /// The honest empty state: the species, drawn, plus the ask.
    private var noPhoto: some View {
        ZStack {
            placeholder
            VStack(spacing: 8) {
                SpeciesMark(species: tree.species, color: .white.opacity(0.9))
                    .frame(width: 66, height: 66)
                Text(tree.commonName).font(.subheadline.weight(.semibold))
                    .foregroundStyle(.white)
                Text("No photograph yet").font(.caption2)
                    .foregroundStyle(.white.opacity(0.75))
            }
        }
    }

    // The heart lives in SaveHeart.swift now: one control, two looks, and the
    // sign-in gate and the remove confirmation written once instead of twice.

    /// THE TAG ROW, the website's (TreeCard.astro, 2026-10-04): at most two
    /// small pills top left on the photograph, the season first and "Seen"
    /// second, clear of the heart. "Seen" is a light pill with a green tick,
    /// no longer the filled canopy badge Hidde found "way too heavy".
    @ViewBuilder private var tagRow: some View {
        let seen = saved.isVisited(tree.id)
        if seasonChip != nil || seen {
            HStack(spacing: 6) {
                if let chip = seasonChip { chip }
                if seen { SeenTag() }
            }
            .padding(10)
            .padding(.trailing, 44)
            .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
        }
    }

    /// THE SEASON CHIP, the website's (phenology.ts seasonChipHtml): the
    /// moment named in sentence case on a soft tint of its own colour, top left
    /// on the photograph, only in the months it is true. Which chip is the
    /// website's answer (`seasonKey` in the feed); the words and tints are this
    /// surface's drawing of it. Behind the same season switch as the map's peak
    /// dots, because the season is the paid feature here.
    private var seasonChip: AnyView? {
        guard Launch.season, let key = tree.seasonKey,
              tree.bestTime?.isNow(Calendar.current.component(.month, from: .now)) == true
        else { return nil }
        // The website's chip (phenology.ts seasonChipHtml), icon and all
        // (Hidde, 2026-10-08: "didn't we make tag redesigns for web, are they
        // consistent? Make them"). The app had the words and tints without the
        // glyph. The glyphs are SF Symbols tinted in the website icon's own
        // colour, the nearest system drawing of each.
        let look: (String, UInt32, UInt32, String, UInt32) = switch key {
        case "bloom": ("In bloom", 0xFCE6EE, 0x9A2F57, "camera.macro", 0xE8705F)
        case "autumn": ("Autumn colour", 0xFCEEDC, 0x8A5216, "leaf.fill", 0xD97843)
        case "leaves": ("Fresh leaves", 0xE5F1D9, 0x355E19, "leaf.fill", 0x7FA653)
        case "catkins": ("Catkins", 0xF2F0D0, 0x615A16, "allergens", 0xC9B458)
        case "winter": ("Winter shape", 0xECEAE4, 0x4F4C45, "tree", 0x8C8577)
        case "fruit": ("In fruit", 0xFBEFD3, 0x7A5A0C, "circle.fill", 0xE8A33D)
        default: ("In season", 0xFBEFD3, 0x7A5A0C, "sparkle", 0xE8A33D)
        }
        return AnyView(
            HStack(spacing: 4) {
                Image(systemName: look.3)
                    .font(.system(size: 11, weight: .semibold))
                    .foregroundStyle(Color(light: look.4, dark: look.4))
                Text(look.0)
                    .foregroundStyle(Color(light: look.2, dark: look.2))
            }
            .font(.caption.weight(.semibold))
            .padding(.leading, 8).padding(.trailing, 10).padding(.vertical, 5)
            .background(Color(light: look.1, dark: look.1), in: .capsule)
            .shadow(color: .black.opacity(0.15), radius: 2, y: 1)
            .accessibilityElement(children: .combine)
            .accessibilityIdentifier("tree-card-season")
        )
    }

    private var meta: some View {
        HStack(spacing: 6) {
            Text(tree.commonName)
            if let age = tree.age { dot; Text(shortAge(age)) }
            // The crosshair that stood here is gone (Hidde, 2026-09-04: "soms
            // zie je een target icoon of locatie icoon op een boom kaart, ik
            // weet niet precies wat dat is maar haal maar helemaal weg, voegt
            // niks toe"). It meant "the pin is approximate", which is worth
            // saying in words on the tree's own page and worth nothing as an
            // undecodable glyph in a row of species and age. Nothing is lost:
            // the page it opens says it in a sentence.
        }
        .font(.caption)
        .foregroundStyle(.secondary)
        .lineLimit(1)
    }

    private var dot: some View { Text("·").foregroundStyle(.tertiary) }

    /// Ages in the feed are sentences ("roughly 131 to 161 years (sources
    /// disagree)"). A card has room for the number, not the caveat, and the
    /// caveat is on the tree's own page where it belongs.
    /// The age a CARD can carry: a number, not a sentence.
    ///
    /// 654 of our ages open with a hedge ("roughly", "about", "over",
    /// "estimated", "at least"), and several carry a clause after a comma or a
    /// bracket. On a one-line meta row that reads as "Bethlehem Plane ·
    /// estimated…" and the reader learns nothing at all (Hidde, 2026-08-21).
    ///
    /// So the number wins where the feed has one, which it now does for 1,159
    /// of 1,406 trees. The hedge is not dropped, it MOVED: the tree page one
    /// tap away prints the sentence as written, hedge and disagreement and
    /// all, which is where a claim about what we do and do not know belongs.
    private func shortAge(_ s: String) -> String {
        // The website's answer first (age_short in the feed, 2026-10-04): the
        // rule below is the fallback for a feed that predates the field.
        if let short = tree.ageShort, !short.isEmpty { return short }
        if let lo = tree.ageMin, lo > 0 {
            if let hi = tree.ageMax, hi > lo { return "\(lo)-\(hi) years" }
            return "\(lo) years"
        }
        // No number: trim the sentence back to its first clause and drop the
        // opening hedge, so at least something readable survives.
        var t = s
        if let r = t.range(of: " (") { t = String(t[..<r.lowerBound]) }
        if let r = t.range(of: ",") { t = String(t[..<r.lowerBound]) }
        for hedge in ["estimated ", "roughly ", "approximately ", "around ", "about "] {
            if t.lowercased().hasPrefix(hedge) { t = String(t.dropFirst(hedge.count)); break }
        }
        return t
    }

    private func fmt(_ km: Double) -> String {
        km < 1 ? "\(Int((km * 1000).rounded())) m" : String(format: "%.1f km", km)
    }
}

/// "SEEN", ONE LOOK EVERYWHERE (Hidde, 2026-10-08: "de witte seen tag in app is
/// echt nice, kunnen we die tag overal zo aanhouden, ik zie m soms in het
/// groen"). A white pill with the green tick, on a photograph and off it, on
/// our trees and on your own. It was a filled canopy capsule on MineCard, and
/// on the website a pale green pill wherever a card had no photograph. The
/// website draws the same pill (.tree-card-seen in style.css).
struct SeenTag: View {
    var body: some View {
        Label("Collected", systemImage: "checkmark.circle.fill")
            .font(.caption.weight(.semibold))
            .foregroundStyle(Brand.canopy)
            .padding(.horizontal, 10).padding(.vertical, 5)
            .background(Color.white, in: .capsule)
            .overlay { Capsule().strokeBorder(Color.black.opacity(0.06), lineWidth: 1) }
            .shadow(color: .black.opacity(0.15), radius: 2, y: 1)
            .accessibilityIdentifier("tree-card-seen")
    }
}
