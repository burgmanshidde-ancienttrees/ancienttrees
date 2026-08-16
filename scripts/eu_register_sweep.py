#!/usr/bin/env python3
"""The same register-first sweep, over Europe's open data instead of ArcGIS.

Companion to scripts/register_sweep.py, which searches ArcGIS Online. ArcGIS is
where the anglophone and Australian registers live; it is NOT where most European
ones live, because European governments publish through national CKAN and DCAT
portals that data.europa.eu aggregates. One search there covers every member
state plus Switzerland and Norway.

The reason this is worth its own script rather than more ArcGIS terms: DCAT
records carry an explicit licence field. Licence, not data, has blocked five
registers in a row here, so a catalogue that states the licence up front is
worth more per hit than one that leaves it blank.

A hit is a lead. The portal says a dataset exists and under what licence; it
does not say the dataset is semantically filtered (a "Baumkataster" is a street
inventory and forbidden), nor that its coordinates are usable.

Usage:
    python3 scripts/eu_register_sweep.py
    python3 scripts/eu_register_sweep.py --open-only
"""
import argparse
import json
import os
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "research", "eu-register-sweep.json")
API = "https://data.europa.eu/api/hub/search/search"
UA = "AncientTrees/1.0 (https://ancienttrees.app; burgmans.hidde@gmail.com)"

# The phrase each country's own administration uses. Generic words are left out
# on purpose: "Baumkataster", "tree cadastre" and "arbres" alone return street
# inventories, which the semantic filter forbids however open the licence.
TERMS = [
    "arbres remarquables", "arbre remarquable",
    "arboles singulares", "arbol singular", "arbres monumentals",
    "alberi monumentali", "albero monumentale",
    "arvores monumentais", "arvore de interesse publico",
    "bijzondere bomen", "monumentale bomen",
    "Naturdenkmal Baum", "Naturdenkmale",
    "pomniki przyrody", "pamatne stromy", "chranene stromy",
    "vardefulla trad", "naturminne", "verneverdige trar",
    "muistomerkki puu", "kaitstavad looduse uksikobjektid",
    "gamtos paveldo objektai", "aizsargajamie koki",
    "vedecke stromy", "emlekfa", "arbori remarcabili",
    "vekove stromy", "spomenik prirode drvo",
]

# What a licence string has to contain before it is worth reading. Anything
# else is recorded verbatim rather than judged, because a licence verdict is a
# human's to make at the primary source, per OPEN_DATA_SURVEY.md.
OPEN_HINTS = ("cc-by", "cc_by", "ccby", "cc0", "creative", "odbl", "dl-de",
              "etalab", "pddl", "public domain", "attribution", "opendata")


def search(term, limit=60):
    url = API + "?" + urllib.parse.urlencode(
        {"q": term, "limit": limit, "filter": "dataset"})
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.load(r).get("result", {})
    except Exception as e:
        print("  ! %s: %s" % (term, e))
        return {}


def text(v):
    """DCAT titles and descriptions are per-language dicts; prefer English."""
    if isinstance(v, dict):
        return (v.get("en") or next(iter(v.values()), "")) if v else ""
    return v or ""


def licence_of(d):
    for dist in (d.get("distributions") or []):
        lic = dist.get("license")
        if isinstance(lic, dict):
            got = lic.get("label") or lic.get("id") or lic.get("resource")
            if got:
                return text(got)
        elif lic:
            return str(lic)
    lic = d.get("license")
    if isinstance(lic, dict):
        return text(lic.get("label") or lic.get("id") or "")
    return str(lic) if lic else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--open-only", action="store_true",
                    help="only rows whose licence string looks open")
    ap.add_argument("--limit", type=int, default=45)
    a = ap.parse_args()

    rows, seen = [], set()
    for term in TERMS:
        res = search(term)
        for d in (res.get("results") or []):
            if d.get("id") in seen:
                continue
            seen.add(d.get("id"))
            title = text(d.get("title"))
            lic = licence_of(d)
            rows.append({
                "title": title[:120],
                "country": (d.get("country") or {}).get("label"),
                "publisher": (d.get("publisher") or {}).get("name"),
                "catalog": (d.get("catalog") or {}).get("id"),
                "licence": lic[:100],
                "licence_looks_open": any(h in lic.lower() for h in OPEN_HINTS),
                "landing_page": text(d.get("landing_page")) if not isinstance(
                    d.get("landing_page"), list) else "",
                "id": d.get("id"),
                "matched_term": term,
            })
        time.sleep(0.3)

    if a.open_only:
        rows = [r for r in rows if r["licence_looks_open"]]
    rows.sort(key=lambda r: (not r["licence_looks_open"],
                             r["country"] or "", r["title"]))
    json.dump({"note": "data.europa.eu datasets matching the phrase each "
                       "country's administration uses for a remarkable-tree "
                       "register. A hit is a LEAD: the portal states that a "
                       "dataset exists and under what licence, never that it "
                       "is semantically filtered or that its coordinates are "
                       "usable. Licence verdicts are read at the primary "
                       "source before anything is imported.",
               "swept": "2026-08-16", "count": len(rows), "datasets": rows},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("%-13s %-42s %-8s %s" % ("country", "dataset", "open?", "licence"))
    for r in rows[:a.limit]:
        print("%-13s %-42s %-8s %s"
              % ((r["country"] or "?")[:13], (r["title"] or "")[:42],
                 "OPEN" if r["licence_looks_open"] else "-",
                 (r["licence"] or "(none stated)")[:34]))
    print("\n%d datasets, %d with an open-looking licence -> %s"
          % (len(rows), sum(1 for r in rows if r["licence_looks_open"]),
             os.path.relpath(OUT, ROOT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
