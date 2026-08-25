// Moving a pin, on the map, with a finger.
//
// Hidde, 2026-08-25: "help us place this tree opens a form, but i guess the
// easiest would be if you open the map and let someone drop / move a pin." He is
// right, and it is the one field this project cannot afford to get wrong: the
// old flow asked somebody standing at the tree to describe a position in a text
// box, which is a coordinate laundered through two translations, ours and
// theirs.
//
// THE PIN DOES NOT MOVE, THE MAP DOES. Google Maps' "Move map to adjust" and
// Airbnb's location step both work this way and for the same reason: dragging a
// marker means your thumb covers the thing you are aiming at, while panning the
// map underneath a fixed crosshair leaves the target visible the whole time. The
// convention is the one to copy here rather than the literal words "drop a pin".
//
// It sends a correction through the channel that already exists: kind
// `correction`, the coordinate in `location_hint`, no new table and no new
// column. A run reads it at rung 1 and moves the pin, or writes down why not.
//
// AND THE OTHER SURFACE: the website's contribute form keeps its "where exactly"
// text field for now. A map picker there is MapLibre GL JS and a draggable
// marker, which is a bigger piece of work than this one; when that form is next
// opened up, this is the pattern to port, not the text box.
import SwiftUI
import MapKit

struct PlacePin: View {
    let tree: Tree
    let catalogue: Catalogue

    @Environment(Account.self) private var account
    @Environment(\.dismiss) private var dismiss
    @State private var region: MKCoordinateRegion?
    @State private var sending = false
    @State private var sent = false
    @State private var failed = false
    @State private var signingIn = false

    /// Where the crosshair is: the middle of the map, which is the middle of the
    /// screen, which is what the pin drawn on top of it marks.
    private var here: CLLocationCoordinate2D {
        region?.center ?? .init(latitude: tree.lat, longitude: tree.lng)
    }

    /// How far they have moved it, so the button can say something true.
    private var movedMetres: Int {
        Int(Geo.km((tree.lat, tree.lng), (here.latitude, here.longitude)) * 1000)
    }

    var body: some View {
        NavigationStack {
            ZStack {
                TreeMap(trees: [tree],
                        focus: .init(latitude: tree.lat, longitude: tree.lng),
                        // The street, not the district: somebody is telling us
                        // which trunk, and at four kilometres a trunk is a dot.
                        spanMeters: 300,
                        clusters: false,
                        region: $region,
                        selected: .constant(nil))
                    .ignoresSafeArea(edges: .bottom)

                crosshair
                bar
            }
            .navigationTitle(sent ? "Thank you" : "Where is it really?")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button(sent ? "Done" : "Cancel") { dismiss() }
                }
            }
            .sheet(isPresented: $signingIn) {
                SignInSheet(reason: .feedback, localCount: 0)
            }
        }
    }

    /// Dead centre, and it hangs from its point like a map pin rather than
    /// sitting on it, so the tip marks the spot and not the middle of a circle.
    private var crosshair: some View {
        VStack(spacing: 0) {
            Image(systemName: "mappin")
                .font(.system(size: 34, weight: .semibold))
                .foregroundStyle(Brand.moss)
                .shadow(color: .black.opacity(0.25), radius: 3, y: 1)
            // The point itself, so there is no doubt which pixel is meant.
            Circle()
                .fill(Brand.moss)
                .frame(width: 6, height: 6)
                .shadow(color: .black.opacity(0.3), radius: 2)
        }
        .offset(y: -20)
        .allowsHitTesting(false)
    }

    @ViewBuilder private var bar: some View {
        VStack {
            Spacer()
            VStack(alignment: .leading, spacing: 10) {
                if sent {
                    Label("We will check it and move the pin.", systemImage: "checkmark.seal.fill")
                        .font(.subheadline.weight(.semibold))
                        .foregroundStyle(Brand.ink)
                } else {
                    Text("Drag the map until the pin sits on the tree.")
                        .font(.subheadline).foregroundStyle(Brand.ink)
                    Text(movedMetres < 5
                         ? "Zoom in as far as you like. The button wakes up once you have moved it."
                         : "That is \(movedMetres) m from where we have it.")
                        .font(.caption).foregroundStyle(Brand.inkSoft)
                    Button {
                        guard account.isSignedIn else { signingIn = true; return }
                        send()
                    } label: {
                        HStack {
                            if sending { ProgressView().tint(.white).padding(.trailing, 6) }
                            Text(sending ? "Sending" : "The tree is here")
                        }
                        .font(.brand(16, .bold))
                        .frame(maxWidth: .infinity).frame(height: 48)
                        .background(Brand.moss, in: .capsule)
                        .foregroundStyle(.white)
                    }
                    .buttonStyle(.plain)
                    .disabled(sending || movedMetres < 5)
                    .accessibilityIdentifier("place-pin-send")
                    if failed {
                        Text("That did not go through. Try again in a moment.")
                            .font(.caption).foregroundStyle(.red)
                    }
                    if !account.isSignedIn {
                        Text("Sending needs a free account, so we can tell you what your correction changed.")
                            .font(.caption2).foregroundStyle(Brand.inkSoft)
                    }
                }
            }
            .padding(16)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(Brand.surface, in: .rect(cornerRadius: 18))
            .padding(.horizontal, 16)
            .padding(.bottom, 16)
        }
    }

    private func send() {
        var d = Submission.Draft()
        d.kind = .correction
        d.city = tree.city
        d.tree = tree.name
        // Six decimals is about 10 cm, which is more than anybody needs and
        // costs nothing; a run pastes this straight into the tree's location.
        d.locationHint = String(format: "%.6f, %.6f", here.latitude, here.longitude)
        d.why = "Moved the pin on the map, \(movedMetres) m from the published "
              + "position. Our pin was \(tree.precision == .confirmed ? "marked confirmed" : "marked approximate")."
        Task {
            sending = true
            let ok = await Submission.send(d, from: tree.url,
                                           token: account.session?.accessToken)
            sending = false
            if ok { sent = true } else { failed = true }
        }
    }
}
