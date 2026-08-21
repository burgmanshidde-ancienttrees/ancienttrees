// Begin: the walk as it happens, rather than as a page about a walk.
//
// Until now Begin handed the person to Apple Maps and our app was over, which
// made walk the one verb of the four that was still an advertisement for
// itself. The teardown's sharpest line was that AllTrails puts Begin under a
// picture of the route and then STAYS with you; this is our version of the
// staying.
//
// Three decisions worth knowing before changing anything here.
//
// PROGRESS IS NOT A NEW STORE. Which trees you have done is `Saved.isVisited`,
// the same flag the tick button on a tree page sets. So a walk survives the app
// being killed, follows the account to another phone, and cannot drift out of
// step with the collection. There is no walk-session object to leak.
//
// GPS IS A BONUS, NEVER A GATE (DECISIONS.md 2026-08-20). Under a canopy
// accuracy falls to tens of metres, and a veteran tree in a wood is exactly
// where it is worst, so a proximity check would refuse people who are standing
// in front of the tree. Ticking therefore always works; being close only
// changes which button is the loud one.
//
// AND THE OTHER SURFACE: the website keeps its static walk page with the route
// and directions. Begin is a phone-in-hand mode and stays app-only, which is
// the honest answer to the both-surfaces rule rather than a promise to port it.

import SwiftUI
import MapKit

struct WalkMode: View {
    let walk: Walk
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    @Environment(Saved.self) private var saved
    @Environment(Account.self) private var account
    @Environment(Nudge.self) private var nudge
    @Environment(\.dismiss) private var dismiss
    @State private var selected: Tree?
    @State private var justTicked: Tree?

    private var trees: [Tree] { catalogue.trees(of: walk) }
    private var done: Int { trees.filter { saved.isVisited($0.id) }.count }

    /// The one you are walking to: the first you have not ticked. Order is the
    /// walk's own order, which is a planning decision rather than an accident.
    private var next: Tree? { trees.first { !saved.isVisited($0.id) } }

    private var route: [CLLocationCoordinate2D] {
        if let shape = walk.shape, shape.count > 1 {
            return shape.compactMap { $0.count == 2 ? CLLocationCoordinate2D(latitude: $0[1], longitude: $0[0]) : nil }
        }
        return trees.map { .init(latitude: $0.lat, longitude: $0.lng) }
    }

    /// Metres to the tree you are heading for, from wherever the phone thinks
    /// it is. Shown, never enforced.
    private func metres(_ t: Tree) -> Int {
        Int(Geo.km(origin, (t.lat, t.lng)) * 1000)
    }

    /// Metres under a kilometre, kilometres above it. "1.924 m" is what a
    /// grouping separator does to 1924 metres, and to a European eye that
    /// reads as one and a bit metres.
    private func distanceLabel(_ t: Tree) -> String {
        let m = metres(t)
        return m < 1000 ? "\(m) m away"
                        : String(format: "%.1f km away", Double(m) / 1000)
    }

    /// Close enough that "are you standing in front of it" is the right
    /// question rather than "shall I take you there". Deliberately loose.
    private func withinReach(_ t: Tree) -> Bool { metres(t) <= 120 }

    var body: some View {
        ZStack(alignment: .bottom) {
            TreeMap(trees: trees,
                    focus: (next ?? trees.first).map { .init(latitude: $0.lat, longitude: $0.lng) },
                    route: route,
                    routeIsReal: (walk.shape?.count ?? 0) > 1,
                    showsRecentre: true,
                    spanMeters: 1600,
                    clusters: false,
                    selected: $selected)
                .ignoresSafeArea()
            topBar
                .frame(maxHeight: .infinity, alignment: .top)
            bottomBar
        }
        // .contain FIRST, or the identifier stamps itself onto every button
        // inside and the close control, the tick and the directions all answer
        // to "walk-mode". That is the same trap this project hit once before
        // with a heart inheriting its card's identifier.
        .accessibilityElement(children: .contain)
        .accessibilityIdentifier("walk-mode")
    }

    // MARK: - the bar that says where you are in it

    private var topBar: some View {
        HStack(spacing: 12) {
            Button { dismiss() } label: {
                Image(systemName: "xmark")
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundStyle(Brand.ink)
                    .frame(width: 34, height: 34)
                    .background(Brand.surface, in: .circle)
                    .frame(width: 44, height: 44)
                    .contentShape(.rect)
            }
            .accessibilityLabel("Leave the walk")
            .accessibilityIdentifier("walk-close")

            VStack(alignment: .leading, spacing: 2) {
                Text(walk.name)
                    .font(.brand(15, .bold))
                    .foregroundStyle(Brand.ink)
                    .lineLimit(1)
                Text("\(done) of \(trees.count) ticked off")
                    .font(.caption)
                    .foregroundStyle(Brand.inkSoft)
                    .monospacedDigit()
            }
            Spacer(minLength: 0)
        }
        .padding(.horizontal, 10)
        .padding(.vertical, 8)
        .background(Brand.surface.opacity(0.96), in: .rect(cornerRadius: 18))
        .padding(.horizontal, 12)
        .padding(.top, 6)
    }

    // MARK: - the bar that says what to do next

    @ViewBuilder private var bottomBar: some View {
        VStack(spacing: 10) {
            if let t = justTicked {
                tickedNote(t)
            }
            if let t = next {
                nextCard(t)
            } else {
                finishedCard
            }
        }
        .padding(.horizontal, 12)
        .padding(.bottom, 10)
    }

    private func tickedNote(_ t: Tree) -> some View {
        HStack(spacing: 8) {
            Image(systemName: "checkmark.seal.fill").foregroundStyle(Brand.moss)
            Text("\(t.name) is yours.")
                .font(.footnote).foregroundStyle(Brand.ink)
            Spacer(minLength: 0)
        }
        .padding(.horizontal, 14).padding(.vertical, 10)
        .background(Brand.surface, in: .rect(cornerRadius: 14))
        .transition(.opacity)
    }

    private func nextCard(_ t: Tree) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(spacing: 12) {
                Text("\((trees.firstIndex(of: t) ?? 0) + 1)")
                    .font(.brand(14, .bold)).foregroundStyle(.white)
                    .frame(width: 26, height: 26)
                    .background(Brand.moss, in: .circle)
                VStack(alignment: .leading, spacing: 2) {
                    Text(t.name)
                        .font(.brand(17, .bold)).foregroundStyle(Brand.ink)
                        .lineLimit(2)
                    Text("\(t.commonName) · \(distanceLabel(t))")
                        .font(.footnote).foregroundStyle(Brand.inkSoft)
                }
                Spacer(minLength: 0)
            }

            // Which button is loud follows the distance; both are always here,
            // because GPS is a bonus and never a gate.
            if withinReach(t) {
                Button { tick(t) } label: { loud("I am standing before it", "checkmark") }
                    .accessibilityIdentifier("walk-tick")
                Button { directions(t) } label: { quiet("Take me there", "arrow.turn.up.right") }
            } else {
                Button { directions(t) } label: { loud("Take me there", "arrow.turn.up.right") }
                Button { tick(t) } label: { quiet("I am standing before it", "checkmark") }
                    .accessibilityIdentifier("walk-tick")
            }
        }
        .padding(14)
        .background(Brand.surface, in: .rect(cornerRadius: 18))
    }

    private var finishedCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("You walked the whole thing")
                .font(.brand(20, .heavy)).foregroundStyle(Brand.ink)
            Text("\(trees.count) trees, \(walk.duration.lowercased()) of \(walk.city). They are all in your collection.")
                .font(.footnote).foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
            Button { dismiss() } label: { loud("Done", "checkmark") }
                .accessibilityIdentifier("walk-done")
        }
        .padding(14)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Brand.surface, in: .rect(cornerRadius: 18))
        .accessibilityIdentifier("walk-finished")
    }

    private func loud(_ title: String, _ icon: String) -> some View {
        HStack { Spacer()
            Label(title, systemImage: icon).font(.brand(17, .bold))
            Spacer() }
            .padding(.vertical, 14)
            .background(Brand.moss, in: .rect(cornerRadius: 15))
            .foregroundStyle(.white)
    }

    private func quiet(_ title: String, _ icon: String) -> some View {
        HStack { Spacer()
            Label(title, systemImage: icon).font(.brand(16, .bold))
            Spacer() }
            .padding(.vertical, 12)
            .background(Brand.surfaceMuted, in: .rect(cornerRadius: 15))
            .foregroundStyle(Brand.ink)
    }

    private func tick(_ t: Tree) {
        if !saved.isVisited(t.id) { saved.toggleVisited(t.id) }
        withAnimation(.snappy) { justTicked = t }
        // The same ask the tree page makes at the same moment, so a walk cannot
        // quietly become the one place that collects without ever offering to
        // keep what it collected.
        nudge.ticked(treeName: t.name, signedIn: account.isSignedIn, total: saved.visitedCount)
    }

    private func directions(_ t: Tree) {
        MKMapItem(placemark: .init(coordinate: .init(latitude: t.lat, longitude: t.lng)))
            .openInMaps(launchOptions: [MKLaunchOptionsDirectionsModeKey: MKLaunchOptionsDirectionsModeWalking])
    }
}
