// A map with a sheet over it. ONE of them, used everywhere it appears.
//
// Hidde, 2026-08-26: "je wilt deze interactie als component hebben en overal
// hetzelfde hebben." He is describing the rule this project already runs on,
// which is that a user-facing thing ships as a shared component because parity
// by hand does not survive contact with the page count. It arrived the hard way
// here: My trees got three different arrangements in one evening, a still cover
// that could not be panned, a scroll view that fought his finger, and finally
// the shape the map screen has had all along.
//
// The interaction lives in BottomSheet and is not repeated here. What this adds
// is the arrangement around it, so a second screen cannot get the stacking, the
// safe areas or the sheet's starting height subtly different from the first:
//
//   - the map fills the screen and runs under the status bar
//   - the sheet lies over it, holding a header that never scrolls
//   - anything that floats over both, a gear or a chip row, goes in `overlay`
//
// Adding a third screen with this shape should be an instance of this view and
// nothing else.

import SwiftUI

struct MapWithSheet<Map: View, Header: View, Content: View, Floating: View>: View {
    @Binding var height: SheetHeight
    /// Which item is at the top of the list, when the caller's content marks
    /// its items as scroll targets and the map wants to follow along.
    var topItem: Binding<String?>? = nil

    @ViewBuilder var map: Map
    @ViewBuilder var header: Header
    @ViewBuilder var content: Content
    /// Controls that sit over both, like the map screen's search field or the
    /// gear on My trees. Empty on a screen that has none.
    @ViewBuilder var floating: Floating

    var body: some View {
        ZStack(alignment: .top) {
            map
                .ignoresSafeArea(edges: [.top, .horizontal])
            BottomSheet(height: $height, topItem: topItem, header: { header },
                        content: { content })
            floating
        }
    }
}

extension MapWithSheet where Floating == EmptyView {
    /// The three-slot form, for a screen with nothing floating over both.
    /// The memberwise initialiser wants values rather than builders once the
    /// properties are @ViewBuilder, which is why this hands them straight in.
    init(height: Binding<SheetHeight>,
         topItem: Binding<String?>? = nil,
         @ViewBuilder map: () -> Map,
         @ViewBuilder header: () -> Header,
         @ViewBuilder content: () -> Content) {
        self._height = height
        self.topItem = topItem
        self.map = map()
        self.header = header()
        self.content = content()
        self.floating = EmptyView()
    }
}
