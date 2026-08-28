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
// WHERE THE LOCATION COMES FROM, rewritten 2026-08-28. It used to be
// CoreLocation and nothing else, on the reasoning that a photo taken through
// UIImagePickerController arrives as a bare UIImage with every scrap of
// metadata gone. That is still true of the camera path and is why it still
// uses the live device fix. It stopped being the whole answer when Hidde asked
// the obvious question: "wat als ik een mooie foto op mn fotorol heb staan en
// die boom wil ik toevoegen." A photograph taken last spring must not be filed
// where you are standing now.
//
// So there are three sources and the record says which one it was:
//
//   .device   the phone, at the shutter. The camera path, unchanged.
//   .photo    the photograph's own coordinate, off the PHAsset (LibraryPicker).
//   .placed   put there by hand, on the map, because the photograph did not say.
//
// A photograph with no location is never refused, which is iNaturalist's rule
// and ours: it is incomplete rather than untrustworthy, and a pin somebody
// dragged into place counts exactly as much as one read out of a file.
//
// The submission reuses the website's own channel (Submission.send, kind
// .tree): no new fields, no name asked, verification happens before anything
// goes live, exactly as Step 0b runs it for the site.

import CoreLocation
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
    @Environment(Navigator.self) private var navigator
    @Environment(\.dismiss) private var dismiss

    /// Where the flow is. One enum rather than five booleans, because the old
    /// sheet grew nine of them and two combinations were unreachable.
    private enum Stage: Equatable {
        case intro
        case place             // the photograph does not say where it was taken
        case identify          // photograph taken, more than one candidate
        case ticked(String)    // tree id, matched and claimed
        case describe          // a tree we do not map
    }

    /// Where the coordinate on this record came from. Kept because it changes
    /// what the record is worth: a run reading the submission needs to know
    /// whether it is a device fix, a file's own GPS, or somebody's finger.
    enum Fix: String {
        case device, photo, placed

        var note: String {
            switch self {
            case .device: "GPS, standing at the tree"
            case .photo: "from the photograph's own location"
            case .placed: "placed on the map by hand"
            }
        }
    }

    @State private var stage: Stage = .intro
    @State private var camera = false
    @State private var library = false
    @State private var fix: Fix = .device
    /// When the photograph was taken, when the photograph says. Nil for the
    /// camera path, where it is now by definition.
    @State private var taken: Date?
    /// The crosshair while the .place stage is up.
    @State private var placing: CLLocationCoordinate2D?
    @State private var shot: UIImage?
    /// Where the shutter actually fell. Held separately from `origin` because
    /// the view can be re-evaluated with a newer fix while the outcome screen
    /// is up, and the record must not quietly move.
    @State private var at: (lat: Double, lng: Double)?
    @State private var why = ""
    @State private var sending = false
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
                CollectIntro(onStart: { camera = true },
                             onLibrary: { openLibrary() })
                    .padding(.horizontal, 20)
                    .padding(.bottom, 24)
            } else if stage == .place {
                // A map needs the whole sheet, so this one does not scroll
                // either. Same reason as the intro.
                placeState
            } else {
                ScrollView {
                    VStack(alignment: .leading, spacing: 20) {
                        switch stage {
                        case .ticked(let id): if let t = catalogue.tree(id) { tickedState(t) }
                        case .identify: identifyState
                        case .describe: describeForm
                        case .intro, .place: EmptyView()
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
        .fullScreenCover(isPresented: $library) {
            LibraryPicker { picked($0) }.ignoresSafeArea()
        }
        .sheet(isPresented: $signingIn) {
            SignInSheet(reason: .feedback, localCount: saved.savedCount)
        }
        .task {
            guard Launch.collectPlace else { return }
            placing = .init(latitude: origin.lat, longitude: origin.lng)
            stage = .place
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

    /// THE CAMERA PATH. You are standing there, so the device fix is the
    /// answer and there is nothing to ask.
    private func resolve(_ image: UIImage?) {
        guard let image else { return }
        taken = nil
        settle(image, at: origin, fix: .device)
    }

    /// THE CAMERA ROLL PATH. The photograph usually knows where it was taken;
    /// when it does not we ask, and asking is a map rather than a text box.
    private func picked(_ p: LibraryPicker.Picked?) {
        guard let p else { return }
        shot = p.image
        taken = p.taken
        if let c = p.coordinate {
            settle(p.image, at: (c.latitude, c.longitude), fix: .photo)
        } else {
            placing = .init(latitude: origin.lat, longitude: origin.lng)
            withAnimation(.snappy) { stage = .place }
        }
    }

    /// Photograph first, ask afterwards, and only ask when we genuinely cannot
    /// tell. What counts as "cannot tell" depends on where the coordinate came
    /// from, which is the correction of 2026-08-28.
    private func settle(_ image: UIImage, at here: (lat: Double, lng: Double), fix source: Fix) {
        shot = image
        at = here
        fix = source
        if Self.mayClaimWithoutAsking(source), let t = Self.confident(origin: here, trees: catalogue.trees) {
            claim(t, image: image, at: here)
        } else if Self.nearby(origin: here, trees: catalogue.trees).isEmpty {
            withAnimation(.snappy) { stage = .describe }
        } else {
            withAnimation(.snappy) { stage = .identify }
        }
    }

    /// WHY A PHOTOGRAPH FROM THE CAMERA ROLL IS NEVER CLAIMED WITHOUT ASKING.
    ///
    /// Hidde, within an hour of the camera roll shipping: "ik uploade een foto
    /// die niet die boom was maar wel daar in de buurt stond, hoe werkt dat dan
    /// want dit klopt niet." The app had told him he found the American Oak of
    /// the Pekingtuin, and he had photographed something else standing near it.
    ///
    /// The confident() rule is sound and it is about STANDING THERE: an 80
    /// metre nearest match with the runner-up twice as far is a safe guess when
    /// somebody has just pointed a camera at the thing in front of them. Every
    /// word of that reasoning fails for a picture off the roll. The coordinate
    /// says where the PHOTOGRAPHER stood, which can be a street away from the
    /// subject, and nothing at all says the subject is a tree, let alone one of
    /// ours. It could be a dog in that park.
    ///
    /// Convention, and both references agree: iNaturalist SUGGESTS an
    /// identification on an uploaded photograph and has you confirm it, and
    /// Google Maps asks which place a photograph belongs to. Neither asserts on
    /// your behalf. So the list is shown, "None of these" is always on it, and
    /// the tick is yours to give.
    ///
    /// It also protects the thing the photograph was for. A collection you can
    /// fake is worth nothing, and it is no better when the app fakes it for
    /// you.
    static func mayClaimWithoutAsking(_ source: Fix) -> Bool { source == .device }

    private func openLibrary() {
        Task {
            // The prompt belongs to the tap, so it is asked here rather than
            // inside the picker. Refused is not a dead end: the picker still
            // opens, and we ask where the tree is instead.
            await LibraryPicker.askForLibrary()
            library = true
        }
    }

    private func claim(_ t: Tree, image: UIImage, at here: (lat: Double, lng: Double)) {
        if !saved.isVisited(t.id) { saved.toggleVisited(t.id) }
        sightings.record(treeId: t.id, name: t.name, lat: t.lat, lng: t.lng,
                         image: image, date: taken ?? Date())
        withAnimation(.snappy) { stage = .ticked(t.id) }
    }

    // MARK: - The photograph does not say where it was taken

    /// Not a failure and not an error state. Most photographs that reach a
    /// phone through a messenger have had their location stripped on the way,
    /// and a screenshot never had one. iNaturalist keeps such an observation
    /// and simply asks; the only thing that changes is that we had to ask.
    ///
    /// A map rather than a text box, for the reason PlacePin is a map: a
    /// position described in words is a coordinate laundered through two
    /// translations, ours and theirs.
    private var placeState: some View {
        VStack(alignment: .leading, spacing: 0) {
            VStack(alignment: .leading, spacing: 6) {
                Text("Where does it stand?")
                    .font(.brand(24, .heavy)).foregroundStyle(Brand.ink)
                Text("Your photograph does not say where it was taken, so drag the map until the pin sits on the tree.")
                    .font(.subheadline).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
            }
            .padding(.horizontal, 20)
            .padding(.bottom, 12)

            ZStack(alignment: .bottom) {
                PinPicker(start: placing ?? .init(latitude: origin.lat, longitude: origin.lng),
                          trees: Self.nearby(origin: (placing?.latitude ?? origin.lat,
                                                      placing?.longitude ?? origin.lng),
                                             trees: catalogue.trees),
                          spanMeters: 400,
                          coordinate: Binding(get: { placing ?? .init(latitude: origin.lat,
                                                                     longitude: origin.lng) },
                                              set: { placing = $0 }))

                Button {
                    guard let c = placing, let image = shot else { return }
                    settle(image, at: (c.latitude, c.longitude), fix: .placed)
                } label: {
                    Text("The tree is here")
                        .font(.brand(16, .bold))
                        .frame(maxWidth: .infinity).frame(height: 48)
                        .background(Brand.moss, in: .capsule)
                        .foregroundStyle(.white)
                }
                .buttonStyle(.plain)
                .padding(.horizontal, 20)
                .padding(.bottom, 20)
                .accessibilityIdentifier("collect-place-confirm")
            }
        }
        .accessibilityIdentifier("collect-place")
    }

    // MARK: - Which one is it

    /// Not an error state and not a fallback. Two trees ten metres apart is
    /// the ordinary case in a park, and being asked which one you are looking
    /// at is also the moment we learn something we could not know.
    private var identifyState: some View {
        Group {
            Text("Which one is it?")
                .font(.brand(24, .heavy)).foregroundStyle(Brand.ink)
            Text(fix == .device
                 ? "You are standing among trees we map. Pick the one in your photograph."
                 : "Your photograph was taken near these trees. Pick the one you photographed, or say it is none of them.")
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
        if let p = t.photo, let url = p.card {
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
                Image(systemName: "leaf")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                // NO CHOICE here any more (Hidde, 2026-08-24: "ik denk ook
                // niet dat je mensen de optie moet geven om te kiezen om hem
                // toe te voegen aan de database of niet - hij komt uberhaupt
                // automatisch bij ons terecht of ze het willen of niet en dan
                // kiezen wij of die het waard is"). Two buttons that differed
                // only in whether we were allowed to look at it made the
                // reader carry a decision that is ours, and most people would
                // have taken the one that gave us nothing.
                //
                // The photograph itself still never leaves the phone; what
                // reaches us is the words, through the submissions channel the
                // website has had all along. Uploading pictures is a bucket, a
                // bill and a deletion duty, and that is Hidde's call.
                Text("Your photograph stays on your phone. What you write reaches us, and we decide whether it joins the map everybody sees. Either way it stays yours.")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
            }

            Button { keepMine() } label: {
                HStack { Spacer()
                    if sending { ProgressView().tint(.white) }
                    Label("Add this tree", systemImage: "checkmark")
                        .font(.brand(17, .bold))
                    Spacer() }
                    .padding(.vertical, 15)
                    .background(Brand.moss, in: .rect(cornerRadius: 15))
                    .foregroundStyle(.white)
            }
            .buttonStyle(.plain)
        }
    }

    /// Yours and nobody else's: no network, no account, no waiting.
    private func keepMine() {
        let here = at ?? origin
        let s = sightings.record(treeId: nil,
                                 name: why.isEmpty ? "A tree I found" : String(why.prefix(60)),
                                 note: why, lat: here.lat, lng: here.lng, image: shot,
                                 date: taken ?? Date())
        shot = nil
        dismiss()
        // Straight to the tree you just made, because that is where you finish
        // the job: the same page ours get, with the fields you have not filled
        // in yet open (Hidde, 2026-08-24: "als ik uit die flow kom van
        // toegevoegde boom wil ik eindigen op de diepere boompagina van de boom
        // die ik net heb gemaakt").
        navigator.push = .mine(s.id)
        // And it reaches us on its own. No account, no waiting: a signed-in
        // person's tree goes now, and anybody else's goes the moment they sign
        // in, which is a queue rather than a question.
        if account.isSignedIn { Task { await transmit(s.id) } }
    }

    /// Sends the WORDS, and nothing else.
    ///
    /// It used to record the sighting as well, which was right when offering
    /// was a second button and is a duplicate now that keeping and offering are
    /// one act: keepMine() has already written the tree by the time this runs.
    private func transmit(_ id: UUID) async {
        sending = true
        let here = at ?? origin
        var d = Submission.Draft()
        d.kind = .tree
        d.why = why
        // Say which of the three ways this coordinate arrived. A run reading
        // the submission treats a hand-placed pin differently from a device
        // fix, and until 2026-08-28 this line called all of them GPS.
        d.locationHint = String(format: "%.5f, %.5f (%@)", here.lat, here.lng, fix.note)
        d.city = nearbyCityName ?? ""
        let ok = await Submission.send(d, from: "app:collect",
                                       token: await account.freshToken())
        // A failed send is a network problem and never a reason to lose
        // somebody's tree: it stays yours and stays queued.
        sightings.update(id, status: ok ? .sent : .mine)
        sending = false
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
