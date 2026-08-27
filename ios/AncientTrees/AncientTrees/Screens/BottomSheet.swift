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

extension View {
    /// A tap that a DRAG CANCELS, for a control that sits in the sheet's own
    /// grab area.
    ///
    /// This is UIScrollView's behaviour, borrowed rather than invented. A
    /// scroll view sets `delaysContentTouches` and `canCancelContentTouches`,
    /// so a touch on a button is held back for a moment and, the instant it
    /// becomes a scroll, the button's press is cancelled and never fires. It is
    /// why you can start a scroll on a row in Settings, or on a cell in the App
    /// Store, without opening it. Every list in iOS has worked this way since
    /// 2007 and people are trained on it.
    ///
    /// Inside a SwiftUI ScrollView you get it for nothing. In a sheet with a
    /// drag gesture of its own you do not, and the reason is what a `Button`
    /// actually asks: did the finger lift inside my bounds. A name row is the
    /// width of the sheet, so a 40 point drag up and down never leaves those
    /// bounds and the button fires on release. That is exactly what Hidde kept
    /// hitting (2026-08-27: "als ik de slider gebruik opent het bewerken van je
    /// profiel veel te makkelijk"), and it is why removing the control was the
    /// wrong fix for it: "andere apps hebben gewoon iets slims als wanneer er
    /// gescrollt wordt is niks klikbaar".
    ///
    /// A TapGesture asks the other question, did the finger STAY STILL, and
    /// cancels itself once the touch travels past its own small slop. So the
    /// control works when you tap it and is inert while you drag, with no
    /// state to keep and nothing to get out of step.
    func tapUnlessDragged(_ action: @escaping () -> Void) -> some View {
        self.contentShape(.rect).onTapGesture(perform: action)
    }
}

/// A card inside a sheet, TAPPED rather than pressed.
///
/// Use this instead of NavigationLink for anything that lives in a sheet's
/// content. It exists because of the same difference tapUnlessDragged is
/// about, on the control people use most: below full height the list does not
/// scroll, so a swipe up on a tree card raises the sheet, and on release the
/// NavigationLink fires anyway and opens the tree, because a link asks only
/// whether the finger lifted inside its bounds and a card is two hundred
/// points tall.
///
/// Turning hit testing off mid-drag does NOT fix it, which was the first thing
/// tried and photographed failing on 2026-08-27: a press SwiftUI has already
/// begun is not cancelled by the view refusing later touches. The tap has to be
/// a TapGesture from the start, because a TapGesture is the one that asks
/// whether the finger stayed still.
///
/// Navigation goes through Navigator rather than a link, which lands in exactly
/// the same place: the root appends it to the showing tab's path.
struct SheetLink<Content: View>: View {
    let route: Route
    @Environment(Navigator.self) private var navigator
    @ViewBuilder var content: Content

    var body: some View {
        content
            .contentShape(.rect)
            .onTapGesture { navigator.push = route }
            .accessibilityAddTraits(.isButton)
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
    /// TRUE WHILE A FINGER IS MOVING THE SHEET, and the whole reason it exists
    /// is that a Button does not care.
    ///
    /// This is the same fault the header's name row had, on the control people
    /// actually use: at card and half height the list does not scroll, so a
    /// swipe up on a tree card raises the sheet, and on release the card opens
    /// the tree anyway, because the finger never left the card's bounds. Hidde
    /// asked the question that found it (2026-08-27: "heb je dit doorgevoerd
    /// overal waar dit component wordt gebruikt, dat is meer dan 1 plek"), and
    /// the answer was no: the name row was one place and every card in every
    /// sheet was the other.
    ///
    /// @GestureState rather than @State, because it resets itself when the
    /// gesture ends OR is cancelled. A plain flag left true by a gesture the
    /// system tore down would make the whole list dead until the next drag,
    /// which is a worse bug than the one being fixed.
    @GestureState private var dragging = false
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
                // THE LIST ENDS ABOVE THE FLOATING BAR, which it did not until
                // 2026-08-27 (Hidde: "de spacing van de lijst is nog steeds
                // niet goed"). The sheet reaches the bottom of the screen and
                // the tab bar floats over its last 62 points, so at every
                // height below full the last thing on the list was sliced
                // across the middle by an opaque bar. Not scrolled behind it,
                // where a finger could recover it: parked there, because the
                // list only scrolls at full height.
                //
                // Padding the SCROLL VIEW rather than its content is the
                // difference that matters. Padding the content adds empty
                // space you have to scroll to; padding the viewport moves the
                // bottom edge, so a card is cut by the edge of a list, which
                // is what a cut card is supposed to mean.
                .padding(.bottom, TabBar.floatDepth + 8)
                .scrollPosition(id: topItem ?? .constant(nil), anchor: .top)
                // THE RULE THE FILE ALREADY WRITES DOWN, now actually applied.
                // "Below full height the sheet moves, the list does not
                // scroll" was the documented arbitration and the code only
                // disabled scrolling at peek, so at card and half an upward
                // swipe scrolled a short list instead of raising the sheet.
                // That is Hidde's fourth report of this control (2026-08-26:
                // "de lijst op de map pagina kan niet soepel of helemaal niet
                // naar boven worden gescrollt"): the list would not go up
                // because the sheet would not, and the two feel like one
                // broken thing under a thumb.
                .scrollDisabled(height != .full || handingOff)
                // THE CANCEL, and it is UIScrollView's own rule: the moment a
                // touch becomes a drag, the control under it stops being
                // pressed. The drag gesture below only begins after 18 points,
                // so a real tap never reaches this and a real drag always does.
                .allowsHitTesting(height != .peek && !dragging)
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
                    .updating($dragging) { _, state, _ in state = true }
                    .onChanged { value in
                        // Claim the gesture only in the cases the rules above
                        // describe. Everything else belongs to the list.
                        if height != .full {
                            // Below full height the sheet owns the finger in
                            // BOTH directions, which is what makes a swipe up
                            // raise it the way it does in Apple Maps.
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
