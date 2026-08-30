# The iOS app

Started 2026-08-19, when Hidde said to build it and that the website waits.

## Where the app is

`ios/AncientTrees/` is the Xcode project and is the whole app. Three targets:
`AncientTrees` (the app), `AncientTreesTests` (Swift Testing, unit) and
`AncientTreesUITests` (XCTest, the walks and the sweep).

    Kit/        the engine: catalogue, sync, account, saves, sightings, photos
    Screens/    the views
    Data/       the catalogue that ships inside the app, the floor it falls back to

The one door out to the network is `Kit/Net.swift`, the one door to Supabase is
`Supa` in `Kit/Account.swift`, and `scripts/netcheck.py` keeps both doors one.

## Verify it

    xcodebuild test -project ios/AncientTrees/AncientTrees.xcodeproj \
      -scheme AncientTrees -destination 'platform=iOS Simulator,name=iPhone 17' \
      -parallel-testing-enabled NO

`.github/workflows/ios.yml` runs the same thing on every push and twice a day on
a schedule, plus the layout gate and the screen sweep. `scripts/health.py` says
whether it is currently red.

## Looking at it

    python3 scripts/appsweep.py     # photograph every screen, then LOOK at them
    python3 scripts/appfit.py       # measure them: CLIPPED, SMALL, DRIFT
    python3 scripts/appwalk.py      # walk the flows, assert there is always a way back
    python3 scripts/refused.py      # run it with location and photos denied

Build app changes in a `git worktree`, not in this checkout;
`scripts/worktree_guard.py` refuses when another session is live and says why.

## What it stands on

The website serves everything the app reads, which is why the app is a reader
rather than a second database:

| feed | what it carries |
|---|---|
| `/api/trees.json` | every tree, with story, coordinates, access, transport, best_time, precision |
| `/api/walks.json` | the walks, tree ids in order, km and minutes |
| `/api/species.json` | the species with phenology, which the Season Radar runs on |
| `/api/browse.json` | the collections, and the face each city, country and species wears |
| `/api/version.json` | a hash and counts, so checking for changes costs a few dozen bytes |

Small enough to hold whole in memory rather than page out of a database, and
that is what makes the app work with no signal. The copy in `Data/` is the
floor: a fresh install on a plane still has every tree. Refresh it with
`python3 scripts/appdata.py`.

An ANSWER travels in the feed; a RULE stays on the server. See CLAUDE.md, "the
both-surfaces rule": everything the app re-decided for itself has drifted.

---

**Deleted 2026-08-30: `ios/AncientTreesKit/`.** It was the half of the app that
could be proven before Xcode arrived, written on 2026-08-19 and made redundant
by the real project a few days later. Nothing referenced it, nothing built it,
and its copy of the models had already fallen behind the app's (no `thumb`, no
`hero`, no `credit_required`), so it read as live code and was a second answer
waiting to be believed. It is in the history if it is ever wanted.
