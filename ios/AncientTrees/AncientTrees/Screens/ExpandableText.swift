// Text cut to a few lines with "more" on its last line, opened in place.
//
// Convention: AllTrails' trail description and the App Store's app
// description both show a few lines and a "more" that opens the rest where it
// stands, with no sheet and no second page. Airbnb opens a sheet instead,
// which suits a listing with headings and is heavier than a paragraph needs.
// Hidde, 2026-09-27, on a tree page whose story and access notes ran to two
// screens: "dit is nogal veel tekst ... afkappen en read more logischer, ook
// op web". The website does the same with .td-clamp in TreeDetail.astro.
//
// THE APP STORE'S SHAPE since 2026-10-30 (Hidde: the "Read more" button was
// "een beetje raar" and had "een raar effect als je erop klikt"; CONVENTIONS.md
// "Long text on a tree page: Read more"). The App Store puts "more" at the end
// of the last visible line, the line fading out under it, and a tap anywhere
// on the text opens the rest AT ONCE: no animation, no "less". The animated
// line limit was the odd effect: SwiftUI cross-fades a text whose line count
// changes, so the paragraph flickered while the page under it slid.
//
// "more" appears only when the text really is cut: a short story gets no
// control, because a control that reveals nothing is noise.

import SwiftUI

struct ExpandableText: View {
    /// Attributed, so the story keeps its quoted readers' words and links.
    let text: AttributedString
    var lines: Int = 6

    init(text: String, lines: Int = 6) {
        self.text = AttributedString(text)
        self.lines = lines
    }

    init(text: AttributedString, lines: Int = 6) {
        self.text = text
        self.lines = lines
    }
    @State private var expanded = false
    @State private var fullHeight: CGFloat = 0
    @State private var cutHeight: CGFloat = 0

    private var isCut: Bool { !expanded && fullHeight > cutHeight + 1 }

    var body: some View {
        Text(text)
            .lineLimit(expanded ? nil : lines)
            .fixedSize(horizontal: false, vertical: true)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(GeometryReader { g in
                Color.clear
                    .onAppear { cutHeight = g.size.height }
                    .onChange(of: g.size.height) { _, h in cutHeight = h }
            })
            // The same text uncut, invisible, to learn whether the cut
            // one is hiding anything.
            .background(alignment: .topLeading) {
                Text(text)
                    .fixedSize(horizontal: false, vertical: true)
                    .hidden()
                    .background(GeometryReader { g in
                        Color.clear
                            .onAppear { fullHeight = g.size.height }
                            .onChange(of: g.size.height) { _, h in fullHeight = h }
                    })
                    .accessibilityHidden(true)
            }
            .overlay(alignment: .bottomTrailing) {
                if isCut {
                    HStack(spacing: 0) {
                        LinearGradient(colors: [Color(.systemBackground).opacity(0), Color(.systemBackground)],
                                       startPoint: .leading, endPoint: .trailing)
                            .frame(width: 44)
                        // The surrounding font, bolder: the story's size in a
                        // story, the footnote's in an access line.
                        Text("more")
                            .fontWeight(.semibold)
                            .foregroundStyle(Brand.moss)
                            .padding(.leading, 2)
                            .background(Color(.systemBackground))
                    }
                    .fixedSize(horizontal: false, vertical: true)
                    .accessibilityHidden(true)
                }
            }
            .contentShape(.rect)
            .onTapGesture {
                guard isCut else { return }
                var t = Transaction()
                t.disablesAnimations = true
                withTransaction(t) { expanded = true }
            }
            .accessibilityAddTraits(isCut ? .isButton : [])
            .accessibilityHint(isCut ? "Shows the rest" : "")
            .accessibilityIdentifier(isCut ? "read-more" : "")
    }
}
