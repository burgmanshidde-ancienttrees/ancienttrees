#!/usr/bin/env python3
"""android_spacing.py - the iPhone's vertical spacing, measured on Android.

Hidde, 2026-11-10: "the vertical spacing feels different on certain pages -
make sure that design really are alike". Screenshots side by side show that
something is off, not by how much, and four points is exactly what eyes read as
"off" without being able to name it (appfit.py says the same about DRIFT). So
this measures it.

    python3 scripts/android_spacing.py --ios-dump <appfit-frames.txt>
        # refresh the iPhone half: data/ios-frames.json, from a SweepFrames dump
        # (appfit.py leaves one at $CLAUDE_SCRATCHPAD/appfit-dump.txt; take the
        # iPhone 17 Pro's)
    python3 scripts/android_spacing.py                  # every ported screen
    python3 scripts/android_spacing.py --only tree explore
    python3 scripts/android_spacing.py --no-device      # judge the dumps already taken
    python3 scripts/android_spacing.py --ci             # android.yml: adb on PATH, no lock

THE SAME WIDTH. The iPhone 17 Pro is 402 points wide and a 1080 pixel Android
phone at its own density about 411 dp, so every photograph that keeps its aspect
ratio would come out 6 dp taller on Android and every line of text would wrap at
a different word. The measurement sets the emulator's density so the screen is
402 dp wide (`wm density`), the width of a real Android phone too, and puts the
density back afterwards. Then a dp is a point and nothing needs a ratio.

WHAT IT COMPARES. The iPhone half is the element tree SweepFrames.swift dumps
(appfit.py's parser, the sheet's own root only). The Android half is UI
Automator's dump of the same launch arguments (LaunchArgs.kt), with Compose's
test tags as resource ids (MainActivity, BrandSheet). An element is matched by
accessibility identifier first, then by its visible text or accessibility label,
in reading order. Between matched neighbours (the next matched element below
one, in both apps) the gap is compared, and so is each element's height and the
first element's distance from the top safe area and the last one's from the
bottom. A page that scrolls is read again after a slow swipe or two: a gap does
not care where the page was scrolled to, so every gap counts once wherever it
was seen whole.

A gap or height that differs by more than 2 is reported; by more than 4 it fails,
unless data/android-parity.json lists it for that screen under "spacing_allowed"
with a reason: {"what": "<a> -> <b>" or "<a> height", "why": "..."}. A screen
still on data/android-spacing-pending.json is reported and not failed.

Writes out/parity/spacing.json and out/parity/android-xml/<screen>-<n>.xml.
"""
import argparse
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

OUT = ROOT / "out" / "parity"
XML_DIR = OUT / "android-xml"
IOS_FRAMES = ROOT / "data" / "ios-frames.json"
# Screens whose spacing is not yet brought in line: measured and reported, not
# failed. A list that only shrinks: a screen leaves it in the change that fixes
# it, and from then on CI holds it to the iPhone.
PENDING = ROOT / "data" / "android-spacing-pending.json"
STATUS = ROOT / "data" / "android-parity.json"
PACKAGE = "app.ancienttrees.android"
ACTIVITY = PACKAGE + "/app.ancienttrees.MainActivity"
ORIGIN = "-at=52.3731,4.8922"

REPORT = 2.0   # a difference worth naming
FAIL = 4.0     # a difference that fails the check
# The iPhone 17 Pro's safe area: the Dynamic Island's 62 at the top, the home
# indicator's 34 at the bottom (UIKit's own numbers for this phone).
IOS_SAFE = (62.0, 34.0)
# How many slow swipes a scrolling page is read after.
PAGES = 3

# What carries something a person sees, on each side.
IOS_TYPES = {"StaticText", "Image", "TextField", "SecureTextField", "SearchField",
             "TextView", "Toggle", "Button", "Link", "Switch", "Slider",
             "SegmentedControl"}
# The phone's own furniture and the map's: neither is laid out by us.
IOS_SKIP_TYPES = {"Keyboard", "KeyboardKey", "NavigationBar"}
IOS_SKIP_IDS = {"AdditionalDimmingOverlay", "PopoverDimmingView"}
IOS_SKIP_LABELS = {"Sheet Grabber", "Legal", "Compass", "About this map", "You Are Here"}


def norm(s):
    # "Amsterdam, 27 trees" (a button's label) and "Amsterdam 27 trees" (the
    # words inside the tappable box) are one name.
    s = re.sub(r"[,.:;\u00a0]", " ", s or "")
    return re.sub(r"\s+", " ", s).strip().lower()


BUTTONS = {"Button", "Link", "Switch", "Toggle", "Slider", "SegmentedControl"}


def kinds_fit(e, n):
    """A button matches something tappable, a line of text matches text: a
    card labelled "Baarn" is not the caption "Baarn" inside another card."""
    tappable = n["clk"] or n["cls"] in ("Button", "Switch", "CheckBox")
    return (e["t"] in BUTTONS) == tappable


# ---------------------------------------------------------------- the iPhone

def ios_from_dump(path):
    import appfit
    screens = appfit.parse(pathlib.Path(path).read_text())
    out = {"_source": f"SweepFrames dump, {time.strftime('%Y-%m-%d')}, iPhone 17 Pro",
           "_safe": list(IOS_SAFE)}
    for s in screens:
        els = []
        for el in s["els"]:
            if el.type not in IOS_TYPES or el.type in IOS_SKIP_TYPES:
                continue
            if el.ident in IOS_SKIP_IDS or el.label in IOS_SKIP_LABELS:
                continue
            if not (el.ident or el.label) or el.w <= 0 or el.h <= 0:
                continue
            # Off the side (the end of a shelf): Android cuts these, so neither counts.
            if (el.x < 0 or el.x + el.w > s["w"]) and el.w < s["w"]:
                continue
            if appfit.inside(el, appfit.NOT_OURS) or in_map(el):
                continue
            # The text inside a button reports the BUTTON's frame on the
            # iPhone, not its own line box: it says nothing about the text.
            if el.type == "StaticText" and same_frame_button_above(el):
                continue
            els.append({"t": el.type, "id": el.ident, "label": el.label,
                        "y": round(el.y, 1), "h": round(el.h, 1),
                        "x": round(el.x, 1), "w": round(el.w, 1),
                        "s": scroller(el, s["h"])})
        out[s["name"]] = {"w": s["w"], "h": s["h"], "els": els}
    IOS_FRAMES.write_text(json.dumps(out, indent=0, ensure_ascii=False) + "\n")
    print(f"wrote {IOS_FRAMES.relative_to(ROOT)}: {len(screens)} screens")


def same_frame_button_above(el):
    p = el.parent
    while p is not None:
        if p.type in ("Button", "Link") and abs(p.y - el.y) < 0.5 and abs(p.h - el.h) < 0.5:
            return True
        p = p.parent
    return False


def scroller(el, screen_h):
    """Which page scroller the element moves with: its top and height, or
    "fixed" for something that stays put (an action bar, a tab bar). Only a
    scroller of 40% of the screen or more counts as the page: a shelf moves
    sideways with the page it sits on."""
    p = el.parent
    while p is not None:
        if p.type in ("ScrollView", "CollectionView", "Table") and p.h >= screen_h * 0.4:
            return f"{round(p.y)}"
        p = p.parent
    return "fixed"


def in_map(el):
    p = el.parent
    while p is not None:
        if p.label == "Map":
            return True
        p = p.parent
    return False


# ---------------------------------------------------------------- Android

class Adb:
    def __init__(self, ci):
        if ci:
            self.adb = shutil.which("adb") or "adb"
        else:
            self.adb = str(pathlib.Path.home() / "Library/Android/sdk/platform-tools/adb")

    def run(self, *args, binary=False):
        r = subprocess.run([self.adb, *args], capture_output=True, text=not binary, check=False)
        return r.stdout

    def shell(self, *args):
        return self.run("shell", *args)


SWEEP_FRAMES = ROOT / "ios/AncientTrees/AncientTreesUITests/SweepFrames.swift"


def frames():
    """name -> launch arguments, as SweepFrames.swift opens each screen.

    SweepFrames, not appsweep.py: the iPhone frames come from SweepFrames, and
    the two lists pick different subjects (ath_004 there, the longest name
    here), so a tree page measured against another tree's would compare two
    stories' line counts.
    """
    import android_parity
    src = SWEEP_FRAMES.read_text()
    base = ["-at=52.3731,4.8922", "-reset-collection", "-reset-blocks", "-no-cover"]
    out = {}
    for m in re.finditer(r'^\s*\("([\w-]+)",\s*\[([^\]]*)\]', src, re.M):
        extra = re.findall(r'"([^"]*)"', m.group(2))
        # A frame's own -at= stands in for the origin, as on the iPhone (the
        # later argument wins there).
        args = ([b for b in base if not (b.startswith("-at=") and any(e.startswith("-at=") for e in extra))]
                + extra)
        out[m.group(1)] = args
    return out, android_parity.PORTED


def set_width(adb, width_dp=402):
    """Density so the screen is width_dp wide; returns the physical size."""
    size = adb.shell("wm", "size")
    m = re.search(r"Physical size: (\d+)x(\d+)", size)
    if not m:
        sys.exit("no Android device answers adb: start the emulator (Medium_Phone_API_37.0), "
                 "or judge the dumps already taken with --no-device")
    w_px, h_px = int(m.group(1)), int(m.group(2))
    density = round(w_px * 160 / width_dp)
    adb.shell("wm", "density", str(density))
    return w_px, h_px, density


def insets(adb, density):
    """The status bar's and the navigation bar's height, in dp."""
    text = adb.shell("dumpsys", "window", "windows")
    top = max([int(v) for v in re.findall(r"type=statusBars[^\n]*?top=(\d+)", text)] or [0])
    bottom = max([int(v) for v in re.findall(r"type=navigationBars[^\n]*?bottom=(\d+)", text)] or [0])
    return top * 160 / density, bottom * 160 / density


def dump_screen(adb, name, args, scrolls, density):
    adb.shell("am", "force-stop", PACKAGE)
    if not any(a.startswith("-at=") for a in args):
        args = args + [ORIGIN]
    joined = ",".join(a.replace(",", "\\,") for a in args)
    adb.run("logcat", "-c")
    adb.shell("am", "start", "-W", "-n", ACTIVITY, "--esa", "args", "'" + joined + "'")
    for _ in range(90):
        if "catalogue" in adb.run("logcat", "-d", "-s", "AncientTrees"):
            break
        time.sleep(1)
    time.sleep(6)
    XML_DIR.mkdir(parents=True, exist_ok=True)
    for old in XML_DIR.glob(f"{name}-*.xml"):
        old.unlink()
    w_px, h_px = map(int, re.search(r"(\d+)x(\d+)", adb.shell("wm", "size")).groups())
    for n in range(scrolls + 1):
        xml = dump_ours(adb, density)
        (XML_DIR / f"{name}-{n}.xml").write_text(xml)
        if n < scrolls:
            if 'scrollable="true"' not in xml:
                break
            # Slow, so it does not fling: a third of the screen per swipe.
            x = w_px // 2
            adb.shell("input", "swipe", str(x), str(int(h_px * 0.7)), str(x), str(int(h_px * 0.37)), "1500")
            time.sleep(1.5)


BOUNDS = re.compile(r"\[(-?\d+),(-?\d+)\]\[(-?\d+),(-?\d+)\]")


def dump_ours(adb, density):
    """UI Automator's tree, with a system dialog out of the way first.

    Found on the first CI run (2026-11-10): a fresh emulator put "Pixel
    Launcher isn't responding" over every screen, the dumps held only that
    dialog, nothing matched, and the check passed on 37 empty screens. So a
    dump without our app in it presses the dialog's Wait (or Close app, or
    OK) and looks again.
    """
    xml = ""
    for _ in range(4):
        adb.shell("uiautomator", "dump", "/sdcard/at-spacing.xml")
        xml = adb.run("exec-out", "cat", "/sdcard/at-spacing.xml")
        if f'package="{PACKAGE}"' in xml:
            return xml
        m = re.search(r'text="(Wait|Close app|OK|Close)"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', xml)
        if m:
            x0, y0, x1, y1 = map(int, m.groups()[1:])
            adb.shell("input", "tap", str((x0 + x1) // 2), str((y0 + y1) // 2))
        else:
            adb.shell("input", "keyevent", "KEYCODE_BACK")
            adb.shell("am", "start", "-n", ACTIVITY)
        time.sleep(4)
    return xml


def android_nodes(xml_text, density, screen_h_dp):
    """Every node with a name, in dp; nodes clipped by a scroller left out."""
    try:
        root = ET.fromstring(xml_text[xml_text.find("<"):])
    except ET.ParseError:
        return []
    k = 160 / density
    out = []

    def walk(node, clip, page):
        b = BOUNDS.match(node.get("bounds", "")) if node.tag == "node" else None
        here, page_here = clip, page
        if b:
            x0, y0, x1, y1 = (int(v) * k for v in b.groups())
            pkg = node.get("package", "")
            if node.get("scrollable") == "true":
                here = (y0, y1)
                if y1 - y0 >= screen_h_dp * 0.4:
                    page_here = f"{round(y0)}"
            if pkg == PACKAGE and y1 > y0:
                rid = node.get("resource-id", "")
                rid = rid.split(":id/")[-1] if ":id/" in rid else rid
                text, desc = node.get("text", ""), node.get("content-desc", "")
                if node.get("clickable") == "true" and not (text or desc):
                    # A tappable box whose words sit in a child: the iPhone's
                    # Button carries those words as its label and its own frame.
                    text = " ".join(t for t in (c.get("text", "") for c in node.iter("node")) if t)
                clipped = False
                if clip is not None:
                    # The accessibility bounds are cut at the scroller's edge,
                    # so a node touching that edge has a height that is not its own.
                    clipped = abs(y0 - clip[0]) < 1.5 or abs(y1 - clip[1]) < 1.5
                if y0 < 0.5 or y1 > screen_h_dp - 0.5:
                    clipped = True
                # A card running off the side of a shelf is cut there too.
                if (x0 < 0.5 or x1 > 401.5) and x1 - x0 < 401:
                    clipped = True
                if (rid or text or desc) and not clipped:
                    out.append({"id": rid, "text": text, "desc": desc,
                                "x": round(x0, 1), "y": round(y0, 1),
                                "w": round(x1 - x0, 1), "h": round(y1 - y0, 1),
                                "cls": node.get("class", "").rsplit(".", 1)[-1],
                                "clk": node.get("clickable") == "true",
                                "s": page})
        for c in node:
            walk(c, here, page_here)

    walk(root, None, "fixed")
    return out


# ---------------------------------------------------------------- comparing

def keys_ios(e):
    # A lone separator ("·") is a glyph inside a line, not a block on the page.
    return [k for k in (("id", e["id"]), ("t", norm(e["label"]))) if k[1] and re.search(r"\w", k[1])]


def keys_android(n):
    return [k for k in (("id", n["id"]), ("t", norm(n["text"])), ("t", norm(n["desc"])))
            if k[1] and re.search(r"\w", k[1])]


def name_of(e):
    s = e.get("id") or e.get("label") or e.get("text") or e.get("desc") or "?"
    s = s.replace("\n", " ")
    return s if len(s) <= 40 else s[:37] + "..."


def match(ios_els, and_nodes):
    """Pairs (ios, android), each element used once, in reading order."""
    # One element per frame and key on each side: a Button and the text inside
    # it often carry the same words and the same frame.
    def dedupe(items, keyf):
        seen, out = set(), []
        for it in items:
            sig = (tuple(keyf(it)), it["y"], it["h"])
            if sig not in seen:
                seen.add(sig)
                out.append(it)
        return out

    ios_els = dedupe(sorted(ios_els, key=lambda e: (e["y"], e["x"])), keys_ios)
    and_nodes = dedupe(sorted(and_nodes, key=lambda n: (n["y"], n["x"])), keys_android)
    pairs, used = [], set()
    for kind in ("id", "t"):
        index = {}
        for i, e in enumerate(ios_els):
            for k in keys_ios(e):
                if k[0] == kind:
                    index.setdefault(k[1], []).append(i)
        for n in and_nodes:
            if id(n) in used:
                continue
            for k in keys_android(n):
                if k[0] != kind:
                    continue
                free = [i for i in index.get(k[1], []) if ("i", i) not in used
                        and (kind == "id" or kinds_fit(ios_els[i], n))]
                if free:
                    i = free[0]
                    used.add(("i", i))
                    used.add(id(n))
                    pairs.append((ios_els[i], n))
                    break
    pairs = [(a, touch_box(a, n)) for a, n in pairs]
    pairs.sort(key=lambda p: (p[0]["y"], p[0]["x"]))
    return pairs


def touch_box(e, n):
    """The drawn box of a tappable node Compose reported at its touch size.

    Compose gives accessibility the TOUCH bounds of anything clickable, grown
    evenly to Android's 48 dp minimum (SemanticsNode.touchBoundsInRoot), so a
    44 point pill drawn exactly as on the iPhone reads as 48 here, two dp
    higher and two lower. Found on the tree page, 2026-11-10: every pill and
    chip "4 taller". A 48 against a smaller iPhone height is taken as the
    iPhone's height, centred; anything not exactly 48 is measured as it is.
    """
    if (n["clk"] or n["cls"] == "Button") and abs(n["h"] - 48) < 0.6 and e["h"] < 47.5:
        n = dict(n, y=round(n["y"] + (48 - e["h"]) / 2, 1), h=e["h"])
    return n


def compare_page(pairs, ios_h):
    """Gaps between neighbours and heights, for one Android dump."""
    gaps, heights = {}, {}
    for a, b in pairs:
        heights[name_of(a)] = (a["h"], b["h"])
    for i, (ia, aa) in enumerate(pairs):
        # The nearest matched element wholly below this one, on the iPhone,
        # horizontally overlapping it; it must be below on Android too.
        # Neighbours only within one layer: a story line and the action bar
        # floating over it are not spaced against each other.
        below = [(ib, ab) for ib, ab in pairs[i + 1:]
                 if (ib["s"] == "fixed") == (ia["s"] == "fixed")
                 and (ab["s"] == "fixed") == (aa["s"] == "fixed")
                 and ib["y"] >= ia["y"] + ia["h"] - 0.5
                 # A header pinned to the top and a tab bar pinned to the foot
                 # are not neighbours: the bottom inset judges the bar.
                 and not (ia["s"] == "fixed" and ib["y"] - ia["y"] > ios_h / 2)
                 and ib["x"] < ia["x"] + ia["w"] and ia["x"] < ib["x"] + ib["w"]]
        if not below:
            continue
        top = min(ib["y"] for ib, _ in below)
        ib, ab = next(p for p in below if p[0]["y"] == top)
        g_ios = ib["y"] - (ia["y"] + ia["h"])
        g_and = ab["y"] - (aa["y"] + aa["h"])
        if ab["y"] < aa["y"]:
            continue  # the order differs: a layout question, not a spacing one
        # With the two Android heights: a node cut at the screen's foot is
        # shorter than itself, so the page that shows both tallest wins.
        gaps[f"{name_of(ia)} -> {name_of(ib)}"] = (round(g_ios, 1), round(g_and, 1), aa["h"] + ab["h"])
    return gaps, heights


def judge(screen, ios, xml_pages, density, safe_and, screen_h_dp, allowed):
    allowed_what = {a["what"]: a.get("why", "") for a in allowed}
    gaps, heights, insets_, seen_gap = {}, {}, {}, {}
    matched = 0
    for n, xml in enumerate(xml_pages):
        nodes = android_nodes(xml, density, screen_h_dp)
        pairs = match(ios["els"], nodes)
        matched = max(matched, len(pairs))
        g, h = compare_page(pairs, ios["h"])
        # A scrolled page meets the same element again: keep the reading
        # where it stood whole (accessibility bounds are cut, never grown).
        for k, v in g.items():
            if k not in seen_gap or v[2] > seen_gap[k][2]:
                seen_gap[k] = v
                gaps[k] = v[:2]
        for k, v in h.items():
            if k not in heights or v[1] > heights[k][1]:
                heights[k] = v
        if n == 0 and pairs:
            # The first named thing under the top safe area, and the lowest one
            # above the bottom one (a tab bar, an action bar, a sheet's button).
            ia, aa = min(pairs, key=lambda p: p[0]["y"])
            # From the safe area, or from the screen's top for a page that
            # draws under the status bar (a hero photograph): whichever agrees
            # better is how the page was laid out.
            from_safe = (round(ia["y"] - IOS_SAFE[0], 1), round(aa["y"] - safe_and[0], 1))
            from_top = (round(ia["y"], 1), round(aa["y"], 1))
            if abs(from_top[1] - from_top[0]) < abs(from_safe[1] - from_safe[0]):
                insets_[f"screen top -> {name_of(ia)}"] = from_top
            else:
                insets_[f"top safe area -> {name_of(ia)}"] = from_safe
            ia, aa = max(pairs, key=lambda p: p[0]["y"] + p[0]["h"])
            if ia["y"] + ia["h"] <= ios["h"] and ia["y"] + ia["h"] > ios["h"] * 0.75:
                insets_[f"{name_of(ia)} -> bottom safe area"] = (
                    round(ios["h"] - IOS_SAFE[1] - ia["y"] - ia["h"], 1),
                    round(screen_h_dp - safe_and[1] - aa["y"] - aa["h"], 1))
    rows = []
    for kind, table, suffix in (("inset", insets_, ""), ("gap", gaps, ""), ("height", heights, " height")):
        for what, (vi, va) in table.items():
            d = round(va - vi, 1)
            if abs(d) <= REPORT:
                continue
            what_s = what + suffix
            rows.append({"kind": kind, "what": what_s, "ios": vi, "android": va, "diff": d,
                         "fails": abs(d) > FAIL and what_s not in allowed_what,
                         "allowed": allowed_what.get(what_s)})
    rows.sort(key=lambda r: -abs(r["diff"]))
    return {"matched": matched, "measured": len(gaps) + len(heights) + len(insets_),
            "gaps": len(gaps), "differences": rows,
            "failing": sum(1 for r in rows if r["fails"])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ios-dump")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--no-device", action="store_true")
    ap.add_argument("--ci", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--apk", help="install this build first, e.g. android/app/build/outputs/apk/debug/app-debug.apk")
    a = ap.parse_args()
    if a.ios_dump:
        ios_from_dump(a.ios_dump)
        return
    ios_all = json.loads(IOS_FRAMES.read_text())
    pend = json.loads(PENDING.read_text()) if PENDING.exists() else {}
    pending = set(pend.get("screens", []))
    # Screens the iPhone's dump cannot be held against, each with its reason:
    # measured, shown, never passed off as equal.
    no_baseline = pend.get("no_ios_baseline", {})
    status = json.loads(STATUS.read_text()) if STATUS.exists() else {}
    FRAMES, PORTED = frames()
    names = a.only or [f for f in PORTED if f in FRAMES and f in ios_all]
    meta_path = XML_DIR / "_device.json"
    if not a.no_device:
        adb = Adb(a.ci)

        def measure():
            if a.apk:
                adb.run("install", "-r", a.apk)
                for perm in ("ACCESS_FINE_LOCATION", "ACCESS_COARSE_LOCATION"):
                    adb.shell("pm", "grant", PACKAGE, "android.permission." + perm)
            w_px, h_px, density = set_width(adb)
            try:
                adb.shell("am", "force-stop", PACKAGE)
                top, bottom = insets(adb, density)
                for name in names:
                    print(f"  {name}", flush=True)
                    dump_screen(adb, name, list(FRAMES[name]), PAGES, density)
            finally:
                adb.shell("wm", "density", "reset")
            XML_DIR.mkdir(parents=True, exist_ok=True)
            prev = json.loads(meta_path.read_text()) if meta_path.exists() else {}
            prev.update({"density": density, "h_dp": h_px * 160 / density, "safe": [top, bottom]})
            meta_path.write_text(json.dumps(prev))

        if a.ci:
            measure()
        else:
            from emulator_lock import emulator
            with emulator("android_spacing"):
                measure()
    meta = json.loads(meta_path.read_text())
    result = {"_device": meta, "_threshold": {"report": REPORT, "fail": FAIL}}
    failing = 0
    for name in names:
        pages = [p.read_text() for p in sorted(XML_DIR.glob(f"{name}-*.xml"))]
        if name not in ios_all or not pages:
            result[name] = {"error": "no iPhone frames" if name not in ios_all else "no Android dump"}
            print(f"FAIL {name:<22} {result[name]['error']}")
            failing += 1
            continue
        if name in no_baseline:
            result[name] = {"error": "not comparable: " + no_baseline[name]}
            print(f"n/a  {name:<22} {no_baseline[name]}")
            continue
        allowed = status.get(name, {}).get("spacing_allowed", [])
        r = judge(name, ios_all[name], pages, meta["density"], meta["safe"], meta["h_dp"], allowed)
        r["pending"] = name in pending
        # NOTHING MEASURED IS A FAILURE, pending or not: the first CI run
        # matched nothing on 37 screens and called every one "ok".
        if len(ios_all[name]["els"]) >= 3 and r["matched"] < 2:
            r["failing"] += 1
            r["differences"].insert(0, {"kind": "error", "what": "nothing matched: the screen did not open",
                                        "ios": len(ios_all[name]["els"]), "android": r["matched"],
                                        "diff": 0, "fails": True, "allowed": None})
            r["pending"] = False
        result[name] = r
        if not r["pending"]:
            failing += r["failing"]
        if not a.quiet:
            mark = ("todo" if r["pending"] and r["failing"] else "FAIL" if r["failing"]
                    else ("diff" if r["differences"] else "ok  "))
            print(f"{mark} {name:<22} {r['matched']} matched, {r['measured']} measured, "
                  f"{len(r['differences'])} over {REPORT:g}, {r['failing']} failing")
            for row in r["differences"]:
                flag = "!" if row["fails"] else ("~" if row["allowed"] else " ")
                print(f"   {flag} {row['kind']:<6} {row['diff']:+6.1f}  {row['what']}  "
                      f"(iPhone {row['ios']:g}, Android {row['android']:g})")
    OUT.mkdir(parents=True, exist_ok=True)
    existing = {}
    path = OUT / "spacing.json"
    if path.exists() and a.only:
        existing = json.loads(path.read_text())
    existing.update(result)
    path.write_text(json.dumps(existing, indent=1, ensure_ascii=False))
    print(f"\n{failing} failing differences over {FAIL:g} on {len(names)} screens; {path.relative_to(ROOT)}")
    sys.exit(1 if failing else 0)


if __name__ == "__main__":
    main()
