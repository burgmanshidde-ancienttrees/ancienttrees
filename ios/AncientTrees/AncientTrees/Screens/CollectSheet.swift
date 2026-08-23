// Collecting a tree: one action, and we work out which kind it was.
//
// Hidde, 2026-08-23, on the two verbs that would not explain themselves:
// "add en collect zijn wel moeilijk uit te leggen". They were, and the reason
// is worth keeping written down, because it is a design lesson rather than a
// naming one. ADD and COLLECT are the SAME PHYSICAL ACT: you stand in front
// of a tree and photograph it. What separates them is not something the
// person does, it is something only our database knows. Two buttons asked
// them to answer a question they cannot answer, and no wording fixes that.
//
// So there is one button and one camera, and the app resolves the outcome
// from where the shutter fell:
//
//   one confident match   -> "This is the Totteridge Yew", ticked off
//   several candidates    -> "Which one is it?", a short list
//   nothing of ours near  -> a tree we do not have; keep it, or offer it
//
// The words "add" and "collect" survive as OUTCOMES WE REPORT, never as a
// choice on the way in. Seek works exactly this way: you point the camera and
// it tells you what you found, it does not ask first whether you think the
// species is in its database.
//
// WHY A PHOTOGRAPH IS COMPULSORY HERE. Hidde: "er is een psychologie dat
// mensen een actie laten doen het meer waard maakt". True, and there is a
// harder reason under it: the photograph is PROOF OF PRESENCE. A tick with no
// photograph is a button you can press from the sofa, and a collection you
// can fake is worth nothing to the person holding it. Geocaching makes you
// sign a physical logbook for the same reason. The web keeps a no-photo path
// at /contribute, which is the honest escape hatch; inside the app there is
// none.
//
// AND THE LOCATION COMES FROM CORELOCATION, NOT FROM THE PICTURE. Worth
// stating because the obvious assumption is the wrong one: a photo taken
// through UIImagePickerController arrives as a bare UIImage with every scrap
// of metadata gone, and a picture chosen from the library may have been
// stripped on share, or be a screenshot, or a download. `origin` here is the
// live device fix, which is the only reliable answer.
//
// The submission reuses the website's own channel (Submission.send, kind
// .tree): no new fields, no name asked, verification happens before anything
// goes live, exactly as Step 0b runs it for the site.

import SwiftUI

struct CollectSheet: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    /// Kept so older call sites and the debug launch arguments still compile;
    /// both modes now enter the same flow, because the flow is what decides.
    enum Mode: String { case collect, add }
    var mode: Mode = .collect

    @Environment(Saved.self) private var saved
    @Environment(Sightings.self) private var sightings
    @Environment(Account.self) private var account
    @Environment(\.dismiss) private var dismiss

    /// Where the flow is. One enum rather than five booleans, because the old
    /// sheet grew nine of them and two combinations were unreachable.
    private enum Stage: Equatable {
        case intro
        case identify          // photograph taken, more than one candidate
        case ticked(String)    // tree id, matched and claimed
        case describe          // a tree we do not map
        case sent
    }

    @State private var stage: Stage = .intro
    @State private var camera = false
    @State private var shot: UIImage?
    /// Where the shutter actually fell. Held separately from `origin` because
    /// the view can be re-evaluated with a newer fix while the outcome screen
    /// is up, and the record must not quietly move.
    @State private var at: (lat: Double, lng: Double)?
    @State private var why = ""
    @State private var sending = false
    @State private var failed = false
    @State private var signingIn = false

    /// Everything close enough to be the tree in front of the lens. 400 metres
    /// is deliberately wide: GPS under a canopy is poor and a short list beats
    /// a wrong no.
    static func nearby(origin: (lat: Double, lng: Double), trees: [Tree]) -> [Tree] {
        trees
            .map { ($0, Geo.km(origin, ($0.lat, $0.lng))) }
            .filter { $0.1 <= 0.4 }
            .sorted { $0.1 < $1.1 }
            .prefix(5)
            .map(\.0)
    }

    /// A match we are willing to make WITHOUT asking: the nearest tree is
    /// inside 80 metres and the runner-up is at least twice as far. Both
    /// halves matter. The first is roughly the worst honest GPS error in a
    /// city; the second is what stops us picking one of two trees standing
    /// side by side in a park, which is the single most common report readers
    /// send us ("I could not tell which tree").
    static func confident(origin: (lat: Double, lng: Double), trees: [Tree]) -> Tree? {
        let d = trees
            .map { ($0, Geo.km(origin, ($0.lat, $0.lng))) }
            .sorted { $0.1 < $1.1 }
        guard let first = d.first, first.1 <= 0.08 else { return nil }
        if d.count > 1, d[1].1 < first.1 * 2 { return nil }
        return first.0
    }

    private var candidates: [Tree] {
        Self.nearby(origin: at ?? origin, trees: catalogue.trees)
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            closeRow
            if stage == .intro {
                // The intro FILLS the sheet so its one action sits where a
                // thumb already is, which is what Airbnb does with any sheet
                // that asks for something. Everything after it is a list or a
                // form, so those scroll.
                CollectIntro(onStart: { camera = true })
                    .padding(.horizontal, 20)
                    .padding(.bottom, 24)
            } else {
                ScrollView {
                    VStack(alignment: .leading, spacing: 20) {
                        switch stage {
                        case .ticked(let id): if let t = catalogue.tree(id) { tickedState(t) }
                        case .identify: identifyState
                        case .describe: describeForm
                        case .sent: sentState
                        case .intro: EmptyView()
                        }
                    }
                    .padding(.horizontal, 20).padding(.bottom, 32)
                    .frame(maxWidth: .infinity, alignment: .leading)
                }
            }
        }
        .brandGround()
        .accessibilityElement(children: .contain)
        .accessibilityIdentifier("spot-sheet")
        .presentationDetents([.large])
        .presentationDragIndicator(.visible)
        .fullScreenCover(isPresented: $camera) {
            CameraPicker { resolve($0) }.ignoresSafeArea()
        }
        .sheet(isPresented: $signingIn) {
            SignInSheet(reason: .feedback, localCount: saved.savedCount)
        }
    }

    private var closeRow: some View {
        HStack {
            Spacer()
            Button { dismiss() } label: {
                Image(systemName: "xmark")
                    .font(.system(size: 13, weight: .semibold))
                    .foregroundStyle(Brand.inkSoft)
                    .frame(width: 30, height: 30)
                    .background(Brand.surfaceMuted, in: .circle)
                    // The circle stays 30 points; the finger gets 44.
                    .frame(width: 44, height: 44)
                    .contentShape(.rect)
            }
            .accessibilityLabel("Close")
            .accessibilityIdentifier("spot-close")
        }
        .padding(.horizontal, 12)
        .padding(.top, 4)
    }

    // MARK: - The one decision

    /// The whole design, in nine lines. Photograph first, ask afterwards, and
    /// only ask when we genuinely cannot tell.
    private func resolve(_ image: UIImage?) {
        guard let image else { return }
        shot = image
        let here = origin
        at = here
        if let t = Self.confident(origin: here, trees: catalogue.trees) {
            claim(t, image: image, at: here)
        } else if Self.nearby(origin: here, trees: catalogue.trees).isEmpty {
            withAnimation(.snappy) { stage = .describe }
        } else {
            withAnimation(.snappy) { stage = .identify }
        }
    }

    private func claim(_ t: Tree, image: UIImage, at here: (lat: Double, lng: Double)) {
        if !saved.isVisited(t.id) { saved.toggleVisited(t.id) }
        sightings.record(treeId: t.id, name: t.name, lat: t.lat, lng: t.lng, image: image)
        withAnimation(.snappy) { stage = .ticked(t.id) }
    }

    // MARK: - Which one is it

    /// Not an error state and not a fallback. Two trees ten metres apart is
    /// the ordinary case in a park, and being asked which one you are looking
    /// at is also the moment we learn something we could not know.
    private var identifyState: some View {
        Group {
            Text("Which one is it?")
                .font(.brand(24, .heavy)).foregroundStyle(Brand.ink)
            Text("You are standing among trees we map. Pick the one in your photograph.")
                .font(.subheadline).foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
            ForEach(candidates) { t in
                Button {
                    if let shot, let at { claim(t, image: shot, at: at) }
                } label: { row(t) }
                    .buttonStyle(.plain)
            }
            Divider().padding(.vertical, 4)
            Button { withAnimation(.snappy) { stage = .describe } } label: {
                HStack(spacing: 10) {
                    Image(systemName: "plus.circle.fill")
                        .font(.system(size: 22)).foregroundStyle(Brand.moss)
                    VStack(alignment: .leading, spacing: 2) {
                        Text("None of these")
                            .font(.brand(16, .bold)).foregroundStyle(Brand.ink)
                        Text("Then it is a tree we do not have yet")
                            .font(.footnote).foregroundStyle(Brand.inkSoft)
                    }
                }
                .frame(minHeight: 44)
                .contentShape(.rect)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("collect-none-of-these")
        }
    }

    private func row(_ t: Tree) -> some View {
        HStack(spacing: 12) {
            thumb(t)
            VStack(alignment: .leading, spacing: 3) {
                Text(t.name)
                    .font(.brand(16, .bold))
                    .foregroundStyle(Brand.ink)
                    .multilineTextAlignment(.leading)
                Text("\(t.commonName) · \(Int(Geo.km(at ?? origin, (t.lat, t.lng)) * 1000)) m")
                    .font(.footnote)
                    .foregroundStyle(Brand.inkSoft)
            }
            Spacer()
            Image(systemName: "chevron.right")
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(Brand.inkSoft)
        }
        .padding(12)
        .background(Brand.surface, in: .rect(cornerRadius: 14))
    }

    @ViewBuilder private func thumb(_ t: Tree) -> some View {
        if let p = t.photo, let url = Photos.thumb(p.url, width: 200) {
            AsyncImage(url: url) { img in
                img.resizable().aspectRatio(contentMode: .fill)
            } placeholder: {
                Brand.surfaceMuted
            }
            .frame(width: 56, height: 56)
            .clipShape(.rect(cornerRadius: 11))
        } else {
            SpeciesMark(species: t.commonName, color: Brand.moss)
                .frame(width: 56, height: 56)
                .background(Brand.surfaceMuted, in: .rect(cornerRadius: 11))
        }
    }

    // MARK: - You found one of ours

    /// The payoff, and the reason this beat exists at all: without it,
    /// collecting is filing paperwork. Somebody stood in front of something
    /// and the app's job at that exact second is to tell them what it is.
    private func tickedState(_ t: Tree) -> some View {
        VStack(alignment: .leading, spacing: 14) {
            Image(systemName: "checkmark.seal.fill")
                .font(.system(size: 44))
                .foregroundStyle(Brand.moss)
            Text("You found \(t.name)")
                .font(.brand(24, .heavy))
                .foregroundStyle(Brand.ink)
                .fixedSize(horizontal: false, vertical: true)
            Text(subtitle(t))
                .font(.body)
                .foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
            Text("It is in your trees now, with your photograph.")
                .font(.subheadline)
                .foregroundStyle(Brand.inkSoft)
            doneButton
            // The escape hatch, small and always there: a confident match is
            // still a guess, and the person holding the phone can see the
            // trunk we cannot.
            if candidates.count > 1 {
                Button("That was a different tree") {
                    if case .ticked(let id) = stage { saved.toggleVisited(id) }
                    withAnimation(.snappy) { stage = .identify }
                }
                .font(.footnote.weight(.semibold))
                .foregroundStyle(Brand.inkSoft)
                .frame(maxWidth: .infinity, minHeight: 44)
            }
        }
    }

    private func subtitle(_ t: Tree) -> String {
        let age = t.age.map { "\($0) old" }
        return [t.commonName, age].compactMap { $0 }.joined(separator: ", ")
    }

    // MARK: - A tree we do not have

    private var describeForm: some View {
        Group {
            Text("We do not have this one")
                .font(.brand(24, .heavy))
                .foregroundStyle(Brand.ink)
            Text("It is yours either way. Tell us about it and we will look at it for the map.")
                .font(.body)
                .foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)

            if let shot {
                Image(uiImage: shot)
                    .resizable().aspectRatio(contentMode: .fill)
                    .frame(height: 170).frame(maxWidth: .infinity)
                    .clipShape(.rect(cornerRadius: 14))
                    .overlay(alignment: .bottomTrailing) {
                        Button("Retake") { camera = true }
                            .font(.caption.weight(.semibold))
                            .foregroundStyle(.white)
                            .padding(.horizontal, 10).padding(.vertical, 6)
                            .background(.black.opacity(0.45), in: .capsule)
                            .padding(10)
                    }
                    .accessibilityIdentifier("spot-camera")
            }

            TextField("What makes it special? A name, a species, a story…",
                      text: $why, axis: .vertical)
                .lineLimit(3...6)
                .padding(13)
                .background(Brand.surfaceMuted, in: .rect(cornerRadius: 14))

            HStack(spacing: 8) {
                Image(systemName: "lock")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                Text("Your photograph stays on your phone and in your trees. Offering it is a separate choice.")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
            }

            Button { keepMine() } label: {
                HStack { Spacer()
                    Label("Keep it as mine", systemImage: "checkmark")
                        .font(.brand(17, .bold))
                    Spacer() }
                    .padding(.vertical, 15)
                    .background(Brand.moss, in: .rect(cornerRadius: 15))
                    .foregroundStyle(.white)
            }
            .buttonStyle(.plain)

            // Offering is the SECOND choice, and it needs the account that
            // lets us answer (2026-08-21, the Google Maps convention).
            Button {
                if account.isSignedIn { Task { await send() } }
                else { signingIn = true }
            } label: {
                HStack { Spacer()
                    if sending { ProgressView() }
                    Text("Keep it and offer it for the map").font(.brand(16, .bold))
                    Spacer() }
                    .padding(.vertical, 13)
                    .background(Brand.surfaceMuted, in: .rect(cornerRadius: 15))
                    .foregroundStyle(Brand.ink)
            }
            .buttonStyle(.plain)
            .disabled(sending || why.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)

            if failed {
                Text("That did not send, so it is kept as yours for now. Try offering it again later.")
                    .font(.footnote)
                    .foregroundStyle(Brand.inkSoft)
            }
        }
    }

    /// Yours and nobody else's: no network, no account, no waiting.
    private func keepMine() {
        let here = at ?? origin
        sightings.record(treeId: nil,
                         name: why.isEmpty ? "A tree I found" : String(why.prefix(60)),
                         note: why, lat: here.lat, lng: here.lng, image: shot)
        shot = nil
        dismiss()
    }

    private func send() async {
        sending = true
        let here = at ?? origin
        var d = Submission.Draft()
        d.kind = .tree
        d.why = why
        d.locationHint = String(format: "%.5f, %.5f (GPS)", here.lat, here.lng)
        d.city = nearbyCityName ?? ""
        let ok = await Submission.send(d, from: "app:collect",
                                       token: account.session?.accessToken)
        // Kept either way. A failed send is a network problem, not a reason to
        // lose somebody's photograph.
        sightings.record(treeId: nil,
                         name: why.isEmpty ? "A tree I found" : String(why.prefix(60)),
                         note: why, lat: here.lat, lng: here.lng, image: shot,
                         status: ok ? .sent : .mine)
        shot = nil
        sending = false
        failed = !ok
        if ok { withAnimation(.snappy) { stage = .sent } }
    }

    /// Best guess at which of our cities the person is in, for the triage
    /// queue only; empty when nowhere near one.
    private var nearbyCityName: String? {
        catalogue.trees
            .map { ($0, $0.distanceKm(from: (at ?? origin).lat, (at ?? origin).lng)) }
            .min { $0.1 < $1.1 }
            .flatMap { $0.1 <= 30 ? $0.0.city : nil }
    }

    /// No timescale, and no word that sets up a rejection. Most offered trees
    /// will not clear the research bar, and the one thing that makes that
    /// survivable is the sentence in the middle: it stays in YOUR trees
    /// whatever we decide about ours.
    private var sentState: some View {
        VStack(alignment: .leading, spacing: 14) {
            Image(systemName: "paperplane.fill")
                .font(.system(size: 40))
                .foregroundStyle(Brand.moss)
            Text("Sent. Thank you.")
                .font(.brand(24, .heavy))
                .foregroundStyle(Brand.ink)
            Text("It is in your trees already, and it stays there whatever we find. We check every tree before it joins the map everybody sees, and we will write to you either way.")
                .font(.body)
                .foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
            doneButton
        }
    }

    private var doneButton: some View {
        Button { dismiss() } label: {
            HStack { Spacer(); Text("Done").font(.brand(17, .bold)); Spacer() }
                .padding(.vertical, 15)
                .background(Brand.moss, in: .rect(cornerRadius: 15))
                .foregroundStyle(.white)
        }
        .accessibilityIdentifier("collect-done")
    }
}
