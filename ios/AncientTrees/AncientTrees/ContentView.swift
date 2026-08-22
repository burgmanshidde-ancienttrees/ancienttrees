// Five slots: Explore, Saved, Spot, Collect, Profile. Hidde's bar, decided
// 2026-08-20 evening after two earlier same-day layouts; the full reasoning
// lives in DECISIONS.md and the reading is short: left looks (free), the
// centre contributes (free, and it is a BUTTON rather than a place), right
// owns (where Plus lives).
//
// Map is the tool ("I am here") and Explore is the FEED ("I am on the couch"):
// two tabs rather than one behind a pill, which is the Komoot split and gives
// the inspiration shelves an address instead of a toggle. Saved is gone as a
// tab: hearts and ticks are one idea, so Collect carries both as segments.
// Spot is the Strava/Untappd centre pattern: selecting it presents a sheet and
// the bar stays where it was. WALK stays a filter on the map and SEASON a
// pulse on the pins, exactly as before.

import SwiftUI
import CoreLocation
import MapKit

struct ContentView: View {
    @State fileprivate var store = CatalogueStore()
    @State fileprivate var saved = Saved()
    @State fileprivate var entitlement = Entitlement()
    @State private var location = LocationProvider()
    @State fileprivate var account = Account()
    @State fileprivate var nudge = Nudge()
    @State fileprivate var navigator = Navigator()
    @State fileprivate var units = Units()
    @State fileprivate var sightings = Sightings()
    @State private var rootSheet: RootSheet?
    @State private var primerAnswered = false
    @State private var slowStart = false
    /// One path per tab, so tapping the tab you are already on can empty it.
    ///
    /// FOUR SEPARATE ARRAYS, not a dictionary keyed by tab. The dictionary
    /// version compiled, looked right and silently killed every link in the
    /// app: `Binding(get: { paths[id] ?? [] }, set: { paths[id] = $0 })` hands
    /// SwiftUI a fresh array on every read, so a push never settled and tapping
    /// a tree card did nothing at all, on the map AND on Explore. Two UI tests
    /// caught it; nothing in a screenshot could have.
    @State private var mapPath: [Route] = []
    @State private var explorePath: [Route] = []
    @State private var collectPath: [Route] = []

    private func path(_ id: Int) -> Binding<[Route]> {
        switch id {
        case 0: $mapPath
        case 1: $explorePath
        default: $collectPath
        }
    }

    private func clearPath(_ id: Int) {
        switch id {
        case 0: mapPath = []
        case 1: explorePath = []
        default: collectPath = []
        }
    }
    @State private var debugTree: String?

    /// Everything the root can put over the app. An enum rather than a pile of
    /// booleans so there is exactly one sheet modifier below.
    enum RootSheet: Identifiable, Equatable {
        case signIn(SignInReason)
        case paywall(Feature)
        /// The centre button's sheet. A case here rather than its own boolean
        /// because SwiftUI honours one sheet modifier per view, which is the
        /// whole reason this enum exists.
        case spot(SpotSheet.Mode)
        var id: String {
            switch self {
            case .signIn(let r): "signin-" + r.id
            case .paywall(let f): "paywall-" + f.rawValue
            case .spot(let m): "spot-" + m.rawValue
            }
        }
    }
    // Screenshotting each tab needs a way to open on one, because this Mac's
    // simulator panel is not available and simctl cannot tap. Debug only.
    @State private var tab = ProcessInfo.processInfo.arguments
        .first(where: { $0.hasPrefix("-tab=") })
        .flatMap { Int($0.dropFirst(5)) } ?? 0

    /// Debug only, same reason as the tab argument: this Mac cannot tap the
    /// simulator's location permission dialog, so screenshots would all be
    /// Amsterdam. `-at=38.11,13.36` starts somewhere else.
    private var debugOrigin: (lat: Double, lng: Double)? {
        guard let a = ProcessInfo.processInfo.arguments
                .first(where: { $0.hasPrefix("-at=") })?.dropFirst(4).split(separator: ","),
              a.count == 2, let la = Double(a[0]), let ln = Double(a[1]) else { return nil }
        return (lat: la, lng: ln)
    }

    /// `-open=tree:lon_001`, `-open=city:london`, `-open=species:Pedunculate Oak`,
    /// `-open=collection:europe`, `-open=walk:london|The City churchyards`.
    /// The walk separator is a pipe because a walk needs two values and a
    /// colon already separates the kind.
    static func debugRoute(_ spec: String) -> Route? {
        guard let colon = spec.firstIndex(of: ":") else { return nil }
        let kind = String(spec[spec.startIndex..<colon])
        let value = String(spec[spec.index(after: colon)...])
        switch kind {
        case "tree": return .tree(value)
        case "city": return .city(value)
        case "collection": return .collection(value)
        case "species": return .species(value)
        case "country": return .country(value)
        case "profile": return .profile
        case "walk":
            let parts = value.split(separator: "|", maxSplits: 1).map(String.init)
            guard parts.count == 2 else { return nil }
            return .walk(city: parts[0], name: parts[1])
        default: return nil
        }
    }

    private var origin: (lat: Double, lng: Double) {
        debugOrigin ?? location.coordinate ?? (lat: 52.3731, lng: 4.8922)   // Dam square
    }

    /// Shown once, and only when iOS has genuinely not been asked yet.
    private var needsPrimer: Bool {
        guard debugOrigin == nil || ProcessInfo.processInfo.arguments.contains("-primer") else { return false }
        if primerAnswered { return false }
        return location.status == .notDetermined
    }

    /// Tapping the tab you are already on empties that tab's stack, which is
    /// what every iOS app with tabs has done since tabs existed and what this
    /// one did not do at all: once you were four trees deep the only way out
    /// was four taps on Back.
    private var tabSelection: Binding<Int> {
        Binding(get: { tab },
                set: { new in
                    // Spot is a button wearing a tab's clothes, the Strava and
                    // Untappd centre pattern: selecting it presents the sheet
                    // and the bar stays exactly where it was.
                    if new == 2 { rootSheet = .spot(.add); return }
                    if new == tab { clearPath(new) }
                    tab = new
                })
    }

    /// One tab's navigation stack, with every destination in this app declared
    /// once rather than inline at ten separate call sites.
    private func stack<Root: View>(_ id: Int, _ cat: Catalogue,
                                   @ViewBuilder root: () -> Root) -> some View {
        NavigationStack(path: path(id)) {
            root()
                .navigationDestination(for: Route.self) { route in
                    destination(route, cat)
                        // A pushed page is a reading page; the bar does nothing
                        // there and AllTrails hides it too. Back is the way out.
                        .toolbar(.hidden, for: .tabBar)
                }
        }
    }

    /// Begin mode, built here so the TabView's own modifier chain stays inside
    /// the type-checker's budget (it went over the moment this was inline).
    private func walkMode(_ w: Walk, _ cat: Catalogue) -> some View {
        WalkMode(walk: w, catalogue: cat, origin: origin)
            .appObjects(self)
    }

    /// Looked up by id at render time on purpose: the catalogue can be replaced
    /// under an open screen now that the app downloads a newer one, and a view
    /// holding a stale struct would quietly keep showing yesterday's story.
    @ViewBuilder
    private func destination(_ route: Route, _ cat: Catalogue) -> some View {
        switch route {
        case .tree(let id):
            if let t = cat.tree(id) {
                TreeDetail(tree: t, catalogue: cat)
            } else {
                ContentUnavailableView("That tree is no longer on the map",
                                       systemImage: "tree",
                                       description: Text("It may have been removed after a correction."))
            }
        case .walk(let city, let name):
            if let w = cat.walks(inCity: city).first(where: { $0.name == name }) {
                WalkDetail(walk: w, catalogue: cat)
            } else {
                ContentUnavailableView("That walk is gone", systemImage: "figure.walk")
            }
        case .collection(let slug):
            if let c = cat.collections.first(where: { $0.slug == slug }) {
                CollectionView(collection: c, catalogue: cat, origin: origin)
            } else {
                ContentUnavailableView("That collection is gone", systemImage: "square.stack")
            }
        case .index(let kind):
            IndexView(kind: kind, catalogue: cat, origin: origin)
        case .profile:
            ProfileView(catalogue: cat)
        case .country(let name):
            CountryView(country: name, catalogue: cat, origin: origin)
        case .species(let name):
            SpeciesView(commonName: name, catalogue: cat, origin: origin)
        case .city(let slug):
            CityView(slug: slug,
                     name: cat.trees.first(where: { $0.citySlug == slug })?.city ?? slug,
                     catalogue: cat, origin: origin)
        }
    }

    var body: some View {
        Group {
            if let cat = store.catalogue {
                TabView(selection: tabSelection) {
                    // Four slots of one weight, and the SELECTED one fills.
                    // Per item rather than globally, because iOS fills EVERY
                    // tab symbol by default and shows selection with tint
                    // alone; Komoot fills only the one you are on, and that is
                    // the convention Hidde asked for (2026-08-22).
                    // Four slots of one weight, and the SELECTED one fills,
                    // which is what iOS does by default and what every app in
                    // Hidde's own references does (2026-08-22, from his Komoot
                    // screenshots). We had turned the fill off the day before
                    // for balance; the balance came from choosing symbols of
                    // one family, not from refusing the convention.
                    // plus.circle and checkmark.circle rhyme on purpose: add
                    // and had are the two halves of the same verb.
                    stack(0, cat) {
                        if let id = debugTree, let t = cat.tree(id) {
                            TreeDetail(tree: t, catalogue: cat)
                        } else {
                            MapTab(catalogue: cat, origin: origin,
                                   located: location.coordinate != nil || debugOrigin != nil,
                                   locationDenied: location.status == .denied || location.status == .restricted,
                                   onUseMyLocation: { location.request() })
                        }
                    }
                        .tag(0)
                        .tabItem { Label("Map", systemImage: "map")
                            .environment(\.symbolVariants, tab == 0 ? .fill : .none) }

                    stack(1, cat) { HomeView(catalogue: cat, origin: origin) }
                        .tag(1)
                        .tabItem { Label("Explore", systemImage: "magnifyingglass")
                            .environment(\.symbolVariants, tab == 1 ? .fill : .none) }

                    // Never actually shown: the selection binding intercepts 2
                    // and presents the Spot sheet instead.
                    Color.clear
                        .tag(2)
                        .tabItem { Label("Add", systemImage: "plus.circle")
                            .environment(\.symbolVariants, tab == 2 ? .fill : .none) }

                    stack(3, cat) { CollectView(catalogue: cat, origin: origin) }
                        .tag(3)
                        .tabItem { Label("Collect", systemImage: "checkmark.circle")
                            .environment(\.symbolVariants, tab == 3 ? .fill : .none) }

                }
                // Outline icons that stay outline when selected, colour doing
                // the selecting (Careem is Hidde's reference; Airbnb does the
                // same). The .none variant sits on each Label because iOS
                // applies its automatic .fill inside the tab item, underneath
                // an environment set on the TabView itself.
                .appObjects(self)
                .onChange(of: navigator.collectNearby) { _, want in
                    if want { rootSheet = .spot(.collect); navigator.collectNearby = false }
                }
                .onChange(of: navigator.push) { _, new in
                    guard let new else { return }
                    path(tab).wrappedValue.append(new)
                    navigator.push = nil
                }
                .onChange(of: navigator.selectTab) { _, new in
                    if let new { tab = new; navigator.selectTab = nil }
                }
                .onChange(of: navigator.showOnMap) { _, new in
                    // POP the map's own stack as well. The tree page you
                    // tapped the inset on is usually pushed ON the map tab, so
                    // switching to tab 0 left you looking at the same page and
                    // the little map read as a dead control (Hidde,
                    // 2026-08-21: "als ik op het kaartje klik opent hij niet").
                    if new != nil { mapPath = [] }
                    if new != nil { tab = 0 }
                }
                // ONE sheet modifier, driven by one optional, because SwiftUI
                // honours only one per view and stacking three meant the ask
                // silently never appeared. The ask is presented from the root so
                // that a tick on a tree page and a third save on the map land in
                // the same sheet rather than in two near-identical ones.
                .sheet(item: $rootSheet) { which in
                    Group {
                        switch which {
                        case .signIn(let reason):
                            SignInSheet(reason: reason, localCount: saved.savedCount)
                        case .paywall(let feature):
                            PaywallView(feature: feature)
                        case .spot(let mode):
                            SpotSheet(catalogue: cat, origin: origin, mode: mode)
                        }
                    }
                    // A sheet does not inherit the environment set on the view
                    // below this modifier, so every object goes in here, once,
                    // for every case. Per-case lists were how the Spot sheet
                    // crashed on 2026-08-21: it gained an Account read and the
                    // .spot case still injected only Saved and Navigator. Any
                    // view a sheet might contain can read any of these.
                    .appObjects(self)
                }
                // DERIVED from the request rather than mirrored into a second
                // piece of state. The mirror version lost the launch argument
                // every time: -begin sets the request in the same update in
                // which the TabView first exists, and an onChange registered by
                // that same update never sees it as a change. A binding cannot
                // miss it, because there is nothing to miss.
                .fullScreenCover(item: Binding(
                    get: { navigator.beginWalk.flatMap { r in
                        cat.walks(inCity: r.city).first { $0.name == r.name } } },
                    set: { if $0 == nil { navigator.beginWalk = nil } })) { w in
                    walkMode(w, cat)
                }
                .onChange(of: nudge.pending) { _, new in
                    if let new { rootSheet = .signIn(new); nudge.pending = nil }
                }
            } else if let err = store.loadError {
                ContentUnavailableView("Something is wrong with the catalogue",
                                       systemImage: "exclamationmark.triangle",
                                       description: Text(err))
                    .brandGround()
            } else {
                // A bare ProgressView on no background is a WHITE SCREEN, and a
                // white screen tells nobody anything. Hidde got one on his own
                // phone and there was no way to tell from it whether the app
                // had crashed, hung, or simply not finished reading 2.5 MB of
                // JSON. So it says what it is doing, on the app's own ground,
                // and says something else if it is taking too long.
                VStack(spacing: 14) {
                    SpeciesMark(species: "Pedunculate Oak", color: Brand.moss)
                        .frame(width: 54, height: 54)
                    ProgressView()
                    if slowStart {
                        Text("This is taking longer than it should. Force quit and open it again, and if it keeps happening, tell us.")
                            .font(.footnote).foregroundStyle(Brand.inkSoft)
                            .multilineTextAlignment(.center)
                            .padding(.horizontal, 40)
                    }
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .brandGround()
                .task {
                    try? await Task.sleep(for: .seconds(6))
                    slowStart = true
                }
            }
        }
        .overlay {
            if needsPrimer {
                LocationPrimer(treeCount: store.catalogue?.trees.count ?? 0,
                               onAllow: { primerAnswered = true; location.request() },
                               onSkip: { primerAnswered = true })
                    .transition(.opacity)
            }
        }
        .animation(.easeInOut(duration: 0.2), value: needsPrimer)
        .task {
            store.loadBundled()
            // Ask whether anything changed. A few dozen bytes, and it is the
            // difference between an app that follows the database and an app
            // frozen at whatever shipped.
            Task { await store.refresh() }
            // Same debug scaffolding as -tab and -at: no simulator panel here,
            // so a screen only reachable by tapping cannot otherwise be looked
            // at before it ships.
            let args = ProcessInfo.processInfo.arguments
            // -tree=<id> opens a tree page directly. simctl cannot tap, so
            // without this the one screen most of the app leads to cannot be
            // looked at or screenshotted at all.
            if let id = args.first(where: { $0.hasPrefix("-tree=") })?.dropFirst(6) {
                debugTree = String(id)
            }
            // -open=<kind>:<value> PUSHES a screen onto the current tab, which
            // is how a person actually arrives at one. Every route in this app
            // is reachable this way, so the screenshot sweep can look at all of
            // them rather than only at the four tab roots. Debug scaffolding
            // like -tab and -at, and the reason it exists is the sweep:
            // scripts/appsweep.py cannot tap, and a screen nobody can open is a
            // screen that ships unseen.
            if let spec = args.first(where: { $0.hasPrefix("-open=") })?.dropFirst(6),
               let route = Self.debugRoute(String(spec)) {
                path(tab).wrappedValue = [route]
            }
            if args.contains("-signin") {
                rootSheet = .signIn(.keepTree("The Last Elm of Stationsplein"))
            } else if args.contains("-paywall") {
                rootSheet = .paywall(.walkBeyondFirst)
            } else if let spec = args.first(where: { $0.hasPrefix("-begin=") })?.dropFirst(7) {
                // Debug scaffolding like -spot: Begin is only reachable by
                // tapping, and simctl has no finger. Routed through the
                // navigator because the catalogue is not in scope here.
                let parts = spec.split(separator: "|", maxSplits: 1).map(String.init)
                if parts.count == 2 {
                    navigator.beginWalk = .init(city: parts[0], name: parts[1])
                }
            } else if args.contains("-spot") || args.contains("-add") {
                // The centre button's sheet, openable without a finger.
                rootSheet = .spot(.add)
            } else if args.contains("-collect-tree") {
                rootSheet = .spot(.collect)
            }
            // -map is kept as an alias for the map tab so older recipes and
            // the sweep lists keep working after the map became tab 0.
            if args.contains("-map") { tab = 0 }
            // Every change to the collection follows the person to their
            // account, if they have one. Wired here rather than inside Saved so
            // the collection keeps knowing nothing about sign-in.
            saved.onMutate = { [account] id, entry in
                guard account.isSignedIn else { return }
                Task { await CloudSync.push(account: account, entry: entry, treeId: id) }
            }
            // An hour-old access token is the failure the website shipped with
            // for three weeks: saves stopped reaching the account and nothing
            // said so. Refreshing on launch means the app never gets there.
            if account.isSignedIn {
                await account.refreshIfNeeded()
                await CloudSync.merge(account: account, saved: saved)
            }
        }
    }
}

struct NothingNearby: View {
    let catalogue: Catalogue
    var body: some View {
        ContentUnavailableView {
            Label("No trees near you yet", systemImage: "tree")
        } description: {
            Text("We map \(catalogue.trees.count) trees in \(catalogue.citySlugs.count) places, and none is within fifty kilometres of here.")
        }
    }
}

@Observable
final class LocationProvider: NSObject, CLLocationManagerDelegate {
    private let manager = CLLocationManager()
    var coordinate: (lat: Double, lng: Double)?
    /// Exposed so the app can tell the three cases apart: never asked, refused,
    /// and allowed. They want different screens, and until now nothing could
    /// distinguish them because nothing read the status at all.
    var status: CLAuthorizationStatus

    override init() {
        status = manager.authorizationStatus
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyHundredMeters
        // Deliberately does NOT ask here. The system dialog is a single shot,
        // and asking it before anybody has been told why is how a refusal
        // becomes permanent. LocationPrimer asks, and calls request().
        if status == .authorizedWhenInUse || status == .authorizedAlways {
            manager.startUpdatingLocation()
        }
    }

    func request() {
        manager.requestWhenInUseAuthorization()
        manager.startUpdatingLocation()
    }

    func locationManager(_ m: CLLocationManager, didUpdateLocations locs: [CLLocation]) {
        guard let l = locs.last else { return }
        coordinate = (lat: l.coordinate.latitude, lng: l.coordinate.longitude)
    }

    func locationManagerDidChangeAuthorization(_ m: CLLocationManager) {
        status = m.authorizationStatus
        if status == .authorizedWhenInUse || status == .authorizedAlways {
            m.startUpdatingLocation()
        }
    }

    func locationManager(_ m: CLLocationManager, didFailWithError error: Error) {}
}

/// Every store the app has, handed to a view in one line.
///
/// SwiftUI sheets and covers do not inherit observables from the view they are
/// attached to, so each presentation used to repeat the list, and twice in two
/// days a presentation was one short and the app TRAPPED at launch rather than
/// degrading: SpotSheet gained an Account read on 2026-08-20 and a Sightings
/// read on 2026-08-21. A single modifier cannot be one short.
extension View {
    func appObjects(_ root: ContentView) -> some View {
        self.environment(root.saved)
            .environment(root.store)
            .environment(root.entitlement)
            .environment(root.account)
            .environment(root.nudge)
            .environment(root.navigator)
            .environment(root.units)
            .environment(root.sightings)
    }
}
