#!/usr/bin/env python3
"""Which places of one country are missing from the queue, ranked by travel demand.

Hidde, 2026-09-01: "ik wil meer lege steden in de US". The 2026-08-17 audit
that first widened the pool worked off Wikivoyage's most-read list, and that
list is truncated at 1,000 articles a month, so it found the big holes and by
construction could not find the tail. Repeating it adds nothing.

This asks the complete question instead: every place in the country that HAS
an English Wikivoyage article (Wikidata knows, one SPARQL query), then that
article's own pageviews (the same free API travel_demand.py already uses, the
same metric the queue's score is built on). Nothing here is a judgement about
which American cities are nice.

Results are cached in data/research/pool-<country>.json, because this costs a
few thousand API calls and CLAUDE.md's standing rule is that research already
paid for never gets thrown away.

Usage:
  python3 scripts/pool_audit.py                      # United States, report only
  python3 scripts/pool_audit.py --country Canada
  python3 scripts/pool_audit.py --min 3000 --write   # add them to the queue
"""
import argparse
import concurrent.futures as futures
import datetime
import json
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "city-queue.json")
RESEARCH = os.path.join(ROOT, "data", "research")
UA = "AncientTrees/1.0 (https://ancienttrees.app; tree mapping)"

# Wikidata item per country, so the SPARQL query needs no name matching.
COUNTRY_Q = {
    "United States": "Q30", "Canada": "Q16", "Australia": "Q408",
    "United Kingdom": "Q145", "Germany": "Q183", "France": "Q142",
    "Italy": "Q38", "Spain": "Q29", "Japan": "Q17", "Netherlands": "Q55",
}


# Articles the diff surfaces that are not new places. Kept as a named list
# rather than a threshold, because both cases are about IDENTITY and no number
# separates them: "New York City" is the queue's "New York" under Wikivoyage's
# own title, and "Manhattan" is a borough of it. A district entering the pool
# as a city would put two rows on the same trees.
SKIP = {"New York City", "Manhattan"}



def slugify(name):
    """The queue's own slug shape: 'San Antonio' -> 'san-antonio'.

    Written after the first --write run omitted it and broke prepare.py, which
    indexes rows by c["slug"] without a guard and is the first thing every
    night run calls. A row missing a field the rest of the queue carries is
    not a harmless row.
    """
    out = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", out.lower())).strip("-")


def _get(url, accept=None, timeout=40):
    """Every fetch gets a hard timeout: CLAUDE.md's own lesson, a host that
    hangs costs the whole window while a refusal costs a second."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    if accept:
        req.add_header("Accept", accept)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def voyage_articles(country):
    """Every English Wikivoyage article about a city in `country`."""
    qid = COUNTRY_Q.get(country)
    if not qid:
        raise SystemExit("no Wikidata id recorded for %r; add it to COUNTRY_Q" % country)
    q = ("SELECT ?article WHERE { ?item wdt:P31/wdt:P279* wd:Q515 ; wdt:P17 wd:%s . "
         "?article schema:about ?item ; schema:isPartOf <https://en.wikivoyage.org/> . }" % qid)
    url = "https://query.wikidata.org/sparql?query=" + urllib.parse.quote(q)
    csv = _get(url, accept="text/csv", timeout=90)
    out = []
    for line in csv.splitlines()[1:]:
        line = line.strip()
        if not line.startswith("https://en.wikivoyage.org/wiki/"):
            continue
        out.append(urllib.parse.unquote(line.rsplit("/", 1)[1]))
    return sorted(set(out))


def top_articles(months=12):
    """Every article in Wikivoyage's monthly top-1000, for the last `months`.

    One call per month instead of one per article. The first version of this
    script asked per article and was rate-limited after 114 of 3,221 requests,
    which is the same Wikimedia throttle CLAUDE.md already records for image
    fetches. This endpoint answers the question we actually have (which places
    carry real travel traffic) in twelve calls.

    The known limit, stated because the 2026-08-17 audit hit it: the list is
    truncated at 1,000 a month, so anything below that rank is invisible here.
    Twelve months rather than three is what widens it, since a seasonal
    destination enters the top 1,000 in its own season and not in a fixed
    quarter.
    """
    totals = {}
    month = datetime.date.today().replace(day=1)
    for _ in range(months):
        month = (month - datetime.timedelta(days=1)).replace(day=1)
        url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/top/"
               "en.wikivoyage/all-access/%04d/%02d/all-days" % (month.year, month.month))
        try:
            d = json.loads(_get(url, timeout=30))
        except Exception as exc:
            print("  %s: skipped (%s)" % (month, exc.__class__.__name__))
            continue
        for item in d.get("items", []):
            for a in item.get("articles", []):
                totals[a["article"]] = totals.get(a["article"], 0) + (a.get("views") or 0)
    return totals


def clean(title):
    """'Alexandria (Virginia)' -> 'Alexandria'. The queue stores plain names."""
    return re.sub(r"\s*\([^)]*\)$", "", title.replace("_", " ")).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--country", default="United States")
    ap.add_argument("--min", type=int, default=5000,
                    help="travel views over 12 months below which a place is not "
                         "worth a row")
    ap.add_argument("--refresh", action="store_true", help="ignore the cache")
    ap.add_argument("--write", action="store_true", help="add the survivors to the queue")
    args = ap.parse_args()

    os.makedirs(RESEARCH, exist_ok=True)
    cache_path = os.path.join(RESEARCH, "pool-%s.json"
                              % args.country.lower().replace(" ", "-"))
    cache = {}
    if os.path.exists(cache_path) and not args.refresh:
        cache = json.load(open(cache_path, encoding="utf-8")).get("views", {})

    titles = voyage_articles(args.country)
    print("%d Wikivoyage articles for %s" % (len(titles), args.country))

    if not cache:
        print("fetching Wikivoyage's monthly top-1000 for the last 12 months...")
        top = top_articles()
        cache = {t: top.get(t, 0) for t in titles}
        json.dump({"_note": "Wikivoyage pageviews over 12 months, summed from the "
                            "monthly top-1000 lists, restricted to this country's "
                            "articles. Gathered by scripts/pool_audit.py.",
                   "_limit": "the top-1000 is truncated, so a 0 here means 'never in "
                             "a monthly top 1,000', not 'no traffic'.",
                   "country": args.country, "gathered": datetime.date.today().isoformat(),
                   "views": cache},
                  open(cache_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("cached in %s" % os.path.relpath(cache_path, ROOT))

    doc = json.load(open(QUEUE, encoding="utf-8"))
    have = {c["city"].lower() for c in doc["cities"]}
    have |= {(c.get("article") or "").lower() for c in doc["cities"]}

    missing = []
    for t in titles:
        name = clean(t)
        if name.lower() in have or t.replace("_", " ") in SKIP or name in SKIP:
            continue
        v = cache.get(t, 0)
        if v >= args.min:
            missing.append((v, name, t))
    missing.sort(reverse=True)

    print("\n%d places over %d views are NOT in the queue:\n" % (len(missing), args.min))
    for v, name, t in missing[:60]:
        print("  %7d  %-28s %s" % (v, name, "" if name == t.replace("_", " ") else t))

    if args.write and missing:
        for v, name, t in missing:
            row = {"city": name, "slug": slugify(name), "country": args.country,
                   "status": "pending", "trees": 0, "travel": v,
                   "source": "pool_audit 2026-09-01"}
            if name != t.replace("_", " "):
                row["article"] = t.replace("_", " ")
            doc["cities"].append(row)
        json.dump(doc, open(QUEUE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("\nadded %d rows to data/city-queue.json; run rescore.py --write next"
              % len(missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
