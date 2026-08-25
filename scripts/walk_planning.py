#!/usr/bin/env python3
"""City data loading and walk planning, extracted from build_site.py when its
rendering code was deleted (2026-08-09, after a clean deploy cycle from the
Astro port: see ARCHITECTURE.md's rollout plan, step 6).

The page-rendering half of build_site.py had no reason to survive the
migration, but this half does: scripts/route_walks.py runs plan_walks() on
every city to work out which walks need a real routed distance cached in
data/walk-routes.json, and that has nothing to do with which generator
renders the pages that walk feeds. Moved verbatim, not rewritten, so its
behaviour (and therefore every existing entry in data/walk-routes.json's
cache keys) stays exactly what it was.

THE PLANNING HALF IS GONE, as of 2026-08-25. What stood here was a second,
independent implementation of the walk algorithm that site/src/lib/walks.ts
also carries, and the header used to defend it as "necessary, not duplicated
for its own sake" while warning that changing one side without the other is
how they drift. They drifted, and not through the algorithm: the site began
planning from walkableTrees() (nothing behind a ticket, nothing without a
story or a coordinate) and this kept planning from every tree. Different
input, different ordered id lists, and the ordered id list is the cache key
data/walk-routes.json is built on, so 67 of 212 walks had no route and the
script that fetches them reported nothing to do.

Hidde, that day: "ik denk dat 1 wandelalgoritme wel de moeite is toch om de
boel simpeler en hetzelfde te houden." So the algorithm lives once, in
TypeScript, where the pages and the app's feed are built, and Python reads its
output through scripts/walks_feed.py. Both callers moved:
scripts/route_walks.py routes the published walks, scripts/city_queue.py
counts them.

What stays here is the half nothing else does: loading the city files and
checking that every city is published under its English name.
"""
import json
import math
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

sys.path.insert(0, str(ROOT / "scripts"))
from geo import km as haversine_km  # noqa: E402

ERRORS = []


def _fold_name(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def city_aliases():
    """Local spelling -> the English name this site publishes under.

    Shared with scripts/passcheck.py so there is one table rather than two that
    drift. See data/city-aliases.json for why the direction matters."""
    f = DATA / "city-aliases.json"
    if not f.exists():
        return {}
    return json.loads(f.read_text()).get("aliases", {})


def check_city_names(city_list):
    """Refuse to ship a city under its local name when English uses another.

    Every page here is written in English and its readers search in English, so
    the site says Florence and Naples. This shipped wrong twice: the brief
    generator once translated names in the wrong direction (2026-08-06), and the
    same day a city went live as Padova while every other Italian city on the
    site used its English name. Per CLAUDE.md's ratchet, a lesson that lands
    twice becomes a build check rather than a third note. Removing this check
    needs Hidde."""
    alias = city_aliases()
    for entry in city_list:
        d = entry.get("data")
        if not d:
            continue
        for value, field in ((d.get("city", ""), "city name"),
                             (entry.get("slug", ""), "slug")):
            english = alias.get(_fold_name(value))
            if english and _fold_name(english) != _fold_name(value):
                ERRORS.append(
                    f"{entry.get('slug')}: {field} is {value!r}, but this site "
                    f"publishes in English, where it is {english.title()!r}. "
                    f"Rename it and add the old slug to RENAMED_CITY_SLUGS so "
                    f"the live URL keeps resolving, or remove the pair from "
                    f"data/city-aliases.json if English really does use {value!r}.")


def load_cities():
    city_list = json.loads((DATA / "city-list.json").read_text())["cities"]
    for entry in city_list:
        f = DATA / "cities" / f"{entry['slug']}.json"
        entry["data"] = json.loads(f.read_text()) if f.exists() else None
    check_city_names(city_list)
    return city_list


# Streets do not run in straight lines, so the crow-flies total always
# understates a real walk. 1.35 is the usual rule of thumb for dense European
# city centres. The number shown to a visitor is deliberately rounded and
# labelled "about", because promising 3.8 km and delivering 4.6 is the kind of
# small lie that loses trust on a hot afternoon.
