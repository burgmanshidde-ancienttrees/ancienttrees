#!/usr/bin/env python3
"""Ask Google, page by page, whether it has seen what we changed.

A one-off (Hidde, 2026-10-20: "ok do the one of"), after three weeks in which
the build kept 2,700 photo-less tree pages out of Google with a googlebot-only
noindex and Search Console's indexed-pages line did not move. The Search
Analytics API says what Google showed; it cannot say what Google has crawled.
The URL Inspection API can, one URL at a time, 2,000 a day.

Three samples, drawn the same way every time it runs:
  out    English tree pages on the google_only noindex list (data/noindex.json)
  kept   English tree pages with a photograph, in cities on the frozen roster
  places place pages on the frozen roster
For each URL Google answers with its verdict (indexed or not, and why), the
last crawl time, what the crawler saw (indexingState: allowed, or blocked by
the meta tag), and the canonical it chose. The script writes every answer to
data/research/gsc-inspection-<date>.json and prints a summary per sample.

Needs GSC_CLIENT_ID / GSC_CLIENT_SECRET / GSC_REFRESH_TOKEN (the digest's
Search Console OAuth, scope webmasters). Runs from gsc-inspect.yml.

    python3 scripts/gsc_inspect.py [--per-sample 25] [--wanted]

--wanted inspects every url in the live sitemap.xml instead of the samples;
the file is then gsc-inspection-<date>-wanted.json. --paths /a,/b asks about
those paths only (gsc-inspection-<date>-paths.json), to see whether pages
Hidde asked Google to index have been taken in.
"""
import collections
import datetime
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://ancienttrees.app"
SITE = "sc-domain:ancienttrees.app"
LANG = re.compile(r"^/(es|it|nl|de|pt|fr|ja)/")


def access_token():
    cid, csec, rtok = (os.environ.get(k) for k in ("GSC_CLIENT_ID", "GSC_CLIENT_SECRET", "GSC_REFRESH_TOKEN"))
    if not (cid and csec and rtok):
        raise SystemExit("gsc_inspect: GSC_* secrets absent, nothing asked")
    body = urllib.parse.urlencode({"client_id": cid, "client_secret": csec,
                                   "refresh_token": rtok, "grant_type": "refresh_token"}).encode()
    with urllib.request.urlopen("https://oauth2.googleapis.com/token", body, timeout=30) as r:
        return json.load(r)["access_token"]


def inspect(token, url):
    req = urllib.request.Request(
        "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
        data=json.dumps({"inspectionUrl": url, "siteUrl": SITE}).encode(),
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r).get("inspectionResult", {}).get("indexStatusResult", {})
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(10 * (attempt + 1))
                continue
            return {"error": e.code, "body": e.read().decode()[:200]}
        except Exception as e:  # noqa: BLE001
            return {"error": e.__class__.__name__}


def live_urls():
    """{tree id: path} from the site's own feed, so the slug rules stay in
    site/src/lib/slug.ts and are not guessed here (tree_approved.py does the same)."""
    try:
        req = urllib.request.Request(f"{BASE}/api/trees.json", headers={"User-Agent": "AncientTreesBot/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return {t["id"]: t["url"] for t in json.load(r).get("trees", []) if t.get("url")}
    except Exception as e:  # noqa: BLE001
        print(f"gsc_inspect: live feed unreadable ({e.__class__.__name__}), kept sample empty")
        return {}


def samples(per):
    noidx = json.load(open(os.path.join(ROOT, "data", "noindex.json"), encoding="utf-8"))
    roster = json.load(open(os.path.join(ROOT, "data", "depth-roster-frozen.json"), encoding="utf-8"))["cities"]
    out_paths = [p for p in noidx.get("google_only", []) if not LANG.match(p) and p.count("/") == 2]
    kept, places = [], []
    noidx_all = set(noidx.get("paths", []))
    urls = live_urls()
    for slug in roster:
        path = os.path.join(ROOT, "data", "cities", f"{slug}.json")
        if not os.path.exists(path):
            continue
        city = json.load(open(path, encoding="utf-8"))
        if f"/{slug}" not in noidx_all:
            places.append(f"/{slug}")
        for t in city.get("trees", []):
            ph = t.get("photo") or {}
            p = urls.get(t.get("id"))
            if p and ph.get("url") and ph.get("status") == "approved" and p not in noidx_all:
                kept.append(p)
    rnd = random.Random(20261020)  # the same sample every run, so runs compare
    return {"out": rnd.sample(out_paths, min(per, len(out_paths))),
            "kept": rnd.sample(kept, min(per, len(kept))),
            "places": rnd.sample(places, min(per // 2, len(places)))}


def wanted():
    """Every url in the live sitemap.xml: the pages we ask Google to index
    (2026-10-28, Hidde asked whether a crawl request could help; it can only
    help a wanted page Google has not indexed, so this names them)."""
    try:
        with urllib.request.urlopen(f"{BASE}/sitemap.xml", timeout=30) as r:
            locs = re.findall(r"<loc>([^<]+)</loc>", r.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"gsc_inspect: live sitemap unreadable ({e.__class__.__name__})")
        return []
    return [u.replace(BASE, "") or "/" for u in locs]


def sitemaps(token):
    """What Search Console knows of each sitemap: submitted, last read, errors, url count."""
    req = urllib.request.Request(
        "https://www.googleapis.com/webmasters/v3/sites/" + urllib.parse.quote(SITE, safe="") + "/sitemaps",
        headers={"Authorization": "Bearer " + token})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r).get("sitemap", [])
    except urllib.error.HTTPError as e:
        return [{"error": e.code, "body": e.read().decode()[:200]}]


def main(argv):
    per = 25
    if "--per-sample" in argv:
        per = int(argv[argv.index("--per-sample") + 1])
    token = access_token()
    today = datetime.date.today().isoformat()
    results = {"date": today, "site": SITE, "samples": {}}
    results["sitemaps"] = sitemaps(token)
    print("sitemaps Search Console knows:")
    for s in results["sitemaps"]:
        sub = ", ".join(f"{c.get('type')} {c.get('submitted')}" for c in s.get("contents", []))
        print(f"  {s.get('path', s)}  last read {s.get('lastDownloaded', '-')}  "
              f"errors {s.get('errors', '-')}  warnings {s.get('warnings', '-')}  {sub}")
    chosen = samples(per)
    if "--wanted" in argv:
        chosen = {"wanted": wanted()}
    if "--paths" in argv:
        chosen = {"paths": [p.strip() for p in argv[argv.index("--paths") + 1].split(",") if p.strip()]}
    for name, paths in chosen.items():
        rows = []
        for p in paths:
            r = inspect(token, BASE + p)
            rows.append({"path": p, **r})
            time.sleep(0.5)
        results["samples"][name] = rows
        verdicts = collections.Counter(r.get("coverageState") or r.get("error") or "?" for r in rows)
        states = collections.Counter(r.get("indexingState") or "-" for r in rows)
        crawls = sorted((r.get("lastCrawlTime") or "")[:10] for r in rows if r.get("lastCrawlTime"))
        since = sum(1 for c in crawls if c >= "2026-10-08")
        print(f"\n{name}: {len(rows)} page(s)")
        for k, v in verdicts.most_common():
            print(f"  verdict  {v:3d}  {k}")
        for k, v in states.most_common():
            print(f"  crawler saw  {v:3d}  {k}")
        if crawls:
            print(f"  last crawl: oldest {crawls[0]}, newest {crawls[-1]}, {since} of {len(crawls)} since 2026-10-08")
        else:
            print("  last crawl: none reported")
    outp = os.path.join(ROOT, "data", "research", f"gsc-inspection-{today}{'-wanted' if '--wanted' in argv else '-paths' if '--paths' in argv else ''}.json")
    with open(outp, "w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=1)
    print(f"\nwritten {os.path.relpath(outp, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
