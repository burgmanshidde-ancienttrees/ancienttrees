// The sponsor sheet. It used to be PaywallView(feature: .sponsor), which put
// the ask for support inside a screen whose whole job is listing Plus, and
// Plus is hidden at launch (Kit/Launch.swift). Sponsoring is not a plan, not a
// trial and not a feature list: it is somebody deciding they want this to keep
// existing.
//
// The copy is the website's, word for word (Hidde, 2026-08-28, having
// rewritten /sponsor himself: "gebruik deze tekst ook in de app"). It is his
// own sentences, so it is not paraphrased per surface: the ask reads the same
// on a phone as on the page, which is the both-surfaces rule at its plainest.

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

                    Text("Ancient Trees is a passion project. I'm building it to let others appreciate nature and go outside. Marvel at something older than you can imagine.")
                        .font(.subheadline).foregroundStyle(Brand.inkSoft)

                    Text("Running the website and app does cost money. A donation would help me enormously: more time and more resources to make this much better, and to get more of these trees on the map.")
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

                    Text("Sponsoring unlocks nothing and is not a subscription. You can also contribute by adding a tree that is missing.")
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
