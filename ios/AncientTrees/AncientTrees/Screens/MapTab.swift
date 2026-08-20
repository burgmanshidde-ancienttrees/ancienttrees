// The map is the product, so the tab called Map opens on a map.
//
// The model is Google Maps' rather than AllTrails', and Hidde is right about
// why: AllTrails is built for LINES and we show POINTS. A route has no location,
// it has a course, which is why they cluster into labels reading "2 routes". A
// tree is exactly what a pin wants to be, and Google Maps has been solving that
// one problem for twenty years.
//
// The piece worth copying is the sheet. It is always there, it has three
// heights, and it carries either the list or whatever pin you last tapped. That
// is what stops the map and the list being two destinations you have to choose
// between, which is what ours were.

import SwiftUI
import MapKit

struct MapTab: View {
    let catalogue: Catalogue
    let origin: (lat: Double, lng: Double)
    let located: Bool
    /// iOS has been asked and said no. A different sentence from "not yet
    /// asked", because the only way out of this one is Settings.
    var locationDenied: Bool = false
    var onUseMyLocation: () -> Void = {}

    @State private var selected: Tree?
    /// Debug only, same family as -tab and -at: selecting a pin needs a tap and
    /// simctl cannot tap, so the one screen that only exists after a tap could
    /// not be looked at before it shipped.
    private var debugSelect: String? {
        ProcessInfo.processInfo.arguments.first { $0.hasPrefix("-select=") }.map { String($0.dropFirst(8)) }
    }
    @State private var sheetHeight: SheetHeight = .peek
    @State private var query = ""
    /// Where the map is looking. nil until it has been moved, so the first list
    /// is still the list of what is near you.
    @State private var mapRegion: MKCoordinateRegion?
    @Environment(Saved.self) private var saved
    @Environment(Account.self) private var account
    @Environment(Nudge.self) private var nudge

    /// EVERY tree, because the map is the whole map.
    ///
    /// This used to hand MapKit the nearest 400 within 200 km, which meant that
    /// zooming out from Amsterdam showed the Netherlands and then nothing: no
    /// Portugal, no Japan, no reason to believe there is a world here. The
    /// website has never done that, it clusters the whole set, and the app
    /// looking narrower than the website is the wrong way round.
    ///
    /// Cheap to do: 1,500 annotations is nothing for MKMapView, the pins carry
    /// a clusteringIdentifier so MapKit collapses them by zoom on its own, and
    /// the set never changes so updateUIView stops churning entirely.
    private var mapTrees: [Tree] { catalogue.trees }
    /// The point the list is about: where the map is looking once it has been
    /// moved, and where you are standing until then.
    private var focus: (lat: Double, lng: Double) {
        guard let c = mapRegion?.center else { return origin }
        return (lat: c.latitude, lng: c.longitude)
    }

    /// How far to look, which has to follow the zoom. Half the visible height,
    /// floored at fifty kilometres so a street-level view still fills the list
    /// rather than showing the four trees actually on screen.
    private var reachKm: Double {
        guard let s = mapRegion?.span else { return 50 }
        return max(50, s.latitudeDelta * 111.0 / 2)
    }

    /// True when the map is still looking at roughly where you are standing, so
    /// the chip can stop saying "near you" the moment that stops being true.
    private var lookingAtYou: Bool {
        guard let c = mapRegion?.center else { return true }
        return CLLocation(latitude: c.latitude, longitude: c.longitude)
            .distance(from: CLLocation(latitude: origin.lat, longitude: origin.lng)) < 3000
    }

    private var listed: [(tree: Tree, km: Double)] {
        let near = catalogue.nearest(to: focus.lat, focus.lng, limit: 60, withinKm: reachKm)
        guard !query.isEmpty else { return near }
        let q = query.lowercased()
        return catalogue.trees
            .filter { $0.name.lowercased().contains(q) || $0.city.lowercased().contains(q)
                      || $0.species.lowercased().contains(q) }
            .prefix(40)
            .map { ($0, $0.distanceKm(from: focus.lat, focus.lng)) }
    }

    var body: some View {
        ZStack(alignment: .bottom) {
            TreeMap(trees: mapTrees,
                    focus: .init(latitude: origin.lat, longitude: origin.lng),
                    showsRecentre: true,
                    region: $mapRegion,
                    selected: $selected)
                .ignoresSafeArea(edges: [.top, .horizontal])
            BottomSheet(height: $sheetHeight) {
                // The arbitration between dragging the sheet and scrolling what
                // is inside it, which is the whole interaction and was wrong.
                //
                // The convention, and Apple Maps, Google Maps and Airbnb all do
                // exactly this: the finger does ONE thing at a time, and which
                // one is decided by the sheet's height rather than by where the
                // finger landed. Below full height the sheet moves and the list
                // does not scroll, so dragging up over the trees raises the
                // sheet instead of scrolling past them. At full height the list
                // scrolls, and the grabber at the top stays outside the scroll
                // view so there is always a way back down.
                sheet
            }
        }
        // The title used to float over the map as bare text with nothing behind
        // it, and worse, "Near Amsterdam" was a statement of a problem with no
        // way to fix it. It is a chip now, and when we do not know where you
        // are it is the button that finds out.
        .overlay(alignment: .top) { whereChip }
        .task {
            if let id = debugSelect, let t = catalogue.tree(id) {
                selected = t
                sheetHeight = .half
            }
        }
        .toolbar(.hidden, for: .navigationBar)
        .onChange(of: selected) { _, new in
            // Tapping a pin raises the sheet to that tree, the way Google Maps
            // turns the sheet into the place you tapped.
            if new != nil { sheetHeight = .half }
        }
    }

    /// Close enough to see it. Beyond this the honest thing is to point rather
    /// than to offer a tick, because a tick you can press from your sofa is
    /// worth nothing to collect.
    private let arrivedKm = 0.12

    private var arrived: Tree? {
        guard query.isEmpty, selected == nil,
              let first = listed.first, first.km <= arrivedKm else { return nil }
        return first.tree
    }

    /// What the pager pages over. The tapped tree first if the list does not
    /// already contain it, which happens when somebody taps a pin outside the
    /// sixty the list shows.
    private var pagerTrees: [Tree] {
        let list = listed.map(\.tree)
        guard let sel = selected else { return list }
        return list.contains(where: { $0.id == sel.id }) ? list : [sel] + list
    }

    @ViewBuilder private var sheet: some View {
        if selected != nil {
            selectedPager
        } else {
            VStack(spacing: 0) {
                if let t = arrived { arrivalCard(t) }
                list
            }
        }
    }

    /// The moment the whole product exists for, surfaced where the user already
    /// is instead of in a tab that would sit dead the rest of the month.
    private func arrivalCard(_ t: Tree) -> some View {
        VStack(spacing: 10) {
            Text("You are standing in front of").font(.caption).foregroundStyle(.secondary)
            Text(t.name).font(.title3.bold()).multilineTextAlignment(.center)
            Button {
                saved.toggleVisited(t.id)
                if saved.isVisited(t.id) {
                    nudge.ticked(treeName: t.name,
                                 signedIn: account.isSignedIn,
                                 total: saved.visitedCount)
                }
            } label: {
                Label(saved.isVisited(t.id) ? "Ticked off" : "I have seen this one",
                      systemImage: saved.isVisited(t.id) ? "checkmark.seal.fill" : "checkmark.seal")
                    .font(.subheadline.weight(.semibold))
                    .frame(maxWidth: .infinity).padding(.vertical, 13)
            }
            .buttonStyle(.borderedProminent)
            .tint(saved.isVisited(t.id) ? .gray : Color(red: 0.20, green: 0.35, blue: 0.20))
            .sensoryFeedback(.success, trigger: saved.isVisited(t.id)) { _, now in now }
        }
        .padding(16)
        .background(Color(.secondarySystemBackground), in: .rect(cornerRadius: 14))
        .padding(.horizontal, 16).padding(.bottom, 6)
    }

    private var list: some View {
        LazyVStack(spacing: 12) {
                searchField
                ForEach(listed, id: \.tree.id) { hit in
                    NavigationLink(value: Route.tree(hit.tree.id)) {
                        TreeCard(tree: hit.tree, km: hit.km)
                    }
                    .buttonStyle(.plain)
                }
                if listed.isEmpty {
                    Text(query.isEmpty
                         ? (lookingAtYou
                            ? "No tree of ours within fifty kilometres."
                            : "No tree of ours in view. Try moving the map.")
                         : "Nothing matches “\(query)”.")
                        .font(.footnote).foregroundStyle(.secondary).padding(.top, 30)
                }
            }
        .padding(.horizontal, 16)
        .padding(.bottom, 110)      // clear of the floating tab bar
    }

    @ViewBuilder private var whereChip: some View {
        if located && !lookingAtYou {
            Label("Trees in this area", systemImage: "map")
                .font(.subheadline.weight(.semibold))
                .padding(.horizontal, 14).padding(.vertical, 8)
                .background(.regularMaterial, in: .capsule)
                .shadow(color: .black.opacity(0.12), radius: 6, y: 2)
                .padding(.top, 10)
        } else if located {
            Label("Near you", systemImage: "location.fill")
                .font(.subheadline.weight(.semibold))
                .padding(.horizontal, 14).padding(.vertical, 8)
                .background(.regularMaterial, in: .capsule)
                .shadow(color: .black.opacity(0.12), radius: 6, y: 2)
                .padding(.top, 10)
        } else {
            Button {
                if locationDenied {
                    if let u = URL(string: UIApplication.openSettingsURLString) {
                        UIApplication.shared.open(u)
                    }
                } else {
                    onUseMyLocation()
                }
            } label: {
                HStack(spacing: 6) {
                    Image(systemName: "location.slash")
                    Text("Near Amsterdam")
                    Text("·").foregroundStyle(.secondary)
                    Text(locationDenied ? "Turn on location" : "Use my location")
                        .foregroundStyle(Color(red: 0.20, green: 0.35, blue: 0.20))
                }
                .font(.subheadline.weight(.semibold))
                .padding(.horizontal, 14).padding(.vertical, 8)
                .background(.regularMaterial, in: .capsule)
                .shadow(color: .black.opacity(0.12), radius: 6, y: 2)
                .padding(.top, 10)
            }
            .buttonStyle(.plain)
        }
    }

    private var searchField: some View {
        HStack(spacing: 8) {
            Image(systemName: "magnifyingglass").foregroundStyle(.secondary)
            TextField("Search a tree, species or place", text: $query)
                .textFieldStyle(.plain)
                .autocorrectionDisabled()
                .onTapGesture { sheetHeight = .full }
            if !query.isEmpty {
                Button { query = "" } label: {
                    Image(systemName: "xmark.circle.fill").foregroundStyle(.secondary)
                }
                .buttonStyle(.plain)
            }
        }
        .padding(.horizontal, 12).padding(.vertical, 10)
        .background(Color(.secondarySystemBackground), in: .capsule)
        .padding(.top, 6)
    }

    /// One tapped pin, shown in the sheet rather than pushed onto a page, so the
    /// map stays visible behind the decision.
    /// Tap a pin and you stay on the map, with the tree in a sheet over it, and
    /// you can swipe sideways through the others without ever leaving.
    ///
    /// Straight out of the AllTrails recordings (Hidde, 2026-08-20: "dat je op
    /// een boom klikt dat dan de kaart nog in het klein in het plaatje staat en
    /// dat je heen en weer kan klikken"). Their route tap does not open a page
    /// either: the whole decision happens on top of the thing being decided
    /// about, and the map underneath moves with you.
    private var selectedPager: some View {
        VStack(spacing: 0) {
            // The hint sits above the cards rather than under them: below, it
            // ends up behind the floating tab bar, and it is the one line that
            // tells you the sideways gesture exists at all.
            HStack(spacing: 6) {
                Image(systemName: "arrow.left.and.right")
                Text("Swipe for the next one nearby")
            }
            .font(.caption).foregroundStyle(Brand.inkSoft)
            .padding(.bottom, 8)
            .opacity(pagerTrees.count > 1 ? 1 : 0)

            TabView(selection: Binding(
                get: { selected?.id ?? "" },
                set: { id in selected = pagerTrees.first { $0.id == id } }
            )) {
                ForEach(pagerTrees) { t in
                    selectedTree(t).tag(t.id)
                }
            }
            .tabViewStyle(.page(indexDisplayMode: .never))
            .frame(height: 340)
            Color.clear.frame(height: 100)      // clear of the floating tab bar
        }
    }

    private func selectedTree(_ t: Tree) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Spacer()
                Button { selected = nil } label: {
                    Image(systemName: "xmark.circle.fill")
                        .font(.title3).foregroundStyle(Brand.inkSoft)
                }
                .buttonStyle(.plain)
            }
            TreeCard(tree: t, km: t.distanceKm(from: origin.lat, origin.lng))
            NavigationLink(value: Route.tree(t.id)) {
                Label("Read why it is worth the walk", systemImage: "book")
            }
            .buttonStyle(BrandButtonStyle())
        }
        .padding(.horizontal, 16).padding(.bottom, 8)
    }
}
