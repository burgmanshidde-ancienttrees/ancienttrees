// The ambassador row on a place: who looks after it, and the open seat.
//
// It lived in PlaceMapPage.swift until that page was set aside on 2026-11-04
// (every city and country is the Map tab now); the map's place header is the
// one that draws it.

import SwiftUI

/// Who looks after a city, komoot's person row, above its trees: the named
/// ambassador (their profile opens when it is public) and the empty seat at the
/// end of the row, or the open seat alone. One view for the city page and the
/// map's place header (2026-11-04), so the two can never draw it differently.
struct PlaceAmbassadors: View {
    let slug: String
    let title: String
    let catalogue: Catalogue
    @Environment(Navigator.self) private var navigator

    var body: some View {
        let named = catalogue.facets.ambassadors(city: slug)
        // ONE ROW (Hidde, 2026-11-03): the empty seat sits at the end of the
        // named person's row, the circle alone. As AmbassadorLine.astro.
        HStack(spacing: 8) {
            VStack(alignment: .leading, spacing: 0) {
                ForEach(named, id: \.self) { a in
                    // The row opens the person's profile while it is public,
                    // with a chevron; otherwise it stays a byline (2026-10-19).
                    if let id = a.profile {
                        // A tap, not a Button: the sheet header is a handle
                        // (BottomSheet sheetTap, 2026-11-05).
                        HStack {
                            AmbassadorRow(name: a.name, place: title, affiliation: a.affiliation)
                            Spacer(minLength: 8)
                            Image(systemName: "chevron.right")
                                .font(.caption.weight(.semibold)).foregroundStyle(Brand.inkSoft)
                        }
                        .frame(minHeight: 44)
                        .sheetTap { navigator.push = .person(id) }
                        .accessibilityIdentifier("ambassador-profile")
                    } else {
                        AmbassadorRow(name: a.name, place: title, affiliation: a.affiliation)
                    }
                }
            }
            // The names fill the row, so the empty seat stands at its right end
            // whether or not the person has a profile (Hidde, 2026-11-04, Lisbon).
            .frame(maxWidth: .infinity, alignment: .leading)
            if !named.isEmpty {
                AmbassadorWantedRow(place: title, seated: true, iconOnly: true)
            }
        }
        // The open seat alone where nobody is named; a place somebody already
        // looks after keeps the row, asking for "an" ambassador (2026-10-27).
        if named.isEmpty {
            AmbassadorWantedRow(place: title, seated: catalogue.facets.seated(city: slug))
        }
    }
}
