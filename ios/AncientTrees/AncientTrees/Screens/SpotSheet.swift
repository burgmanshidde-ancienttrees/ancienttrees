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
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    @Environment(Saved.self) private var saved
    @Environment(\.dismiss) private var dismiss
    @State private var adding = false
    @State private var why = ""
    @State private var sending = false
    @State private var sent: Bool?
    @State private var ticked: Tree?

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
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
    }

    // MARK: - Tick a tree we map

    private var tickList: some View {
        Group {
            Text("Which tree did you find?")
                .font(.brand(24, .heavy))
                .foregroundStyle(Brand.ink)
            ForEach(nearbyTrees) { t in
                Button { tick(t) } label: { row(t) }
                    .buttonStyle(.plain)
            }
            Divider().padding(.vertical, 4)
            Button { adding = true } label: {
                HStack(spacing: 10) {
                    Image(systemName: "plus.circle.fill")
                        .font(.system(size: 22))
                        .foregroundStyle(Brand.moss)
                    VStack(alignment: .leading, spacing: 2) {
                        Text("Standing before a tree we miss?")
                            .font(.brand(16, .bold))
                            .foregroundStyle(Brand.ink)
                        Text("Add it, and we will check it out.")
                            .font(.footnote)
                            .foregroundStyle(Brand.inkSoft)
                    }
                }
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
            Image(systemName: saved.isVisited(t.id) ? "checkmark.circle.fill" : "circle")
                .font(.system(size: 26))
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

    private func tick(_ t: Tree) {
        if !saved.isVisited(t.id) { saved.toggleVisited(t.id) }
        withAnimation(.snappy) { ticked = t }
    }

    private func tickedState(_ t: Tree) -> some View {
        VStack(alignment: .leading, spacing: 14) {
            Image(systemName: "checkmark.seal.fill")
                .font(.system(size: 44))
                .foregroundStyle(Brand.moss)
            Text("That one is yours")
                .font(.brand(24, .heavy))
                .foregroundStyle(Brand.ink)
            Text("\(t.name) is in your collection.")
                .font(.body)
                .foregroundStyle(Brand.inkSoft)
            doneButton
        }
    }

    // MARK: - Add a tree we miss

    private var addForm: some View {
        Group {
            Text(nearbyTrees.isEmpty ? "No tree on our map here" : "A tree we miss")
                .font(.brand(24, .heavy))
                .foregroundStyle(Brand.ink)
            Text("Standing before something remarkable? Tell us. We check every tree before it goes on the map.")
                .font(.body)
                .foregroundStyle(Brand.inkSoft)
            TextField("What makes it special? A name, a species, a story…",
                      text: $why, axis: .vertical)
                .lineLimit(3...6)
                .padding(13)
                .background(Brand.surfaceMuted, in: .rect(cornerRadius: 14))
            HStack(spacing: 8) {
                Image(systemName: "location.fill")
                    .font(.footnote)
                    .foregroundStyle(Brand.inkSoft)
                Text("Your location rides along, so we know which tree.")
                    .font(.footnote)
                    .foregroundStyle(Brand.inkSoft)
            }
            Button { Task { await send() } } label: {
                HStack {
                    Spacer()
                    if sending { ProgressView().tint(.white) }
                    Text("Send it in").font(.brand(17, .bold))
                    Spacer()
                }
                .padding(.vertical, 15)
                .background(Brand.moss, in: .rect(cornerRadius: 15))
                .foregroundStyle(.white)
            }
            .disabled(sending || why.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
            if sent == false {
                Text("That did not send. Try again in a minute.")
                    .font(.footnote)
                    .foregroundStyle(Brand.inkSoft)
            }
        }
    }

    private func send() async {
        sending = true
        var d = Submission.Draft()
        d.kind = .tree
        d.why = why
        d.locationHint = String(format: "%.5f, %.5f (GPS)", origin.lat, origin.lng)
        d.city = nearbyCityName ?? ""
        let ok = await Submission.send(d, from: "app:spot")
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
            Text("We check every tree before it goes on the map. If it makes it, it will be here.")
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
