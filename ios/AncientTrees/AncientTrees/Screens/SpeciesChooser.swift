// Naming the species of a tree you added yourself.
//
// Convention: iNaturalist, whose identify screen is a searchable list of taxa
// with a suggestion block above it, and where the tick is always yours to give.
// PictureThis is the same shape with a stronger claim on top. We have the list
// and not yet the claim, so this ships as the list, ordered by what actually
// grows around you, with room kept for a suggestion when we can make one
// honestly.
//
// It replaces a free text field. Species had been an ordinary editable string
// like the name and the age, and a typed string cannot group: hard rule 9 says
// one canonical common name per species, and "beuk", "Beech" and "European
// Beech" are three species to every screen that counts them.
//
// A tree we do not map yet is still typeable, because 400 names is not the
// world and a person standing in front of a hornbeam should not be told no.
import SwiftUI

struct SpeciesChooser: View {
    let catalogue: Catalogue
    /// Common names of the trees on the map around this one, so the list opens
    /// on what grows here rather than on what we happen to map most worldwide.
    let nearby: [String]
    /// What the tree says today, so the current answer carries a tick.
    let current: String
    let onPick: (String) -> Void

    @Environment(\.dismiss) private var dismiss
    @State private var query = ""
    /// Counted once, when the sheet opens. The same freeze SpeciesPicker hit
    /// on 2026-08-24: 1,900 trees times 400 rows on every keystroke.
    @State private var index: [(name: String, count: Int)] = []

    private func build() {
        guard index.isEmpty else { return }
        var counts: [String: Int] = [:]
        for t in catalogue.trees where !t.commonName.isEmpty {
            counts[t.commonName, default: 0] += 1
        }
        let near = Set(nearby)
        index = counts.map { (name: $0.key, count: $0.value) }
            .sorted {
                if near.contains($0.name) != near.contains($1.name) {
                    return near.contains($0.name)
                }
                return $0.count == $1.count ? $0.name < $1.name : $0.count > $1.count
            }
    }

    private var typed: String { query.trimmingCharacters(in: .whitespaces) }

    private var rows: [(name: String, count: Int, hit: SpeciesHit)] {
        guard !typed.isEmpty else { return index.map { ($0.name, $0.count, .name) } }
        // Every name it goes by answers. It matters most here: a reader who
        // knows their tree as Taxus baccata (2026-10-03) or as a zomereik
        // (2026-10-31, Hidde: "I often dont know the english name") and finds
        // no row would type a second name for a species we already carry,
        // which is the exact split this chooser exists to prevent.
        let counts = Dictionary(index.map { ($0.name, $0.count) }, uniquingKeysWith: { a, _ in a })
        return catalogue.filterSpecies(index.map(\.name), query: typed)
            .map { ($0.name, counts[$0.name] ?? 0, $0.hit) }
    }

    /// Kinds of tree we know by name and do not map yet: species met in our
    /// leads and genera. A reader at a hornbeam gets Hornbeam, not a name of
    /// their own; one who only knows "eik" gets Oak (Quercus sp.), which is
    /// the publish-and-ask answer the site gives itself.
    private var notMapped: [(row: SpeciesNameRow, hit: SpeciesHit)] {
        catalogue.unmappedSpecies(matching: typed)
    }

    /// Offered while no row carries exactly what they typed, and at the foot
    /// of the list, under every row that matched: the tag field that also
    /// accepts new tags. Above a matching row it invited a second spelling of
    /// a name we already have, which is the whole reason this screen exists.
    private var mayTypeOwn: Bool {
        let t = SpeciesSearch.fold(typed)
        return typed.count >= 3
            && !rows.contains { SpeciesSearch.fold($0.name) == t }
            && !notMapped.contains { SpeciesSearch.fold($0.row.c) == t }
    }

    var body: some View {
        NavigationStack {
            List {
                Section {
                    ForEach(rows, id: \.name) { row in
                        Button {
                            onPick(row.name)
                            dismiss()
                        } label: {
                            HStack(spacing: 12) {
                                SpeciesMark(species: row.name, color: Brand.moss)
                                    .frame(width: 26, height: 26)
                                SpeciesRowName(catalogue: catalogue, name: row.name, hit: row.hit)
                                Spacer(minLength: 8)
                                if row.name.lowercased() == current.lowercased() {
                                    Image(systemName: "checkmark")
                                        .foregroundStyle(Brand.moss)
                                } else {
                                    Text("\(row.count)")
                                        .font(.subheadline).monospacedDigit()
                                        .foregroundStyle(Brand.inkSoft)
                                }
                            }
                            // The whole row, per Hidde 2026-08-25 on the filter
                            // picker: an HStack of glyphs inside a Button hands
                            // the button the bounds of the glyphs, so every gap
                            // between them is dead.
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .contentShape(.rect)
                            .frame(minHeight: 44)
                        }
                        .buttonStyle(.plain)
                    }
                } header: {
                    if typed.isEmpty, !nearby.isEmpty {
                        Text("Growing near you first")
                    }
                }

                if !notMapped.isEmpty {
                    Section {
                        ForEach(notMapped, id: \.row) { item in
                            Button {
                                onPick(item.row.species)
                                dismiss()
                            } label: {
                                HStack(spacing: 12) {
                                    SpeciesMark(species: item.row.c, color: Brand.moss)
                                        .frame(width: 26, height: 26)
                                    SpeciesRowName(catalogue: catalogue, name: item.row.c, hit: item.hit,
                                                   latin: item.row.isGenus ? item.row.l + " sp." : item.row.l)
                                    Spacer(minLength: 8)
                                    if SpeciesSearch.fold(item.row.species) == SpeciesSearch.fold(current)
                                        || SpeciesSearch.fold(item.row.c) == SpeciesSearch.fold(current) {
                                        Image(systemName: "checkmark")
                                            .foregroundStyle(Brand.moss)
                                    }
                                }
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .contentShape(.rect)
                                .frame(minHeight: 44)
                            }
                            .buttonStyle(.plain)
                        }
                    } header: {
                        Text("Not on the map yet")
                    }
                }

                if mayTypeOwn {
                    Section {
                        Button {
                            onPick(typed)
                            dismiss()
                        } label: {
                            HStack(spacing: 12) {
                                Image(systemName: "plus.circle")
                                    .foregroundStyle(Brand.moss)
                                    .frame(width: 26, height: 26)
                                Text("Use \u{201C}\(typed)\u{201D}")
                                    .foregroundStyle(Brand.ink)
                            }
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .contentShape(.rect)
                            .frame(minHeight: 44)
                        }
                        .buttonStyle(.plain)
                    } footer: {
                        Text("You can name a kind of tree we do not map yet.")
                    }
                }
            }
            .searchable(text: $query, prompt: "Which kind of tree?")
            .task { build() }
            .navigationTitle("What kind of tree is it?")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }
                }
            }
        }
    }
}
