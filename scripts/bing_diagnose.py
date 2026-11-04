#!/usr/bin/env python3
"""bing_diagnose.py - where a jump in Bing's impressions came from.

Written 2026-11-04, after Bing showed 2,225 impressions on 11-01 against
85 to 130 on the days before, with 8 clicks (0.4%). Hidde: "ik denk bijna
dat het fout moet zijn. Zoek dat uit." The digest's top-query line sorts by
clicks, so a query that brings impressions and no clicks never shows there.
This prints the raw rows sorted by impressions instead, per query and per
page, and the day-by-day history of the biggest ones.

Read-only, the key is BING_API_KEY (a GitHub secret, so it runs in
.github/workflows/bing-diagnose.yml). Every section is caught on its own.
"""
import sys

from bing_search import _get, _int, key, parse_date

TOP = 25


def section(title):
    print()
    print("== " + title)


def safe(method, **params):
    try:
        return _get(method, **params)
    except Exception as e:
        print("  %s failed: %s" % (method, e))
        return []


def daily():
    section("Traffic per day (GetRankAndTrafficStats), last 30 rows")
    rows = sorted(safe("GetRankAndTrafficStats"), key=lambda r: parse_date(r.get("Date")) or "")
    for r in rows[-30:]:
        i, c = _int(r.get("Impressions")), _int(r.get("Clicks"))
        print("  %s  impressions %6d  clicks %4d" % (parse_date(r.get("Date")), i, c))


def crawl():
    section("Crawl per day (GetCrawlStats), last 14 rows")
    rows = sorted(safe("GetCrawlStats"), key=lambda r: parse_date(r.get("Date")) or "")
    for r in rows[-14:]:
        print("  %s  crawled %5d  in index %6d  2xx %5d  other %5d" % (
            parse_date(r.get("Date")), _int(r.get("CrawledPages")), _int(r.get("InIndex")),
            _int(r.get("Code2xx")), _int(r.get("AllOtherCodes"))))


def ranked(method, field):
    rows = safe(method)
    rows = sorted(rows, key=lambda r: -_int(r.get("Impressions")))
    section("%s by impressions, top %d (%d rows)" % (method, TOP, len(rows)))
    for r in rows[:TOP]:
        print("  %s  i %5d  c %3d  pos %5.1f  %s" % (
            parse_date(r.get("Date")), _int(r.get("Impressions")), _int(r.get("Clicks")),
            float(r.get("AvgImpressionPosition") or 0), str(r.get(field) or "").strip()))
    return rows


def history(method, param, values):
    for v in values:
        section("%s for %r, per day" % (method, v))
        rows = sorted(safe(method, **{param: v}), key=lambda r: parse_date(r.get("Date")) or "")
        for r in rows[-21:]:
            print("  %s  i %5d  c %3d" % (parse_date(r.get("Date")), _int(r.get("Impressions")),
                                         _int(r.get("Clicks"))))


def main():
    if not key():
        print("no BING_API_KEY")
        return 1
    daily()
    crawl()
    queries = ranked("GetQueryStats", "Query")
    pages = ranked("GetPageStats", "Query")
    history("GetQueryTrafficStats", "query",
            [str(r.get("Query")).strip() for r in queries[:5] if r.get("Query")])
    history("GetPageQueryStats", "page",
            [str(r.get("Query")).strip() for r in pages[:3] if r.get("Query")])
    return 0


if __name__ == "__main__":
    sys.exit(main())
