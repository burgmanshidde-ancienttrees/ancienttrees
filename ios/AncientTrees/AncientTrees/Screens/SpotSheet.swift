// The centre button's sheet: you are standing before a tree.
//
// One screen, both outcomes, GPS only orders them (DECISIONS.md 2026-08-20
// evening): trees we map within reach are there to tick off, and beneath them,
// always, the second way in: a tree we miss can be sent in. The button never
// has a dead state, because anywhere on earth one of the two applies. That is
// the Untappd shape (check in, with "add a new one" always at the end of the
// list) and it is what makes one label teach both verbs.
//
// The submission reuses the website's own channel (Submission.send, kind
// .tree): no new fields, no name asked, verification happens before anything
// goes live, exactly as Step 0b runs it for the site.

import SwiftUI

struct SpotSheet: View {
    /// The two jobs that used to share one button and one name, which is what
    /// made both of them fuzzy (Hidde, 2026-08-22). COLLECT claims a tree we
    /// already map and belongs with your collection; ADD contributes a tree we
    /// do not have and belongs in the centre of the bar.
    enum Mode: String { case collect, add }

    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    var mode: Mode = .add
    @Environment(Saved.self) private var saved
    @Environment(Sightings.self) private var sightings
    @Environment(Account.self) private var account
    @Environment(\.dismiss) private var dismiss
    @State private var adding = false
    /// The sheet opens on the EXPLANATION, not on a list. Somebody who has
    /// used it once taps straight past; somebody who has not gets told what
    /// the button is for.
    @State private var intro = true
    @State private var why = ""
    @State private var sending = false
    @State private var sent: Bool?
    @State private var ticked: Tree?
    @State private var signingIn = false
    @State private var camera = false
    /// The tree the camera is being opened FOR. nil means a tree we do not map.
    @State private var shooting: Tree?
    @State private var shot: UIImage?

    /// The split the whole sheet stands on: what is close enough to be the
    /// tree the person is standing before. 400 metres is deliberately wide,
    /// because GPS under a canopy is bad and a short list beats a wrong no.
    static func nearby(origin: (lat: Double, lng: Double), trees: [Tree]) -> [Tree] {
        trees
            .map { ($0, Geo.km(origin, ($0.lat, $0.lng))) }
            .filter { $0.1 <= 0.4 }
            .sorted { $0.1 < $1.1 }
            .prefix(5)
            .map(\.0)
    }

    private var nearbyTrees: [Tree] { Self.nearby(origin: origin, trees: catalogue.trees) }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
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
                .padding(.bottom, -26)
                if let t = ticked {
                    tickedState(t)
                } else if sent == true {
                    sentState
                } else if intro && mode == .add {
                    AddIntro(onStart: { intro = false; adding = true })
                } else if mode == .collect && !adding {
                    if nearbyTrees.isEmpty { noTreeNearby } else { tickList }
                } else if adding || nearbyTrees.isEmpty {
                    addForm
                } else {
                    tickList
                }
            }
            .padding(20)
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .brandGround()
        .accessibilityElement(children: .contain)
        .accessibilityIdentifier("spot-sheet")
        .presentationDetents([.large])
        .presentationDragIndicator(.visible)
        .fullScreenCover(isPresented: $camera) {
            CameraPicker { keep($0) }.ignoresSafeArea()
        }
        .sheet(isPresented: $signingIn) {
            SignInSheet(reason: .feedback, localCount: saved.savedCount)
        }
    }

    // MARK: - Tick a tree we map

    /// Standing somewhere we map nothing at all. Collecting needs one of our
    /// trees in front of you, so this says so and points at the other verb
    /// rather than quietly turning into it.
    private var noTreeNearby: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text("No tree of ours within reach")
                .font(.brand(24, .heavy)).foregroundStyle(Brand.ink)
            Text("Collecting means standing in front of a tree we map. There is none near you right now.")
                .font(.body).foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
            Button { adding = true } label: {
                HStack { Spacer()
                    Label("Add a tree we are missing", systemImage: "plus")
                        .font(.brand(16, .bold))
                    Spacer() }
                    .padding(.vertical, 13)
                    .background(Brand.surfaceMuted, in: .rect(cornerRadius: 15))
                    .foregroundStyle(Brand.ink)
            }
            .buttonStyle(.plain)
        }
    }

    private var tickList: some View {
        Group {
            Text("Which tree are you at?")
                .font(.brand(24, .heavy))
                .foregroundStyle(Brand.ink)
            ForEach(nearbyTrees) { t in
                Button { collect(t) } label: { row(t) }
                    .buttonStyle(.plain)
            }
            Divider().padding(.vertical, 4)
            Button { adding = true } label: {
                HStack(spacing: 10) {
                    Image(systemName: "plus.circle.fill")
                        .font(.system(size: 22))
                        .foregroundStyle(Brand.moss)
                    VStack(alignment: .leading, spacing: 2) {
                        Text("A tree we do not have?")
                            .font(.brand(16, .bold))
                            .foregroundStyle(Brand.ink)
                        Text("Photograph it and it is yours. Offer it and we will look.")
                            .font(.footnote)
                            .foregroundStyle(Brand.inkSoft)
                    }
                }
                // Two lines of text are 36 points; the finger gets 44.
                .frame(minHeight: 44)
                .contentShape(.rect)
            }
            .buttonStyle(.plain)
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
                Text("\(t.commonName) · \(Int(Geo.km(origin, (t.lat, t.lng)) * 1000)) m")
                    .font(.footnote)
                    .foregroundStyle(Brand.inkSoft)
            }
            Spacer()
            Image(systemName: saved.isVisited(t.id) ? "checkmark.circle.fill" : "camera")
                .font(.system(size: 24))
                .foregroundStyle(Brand.moss)
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

    /// Collecting one of ours: photograph it, and the photograph IS the
    /// record. A tap could be done from the sofa; standing there with a camera
    /// could not (Hidde, 2026-08-21).
    private func collect(_ t: Tree) {
        shooting = t
        camera = true
    }

    private func keep(_ image: UIImage?) {
        guard let image else { return }
        if let t = shooting {
            if !saved.isVisited(t.id) { saved.toggleVisited(t.id) }
            sightings.record(treeId: t.id, name: t.name,
                             lat: t.lat, lng: t.lng, image: image)
            withAnimation(.snappy) { ticked = t }
        } else {
            shot = image
        }
        shooting = nil
    }

    private func tickedState(_ t: Tree) -> some View {
        VStack(alignment: .leading, spacing: 14) {
            Image(systemName: "checkmark.seal.fill")
                .font(.system(size: 44))
                .foregroundStyle(Brand.moss)
            Text("That one is yours")
                .font(.brand(24, .heavy))
                .foregroundStyle(Brand.ink)
            Text("\(t.name) is in your collection, with your photograph.")
                .font(.body)
                .foregroundStyle(Brand.inkSoft)
            doneButton
        }
    }

    // MARK: - Add a tree we miss

    private var addForm: some View {
        Group {
            Text(nearbyTrees.isEmpty ? "No tree of ours here" : "A tree we do not have")
                .font(.brand(24, .heavy))
                .foregroundStyle(Brand.ink)
            Text("Photograph it and it joins your own trees. Tell us about it and we will look at it for the map.")
                .font(.body)
                .foregroundStyle(Brand.inkSoft)

            // The photograph FIRST, because it is the thing you are here to
            // do and the thing that keeps the tree yours even if we never
            // take it.
            Button { shooting = nil; camera = true } label: {
                if let shot {
                    Image(uiImage: shot)
                        .resizable().aspectRatio(contentMode: .fill)
                        .frame(height: 170).frame(maxWidth: .infinity)
                        .clipShape(.rect(cornerRadius: 14))
                        .overlay(alignment: .bottomTrailing) {
                            Text("Retake").font(.caption.weight(.semibold))
                                .foregroundStyle(.white)
                                .padding(.horizontal, 10).padding(.vertical, 6)
                                .background(.black.opacity(0.45), in: .capsule)
                                .padding(10)
                        }
                } else {
                    VStack(spacing: 8) {
                        Image(systemName: "camera").font(.system(size: 26))
                            .foregroundStyle(Brand.moss)
                        Text("Photograph the tree")
                            .font(.brand(16, .bold)).foregroundStyle(Brand.moss)
                        Text("Trunk and crown in the frame helps us most, if you can manage it")
                            .font(.caption2).foregroundStyle(Brand.inkSoft)
                    }
                    .frame(height: 170).frame(maxWidth: .infinity)
                    .background(Brand.surface, in: .rect(cornerRadius: 14))
                    .overlay {
                        RoundedRectangle(cornerRadius: 14)
                            .strokeBorder(Brand.hairline, style: StrokeStyle(lineWidth: 1.5, dash: [6, 5]))
                    }
                }
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("spot-camera")

            TextField("What makes it special? A name, a species, a story…",
                      text: $why, axis: .vertical)
                .lineLimit(3...6)
                .padding(13)
                .background(Brand.surfaceMuted, in: .rect(cornerRadius: 14))

            HStack(spacing: 8) {
                Image(systemName: "lock")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                Text("Your photograph stays on your phone and in your collection. Offering it is a separate choice.")
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
            .disabled(shot == nil)
            .opacity(shot == nil ? 0.45 : 1)

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

            if sent == false {
                Text("That did not send, so it is kept as yours for now. Try offering it again later.")
                    .font(.footnote)
                    .foregroundStyle(Brand.inkSoft)
            }
        }
    }

    /// Yours and nobody else's: no network, no account, no waiting.
    private func keepMine() {
        sightings.record(treeId: nil,
                         name: why.isEmpty ? "A tree I found" : String(why.prefix(60)),
                         note: why, lat: origin.lat, lng: origin.lng, image: shot)
        shot = nil
        dismiss()
    }

    private func send() async {
        sending = true
        var d = Submission.Draft()
        d.kind = .tree
        d.why = why
        d.locationHint = String(format: "%.5f, %.5f (GPS)", origin.lat, origin.lng)
        d.city = nearbyCityName ?? ""
        let ok = await Submission.send(d, from: "app:spot",
                                       token: account.session?.accessToken)
        // Kept either way. A failed send is a network problem, not a reason to
        // lose somebody's photograph.
        sightings.record(treeId: nil,
                         name: why.isEmpty ? "A tree I found" : String(why.prefix(60)),
                         note: why, lat: origin.lat, lng: origin.lng, image: shot,
                         status: ok ? .sent : .mine)
        shot = nil
        sending = false
        withAnimation(.snappy) { sent = ok }
    }

    /// Best guess at which of our cities the person is in, for the triage
    /// queue only; empty when nowhere near one.
    private var nearbyCityName: String? {
        catalogue.trees
            .map { ($0, $0.distanceKm(from: origin.lat, origin.lng)) }
            .min { $0.1 < $1.1 }
            .flatMap { $0.1 <= 30 ? $0.0.city : nil }
    }

    private var sentState: some View {
        VStack(alignment: .leading, spacing: 14) {
            Image(systemName: "paperplane.fill")
                .font(.system(size: 40))
                .foregroundStyle(Brand.moss)
            Text("Sent. Thank you.")
                .font(.brand(24, .heavy))
                .foregroundStyle(Brand.ink)
            Text("It is in your collection already. We check every tree before it goes on our map, and you will see where it stands under Collect.")
                .font(.body)
                .foregroundStyle(Brand.inkSoft)
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
    }
}
