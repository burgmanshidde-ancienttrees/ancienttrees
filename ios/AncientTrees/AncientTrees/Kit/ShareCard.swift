// A picture of a tree you added, made to be posted somewhere else.
//
// CONVENTION: Strava, and it is the one product that has our exact problem.
// A tree only you have holds no address on the web (TreeDetail says so where
// it withholds the toolbar's share button), so there is nothing to send
// anybody and a link would be an invention. Strava answers this by sharing an
// IMAGE rather than a URL: tap share on an activity and it draws a card from
// your own photograph or your map, puts the facts and its own mark on it, and
// hands that to the system sheet. If the activity carries photographs it asks
// which one; ours always has one, so it never asks.
//
// Read 2026-09-02:
// - https://support.strava.com/hc/en-us/articles/221089587-Sharing-Your-Strava-Activities
// See CONVENTIONS.md, "Sharing something you made that has no page".
//
// 4:5 and 1080 wide, which is the portrait shape Instagram, WhatsApp and
// Messages all show without cropping into it. A 9:16 story card is the other
// half of what Strava draws and it is a second size for the day somebody asks.

import SwiftUI
import UIKit

enum ShareCard {

    static let size = CGSize(width: 1080, height: 1350)

    /// The card, drawn from a tree of yours. Never nil: a sighting whose
    /// photograph has gone missing still gets a card with the species mark on
    /// it, the same fallback the page itself shows, because a share button
    /// that disappears in one case is a control nobody learns.
    @MainActor
    static func render(photo: UIImage?, name: String, species: String?, date: Date) -> UIImage {
        let renderer = ImageRenderer(content:
            Card(photo: photo, name: name, species: species, date: date)
                .frame(width: size.width, height: size.height))
        // 1, because the frame above is already in pixels. Leaving it at the
        // screen's scale would draw a 3240 point card on a modern phone.
        renderer.scale = 1
        return renderer.uiImage ?? UIImage(cgImage: UIImage().cgImage ?? blank())
    }

    private static func blank() -> CGImage {
        UIGraphicsImageRenderer(size: CGSize(width: 1, height: 1)).image { _ in }.cgImage!
    }

    private struct Card: View {
        let photo: UIImage?
        let name: String
        let species: String?
        let date: Date

        private var when: String {
            let f = DateFormatter()
            f.dateFormat = "d MMMM yyyy"
            return f.string(from: date)
        }

        var body: some View {
            ZStack(alignment: .bottomLeading) {
                if let photo {
                    Image(uiImage: photo)
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                } else {
                    ZStack {
                        Brand.surfaceMuted
                        SpeciesMark(species: species ?? "", color: Brand.inkSoft.opacity(0.5))
                            .frame(width: 320, height: 320)
                    }
                }
                // The words sit on the photograph, so they need their own
                // ground: a dark gradient rather than a bar, which is what
                // every card of this kind does and what keeps the picture
                // whole.
                LinearGradient(colors: [.clear, .black.opacity(0.75)],
                               startPoint: .center, endPoint: .bottom)
                VStack(alignment: .leading, spacing: 14) {
                    Text(name)
                        .font(.brand(76, .bold))
                        .foregroundStyle(.white)
                        .lineLimit(3)
                        .minimumScaleFactor(0.6)
                    HStack(spacing: 16) {
                        Text([species, when].compactMap { $0 }
                                .filter { !$0.isEmpty }
                                .joined(separator: " · "))
                            .font(.brand(34, .regular))
                            .foregroundStyle(.white.opacity(0.85))
                        Spacer(minLength: 0)
                        // Our own mark, small, the way Strava's sits in the
                        // corner of theirs. It is the whole reason a shared
                        // picture is worth drawing rather than sending the
                        // photograph on its own.
                        Text("ancienttrees.app")
                            .font(.brand(30, .bold))
                            .foregroundStyle(.white.opacity(0.85))
                    }
                }
                .padding(64)
            }
            .frame(width: size.width, height: size.height)
            .clipped()
        }
    }
}
