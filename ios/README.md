# The iOS app

Started 2026-08-19, when Hidde said to build it and that the website waits.

## State

**AncientTreesKit is written and verified. No app exists yet, and cannot yet.**
This Mac has the Command Line Tools but not Xcode, so there is no iOS SDK, no
simulator and no `xcodebuild`. Xcode is downloading; when it lands, the fix that
needs Hidde's password is:

    sudo xcode-select -s /Applications/Xcode.app/Contents/Developer

Everything in `AncientTreesKit/Sources` compiles and runs today with the Swift
toolchain that is already here, which is why it was built first: it is the half
of the app that does not need a simulator to be proven right.

## What it stands on

The website already serves what an app needs, which was the pleasant surprise:

| feed | what it carries |
|---|---|
| `/api/trees.json` | 1377 trees, 2.5 MB, with story, coordinates, access, transport, best_time, precision |
| `/api/walks.json` | 175 walks, tree ids in order, km and minutes |
| `/api/species.json` | 34 species with phenology, enough for the Season Radar |
| `/api/version.json` | a hash and counts, so checking for changes costs a few dozen bytes |

2.5 MB is small enough to hold whole in memory rather than page out of a
database, and that is what makes the app work with no signal. Offline is
effectively solved except for photographs, which is what the paywall promises.

## Verify it

    cd ios/AncientTreesKit
    curl -s https://ancienttrees.app/api/trees.json -o /tmp/trees.json
    curl -s https://ancienttrees.app/api/walks.json -o /tmp/walks.json
    swiftc -O Sources/*.swift Checks/main.swift -o /tmp/atkit && /tmp/atkit /tmp

17 checks, all against the live feed rather than a fixture, because a model that
compiles proves nothing and a model that decodes 1377 real trees proves the
shape. They assert the counts that were measured on the day (3 trees with no
age, 353 with a photo, 546 with a best_time, 458 approximate pins), so a feed
change that breaks an assumption shows up as a failure rather than as a bug
later.

## Two product rules are in the code rather than in a comment

**An unknown `precision` decodes to `.approximate`, never `.confirmed`.** A wrong
pin is the one error a reader cannot forgive, because they are already standing
in the wrong place before any correction reaches them, so an unrecognised value
has to fall on the side of admitting we are unsure.

**`nearest` takes a radius and is allowed to return nothing.** Most of the world
has no tree of ours within an hour, and showing somebody the twelfth nearest at
400 km is worse than saying there is nothing here yet.

## Next, once Xcode is here

The teardown at `ALLTRAILS_TEARDOWN.md` decides the screens. In short: the map is
Google Maps' model rather than AllTrails', because a tree is a point and a route
is a line; the walk sheet is AllTrails', because `Begin` pinned to the bottom of
the phone is the fix for `directions` never having fired once on the website; and
the collection is lists before badges.
