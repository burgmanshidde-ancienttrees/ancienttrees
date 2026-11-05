// The place's white box: who looks after it, and the Plus question.
//
// DIRECTION C (Hidde, 2026-11-05, "1b, link"): under the place's name one slim
// white box, the way Google Maps and komoot keep a place's people and asks in
// one block. Its first row is the ambassador: the named person, with a green
// "Become one too" at the end of their line, or, with nobody named, "Become the
// <place> ambassador". Its second row is "Help create Ancient Trees Plus". No
// affiliation in the line (Hidde: "leaving out quercus lisboa is good"). The
// website draws the same box (AmbassadorLine.astro, PlusAsk.astro).
//
// Spacing copied from the sheet's other boxes: radius 14, a hairline border,
// rows 46 tall (58 with an avatar), 14 inside the edges.

import SwiftUI

struct PlaceAsksBox: View {
    let slug: String
    let title: String
    let catalogue: Catalogue

    var body: some View {
        VStack(spacing: 0) {
            PlaceAmbassadors(slug: slug, title: title, catalogue: catalogue)
            Rectangle().fill(Brand.hairline).frame(height: 1)
            PlusRow(city: title)
        }
        .background(Brand.surface, in: .rect(cornerRadius: 14))
        .overlay {
            RoundedRectangle(cornerRadius: 14, style: .continuous)
                .strokeBorder(Brand.hairline, lineWidth: 1)
        }
        .accessibilityElement(children: .contain)
        .accessibilityIdentifier("place-asks")
    }
}

/// The ambassador row(s) of the box. One view for every place, so the map's
/// place header can never draw it two ways.
struct PlaceAmbassadors: View {
    let slug: String
    let title: String
    let catalogue: Catalogue
    @Environment(Navigator.self) private var navigator

    var body: some View {
        let named = catalogue.facets.ambassadors(city: slug)
        if named.isEmpty {
            AmbassadorWantedRow(place: title, seated: catalogue.facets.seated(city: slug), look: .slim)
        } else {
            VStack(spacing: 0) {
                ForEach(Array(named.enumerated()), id: \.offset) { i, a in
                    if i > 0 { Rectangle().fill(Brand.hairline).frame(height: 1) }
                    personRow(a.name, profile: a.profile, last: i == named.count - 1)
                }
            }
        }
    }

    /// The person: initial with the badge, the name, and under it "<place>
    /// ambassador · Become one too". The row opens their profile while it is
    /// public (2026-10-19); the green words open the ask, their own tap.
    @ViewBuilder private func personRow(_ name: String, profile: String?, last: Bool) -> some View {
        let row = HStack(spacing: 12) {
            Text(String(name.trimmingCharacters(in: .whitespaces).prefix(1)).uppercased())
                .font(.system(size: 13, weight: .bold))
                .foregroundStyle(Brand.moss)
                .frame(width: 30, height: 30)
                .background(Brand.mossTint, in: .circle)
                .overlay(alignment: .bottomTrailing) {
                    Image(systemName: "checkmark.seal.fill")
                        .font(.system(size: 11, weight: .semibold))
                        .foregroundStyle(Brand.moss)
                        .background(Brand.surface, in: .circle)
                        .offset(x: 3, y: 3)
                }
                .accessibilityHidden(true)
            VStack(alignment: .leading, spacing: 0) {
                Text(name)
                    .font(.system(size: 15, weight: .semibold))
                    .foregroundStyle(Brand.ink)
                HStack(spacing: 0) {
                    Text(last ? "\(title) ambassador · " : "\(title) ambassador")
                        .font(.system(size: 12))
                        .foregroundStyle(Brand.inkSoft)
                    if last {
                        AmbassadorWantedRow(place: title, seated: true, look: .link)
                    }
                }
            }
            Spacer(minLength: 8)
            if profile != nil {
                Image(systemName: "chevron.right")
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(Brand.inkSoft.opacity(0.6))
            }
        }
        .padding(.horizontal, 14)
        .frame(minHeight: 58)

        if let id = profile {
            // A tap, not a Button: the box rides the sheet (sheetTap). The
            // "Become one too" inside keeps its own tap, which wins.
            row.contentShape(.rect)
                .modifier(SheetStillTap(enabled: true) { navigator.push = .person(id) })
                .accessibilityAction(named: Text("Open \(name)'s profile")) { navigator.push = .person(id) }
                .accessibilityIdentifier("ambassador-profile")
        } else {
            row.accessibilityIdentifier("ambassador-row")
        }
    }
}
