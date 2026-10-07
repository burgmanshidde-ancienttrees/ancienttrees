#!/usr/bin/env python3
"""Every account gate in the app is walked signed out, or says why not.

Hidde, 2026-10-07: "how do we make sure we dont have more gaps and this
doesnt happen in the future". The gap class has one shape: a control that
touches the account exists on a screen no test visits. So every Swift file
that gates on the account (nudge.require(...) or signingIn = true) must carry
an accessibility identifier that AncientTreesUITests/SignedOutWalk.swift taps,
or be named below with the reason it is reached another way. A new gated
screen with neither fails the push and the iOS gate.

    python3 scripts/gatecheck.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT / "ios" / "AncientTrees" / "AncientTrees"
WALK = ROOT / "ios" / "AncientTrees" / "AncientTreesUITests" / "SignedOutWalk.swift"
GATE = re.compile(r"nudge\.require\(|signingIn = true")
# Every string literal inside accessibilityIdentifier(...), so a conditional
# like accessibilityIdentifier(compact ? "a" : "b") yields both.
IDENT_CALL = re.compile(r'accessibilityIdentifier\(([^)]*)\)')
IDENT_STR = re.compile(r'"([^"\\]+)')

# Files whose gate is reached through a control walked elsewhere, or that
# cannot be put on screen signed out without another account. Each line is a
# decision with its reason; an entry here is not a free pass for a new gate
# in the same file, so re-read the reason when the file changes.
REACHED_ANOTHER_WAY = {
    "Collect.swift": "signed out the Collection tab IS the sign-in lane (lane-signin); nothing to gate behind it",
    "Profile.swift": "the profile screen signed out is the sign-in lane; its edit gate needs an account to exist",
    "ProfileButton.swift": "the bar's avatar opens sign-in itself; it is the door, not a gate",
    "CollectSheet.swift": "reached only through tab-collect, which the walk taps (testCameraAsks)",
    "PlacePin.swift": "inside the collect flow behind tab-collect",
    "Paywall.swift": "the paywall's own sign-in is the purchase gate, Hidde's under hard rule 2, not an account act",
    "People.swift": "follow and report need another account's profile on screen; walked by eyes",
    "WalkMode.swift": "the tick inside a walk needs a walk begun; its gate is the same nudge.require as seen-tick",
    "SignIn.swift": "the sheet itself",
    "Contribute.swift": "opens sign-in by itself on arrival; walked as testContributeAsks (-contribute)",
    "ContentView.swift": "its one gate is openCollect(), the camera tab, walked as testCameraAsks (tab-collect)",
}


def main():
    walk = WALK.read_text(encoding="utf-8") if WALK.exists() else ""
    if not walk:
        print("gatecheck: no SignedOutWalk.swift; every gate is unwalked")
        return 1
    bad = []
    for path in sorted(APP.rglob("*.swift")):
        text = path.read_text(encoding="utf-8")
        if not GATE.search(text):
            continue
        # An interpolated identifier ("worth-the-trip-\(value)") is matched on
        # the part before the interpolation.
        ids = [i.split("\\(")[0] for call in IDENT_CALL.findall(text) for i in IDENT_STR.findall(call)]
        if any(i and (f'"{i}"' in walk or f'"{i}' in walk) for i in ids):
            continue
        if path.name in REACHED_ANOTHER_WAY:
            continue
        bad.append(path.relative_to(ROOT))
    if bad:
        print("gatecheck: a gate on the account that no signed-out walk taps and no reason excuses:")
        for b in bad:
            print(f"  {b}: add an accessibilityIdentifier and a test in SignedOutWalk.swift, "
                  "or a line with the reason in scripts/gatecheck.py")
        return 1
    print(f"gatecheck: every gated file is walked or named ({len(REACHED_ANOTHER_WAY)} reached another way)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
