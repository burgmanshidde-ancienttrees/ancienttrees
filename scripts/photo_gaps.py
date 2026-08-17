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
# A famous NAME is not always a living tree, and two of the first six pairings
# this list produced were not trees at all: Chicago's "Old Treaty Elm
# Historical Marker" is a plaque where a famous elm used to stand, and Breda's
# "Sprookjesboom" is the talking animatronic in the Efteling's fairytale
# forest. Both carry photographs and coordinates and would have cost a verify
# pass to discover. A marker, a memorial or a stump is the record of a tree,
# not somewhere to send anybody.
NOT_A_LIVING_TREE = re.compile(
    r"historical marker|\bmarker\b|memorial to|monument to|\bplaque\b|"
    r"sprookjesboom|efteling|\bstump\b|\bstub\b|remains of", re.I)
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


def names_match(tree, cand):
    """How likely this file actually shows THIS tree. 0 means do not look.

    The weighting is taken from scripts/photo_shortlist.py, which a night run
    wrote independently the same morning this file was written; two tools for
    one job is the disease this project keeps catching, so that one was folded
    in here and deleted. Its insight is the part worth keeping: a picture
    hanging off the tree's own Wikidata item was attached by somebody who knew
    which tree they meant, and that is worth far more than any filename.
    """
    title = str(cand.get("title") or cand.get("file") or "").lower()
    if any(bad in title for bad in NOT_A_TREE) or ARCHIVAL.search(title):
        return 0
    cats = str(cand.get("cats") or "").lower()
    src = str(cand.get("source") or "").lower()
    words = lambda s: {w for w in re.split(r"[^a-zà-ÿ]+", (s or "").lower())
                       if len(w) >= 4} - GENERIC
    score = 0.0
    if "wikidata" in src:
        score += 60
    if "inat" in src:
        # Demoted from a bonus to a penalty on 2026-08-17, after looking.
        # iNaturalist is an IDENTIFICATION platform and its photographs are
        # identification photographs: the Montreal candidate that scored well
        # here is a hand holding a single oak leaf, and the Groningen one is
        # the same shape. Both pass the exposure check and both fail the Cadiz
        # standard outright, which bans close-ups of bark and leaves. A tree
        # page needs the tree. Kept in the list rather than excluded, because
        # an observation occasionally carries a whole-tree shot, but it should
        # never outrank a candidate that names the tree.
        score -= 20
    name_words = words(tree.get("name"))
    score += 25 * sum(1 for w in name_words if w in title)
    score += 8 * sum(1 for w in name_words if w in cats)
    score += 6 * sum(1 for w in words(tree.get("species")) if w in title)
    # A whole-scene photograph has the tree in it somewhere and is not of it.
    for bad in ("panorama", "aerial", "skyline", "statue", "church of",
                "monument to", "street", "square", "bridge", "night", "snow"):
        if bad in title:
            score -= 12
    if cand.get("lat") is not None:
        score += 4        # a geotag is what settles which trunk it is
    # A filename that is only a PLACE is a photograph of that place, and the
    # trees are scenery in it. "Giardini del Frontone.JPG" scored 62 on the
    # park's name and turned out to be statues, event chairs and a dog, with
    # the trees as background; "Assistens Kirkegard, Copenhagen.jpg" was one
    # cemetery view offered for five different trees. Neither is rescuable by
    # weighting, because the photograph a tree page needs was never taken.
    # So a candidate must carry at least one signal that a PLANT is the
    # subject: a species word, or a word for tree in some language.
    plant = set(GENERIC) | {"oak", "beech", "fig", "plane", "cedar", "yew",
                            "lime", "linden", "elm", "pine", "cypress", "olive",
                            "chestnut", "maple", "birch", "willow", "poplar",
                            "ginkgo", "mulberry", "palm", "eucalyptus", "ficus",
                            "quercus", "platanus", "fagus", "tilia", "pinus",
                            "eik", "buche", "chene", "tiglio", "quercia",
                            "medis", "drzewo", "strom", "traeet"}
    # In the TITLE, not the categories. Commons files land in categories like
    # "Trees in Perugia" almost regardless of subject, so testing cats let a
    # Raphael painting score 4 and an equestrian bronze score 58. The title is
    # what the uploader chose to call the thing.
    if not any(w in title for w in plant):
        return 0
    return max(score, 0)


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
            s = names_match(entry, cand)
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



def famous_near(limit, photo_only=False, per_city=3):
    """Famous trees WITH a photograph, near a city we already publish.

    Proved on 2026-08-17 rather than assumed. Copenhagen has 13 trees and no
    photograph, and no photograph of ITS trees exists to find: a viewing pass
    rejected six candidates across two sessions and the pattern was never
    picture quality, it was that nobody photographed those trunks. Meanwhile
    Klopstocks Eg sits 12 km outside Copenhagen with three Commons photographs,
    and the first one opened is a textbook Cadiz image: an ancient oak filling
    the frame, trunk and crown readable, a bench for scale, CC BY-SA 4.0.

    So reverse the problem. Do not hunt a picture for a tree nobody
    photographed; add a tree that arrives with its own, and which people have
    heard of.

    THE SIZE OF THE PRIZE, measured 2026-08-17 so nobody has to guess: the
    leads files hold 995 famous trees, 702 of them with coordinates, and only
    **68 sit within 30 km of a city we publish**. Bulk-adding "all of them" is
    therefore not a thing that exists: 927 belong to villages, forests and
    countryside, which is the wider-database ambition rather than the city
    pages. The 68 are one finite batch.

    Not photo-less cities only. A famous tree is worth adding to any city
    (it is a tree people recognise), so the default lists every city and
    marks which ones have no photograph yet. --photo-only narrows it.

    It is a RESEARCH list and never an import. Each still needs a verify pass
    to our bar: alive, two independent sources, a location we can state
    honestly, publicly reachable, one place to stand. The famous-trees name
    matching is deliberately loose and has produced nonsense: Hobart's dawn
    redwoods matched a 1920 street scene in Bundaberg.
    """
    from geo import km
    pool = [c for c in cities()
            if not photo_only or (c["photos"] == 0 and c["trees"] >= PHOTO_FLOOR)]
    centres = {}
    for c in pool:
        doc = json.load(open(os.path.join(ROOT, "data", "cities", c["slug"] + ".json"),
                             encoding="utf-8"))
        pts = [(t["location"]["latitude"], t["location"]["longitude"])
               for t in doc["trees"] if (t.get("location") or {}).get("latitude") is not None]
        if pts:
            centres[c["slug"]] = (sum(p[0] for p in pts) / len(pts),
                                  sum(p[1] for p in pts) / len(pts), c)
    # Nearest city per tree, not every city within range, so one tree is not
    # offered to three cities at once.
    rows = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "leads", "_famous-*.json"))):
        try:
            doc = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        country = os.path.basename(path)[len("_famous-"):-len(".json")]
        for lead in (doc.get("leads") or []):
            if lead.get("lat") is None or not lead.get("photos"):
                continue
            if NOT_A_LIVING_TREE.search(lead.get("name") or ""):
                continue
            best = None
            for slug, (la, lo, c) in centres.items():
                d = km((la, lo), (lead["lat"], lead["lng"]))
                if best is None or d < best[0]:
                    best = (d, slug, c)
            if best and best[0] <= 30:
                rows.append({"km": round(best[0], 1), "slug": best[1],
                             "trees": best[2]["trees"], "photos": best[2]["photos"],
                             "name": lead["name"], "country": country,
                             "n_photos": len(lead["photos"]),
                             "first_photo": lead["photos"][0],
                             "lat": lead["lat"], "lng": lead["lng"]})
    # Commons lists the same tree under more than one category, so the same
    # lead arrives twice: Zurich was offered "Messikomer Eich" twice at an
    # identical coordinate. Fold on name plus position.
    seen_tree, unique = set(), []
    for r in rows:
        key = (r["name"].lower(), round(r["lat"], 4), round(r["lng"], 4))
        if key in seen_tree:
            continue
        seen_tree.add(key)
        unique.append(r)
    rows = unique

    # Group by city so a verify pass can be briefed on a whole cluster at once,
    # which is the point: three trees at one city is a pass, one tree is not.
    by = {}
    for r in rows:
        by.setdefault(r["slug"], []).append(r)
    for v in by.values():
        v.sort(key=lambda r: r["km"])
    # Cities with no photograph first, then the biggest clusters.
    order = sorted(by.items(), key=lambda kv: (kv[1][0]["photos"] > 0, -len(kv[1])))
    out = []
    for slug, group in order[:limit]:
        out.append((slug, group[:per_city]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shortlist", action="store_true")
    ap.add_argument("--famous", action="store_true")
    ap.add_argument("--photo-only", action="store_true", dest="photo_only")
    ap.add_argument("--per-city", type=int, default=3, dest="per_city")
    ap.add_argument("--limit", type=int, default=20)
    a = ap.parse_args()

    if a.famous:
        groups = famous_near(a.limit, photo_only=a.photo_only, per_city=a.per_city)
        print("FAMOUS TREES THAT BRING THEIR OWN PHOTOGRAPH, near a city we publish.")
        print("Grouped by city, because three trees at one place is a verify pass")
        print("and one tree is not. A RESEARCH list: each still needs the bar")
        print("(alive, two sources, honest location, publicly reachable).\n")
        if not groups:
            print("  Nothing within 30 km of a city we publish.")
            return 0
        total = 0
        for slug, rows in groups:
            head = rows[0]
            flag = "  NO PHOTOGRAPH YET" if head["photos"] == 0 else ""
            print("  %s (%d trees, %d photos)%s"
                  % (slug, head["trees"], head["photos"], flag))
            for r in rows:
                total += 1
                print("      %5.1f km  %-38s %d photo(s)  %.4f,%.4f"
                      % (r["km"], r["name"][:38], r["n_photos"], r["lat"], r["lng"]))
                print("               %s" % r["first_photo"])
        print("\n  %d tree(s) across %d city/cities." % (total, len(groups)))
        print("  Brief a verify pass on ONE city's group at a time; the whole")
        print("  reachable pool is 68 trees, so this is a batch, not a campaign.")
        return 0

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
        print("  [%3.0f] %-22s %-30s %s  %s"
              % (score, "%s (%d)" % (slug, trees), name[:30], title[:52], lic or ""))
    print("\n  For each: fetch it, run photo_light.py, LOOK at it, and check it is")
    print("  THIS tree and not another one in the same park. A geotag settles that")
    print("  when the file has one; without a geotag and with two similar trees")
    print("  nearby, the honest status is `held`, not `approved`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
