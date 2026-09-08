#!/usr/bin/env python3
"""Backlinks, checked by fetching the page rather than by reading referrers.

Why this exists, and it is not a nicer version of the referrer line.

On 2026-09-08 getLISBON's link to us was found live on two of their pages.
It had been up since 2026-09-04 and the digest had reported "external
referrers: none yet" every morning in between. Nothing was broken: their
link carries rel="noreferrer", which is what WordPress writes on an outbound
link by default, and noreferrer strips the referrer header, so every click
arriving from it lands in Cloudflare as "(direct)".

So the referrer table is blind to exactly the kind of link this project is
trying to win. The two mechanisms are complements rather than rivals:

  - the referrer line catches links we did not know about but that somebody
    clicked, and only when the linking page allows a referrer;
  - this catches links on pages we DO know about, clicked or not, followed
    or not.

Neither discovers an unknown link on a page nobody clicked from. That gap is
real and cannot be closed from here: Search Console's API has no links
endpoint (confirmed 2026-08-07), so the Links report stays a manual read.

Usage:
    python3 scripts/backlinks.py            # check the watch list, print the table
    python3 scripts/backlinks.py --add URL --who NAME --why TEXT
    python3 scripts/backlinks.py --quiet    # table only, for the digest
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, "data", "backlinks.json")
BLOCKLIST = os.path.join(ROOT, "data", "fetch-blocklist.json")

OUR_HOST = "ancienttrees.app"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# A hard timeout on every fetch, per CLAUDE.md: a refusal costs a second, a
# hang costs the whole window. Serialised with a pause, because a burst is how
# a polite checker turns into something a small blog blocks.
TIMEOUT = 20
PAUSE = 2.0

# One <a ...> tag containing our host, captured with its attributes and anchor
# text. Deliberately tolerant: single quotes, extra attributes, any order.
LINK_RE = re.compile(
    r"<a\s([^>]*?href=[\"'][^\"']*%s[^\"']*[\"'][^>]*)>(.{0,120}?)</a>"
    % re.escape(OUR_HOST),
    re.I | re.S)
HREF_RE = re.compile(r"href=[\"']([^\"']+)[\"']", re.I)
REL_RE = re.compile(r"\brel=[\"']([^\"']*)[\"']", re.I)
TAG_RE = re.compile(r"<[^>]+>")


def load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def blocked_hosts():
    d = load(BLOCKLIST, {})
    hosts = d.get("hosts") or d.get("blocked") or []
    out = []
    for h in hosts:
        out.append(h if isinstance(h, str) else (h.get("host") or ""))
    return [h.lower() for h in out if h]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        raw = r.read(3_000_000)
    return raw.decode("utf-8", "replace")


def links_on(html):
    """Every link to us on the page, with the one property that decides its
    SEO value: whether rel carries nofollow."""
    found = []
    for attrs, anchor in LINK_RE.findall(html):
        href = HREF_RE.search(attrs)
        if not href:
            continue
        rel_m = REL_RE.search(attrs)
        rel = rel_m.group(1).lower() if rel_m else ""
        text = " ".join(TAG_RE.sub(" ", anchor).split())[:60]
        found.append({
            "target": href.group(1),
            "rel": rel,
            "followed": "nofollow" not in rel and "sponsored" not in rel
                        and "ugc" not in rel,
            "anchor": text,
        })
    return found


def due(watch, limit):
    """The slice to check this run, least-recently-checked first.

    Fetching every watched page every morning is both slow and rude to small
    blogs. A rotation covers the whole list within a few days and costs a
    handful of requests a run, which is the right shape for something that
    changes maybe twice a month."""
    return sorted(watch, key=lambda w: w.get("checked") or "")[:limit]


def check(store, today, limit=12, verbose=True):
    """Fetch every watched page, fold what is found into `seen`.

    A page that fails to load is NOT recorded as a lost link: a 503 or a
    timeout is our problem, not theirs, and marking a live link gone on one
    bad morning would turn this table into noise."""
    bad = blocked_hosts()
    seen = store.setdefault("seen", {})
    events = []
    for item in due(store.get("watch", []), limit):
        url = item["url"]
        item["checked"] = today
        if any(b in url.lower() for b in bad):
            if verbose:
                print("  skipped (blocklist): %s" % url, file=sys.stderr)
            continue
        try:
            html = fetch(url)
        except (urllib.error.URLError, OSError, ValueError) as e:
            if verbose:
                print("  unreachable, left as-is: %s (%s)" % (url, e),
                      file=sys.stderr)
            continue
        finally:
            time.sleep(PAUSE)

        hits = links_on(html)
        prev = seen.get(url)
        if hits:
            best = sorted(hits, key=lambda h: not h["followed"])[0]
            rec = {
                "who": item.get("who", ""),
                "target": best["target"],
                "rel": best["rel"],
                "followed": best["followed"],
                "anchor": best["anchor"],
                "count": len(hits),
                "first_seen": (prev or {}).get("first_seen", today),
                "last_seen": today,
                "state": "live",
            }
            if not prev or prev.get("state") != "live":
                events.append("NEW: %s links to %s" % (url, best["target"]))
            seen[url] = rec
        elif prev and prev.get("state") == "live":
            prev["state"] = "gone"
            prev["gone_since"] = today
            events.append("GONE: %s no longer links to us" % url)
    store["checked"] = today
    return events


def table(store):
    """The digest's table. Rows only, so the caller decides the heading."""
    live = [(u, r) for u, r in (store.get("seen") or {}).items()
            if r.get("state") == "live"]
    if not live:
        return ("| (none yet) | | | |",
                0, 0)
    live.sort(key=lambda x: x[1].get("first_seen", ""))
    rows = []
    for url, r in live:
        host = url.split("//", 1)[-1].split("/", 1)[0]
        target = r["target"].split(OUR_HOST, 1)[-1] or "/"
        rows.append("| %s | %s | %s | %s |" % (
            host, target,
            "followed" if r.get("followed") else "nofollow",
            r.get("first_seen", "?")))
    followed = sum(1 for _, r in live if r.get("followed"))
    return ("\n".join(rows), len(live), followed)


def digest_section(store):
    rows, n, followed = table(store)
    head = ("| Site | Links to | rel | First seen |\n|---|---|---|---|\n"
            + rows)
    note = ("\n%d linking page(s), %d followed. Checked by fetching the page: "
            "a link with rel=\"noreferrer\" never appears in the referrer "
            "table, so these two lines measure different things and neither "
            "replaces the other. Unknown links stay a manual read of Search "
            "Console's Links report." % (n, followed))
    return "Backlinks (watched pages):\n" + head + note


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--add", help="URL of a page to watch")
    ap.add_argument("--who", default="", help="who owns it")
    ap.add_argument("--why", default="", help="why we expect a link there")
    ap.add_argument("--quiet", action="store_true",
                    help="print the digest section only")
    ap.add_argument("--no-fetch", action="store_true",
                    help="print what is stored without checking")
    ap.add_argument("--limit", type=int, default=12,
                    help="how many watched pages to fetch this run")
    ap.add_argument("--all", action="store_true",
                    help="check every watched page, ignoring the rotation")
    a = ap.parse_args()

    store = load(STORE, {"watch": [], "seen": {}})
    today = date.today().isoformat()

    if a.add:
        if any(w["url"] == a.add for w in store["watch"]):
            print("already watched")
        else:
            store["watch"].append({"url": a.add, "who": a.who, "why": a.why})
            with open(STORE, "w", encoding="utf-8") as f:
                json.dump(store, f, indent=2, ensure_ascii=False)
                f.write("\n")
            print("watching %s (%d total)" % (a.add, len(store["watch"])))
        return 0

    limit = 10 ** 6 if a.all else a.limit
    events = ([] if a.no_fetch
              else check(store, today, limit=limit, verbose=not a.quiet))
    if not a.no_fetch:
        with open(STORE, "w", encoding="utf-8") as f:
            json.dump(store, f, indent=2, ensure_ascii=False)
            f.write("\n")

    print(digest_section(store))
    for e in events:
        print(e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
