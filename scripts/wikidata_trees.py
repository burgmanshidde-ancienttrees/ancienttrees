#!/usr/bin/env python3
"""Wikidata's own layer of remarkable trees, measured per city.

Why this exists. Two register scouting passes (the English-speaking block on
2026-08-13, the German Bundeslaender the same day) went looking for
government-published, semantically-filtered tree registers and mostly did not
find them: 78,000 tokens bought one import in the first, five cities of
fourteen in the second. The lesson recorded there was that such registers are
rarer as clean open-data endpoints than the briefs assumed. This script asks a
different question, and asks it for nothing: where has somebody ALREADY done
that work, tree by tree, in a place we can query in one request.

Wikidata models an individual remarkable tree as an instance of Q811534 (or a
subclass: heritage tree, natural monument tree). That is a semantic filter in
the sense hard rule "never bulk import" wants, not a street-tree inventory: an
item exists because a person thought that particular tree worth an item. Every
item carries coordinates, most carry a species, many carry a national
protection designation and a source. Wikidata's own data is CC0.

What this is NOT. It is scouting gear, not a register import: nothing here
ships to the site. A Wikidata item is one source, the same standing as a
government register entry under the layer-2 rule, and layer 1 still wants its
second independent source, its vitality check and its pin. What it buys is the
expensive half of a research pass, which is knowing WHICH trees to look at.

Usage:
    python3 scripts/wikidata_trees.py --fetch     refresh the local copy
    python3 scripts/wikidata_trees.py             per-city supply, queue order
    python3 scripts/wikidata_trees.py --country Austria
"""
import argparse
import json
import math
import os
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

OUT = os.path.join(ROOT, "data", "research", "wikidata-remarkable-trees.json")
QUEUE = os.path.join(ROOT, "data", "city-queue.json")
ENDPOINT = "https://query.wikidata.org/sparql"
UA = "AncientTrees/1.0 (https://ancienttrees.app; burgmans.hidde@gmail.com)"

# P31/P279* Q811534 is the whole point: "remarkable tree" and everything
# subclassed under it (heritage tree, natural monument tree), which is what
# makes this a designation query rather than a tree-inventory query.
# P10241 is the species link on an individual organism, NOT P225 (which lives
# on the taxon item itself); the first version of this script asked for P225
# and got a species column of zeros. P569 on a tree is its planting or
# germination year, which is the one field registers almost never carry. P18
# is a Commons file, so a hit here is a photo candidate with a licence already
# attached. P1435 is the national protection designation, which is what makes
# an entry a designation rather than an opinion.
QUERY = """
SELECT ?t ?tLabel ?p ?cLabel ?taxonLabel ?adminLabel ?planted ?image ?desigLabel
WHERE {
  ?t wdt:P31/wdt:P279* wd:Q811534 ; wdt:P625 ?p ; wdt:P17 ?c .
  OPTIONAL { ?t wdt:P10241 ?taxon }
  OPTIONAL { ?t wdt:P131 ?admin }
  OPTIONAL { ?t wdt:P569 ?planted }
  OPTIONAL { ?t wdt:P18 ?image }
  OPTIONAL { ?t wdt:P1435 ?desig }
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en,de,fr,it,es,nl,cs,lt,et,pt,ko,bg" }
}
"""


def fetch():
    """One request, roughly 20,000 trees. Hard timeout per the fetch rule."""
    url = ENDPOINT + "?" + urllib.parse.urlencode({"query": QUERY})
    req = urllib.request.Request(url, headers={
        "Accept": "application/sparql-results+json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        raw = json.load(r)
    # An OPTIONAL that matches twice (two designations, two admin areas) returns
    # the tree once per combination, so the raw rows over-count. Fold on qid and
    # keep the first non-empty value of each field.
    by_qid = {}
    for b in raw["results"]["bindings"]:
        t = parse_row(b)
        if not t:
            continue
        seen = by_qid.setdefault(t["qid"], t)
        for k, v in t.items():
            if v and not seen.get(k):
                seen[k] = v
    return list(by_qid.values())


def parse_row(b):
    point = b.get("p", {}).get("value", "")
    # Point(lon lat), and the order is longitude first, which is the reverse of
    # every other coordinate in this repo and has bitten register imports before.
    if not point.startswith("Point("):
        return None
    try:
        lon, lat = (float(v) for v in point[6:-1].split())
    except ValueError:
        return None
    qid = b.get("t", {}).get("value", "").rsplit("/", 1)[-1]
    label = b.get("tLabel", {}).get("value") or ""
    planted = b.get("planted", {}).get("value") or ""
    image = b.get("image", {}).get("value")
    return {
        "qid": qid,
        # A label that is just the Q-number means the item has no name in any
        # language we asked for; keep it, it is still a located tree.
        "name": None if label == qid else label,
        "latitude": round(lat, 6),
        "longitude": round(lon, 6),
        "country": b.get("cLabel", {}).get("value"),
        "species": b.get("taxonLabel", {}).get("value"),
        "admin": b.get("adminLabel", {}).get("value"),
        # A year, and only ever a year. The SPARQL endpoint normalises a bare
        # year to a full dateTime (1809-01-01T00:00:00Z), so the day and month
        # here are an artefact of the serialisation and never a fact; reading
        # this as a date would invent a precision the source does not have.
        "planted_year": planted[:4] if planted[:4].isdigit() else None,
        "commons_image": image,
        "designation": b.get("desigLabel", {}).get("value"),
        "source": "https://www.wikidata.org/wiki/" + qid,
    }


def save(trees):
    doc = {
        "source": "Wikidata SPARQL, instances of Q811534 (remarkable tree) and "
                  "its subclasses that carry coordinates",
        "licence": "CC0 1.0. Wikidata's own data is released into the public "
                   "domain (https://www.wikidata.org/wiki/Wikidata:Licensing). "
                   "This file is scouting gear, not an import: promoting it to "
                   "data/registers/ needs the licence sentence read at the "
                   "primary source and written into OPEN_DATA_SURVEY.md first.",
        "caveat": "One source per tree, crowd-maintained, no vitality field. "
                  "Every entry is a lead to verify, never a publishable fact. "
                  "Coordinates vary from surveyed to guessed at the village.",
        "count": len(trees),
        "trees": sorted(trees, key=lambda t: (t["country"] or "", t["qid"])),
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    return doc


def load():
    with open(OUT, encoding="utf-8") as fh:
        return json.load(fh)


def registers():
    """The register files this project already holds, for the imported column."""
    import glob
    out = []
    for p in glob.glob(os.path.join(ROOT, "data", "registers", "*.json")):
        try:
            with open(p, encoding="utf-8") as fh:
                d = json.load(fh)
            if isinstance(d, dict):
                out.append(d)
        except (OSError, ValueError):
            continue
    return out


def near(trees, lat, lng, km):
    dlat = km / 111.0
    dlng = km / (111.0 * max(math.cos(math.radians(lat)), 0.1))
    return [t for t in trees
            if abs(t["latitude"] - lat) < dlat and abs(t["longitude"] - lng) < dlng]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="refresh from Wikidata")
    ap.add_argument("--country", help="list what is known for one country")
    ap.add_argument("--designations", action="store_true",
                    help="the legal protection scheme behind each country's "
                         "trees: the search term that finds its register")
    ap.add_argument("--km", type=float, default=15.0,
                    help="radius per city (default 15, a day-trip band)")
    ap.add_argument("--limit", type=int, default=40)
    a = ap.parse_args()

    if a.fetch:
        trees = fetch()
        doc = save(trees)
        print("%d remarkable trees with coordinates -> %s"
              % (doc["count"], os.path.relpath(OUT, ROOT)))
        return 0

    try:
        doc = load()
    except OSError:
        print("no local copy yet, run: python3 scripts/wikidata_trees.py --fetch")
        return 1
    trees = doc["trees"]

    if a.designations:
        # Estonia was found this way and it is the cheapest scouting move in
        # the project. Wikidata records WHICH legal designation protects each
        # tree, and searching a government for the term its own law uses beats
        # searching it for "tree register": "kaitstav looduse uksikobjekt"
        # lands on the EELIS WFS in one search, "Estonia tree register" does
        # not. Run this before scouting any country.
        by = {}
        for t in trees:
            if not t.get("designation") or t["designation"].startswith("Q"):
                continue
            by.setdefault((t["country"], t["designation"]), 0)
            by[(t["country"], t["designation"])] += 1
        # Deliberately NOT a per-designation "imported" flag. Country is the
        # only key both sides share, and in a federal country that answers the
        # wrong question: we hold Bayern and Berlin, so Germany reads as
        # covered while Saxony, Hesse, Thuringia and Brandenburg (2,464 trees
        # between them) are exactly the gap. The column says how much of the
        # country we hold, and a scheme in a partly-covered country still has
        # to be checked by hand.
        have = {}
        for r in registers():
            # A few register files carry a dict or list in "source" rather than
            # a string, so only the country key is read here.
            have.setdefault(r.get("country"), []).append(1)
        print("The legal scheme protecting each country's trees: the term to "
              "search a\ngovernment for. Estonia was found this way. The last "
              "column counts register\nfiles we hold for that COUNTRY, which "
              "in a federal state says nothing about\nthe particular Land or "
              "region a scheme belongs to.\n")
        print("%6s  %-18s %-46s %s" % ("trees", "country", "designation", "our files"))
        for (country, desig), n in sorted(by.items(), key=lambda kv: -kv[1])[:a.limit]:
            files = have.get(country)
            print("%6d  %-18s %-46s %s"
                  % (n, (country or "")[:18], desig[:46],
                     ("%d" % len(files)) if files else "none"))
        return 0

    if a.country:
        rows = [t for t in trees if (t["country"] or "").lower() == a.country.lower()]
        print("%d trees in %s" % (len(rows), a.country))
        for t in rows[:a.limit]:
            print("  %-38s %-28s %s" % ((t["name"] or t["qid"])[:38],
                                        (t["species"] or "")[:28], t["admin"] or ""))
        return 0

    import city_queue as Q
    queue = json.load(open(QUEUE, encoding="utf-8"))["cities"]
    todo = [c for c in queue if (c.get("rank") or 9999) <= 250
            and c.get("trees", 0) < 10]
    print("Wikidata remarkable trees within %g km, cities below 10 trees, "
          "queue order.\n" % a.km)
    print("  #  city                 trees  register  wikidata  named  species")
    total = 0
    for c in sorted(todo, key=lambda c: c["rank"]):
        pos = Q.city_coords(c["city"], c.get("article"))
        if not pos:
            continue
        found = near(trees, pos[0], pos[1], a.km)
        if not found:
            continue
        named = sum(1 for t in found if t["name"])
        spec = sum(1 for t in found if t["species"])
        total += len(found)
        print("%3d  %-20s %5d %9d %9d %6d %8d"
              % (c["rank"], c["city"][:20], c.get("trees", 0),
                 c.get("register", 0), len(found), named, spec))
    print("\n%d trees reachable from cities still short of 10." % total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
