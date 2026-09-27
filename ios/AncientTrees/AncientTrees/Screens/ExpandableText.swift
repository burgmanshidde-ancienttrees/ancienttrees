// Text cut to a few lines with "Read more" under it, expanded in place.
//
// Convention: AllTrails' trail description and the App Store's app
// description both show a few lines and a "more" that opens the rest where it
// stands, with no sheet and no second page. Airbnb opens a sheet instead,
// which suits a listing with headings and is heavier than a paragraph needs.
// Hidde, 2026-09-27, on a tree page whose story and access notes ran to two
// screens: "dit is nogal veel tekst ... afkappen en read more logischer, ook
// op web". The website does the same with .td-clamp in TreeDetail.astro.
//
// "Read more" appears only when the text really is cut: a short story gets no
// button, because a control that reveals nothing is noise.

import SwiftUI

struct ExpandableText: View {
    let text: String
    var lines: Int = 6
    @State private var expanded = false
    @State private var fullHeight: CGFloat = 0
    @State private var cutHeight: CGFloat = 0

    private var isCut: Bool { !expanded && fullHeight > cutHeight + 1 }

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
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
            if isCut {
                Button { withAnimation(.snappy) { expanded = true } } label: {
                    // The surrounding font, bolder: the story's size under a
                    // story, the footnote's under an access line.
                    Text("Read more")
                        .fontWeight(.semibold)
                        .foregroundStyle(Brand.moss)
                        .padding(.top, 4)
                        // A 44-point target without a 44-point gap: the frame
                        // keeps its height for the finger and gives most of it
                        // back to the layout, so the next block sits where it
                        // would under plain text (Hidde, 2026-09-27: "the
                        // vertical spacing feels off").
                        .frame(minHeight: 44, alignment: .topLeading)
                        .contentShape(.rect)
                }
                .buttonStyle(.plain)
                .padding(.bottom, -18)
                .accessibilityIdentifier("read-more")
            }
        }
    }
}
