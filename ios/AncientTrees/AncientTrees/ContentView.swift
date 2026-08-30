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
    @State fileprivate var saved: Saved = {
        let s = Saved()
        s.seedFromLaunchArguments()
        return s
    }()
    @State fileprivate var entitlement = Entitlement()
    /// The opening frame, on a cold start only. A `@State` on the root is
    /// exactly that: the root is built once per launch and never again when
    /// somebody comes back from the home screen.
    @State private var showingCover = !ProcessInfo.processInfo.arguments.contains("-no-cover")
    /// Reporting and blocking, which the social half cannot ship without.
    @State fileprivate var moderation = Moderation()
    /// What this account has already said about a tree, read from the account
    /// rather than remembered by this phone.
    @State fileprivate var myVotes = MyVotes()
    @State private var location = LocationProvider()
    @State fileprivate var account = Account()
    @State fileprivate var nudge = Nudge()
    @State fileprivate var navigator = Navigator()
    @State fileprivate var units = Units()
    @State fileprivate var sightings = Sightings()
    /// How many people saved each tree, counted by the server because a client
    /// can only see its own rows. Empty until Hidde runs supabase/like-counts.sql.
    @State fileprivate var voteCounts = VoteCounts()
    /// Who you are and who you follow, opened on his 2026-08-26 yes.
    @State fileprivate var profiles = Profiles()
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
    /// Profile keeps its own stack like the others, or pushing from it would
    /// land in the collection's history and Back would leave the wrong tab.

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
        case spot(CollectSheet.Mode)
        var id: String {
            switch self {
            case .signIn(let r): "signin-" + r.id
            case .paywall(let f): "paywall-" + f.rawValue
            case .spot(let m): "spot-" + m.rawValue
            }
        }
    }
    /// The pending "which maps app" question, owned in one place so the dialog
    /// below is the app's only one.
    @State private var directionsAsk = DirectionsAsk.shared

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
        // The pushed place map, which is otherwise only reachable by tapping
        // the preview on a city or a country page. Same rule as every other
        // argument here: a screen no argument can open is a screen that ships
        // unlooked at.
        case "citymap": return .placeMap(.city(value))
        case "countrymap": return .placeMap(.country(value))
        // A single tree's own map, otherwise reached only by tapping the inset
        // on its page. Added 2026-08-29 so the recentre test can reach it:
        // it was the last full map in the app no argument could open, which is
        // exactly the condition under which a control goes missing unnoticed.
        case "treemap": return .treeMap(value)
        case "profile": return .profile
        // A tree of YOURS, which was the last screen here no argument could
        // open. Sightings.demoIDs are the two that -mine-demo always creates.
        case "mine": return UUID(uuidString: value).map { Route.mine($0) }
        case "walk":
            let parts = value.split(separator: "|", maxSplits: 1).map(String.init)
            guard parts.count == 2 else { return nil }
            return .walk(city: parts[0], name: parts[1])
        default: return nil
        }
    }

    private var origin: (lat: Double, lng: Double) {
        // Live fix, then the last one this phone had, then Dam square as the
        // first-launch-anywhere default. See LocationProvider.remembered.
        debugOrigin ?? location.coordinate ?? LocationProvider.remembered
            ?? (lat: 52.3731, lng: 4.8922)   // Dam square
    }

    /// Shown once, and only when iOS has genuinely not been asked yet.
    private var needsPrimer: Bool {
        guard debugOrigin == nil || ProcessInfo.processInfo.arguments.contains("-primer") else { return false }
        // -refused judges the recovery sheet, which belongs over the MAP. The
        // primer answers the same question one step earlier and would sit
        // behind it in every sweep frame, which is not the screen anybody
        // meets: by the time this sheet exists, iOS has been asked and refused.
        if ProcessInfo.processInfo.arguments.contains("-refused") { return false }
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
                    // The camera is no longer a slot to intercept: it sits on
                    // its own disc beside the bar and calls openCollect()
                    // directly (Hidde, 2026-08-26). -tab=2 kept meaning the
                    // collect sheet for one release so older launch arguments
                    // and deep links still land somewhere sensible.
                    if new == TabBar.collectTag { openCollect(); return }
                    if new == tab { clearPath(new) }
                    // ONLY A REAL SWITCH. Tapping the tab you are already on
                    // empties that tab's stack, which is a different action
                    // wearing the same gesture, and counting it as a visit made
                    // Hidde's first session read as two Discovers a second
                    // apart (2026-08-30, the first data this app ever produced).
                    if new != tab {
                        Measure.event("tab", ["tab": TabBar.items.indices.contains(new)
                            ? TabBar.items[new].title : String(new)])
                    }
                    tab = new
                })
    }

    /// Nothing of somebody's collection survives on a phone nobody is signed
    /// in to. The stores keep the data on the SERVER; this only empties the
    /// copy here, which is why both calls are named forgetLocally.
    private func forgetIfSignedOut() {
        guard !account.isSignedIn else { return }
        saved.forgetLocally()
        profiles.forgetLocally()
        // AND THE TREES SOMEBODY ADDED THEMSELVES (Hidde, 2026-08-29: "als je
        // uitlogt moeten de bomen die je hebt toegevoegd niet meer zichtbaar
        // zijn op de kaart en in de lijsten", and "ik kan ook een boom removen
        // terwijl ik uitgelogd ben"). They were the loudest leftover of the
        // three, because they carry a photograph and they sit on the map.
        // Only the ones the account already holds; Sightings.forgetLocally()
        // says why.
        sightings.forgetLocally()
    }

    /// The centre button, gated.
    ///
    /// Collecting writes a sighting, a photograph and, when the tree is one we
    /// do not have, a row in the submissions table that the reply mail is
    /// addressed to. All three are things kept on somebody's behalf, and Hidde
    /// closed the soft wall on all of it on 2026-08-25. Gating the heart and
    /// leaving the camera open would have been the same hole one button along.
    ///
    /// The launch-argument route into this sheet is deliberately NOT gated, so
    /// appsweep can still photograph the collect screens on a simulator that
    /// has never signed in.
    private func openCollect() {
        guard account.isSignedIn else {
            nudge.require(.general)
            return
        }
        rootSheet = .spot(.collect)
    }

    /// One tab's navigation stack, with every destination in this app declared
    /// once rather than inline at ten separate call sites.
    private func stack<Root: View>(_ id: Int, _ cat: Catalogue,
                                   @ViewBuilder root: () -> Root) -> some View {
        NavigationStack(path: path(id)) {
            root()
                // The native bar is off everywhere: TabBar.swift draws ours,
                // because iOS puts its capsule around icon AND label and the
                // reference puts it behind the icon alone.
                .toolbar(.hidden, for: .tabBar)
                .navigationDestination(for: Route.self) { route in
                    destination(route, cat)
                        // A pushed page is a reading page; the bar does nothing
                        // there and AllTrails hides it too. Back is the way out.
                        .toolbar(.hidden, for: .tabBar)
                        // And anything on it that reserves room for the bar,
                        // which is the sheet, is told there is none.
                        .environment(\.floatingBarDepth, 0)
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
                TreeDetail(tree: t, catalogue: cat, origin: origin)
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
        case .mine(let id):
            if let s = sightings.all.first(where: { $0.id == id }) {
                TreeDetail(tree: sightings.asTree(s), mine: s, catalogue: cat, origin: origin)
            } else {
                ContentUnavailableView("That tree is gone", systemImage: "leaf")
            }
        case .profile:
            ProfileView(catalogue: cat)
        case .collectionMap:
            CollectionMapPage(catalogue: cat)
        case .placeMap(let place):
            PlaceMapPage(place: place, catalogue: cat)
        case .treeMap(let id):
            if let t = cat.tree(id) {
                TreeMapPage(tree: t, catalogue: cat)
            } else {
                ContentUnavailableView("That tree is gone", systemImage: "leaf")
            }
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
                    // ONE line weight across the whole bar, nothing filled,
                    // and the selection said by the pill and the colour alone.
                    //
                    // This reverses the 2026-08-22 decision to fill the
                    // selected symbol, which came from Hidde's Komoot
                    // screenshots. On 2026-08-24 he sent an AllTrails frame
                    // and said the bar was "afschuwelijk lelijk": filling
                    // `map` turns it into a solid green blob next to a
                    // hairline magnifying glass, so the bar carries two
                    // drawing styles at once. AllTrails uses one outline
                    // weight for all four and lets the pill do the selecting,
                    // and that is what he asked for, precisely.
                    //
                    // Symbols are the lightest member of one family for the
                    // same reason. `map` for the map, `magnifyingglass` for
                    // search (AllTrails' own), `camera` for the act of
                    // collecting (Hidde, 2026-08-23: a camera and never a
                    // plus) and `checkmark.circle` for the ones ticked off.
                    stack(0, cat) {
                        if let id = debugTree, let t = cat.tree(id) {
                            TreeDetail(tree: t, catalogue: cat, origin: origin)
                        } else {
                            MapTab(catalogue: cat, origin: origin,
                                   located: location.coordinate != nil || debugOrigin != nil,
                                   locationDenied: location.status == .denied || location.status == .restricted,
                                   onUseMyLocation: { location.request() })
                        }
                    }
                        .tag(0)
                        .tabItem { Label("Map", systemImage: "map")
                            .environment(\.symbolVariants, .none) }

                    stack(1, cat) { HomeView(catalogue: cat, origin: origin) }
                        .tag(1)

                    // MY TREES, which is the Collection and the account in one
                    // place (Hidde, 2026-08-26). Polarsteps is the reference he
                    // gave: your own page carries the map of what you have
                    // done, your numbers, and your things, with settings behind
                    // a gear in the corner rather than as a destination of its
                    // own. Profile stopped being a tab the same day.
                    stack(2, cat) { CollectView(catalogue: cat, origin: origin) }
                        .tag(2)
                }
                // Outline icons that stay outline when selected, colour doing
                // the selecting (Careem is Hidde's reference; Airbnb does the
                // same). The .none variant sits on each Label because iOS
                // applies its automatic .fill inside the tab item, underneath
                // an environment set on the TabView itself.
                .safeAreaInset(edge: .bottom, spacing: 0) {
                    // Gone on a pushed page, which the native bar already did
                    // and which AllTrails does too: a reading page has no bar
                    // and back is the way out. An EmptyView reserves no space,
                    // so the page grows into it rather than leaving a gap.
                    // ALWAYS IN THE LAYOUT, hidden rather than removed
                    // (Hidde, 2026-08-26: "de floating menu verdwijnt nu als
                    // ik van settings terug kom naar de andere schermen").
                    //
                    // It used to be inserted and removed from the safe area,
                    // and a safeAreaInset that appears and disappears is a
                    // known way to end up with neither: come back from a
                    // pushed page and the inset does not always come back with
                    // you. Keeping one bar and giving it no height on a pushed
                    // page cannot fail that way, because there is nothing to
                    // re-insert.
                    let showing = path(tab).wrappedValue.isEmpty
                    // THE INSET ALWAYS HAS CONTENT, and the content is either
                    // the bar or nothing at all.
                    //
                    // Two failures, one line apart. An `if` with no `else`
                    // makes the inset itself come and go, and it does not
                    // always come back: that is the bar vanishing after
                    // settings. Keeping the bar and merely making it
                    // transparent leaves it in the accessibility tree, so
                    // VoiceOver reads three tabs that are not there and the
                    // layout gate finds the tree page's own buttons buried
                    // under a bar nobody can see. This has an else, so the
                    // inset never disappears, and it swaps the bar out rather
                    // than dimming it, so nothing invisible is left behind.
                    if showing {
                        TabBar(selected: tab,
                               select: { tabSelection.wrappedValue = $0 },
                               collect: { openCollect() })
                    } else {
                        Color.clear.frame(height: 0)
                    }
                        // AND GONE FROM THE TREE, not merely transparent. A
                        // bar with no height, no opacity and no hit testing is
                        // invisible to a person and still present to anything
                        // reading the screen: VoiceOver would announce three
                        // tabs that are not there, and the layout gate reported
                        // the tree page's own buttons as buried underneath it
                        // (2026-08-27). Both are the same mistake, which is
                        // hiding something from eyes only.

                }
                .appObjects(self)
                .onChange(of: navigator.collectNearby) { _, want in
                    if want { openCollect(); navigator.collectNearby = false }
                }
                .onChange(of: navigator.push) { _, new in
                    guard let new else { return }
                    path(tab).wrappedValue.append(new)
                    navigator.push = nil
                }
                .onChange(of: navigator.selectTab) { _, new in
                    // ONLY A TAB THAT EXISTS. A selection matching no tag
                    // leaves the TabView showing its first page with our bar
                    // gone, which is a dead end: no bar, no back button, and
                    // the tab it thinks it is on is not on screen. One stale
                    // call site did exactly that for a day (Profile's identity
                    // row still asked for tab 3), and the cost of the guard is
                    // a comparison.
                    if let new { if (0...2).contains(new) { tab = new }
                                 navigator.selectTab = nil }
                }
                .onChange(of: navigator.showCityOnMap) { _, new in
                    // Same handling as showOnMap below: pop the map's stack and
                    // go there. MapTab frames the city and clears the request.
                    if new != nil { mapPath = []; tab = 0 }
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
                            CollectSheet(catalogue: cat, origin: origin, mode: mode)
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
                // WHICH MAPS APP, asked once, from the ROOT. Presented here
                // rather than from the button because Take me there exists on a
                // tree page, on the pushed map and inside walk mode, and a
                // dialog attached to each would be three to keep in step.
                //
                // AN ALERT, NOT A confirmationDialog, and the first version was
                // the second one. iOS 26 draws a confirmationDialog as a
                // floating card and silently drops every button carrying
                // role: .cancel: the sweep photographed this question with
                // Apple Maps, Google Maps and no way out, which is the same
                // fault a destructive confirmation shipped with on 2026-08-27.
                // Presenting from the root was supposed to avoid it and does
                // not. An alert renders every button it is given.
                .alert(
                    "Open directions in",
                    isPresented: Binding(get: { directionsAsk.pending != nil },
                                         set: { if !$0 { directionsAsk.pending = nil } })
                ) {
                    ForEach(Directions.MapsApp.allCases) { app in
                        Button(app.label) { directionsAsk.answer(app) }
                    }
                    Button("Cancel", role: .cancel) { directionsAsk.pending = nil }
                } message: {
                    Text("You can change this in Settings.")
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
        // THE OPENING FRAME, and it is his, asked for four times before I
        // stopped arguing (2026-08-29: "als in elke keer als je de app opent
        // toon je een andere", and then "hier hebben we toch net een gesprek
        // over gehad?").
        //
        // What I kept answering was about the wrong thing. An iOS LAUNCH
        // SCREEN is a storyboard rendered before the app runs: static, one
        // image, no code, so it genuinely cannot rotate. A cover the APP draws
        // is a different object and can do anything, which is what he was
        // describing all along.
        //
        // Kept short and cheap on purpose, because the objection underneath my
        // arguing is still true: somebody opening this app may be standing
        // outside. It goes after 1.4 seconds, any tap takes it away sooner, and
        // it never appears on a return from the background, only on a cold
        // start. And it shows the same photograph Discover is wearing this
        // launch, so the two are one thing rather than two decorations.
        .overlay {
            if showingCover, let photo = Heroes.image {
                HeroCover(photo: photo) { withAnimation(.easeOut(duration: 0.35)) { showingCover = false } }
                    .transition(.opacity)
                    .zIndex(2)
            }
            if needsPrimer {
                LocationPrimer(treeCount: store.catalogue?.trees.count ?? 0,
                               onAllow: { primerAnswered = true; location.request() },
                               onSkip: { primerAnswered = true })
                    .transition(.opacity)
            }
        }
        // 2.4 SECONDS, and the number comes from reading rather than from a
        // convention, because neither platform publishes one for this.
        //
        // Looked up 2026-08-30 (Hidde: "die toont te kort - kun je even
        // benchmarken wat een normale lengte is"). Apple's Launching guidance
        // names this exact object and allows it: "If you need a splash screen,
        // consider displaying it at the beginning of your onboarding flow. If
        // you don't provide an onboarding experience, you might display your
        // splash screen as soon as launching completes." What it forbids is
        // dressing up the LAUNCH SCREEN, which "isn't an opportunity for
        // artistic expression". Android publishes 1,000 ms, but that is the cap
        // on its system splash's icon animation, not on a branded cover.
        //
        // So the honest constraint is the sentence. "Trees worth the walk,
        // wherever you are." is seven words, which is about 1.7 seconds of
        // reading at an ordinary pace, and that clock only starts once the eye
        // has found the words. At 1.4 it was gone before it could be read,
        // which is exactly what he saw.
        .task {
            try? await Task.sleep(for: .seconds(2.4))
            withAnimation(.easeOut(duration: 0.4)) { showingCover = false }
        }
        .animation(.easeInOut(duration: 0.2), value: needsPrimer)
        // SIGNING OUT EMPTIES THIS PHONE (Hidde, 2026-08-29: "de favourites en
        // seen moet ook leeg wanneer niet ingelogd", and beside it "profielfoto
        // moet weg als je uitlogt net als alle hartjes op de thumbnails").
        //
        // Saving and collecting have needed an account since 2026-08-25, so a
        // filled heart on a signed-out phone is a leftover from a session that
        // has ended, and it is the loudest kind: it appears on every card, on
        // the pins, and as a name and a picture over the settings page. The app
        // was still wearing somebody's face after they left.
        //
        // Nothing is deleted anywhere but here. The collection lives in the
        // account and comes back on the next sign-in, which is why both calls
        // are named forgetLocally rather than clear.
        //
        // Your own photographs stay ONLY while the account has not got them
        // yet. That exemption used to be blanket, on the sound half of this
        // reasoning: a picture somebody took under a tree is not recoverable by
        // signing back in. The unsound half was applying it to photographs the
        // server demonstrably holds, which left a signed-out phone showing
        // somebody's trees on the map and letting anyone delete them. It is
        // asked per sighting now, and `syncedAt` is the answer.
        .onChange(of: account.isSignedIn) { _, _ in forgetIfSignedOut() }
        .task {
            // AT LAUNCH TOO, not only on the transition (Hidde, 2026-08-29:
            // "ik zie nog steeds favoriet een vink icoon op de map waar niet
            // ingelogd", and "ook seen op thumbnails").
            //
            // The onChange above fires when somebody signs OUT, and that was
            // the whole of it, so a phone that had entries on disk and then
            // launched signed out kept every heart and tick for ever: nothing
            // ever transitioned. A session can also end without a sign-out at
            // all, when a refresh token is refused after three weeks away.
            //
            // Safe here because Account.restore() reads the Keychain
            // synchronously in its init, so isSignedIn is already right on the
            // first frame rather than a moment later.
            forgetIfSignedOut()
            await store.loadBundled()
            // Ask whether anything changed. A few dozen bytes, and it is the
            // difference between an app that follows the database and an app
            // frozen at whatever shipped.
            Task { await store.refresh() }
            // Crashes and hangs, from Apple's own MetricKit rather than an SDK
            // (Kit/Diagnostics.swift). Registering at launch is the whole of
            // the app's part: the system hands over what it gathered the next
            // time the app opens, and only on a real device.
            Diagnostics.shared.start()
            // What people do, to our own PostHog project (Kit/Measure.swift).
            // The queue goes first so anything stranded by a wood with no
            // signal is filed before today adds to it.
            Measure.flush()
            Measure.event("app_open")
            // The thumbs' figures, once per launch and never per card: the
            // whole table is a few thousand short rows and a request inside a
            // scrolling list is a stutter.
            Task { await voteCounts.loadOnce() }
            // A TOKEN THAT IS STILL GOOD, or none at all.
            //
            // This read the stored token straight out, and those live an hour,
            // so on every launch after the first hour the request came back 401
            // and the profile stayed empty: no name, no picture, and it looked
            // exactly like a picture that had never saved (Hidde, 2026-08-27:
            // "ik heb de app opnieuw opgestart en hij heeft mn profielfoto niet
            // opgeslagen"). It had saved. It could not be read back.
            //
            // Falling through to nil rather than a stale token matters too: a
            // profile is readable by anybody signed in OR not, so with no token
            // the request still succeeds on the publishable key, where an
            // expired one makes PostgREST refuse the whole call.
            Task {
                let token = await account.freshToken()
                await profiles.load(userId: account.session?.userId, token: token)
            }
            // Who you have blocked, from the server rather than only from this
            // phone: a reinstall or a second phone has to start where the last
            // one left off, or a block is not a block.
            Task {
                guard let token = await account.freshToken() else { return }
                await moderation.load(me: account.session?.userId, token: token)
            }
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
            } else if args.contains("-spot") || args.contains("-add") || args.contains("-collect") {
                // The centre button's sheet, openable without a finger.
                rootSheet = .spot(.collect)
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
                // And the trees somebody added themselves, which until today
                // lived on one phone and nowhere else (Hidde, 2026-08-27:
                // "niemand wil een backup my trees knop, je wilt gewoon dat dit
                // automatisch goed gaat"). Photographs included: the words on
                // their own would bring back a list of names with no pictures,
                // which is most of what was lost rather than all of it.
                // ANYTHING PARKED AT THE LAST SIGN-OUT FIRST, so the merge's
                // push carries it and the account finally gets the copy it
                // never had. Signing back in is what these were kept for.
                sightings.restorePending()
                await SightingSync.merge(account: account, sightings: sightings)
            }
            // Every later change goes the same way. Set here because this is
            // the only place that knows about both, so Sightings itself keeps
            // knowing nothing about the network.
            Sightings.syncOne = { [account, sightings] s in
                Task { await SightingSync.push(account: account, sightings: sightings, sighting: s) }
            }
            Sightings.syncGone = { [account] id in
                Task { await SightingSync.remove(account: account, id: id) }
            }
            // Kilometres or miles follows the account too, so it does not stay
            // behind on an old phone.
            Units.sync = { [account, profiles] u in
                Task {
                    guard let t = await account.freshToken(),
                          let uid = account.session?.userId else { return }
                    await profiles.saveUnits(u == .metric ? "km" : "mi",
                                             userId: uid, token: t)
                }
            }
            // And the votes this account has already cast, written into the
            // same place the tree pages already read, so the local copy becomes
            // a cache of the account rather than the only copy there is.
            if account.isSignedIn {
                await myVotes.load(account: account)
                for (tree, vote) in myVotes.byTree {
                    UserDefaults.standard.set(vote, forKey: "at_worthit_\(tree)")
                }
                if let remote = profiles.me?.units {
                    units.unit = remote == "mi" ? .imperial : .metric
                }
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

    /// The last fix we ever had, kept across launches.
    ///
    /// Hidde opened the app in Baarn on 2026-08-25 and the map opened on
    /// Amsterdam. The Info.plist key that broke this in August is present and
    /// the dialog does appear, so the cause is the other half: a cold start
    /// draws the map before the first fix lands, and a refusal leaves
    /// `coordinate` nil forever. Both fell through to Dam square, which is not
    /// a neutral default, it is a wrong answer stated confidently in a product
    /// whose one unforgivable error is telling somebody they are somewhere
    /// they are not.
    ///
    /// A remembered coordinate is honest in a way the hardcoded one is not: it
    /// is where this phone actually was, so the map opens on the trees near
    /// home rather than near our office.
    private static let key = "ancienttrees.last_fix"

    static var remembered: (lat: Double, lng: Double)? {
        let d = UserDefaults.standard
        guard let a = d.array(forKey: key) as? [Double], a.count == 2 else { return nil }
        return (lat: a[0], lng: a[1])
    }

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

    /// Twenty metres, or nothing happens.
    ///
    /// This is an @Observable property that half the app reads through `origin`,
    /// so every published change rebuilds the home screen, the collection and
    /// the map's list. Core Location delivers a fix every second or two while
    /// somebody walks, each a metre or two from the last, and every one of them
    /// was a full re-render and a UserDefaults write. It is also half of why the
    /// species grid appeared to shuffle by itself on 2026-08-25: the grid was
    /// not deterministic and this rebuilt it constantly.
    ///
    /// Twenty metres is well inside the accuracy we ask for (hundred metres) and
    /// far below the distances any of this copy talks about.
    private static let minMove = 20.0

    func locationManager(_ m: CLLocationManager, didUpdateLocations locs: [CLLocation]) {
        guard let l = locs.last else { return }
        let new = (lat: l.coordinate.latitude, lng: l.coordinate.longitude)
        if let old = coordinate, Geo.km(old, new) * 1000 < Self.minMove { return }
        coordinate = new
        UserDefaults.standard.set([new.lat, new.lng], forKey: Self.key)
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
/// degrading: the collect sheet gained an Account read on 2026-08-20 and a Sightings
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
            .environment(root.voteCounts)
            .environment(root.profiles)
            .environment(root.moderation)
    }
}
