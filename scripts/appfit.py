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
    r"\{(?P<w>-?[\d.]+), (?P<h>-?[\d.]+)\}\}(?P<rest> .*)?$")
LABEL = re.compile(r"label: '(.*?)'")
IDENT = re.compile(r"identifier: '(.*?)'")

TAPPABLE = {"Button", "Link", "Switch", "Slider", "Segmented Control"}
# Elements that carry no visual of their own, so a drift in them is a container
# artefact rather than something a reader can see.
INVISIBLE = {"Application", "Window", "Other", "Scroll View", "Collection View",
             "Table", "Cell", "Navigation Bar", "Tab Bar", "Any"}


class El:
    __slots__ = ("type", "x", "y", "w", "h", "label", "ident", "depth", "parent")

    def __init__(self, m):
        self.type = m.group("type").strip()
        self.x, self.y = float(m.group("x")), float(m.group("y"))
        self.w, self.h = float(m.group("w")), float(m.group("h"))
        rest = m.group("rest") or ""
        self.label = (LABEL.search(rest).group(1) if LABEL.search(rest) else "")
        self.ident = (IDENT.search(rest).group(1) if IDENT.search(rest) else "")
        self.depth = len(m.group("indent"))
        self.parent = None

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
            _, name, size = line.split(" ", 2)
            w, h = size.split("x")
            current = {"name": name, "w": float(w), "h": float(h), "els": []}
            continue
        if line.startswith("SWEEP>>>"):
            if current:
                screens.append(link(current))
            current = None
            continue
        if current is None:
            continue
        m = ROW.match(line)
        if m:
            current["els"].append(El(m))
    return screens


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
    """True when something above this element is a horizontal scroller.

    A shelf is detected rather than declared: a scroll view whose own children
    reach past its right edge scrolls sideways, and everything inside it is
    supposed to run off the screen.
    """
    p = el.parent
    while p is not None:
        if p.type in ("Scroll View", "Collection View") and getattr(p, "_horizontal", False):
            return True
        p = p.parent
    return False


def mark_shelves(screen):
    kids = collections.defaultdict(list)
    for el in screen["els"]:
        if el.parent is not None:
            kids[id(el.parent)].append(el)
    for el in screen["els"]:
        if el.type in ("Scroll View", "Collection View"):
            children = kids.get(id(el), [])
            el._horizontal = any(c.right > el.right + SAME or c.x < el.x - SAME
                                 for c in children)


def check(screen):
    findings = []
    W = screen["w"]
    mark_shelves(screen)
    els = screen["els"]

    for el in els:
        if el.w <= 0 or el.h <= 0:
            continue
        on_screen = -SAME < el.x < W - SAME and el.y < screen["h"]
        if not on_screen:
            continue

        if el.right > W + SAME and not in_shelf(el):
            findings.append(("CLIPPED", el,
                             f"ends at {el.right:.0f} on a {W:.0f} point screen, "
                             f"so {el.right - W:.0f} points are off the edge"))

        if el.type in TAPPABLE and (el.w < MIN_TAP - SAME or el.h < MIN_TAP - SAME):
            findings.append(("SMALL", el,
                             f"{el.w:.0f} by {el.h:.0f}, under Apple's 44 by 44"))

    # Leading edges. Only real content: something with width, on screen, and of
    # a type a reader can actually see.
    lefts = collections.defaultdict(list)
    for el in els:
        if (el.type not in INVISIBLE and el.w > 40 and el.h > 4
                and 0 <= el.x < W / 2 and not in_shelf(el)):
            lefts[round(el.x * 2) / 2].append(el)
    if lefts:
        dominant = max(lefts, key=lambda x: len(lefts[x]))
        for x, group in sorted(lefts.items()):
            gap = abs(x - dominant)
            if SAME < gap <= DRIFT_MAX:
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

    udid = appsweep.udid_for(device, dict(appsweep.DEVICES).get(device, ""))
    device_dir = pathlib.Path.home() / "Library/Developer/CoreSimulator/Devices" / udid
    for stale in device_dir.rglob(DUMP_NAME):
        stale.unlink()

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
         "-parallel-testing-enabled", "NO"],
        cwd=APP_DIR, capture_output=True, text=True)

    found = sorted(device_dir.rglob(DUMP_NAME), key=lambda p: p.stat().st_mtime)
    if not found:
        for line in (r.stdout + r.stderr).splitlines():
            if "error:" in line or "TEST FAILED" in line:
                print("  " + line)
        sys.exit("the test left no measurements behind")
    return found[-1].read_text()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="iPhone SE (sweep)",
                    help="the phone to measure on; the smallest is the honest one")
    ap.add_argument("--dump", default=None, help="a saved test output to judge")
    ap.add_argument("--json", action="store_true", help="findings as JSON")
    args = ap.parse_args()

    scratch = os.environ.get("CLAUDE_SCRATCHPAD", "/tmp")
    if args.dump:
        dump = pathlib.Path(args.dump).read_text()
    else:
        dump = run_test(args.device, scratch)
        pathlib.Path(scratch, "appfit-dump.txt").write_text(dump)

    screens = parse(dump)
    if not screens:
        sys.exit("no screens in the dump")

    total = []
    for screen in screens:
        findings = check(screen)
        total += [(screen["name"],) + f for f in findings]

    if args.json:
        print(json.dumps([{"screen": s, "kind": k, "element": el.name(),
                           "frame": [el.x, el.y, el.w, el.h], "why": why}
                          for s, k, el, why in total], indent=1))
    else:
        by_screen = collections.defaultdict(list)
        for s, k, el, why in total:
            by_screen[s].append((k, el, why))
        for screen in screens:
            rows = by_screen.get(screen["name"], [])
            mark = "ok  " if not rows else "FAIL"
            print(f"{mark} {screen['name']:<14} {len(screen['els'])} elements"
                  + (f", {len(rows)} findings" if rows else ""))
            for kind, el, why in rows:
                print(f"       {kind:<8} {el.name()}")
                print(f"                {why}")
        print(f"\n{len(total)} findings on {len(screens)} screens"
              f" ({args.device if not args.dump else 'from dump'})")

    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
