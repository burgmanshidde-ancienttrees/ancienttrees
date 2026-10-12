#!/usr/bin/env python3
"""Google Analytics for the daily digest (Hidde, 2026-10-12: "id rather use
google analytics im used to it").

Reads property 558526877 through the GA4 Data API with a read-only OAuth
refresh token (GA_CLIENT_ID / GA_CLIENT_SECRET / GA_REFRESH_TOKEN, minted by
scripts/ga_auth.py because the Cloud organisation blocks service-account
keys). On the Mac it falls back to ~/.ancienttrees-ga.env.

GA only sees visitors who pressed Accept on the cookie bar, so every table
here is a sample of the site, not a count of it; Cloudflare's beacon stays
the count until the two have run side by side (from 2026-10-12).

    python3 scripts/ga_report.py          prints the digest block
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

PROPERTY = "558526877"
API = "https://analyticsdata.googleapis.com/v1beta/properties/%s:runReport" % PROPERTY


def creds():
    keys = ("GA_CLIENT_ID", "GA_CLIENT_SECRET", "GA_REFRESH_TOKEN")
    got = {k: os.environ.get(k) for k in keys}
    if not all(got.values()):
        f = Path.home() / ".ancienttrees-ga.env"
        if f.exists():
            for line in f.read_text().split():
                k, _, v = line.partition("=")
                if k in keys and not got.get(k):
                    got[k] = v
    return got if all(got.values()) else None


def _token(c):
    body = urllib.parse.urlencode({
        "client_id": c["GA_CLIENT_ID"], "client_secret": c["GA_CLIENT_SECRET"],
        "refresh_token": c["GA_REFRESH_TOKEN"], "grant_type": "refresh_token",
    }).encode()
    with urllib.request.urlopen("https://oauth2.googleapis.com/token", body, timeout=30) as r:
        return json.loads(r.read())["access_token"]


def _report(tok, body):
    req = urllib.request.Request(API, data=json.dumps(body).encode(), headers={
        "Authorization": "Bearer " + tok, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.loads(r.read())
    rows = []
    for row in out.get("rows", []):
        rows.append([d["value"] for d in row.get("dimensionValues", [])] +
                    [m["value"] for m in row.get("metricValues", [])])
    return rows


def fetch(days=7):
    c = creds()
    if not c:
        return None
    tok = _token(c)
    rng = [{"startDate": "%ddaysAgo" % days, "endDate": "yesterday"}]
    daily = _report(tok, {
        "dateRanges": rng, "dimensions": [{"name": "date"}],
        "metrics": [{"name": "activeUsers"}, {"name": "newUsers"}, {"name": "sessions"},
                    {"name": "screenPageViews"}, {"name": "engagedSessions"}],
        "orderBys": [{"dimension": {"dimensionName": "date"}}]})
    pages = _report(tok, {
        "dateRanges": rng, "dimensions": [{"name": "pagePath"}],
        "metrics": [{"name": "screenPageViews"}, {"name": "activeUsers"}],
        "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}], "limit": 10})
    sources = _report(tok, {
        "dateRanges": rng, "dimensions": [{"name": "sessionSource"}, {"name": "sessionMedium"}],
        "metrics": [{"name": "sessions"}, {"name": "activeUsers"}],
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}], "limit": 8})
    returning = _report(tok, {
        "dateRanges": [{"startDate": "28daysAgo", "endDate": "yesterday"}],
        "dimensions": [{"name": "newVsReturning"}], "metrics": [{"name": "activeUsers"}]})
    return daily, pages, sources, returning


def lines(daily, pages, sources, returning):
    out = []
    if not daily:
        return ["- No visitor has accepted the cookie bar yet, so Google Analytics has nothing to report."]
    out += ["| Day | People | New | Returning | Visits | Pageviews | Engaged visits |",
            "|---|---:|---:|---:|---:|---:|---:|"]
    tot = [0, 0, 0, 0, 0]
    for d, users, new, sess, pv, eng in daily:
        u, n, s, p, e = (int(x) for x in (users, new, sess, pv, eng))
        tot = [a + b for a, b in zip(tot, (u, n, s, p, e))]
        out.append("| %s-%s | %d | %d | %d | %d | %d | %d |" % (d[4:6], d[6:8], u, n, max(u - n, 0), s, p, e))
    out.append("| **window** | | **%d** | | **%d** | **%d** | **%d** |" % (tot[1], tot[2], tot[3], tot[4]))
    out.append("- People per day are not summed: one person on two days is one person, and GA counts them once per day.")
    if returning:
        r = {k: int(v) for k, v in returning}
        new, back = r.get("new", 0), r.get("returning", 0)
        if new + back:
            out.append("- Coming back (28 days): %d returning against %d new, %d%% of the people GA saw."
                       % (back, new, round(100 * back / (new + back))))
    if pages:
        out += ["", "| Page | Pageviews | People |", "|---|---:|---:|"]
        out += ["| %s | %s | %s |" % (p[:70], v, u) for p, v, u in pages]
    if sources:
        out += ["", "| Came from | Visits | People |", "|---|---:|---:|"]
        out += ["| %s / %s | %s | %s |" % (s, m, v, u) for s, m, v, u in sources]
    out.append("- GA sees only visitors who pressed Accept on the cookie bar; read it as a sample. Cloudflare's table stays the count.")
    return out


def main():
    got = fetch()
    if got is None:
        print("GA credentials not found (GA_CLIENT_ID / GA_CLIENT_SECRET / GA_REFRESH_TOKEN)")
        return 1
    print("\n".join(lines(*got)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
