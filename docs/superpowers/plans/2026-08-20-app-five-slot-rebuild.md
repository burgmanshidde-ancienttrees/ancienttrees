# App five-slot rebuild — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the iOS app's screen layer to the bar Hidde set on 2026-08-20 (Explore with the map behind AllTrails' pill, Saved, Spot as the centre button, Collect, Profile), copying AllTrails' composition the way the website does, while keeping the engine (Kit/, AncientTreesKit, sync, accounts, catalogue) untouched.

**Architecture:** ContentView gains a fifth slot whose "tab" is not a destination but a sheet (the Strava/Untappd centre-button pattern done with a plain TabView: selecting the Spot tab reverts the selection and presents the sheet). Explore hosts HomeView and MapTab as two modes of one tab behind a floating pill. Saved and Spot are new screens; Collect gets a day-zero state; every list card converges on the AllTrails card anatomy that TreeCard + MapInset already implement.

**Tech Stack:** SwiftUI, existing Kit stores (`Saved`, `Entitlement`, `Account`, `CatalogueStore`, `Submissions`, `Geo`), XCTest (`AncientTreesTests`, `AncientTreesUITests`). No new dependencies (hard rule 5).

## Global Constraints

- **The engine is kept**: nothing under `ios/AncientTreesKit/` or `ios/AncientTrees/AncientTrees/Kit/` changes semantics; UI-facing additions only.
- **Free/paid split is settled and untouched** (DECISIONS.md 2026-08-20 morning): ticking is free; photo, GPS seal and badges are Plus; GPS proximity is a bonus, never a gate; the nearest walk stays free (`Feature.walkBeyondFirst`).
- **Copy rules**: English, no em dashes, no builder-speak (never explain our own publishing/licence rules to the reader), no forever-promises. The photo placeholder line becomes "No photograph of this tree yet."
- **Style**: `Brand` palette and Gabarito via `Style.swift`; the one press-colour is `Brand.moss`; kill every default blue with `.tint(Brand.moss)` at the root. AllTrails composition per `ALLTRAILS_TEARDOWN.md`.
- **Verification**: no CI for the app. Every task ends with: build for iPhone 17 Pro simulator, install, screenshot the changed screen (light mode is enough per task; a final sweep covers dark), and run the test bundle locally. Build command as in `environment-setup` memory (`xcodebuild -scheme AncientTrees -destination 'platform=iOS Simulator,name=iPhone 17 Pro' -derivedDataPath <scratchpad>/dd build`).
- **Day-zero rule (Hidde, this session)**: the middle three slots must never feel empty. Saved and Collect open with suggestions; Spot always shows both outcomes.
- **Commit per task**, message in the repo's voice; append one LOG.md entry at the end of the whole plan, not per task.

---

### Task 1: The five-slot bar

**Files:**
- Modify: `ios/AncientTrees/AncientTrees/ContentView.swift`
- Create: `ios/AncientTrees/AncientTrees/Screens/SpotSheet.swift` (stub in this task, real flow in Task 4)
- Test: `ios/AncientTrees/AncientTreesUITests/AncientTreesUITests.swift`

**Interfaces:**
- Consumes: existing `stack(_:_:root:)`, `RootSheet`, path arrays.
- Produces: tab ids `0 Explore, 1 Saved, 2 Spot (sheet only), 3 Collect, 4 Profile`; `@State var spotPresented: Bool`; `-tab=N` keeps working with the new ids; `-spot` launch arg opens the Spot sheet (simctl cannot tap).

- [ ] **Step 1: Failing UI test** — assert the five tab labels exist and that selecting Spot presents a sheet rather than switching screens:

```swift
func testFiveSlotBar() throws {
    let app = XCUIApplication()
    app.launchArguments = ["-at=52.3731,4.8922"]
    app.launch()
    for label in ["Explore", "Saved", "Spot", "Collect", "Profile"] {
        XCTAssertTrue(app.tabBars.buttons[label].waitForExistence(timeout: 10), label)
    }
    app.tabBars.buttons["Spot"].tap()
    XCTAssertTrue(app.otherElements["spot-sheet"].waitForExistence(timeout: 5))
    // The bar must still be on Explore underneath: dismiss and check.
    app.swipeDown(velocity: .fast)
    XCTAssertTrue(app.tabBars.buttons["Explore"].isSelected)
}
```

- [ ] **Step 2: Run it, expect FAIL** (`xcodebuild test -only-testing:AncientTreesUITests/AncientTreesUITests/testFiveSlotBar ...`).
- [ ] **Step 3: Implement.** In `ContentView`: rename path arrays to `explorePath, savedPath, collectPath, profilePath`; add `spotPresented`; the selection binding becomes the centre-button pattern:

```swift
private var tabSelection: Binding<Int> {
    Binding(get: { tab },
            set: { new in
                if new == 2 { spotPresented = true; return }   // Spot never becomes the tab
                if new == tab { clearPath(new) }
                tab = new
            })
}
```

Tab items: `0 ExploreTab` (Task 2), `1 SavedView` (Task 3, stub `Text` first), `2 Color.clear.tabItem { Label("Spot", systemImage: "plus.circle.fill") }`, `3 CollectView`, `4 ProfileView`. Present `SpotSheet` from the root (`.sheet(isPresented: $spotPresented)`), stub body carries `.accessibilityIdentifier("spot-sheet")` on the outer container (on the container, never inside a card, per the ios-app-workflow lesson). Add `-spot` to the debug args next to `-signin`. `.tint(Brand.moss)` on the TabView.
- [ ] **Step 4: Run the UI test, expect PASS.**
- [ ] **Step 5: Screenshot each tab** (`-tab=0/1/3/4` plus `-spot`), look at them, then commit: `The bar becomes five slots, and Spot is a button, not a place`.

### Task 2: Explore = Home with the map behind the pill

**Files:**
- Modify: `ios/AncientTrees/AncientTrees/ContentView.swift` (tab 0 root)
- Create: `ios/AncientTrees/AncientTrees/Screens/ExploreTab.swift`
- Test: UI test `testPillSwapsListAndMap`

**Interfaces:**
- Consumes: `HomeView(catalogue:origin:)`, `MapTab(catalogue:origin:located:locationDenied:onUseMyLocation:)`, `navigator.showOnMap`.
- Produces: `ExploreTab(catalogue:origin:located:locationDenied:onUseMyLocation:)` with `@State private var showsMap: Bool`; `navigator.showOnMap` now selects tab 0 AND sets `showsMap = true`.

- [ ] **Step 1: Failing UI test** — pill labelled "Map" exists on Explore; tapping it shows the map (assert `app.otherElements["explore-map"]`), the pill now reads "List"; tapping again returns the shelves.
- [ ] **Step 2: Run, expect FAIL.**
- [ ] **Step 3: Implement `ExploreTab`:** a `ZStack(alignment: .bottom)` holding `HomeView` or `MapTab` by `showsMap`, and the floating pill (AllTrails': capsule, `Brand.ink` ground in light / surface in dark, icon + one word, centred above the bar):

```swift
Button { withAnimation(.snappy) { showsMap.toggle() } } label: {
    Label(showsMap ? "List" : "Map", systemImage: showsMap ? "list.bullet" : "map.fill")
        .font(.brand(15, .bold))
        .padding(.horizontal, 18).padding(.vertical, 11)
        .background(Capsule().fill(Brand.ink))
        .foregroundStyle(Brand.ground)
}
.padding(.bottom, 8)
.accessibilityIdentifier("explore-pill")
```

Remove the old Map tab from `ContentView`; route `navigator.showOnMap` to `{ tab = 0; explore shows map }` (pass a binding or put `showsMap` in `Navigator`). Delete the `Label("Home", ...)` title copy inside HomeView if it renders a literal "Home" heading; the shelf content is the heading.
- [ ] **Step 4: Run test, expect PASS.** Also rerun the two existing navigation UI tests that caught the dictionary-binding bug; the path arrays changed names.
- [ ] **Step 5: Screenshots** of Explore shelves, Explore map, and a tree card tap from each mode. Commit: `Home and the map become one tab, with AllTrails' pill between them`.

### Task 3: Saved, and it is never empty

**Files:**
- Create: `ios/AncientTrees/AncientTrees/Screens/SavedView.swift`
- Test: unit test in `AncientTreesTests` for the suggestion picker; UI test `testSavedShowsSuggestionsWhenEmpty`

**Interfaces:**
- Consumes: `Saved.entries`, `Saved.isVisited`, `TreeCard`, `Geo.km`, `catalogue.walks(inCity:)`, `Entitlement.allows(.walkBeyondFirst)`.
- Produces: `SavedView(catalogue:origin:)`; `func savedSuggestions(catalogue:origin:excluding:) -> [Tree]` (pure, testable: nearest trees with an approved photo, best-first, max 6).

- [ ] **Step 1: Failing unit test:** suggestions exclude already-saved ids, prefer photo-carrying trees, are ordered by distance, cap at 6.
- [ ] **Step 2: Run, expect FAIL.**
- [ ] **Step 3: Implement.** Filled state: "To visit" (saved, not visited) as TreeCards with distance, then "Walks you saved" when walk-saving lands later (not in this plan; no empty section renders). Day-zero state per Hidde ("daar moeten suggesties in staan iig in saved"): header "Nothing saved yet. Start with these." followed by the suggestion cards, each with its heart live, plus the nearest walk card (free one) beneath. No zeros, no grey ghosts.
- [ ] **Step 4: Tests pass; screenshot day-zero and a filled state (save two trees via UI test or `-at` + taps in simulator is impossible: use a debug arg `-seed-saves=ams_004,ams_007` added to ContentView's task block, debug scaffolding like `-tab`).**
- [ ] **Step 5: Commit:** `Saved exists, and its empty state is suggestions, not zeros`.

### Task 4: Spot, one screen, both outcomes

**Files:**
- Modify: `ios/AncientTrees/AncientTrees/Screens/SpotSheet.swift`
- Modify: `ios/AncientTrees/AncientTrees/Kit/Submissions.swift` (one new `Kind` case `newTree` if absent; wire coordinates into `Draft.locationHint`)
- Test: unit test for the split logic; UI test `testSpotAlwaysOffersBothOutcomes`

**Interfaces:**
- Consumes: `origin`, `catalogue.trees` + `Geo.km`, `Saved.toggleVisited`, `Submissions.send`, `Entitlement` (photo upload stays Plus-gated inside Collect proof, NOT here: a submission photo is a contribution and free — but photo capture UI needs Hidde's storage yes, so this task ships the text submission and a "photo comes later" note in the plan, not in the copy).
- Produces: `SpotSheet(catalogue:origin:)`; `func spotSplit(origin:trees:) -> (nearby: [Tree], canAdd: Bool)` with `nearby` = trees within 400 m, nearest first, max 5.

- [ ] **Step 1: Failing unit test** for `spotSplit`: at Wertheimpark it returns ams_004 first; in Baarn it returns empty nearby.
- [ ] **Step 2: Run, expect FAIL.**
- [ ] **Step 3: Implement the sheet.** Nearby non-empty: "Which tree did you find?" + rows (photo thumb, name, species, metres) where the row's tick calls `saved.toggleVisited(id)` and dismisses with a stamp toast; ALWAYS beneath: "Standing before a tree we miss? Add it" leading to the add-form (two fields: what makes it special, optional name/species; the line "Your location rides along, so we know which tree."; sends `Submissions.Draft(kind: .newTree, locationHint: "lat,lng ±accuracy", why: text)`; confirmation copy "We check every tree before it goes on the map. Thank you."). Nearby empty: the add-form is the headline, distant known trees not shown. First-use coachmark (one `@AppStorage("spotCoachShown")` bool): "Standing before a tree? Tick it off, or add it if we miss it."
- [ ] **Step 4: Tests pass; screenshots of both states (`-at` near Wertheimpark and `-at=52.0,5.9`).**
- [ ] **Step 5: Commit:** `Spot: tick what we map, add what we miss, GPS decides the order`.

### Task 5: Collect opens with a mission, not zeros

**Files:**
- Modify: `ios/AncientTrees/AncientTrees/Screens/Collect.swift`
- Test: UI test `testCollectDayZeroShowsMission`

**Interfaces:**
- Consumes: `savedSuggestions` (Task 3) for the nearest good tree; `Saved.visitedCount`.

- [ ] **Step 1: Failing UI test:** with no visits, Collect shows an element `collect-mission` naming one real tree, and does NOT render the "0 of 18" species grid as its opening block.
- [ ] **Step 2: Run, expect FAIL.**
- [ ] **Step 3: Implement.** Day zero: one big card, AllTrails anatomy (photo, map inset, four facts), header "Your first tree is 400 m away", primary "Show the way" (pushes `.tree(id)`), plus a three-line explainer of the game (tick, stamp, streak of years seen). The stats row and stamp grid render only once `visitedCount > 0`; greyed stamps keep rendering after that (they are progress then, not absence). The paid proof (photo, seal, badges) keeps its existing gates untouched.
- [ ] **Step 4: Test passes; screenshots day-zero and seeded (`-seed-saves` from Task 3 plus visited flag; extend the arg to `-seed-visits=`).**
- [ ] **Step 5: Commit:** `Collect greets day zero with a mission instead of four zeros`.

### Task 6: The AllTrails sweep plus the copy check

**Files:**
- Modify: `Screens/TreeCard.swift`, `Screens/Home.swift`, `Screens/MapTab.swift`, `Screens/TreeDetail.swift`, `Screens/Profile.swift` (composition only)
- Create: `scripts/appcopy.py`; wire into nothing automatic (no CI) but callable and listed in the plan's final step
- Test: `python3 scripts/appcopy.py` exits 1 on a planted violation, 0 on the tree

**Interfaces:**
- Produces: every tree card = photo (or the species mark with the honest one-liner "No photograph of this tree yet"), MapInset in the photo's corner, title, one meta line of four facts (species · age · distance · walk minutes); section headers Gabarito bold, large; one moss primary per screen.

- [ ] **Step 1:** `appcopy.py`: grep Swift string literals for em dashes, "hidden gem/must-see/breathtaking/nestled", "licence we can use", "free forever/always free", "curation|verified by us|our sources say" style builder-speak; print file:line, exit 1 on hits. Run: expect it to FAIL on the current photo-placeholder line.
- [ ] **Step 2:** Fix the copy it catches (the placeholder line, any others), rerun: exit 0.
- [ ] **Step 3:** Composition sweep per screen against the teardown: cards, headers, stat rows, one primary. Screenshot every tab and a tree page, light AND dark, 375-pt-width device too (iPhone SE simulator if installed, else note it).
- [ ] **Step 4:** Full local test bundle run (`xcodebuild test -scheme AncientTrees ...`), all green.
- [ ] **Step 5: Commit:** `The app reads as one product, and a script now guards its copy`.

### Task 7: Close the loop

- [ ] Update `.claude/agents` or memory notes if any referenced the four-tab layout; update the `ios-app-workflow` memory (five slots, `-spot`, `-seed-saves`, `-seed-visits` args).
- [ ] Append LOG.md (newest first): what changed, the decision it executes, what still needs Hidde (photo capture in Spot needs his storage yes; walk-saving in Saved is deliberately not built).
- [ ] Final screenshot set of all five slots posted in chat for Hidde.

## Self-review notes

- Spec coverage: structure (T1), merge+pill (T2), Saved+suggestions (T3), Spot dual outcome (T4), day-zero Collect (T5), AllTrails composition + copy ratchet (T6), corpus/log (T7). The improvement-list items "editorial selection" live in T3/T5 (suggestions always photo-first) and T6 (card anatomy).
- Names used across tasks: `savedSuggestions` (T3, reused T5), `spotSplit` (T4), `ExploreTab` (T2), tab ids 0..4 (T1). Consistent.
- Not in scope, said out loud: walk/place hearts in Saved (schema change), Spot photo capture (needs Hidde), Season Radar notifications (Plus, phase 2), any Kit semantics.
