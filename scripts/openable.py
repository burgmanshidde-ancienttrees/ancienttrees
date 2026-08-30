"""Which zero-tree cities can ACTUALLY be opened today, and with what.

Written 2026-08-30, because `city_queue.py --next`'s "OPENABLE TODAY" counts
sent three windows at cities with no usable supply in a single day. The counts
were not wrong so much as credulous: they ask how many candidate trees sit near
a city's coordinate, and near is not the same question as belongs to.

Three ways that goes wrong, each of which cost a real window:

  Girona was listed with 11 Wikidata candidates and released twice on 08-29,
  both times after a hand-check found 4. The count uses a bounding BOX where
  the check used a radius, and a box is 27 percent larger at its corners.

  Mechelen was listed with 214 register trees. Every one of them is in the
  Brussels remarkable-trees register, most of them in Brussels itself, which
  has had its own page since July. Pisa's 32 are Lucca's, 20 km up the road.
  Supply that belongs to a city we already publish is not supply, it is that
  city's trees seen from the neighbouring town.

  Bruges was listed with 56, all of them in the Dutch national register, over
  the border. Within 20 km and in another country.

So this asks a stricter question than city_queue does, and prints its working
rather than a number: a candidate counts for a city only if that city is the
NEAREST published-or-ranked place to it, it is not already on our map, and it
is in the same country. The output is a shortlist a run can dispatch from
without re-deriving any of it.

    python3 scripts/openable.py            # the shortlist
    python3 scripts/openable.py --city X   # everything held for one city
"""
import argparse
import glob
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from city_queue import register_rows  # noqa: E402

R = 6371.0
# Six is the assembly line's own floor: below it a pass costs more in fixed
# overhead than the trees are worth (CLAUDE.md, "No pass under six expected
# candidates").
FLOOR = 6
WD_KM = 15.0
REG_KM = 20.0


def path(*p):
    return os.path.join(ROOT, *p)


def hav(a, b, c, d):
    p = math.radians
    return 2 * R * math.asin(math.sqrt(
        math.sin(p(c - a) / 2) ** 2
        + math.cos(p(a)) * math.cos(p(c)) * math.sin(p(d - b) / 2) ** 2))


def load_places():
    """Every place a candidate could belong to: published cities and ranked ones.

    Published cities are located from their own trees, which is the one
    coordinate we know is right. Ranked-but-unopened cities come from the
    coordinate cache city_queue.py already keeps.
    """
    coords = json.load(open(path("data", "city-coords.json"), encoding="utf-8"))
    queue = json.load(open(path("data", "city-queue.json"), encoding="utf-8"))["cities"]

    published, ours = {}, []
    for f in glob.glob(path("data", "cities", "*.json")):
        d = json.load(open(f, encoding="utf-8"))
        pts = [(t["location"]["latitude"], t["location"]["longitude"])
               for t in d.get("trees", [])
               if (t.get("location") or {}).get("latitude") is not None]
        if not pts:
            continue
        ours.extend(pts)
        published[d["city"]] = (sum(p[0] for p in pts) / len(pts),
                                sum(p[1] for p in pts) / len(pts),
                                d.get("country", ""))

    zero = []
    for c in queue:
        if not c.get("rank") or (c.get("trees") or 0):
            continue
        p = coords.get(c["city"]) or coords.get(c["slug"])
        if not p:
            continue
        zero.append((c["rank"], c["city"], c["country"], p[0], p[1]))
    return published, ours, zero


def mapped(ours, lat, lng):
    return any(abs(a - lat) < 0.0008 and abs(b - lng) < 0.0008 for a, b in ours)


def known_countries():
    """Every country name the corpus uses, for reading one off a filename.

    A register file is supposed to carry a `country` field and several do not:
    netherlands-lrmb.json is the one that matters, because its trees sit within
    20 km of Bruges and would otherwise be counted as Belgian supply. The
    filename says Netherlands and nothing else does, so read it there rather
    than leave the check off for the one file it was written for.
    """
    out = set()
    q = json.load(open(path("data", "city-queue.json"), encoding="utf-8"))["cities"]
    for c in q:
        if c.get("country"):
            out.add(c["country"])
    for f in glob.glob(path("data", "cities", "*.json")):
        try:
            out.add(json.load(open(f, encoding="utf-8")).get("country", ""))
        except Exception:
            pass
    return {c.lower().replace(" ", "-"): c for c in out if c}


def country_of(d, filename, names):
    if isinstance(d, dict) and d.get("country"):
        return d["country"]
    stem = os.path.basename(filename)[:-5].lower()
    parts = stem.split("-")
    for n in range(len(parts), 0, -1):
        hit = names.get("-".join(parts[:n]))
        if hit:
            return hit
    return ""


def candidates():
    """(lat, lng, label, species, country, source) for everything on hand."""
    names = known_countries()
    out = []
    wd = json.load(open(path("data", "research", "wikidata-remarkable-trees.json"),
                        encoding="utf-8"))
    for t in wd["trees"]:
        if t.get("latitude") is None:
            continue
        out.append((t["latitude"], t["longitude"], t.get("name") or "(unnamed)",
                    t.get("species") or "", t.get("country") or "", "wikidata"))
    for f in glob.glob(path("data", "registers", "*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        name = os.path.basename(f)
        country = country_of(d, f, names)
        for r in register_rows(d):
            if not isinstance(r, dict):
                continue
            lat = r.get("latitude", r.get("lat"))
            lng = r.get("longitude", r.get("lng"))
            if lat is None or lng is None:
                continue
            try:
                lat, lng = float(lat), float(lng)
            except (TypeError, ValueError):
                continue
            label = (r.get("name") or r.get("name_it") or r.get("common_name")
                     or r.get("locality") or "(unnamed)")
            species = (r.get("species") or r.get("species_latin") or "")
            out.append((lat, lng, str(label), str(species), country, name))
    return out


def collect(city, lat, lng, country, cands, published, ours):
    """What genuinely belongs to this city, and what was rejected and why."""
    keep, drop = [], {"mapped": 0, "nearer another city": 0, "another country": 0}
    for clat, clng, label, species, ccountry, src in cands:
        km = REG_KM if src != "wikidata" else WD_KM
        if abs(clat - lat) > km / 111.0:
            continue
        d = hav(lat, lng, clat, clng)
        if d > km:
            continue
        if mapped(ours, clat, clng):
            drop["mapped"] += 1
            continue
        if ccountry and country and ccountry.lower() != country.lower():
            drop["another country"] += 1
            continue
        nearer = [n for n, (a, b, _) in published.items()
                  if hav(a, b, clat, clng) < d]
        if nearer:
            drop["nearer another city"] += 1
            continue
        keep.append((round(d, 1), label, species, src))
    keep.sort()
    return keep, drop


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city")
    ap.add_argument("--floor", type=int, default=FLOOR)
    args = ap.parse_args()

    published, ours, zero = load_places()
    cands = candidates()

    if args.city:
        zero = [z for z in zero if z[1].lower() == args.city.lower()]
        if not zero:
            print(f"{args.city} is not a ranked city standing at zero trees.")
            return 1

    rows = []
    for rank, city, country, lat, lng in zero:
        keep, drop = collect(city, lat, lng, country, cands, published, ours)
        if args.city or len(keep) >= args.floor:
            rows.append((rank, city, country, keep, drop))
    rows.sort()

    if not args.city:
        print(f"OPENABLE: ranked cities at zero holding {args.floor}+ candidates that")
        print("are ours to take. A candidate nearer a city we already publish is that")
        print("city's tree, not this one's, and is not counted here.\n")
        print(f"{'rank':>5}  {'city':<22} {'country':<16} {'cands':>5}  sources")
    for rank, city, country, keep, drop in rows:
        srcs = sorted({k[3] for k in keep})
        print(f"{rank:>5}  {city:<22} {country:<16} {len(keep):>5}  {', '.join(srcs)}")
        if args.city:
            lat, lng = [(a, b) for r, c, co, a, b in zero if c == city][0]
            near = sorted(((hav(lat, lng, a, b), n)
                           for n, (a, b, _) in published.items()), key=lambda x: x[0])[:2]
            # A published city a short walk away is not a reason to stop, but it
            # is the question to answer first: these trees may belong on ITS page
            # rather than on a new one. Funchal is the standing example, 12
            # unmapped candidates sitting beside a published Madeira.
            print("\n   nearest published: "
                  + ", ".join(f"{n} {d:.0f} km" for d, n in near))
            print()
            for d, label, species, src in keep:
                print(f"   {d:>5.1f} km  {label[:46]:<46} {species[:30]:<30} {src}")
            print("\n   not counted: " + ", ".join(f"{v} {k}" for k, v in drop.items() if v))
    if not args.city:
        print(f"\n{len(rows)} of {len(zero)} zero-tree ranked cities are openable today.")
        print("Read one with: python3 scripts/openable.py --city <name>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
