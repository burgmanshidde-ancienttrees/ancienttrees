#!/usr/bin/env python3
"""bing_search.py - what Bing shows, sends, crawls and indexes, from Bing
Webmaster Tools' API.

Written 2026-10-09, the day Hidde opened the Bing dashboard and it showed 13
clicks on 231 impressions in five days: more clicks than Google was sending
in the same days, and invisible in Cloudflare's referrer table because that
rounds to tens. A number only readable on a screen is a number nobody reads,
so this puts it in the digest beside Google's.

Widened the same day, after the googlebot-only noindex split (2026-10-08)
left Bing as the one engine still shown 3,815 photo-less tree pages. Hidde
asked whether Bing would demote us the way Google did on 09-28, and the
honest answer was that nothing measured Bing. So the table now carries what
Bing CRAWLS and holds IN ITS INDEX beside what it shows and sends, and a
one-line watchdog fires when either the week's impressions halve or the
indexed count drops by a fifth, so a demotion is visible in DATA.md within
days rather than when somebody opens the dashboard.

Gear for us, hard rule 5's carve-out: read-only, stdlib urllib, nothing a
reader meets. The key is the BING_API_KEY secret, the same one indexnow.yml
passes (the older BING_WEBMASTER_KEY name still works); with no key every
function returns None and the digest prints one line and no table.

Three calls on https://ssl.bing.com/webmaster/api.svc/json/, the request
shape of bwt_call() in indexnow.py, 20-second timeouts:
  GetRankAndTrafficStats  one row per day: Clicks, Impressions, Date
  GetCrawlStats           one row per day: CrawledPages, InIndex, Code2xx,
                          AllOtherCodes, Date
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
TIMEOUT = 20

# The watchdog's two thresholds. Impressions: the newest seven days against
# the seven before them, under half. In index: the newest count against the
# highest of the previous seven days, down more than a fifth. Both are blunt
# on purpose; a demotion is not a subtle event (Google's took the site from
# ~2,000 impressions a day to ~50 in one step).
IMPRESSIONS_HALVED = 0.5
INDEX_DROP = 0.20


def key():
    return (os.environ.get("BING_API_KEY", "").strip()
            or os.environ.get("BING_WEBMASTER_KEY", "").strip() or None)


def _get(method, **params):
    params = {"apikey": key(), "siteUrl": SITE, **params}
    url = API + method + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "ancienttrees-digest"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8", "replace")).get("d") or []


def parse_date(s):
    """'/Date(1696204800000)/' -> '2023-10-02'. Bing dates are UTC midnight."""
    m = re.search(r"-?\d+", str(s))
    if not m:
        return None
    return datetime.datetime.fromtimestamp(int(m.group()) / 1000, datetime.timezone.utc).date().isoformat()


def _int(v):
    try:
        return int(v or 0)
    except (TypeError, ValueError):
        return 0


def daily_rows(traffic, crawl=None):
    """One row per day, sorted by date, joining traffic and crawl stats on the
    date. A day present in only one feed keeps None for the other's fields,
    so a missing crawl figure prints as a dash rather than as a zero that
    would trip the watchdog."""
    by_day = {}
    for r in traffic or []:
        d = parse_date(r.get("Date"))
        if d:
            row = by_day.setdefault(d, {"date": d, "clicks": None, "impressions": None,
                                        "crawled": None, "in_index": None})
            row["clicks"] = _int(r.get("Clicks"))
            row["impressions"] = _int(r.get("Impressions"))
    for r in crawl or []:
        d = parse_date(r.get("Date"))
        if d:
            row = by_day.setdefault(d, {"date": d, "clicks": None, "impressions": None,
                                        "crawled": None, "in_index": None})
            row["crawled"] = _int(r.get("CrawledPages"))
            row["in_index"] = _int(r.get("InIndex"))
    return [by_day[d] for d in sorted(by_day)]


def split_window(rows, days=7):
    """(newest `days` rows, the `days` before them). Rows, not calendar days:
    Bing's data lags about two days, so a calendar filter on "the last 7
    days" would print five rows and call it a week."""
    rows = [r for r in rows if r.get("impressions") is not None or r.get("in_index") is not None]
    return rows[-days:], rows[-2 * days:-days]


def query_rows(raw, limit=8):
    """Top queries by clicks then impressions, from GetQueryStats rows."""
    rows = [{"query": str(r.get("Query") or "").strip(), "clicks": _int(r.get("Clicks")),
             "impressions": _int(r.get("Impressions")),
             "position": float(r.get("AvgImpressionPosition") or 0)} for r in raw or []]
    rows = [r for r in rows if r["query"]]
    return sorted(rows, key=lambda r: (-r["clicks"], -r["impressions"]))[:limit]


def fetch(days=7):
    """(this week's rows, last week's rows, top queries) or None without a key.
    Traffic is the call that must succeed; crawl stats and queries degrade
    to empty, because a table with two of four columns beats no table."""
    if not key():
        return None
    traffic = _get("GetRankAndTrafficStats")
    try:
        crawl = _get("GetCrawlStats")
    except Exception:
        crawl = []
    this_week, last_week = split_window(daily_rows(traffic, crawl), days)
    try:
        queries = query_rows(_get("GetQueryStats"))
    except Exception:
        queries = []
    return this_week, last_week, queries


def _sum(rows, field):
    return sum(r[field] or 0 for r in rows)


def _latest(rows, field):
    for r in reversed(rows):
        if r.get(field) is not None:
            return r[field]
    return None


def watchdog(this_week, last_week):
    """The one line under the table, or None when nothing moved.

    Impressions: this window under half of the previous one (both need data).
    In index: the newest count more than a fifth below the previous window's
    highest. Either alone fires; both print on one line."""
    alarms = []
    now_imp, then_imp = _sum(this_week, "impressions"), _sum(last_week, "impressions")
    if last_week and then_imp > 0 and now_imp < then_imp * IMPRESSIONS_HALVED:
        alarms.append("impressions fell from %d to %d week on week" % (then_imp, now_imp))
    now_idx = _latest(this_week, "in_index")
    prev = [r["in_index"] for r in last_week if r.get("in_index") is not None]
    if now_idx is not None and prev:
        peak = max(prev)
        if peak > 0 and now_idx < peak * (1 - INDEX_DROP):
            alarms.append("pages in Bing's index fell from %d to %d" % (peak, now_idx))
    if not alarms:
        return None
    return ("- **BING WATCHDOG:** " + "; ".join(alarms)
            + ". That is the shape of a demotion; read the Bing Webmaster dashboard today.")


def _cell(v):
    return "-" if v is None else "%d" % v


def lines(this_week, last_week, queries):
    """Digest-ready markdown: one row per day, totals, the watchdog line when
    it fires, then top queries and the standing note."""
    if not this_week:
        return ["- Bing Webmaster Tools: connected, no rows for the window yet."]
    out = ["| Day | Impressions | Clicks | CTR | Pages crawled | Pages in index |",
           "|---|---:|---:|---:|---:|---:|"]
    for d in this_week:
        imp, clk = d["impressions"] or 0, d["clicks"] or 0
        out.append("| %s | %s | %s | %.1f%% | %s | %s |" % (
            d["date"][5:], _cell(d["impressions"]), _cell(d["clicks"]),
            clk * 100.0 / max(imp, 1), _cell(d["crawled"]), _cell(d["in_index"])))
    ti, tc = _sum(this_week, "impressions"), _sum(this_week, "clicks")
    out.append("| **%d days** | **%d** | **%d** | **%.1f%%** | **%d** | **%s** |" % (
        len(this_week), ti, tc, tc * 100.0 / max(ti, 1), _sum(this_week, "crawled"),
        _cell(_latest(this_week, "in_index"))))
    alarm = watchdog(this_week, last_week)
    if alarm:
        out.append(alarm)
    elif last_week:
        out.append("- Week before: %d impressions, %d clicks; in index then: %s. No Bing demotion in sight."
                   % (_sum(last_week, "impressions"), _sum(last_week, "clicks"),
                      _cell(_latest(last_week, "in_index"))))
    if queries:
        out.append("- Top Bing queries: " + "; ".join(
            "%s (c%d/i%d, p%.0f)" % (q["query"], q["clicks"], q["impressions"], q["position"]) for q in queries))
    out.append("- Bing alone, from Bing Webmaster Tools; the in-index column is the "
               "last day's count. DuckDuckGo and Yahoo draw on the same index and are "
               "not in these numbers. Bing's data lags about two days.")
    return out


if __name__ == "__main__":
    got = fetch()
    if got is None:
        print("BING_API_KEY not set; nothing fetched")
    else:
        print("\n".join(lines(*got)))
