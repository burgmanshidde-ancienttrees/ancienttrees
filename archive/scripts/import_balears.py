#!/usr/bin/env python3
"""Import the Catalogue of Singular Trees of the Balearic Islands.

78 catalogued entries from the Govern de les Illes Balears, served as a live
ArcGIS layer already in WGS84, so no reprojection and no shapefile.

Licence: CC BY. The government's own CKAN catalogue answers
intranet.caib.es/opendatacataleg/api/3/action/package_search?q=arbres with one
dataset, "Arbres Singulars Illes Balears", license_id "cc-by", license_title
"Creative Commons Attribution". The service's own copyrightText is "Servei
d'Informacio Territorial de les Illes Balears (SITIBSA)".

Two fields here that most registers do not have, and both are used:

MORTS and QUEDEN count how many of the catalogued specimens have died and how
many remain. An entry whose survivors have dropped to zero is recorded as
extinct rather than silently dropped, because knowing a catalogued tree is gone
is worth as much as knowing one stands (Hidde, 2026-08-06: import broadly, be
specific later). Nothing extinct may ever become a published entry; that is the
dead-tree rule and it is about what ships, not about what we keep.

PROPIETAT says PUBLICA or PRIVADA. Private entries are imported and flagged,
never mapped: hard rule 10, enforced again in build_site's register loader.

    python3 scripts/import_balears.py
"""
import json
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "registers" / "balears-arbres-singulars.json"
BASE = ("https://ideib.caib.es/geoserveis/rest/services/public/"
        "GOIB_ArbresSingulars_IB/MapServer/0/query")
UA = "AncientTrees/import (https://ancienttrees.app)"


def fetch():
    q = urllib.parse.urlencode({
        "where": "1=1", "outFields": "*", "outSR": 4326, "f": "json",
        "resultRecordCount": 2000,
    })
    req = urllib.request.Request(f"{BASE}?{q}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def clean(v):
    return (str(v).strip() if v not in (None, "") else "") or ""


def main():
    data = fetch()
    entries = []
    for f in data.get("features", []):
        a = f.get("attributes", {})
        g = f.get("geometry") or {}
        lat, lng = g.get("y"), g.get("x")
        if lat is None or lng is None:
            continue
        started = a.get("NÚM_INICI")
        dead = a.get("MORTS")
        left = a.get("QUEDEN")
        private = clean(a.get("PROPIETAT")).upper().startswith("PRIV")
        # More than one specimen under one catalogue entry is an ensemble, not a
        # place to stand in front of one tree.
        group = bool(left and left > 1)
        e = {
            "register_id": a.get("OBJECTID"),
            "name": clean(a.get("NOM")),
            "species": clean(a.get("ESPÈCIE")),
            "place": clean(a.get("MUNICIPI")).title(),
            "island": clean(a.get("ILLA")).title(),
            "catalogued": int(a["ANY_CATALO"]) if a.get("ANY_CATALO") else None,
            "latitude": round(lat, 6),
            "longitude": round(lng, 6),
            "ownership": clean(a.get("PROPIETAT")).title(),
            "holder": clean(a.get("TITULAR")),
            "specimens_catalogued": int(started) if started else None,
            "specimens_dead": int(dead) if dead is not None else None,
            "specimens_remaining": int(left) if left is not None else None,
            "notes": clean(a.get("OBSERVACIO")),
            "url": clean(a.get("WEB")),
        }
        if group:
            e["group"] = True
        if private:
            e["private"] = True
        if left == 0:
            e["extinct"] = True
        entries.append(e)

    entries.sort(key=lambda e: (e["island"], e["place"], e["name"]))
    priv = sum(1 for e in entries if e.get("private"))
    grp = sum(1 for e in entries if e.get("group"))
    gone = sum(1 for e in entries if e.get("extinct"))
    out = {
        "source": ("Govern de les Illes Balears, Cataleg d'Arbres Singulars "
                   "(catalogue of singular trees)"),
        "endpoint": BASE,
        "licence": "CC BY",
        "licence_proof": (
            "The Govern's own open data catalogue API "
            "(intranet.caib.es/opendatacataleg/api/3/action/package_search?q=arbres, "
            "the host catalegdades.caib.cat now redirects to) returns the dataset "
            "\"Arbres Singulars Illes Balears\" with license_id \"cc-by\" and "
            "license_title \"Creative Commons Attribution\". The ArcGIS service's "
            "own copyrightText reads \"Servei d'Informacio Territorial de les "
            "Illes Balears (SITIBSA)\"."),
        "designation": "Arbre Singular de les Illes Balears",
        "country": "Spain",
        "attribution": "Govern de les Illes Balears (SITIBSA)",
        "fetched": date.today().isoformat(),
        "publish_dots": True,
        "scope": (
            f"All {len(entries)} catalogued entries. 'group': true marks the "
            f"{grp} entries holding more than one surviving specimen, which are "
            f"not a single place to stand. 'private': true marks the {priv} on "
            f"private land, imported for research and never mapped, per hard "
            f"rule 10. 'extinct': true marks the {gone} whose catalogued "
            f"specimens have all died, per the register's own MORTS and QUEDEN "
            f"counts; kept as knowledge, never publishable as an entry."),
        "caveat": (
            "The register counts specimens per catalogue entry rather than per "
            "trunk, so specimens_remaining is the number still alive under one "
            "name. Coordinates come from the service in WGS84 and are the "
            "register's own; treat them as approximate until verified, as with "
            "every register."),
        "entries": entries,
    }
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(entries)} entries -> {OUT.relative_to(ROOT)}")
    print(f"  {grp} groups, {priv} private (never mapped), {gone} extinct")
    print(f"  mappable single public living trees: "
          f"{sum(1 for e in entries if not e.get('group') and not e.get('private') and not e.get('extinct'))}")


if __name__ == "__main__":
    main()
