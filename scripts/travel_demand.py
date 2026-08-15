#!/usr/bin/env python3
"""Travel intent, not fame. The demand proxy the queue should have used.

Hidde, 2026-08-15: "I don't think Wikipedia impression gives a good
representation of English tourist can't we make our top 250 smarter?"

He is right, and for once we could settle it with evidence rather than
argument, because the queue already carries `impressions_10d` per city from
the Search Console readback. That is 55 published, indexed cities where we
know what our pages actually earn, which makes any proposed proxy testable
against the only outcome we care about.

Measured 2026-08-15 on those cities (Spearman rank correlation against our
own impressions, so a proxy scores well only if it orders cities the way
reality does):

    English Wikipedia pageviews   rho +0.24    <- what the queue used
    English WIKIVOYAGE pageviews  rho +0.41    <- this file
    English share of pageviews    rho +0.11    <- the anglophone hypothesis

Three things follow, and the second is the one that surprised us.

1. Wikivoyage nearly doubles the signal. It is the same free API, no key, no
   account, and the article exists for essentially every place we would
   consider. Someone reading a Wikivoyage article is planning a trip; someone
   reading a Wikipedia article is settling an argument. Chernobyl and the
   Potsdam Conference are famous. Nobody packs a bag for them.

2. The anglophone hypothesis FAILED. Ranking cities by how English-dominant
   their readership is scores +0.11, which is nothing, and our six best pages
   (Palermo, Amsterdam, Rome, Prague, Barcelona, Vienna) are all in countries
   that read about themselves in their own language. What English speakers do
   is TRAVEL to continental Europe, and Wikivoyage catches that while a
   language ratio cannot. Recorded because the instinct is a natural one and
   would otherwise get proposed again.

3. It is a better proxy, not a good one. +0.41 explains part of the ordering
   and no more, and it is measured on the half of the site Google has indexed;
   the unindexed half cannot vote. Read it as "which of these places do
   English speakers plan trips to", never as a forecast of clicks.

Titles are resolved through WIKIDATA rather than guessed, which matters more
here than for Wikipedia. A wrong title returns 404 and reads as zero demand,
and the naive version of this test produced exactly that: New York on 616
views, Krakow on 385, Cadiz on 143, all of them title failures wearing the
costume of a finding. Wikidata's enwikivoyage sitelink cannot make that
mistake.

    python3 scripts/travel_demand.py              # every queue city, cached
    python3 scripts/travel_demand.py --write      # write `travel` into the queue
    python3 scripts/travel_demand.py --validate   # re-run the proxy test above
"""
import datetime
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "city-queue.json")
CACHE = os.path.join(ROOT, "data", "travel-demand-cache.json")
UA = "AncientTrees/1.0 (https://ancienttrees.app; tree mapping project)"
PAUSE = 0.1
STALE_DAYS = 30


# Wikidata resolves nearly everything, and these are the ones it cannot,
# found 2026-08-15 by flagging every city with big Wikipedia traffic and
# almost no Wikivoyage traffic. Each was a title failure wearing the costume
# of a finding: New York resolved to the STATE (501 views against the city's
# 21,737), Bath to a disambiguation page, and Faro, Cork, Split and Brussels
# to nothing at all. Left uncorrected they would have sunk four real tourist
# cities to the bottom of the queue.
#
# The trap this table also records: pick by MEANING, never by the biggest
# number. An automatic "take the busiest candidate" rule sent our Cartagena to
# Colombia's (5,169) over Spain's (905), which happened to be right, and would
# have sent Syracuse to New York State's over Sicily's, which would not.
TITLE_OVERRIDES = {
    "New York": "New York City",
    "Bath": "Bath",
    "Faro": "Faro",
    "Cork": "Cork",
    "Split": "Split",
    "Brussels": "Brussels",
    "Syracuse": "Syracuse (Italy)",       # ours is Sicily, not the one in NY
    "Cartagena": "Cartagena (Colombia)",  # ours is Colombia, not Spain
}


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def wikidata_voyage_titles(city_titles):
    """{en.wikipedia title: en.wikivoyage title}, 50 at a time.

    Two hops, both batched: the Wikipedia article gives its Wikidata id, and
    the Wikidata item gives its enwikivoyage sitelink. A city with no
    Wikivoyage article simply does not appear, which is a real answer (nobody
    wrote a travel guide for it) and not an error.
    """
    out = {}
    titles = list(city_titles)
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        try:
            d = _get("https://en.wikipedia.org/w/api.php?action=query&format=json"
                     "&prop=pageprops&ppprop=wikibase_item&redirects=1&titles="
                     + urllib.parse.quote("|".join(chunk), safe="|"))
        except Exception:
            continue
        q = d.get("query", {})
        # redirects and normalisation both rename our input, so map back
        back = {}
        for kind in ("normalized", "redirects"):
            for r in q.get(kind, []):
                back[r["to"]] = back.get(r["from"], r["from"])
        qids = {}
        for p in (q.get("pages") or {}).values():
            qid = (p.get("pageprops") or {}).get("wikibase_item")
            if qid:
                qids[qid] = back.get(p["title"], p["title"])
        if not qids:
            continue
        ids = list(qids)
        for j in range(0, len(ids), 50):
            try:
                w = _get("https://www.wikidata.org/w/api.php?action=wbgetentities"
                         "&format=json&props=sitelinks&sitefilter=enwikivoyage&ids="
                         + "|".join(ids[j:j + 50]))
            except Exception:
                continue
            for qid, ent in (w.get("entities") or {}).items():
                link = (ent.get("sitelinks") or {}).get("enwikivoyage")
                if link and qid in qids:
                    out[qids[qid]] = link["title"]
            time.sleep(PAUSE)
        time.sleep(PAUSE)
    return out


def voyage_views(title, months=3):
    """90 days of English Wikivoyage pageviews, human traffic only."""
    end = datetime.date.today().replace(day=1)
    start = end
    for _ in range(months):
        start = (start - datetime.timedelta(days=1)).replace(day=1)
    url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
           "en.wikivoyage/all-access/user/"
           + urllib.parse.quote(title.replace(" ", "_"), safe="")
           + "/monthly/%s/%s" % (start.strftime("%Y%m%d"), end.strftime("%Y%m%d")))
    try:
        return sum(i["views"] for i in _get(url).get("items", []))
    except Exception:
        return None


def load_cache():
    if os.path.exists(CACHE):
        try:
            return json.load(open(CACHE, encoding="utf-8"))
        except Exception:
            pass
    return {"fetched": {}, "titles": {}}


def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for pos, i in enumerate(order):
            r[i] = pos + 1
        return r
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    if n < 3:
        return 0.0
    return 1 - 6 * sum((a - b) ** 2 for a, b in zip(rx, ry)) / (n * (n * n - 1))


def main():
    write = "--write" in sys.argv
    validate = "--validate" in sys.argv
    doc = json.load(open(QUEUE, encoding="utf-8"))
    cities = doc["cities"]
    cache = load_cache()
    today = datetime.date.today().isoformat()

    # `article` overrides the city name where the two differ (Den Bosch,
    # Washington DC); it is the same column demand.py already maintains.
    want = {}
    for c in cities:
        art = c.get("article") or c["city"]
        if c["city"] not in cache["titles"]:
            want[art] = c["city"]
    if want:
        print("resolving %d Wikivoyage titles through Wikidata..." % len(want))
        found = wikidata_voyage_titles(want)
        for art, city in want.items():
            cache["titles"][city] = found.get(art)  # None = no travel guide
    for city, title in TITLE_OVERRIDES.items():
        if cache["titles"].get(city) != title:
            cache["titles"][city] = title
            cache["fetched"].pop(city, None)  # force a refetch on the right one
        json.dump(cache, open(CACHE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    fresh = 0
    for c in cities:
        title = cache["titles"].get(c["city"])
        rec = cache["fetched"].get(c["city"])
        if rec and (datetime.date.fromisoformat(rec["on"]) >
                    datetime.date.today() - datetime.timedelta(days=STALE_DAYS)):
            continue
        v = voyage_views(title) if title else 0
        cache["fetched"][c["city"]] = {"views": v if v is not None else 0, "on": today}
        fresh += 1
        if fresh % 25 == 0:
            print("  %d fetched" % fresh)
            json.dump(cache, open(CACHE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        time.sleep(PAUSE)
    json.dump(cache, open(CACHE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    for c in cities:
        c["travel"] = (cache["fetched"].get(c["city"]) or {}).get("views", 0)

    if validate:
        test = [c for c in cities
                if c["status"] == "published" and (c.get("impressions_10d") or 0) > 0]
        imp = [c["impressions_10d"] for c in test]
        print("\nProxy test on %d indexed, published cities" % len(test))
        print("  English Wikipedia pageviews  -> impressions:  rho = %+.2f"
              % spearman([c.get("demand") or 0 for c in test], imp))
        print("  English Wikivoyage pageviews -> impressions:  rho = %+.2f"
              % spearman([c["travel"] for c in test], imp))

    if write:
        json.dump(doc, open(QUEUE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("\nwrote `travel` into data/city-queue.json for %d cities" % len(cities))

    unpub = sorted([c for c in cities if c["status"] != "published" and c.get("travel")],
                   key=lambda c: -c["travel"])[:25]
    print("\nUnpublished cities by TRAVEL demand (what the queue should chase):")
    print("  %-20s %9s %10s %9s" % ("city", "travel", "wikipedia", "register"))
    for c in unpub:
        print("  %-20s %9s %10s %9s" % (
            c["city"], "{:,}".format(c["travel"]),
            "{:,}".format(c.get("demand") or 0), c.get("register") or 0))


if __name__ == "__main__":
    main()
