// Why we ask for your location, said before iOS asks for it.
//
// The system dialog is a single shot. Tap "Don't Allow" once and the app cannot
// ask again; the person has to find their way into Settings, which almost
// nobody does. So the expensive mistake is not being refused, it is being
// refused by somebody who would have said yes if they had known what it was
// for. AllTrails, Komoot and Citymapper all put a screen in front of it for
// exactly that reason, and the convention rule says take theirs rather than
// invent one.
//
// Three things this screen does, in the order they matter:
//
// 1. It says what you GET, not what we need. "See the remarkable old trees
//    closest to you" is the product; "allow location access" is plumbing.
// 2. It says where the location goes, which is nowhere. That sentence is cheap
//    and it is the objection most people actually have.
// 3. It has a way out that is not a refusal. "Not now" leaves the system
//    dialog unasked, so the map opens on Amsterdam and says so, and we can ask
//    again another day. A "Don't Allow" tap cannot be taken back.
//
// It is shown once, only when the status is genuinely undecided, and never
// again. Someone who has already answered iOS never sees it.

import SwiftUI

struct LocationPrimer: View {
    let treeCount: Int
    let onAllow: () -> Void
    let onSkip: () -> Void

    private let brand = Color(red: 0.20, green: 0.35, blue: 0.20)

    var body: some View {
        ZStack {
            LinearGradient(colors: [Color(red: 0.13, green: 0.22, blue: 0.13),
                                    Color(red: 0.24, green: 0.36, blue: 0.22)],
                           startPoint: .top, endPoint: .bottom)
                .ignoresSafeArea()

            VStack(spacing: 0) {
                Spacer(minLength: 24)

                // Three species drawn rather than a map screenshot: the point of
                // the screen is the trees, and a picture of a map would be a
                // picture of the permission.
                HStack(spacing: 18) {
                    ForEach(["Pedunculate Oak", "Ginkgo", "Cedar of Lebanon"], id: \.self) { s in
                        SpeciesMark(species: s, color: .white.opacity(0.92))
                            .frame(width: 62, height: 62)
                    }
                }
                .padding(.bottom, 26)

                // Every line of text on this screen is centred inside the
                // same 30 point margins and takes the full width between
                // them, so its frame starts at the margin whatever its
                // length. A centred line that hugs its own letters starts
                // wherever its width puts it, and reads as a drift.
                Text("Trees worth the walk, wherever you are")
                    .font(.largeTitle.bold())
                    .foregroundStyle(.white)
                    .multilineTextAlignment(.center)
                    .frame(maxWidth: .infinity)
                    .padding(.horizontal, 30)

                Text("We map \(treeCount.formatted(.number.locale(Locale(identifier: "en_US")))) remarkable old trees. Let the map see where you are and it opens on the ones nearest you, with the walk time to each.")
                    .font(.subheadline)
                    .foregroundStyle(.white.opacity(0.85))
                    .multilineTextAlignment(.center)
                    .frame(maxWidth: .infinity)
                    .padding(.horizontal, 30)
                    .padding(.top, 12)

                Label("Your location stays on your phone. We never send it anywhere.",
                      systemImage: "lock.fill")
                    .font(.footnote)
                    .foregroundStyle(.white.opacity(0.8))
                    .multilineTextAlignment(.center)
                    .frame(maxWidth: .infinity)
                    .padding(.horizontal, 30)
                    .padding(.top, 18)

                Spacer(minLength: 24)

                Button(action: onAllow) {
                    Text("Show me trees near me")
                        .font(.headline)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 16)
                }
                .background(.white, in: .capsule)
                .foregroundStyle(brand)
                // The same 30 as the paragraphs above it; at 26 the button
                // started four points left of every line of text.
                .padding(.horizontal, 30)

                Button(action: onSkip) {
                    Text("Not now")
                        .font(.subheadline.weight(.medium))
                        .foregroundStyle(.white.opacity(0.75))
                        .padding(.vertical, 14)
                }
                .padding(.bottom, 10)
            }
        }
        .accessibilityElement(children: .contain)
        .accessibilityIdentifier("primer")
    }
}
