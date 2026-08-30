// Getting from one tab to another, which nothing could do until now.
//
// Hidde, 2026-08-20, on the map card that had just been put on the tree page:
// "het slaat natuurlijk nergens op om die kaart klein op de boom te zetten als
// de kaart ook boven te vinden is op de map tab - dat moet je doen op paginas
// waar de kaart niet is zodat je erheen navigeert."
//
// He is right, and the second half of that sentence is the sharper part. A small
// map on a page is not a second map, it is a WAY TO THE MAP. What was built was
// a 220 point interactive map you cannot really pan, sitting three inches from a
// tab that opens the real one, which is duplication rather than navigation.
//
// So the tree page keeps a picture of where the tree is, and the whole picture
// is a button that opens the Map tab with that tree already selected. That needs
// one tab to be able to talk to another, which this is: a single request, set by
// whoever wants to go somewhere and cleared by whoever answers it.

import Foundation
import Observation

/// Main-actor isolated, like every store the root holds. See Account.swift for
/// why: SwiftUI already reads these from the main actor, so the annotation
/// costs nothing at runtime and makes a background write a compiler error
/// instead of a data race nobody can reproduce.
@MainActor
@Observable
public final class Navigator {
    /// A tree id somebody wants to see on the map. ContentView switches tabs on
    /// it, MapTab selects it and clears it.
    public var showOnMap: String?

    /// A walk somebody wants to WALK, by city slug and name. The root turns it
    /// into the full-screen Begin mode and clears it, the same shape as
    /// showOnMap, so a walk card anywhere can start one without every screen
    /// owning a copy of that screen.
    public struct WalkRef: Equatable { public let city: String; public let name: String
        public init(city: String, name: String) { self.city = city; self.name = name } }
    public var beginWalk: WalkRef?

    /// A tab somebody wants to be on. Set by whoever offers the shortcut,
    /// cleared by the root, same shape as showOnMap.
    public var selectTab: Int?

    /// Somewhere to PUSH on whichever tab is showing. Set by anything that
    /// finds a destination (search, a shortcut), cleared by the root.
    public var push: Route?

    /// A CITY somebody wants to see on the map, by slug. The same shape as
    /// showOnMap and for the same reason: a city page's map preview is a way to
    /// the map rather than a second map, and until 2026-08-25 it was neither,
    /// because it carried allowsHitTesting(false) and nothing else (Hidde:
    /// "dan kan ik niet op de kaart klikken... als je zoekt in de map op
    /// Barcelona, je op de Barcelona-pagina in de map komt").
    ///
    /// A slug rather than a tree id, so the map frames the whole city instead
    /// of selecting one arbitrary trunk in it.
    public var showCityOnMap: String?

    /// Collect's own button asking for the nearby-trees sheet. The root owns
    /// every sheet, so the request travels rather than the presentation.
    public var collectNearby = false


    public init() {}
}
