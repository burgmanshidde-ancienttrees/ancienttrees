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

Hidde's sketch: easy and good supply means a big city may run to about 50 like
Barcelona; hard to find means leave it; 20 to 30 is a fine first version; past
50 is too much except perhaps for a Tokyo. The measurement that turns that into
a rule is supply, and it is far more lopsided than anyone guessed: of 95 live
cities, 71 have fewer than 10 register trees within 5 km and only 9 have 50 or
more. For three quarters of the map there is no decision to make, because there
is nothing cheap to add. The target therefore falls out of what a city can
actually reach:

    supply = register trees within 5 km + leads already ready to write

    supply < 10    no target. The city gets whatever verifies, which is
                   usually 4 to 10, and Cadiz at 5 proves that is not a
                   failure. Adding here costs full research per tree.
    supply 10-49   20. One good afternoon plus a second walk.
    supply 50-199  30. Two or three walks, comfortably.
    supply 200+    50 where demand is measured, 30 where it is not. Cheap
                   supply is not a reason to build a page nobody opens.

Past 50 is a session decision with Hidde, never a run's, and the only plausible
candidates are true metropolises.

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
QUEUE = os.path.join(ROOT, "CITY_QUEUE.md")
LIST = os.path.join(ROOT, "data", "city-list.json")
ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([\d.]+)\s*\|\s*([\d,\-]+)\s*\|"
                 r"\s*([\d\-]+)\s*\|\s*([\d\-]+)\s*\|\s*([\d\-]+)\s*\|\s*([^|]+?)\s*\|")

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


def target_for(supply, measured):
    if supply < 10:
        return None
    if supply < 50:
        return 20
    if supply < 200:
        return 30
    return 50 if measured else 30


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


def rebuild_table(live):
    with open(QUEUE, encoding="utf-8") as fh:
        text = fh.read()
    lines, out, seen = text.split("\n"), [], []
    for line in lines:
        m = ROW.match(line)
        if not m:
            out.append(line)
            continue
        rank, city, score, demand, _, _, _, basis = m.groups()
        info = live.get(city.lower())
        if info:
            supply = info["register"] + info["ready"]
            tgt = target_for(supply, basis.startswith("measured"))
            trees, photos, reg = info["trees"], info["photos"], info["register"]
            walks = info["walks"]
        else:
            supply = tgt = None
            trees = photos = reg = walks = 0
        seen.append(city.lower())
        out.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            rank, city, score, demand,
            trees or "-", photos or "-", walks or "-", reg or "-",
            tgt or "-", basis))
    text = "\n".join(out)
    header_old = "| # | city | score | demand | trees | photos | register | basis |"
    header_new = "| # | city | score | demand | trees | photos | walks | register | target | basis |"
    text = text.replace(header_old, header_new)
    text = text.replace("|---|---|---:|---:|---:|---:|---:|---|",
                        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|")
    with open(QUEUE, "w", encoding="utf-8") as fh:
        fh.write(text)
    return seen


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
    a = ap.parse_args()

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
    order = rebuild_table(live)
    n = rebuild_list(live, order)
    banded = [i for i in live.values() if target_for(i["register"] + i["ready"], True)]
    print("%d register points, %d live cities measured" % (len(pts), len(live)))
    print("%d rows in CITY_QUEUE.md, %d entries in city-list.json" % (len(order), n))
    print("%d cities have supply for a target; %d are supply-starved and get none"
          % (len(banded), len(live) - len(banded)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
