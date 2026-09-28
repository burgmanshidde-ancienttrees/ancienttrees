#!/usr/bin/env python3
"""Is there a recent, dated sign that the tree at this spot is still standing?

Written 2026-09-28, when Hidde agreed that one official register is enough to
say WHAT a tree is, anywhere in the world, and that the second source a
verify pass used to hunt for was mostly buying one fact: that the tree is
still alive. Registers almost never record a death (Lazio's national file kept
five dead Rome trees live), so that fact is the one thing a register cannot
give us, and it is cheap to look for by machine.

Two free, read-only APIs, no key, hard timeouts:
  - Wikimedia Commons: geotagged files within RADIUS metres, with the date
    the photograph was taken (falling back to the upload date).
  - iNaturalist: plant observations within RADIUS metres since CUTOFF years.

It prints the newest evidence it found and a verdict:
  RECENT   a dated photograph or observation at the spot within CUTOFF years
  OLD      evidence exists but nothing within CUTOFF years
  NONE     nothing geotagged at the spot at all

What it cannot do, so nobody trusts it further than it goes: it proves that
SOMETHING was photographed at the spot recently, not that it was this trunk.
A park full of limes will always say RECENT. Read it as "no reason to doubt",
never as "confirmed", and look at the photograph when two similar trees stand
close. NONE is not a death, it is an absence of evidence, and the tree still
ships flagged under the register rule; a reader tells us when it is gone.

Usage:
  python3 scripts/lifecheck.py LAT LON [--radius 30] [--years 4]
  python3 scripts/lifecheck.py --file data/research/x-verified.json
"""
import argparse
import datetime as dt
import json
import sys
import time
import urllib.parse
import urllib.request

UA = "AncientTrees-lifecheck/1.0 (https://ancienttrees.app)"


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def commons(lat, lon, radius):
    """(date, url) pairs for geotagged Commons files near the spot."""
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "geosearch",
        "ggscoord": f"{lat}|{lon}", "ggsradius": max(10, int(radius)),
        "ggsnamespace": 6, "ggslimit": 30, "prop": "imageinfo",
        "iiprop": "timestamp|extmetadata|url", "iiextmetadatafilter": "DateTimeOriginal",
    })
    out = []
    try:
        pages = _get("https://commons.wikimedia.org/w/api.php?" + q).get("query", {}).get("pages", {})
    except Exception as e:
        print(f"  commons: unreachable ({e.__class__.__name__})", file=sys.stderr)
        return out
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        raw = ((ii.get("extmetadata") or {}).get("DateTimeOriginal") or {}).get("value") or ii.get("timestamp") or ""
        d = _date(raw)
        if d:
            out.append((d, ii.get("descriptionurl") or p.get("title")))
    return out


def inat(lat, lon, radius, since):
    """(date, url) pairs for plant observations near the spot since a date."""
    q = urllib.parse.urlencode({
        "lat": lat, "lng": lon, "radius": radius / 1000.0, "iconic_taxa": "Plantae",
        "d1": since.isoformat(), "order_by": "observed_on", "order": "desc", "per_page": 10,
    })
    try:
        res = _get("https://api.inaturalist.org/v1/observations?" + q).get("results", [])
    except Exception as e:
        print(f"  inaturalist: unreachable ({e.__class__.__name__})", file=sys.stderr)
        return []
    return [(_date(o.get("observed_on") or ""), o.get("uri")) for o in res if _date(o.get("observed_on") or "")]


def _date(s):
    s = str(s).strip()
    for n in (10, 7, 4):
        try:
            return dt.date.fromisoformat(s[:n].replace(":", "-") + ("-01" if n == 7 else "-01-01" if n == 4 else ""))
        except ValueError:
            continue
    return None


def check(lat, lon, radius=30, years=4):
    since = dt.date.today() - dt.timedelta(days=365 * years)
    ev = commons(lat, lon, radius)
    time.sleep(1)
    ev += inat(lat, lon, radius, since)
    ev.sort(reverse=True)
    if not ev:
        return "NONE", None
    return ("RECENT" if ev[0][0] >= since else "OLD"), ev[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lat", nargs="?", type=float)
    ap.add_argument("lon", nargs="?", type=float)
    ap.add_argument("--radius", type=float, default=30)
    ap.add_argument("--years", type=int, default=4)
    ap.add_argument("--file", help="a verified-research JSON: a list of trees, or {trees: [...]}")
    a = ap.parse_args()
    if a.file:
        data = json.load(open(a.file))
        trees = data.get("trees", data) if isinstance(data, dict) else data
        for t in trees:
            loc = t.get("location") or t
            lat, lon = loc.get("latitude"), loc.get("longitude")
            if lat is None or lon is None:
                print(f"{t.get('id', '?'):12} no coordinate")
                continue
            v, e = check(lat, lon, a.radius, a.years)
            print(f"{t.get('id', '?'):12} {v:6} {e[0] if e else '':10} {e[1] if e else ''}  {t.get('name', '')}")
            time.sleep(2)
        return
    if a.lat is None or a.lon is None:
        ap.error("give LAT LON or --file")
    v, e = check(a.lat, a.lon, a.radius, a.years)
    print(v, e[0] if e else "", e[1] if e else "")


if __name__ == "__main__":
    main()
