#!/usr/bin/env python3
"""How big is a place, in people, from Wikidata.

Hidde, 2026-09-23, after seeing that the field deciding how many trees a city
may hold put Tokyo below Cadiz: "kijk naar hoe groot een stad is en stel daar
het plafond op, ik denk dat het zo simpel is."

It is that simple, and the number was simply missing. The queue held demand
(English Wikipedia pageviews, which measures ATTENTION) and travel (a tourism
proxy that reads 1,928 for Tokyo and 20,920 for Aarhus). Neither is size.

This resolves each place in data/city-queue.json to a Wikidata item and reads
P1082, population. Cached in data/city-population.json, so it runs once and
costs nothing afterwards. Gear for us rather than a dependency in the product:
nothing it fetches reaches a reader's browser, and if Wikidata vanished
tomorrow the cache would still answer.

Resolution is checked rather than trusted: the candidate's country (P17) has to
match the country the queue already records, otherwise the row is left blank
for a human. A wrong Cambridge is worse than no Cambridge.

Usage:
  python3 scripts/city_size.py            # fill the cache, skipping what it has
  python3 scripts/city_size.py --missing  # what it could not resolve
  python3 scripts/city_size.py --ladder   # what each tier would hold
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

CACHE = "data/city-population.json"
API = "https://www.wikidata.org/w/api.php"
UA = "ancienttrees.app city sizes (ancienttrees.app)"


def get(url, tries=4):
    """Wikidata rate-limits rather than blocks, the same shape as Wikimedia's
    429 on image bursts. Back off and carry on; a hard timeout every time,
    because a host that hangs costs the whole window."""
    for n in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code != 429 or n == tries - 1:
                raise
            time.sleep(5 * (n + 1))
    return {}


def search(name):
    q = urllib.parse.urlencode({"action": "wbsearchentities", "search": name,
                                "language": "en", "format": "json", "limit": 5, "type": "item"})
    return [h["id"] for h in get(f"{API}?{q}").get("search", [])]


def entity(qid):
    q = urllib.parse.urlencode({"action": "wbgetentities", "ids": qid, "format": "json",
                                "props": "claims|labels", "languages": "en"})
    return get(f"{API}?{q}")["entities"][qid]


def claim_value(ent, prop):
    """The CURRENT value, not the first one written down.

    Wikidata keeps every census a place has ever had, as separate P1082
    statements qualified with P585, point in time. Taking the first one handed
    Berlin a population of 1,200 (a medieval figure), London 1,011,157 and Hong
    Kong 3.1 million. So: prefer the statement Wikidata itself marks preferred,
    otherwise the one with the latest point in time.
    """
    claims = ent.get("claims", {}).get(prop, [])
    best = None
    for c in claims:
        v = c.get("mainsnak", {}).get("datavalue", {}).get("value")
        if isinstance(v, dict) and "id" in v:
            return v["id"]
        if not (isinstance(v, dict) and "amount" in v):
            continue
        when = ""
        for q in c.get("qualifiers", {}).get("P585", []):
            t = q.get("datavalue", {}).get("value", {}).get("time")
            if t:
                when = max(when, t)
        rank = 2 if c.get("rank") == "preferred" else (0 if c.get("rank") == "deprecated" else 1)
        key = (rank, when)
        if best is None or key > best[0]:
            best = (key, abs(float(v["amount"])))
    return best[1] if best else None


def country_label(qid):
    try:
        return entity(qid).get("labels", {}).get("en", {}).get("value")
    except Exception:
        return None


# English Wikipedia titles that are not the place we mean. "New York" is the
# STATE there, which handed the city 19.4 million people and the wrong tier.
ALIAS = {"New York": "New York City", "Washington DC": "Washington, D.C.",
         "Mexico City": "Mexico City", "Quebec": "Quebec City",
         "Luxembourg": "Luxembourg City", "Kuwait": "Kuwait City",
         "Panama": "Panama City", "Guatemala": "Guatemala City"}


def by_wikipedia(name):
    """Resolve through the English Wikipedia article of that exact name.

    This is the accurate route and it should have been the first one: the
    queue's own `demand` column is English Wikipedia pageviews, so the article
    that measures a place's attention is the article that should give its size.
    Searching by label instead handed Albuquerque a population of 3,785 (a
    village in Spain), New York the population of the STATE, and found nothing
    at all for Aarhus, Antwerp or Auckland.
    """
    name = ALIAS.get(name, name)
    q = urllib.parse.urlencode({"action": "wbgetentities", "sites": "enwiki", "titles": name,
                                "format": "json", "props": "claims|labels", "languages": "en"})
    ents = get(f"{API}?{q}").get("entities", {})
    for qid, ent in ents.items():
        if qid.startswith("-") or "missing" in ent:
            continue
        pop = claim_value(ent, "P1082")
        if pop:
            return {"qid": qid, "population": int(pop), "via": "enwiki"}
    return None


def resolve(name, country, countries):
    """The first hit whose country matches what the queue already says."""
    for qid in search(name):
        try:
            ent = entity(qid)
        except Exception:
            continue
        pop = claim_value(ent, "P1082")
        c = claim_value(ent, "P17")
        if not pop or not isinstance(c, str):
            continue
        if c not in countries:
            countries[c] = country_label(c)
            time.sleep(0.3)
        if countries.get(c) and country and countries[c].lower() not in country.lower() \
           and country.lower() not in countries[c].lower():
            continue
        return {"qid": qid, "population": int(pop), "country_checked": countries.get(c)}
    return None


TIERS = [(5_000_000, 100), (1_000_000, 60), (250_000, 30), (50_000, 20), (0, 10)]


def ceiling(pop):
    """Hidde's own three points, and the cutoffs that reproduce them:
    Baarn 25k -> 10, Copenhagen 660k -> 30, Tokyo 14M -> 100."""
    if not pop:
        return None
    for floor, n in TIERS:
        if pop >= floor:
            return n
    return 10


def main():
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    rows = json.load(open("data/city-queue.json"))
    rows = rows if isinstance(rows, list) else rows.get("cities", [])
    a = sys.argv[1:]

    if a and a[0] == "--missing":
        for c in rows:
            if c.get("slug") and not cache.get(c["slug"], {}).get("population"):
                print(f"  {c['city']} ({c.get('country')})")
        return
    if a and a[0] == "--ladder":
        import collections
        n = collections.Counter()
        for c in rows:
            p = cache.get(c.get("slug") or "", {}).get("population")
            n[ceiling(p)] += 1
        for k in (100, 60, 30, 20, 10, None):
            print(f"  ceiling {str(k):>4}: {n[k]:4d} places")
        return

    countries = {}
    todo = [c for c in rows if c.get("slug") and c["slug"] not in cache]
    print(f"{len(cache)} cached, {len(todo)} to resolve")
    for i, c in enumerate(todo, 1):
        try:
            hit = by_wikipedia(c["city"]) or resolve(c["city"], c.get("country") or "", countries)
        except Exception as e:
            print(f"  {c['city']}: {e}")
            hit = None
        cache[c["slug"]] = hit or {"population": None}
        if i % 25 == 0:
            json.dump(cache, open(CACHE, "w"), ensure_ascii=False, indent=1, sort_keys=True)
            print(f"  {i}/{len(todo)}")
        time.sleep(1.0)
    json.dump(cache, open(CACHE, "w"), ensure_ascii=False, indent=1, sort_keys=True)
    ok = sum(1 for v in cache.values() if v.get("population"))
    print(f"done: {ok} of {len(cache)} resolved")


if __name__ == "__main__":
    main()
