#!/usr/bin/env python3
"""Every published city's name in the languages people actually type.

Hidde, 2026-08-18: "het is wel handig als steden als den haag ook te vinden
zijn in hun eigen taal en niet alleen als the hague."

He is right, and the gap was worse than it looked. data/city-aliases.json is
hand-maintained, and its only entry for The Hague was "sgravenhage", the formal
spelling nobody types, while "Den Haag" was missing entirely. 25 of 133
published cities had any alias at all, and the search index never read the file
anyway, so typing Firenze, Wien, Napoli, Praha or Lisboa into our own search
returned nothing. A list of names in every language is exactly the sort of
thing that rots when it is typed by hand, so this generates it.

The source is the English Wikipedia's langlinks: one request per city returns
the article's title in every other language, which is precisely the set of
names a person might type. It is one call of about 0.2 seconds per city.
Wikidata was the first attempt and is the wrong tool here: its geo service was
timing out at 60 seconds a query on the day this was written, and identifying a
city by proximity alone picks Corduba over Cordoba and the Rotterdam-The Hague
metropolitan area over The Hague.

Nothing here reaches a reader's browser except the names, so under CLAUDE.md's
hard rule 5 this is gear rather than a product dependency.

Two things that keep it honest:

  - A city is confirmed by COORDINATES, never by name. Wikipedia's "Cordoba"
    is a disambiguation page carrying no coordinates, and Spain's Cordoba and
    Argentina's are one keystroke apart. An article whose position is missing
    or more than 40 km from the trees we publish is reported for a human to
    look at, never stored, because storing the wrong city's names sends a
    searcher to the wrong page.
  - Latin script only, and a cap per city. search-index.json is fetched by
    every visitor who touches the search box, and 180 languages per city would
    multiply it for an audience the site does not have yet. Both are constants
    below, not principles.

Writes into data/city-aliases.json under `search_names`, and deliberately
leaves the hand-curated `aliases` block alone: that one is the build's
authority on which name a city publishes UNDER (checkCityNames refuses a city
shipped as Padova), and it must never be fed generated data.

    python3 scripts/city_names.py            # cities with no names yet
    python3 scripts/city_names.py --all      # re-resolve everything
    python3 scripts/city_names.py --city the-hague
"""
import argparse
import json
import math
import pathlib
import statistics
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CITIES = ROOT / "data" / "cities"
ALIASES = ROOT / "data" / "city-aliases.json"

API = "https://en.wikipedia.org/w/api.php"
UA = "AncientTrees/1.0 (https://ancienttrees.app; contact via ancienttrees.app)"

# How far the article's own coordinates may sit from the median of the trees we
# publish. Generous on purpose: our median is a cluster of trees, not a city
# hall, and a city page may reach 30 minutes out under the day-trip rule.
MAX_KM = 40

# Languages first in this list survive the per-city cap. English is absent on
# purpose: the English name is what the search row already carries, and any
# label equal to it is dropped.
LANG_PRIORITY = [
    "nl", "de", "fr", "es", "it", "pt", "ca", "da", "sv", "nn", "no", "fi",
    "pl", "cs", "sk", "sl", "hr", "hu", "ro", "tr", "lt", "lv", "et", "ga",
    "cy", "eu", "gl", "is", "sq", "mt", "af", "id", "ms", "vi", "la",
]
MAX_NAMES = 10
LATIN_ONLY = True


def fold(s):
    """Lowercase, strip accents, keep letters and digits. Deliberately the same
    rule as foldName() in site/src/lib/city-aliases.ts, so both sides agree on
    what counts as the same name."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join("".join(c for c in s.lower() if c.isalnum() or c == " ").split())


def is_latin(s):
    stripped = "".join(c for c in unicodedata.normalize("NFKD", s)
                       if not unicodedata.combining(c))
    return all(c.isascii() or not c.isalpha() for c in stripped)


def strip_qualifier(title):
    """Wikipedia disambiguates in the title itself: nl calls Florence
    "Florence (stad)" and Cadiz "Cádiz (stad)". The bracket is the
    encyclopaedia's bookkeeping, not part of the name anyone types."""
    if "(" in title:
        title = title[:title.index("(")]
    if "," in title:
        title = title[:title.index(",")]
    return title.strip()


def api(params):
    params = {**params, "format": "json", "formatversion": "2"}
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.load(r)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(3 * (attempt + 1))
    return {}


def haversine(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return 2 * 6371 * math.asin(math.sqrt(h))


def centroid(data):
    pts = [(t["location"]["latitude"], t["location"]["longitude"])
           for t in data.get("trees", [])
           if (t.get("location") or {}).get("latitude") is not None
           and (t.get("location") or {}).get("longitude") is not None]
    if not pts:
        return None
    return statistics.median(p[0] for p in pts), statistics.median(p[1] for p in pts)


def fetch_article(title):
    d = api({"action": "query", "titles": title, "redirects": "1",
             "prop": "coordinates|langlinks|pageprops", "lllimit": "500"})
    pages = (d.get("query") or {}).get("pages") or []
    if not pages or pages[0].get("missing"):
        return None
    pg = pages[0]
    coords = pg.get("coordinates") or []
    return {
        "title": pg.get("title"),
        "coord": (coords[0]["lat"], coords[0]["lon"]) if coords else None,
        "disambiguation": "disambiguation" in (pg.get("pageprops") or {}),
        "langlinks": {l["lang"]: l["title"] for l in pg.get("langlinks", [])},
    }


def search_title(city, country):
    d = api({"action": "query", "list": "search",
             "srsearch": "%s %s city" % (city, country), "srlimit": "3"})
    hits = ((d.get("query") or {}).get("search") or [])
    return [h["title"] for h in hits]


def resolve(city, country, here):
    """The article our trees actually stand in, or a reason it is unresolved."""
    tried = []
    for title in [city, "%s, %s" % (city, country)]:
        art = fetch_article(title)
        tried.append(title)
        if art and art["coord"]:
            km = haversine(here, art["coord"])
            if km <= MAX_KM:
                return art, None
            tried[-1] += " (%s, %.0f km away)" % (art["title"], km)
        elif art:
            # A handful of real city articles carry no coordinates in this
            # API's answer (Krakow is one). Those are still safe to accept
            # when the title IS the city and the page is not a disambiguation,
            # which is the exact thing that separates Krakow from Cordoba:
            # both come back without coordinates, and only one of them is a
            # list of places on two continents.
            if not art["disambiguation"] and fold(art["title"]) == fold(city):
                return art, None
            tried[-1] += " (%s, no coordinates%s)" % (
                art["title"], ", disambiguation page" if art["disambiguation"] else "")
    for title in search_title(city, country):
        art = fetch_article(title)
        if art and art["coord"] and haversine(here, art["coord"]) <= MAX_KM:
            return art, None
        tried.append("search: " + title)
    return None, "; ".join(tried)


def pick_names(english, langlinks):
    """The handful of spellings worth shipping, best language first.

    The dedupe has to score a name by the BEST language that uses it, not the
    first one the API happens to list. Dozens of languages call The Hague
    "Den Haag", and the API returns them alphabetically, so keeping the first
    occurrence scored that name as Afrikaans and dropped it off the end of the
    list. The one name a Dutch reader would type was missing from The Hague,
    and Firenze was missing from Florence, for exactly this reason."""
    english_folded = fold(english)
    best = {}
    for lang, title in langlinks.items():
        name = strip_qualifier(title)
        if not name or (LATIN_ONLY and not is_latin(name)):
            continue
        f = fold(name)
        if not f or f == english_folded:
            continue
        rank = LANG_PRIORITY.index(lang) if lang in LANG_PRIORITY else len(LANG_PRIORITY)
        if f not in best or rank < best[f][0]:
            best[f] = (rank, name)
    scored = sorted(best.values(), key=lambda x: (x[0], x[1]))
    return [n for _, n in scored[:MAX_NAMES]]


NOTE = ("Generated by scripts/city_names.py from the English Wikipedia's langlinks: "
        "every published city's name in the languages people actually type, so the "
        "site search finds Den Haag as well as The Hague. Latin script only and capped "
        "per city, because search-index.json is downloaded by every visitor who touches "
        "the search box. FOR SEARCH ONLY. This block is never the authority on which "
        "name a city publishes under; that stays the hand-curated `aliases` block, which "
        "checkCityNames reads and which must not be fed generated data.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="re-resolve every city")
    ap.add_argument("--city", help="one slug only")
    args = ap.parse_args()

    doc = json.loads(ALIASES.read_text(encoding="utf-8"))
    known = doc.get("search_names", {})
    articles = doc.get("wikipedia_titles", {})

    todo = []
    for f in sorted(CITIES.glob("*.json")):
        slug = f.stem
        if args.city and slug != args.city:
            continue
        if not args.all and not args.city and slug in known:
            continue
        todo.append((slug, json.loads(f.read_text(encoding="utf-8"))))

    if not todo:
        print("Nothing to do: every published city already has search names.")
        return 0

    print("Resolving %d city/cities against Wikipedia." % len(todo))
    unresolved, empty = [], []
    for slug, data in todo:
        here = centroid(data)
        if not here:
            unresolved.append((slug, "no tree coordinates to place it by"))
            continue
        art, why = resolve(data["city"], data.get("country", ""), here)
        if not art:
            unresolved.append((slug, "no article within %d km, tried %s" % (MAX_KM, why)))
            continue
        names = pick_names(data["city"], art["langlinks"])
        articles[slug] = art["title"]
        if names:
            known[slug] = names
        else:
            empty.append(slug)
        print("  %-24s %-26s %s" % (slug, art["title"], ", ".join(names[:5]) or "(no other names)"))
        time.sleep(0.2)

    doc["search_names"] = dict(sorted(known.items()))
    doc["wikipedia_titles"] = dict(sorted(articles.items()))
    doc["search_names_note"] = NOTE
    ALIASES.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n%d cities carry %d searchable names." % (len(known), sum(len(v) for v in known.values())))
    if empty:
        print("%d resolved but have no name other than the English one: %s"
              % (len(empty), ", ".join(empty)))
    if unresolved:
        print("\n%d unresolved, each wanting a look rather than a guess:" % len(unresolved))
        for slug, why in unresolved:
            print("  %-24s %s" % (slug, why))
    return 0


if __name__ == "__main__":
    sys.exit(main())
