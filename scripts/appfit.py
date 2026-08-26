#!/usr/bin/env python3
"""appfit.py - measure the app's layout, the way qa.py measures the website's.

The website has had a fit check since 2026-08-18: the smoke test loads six pages
in a 375px frame and fails the deploy if anything runs past the right edge. The
app had nothing, so every layout fault reached Hidde's telephone before it
reached a check. This is that check for the app.

    python3 scripts/appfit.py            # run the UI test, then judge
    python3 scripts/appfit.py --dump X   # judge a dump made earlier

It reads the element frames that SweepFrames.swift prints for every screen and
looks for the three faults a screenshot does not reliably show a human:

  CLIPPED   something starts on the screen and ends past its edge. The reader
            sees a word cut in half. Horizontal shelves are exempt, because a
            shelf is MEANT to run off the edge, and they are detected rather
            than listed by hand: a scroll view whose own children reach past its
            right edge is a shelf.

  SMALL     a control under Apple's own 44 by 44 point minimum. Missing one of
            these is not a matter of taste, it is somebody's thumb missing the
            button three times in a row at the foot of a tree.

  DRIFT     two things that are meant to line up and are four points apart. This
            is the one Hidde keeps seeing and the one eyes are worst at: a
            heading at x=20 over a card at x=16 reads as "off" without reading
            as anything nameable. Only NEAR misses are reported, because a real
            inset is deliberate and large; a drift is small and is a mistake.

Every finding names the screen and the element, so the fix is a grep away.
"""

import argparse
import collections
import json
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP_DIR = ROOT / "ios" / "AncientTrees"

# The thresholds live in scripts/layout_rules.py since 2026-08-20, because the
# website's smoke test now applies the same three rules and a bar written down
# twice is two bars (Hidde: "zorgen dat de CI voor app en web dezelfde kwaliteit
# nastreven"). Same names, same numbers, both platforms.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layout_rules import MIN_TAP, DRIFT_MAX, SAME  # noqa: E402

ROW = re.compile(
    r"^(?P<indent> *)(?:→)?(?P<type>[A-Za-z][\w ()'-]*?), "
    r"0x[0-9a-f]+, \{\{(?P<x>-?[\d.]+), (?P<y>-?[\d.]+)\}, "
    # `(?P<rest> .*)` here would need a SPACE after the frame and the dump has a
    # COMMA: `}}, identifier: 'heart'`. Every labelled element in the app failed
    # to parse because of it, so the first working version of this check
    # measured nothing but anonymous containers and reported the app clean.
    r"\{(?P<w>-?[\d.]+), (?P<h>-?[\d.]+)\}\}(?P<rest>.*)$")
LABEL = re.compile(r"label: '(.*?)'")
IDENT = re.compile(r"identifier: '(.*?)'")

TAPPABLE = {"Button", "Link", "Switch", "Slider", "SegmentedControl"}
# Elements that carry no visual of their own, so a drift in them is a container
# artefact rather than something a reader can see. SwiftUI's own spelling, taken
# from a real dump: "ScrollView", not "Scroll View", and the first version of
# this list used the wrong one throughout, which is why a ScrollView was
# reported as a drift on the sign-in sheet.
INVISIBLE = {"Application", "Window", "Other", "ScrollView", "CollectionView",
             "Table", "Cell", "NavigationBar", "TabBar", "Any", "Group"}
SCROLLERS = ("ScrollView", "CollectionView", "Table")

# What a person can actually SEE. Only these are judged, because a fault in a
# container repeats itself down every anonymous box inside it: one scroll view
# hanging 20 points over the edge reported itself 24 times, once per nameless
# wrapper, and none of those 24 lines named the thing a reader would notice.
# The leaf is the finding; the container is only how it got there.
VISIBLE = {"StaticText", "Image", "TextField", "SecureTextField", "SearchField",
           "TextView", "Toggle", "ProgressIndicator", "Icon"} | TAPPABLE

# iOS draws its own furniture into the same tree and some of it is enormous: a
# 2196 point wide backdrop behind the tab bar, and a dimming overlay hanging 120
# points off the left. Ours are never a multiple of the screen wide, and they do
# not carry Apple's identifiers.
SYSTEM_IDS = {"AdditionalDimmingOverlay", "PopoverDimmingView"}
# Apple's own furniture inside a sheet, by label: the little grey handle at the
# top is 24 points tall and always will be.
SYSTEM_LABELS = {"Sheet Grabber", "Legal"}

# Furniture we do not lay out and cannot fix. Apple draws its own "Legal" link
# into every MapKit view at 29 by 11 points, and a tab bar centres its items in
# equal columns rather than aligning them to the page's margin, so both would
# report forever without anything to do about either.
# And the navigation bar: Back, a toolbar's Cancel and Share are placed and
# sized by Apple (a toolbar button is 36 tall, Back starts at 16 whatever the
# page's inset is), so judging them judges iOS. Added 2026-08-21, when the
# first read of a green-free workflow found six of its findings were these.
# And the KEYBOARD. The search screen joined the measured list on 2026-08-25 and
# brought iOS's own keyboard with it, which reported a 37 by 54 dictation button
# and a shift key starting 4.5 points in. Both are Apple's, on a view we do not
# lay out and cannot change, and a check that reports the keyboard on every
# search screen forever is a check people learn to skim.
# A Form is Apple's too. Its section headers sit at 16 while our own pages
# start their content at 20, which is not a drift anybody introduced: it is the
# inset UIKit has used for grouped tables since before SwiftUI existed, and it
# is what every Settings screen on the phone looks like.
NOT_OURS = ("Map", "TabBar", "NavigationBar", "Keyboard", "KeyboardKey",
            "Table", "CollectionView")

# And Apple's onboarding overlays, which are not INSIDE the Keyboard element at
# all: the QuickPath introduction ("Speed up your typing by sliding your finger
# across the letters") hangs beside it, carrying a 224 by 21 Continue button that
# fails the 44 point floor. It shows the first time a keyboard appears on a fresh
# simulator, so it failed the gate on the CI runner (a fresh simulator every
# time) and never once on this desk, which is the worst kind of finding: real in
# the log, unreproducible where the fix would be made. Matched by an ancestor's
# identifier because the button itself carries none (2026-08-26).
NOT_OURS_IDS = ("UIContinuousPathIntroductionView",)


def inside(el, types, idents=()):
    p = el.parent
    while p is not None:
        if p.type in types or (idents and p.ident in idents):
            return True
        p = p.parent
    return False


class El:
    __slots__ = ("type", "x", "y", "w", "h", "label", "ident", "depth", "parent",
                 "_horizontal")

    def __init__(self, m):
        self.type = m.group("type").strip()
        self.x, self.y = float(m.group("x")), float(m.group("y"))
        self.w, self.h = float(m.group("w")), float(m.group("h"))
        rest = m.group("rest") or ""
        self.label = (LABEL.search(rest).group(1) if LABEL.search(rest) else "")
        self.ident = (IDENT.search(rest).group(1) if IDENT.search(rest) else "")
        self.depth = len(m.group("indent"))
        self.parent = None
        self._horizontal = False

    @property
    def right(self):
        return self.x + self.w

    def name(self):
        who = self.ident or self.label or ""
        who = who.replace("\n", " ")
        if len(who) > 44:
            who = who[:41] + "..."
        return f"{self.type}{(' ' + repr(who)) if who else ''}"


def parse(dump):
    """Split the dump into screens, each a list of elements with parents set."""
    screens = []
    current = None
    for line in dump.splitlines():
        if line.startswith("<<<SWEEP "):
            parts = line.split(" ")
            name, size = parts[1], parts[2]
            root = next((p[5:] for p in parts[3:] if p.startswith("root=")), None)
            w, h = size.split("x")
            current = {"name": name, "w": float(w), "h": float(h), "els": [],
                       "root": root}
            continue
        if line.startswith("SWEEP>>>"):
            if current:
                screens.append(under_root(link(current)))
            current = None
            continue
        if current is None:
            continue
        m = ROW.match(line)
        if m:
            current["els"].append(El(m))
    return screens


def under_root(screen):
    """Keep only the elements under the screen's named root, when it has one.

    A sheet is measured on its own. Before this, the paywall's list was judged
    against Explore's hero chip behind it, and the contribute form against the
    profile it was opened from: a "drift" from something nobody could see.
    The whole tree is still dumped, because an element's own debugDescription
    prints the whole application regardless; the cut is made here, by
    ancestry, which the indentation gives us (2026-08-21).
    """
    root = screen.get("root")
    if not root:
        return screen
    roots = [el for el in screen["els"] if el.ident == root]
    if not roots:
        print(f"  (no element named {root!r} on {screen['name']}; judging the whole screen)")
        return screen
    top = roots[0]

    def under(el):
        p = el
        while p is not None:
            if p is top:
                return True
            p = p.parent
        return False

    screen["els"] = [el for el in screen["els"] if under(el)]
    # iOS 26 draws a sheet that is not at its large detent as a floating card,
    # eight points in from each edge, and draws the content inside it through
    # the same transform: a 44 point button in a 359 point wide sheet measures
    # 42.1. That is Apple's sheet, not our layout, so the measurements are read
    # back to layout points, and a control is small only when it is small in
    # the points we laid it out in.
    if 0 < top.w < screen["w"] * 0.99:
        screen["scale"] = top.w / screen["w"]
    return screen


def link(screen):
    """Set each element's parent from the indentation."""
    stack = []
    for el in screen["els"]:
        while stack and stack[-1].depth >= el.depth:
            stack.pop()
        el.parent = stack[-1] if stack else None
        stack.append(el)
    return screen


def in_shelf(el):
    """True when something above this element is a horizontal scroller."""
    p = el.parent
    while p is not None:
        if getattr(p, "_horizontal", False):
            return True
        p = p.parent
    return False


def mark_shelves(screen):
    """Find the horizontal shelves, and ONLY the horizontal shelves.

    The first version called any scroller a shelf as soon as one child spilled a
    single point over its edge, and a row of buttons whose first one starts at
    x=-3.5 spills exactly like that. The tree page's action bar was therefore
    exempted from every check, and the check missed a heart button hanging four
    points off the right of the screen, which is the precise bug this whole file
    exists to catch.

    A real shelf is not a few points wider than its frame, it is wider than it
    by more than rounding: there are more cards than fit.

    The line was half a screen of overflow, and that was too generous by
    accident. Two walk cards at 230 points plus a 12 point gap span 472 in a
    375 point scroller, which is a shelf by any reading and did not clear
    375 * 1.5, so the second card was reported CLIPPED. It only passed before
    2026-08-25 because a padlock wrapper stretched every card to full width and
    inflated the span, which is to say the check was being satisfied by the bug
    it should have been reporting. Ten percent still excludes what the 1.5 rule
    was written for: the tree page's action bar spills about four points, and
    the heart hanging off its right edge stays a finding.
    """
    kids = collections.defaultdict(list)
    for el in screen["els"]:
        if el.parent is not None:
            kids[id(el.parent)].append(el)
    for el in screen["els"]:
        el._horizontal = False
        if el.type in SCROLLERS and el.w > 0:
            children = kids.get(id(el), [])
            if not children:
                continue
            span = max(c.right for c in children) - min(c.x for c in children)
            el._horizontal = span > el.w * 1.1


def centred(el, W):
    """True for something laid out around the screen's centre line.

    Centred content shares a centre, not a left edge: a headline, a sentence
    and a button all centred in the same margins start at 34.5, 43 and 30,
    because each starts where its own width puts it. The location primer is
    built that way, as permission screens are, and the left-edge rule has
    nothing to say about it. Full-width things are not centred in this sense,
    because they also have a left edge to keep.
    """
    return abs((el.x + el.w / 2) - W / 2) <= 2.0 and el.w < W * 0.88


def check(screen):
    findings = []
    W = screen["w"]
    mark_shelves(screen)
    els = screen["els"]

    for el in els:
        if (el.w <= 0 or el.h <= 0 or el.ident in SYSTEM_IDS
                or el.label in SYSTEM_LABELS
                or el.label in FRAMEWORK_CONTROLS):
            continue
        if el.type not in VISIBLE or inside(el, NOT_OURS, NOT_OURS_IDS):
            continue
        # Nothing of ours is half again as wide as the phone. What is, is
        # Apple's: the backdrop behind the tab bar measures 2196 points.
        if el.w > W * 1.5:
            continue
        on_screen = el.x < W - SAME and el.y < screen["h"]
        if not on_screen:
            continue

        # Off the LEFT edge counts too, and is how the tree page's "Take me
        # there" button sat at x=-3.5 without anyone noticing.
        if el.x < -SAME and not in_shelf(el):
            findings.append(("CLIPPED", el,
                             f"starts at x={el.x:.0f}, so it hangs off the left edge"))

        if el.right > W + SAME and not in_shelf(el):
            findings.append(("CLIPPED", el,
                             f"ends at {el.right:.0f} on a {W:.0f} point screen, "
                             f"so {el.right - W:.0f} points are off the edge"))

        min_tap = MIN_TAP * screen.get("scale", 1.0)
        # APPLE'S OWN SEGMENTED CONTROL IS 32 POINTS TALL and always has been:
        # it is the height UIKit ships, the height Photos, Files and the App
        # Store all show, and it cannot be made 44 without drawing our own.
        # Reporting it, and its segments, means three findings on every screen
        # that carries one, forever, about a control nobody here laid out.
        # This is the same judgement as the keyboard above rather than a new
        # one: the gate is about OUR geometry.
        if el.type == "SegmentedControl" or inside(el, ("SegmentedControl",)):
            continue
        if el.type in TAPPABLE and (el.w < min_tap - SAME or el.h < min_tap - SAME):
            findings.append(("SMALL", el,
                             f"{el.w:.0f} by {el.h:.0f}, under Apple's 44 by 44"))

    # Leading edges. Only real content: something with width, on screen, and of
    # a type a reader can actually see.
    lefts = collections.defaultdict(list)
    for el in els:
        # The same exemptions the size loop above applies, and it did not:
        # Apple's keyboard and its own map furniture were exempt from CLIPPED
        # and SMALL and reported for DRIFT, so the search screen's finding was
        # the "Next keyboard" key (2026-08-25). One list of what is not ours.
        if el.ident in SYSTEM_IDS or el.label in SYSTEM_LABELS \
                or el.label in FRAMEWORK_CONTROLS:
            continue
        # WIDER THAN A TOUCH TARGET. 48, not 40.
        #
        # A 44 by 44 icon button's left edge is set by whatever encloses it, not
        # by the page: the search field is a capsule with the page's 16 points
        # outside it and 6 inside, so its back arrow starts at 22, and calling
        # that a 6 point drift asks for the icon to sit flush against the pill
        # (2026-08-25). This check is about the margins of text and cards, and
        # those are all far wider than a thumb.
        if (el.type not in INVISIBLE and el.w > 48 and el.h > 4
                and 0 <= el.x < W / 2 and not in_shelf(el)
                and not inside(el, NOT_OURS, NOT_OURS_IDS) and not centred(el, W)):
            lefts[round(el.x * 2) / 2].append(el)
    if lefts:
        dominant = max(lefts, key=lambda x: len(lefts[x]))

        for x, group in sorted(lefts.items()):
            gap = abs(x - dominant)
            # Below two points is the shape of the glyphs, not the layout: a
            # line of text reports the bounds of its letters, so one string
            # starting at 0.5 and another at 1.5 is the difference between an F
            # and a J rather than a mistake anyone made.
            if 2.0 <= gap <= DRIFT_MAX:
                findings.append(("DRIFT", group[0],
                                 f"starts at x={x:g} while {len(lefts[dominant])} "
                                 f"other things on this screen start at x={dominant:g}"
                                 + (f", and {len(group) - 1} more like it" if len(group) > 1 else "")))
    return findings


DUMP_NAME = "appfit-frames.txt"


def run_test(device, scratch):
    """Run the dumping UI test and read the file it leaves behind.

    A FILE rather than the test's output, because XCTest does not forward a
    test's standard output to xcodebuild: the first version of this printed
    fourteen screens of measurements into a result bundle and reported that the
    test produced nothing.
    """
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import appsweep

    udid = device if "-" in device and len(device) == 36 else \
        appsweep.udid_for(device, dict(appsweep.DEVICES).get(device, ""))
    device_dir = pathlib.Path.home() / "Library/Developer/CoreSimulator/Devices" / udid
    for stale in device_dir.rglob(DUMP_NAME):
        stale.unlink()

    from worktree_guard import guard
    guard("running the app's UI test")
    print(f"running SweepFrames on {device}, this takes a few minutes")
    r = subprocess.run(
        ["xcodebuild", "test",
         "-scheme", "AncientTrees",
         "-destination", f"platform=iOS Simulator,id={udid}",
         "-derivedDataPath", str(pathlib.Path(scratch) / "dd"),
         "-only-testing:AncientTreesUITests/SweepFrames",
         # WITHOUT THIS THERE IS NOTHING TO READ. Xcode runs UI tests on a
         # throwaway CLONE of the simulator and deletes it when the run ends,
         # taking the file with it. The test passed three times and left
         # nothing behind before this line existed.
         "-parallel-testing-enabled", "NO",
         # The CI runner has no signing identity and does not need one to run a
         # simulator test.
         "CODE_SIGNING_ALLOWED=NO", "CODE_SIGNING_REQUIRED=NO",
         "CODE_SIGN_IDENTITY="],
        cwd=APP_DIR, capture_output=True, text=True)

    # ONE SIMULATOR BOOTED AT A TIME. xcodebuild boots the destination and
    # leaves it booted, so walking two phones meant the second one started
    # while the first was still running, and the runner cannot carry two.
    # That is not a guess: the workflow's own test step already records this
    # exact failure and its cause ("two apps launching at once took 60 to 110
    # seconds each and then 'did not have a process ID'"), and it is why the
    # layout gate went red in CI on 2026-08-26 while passing on every desk,
    # because a desk runs `--device` and measures one phone.
    subprocess.run(["xcrun", "simctl", "shutdown", udid],
                   capture_output=True, text=True)

    found = sorted(device_dir.rglob(DUMP_NAME), key=lambda p: p.stat().st_mtime)
    if not found:
        for line in (r.stdout + r.stderr).splitlines():
            if "error:" in line or "TEST FAILED" in line:
                print("  " + line)
        sys.exit("the test left no measurements behind")
    return found[-1].read_text()


SELF_PADDING = {
    # Components that put their OWN horizontal inset on. Giving one of these a
    # second .padding(.horizontal) stacks it, and the thing sits further in than
    # everything below it. Found 2026-08-24, when Hidde saw "By species" and
    # "the oldest tree we map" sitting at 32 while their cards sat at 16, and
    # asked the right question: "hoe voorkomen we dit soort slordigheden."
    #
    # A SOURCE check and not a pixel one on purpose. appfit measures what a
    # screen looks like and can only report a drift it happens to see on a
    # screen somebody photographed; this catches the mistake wherever it is
    # written, including on a screen no launch argument opens yet.
    "ShelfHeader",
}


# MapLibre's own two controls. Both are hidden and neither is on screen, and
# both keep appearing in the accessibility tree whatever isHidden,
# isAccessibilityElement and accessibilityElementsHidden are set to, on every
# screen holding a map. Reported for hours as a 40 by 40 compass and a 26 by 26
# info button; three attempts to suppress them failed, and a check that cannot
# be satisfied is a check people learn to scroll past.
#
# Exempt with the reason rather than left to rot: the compass is hidden because
# our recentre control puts north back, and the map's credit is named in About
# on the Profile tab, which is where iOS apps keep it and where it can be read.
FRAMEWORK_CONTROLS = {"Compass", "About this map",
                      # The keyboard, by label as well as by type. Its keys
                      # report as plain Buttons rather than as anything named
                      # Keyboard, so the type exemption misses these three
                      # (found 2026-08-25, on the big phone, the first time the
                      # search screen was measured on anything but the SE).
                      "Next keyboard", "Dictate", "dictation", "shift",
                      "delete", "Emoji", "space", "return", "more"}


def check_double_padding():
    """Any self-padding component handed a second horizontal inset."""
    root = pathlib.Path(__file__).resolve().parent.parent / "ios"
    out = []
    pat = re.compile(
        r"\b(" + "|".join(SELF_PADDING) + r")\((?:[^()]|\([^()]*\))*\)"
        r"[^\n]*(?:\n[^\n]*?)??\.padding\(\.horizontal")
    for f in sorted(root.rglob("*.swift")):
        src = f.read_text(encoding="utf-8")
        for m in pat.finditer(src):
            line = src[:m.start()].count("\n") + 1
            out.append("%s:%d: %s already pads itself; this adds a second inset"
                       % (f.relative_to(root.parent), line, m.group(1)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default=None,
                    help="one phone, by name or by udid. Omit it and EVERY "
                         "phone in appsweep's list is measured, which is what "
                         "CI does: the layout gate measured only the smallest "
                         "until 2026-08-25, and the big one was carrying four "
                         "findings nobody had ever seen, one of them a button "
                         "a point under Apple's floor")
    ap.add_argument("--dump", default=None, help="a saved test output to judge")
    ap.add_argument("--json", action="store_true", help="findings as JSON")
    args = ap.parse_args()

    scratch = os.environ.get("CLAUDE_SCRATCHPAD", "/tmp")

    # The source check runs first and needs no simulator: it catches the
    # mistake where it is written rather than where it happens to be seen.
    source_problems = check_double_padding()
    for p in source_problems:
        print("SOURCE  " + p)
    if source_problems:
        print()

    if args.dump:
        runs = [("from dump", pathlib.Path(args.dump).read_text())]
    else:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import appsweep
        # The two lists have to be one list before either is trusted.
        drift = appsweep.check_lists()
        for d in drift:
            print("LISTS   " + d)
        if drift:
            sys.exit("the sweep and the layout gate disagree about which "
                     "screens exist")
        names = [args.device] if args.device else [d[0] for d in appsweep.DEVICES]
        runs = []
        for name in names:
            runs.append((name, run_test(name, scratch)))
            pathlib.Path(scratch, "appfit-dump.txt").write_text(runs[-1][1])

    total = []
    screens = []
    for device, dump in runs:
        got = parse(dump)
        if not got:
            sys.exit(f"no screens in the dump for {device}")
        for screen in got:
            screen["device"] = device
            screens.append(screen)
            total += [(screen["name"],) + f for f in check(screen)]

    if args.json:
        print(json.dumps([{"screen": s, "kind": k, "element": el.name(),
                           "frame": [el.x, el.y, el.w, el.h], "why": why}
                          for s, k, el, why in total], indent=1))
    else:
        by_screen = collections.defaultdict(list)
        for s, k, el, why in total:
            by_screen[s].append((k, el, why))
        seen_device = None
        for screen in screens:
            if screen.get("device") != seen_device:
                seen_device = screen.get("device")
                print(f"\n{seen_device}")
            rows = by_screen.get(screen["name"], [])
            mark = "ok  " if not rows else "FAIL"
            print(f"{mark} {screen['name']:<14} {len(screen['els'])} elements"
                  + (f", {len(rows)} findings" if rows else ""))
            for kind, el, why in rows:
                print(f"       {kind:<8} {el.name()}")
                print(f"                {why}")
        print(f"\n{len(total)} findings on {len(screens)} screens"
              f" across {len(runs)} phone(s)")

    sys.exit(1 if (total or source_problems) else 0)


if __name__ == "__main__":
    main()
