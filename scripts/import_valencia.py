#!/usr/bin/env python3
"""Import the Catalogue of Monumental and Singular Trees of the Comunitat Valenciana.

2,439 protected entries from the Generalitat Valenciana, served as a live
ArcGIS layer, requested in WGS84 so there is no reprojection and no shapefile.
The dataset page advertises a shapefile download, but that URL is an interactive
HTML form rather than a file; the map service behind it answers directly.

Licence: CC BY. The Generalitat's own dataset page embeds
"schema:license": "http://www.opendefinition.org/licenses/cc-by" and displays
"Llicencia Creative Commons Attribution".

Two things this register does NOT carry, and both change how it may be used:

No ownership or access field. Its larger category, "Proteccion Generica", is
automatic under Ley 4/2006 for any tree meeting the size or age criteria,
regardless of who owns the ground, so private trees are certainly included and
cannot be told apart. Hard rule 10 therefore holds the dots back: the file
imports in full for research, and every tree needs its own access check before
it can ship or be mapped.

No vitality field either, so nothing here proves a tree still stands. That is
normal for a register and is a per-tree check, not a reason to skip the import
(Hidde, 2026-08-06: get the data now, be specific later).

    python3 scripts/import_valencia.py
"""
import json
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "registers" / "valencia-arboles-monumentales.json"
BASE = ("https://carto.icv.gva.es/arcgis/rest/services/tm_medio_ambiente/"
        "forestal/MapServer/0/query")
UA = "AncientTrees/import (https://ancienttrees.app)"
PAGE = 1000


def page(offset):
    q = urllib.parse.urlencode({
        "where": "1=1", "outFields": "*", "outSR": 4326, "f": "json",
        "resultOffset": offset, "resultRecordCount": PAGE, "returnGeometry": "true",
    })
    req = urllib.request.Request(f"{BASE}?{q}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def clean(v):
    s = str(v).strip() if v is not None else ""
    return "" if s in ("", "0", "None") else s


def num(v):
    try:
        f = float(v)
        return round(f, 2) if f > 0 else None
    except (TypeError, ValueError):
        return None


def main():
    entries, offset = [], 0
    while True:
        d = page(offset)
        feats = d.get("features", [])
        if not feats:
            break
        for f in feats:
            a = f.get("attributes", {})
            g = f.get("geometry") or {}
            lat, lng = g.get("y"), g.get("x")
            if lat is None or lng is None:
                continue
            elemento = clean(a.get("elemento"))
            e = {
                "register_id": a.get("ipa") or a.get("objectid"),
                "name": clean(a.get("denominaci")),
                "species": clean(a.get("especie")),
                "category": clean(a.get("categoria")),
                "element": elemento,
                "latitude": round(lat, 6),
                "longitude": round(lng, 6),
                "girth_m": num(a.get("tronco")),
                "height_m": num(a.get("altura")),
                "crown_m": num(a.get("copa")),
            }
            # The register flags trees it considers over 350 years, which is the
            # threshold Ley 4/2006 protects automatically. It is a flag, not a
            # measured age, and is recorded as such.
            if clean(a.get("edad350")).lower() == "x":
                e["over_350_years_per_register"] = True
            # An "Arboleda" is a stand of trees, not one place to stand.
            if elemento.lower().startswith("arboleda"):
                e["group"] = True
            entries.append(e)
        offset += PAGE
        if len(feats) < PAGE:
            break

    entries.sort(key=lambda e: (e["name"] or "", e["register_id"] or 0))
    groves = sum(1 for e in entries if e.get("group"))
    old = sum(1 for e in entries if e.get("over_350_years_per_register"))
    local = sum(1 for e in entries if e["category"].startswith("Árbol Monumental"))
    out = {
        "source": ("Generalitat Valenciana, Catalogo de Arboles Monumentales y "
                   "Singulares de la Comunitat Valenciana (Ley 4/2006)"),
        "endpoint": BASE,
        "licence": "CC BY",
        "licence_proof": (
            "The Generalitat's own open data page for this dataset "
            "(dadesobertes.gva.es/va/dataset/catalogo-de-arboles-monumentales-y-"
            "singulares-de-la-comunitat-valenciana) embeds "
            "\"schema:license\": \"http://www.opendefinition.org/licenses/cc-by\" "
            "in its structured data and displays \"Llicencia Creative Commons "
            "Attribution\"."),
        "designation": "Arbol Monumental o Singular de la Comunitat Valenciana",
        "country": "Spain",
        "attribution": "Generalitat Valenciana, Institut Cartografic Valencia (ICV)",
        "fetched": date.today().isoformat(),
        "publish_dots": False,
        "dots_held_reason": (
            "Hard rule 10. This register carries no ownership or access field, and "
            f"its larger category, Proteccion Generica ({len(entries) - local} of "
            f"{len(entries)} entries), applies automatically under Ley 4/2006 to any "
            "tree meeting the size or age criteria regardless of who owns the land. "
            "Private trees are therefore certainly included and cannot be "
            "distinguished, so publishing exact coordinates would send people into "
            "gardens and farmland uninvited. The data is imported in full and is "
            "usable for research; a tree from it reaches a page only after its own "
            "access check. To turn the dots on, find a per-tree ownership or "
            "visitability signal."),
        "scope": (
            f"All {len(entries)} catalogued entries. 'group': true marks the "
            f"{groves} Arboleda stands, which are not a single place to stand. "
            f"{local} carry the declared category Arbol Monumental de Interes "
            f"Local; the rest hold generic statutory protection. "
            f"'over_350_years_per_register': true marks the {old} the register "
            "itself flags as over 350 years, which is a legal threshold flag and "
            "not a measured age."),
        "caveat": (
            "No vitality field, so nothing here proves a tree still stands: that is "
            "a per-tree check, as with every register. Girth, height and crown are "
            "in METRES, not centimetres; the ICNF import once read metres as "
            "centimetres and turned a 2.84 m trunk into 3 cm, so sanity-check any "
            "numeric column against the physical world before trusting it."),
        "entries": entries,
    }
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(entries)} entries -> {OUT.relative_to(ROOT)}")
    print(f"  {groves} groves (not collectible), {local} locally declared monumental, "
          f"{old} flagged over 350 years")
    print("  dots held: no ownership field, hard rule 10")


if __name__ == "__main__":
    main()
