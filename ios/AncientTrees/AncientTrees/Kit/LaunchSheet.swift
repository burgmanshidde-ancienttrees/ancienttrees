// A sheet a launch argument opens (-people, -contribute, -feedback ...), raised
// once the screen is actually up rather than on its first frame.
//
// Debug scaffolding only, the same family as -tab= and -at=: the screenshot
// sweep and the UI tests cannot tap, so these arguments open the sheet for
// them. They used to do it by starting the sheet's @State at true, which asks
// UIKit to present during the very first layout, while the tab is still being
// built or the page that owns the sheet is still being pushed. UIKit drops a
// presentation made mid-transition without a word, so the sheet simply never
// came. On a quiet desk the transition is over before the request lands; on a
// busy CI runner it is not, and the iOS 18 floor went red twice on 2026-10-13
// (FlowWalk's find-people flows: no "person-follow"; SignedOutWalk: no
// sign-in sheet after -contribute). Reproduced on 2026-10-14 by loading the
// Mac's CPU: the Settings page pushed and on screen, no sheet over it.
//
// So: ask after the screen has appeared, then LOOK whether something is
// presented, and ask again if the request was dropped. A wider timeout in the
// test would not help; the sheet was never coming.

import SwiftUI
import UIKit

extension View {
    /// Raises `isPresented` when the app was launched with `argument`.
    func launchSheet(_ argument: String, isPresented: Binding<Bool>) -> some View {
        modifier(LaunchSheet(argument: argument, isPresented: isPresented))
    }
}

private struct LaunchSheet: ViewModifier {
    let argument: String
    @Binding var isPresented: Bool

    func body(content: Content) -> some View {
        content.task {
            guard ProcessInfo.processInfo.arguments.contains(argument) else { return }
            for _ in 0..<8 {
                isPresented = true
                try? await Task.sleep(for: .seconds(0.6))
                if Self.somethingIsPresented || Task.isCancelled { return }
                // Dropped: the binding still says true and nothing is up.
                // Put it back so the next true is a new request.
                isPresented = false
                try? await Task.sleep(for: .seconds(0.3))
            }
        }
    }

    /// Whether any view controller in the window presents something: the
    /// sheet, or the dialog, this argument asked for. Walked down the children
    /// because a tab's or a stack's own controller may be the presenter.
    @MainActor private static var somethingIsPresented: Bool {
        func presents(_ vc: UIViewController) -> Bool {
            vc.presentedViewController != nil || vc.children.contains(where: presents)
        }
        return UIApplication.shared.connectedScenes
            .compactMap { ($0 as? UIWindowScene)?.keyWindow?.rootViewController }
            .contains(where: presents)
    }
}
