#!/usr/bin/env python3
"""Import Navarra's Monumentos Naturales (trees) into data/registers/.

47 declared natural monuments with per-tree coordinates and species, plus a
companion layer of 8 in the Pamplona river park. Small, but it is the first
Spanish shapefile register imported and it proves the reader that Castilla y
Leon and Aragon need too.

Licence, read from the ISO metadata inside the download itself: "Esta capa se
publica bajo los terminos de la licencia Creative Commons Reconocimiento 4.0
Internacional (CC BY 4.0). Sera necesario nombrar la fuente de procedencia de
la informacion de la manera siguiente: Informacion geografica propiedad del
Gobierno de Navarra."

    python3 scripts/import_navarra.py [path-to-zip]
"""
import json
import os
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shapefile_reader import read_points  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "registers" / "navarra-sitna.json"
URL = "https://idena.navarra.es/descargas/BIODIV_Sym_MonumNat.zip"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "navarra.zip"
    z = zipfile.ZipFile(path)
    base = next(n[:-4] for n in z.namelist() if n.endswith(".shp"))
    rows = read_points(z.read(base + ".shp"), z.read(base + ".dbf"),
                       z.read(base + ".prj").decode("latin-1"))
    entries = []
    for r in rows:
        try:
            count = int(r.get("NUMEJEMP") or 1)
        except ValueError:
            count = 1
        e = {
            "name": r.get("ESPP") or "",
            "name_eu": r.get("NOMBRE_eus") or None,
            "species": r.get("ESPECIE") or "",
            "place": r.get("LUGAR") or "",
            "declared": r.get("YEAR") or None,
            "individuals": count,
            "latitude": r["lat"],
            "longitude": r["lng"],
        }
        if count > 1:
            # The register declares some monuments as a set of trees. A set is
            # not a collectible point: there is no one place to stand.
            e["group"] = True
        entries.append(e)
    singles = [e for e in entries if not e.get("group")]
    print(f"{len(entries)} declared monuments, {len(singles)} single trees, "
          f"{len(entries) - len(singles)} groups")
    payload = {
        "source": "Gobierno de Navarra, SITNA/IDENA, Monumentos Naturales (declared natural monument trees)",
        "endpoint": URL,
        "licence": "CC BY 4.0",
        "licence_proof": ("The ISO metadata inside the download states: Esta capa se publica bajo los "
                          "terminos de la licencia Creative Commons Reconocimiento 4.0 Internacional "
                          "(CC BY 4.0). Sera necesario nombrar la fuente de procedencia de la "
                          "informacion de la manera siguiente: Informacion geografica propiedad del "
                          "Gobierno de Navarra."),
        "designation": "Monumento Natural de Navarra",
        "country": "Spain",
        "attribution": "Informacion geografica propiedad del Gobierno de Navarra",
        "fetched": "2026-08-05",
        "scope": ("All 47 declared tree monuments. 'group': true marks those the register itself "
                  "counts as more than one individual, which are not collectible points."),
        "caveat": ("Coordinates were published in ETRS89 / UTM zone 30N and converted here; ETRS89 and "
                   "WGS84 differ by centimetres in Europe. The register carries no vitality field and no "
                   "age, only the year of declaration, so both stay per-tree checks."),
        "entries": entries,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
