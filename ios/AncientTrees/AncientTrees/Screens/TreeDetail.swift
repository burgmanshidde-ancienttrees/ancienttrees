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
    @State private var showFullStory = false
    @State private var reporting = false

    var body: some View {
        ZStack(alignment: .bottom) {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    hero
                    header
                    facts
                    if tree.precision.needsWarning { approximateNote }
                    story
                    accessBlock
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
        .navigationTitle(tree.name)
        .navigationBarTitleDisplayMode(.inline)
        .sheet(isPresented: $reporting) { ContributeView(about: tree) }
    }

    /// The photograph, or the species drawn, edge to edge. AllTrails leads every
    /// route with a picture and it is most of why their pages feel like an
    /// invitation rather than a database record.
    @ViewBuilder private var hero: some View {
        if let p = tree.photo, let url = Photos.thumb(p.url, width: 960) {
            AsyncImage(url: url) { img in
                img.resizable().aspectRatio(contentMode: .fill)
            } placeholder: {
                heroFallback
            }
            .frame(height: 240)
            .clipped()
            .clipShape(.rect(cornerRadius: 14))
            // Same reason as the card: on the image the credit is clipped away
            // with the overflow, and a CC BY-SA photograph without its credit is
            // a licence breach.
            .overlay(alignment: .bottomLeading) {
                if let c = Photos.credit(p) {
                    Text(c).font(.system(size: 10)).foregroundStyle(.white.opacity(0.95))
                        .padding(.horizontal, 7).padding(.vertical, 4)
                        .background(.black.opacity(0.45), in: .rect(cornerRadius: 5))
                        .padding(8)
                }
            }
        } else {
            heroFallback.frame(height: 200).clipShape(.rect(cornerRadius: 14))
        }
    }

    private var heroFallback: some View {
        ZStack {
            LinearGradient(colors: [Color(red: 0.20, green: 0.35, blue: 0.20),
                                    Color(red: 0.36, green: 0.49, blue: 0.31)],
                           startPoint: .topLeading, endPoint: .bottomTrailing)
            VStack(spacing: 10) {
                SpeciesMark(species: tree.species, color: .white.opacity(0.9))
                    .frame(width: 78, height: 78)
                Text("Nobody has published a photograph of this tree under a licence we can use.")
                    .font(.caption2).foregroundStyle(.white.opacity(0.8))
                    .multilineTextAlignment(.center).padding(.horizontal, 28)
            }
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(tree.name).font(.largeTitle.bold())
            Text(tree.species).font(.subheadline).foregroundStyle(.secondary)
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
        .padding(.vertical, 12)
        .frame(maxWidth: .infinity)
        .background(Color(.secondarySystemBackground), in: .rect(cornerRadius: 12))
    }

    private func fact(_ value: String, _ label: String) -> some View {
        VStack(spacing: 3) {
            Text(value).font(.footnote.weight(.semibold)).multilineTextAlignment(.center)
                .lineLimit(2).minimumScaleFactor(0.8)
            Text(label).font(.caption2).foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding(.horizontal, 6)
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
                        .font(.subheadline.weight(.semibold))
                    Text("If you are standing in front of it, yours could be the picture on this page.")
                        .font(.caption).foregroundStyle(.secondary)
                }
            }
            .padding(.vertical, 4)
        }
        .padding(14)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(.secondarySystemBackground), in: .rect(cornerRadius: 12))
    }

    private var actionBar: some View {
        HStack(spacing: 10) {
            Button {
                MKMapItem(placemark: .init(coordinate: .init(latitude: tree.lat, longitude: tree.lng)))
                    .openInMaps(launchOptions: [MKLaunchOptionsDirectionsModeKey:
                                                MKLaunchOptionsDirectionsModeWalking])
            } label: {
                Label("Take me there", systemImage: "location.fill")
                    .font(.headline).frame(maxWidth: .infinity).padding(.vertical, 14)
            }
            .buttonStyle(.borderedProminent)
            .tint(Color(red: 0.20, green: 0.35, blue: 0.20))

            Button {
                saved.toggleVisited(tree.id)
            } label: {
                Image(systemName: saved.isVisited(tree.id) ? "checkmark.seal.fill" : "checkmark.seal")
                    .font(.headline).padding(.vertical, 14).padding(.horizontal, 16)
            }
            .buttonStyle(.bordered)

            Button {
                saved.toggleSaved(tree.id)
            } label: {
                Image(systemName: saved.isSaved(tree.id) ? "heart.fill" : "heart")
                    .font(.headline).padding(.vertical, 14).padding(.horizontal, 16)
            }
            .buttonStyle(.bordered)
        }
        .padding(.horizontal, 16)
        .padding(.bottom, 8)
        .padding(.top, 10)
        .background(.bar)
    }
}
