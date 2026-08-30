// The four "see all" pages behind Explore's shelves.
//
// A shelf shows a dozen and the database holds hundreds, so a shelf without a
// way out quietly claims that the row you can see is everything there is
// (Hidde, 2026-08-21). One screen with four modes rather than four screens,
// because the only thing that differs is what a row is.

import SwiftUI

struct IndexView: View {
    let kind: Route.Index
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    @State private var search = ""

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 10) {
                switch kind {
                case .cities: cities
                case .countries: countries
                case .species: species
                case .oldest: oldest
                }
                Color.clear.frame(height: 80)
            }
            .padding(.horizontal, 16).padding(.top, 6)
        }
        .brandGround()
        .navigationTitle(kind.title)
        .navigationBarTitleDisplayMode(.inline)
        .searchable(text: $search, prompt: "Search")
    }

    private func matches(_ s: String) -> Bool {
        search.isEmpty || s.lowercased().contains(search.lowercased())
    }

    // MARK: - the four kinds of row

    private var cities: some View {
        let all = catalogue.citiesWithTrees
            .map { (slug: $0.key, name: $0.value[0].city,
                    country: $0.value[0].country, count: $0.value.count) }
            .filter { matches($0.name) || matches($0.country) }
            .sorted { $0.count > $1.count }
        return ForEach(all, id: \.slug) { c in
            NavigationLink(value: Route.city(c.slug)) {
                row(c.name, c.country, c.count)
            }
            .buttonStyle(.plain)
        }
    }

    private var countries: some View {
        let all = catalogue.countriesWithTrees
            .map { (name: $0.key, count: $0.value.count,
                    cities: Set($0.value.map(\.citySlug)).count) }
            .filter { matches($0.name) }
            .sorted { $0.count > $1.count }
        return ForEach(all, id: \.name) { c in
            NavigationLink(value: Route.country(c.name)) {
                row(c.name, "\(c.cities) \(c.cities == 1 ? "place" : "places")", c.count)
            }
            .buttonStyle(.plain)
        }
    }

    /// Vertically, because a species is a WORD. Side by side they were a row
    /// of tiny labels you had to scroll to read (Hidde, 2026-08-21: "het
    /// voelt eigenlijk alsof je ze meer onder elkaar kunt zetten").
    private var species: some View {
        let all = catalogue.speciesWithTrees
            .map { (name: $0.key, count: $0.value.count) }
            .filter { matches($0.name) }
            .sorted { $0.count > $1.count }
        return ForEach(all, id: \.name) { sp in
            NavigationLink(value: Route.species(sp.name)) {
                HStack(spacing: 12) {
                    SpeciesMark(species: sp.name, color: Brand.moss)
                        .frame(width: 30, height: 30)
                    Text(sp.name)
                        .font(.brand(16, .bold)).foregroundStyle(Brand.ink)
                        .lineLimit(1)
                    Spacer(minLength: 8)
                    Text("\(sp.count)")
                        .font(.subheadline).foregroundStyle(Brand.inkSoft).monospacedDigit()
                    Image(systemName: "chevron.right")
                        .font(.caption).foregroundStyle(Brand.inkSoft.opacity(0.6))
                }
                .padding(.horizontal, 16).frame(minHeight: 56)
                .brandCard(12)
            }
            .buttonStyle(.plain)
        }
    }

    private var oldest: some View {
        let all = catalogue.trees
            .filter { ($0.ageMin ?? 0) > 0 && (matches($0.name) || matches($0.city)) }
            .sorted { ($0.ageMin ?? 0) > ($1.ageMin ?? 0) }
            .prefix(120)
        return ForEach(Array(all)) { t in
            NavigationLink(value: Route.tree(t.id)) {
                TreeCard(tree: t)
            }
            .buttonStyle(.plain)
            .padding(.bottom, 6)
        }
    }

    private func row(_ title: String, _ subtitle: String, _ count: Int) -> some View {
        HStack(spacing: 12) {
            VStack(alignment: .leading, spacing: 2) {
                Text(title).font(.brand(16, .bold)).foregroundStyle(Brand.ink).lineLimit(1)
                Text(subtitle).font(.caption).foregroundStyle(Brand.inkSoft).lineLimit(1)
            }
            Spacer(minLength: 8)
            Text("\(count)")
                .font(.subheadline).foregroundStyle(Brand.inkSoft).monospacedDigit()
            Image(systemName: "chevron.right")
                .font(.caption).foregroundStyle(Brand.inkSoft.opacity(0.6))
        }
        .padding(.horizontal, 16).frame(minHeight: 60)
        .brandCard(12)
    }
}
