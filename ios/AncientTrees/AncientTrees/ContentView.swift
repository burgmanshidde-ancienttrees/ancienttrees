// The four verbs, one tab each: find, walk, collect, season.
//
// The tab bar is the product's own doctrine rather than a copy of AllTrails',
// though theirs is the evidence that verbs work as tabs: Verkennen, Opgeslagen,
// Navigeer, Activiteit. Three of their four map onto ours almost exactly.

import SwiftUI
import CoreLocation
import MapKit

struct ContentView: View {
    @State private var store = CatalogueStore()
    @State private var saved = Saved()
    @State private var entitlement = Entitlement()
    @State private var location = LocationProvider()
    @State private var account = Account()
    @State private var nudge = Nudge()
    @State private var rootSheet: RootSheet?
    @State private var primerAnswered = false
    /// One path per tab, so tapping the tab you are already on can empty it.
    /// Arrays rather than NavigationPath because clearing one is `= []` and
    /// because every route in this app is the same type.
    @State private var paths: [Int: [Route]] = [:]
    @State private var debugTree: String?

    /// Everything the root can put over the app. An enum rather than a pile of
    /// booleans so there is exactly one sheet modifier below.
    enum RootSheet: Identifiable, Equatable {
        case signIn(SignInReason)
        case paywall(Feature)
        var id: String {
            switch self {
            case .signIn(let r): "signin-" + r.id
            case .paywall(let f): "paywall-" + f.rawValue
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
                    if new == tab { paths[new] = [] }
                    tab = new
                })
    }

    /// One tab's navigation stack, with every destination in this app declared
    /// once rather than inline at ten separate call sites.
    private func stack<Root: View>(_ id: Int, _ cat: Catalogue,
                                   @ViewBuilder root: () -> Root) -> some View {
        NavigationStack(path: Binding(get: { paths[id] ?? [] },
                                      set: { paths[id] = $0 })) {
            root()
                .navigationDestination(for: Route.self) { route in
                    destination(route, cat)
                }
        }
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
                        .tabItem { Label("Map", systemImage: "map.fill") }

                    stack(1, cat) { ExploreView(catalogue: cat, origin: origin) }
                        .tag(1)
                        .tabItem { Label("Explore", systemImage: "square.grid.2x2") }

                    stack(2, cat) { SavedView(catalogue: cat, origin: origin) }
                        .tag(2)
                        .tabItem { Label("Saved", systemImage: "heart") }

                    stack(3, cat) { YouView(catalogue: cat) }
                        .tag(3)
                        .tabItem { Label("You", systemImage: "person.crop.circle") }
                }
                .environment(saved)
                .environment(store)
                .environment(entitlement)
                .environment(account)
                .environment(nudge)
                // ONE sheet modifier, driven by one optional, because SwiftUI
                // honours only one per view and stacking three meant the ask
                // silently never appeared. The ask is presented from the root so
                // that a tick on a tree page and a third save on the map land in
                // the same sheet rather than in two near-identical ones.
                .sheet(item: $rootSheet) { which in
                    switch which {
                    case .signIn(let reason):
                        SignInSheet(reason: reason, localCount: saved.savedCount)
                            .environment(account).environment(saved)
                    case .paywall(let feature):
                        PaywallView(feature: feature)
                            .environment(entitlement).environment(account).environment(saved)
                    }
                }
                .onChange(of: nudge.pending) { _, new in
                    if let new { rootSheet = .signIn(new); nudge.pending = nil }
                }
            } else if let err = store.loadError {
                ContentUnavailableView("Something is wrong with the catalogue",
                                       systemImage: "exclamationmark.triangle",
                                       description: Text(err))
            } else {
                ProgressView()
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
            if args.contains("-signin") {
                rootSheet = .signIn(.keepTree("The Last Elm of Stationsplein"))
            } else if args.contains("-paywall") {
                rootSheet = .paywall(.walkBeyondFirst)
            }
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
