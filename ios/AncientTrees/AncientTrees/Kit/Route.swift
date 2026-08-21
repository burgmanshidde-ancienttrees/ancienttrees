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
    case walk(city: String, name: String)      // a walk is only unique per city
    case city(String)                          // city slug
    case collection(String)                    // collection slug
    case species(String)                       // common name
    case country(String)                       // country name, as the feed spells it
    /// The "see all" behind a shelf. Netflix, AllTrails and Airbnb all put one
    /// in the shelf header, and a shelf without one is a promise that the row
    /// you can see is everything there is (Hidde, 2026-08-21).
    case index(Index)

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
