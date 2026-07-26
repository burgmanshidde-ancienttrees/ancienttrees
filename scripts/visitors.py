"""Read the visitor trend from Cloudflare Web Analytics, for runs to carry into LOG.md.

Reads CLOUDFLARE_ANALYTICS_TOKEN from the environment (a GitHub Actions secret;
never stored in the repo). Prints a compact 7-day table of visits and page views.
Degrades silently: no token or an API refusal prints one line and exits 0, so a
run is never broken by its own eyes.

Auto-discovers the account and the site tag through the GraphQL API, so nothing
about the account is hardcoded here.
"""
import json
import os
import sys
import urllib.request
from datetime import date, timedelta

API = "https://api.cloudflare.com/client/v4/graphql"


def gql(token, query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    token = os.environ.get("CLOUDFLARE_ANALYTICS_TOKEN", "").strip()
    if not token:
        print("visitors: no CLOUDFLARE_ANALYTICS_TOKEN set, skipping.")
        return 0

    try:
        # An Account Analytics: Read token may read the data without being
        # allowed to enumerate accounts, so the tag can be supplied directly
        # (CF_ACCOUNT_TAG, plain env in the workflow: it is an id, not a secret).
        account = os.environ.get("CF_ACCOUNT_TAG", "").strip()
        if not account:
            acc = gql(token, "{ viewer { accounts { accountTag } } }")
            tags = [a["accountTag"] for a in (acc.get("data") or {}).get("viewer", {}).get("accounts", [])]
            if not tags:
                print("visitors: no CF_ACCOUNT_TAG set and token cannot enumerate accounts.")
                return 0
            account = tags[0]

        since = (date.today() - timedelta(days=7)).isoformat()
        until = date.today().isoformat()
        q = """
        query($account: String!, $since: Date!, $until: Date!) {
          viewer { accounts(filter: {accountTag: $account}) {
            rumPageloadEventsAdaptiveGroups(
              filter: {date_geq: $since, date_leq: $until},
              limit: 100, orderBy: [date_ASC]) {
              count
              sum { visits }
              dimensions { date }
            }
          } }
        }"""
        data = gql(token, q, {"account": account, "since": since, "until": until})
        if data.get("errors"):
            print(f"visitors: API refused: {data['errors'][0].get('message', 'unknown')}")
            return 0
        rows = data["data"]["viewer"]["accounts"][0]["rumPageloadEventsAdaptiveGroups"]
        if not rows:
            print(f"visitors: 0 visits recorded {since}..{until}.")
            return 0
        tv = sum(r["sum"]["visits"] for r in rows)
        tp = sum(r["count"] for r in rows)
        print(f"visitors last 7 days: {tv} visits, {tp} page views")
        for r in rows:
            print(f"  {r['dimensions']['date']}  visits {r['sum']['visits']:>4}  views {r['count']:>4}")
    except Exception as e:  # noqa: BLE001 - eyes must never break the run
        print(f"visitors: could not read analytics ({e}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
