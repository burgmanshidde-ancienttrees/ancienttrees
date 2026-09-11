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
    /// The tree somebody tapped the camera on, when there is one. Only the
    /// intro screen reads it: see CollectIntro.
    var about: String? = nil

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
        case unsure            // one of ours, and they could not say which
        case compare(String)   // looking at one candidate before committing
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
    /// What the tree is called, or what kind it is. Its OWN field since
    /// 2026-09-08; see the two-field note over the form below.
    @State private var callsIt = ""
    /// How many adult hugs around the trunk is, when they answered. See the
    /// note over HugRow at the bottom of this file.
    @State private var hugs: String?
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
        // AND OUR OWN PIN HAS TO BE WORTH MEASURING AGAINST (2026-09-07).
        // Both tests above measure a distance to a coordinate, and an
        // approximate coordinate means we know the park and not the trunk, so
        // the arithmetic is being done against a number that was never a
        // claim about where the tree stands. Hidde, testing in Nara: "the pin
        // was approximate, did I find it?" He photographed a cedar at
        // Nigatsu-do, where three Japanese cedars sit within 200 metres and
        // all three pins are approximate; nothing in this function could have
        // told him, and it would happily have ticked one off for him.
        //
        // So an approximate pin never claims a tree silently. It asks, which
        // is the honest thing and also the useful one: the answer is worth
        // more to us than the tick is to anybody.
        guard first.0.precision == .confirmed else { return nil }
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
                CollectIntro(about: about,
                             onStart: { openCamera() },
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
                        case .unsure: unsureState
                        case .compare(let id):
                            if let t = catalogue.tree(id) { compareState(t) }
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
            if Launch.collectCompare, let t = Self.nearby(origin: origin,
                                                          trees: catalogue.trees).first {
                at = origin
                shot = UIGraphicsImageRenderer(size: .init(width: 1, height: 1))
                    .image { _ in }
                stage = .compare(t.id)
                return
            }
            if Launch.collectTicked, let t = Self.nearby(origin: origin,
                                                         trees: catalogue.trees).first {
                at = origin
                shot = UIGraphicsImageRenderer(size: .init(width: 1, height: 1))
                    .image { _ in }
                stage = .ticked(t.id)
                return
            }
            if Launch.collectDescribe {
                at = origin
                shot = UIGraphicsImageRenderer(size: .init(width: 1, height: 1))
                    .image { _ in }
                stage = .describe
                return
            }
            if Launch.collectIdentify {
                // A one-pixel stand-in for the photograph, because every
                // action on this screen needs one and a simulator has no
                // camera. Nothing draws it: the screen shows the candidates.
                at = origin
                shot = UIGraphicsImageRenderer(size: .init(width: 1, height: 1))
                    .image { _ in }
                stage = .identify
                return
            }
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
        if case .unsure = stage { return false }
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
    static func candidateLabel(species: String, metres: Int?, direction: String = "") -> String {
        guard let metres else { return species }
        // The direction is what turns a distance into an instruction. "40 m"
        // between two limes tells you nothing you did not already know; "40 m
        // north-east" tells you which one to walk to.
        let d = direction.isEmpty ? "" : " \(direction)"
        return "\(species) · \(metres) m\(d)"
    }

    /// Eight compass points, in words.
    ///
    /// Convention: AllTrails, Google Maps and Komoot all print a compass WORD
    /// rather than a bearing in degrees, and eight points rather than sixteen.
    /// Somebody standing between two trees can act on "north-east" and cannot
    /// act on "north-north-east" or on 37 degrees.
    ///
    /// Empty when the two points are the same, which is what a hand-placed pin
    /// dropped exactly on a tree gives.
    static func compass(from a: (lat: Double, lng: Double),
                        to b: (lat: Double, lng: Double)) -> String {
        let dLat = b.lat - a.lat
        let dLng = (b.lng - a.lng) * cos((a.lat + b.lat) / 2 * .pi / 180)
        if abs(dLat) < 1e-7 && abs(dLng) < 1e-7 { return "" }
        let deg = (atan2(dLng, dLat) * 180 / .pi + 360)
            .truncatingRemainder(dividingBy: 360)
        let points = ["north", "north-east", "east", "south-east",
                      "south", "south-west", "west", "north-west"]
        return points[Int((deg + 22.5) / 45) % 8]
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
            Text(pickerBlurb)
                .font(.subheadline).foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
            // Said once here rather than repeated on every row: the rows are
            // already carrying a name, a species, a distance, a direction and
            // sometimes four lines telling the tree from its neighbours.
            Text("Tap one to see how to tell it apart.")
                .font(.footnote).foregroundStyle(Brand.inkSoft)
            // Tapping a candidate OPENS it rather than claiming it (Hidde,
            // 2026-09-07, sketching the flow he wanted: "dan als je op de boom
            // klikt dan krijg je uitleg of foto of een exacte pin om te
            // confirmen, en dan kan je zeggen this is the one").
            //
            // It is Merlin's flow, which CONVENTIONS.md recorded this morning:
            // a short list, then you decide by COMPARING against the example
            // photographs and species details, and only then tap "This is my
            // bird!". A list whose rows commit on touch skips the comparing,
            // which is the only part that makes the answer worth anything.
            ForEach(Array(candidates.enumerated()), id: \.element.id) { i, t in
                Button { withAnimation(.snappy) { stage = .compare(t.id) } } label: { row(t) }
                    .buttonStyle(.plain)
                    // Indexed rather than named: a UI test runs in its own
                    // process and cannot know which trees are near the
                    // simulator's fixed location.
                    .accessibilityIdentifier("collect-candidate-\(i)")
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
            Button { notSure() } label: {
                HStack(spacing: 10) {
                    Image(systemName: "questionmark.circle.fill")
                        .font(.system(size: 22)).foregroundStyle(Brand.inkSoft)
                    VStack(alignment: .leading, spacing: 2) {
                        Text("I am not sure which")
                            .font(.brand(16, .bold)).foregroundStyle(Brand.ink)
                        Text("We will work it out from your photograph")
                            .font(.footnote).foregroundStyle(Brand.inkSoft)
                    }
                }
                .frame(minHeight: 44)
                .contentShape(.rect)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("collect-not-sure")
        }
    }

    /// The third answer, and the one the sheet was missing (Hidde, 2026-09-07,
    /// testing in Nara: "its hard to see which tree is what, we need a im not
    /// sure button when chosing").
    ///
    /// Without it the two ways out are both wrong. Picking one is a guess that
    /// puts somebody's photograph on the wrong trunk, which is the error this
    /// project treats as unforgivable everywhere else. "None of these" is
    /// worse: it files a tree we already map as a new one, so a duplicate
    /// enters the database on the strength of somebody being unsure.
    ///
    /// So this claims no tree and ticks nothing off. It keeps the photograph,
    /// sends it with the shortlist we showed, and says who is going to do the
    /// work. Being unsure is a normal state here, not a failure: two limes ten
    /// metres apart is the ordinary case, and the person standing in front of
    /// them is telling us something true.
    private func notSure() {
        guard account.isSignedIn else {
            nudge.require(.general)
            return
        }
        let here = at ?? origin
        let picks = candidates
        let s = sightings.record(treeId: nil,
                                 name: picks.first?.name ?? "A tree I could not place",
                                 lat: here.lat, lng: here.lng, image: shot,
                                 date: taken ?? Date(),
                                 unsureOf: picks.map(\.id))
        shot = nil
        withAnimation(.snappy) { stage = .unsure }
        Task { await reportUnsure(sighting: s.id, among: picks, at: here) }
    }

    /// Reaches us in the same words the website already uses for this, so one
    /// pipeline reads both surfaces: the web's worth-it control has had a
    /// "could not tell which tree" chip since 2026-08-21, and three of the
    /// first four real reports we ever got were exactly that. The shortlist
    /// rides in the text, so whoever looks at the photograph starts from three
    /// named trees rather than from a coordinate.
    private func reportUnsure(sighting: UUID, among picks: [Tree],
                              at here: (lat: Double, lng: Double)) async {
        var d = Submission.Draft()
        d.kind = .correction
        d.tree = sighting.uuidString
        d.city = nearbyCityName ?? ""
        d.locationHint = String(format: "%.5f, %.5f (%@)", here.lat, here.lng, fix.note)
        d.why = "could not tell which tree: "
            + picks.map { "\($0.name) (\($0.id))" }.joined(separator: "; ")
        _ = await Submission.send(d, from: "app:collect-unsure",
                                  token: await account.freshToken())
    }

    /// Same shape as the other two payoffs, and deliberately not a checkmark:
    /// nothing has been ticked off, because nobody has said which tree it was.
    private var unsureState: some View {
        VStack(alignment: .leading, spacing: 14) {
            Image(systemName: "paperplane.circle.fill")
                .font(.system(size: 44))
                .foregroundStyle(Brand.moss)
            Text("Thank you, that helps")
                .font(.brand(24, .heavy))
                .foregroundStyle(Brand.ink)
            Text("We will work out which tree it is from your photograph, and your log will show it once we know.")
                .font(.body)
                .foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
            Text("Trees standing close together catch us out too. Telling us is more useful than a guess.")
                .font(.footnote)
                .foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
            Button { dismiss() } label: {
                HStack { Spacer(); Text("Done").font(.brand(17, .bold)); Spacer() }
                    .padding(.vertical, 15)
                    .background(Brand.moss, in: .rect(cornerRadius: 15))
                    .foregroundStyle(.white)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("collect-unsure-done")
        }
    }

    // MARK: - Is this the one

    /// Everything we hold that could settle it, on one screen, and an honest
    /// line when we hold nothing.
    ///
    /// The three things that can answer "which of these is it" are a
    /// photograph of the tree, a sentence saying what tells it from its
    /// neighbours, and a pin exact enough to walk to. 551 of our trees carry
    /// none of the three, and this screen is where that costs somebody
    /// something, so it says so in plain words rather than showing an empty
    /// space. Hidde's rule, same day: without one of the three it should not
    /// be offered as a thing you can confirm.
    private func compareState(_ t: Tree) -> some View {
        VStack(alignment: .leading, spacing: 14) {
            Text(t.name)
                .font(.brand(24, .heavy)).foregroundStyle(Brand.ink)
                .fixedSize(horizontal: false, vertical: true)
            Text(Self.candidateLabel(species: t.commonName,
                                     metres: (at != nil || location.known)
                                         ? Int(Geo.km(at ?? origin, (t.lat, t.lng)) * 1000)
                                         : nil,
                                     direction: (at != nil || location.known)
                                         ? Self.compass(from: at ?? origin, to: (t.lat, t.lng))
                                         : ""))
                .font(.subheadline).foregroundStyle(Brand.inkSoft)

            // A photograph of OUR tree, as large as the sheet allows, because
            // comparing two pictures is the one check anybody can do standing
            // up. Merlin shows its example photographs at exactly this moment.
            if let p = t.photo, let url = p.full ?? p.card {
                TreePhoto(url: url) { Brand.surfaceMuted }
                    .frame(maxWidth: .infinity)
                    .frame(height: 220)
                    .clipShape(.rect(cornerRadius: 14))
            }

            if !t.howToRecognise.isEmpty {
                VStack(alignment: .leading, spacing: 4) {
                    Text("How do I find it?")
                        .font(.brand(13, .bold)).foregroundStyle(Brand.inkSoft)
                    Text(t.howToRecognise)
                        .font(.body).foregroundStyle(Brand.ink)
                        .fixedSize(horizontal: false, vertical: true)
                }
            }

            if t.precision == .approximate {
                Text("Our pin for this one is rough: it marks the place, not the trunk.")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
            }

            // The honest empty state, and the reason the 551 matter.
            if t.photo == nil && t.howToRecognise.isEmpty && t.precision == .approximate {
                Text("We have no photograph of this one, nothing written down about what tells it from its neighbours, and only a rough pin. We cannot help you be sure, and we would rather say so.")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
            }

            Button {
                if let shot, let at { claim(t, image: shot, at: at) }
            } label: {
                HStack { Spacer(); Text("This is the one").font(.brand(17, .bold)); Spacer() }
                    .padding(.vertical, 15)
                    .background(Brand.moss, in: .rect(cornerRadius: 15))
                    .foregroundStyle(.white)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("collect-this-is-the-one")

            Button("Back to the list") {
                withAnimation(.snappy) { stage = .identify }
            }
            .font(.footnote.weight(.semibold))
            .foregroundStyle(Brand.inkSoft)
            .frame(maxWidth: .infinity, minHeight: 44)
        }
    }

    /// What we say above the list, and it depends on how good OUR pins are.
    ///
    /// When one of the candidates is on an approximate pin, "pick the one in
    /// your photograph" is asking somebody to be certain about something we
    /// were not certain about first. Saying so turns "I am not sure" from
    /// their failure into our honesty, which is what it actually is.
    private var pickerBlurb: String {
        if candidates.contains(where: { $0.precision == .approximate }) {
            return "Our own pin is rough for some of these, so we cannot tell you which is which. Pick one if you know, and say you are not sure if you do not."
        }
        return fix == .device
            ? "You are standing among trees we map. Pick the one in your photograph."
            : "Your photograph was taken near these trees. Pick the one you photographed, or say it is none of them."
    }

    private func row(_ t: Tree) -> some View {
        // Top-aligned, because a recognition line can run to four lines and a
        // centred thumbnail then floats halfway down beside it.
        HStack(alignment: .top, spacing: 12) {
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
                                             : nil,
                                         direction: (at != nil || location.known)
                                             ? Self.compass(from: at ?? origin, to: (t.lat, t.lng))
                                             : ""))
                    .font(.footnote)
                    .foregroundStyle(Brand.inkSoft)
                // The line written for exactly this moment. The website has
                // printed it on the tree page under the same heading this
                // sheet uses, "Which one is it?", and until 2026-09-07 it did
                // not travel to the phone, which is the only place anybody is
                // actually standing between two trees. About a fifth of trees
                // carry one, so this is conditional and stays quiet otherwise.
                if !t.howToRecognise.isEmpty {
                    Text(t.howToRecognise)
                        .font(.footnote)
                        .foregroundStyle(Brand.ink)
                        .multilineTextAlignment(.leading)
                        .fixedSize(horizontal: false, vertical: true)
                } else if t.precision == .approximate {
                    // The metres above are measured from a pin that only ever
                    // claimed the park, and without this line they read as a
                    // precision we do not have. Same rule as the warning
                    // beside the directions button, at the moment it decides
                    // something.
                    Text("Our pin for this one is rough")
                        .font(.footnote)
                        .foregroundStyle(Brand.inkSoft)
                }
            }
            Spacer()
            Image(systemName: "chevron.right")
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(Brand.inkSoft)
                .padding(.top, 20)
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
            if let first = Self.firstOf(tree: t, visited: saved.entries,
                                        trees: catalogue.trees) {
                milestone(first)
            }
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
            // THE ONE MOMENT THIS QUESTION CAN BE ASKED HONESTLY. Somebody is
            // standing in front of a tree we already map, having just found
            // it, which is the only state in the whole product where "was it
            // worth the trip" has a real answer. It sits above Done rather
            // than below it, because a control under the button that ends the
            // screen is a control nobody sees.
            WorthTheTripAsk(tree: t)
            doneButton
            // THE ESCAPE FROM A CONFIDENT MATCH, and it used to be a grey link
            // in the footnote size. Hidde photographed exactly this screen in
            // Nara and said the thing that matters: "deze hele bevestiging is
            // wel heel nice maar dan moet je wel 100% zeker weten of dat m was
            // - ik heb geen idee en ik gok van niet." A page-wide green button
            // saying You Found It, with the doubt hidden underneath it in the
            // smallest type on the screen, is an interface arguing with the
            // person holding it.
            //
            // So it is a bordered control the same size as Done, always shown.
            // Where several trees are near, it reopens the list; where only
            // this one is, being wrong means we do not map the tree at all, so
            // it goes to the form.
            Button {
                if case .ticked(let id) = stage { saved.toggleVisited(id) }
                // DOUBT IS NOT DENIAL, and this line used to treat it as one.
                // With a single candidate near, it sent an unsure person
                // straight to "We do not have this one" and a form asking them
                // to name a new tree, which is how a duplicate of a tree we
                // already map enters the database on the strength of somebody
                // hesitating. It is the same mistake "None of these" makes,
                // arrived at from the other side, and the flow walk caught it
                // on its first run.
                //
                // The list is the honest destination whatever its length: it
                // holds all three answers, including "I am not sure which".
                // Only with nothing of ours near at all is the form right.
                withAnimation(.snappy) {
                    stage = candidates.isEmpty ? .describe : .identify
                }
            } label: {
                HStack { Spacer(); Text("I am not sure it was this one")
                    .font(.brand(16, .bold)); Spacer() }
                    .padding(.vertical, 14)
                    .overlay(RoundedRectangle(cornerRadius: 15)
                        .stroke(Brand.inkSoft.opacity(0.35), lineWidth: 1))
                    .foregroundStyle(Brand.ink)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("collect-not-this-one")
        }
    }

    /// The one line that says this was a FIRST, or nothing at all.
    ///
    /// Two references, and they disagree on purpose (CONVENTIONS.md, 2026-09-07).
    /// Geocaching's First To Find is the most popular unofficial statistic in
    /// the hobby: people travel for it and cache owners leave a gift for
    /// whoever signs first. Ours is rarer and leaves more behind, because
    /// around two thousand of our trees have never been photographed by
    /// anybody and the picture stays there for everyone who comes after.
    ///
    /// Strava is the other half. It gives no personal record for the FIRST
    /// time you ride a segment, because a first has nothing to compare against
    /// and marking it makes the mark meaningless. That decides the case Hidde
    /// raised: "first in your own trees" is every tick you will ever make, so
    /// it is not an event. What IS one is the first of a KIND, which is
    /// Merlin's life list: your first tree at all, your first in this city.
    ///
    /// Ordered hardest-won first, and only one ever shows. "Nobody had
    /// photographed this" is a claim about what we had published when the app
    /// last read the feed, which is why it is past tense.
    static func firstOf(tree t: Tree, visited: [String: Saved.Entry],
                        trees: [Tree]) -> String? {
        let ticked = visited.filter { $0.value.visitedAt != nil }.keys
        if t.photo == nil {
            return "Nobody had photographed this one. Yours is the first."
        }
        if ticked.filter({ $0 != t.id }).isEmpty {
            return "The first tree in your collection."
        }
        let byId = Dictionary(uniqueKeysWithValues: trees.map { ($0.id, $0) })
        let elsewhereInCity = ticked.contains { $0 != t.id && byId[$0]?.citySlug == t.citySlug }
        if !elsewhereInCity && !t.city.isEmpty {
            return "Your first in \(t.city)."
        }
        return nil
    }

    /// A first is marked rather than narrated: one row, the project's own
    /// green, and no exclamation mark doing the work a fact should do.
    private func milestone(_ line: String) -> some View {
        HStack(alignment: .top, spacing: 10) {
            Image(systemName: "rosette")
                .font(.system(size: 18, weight: .semibold))
                .foregroundStyle(Brand.moss)
            Text(line)
                .font(.brand(15, .bold))
                .foregroundStyle(Brand.ink)
                .fixedSize(horizontal: false, vertical: true)
        }
        .padding(12)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Brand.surface, in: .rect(cornerRadius: 14))
    }

    private func subtitle(_ t: Tree) -> String {
        return [t.commonName, Self.agePhrase(t.age)].compactMap { $0 }
            .joined(separator: ", ")
    }

    /// " old" belongs after "roughly 400 years" and nowhere else.
    ///
    /// It was appended to every age string, and 697 of our 2,342 are not bare
    /// quantities: they already say "old", or they are whole sentences with a
    /// comma in them. Hidde's own screenshot from Nara reads "current tree
    /// roughly 60 years old, replanted after 1961 old", which is the payoff
    /// line of the app's best moment ending in nonsense.
    static func agePhrase(_ age: String?) -> String? {
        guard let a = age?.trimmingCharacters(in: .whitespaces), !a.isEmpty else { return nil }
        let lower = a.lowercased()
        if lower.contains("old") || a.contains(",") { return a }
        return "\(a) old"
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

            // TWO FIELDS, NOT ONE, AND THIS IS THE CONVENTION RATHER THAN A
            // REDESIGN. Until 2026-09-08 a single field asked "What makes it
            // special? A name, a species, a story…" and then USED THE SAME TEXT
            // AS THE TREE'S NAME, cut at 60 characters. So writing a real
            // sentence turned your sentence into the title, and writing nothing
            // was rewarded with a tidy-looking "A tree I found". Eight of the
            // first eight photographs came in with the default name and an
            // empty note, seven of them literally empty.
            //
            // Google Maps' "add a missing place" keeps the name as its own
            // required field and never asks why the place is good; the opinion
            // is a review, a separate act, later. iNaturalist's notes field is
            // for context a photograph cannot carry, not for advocacy. Both
            // separate what the thing IS from what you thought of it, and our
            // single field had merged them.
            //
            // So the reason is asked in the reader's own terms, and it stays
            // OPTIONAL: none of the references makes somebody argue for a place
            // before they may add it, and a required justification would turn a
            // thirty-second act into homework.
            //
            // The placeholder is the question and nothing else. The first draft
            // added "Tell somebody else why they should come and see it", which
            // is an order and is the exact habit PRODUCT_COPY.md exists to
            // stop, and it is more words on a screen Hidde has twice said has
            // too many.
            VStack(alignment: .leading, spacing: 10) {
                TextField("What is it called, or what kind of tree?",
                          text: $callsIt)
                    .padding(13)
                    .background(Brand.surfaceMuted, in: .rect(cornerRadius: 14))
                    .accessibilityLabel("What the tree is called, or what kind it is")

                TextField("Why is it worth the walk?",
                          text: $why, axis: .vertical)
                    .lineLimit(3...6)
                    .padding(13)
                    .background(Brand.surfaceMuted, in: .rect(cornerRadius: 14))
                    .accessibilityLabel("Why this tree is worth the walk")
            }

            // HOW THICK, and it is here rather than on a later screen because
            // it is the one fact that can only be answered while standing at
            // the trunk. Hidde, 2026-09-11: "en bij het toevoegen van een boom
            // een nieuw veld - girth".
            //
            // WHY IT EARNS A THIRD FIELD on a form we have twice cut down.
            // Girth is the only measurement an AGE can be derived from rather
            // than invented, which is this project's own rule since 2026-08-16
            // and now a script (scripts/ages.py). Nothing else somebody can
            // give us in five seconds turns into a fact on a page.
            //
            // THE HUG, not centimetres. CONVENTIONS.md, "Asking a contributor
            // how thick a tree is": the Ancient Tree Inventory has run fifteen
            // years of citizen tree recording and hands anybody without a tape
            // the hug, one adult hug being 1.5 m fingertip to fingertip. It is
            // the only measurement available to somebody holding a phone in a
            // park, and it sidesteps the metric-or-imperial question a number
            // would raise. The precision costs nothing either: a hug is good
            // to about 25 cm, a LiDAR scan to 3, and the growth rate makes the
            // derived age a band a factor of two wide whichever you use.
            //
            // OPTIONAL, like both fields above it and for the reason recorded
            // there: none of the references makes somebody fill anything in
            // before they may contribute.
            VStack(alignment: .leading, spacing: 8) {
                Text("How thick is the trunk?")
                    .font(.brand(15, .bold))
                    .foregroundStyle(Brand.ink)
                // THE EXPLANATION SITS ABOVE THE CHIPS, which is not where a
                // footnote normally goes. It is not help after the fact: it
                // defines the unit somebody is about to count in, and a chip
                // saying "2 hugs" means nothing until you have read it. Our own
                // web form does the same, hint between the label and the field
                // (site/src/pages/contribute.astro, "Where does it stand?").
                Text("You can measure it by putting your arms around it. One adult hug is about a metre and a half.")
                    .font(.footnote)
                    .foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
                HugRow(picked: $hugs)
            }

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
        // The name is its own field now, so the note is never silently promoted
        // into a title. "A tree I found" survives only as the last resort, for
        // somebody who fills in neither, and it is honest there: we genuinely
        // do not know what it is called and neither did they.
        let named = callsIt.trimmingCharacters(in: .whitespacesAndNewlines)
        let s = sightings.record(treeId: nil,
                                 name: named.isEmpty ? "A tree I found" : String(named.prefix(60)),
                                 note: why, lat: here.lat, lng: here.lng, image: shot,
                                 date: taken ?? Date(), girth: hugs)
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
            // The two halves said apart, on Hidde's own sketch of the flow
            // (2026-09-07): "it's added, we will do a double check for the
            // platform, but added to your trees already?" Yes, and saying so
            // is the whole point. Your collection is yours the second you
            // press the shutter and nothing we decide later takes it away;
            // whether the tree earns a place on the map is our question, not a
            // condition on theirs. Left unsaid, somebody reasonably assumes
            // their tree is on the map, and hears a later silence as a no.
            Text("We will look at whether it belongs on the map as well. Either way it stays in your trees.")
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

/// Picking how many adult hugs go round a trunk.
///
/// Convention: the Ancient Tree Inventory's hug, the tape-free unit fifteen
/// years of citizen tree recording are built on, one adult hug being 1.5 m
/// fingertip to fingertip. CONVENTIONS.md, "Asking a contributor how thick a
/// tree is", holds the lookup and the sources.
///
/// A WRAPPING ROW OF CHIPS rather than a segmented control, and the difference
/// between the two is the reason rather than the look. A segmented control is
/// for switching between views or modes, its segments are equal width, and
/// Apple asks for five or fewer with short labels; a choice chip is for picking
/// a VALUE out of roughly three to six options, it sizes to its own text, and
/// the row wraps. This is a value, "4+ hugs" and "Less than 1" are not equal
/// width, and five capsules do not fit one line at 375 points.
///
/// The first version used a LazyVGrid with adaptive columns. It wrapped, and it
/// forced every chip to one width, which is a segmented control wearing
/// capsules. FlowRow below is the Layout protocol doing the one thing it is
/// for, since SwiftUI ships no flow container.
///
/// The stored value is terse ("<1", "2", "4+") because it travels to a script
/// rather than to a reader; the label is what the person sees.
private struct HugRow: View {
    @Binding var picked: String?

    /// A struct rather than a labelled tuple because Swift has no key path
    /// into a tuple, so ForEach cannot identify one.
    struct Option: Identifiable {
        /// What gets stored and sent. Terse on purpose: it travels to a script.
        let id: String
        let label: String
    }

    static let options = [
        Option(id: "<1", label: "Less than 1"),
        Option(id: "1", label: "1 hug"),
        Option(id: "2", label: "2 hugs"),
        Option(id: "3", label: "3 hugs"),
        Option(id: "4+", label: "4+ hugs"),
    ]

    var body: some View {
        FlowRow(spacing: 8) {
            ForEach(Self.options) { option in
                let on = picked == option.id
                Button {
                    // Tapping the chosen one clears it, so an answer given by
                    // accident can be taken back. There is no other way out of
                    // a single-choice row, and the field is optional.
                    picked = on ? nil : option.id
                } label: {
                    Text(option.label)
                        .font(.brand(13, .medium, relativeTo: .caption))
                        .foregroundStyle(on ? .white : Brand.ink)
                        .padding(.horizontal, 14)
                        .frame(height: 44)
                        .background(on ? Brand.moss : Brand.surface, in: .capsule)
                        .overlay {
                            if !on { Capsule().strokeBorder(Brand.hairline, lineWidth: 1) }
                        }
                        .contentShape(.rect)
                }
                .buttonStyle(.plain)
                .accessibilityLabel(option.label)
                .accessibilityAddTraits(on ? [.isSelected] : [])
            }
        }
        .accessibilityIdentifier("hug-row")
    }
}

/// Views laid left to right, wrapping onto a new line when the row runs out.
///
/// SwiftUI ships no flow container, and this is the one thing the Layout
/// protocol exists for. Kept here beside its only caller rather than promoted
/// to Kit: one use is not a component, and moving it the day there is a second
/// one costs nothing.
///
/// Each subview is measured unconstrained and placed at the size it asks for,
/// which is what makes a chip hug its own text instead of being stretched to a
/// column's width. A subview wider than the whole row gets its own line and
/// overflows it, which cannot happen here (five short labels) and is the
/// honest behaviour if it ever does: nothing is silently clipped.
struct FlowRow: Layout {
    var spacing: CGFloat = 8

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews,
                      cache: inout ()) -> CGSize {
        let limit = proposal.width ?? .infinity
        var x: CGFloat = 0, height: CGFloat = 0, lineHeight: CGFloat = 0
        for view in subviews {
            let size = view.sizeThatFits(.unspecified)
            if x > 0, x + size.width > limit {
                x = 0
                height += lineHeight + spacing
                lineHeight = 0
            }
            x += size.width + spacing
            lineHeight = max(lineHeight, size.height)
        }
        return CGSize(width: proposal.width ?? max(0, x - spacing),
                      height: height + lineHeight)
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize,
                       subviews: Subviews, cache: inout ()) {
        var x = bounds.minX, y = bounds.minY, lineHeight: CGFloat = 0
        for view in subviews {
            let size = view.sizeThatFits(.unspecified)
            if x > bounds.minX, x + size.width > bounds.maxX {
                x = bounds.minX
                y += lineHeight + spacing
                lineHeight = 0
            }
            view.place(at: CGPoint(x: x, y: y), proposal: ProposedViewSize(size))
            x += size.width + spacing
            lineHeight = max(lineHeight, size.height)
        }
    }
}
