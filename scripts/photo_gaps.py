#!/usr/bin/env python3
"""Which city has no photograph at all, and what a session could approve today.

Hidde, 2026-08-17: "can we make part of the nightly runs that we aim to get at
least 1 photo per city". Yes, with one hard constraint that shapes the whole
design: **a night run cannot judge a photograph.** The CI runner's egress proxy
blocks upload.wikimedia.org, measured 2026-08-07 when 313 of 337 candidates were
unreachable and a whole window went on discovering it. And approving an image
without looking at it is forbidden outright (CLAUDE.md, the Cadiz standard).

So the goal splits in two, and this script is the seam:

    the night run   sweeps the free APIs, keeps the queue stocked, and runs
                    THIS to leave a ranked shortlist behind
    a session       opens the shortlist, looks at the pixels, approves or
                    rejects

Run it with no arguments for the city view, --shortlist for the work list.

    python3 scripts/photo_gaps.py
    python3 scripts/photo_gaps.py --shortlist        # what to view next
    python3 scripts/photo_gaps.py --shortlist --limit 30

WHAT IT FILTERS OUT, and why the filter exists at all. A geosearch queue is
mostly noise: sweeping Copenhagen returned one cemetery photograph attached to
five different trees, sweeping Brisbane returned Christmas trees, a frog and a
bamboo memorial, and Rotterdam's "Wilhelmina Linden" matched a PORTRAIT of a
woman named Van der Linden. Judged one by one that is a whole session for
nothing. So a candidate only reaches the shortlist when its filename actually
names the tree or its place, and obvious non-tree words disqualify it.

WHAT IT CANNOT DO, stated so nobody trusts it too far. A filename match is not
evidence the photograph is OF that tree. Copenhagen's pacifier tree scored
perfectly and was the wrong tree, in the wrong park, three kilometres away.
Alicante's best candidate had no geotag and Canalejas holds two Moreton Bay
figs 400 m apart, so it was held rather than attached. The shortlist decides
what is worth LOOKING at. Only a person looking decides what ships.
"""
import argparse
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Words that mean the file is not a photograph of our tree. Every one of these
# was found attached to a real candidate in the 2026-08-16 sweep.
NOT_A_TREE = ("christmas", "frog", "sign", "bordje", "affichette", "bamboo",
              "interior", "town hall", "panoramio-only", "detail", "leaf",
              "map", "plan", "portret", "portrait", "tomb", "grave",
              "logo", "coat of arms", "postcard", "railway", "locomotive",
              "coast line", "entrée du cimetière", "cemetery entrance")
# A dated archival file is a museum piece, not a reason to go this afternoon,
# and hard rule: no black-and-white or archival imagery. "Bourbong Street
# Bundaberg, circa 1890" reached the Hobart shortlist; "Atlantic Coast Line
# 1941" reached Chicago's. Both are the same shape.
ARCHIVAL = re.compile(r"\bcirca\s*1[89]|\b1[89]\d{2}\b", re.I)
# Words too generic to count as naming a tree.
GENERIC = {"tree", "trees", "the", "of", "great", "old", "giant", "ancient",
           "boom", "bomen", "arbre", "albero", "arbol", "baum", "drzewo"}


def cities():
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        doc = json.load(open(path, encoding="utf-8"))
        trees = doc.get("trees") or []
        if not trees:
            continue
        have = sum(1 for t in trees if (t.get("photo") or {}).get("url")
                   and (t.get("photo") or {}).get("status") != "held")
        out.append({"city": doc["city"], "slug": os.path.basename(path)[:-5],
                    "trees": len(trees), "photos": have})
    return out


def queue():
    try:
        doc = json.load(open(os.path.join(ROOT, "data", "photo-queue.json"),
                             encoding="utf-8"))
    except Exception:
        return {}
    trees = doc.get("trees") or {}
    return trees if isinstance(trees, dict) else {t.get("id"): t for t in trees}


def names_match(tree_name, species, title):
    """How strongly a filename names this tree. 0 means do not bother looking."""
    low = title.lower()
    if any(bad in low for bad in NOT_A_TREE) or ARCHIVAL.search(low):
        return 0
    words = {w for w in re.split(r"[^a-zà-ÿ]+", (tree_name or "").lower())
             if len(w) > 3 and w not in GENERIC}
    sp = {w for w in re.split(r"[^a-zà-ÿ]+", (species or "").lower()) if len(w) > 3}
    return 2 * len(words & set(re.split(r"[^a-zà-ÿ]+", low))) + \
        len(sp & set(re.split(r"[^a-zà-ÿ]+", low)))


# Hidde, 2026-08-17: "focus should be first get it to +5 trees than get photos".
# A city under this many trees is a TREE problem, not a photo problem, and a
# photograph on a three-tree page does not make it an afternoon out. So those
# cities are counted and named, and deliberately kept out of the viewing
# shortlist until they clear the floor.
PHOTO_FLOOR = 5


def shortlist(limit):
    q = queue()
    need = {c["slug"]: c for c in cities()
            if c["photos"] == 0 and c["trees"] >= PHOTO_FLOOR}
    rows = []
    for tid, entry in q.items():
        slug = (entry.get("city") or "").lower().replace(" ", "-")
        city = need.get(slug)
        if not city:
            continue
        best = None
        for cand in (entry.get("candidates") or []):
            title = str(cand.get("title") or cand.get("file") or "")
            s = names_match(entry.get("name"), cand.get("species"), title)
            if s and (best is None or s > best[0]):
                best = (s, title, cand.get("licence"))
        if best:
            rows.append((best[0], city["trees"], slug, tid,
                         entry.get("name", "?"), best[1], best[2]))
    # City need first (a city with no photo at all and many trees is the
    # biggest hole), then how well the filename names the tree.
    rows.sort(key=lambda r: (-r[1], -r[0]))
    seen, out = set(), []
    for r in rows:
        if r[2] in seen:      # one candidate per city: the goal is ONE photo
            continue
        seen.add(r[2])
        out.append(r)
    return out[:limit]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shortlist", action="store_true")
    ap.add_argument("--limit", type=int, default=20)
    a = ap.parse_args()

    all_cities = cities()
    none = [c for c in all_cities if c["photos"] == 0]
    print("%d of %d published cities have no photograph at all (%d trees)."
          % (len(none), len(all_cities), sum(c["trees"] for c in none)))

    thin = [c for c in none if c["trees"] < PHOTO_FLOOR]
    ready = [c for c in none if c["trees"] >= PHOTO_FLOOR]
    if not a.shortlist:
        print("\nReady for a photo (%d or more trees), biggest first:" % PHOTO_FLOOR)
        for c in sorted(ready, key=lambda c: -c["trees"])[:20]:
            print("  %3d trees  %-24s %s" % (c["trees"], c["city"], c["slug"]))
        if thin:
            print("\nTREES FIRST, not photos: %d city/cities under %d trees."
                  % (len(thin), PHOTO_FLOOR))
            print("  A photograph does not make a three-tree page an afternoon out.")
            for c in sorted(thin, key=lambda c: -c["trees"]):
                print("  %3d trees  %-24s %s" % (c["trees"], c["city"], c["slug"]))
        print("\n  python3 scripts/photo_gaps.py --shortlist   what to view next")
        return 0

    rows = shortlist(a.limit)
    print("\nVIEWING SHORTLIST, one candidate per photo-less city, biggest city first.")
    print("A SESSION does this: the CI runner cannot reach upload.wikimedia.org,")
    print("and no photograph ships without somebody looking at the pixels.\n")
    if not rows:
        print("  Nothing queued for any photo-less city. Run photo_hunt.py --recheck,")
        print("  or scripts/famous_trees.py --country <name>, which finds named trees")
        print("  that arrive WITH a photograph instead of hunting one for ours.")
        return 0
    print("  %-4s %-22s %-30s %s" % ("hit", "city", "tree", "candidate"))
    for score, trees, slug, tid, name, title, lic in rows:
        print("  [%d]  %-22s %-30s %s  %s"
              % (score, "%s (%d)" % (slug, trees), name[:30], title[:52], lic or ""))
    print("\n  For each: fetch it, run photo_light.py, LOOK at it, and check it is")
    print("  THIS tree and not another one in the same park. A geotag settles that")
    print("  when the file has one; without a geotag and with two similar trees")
    print("  nearby, the honest status is `held`, not `approved`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
