#!/usr/bin/env python3
"""Which of the world's best-known parks do we map, and which are free wins?

Hidde, 2026-09-18: "Ik denk dat er nog wel heel veel te winnen is qua parken.
Om beroemde parken waar veel op gezocht wordt bij Google om die toe te voegen.
[...] Deze hoeft dus niet per se in een grote stad te liggen. [...] ik wil
gewoon zoekvolume winnen."

He is right that a park is a search term in a way a city page is not, and the
evidence is Google's own: Park Guell was the most searched park on Google Maps
in 2023 and Central Park in 2024, and three of that 2023 top ten are places we
already publish trees in. A park page (Contract H) needs no new trees at all
when five are already mapped inside it, which makes this the cheapest supply on
the ladder after a translation.

Two halves, and only the first needs the network:

  COVERAGE, computed from our own files. For each park it counts the trees we
  publish inside its radius, whether the site can GROUP them (which is a text
  question, not a tree question: parkKey() reads the address, so five trees in
  Hyde Park that never say "Hyde Park" cannot become a page), whether an intro
  exists, and what supply is sitting nearby in leads and registers.

  DEMAND, measured with --views: English Wikipedia pageviews for the park's own
  article, the same proxy demand.py uses for cities, cached so the ranking is
  free afterwards. Read it as order, never as search volume: it says which
  parks are in more people's heads.

This is NOT a queue and must not become one. CITY_QUEUE.md is the single city
list and the single order, and it says outright not to re-derive one anywhere
else, after six prioritisations were found running at once. What this ranks is
PARKS, almost all of them inside cities that are already published, so the work
it points at is a page the trees have already earned or a handful of trees
inside a city the queue has already opened. When it names a park in a city we
do not publish, that city's turn is still CITY_QUEUE.md's to give.

Matching is by DISTANCE, never by name, per CLAUDE.md: a park page is found by
asking whether any of the site's own park groups has its trees inside this
park's radius, which no spelling can fool. That is how Villa Borghese, the
Retiro and Nara Park were recognised as already written rather than reported as
missing.

    python3 scripts/park_demand.py                 # the coverage table
    python3 scripts/park_demand.py --next 15       # the batch to work next
    python3 scripts/park_demand.py --gaps          # famous parks we map nothing in
    python3 scripts/park_demand.py --views         # fill the demand cache (network)
    python3 scripts/park_demand.py --coords        # refresh coordinates (network)
    python3 scripts/park_demand.py --check         # exit 1 if a page is sitting free
"""
import argparse
import datetime
import glob
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geo
from pagegaps import park_name_of

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = os.path.join(ROOT, "data", "famous-parks.json")
CACHE = os.path.join(ROOT, "data", "park-demand.json")
SCOUTING = os.path.join(ROOT, "data", "register-scouting.json")
PARK_MIN_TREES = 5          # mirrors site/src/lib/parks.ts
NEAR_CITY_KM = 30.0         # the day-trip boundary CLAUDE.md already uses
UA = {"User-Agent": "AncientTrees/1.0 (ancienttrees.app; tree research)"}
VIEWS_API = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
             "en.wikipedia/all-access/user/%s/monthly/%s/%s")
GEO_API = "https://en.wikipedia.org/w/api.php"
PAUSE = 0.6                 # the pageviews API starts refusing a burst


# ---------------------------------------------------------------- reading ---

def load_seed():
    with open(SEED, encoding="utf-8") as fh:
        return json.load(fh)


def out_of_focus_countries():
    """The regions Hidde ruled out of focus, read from the one file that holds
    them. Never copied here: reversing that decision means deleting a line in
    data/register-scouting.json, and a second list would outlive it."""
    try:
        with open(SCOUTING, encoding="utf-8") as fh:
            oof = json.load(fh).get("out_of_focus") or {}
    except (OSError, ValueError):
        return set()
    return set(oof.get("countries") or []) | set(oof.get("africa_countries") or [])


def cities():
    """Published places, each with its trees that carry a coordinate."""
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        try:
            with open(path, encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError):
            continue
        slug = os.path.basename(path)[:-5]
        trees = []
        for t in d.get("trees") or []:
            loc = t.get("location") or {}
            lat, lng = loc.get("latitude"), loc.get("longitude")
            if isinstance(lat, (int, float)) and isinstance(lng, (int, float)):
                trees.append((t, float(lat), float(lng)))
        out.append({"slug": slug, "city": d.get("city") or slug,
                    "country": d.get("country") or "", "trees": trees,
                    "all_trees": len(d.get("trees") or [])})
    return out


def written_parks():
    """(city_slug, lowercased park name) -> the intro file's slug. The key the
    site itself uses; see pagegaps.written_parks() for why a reconstructed slug
    is the wrong thing to match on."""
    out = {}
    for path in glob.glob(os.path.join(ROOT, "data", "parks", "*.json")):
        try:
            with open(path, encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError):
            continue
        if d.get("city_slug") and d.get("park"):
            out[(d["city_slug"], d["park"].strip().lower())] = (
                d.get("slug") or os.path.basename(path)[:-5])
    return out


def park_groups(places):
    """The site's own park groups: (city_slug, park name) -> trees, plus the
    centroid, which is what lets a group be recognised by position."""
    groups = {}
    for place in places:
        for tree, lat, lng in place["trees"]:
            name = park_name_of(tree)
            if not name:
                continue
            g = groups.setdefault((place["slug"], name),
                                  {"city": place["city"], "pts": [], "trees": []})
            g["pts"].append((lat, lng))
            g["trees"].append(tree)
    for g in groups.values():
        g["centroid"] = (sum(p[0] for p in g["pts"]) / len(g["pts"]),
                         sum(p[1] for p in g["pts"]) / len(g["pts"]))
    return groups


def _coord(row):
    for a, b in (("lat", "lng"), ("latitude", "longitude"), ("lat", "lon")):
        x, y = row.get(a), row.get(b)
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            return float(x), float(y)
    return None


def supply():
    """Every lead and register row that carries a coordinate, as flat points.

    Leads and registers are what make a park cheap to open: a register row with
    a species and a coordinate costs ~0.4k tokens per tree against ~19k for
    research from zero (CLAUDE.md, the measured week of 2026-08-04). Blocked
    leads are left out on purpose: they must never ship whatever happens later.
    """
    leads, regs = [], []
    for path in glob.glob(os.path.join(ROOT, "data", "leads", "*.json")):
        try:
            with open(path, encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError):
            continue
        for row in (d.get("leads") or []) if isinstance(d, dict) else []:
            c = _coord(row)
            if c:
                leads.append(c)
    for path in glob.glob(os.path.join(ROOT, "data", "registers", "*.json")):
        try:
            with open(path, encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError):
            continue
        rows = d.get("trees") if isinstance(d, dict) else d
        for row in rows or []:
            if not isinstance(row, dict):
                continue
            c = _coord(row)
            if c:
                regs.append(c)
    return leads, regs


def load_cache():
    try:
        with open(CACHE, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {"note": "Wikipedia pageviews per park, filled by "
                        "scripts/park_demand.py --views. Demand, not search volume.",
                "views": {}}


# --------------------------------------------------------------- crossing ---

def assess(seed, places, groups, intros, leads, regs, skip_countries):
    rows = []
    for p in seed["parks"]:
        here = (p["lat"], p["lng"])
        radius = float(p.get("radius_km") or 1.2)
        inside = []
        for place in places:
            for tree, lat, lng in place["trees"]:
                if geo.km(here, (lat, lng)) <= radius:
                    inside.append((place, tree))
        # The site's own group for this park, found by position. A group whose
        # trees sit inside the radius IS this park however either spells it.
        page, grouped, group_name = None, 0, None
        for (slug, name), g in groups.items():
            if geo.km(here, g["centroid"]) <= radius:
                if len(g["trees"]) > grouped:
                    grouped, group_name = len(g["trees"]), name
                    page = intros.get((slug, name.strip().lower()))
        nearest, nearest_km = None, None
        for place in places:
            for _t, lat, lng in place["trees"]:
                d = geo.km(here, (lat, lng))
                if nearest_km is None or d < nearest_km:
                    nearest, nearest_km = place, d
        rows.append({
            "park": p["name"], "city": p["city"], "country": p["country"],
            "evidence": p.get("evidence", ""), "wikipedia": p.get("wikipedia"),
            "radius_km": radius,
            "trees": len(inside),
            "grouped": grouped, "group_name": group_name, "page": page,
            "nearest": nearest["city"] if nearest else None,
            "nearest_km": nearest_km,
            "city_live": bool(nearest_km is not None and nearest_km <= NEAR_CITY_KM),
            "leads": sum(1 for c in leads if geo.km(here, c) <= radius),
            "register": sum(1 for c in regs if geo.km(here, c) <= radius),
            "out_of_focus": p["country"] in skip_countries,
        })
    return rows


def verdict(r):
    """One word for what this park needs next, in the order the work is cheap.

    The distinction that matters, and the one no other script here can see: a
    park with five groupable trees and a page is DONE, a park with five
    groupable trees and no intro is a page nobody has written, and a park with
    five trees NEAR it that the site cannot group is a question rather than a
    win. "check" is deliberately not called "regroup": a radius catches the
    streets around a city-centre park as well as the park, so whether those
    trees stand in it is answered by --park and by nothing else.
    """
    if r["out_of_focus"]:
        return "out of focus"
    if r["page"] and r["grouped"] >= PARK_MIN_TREES:
        return "page"
    if r["page"]:
        # Contract H needs five trees AND an intro, so an intro on a group of
        # four is prose nobody can read: the page does not render at all. This
        # said "page" until Nara Park was checked against the built site, which
        # is the one number in this tool worth disbelieving, because an intro
        # file existing looks exactly like a page from the data side. It is also
        # the cheapest work on the whole list, one verified tree for a page.
        return "one short"
    if r["grouped"] >= PARK_MIN_TREES:
        return "intro"                      # groupable, gate cleared, no page
    if r["trees"] >= PARK_MIN_TREES:
        return "check"                      # enough trees NEAR it; --park says which
    if r["trees"]:
        return "thin %d" % r["trees"]       # some trees, below the gate
    if r["leads"] or r["register"]:
        return "supply"                     # nothing published, material on hand
    if r["city_live"]:
        return "empty"                      # we publish nearby, park has nothing
    return "no coverage"


ORDER = {"one short": 0, "intro": 1, "check": 2, "supply": 3, "thin": 4,
         "empty": 5, "no coverage": 6, "page": 7, "out of focus": 8}


def rank(r, views):
    """Cheapest first, and inside a tier the one closest to shipping.

    grouped comes before trees on purpose: a park with four groupable trees is
    one tree from a page, while a park with four trees the site cannot group is
    a park with an address problem and an unknown amount of work behind it.
    """
    v = verdict(r)
    key = v.split()[0] if v.startswith("thin") else v
    seen = views.get(r["wikipedia"] or r["park"])
    return (ORDER.get(key, 9), -(seen or 0), -r["grouped"], -r["trees"], r["park"])


# ---------------------------------------------------------------- network ---

def fetch(url, tries=4):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as fh:
                return json.load(fh)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code != 429 or attempt == tries - 1:
                raise
            time.sleep(2 ** attempt)
        except (urllib.error.URLError, OSError):
            if attempt == tries - 1:
                raise
            time.sleep(2 ** attempt)
    return None


def fill_views(seed, cache):
    """Monthly pageviews over the last full three months, summed.

    A 429 is indistinguishable from an article nobody reads unless it is
    caught, which is how famous_demand.py once reported the Major Oak as read
    by nobody. fetch() catches it; a failure here is printed, never silently
    stored as zero.
    """
    end = datetime.date.today().replace(day=1)
    start = end - datetime.timedelta(days=95)
    a, b = start.strftime("%Y%m0100"), end.strftime("%Y%m0100")
    views = cache.setdefault("views", {})
    for p in seed["parks"]:
        title = p.get("wikipedia") or p["name"]
        if title in views:
            continue
        url = VIEWS_API % (urllib.parse.quote(title.replace(" ", "_"), safe=""), a, b)
        try:
            d = fetch(url)
        except Exception as exc:                       # noqa: BLE001
            print("  ! %s: %s" % (title, exc))
            continue
        if not d or not d.get("items"):
            print("  ? %s: no data (check the article title)" % title)
            continue
        views[title] = sum(i.get("views", 0) for i in d["items"])
        print("  %-46s %8d" % (title, views[title]))
        time.sleep(PAUSE)
    cache["views_window"] = "%s to %s, monthly, summed" % (a[:6], b[:6])
    cache["updated"] = datetime.date.today().isoformat()
    with open(CACHE, "w", encoding="utf-8") as fh:
        json.dump(cache, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return cache


def fill_coords(seed):
    """Replace the hand-written centroids with Wikipedia's own coordinates.

    The seed was written on a machine whose network policy blocks every
    Wikimedia host, so every coordinate in it is knowledge rather than a fetch.
    This prints what moved and by how far, because a park that jumps kilometres
    is a wrong article rather than a better coordinate.
    """
    moved = 0
    for p in seed["parks"]:
        title = p.get("wikipedia") or p["name"]
        url = GEO_API + "?" + urllib.parse.urlencode({
            "action": "query", "prop": "coordinates", "titles": title,
            "format": "json", "formatversion": "2"})
        try:
            d = fetch(url)
        except Exception as exc:                       # noqa: BLE001
            print("  ! %s: %s" % (title, exc))
            continue
        pages = ((d or {}).get("query") or {}).get("pages") or []
        coords = (pages[0].get("coordinates") if pages else None) or []
        if not coords:
            print("  ? %s: no coordinate on the article" % title)
            continue
        lat, lng = float(coords[0]["lat"]), float(coords[0]["lon"])
        d_km = geo.km((p["lat"], p["lng"]), (lat, lng))
        if d_km > 0.05:
            print("  %-42s moved %5.2f km" % (p["name"], d_km))
            moved += 1
        p["lat"], p["lng"], p["coord_source"] = round(lat, 5), round(lng, 5), "wikipedia"
        time.sleep(PAUSE)
    seed["updated"] = datetime.date.today().isoformat()
    with open(SEED, "w", encoding="utf-8") as fh:
        json.dump(seed, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("\n%d of %d coordinates moved more than 50 m." % (moved, len(seed["parks"])))


# ------------------------------------------------------------------ output ---

def table(rows, views, limit=None):
    print("%-34s %-16s %5s %5s %4s %4s  %-11s %s" % (
        "PARK", "CITY", "VIEWS", "TREES", "GRP", "SUP", "NEEDS", "NEAREST OF OURS"))
    for r in rows[:limit]:
        seen = views.get(r["wikipedia"] or r["park"])
        near = "-"
        if r["nearest"]:
            near = "%s %.0f km" % (r["nearest"], r["nearest_km"])
        print("%-34s %-16s %5s %5d %4d %4d  %-11s %s" % (
            r["park"][:34], r["city"][:16],
            ("%.0fk" % (seen / 1000.0)) if seen else "-",
            r["trees"], r["grouped"], r["leads"] + r["register"],
            verdict(r), near))


def detail(seed, places, name):
    """Every tree inside one park's radius, with what its address actually says.

    This is the column the table cannot carry and the only way to judge a
    "check" verdict, because a radius around a city-centre park catches the
    streets around it too. Krakow's Planty is the worked example: nineteen of
    our trees sit within 1.2 km of its centre and it is a ring around the old
    town, so most of them stand in the town rather than in the park. The
    question a table cannot answer is which, and the address head answers it.
    """
    hits = [p for p in seed["parks"] if name.lower() in p["name"].lower()]
    if not hits:
        print("No park matching %r in data/famous-parks.json." % name)
        return 1
    for p in hits:
        here, radius = (p["lat"], p["lng"]), float(p.get("radius_km") or 1.2)
        print("%s, %s (%s)  radius %.1f km" % (p["name"], p["city"], p["country"], radius))
        print("  %s\n" % p.get("evidence", ""))
        rows = []
        for place in places:
            for tree, lat, lng in place["trees"]:
                d = geo.km(here, (lat, lng))
                if d <= radius:
                    rows.append((d, place["city"], tree))
        for d, city, tree in sorted(rows):
            loc = tree.get("location") or {}
            print("  %4.0f m  %-34s %-22s %s" % (
                d * 1000, (tree.get("name") or "")[:34],
                (park_name_of(tree) or "-")[:22],
                (loc.get("address") or "")[:46]))
        # Per group, not a single total: Florence is the reason. Six of our
        # trees sit within 800 m of the Boboli centre and five carry a park
        # name, which reads like a page until you see that they are two
        # different gardens, the Boboli and the Bobolino, three and two. The
        # gate is per park, so a total answers the wrong question.
        by = {}
        for _d, _c, t in rows:
            by[park_name_of(t) or "(no park in the address)"] = by.get(
                park_name_of(t) or "(no park in the address)", 0) + 1
        print("\n  %d trees inside the radius. The site groups them as:" % len(rows))
        for name, n in sorted(by.items(), key=lambda kv: -kv[1]):
            flag = "  <- clears the %d-tree gate" % PARK_MIN_TREES if n >= PARK_MIN_TREES else ""
            print("    %2d  %s%s" % (n, name, flag))
        print()
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--park", metavar="NAME",
                    help="every tree inside one park's radius, to judge it")
    ap.add_argument("--next", type=int, metavar="N",
                    help="the N cheapest wins, work top down")
    ap.add_argument("--gaps", action="store_true",
                    help="famous parks where we map nothing at all")
    ap.add_argument("--views", action="store_true", help="fill the demand cache (network)")
    ap.add_argument("--coords", action="store_true", help="refresh coordinates (network)")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 when a park page is sitting free")
    args = ap.parse_args()

    seed = load_seed()
    if args.coords:
        fill_coords(seed)
        return 0
    cache = load_cache()
    if args.views:
        cache = fill_views(seed, cache)
    views = cache.get("views") or {}

    places = cities()
    if args.park:
        return detail(seed, places, args.park)
    groups = park_groups(places)
    rows = assess(seed, places, groups, written_parks(), *supply(),
                  skip_countries=out_of_focus_countries())
    rows.sort(key=lambda r: rank(r, views))

    if args.check:
        free = [r for r in rows if verdict(r) in ("intro", "one short")]
        for r in free:
            print("%s (%s): %d trees mapped, %d groupable, no page" % (
                r["park"], r["city"], r["trees"], r["grouped"]))
        print("\n%d famous parks clear the five-tree gate with no page." % len(free))
        return 1 if free else 0

    if args.gaps:
        rows = [r for r in rows if not r["trees"] and not r["out_of_focus"]]
        print("FAMOUS PARKS WE MAP NOTHING IN\n")
    elif args.next:
        rows = [r for r in rows if verdict(r) not in ("page", "out of focus")]
        print("THE CHEAPEST PARK WINS, IN ORDER\n")
    else:
        print("THE WORLD'S BEST-KNOWN PARKS, AGAINST WHAT WE MAP\n")

    table(rows, views, args.next)

    done = sum(1 for r in rows if verdict(r) == "page")
    if not args.next and not args.gaps:
        counts = {}
        for r in rows:
            v = verdict(r)
            counts[v.split()[0] if v.startswith("thin") else v] = counts.get(
                v.split()[0] if v.startswith("thin") else v, 0) + 1
        print("\n%d parks. %s" % (len(rows), ", ".join(
            "%s %d" % (k, counts[k]) for k in sorted(counts, key=lambda k: ORDER.get(k, 9)))))
        if not views:
            print("No demand measured yet: run --views on a machine that can "
                  "reach wikimedia.org.")
    elif args.gaps:
        print("\n%d of %d famous parks have no tree of ours inside them." % (
            len(rows), len(seed["parks"])))
    print("\nVIEWS = English Wikipedia pageviews, 3 months, demand not search volume. "
          "GRP = trees the site can group into a park page. SUP = leads and register rows.")
    if done:
        print("page = %d already written under Contract H." % done)
    return 0


if __name__ == "__main__":
    sys.exit(main())
