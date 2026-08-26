// The sponsor sheet. It used to be PaywallView(feature: .sponsor), which put
// the ask for support inside a screen whose whole job is listing Plus, and
// Plus is hidden at launch (Kit/Launch.swift). Sponsoring is not a plan, not a
// trial and not a feature list: it is somebody deciding they want this to keep
// existing.
//
// The copy is the website's, on purpose. /sponsor leads with what Ancient
// Trees is and ties the money to the one unit of work this project has, the
// next city, because that is what the strongest creator pages do: orientation
// first, then a concrete outcome. Both surfaces say the same thing in their
// own shape, which is the both-surfaces rule.

import SwiftUI
import StoreKit

struct SponsorSheet: View {
    @Environment(\.dismiss) private var dismiss
    @State private var tips = Tips()

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 18) {
                    SpeciesMark(species: "Cedar of Lebanon", color: Brand.moss)
                        .frame(width: 54, height: 54)

                    Text("Sponsor this project")
                        .font(.largeTitle.bold()).foregroundStyle(Brand.ink)

                    Text("Ancient Trees maps the oldest and most remarkable trees of the world's cities: where each one stands, how old it is, and why it is worth the walk.")
                        .font(.subheadline).foregroundStyle(Brand.inkSoft)

                    Text("A city takes days rather than minutes: finding the trees a listicle never mentions, checking each one against two independent sources, and placing every pin. Sponsoring is what puts the next city on the map.")
                        .font(.subheadline).foregroundStyle(Brand.inkSoft)

                    if tips.thanked {
                        Label("Thank you. That goes straight into the next city.",
                              systemImage: "checkmark.seal.fill")
                            .font(.callout.weight(.medium))
                            .foregroundStyle(Brand.moss)
                    } else if tips.loading {
                        ProgressView().frame(maxWidth: .infinity)
                    } else if tips.products.isEmpty {
                        // Honest empty, the same rule the website follows while
                        // its sponsor link is unset: say what is true rather
                        // than show a button that cannot work.
                        Text("Sponsoring from inside the app is not open yet.")
                            .font(.callout.weight(.medium)).foregroundStyle(Brand.ink)
                    } else {
                        VStack(spacing: 10) {
                            ForEach(tips.products, id: \.id) { p in
                                Button {
                                    Task { await tips.buy(p) }
                                } label: {
                                    HStack {
                                        Text(p.displayName)
                                        Spacer()
                                        Text(p.displayPrice).monospacedDigit()
                                    }
                                    .font(.callout.weight(.semibold))
                                    .frame(maxWidth: .infinity, minHeight: 48)
                                    .padding(.horizontal, 16)
                                    .background(Brand.moss.opacity(0.10), in: .rect(cornerRadius: 14))
                                    .foregroundStyle(Brand.moss)
                                }
                                .buttonStyle(.plain)
                                .accessibilityIdentifier("sponsor-tip-\(p.id)")
                            }
                        }
                    }

                    if tips.failed {
                        Text("That did not go through. Nothing was charged.")
                            .font(.footnote).foregroundStyle(.red)
                    }

                    Text("Sponsoring unlocks nothing and is not a subscription. If you would rather help without money, send us a tree we are missing.")
                        .font(.footnote).foregroundStyle(Brand.inkSoft)
                }
                .padding(20)
            }
            .accessibilityElement(children: .contain)
            .accessibilityIdentifier("sponsor-sheet")
            .navigationTitle("Sponsor")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button(tips.thanked ? "Done" : "Close") { dismiss() }
                }
            }
            .task { await tips.load() }
        }
    }
}
