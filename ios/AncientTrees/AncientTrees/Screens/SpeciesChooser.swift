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

    private var rows: [(name: String, count: Int)] {
        guard !typed.isEmpty else { return index }
        return index.filter { $0.name.localizedCaseInsensitiveContains(typed) }
    }

    /// Offered only when nothing on the list matches what they typed, which is
    /// how every tag field that also accepts new tags behaves. Offering it
    /// beside a matching row invites a second spelling of a name we already
    /// have, which is the whole reason this screen exists.
    private var mayTypeOwn: Bool {
        typed.count >= 3 && !rows.contains { $0.name.lowercased() == typed.lowercased() }
    }

    var body: some View {
        NavigationStack {
            List {
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

                Section {
                    ForEach(rows, id: \.name) { row in
                        Button {
                            onPick(row.name)
                            dismiss()
                        } label: {
                            HStack(spacing: 12) {
                                SpeciesMark(species: row.name, color: Brand.moss)
                                    .frame(width: 26, height: 26)
                                Text(row.name).foregroundStyle(Brand.ink)
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
