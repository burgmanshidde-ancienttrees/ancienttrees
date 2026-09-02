#!/usr/bin/env python3
"""Regenerate CITY_QUEUE.md's table, and make data/city-list.json agree with it.

Written 2026-08-12, after Hidde asked for "1 wachtrij / city order" and a rule
for how many trees a city should aim for. Both problems had the same cause: the
order was maintained by hand in CITY_QUEUE.md while data/city-list.json carried
its own `rank`, `queue` and `tier` fields from an older scheme. They disagreed
badly. Porto was rank 62 in the json and rank 2 in the queue; Rome was rank 4
against 12. CLAUDE.md Step 0 tells every run to read city-list.json first, so
the stale order was the one being obeyed.

So: this script owns the table. It preserves the two columns it cannot compute
(`score` and `demand`, which come from Search Console evidence and Wikipedia
pageviews, both decided in session), recomputes everything measurable, and
writes city-list.json with no ordering fields at all. The json is inventory now:
which city, which country, published or not. Order lives in one place.

    python3 scripts/city_queue.py            # rewrite both
    python3 scripts/city_queue.py --check    # exit 1 if either is stale

THE TARGET COLUMN lives in CITY_QUEUE.md, not here.

Ruled by Hidde 2026-08-19, replacing the 2026-08-13 sprint: DEEPENING OUTRANKS
opening new cities, confirmed cities aim at 30, and the biggest confirmed ones
at 50. `target_for()` below is the whole implementation and carries the
reasoning; the rule and every superseded version are written once in
CITY_QUEUE.md's "How far to take a city" section.

This docstring used to restate the rule in full, and within the hour it was
describing the previous version while the code did something else, which is the
same two-copies disease this script exists to cure for the city order.
"""
import argparse
import glob
import json
import math
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "data", "city-queue.json")
QUEUE = os.path.join(ROOT, "CITY_QUEUE.md")
LIST = os.path.join(ROOT, "data", "city-list.json")
# A data row is any table line whose first cell is a rank. Parsed by SPLITTING
# rather than by a full-shape regex, because the first version pinned the old
# eight-column layout: after this script added `walks` and `target` the pattern
# still matched the first eight cells, so `basis` captured the register count
# and every row's "measured" was overwritten with a number on the next run. A
# generator that corrupts its own output on the second run is worse than no
# generator, so the parser now reads the two columns it must preserve (score,
# demand) from the front and `basis` from the END, where it always sits.
ROW = re.compile(r"^\|\s*\d+\s*\|")

sys.path.insert(0, os.path.join(ROOT, "scripts"))
import walk_planning as B          # noqa: E402
import walks_feed                  # noqa: E402

# Read once. The walks live in site/src/lib/walks.ts and are published in the
# feed; this file used to plan them again in Python to count them, which is the
# duplication Hidde asked to end ("1 wandelalgoritme"). A count is the cheapest
# possible reason to keep a second implementation alive.
try:
    WALKS = walks_feed.by_city()
except SystemExit:
    WALKS = {}
import leads as L                  # noqa: E402



UA = "AncientTrees/1.0 (https://ancienttrees.app; tree mapping project)"
COORD_CACHE = os.path.join(ROOT, "data", "city-coords.json")


def city_coords(city, article=None):
    """Lat/lon for a city we do not publish yet, from Wikipedia's own API.

    Written 2026-08-13, when the sprint list said 54 of 60 cheap cities needed a
    scout. It was a measurement artefact: `near()` counts register points around
    the mean position of a city's PUBLISHED trees, so an unpublished city had no
    centre and scored zero register supply by construction. Pisa, Siena, Bergamo
    and every other unopened Italian city read as expensive while MASAF holds
    5,007 trees. Cached on disk; one fetch per city, ever."""
    try:
        with open(COORD_CACHE, encoding="utf-8") as fh:
            cache = json.load(fh)
    except (OSError, ValueError):
        cache = {}
    key = article or city
    if key in cache:
        v = cache[key]
        return tuple(v) if v else None
    # `coprimary=all` matters too: Assisi, Matera and Sorrento all carry their
    # coordinates as non-primary, so a primary-only query returned a page with
    # no position at all and every Italian comune of that shape read as having
    # no register behind it while MASAF holds 5,007 trees.
    # `redirects` matters more than it looks: the queue writes city names in
    # ASCII, so Malmo, Bogota, Sao Paulo, Evora and Cesky Krumlov all missed
    # their own article and scored zero register supply by construction, which
    # is the same artefact this function was written to fix, one layer down.
    q = urllib.parse.urlencode({"action": "query", "prop": "coordinates",
                                "titles": article or city, "format": "json",
                                "formatversion": "2", "redirects": "1",
                                "coprimary": "all"})
    out = None
    try:
        req = urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q,
                                     headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.load(r)
        for page in d.get("query", {}).get("pages", []):
            c = (page.get("coordinates") or [{}])[0]
            if c.get("lat") is not None:
                out = (c["lat"], c["lon"])
    except Exception:
        out = None
    cache[key] = list(out) if out else None
    with open(COORD_CACHE, "w", encoding="utf-8") as fh:
        json.dump(cache, fh, ensure_ascii=False, indent=1, sort_keys=True)
    return out


def register_rows(d):
    """Every list of dicts in a register file, whatever it is called.

    This used to read `trees` or `entries` and nothing else, which silently
    lost two whole registers: Quebec City stores raw GeoJSON under `features`
    (685 trees) and Massachusetts splits its data into `champion_trees_2026`
    and `legacy_trees_2026` (615, and Boston sits in it). Both files were
    correct and both counted as zero supply, which is the same failure as the
    coordinate bug found the same morning: a measurement that reads zero
    because of its own shape assumption, not because the data is missing.
    So: take any list of dicts, and let the coordinate reader decide."""
    if isinstance(d, list):
        return d
    out = []
    for v in d.values():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            out.extend(v)
    return out


def row_point(r):
    """Lat/lon out of a register row in any of the three shapes seen so far."""
    la, lo = r.get("latitude", r.get("lat")), r.get("longitude", r.get("lng"))
    if la is None and isinstance(r.get("geometry"), dict):
        # Raw GeoJSON, and the order is longitude first, which is the reverse
        # of every other coordinate in this repo.
        c = r["geometry"].get("coordinates")
        if isinstance(c, list) and len(c) >= 2:
            lo, la = c[0], c[1]
    try:
        return (float(la), float(lo)) if la is not None and lo is not None else None
    except (TypeError, ValueError):
        return None


def register_points(warn=False):
    pts = []
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "registers", "*.json"))):
        with open(p, encoding="utf-8") as fh:
            d = json.load(fh)
        rows = register_rows(d)
        got = [q for q in (row_point(r) for r in rows if isinstance(r, dict)) if q]
        # A register file that contributes nothing is nearly always a shape
        # this reader has not met yet, not an empty register. Say so rather
        # than letting it count as zero supply for a city.
        if warn and not got:
            print("  WARNING %s yields no coordinates (%d rows read). If the "
                  "file has data, register_points() cannot see its shape."
                  % (os.path.basename(p), len(rows)))
        pts.extend(got)
    return pts


WIKIDATA = os.path.join(ROOT, "data", "research", "wikidata-remarkable-trees.json")


def wikidata_points():
    """The Wikidata remarkable-tree layer as points, minus what we already map.

    Why this is here at all, 2026-08-27. The stage-1 table printed `register 0,
    ready 0` for Leipzig, and a night run reading that line concluded there was
    nothing it was allowed to do there, nine times a day. On disk sat 63 named
    Leipzig trees with a species each, and 209 for Dresden, 151 for Potsdam:
    the exact supply data/register-scouting.json names as Germany's route
    ("the route here is the Wikidata layer, not the state"). The queue's own
    header already told a run to open a city "from a register, a leads file or
    a Wikidata cluster" and then printed no column for the third one, so the
    one country whose supply is entirely Wikidata read as empty everywhere.

    Deduped at 80 m against our published pins, the same threshold passcheck
    uses, so the number means trees we do NOT have rather than trees that
    exist. Missing file returns nothing: this is scouting gear, and a queue
    rebuild must never fail because a scouting fetch has not been run.
    """
    try:
        with open(WIKIDATA, encoding="utf-8") as fh:
            rows = json.load(fh)["trees"]
    except (OSError, ValueError, KeyError):
        return []
    ours = []
    for f in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        try:
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError):
            continue
        for t in d.get("trees", []):
            loc = t.get("location") or {}
            if loc.get("latitude") is not None:
                ours.append((loc["latitude"], loc["longitude"]))
    out = []
    for r in rows:
        lat, lng = r.get("latitude"), r.get("longitude")
        if lat is None or lng is None:
            continue
        if any(abs(a - lat) < 0.0008 and abs(b - lng) < 0.0008 for a, b in ours):
            continue
        out.append((lat, lng))
    return out


WD = []


def near(pts, lat, lng, km=5.0):
    """Bounding box, not haversine: at 5 km the difference cannot change a
    band, and 17,854 register points times 95 cities wants the cheap test."""
    dlat = km / 111.0
    dlng = km / (111.0 * max(math.cos(math.radians(lat)), 0.1))
    return sum(1 for a, b in pts if abs(a - lat) < dlat and abs(b - lng) < dlng)


def target_for(demand, measured, impressions=0, travel=0):
    """How far a city goes. Three numbers, and 50 is not one of them.

    Hidde, 2026-08-19, correcting the version written an hour earlier: "we
    willen helemaal geen 50 bomen in bath mss max 20. kunnen we vanaf nu gewoon
    voor 30 grote bomen streven bij grote stad en bevestigd."

        not confirmed by Search Console       10
        confirmed, ordinary city              20
        confirmed, big city                   30

    **The 50 tier is gone entirely**, not narrowed. It survived about an hour
    and he was right to kill it: thirty remarkable trees is already a lot of
    city, and a page that needs fifty is a page padded past the point where
    every entry deserves its spot. Exclusivity is the product (CLAUDE.md), so a
    higher ceiling buys nothing and risks the one thing that makes collecting
    work.

    The 20/30 split is city size, and size is travel demand, the term the queue
    already ranks by. Bath is the worked example he named: it ranks well, which
    is why the impressions-only version handed it 50, but it is a small city and
    tops out at 20. Rome and Amsterdam carry 30.

    Unchanged and load-bearing: an unconfirmed city stops at 10, the floor is
    four verified trees or no page, and the 80/20 rule ends any city the moment
    its next tree gets hard to find. A target is a ceiling and a stopping point,
    never a quota. Cadiz at 5 is finished work.
    """
    if not measured:
        return 10
    return 30 if (travel or 0) >= 8000 else 20


def measure(pts):
    """Per published city: trees, photos, walks, register supply, ready leads."""
    blocking = L.rules()["blocking"]
    out = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        with open(p, encoding="utf-8") as fh:
            d = json.load(fh)
        slug = os.path.basename(p)[:-5]
        ts = [t for t in d["trees"] if (t.get("location") or {}).get("latitude")]
        if not ts:
            continue
        lat = sum(t["location"]["latitude"] for t in ts) / len(ts)
        lng = sum(t["location"]["longitude"] for t in ts) / len(ts)
        PUB_PINS.extend((t["location"]["latitude"], t["location"]["longitude"],
                         d["city"]) for t in ts)
        lp = os.path.join(ROOT, "data", "leads", f"{slug}.json")
        ready = 0
        if os.path.exists(lp):
            with open(lp, encoding="utf-8") as fh:
                for e in json.load(fh).get("leads") or []:
                    if (not L.is_done(e) and not L.published_match(slug, e)
                            and not L.classify(e, blocking) and not L.readiness(e)):
                        ready += 1
        out[d["city"].lower()] = {
            "slug": slug,
            "city": d["city"],
            "country": d.get("country", ""),
            "trees": len(d["trees"]),
            "photos": sum(1 for t in d["trees"]
                          if (t.get("photo") or {}).get("status") == "approved"
                          or (t.get("photo") or {}).get("url")),
            # The published count, not a second planning of it (2026-08-25).
            "walks": len(WALKS.get(slug, [])),
            "register": near(pts, lat, lng),
            # 15 km, not 5: the Wikidata layer is a day-trip band rather than a
            # walk, and it is what wikidata_trees.py reports against.
            "wikidata": near(WD, lat, lng, 15.0),
            "ready": ready,
        }
    return out


def load_source():
    with open(SOURCE, encoding="utf-8") as fh:
        return json.load(fh)


# Countries whose register story makes a city cheap to open or deepen, per
# OPEN_DATA_SURVEY.md's verdicts: a usable national register (Portugal ICNF,
# Italy MASAF, Japan's giant-tree db, Ireland's heritage trees), Spain's
# regional patchwork (mostly imported), or a proven municipal pattern
# (Netherlands: Den Bosch and Amsterdam both ship from city ArcGIS). City-
# scoped imports (Berlin, Vienna, Paris, Brussels) deliberately do NOT clear
# their whole country; those cities score through nearby register points.
REGISTER_COUNTRIES = {"Portugal", "Italy", "Japan", "Ireland", "Spain", "Netherlands"}


def ease_for(country, supply):
    """1.0 to 2.0. Hidde, 2026-08-13: "steden met registers en dus makkelijk
    aanpak prioriteren... potentie qua toerisme + bewezen google prestatie +
    gemak in opstellen". The boundary that keeps this honest, from the Vienna-50
    mistake the same week: ease multiplies the ORDER of work, never the target,
    because a register measures how easy trees are to find, not how good."""
    return 1.0 + (0.5 if country in REGISTER_COUNTRIES else 0.0) + 0.5 * min(supply, 25) / 25


PTS = []

# Every pin we already publish, as (lat, lng, city). Built once in main().
PUB_PINS = []


def covered_by(lat, lng, km=8.0):
    """Which published city, if any, already has trees in this town.

    Written 2026-09-02 after a session claimed Funchal (#176, "0 trees") and
    dispatched a pass to open it, when nine of the thirteen candidates it was
    handed sat inside data/cities/madeira.json and five were already live. The
    queue is not wrong about the count: nothing is published under the name
    Funchal. It is matching by NAME, which is the exact failure CLAUDE.md
    records for Napoli and Firenze and which backlog.py exists to prevent, so
    the fix belongs here rather than in a run's memory.

    8 km, not 25: the question is "are our pins already in this town", not
    "is there a published city in the region". Pisa and Lucca are 20 km apart
    and are genuinely two cities; Funchal and Madeira are 500 metres apart and
    are one.
    """
    dlat = km / 111.0
    dlng = km / (111.0 * max(math.cos(math.radians(lat)), 0.1))
    hits = {}
    for a, b, city in PUB_PINS:
        if abs(a - lat) < dlat and abs(b - lng) < dlng:
            hits[city] = hits.get(city, 0) + 1
    if not hits:
        return None
    city, n = max(hits.items(), key=lambda kv: kv[1])
    return {"city": city, "trees": n}


def enrich(doc, live):
    """Write the measured columns into the source file itself, so the numbers a
    human reads and the numbers a script computes are the same object."""
    for c in doc["cities"]:
        info = live.get(c["city"].lower())
        if info:
            # Measure supply around the city itself, not around the mean of the
            # trees we happen to publish. Hong Kong's six trees average out to a
            # point in the harbour with 19 register trees near it, while Central
            # has 505: a spread-out city was reading as having no supply at all,
            # which is the Kyoto 35-km problem wearing a different hat.
            pos = city_coords(c["city"], c.get("article"))
            reg = near(PTS, pos[0], pos[1]) if pos else info["register"]
            info["register"] = max(reg, info["register"])
            wd = near(WD, pos[0], pos[1], 15.0) if pos else info["wikidata"]
            info["wikidata"] = max(wd, info["wikidata"])
            supply = info["register"] + info["ready"] + info["wikidata"]
            c.update(status="published", trees=info["trees"], photos=info["photos"],
                     walks=info["walks"], register=info["register"],
                     ready=info["ready"], wikidata=info["wikidata"], supply=supply,
                     target=target_for(c.get("demand"), c.get("basis", "").startswith("measured"), c.get("impressions_10d"), c.get("travel")))
        else:
            # An unpublished city still has register supply around it; it just
            # has no trees to average a centre from. Look the city itself up.
            pos = city_coords(c["city"], c.get("article"))
            reg = near(PTS, pos[0], pos[1]) if pos else 0
            # The branch that matters for stage 1: a city on zero has no trees
            # to average a centre from, so if the Wikidata layer is not counted
            # HERE it is not counted anywhere for exactly the cities the queue
            # is telling a run to open.
            wd = near(WD, pos[0], pos[1], 15.0) if pos else 0
            supply = reg + wd
            cov = covered_by(pos[0], pos[1]) if pos else None
            if cov:
                c["covered_by"] = cov
            else:
                c.pop("covered_by", None)
            c.update(status="pending", trees=0, photos=0, walks=0,
                     register=reg, ready=0, wikidata=wd, supply=supply,
                     target=target_for(c.get("demand"), c.get("basis", "").startswith("measured"), c.get("impressions_10d"), c.get("travel")))
        c["ease"] = round(ease_for(c.get("country", ""), supply), 2)
        c["work_score"] = round((c.get("score") or 0) * c["ease"], 2)
    ranked = sorted([c for c in doc["cities"] if c.get("score") is not None],
                    key=lambda c: (-c["work_score"], c["city"]))
    for n, c in enumerate(ranked, 1):
        c["rank"] = n
    for c in doc["cities"]:
        if c.get("score") is None:
            c["rank"] = None
    doc["cities"].sort(key=lambda c: (c["rank"] is None, c["rank"] or 0, c["city"]))
    with open(SOURCE, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    return doc


def rebuild_table(doc):
    """Render CITY_QUEUE.md's table FROM the source file.

    It used to be the other way round: the markdown table was the source and
    this script regex-parsed it. That is how the first version corrupted every
    row's `basis` when the layout gained two columns. A rendered table cannot
    drift from the data it is rendered from."""
    with open(QUEUE, encoding="utf-8") as fh:
        text = fh.read()
    head = "| # | city | score | demand | trees | photos | walks | register | target | basis |"
    sep = "|---|---|---:|---:|---:|---:|---:|---:|---:|---|"
    body = []
    for c in doc["cities"]:
        if c["rank"] is None:
            continue
        body.append("| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            c["rank"], c["city"],
            ("%.2f" % c["score"]) if c.get("score") is not None else "-",
            ("{:,}".format(c["demand"])) if c.get("demand") else "-",
            c["trees"] or "-", c["photos"] or "-", c["walks"] or "-",
            c["register"] or "-", c["target"] or "-", c["basis"]))
    table = "\n".join([head, sep] + body)
    start = text.index(head) if head in text else text.index("| # | city |")
    end = text.index("\n\n", start)
    text = text[:start] + table + text[end:]
    with open(QUEUE, "w", encoding="utf-8") as fh:
        fh.write(text)
    return [c["city"].lower() for c in doc["cities"] if c["rank"]]


def rebuild_list(live, order):
    """city-list.json becomes inventory: no rank, no queue, no tier.

    Those three fields were the rival ordering. Nothing reads them (checked
    across scripts/ and site/src on 2026-08-12; brief.py reads the file but only
    for city and status), and leaving them in is what let a run obey the wrong
    order. `trees` is regenerated rather than kept, because a hand-maintained
    count goes stale the moment a write pass lands: Barcelona read 33 while it
    published 46."""
    with open(LIST, encoding="utf-8") as fh:
        d = json.load(fh)
    rows = d if isinstance(d, list) else d["cities"]
    pos = {c: i for i, c in enumerate(order)}
    for r in rows:
        for dead in ("rank", "queue", "tier"):
            r.pop(dead, None)
        info = live.get((r.get("city") or "").lower())
        r["status"] = "published" if info else r.get("status", "pending")
        r["trees"] = info["trees"] if info else 0
    rows.sort(key=lambda r: (pos.get((r.get("city") or "").lower(), 9999),
                             r.get("city") or ""))
    if isinstance(d, list):
        d = rows
    else:
        d["cities"] = rows
        d["note"] = ("Inventory only: which city, which country, published or not. "
                     "The ORDER lives in CITY_QUEUE.md and nowhere else, and this "
                     "file is regenerated by scripts/city_queue.py. It used to "
                     "carry rank/queue/tier from an older scheme, which disagreed "
                     "with the queue (Porto 62 here against 2 there) and was the "
                     "one runs actually read.")
    with open(LIST, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
    return len(rows)


NAMED_BY_HIDDE = [
    # 2026-08-19, verbatim from his own message and recorded in CITY_QUEUE.md.
    # This list is the SCOPE of "from-zero web research is on", not a synonym
    # for "unopened": see the WARN answered in the --next printer below.
    "Seattle", "Dallas", "Houston", "Cologne", "Perth", "Sydney", "Las Vegas",
    "Frankfurt", "Bilbao", "Dubai", "Kansas City", "Mexico City", "Vancouver",
    "Manchester", "Taipei", "Buenos Aires", "Hawaii",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if city-list.json still carries an ordering field")
    ap.add_argument("--next", action="store_true",
                    help="print the cities below target, in queue order: what to work on")
    a = ap.parse_args()

    if a.next:
        # ORDER, settled 2026-08-19 after Hidde looked at the actual list and
        # corrected the version written an hour earlier: "persoonlijk denk ik
        # dat deze steden zonder register toch starten interessanter is dan
        # verdiepen... deze zsm naar 10 krijgen." He named Seattle, Dallas,
        # Houston, Cologne, Perth, Sydney, Las Vegas, Frankfurt, Bilbao, Dubai,
        # Kansas City, Mexico City, Vancouver, Manchester, Taipei, Buenos Aires
        # and Hawaii, all ranked, all at zero trees, several with no register.
        #
        # So OPENING comes first again and deepening second. The reasoning is
        # visible in the numbers he was reading: a new city taken to 10 is a
        # page that can start ranking, while a thirtieth tree in Rome is
        # marginal. It also means from-zero research on a named city is on,
        # which rule 1(d) already allows when Hidde names the city.
        #
        # What did NOT come back with it: the old 10/20/30/50 ladder. Targets
        # are 10 unconfirmed, 20 confirmed, 30 for a big confirmed city, set the
        # same morning and unchanged by this.
        doc = load_source()
        s1 = [c for c in doc["cities"] if c.get("rank") and not c.get("trees", 0)]
        s2 = [c for c in doc["cities"] if c.get("rank") and c.get("target")
              and c.get("trees", 0) and c.get("trees", 0) < c["target"]]
        s1.sort(key=lambda c: c["rank"])
        s2.sort(key=lambda c: c["rank"])
        # The star matters, and it is the whole of the 2026-08-19 fresh-eyes
        # WARN: Hidde named SEVENTEEN cities, and this list is every ranked
        # city with no trees, currently ten times that. The header used to say
        # "he named these cities" over all of them, which reads as blanket
        # permission for from-zero web research and is exactly what rule 1(d)
        # exists to stop. Named is named; the rest still need a register, a
        # lead file or a Wikidata cluster before a pass is worth dispatching.
        named = {c.lower() for c in NAMED_BY_HIDDE}
        print("STAGE 1, OPEN THE UNOPENED: every ranked city with no trees yet,")
        print("to 10, as fast as they go. Hidde, 2026-08-19: starting these beats")
        print("deepening.\n")
        print("  * = one of the 17 he named on 2026-08-19, so from-zero web")
        print("      research is ON there (rule 1(d)). Everywhere else on this")
        print("      list, from-zero is still OFF: open it from a register, a")
        print("      leads file or a Wikidata cluster, or leave it.")
        print("  wikidata = named trees within 15 km that we do NOT map, from")
        print("      the CC0 layer. It is a lead list, not a register: every")
        print("      entry still needs its second source and its own pin.")
        print("  COVERED = we already publish trees in this town under another")
        print("      name. Zero here means zero pages called that, not zero")
        print("      trees on the ground: deepen the named city instead of")
        print("      opening a second page beside it.\n")
        # Supply first, rank second, since 2026-08-28. Hidde put opening a
        # zero-tree city with supply at the top of rule one that day ("ik denk
        # nog steeds dat het nuttiger is om steden toe te voegen die op 0 staan
        # maar wel in onze top lijst"), and this list was printing in pure rank
        # order, so the cities a run may actually open sat scattered among
        # dozens it may not touch at all. A run reading the top of the list saw
        # Chiang Mai, Jerusalem and Dubai, all with nothing to open them from,
        # and Dresden with 209 Wikidata trees was twenty rows down.
        def _supply(c):
            return c.get("register", 0) + c.get("ready", 0) + c.get("wikidata", 0)

        openable = [c for c in s1 if _supply(c) > 0]
        dry = [c for c in s1 if _supply(c) == 0]
        print("  OPENABLE TODAY (%d of %d): supply already on hand, so rule 1(d)"
              % (len(openable), len(s1)))
        print("  does not apply. These are the top of rule one.\n")
        print("  #  city             register  ready  wikidata")
        for c in openable[:25]:
            print("%3d %s%-16s %9d %6d %9d" % (
                c["rank"], "* " if c["city"].lower() in named else "  ",
                c["city"][:16], c.get("register", 0), c.get("ready", 0),
                c.get("wikidata", 0)))
            cov = c.get("covered_by")
            if cov:
                print("      COVERED: %d trees already published as %s"
                      % (cov["trees"], cov["city"]))
        print("\n  NOTHING TO OPEN THEM FROM (%d): scout a register (rung 5) or"
              % len(dry))
        print("  wait for Hidde to name one. Do not research these from zero.\n")
        print("  " + ", ".join("%s (#%d)" % (c["city"], c["rank"]) for c in dry[:15]))
        print("\nSTAGE 2, DEEPENING: once stage 1 has nothing left that moves")
        print("cheaply. Targets are 20, or 30 for a big confirmed city.\n")
        print("  #  city             now target  ready  register  wikidata")
        for c in s2[:20]:
            print("%3d  %-16s %4d %6d %6d %9d %9d" % (
                c["rank"], c["city"][:16], c.get("trees", 0),
                c["target"], c.get("ready", 0), c.get("register", 0),
                c.get("wikidata", 0)))
        print("\nStage 1: %d cities unopened. Stage 2: %d cities, %d trees to target."
              % (len(s1), len(s2), sum(c["target"] - c.get("trees", 0) for c in s2)))

        # WHAT A RUN CAN ACTUALLY MOVE, added 2026-08-16 from the night's own
        # numbers. The lists above are the STRATEGIC order and are correct as
        # that; they are not a to-do list, and a night run was reading them as
        # one. Measured that morning: 4 of the 29 stage-1 cities had any
        # register or ready supply at all. The other 25 are from-zero web
        # research, which CLAUDE.md turns off unless Hidde names the city, so a
        # run walking this list top-down meets Toronto, Montreal, Sydney,
        # Frankfurt, Perth, Vilnius and Los Angeles in a row and is forbidden
        # to touch any of them. It then has to reason its way past all of them
        # before finding real work, nine times a day. Four runs that night
        # spent their whole window on exactly that and shipped nothing.
        #
        # So the order stays untouched (it is Hidde's) and the actionable
        # subset is printed under it. Nothing here decides priority; it only
        # says which of the ranked cities have something to work FROM.
        movable = [c for c in s1 + s2
                   if (c.get("ready", 0) or c.get("register", 0)
                       or c.get("wikidata", 0) >= 4)]
        # UNOPENED FIRST, and it is a priority ruling rather than a tidy-up.
        # Hidde, 2026-08-27: "wat mij betreft gaan we zoveel mogelijk steden
        # van nul naar tien zetten", so that they get indexed and Google can
        # say which ones are worth deepening. Sorting this list by rank alone
        # put Milan, Florence and Singapore at the top of it, all published and
        # all deepening, which is the opposite of the order the header above
        # states. Within each half the order is still the queue's own.
        movable.sort(key=lambda c: (c.get("trees", 0) > 0, c.get("rank") or 9999))
        print("\nWHAT YOU CAN ACTUALLY MOVE, i.e. the ranked cities that have "
              "data to work from.\nEverything else on the lists above needs "
              "from-zero web research, which is OFF\nunless Hidde names the "
              "city (CLAUDE.md, rule one (d)).\n")
        if movable:
            print("  #  city             now  ready  register  wikidata")
            for c in movable[:18]:
                print("%3d  %-16s %4d %6d %9d %9d" % (
                    c["rank"], c["city"][:16], c.get("trees", 0),
                    c.get("ready", 0), c.get("register", 0), c.get("wikidata", 0)))
            print("\n  %d of %d ranked cities have supply."
                  % (len(movable), len(s1) + len(s2)))
        else:
            print("  None. Every ranked city is out of data.")
        print("\nAnd the shelf is usually the cheaper answer than any of them:\n"
              "  python3 scripts/prepare.py     staged for verify, awaiting a writer\n"
              "  python3 scripts/leads.py       READY leads needing only a story")
        return 0

    if a.check:
        with open(LIST, encoding="utf-8") as fh:
            d = json.load(fh)
        rows = d if isinstance(d, list) else d["cities"]
        bad = sorted({k for r in rows for k in ("rank", "queue", "tier") if k in r})
        if bad:
            print("FAIL data/city-list.json carries ordering field(s): %s. "
                  "The order lives in CITY_QUEUE.md; run python3 scripts/city_queue.py"
                  % ", ".join(bad))
            return 1
        print("city-list.json is inventory only, order lives in CITY_QUEUE.md")
        return 0

    pts = register_points(warn=True)
    globals()['PTS'] = pts
    globals()['WD'] = wikidata_points()
    live = measure(pts)
    doc = enrich(load_source(), live)
    order = rebuild_table(doc)
    n = rebuild_list(live, order)
    confirmed = [c for c in doc["cities"] if c.get("basis","").startswith("measured")]
    print("%d register points, %d live cities measured" % (len(pts), len(live)))
    print("data/city-queue.json: %d cities, %d ranked (the source)"
          % (len(doc["cities"]), len(order)))
    print("rendered: %d rows in CITY_QUEUE.md, %d entries in city-list.json"
          % (len(order), n))
    print("%d cities are Google-confirmed and aim at 30 or 50; "
          "the rest aim at 10" % len(confirmed))

    # LEDGER.html is Hidde's own view of the same numbers, and it is rebuilt
    # here so it can never be staler than the queue it draws from. Deterministic
    # rendering, no fetches, no tokens. Wrapped because a rendering failure must
    # never take down the queue rebuild that a night run depends on.
    try:
        import ledger
        ledger.main()
    except Exception as e:
        print("  (LEDGER.html not rewritten: %s)" % e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
