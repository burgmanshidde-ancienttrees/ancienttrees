#!/usr/bin/env python3
"""Ask Google directly why search went quiet. Read-only, prints a report.

Written 2026-10-01 after impressions fell from ~1,900 a day to ~50 on 09-28 and
stayed there for three days, with Google referrals in our own beacon falling
alongside. A sandbox session cannot see Search Console; the digest workflow
holds the credentials, so this runs there (.github/workflows/seo-diagnose.yml).

It answers, in order:
  1. Is it every day since a date, or a reporting gap? (final vs fresh data)
  2. Did every country, device and page fall, or some? (a demotion hits all)
  3. What does Google say about our pages? (URL Inspection API)
  4. Can Google fetch the sitemaps, and when did it last? (Sitemaps API)
  5. What does the site send a crawler right now? (robots.txt, headers, meta)
  6. Did real Google visitors fall per day? (Cloudflare beacon, per day)

Never raises past a section: one failing question must not hide the others.
"""
import datetime
import json
import os
import re
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from daily_digest import api, ACCOUNT_TAG  # noqa: E402

SITE = "sc-domain:ancienttrees.app"
BASE = "https://ancienttrees.app"
INSPECT = ["/", "/prague", "/seville", "/lisbon", "/malaga", "/cities",
           "/de/vienna/chestnut-avenue-of-the-hauptallee", "/de/graz",
           "/explore", "/united-states"]
UA_BOT = ("Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/126.0 Mobile Safari/537.36 "
          "(compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
UA_HUMAN = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 Safari/605.1.15"


def token():
    body = urllib.parse.urlencode({
        "client_id": os.environ["GSC_CLIENT_ID"],
        "client_secret": os.environ["GSC_CLIENT_SECRET"],
        "refresh_token": os.environ["GSC_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    with urllib.request.urlopen("https://oauth2.googleapis.com/token", body, timeout=30) as r:
        return json.load(r)["access_token"]


def call(access, url, payload=None, method=None):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Authorization": "Bearer " + access, "Content-Type": "application/json"},
        method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def q(access, payload):
    url = ("https://www.googleapis.com/webmasters/v3/sites/%s/searchAnalytics/query"
           % urllib.parse.quote(SITE, safe=""))
    return call(access, url, payload).get("rows", [])


def section(title, fn):
    print("\n## " + title + "\n")
    try:
        fn()
    except Exception as e:  # one failing question must not hide the others
        print("FAILED: %s: %s" % (type(e).__name__, e))


def main():
    today = datetime.date.today()
    access = token()
    start = (today - datetime.timedelta(days=24)).isoformat()
    end = today.isoformat()
    split = "2026-09-28"

    def days():
        fin = {r["keys"][0]: r for r in q(access, {"startDate": start, "endDate": end,
                                                    "dimensions": ["date"], "dataState": "final"})}
        fresh = {r["keys"][0]: r for r in q(access, {"startDate": start, "endDate": end,
                                                      "dimensions": ["date"], "dataState": "all"})}
        print("| Day | Impr (final) | Impr (fresh) | Clicks (fresh) | Position |")
        print("|---|---:|---:|---:|---:|")
        for d in sorted(set(fin) | set(fresh)):
            f, a = fin.get(d), fresh.get(d)
            print("| %s | %s | %s | %s | %s |" % (
                d, int(f["impressions"]) if f else "-", int(a["impressions"]) if a else "-",
                int(a["clicks"]) if a else "-", "%.1f" % a["position"] if a else "-"))

    def split_by(dim, limit=12):
        rows_b = q(access, {"startDate": (today - datetime.timedelta(days=14)).isoformat(),
                            "endDate": "2026-09-27", "dimensions": [dim], "rowLimit": 200,
                            "dataState": "all"})
        rows_a = q(access, {"startDate": split, "endDate": end, "dimensions": [dim],
                            "rowLimit": 200, "dataState": "all"})
        nb = max(1, (datetime.date(2026, 9, 27) - (today - datetime.timedelta(days=14))).days + 1)
        na = max(1, (today - datetime.date(2026, 9, 28)).days + 1)
        after = {r["keys"][0]: r for r in rows_a}
        print("Impressions per day, before (to 09-27) and after (from 09-28):\n")
        print("| %s | Before/day | After/day | Kept |" % dim)
        print("|---|---:|---:|---:|")
        for r in sorted(rows_b, key=lambda r: -r["impressions"])[:limit]:
            k = r["keys"][0]
            b = r["impressions"] / nb
            a = after.get(k, {}).get("impressions", 0) / na
            print("| %s | %.0f | %.1f | %.0f%% |" % (k[:70], b, a, 100 * a / b if b else 0))

    def appearance():
        rows = q(access, {"startDate": start, "endDate": end,
                          "dimensions": ["searchAppearance"], "dataState": "all"})
        for r in rows:
            print("- %s: %d impressions" % (r["keys"][0], r["impressions"]))
        if not rows:
            print("(none)")

    def inspect():
        url = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
        for path in INSPECT:
            try:
                r = call(access, url, {"inspectionUrl": BASE + path, "siteUrl": SITE})
                s = r["inspectionResult"]["indexStatusResult"]
                print("- %s: verdict=%s | %s | lastCrawl=%s | fetch=%s | robots=%s | "
                      "indexing=%s | google canonical=%s | user canonical=%s" % (
                          path, s.get("verdict"), s.get("coverageState"), s.get("lastCrawlTime"),
                          s.get("pageFetchState"), s.get("robotsTxtState"),
                          s.get("indexingState"), s.get("googleCanonical"),
                          s.get("userCanonical")))
            except Exception as e:
                print("- %s: FAILED %s" % (path, e))

    def sitemaps():
        url = ("https://www.googleapis.com/webmasters/v3/sites/%s/sitemaps"
               % urllib.parse.quote(SITE, safe=""))
        for s in call(access, url).get("sitemap", []):
            c = s.get("contents") or [{}]
            print("- %s: lastSubmitted=%s lastDownloaded=%s pending=%s errors=%s warnings=%s submitted=%s" % (
                s.get("path"), s.get("lastSubmitted"), s.get("lastDownloaded"), s.get("isPending"),
                s.get("errors"), s.get("warnings"), c[0].get("submitted")))

    def live():
        for path in ["/robots.txt", "/", "/prague", "/sitemap-index.xml"]:
            for name, ua in (("human", UA_HUMAN), ("googlebot UA", UA_BOT)):
                req = urllib.request.Request(BASE + path, headers={"User-Agent": ua})
                try:
                    with urllib.request.urlopen(req, timeout=30) as r:
                        body = r.read(400000).decode("utf-8", "replace")
                        h = r.headers
                        status, url = r.status, r.geturl()
                except urllib.error.HTTPError as e:
                    body, h, status, url = e.read(2000).decode("utf-8", "replace"), e.headers, e.code, BASE + path
                meta = re.findall(r'<meta[^>]+name="robots"[^>]*>', body, re.I)
                canon = re.findall(r'<link[^>]+rel="canonical"[^>]*>', body, re.I)
                print("- %s as %s: %s final=%s x-robots=%s server=%s len=%d meta=%s canonical=%s" % (
                    path, name, status, url, h.get("x-robots-tag"), h.get("server"),
                    len(body), meta[:1], canon[:1]))
                if path == "/robots.txt" and name == "human":
                    print("```\n" + body[:1500] + "\n```")

    def beacon():
        tok = os.environ.get("CLOUDFLARE_ANALYTICS_TOKEN")
        if not tok:
            print("no CLOUDFLARE_ANALYTICS_TOKEN")
            return
        query = {"query": """
query($tag: String!, $since: Date!, $until: Date!) {
  viewer { accounts(filter: {accountTag: $tag}) {
    g: rumPageloadEventsAdaptiveGroups(limit: 200,
        filter: {date_geq: $since, date_lt: $until}, orderBy: [date_ASC]) {
      count dimensions { date refererHost }
    }
  } }
}""", "variables": {"tag": ACCOUNT_TAG, "since": start, "until": end}}
        g = api("https://api.cloudflare.com/client/v4/graphql", query, token=tok)
        if g.get("errors"):
            raise RuntimeError(json.dumps(g["errors"]))
        per = {}
        for r in g["data"]["viewer"]["accounts"][0]["g"]:
            d, host = r["dimensions"]["date"], (r["dimensions"]["refererHost"] or "")
            row = per.setdefault(d, {"google": 0, "bing": 0, "all": 0})
            row["all"] += r["count"]
            if "google." in host or "googlequicksearchbox" in host:
                row["google"] += r["count"]
            if "bing." in host:
                row["bing"] += r["count"]
        print("| Day | From Google | From Bing | All pageviews |")
        print("|---|---:|---:|---:|")
        for d in sorted(per):
            print("| %s | %d | %d | %d |" % (d, per[d]["google"], per[d]["bing"], per[d]["all"]))

    def who_is_left():
        # The digest's own beacon reader, run here so a change to it can be
        # seen against live data without waiting for the morning digest.
        from daily_digest import fetch_rum
        tok = os.environ.get("CLOUDFLARE_ANALYTICS_TOKEN")
        if not tok:
            print("no CLOUDFLARE_ANALYTICS_TOKEN")
            return
        print(fetch_rum(tok, today).split("\n\nLinks:")[0])

    print("# SEO diagnosis, %s" % today.isoformat())
    section("1. Day by day, final against fresh data", days)
    section("2a. By country", lambda: split_by("country"))
    section("2b. By device", lambda: split_by("device", 3))
    section("2c. By page", lambda: split_by("page", 20))
    section("2d. By query", lambda: split_by("query", 15))
    section("2e. Search appearance", appearance)
    section("3. What Google says about our pages (URL Inspection)", inspect)
    section("4. Sitemaps", sitemaps)
    section("5. What the site sends right now", live)
    section("6. Real visitors from search engines, per day (beacon)", beacon)
    section("7. The digest's beacon table, people only", who_is_left)


if __name__ == "__main__":
    main()
