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
    init() {
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
        }
    }
}
