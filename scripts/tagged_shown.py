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
EARNED = os.path.join(ROOT, "data", "earned-back.json")
SINCE = "2026-11-01"

# EARNED BACK (Hidde, 2026-11-04: "Ja, bouw de regel"). A tagged page Google
# keeps showing with clicks has answered the question the cut asked, so it
# leaves the noindex list: 2 clicks since SINCE, or 1 click and 10
# impressions. One click alone is luck (24 of the first 31 clicks fell on
# pages with under five impressions). Never a translation or a question
# page: machine translation at scale is what Google's scaled-content policy
# names, and a question page repeats its city's FAQ. The list only grows, so
# a page that came back does not go dark again the day it stops being
# tagged; thin_pages.py reads it (EARNED_BACK) and the release lane still
# meters what enters. Removing a page from data/earned-back.json undoes it.
# Widened 2026-11-05 (Hidde: "zolang google weer impressies heeft op paginas
# voegen we die ook toe", choosing 3+ impressions over every page shown): a
# page Google keeps showing 3 times since SINCE has been read and approved by
# Google after the recovery, so our tag would only take away what Google gave
# back. Daily, so a page that reaches 3 later is added later. 176 English tree
# and place pages qualified that day; the release lane still lets at most 70
# into Google per build.
EARNED_CLICKS = 2
EARNED_ONE_CLICK_IMPRESSIONS = 10
EARNED_IMPRESSIONS = 3
LANGS = {"de", "es", "fr", "it", "ja", "nl", "pt"}
QSLUGS = {"oldest-tree", "aeltester-baum", "arbol-mas-antiguo", "arbre-le-plus-vieux",
          "albero-piu-antico", "saiko-rei-no-ki", "oudste-boom", "arvore-mais-antiga"}


LISTINGS = {"species", "parks", "collections", "united-states", "countries"}
# A creep guard: the rule never becomes a way back for a whole group. 10 on
# 2026-11-04; 250 from 2026-11-05 with the 3-impression rule (Hidde), the
# per-build pace is the release lane's 70.
EARNED_PER_WEEK = 250


def may_earn(p):
    seg = [x for x in p["path"].split("/") if x]
    if not seg or seg[0] in LANGS or seg[0] in LISTINGS or seg[-1] in QSLUGS:
        return False
    return p["clicks"] >= EARNED_CLICKS or p["impressions"] >= EARNED_IMPRESSIONS or (
        p["clicks"] >= 1 and p["impressions"] >= EARNED_ONE_CLICK_IMPRESSIONS)


def record_earned(pages, today):
    try:
        with open(EARNED) as f:
            doc = json.load(f)
    except (OSError, ValueError):
        doc = {}
    earned = doc.get("pages") or {}
    week_ago = (datetime.date.fromisoformat(today) - datetime.timedelta(days=7)).isoformat()
    room = EARNED_PER_WEEK - sum(1 for v in earned.values() if v.get("date", "") > week_ago)
    new = []
    for p in pages:  # most clicks first, so the cap keeps the strongest
        if len(new) >= room:
            break
        if p["path"] not in earned and may_earn(p):
            earned[p["path"]] = {"date": today, "impressions": p["impressions"], "clicks": p["clicks"]}
            new.append(p["path"])
    with open(EARNED, "w") as f:
        json.dump({"generated": "scripts/tagged_shown.py",
                   "rule": "3 impressions or 2 clicks since %s, or 1 click and %d impressions; never a translation, "
                           "a question page or a listing page; at most %d a week (Hidde, 2026-11-04; 3 impressions from 2026-11-05)"
                           % (SINCE, EARNED_ONE_CLICK_IMPRESSIONS, EARNED_PER_WEEK),
                   "pages": dict(sorted(earned.items()))}, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return new


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
    new = record_earned(ordered, datetime.date.today().isoformat())
    print("earned back today: %d (%s)" % (len(new), ", ".join(new) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
