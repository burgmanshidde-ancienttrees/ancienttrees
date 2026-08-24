// A tree only you have, as a card.
//
// One card, used by the map's list and by the Collection screen, because it
// was written twice the moment there were two places to show one (Hidde,
// 2026-08-24: "eigen geuploade bomen moeten ook gewoon in de lijst alleen dan
// met een your tree label erop ofzo").
//
// The label is the whole point. On the map's list your trees sit among ours,
// and without a word saying which is which the reader has to work it out from
// the photograph. It is a chip rather than a different card shape, so the list
// still reads as one list.
import SwiftUI

struct MineCard: View {
    let sighting: Sightings.Sighting
    @Environment(Sightings.self) private var sightings

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            if let img = sightings.image(sighting) {
                Image(uiImage: img)
                    .resizable().aspectRatio(contentMode: .fill)
                    .frame(height: 170).frame(maxWidth: .infinity)
                    .clipped()
            }
            VStack(alignment: .leading, spacing: 6) {
                HStack(spacing: 8) {
                    Text(sighting.name)
                        .font(.cardTitle).foregroundStyle(Brand.ink)
                        .lineLimit(2).multilineTextAlignment(.leading)
                    Spacer(minLength: 6)
                    Text("Your tree")
                        .font(.caption2.weight(.semibold))
                        .foregroundStyle(Brand.moss)
                        .padding(.horizontal, 8).padding(.vertical, 4)
                        .background(Brand.moss.opacity(0.15), in: .capsule)
                }
                HStack(spacing: 6) {
                    Text(sighting.species ?? sighting.date.formatted(date: .abbreviated, time: .omitted))
                    if sighting.status != .mine {
                        Text("·")
                        Text(sighting.status.label)
                            .foregroundStyle(sighting.status == .published ? Brand.moss : Brand.inkSoft)
                    }
                }
                .font(.caption).foregroundStyle(Brand.inkSoft)
            }
            .padding(.horizontal, 14).padding(.vertical, 12)
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .brandCard()
    }
}
