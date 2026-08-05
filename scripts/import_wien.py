#!/usr/bin/env python3
"""Import Vienna's Naturdenkmale (natural monuments) into data/registers/.

762 declared monuments, of which 394 are a single tree. The rest are woods,
groups of four or more, avenues, tree lines, meadows, watercourses and
geological outcrops: all real monuments, none of them a place to stand in front
of one tree, so they are kept and flagged rather than dropped.

Licence: the city's own WFS capabilities document declares CC BY 3.0 AT
(https://creativecommons.org/licenses/by/3.0/at/deed.de) as its fee terms, with
terms of use at https://data.wien.gv.at/nutzungsbedingungen. Attribution
required, commercial use allowed.

    python3 scripts/import_wien.py
"""
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "registers" / "wien-naturdenkmale.json"
URL = ("https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0"
       "&typeName=ogdwien:NATDENKMALPKTOGD&srsName=EPSG:4326&outputFormat=json")
SINGLE = "Einzelbaum"


def main():
    with urllib.request.urlopen(urllib.request.Request(
            URL, headers={"User-Agent": "AncientTrees/import"}), timeout=120) as r:
        data = json.load(r)
    entries = []
    for f in data["features"]:
        p = f["properties"]
        lon, lat = f["geometry"]["coordinates"]
        e = {
            "register_id": p.get("OBJECTID"),
            "name": p.get("ARTBEZ") or "",
            "species": p.get("WISSBEZ") or "",
            "place": (p.get("ADRESSE") or "").strip(" -"),
            "district": p.get("BEZ"),
            "monument_type": p.get("ND_TYP"),
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
        }
        if p.get("ND_TYP") != SINGLE:
            e["group"] = True
        entries.append(e)
    singles = [e for e in entries if not e.get("group")]
    print(f"{len(entries)} declared monuments, {len(singles)} single trees")
    OUT.write_text(json.dumps({
        "source": "Stadt Wien, Naturdenkmale (declared natural monuments)",
        "endpoint": URL,
        "licence": "CC BY 3.0 AT",
        "licence_proof": ("The city's own WFS capabilities document declares "
                          "https://creativecommons.org/licenses/by/3.0/at/deed.de as its fee terms, "
                          "with access constraints at https://data.wien.gv.at/nutzungsbedingungen. "
                          "Attribution required, commercial use allowed."),
        "designation": "Naturdenkmal Wien",
        "country": "Austria",
        "attribution": "Stadt Wien, data.wien.gv.at",
        "fetched": "2026-08-05",
        "publish_dots": True,
        "scope": ("All 762 declared monuments. 'group': true marks everything that is not a single "
                  "tree: woods, groups of four or more, avenues, tree lines, meadows, watercourses "
                  "and geological outcrops."),
        "caveat": ("No age and no vitality field, so both stay per-tree work. A second city "
                   "department publishes a Baumkataster carrying planting year, girth, crown and "
                   "height for the same trees, which is the cheapest second source in Vienna."),
        "entries": entries,
    }, ensure_ascii=False, indent=1) + "\n")
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
