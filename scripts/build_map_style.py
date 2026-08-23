#!/usr/bin/env python3
"""Our own map style, generated from OpenFreeMap's positron.

Hidde, 2026-08-23, after asking which map Polarsteps uses: they run Mapbox, and
their own CEO says why, which is "design control". We do not need their supplier
to get that. A map style is a JSON file over vector tiles, MapLibre reads the
same format Mapbox GL JS does, and OpenFreeMap already serves us the tiles. So
the part worth copying is free.

What was wrong with the stock style, measured rather than felt: positron spends
TWENTY layers on roads and ONE on parks. For a site whose entire content is old
trees standing in parks, that is exactly backwards. It is also nobody's brand;
it is a generic grey basemap equally suited to a parcel courier.

What this changes, in order of how much it matters:

  1. Green comes forward. Parks, woodland and grass get the site's own moss
     tones and enough opacity to read as the subject rather than as filler.
  2. Roads go back. Same geometry, paler and thinner, because a reader is
     looking for a park, not for a route to drive.
  3. The ground turns to paper. The site is cream and ink; the map was cold
     grey. Now the map and the page it sits in are the same document.
  4. Water sits with the cream instead of fighting it.

What it deliberately does NOT change: the tiles, the sprite, the glyphs and the
attribution all stay OpenFreeMap's. This is a restyle, not a new dependency, so
it needs nobody's permission and costs nothing (hard rule 5 is about services a
reader's browser talks to, and this talks to exactly the same one as before).

Labels stay Noto Sans because that is what OpenFreeMap serves; Gabarito would
mean hosting our own glyph pyramid, which is a bigger job for a smaller gain.

    python3 scripts/build_map_style.py            write site/public/assets/map-style.json
    python3 scripts/build_map_style.py --check    fail if the committed file is stale
"""
import argparse, json, os, sys, urllib.request

BASE = "https://tiles.openfreemap.org/styles/positron"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "site", "public", "assets", "map-style.json")

# The site's own tokens, read off site/public/assets/style.css so the map and
# the page cannot drift apart.
PAPER      = "#F7F6F1"   # --surface, the ground
PAPER_DEEP = "#EFEDE5"   # residential blocks, a shade down from the ground
INK        = "#26301E"   # --ink, big labels
INK_MID    = "#5C6350"   # --ink-mid, smaller labels
INK_LIGHT  = "#8A8B80"   # --ink-light, the quietest labels
MOSS_LIGHT = "#E4EDD6"   # --moss-light, warmed slightly so it reads on paper
MOSS_WOOD  = "#D8E5C6"   # woodland, a step deeper than open park
WATER      = "#D6E2E6"   # a blue that sits with cream rather than against it
WATER_LINE = "#C4D5DB"
ROAD       = "#E9E7DF"   # roads, barely above the ground
ROAD_CASE  = "#E2DFD5"
RAIL       = "#DEDBD1"
BUILDING   = "#EDEBE3"
BOUNDARY   = "#C9C6BC"

# id -> (paint key, value) overrides. Anything not named here keeps positron's
# own value, which is why this file is short and why an upstream fix to, say,
# tunnel geometry still reaches us.
FILLS = {
    "park":                (MOSS_LIGHT, 0.85),
    "landcover_wood":      (MOSS_WOOD, 0.75),
    "landuse_residential": (PAPER_DEEP, 0.6),
    "water":               (WATER, 1.0),
    "building":            (BUILDING, 0.7),
    "landcover_ice_shelf": ("#F2F4F5", 0.8),
    "landcover_glacier":   ("#F2F4F5", 0.8),
    "aeroway-area":        (PAPER_DEEP, 0.7),
}
LINES = {
    "waterway":                      WATER_LINE,
    "highway_path":                  ROAD_CASE,
    "highway_minor":                 ROAD,
    "highway_major_casing":          ROAD_CASE,
    "highway_major_inner":           ROAD,
    "highway_major_subtle":          ROAD,
    "highway_motorway_casing":       ROAD_CASE,
    "highway_motorway_inner":        ROAD,
    "highway_motorway_subtle":       ROAD,
    "highway_motorway_bridge_casing": ROAD_CASE,
    "highway_motorway_bridge_inner": ROAD,
    "tunnel_motorway_casing":        ROAD_CASE,
    "tunnel_motorway_inner":         ROAD,
    "road_pier":                     ROAD_CASE,
    "railway":                       RAIL,
    "railway_dashline":              RAIL,
    "railway_transit":               RAIL,
    "railway_transit_dashline":      RAIL,
    "railway_service":               RAIL,
    "railway_service_dashline":      RAIL,
    "aeroway-runway":                PAPER_DEEP,
    "aeroway-runway-casing":         ROAD_CASE,
    "aeroway-taxiway":               PAPER_DEEP,
    "boundary_2":                    BOUNDARY,
    "boundary_3":                    BOUNDARY,
    "boundary_disputed":             BOUNDARY,
}
# Label colour by layer. Places read in ink; everything a walker does not need
# reads in the lightest grey we have.
LABELS = {
    "label_country_1": INK, "label_country_2": INK, "label_country_3": INK,
    "label_city_capital": INK, "label_city": INK, "label_state": INK_MID,
    "label_town": INK_MID, "label_village": INK_MID, "label_other": INK_LIGHT,
    "water_name_point_label": "#8FA8B0", "water_name_line_label": "#8FA8B0",
    "waterway_line_label": "#8FA8B0",
    "highway-name-path": INK_LIGHT, "highway-name-minor": INK_LIGHT,
    "highway-name-major": INK_LIGHT, "airport": INK_LIGHT,
}
# Road name labels and shields are noise on a map about trees. Kept in the
# style rather than deleted so turning them back on is one edit.
DROP = {"highway-shield-non-us", "highway-shield-us-interstate", "road_shield_us"}


def scale(value, factor):
    """Multiply a paint value that may be a plain number or a zoom expression."""
    if isinstance(value, (int, float)):
        return round(value * factor, 3)
    if isinstance(value, dict) and "stops" in value:
        out = dict(value)
        out["stops"] = [[z, round(v * factor, 3)] if isinstance(v, (int, float)) else [z, v]
                        for z, v in value["stops"]]
        return out
    if isinstance(value, list):
        # ["interpolate", [...], ["zoom"], z1, v1, z2, v2, ...]
        out = list(value)
        for i in range(len(out)):
            if isinstance(out[i], (int, float)) and i >= 3 and i % 2 == 0:
                out[i] = round(out[i] * factor, 3)
        return out
    return value


def build():
    # OpenFreeMap answers 403 to the stock Python user agent; identify ourselves.
    req = urllib.request.Request(BASE, headers={
        "User-Agent": "AncientTrees/1.0 (+https://ancienttrees.app) style build"})
    with urllib.request.urlopen(req, timeout=30) as fh:
        style = json.load(fh)

    style["name"] = "Ancient Trees"
    style["metadata"] = {
        "ancienttrees:generated_by": "scripts/build_map_style.py",
        "ancienttrees:base": BASE,
        "ancienttrees:why": ("positron gives 20 layers to roads and 1 to parks; this site is "
                             "about trees standing in parks. Regenerate rather than hand-edit."),
    }
    style["layers"] = [l for l in style["layers"] if l["id"] not in DROP]

    # Attribution rides in on the TileJSON today, which is fine until it is not.
    # A self-hosted style should carry it explicitly: OpenStreetMap's licence is
    # the reason we can have a map at all, and OpenFreeMap serve it for nothing.
    src = style["sources"].get("openmaptiles")
    if src is not None and not src.get("attribution"):
        src["attribution"] = ('<a href="https://openfreemap.org" target="_blank">OpenFreeMap</a> '
                              '&copy; <a href="https://www.openmaptiles.org/" target="_blank">'
                              'OpenMapTiles</a> Data from <a href="https://www.openstreetmap.org/copyright" '
                              'target="_blank">OpenStreetMap</a>')

    for layer in style["layers"]:
        lid, ltype = layer["id"], layer["type"]
        paint = layer.setdefault("paint", {})
        if lid == "background":
            paint["background-color"] = PAPER
        elif ltype == "fill" and lid in FILLS:
            colour, opacity = FILLS[lid]
            paint["fill-color"] = colour
            paint["fill-opacity"] = opacity
            paint.pop("fill-outline-color", None)
        elif ltype == "line" and lid in LINES:
            paint["line-color"] = LINES[lid]
            # Roads keep their geometry and lose their weight: thinner at every
            # zoom, so the shape of a city is still legible and the eye is not
            # dragged along it.
            if lid.startswith(("highway", "tunnel", "road", "aeroway")) and "line-width" in paint:
                paint["line-width"] = scale(paint["line-width"], 0.7)
            if lid.startswith("railway") and "line-width" in paint:
                paint["line-width"] = scale(paint["line-width"], 0.8)
        elif ltype == "symbol" and lid in LABELS:
            paint["text-color"] = LABELS[lid]
            paint["text-halo-color"] = PAPER
            paint["text-halo-width"] = 1.4

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    return style


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="fail if the committed file differs from a fresh build")
    a = ap.parse_args()
    style = build()
    fresh = json.dumps(style, indent=1, ensure_ascii=False, sort_keys=True)
    if a.check:
        if not os.path.exists(OUT):
            print("map-style.json is missing; run scripts/build_map_style.py"); return 1
        have = json.dumps(json.load(open(OUT, encoding="utf-8")), indent=1,
                          ensure_ascii=False, sort_keys=True)
        if have != fresh:
            print("map-style.json is stale against positron; regenerate it"); return 1
        print("map-style.json is current"); return 0
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(fresh + "\n")
    print("wrote %s: %d layers" % (OUT, len(style["layers"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
