"""Who are the visitors from one country: pages, referrers, browsers, OS, per day.

Written 2026-09-26 when Singapore became the biggest country in the beacon (420
visits in 8 days) while Google sent /singapore six clicks in ten days. The
question was whether those are people or machines, and the digest's country
line cannot say: it counts, it does not describe.

    CLOUDFLARE_ANALYTICS_TOKEN=... python3 scripts/country_look.py SG [US ...]

Gear, not product: reads Cloudflare's GraphQL API, prints, writes nothing.
Runs in CI through .github/workflows/country-look.yml, where the token lives.
"""
import datetime
import json
import os
import sys
import urllib.request

API = "https://api.cloudflare.com/client/v4/graphql"
FALLBACK_TAG = "3c5f7c8dd0e00e8d3ba0d0a4d1a3c5e2"
DAYS = 8
CUTS = [("pages", "requestPath", 20), ("referrers", "refererHost", 10),
        ("browsers", "userAgentBrowser", 8), ("os", "userAgentOS", 8),
        ("devices", "deviceType", 4), ("days", "date", 12)]


def gql(token, query, variables):
    req = urllib.request.Request(API, data=json.dumps(
        {"query": query, "variables": variables}).encode(), headers={
        "Authorization": "Bearer " + token, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        g = json.load(r)
    if g.get("errors"):
        raise RuntimeError(json.dumps(g["errors"])[:400])
    return g["data"]


def main(countries):
    token = os.environ.get("CLOUDFLARE_ANALYTICS_TOKEN", "").strip()
    if not token:
        print("country_look: no CLOUDFLARE_ANALYTICS_TOKEN set, skipping.")
        return 0
    tag = os.environ.get("CF_ACCOUNT_TAG", "").strip() or FALLBACK_TAG
    today = datetime.date.today()
    since = (today - datetime.timedelta(days=DAYS)).isoformat()
    for cc in countries:
        parts = []
        for alias, dim, lim in CUTS:
            order = "date_ASC" if dim == "date" else "count_DESC"
            parts.append(
                f"{alias}: rumPageloadEventsAdaptiveGroups(limit: {lim}, "
                f"filter: {{date_geq: $since, date_lt: $until, countryName: $cc}}, "
                f"orderBy: [{order}]) {{ count sum {{ visits }} dimensions {{ {dim} }} }}")
        q = ("query($tag: String!, $since: Date!, $until: Date!, $cc: String!) {"
             " viewer { accounts(filter: {accountTag: $tag}) { "
             + " ".join(parts) + " } } }")
        try:
            acct = gql(token, q, {"tag": tag, "since": since,
                                  "until": today.isoformat(), "cc": cc})
        except Exception as e:
            print(f"{cc}: unreadable: {e}")
            continue
        a = (acct["viewer"]["accounts"] or [{}])[0]
        print(f"\n===== {cc}, {since} to {today} =====")
        for alias, dim, _ in CUTS:
            print(f"-- {alias}")
            for r in a.get(alias) or []:
                v = r["dimensions"].get(dim) or "(none)"
                print(f"   {r['count']:6d} views {r['sum']['visits']:6d} visits  {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["SG"]))
