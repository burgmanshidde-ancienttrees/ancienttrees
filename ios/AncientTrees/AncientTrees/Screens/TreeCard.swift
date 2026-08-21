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
    /// Off when the card is already sitting on the map (Hidde, 2026-08-20). A
    /// small map is a WAY to the map, so on a screen that has one it is not a
    /// shortcut, it is a picture of what you are already looking at.
    var showsInset = true
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
                heart.padding(6)
                if saved.isVisited(tree.id) { ticked }
            }
            VStack(alignment: .leading, spacing: 5) {
                Text(tree.name).font(.cardTitle).foregroundStyle(Brand.ink).lineLimit(3)
                meta
            }
            .padding(.horizontal, 12).padding(.vertical, 10)
        }
        .background(Brand.surface)
        .clipShape(.rect(cornerRadius: corner))
        // The tap area is the visible card and nothing more. The photograph
        // is drawn with .fill inside a 190 point box and .clipped() clips the
        // DRAWING only: the image still measured 33 points above and below
        // the card for hit-testing, so the first card in the map's sheet was
        // tappable through the lower half of the search field above it, and
        // a press on the field opened the tree (the SE, 2026-08-21, found by
        // a UI test that kept landing on a tree page it never asked for).
        .contentShape(.rect(cornerRadius: corner))
        .shadow(color: .black.opacity(0.07), radius: 8, y: 3)
    }

    @ViewBuilder private var image: some View {
        if let p = tree.photo, let url = Photos.thumb(p.url, width: 500) {
            // The same empty box with the photograph laid over it as the tree
            // page's hero, and for the same reason: a .fill image proposes the
            // width its own picture wants, and a card that does that makes the
            // page it sits on wider than the phone.
            Color.clear
                .frame(height: imageHeight)
                .overlay {
                    AsyncImage(url: url) { phase in
                        switch phase {
                        case .success(let img):
                            img.resizable().aspectRatio(contentMode: .fill)
                        default:
                            placeholder.overlay(ProgressView().tint(.white))
                        }
                    }
                }
                .clipped()
            // The little map in the corner, from the AllTrails frames. On a
            // route it shows the shape; on a tree it shows the SETTING, and that
            // answers the thing a photograph of a trunk cannot: park, canal or
            // street corner.
            .overlay(alignment: .bottomTrailing) {
                // Honoured on BOTH branches. It used to guard only the
                // photo-less one, so a card in the map's own sheet still drew
                // a little map on top of the big map behind it.
                if showsInset { MapInset(lat: tree.lat, lng: tree.lng).padding(10) }
            }
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
                .overlay(alignment: .bottomTrailing) {
                    if showsInset { MapInset(lat: tree.lat, lng: tree.lng).padding(10) }
                }
        }
    }

    private var placeholder: some View {
        LinearGradient(colors: [Color(red: 0.20, green: 0.35, blue: 0.20),
                                Color(red: 0.35, green: 0.48, blue: 0.30)],
                       startPoint: .topLeading, endPoint: .bottomTrailing)
    }

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

    private var heart: some View {
        Button { saved.toggleSaved(tree.id) } label: {
            Image(systemName: saved.isSaved(tree.id) ? "heart.fill" : "heart")
                .font(.system(size: 15, weight: .semibold))
                .foregroundStyle(saved.isSaved(tree.id) ? .pink : .white)
                .padding(9)
                .background(.black.opacity(0.38), in: .circle)
                // The CIRCLE stays 35 points because a bigger one would sit on
                // the photograph; the TAP TARGET is 44, which is Apple's
                // minimum and was being missed by nine points on every card in
                // the app. Measured by scripts/appfit.py, not noticed by eye.
                .frame(width: 44, height: 44)
                .contentShape(.rect)
        }
        .buttonStyle(.plain)
        .accessibilityLabel(saved.isSaved(tree.id)
                            ? "Saved \(tree.name). Tap to remove"
                            : "Save \(tree.name)")
        .sensoryFeedback(.selection, trigger: saved.isSaved(tree.id))
    }

    private var ticked: some View {
        Label("Seen", systemImage: "checkmark.seal.fill")
            .font(.caption2.weight(.semibold))
            .foregroundStyle(.white)
            .padding(.horizontal, 8).padding(.vertical, 5)
            .background(Color(red: 0.20, green: 0.35, blue: 0.20), in: .capsule)
            .padding(10)
            .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
    }

    private var meta: some View {
        HStack(spacing: 6) {
            Text(tree.commonName)
            if let age = tree.age { dot; Text(shortAge(age)) }
            if let km { dot; Text(fmt(km)).monospacedDigit() }
            if tree.precision.needsWarning {
                dot; Image(systemName: "scope")
            }
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
