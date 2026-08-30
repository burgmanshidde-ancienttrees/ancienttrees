// The way back, after somebody has already said no.
//
// Convention: Apple Maps, driven with location revoked rather than read about,
// and AllTrails' own dialog from Hidde's phone. CONVENTIONS.md carries the
// entry, the screenshots and the sources. The shape, in four parts:
//
// 1. The title says what the app CANNOT DO WELL and names the feature. Never
//    "you denied permission" and never the name of the permission itself.
//    Apple: "Maps works best with Location Services turned on." AllTrails:
//    "tijdens het navigeren".
// 2. The body lists what they are missing, in features rather than plumbing.
// 3. Two buttons, and the second one is a real choice with a name. Apple's is
//    "Keep Location Services Off" rather than "Cancel", so declining twice is
//    a decision somebody makes instead of a dialog they escape.
// 4. THE PATH, in one line under the buttons, which is the half neither
//    reference does and the half Hidde asked for.
//
// Why the path line exists at all, since openSettingsURLString is supposed to
// land on our own page in Settings: measured on 2026-08-30 it did not. Somebody
// tapping "Don't Allow" and then our chip landed on the ROOT of Settings, and
// the toggle lives four steps away at Settings > Apps > Ancient Trees >
// Location, under an "Apps" row most of a screen down. A real App Store install
// may well behave better, and we cannot tell which phone will do which, so the
// line costs one row of small type and removes the whole question.
//
// It is deliberately ONE LINE and not a numbered tutorial with pictures. Apple
// moves these screens (apps moved under "Apps" in iOS 26), and an illustrated
// walkthrough is wrong the day that happens while a single line still reads as
// roughly where to look.

import SwiftUI
import UIKit

/// Which permission, and everything the sheet says about it.
///
/// One type rather than three sheets, because the difference between them is
/// four strings and the shape is the part that must not drift.
enum Permission: String, Identifiable {
    case location
    case camera
    case photos

    var id: String { rawValue }

    /// What the app cannot do well. Never the name of the permission.
    var title: String {
        switch self {
        case .location: return "Ancient Trees works best with your location turned on"
        case .camera:   return "Ancient Trees needs the camera to photograph a tree"
        case .photos:   return "Ancient Trees needs your photos to place a tree on the map"
        }
    }

    /// The features, not the plumbing.
    var body: String {
        switch self {
        case .location:
            return "You will see the old trees nearest you, the walk time to each, and the map will open where you are standing."
        case .camera:
            return "You can photograph the tree in front of you and add it to your collection. You can still pick a photograph you already took."
        case .photos:
            return "We can read where and when a photograph was taken, so the tree lands in the right place. You can still place the pin yourself."
        }
    }

    /// Named, so declining is a decision rather than an escape.
    ///
    /// The camera's is not a decline at all, it is the way on. Hidde,
    /// 2026-08-30: the camera button must raise this message rather than
    /// silently opening the gallery, and once it does, the gallery is the
    /// obvious second button. Apple's rule that the second button is a real
    /// named choice is better served by naming the route than by naming the
    /// refusal.
    var decline: String {
        switch self {
        case .location: return "Keep location off"
        case .camera:   return "Choose a photo instead"
        case .photos:   return "Keep photos off"
        }
    }

    /// The row to look for once Settings opens.
    var path: String {
        switch self {
        case .location: return "Settings › Apps › Ancient Trees › Location"
        case .camera:   return "Settings › Apps › Ancient Trees › Camera"
        case .photos:   return "Settings › Apps › Ancient Trees › Photos"
        }
    }

    var identifier: String {
        switch self {
        case .location: return "permission-recovery-location"
        case .camera:   return "permission-recovery-camera"
        case .photos:   return "permission-recovery-photos"
        }
    }
}

struct PermissionRecovery: View {
    let permission: Permission
    /// Run when the second button is tapped, for the case where that button is
    /// a route on rather than a refusal. Nil means it only dismisses.
    var onDecline: (() -> Void)? = nil
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Text(permission.title)
                .font(.brand(24, .heavy))
                .foregroundStyle(Brand.ink)
                .fixedSize(horizontal: false, vertical: true)
                .padding(.bottom, 10)

            Text(permission.body)
                .font(.subheadline)
                .foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
                .padding(.bottom, 24)

            Button {
                if let u = URL(string: UIApplication.openSettingsURLString) {
                    UIApplication.shared.open(u)
                }
                dismiss()
            } label: {
                Text("Open Settings")
                    .font(.headline)
                    .frame(maxWidth: .infinity, minHeight: 50)
                    .background(Brand.canopy, in: .capsule)
                    .foregroundStyle(.white)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("permission-open-settings")

            // The path, under the button that needs it. Small, secondary, and
            // present whether or not Settings happens to land on our page.
            Text(permission.path)
                .font(.caption)
                .foregroundStyle(Brand.inkSoft)
                .frame(maxWidth: .infinity)
                .padding(.top, 8)
                .accessibilityIdentifier("permission-path")

            Button { dismiss(); onDecline?() } label: {
                Text(permission.decline)
                    .font(.subheadline.weight(.semibold))
                    .frame(maxWidth: .infinity, minHeight: 44)
                    .foregroundStyle(Brand.inkSoft)
            }
            .buttonStyle(.plain)
            .padding(.top, 6)
            .accessibilityIdentifier("permission-decline")
        }
        .padding(.horizontal, 24)
        .padding(.top, 28)
        .padding(.bottom, 12)
        // maxHeight as well as maxWidth. Without it the ground is only as tall
        // as the words, and the detent's remaining height showed as a pale band
        // under the last button: one sheet wearing two backgrounds.
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)
        .brandGround()
        .accessibilityIdentifier(permission.identifier)
        .presentationDetents([.height(340)])
        .presentationDragIndicator(.visible)
    }
}
