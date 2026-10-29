"""asc_reviews.py - the App Store reviews people wrote, newest first.

Hidde, 2026-10-29: "kun je ook uitlezen als we een review op apple krijgen?
zou je die ook mee willen nemen in de daily als die er is".

App Store Connect's customerReviews, all territories. Apple only hands out
reviews with a written text; a star rating without words never shows here.
The reviewer's nickname is a person's name in our sense: it stays out of
DATA.md (a public file) and is never printed here either. The local digest
page shows the words in full, like every other reader's words.

    python3 scripts/asc_reviews.py            every review, newest first
    python3 scripts/asc_reviews.py --since 2026-10-01
"""
import argparse
import sys

from asc_auth import bearer_token
from asc_downloads import API, APP_ID, _get


def reviews(since=None, limit=200):
    """[{date, rating, title, body, territory}] newest first, on or after
    `since` (YYYY-MM-DD) when given."""
    out = []
    url = "%s/apps/%s/customerReviews" % (API, APP_ID)
    params = {"sort": "-createdDate", "limit": 200,
              "fields[customerReviews]": "rating,title,body,createdDate,territory"}
    token = bearer_token()
    while url and len(out) < limit:
        doc = _get(url, token, params)
        params = None  # the next link carries its own query
        for r in doc.get("data") or []:
            a = r.get("attributes") or {}
            day = a.get("createdDate") or ""
            if since and day[:len(since)] < since:
                return out
            out.append({"date": day, "rating": a.get("rating"),
                        "title": a.get("title") or "", "body": a.get("body") or "",
                        "territory": a.get("territory") or ""})
        url = (doc.get("links") or {}).get("next")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--since")
    a = ap.parse_args()
    rows = reviews(a.since)
    if not rows:
        print("No written App Store reviews%s." % (" since " + a.since if a.since else ""))
        return 0
    for r in rows:
        print("%s  %s  %s  %s" % (r["date"][:10], "*" * int(r["rating"] or 0), r["territory"], r["title"]))
        if r["body"]:
            print("    " + r["body"].replace("\n", "\n    "))
    return 0


if __name__ == "__main__":
    sys.exit(main())
