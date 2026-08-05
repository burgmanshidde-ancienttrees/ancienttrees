#!/usr/bin/env python3
"""Import Italy's national monumental tree register (MASAF) into data/registers/.

The single biggest coverage lever in Europe: 5,008 entries across 21 regional
files, one identical schema, CC BY 4.0, with per-tree coordinates, girth,
height and an urban/rural flag that filters city trees for free.

Two things this has to get right, and both have already bitten someone:

1. **Groups are not collectible points.** MASAF records avenues and stands as a
   single entry whose species field reads "Insieme omogeneo di ..." (a
   homogeneous set of). 485 of the 5,008 are those, and they fail the
   collectible-point test in CLAUDE.md by default. They are kept in the file,
   flagged, never treated as a tree.
2. **The coordinates are sexagesimal text.** "37° 17' 22,25''" with a comma for
   the decimal point. Converted here, and checked against Sicily's own GeoJSON
   republication, which carries the same trees in decimal degrees.

Usage:
    python3 scripts/import_masaf.py <dir-of-xls-files> [--check sicilia.geojson]

Downloads are not automated on purpose: the 21 files sit behind per-file
attachment URLs on masaf.gov.it that change with each decree update, so the
fetch stays a deliberate step and the URLs live in the register file itself.
"""
import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xls_parser import load_xls, grid_to_rows  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "registers" / "italy-masaf.json"

COLS = ["progr", "region", "sheet_id", "province", "comune", "locality",
        "lat_dms", "lon_dms", "altitude_m", "urban", "species", "name_it",
        "girth_cm", "height_m", "criteria", "public_interest"]

DMS = re.compile(r"""^\s*(\d+)\s*°\s*(\d+)\s*'\s*([\d.,]+)\s*(?:''|"|″)?\s*$""")
GROUP_PREFIX = "insieme"


def dms_to_decimal(text):
    """'37° 17' 22,25''' to 37.289514. Returns None on anything unexpected,
    because a coordinate we cannot read is better absent than guessed."""
    if text is None:
        return None
    m = DMS.match(str(text).replace(" ", " "))
    if not m:
        return None
    deg, minutes, seconds = m.groups()
    try:
        return int(deg) + int(minutes) / 60.0 + float(seconds.replace(",", ".")) / 3600.0
    except ValueError:
        return None


def number(text):
    """Italian decimal comma to float, blanks to None."""
    if text is None:
        return None
    s = str(text).strip().replace(",", ".")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def read_rows(directory):
    rows = []
    for path in sorted(glob.glob(os.path.join(directory, "*.xls"))):
        sheets = load_xls(path)
        if not sheets:
            print(f"  {os.path.basename(path)}: no sheets", file=sys.stderr)
            continue
        _, grid = sheets[0]
        table = grid_to_rows(grid)
        if len(table) < 2:
            continue
        header = [str(c).strip() for c in table[0]]
        if header[0] != "PROGR":
            print(f"  {os.path.basename(path)}: unexpected header {header[:3]}", file=sys.stderr)
            continue
        rows.extend(table[1:])
    return rows


def build(rows):
    entries, dropped = [], 0
    for r in rows:
        r = list(r) + [None] * (len(COLS) - len(r))
        rec = {k: (str(v).strip() if isinstance(v, str) else v) for k, v in zip(COLS, r)}
        lat = dms_to_decimal(rec["lat_dms"])
        lon = dms_to_decimal(rec["lon_dms"])
        if lat is None or lon is None:
            dropped += 1
            continue
        species = str(rec["species"] or "").strip()
        entry = {
            "sheet_id": rec["sheet_id"],
            "region": rec["region"],
            "province": rec["province"],
            "comune": rec["comune"],
            "locality": rec["locality"],
            "species": species,
            "name_it": rec["name_it"],
            "girth_cm": number(rec["girth_cm"]),
            "height_m": number(rec["height_m"]),
            "altitude_m": number(rec["altitude_m"]),
            "urban": str(rec["urban"] or "").strip().startswith("s"),
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
        }
        if species.lower().startswith(GROUP_PREFIX):
            # An avenue or a stand. Kept for the record, never a collectible
            # point: there is nowhere obvious to stand and nothing to have seen.
            entry["group"] = True
        entries.append(entry)
    return entries, dropped


def check_against_geojson(entries, path):
    """Sicily republishes the same trees in decimal degrees. If our conversion
    is right the two agree to within a few metres."""
    ref = {}
    for f in json.load(open(path))["features"]:
        sid = f["properties"].get("ID SCHEDA")
        lon, lat = f["geometry"]["coordinates"]
        if sid:
            ref[sid] = (lat, lon)
    gaps = []
    for e in entries:
        if e["sheet_id"] in ref:
            lat, lon = ref[e["sheet_id"]]
            gaps.append(max(abs(lat - e["latitude"]), abs(lon - e["longitude"])) * 111000)
    if not gaps:
        return 0, 0.0, 0
    gaps.sort()
    # The median is the test, not the worst case. Sicily's GeoJSON is the 2021
    # republication and the .xls is the 2025 decree, so a handful of trees have
    # genuinely been re-surveyed in between. A conversion error would move all
    # of them, not three.
    median = gaps[len(gaps) // 2]
    return len(gaps), median, sum(1 for g in gaps if g > 5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("directory", help="folder holding the 21 regional .xls files")
    ap.add_argument("--check", help="Sicily GeoJSON to validate the conversion against")
    args = ap.parse_args()

    rows = read_rows(args.directory)
    entries, dropped = build(rows)
    singles = [e for e in entries if not e.get("group")]
    urban = [e for e in singles if e["urban"]]
    print(f"rows {len(rows)}, usable {len(entries)}, unreadable coordinates {dropped}")
    print(f"single trees {len(singles)}, of which urban {len(urban)}; groups {len(entries) - len(singles)}")

    if args.check:
        checked, median, moved = check_against_geojson(entries, args.check)
        print(f"cross-checked {checked} Sicilian trees against their own GeoJSON: "
              f"median disagreement {median:.1f} m, {moved} tree(s) more than 5 m apart")
        if median > 2 or moved > checked * 0.05:
            print("conversion looks wrong, refusing to write", file=sys.stderr)
            return 1

    payload = {
        "source": "MASAF, Elenco degli alberi monumentali d'Italia (Italy's national register of monumental trees)",
        "endpoint": "https://www.masaf.gov.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/11260 (21 regional .xls files)",
        "licence": "CC BY 4.0",
        "licence_proof": "The register page publishes the regional lists under CC BY 4.0; the Sicilian republication of the same data carries license_id cc-by in its portal metadata (dati.regione.sicilia.it, dataset alberi-monumentali-di-sicilia).",
        "designation": "Albero monumentale d'Italia",
        "country": "Italy",
        "attribution": "MASAF",
        "fetched": "2026-08-05",
        "scope": "All 5,008 register entries. 'group': true marks the 485 that are avenues or stands rather than one tree, and those are not collectible points.",
        "caveat": "Coordinates are converted from the sexagesimal text in the register. The photo gallery on masaf.gov.it is explicitly NOT under the CC BY licence: data yes, images never. An entry says protected, not that it is worth the walk, and the register carries no vitality field, so whether a tree still stands is a per-tree check.",
        "entries": entries,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n")
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
