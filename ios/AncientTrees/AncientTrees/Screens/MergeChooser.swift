// Merging a tree you added into one of ours, from the ⋯ menu on its page.
//
// Convention: Google Maps fixes a duplicate place through its report menu
// ("Suggest an edit", "Place is a duplicate"), never through a banner on the
// place (CONVENTIONS.md, "Adding a tree that is already on the map"). Hidde,
// 2026-10-19, on the box that asked on the page itself: "this is hell
// intrusive flow for how rare it is". So it lives in the menu, beside the
// other things you can do to your own tree, and this list is shaped like the
// species one beside it (SpeciesChooser): nearest first, search by name.
//
// The merge itself is instant (Hidde, same day: "let them do it"). It only
// changes the person's own tree; whether their photograph shows on our page
// is still decided by the photo review, which is where a wrong trunk is caught.
import SwiftUI

struct MergeChooser: View {
    let catalogue: Catalogue
    /// Where the tree you added stands.
    let origin: (lat: Double, lng: Double)
    let onMerge: (Tree) -> Void

    @Environment(\.dismiss) private var dismiss
    @State private var query = ""
    @State private var confirming: Tree?
    /// Sorted once, when the sheet opens, the same reason SpeciesChooser
    /// builds its index once: every tree times every keystroke froze it.
    @State private var nearest: [Tree] = []

    private var typed: String { query.trimmingCharacters(in: .whitespaces) }

    private var rows: [Tree] {
        typed.count >= 2
            ? CollectSheet.search(typed, origin: origin, trees: catalogue.trees)
            : nearest
    }

    private func metres(_ t: Tree) -> Int {
        Int(Geo.km(origin, (t.lat, t.lng)) * 1000)
    }

    var body: some View {
        NavigationStack {
            List {
                Section {
                    ForEach(rows) { t in
                        Button { confirming = t } label: {
                            VStack(alignment: .leading, spacing: 2) {
                                Text(t.name).foregroundStyle(Brand.ink)
                                Text(CollectSheet.candidateLabel(species: t.commonName,
                                                                 metres: metres(t)))
                                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                            }
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .contentShape(.rect)
                            .frame(minHeight: 44)
                        }
                        .buttonStyle(.plain)
                    }
                } footer: {
                    if rows.isEmpty, typed.count >= 2 {
                        Text("None of our trees is called that.")
                    }
                }
            }
            .searchable(text: $query, prompt: "Search trees by name")
            .task {
                guard nearest.isEmpty else { return }
                let measured: [(tree: Tree, km: Double)] = catalogue.trees.map {
                    ($0, Geo.km(origin, ($0.lat, $0.lng)))
                }
                nearest = measured.sorted { $0.km < $1.km }.prefix(20).map { $0.tree }
            }
            .navigationTitle("Merge with")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
            }
            .sheet(item: $confirming) { t in
                BrandSheet(
                    icon: "arrow.triangle.merge",
                    title: "Merge into \(t.name)?",
                    message: "Your photos move to its page and this copy goes from your trees.",
                    buttons: [
                        .primary("Merge trees", id: "merge-confirm") {
                            confirming = nil
                            onMerge(t)
                            dismiss()
                        },
                        .quiet("Cancel") { confirming = nil },
                    ])
            }
        }
    }
}
