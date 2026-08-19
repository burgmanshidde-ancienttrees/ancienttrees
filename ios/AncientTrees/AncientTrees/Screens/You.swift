// The collect verb.
//
// The scaffolding shows before there is anything in it. AllTrails' progress
// screen draws a full-size chart with exactly one bar on it and tiles reading
// 0.2 km, rather than hiding behind a "you have not collected anything yet"
// message. The shape of what you are about to fill in is itself the invitation,
// and on launch day this screen is empty for every single user.

import SwiftUI

struct YouView: View {
    let catalogue: Catalogue
    @Environment(Saved.self) private var saved

    private var visited: [Tree] {
        saved.entries.values.filter { $0.visitedAt != nil }
            .sorted { ($0.visitedAt ?? .distantPast) > ($1.visitedAt ?? .distantPast) }
            .compactMap { catalogue.tree($0.treeId) }
    }
    private var wishlist: [Tree] {
        saved.entries.values.filter { $0.visitedAt == nil }
            .sorted { $0.savedAt > $1.savedAt }
            .compactMap { catalogue.tree($0.treeId) }
    }
    private var countries: Int { Set(visited.map(\.country)).count }
    private var cities: Int { Set(visited.map(\.citySlug)).count }

    var body: some View {
        List {
            Section {
                HStack(spacing: 0) {
                    tile("\(visited.count)", "Stood in front of")
                    Divider().frame(height: 40)
                    tile("\(cities)", cities == 1 ? "Place" : "Places")
                    Divider().frame(height: 40)
                    tile("\(countries)", countries == 1 ? "Country" : "Countries")
                }
                .padding(.vertical, 8)
                .listRowInsets(.init(top: 0, leading: 0, bottom: 0, trailing: 0))
            }

            if !visited.isEmpty {
                Section("Trees you have stood in front of") {
                    ForEach(visited) { t in row(t, ticked: true) }
                }
            }
            if !wishlist.isEmpty {
                Section("Saved for later") {
                    ForEach(wishlist) { t in row(t, ticked: false) }
                }
            }
            Section("Account") {
                // Sign-in and the subscription both land here. Neither is wired
                // yet: accounts exist on the website against Supabase, and the
                // price is Hidde's alone under hard rule 2, so this is the shelf
                // they go on rather than a promise the app already keeps.
                LabeledContent("Signed in", value: "not yet")
                LabeledContent("Plan", value: "Free")
            }

            if visited.isEmpty && wishlist.isEmpty {
                Section {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Nothing here yet, and that is the point.")
                            .font(.subheadline.weight(.semibold))
                        Text("Tick a tree off when you have stood in front of it. There are \(catalogue.trees.count) to find, in \(Set(catalogue.trees.map(\.country)).count) countries.")
                            .font(.footnote).foregroundStyle(.secondary)
                    }
                    .padding(.vertical, 6)
                }
            }
        }
        .navigationTitle("You")
    }

    private func tile(_ value: String, _ label: String) -> some View {
        VStack(spacing: 4) {
            Text(value).font(.title.bold()).monospacedDigit()
            Text(label).font(.caption2).foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .frame(maxWidth: .infinity)
    }

    private func row(_ t: Tree, ticked: Bool) -> some View {
        NavigationLink {
            TreeDetail(tree: t, catalogue: catalogue)
        } label: {
            HStack(spacing: 10) {
                Image(systemName: ticked ? "checkmark.seal.fill" : "heart.fill")
                    .foregroundStyle(ticked ? Color(red: 0.20, green: 0.35, blue: 0.20) : .pink)
                VStack(alignment: .leading, spacing: 2) {
                    Text(t.name).font(.subheadline.weight(.medium))
                    Text("\(t.commonName) · \(t.city)").font(.caption).foregroundStyle(.secondary)
                }
            }
        }
    }
}
