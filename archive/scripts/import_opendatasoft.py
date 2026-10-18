#!/usr/bin/env python3
"""Import remarkable-tree datasets from Opendatasoft city portals.

Paris and Brussels both run Opendatasoft, both publish a curated remarkable-tree
dataset rather than a bulk inventory, and both give more per tree than any
national register does. One paginated fetch each.

    python3 scripts/import_opendatasoft.py paris
    python3 scripts/import_opendatasoft.py brussels

A note on licences, because they differ in a way that matters. Brussels is
CC BY 4.0 and behaves like every other register here. Paris is ODbL, which is
share-alike: publishing a derived database can oblige us to offer that database
under ODbL too. Our explore map publishes exactly such a derived file
(assets/registers.json), so Paris is imported with `publish_dots: false` and
stays a research source until Hidde decides whether our own register file may
carry ODbL terms. That is his call, not a run's: it is about how this project
licenses what it publishes.
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SETS = {
    "paris": {
        "base": "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/arbresremarquablesparis",
        "out": "paris-arbres-remarquables.json",
        "licence": "ODbL",
        "publish_dots": False,
        "designation": "Arbre remarquable de Paris",
        "attribution": "Ville de Paris, Direction des Espaces Verts et de l'Environnement",
        "licence_proof": ("The dataset page on opendata.paris.fr states ODbL (Open Database License). "
                          "ODbL is share-alike for derived databases, so these entries are held back "
                          "from the published map layer until that is decided."),
        "country": "France",
        "city": "Paris",
    },
    "brussels": {
        "base": "https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/bruxelles_arbres_remarquables",
        "out": "brussels-arbres-remarquables.json",
        "licence": "CC BY 4.0",
        "publish_dots": True,
        "designation": "Arbre remarquable de Bruxelles",
        "attribution": "heritage.brussels",
        "licence_proof": ("The dataset metadata on opendata.brussels.be states CC BY 4.0, publisher "
                          "heritage.brussels."),
        "country": "Belgium",
        "city": "Brussels",
    },
}


def fetch_all(base):
    rows, offset = [], 0
    while True:
        url = f"{base}/records?" + urllib.parse.urlencode({"limit": 100, "offset": offset})
        with urllib.request.urlopen(urllib.request.Request(
                url, headers={"User-Agent": "AncientTrees/import"}), timeout=90) as r:
            page = json.load(r)
        rows.extend(page.get("results", []))
        total = page.get("total_count", 0)
        offset += 100
        if offset >= total or not page.get("results"):
            return rows, total
        time.sleep(0.4)


def paris_entry(r):
    geo = r.get("geom_x_y") or {}
    genus = (r.get("arbres_genre") or "").strip()
    species = (r.get("arbres_espece") or "").strip()
    planted = (r.get("arbres_dateplantation") or "")[:4]
    return {
        "register_id": r.get("arbres_idbase"),
        "name": r.get("com_nom_usuel") or r.get("arbres_libellefrancais") or "",
        "species": " ".join(x for x in (genus, species) if x),
        "common_fr": r.get("arbres_libellefrancais"),
        "place": r.get("com_site") or r.get("arbres_adresse") or "",
        "address": r.get("com_adresse") or r.get("arbres_adresse"),
        "arrondissement": r.get("com_arrondissement"),
        # Paris publishes girth in centimetres and height in metres.
        "girth_cm": r.get("arbres_circonferenceencm"),
        "height_m": r.get("arbres_hauteurenm"),
        "planted": planted if planted and planted != "1700" else None,
        "latitude": geo.get("lat"),
        "longitude": geo.get("lon"),
    }


def brussels_entry(r):
    geo = r.get("geo_point_2d") or {}
    girth_m = r.get("circonference")
    return {
        "register_id": r.get("id_arbres_cms"),
        "name": r.get("nom_fr") or r.get("nom_nl") or "",
        "name_nl": r.get("nom_nl"),
        "species": r.get("nom_la") or "",
        "status": r.get("statuts_fr"),
        # Brussels publishes girth in METRES. Converted here, because the column
        # name says circonference and a bare 3.16 has already been misread as
        # centimetres once on another register.
        "girth_cm": round(girth_m * 100) if isinstance(girth_m, (int, float)) else None,
        "crown_m": r.get("diametre_cime"),
        "url": r.get("url_fr"),
        "latitude": geo.get("lat"),
        "longitude": geo.get("lon"),
    }


BUILDERS = {"paris": paris_entry, "brussels": brussels_entry}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in SETS:
        print("usage: import_opendatasoft.py [%s]" % "|".join(SETS), file=sys.stderr)
        return 1
    key = sys.argv[1]
    cfg = SETS[key]
    rows, total = fetch_all(cfg["base"])
    entries = [e for e in (BUILDERS[key](r) for r in rows)
               if e["latitude"] is not None and e["longitude"] is not None]
    print(f"{key}: {total} records reported, {len(rows)} fetched, {len(entries)} with coordinates")

    payload = {
        "source": f"{cfg['attribution']}, remarkable trees of {cfg['city']}",
        "endpoint": cfg["base"],
        "licence": cfg["licence"],
        "licence_proof": cfg["licence_proof"],
        "designation": cfg["designation"],
        "country": cfg["country"],
        "attribution": cfg["attribution"],
        "fetched": "2026-08-05",
        "publish_dots": cfg["publish_dots"],
        "scope": ("A curated remarkable-tree list published by the city itself, not a bulk street-tree "
                  "inventory, which our own rules forbid importing."),
        "caveat": ("The register carries no vitality field, so whether a tree still stands is a per-tree "
                   "check. Ages, where present, are planting years rather than estimates."),
        "entries": entries,
    }
    out = ROOT / "data" / "registers" / cfg["out"]
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
