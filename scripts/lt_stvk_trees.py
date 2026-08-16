#!/usr/bin/env python3
"""Lithuania's nature heritage trees, off the STVK map's own vector tiles.

Why it is done this way. Lithuania's Saugomų teritorijų valstybės kadastras
(STVK) is a real, public register, and its download page requires a login this
project will never create. Two earlier attempts died guessing hostnames, because
stvk.lt is an Angular app and its API is at /stk-api/rest/, which no reasonable
guess finds. A browser session read the app's own network calls in a minute:
the map draws from public Mapbox vector tiles at
`https://stvk.lt/tiles/maps/stvk/{z}/{x}/{y}.pbf`, no authentication, and the
`gpo_t` layer inside them is Gamtos Paveldo Objektai, the nature heritage
objects. `kind` splits them, and `gpo_bot_t` is the botanical ones: the trees.

Zoom 11 is the working zoom and the choice matters. Below it the tiles carry ids
and coordinates but drop the name fields; above it the tile count explodes for
no extra data. Measured over Vilnius: z10 gave 47 objects and 0 names, z11 gave
45 objects and 45 names.

The coordinates are tile-space decoded back to lon/lat, so they carry that
rounding: at z11 one tile unit is a few metres, which is fine for an approximate
pin and is not a survey. Every entry here is a lead.

Usage:
    python3 scripts/lt_stvk_trees.py --fetch
"""
import argparse
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import mvt  # noqa: E402

OUT = os.path.join(ROOT, "data", "registers", "lithuania-stvk-gpo.json")
TILE = "https://stvk.lt/tiles/maps/stvk/%d/%d/%d.pbf"
UA = "AncientTrees/1.0 (https://ancienttrees.app; burgmans.hidde@gmail.com)"
Z = 11
# Lithuania's bounding box, generous at the edges.
BBOX = (53.80, 20.85, 56.55, 26.95)   # south, west, north, east

# The register's own object kinds. Only the botanical ones are trees; the rest
# are boulders, outcrops, springs and landforms, and are dropped here the same
# way Estonia's non-tree objects are.
KINDS = {
    "gpo_bot_t": "botanical (tree or shrub)",
    "gpo_geo_t": "geological",
    "gpo_gmo_t": "geomorphological",
    "gpo_hge_t": "hydrogeological",
    "gpo_hgr_t": "hydrographic",
    "gpo_zoo_t": "zoological",
}


def tile_xy(lat, lon, z):
    n = 1 << z
    return (int((lon + 180) / 360 * n),
            int((1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n))


def sweep():
    x0, y0 = tile_xy(BBOX[2], BBOX[1], Z)
    x1, y1 = tile_xy(BBOX[0], BBOX[3], Z)
    found, misses, n = {}, 0, 0
    total = (x1 - x0 + 1) * (y1 - y0 + 1)
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            n += 1
            try:
                req = urllib.request.Request(TILE % (Z, x, y),
                                             headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=25) as r:
                    raw = r.read()
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    misses += 1
                continue
            except Exception:
                misses += 1
                continue
            try:
                layers = mvt.read(raw, x, y, Z)
            except Exception:
                misses += 1
                continue
            for row in layers.get("gpo_t", []):
                p = row["props"]
                if not row["lonlat"] or not p.get("id"):
                    continue
                found[p["id"]] = {
                    "register_id": p["id"],
                    "name_lt": p.get("pavadinimas"),
                    "name_en": p.get("eng_pavadinimas"),
                    "kind_code": p.get("kind"),
                    "kind": KINDS.get(p.get("kind"), p.get("kind")),
                    "longitude": round(row["lonlat"][0], 6),
                    "latitude": round(row["lonlat"][1], 6),
                    # status 1 is the only value seen; kept raw rather than
                    # guessed at, because a register's status field is exactly
                    # the kind of thing that means something we do not know.
                    "status_raw": p.get("status"),
                }
            if n % 60 == 0:
                print("  %d/%d tiles, %d objects" % (n, total, len(found)),
                      file=sys.stderr)
            # Politeness: this is somebody's public map server, not an API we
            # were given. Roughly five requests a second, single threaded.
            time.sleep(0.2)
    return found, misses, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args()
    if not a.fetch:
        print(__doc__)
        return 0

    found, misses, total = sweep()
    rows = sorted(found.values(), key=lambda r: r["register_id"])
    trees = [r for r in rows if r["kind_code"] == "gpo_bot_t"]
    for r in trees:
        # Named or not, every one of these is a lead: the register says
        # protected, never that the tree is alive or worth the walk.
        r["publishable"] = bool(r.get("name_lt"))
    doc = {
        "source": "Lietuvos Respublikos saugomų teritorijų valstybės kadastras "
                  "(STVK), gamtos paveldo objektai, botanical objects",
        "endpoint": "https://stvk.lt/tiles/maps/stvk/11/{x}/{y}.pbf "
                    "(public Mapbox vector tiles behind the stvk.lt/map "
                    "viewer; layer gpo_t, kind gpo_bot_t)",
        "country": "Lithuania",
        "designation": "gamtos paveldo objektas (nature heritage object), "
                       "botanical category, state protection",
        "licence": "Commercial reuse explicitly permitted; no named licence",
        "licence_proof": "data.gov.lt dataset 3040 (Lietuvos Respublikos "
                         "saugomų teritorijų valstybės kadastras), read in a "
                         "browser 2026-08-16: 'Duomenys gali būti naudojami "
                         "komerciniais ir nekomerciniais tikslais' (the data "
                         "may be used for commercial and non-commercial "
                         "purposes). Recorded as a permission sentence rather "
                         "than a licence tag, because the portal names no "
                         "licence for this dataset.",
        "attribution": "Lietuvos Respublikos saugomų teritorijų valstybės "
                       "kadastras (STVK), Valstybinė saugomų teritorijų "
                       "tarnyba, extract of 2026-08-16",
        "fetched": "2026-08-16",
        "scope": "%d nature heritage objects swept at zoom 11 over Lithuania "
                 "(%d tiles, %d failed); %d are botanical, the rest geological, "
                 "geomorphological, hydrographic or zoological and dropped."
                 % (len(rows), total, misses, len(trees)),
        "caveat": "Coordinates are decoded from vector tiles, so they carry "
                  "tile rounding of a few metres and are not survey positions: "
                  "default to location_precision approximate. No age, girth or "
                  "vitality field. The botanical category covers shrubs and "
                  "tree groups as well as single trees, and the name is the "
                  "only thing that distinguishes them, so each is a lead to "
                  "verify. Objects whose tile carried no name are kept with "
                  "publishable=false rather than dropped.",
        "count": len(trees),
        "trees": trees,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    print("%d objects, %d botanical -> %s"
          % (len(rows), len(trees), os.path.relpath(OUT, ROOT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
