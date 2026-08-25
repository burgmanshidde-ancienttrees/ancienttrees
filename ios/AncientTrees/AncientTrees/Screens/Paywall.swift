// The upgrade screen, built to the shape AllTrails uses because that shape is
// doing specific work rather than looking nice.
//
// The element worth copying almost verbatim is the trial timeline. Theirs reads
// "Vandaag: ontgrendel alle eigenschappen / Dag 5: ontvang een herinnering /
// Dag 7: er wordt EUR 29,99 in rekening gebracht". It answers the only real
// objection to a free trial, which is the fear of a silent charge, and it does
// it by promising a reminder two days before rather than by asking for trust.
//
// Two deliberate differences from theirs.
//
// They lead with social proof, 4.9 stars and a million reviews. We have nine
// waitlist signups, so the same move would read as desperate. We lead with the
// thing the person was already reaching for.
//
// And there is no purchase here, on purpose. The price and the processor are
// Hidde's alone. What this screen does today is put a real number in front of a
// real intention and count who says yes, which is the only honest answer to
// "have we validated that real people will pay for this".

import SwiftUI

struct PaywallView: View {
    let feature: Feature
    @Environment(Entitlement.self) private var entitlement
    @Environment(Account.self) private var account
    @Environment(Saved.self) private var saved
    @Environment(\.dismiss) private var dismiss
    @State private var registered = false
    @State private var sending = false
    @State private var signingIn = false
    @State private var failed = false

    private let price = "€19.95"
    private let trialDays = 7

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 22) {
                    headline
                    timeline
                    everythingElse
                    freeForever
                }
                .padding(20)
                .padding(.bottom, 110)
            }
            .safeAreaInset(edge: .bottom) { cta }
            .sheet(isPresented: $signingIn) {
                SignInSheet(reason: .seasonAlerts, localCount: saved.savedCount)
                    .environment(account)
                    .environment(saved)
            }
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Not now") { dismiss() }
                }
            }
        }
        .accessibilityElement(children: .contain)
        .accessibilityIdentifier("paywall-sheet")
    }

    /// Names what they were doing, never the plan. "Download Palermo" converts;
    /// "Go Plus" does not.
    private var headline: some View {
        VStack(alignment: .leading, spacing: 10) {
            SpeciesMark(species: "Cedar of Lebanon",
                        color: Color(red: 0.20, green: 0.35, blue: 0.20))
                .frame(width: 54, height: 54)
            Text(feature.ask).font(.largeTitle.bold())
            Text(feature.detail).font(.subheadline).foregroundStyle(.secondary)
            Text("The first week is on us. \(price) a year after that.")
                .font(.subheadline.weight(.medium))
                .padding(.top, 2)
        }
    }

    /// The box that removes the fear of a silent charge.
    private var timeline: some View {
        VStack(alignment: .leading, spacing: 0) {
            Text("How the free week works")
                .font(.footnote.weight(.semibold)).foregroundStyle(.secondary)
                .padding(.bottom, 12)
            step("lock.open", "Today", "Everything unlocks.")
            step("bell", "Day 5", "We remind you the week is nearly up.")
            step("checkmark.circle", "Day \(trialDays)", "\(price) is charged, unless you cancelled.", last: true)
        }
        .padding(16)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(.secondarySystemBackground), in: .rect(cornerRadius: 14))
    }

    private func step(_ icon: String, _ when: String, _ what: String, last: Bool = false) -> some View {
        HStack(alignment: .top, spacing: 12) {
            VStack(spacing: 0) {
                Image(systemName: icon).font(.footnote).frame(width: 22, height: 22)
                if !last {
                    Rectangle().fill(.quaternary).frame(width: 1, height: 22)
                }
            }
            VStack(alignment: .leading, spacing: 2) {
                Text(when).font(.subheadline.weight(.semibold))
                Text(what).font(.footnote).foregroundStyle(.secondary)
            }
            .padding(.bottom, last ? 0 : 14)
            Spacer()
        }
    }

    private var everythingElse: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Also included").font(.footnote.weight(.semibold)).foregroundStyle(.secondary)
            ForEach([Feature.offlineDownload, .walkBeyondFirst, .badges,
                     .photoUpload, .seasonAlerts].filter { $0 != feature }, id: \.rawValue) { f in
                HStack(alignment: .top, spacing: 10) {
                    Image(systemName: "checkmark").font(.caption.weight(.bold))
                        .foregroundStyle(Color(red: 0.20, green: 0.35, blue: 0.20))
                        .frame(width: 18)
                        .padding(.top, 3)
                    VStack(alignment: .leading, spacing: 1) {
                        Text(f.ask).font(.subheadline.weight(.medium))
                        Text(f.detail).font(.caption).foregroundStyle(.secondary)
                    }
                }
            }
        }
    }

    /// Said plainly, because it is the strongest thing we have to say and
    /// because it is true: the trees themselves are never behind this.
    private var freeForever: some View {
        Text("Every tree, every story and every location stays free, here and on the website. This pays for the things that make them easier to reach.")
            .font(.footnote).foregroundStyle(.secondary)
            .padding(16)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(Color(.secondarySystemBackground), in: .rect(cornerRadius: 12))
    }

    private var cta: some View {
        VStack(spacing: 8) {
            if registered {
                Label("We will tell you the day it opens", systemImage: "checkmark.seal.fill")
                    .font(.subheadline.weight(.semibold))
                    .frame(maxWidth: .infinity).padding(.vertical, 15)
                    .background(Color(.secondarySystemBackground), in: .capsule)
            } else {
                Button {
                    // Signed out, this button cannot keep its own promise, so it
                    // asks the one question that lets it: who are you. That also
                    // makes the highest-intent screen in the app an account
                    // surface, which is where AllTrails gets most of theirs.
                    guard let mail = account.email else { signingIn = true; return }
                    Task {
                        sending = true
                        entitlement.registerInterest(feature)
                        // Only claim it worked if it worked. The old code threw
                        // the result away and said yes regardless, which is how
                        // a button that had never once succeeded still looked
                        // like it had.
                        let ok = await Waitlist.join(reason: feature.rawValue, email: mail)
                        sending = false
                        registered = ok
                        failed = !ok
                    }
                } label: {
                    HStack {
                        if sending { ProgressView().tint(.white).padding(.trailing, 6) }
                        Text("Tell me when this opens")
                    }
                    .font(.headline).frame(maxWidth: .infinity).padding(.vertical, 15)
                }
                .buttonStyle(.borderedProminent)
                .tint(Color(red: 0.20, green: 0.35, blue: 0.20))
                .clipShape(.capsule)
                .disabled(sending)
                Text(failed
                     ? "That did not go through. Try again in a minute."
                     : account.isSignedIn
                       ? "Not open yet. No card, nothing charged."
                       : "Not open yet, so there is no card and nothing to pay. We only need an address to write to.")
                    .font(.caption2)
                    .foregroundStyle(failed ? .red : .secondary)
                    .multilineTextAlignment(.center)
            }
        }
        .padding(.horizontal, 20).padding(.bottom, 10).padding(.top, 8)
        .background(.bar)
    }
}

/// A locked row: shows the thing, says it is locked, and opens the ask on tap.
/// Never hides what is behind it, because a lock over something invisible is
/// just an absence and sells nothing.
struct LockedRow<Label: View>: View {
    let feature: Feature
    /// How far the lock sits from the right edge. It used to sit flush against
    /// it while the label inside carried its own 16 points, so on the Season
    /// alerts row the padlock hung past everything else on the card (Hidde,
    /// 2026-08-24). The default matches what every caller here uses.
    var inset: CGFloat = 16
    /// Whether to draw the padlock. False when the thing inside already says
    /// Plus on its face, which is every walk card (Hidde, 2026-08-25: "dat
    /// lock icoontje voegt niks toe, plus label is genoeg").
    ///
    /// It was not only redundant. This row is an HStack with a Spacer and
    /// `maxWidth: .infinity`, which is right in a settings list and wrong
    /// inside a horizontal shelf: each card stretched to fill, so the padlock
    /// floated in the gap BETWEEN two walk cards and the gap itself grew to
    /// about ninety points. He reported the spacing and the padlock as two
    /// separate complaints on the same screen and they were one bug.
    var lockGlyph: Bool = true
    @ViewBuilder var label: Label
    @Environment(Entitlement.self) private var entitlement
    @State private var asking = false

    var body: some View {
        Button {
            if !entitlement.allows(feature) { asking = true }
        } label: {
            if lockGlyph {
                HStack {
                    label
                    Spacer()
                    if !entitlement.allows(feature) {
                        Image(systemName: "lock.fill").font(.caption)
                            .foregroundStyle(.secondary)
                            .padding(.trailing, inset)
                    }
                }
                .frame(maxWidth: .infinity, minHeight: 44, alignment: .leading)
                .contentShape(.rect)
                // One element the size of the row. A plain button in a list
                // reports the bounds of its glyphs otherwise, which made five
                // rows start at five different x positions, one per SF Symbol.
                .accessibilityElement(children: .combine)
            } else {
                label
                    .contentShape(.rect)
                    .accessibilityElement(children: .combine)
            }
        }
        .buttonStyle(.plain)
        .sheet(isPresented: $asking) { PaywallView(feature: feature) }
    }
}
