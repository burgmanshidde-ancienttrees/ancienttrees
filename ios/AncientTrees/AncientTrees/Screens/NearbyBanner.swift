// "You're 40 m from The Pacifier Tree": a banner when the app is open and you
// come within 50 metres of a tree (Hidde, 2026-10-10: "should we build some
// sort of overlay ... if the app is open and you're actually close to a tree",
// then "the overlay looks good", and "i would still show it on the map page").
//
// Convention: the Geocaching app buzzes within 10 metres of a cache, and Cachly
// and Locus Map let you set the radius; Swarm reminds you to check in where you
// arrive, with notifications switched on. All of them say it once and get out
// of the way, so this is a banner from the top, never a sheet, gone after eight
// seconds, once per tree per launch, and never with the app closed. Google's
// Field Trip, which alerted from the background, is the cautionary case.
// Board "Near a tree" on the Discover canvas.
import SwiftUI

struct NearbyBanner: View {
    let tree: Tree
    let meters: Int
    let open: () -> Void
    let dismiss: () -> Void

    var body: some View {
        HStack(spacing: 12) {
            Button(action: open) {
                HStack(spacing: 12) {
                    Color.clear.frame(width: 48, height: 48)
                        .overlay {
                            if let url = tree.photo?.card {
                                TreePhoto(url: url) { Brand.surfaceMuted }
                            } else {
                                Brand.surfaceMuted
                            }
                        }
                        .clipShape(.rect(cornerRadius: 12))
                    VStack(alignment: .leading, spacing: 1) {
                        Text("You are \(meters) m from \(tree.name)")
                            .font(.subheadline.weight(.semibold))
                            .foregroundStyle(Brand.ink)
                            .lineLimit(2)
                            .multilineTextAlignment(.leading)
                        Text("You can open it to collect it")
                            .font(.footnote)
                            .foregroundStyle(Brand.inkSoft)
                    }
                    Spacer(minLength: 0)
                }
                .contentShape(.rect)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("nearby-open")
            Button(action: dismiss) {
                Image(systemName: "xmark")
                    .font(.system(size: 13, weight: .bold))
                    .foregroundStyle(Brand.inkSoft)
                    .frame(width: 44, height: 44)
            }
            .buttonStyle(.plain)
            .accessibilityLabel("Dismiss")
            .accessibilityIdentifier("nearby-dismiss")
        }
        .padding(.leading, 10).padding(.vertical, 8)
        .background(Brand.surface, in: .rect(cornerRadius: 20))
        .shadow(color: .black.opacity(0.2), radius: 16, y: 6)
        .padding(.horizontal, 10)
        .padding(.top, 6)
        .transition(.move(edge: .top).combined(with: .opacity))
        .accessibilityElement(children: .contain)
        .accessibilityIdentifier("nearby-banner")
    }
}
