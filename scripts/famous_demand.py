#!/usr/bin/env python3
"""Which famous trees do people actually look up? Rank the leads by demand.

Hidde, 2026-09-03: "die famous bomen komen gelijk in de lijst van oudste
bomen... misschien wel bomen die mensen daadwerkelijk zelf googelen." He is
right that a named tree is a search term in a way a city page never is, and
wrong to assume the list is uniformly good: data/leads/_famous-*.json holds
987 leads and they run from the Major Oak, which has an article in nineteen
languages, to an apple tree in Bosaca that has none anywhere.

So this measures rather than guesses, the same way demand.py does for cities.
The chain is Commons category -> Wikidata item -> the Wikipedias that wrote
about it -> what those articles are read. Two numbers come out and they say
different things:

    langs   how many language Wikipedias bothered. Fame, and it is the
            sturdier of the two: a tree with articles in nine languages is
            famous whatever this month's traffic did.
    views   monthly reads of those articles, summed. Demand, and it is the
            number that says somebody typed the name into something.

Neither is search volume for OUR page, and nothing here pretends otherwise.
What they are good for is ORDER: a tree read ten thousand times a month is
worth a verify pass before one read nine times, and both beat one nobody has
ever written a sentence about.

Read the ranking with CLAUDE.md's distribution rule in hand, because the top
of this list is the contested end. Everybody has written about the Major Oak.
The sweet spot is the same as it is for cities: real demand, thin competition,
which here means a tree with several language articles and no English one.
`--gap` prints exactly those.

    python3 scripts/famous_demand.py --resolve     # fill the cache (network)
    python3 scripts/famous_demand.py               # the ranking
    python3 scripts/famous_demand.py --gap         # read elsewhere, unwritten in English
    python3 scripts/famous_demand.py --country japan
"""
import argparse
import collections
import datetime
import glob
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEADS = os.path.join(ROOT, "data", "leads")
CACHE = os.path.join(ROOT, "data", "famous-demand.json")
UA = {"User-Agent": "AncientTrees/1.0 (ancienttrees.app; tree research)"}
# Wikidata takes fifty titles a call, so the whole list of leads costs about
# twenty requests. Pageviews are one call per article and there is no batch
# endpoint, which is what the pause is for.
BATCH = 50
PAUSE = 0.6


def fetch(url, tries=4):
    """One GET, backing off on the 429 the pageviews API hands out freely.

    Measured 2026-09-03: a burst of unauthenticated pageviews calls starts
    refusing after a few dozen, and the refusal is indistinguishable from an
    article that has no data unless you catch it. That is how the first run of
    this script reported the Major Oak as read by nobody.
    """
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise
            if exc.code != 429 or attempt == tries - 1:
                raise
            time.sleep(2 ** attempt)
        except Exception:
            if attempt == tries - 1:
                raise
            time.sleep(1 + attempt)
    raise RuntimeError("unreachable")


def leads():
    """Every famous-tree lead, with the country its file names."""
    out = []
    for path in sorted(glob.glob(os.path.join(LEADS, "_famous-*.json"))):
        country = os.path.basename(path)[len("_famous-"):-len(".json")]
        doc = json.load(open(path, encoding="utf-8"))
        for row in doc.get("leads", []):
            row = dict(row)
            row["country"] = country
            out.append(row)
    return out


def resolve(rows, cache, limit=None):
    """Commons category -> Wikidata sitelinks, in batches of fifty."""
    todo = [r for r in rows if r["name"] not in cache]
    if limit:
        todo = todo[:limit]
    print("%d lead(s) to resolve" % len(todo), file=sys.stderr)
    for i in range(0, len(todo), BATCH):
        chunk = todo[i:i + BATCH]
        titles = "|".join("Category:" + r["name"] for r in chunk)
        url = ("https://www.wikidata.org/w/api.php?action=wbgetentities"
               "&format=json&sites=commonswiki&props=sitelinks&titles="
               + urllib.parse.quote(titles, safe="|"))
        try:
            data = fetch(url)
        except Exception as exc:                      # noqa: BLE001
            print("  batch failed (%s), skipping" % exc, file=sys.stderr)
            continue
        # Map back by the entity's OWN commons sitelink, never by position:
        # the answer is a dict, unfound titles collapse into a single "-1"
        # key, and there is no _index to pair on. Asking the item which
        # category it belongs to cannot drift.
        ents = data.get("entities", {})
        for key, ent in ents.items():
            if key.startswith("-"):
                continue
            sl = ent.get("sitelinks", {})
            cat = (sl.get("commonswiki") or {}).get("title", "")
            if not cat.startswith("Category:"):
                continue
            name = cat[len("Category:"):]
            wikis = {s: v["title"] for s, v in sl.items()
                     if s.endswith("wiki") and s not in
                     ("commonswiki", "specieswiki", "sourceswiki")}
            cache[name] = {"qid": key, "wikis": wikis}
        for row in chunk:
            cache.setdefault(row["name"], {"qid": None, "wikis": {}})
        print("  resolved %d/%d" % (min(i + BATCH, len(todo)), len(todo)),
              file=sys.stderr)
        save(cache)
        time.sleep(PAUSE)
    return cache


def views_for(project, title, months=12):
    """Monthly reads of one article, averaged over the last full months."""
    end = datetime.date.today().replace(day=1)
    start = end - datetime.timedelta(days=31 * months)
    start = start.replace(day=1)
    url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
           "%s/all-access/user/%s/monthly/%s/%s"
           % (project.replace("wiki", ".wikipedia"),
              urllib.parse.quote(title.replace(" ", "_"), safe=""),
              start.strftime("%Y%m%d"), end.strftime("%Y%m%d")))
    try:
        data = fetch(url)
    except Exception:                                 # noqa: BLE001
        return None
    items = data.get("items", [])
    if not items:
        return None
    return round(sum(i["views"] for i in items) / len(items))


def count_views(cache, limit=None):
    """Fill monthly reads for every resolved lead that has an article."""
    todo = [(n, e) for n, e in cache.items()
            if e.get("wikis") and "views" not in e]
    if limit:
        todo = todo[:limit]
    print("%d lead(s) to count" % len(todo), file=sys.stderr)
    for done, (name, entry) in enumerate(todo, 1):
        per = {}
        # Big wikis first and stop at five: the tail adds reads in the tens
        # while costing a request each, and the ranking never turns on it.
        wikis = sorted(entry["wikis"], key=lambda w: w != "enwiki")[:2]
        for wiki in wikis:
            v = views_for(wiki, entry["wikis"][wiki])
            if v:
                per[wiki] = v
            time.sleep(PAUSE)
        if not per and entry["wikis"]:
            # Every article refused or missing: leave it uncounted rather than
            # writing a zero, because a zero here reads as "nobody looks at
            # this tree" and would sink a famous one for good.
            continue
        entry["views"] = sum(per.values())
        entry["views_by_wiki"] = per
        if done % 10 == 0:
            print("  counted %d/%d" % (done, len(todo)), file=sys.stderr)
            save(cache)
    save(cache)
    return cache


def published_places():
    """Every place we publish, as a centre point and a tree count."""
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        doc = json.load(open(path, encoding="utf-8"))
        pts = [(t["location"]["latitude"], t["location"]["longitude"])
               for t in doc.get("trees", [])
               if (t.get("location") or {}).get("latitude") is not None]
        if pts:
            out.append((doc["city"],
                        sum(p[0] for p in pts) / len(pts),
                        sum(p[1] for p in pts) / len(pts),
                        len(doc.get("trees", []))))
    return out


def km(lat1, lon1, lat2, lon2):
    R, p = 6371.0, math.pi / 180
    return 2 * R * math.asin(math.sqrt(
        math.sin((lat2 - lat1) * p / 2) ** 2
        + math.cos(lat1 * p) * math.cos(lat2 * p)
        * math.sin((lon2 - lon1) * p / 2) ** 2))


# Same fix as scripts/famous_map.py's SAME_TREE_M, applied here too: a famous
# tree already published under a different id still carries status "lead" in
# its own leads file (nobody flips it, because the write pass edits a city
# file and a leads file in one sitting and this specific field is easy to
# miss), so --next kept re-surfacing already-shipped trees as candidates.
# Measured 2026-09-03: an entire 12-candidate Japan batch turned out to be 5
# duplicates (kag_010, tok_016, nag_001, yos_001, hok_001), three verify
# passes burning tokens to rediscover what was already live.
SAME_TREE_M = 0.06  # km, i.e. 60 metres


def already_published_trees():
    """Every live tree as (lat, lng), for the same-tree de-dup."""
    out = []
    for path in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        doc = json.load(open(path, encoding="utf-8"))
        for t in doc.get("trees", []):
            loc = t.get("location") or {}
            if loc.get("latitude") is not None:
                out.append((loc["latitude"], loc["longitude"]))
    return out


def drop_already_published(rows, live_trees):
    """Leads within 60m of a tree we already publish: not candidates."""
    keep = []
    for r in rows:
        if r.get("lat") is None:
            keep.append(r)
            continue
        if any(km(r["lat"], r["lng"], t[0], t[1]) <= SAME_TREE_M
               for t in live_trees):
            continue
        keep.append(r)
    return keep


# The day-trip boundary of CLAUDE.md, in kilometres. Inside it a famous tree
# joins the place that already exists; outside it the tree IS the place, under
# the single-famous-tree exception of 2026-08-31.
DAYTRIP_KM = 30


def container(row, places):
    """Which place does this tree land on, and is that place new."""
    if row.get("lat") is None:
        return (None, None)
    near = min((km(row["lat"], row["lng"], p[1], p[2]), p[0]) for p in places)
    if near[0] <= DAYTRIP_KM:
        return (near[1], round(near[0], 1))
    return (None, round(near[0], 1))


def save(cache):
    tmp = CACHE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(cache, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    os.replace(tmp, CACHE)


def load():
    if os.path.exists(CACHE):
        return json.load(open(CACHE, encoding="utf-8"))
    return {}


def print_next(scored, rows_by_name, places, count):
    """The batch a night run should take, in the shape a brief needs.

    Grouped by country because a verify pass shares its sources across one,
    and never under six candidates, which is CLAUDE.md's floor: the fixed cost
    of a pass makes a small one expensive by definition.
    """
    by_country = collections.defaultdict(list)
    for s in scored:
        by_country[s["country"]].append(s)
    ranked = sorted(by_country.items(),
                    key=lambda kv: -sum(x["views"] for x in kv[1]))
    shown = 0
    for country, group in ranked:
        group = [g for g in group if g["pin"]][:12]
        if len(group) < 6:
            continue
        print("## %s   %d candidate(s), %d reads a month between them"
              % (country.replace("-", " ").title(), len(group),
                 sum(g["views"] for g in group)))
        print("   Dispatch: verify agent, BRIEF_RESEARCH.md. Claim first: "
              "python3 scripts/passcheck.py --claim <place> --kind verify")
        print("   A candidate marked 'its own place' has to pass the "
              "destination test first (CLAUDE.md, 2026-08-31): would somebody "
              "travel specifically for THIS ONE TREE. Being a good tree is "
              "not the test. One that fails it stays a lead.")
        for g in group:
            row = rows_by_name[g["name"]]
            place, dist = container(row, places)
            where = ("joins %s, %s km" % (place, dist) if place
                     else "its own place, nearest is %s km away" % dist)
            print("    %-38.38s %5d/mo %2d langs | %-26.26s | %.5f,%.5f | %s"
                  % (g["name"], g["views"], g["langs"],
                     (g["species"] or "?"), row["lat"], row["lng"], where))
            for u in (row.get("photos") or [])[:3]:
                print("        %s" % u)
        print()
        shown += 1
        if shown >= count:
            break
    if not shown:
        print("No country holds six pinned candidates. Widen with --top or "
              "pin the leads that carry none (296 of them).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resolve", action="store_true",
                    help="ask Wikidata and the pageviews API (network)")
    ap.add_argument("--limit", type=int, help="stop after N lookups")
    ap.add_argument("--country")
    ap.add_argument("--gap", action="store_true",
                    help="read in other languages, no English article yet")
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--next", action="store_true", dest="nxt",
                    help="print the batch a night run should take")
    ap.add_argument("--batches", type=int, default=1)
    args = ap.parse_args()

    rows = leads()
    cache = load()
    if args.resolve:
        cache = resolve(rows, cache, args.limit)
        cache = count_views(cache, args.limit)

    open_rows = [r for r in rows if r.get("status") == "lead"]
    open_rows = drop_already_published(open_rows, already_published_trees())
    if args.country:
        open_rows = [r for r in open_rows
                     if r["country"] == args.country.lower().replace(" ", "-")]

    scored = []
    for r in open_rows:
        e = cache.get(r["name"])
        if not e:
            continue
        wikis = e.get("wikis") or {}
        scored.append({
            "name": r["name"], "country": r["country"],
            "langs": len(wikis), "views": e.get("views") or 0,
            "en": "enwiki" in wikis,
            "pin": r.get("lat") is not None,
            "photos": len(r.get("photos") or []),
            "species": r.get("species"),
        })
    if args.gap:
        scored = [s for s in scored if s["langs"] and not s["en"]]
    scored.sort(key=lambda s: (-s["views"], -s["langs"]))

    if args.nxt:
        rows_by_name = {r["name"]: r for r in open_rows}
        print_next(scored, rows_by_name, published_places(), args.batches)
        return

    resolved = sum(1 for r in open_rows if r["name"] in cache)
    print("%d open famous-tree lead(s), %d resolved, %d with an article "
          "somewhere" % (len(open_rows), resolved,
                         sum(1 for s in scored if s["langs"])))
    if args.gap:
        print("Read in other languages and unwritten in English: the thin-"
              "competition end of the list.")
    print()
    print("%-42s %-15s %5s %7s %4s %3s" %
          ("tree", "country", "langs", "views/mo", "pin", "ph"))
    for s in scored[:args.top]:
        print("%-42.42s %-15.15s %5d %7d %4s %3d" %
              (s["name"], s["country"], s["langs"], s["views"],
               "yes" if s["pin"] else "-", s["photos"]))
    if not args.resolve and resolved < len(open_rows):
        print("\n%d lead(s) never resolved; run --resolve"
              % (len(open_rows) - resolved))


if __name__ == "__main__":
    main()
