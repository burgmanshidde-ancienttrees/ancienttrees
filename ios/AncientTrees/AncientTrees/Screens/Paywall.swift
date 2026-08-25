// The upgrade screen, built to the shape AllTrails uses because that shape is
// doing specific work rather than looking nice.
//
// AS OF 2026-08-25 IT SELLS NOTHING AND SAYS SO. Hidde turned Plus off for the
// MVP ("it just says it will come soon"), so the trial timeline and the price
// are gone: they described a charge this app has no way to make. What stays is
// the part that earns its place in phase 1, which is the list of what Plus will
// hold and a button that counts who wants it.
//
// The timeline is worth rebuilding verbatim the day a processor exists. Theirs
// reads "Vandaag: ontgrendel alle eigenschappen / Dag 5: ontvang een
// herinnering / Dag 7: er wordt EUR 29,99 in rekening gebracht", and it answers
// the only real objection to a free trial by promising a reminder two days
// before rather than by asking for trust.
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

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 22) {
                    headline
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
            // COMING, not for sale (Hidde, 2026-08-25: "I think we should work
            // towards an MVP of the app that does not allow Plus yet, but it
            // just says it will come soon"). What stood here was a trial
            // timeline ending in "19.95 is charged, unless you cancelled",
            // which described a transaction this app cannot carry out: there
            // is no processor and the price is not public yet. A screen that
            // walks somebody through a charge that cannot happen is the one
            // kind of dishonesty this project cannot afford.
            Text("Plus is not open yet. We are building it, and this is the list.")
                .font(.subheadline.weight(.medium))
                .padding(.top, 2)
        }
    }

    // The trial timeline went with the price on 2026-08-25. It was the best
    // thing on this screen and it was answering a question nobody can ask yet:
    // "when am I charged" has no answer while there is nothing to charge with.
    // It is worth rebuilding exactly as it was the day a processor exists, and
    // the shape is recorded in DECISIONS.md rather than left here as dead code:
    // today, day five a reminder, day seven the charge.

    private var everythingElse: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Also included").font(.footnote.weight(.semibold)).foregroundStyle(.secondary)
            ForEach([Feature.offlineDownload, .walkBeyondFirst, .badges,
                     .photoUpload, .seasonAlerts].filter { $0 != feature },
                    id: \.rawValue) { f in
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
        Text("Every tree, every story and every location stays free, here and on the website. Plus will pay for the things that make them easier to reach.")
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
