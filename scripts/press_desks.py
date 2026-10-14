#!/usr/bin/env python3
"""Find the local newspaper desks for the cities that already earn impressions.

Hidde, 2026-10-14: press goes out in small rounds (four, then about twenty),
one desk per city, and the address list should cost code rather than tokens.
This is that list. It never sends anything; outreach_send.py does, after he
has read the batch.

How it works, per city:
1. Cities are ranked by Search Console impressions from DATA.md's depth roster
   (langcheck.english_impressions()), so a desk is only looked up where a
   visitor already arrives.
2. Wikidata lists newspapers (Q11032 and subclasses) published within
   RADIUS_KM of the centre of the city's trees, with their website, and an
   email address when Wikidata holds one. Dissolved papers are left out.
3. Each paper's homepage is fetched, its contact / Impressum / newsroom links
   are followed (at most three), and every address found is scored: news,
   desk and editorial addresses rank first; subscriptions, ads, privacy and
   jobs addresses are dropped.

The output holds newsroom addresses, so it goes to data/outreach-press-desks.json,
which is gitignored (data/outreach-*.json) and synced by private_store.py like
the other outreach files. Never commit it.

    python3 scripts/press_desks.py --top 25
    python3 scripts/press_desks.py --city berlin
    python3 scripts/press_desks.py --top 25 --no-fetch   (Wikidata only)
"""
import argparse
import glob
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

OUT = os.path.join(ROOT, "data", "outreach-press-desks.json")
BLOCKLIST = os.path.join(ROOT, "data", "fetch-blocklist.json")
UA = "AncientTreesBot/1.0 (https://ancienttrees.app; info@ancienttrees.app)"
RADIUS_KM = 15
TIMEOUT = 15

CONTACT_WORDS = ("impressum", "kontakt", "contact", "redaktion", "newsroom",
                 "about", "tips", "news-tips", "contatti", "contacto", "redactie")
GOOD = ("redaktion", "lokal", "news", "desk", "editor", "newsdesk", "tips",
        "story", "stories", "city", "stadt", "redazione", "redaccion", "redactie",
        "nieuws", "planning", "features", "leserbriefe")
BAD = ("abo", "anzeig", "werbung", "datenschutz", "privacy", "job", "karriere",
       "career", "advert", "ads", "subscri", "noreply", "no-reply", "webmaster",
       "leserservice", "kundenservice", "billing", "sales", "dpo", "gdpr",
       "marketing", "vertrieb", "media-sales", "recruit", "example",
       "jugendschutz", "security", "lizenz", "licens", "newsletter", "abuse",
       "presse@", "pr@", "press@", "beispiel", "user@", "name@", "formbricks")
EMAIL = re.compile(r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@(?:[A-Za-z0-9-]+\.)+(?:com|org|net|info|news|world|[a-z]{2})(?![A-Za-z0-9-])")


def get(url, accept="text/html"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read(800_000).decode("utf-8", "replace")


def blocked_hosts():
    try:
        d = json.load(open(BLOCKLIST))
    except (OSError, ValueError):
        return set()
    items = d.get("hosts", d) if isinstance(d, dict) else d
    return {(h if isinstance(h, str) else h.get("host", "")).lower() for h in items}


def city_centre(slug):
    d = json.load(open(os.path.join(ROOT, "data", "cities", slug + ".json")))
    pts = [(t["location"]["latitude"], t["location"]["longitude"])
           for t in d["trees"] if t.get("location", {}).get("latitude") is not None]
    if not pts:
        return None, d
    pts.sort()
    lat = sorted(p[0] for p in pts)[len(pts) // 2]
    lon = sorted(p[1] for p in pts)[len(pts) // 2]
    return (lat, lon), d


def wikidata_papers(lat, lon):
    q = """
SELECT DISTINCT ?paper ?paperLabel ?site ?mail ?langLabel WHERE {
  SERVICE wikibase:around {
    ?place wdt:P625 ?loc .
    bd:serviceParam wikibase:center "Point(%f %f)"^^geo:wktLiteral .
    bd:serviceParam wikibase:radius "%d" .
  }
  ?paper (wdt:P291|wdt:P159) ?place ; wdt:P31/wdt:P279* wd:Q11032 ; wdt:P856 ?site .
  FILTER NOT EXISTS { ?paper wdt:P576 ?end }
  OPTIONAL { ?paper wdt:P968 ?mail }
  OPTIONAL { ?paper wdt:P407 ?lang }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,de,fr,es,it,nl,pt,ja". }
}""" % (lon, lat, RADIUS_KM)
    url = "https://query.wikidata.org/sparql?format=json&query=" + urllib.parse.quote(q)
    data = json.loads(get(url, "application/sparql-results+json"))
    papers = {}
    for b in data["results"]["bindings"]:
        pid = b["paper"]["value"].rsplit("/", 1)[-1]
        p = papers.setdefault(pid, {"wikidata": pid, "name": b["paperLabel"]["value"],
                                    "site": b["site"]["value"], "emails": [], "language": ""})
        if "mail" in b:
            p["emails"].append(b["mail"]["value"].replace("mailto:", ""))
        if "langLabel" in b:
            p["language"] = b["langLabel"]["value"]
    return list(papers.values())


def score(addr, city):
    a = addr.lower()
    if any(w in a.split("@")[0] + "@" for w in BAD):
        return None
    s = 1
    local = a.split("@")[0]
    if "." in local and not any(w in local for w in GOOD):
        s -= 1  # firstname.lastname: a person, kept below every desk address
    if any(w in a for w in GOOD):
        s += 2
    if city.lower().split()[0] in a:
        s += 1
    return s


def scrape(site, city, blocked):
    host = urllib.parse.urlparse(site).netloc.lower()
    if host in blocked or host.removeprefix("www.") in blocked:
        return [], "blocklisted"
    try:
        home = get(site)
    except Exception as e:  # a dead or slow site is a note, not a stop
        return [], "home failed: %s" % type(e).__name__
    found = set(EMAIL.findall(home))
    links = []
    for href in re.findall(r'href="([^"#]+)"', home):
        if any(w in href.lower() for w in CONTACT_WORDS):
            full = urllib.parse.urljoin(site, href)
            if urllib.parse.urlparse(full).netloc.lower().removeprefix("www.") == host.removeprefix("www.") and full not in links:
                links.append(full)
    for link in links[:3]:
        try:
            found |= set(EMAIL.findall(get(link)))
        except Exception:
            continue
        time.sleep(1)
    out = []
    for a in found:
        a = a.strip(".").lower()
        if a.startswith("u003e"):
            a = a[5:]
        if a.endswith((".png", ".jpg", ".gif", ".webp", ".svg")):
            continue
        s = score(a, city)
        if s is not None:
            out.append((s, a))
    out.sort(key=lambda x: (-x[0], x[1]))
    return [a for _, a in out[:5]], "ok, %d contact page(s)" % min(3, len(links))


def ranked_cities():
    from langcheck import english_impressions
    imp = english_impressions()
    live = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))}
    return [c for c, _ in sorted(imp.items(), key=lambda kv: -kv[1][1]) if c in live], imp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--city")
    ap.add_argument("--no-fetch", action="store_true")
    args = ap.parse_args()

    cities, imp = ranked_cities()
    if args.city:
        cities = [args.city]
    else:
        cities = cities[:args.top]
    try:
        doc = json.load(open(OUT))
    except (OSError, ValueError):
        doc = {"_note": "Newsroom addresses per city, from scripts/press_desks.py. Private: never commit.", "cities": {}}
    blocked = blocked_hosts()

    for slug in cities:
        centre, city = city_centre(slug)
        if not centre:
            continue
        name = city.get("city", slug)
        try:
            papers = wikidata_papers(*centre)
        except Exception as e:
            print("%-16s wikidata failed: %s" % (slug, type(e).__name__))
            time.sleep(3)
            continue
        time.sleep(2)
        for p in papers:
            if not args.no_fetch and not p["emails"]:
                p["emails"], p["fetch"] = scrape(p["site"], name, blocked)
        doc["cities"][slug] = {"city": name, "country": city.get("country", ""),
                               "impressions": imp.get(slug, (0, 0))[1],
                               "checked": time.strftime("%Y-%m-%d"), "papers": papers}
        with_mail = sum(1 for p in papers if p["emails"])
        print("%-16s %4d impr  %2d papers, %2d with an address" % (slug, imp.get(slug, (0, 0))[1], len(papers), with_mail))
        json.dump(doc, open(OUT, "w"), ensure_ascii=False, indent=1)
    print("written to", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
