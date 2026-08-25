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
    case peek, card, half, full

    func points(in total: CGFloat) -> CGFloat {
        switch self {
        // Tall enough to clear the floating tab bar AND still show a whole
        // card. At 160 the tab bar ate most of it and the first tree card was
        // sliced in half, which is what the sheet is entirely for.
        // Tall enough for the count AND the top of the first photograph,
        // which is the invitation to scroll (Hidde, 2026-08-22, and Komoot
        // does the same). Not tappable at this height, so it invites without
        // catching a thumb.
        case .peek: 168
        // ONE selected tree, and nothing else. Sized to the card rather than
        // to the screen, because a half-screen sheet holding a single card is
        // mostly empty (Hidde, 2026-08-24, on his own phone: "het is best wel
        // onzinnig om de lijst die naar boven komt groter te maken dan de
        // content die het laat zien"). He is right and it is not the
        // convention either: Apple Maps, Google Maps and AllTrails all raise a
        // short card for one tapped place and keep the taller stop for a list.
        case .card: 400
        case .half: total * 0.52
        // Full stops 124 points short of the top, never 8 percent of it: on
        // an iPhone SE 8 percent is 53 points, and the sheet's search field
        // then sat under the floating chip row, which is 116 points deep.
        // A field you cannot reach at full height is no field (2026-08-21,
        // found by a UI test whose second press kept landing on a chip).
        case .full: min(total * 0.92, total - 124)
        }
    }
}

struct BottomSheet<Header: View, Content: View>: View {
    @Binding var height: SheetHeight
    /// Which item is at the top of the list, when the content marks its items
    /// as scroll targets. The map reads this so it can follow what you are
    /// reading (Hidde, 2026-08-24: "dat de kaart mee hovert naar die andere
    /// boom als je door de lijst gaat"). Optional, because a sheet holding a
    /// walk has nothing to report.
    var topItem: Binding<String?>? = nil
    /// A row that stays OUTSIDE the scroll view, under the grabber.
    ///
    /// Hidde, 2026-08-25: "het is vrijwel onmogelijk om de lijst over de map nog
    /// te verschuiven wanneer je over de bomen in de lijst bent gaan scrollen."
    /// He is right and the arbitration below explains why: the sheet only takes
    /// a downward drag when the list is at its very top, so once you have
    /// scrolled, the only draggable thing left is a five-point capsule.
    ///
    /// Every map app answers this the same way: the sheet has a HEADER that does
    /// not scroll, and the header is a handle. Apple Maps keeps its search field
    /// there, Google Maps its place name. Ours keeps the count, which was inside
    /// the scrolling content and therefore scrolled away exactly when it was
    /// most useful as a grip.
    @ViewBuilder var header: Header
    @ViewBuilder var content: Content

    @State private var drag: CGFloat = 0
    /// Whether the list inside is scrolled to its very top. The handoff downward
    /// is only allowed from there, because taking the gesture mid-list would
    /// yank the sheet away while somebody is reading.
    @State private var atTop = true
    /// Set the moment a downward drag begins at the top, which turns scrolling
    /// off for the rest of that gesture so the two never fight.
    @State private var handingOff = false
    /// How deep the grabber and the header are, measured FROM THE SHEET'S OWN
    /// TOP. A downward drag that starts inside them belongs to the sheet
    /// whatever the list is doing, which is what makes the header a handle.
    ///
    /// The first version compared against the screen's top and therefore never
    /// fired: the sheet's top edge sits at 171 points on a raised sheet, so a
    /// drag on the header reports a startLocation.y of about 190 and 190 is not
    /// less than 74. A test that drives the real sequence caught it in one run
    /// (2026-08-25); the fix I shipped an hour earlier had not worked at all.
    private let headerDepth: CGFloat = 90

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

                header
                    .frame(maxWidth: .infinity)
                    .contentShape(.rect)

                ScrollView {
                    content
                        .frame(maxWidth: .infinity, alignment: .top)
                }
                .scrollPosition(id: topItem ?? .constant(nil), anchor: .top)
                .scrollDisabled(height == .peek || handingOff)
                // At peek the content is a PREVIEW, not a control panel. Every
                // finger that lands here belongs to the sheet, so a swipe up
                // raises it instead of half-raising it and opening whatever
                // card it started on (Hidde, 2026-08-21: "het is bijna
                // onmogelijk om de lijst omhoog te swipen zonder de boom aan
                // te klikken. Als ik omhoog swipe moet het ding omhoog komen
                // en dan pas moet ik erop kunnen klikken"). Google Maps and
                // Apple Maps both do exactly this.
                .allowsHitTesting(height != .peek)
                .onScrollGeometryChange(for: CGFloat.self) { $0.contentOffset.y } action: { _, y in
                    atTop = y <= 1
                }
            }
            .frame(height: h)
            .overlay {
                if height == .peek {
                    Color.clear
                        .contentShape(.rect)
                        .onTapGesture { withAnimation(.spring(duration: 0.28)) { height = .half } }
                }
            }
            .frame(maxWidth: .infinity)
            .background(.regularMaterial)
            .clipShape(.rect(topLeadingRadius: 16, topTrailingRadius: 16))
            .shadow(color: .black.opacity(0.12), radius: 10, y: -3)
            .frame(maxHeight: .infinity, alignment: .bottom)
            // simultaneous, not exclusive: the scroll view has to keep working
            // for every gesture this one does not want.
            //
            // And minimumDistance is 18 rather than 4, which is not a tuning
            // preference. At 4 this gesture won the tap-versus-drag arbitration
            // against the cards underneath, so tapping a tree in the list did
            // nothing at all: the finger moves a point or two on any real tap.
            // Three UI tests caught it, which is the entire reason they exist,
            // because a card that does not open is invisible in a screenshot.
            .simultaneousGesture(
                DragGesture(minimumDistance: 18)
                    .onChanged { value in
                        // Claim the gesture only in the cases the rules above
                        // describe. Everything else belongs to the list.
                        if height == .peek {
                            drag = value.translation.height
                        } else if (atTop || value.startLocation.y - (geo.size.height - h) < headerDepth)
                                    && value.translation.height > 0 {
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
