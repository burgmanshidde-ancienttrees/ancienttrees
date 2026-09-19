#!/usr/bin/env python3
"""The tree-of-the-year contests, read as a supply line instead of by accident.

Hidde, 2026-09-18: "There is a tree of the year contest is that a database we
can use". The honest answer is no and yes. No, because there is no file, no
API, no coordinate and no licence anywhere near it, and the photographs belong
to the people who entered them. Yes, because a contest is a NOMINATION LIST,
and a national vote is the closest thing to the reader validation ruled on
2026-09-08 that exists before we have readers. Somebody stood in front of that
tree, wrote down why it mattered, and then thousands of people agreed.

We have been living off this source without saying so: 100 published trees
across 93 places already cite a tree-of-the-year award, and they arrived one at
a time, found by hand, mostly as a sentence in somebody else's article. The
archives behind them hold ten to twelve finalists a year, some back to 2002,
and nothing here has ever read one as a list.

Three commands, and the split between them is this project's usual one:
retrieval is the script's, judgement is the run's.

    python3 scripts/toty_scout.py --list          the ledger, offline
    python3 scripts/toty_scout.py --gap           what we hold per country, offline
    python3 scripts/toty_scout.py --fetch hungary fetches the archive pages

--fetch deliberately does NOT parse a contest's HTML into leads. Every one of
these sites is a different CMS, none of them is stable across a decade, and a
scraper written against a page nobody has looked at is a scraper that invents
trees. It saves the readable text of each year's page into data/research/toty/
and stops there. The run reads that file and writes the leads itself, which is
the same shape as the photo viewing pass: the script fetches, the eyes judge.
"""
import argparse
import glob
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "data", "toty-contests.json")
OUT = os.path.join(ROOT, "data", "research", "toty")
UA = "AncientTreesBot/1.0 (https://ancienttrees.app; tree of the year scout)"
TIMEOUT = 20        # a host that hangs costs the whole window (CLAUDE.md)
PAUSE = 1.5

# The award words our own pages already use, one per contest language. Used by
# --gap to count what we hold, and kept beside the ledger rather than inside a
# country entry because a Czech award gets cited on a Slovak tree's page.
AWARD_WORDS = [
    "tree of the year", "strom roku", "strom roka", "drzewo roku",
    "drzewem roku", "arbol del ano", "árbol del año", "albero dell'anno",
    "arbre de l'annee", "arbre de l'année", "boom van het jaar", "ev faja",
    "év fája", "aasta puu", "metu medis", "metų medis", "arborele anului",
    "drevo leta", "darvo s koren", "дърво с корен",
]


def ledger():
    with open(LEDGER, encoding="utf-8") as f:
        return json.load(f)


def blocked_hosts():
    p = os.path.join(ROOT, "data", "fetch-blocklist.json")
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
    except (OSError, ValueError):
        return set()
    rows = d.get("hosts", d) if isinstance(d, dict) else d
    out = set()
    for r in rows:
        h = r.get("host") if isinstance(r, dict) else r
        if h:
            out.add(h.lower())
    return out


def text_of(page):
    """The readable text of an HTML page, in the order a reader meets it.

    Not a parser. It drops script and style outright, turns block tags into
    line breaks so a list of finalists does not arrive as one paragraph, and
    unescapes entities so a Hungarian name survives.
    """
    page = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", " ", page)
    page = re.sub(r"(?is)<!--.*?-->", " ", page)
    page = re.sub(r"(?i)<(br|/p|/div|/li|/h[1-6]|/tr)\b[^>]*>", "\n", page)
    page = re.sub(r"(?s)<[^>]+>", " ", page)
    page = html.unescape(page)
    page = re.sub(r"[ \t\r\f\v]+", " ", page)
    page = re.sub(r"\n\s*\n\s*\n+", "\n\n", page)
    return "\n".join(ln.strip() for ln in page.split("\n")).strip()


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        raw = r.read()
    enc = "utf-8"
    m = re.search(rb'charset=["\']?([\w-]+)', raw[:4000], re.I)
    if m:
        enc = m.group(1).decode("ascii", "ignore")
    return raw.decode(enc, "replace")


def published_counts():
    """Trees per country, and how many of them already cite an award."""
    per, awarded = {}, {}
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        c = d.get("country", "?")
        per[c] = per.get(c, 0) + len(d.get("trees", []))
        for t in d.get("trees", []):
            blob = json.dumps(t, ensure_ascii=False).lower()
            if any(w in blob for w in AWARD_WORDS):
                awarded[c] = awarded.get(c, 0) + 1
    return per, awarded


def open_leads(country):
    f = os.path.join(ROOT, "data", "leads",
                     "_famous-%s.json" % country.lower().replace(" ", "-"))
    try:
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
    except (OSError, ValueError):
        return None
    return sum(1 for l in d.get("leads", []) if l.get("status") == "lead")


def cmd_list(_args):
    d = ledger()
    print(d["note"])
    print()
    print("%-16s %-24s %-11s %-9s %s" % ("COUNTRY", "CONTEST", "KIND", "STATUS", "ARCHIVE"))
    for c in d["contests"]:
        print("%-16s %-24s %-11s %-9s %s"
              % (c["country"][:16], c["contest"][:24], c["kind"],
                 c["status"][:9], (c.get("archive") or "-")[:60]))
    print()
    print("THE TRAP: " + d["the_trap"])
    print()
    print("LICENCE: " + d["licence"])
    return 0


def cmd_gap(_args):
    d = ledger()
    per, awarded = published_counts()
    print("What we already hold in the countries that run an individual-tree contest.")
    print("'award' counts published trees whose own record cites one.\n")
    print("%-16s %-24s %7s %7s %7s  %s"
          % ("COUNTRY", "CONTEST", "TREES", "AWARD", "LEADS", "STATUS"))
    total_award = 0
    for c in d["contests"]:
        if c["kind"] == "species" or c["country"] == "Europe":
            continue
        co = c["country"]
        a = awarded.get(co, 0)
        total_award += a
        ol = open_leads(co)
        print("%-16s %-24s %7d %7d %7s  %s"
              % (co[:16], c["contest"][:24], per.get(co, 0), a,
                 "-" if ol is None else ol, c["status"]))
    print("\nacross every country: %d published trees cite a tree-of-the-year award"
          % sum(awarded.values()))
    print("excluded as species awards, not trees: %s"
          % ", ".join(c["country"] for c in d["contests"] if c["kind"] == "species"))
    return 0


def cmd_fetch(args):
    d = ledger()
    want = args.fetch.lower()
    hit = [c for c in d["contests"] if c["country"].lower() == want]
    if not hit:
        print("no contest for %r. Try --list." % args.fetch)
        return 1
    c = hit[0]
    if c["kind"] == "species":
        print("%s's %s is a SPECIES award. Nothing to fetch, by design."
              % (c["country"], c["contest"]))
        return 1
    if not c.get("year_url"):
        print("%s: no per-year url established (status %s)."
              % (c["country"], c["status"]))
        print("  note: %s" % c["note"])
        if c.get("archive"):
            print("  the archive page is %s; fetch it by hand first and add the"
                  " pattern to data/toty-contests.json." % c["archive"])
        return 1

    lo, hi = (int(x) for x in args.years.split("-"))
    host = re.sub(r"^https?://([^/]+)/.*$", r"\1", c["year_url"]).lower()
    if host in blocked_hosts():
        print("%s is on data/fetch-blocklist.json. Not fetching." % host)
        return 1

    os.makedirs(OUT, exist_ok=True)
    slug = c["country"].lower().replace(" ", "-")
    path = os.path.join(OUT, "%s.md" % slug)
    got, failed = [], []
    parts = ["# %s: %s\n" % (c["country"], c["contest"]),
             "Fetched by scripts/toty_scout.py. Raw page text, nothing parsed.",
             "Source: %s\n" % c["year_url"]]
    for year in range(lo, hi + 1):
        url = c["year_url"].format(year=year)
        try:
            body = text_of(fetch(url))
        except (urllib.error.URLError, OSError, ValueError) as e:
            failed.append((year, str(e)[:60]))
            print("  %d  FAILED  %s" % (year, str(e)[:60]))
            time.sleep(PAUSE)
            continue
        got.append((year, len(body)))
        print("  %d  %6d chars  %s" % (year, len(body), url))
        parts.append("\n## %d\n\n%s\n\n%s" % (year, url, body))
        time.sleep(PAUSE)

    if not got:
        print("\nnothing fetched. Leaving %s alone." % path)
        return 1
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts) + "\n")
    print("\n%d years fetched, %d failed -> %s" % (len(got), len(failed), path))
    print("Now READ it and write the leads yourself: a name, a place, the year,"
          " the contest and the url. No coordinate and no species unless the"
          " page states one.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--list", action="store_true", help="the ledger")
    ap.add_argument("--gap", action="store_true", help="what we already hold")
    ap.add_argument("--fetch", metavar="COUNTRY", help="fetch that archive")
    ap.add_argument("--years", default="2011-2026", help="e.g. 2011-2026")
    args = ap.parse_args()
    if args.fetch:
        return cmd_fetch(args)
    if args.gap:
        return cmd_gap(args)
    return cmd_list(args)


if __name__ == "__main__":
    sys.exit(main())
