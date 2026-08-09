#!/usr/bin/env python3
"""Who actually visits, where from, in which language, on what, and what they read.

Written 2026-08-09 because Hidde asked the question and nothing answered it.
The daily digest reports volume (clicks, visits, a top five) which is the right
thing for a daily line and the wrong thing for understanding an audience. This
cuts the same two sources by audience dimensions over 28 days and writes
AUDIENCE.md.

Two honesty rules the report enforces on itself, because at these volumes a
confident dashboard would lie:
  1. Every table says how many observations it rests on. A "top country" drawn
     from nine clicks is noise wearing a hat.
  2. Cloudflare's beacon numbers before 2026-08-08 include our own CI, preview
     sessions and Hidde's browsing (DATA.md, "Break in series"). The report
     refuses to average across that date and says so.

Needs the same secrets as the digest: GSC_CLIENT_ID/SECRET/REFRESH_TOKEN and
CLOUDFLARE_ANALYTICS_TOKEN. Absent, it says which half it could not read
rather than failing.
"""
import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

SITE = "sc-domain%3Aancienttrees.app"
ACCOUNT_TAG = "3c5f7c8dd0e00e8d3ba0d0a4d1a3c5e2"   # overwritten from the digest below
CLEAN_FROM = datetime.date(2026, 8, 8)             # beacon data is ours-free from here
WINDOW = 28
OUT = "AUDIENCE.md"

# The account tag lives in the digest; read it from there rather than keeping a
# second copy that can drift.
try:
    with open(os.path.join(os.path.dirname(__file__), "daily_digest.py")) as f:
        for line in f:
            if line.startswith("ACCOUNT_TAG"):
                # The line carries a trailing comment, so cut that before the quotes.
                ACCOUNT_TAG = line.split("=", 1)[1].split("#")[0].strip().strip('"\'')
                break
except Exception:
    pass


def gsc_client(today):
    cid = os.environ.get("GSC_CLIENT_ID")
    csec = os.environ.get("GSC_CLIENT_SECRET")
    rtok = os.environ.get("GSC_REFRESH_TOKEN")
    if not (cid and csec and rtok):
        return None
    body = urllib.parse.urlencode({
        "client_id": cid, "client_secret": csec,
        "refresh_token": rtok, "grant_type": "refresh_token"}).encode()
    with urllib.request.urlopen("https://oauth2.googleapis.com/token", body, timeout=30) as r:
        access = json.load(r)["access_token"]

    start = (today - datetime.timedelta(days=WINDOW)).isoformat()
    end = today.isoformat()

    def q(dims, limit=25, extra=None):
        payload = {"startDate": start, "endDate": end, "dimensions": dims,
                   "rowLimit": limit, "dataState": "all"}
        if extra:
            payload.update(extra)
        req = urllib.request.Request(
            "https://www.googleapis.com/webmasters/v3/sites/%s/searchAnalytics/query" % SITE,
            data=json.dumps(payload).encode(),
            headers={"Authorization": "Bearer " + access, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=45) as r:
            return json.load(r).get("rows", [])
    return q


def rum(token, today):
    since = (today - datetime.timedelta(days=WINDOW)).isoformat()
    clean_since = max(CLEAN_FROM, today - datetime.timedelta(days=WINDOW)).isoformat()
    gql = """
query($tag: String!, $since: Date!, $until: Date!) {
  viewer { accounts(filter: {accountTag: $tag}) {
    countries: rumPageloadEventsAdaptiveGroups(limit: 12,
        filter: {date_geq: $since, date_lt: $until}, orderBy: [count_DESC]) {
      count dimensions { countryName } }
    devices: rumPageloadEventsAdaptiveGroups(limit: 5,
        filter: {date_geq: $since, date_lt: $until}, orderBy: [count_DESC]) {
      count dimensions { deviceType } }
    browsers: rumPageloadEventsAdaptiveGroups(limit: 8,
        filter: {date_geq: $since, date_lt: $until}, orderBy: [count_DESC]) {
      count dimensions { userAgentBrowser } }
    paths: rumPageloadEventsAdaptiveGroups(limit: 25,
        filter: {date_geq: $since, date_lt: $until}, orderBy: [count_DESC]) {
      count dimensions { requestPath } }
    refs: rumPageloadEventsAdaptiveGroups(limit: 12,
        filter: {date_geq: $since, date_lt: $until}, orderBy: [count_DESC]) {
      count dimensions { refererHost } }
    days: rumPageloadEventsAdaptiveGroups(limit: 40,
        filter: {date_geq: $since, date_lt: $until}, orderBy: [date_ASC]) {
      count dimensions { date } sum { visits } }
  } }
}"""
    req = urllib.request.Request(
        "https://api.cloudflare.com/client/v4/graphql",
        data=json.dumps({"query": gql, "variables": {
            "tag": ACCOUNT_TAG, "since": clean_since, "until": today.isoformat()}}).encode(),
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        g = json.load(r)
    if g.get("errors"):
        raise RuntimeError(json.dumps(g["errors"])[:300])
    acct = g["data"]["viewer"]["accounts"]
    return (acct[0] if acct else None), clean_since


# Which language a search was typed in. Deliberately crude and it says so:
# a handful of unmistakable markers per language, nothing clever, and anything
# unmatched counts as "unclassified" rather than being guessed into English.
MARKERS = {
    "Spanish": ["arbol", "árbol", "arboles", "árboles", "mas antiguo", "más antiguo", "viejo"],
    "Portuguese": ["arvore", "árvore", "arvores", "árvores", "mais antiga", "velha"],
    "Italian": ["albero", "alberi", "piu antico", "più antico", "secolare", "monumentale"],
    "Dutch": ["boom", "bomen", "oudste", "dikste"],
    "German": ["baum", "baume", "bäume", "alteste", "älteste"],
    "French": ["arbre", "arbres", "plus vieux", "remarquable"],
    "Japanese": ["木", "樹", "巨樹", "古木"],
    "Turkish": ["agac", "ağaç", "anitagac", "anıt ağaç"],
    "Polish": ["drzewo", "drzewa", "najstarsze"],
}
ENGLISH = ["tree", "trees", "oldest", "ancient", "biggest", "largest", "old"]


def classify(q):
    s = q.lower()
    for lang, words in MARKERS.items():
        if any(w in s for w in words):
            return lang
    if any(w in s for w in ENGLISH):
        return "English"
    return "unclassified"


def table(rows, key, label, total_label="clicks"):
    if not rows:
        return "  (no rows)\n"
    out = []
    for r in rows:
        out.append("  %-28s %5d %s, %6d impressions" % (
            (r["keys"][0] or "(none)")[:28], r["clicks"], total_label, r["impressions"]))
    return "\n".join(out) + "\n"


def main():
    today = datetime.datetime.now(datetime.timezone.utc).date()
    L = []
    L.append("# AUDIENCE — who visits, from where, in which language, on what\n")
    L.append("Generated %s, over the %d days to %s. Regenerate with the Audience\n"
             "workflow; this file is overwritten, not appended.\n" % (today.isoformat(), WINDOW, today.isoformat()))
    L.append("Read the counts before the rankings. A top row drawn from single-digit\n"
             "observations is noise, and this report prints the denominator so you can\n"
             "see when that is the case.\n")

    q = gsc_client(today)
    if q is None:
        L.append("\n## Search (Google)\n\nGSC secrets absent; this half could not be read.\n")
    else:
        countries = q(["country"], 15)
        devices = q(["device"], 5)
        pages = q(["page"], 20)
        queries = q(["query"], 100)
        tc = sum(r["clicks"] for r in countries)
        ti = sum(r["impressions"] for r in countries)
        L.append("\n## Search (Google), %d days\n" % WINDOW)
        L.append("\nTotal: **%d clicks, %d impressions**. Everything below divides these.\n" % (tc, ti))

        L.append("\n### Where they are\n```\n" + table(countries, "country", "country") + "```\n")
        L.append("\n### Phone or desktop\n```\n" + table(devices, "device", "device") + "```\n")
        L.append("\n### What they land on\n```\n" + table(pages[:20], "page", "page") + "```\n")

        langs = {}
        for r in queries:
            lang = classify(r["keys"][0])
            a = langs.setdefault(lang, {"clicks": 0, "impressions": 0, "n": 0, "sample": []})
            a["clicks"] += r["clicks"]; a["impressions"] += r["impressions"]; a["n"] += 1
            if len(a["sample"]) < 3:
                a["sample"].append(r["keys"][0])
        L.append("\n### Which language they search in\n")
        L.append("Crude keyword classification over the top %d queries, unmatched left\n"
                 "as unclassified rather than guessed.\n\n```\n" % len(queries))
        for lang, a in sorted(langs.items(), key=lambda kv: -kv[1]["impressions"]):
            L.append("  %-14s %4d queries, %4d clicks, %6d impressions   e.g. %s\n" % (
                lang, a["n"], a["clicks"], a["impressions"], "; ".join(a["sample"])[:70]))
        L.append("```\n")

        L.append("\n### What they actually type\n```\n")
        for r in queries[:25]:
            L.append("  %-40s %4d clicks, %5d impr, position %4.1f\n" % (
                r["keys"][0][:40], r["clicks"], r["impressions"], r.get("position", 0)))
        L.append("```\n")

    token = os.environ.get("CLOUDFLARE_ANALYTICS_TOKEN")
    if not token:
        L.append("\n## On the site (beacon)\n\nCloudflare token absent; this half could not be read.\n")
    else:
        try:
            a, since = rum(token, today)
        except Exception as e:
            a, since = None, None
            L.append("\n## On the site (beacon)\n\nUnreadable: %s\n" % e)
        if a:
            days = a.get("days") or []
            pv = sum(d["count"] for d in days)
            vis = sum(d["sum"]["visits"] for d in days)
            L.append("\n## On the site (beacon), from %s\n" % since)
            L.append("\nWindow starts at the analytics cleanup, not %d days back: everything\n"
                     "before 2026-08-08 counts our own CI and browsing and is not an audience.\n" % WINDOW)
            L.append("\nTotal: **%d visits, %d pageviews** (%.1f pages per visit).\n" % (
                vis, pv, (pv / vis) if vis else 0))
            for label, key, rows in [("Where they are", "countryName", a.get("countries")),
                                     ("Phone or desktop", "deviceType", a.get("devices")),
                                     ("Browser", "userAgentBrowser", a.get("browsers")),
                                     ("How they arrived", "refererHost", a.get("refs")),
                                     ("What they opened", "requestPath", a.get("paths"))]:
                L.append("\n### %s\n```\n" % label)
                for r in (rows or []):
                    v = r["dimensions"].get(key) or "(direct/none)"
                    L.append("  %-34s %5d pageviews\n" % (str(v)[:34], r["count"]))
                L.append("```\n")

    with open(OUT, "w") as f:
        f.write("".join(L))
    print("wrote %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
