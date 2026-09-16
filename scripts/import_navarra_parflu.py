#!/usr/bin/env python3
"""Import Navarra's Parque Fluvial de la Comarca de Pamplona singular trees.

The companion layer to navarra-sitna.json, named in OPEN_DATA_SURVEY.md's
Navarra scouting note ("A companion layer covers 8 trees in the Pamplona
river park, a walkable cluster on its own") but never actually imported.
8 trees along the Arga river park, mostly black poplars.

Licence, read from the dataset's own catalogue page (datosabiertos.navarra.es,
spasitnaparflu_sym_arbolsing-xml): "Creative Commons Attribution 4.0", linking
publications.europa.eu's CC_BY_4_0 authority entry. No non-commercial clause
stated.

Unlike the Monumentos Naturales layer, this register carries no per-tree name
and no declaration year: DESCRIPCIO is a free-text field mixing size figures
(diametro, i.e. diameter, not girth) with condition notes, so no unit
conversion happens here; a verify pass reads the raw Spanish text.

    python3 scripts/import_navarra_parflu.py [path-to-zip]
"""
import json
import os
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shapefile_reader import read_points  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "registers" / "navarra-parflu.json"
URL = "https://idena.navarra.es/descargas/PARFLU_Sym_ArbolSing.zip"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "parflu.zip"
    z = zipfile.ZipFile(path)
    base = next(n[:-4] for n in z.namelist() if n.endswith(".shp"))
    rows = read_points(z.read(base + ".shp"), z.read(base + ".dbf"),
                       z.read(base + ".prj").decode("latin-1"))
    entries = []
    for r in rows:
        entries.append({
            "feature_id": r.get("FEATURE"),
            "tree_no": r.get("CARBOL"),
            "species": r.get("ESPECIE") or "",
            "description_es": r.get("DESCRIPCIO") or "",
            "surveyed": r.get("BEGINLIFE") or None,
            "latitude": r["lat"],
            "longitude": r["lng"],
        })
    print(f"{len(entries)} trees in the Pamplona river park layer")
    payload = {
        "source": "Gobierno de Navarra, SITNA/IDENA, Parque Fluvial de la Comarca de Pamplona - Arboles Singulares",
        "endpoint": URL,
        "licence": "CC BY 4.0",
        "licence_proof": ("datosabiertos.navarra.es's own catalogue page for this dataset "
                          "(spasitnaparflu_sym_arbolsing-xml) states 'Creative Commons Attribution 4.0', "
                          "linking publications.europa.eu's CC_BY_4_0 authority entry. No non-commercial "
                          "clause stated."),
        "designation": "Arbol singular del Parque Fluvial de la Comarca de Pamplona (not a Monumento Natural; a "
                       "regional-park inventory of notable trees, distinct from navarra-sitna.json)",
        "country": "Spain",
        "attribution": "Informacion geografica propiedad del Gobierno de Navarra",
        "fetched": "2026-09-16",
        "scope": ("All 8 entries in the shapefile. DESCRIPCIO is free Spanish text mixing size (usually "
                  "diametro/diameter in cm, not girth) with condition notes; a verify pass must read and "
                  "convert it, never trust a bare number without checking which measurement it is."),
        "caveat": ("Coordinates were published in ETRS89 / UTM zone 30N and converted here; ETRS89 and WGS84 "
                   "differ by centimetres in Europe. No individual name, no declaration/protection year, no "
                   "age: BEGINLIFE looks like a survey date (all 8 share 08/01/2013) rather than a planting "
                   "date, do not read it as one. Several entries plausibly describe more than one trunk at "
                   "one point ('2 chopos lombardos', 'Chopos de gran tamano'); check whether each is a single "
                   "collectible point before shipping."),
        "entries": entries,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
