// A bottom sheet that does not cover the tab bar.
//
// SwiftUI's .sheet is presented over everything, tab bar included, which is
// exactly wrong here: Google Maps keeps its tab bar visible under the sheet and
// you can switch tabs without dismissing anything. So this is an overlay in the
// view rather than a presentation, with the same three heights and the same drag.

import SwiftUI

enum SheetHeight: CaseIterable {
    case peek, half, full

    func points(in total: CGFloat) -> CGFloat {
        switch self {
        case .peek: 160
        case .half: total * 0.52
        case .full: total * 0.92
        }
    }
}

struct BottomSheet<Content: View>: View {
    @Binding var height: SheetHeight
    @ViewBuilder var content: Content

    @State private var drag: CGFloat = 0

    var body: some View {
        GeometryReader { geo in
            let target = height.points(in: geo.size.height)
            let h = min(max(target - drag, 90), geo.size.height * 0.94)
            VStack(spacing: 0) {
                Capsule()
                    .fill(.tertiary)
                    .frame(width: 40, height: 5)
                    .padding(.top, 8).padding(.bottom, 6)
                content
                    .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)
            }
            .frame(height: h)
            .frame(maxWidth: .infinity)
            .background(.regularMaterial)
            .clipShape(.rect(topLeadingRadius: 16, topTrailingRadius: 16))
            .shadow(color: .black.opacity(0.12), radius: 10, y: -3)
            .frame(maxHeight: .infinity, alignment: .bottom)
            .gesture(
                DragGesture()
                    .onChanged { drag = $0.translation.height }
                    .onEnded { value in
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
