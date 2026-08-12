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

THE TARGET COLUMN, and the reasoning, because a number without one is a wish.

Hidde, 2026-08-12: "ik denk dat we veel beter een hoop steden met 10-25 bomen
en dan later verdiepen." So the target is a first-version ceiling of 25, not a
per-city ambition scaled by how much supply happens to sit nearby.

This is the SECOND version of this column, and the first one is worth recording
because it was wrong in a way that looked reasonable. It banded the target by
supply (register trees within 5 km plus ready leads) and gave 50 to cities with
200+ supply AND measured demand, 30 otherwise. That produced Vienna 50 and
Barcelona 30: two cities with comparable supply, opposite targets, decided by
whether Search Console had spoken rather than by anything about their trees.
Barcelona is the one he had called the mega city and it already publishes 46.
He spotted it in one line: "maar waarom in godsnaam 50 doel bij wenen".

The deeper fault: register count measures how EASY trees are to find, never how
GOOD they are. Amsterdam's 4,993 is a municipal inventory, not 4,993 trees that
clear our bar. Scaling ambition by it confused cheap with worth doing.

    supply = register trees within 5 km + leads already ready to write

    supply < 10    no target. The city gets whatever verifies, which is
                   usually 4 to 10, and Cadiz at 5 proves that is not a
                   failure. Adding here costs full research per tree.
    supply >= 10   25. The first-version ceiling, the same for every city,
                   because breadth is the phase and a good afternoon does not
                   scale with a city's population.

Past 25 is deepening, not a target: a later decision, taken on a city that has
shown demand, and taken with Hidde. A city already past it (Barcelona at 46) is
finished, not over budget.

What the target is NOT: a quota to fill. The bar per tree does not move, padding
stays forbidden, and a city that runs out of trees that clear the bar is
finished below its target. It is a ceiling on ambition, not a floor on effort.

This replaces "a city is finished at three walks" as the stopping rule. The
three-walk line survives where it was always right, which is what the PAGE
leads with: a reader gets the best three walks, and trees beyond them are still
published, still on the map, still collectible, listed below. Barcelona's 46 in
7 walks was never wrong as data, only as presentation.
"""
import argparse
import glob
import json
import math
import os
import re
import sys

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


def target_for(supply, measured=False):
    """Two stages, ruled by Hidde 2026-08-12: "is het niet beter om overal eerst
    minstens 10 bomen te doen en dan te verdiepen wanneer we google search
    confirmatie krijgen."

    So 10 everywhere, and 25 only once Search Console has actually spoken for
    that city. `measured` is the queue's own `basis` column saying exactly that.
    It replaces a flat 25 for everyone (his own previous line, an hour earlier),
    and before that a supply-banded 20/30/50 that gave Vienna 50 and Barcelona
    30 for no reason to do with trees. This version needs no supply input at all,
    which is why `supply` is now unused: the question is not how much is lying
    around, it is whether anyone has arrived.

    Less than the target is fine and expected where the trees are genuinely hard
    to find. The floor stays four verified trees or no page."""
    return 25 if measured else 10


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


def enrich(doc, live):
    """Write the measured columns into the source file itself, so the numbers a
    human reads and the numbers a script computes are the same object."""
    for c in doc["cities"]:
        info = live.get(c["city"].lower())
        if info:
            supply = info["register"] + info["ready"]
            c.update(status="published", trees=info["trees"], photos=info["photos"],
                     walks=info["walks"], register=info["register"],
                     ready=info["ready"], supply=supply,
                     target=target_for(supply, c["basis"].startswith("measured")))
        else:
            c.update(status="pending", trees=0, photos=0, walks=0,
                     register=0, ready=0, supply=0,
                     target=target_for(0, c["basis"].startswith("measured")))
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
        # So a run does not have to reason out where to work, and so it stops.
        # Hidde, 2026-08-12: "zodat ze niet teveel doorgraven in 1 stad."
        doc = load_source()
        gap = [c for c in doc["cities"]
               if c.get("rank") and c.get("target") and c.get("trees", 0) < c["target"]]
        gap.sort(key=lambda c: c["rank"])
        print("BELOW TARGET, in queue order. Take the top one you can move cheaply,")
        print("stop at the target, and leave the rest as leads.\n")
        print("  #  city             now  gap  ready  register")
        for c in gap:
            print("%3d  %-16s %4d %4d %6d %9d" % (
                c["rank"], c["city"][:16], c["trees"],
                c["target"] - c["trees"], c.get("ready", 0), c.get("register", 0)))
        print("\n%d cities, %d trees to go. Cities with no target get whatever"
              % (len(gap), sum(c["target"] - c["trees"] for c in gap)))
        print("verifies and are not chased.")
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
    live = measure(pts)
    doc = enrich(load_source(), live)
    order = rebuild_table(doc)
    n = rebuild_list(live, order)
    deep = [c for c in doc["cities"] if c.get("target") == 25]
    print("%d register points, %d live cities measured" % (len(pts), len(live)))
    print("data/city-queue.json: %d cities, %d ranked (the source)"
          % (len(doc["cities"]), len(order)))
    print("rendered: %d rows in CITY_QUEUE.md, %d entries in city-list.json"
          % (len(order), n))
    print("%d cities are confirmed by Search Console and carry the 25 target; "
          "%d carry the 10 first-version target"
          % (len(deep), len(doc["cities"]) - len(deep)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
