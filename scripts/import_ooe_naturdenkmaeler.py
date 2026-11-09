#!/usr/bin/env python3
"""Import Upper Austria's Naturdenkmaeler (INSPIRE GML) into data/registers/.

446 declared natural monuments, each a polygon with a site name and the date of
the Bescheid. No species, age or girth. Tree sites are told apart by their
name (Eibe, Linde, Eiche ...); springs, ponds, rocks and caves are kept and
flagged `non_tree`. Coordinates are polygon centroids, so they are approximate.

Licence: CC BY 4.0, declared on the distributions of data.europa.eu dataset
50a04bcd-858a-4656-b136-f8de18d8f9c0 (Land Oberoesterreich via inspire.gv.at).
Proof sentence in OPEN_DATA_SURVEY.md.

    python3 scripts/import_ooe_naturdenkmaeler.py [path/to/VWNaturdenkmaeler_ETRS89TM33N.zip]

Without an argument it downloads the zip into out/dl/ooe/.
"""
import json
import math
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "registers" / "ooe-naturdenkmaeler.json"
URL = "https://www.doris.at/service/metadaten/daten/VWNaturdenkmaeler_ETRS89TM33N.zip"
ZIP = ROOT / "out" / "dl" / "ooe" / "nd.zip"

TREE_WORDS = ("eibe", "linde", "eiche", "buche", "ulme", "ahorn", "esche", "kastanie", "platane",
              "birke", "pappel", "weide", "tanne", "fichte", "kiefer", "zeder", "zirbe", "laerche",
              "lärche", "nussbaum", "baum", "baeume", "bäume", "allee", "tilia", "taxus", "quercus",
              "fagus", "acer", "ulmus", "fraxinus")


def utm33_to_wgs84(easting, northing):
    """Inverse transverse Mercator, ETRS89 / UTM 33N (GRS80, same as WGS84 to the metre)."""
    a, f = 6378137.0, 1 / 298.257222101
    k0, lon0 = 0.9996, math.radians(15.0)
    e2 = f * (2 - f)
    ep2 = e2 / (1 - e2)
    x, y = easting - 500000.0, northing
    m = y / k0
    mu = m / (a * (1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256))
    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))
    phi1 = (mu + (3 * e1 / 2 - 27 * e1 ** 3 / 32) * math.sin(2 * mu)
            + (21 * e1 ** 2 / 16 - 55 * e1 ** 4 / 32) * math.sin(4 * mu)
            + (151 * e1 ** 3 / 96) * math.sin(6 * mu)
            + (1097 * e1 ** 4 / 512) * math.sin(8 * mu))
    s, c, t = math.sin(phi1), math.cos(phi1), math.tan(phi1)
    n1 = a / math.sqrt(1 - e2 * s ** 2)
    t1, c1 = t ** 2, ep2 * c ** 2
    r1 = a * (1 - e2) / (1 - e2 * s ** 2) ** 1.5
    d = x / (n1 * k0)
    lat = phi1 - (n1 * t / r1) * (d ** 2 / 2 - (5 + 3 * t1 + 10 * c1 - 4 * c1 ** 2 - 9 * ep2) * d ** 4 / 24
                                  + (61 + 90 * t1 + 298 * c1 + 45 * t1 ** 2 - 252 * ep2 - 3 * c1 ** 2) * d ** 6 / 720)
    lon = lon0 + (d - (1 + 2 * t1 + c1) * d ** 3 / 6
                  + (5 - 2 * c1 + 28 * t1 - 3 * c1 ** 2 + 8 * ep2 + 24 * t1 ** 2) * d ** 5 / 120) / c
    return math.degrees(lat), math.degrees(lon)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ZIP
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(urllib.request.Request(
                URL, headers={"User-Agent": "AncientTrees/import"}), timeout=60) as r:
            path.write_bytes(r.read())
    z = zipfile.ZipFile(path)
    gml = z.read(z.namelist()[0]).decode("utf-8", "replace")
    entries = []
    for part in gml.split("<gml:featureMember>")[1:]:
        pos = re.search(r"<gml:posList>([^<]+)</gml:posList>", part)
        name = re.search(r"<gn:text>([^<]*)</gn:text>", part)
        local = re.search(r"<base:localId>([^<]*)</base:localId>", part)
        bescheid = re.search(r"<gco:CharacterString>(Bescheid[^<]*)</gco:CharacterString>", part)
        if not (pos and name):
            continue
        v = [float(x) for x in pos.group(1).split()]
        north, east = v[0::2], v[1::2]
        lat, lon = utm33_to_wgs84(sum(east) / len(east), sum(north) / len(north))
        nm = name.group(1).strip()
        e = {
            "register_id": local.group(1) if local else None,
            "name": nm,
            "legal_basis": bescheid.group(1) if bescheid else "",
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "location_precision": "approximate",
        }
        if not any(w in nm.lower() for w in TREE_WORDS):
            e["non_tree"] = True
        entries.append(e)
    trees = [e for e in entries if not e.get("non_tree")]
    print(f"{len(entries)} monuments, {len(trees)} named like trees")
    OUT.write_text(json.dumps({
        "source": "Land Oberoesterreich, Naturdenkmaeler Oberoesterreich (INSPIRE ProtectedSite)",
        "endpoint": URL,
        "licence": "CC BY 4.0",
        "licence_proof": ("data.europa.eu dataset 50a04bcd-858a-4656-b136-f8de18d8f9c0 declares "
                          "https://creativecommons.org/licenses/by/4.0/ on its distributions (read 2026-11-09)."),
        "designation": "Naturdenkmal Oberoesterreich",
        "country": "Austria",
        "attribution": "Land Oberoesterreich, data.ooe.gv.at",
        "fetched": "2026-11-09",
        "publish_dots": False,
        "scope": ("All declared monuments. Coordinates are polygon centroids (approximate). "
                  "'non_tree': true marks names with no tree word: springs, ponds, rocks, caves."),
        "caveat": ("No species, age or girth. A name may name a group (Drei Eiben, 7 Linden). "
                   "publish_dots stays False until a session decides to show approximate centroids."),
        "entries": entries,
    }, ensure_ascii=False, indent=1) + "\n")
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
