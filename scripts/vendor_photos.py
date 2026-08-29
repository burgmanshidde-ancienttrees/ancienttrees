#!/usr/bin/env python3
"""Copy the photographs onto our own domain, because Wikimedia rate-limits.

Hidde, 2026-08-27: the tree photographs stopped loading in the app. Measured
the same hour, a burst of 24 thumbnails fetched the way a card grid fetches
them came back 13 x HTTP 429 and 11 x 200. Wikimedia does not block us and
never has; it rate-limits, which CURATION.md recorded on 2026-08-08 as
"roughly one request every three seconds runs clean". Nothing broke. The app
grew past the threshold: more photographs, more cities, and shelves that put
ten cards on screen at once.

Serving them ourselves is the only fix that removes the cause. A retrying
image loader in the app treats the symptom and keeps the dependency; loading
fewer at a time makes the app worse to use.

Licences: every Creative Commons and public-domain licence here permits
redistribution, and attribution is unaffected because the credit lives in the
tree data and renders from there either way. Anything that does NOT permit it
is skipped by name rather than by guess, and the skip is printed.

Rate: one request every RATE seconds, single-threaded, on purpose. This script
is the thing that must not get rate-limited, and it runs once.

Usage:
  python3 scripts/vendor_photos.py --dry-run     # what it would do
  python3 scripts/vendor_photos.py               # fetch what is missing
  python3 scripts/vendor_photos.py --limit 20    # a slice
"""
import argparse
import glob
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "public", "photos")
RATE = 3.0
UA = "AncientTrees/1.0 (https://ancienttrees.app; info@ancienttrees.app) photo-vendoring"

# The CARD size only, and that is the whole point rather than a saving.
#
# The bug is a burst: a grid asks for two dozen images at once and Wikimedia
# rate-limits everything past about twelve. A hero does not burst. Checked in
# the app before deciding: `.full` (960) is read on exactly one screen,
# TreeDetail, one image at a time, while `.card` (500) is what Home's shelves,
# the map list and Collect all load by the screenful.
#
# So vendoring the hero as well would have tripled the repository to roughly
# 308 MB to fix a problem the hero does not have. 500 only, at Wikimedia's own
# rendering, is 62 MB and fixes the thing that is actually broken.
WIDTHS = (500,)

# A licence that does not permit us to host a copy. Matched on the recorded
# licence string, and anything unrecognised is skipped rather than assumed.
def may_rehost(lic):
    l = (lic or "").strip().lower()
    if not l:
        return False, "no licence recorded"
    if "all rights reserved" in l:
        return False, "all rights reserved"
    if l.startswith("cc0") or l.startswith("cc by") or "public domain" in l:
        return True, ""
    if l.startswith("kogl"):          # Korea Open Government Licence Type 1
        return True, ""
    if "own photograph" in l:
        return True, ""
    if "permission" in l:
        # Written permission to use the photograph covers hosting it.
        #
        # This said the opposite for one afternoon, and Hidde corrected it:
        # "daar hadden ze al toestemming voor gegeven". He is right, and the
        # caution was not merely redundant, it was backwards. Somebody who
        # says "use my photograph on your page" does not mean "and fetch it
        # from my server every time"; keeping our own copy is the politer half
        # of the arrangement, not the bolder one. mailcheck.py agreed from the
        # other direction and refused the mail as ASKING TWICE, which is the
        # thing most likely to lose a contributor who has already said yes.
        return True, ""
    return False, "licence not recognised: %s" % lic


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s[:48]


def wikimedia_at(url, width):
    """Wikimedia's own thumbnail URL at this width, or None if not Wikimedia.

    Only the buckets Wikimedia actually serves: probed 2026-07-31 and recorded
    in images.ts, 250/330/500/960 are live and 400/800 return 400s."""
    if "upload.wikimedia.org/wikipedia/commons/" not in url or "/thumb/" in url:
        return None
    head, _, tail = url.partition("/wikipedia/commons/")
    fname = tail.split("/")[-1]
    if not re.search(r"\.(jpe?g|png|gif)$", fname, re.I):
        return None
    buckets = [250, 330, 500, 960]
    w = next((b for b in buckets if width <= b), 960)
    return "%s/wikipedia/commons/thumb/%s/%dpx-%s" % (head, tail, w, fname)


def fetch(url, tries=3):
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 10 * (a + 1)
                print("    429, backing off %ds" % wait, flush=True)
                time.sleep(wait)
                continue
            raise
        except Exception:
            time.sleep(4 * (a + 1))
    return None


def write_manifest():
    """Map each original photo URL to its vendored basename.

    thumbUrl() takes (url, width) and nothing else, which is what makes it a
    pure function both surfaces can share. It cannot know a tree id, so the
    lookup has to arrive as data. Built from what is actually on disk rather
    than from what the fetch intended, so a half-finished run produces a
    manifest that is true rather than one that promises files that are not
    there.
    """
    on_disk = set(os.listdir(OUT))
    man = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        with open(f, encoding="utf-8") as fh:
            city = json.load(fh)
        for t in city.get("trees", []):
            p = t.get("photo") or {}
            if not p.get("url"):
                continue
            base = "%s-%s" % (t["id"], slugify(t.get("name")))
            widths = [w for w in WIDTHS if "%s-%d.jpg" % (base, w) in on_disk]
            if widths:
                man[p["url"]] = {"base": base, "widths": widths}
    out = os.path.join(ROOT, "data", "photo-manifest.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"_note": "Original photo URL -> the vendored copy under "
                            "site/public/photos. Written by scripts/vendor_photos.py "
                            "--manifest from the files actually on disk. thumbUrl() "
                            "reads it so the website and the app feed both point at "
                            "our own domain instead of at Wikimedia, which rate-limits "
                            "a card grid into HTTP 429.",
                   "photos": man}, fh, indent=1, ensure_ascii=False)
    print("manifest: %d photographs vendored, %d widths"
          % (len(man), sum(len(v["widths"]) for v in man.values())))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--manifest", action="store_true",
                    help="rebuild data/photo-manifest.json from what is on disk")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    if args.manifest:
        return write_manifest()
    todo, skipped, have = [], [], 0
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        with open(f, encoding="utf-8") as fh:
            city = json.load(fh)
        for t in city.get("trees", []):
            p = t.get("photo") or {}
            url = p.get("url")
            if not url or p.get("status") not in ("approved", "found_needs_check"):
                continue
            ok, why = may_rehost(p.get("license"))
            if not ok:
                skipped.append((t["id"], why))
                continue
            base = "%s-%s" % (t["id"], slugify(t.get("name")))
            if all(os.path.exists(os.path.join(OUT, "%s-%d.jpg" % (base, w))) for w in WIDTHS):
                have += 1
                continue
            todo.append((t["id"], base, url, p))

    print("%d already vendored, %d to fetch, %d skipped on licence"
          % (have, len(todo), len(skipped)))
    for tid, why in skipped[:8]:
        print("   skip %-9s %s" % (tid, why))
    if args.dry_run:
        print("\n(dry run; nothing fetched. ~%.0f minutes at one request every %.0fs)"
              % (len(todo) * RATE / 60.0, RATE))
        return 0

    done = 0
    for tid, base, url, p in (todo[:args.limit] if args.limit else todo):
        # Fetch Wikimedia's OWN rendering at each width and save the bytes
        # verbatim. The first version fetched the 960 and downscaled it with
        # PIL, so every file was a re-compression of a re-compression: measured
        # against Wikimedia's own 500px the mean pixel difference was 8.89 of
        # 255, three times what dropping JPEG quality from 82 to 78 costs.
        # Hidde saw the softness before it shipped. Two requests per photograph
        # instead of one is the honest price, and there is no re-encoding at
        # all now, which is also why PIL is no longer imported here.
        got = 0
        for w in WIDTHS:
            out = os.path.join(OUT, "%s-%d.jpg" % (base, w))
            if os.path.exists(out):
                got += 1
                continue
            src = wikimedia_at(url, w) or (p.get("hero") if w >= 960 else p.get("thumb")) or url
            blob = fetch(src)
            time.sleep(RATE)
            if not blob or len(blob) < 1000:
                print("  %-9s FETCH FAILED w=%d %s" % (tid, w, str(src)[:60]), flush=True)
                continue
            with open(out, "wb") as fh:
                fh.write(blob)
            got += 1
        if got:
            done += 1
            print("  %-9s %s (%d/%d widths)" % (tid, base, got, len(WIDTHS)), flush=True)
    print("\nvendored %d photographs into site/public/photos" % done)
    # AND THE MANIFEST, ALWAYS. Fetching without rewriting it changes nothing
    # anybody can see: thumbUrl() looks a photograph up by its original url in
    # data/photo-manifest.json, so eleven files landed on disk on 2026-08-29 and
    # the feed went on pointing every one of them at Wikimedia. A two-step job
    # where the second step is optional is a job that gets half done.
    write_manifest()
    return 0


if __name__ == "__main__":
    sys.exit(main())
