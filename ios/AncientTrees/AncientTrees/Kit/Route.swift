// Where a tap goes, as a value rather than as a closure.
//
// Every NavigationLink in this app used to carry its own destination view
// inline, which works and costs nothing until you want to do something to the
// navigation itself. Then it costs everything, because a stack built that way
// has no path to read or clear: SwiftUI knows a view was pushed and the app
// does not know what.
//
// The thing we wanted was the ordinary one: tapping the tab you are already on
// takes you back to the top of it, which is what every iOS app with tabs has
// done since tabs existed. That needs a NavigationPath, which needs routes to
// be values, which is this file.
//
// The ids rather than the objects, deliberately. A Route survives the catalogue
// being replaced under it, which now happens: CatalogueStore learned to download
// a newer one on 2026-08-20, and a pushed screen holding a stale struct would
// keep showing yesterday's story. Looking the tree up by id at render time means
// a refresh reaches every screen that is already open.

import Foundation

public enum Route: Hashable {
    case tree(String)                          // tree id
    /// One of YOURS, which has no tree id because it is in nobody's catalogue.
    case mine(UUID)
    /// Somebody's shared sighting, opened from its unlisted link
    /// (ancienttrees.app/t?id=) rather than from your own collection. When
    /// the uuid IS yours, `destination(_:_:)` shows the same editable page
    /// `.mine` does; this case exists for everybody else, and for you on a
    /// device that has not seen this sighting yet. See SharedTreeView.swift.
    case shared(UUID)
    case walk(city: String, name: String)      // a walk is only unique per city
    case city(String)                          // city slug
    case collection(String)                    // collection slug
    case species(String)                       // common name
    case country(String)                       // country name, as the feed spells it
    /// THE MAP OF ONE TREE, pushed on whatever stack you are already on
    /// (Hidde, 2026-08-26: "ideaal expand je alleen de map van de locatie waar
    /// die boom staat, in een eigen subpagina met een backbutton terug naar de
    /// detailpagina ... dat je gewoon niet verdwijnt uit die detailpagina").
    ///
    /// Expanding used to hand you to the Map tab, which is a different place
    /// with a different history, so the way back to what you were reading was
    /// gone. A pushed page keeps the trail.
    case treeMap(String)                       // tree id
    /// YOUR OWN COLLECTION ON A REAL MAP, pushed from the cover on My trees
    /// (Hidde, 2026-08-26: "je moet nog wel de kaart kunnen scrollen enzo").
    ///
    /// The cover cannot itself be draggable: a map you can pan inside a scroll
    /// view is the gesture fight that page just lost the sheet over. Every
    /// reference answers this the same way, a still preview that opens a map
    /// you can move: Airbnb's listing, Google Maps' place card, Strava's
    /// activity. Back returns to your page.
    case collectionMap
    /// A PLACE ON A REAL MAP, pushed from the preview on a city or a country
    /// page, and never a jump to the Map tab (Hidde, 2026-08-27: "je wilt dat
    /// mensen in discovery blijven ... je gaat alleen naar de kaartkant als
    /// mensen dat in de menubar doen, nooit via dat").
    ///
    /// Handing somebody to the Map tab throws away the trail they arrived on:
    /// a different stack, a different history, and no way back to the city they
    /// were reading. Pushed, the back button is exactly where they expect it,
    /// and the page they were on is still there. The website already works
    /// this way.
    case placeMap(Place)
    /// Which place a placeMap is about. A city by its slug, a country by the
    /// name the feed spells it with, so both can be looked up the same way the
    /// pages themselves do.
    public enum Place: Hashable, Codable, Sendable {
        case city(String)
        case country(String)
    }
    /// The "see all" behind a shelf. Netflix, AllTrails and Airbnb all put one
    /// in the shelf header, and a shelf without one is a promise that the row
    /// you can see is everything there is (Hidde, 2026-08-21).
    case index(Index)
    /// Not a tab any more (Hidde, 2026-08-22): the avatar top right of
    /// Collect, which is where Komoot keeps it.
    case profile

    public enum Index: String, Hashable {
        case cities, countries, species, oldest
        public var title: String {
            switch self {
            case .cities: "Tree cities"
            case .countries: "Tree countries"
            case .species: "Species"
            case .oldest: "The oldest trees we map"
            }
        }
    }
}
