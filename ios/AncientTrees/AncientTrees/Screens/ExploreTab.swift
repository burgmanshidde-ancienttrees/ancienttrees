// One tab, two modes, one pill between them.
//
// The teardown's own words on AllTrails' floating Kaart pill: "One control,
// always in the same place, and it means the user never has to decide which of
// two pages to be on. We currently ship the map and the list as separate
// destinations." This is that lesson applied to ourselves: Home's shelves and
// the map stop being two tabs and become the two faces of Explore.

import SwiftUI

struct ExploreTab: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    let located: Bool
    let locationDenied: Bool
    let onUseMyLocation: () -> Void
    @Environment(Navigator.self) private var navigator

    var body: some View {
        ZStack(alignment: .bottom) {
            if navigator.exploreShowsMap {
                MapTab(catalogue: catalogue, origin: origin,
                       located: located,
                       locationDenied: locationDenied,
                       onUseMyLocation: onUseMyLocation)
                    .accessibilityIdentifier("explore-map")
            } else {
                HomeView(catalogue: catalogue, origin: origin)
            }
            pill
        }
    }

    /// AllTrails' control, in our ink: dark capsule, an icon and one word,
    /// floating above the bar on both of the tab's faces.
    private var pill: some View {
        Button {
            withAnimation(.snappy) { navigator.exploreShowsMap.toggle() }
        } label: {
            Label(navigator.exploreShowsMap ? "List" : "Map",
                  systemImage: navigator.exploreShowsMap ? "list.bullet" : "map.fill")
                .font(.brand(15, .bold))
                .padding(.horizontal, 18)
                // 44 tall: Apple's floor for a tap target, measured by appfit
                // rather than eyeballed (it shipped at 40 first).
                .frame(minHeight: 44)
                .background(Capsule().fill(Brand.ink))
                .foregroundStyle(Brand.ground)
        }
        .padding(.bottom, 8)
        .accessibilityIdentifier("explore-pill")
    }
}
