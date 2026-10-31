// The name block of a species row in the two species lists (the map's filter
// and the chooser for naming your own tree).
//
// Reference: iNaturalist's taxon row, the common name on top and the Latin in
// italics beneath, and its autocomplete's `matched_term`: when somebody typed
// "zomereik", the row says Zomereik, so the answer "Pedunculate Oak" makes
// sense (CONVENTIONS.md, "Searching a species by any of its names"). Map
// search already printed the Latin under each species (MapSearch.speciesSub);
// these two lists printed the common name alone.
import SwiftUI

struct SpeciesRowName: View {
    let catalogue: Catalogue
    let name: String
    var hit: SpeciesHit = .name
    /// For a row that is not one of our species: its Latin as given.
    var latin: String? = nil

    var body: some View {
        let sci = latin ?? catalogue.scientificName(of: name)
        VStack(alignment: .leading, spacing: 2) {
            Text(name).foregroundStyle(Brand.ink)
            if hit.via != nil || sci != nil {
                sub(via: hit.via, sci: sci)
                    .font(.footnote)
                    .foregroundStyle(Brand.inkSoft)
                    .lineLimit(1)
            }
        }
    }

    private func sub(via: String?, sci: String?) -> Text {
        switch (via, sci) {
        case let (v?, s?): Text(v) + Text(" · ") + scientificNameText(s)
        case let (v?, nil): Text(v)
        case let (nil, s?): scientificNameText(s)
        default: Text("")
        }
    }
}
