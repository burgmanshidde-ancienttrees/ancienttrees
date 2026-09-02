// The system share sheet, presented after work rather than before it.
//
// CONVENTION: Apple's own. `UIActivityViewController` is the share sheet every
// iPhone owner knows, and `ShareLink` is SwiftUI's wrapper around exactly this.
// The wrapper is what the rest of the app uses and what it should keep using;
// this exists for the one case it cannot serve, which is sharing something
// that does not exist until the button is tapped. A ShareLink needs its item
// up front, and a tree's unlisted page is made by a network call at the moment
// somebody asks for it.
//
// Both things go in: the link and the picture. That is deliberate and it is
// what the sheet is for. Messages takes both, Instagram takes the picture,
// Copy takes the link, and each target picks what it can use rather than us
// guessing for them.
import SwiftUI
import UIKit

struct ShareSheet: UIViewControllerRepresentable {
    let items: [Any]

    func makeUIViewController(context: Context) -> UIActivityViewController {
        UIActivityViewController(activityItems: items, applicationActivities: nil)
    }

    func updateUIViewController(_ c: UIActivityViewController, context: Context) {}
}
