#!/usr/bin/env python3
"""Import Andalusia's register of singular trees (REDIAM) into data/registers/.

749 trees across eight province KML files, decimal WGS84 per tree, and every
entry links to its own official PDF sheet, which is the cheapest verification
path in Spain. It deepens five cities we already publish (Seville, Granada,
Cordoba, Cadiz, Malaga) as much as it opens new ones.

Licence: CC BY 4.0, stated in the dataset's own metadata record. Recorded in
OPEN_DATA_SURVEY.md with the proving sentence. The Junta mixes CC BY, CC BY-NC
and CC BY 3.0 across its portal, so that proof authorises this dataset and
nothing else from that source.

The KML files are ISO-8859-1, their descriptions are HTML inside CDATA, and
the useful fields (what makes the tree singular, and the PDF sheet) live in
that HTML rather than in KML elements.

Usage:
    python3 scripts/import_rediam.py <dir-of-kml-files>
"""
import argparse
import glob
import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "registers" / "andalucia-rediam.json"

PROVINCES = {"al": "Almeria", "ca": "Cadiz", "co": "Cordoba", "gr": "Granada",
             "hu": "Huelva", "ja": "Jaen", "ma": "Malaga", "se": "Sevilla"}

PLACEMARK = re.compile(r"<Placemark[^>]*id=\"(\d+)\"[^>]*>(.*?)</Placemark>", re.S)
NAME = re.compile(r"<name>(.*?)</name>", re.S)
COORDS = re.compile(r"<coordinates>\s*([-\d.]+)\s*,\s*([-\d.]+)", re.S)
SINGULARIDAD = re.compile(r"Singularidad:\s*<b>(.*?)</b>", re.S)
PDF = re.compile(r"href=\"(http[^\"]*?Arb_\d+\.pdf)\"", re.S)


def clean(text):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", text))).strip()


def parse_kml(path, province):
    raw = open(path, encoding="iso-8859-1").read()
    out = []
    for pid, body in PLACEMARK.findall(raw):
        name = NAME.search(body)
        coords = COORDS.search(body)
        if not name or not coords:
            continue
        lon, lat = float(coords.group(1)), float(coords.group(2))
        singular = SINGULARIDAD.search(body)
        pdf = PDF.search(body)
        out.append({
            "id": f"rediam_{pid}",
            "name": clean(name.group(1)),
            "province": province,
            # Why the register calls it singular: size, age, shape, rarity,
            # landscape or history. Useful as a first filter on what is
            # actually worth a walk.
            "criteria": clean(singular.group(1)) if singular else None,
            "sheet_pdf": pdf.group(1) if pdf else None,
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("directory", help="folder holding arb_<province>.kml files")
    args = ap.parse_args()

    entries = []
    for path in sorted(glob.glob(os.path.join(args.directory, "arb_*.kml"))):
        code = os.path.basename(path).split("_")[-1].split(".")[0]
        province = PROVINCES.get(code)
        if not province:
            print(f"  skipping {os.path.basename(path)}: unknown province code", file=sys.stderr)
            continue
        found = parse_kml(path, province)
        print(f"  {province:9} {len(found):4}")
        entries.extend(found)

    seen, unique = set(), []
    for e in entries:
        if e["id"] in seen:
            continue
        seen.add(e["id"])
        unique.append(e)

    with_pdf = sum(1 for e in unique if e["sheet_pdf"])
    print(f"total {len(unique)} trees, {with_pdf} with an official PDF sheet")
    if not unique:
        print("nothing parsed, refusing to write", file=sys.stderr)
        return 1

    payload = {
        "source": "REDIAM, Inventario de arboles y arboledas singulares de Andalucia (Andalusia's register of singular trees)",
        "endpoint": "https://portalrediam.cica.es/descargas/ (eight province KML files, arb_sing_<province>.kml)",
        "licence": "CC BY 4.0",
        "licence_proof": "The dataset's own metadata record (GeoNetwork uuid c5d37ec9-a857-42b2-a8d2-2e0d4b947a4e, 'Inventario de arboles y arboledas singulares de Andalucia') carries the licence 'Creative Commons Attribution 4.0 International Public License (CC BY 4.0)'. The Junta mixes CC BY, CC BY-NC and CC BY 3.0 across its portal, so this proof covers this dataset only.",
        "designation": "Arbol singular de Andalucia",
        "country": "Spain",
        "attribution": "REDIAM, Junta de Andalucia",
        "fetched": "2026-08-05",
        "scope": "Individual singular trees only (arb_sing_*). The companion groves layer (arbda_sing_*) is deliberately not imported: a grove is not a collectible point.",
        "caveat": "Each entry links to an official PDF sheet with species, dimensions and history, which is the verification path. The register carries no vitality field, so whether a tree still stands is a per-tree check. The register says singular, not that it is worth the walk.",
        "entries": unique,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n")
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
