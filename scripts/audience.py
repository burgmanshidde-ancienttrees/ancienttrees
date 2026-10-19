#!/usr/bin/env python3
"""Who actually visits, where from, in which language, on what, and what they read.

Written 2026-08-09 because Hidde asked the question and nothing answered it.
The daily digest reports volume (clicks, visits, a top five) which is the right
thing for a daily line and the wrong thing for understanding an audience. This
cuts Search Console by audience dimensions over 28 days and writes
AUDIENCE.md. (Its Cloudflare half left with Cloudflare on 2026-10-19; Google
Analytics covers the on-site side in the digest.)

The honesty rule the report enforces on itself, because at these volumes a
confident dashboard would lie: every table says how many observations it rests
on. A "top country" drawn from nine clicks is noise wearing a hat.

Needs the digest's Search Console secrets: GSC_CLIENT_ID/SECRET/REFRESH_TOKEN.
Absent, it says so rather than failing.
"""
import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

SITE = "sc-domain%3Aancienttrees.app"
WINDOW = 28
OUT = "AUDIENCE.md"


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

    with open(OUT, "w") as f:
        f.write("".join(L))
    print("wrote %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
