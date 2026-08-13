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

Ruled by Hidde 2026-08-12: ten trees everywhere first, twenty-five once Search
Console confirms a city. `target_for()` below is the whole implementation and
carries the reasoning; the rule, its two superseded versions and why they were
wrong are written once in CITY_QUEUE.md's "How far to take a city" section.

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
    q = urllib.parse.urlencode({"action": "query", "prop": "coordinates",
                                "titles": article or city, "format": "json",
                                "formatversion": "2"})
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


def register_points():
    pts = []
    for p in glob.glob(os.path.join(ROOT, "data", "registers", "*.json")):
        with open(p, encoding="utf-8") as fh:
            d = json.load(fh)
        rows = d if isinstance(d, list) else (d.get("trees") or d.get("entries") or [])
        for r in rows:
            if not isinstance(r, dict):
                continue
            la = r.get("latitude", r.get("lat"))
            lo = r.get("longitude", r.get("lng"))
            try:
                if la is not None and lo is not None:
                    pts.append((float(la), float(lo)))
            except (TypeError, ValueError):
                continue
    return pts


def near(pts, lat, lng, km=5.0):
    """Bounding box, not haversine: at 5 km the difference cannot change a
    band, and 17,854 register points times 95 cities wants the cheap test."""
    dlat = km / 111.0
    dlng = km / (111.0 * max(math.cos(math.radians(lat)), 0.1))
    return sum(1 for a, b in pts if abs(a - lat) < dlat and abs(b - lng) < dlng)


def target_for(demand, measured):
    """Hidde's staircase, ruled 2026-08-13: everyone gets to 10 first, and only
    a city Google has confirmed climbs further, by size. "stadje 10 bomen,
    grote stad 20, mega stad 30, metropool tot max 50." Size comes from the
    demand column (English Wikipedia pageviews), the proxy the queue already
    ranks by; `measured` is the basis column saying Search Console has spoken.

    The target is a ceiling and a stopping point, and his 80/20 rule governs
    reaching it: when the next tree gets hard to find, move on to the next
    city rather than grinding out the max ("eeuwig tokens gebruiken tot deze
    max te halen is niet de strategie"). The floor stays four or no page."""
    if not measured:
        return 10
    d = demand or 0
    if d >= 700_000:
        return 50   # metropool: London, New York class
    if d >= 300_000:
        return 30   # mega stad: Rome, Prague, Barcelona class
    if d >= 100_000:
        return 20   # grote stad: Vienna, Lisbon, Porto class
    return 10       # stadje: Cadiz, Sintra class; confirmed changes nothing


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
        markers = [{"lat": t["location"]["latitude"], "lng": t["location"]["longitude"],
                    "name": t.get("name", "")} for t in ts]
        lp = os.path.join(ROOT, "data", "leads", f"{slug}.json")
        ready = 0
        if os.path.exists(lp):
            with open(lp, encoding="utf-8") as fh:
                for e in json.load(fh).get("leads") or []:
                    if not L.is_done(e) and not L.classify(e, blocking) and not L.readiness(e):
                        ready += 1
        out[d["city"].lower()] = {
            "slug": slug,
            "city": d["city"],
            "country": d.get("country", ""),
            "trees": len(d["trees"]),
            "photos": sum(1 for t in d["trees"]
                          if (t.get("photo") or {}).get("status") == "approved"
                          or (t.get("photo") or {}).get("url")),
            "walks": len(B.plan_walks(markers)),
            "register": near(pts, lat, lng),
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
            supply = info["register"] + info["ready"]
            c.update(status="published", trees=info["trees"], photos=info["photos"],
                     walks=info["walks"], register=info["register"],
                     ready=info["ready"], supply=supply,
                     target=target_for(c.get("demand"), c["basis"].startswith("measured")))
        else:
            # An unpublished city still has register supply around it; it just
            # has no trees to average a centre from. Look the city itself up.
            pos = city_coords(c["city"], c.get("article"))
            reg = near(PTS, pos[0], pos[1]) if pos else 0
            supply = reg
            c.update(status="pending", trees=0, photos=0, walks=0,
                     register=reg, ready=0, supply=reg,
                     target=target_for(c.get("demand"), c["basis"].startswith("measured")))
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if city-list.json still carries an ordering field")
    ap.add_argument("--next", action="store_true",
                    help="print the cities below target, in queue order: what to work on")
    a = ap.parse_args()

    if a.next:
        # Two stages, worked in this order. Stage 1 is the sprint: every ranked
        # city to 10, because a page must exist before Google can judge it.
        # Stage 2 is deepening, only on Google-confirmed cities, up the
        # 20/30/50 staircase. Hidde, 2026-08-13: "zo snel mogelijk bij de top
        # 100 10 bomen bij elke stad... daarna verdiepen op degene die echt
        # goed presteren." His 80/20 rule rides along: stop at the target, and
        # stop EARLIER the moment the next tree gets hard to find.
        doc = load_source()
        s1 = [c for c in doc["cities"] if c.get("rank") and c.get("trees", 0) < 10]
        s2 = [c for c in doc["cities"] if c.get("rank") and c.get("target")
              and 10 <= c.get("trees", 0) < c["target"]]
        s1.sort(key=lambda c: c["rank"])
        s2.sort(key=lambda c: c["rank"])
        print("STAGE 1, the sprint: every ranked city to 10 trees. Top-down,")
        print("take the first you can move cheaply. 80/20: when the next tree")
        print("gets hard to find, move to the next city, never grind.\n")
        print("  #  city             now  gap  ready  register")
        for c in s1:
            print("%3d  %-16s %4d %4d %6d %9d" % (
                c["rank"], c["city"][:16], c.get("trees", 0),
                10 - c.get("trees", 0), c.get("ready", 0), c.get("register", 0)))
        print("\nSTAGE 2, deepening: PAUSED while any ranked city above can still")
        print("be moved to 10 cheaply (Hidde, 2026-08-13: breadth over depth in")
        print("the whole top 250). Listed only so the later work stays visible.\n")
        print("  #  city             now target  ready  register")
        for c in s2:
            print("%3d  %-16s %4d %6d %6d %9d" % (
                c["rank"], c["city"][:16], c.get("trees", 0),
                c["target"], c.get("ready", 0), c.get("register", 0)))
        print("\nStage 1: %d cities, %d trees. Stage 2: %d cities, %d trees."
              % (len(s1), sum(10 - c.get("trees", 0) for c in s1),
                 len(s2), sum(c["target"] - c.get("trees", 0) for c in s2)))
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

    pts = register_points()
    globals()['PTS'] = pts
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
    print("%d cities are Google-confirmed and climb the 20/30/50 staircase; "
          "the rest aim at 10" % len(confirmed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
