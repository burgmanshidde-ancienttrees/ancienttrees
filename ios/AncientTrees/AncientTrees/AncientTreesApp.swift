//
//  AncientTreesApp.swift
//  AncientTrees
//
//  Created by Hidde on 19/08/2026.
//

import SwiftUI
import UIKit

@main
struct AncientTreesApp: App {
    /// Registering the brand font and styling the navigation bar used to happen
    /// in init(), which runs before any view exists. Anything that hangs there
    /// gives a white screen with nothing to read: no view, no console output, no
    /// crash report. It runs on the first view's appearance now, so the worst
    /// case is an unstyled first frame rather than a blank app.
    @MainActor static func configureAppearance() {
// The brand face has to exist before the first view asks for it.
        BrandFont.register()

        // A large navigation title is drawn by UIKit, so SwiftUI cannot set its
        // font. The appearance proxy can, and doing it once here is what stops
        // every screen's own name from being the system face while everything
        // under it is not.
        let bar = UINavigationBarAppearance()
        bar.configureWithTransparentBackground()
        let ink = UIColor { $0.userInterfaceStyle == .dark
            ? UIColor(hex: 0xECEFE4) : UIColor(hex: 0x26301E) }
        if let large = UIFont(name: "Gabarito-Black", size: 34) {
            bar.largeTitleTextAttributes = [.font: large, .foregroundColor: ink]
        }
        if let inline = UIFont(name: "Gabarito-Bold", size: 17) {
            bar.titleTextAttributes = [.font: inline, .foregroundColor: ink]
        }
        UINavigationBar.appearance().standardAppearance = bar
        UINavigationBar.appearance().scrollEdgeAppearance = bar
        UINavigationBar.appearance().compactAppearance = bar
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
                // The whole app presses in moss, not in system blue. Without
                // this, iOS tints the selected tab, the map's locate button and
                // every text field's caret and placeholder link with its own
                // accent, so four screens out of fourteen had a blue element on
                // them and the app read as half-finished. Found by the first
                // screenshot sweep on 2026-08-20, on the first screenshot.
                .tint(Brand.moss)
                .task { AncientTreesApp.configureAppearance() }
        }
    }
}
