#!/usr/bin/env python3
"""How famous is each tree we publish, measured rather than felt.

Hidde, 2026-09-11: "Moeten we een famous tree collectie maken?" Yes, and the
question that decides whether such a page is any good is what it ranks ON.
Fame as a feeling ranks the trees whoever writes the list has heard of. This
ranks by what somebody else already did: how many language Wikipedias bothered
to write the tree up, and how often those articles are read.

The chain already exists for LEADS in famous_demand.py (Commons category ->
Wikidata -> sitelinks -> pageviews) and its answers sit in
data/famous-demand.json. What was missing is the join to the trees we actually
publish, because a collection can only point at published trees. This does that
join, and it does it BY DISTANCE, never by name: CLAUDE.md's own rule, learned
when register place names were matched against our city names and three passes
were briefed on cities that had been live for weeks. A lead 40 metres from one
of our pins is our tree under somebody else's spelling; a lead with the same
name 300 km away is a different tree.

    python3 scripts/fame.py              # the ranking, nothing written
    python3 scripts/fame.py --apply      # write `fame` onto the trees
    python3 scripts/fame.py --gaps       # trees that ought to have a number

TO FILL THE NUMBERS, where there is network (this needs Wikidata and the
pageviews API, which a sandbox often blocks):

    python3 scripts/famous_demand.py --resolve
    python3 scripts/famous_demand.py --count
    python3 scripts/fame.py --apply

429 of the 938 cached leads are unresolved as of the day this was written, and
they include General Sherman, so running those two lines is what puts the most
famous tree in America onto the page. Nothing here guesses in the meantime: a
tree with no number simply does not appear in the ranking.
"""
import argparse
import datetime
import glob
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "famous-demand.json")
LEADS = os.path.join(ROOT, "data", "leads")
CITIES = os.path.join(ROOT, "data", "cities")

# A lead this close to one of our pins is the same tree. 150 metres is the
# number famous_map.py already uses for the same question, and it has to be
# loose: a lead's coordinate comes from a Commons category or a Wikidata item
# and ours from a register or an aerial check, so two honest fixes on one trunk
# can sit a hundred metres apart. Anything looser starts swallowing the
# neighbour, which is the failure the Copenhagen pacifier tree recorded.
MATCH_M = 150


def haversine_m(a, b):
    r = 6371000.0
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * r * math.asin(math.sqrt(h))


def renderable(tree):
    loc = tree.get("location") or {}
    return bool(tree.get("story")) and loc.get("latitude") is not None


def published_trees():
    """(slug, city, tree dict) for every tree that has a page."""
    out = []
    for path in sorted(glob.glob(os.path.join(CITIES, "*.json"))):
        doc = json.load(open(path, encoding="utf-8"))
        for tree in doc.get("trees", []):
            if renderable(tree):
                out.append((os.path.basename(path)[:-5], doc["city"], tree))
    return out


def famous_leads(cache):
    """Every famous-tree lead that carries both a position and a fame number."""
    out = []
    for path in sorted(glob.glob(os.path.join(LEADS, "_famous-*.json"))):
        for row in json.load(open(path, encoding="utf-8")).get("leads", []):
            entry = cache.get(row.get("name"))
            if not entry or not entry.get("wikis"):
                continue
            if row.get("lat") is None or row.get("lng") is None:
                continue
            out.append({
                "name": row["name"],
                "lat": row["lat"],
                "lng": row["lng"],
                "qid": entry.get("qid"),
                "langs": len(entry["wikis"]),
                "views": entry.get("views"),
            })
    return out


def match(trees, leads):
    """Best lead per published tree, nearest first, most-written-up wins ties."""
    best = {}
    for lead in leads:
        hit = None
        for slug, city, tree in trees:
            loc = tree["location"]
            d = haversine_m((lead["lat"], lead["lng"]),
                            (loc["latitude"], loc["longitude"]))
            if d <= MATCH_M and (hit is None or d < hit[0]):
                hit = (d, slug, city, tree)
        if not hit:
            continue
        key = (hit[1], hit[3]["id"])
        prev = best.get(key)
        if prev is None or lead["langs"] > prev["lead"]["langs"]:
            best[key] = {"slug": hit[1], "city": hit[2], "tree": hit[3],
                         "lead": lead, "metres": round(hit[0])}
    return best


def apply(best):
    """Write the fame block onto each matched tree, provenance included.

    Provenance rather than a bare score, per goal 3 (DECISIONS.md 2026-08-14):
    the qid is what lets the next run check the number instead of trusting it,
    and `source_name` is what lets somebody see that the lead behind it is the
    tree they think it is.
    """
    today = datetime.date.today().isoformat()
    written = 0
    for path in sorted(glob.glob(os.path.join(CITIES, "*.json"))):
        slug = os.path.basename(path)[:-5]
        doc = json.load(open(path, encoding="utf-8"))
        touched = False
        for tree in doc.get("trees", []):
            row = best.get((slug, tree.get("id")))
            if not row:
                continue
            fame = {"langs": row["lead"]["langs"], "checked": today,
                    "source_name": row["lead"]["name"]}
            if row["lead"]["qid"]:
                fame["qid"] = row["lead"]["qid"]
            if row["lead"]["views"] is not None:
                fame["views"] = row["lead"]["views"]
            if tree.get("fame") != fame:
                tree["fame"] = fame
                touched = True
                written += 1
        if touched:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(doc, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="write the fame block onto data/cities")
    ap.add_argument("--gaps", action="store_true",
                    help="cached leads whose fame is unresolved")
    args = ap.parse_args()

    cache = json.load(open(CACHE, encoding="utf-8"))
    trees = published_trees()
    leads = famous_leads(cache)
    best = match(trees, leads)

    if args.gaps:
        unresolved = [n for n, e in cache.items() if not e.get("wikis")]
        print("%d of %d cached leads have no fame number yet."
              % (len(unresolved), len(cache)))
        print("Run famous_demand.py --resolve then --count where there is "
              "network, then fame.py --apply.")
        for name in sorted(unresolved)[:20]:
            print("  " + name)
        return 0

    ranked = sorted(best.values(),
                    key=lambda r: (-r["lead"]["langs"], -(r["lead"]["views"] or 0)))
    print("%d of %d published trees carry a fame number (%d cached leads "
          "still unresolved)"
          % (len(ranked), len(trees),
             sum(1 for e in cache.values() if not e.get("wikis"))))
    for row in ranked[:30]:
        print("%3d langs %8s views  %-44s %s"
              % (row["lead"]["langs"], row["lead"]["views"] or "-",
                 row["tree"]["name"][:44], row["city"]))

    if args.apply:
        print("wrote fame onto %d tree(s)" % apply(best), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
