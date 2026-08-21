// One tree, and the two actions that matter under it.
//
// The action bar is pinned to the bottom and does not scroll away, which is the
// sharpest thing the AllTrails teardown found: their `Begin` is not merely under
// the elevation chart, it is fixed to the bottom of the phone everywhere the
// route exists. `directions` fired zero times on our website, where the button
// lives at the end of a story somebody has to scroll through.

import SwiftUI
import MapKit

struct TreeDetail: View {
    let tree: Tree
    let catalogue: Catalogue
    @Environment(Saved.self) private var saved
    @Environment(Account.self) private var account
    @Environment(Nudge.self) private var nudge
    @State private var showFullStory = false
    @State private var reporting = false
    @Environment(Navigator.self) private var navigator

    var body: some View {
        ZStack(alignment: .bottom) {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    hero
                    header
                    facts
                    // Where it is, on the page rather than one tap away in
                    // Apple Maps. Their route page has exactly this and ours did
                    // not, which left the app behind our own website on the one
                    // field that decides whether somebody gets there: the site's
                    // tree page has carried a map since it shipped.
                    mapCard
                    if tree.precision.needsWarning { approximateNote }
                    story
                    accessBlock
                    // The same control the website carries, born as toggles
                    // (2026-08-21): sibling of the report button, per the
                    // vote-and-report split.
                    WorthItView(tree: tree)
                    if tree.photo == nil { offerPhoto }
                    Button { reporting = true } label: {
                        Label("Something here is wrong", systemImage: "exclamationmark.bubble")
                            .font(.footnote)
                    }
                    Color.clear.frame(height: 90)   // room for the pinned bar
                }
                .padding(.horizontal, 20)
                .padding(.top, 8)
            }
            actionBar
        }
        .brandGround()
        // The name renders once, in the body's own heading; a second copy in
        // the bar was the "title twice" mess from the findings list.
        .navigationTitle("")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                ShareLink(item: URL(string: "https://ancienttrees.app" + tree.url)!,
                          subject: Text(tree.name),
                          message: Text("\(tree.name), \(tree.city).")) {
                    Image(systemName: "square.and.arrow.up")
                        .frame(width: 44, height: 44)
                        .contentShape(.rect)
                }
                .accessibilityLabel("Share this tree")
            }
        }
        .sheet(isPresented: $reporting) { ContributeView(about: tree) }
    }

    /// The photograph, or the species drawn, edge to edge. AllTrails leads every
    /// route with a picture and it is most of why their pages feel like an
    /// invitation rather than a database record.
    ///
    /// The credit sits UNDER it rather than painted across it.
    ///
    /// This is the only place the attribution appears now, which is deliberate:
    /// cards stopped carrying it on 2026-08-20 because a dark chip over the
    /// trunk is the one thing on a card that is not the tree. A CC BY or BY-SA
    /// licence obliges a credit and this is it, in the ordinary place a caption
    /// goes, which is also what every image search and Wikipedia's own apps do.
    @ViewBuilder private var hero: some View {
        if let p = tree.photo, let url = Photos.thumb(p.url, width: 960) {
            VStack(alignment: .leading, spacing: 6) {
                // AN EMPTY BOX WITH THE PHOTOGRAPH LAID OVER IT, not a
                // photograph with a height. A .fill image asks for the width
                // its own picture wants (a landscape shot 240 points tall asks
                // for about 410) and everything around it grows to match: on a
                // 375 point phone the whole tree page sat 19.5 points to the
                // left, the photograph against the left edge and the heart
                // button hanging off the right. One unbounded image moved every
                // element on the screen, and adding maxWidth did not fix it,
                // because a frame's maximum still yields to the image's ideal.
                // An overlay never takes part in layout at all, which is the
                // only version that cannot do this again.
                Color.clear
                    .frame(height: 240)
                    .overlay {
                        AsyncImage(url: url) { img in
                            img.resizable().aspectRatio(contentMode: .fill)
                        } placeholder: {
                            heroFallback
                        }
                    }
                    .clipped()
                    .clipShape(.rect(cornerRadius: 14))
                if let c = Photos.credit(p) {
                    Text(c)
                        .font(.caption2)
                        .foregroundStyle(.secondary)
                        .lineLimit(2)
                }
            }
        } else {
            heroFallback.frame(height: 200).clipShape(.rect(cornerRadius: 14))
        }
    }

    /// The tree, and whatever else of ours is within a few streets, because the
    /// second most useful thing after "where is it" is "is it worth the trip on
    /// its own or are there three more round the corner".
    private var nearbyTrees: [Tree] {
        catalogue.nearest(to: tree.lat, tree.lng, limit: 8, withinKm: 0.5).map(\.tree)
    }

    /// Not a second map: a way to the map.
    ///
    /// The first version of this was an interactive 220 point map sitting three
    /// inches from the tab that opens the real one, which is duplication rather
    /// than navigation (Hidde, 2026-08-20). A picture cannot be mistaken for a
    /// map you should be pinching, and the whole picture is the button.
    private var mapCard: some View {
        Button {
            navigator.showOnMap = tree.id
        } label: {
            ZStack(alignment: .bottomLeading) {
                MapInset(lat: tree.lat, lng: tree.lng, side: nil, height: 150)
                LinearGradient(colors: [.clear, .black.opacity(0.45)],
                               startPoint: .center, endPoint: .bottom)
                HStack(spacing: 6) {
                    Image(systemName: "map.fill").font(.caption)
                    Text("Show on the map").font(.brand(15, .bold, relativeTo: .subheadline))
                    Spacer()
                    Image(systemName: "arrow.up.right").font(.caption)
                }
                .foregroundStyle(.white)
                .padding(14)
            }
            .frame(height: 150)
            .clipShape(.rect(cornerRadius: 14))
            .shadow(color: .black.opacity(0.07), radius: 8, y: 3)
        }
        .buttonStyle(.plain)
    }

    private var heroFallback: some View {
        ZStack {
            LinearGradient(colors: [Color(red: 0.20, green: 0.35, blue: 0.20),
                                    Color(red: 0.36, green: 0.49, blue: 0.31)],
                           startPoint: .topLeading, endPoint: .bottomTrailing)
            VStack(spacing: 10) {
                SpeciesMark(species: tree.species, color: .white.opacity(0.9))
                    .frame(width: 78, height: 78)
                Text("No photograph of this tree yet.")
                    .font(.caption2).foregroundStyle(.white.opacity(0.8))
                    .multilineTextAlignment(.center).padding(.horizontal, 28)
            }
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(tree.name)
                .font(.brand(32, .black, relativeTo: .largeTitle))
                .foregroundStyle(Brand.ink)
            Text(tree.species).font(.subheadline).foregroundStyle(Brand.inkSoft)
        }
    }

    /// Four facts with their units labelled, the way AllTrails does it and the
    /// way our own website already does on a tree page.
    private var facts: some View {
        HStack(alignment: .top, spacing: 0) {
            fact(tree.age ?? "not recorded", "Age")
            Divider().frame(height: 34)
            fact(tree.neighbourhood, "Where")
            Divider().frame(height: 34)
            fact(tree.precision == .confirmed ? "Exact" : "Approximate", "Pin")
        }
        .padding(.vertical, 14)
        .frame(maxWidth: .infinity)
        .brandCard(14)
    }

    private func fact(_ value: String, _ label: String) -> some View {
        // Leading, not centred: a centred value starts wherever its width
        // puts it, so "up to 1,500 years" sat seven points right of the card
        // edge and the layout gate read it as a drift. The fourteen matches
        // the card's own inset elsewhere on the page.
        VStack(alignment: .leading, spacing: 3) {
            Text(value).font(.brand(14, .bold, relativeTo: .footnote))
                .foregroundStyle(Brand.ink).multilineTextAlignment(.leading)
                .lineLimit(2).minimumScaleFactor(0.8)
            Text(label).font(.caption2).foregroundStyle(Brand.inkSoft)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(.horizontal, 14)
    }

    /// The one warning this product must never soften. An approximate pin that
    /// says so sends somebody to the right park knowing they will have to look;
    /// one that pretends to be exact sends them to a spot where the tree is not.
    private var approximateNote: some View {
        Label {
            Text("This pin marks the area, not the trunk. You may have to look around once you are there.")
        } icon: {
            Image(systemName: "scope")
        }
        .font(.footnote)
        .padding(12)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color.orange.opacity(0.12), in: .rect(cornerRadius: 10))
    }

    private var story: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(tree.story)
                .lineLimit(showFullStory ? nil : 6)
                .animation(.default, value: showFullStory)
            if !showFullStory {
                Button("Read the whole story") { showFullStory = true }
                    .font(.footnote.weight(.semibold))
            }
        }
    }

    private var accessBlock: some View {
        VStack(alignment: .leading, spacing: 10) {
            Label(tree.access, systemImage: "figure.walk")
            Label(tree.transport, systemImage: "tram.fill")
        }
        .font(.footnote)
        .foregroundStyle(.secondary)
    }

    /// The highest-intent moment there is for this feature: you are on a tree
    /// with no photograph, and 1077 of our 1435 trees are in that state. Asking
    /// here beats a row in settings, and it measures demand for the feature
    /// exactly where somebody would use it.
    private var offerPhoto: some View {
        LockedRow(feature: .photoUpload) {
            HStack(alignment: .top, spacing: 12) {
                SpeciesMark(species: tree.species,
                            color: Color(red: 0.20, green: 0.35, blue: 0.20).opacity(0.55))
                    .frame(width: 34, height: 34)
                VStack(alignment: .leading, spacing: 3) {
                    Text("Nobody has photographed this one")
                        .font(.brand(16, .bold, relativeTo: .subheadline))
                        .foregroundStyle(Brand.ink)
                    Text("If you are standing in front of it, yours could be the picture on this page.")
                        .font(.caption).foregroundStyle(.secondary)
                }
            }
            .padding(.vertical, 4)
        }
        .padding(14)
        .frame(maxWidth: .infinity, alignment: .leading)
        .brandCard(12)
    }

    private var actionBar: some View {
        HStack(spacing: 10) {
            Button {
                MKMapItem(placemark: .init(coordinate: .init(latitude: tree.lat, longitude: tree.lng)))
                    .openInMaps(launchOptions: [MKLaunchOptionsDirectionsModeKey:
                                                MKLaunchOptionsDirectionsModeWalking])
            } label: {
                Label("Take me there", systemImage: "location.fill")
            }
            .buttonStyle(BrandButtonStyle())

            Button {
                saved.toggleVisited(tree.id)
                // The strongest moment this product has: somebody is standing in
                // front of the thing and has just made a record of it. If we are
                // ever going to ask, it is here.
                if saved.isVisited(tree.id) {
                    nudge.ticked(treeName: tree.name,
                                 signedIn: account.isSignedIn,
                                 total: saved.visitedCount)
                }
            } label: {
                Image(systemName: saved.isVisited(tree.id) ? "checkmark.seal.fill" : "checkmark.seal")
                    .font(.title3)
                    .foregroundStyle(saved.isVisited(tree.id) ? Brand.moss : Brand.inkSoft)
                    .frame(width: 52, height: 52)
                    .background(Brand.surface, in: .circle)
                    .overlay { Circle().strokeBorder(Brand.hairline, lineWidth: 1) }
            }
            .buttonStyle(.plain)
            .accessibilityLabel(saved.isVisited(tree.id)
                                ? "Ticked off. Tap to undo"
                                : "I have stood in front of this tree")
            .sensoryFeedback(.success, trigger: saved.isVisited(tree.id)) { _, now in now }

            Button {
                saved.toggleSaved(tree.id)
                if saved.isSaved(tree.id) {
                    nudge.saved(count: saved.savedCount, signedIn: account.isSignedIn)
                }
            } label: {
                Image(systemName: saved.isSaved(tree.id) ? "heart.fill" : "heart")
                    .font(.title3)
                    .foregroundStyle(saved.isSaved(tree.id) ? .pink : Brand.inkSoft)
                    .frame(width: 52, height: 52)
                    .background(Brand.surface, in: .circle)
                    .overlay { Circle().strokeBorder(Brand.hairline, lineWidth: 1) }
            }
            .buttonStyle(.plain)
            .accessibilityLabel(saved.isSaved(tree.id) ? "Saved. Tap to remove" : "Save this tree")
            .sensoryFeedback(.selection, trigger: saved.isSaved(tree.id))
        }
        // The same 20 as the page's content above it; at 16 the bar began
        // four points left of every paragraph, which is the drift the layout
        // gate exists to catch.
        .padding(.horizontal, 20)
        .padding(.bottom, 8)
        .padding(.top, 10)
        // Opaque, with a short fade above it. At 96 percent the story showed
        // through the bar as ghost text, which reads as a rendering fault
        // rather than as translucency.
        .background(alignment: .top) {
            VStack(spacing: 0) {
                LinearGradient(colors: [Brand.ground.opacity(0), Brand.ground],
                               startPoint: .top, endPoint: .bottom)
                    .frame(height: 18)
                Brand.ground
            }
            .ignoresSafeArea(edges: .bottom)
        }
    }
}
