#!/usr/bin/env python3
"""The one database: every tree this project knows about, in one file.

Hidde, 2026-08-04: "whenever you find trees' information, you should just add
it to our larger database... we shouldn't just make separate city pages. In
the end we should have a world database, then a country database, then a city
database."

Three things were being kept in three shapes and never seen together:

  data/cities/*.json     highlighted trees, the ones with a story and a page
  data/leads/*.json      what research found and did not ship, in two kinds
  data/registers/*.json  official designations, bought cheaply from the state

This unions them into data/tree-index.json, keyed by a stable id, with a
`tier` saying what each record is. Nothing moves: the three sources stay
where they are and stay authoritative. This is the view over them, rebuilt
from scratch every time, so it can never drift out of date.

    python3 scripts/tree_index.py            write the index and print the count
    python3 scripts/tree_index.py --summary  just the numbers, write nothing

Tiers, and what each one means:

  highlighted  a full entry: verified against two sources, story, honest pin.
               This is the product. Expensive, roughly 20k tokens each.
  known        an official register record: species, size, location, no story.
               Cheap, near zero per tree. The layer that makes routes possible.
  lead         found during research, did not make the page: undated, single
               sourced, no photo, or simply ninth in line. The pool a city
               grows from.
  blocked      must never ship: gone, private, access restricted, location
               withheld, or not a collectible point. Kept so nobody
               re-researches their way to the same no.
"""
import argparse
import glob
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "tree-index.json")


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s or "unknown"


def from_cities():
    for f in sorted(glob.glob(os.path.join(DATA, "cities", "*.json"))):
        d = json.load(open(f))
        city, country = d.get("city", ""), d.get("country", "")
        for t in d.get("trees", []):
            loc = t.get("location") or {}
            ph = t.get("photo") or {}
            yield {
                "id": t.get("id"),
                "tier": "highlighted",
                "name": t.get("name"),
                "species": t.get("species", ""),
                "city": city, "country": country,
                "lat": loc.get("latitude"), "lng": loc.get("longitude"),
                "precision": t.get("location_precision"),
                "age_min": t.get("age_min"), "age_max": t.get("age_max"),
                "has_photo": bool(ph.get("url") and ph.get("status") == "approved"),
                "has_story": bool(t.get("story")),
                "sources": len(t.get("verified_sources") or []),
            }


def from_leads():
    for f in sorted(glob.glob(os.path.join(DATA, "leads", "*.json"))):
        d = json.load(open(f))
        city, country = d.get("city", ""), d.get("country", "")
        for n, t in enumerate(d.get("leads", []), 1):
            yield {
                "id": f"lead_{slugify(city)}_{n:03d}",
                "tier": "blocked" if t.get("status") == "blocked" else "lead",
                "name": t.get("name"),
                "species": t.get("species", ""),
                "city": city, "country": country,
                "lat": t.get("lat"), "lng": t.get("lng"),
                "precision": None,
                "reason": t.get("blocked_reason") or "",
                "note": (t.get("why") or "")[:400],
                "has_photo": False, "has_story": False, "sources": 0,
            }


def from_registers():
    for f in sorted(glob.glob(os.path.join(DATA, "registers", "*.json"))):
        d = json.load(open(f))
        rows = d.get("entries") or d.get("trees") or []
        src = d.get("source", os.path.basename(f))
        country = d.get("country") or ("Portugal" if "portugal" in f
                                       else "Japan" if "tokyo" in f or "japan" in f
                                       else "")
        for n, t in enumerate(rows, 1):
            loc = t.get("location") or {}
            yield {
                "id": f"reg_{slugify(os.path.basename(f)[:-5])}_{n:04d}",
                "tier": "known",
                "name": (t.get("name") or t.get("name_pt") or t.get("name_it")
                         or t.get("species") or ""),
                "species": t.get("species", ""),
                "city": t.get("city") or t.get("concelho") or t.get("comune") or "",
                "country": country,
                "lat": t.get("latitude") or loc.get("latitude"),
                "lng": t.get("longitude") or loc.get("longitude"),
                "precision": "approximate",
                "register": src,
                "girth_cm": t.get("girth_cm"), "height_m": t.get("height_m"),
                "has_photo": False, "has_story": False, "sources": 1,
            }


def build():
    rows = list(from_cities()) + list(from_registers()) + list(from_leads())
    # A register record that names a tree we already highlight is the same
    # tree twice; drop it from the known layer rather than double count.
    highlighted = {(r["name"] or "").lower().strip()
                   for r in rows if r["tier"] == "highlighted"}
    out, dropped = [], 0
    for r in rows:
        if r["tier"] == "known" and (r["name"] or "").lower().strip() in highlighted:
            dropped += 1
            continue
        out.append(r)
    return out, dropped


def summarise(rows):
    tiers = Counter(r["tier"] for r in rows)
    with_coords = sum(1 for r in rows if r.get("lat") and r.get("lng"))
    countries = Counter(r["country"] for r in rows if r["country"])
    print(f"  {len(rows)} trees in the database, {with_coords} with coordinates")
    for t in ("highlighted", "known", "lead", "blocked"):
        if tiers[t]:
            print(f"    {tiers[t]:5d}  {t}")
    print("\n  by country (top 8):")
    for c, n in countries.most_common(8):
        per = Counter(r["tier"] for r in rows if r["country"] == c)
        bits = ", ".join(f"{per[t]} {t}" for t in ("highlighted", "known", "lead") if per[t])
        print(f"    {n:5d}  {c:<16} {bits}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", action="store_true", help="print only, write nothing")
    args = ap.parse_args()
    rows, dropped = build()
    summarise(rows)
    if dropped:
        print(f"\n  {dropped} register records dropped as duplicates of highlighted trees")
    if not args.summary:
        json.dump({"generated_from": ["data/cities", "data/registers", "data/leads"],
                   "count": len(rows), "trees": rows},
                  open(OUT, "w"), indent=1, ensure_ascii=False)
        print(f"\n  written to {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
