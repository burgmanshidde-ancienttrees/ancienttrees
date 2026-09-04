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
import Photos
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
    @Environment(Nudge.self) private var nudge
    @Environment(ReviewPrompt.self) private var reviewPrompt
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
        case added(UUID)       // a tree we do not map, just written and sent
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
    /// Whether `origin` is a fix or a fallback. See LocationOff.swift.
    @Environment(\.locationState) private var location
    @State private var camera = false
    @State private var library = false
    /// Which permission the recovery sheet is explaining, nil when it is shut.
    @State private var refused: Permission?
    @State private var fix: Fix = .device
    /// When the photograph was taken, when the photograph says. Nil for the
    /// camera path, where it is now by definition.
    @State private var taken: Date?
    /// The crosshair while the .place stage is up.
    @State private var placing: CLLocationCoordinate2D?
    /// How tall the sheet stands, which is a property of the STEP rather than
    /// of the flow. See presentationDetents below.
    @State private var detent: PresentationDetent = .height(320)
    @State private var shot: UIImage?
    /// Where the shutter actually fell. Held separately from `origin` because
    /// the view can be re-evaluated with a newer fix while the outcome screen
    /// is up, and the record must not quietly move.
    @State private var at: (lat: Double, lng: Double)?
    @State private var why = ""
    @State private var sending = false
    @State private var signingIn = false
    /// Leaving with a photograph in hand asks first. See closeRow.
    @State private var confirmingDiscard = false

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
                CollectIntro(onStart: { openCamera() },
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
                        case .added(let id): addedState(id)
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
        // THE SHEET FITS THE STEP, from 2026-08-28. Hidde, looking at an intro
        // that had shrunk to four lines inside a full-height sheet: "lucht gaan
        // vullen met nodeloze zinnen lijkt me iig geen goed idee, maken ze dan
        // de overlay kleiner idk?" They do, and Apple's guidance is the same:
        // a sheet rests at detents and should fit its content rather than the
        // content being written to fill it.
        //
        // The intro offers both heights rather than only medium, which is
        // HIG's own progressive disclosure: it opens at the smaller one, and
        // somebody running large Dynamic Type can still drag it up rather than
        // meeting clipped text. Every later step is a map, a list or a form,
        // and those want the whole sheet.
        // FITTED, not medium. `.medium` is half the phone whatever is on it,
        // and this step holds a title, a line and two buttons: on a large phone
        // that left a hand's width of empty white between the sentence and the
        // buttons, which reads as something that failed to load rather than as
        // air. Apple's own short action sheets are sized to their content.
        //
        // `.large` stays in the set for the same reason it always did: somebody
        // running large Dynamic Type can drag it up rather than meeting clipped
        // text. Every later step is a map, a list or a form, and those want the
        // whole sheet.
        .presentationDetents(stage == .intro ? [.height(320), .large] : [.large],
                             selection: $detent)
        .onChange(of: stage) { _, now in
            detent = now == .intro ? .height(320) : .large
        }
        .presentationDragIndicator(.visible)
        // AND A SWIPE CANNOT THROW IT AWAY EITHER (Hidde, 2026-08-29: "als ik
        // een boom aan het toevoegen ben met een foto moet ik niet zomaar op
        // vorige knop kunnen klikken en dat je dan alles weg gooit, dan moet
        // daar in ieder geval een waarschuwing komen").
        //
        // Guarding the button alone would leave the bigger hole: this is a
        // sheet, and a sheet goes away when you drag it down, which is easier
        // to do by accident than pressing a cross. Disabling the interactive
        // dismiss while there is a photograph is what iOS gives you for exactly
        // this, and it routes every exit through the one control that asks.
        .interactiveDismissDisabled(hasWork)
        // AN ALERT, NOT A confirmationDialog. iOS 26 draws a
        // confirmationDialog anchored to its control as a popover and silently
        // drops every button carrying role: .cancel, which this app has already
        // shipped once as a destructive question with no way out (2026-08-27).
        // An alert renders every button it is given.
        .alert("Discard this tree?", isPresented: $confirmingDiscard) {
            Button("Cancel", role: .cancel) {}
            Button("Discard", role: .destructive) { dismiss() }
        } message: {
            // Named plainly, because on the camera path the photograph exists
            // nowhere else: it was never written to the camera roll.
            Text("You will lose the photograph and what you have filled in.")
        }
        .fullScreenCover(isPresented: $camera) {
            CameraPicker { resolve($0) }.ignoresSafeArea()
        }
        .sheet(item: $refused) { which in
            // The camera's second button is the route on rather than a refusal,
            // so declining here opens the library and the task still finishes.
            PermissionRecovery(permission: which,
                               onDecline: which == .camera ? { openLibrary() } : nil)
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

    /// Whether there is anything here that closing would throw away.
    ///
    /// The photograph is the whole of it. Everything else on these screens is a
    /// choice that can be made again in seconds; a photograph was taken while
    /// somebody stood under a tree, and on the camera path it exists nowhere
    /// else, not even in their camera roll.
    private var hasWork: Bool {
        if case .intro = stage { return false }
        if case .ticked = stage { return false }
        // Already recorded and sent by the time this stage shows: nothing left
        // for the X button to throw away, same reasoning as .ticked above.
        if case .added = stage { return false }
        return shot != nil
    }

    private var closeRow: some View {
        HStack {
            Spacer()
            Button { if hasWork { confirmingDiscard = true } else { dismiss() } } label: {
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

    /// What a fresh photograph earns: a coordinate we may stand behind, or the
    /// pin-dragging stage.
    enum Route: Equatable {
        case settle(Fix)
        /// We cannot honestly say where this was taken, so we ask.
        case askForThePin
    }

    /// WHERE A PHOTOGRAPH GOES, as a decision rather than as a branch buried in
    /// a SwiftUI view.
    ///
    /// It is pulled out here for the reason CLAUDE.md records about the camera:
    /// when a check cannot run on the machine that tests it, make the DECISION
    /// testable instead of the situation. A simulator cannot deny a real GPS
    /// fix in the middle of a camera flow, which is why the bug below reached a
    /// phone; this function can be asked all four questions anywhere.
    ///
    /// The bug it exists to keep out (found on-device by Hidde, 2026-09-03,
    /// fixed in c4598e78): with location off or refused, `origin` quietly falls
    /// back to the last fix this phone ever had, or to Dam square
    /// (LocationOff.swift), and the camera path recorded that as `.device`,
    /// "GPS, standing at the tree". A confident lie is worse than the honest
    /// gap the library path already has for the same case, and CLAUDE.md calls
    /// a fabricated location the one error a reader cannot forgive, because
    /// they are already standing in the wrong place before any correction
    /// reaches them.
    static func route(cameraShot: Bool,
                      locationKnown: Bool,
                      photoHasCoordinate: Bool) -> Route {
        if cameraShot {
            // Standing there IS the fix, but only when the phone actually has
            // one. Never .device on a fallback.
            return locationKnown ? .settle(.device) : .askForThePin
        }
        // The camera roll. The file's own coordinate beats ours, because it
        // records where the picture was taken rather than where the phone is
        // now; without one we ask, whatever location says.
        return photoHasCoordinate ? .settle(.photo) : .askForThePin
    }

    /// THE CAMERA PATH. You are standing there, so the device fix is the
    /// answer and there is nothing to ask, unless the phone cannot tell us
    /// where that is. See `route(cameraShot:locationKnown:photoHasCoordinate:)`.
    private func resolve(_ image: UIImage?) {
        guard let image else { return }
        taken = nil
        switch Self.route(cameraShot: true,
                          locationKnown: location.known,
                          photoHasCoordinate: false) {
        case .settle(let fix):
            settle(image, at: origin, fix: fix)
        case .askForThePin:
            shot = image
            placing = .init(latitude: origin.lat, longitude: origin.lng)
            withAnimation(.snappy) { stage = .place }
        }
    }

    /// THE CAMERA ROLL PATH. The photograph usually knows where it was taken;
    /// when it does not we ask, and asking is a map rather than a text box.
    private func picked(_ p: LibraryPicker.Picked?) {
        guard let p else { return }
        shot = p.image
        taken = p.taken
        let route = Self.route(cameraShot: false,
                               locationKnown: location.known,
                               photoHasCoordinate: p.coordinate != nil)
        // The binding rather than a force unwrap: `route` only says settle when
        // there IS a coordinate, and a crash is a poor way to find out that
        // stopped being true.
        if case .settle(let fix) = route, let c = p.coordinate {
            settle(p.image, at: (c.latitude, c.longitude), fix: fix)
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

    /// The camera button, which no longer decides in silence.
    ///
    /// Refused raises the explanation; anything else presents the picker, and
    /// notDetermined is deliberately in that second group because presenting is
    /// what triggers the system prompt, and that prompt is the right place to
    /// ask somebody who has just tapped photograph a tree.
    /// A candidate in the "which of these is it" list. Pure, because the state
    /// that matters (no photo coordinate AND no fix) cannot be produced on a
    /// simulator, which always has one or the other.
    static func candidateLabel(species: String, metres: Int?) -> String {
        guard let metres else { return species }
        return "\(species) · \(metres) m"
    }

    /// Why we are asking where the tree stands. Pure, so both branches are
    /// testable on a machine with no photo library to refuse.
    static func placeReason(libraryRefused: Bool) -> String {
        libraryRefused
            ? "We cannot read where your photograph was taken, so drag the map until the pin sits on the tree. Allowing photos would place it for you."
            : "Your photograph does not say where it was taken, so drag the map until the pin sits on the tree."
    }

    private func openCamera() {
        if CameraPicker.isRefused { refused = .camera } else { camera = true }
    }

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
        let isNewTick = !saved.isVisited(t.id)
        if isNewTick { saved.toggleVisited(t.id) }
        sightings.record(treeId: t.id, name: t.name, lat: t.lat, lng: t.lng,
                         image: image, date: taken ?? Date())
        withAnimation(.snappy) { stage = .ticked(t.id) }
        // "You found \(t.name)" below is the payoff moment; see
        // ReviewPrompt.swift and CONVENTIONS.md for why the native ask may
        // fall here. A tree ticked off is a tree seen, and the strongest
        // kind, so it counts toward the same three. The delay lets the
        // payoff card actually land before the system prompt can cover it:
        // asking AT the moment of success, rather than simultaneously with
        // the animation that reveals it, per Apple's own guidance.
        if isNewTick {
            reviewPrompt.saw(t.id)
            Task {
                try? await Task.sleep(for: .seconds(2))
                reviewPrompt.consider()
            }
        }
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
                // TWO DIFFERENT REASONS, and they must not share a sentence.
                // A screenshot genuinely carries no location; a refused library
                // means we were not allowed to read the one it has. The second
                // person can act on that and the first cannot, so telling them
                // both the same thing wastes the only fixable case.
                Text(Self.placeReason(libraryRefused:
                        PHPhotoLibrary.authorizationStatus(for: .readWrite) == .denied
                        || PHPhotoLibrary.authorizationStatus(for: .readWrite) == .restricted))
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
                // The metres are real when `at` is real: a photograph's own
                // coordinate survives a refused location perfectly well, and
                // the shutter's fix does too. They are invented only when both
                // are missing and `origin` has fallen back to Dam square, and
                // then the species alone is the honest label.
                Text(Self.candidateLabel(species: t.commonName,
                                         metres: (at != nil || location.known)
                                             ? Int(Geo.km(at ?? origin, (t.lat, t.lng)) * 1000)
                                             : nil))
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
            TreePhoto(url: url) { Brand.surfaceMuted }
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
            // The same sentence as the submit screen, and it belongs here for
            // the same reason: Hidde's ruling covers a tree we ALREADY map, so
            // a photograph taken on this screen can end up on that tree's page
            // when the page has none or this one is better. Somebody who is
            // told that only on the other screen has not been told.
            Text("Your photograph can appear on the tree's page.")
                .font(.footnote)
                .foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
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
                        Button("Retake") { openCamera() }
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
                // THIS SENTENCE HAS BEEN WRONG TWICE, in opposite directions.
                // Until 08-28 it said the photograph never leaves the phone,
                // which stopped being true the day SightingSync landed. Then it
                // said nobody else sees it, which was true of the code and
                // false of the intention, on the one screen where somebody
                // hands us a photograph FOR the map. Hidde, 2026-09-02: "het
                // hele idee is dat als mensen fotos indienen dat hij potentieel
                // voor het grote publiek word gebruikt", and "ook als de boom
                // er al is en geen foto heeft of de foto van de gebruiker is
                // beter gaan we die gebruiken."
                //
                // So it says what we may actually do, at the moment somebody
                // decides to send it, which is the only moment consent means
                // anything. No toggle beside it, per his 2026-08-24 ruling that
                // the reader should not carry a choice that is ours.
                //
                // NO NAME, AND NOT A WORD ABOUT DELETING AN ACCOUNT (Hidde,
                // 2026-09-04: "hier staat veel te veel tekst, begin hier niet
                // over delete account, en laten we niet mensen hun naam noemen,
                // laten we alleen hun fotos gebruiken als ze goed zijn, het kan
                // mensen afschrikken als hun naam erbij staat").
                //
                // This retires the credit half of the 2026-09-02 decision: a
                // photograph somebody sends is published without a name on it.
                // The deletion sentence went with it, because it only existed
                // to explain what happens to a name that will now never be
                // there, and it raised losing your account at the moment
                // somebody is deciding to give us something.
                Text("Your photograph can appear on the tree's page. We read every word you send.")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
            }

            // THE PRIVATE LINK, said before the tap rather than only after it
            // (Hidde, 2026-09-03: sharing is now on from the moment a tree is
            // added, so somebody can open theirs from the thank-you mail
            // without a separate step). Consent belongs at the moment it is
            // decided, the same reasoning as the sentence above, not buried in
            // a menu item three screens later.
            HStack(spacing: 8) {
                Image(systemName: "link")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                Text("We also make a private page for it that only somebody with the link can open. You can turn that off any time.")
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

    /// ADDING A TREE NEEDS AN ACCOUNT (Hidde, 2026-08-29, asked directly:
    /// "nee, inloggen verplicht"). It is the rule he set for the thumbs on
    /// 2026-08-21 and for the heart and this camera on 2026-08-25, now true of
    /// the write as well as of the two buttons in front of it.
    ///
    /// This used to read "Yours and nobody else's: no network, no account, no
    /// waiting", and a tree written that way belonged to nobody: no server had
    /// it, so signing out could not take it off the phone without destroying
    /// the only copy in the world, and anybody holding the phone could delete
    /// it. That is the hole he found. See Sightings.forgetLocally().
    ///
    /// The guard is here and not only on the buttons because a third way into
    /// this sheet is one afternoon away, and a rule enforced at two call sites
    /// is a rule that leaks at the third. Both current callers check first, so
    /// in practice this never fires.
    private func keepMine() {
        guard account.isSignedIn else {
            nudge.require(.general)
            return
        }
        let here = at ?? origin
        let s = sightings.record(treeId: nil,
                                 name: why.isEmpty ? "A tree I found" : String(why.prefix(60)),
                                 note: why, lat: here.lat, lng: here.lng, image: shot,
                                 date: taken ?? Date())
        shot = nil
        // The payoff beat this path was missing (Hidde, 2026-09-03: "ik mis
        // ook een vink bevestiging na het nemen van de foto dat de tree is
        // toegevoegd"). tickedState already gives the matched-tree path a
        // checkmark and a sentence; this path went straight to the tree's own
        // page with nothing in between, so the moment somebody presses "Add
        // this tree" had no answer of its own. addedState is that answer, and
        // the trip to the tree's page happens when they press its own button.
        withAnimation(.snappy) { stage = .added(s.id) }
        // And it reaches us on its own, with no second step to remember. The
        // queue-until-sign-in branch that used to be here is gone with the
        // signed-out route that created it.
        Task { await transmit(s.id) }
    }

    /// The payoff for a tree we did not already have. Mirrors tickedState:
    /// same icon, same shape, because both answer the same question (did
    /// this work?) and a reader should not have to learn two answers to it.
    private func addedState(_ id: UUID) -> some View {
        VStack(alignment: .leading, spacing: 14) {
            Image(systemName: "checkmark.seal.fill")
                .font(.system(size: 44))
                .foregroundStyle(Brand.moss)
            Text("You added it")
                .font(.brand(24, .heavy))
                .foregroundStyle(Brand.ink)
            Text("It is in your trees now, with your photograph.")
                .font(.subheadline)
                .foregroundStyle(Brand.inkSoft)
            Text("Your photograph can appear on the tree's page. We read every word you send.")
                .font(.footnote)
                .foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
            Button {
                dismiss()
                // Straight to the tree you just made, because that is where
                // you finish the job: the same page ours get, with the fields
                // you have not filled in yet open (Hidde, 2026-08-24: "als ik
                // uit die flow kom van toegevoegde boom wil ik eindigen op de
                // diepere boompagina van de boom die ik net heb gemaakt").
                navigator.push = .mine(id)
            } label: {
                HStack { Spacer(); Text("See it").font(.brand(17, .bold)); Spacer() }
                    .padding(.vertical, 15)
                    .background(Brand.moss, in: .rect(cornerRadius: 15))
                    .foregroundStyle(.white)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("collect-added-done")
        }
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
        // The sighting's own id, so the thank-you mail can link straight to
        // its unlisted page instead of printing the raw coordinate below.
        // Nothing else in `tree` for a kind:tree row ever looks like a uuid,
        // so contributor_reply.py tells the two shapes apart on sight.
        d.tree = id.uuidString
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
