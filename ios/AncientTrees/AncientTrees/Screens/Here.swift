// "Here": the tab that is a verb rather than a place.
//
// Every nature and collecting app has one and it is usually in the middle:
// Strava records, iNaturalist observes, Merlin identifies, AllTrails navigates,
// Google Maps contributes. It is the button you press while you are standing in
// front of the thing, and it is the moment this whole product exists for.
//
// It also answers the open question the AllTrails teardown ended on. They know
// what you did because the phone recorded your track; we are asking somebody to
// tick a tree deliberately, and a deliberate tick reads as homework unless the
// app meets you at the moment you arrive. This screen is that meeting.

import SwiftUI

struct HereView: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    let located: Bool
    @Environment(Saved.self) private var saved

    /// Close enough that you can see it. Beyond this the honest thing is to
    /// point rather than to offer a tick.
    private let arrivedKm = 0.12

    private var nearest: [(tree: Tree, km: Double)] {
        catalogue.nearest(to: origin.lat, origin.lng, limit: 4, withinKm: 25)
    }
    private var arrived: (tree: Tree, km: Double)? {
        nearest.first.flatMap { $0.km <= arrivedKm ? $0 : nil }
    }

    var body: some View {
        ScrollView {
            VStack(spacing: 18) {
                if !located {
                    notice("Location is off, so this screen cannot tell what you are standing in front of. It works without it, just not here.")
                }
                if let hit = arrived {
                    arrivedCard(hit.tree)
                } else if let next = nearest.first {
                    walkingCard(next.tree, km: next.km)
                } else {
                    notice("No tree of ours within twenty-five kilometres. Nothing to tick off here yet.")
                }

                if nearest.count > 1 {
                    VStack(alignment: .leading, spacing: 10) {
                        Text("Also close").font(.footnote.weight(.semibold))
                            .foregroundStyle(.secondary)
                            .frame(maxWidth: .infinity, alignment: .leading)
                        ForEach(nearest.dropFirst(), id: \.tree.id) { hit in
                            NavigationLink {
                                TreeDetail(tree: hit.tree, catalogue: catalogue)
                            } label: {
                                HStack {
                                    VStack(alignment: .leading, spacing: 2) {
                                        Text(hit.tree.name).font(.subheadline.weight(.medium))
                                        Text(hit.tree.commonName).font(.caption)
                                            .foregroundStyle(.secondary)
                                    }
                                    Spacer()
                                    Text(fmt(hit.km)).font(.caption).foregroundStyle(.secondary)
                                        .monospacedDigit()
                                }
                                .padding(.vertical, 8)
                            }
                            .buttonStyle(.plain)
                            Divider()
                        }
                    }
                    .padding(.horizontal, 4)
                }
            }
            .padding(20)
        }
        .navigationTitle("Here")
    }

    /// You are at it. One big irreversible-feeling action and nothing competing
    /// with it.
    private func arrivedCard(_ t: Tree) -> some View {
        VStack(spacing: 14) {
            Text("You are standing in front of").font(.footnote).foregroundStyle(.secondary)
            Text(t.name).font(.title.bold()).multilineTextAlignment(.center)
            Text(t.commonName).font(.subheadline).foregroundStyle(.secondary)

            Button {
                saved.toggleVisited(t.id)
            } label: {
                Label(saved.isVisited(t.id) ? "Ticked off" : "I have seen this one",
                      systemImage: saved.isVisited(t.id) ? "checkmark.seal.fill" : "checkmark.seal")
                    .font(.headline).frame(maxWidth: .infinity).padding(.vertical, 16)
            }
            .buttonStyle(.borderedProminent)
            .tint(saved.isVisited(t.id) ? .gray : Color(red: 0.20, green: 0.35, blue: 0.20))

            NavigationLink("Read why it is worth it") {
                TreeDetail(tree: t, catalogue: catalogue)
            }
            .font(.footnote.weight(.semibold))
        }
        .padding(22)
        .frame(maxWidth: .infinity)
        .background(Color(.secondarySystemBackground), in: .rect(cornerRadius: 16))
    }

    /// You are not at it yet. Point, do not offer a tick: a tick you can press
    /// from your sofa is worth nothing to collect.
    private func walkingCard(_ t: Tree, km: Double) -> some View {
        VStack(spacing: 12) {
            Text("Nearest tree").font(.footnote).foregroundStyle(.secondary)
            Text(t.name).font(.title2.bold()).multilineTextAlignment(.center)
            Text("\(fmt(km)) away, about \(Geo.walkingMinutes(km: km)) min on foot")
                .font(.subheadline).foregroundStyle(.secondary)
            NavigationLink {
                TreeDetail(tree: t, catalogue: catalogue)
            } label: {
                Label("Take me there", systemImage: "location.fill")
                    .font(.headline).frame(maxWidth: .infinity).padding(.vertical, 15)
            }
            .buttonStyle(.borderedProminent)
            .tint(Color(red: 0.20, green: 0.35, blue: 0.20))
        }
        .padding(22)
        .frame(maxWidth: .infinity)
        .background(Color(.secondarySystemBackground), in: .rect(cornerRadius: 16))
    }

    private func notice(_ s: String) -> some View {
        Text(s).font(.footnote).foregroundStyle(.secondary)
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(14)
            .background(Color(.secondarySystemBackground), in: .rect(cornerRadius: 10))
    }

    private func fmt(_ km: Double) -> String {
        km < 1 ? "\(Int((km * 1000).rounded())) m" : String(format: "%.1f km", km)
    }
}
