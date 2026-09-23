// A tree you told us about in words, as a card.
//
// Convention: CONVENTIONS.md, "Landing after you have added something".
// Google Maps puts a place you submitted under Your contributions and keeps a
// STATUS on it until the review is over, which is the half a toast cannot do.
// iNaturalist does the same with an observation's upload state. We had the
// acknowledgement and not the status, on either surface.
//
// It is deliberately NOT a MineCard. That card is for a tree you photographed,
// which has an image, a place on your map and a page of its own. This one has
// none of those yet: it is a sentence somebody typed, and the honest card says
// what it is and where it stands rather than dressing it as a tree page.
import SwiftUI

struct SentCard: View {
    let sent: Submission.Sent

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack(spacing: 8) {
                Text(sent.title)
                    .font(.cardTitle).foregroundStyle(Brand.ink)
                    .lineLimit(2).multilineTextAlignment(.leading)
                Spacer(minLength: 6)
                Text("You sent this")
                    .font(.caption2.weight(.semibold))
                    .foregroundStyle(Brand.moss)
                    .padding(.horizontal, 8).padding(.vertical, 4)
                    .background(Brand.moss.opacity(0.15), in: .capsule)
            }
            HStack(spacing: 6) {
                if !sent.tree.isEmpty, !sent.city.isEmpty { Text(sent.city); Text("·") }
                if let d = sent.sentAt {
                    Text(d.formatted(date: .abbreviated, time: .omitted))
                    Text("·")
                }
                Text(sent.status.label)
                    .foregroundStyle(sent.status == .published ? Brand.moss : Brand.inkSoft)
                // There is no way to edit a tip, so refining one means sending
                // it again. Saying how many times is what tells somebody the
                // earlier ones arrived.
                if sent.times > 1 {
                    Text("·")
                    Text("sent \(sent.times) times")
                }
            }
            .font(.caption).foregroundStyle(Brand.inkSoft)

            // What we wrote back, where we have. A four-state label says which
            // state it is in; this says what actually happened to the tree.
            if let reply = sent.reply?.split(separator: "\n").first, !reply.isEmpty {
                Text(String(reply))
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
                    .padding(.top, 2)
            }
        }
        .padding(.horizontal, 14).padding(.vertical, 12)
        .frame(maxWidth: .infinity, alignment: .leading)
        .brandCard()
    }
}
