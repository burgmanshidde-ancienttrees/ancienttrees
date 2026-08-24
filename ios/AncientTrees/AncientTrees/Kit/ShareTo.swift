// The share control, in one place so three screens cannot drift apart.
//
// Hidde, 2026-08-24: a share button on beautiful trees and beautiful cities,
// consistent, and copied rather than designed. His own frames settled the
// shape: AllTrails and komoot both hang it top-right of the page, and komoot's
// opens the plain system sheet with a link preview rather than a sheet of its
// own. So this is ShareLink in a toolbar item, nothing more.
//
// The website carries the same button beside its titles, on the same three
// page types, for the same reason: a person who finds a tree on a phone and
// sends it from a laptop is one person.
//
// The 44 by 44 frame is not decoration. A bare toolbar glyph measured 37 by 13
// in the app's own layout check, and appfit fails on anything under Apple's
// floor.
import SwiftUI

struct ShareTo: ToolbarContent {
    let url: URL
    let subject: String
    let message: String
    var label: String = "Share"

    var body: some ToolbarContent {
        ToolbarItem(placement: .topBarTrailing) {
            ShareLink(item: url, subject: Text(subject), message: Text(message)) {
                Image(systemName: "square.and.arrow.up")
                    .frame(width: 44, height: 44)
                    .contentShape(.rect)
            }
            .accessibilityLabel(label)
        }
    }
}
