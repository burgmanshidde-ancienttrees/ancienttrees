// Choosing a species to filter the map by.
//
// It was a Menu holding the fourteen commonest, which is a dropdown pretending
// to be a picker: there are forty species on the map and the one somebody wants
// is often not in the top fourteen (Hidde, 2026-08-24: "als ik op species klik
// dan zou ik een dieperliggende pagina verwachten om te selecteren omdat het er
// zoveel zijn, eigenlijk zoiets als je op de zoekfunctie klikt").
//
// So it is the app's own search pattern instead: a list you can type into, with
// the count beside each name so the choice is informed. Nothing invented; this
// is the shape every filter with more than a handful of options has.
import SwiftUI

struct SpeciesPicker: View {
    let catalogue: Catalogue
    /// What is on the map right now, so the list leads with what is actually
    /// around you rather than with what we happen to map most worldwide.
    let nearby: [String]
    @Binding var selection: String?

    @Environment(\.dismiss) private var dismiss
    @State private var query = ""

    private var counts: [String: Int] {
        Dictionary(grouping: catalogue.trees, by: \.commonName).mapValues(\.count)
    }

    private var rows: [String] {
        let all = Array(Set(catalogue.trees.map(\.commonName)))
        let q = query.trimmingCharacters(in: .whitespaces).lowercased()
        let hits = q.isEmpty ? all : all.filter { $0.lowercased().contains(q) }
        let near = Set(nearby)
        return hits.sorted {
            // Around you first, then by how many we map, then alphabetically so
            // the order never wobbles between two species with the same count.
            if near.contains($0) != near.contains($1) { return near.contains($0) }
            let a = counts[$0] ?? 0, b = counts[$1] ?? 0
            return a == b ? $0 < $1 : a > b
        }
    }

    var body: some View {
        NavigationStack {
            List {
                if selection != nil {
                    Button("Any species") { selection = nil; dismiss() }
                        .foregroundStyle(Brand.moss)
                }
                ForEach(rows, id: \.self) { name in
                    Button {
                        selection = name
                        dismiss()
                    } label: {
                        HStack(spacing: 12) {
                            SpeciesMark(species: name, color: Brand.moss)
                                .frame(width: 26, height: 26)
                            Text(name).foregroundStyle(Brand.ink)
                            Spacer(minLength: 8)
                            if selection == name {
                                Image(systemName: "checkmark").foregroundStyle(Brand.moss)
                            } else {
                                Text("\(counts[name] ?? 0)")
                                    .font(.subheadline).monospacedDigit()
                                    .foregroundStyle(Brand.inkSoft)
                            }
                        }
                        .frame(minHeight: 44)
                    }
                    .buttonStyle(.plain)
                }
            }
            .searchable(text: $query, prompt: "Which kind of tree?")
            .navigationTitle("Species")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }
                }
            }
        }
    }
}
