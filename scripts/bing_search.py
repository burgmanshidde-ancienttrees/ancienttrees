#!/usr/bin/env python3
"""bing_search.py - what Bing shows and sends, from Bing Webmaster Tools' API.

Written 2026-10-09, the day Hidde opened the Bing dashboard and it showed 13
clicks on 231 impressions in five days: more clicks than Google was sending
in the same days, and invisible in Cloudflare's referrer table because that
rounds to tens. A number only readable on a screen is a number nobody reads,
so this puts it in the digest beside Google's.

Gear for us, hard rule 5's carve-out: read-only, stdlib urllib, nothing a
reader meets. The key is the BING_WEBMASTER_KEY secret (generated under the
gear icon in Bing Webmaster Tools, API access, API Key); with no key every
function returns None and the digest prints nothing.

Two calls on https://ssl.bing.com/webmaster/api.svc/json/:
  GetRankAndTrafficStats  one row per day: Clicks, Impressions, Date
  GetQueryStats           one row per query: Query, Clicks, Impressions,
                          AvgClickPosition, AvgImpressionPosition
Dates arrive as "/Date(1696204800000)/", milliseconds since the epoch.
"""
import datetime
import json
import os
import re
import urllib.parse
import urllib.request

SITE = "https://ancienttrees.app/"
API = "https://ssl.bing.com/webmaster/api.svc/json/"


def key():
    return os.environ.get("BING_WEBMASTER_KEY", "").strip() or None


def _get(method, **params):
    params = {"siteUrl": SITE, "apikey": key(), **params}
    url = API + method + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "ancienttrees-digest"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("d") or []


def parse_date(s):
    """'/Date(1696204800000)/' -> '2023-10-02'. Bing dates are UTC midnight."""
    m = re.search(r"-?\d+", str(s))
    if not m:
        return None
    return datetime.datetime.fromtimestamp(int(m.group()) / 1000, datetime.timezone.utc).date().isoformat()


def daily_rows(raw):
    """[{date, clicks, impressions}] sorted by date, from GetRankAndTrafficStats rows."""
    out = []
    for r in raw or []:
        d = parse_date(r.get("Date"))
        if d:
            out.append({"date": d, "clicks": int(r.get("Clicks") or 0),
                        "impressions": int(r.get("Impressions") or 0)})
    return sorted(out, key=lambda x: x["date"])


def query_rows(raw, limit=8):
    """Top queries by clicks then impressions, from GetQueryStats rows."""
    rows = [{"query": str(r.get("Query") or "").strip(), "clicks": int(r.get("Clicks") or 0),
             "impressions": int(r.get("Impressions") or 0),
             "position": float(r.get("AvgImpressionPosition") or 0)} for r in raw or []]
    rows = [r for r in rows if r["query"]]
    return sorted(rows, key=lambda r: (-r["clicks"], -r["impressions"]))[:limit]


def fetch(days=7):
    """(daily rows for the last `days` days, top queries) or None without a key."""
    if not key():
        return None
    daily = daily_rows(_get("GetRankAndTrafficStats"))
    since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    daily = [d for d in daily if d["date"] >= since]
    try:
        queries = query_rows(_get("GetQueryStats"))
    except Exception:
        queries = []
    return daily, queries


def lines(daily, queries):
    """Digest-ready markdown: one row per day, totals, top queries."""
    if not daily:
        return ["- Bing Webmaster Tools: connected, no rows for the window yet."]
    out = ["| Day | Clicks | Impressions | CTR |", "|---|---:|---:|---:|"]
    tc = ti = 0
    for d in daily:
        tc += d["clicks"]; ti += d["impressions"]
        out.append("| %s | %d | %d | %.1f%% |" % (d["date"][5:], d["clicks"], d["impressions"],
                                                   d["clicks"] * 100.0 / max(d["impressions"], 1)))
    out.append("| **%d days** | **%d** | **%d** | **%.1f%%** |" % (len(daily), tc, ti, tc * 100.0 / max(ti, 1)))
    if queries:
        out.append("- Top Bing queries: " + "; ".join(
            "%s (c%d/i%d, p%.0f)" % (q["query"], q["clicks"], q["impressions"], q["position"]) for q in queries))
    out.append("- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same "
               "index and are not in these numbers. Bing's data lags about two days.")
    return out


if __name__ == "__main__":
    got = fetch()
    if got is None:
        print("BING_WEBMASTER_KEY not set; nothing fetched")
    else:
        print("\n".join(lines(*got)))
