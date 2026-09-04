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
    /// The stops, when the caller already holds them.
    ///
    /// A walk normally names its trees by id and this view looks them up, which
    /// is right for a walk from the feed and WRONG for a tree you added
    /// yourself: your tree is not in the catalogue, so a one-tree walk to it
    /// resolved to no trees at all, and a walk with no trees has nothing left
    /// to tick, so it opened straight onto "You walked the whole thing. 0
    /// trees. They are all in your collection." (Hidde, 2026-08-25, on his own
    /// Baarn tree: "dan staat er zero ticked off... dan wel take me there zou
    /// gewoon een route moeten tonen van waar ik nu ben naar die boom").
    var only: [Tree]? = nil
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    @Environment(Saved.self) private var saved
    @Environment(Account.self) private var account
    @Environment(Nudge.self) private var nudge
    @Environment(ReviewPrompt.self) private var reviewPrompt
    // Both only to hand on to the collect sheet: a sheet does not inherit
    // observables from the view that presents it, which is the trap ContentView's
    // appObjects() exists for and which trapped the app twice in two days.
    @Environment(Sightings.self) private var sightings
    @Environment(Navigator.self) private var navigator
    @Environment(Units.self) private var units
    @Environment(Entitlement.self) private var entitlement
    @Environment(\.dismiss) private var dismiss
    @State private var selected: Tree?
    /// A real pedestrian route, fetched once when this screen opens and the
    /// feed had none. See Kit/Routing.swift for why it is one call and why
    /// failing is fine.
    @State private var liveRoute: [CLLocationCoordinate2D]?
    /// The camera, presented from here rather than through the root, because
    /// this screen is a fullScreenCover and a sheet asked for on the root would
    /// have nowhere to appear.
    @State private var photographing = false

    private var trees: [Tree] { only ?? catalogue.trees(of: walk) }
    private var done: Int { trees.filter { saved.isVisited($0.id) }.count }

    /// The one you are walking to: the first you have not ticked. Order is the
    /// walk's own order, which is a planning decision rather than an accident.
    private var next: Tree? { trees.first { !saved.isVisited($0.id) } }

    private var route: [CLLocationCoordinate2D] {
        if let shape = walk.shape, shape.count > 1 {
            return shape.compactMap { $0.count == 2 ? CLLocationCoordinate2D(latitude: $0[1], longitude: $0[0]) : nil }
        }
        if let live = liveRoute, live.count > 1 { return live }
        let stops = trees.map { CLLocationCoordinate2D(latitude: $0.lat, longitude: $0.lng) }
        // A walk of ONE has no line between stops, so the useful line is from
        // you to it. Without this you saw the tree and nothing about getting
        // there, which is most of what somebody who tapped Take me there
        // wanted. Drawn dashed like every unrouted line here, because it is the
        // direction rather than the way.
        if stops.count == 1 { return [.init(latitude: origin.lat, longitude: origin.lng), stops[0]] }
        return stops
    }

    /// What the end of the walk says, in a sentence that holds together for
    /// one tree as well as for nine.
    private var finishedLine: String {
        let n = trees.count
        let what = n == 1 ? "One tree" : "\(n) trees"
        let how = walk.duration.trimmingCharacters(in: .whitespaces).lowercased()
        let where_ = walk.city.isEmpty ? "" : " of \(walk.city)"
        let middle = how.isEmpty ? "" : ", \(how)"
        let tail = n == 1 ? "It is in your collection." : "They are all in your collection."
        return "\(what)\(middle)\(where_). \(tail)"
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

    /// SHOW THE WHOLE WALK WHEN IT OPENS.
    ///
    /// This used to centre on one tree at a fixed 1600 metre span, which is
    /// narrower than most walks: opening Plantage put the route running off the
    /// left edge with its trees piled bottom right, so the first thing you saw
    /// of the walk you had just chosen was a corner of it. A walk is a shape,
    /// and the question at this moment is "is this an afternoon I want", which
    /// you cannot answer from a corner.
    ///
    /// Only the opening camera. TreeMap applies focus and span once when it
    /// makes the map, so panning, following and the recentre button are all
    /// untouched, and once you are walking the next tree is what the bottom bar
    /// is for.
    private var walkPoints: [CLLocationCoordinate2D] {
        let stops = trees.map { CLLocationCoordinate2D(latitude: $0.lat, longitude: $0.lng) }
        return route.count > 1 ? route + stops : stops
    }

    private var openingCentre: CLLocationCoordinate2D? {
        let pts = walkPoints
        guard !pts.isEmpty else { return nil }
        let lats = pts.map(\.latitude), lngs = pts.map(\.longitude)
        guard let a = lats.min(), let b = lats.max(),
              let c = lngs.min(), let d = lngs.max() else { return nil }
        return .init(latitude: (a + b) / 2, longitude: (c + d) / 2)
    }

    private var openingSpan: CLLocationDistance {
        let pts = walkPoints
        guard pts.count > 1,
              let a = pts.map(\.latitude).min(), let b = pts.map(\.latitude).max(),
              let c = pts.map(\.longitude).min(), let d = pts.map(\.longitude).max()
        else { return 1600 }
        let midLat = (a + b) / 2
        let tall = (b - a) * 111_320
        let wide = (d - c) * 111_320 * cos(midLat * .pi / 180)
        // A quarter more than the walk itself, so nothing sits on the bezel,
        // and never so tight that a compact walk fills the screen with one
        // street. 400 m is about a city block in view either side.
        return max(400, max(tall, wide) * 1.25)
    }

    var body: some View {
        ZStack(alignment: .bottom) {
            TreeMap(trees: trees,
                    focus: openingCentre,
                    route: route,
                    routeIsReal: (walk.shape?.count ?? 0) > 1 || (liveRoute?.count ?? 0) > 1,
                    showsRecentre: true,
                    spanMeters: openingSpan,
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
        .sheet(isPresented: $photographing) {
            CollectSheet(catalogue: catalogue, origin: origin, mode: .collect)
                .environment(saved)
                .environment(account)
                .environment(nudge)
                .environment(reviewPrompt)
                .environment(sightings)
                .environment(navigator)
                .environment(units)
                .environment(entitlement)
        }
        .task {
            // One call, and only where the feed left a gap. A walk that came
            // with a routed shape needs nothing, and 161 of 212 do.
            guard liveRoute == nil, (walk.shape?.count ?? 0) <= 1, !trees.isEmpty else { return }
            var stops: [CLLocationCoordinate2D] = [
                .init(latitude: origin.lat, longitude: origin.lng)
            ]
            stops.append(contentsOf: trees.map {
                CLLocationCoordinate2D(latitude: $0.lat, longitude: $0.lng)
            })
            liveRoute = await Routing.pedestrian(through: stops)
        }
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
            // The "X is yours" note went with the tap-to-tick on 2026-08-25.
            // The collect sheet says it now, over the photograph that proves it,
            // which is a better place for it than a line on a card behind.
            if let t = next {
                nextCard(t)
            } else if trees.isEmpty {
                // Not finished: empty. A walk whose stops we cannot resolve
                // has to say that rather than congratulate somebody for a walk
                // they never took, which is what it did.
                emptyCard
            } else {
                finishedCard
            }
        }
        .padding(.horizontal, 12)
        .padding(.bottom, 10)
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
            // WITHIN REACH OR NOT AT ALL (Hidde, 2026-08-25, looking at a tree
            // 17 km away: "the option im standing in front of it makes no
            // sense"). It used to offer the tick at any distance, loud when you
            // were close and quiet when you were not, on the reasoning that GPS
            // is a bonus and never a gate. That reasoning was about not blocking
            // somebody whose phone is confused by 30 metres of city; it was
            // never an argument for offering to collect a tree in another
            // province. And since the tick opens the camera, the offer is now
            // literally impossible to accept from there.
            if withinReach(t) {
                Button { tick(t) } label: { loud("I am standing before it", "checkmark") }
                    .accessibilityIdentifier("walk-tick")
                Button { directions(t) } label: { quiet("Open in Maps", "arrow.turn.up.right") }
            } else {
                Button { directions(t) } label: { loud("Open in Maps", "arrow.turn.up.right") }
            }
        }
        .padding(14)
        .background(Brand.surface, in: .rect(cornerRadius: 18))
    }

    private var emptyCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("We cannot open this walk")
                .font(.brand(20, .heavy)).foregroundStyle(Brand.ink)
            Text("Its trees are not in this copy of the map. Try again after the app has updated.")
                .font(.footnote).foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)
            Button { dismiss() } label: { loud("Close", "xmark") }
        }
        .padding(14)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Brand.surface, in: .rect(cornerRadius: 18))
    }

    private var finishedCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("You walked the whole thing")
                .font(.brand(20, .heavy)).foregroundStyle(Brand.ink)
            // Plural and duration both have to survive a walk of ONE, which
            // is what a single tree becomes now that Take me there opens this
            // view instead of somebody else's app. "1 trees, of Amsterdam"
            // with a hole where the duration should be is what it said before.
            Text(finishedLine)
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
            // 44, Apple's floor, asserted rather than arrived at. Twelve points
            // of padding around a 16 point label came to 43 on a large phone,
            // and appfit only ever measured the SE until 2026-08-25, where the
            // same arithmetic happened to reach 44.
            .frame(minHeight: 44)
            .background(Brand.surfaceMuted, in: .rect(cornerRadius: 15))
            .foregroundStyle(Brand.ink)
    }

    private func tick(_ t: Tree) {
        // The account first, here as everywhere else that keeps something
        // (Hidde, 2026-08-25). A walk cannot be the one place that collects
        // into a collection nobody is signed in to keep.
        guard account.isSignedIn else {
            nudge.require(.keepTree(t.name))
            return
        }
        // THE PHOTOGRAPH IS THE TICK (Hidde, 2026-08-25: "you shouldn't give
        // the option for I'm in front of it without taking a photo, it should
        // go to that flow then"). It used to tick straight off a tap, which is
        // a claim anybody can make from the sofa, and it left the collection
        // with nothing in it worth looking at. The collect sheet does the whole
        // job: photograph, work out which tree it is, tick, keep the picture.
        photographing = true
    }

    private func directions(_ t: Tree) {
        Directions.walk(lat: t.lat, lng: t.lng)
    }
}
