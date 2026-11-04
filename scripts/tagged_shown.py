#!/usr/bin/env python3
"""tagged_shown.py - the pages on the noindex list that Google still shows.

Written 2026-11-04. Google's impressions came back on 11-01 (position ~25 to
~9 across the site), and among the pages earning them were pages that carry
the googlebot noindex: Google keeps showing a tagged page until it recrawls
it. Hidde asked whether that means we take well-performing pages out of
Google; the answer agreed that day was to change nothing until the recovery
has held about two weeks (to about 11-17) and meanwhile keep this list, so
the first step back can start from pages Google has shown rather than from a
guess ("Ja, bijhouden").

A data file only, not a digest block (a new block needs his yes). It writes
data/tagged-still-shown.json: per tagged path, impressions and clicks since
SINCE, the days it was seen, and the first and last of them. A page that
drops out of Google stops gaining days; that is the recrawl reading the tag.

Read-only against Search Console, same three GSC_* secrets as the digest;
without them it prints one line and leaves the file as it was.
"""
import datetime
import json
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_diagnose import q, token  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "tagged-still-shown.json")
SINCE = "2026-11-01"


def tagged_paths():
    with open(os.path.join(ROOT, "data", "noindex.json")) as f:
        data = json.load(f)
    paths = data.get("paths", []) if isinstance(data, dict) else data
    return {p.rstrip("/") or "/" for p in paths}


def main():
    if not all(os.environ.get(k) for k in ("GSC_CLIENT_ID", "GSC_CLIENT_SECRET", "GSC_REFRESH_TOKEN")):
        print("tagged_shown: no Search Console credentials, file left as it was")
        return 0
    tagged = tagged_paths()
    rows = q(token(), {"startDate": SINCE, "endDate": datetime.date.today().isoformat(),
                       "dimensions": ["date", "page"], "rowLimit": 25000, "dataState": "all"})
    pages = {}
    for r in rows:
        day, url = r["keys"]
        path = urllib.parse.urlparse(url).path.rstrip("/") or "/"
        if path not in tagged:
            continue
        p = pages.setdefault(path, {"path": path, "impressions": 0, "clicks": 0, "days": []})
        p["impressions"] += int(r.get("impressions", 0))
        p["clicks"] += int(r.get("clicks", 0))
        p["days"].append(day)
    for p in pages.values():
        p["days"] = sorted(set(p["days"]))
        p["first_day"], p["last_day"] = p["days"][0], p["days"][-1]
    ordered = sorted(pages.values(), key=lambda p: (-p["clicks"], -p["impressions"], p["path"]))
    newest = max((r["keys"][0] for r in rows), default=None)
    with open(OUT, "w") as f:
        json.dump({"generated": "scripts/tagged_shown.py",
                   "since": SINCE, "google_data_through": newest,
                   "tagged_pages_shown": len(ordered),
                   "impressions": sum(p["impressions"] for p in ordered),
                   "clicks": sum(p["clicks"] for p in ordered),
                   "pages": ordered}, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("tagged_shown: %d tagged pages shown since %s, %d impressions, %d clicks (Google through %s)"
          % (len(ordered), SINCE, sum(p["impressions"] for p in ordered),
             sum(p["clicks"] for p in ordered), newest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
