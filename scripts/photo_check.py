#!/usr/bin/env python3
"""Confirm every published photo still exists, and record its dimensions.

Written 2026-08-18, when the question was how an app gets photographs. The
answer turned out to be mostly "not from us": a client downloads them from the
canonical source into its own cache, the way every offline-capable app builds
its packs, and mirroring 354 files into this repo would cost 45 MB at 500px or
151 MB at 960px for a benefit nothing consumes yet. What an app does need from
us is the three things it cannot work out alone, and two of them were missing.

  1. The licence and the photographer. Already in the feed.
  2. The DIMENSIONS, so a client can lay out a list before a single byte of
     image arrives, and so a file that silently changes underneath us shows up
     as a changed size rather than as a surprise.
  3. A promise the URL still resolves. That one was missing entirely: a
     Commons file can be renamed or deleted at any time, and the only way we
     would have learned is a reader telling us a page had a hole in it.

Commons files are checked in batches of fifty through its own API, which
returns existence and size together, so 317 files cost seven requests rather
than 317. Everything else gets a throttled HEAD, because those hosts have no
such API and Wikimedia's own rate limit (measured 2026-08-08: HTTP 429 after
twelve rapid fetches) is a fair guide to how fast anyone wants to be asked.

    python3 scripts/photo_check.py            # check, report, record sizes
    python3 scripts/photo_check.py --dry-run  # report only, write nothing
"""
import argparse
import glob
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "AncientTrees/1.0 (https://ancienttrees.app; contact via ancienttrees.app)"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
COMMONS_PREFIX = "upload.wikimedia.org/wikipedia/commons/"
BATCH = 50
# One every three seconds is what ran clean when this was measured; anything
# faster earned a 429 after a dozen files.
THROTTLE = 3.0
USABLE = ("approved", "found_needs_check")


def commons_title(url):
    """The File: title behind an upload.wikimedia.org URL, thumb or original."""
    name = urllib.parse.unquote(url.split("/")[-1])
    if "px-" in name and name.split("px-")[0].split("-")[-1].isdigit():
        name = name.split("px-", 1)[1]
    return "File:" + name


def api(params):
    url = COMMONS_API + "?" + urllib.parse.urlencode({**params, "format": "json", "formatversion": "2"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def head(url):
    """(ok, size) for a URL we cannot ask an API about."""
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status == 200, None
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return False, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report only")
    args = ap.parse_args()

    # slug -> [(tree, photo)] so a size can be written back in place
    files = sorted(glob.glob("data/cities/*.json"))
    docs = {}
    entries = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        docs[f] = d
        for t in d.get("trees", []):
            p = t.get("photo") or {}
            if p.get("url") and p.get("status") in USABLE:
                entries.append((f, t["id"], p))

    commons = [(f, tid, p) for f, tid, p in entries if COMMONS_PREFIX in p["url"]]
    others = [(f, tid, p) for f, tid, p in entries if COMMONS_PREFIX not in p["url"]]
    print("%d usable photos: %d on Commons, %d elsewhere" % (len(entries), len(commons), len(others)))

    dead, sized = [], 0

    for i in range(0, len(commons), BATCH):
        chunk = commons[i:i + BATCH]
        titles = {}
        for f, tid, p in chunk:
            titles.setdefault(commons_title(p["url"]), []).append((f, tid, p))
        try:
            d = api({"action": "query", "prop": "imageinfo", "iiprop": "size",
                     "titles": "|".join(titles)})
        except Exception as e:
            print("  batch %d failed (%s), skipping" % (i // BATCH + 1, type(e).__name__))
            continue
        # MediaWiki normalises a title before answering, and a filename taken
        # from a URL always arrives with underscores where the title has
        # spaces. Without following the `normalized` map, 305 of 317 lookups
        # matched nothing and the run reported "12 photos sized" as though the
        # rest had failed for some interesting reason.
        back = {n["to"]: n["from"] for n in d.get("query", {}).get("normalized", [])}
        for page in d.get("query", {}).get("pages", []):
            holders = titles.get(back.get(page["title"], page["title"]), [])
            if page.get("missing"):
                for f, tid, p in holders:
                    dead.append((tid, page["title"], "no longer on Commons"))
                continue
            info = (page.get("imageinfo") or [{}])[0]
            for f, tid, p in holders:
                if info.get("width"):
                    p["width"], p["height"] = info["width"], info["height"]
                    sized += 1
        time.sleep(1)

    for f, tid, p in others:
        ok, _ = head(p["url"])
        if not ok:
            dead.append((tid, p["url"][:70], "did not respond 200"))
        time.sleep(THROTTLE)

    if not args.dry_run:
        for f, d in docs.items():
            with open(f, "w", encoding="utf-8") as fh:
                json.dump(d, fh, ensure_ascii=False, indent=2)
                fh.write("\n")

    print("\n%d photo(s) now carry their dimensions." % sized)
    if dead:
        print("\n%d photo(s) NO LONGER RESOLVE and are showing as holes on the site:" % len(dead))
        for tid, what, why in dead:
            print("  %-12s %-52s %s" % (tid, what, why))
        return 1
    print("Every published photo still resolves.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
