// A bottom sheet that does not cover the tab bar, and that hands the gesture
// back and forth with the list inside it.
//
// SwiftUI's .sheet is presented over everything, tab bar included, which is
// exactly wrong here: Google Maps keeps its tab bar visible under the sheet and
// you can switch tabs without dismissing anything. So this is an overlay in the
// view rather than a presentation, with the same three heights and the same
// drag.
//
// THE ARBITRATION, which is the whole thing and took two goes to get right.
//
// One finger does one thing at a time, and which one is decided by the state
// rather than by where the finger landed. Apple Maps, Google Maps and Airbnb all
// behave exactly this way and people are trained on it:
//
//   Below full height          the sheet moves, the list does not scroll
//   At full height             the list scrolls
//   At full height, list at
//   the top, dragging DOWN     the sheet moves again, and the sheet closes
//
// The first version only did the first two rules, and Hidde found both halves of
// what that costs within a minute of running it on his own phone: first
// "als ik de lijst omhoog trek ... ga ik dan tussen de bomen scrollen ipv het
// omhoog doen", and then the mirror of it, "als ik de lijst weer naar beneden
// wil slepen ga ik scrollen in de kaart". Two thirds of a rule is not a rule.
//
// That third case is why this file now OWNS the scroll view rather than taking
// whatever the caller passes in. Knowing whether the content is scrolled to the
// top is what the whole handoff turns on, and that fact only exists inside the
// scroll view. Handing it up through a binding from every caller would put the
// same three lines in every screen that uses a sheet, and one of them would
// eventually be wrong.

import SwiftUI

enum SheetHeight: CaseIterable {
    case peek, half, full

    func points(in total: CGFloat) -> CGFloat {
        switch self {
        // Tall enough to clear the floating tab bar AND still show a whole
        // card. At 160 the tab bar ate most of it and the first tree card was
        // sliced in half, which is what the sheet is entirely for.
        case .peek: 268
        case .half: total * 0.52
        case .full: total * 0.92
        }
    }
}

struct BottomSheet<Content: View>: View {
    @Binding var height: SheetHeight
    @ViewBuilder var content: Content

    @State private var drag: CGFloat = 0
    /// Whether the list inside is scrolled to its very top. The handoff downward
    /// is only allowed from there, because taking the gesture mid-list would
    /// yank the sheet away while somebody is reading.
    @State private var atTop = true
    /// Set the moment a downward drag begins at the top, which turns scrolling
    /// off for the rest of that gesture so the two never fight.
    @State private var handingOff = false

    var body: some View {
        GeometryReader { geo in
            let target = height.points(in: geo.size.height)
            let h = min(max(target - drag, 90), geo.size.height * 0.94)
            VStack(spacing: 0) {
                // The grabber is the one handle that always works, including
                // when the content below it is scrolling, because it sits
                // outside the scroll view. So it gets a real target rather than
                // a five point line: the capsule is what you see, the padding
                // around it is what you can actually grab.
                Capsule()
                    .fill(.tertiary)
                    .frame(width: 40, height: 5)
                    .padding(.top, 10).padding(.bottom, 12)
                    .frame(maxWidth: .infinity)
                    .contentShape(.rect)

                ScrollView {
                    content
                        .frame(maxWidth: .infinity, alignment: .top)
                }
                .scrollDisabled(height != .full || handingOff)
                .onScrollGeometryChange(for: CGFloat.self) { $0.contentOffset.y } action: { _, y in
                    atTop = y <= 1
                }
            }
            .frame(height: h)
            .frame(maxWidth: .infinity)
            .background(.regularMaterial)
            .clipShape(.rect(topLeadingRadius: 16, topTrailingRadius: 16))
            .shadow(color: .black.opacity(0.12), radius: 10, y: -3)
            .frame(maxHeight: .infinity, alignment: .bottom)
            // simultaneous, not exclusive: the scroll view has to keep working
            // for every gesture this one does not want.
            .simultaneousGesture(
                DragGesture(minimumDistance: 4)
                    .onChanged { value in
                        // Claim the gesture only in the cases the rules above
                        // describe. Everything else belongs to the list.
                        if height != .full {
                            drag = value.translation.height
                        } else if atTop && value.translation.height > 0 {
                            handingOff = true
                            drag = value.translation.height
                        }
                    }
                    .onEnded { value in
                        defer { handingOff = false }
                        guard drag != 0 else { return }
                        let settled = target - value.translation.height
                        height = SheetHeight.allCases.min {
                            abs($0.points(in: geo.size.height) - settled)
                                < abs($1.points(in: geo.size.height) - settled)
                        } ?? .peek
                        withAnimation(.spring(duration: 0.28)) { drag = 0 }
                    }
            )
            .animation(.spring(duration: 0.28), value: height)
        }
    }
}
