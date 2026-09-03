#!/usr/bin/env python3
"""map_style_dark.py - derive the dark map style from the light one.

Written 2026-09-03, the day the app shipped and the first thing two people in
dark mode met was a cream-white map filling the whole screen. Everything that
floats on that map is a translucent material, so a bright map also made the
bottom sheet grey, the "Map" pill white and the tree page's map inset a lit
postage stamp on a black page. One cause, four symptoms.

WHY A MAPPING RATHER THAN AN INVERSION. Inverting a map's colours gives blue
land and brown water; every reference night map is hand-picked instead. Google's
own night style array reads land #242f3e, water #17263c (darker than the land,
so water recedes), and every label halo set to the background colour. OpenFreeMap
publishes a dark style over the same OpenMapTiles source we use, on the same
layer ids. This file copies their two structural rules and keeps our own hues:
moss where the light style is green, and the app's own dark ground under it.

WHY A SCRIPT RATHER THAN A SECOND FILE BY HAND. Two hand-maintained styles drift,
and the drift is silent because nobody opens the dark one in daylight. The light
style stays the source of truth; this reads it, swaps 17 colours and writes the
dark twin. An unmapped colour is an ERROR rather than a pass-through, so adding
a layer to the light style makes this fail loudly instead of leaving one cream
shape on a black map.

    python3 scripts/map_style_dark.py          # write it
    python3 scripts/map_style_dark.py --check   # fail if it is out of date
"""

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIGHT = ROOT / "site" / "public" / "assets" / "map-style.json"
DARK = ROOT / "site" / "public" / "assets" / "map-style-dark.json"

# The map is the BASE layer in Apple's sense: everything else in the app sits on
# top of it, so it is the darkest surface in the product, one step under
# Brand.ground. Sheets and cards are the elevated ones.
BASE = "#0D0F0C"

COLOURS = {
    # ground, and every label halo, which is Google's night rule: a halo the
    # colour of the background reads as a gap around the letter rather than as
    # an outline drawn on top of the map.
    "#F7F6F1": BASE,
    # Water DARKER than the land and bluer, so it recedes at night. Google's
    # night style does the same: land #242f3e, water #17263c.
    "#D6E2E6": "#101A20",
    "#C4D5DB": "#16242C",
    # Green stays green, because green is what this product is looking for. A
    # wood is slightly more prominent than a park in the light style and stays
    # slightly more prominent here, which in dark means slightly lighter.
    "#E4EDD6": "#1A2214",
    "#D8E5C6": "#1F2A17",
    # Ice and glacier: neutral, barely above the ground.
    "#F2F4F5": "#16191A",
    # Built ground. Residential is a shade above the base, buildings a shade
    # above that, which is the light style's own order read the other way up.
    "#EFEDE5": "#131610",
    "rgb(242,243,240)": "#131610",
    "#EDEBE3": "#171A13",
    # The road network is the one thing that must read at a glance, so the
    # carriageway is clearly lighter than the land and the casing sits between
    # the two as an edge rather than as an outline.
    "#E9E7DF": "#2C3326",
    "#E2DFD5": "#1A1E15",
    "#DEDBD1": "#232A1D",
    "#C9C6BC": "#3E4536",
    # Labels. The two big ones are Brand.ink and Brand.inkSoft, so a place name
    # on the map is the same white as a place name on a card.
    "#26301E": "#E6EADD",
    "#5C6350": "#A2AA97",
    "#8A8B80": "#8E9583",
    "#8FA8B0": "#6E8B95",
}


def convert(style):
    out = json.loads(json.dumps(style))
    out["name"] = style.get("name", "Ancient Trees") + " dark"
    unmapped = []
    for layer in out["layers"]:
        paint = layer.get("paint", {})
        for key, value in paint.items():
            if "color" not in key or not isinstance(value, str):
                continue
            if value not in COLOURS:
                unmapped.append(f'{layer["id"]}.{key} = {value}')
                continue
            paint[key] = COLOURS[value]
    if unmapped:
        raise SystemExit(
            "map_style_dark: no dark colour for:\n  "
            + "\n  ".join(unmapped)
            + "\nAdd it to COLOURS. A pass-through would leave one cream shape "
              "on a black map and nobody would see it until a reader did.")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 when the file on disk is not what this writes")
    args = ap.parse_args()

    built = convert(json.loads(LIGHT.read_text()))
    text = json.dumps(built, indent=1, sort_keys=True) + "\n"

    if args.check:
        if not DARK.exists() or DARK.read_text() != text:
            sys.exit("map-style-dark.json is out of date: "
                     "python3 scripts/map_style_dark.py")
        print("map-style-dark.json is up to date")
        return 0

    DARK.write_text(text)
    print(f"wrote {DARK.relative_to(ROOT)} ({len(built['layers'])} layers, "
          f"{len(COLOURS)} colours mapped)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
