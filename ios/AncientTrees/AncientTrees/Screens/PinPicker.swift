// A map you drag under a fixed pin, to say where something is.
//
// Convention: Google Maps ("Move map to adjust") and Airbnb's location step.
// Both move the MAP under a pin that never moves, and for the same reason:
// dragging a marker puts your thumb over the thing you are aiming at, while a
// fixed crosshair leaves the target visible the whole time. CONVENTIONS.md
// carries the entry.
//
// Lifted out of PlacePin on 2026-08-28 rather than copied. That screen asks
// where a tree we publish really is; the collect flow now has to ask where a
// photograph was taken when the photograph does not say. Two screens, one
// question, and a second hand-built crosshair would have drifted from this one
// within a month.

import SwiftUI
import MapKit

struct PinPicker: View {
    /// Where the map opens. For a correction that is our own pin; for a
    /// photograph with no location of its own it is wherever the person is,
    /// or the last place they looked.
    let start: CLLocationCoordinate2D
    /// Drawn for context and never selectable: knowing which trees we already
    /// map is most of what tells somebody they are in the right place.
    var trees: [Tree] = []
    /// The street, not the district. Somebody is telling us which trunk, and
    /// at four kilometres a trunk is a dot.
    var spanMeters: Double = 300
    @Binding var coordinate: CLLocationCoordinate2D

    @State private var region: MKCoordinateRegion?

    var body: some View {
        ZStack {
            TreeMap(trees: trees,
                    focus: start,
                    spanMeters: spanMeters,
                    clusters: false,
                    region: $region,
                    selected: .constant(nil))
                .ignoresSafeArea(edges: .bottom)
            crosshair
        }
        .onChange(of: region?.center.latitude) { _, _ in read() }
        .onChange(of: region?.center.longitude) { _, _ in read() }
    }

    private func read() {
        guard let c = region?.center else { return }
        coordinate = c
    }

    /// Dead centre, hanging from its point like a map pin rather than sitting
    /// on it, so the tip marks the spot and not the middle of a circle.
    private var crosshair: some View {
        VStack(spacing: 0) {
            Image(systemName: "mappin")
                .font(.system(size: 34, weight: .semibold))
                .foregroundStyle(Brand.moss)
                .shadow(color: .black.opacity(0.25), radius: 3, y: 1)
            Circle()
                .fill(Brand.moss)
                .frame(width: 6, height: 6)
                .shadow(color: .black.opacity(0.3), radius: 2)
        }
        .offset(y: -20)
        .allowsHitTesting(false)
        .accessibilityHidden(true)
    }
}
