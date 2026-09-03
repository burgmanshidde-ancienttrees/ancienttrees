// Do we actually know where this person is, and what the app says when it does
// not.
//
// Convention: Apple Maps, driven with location revoked on 2026-08-30. It does
// not centre on a guess and it does not print a distance it cannot compute. It
// zooms out, puts a permanent pill on the map, and its own sheet drops the
// proximity content entirely: Places, Home, Work, Your Guides, none of which
// claims to be near anything. CONVENTIONS.md carries the walk-through.
//
// Hidde, 2026-08-30, shown that Discover, My trees and Collect all sorted by a
// coordinate we did not have: "ja doe apple na."
//
// WHY AN ENVIRONMENT VALUE. `origin` is a plain tuple threaded through fifteen
// call sites and it always has a value, because it falls back to the last fix
// this phone had and then to Dam square. That fallback is right for the MAP,
// which has to open somewhere, and it is a lie everywhere a number gets
// printed: "your first tree is 350 m away" measured from a square in a city
// this person may never have visited. Passing a second parameter alongside
// origin to every one of those call sites is how half of them end up not
// getting it. One environment value cannot drift.
//
// It defaults to TRUE, so a preview, a test and any screen nobody has thought
// about behave exactly as they did. Only ContentView sets it, from the one
// place that knows.

import SwiftUI

/// Everything a screen needs to know about where it stands, in one value.
///
/// One key rather than three, because three keys is three chances to set two of
/// them. The ask travels with it because the chip needs the app's own single
/// CLLocationManager: a view that makes its own gets a second manager whose
/// authorisation callback nobody is listening to.
struct LocationState {
    /// False when `origin` is a fallback rather than a fix. Anything that prints
    /// a distance, a walk time or the word "near" has to read this first.
    var known: Bool = true
    /// Asked and refused, as opposed to not asked yet. The two need different
    /// buttons: a refusal can only be undone in Settings, while an unasked
    /// permission can still be asked right here.
    var denied: Bool = false
    var ask: () -> Void = {}
}

private struct LocationStateKey: EnvironmentKey {
    static let defaultValue = LocationState()
}

extension EnvironmentValues {
    var locationState: LocationState {
        get { self[LocationStateKey.self] }
        set { self[LocationStateKey.self] = newValue }
    }
}

/// The pill, the same one the map has worn since before this was written.
///
/// Apple's is permanent furniture rather than a dismissible banner, in the app's
/// accent colour, and it opens the recovery sheet rather than Settings. This is
/// that, made shared so the other screens carry the identical thing instead of
/// three cousins of it.
struct LocationOffChip: View {
    @Environment(\.locationState) private var location
    @State private var refused: Permission?

    var body: some View {
        Button {
            if location.denied { refused = .location } else { location.ask() }
        } label: {
            HStack(spacing: 6) {
                Image(systemName: "location.slash")
                Text("Location off")
                Text("·").foregroundStyle(.secondary)
                Text(location.denied ? "Turn on location" : "Use my location")
                    .foregroundStyle(Brand.moss)
            }
            .font(.subheadline.weight(.semibold))
            .padding(.horizontal, 14).padding(.vertical, 8)
            .background(.regularMaterial, in: .capsule)
        }
        .buttonStyle(.plain)
        .accessibilityIdentifier("location-off-chip")
        .sheet(item: $refused) { PermissionRecovery(permission: $0) }
    }
}
