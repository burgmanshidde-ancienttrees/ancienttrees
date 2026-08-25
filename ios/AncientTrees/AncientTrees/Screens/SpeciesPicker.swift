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
    /// Counted ONCE, when the sheet opens.
    ///
    /// It used to be two computed properties: a Dictionary(grouping:) over
    /// every tree we map, and a Set of every common name, both rebuilt on each
    /// view update and the first of them read again inside the row loop. That
    /// is roughly 1,842 trees times 40 rows per keystroke, and it froze the app
    /// the moment the sheet opened (Hidde, 2026-08-24: "de app loopt vast als
    /// ik op de species filter druk").
    @State private var index: [(name: String, count: Int)] = []

    private func build() {
        guard index.isEmpty else { return }
        var counts: [String: Int] = [:]
        for t in catalogue.trees { counts[t.commonName, default: 0] += 1 }
        let near = Set(nearby)
        index = counts.map { (name: $0.key, count: $0.value) }
            .sorted {
                // Around you first, then by how many we map, then alphabetically
                // so the order never wobbles between two with the same count.
                if near.contains($0.name) != near.contains($1.name) {
                    return near.contains($0.name)
                }
                return $0.count == $1.count ? $0.name < $1.name : $0.count > $1.count
            }
    }

    private var rows: [(name: String, count: Int)] {
        let q = query.trimmingCharacters(in: .whitespaces).lowercased()
        guard !q.isEmpty else { return index }
        return index.filter { $0.name.lowercased().contains(q) }
    }

    var body: some View {
        NavigationStack {
            List {
                if selection != nil {
                    Button("Any species") { selection = nil; dismiss() }
                        .foregroundStyle(Brand.moss)
                }
                ForEach(rows, id: \.name) { row in
                    let name = row.name
                    Button {
                        // Tapping the one already chosen turns it OFF (Hidde,
                        // 2026-08-25: "als je er een selecteerd en je klikt er
                        // nog een keer op dat hij hem deselecteert"). A row
                        // with a tick beside it that does nothing when you tap
                        // it is the one row on the screen whose behaviour
                        // nobody can guess.
                        selection = (selection == name) ? nil : name
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
                                Text("\(row.count)")
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
            .task { build() }
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
