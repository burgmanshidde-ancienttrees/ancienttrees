// Account, subscription and what you have added up to. Deliberately thin: the
// saved trees moved to their own tab, because that is the screen people open
// weekly and this is the one they open twice a year.

import SwiftUI

struct YouView: View {
    let catalogue: Catalogue
    @Environment(Saved.self) private var saved

    private var visited: [Tree] {
        saved.entries.values.filter { $0.visitedAt != nil }.compactMap { catalogue.tree($0.treeId) }
    }
    private var countries: Int { Set(visited.map(\.country)).count }
    private var cities: Int { Set(visited.map(\.citySlug)).count }
    private var species: Int { Set(visited.map(\.commonName)).count }

    var body: some View {
        List {
            Section {
                HStack(spacing: 0) {
                    tile("\(visited.count)", "Trees")
                    Divider().frame(height: 40)
                    tile("\(cities)", cities == 1 ? "Place" : "Places")
                    Divider().frame(height: 40)
                    tile("\(species)", species == 1 ? "Species" : "Species")
                    Divider().frame(height: 40)
                    tile("\(countries)", countries == 1 ? "Country" : "Countries")
                }
                .padding(.vertical, 10)
                .listRowInsets(.init(top: 0, leading: 0, bottom: 0, trailing: 0))
            } footer: {
                Text("Out of \(catalogue.trees.count) trees in \(Set(catalogue.trees.map(\.country)).count) countries.")
            }

            Section("Account") {
                // Sign-in exists on the website against Supabase and the price is
                // Hidde's alone under hard rule 2, so these are the shelves they
                // go on rather than promises the app already keeps.
                LabeledContent("Signed in", value: "not yet")
                LockedRow(feature: .badges) {
                    LabeledContent("Badges", value: "Plus")
                }
                LockedRow(feature: .offlineDownload) {
                    LabeledContent("Offline", value: "Plus")
                }
                LockedRow(feature: .seasonAlerts) {
                    LabeledContent("Season alerts", value: "Plus")
                }
            }

            Section {
                Link("The website", destination: URL(string: "https://ancienttrees.app")!)
                Link("Privacy", destination: URL(string: "https://ancienttrees.app/privacy")!)
            } footer: {
                Text("Catalogue version \(catalogue.version). Every tree, story and location is free, on the web and here.")
            }
        }
        .navigationTitle("You")
    }

    private func tile(_ value: String, _ label: String) -> some View {
        VStack(spacing: 4) {
            Text(value).font(.title2.bold()).monospacedDigit()
            Text(label).font(.caption2).foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity)
    }
}
