#!/usr/bin/env python3
"""How much autumn is in each tree's lead photograph.

Hidde, 2026-10-08, on the app's "Autumn Worth the Trip" shelf: "maybe makes
sense to select as much as possible trees that have photos that are yellow from
autumn." A ginkgo shelf fronted by a green summer photograph sells a month that
is not the one on the label.

The score is the share of the frame's centre band (the part a card keeps after
its crop, the Cadiz standard's fifth point) whose pixels are clearly yellow,
orange or red: hue 8 to 58 degrees, saturated and lit. Sky, bark, grass and
buildings all fall outside it. It cannot tell a gold crown from a yellow
building, so it ORDERS a shelf and never decides what ships.

    python3 scripts/photo_autumn.py            # score what is missing
    python3 scripts/photo_autumn.py --all      # rescore everything

Writes data/photo-autumn.json, {tree_id: {"url": photo url, "autumn": 0..1}}.
A url that changed is rescored, so a new lead photograph never keeps the old
one's score. Read by site/src/pages/api/browse.json.ts, which puts the most
autumnal photographs first on the autumn shelves. Throttled to one fetch every
three seconds, because Wikimedia rate-limits rather than blocks.
"""
import colorsys
import glob
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "photo-autumn.json")
UA = "AncientTreesBot/1.0 (https://ancienttrees.app; autumn photo check)"
AUTUMN_MONTHS = {9, 10, 11}


def thumb(url):
    """A 330px Wikimedia bucket for a Commons original; anything else as is."""
    p = urllib.parse.urlparse(url)
    if p.netloc == "upload.wikimedia.org" and "/thumb/" not in p.path:
        parts = p.path.split("/")  # ['', 'wikipedia', 'commons', 'a', 'ab', 'Name']
        if len(parts) >= 6:
            name = parts[-1]
            return f"https://upload.wikimedia.org/{parts[1]}/{parts[2]}/thumb/{parts[3]}/{parts[4]}/{name}/330px-{name}"
    return url


def load(url):
    if url.startswith("/"):
        path = os.path.join(ROOT, "site", "public", url.lstrip("/"))
        return open(path, "rb").read()
    req = urllib.request.Request(thumb(url), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def score(data):
    from PIL import Image
    im = Image.open(io.BytesIO(data)).convert("RGB")
    im.thumbnail((160, 160))
    w, h = im.size
    band = im.crop((0, int(h * 0.2), w, int(h * 0.8)))
    px = list(band.getdata())
    warm = 0
    for r, g, b in px:
        hh, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if 8 / 360 <= hh <= 58 / 360 and s >= 0.38 and v >= 0.32:
            warm += 1
    return round(warm / max(1, len(px)), 3)


def candidates():
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        for t in json.load(open(f))["trees"]:
            ph = t.get("photo") or {}
            bt = t.get("best_time") or {}
            if ph.get("status") != "approved" or not ph.get("url"):
                continue
            if not AUTUMN_MONTHS & set(bt.get("months") or []):
                continue
            yield t["id"], ph["url"]


def main():
    redo = "--all" in sys.argv
    have = json.load(open(OUT)) if os.path.exists(OUT) else {}
    todo = [(i, u) for i, u in candidates() if redo or have.get(i, {}).get("url") != u]
    print(f"{len(todo)} photographs to score")
    for n, (tid, url) in enumerate(todo, 1):
        try:
            have[tid] = {"url": url, "autumn": score(load(url))}
            print(f"{n}/{len(todo)} {tid} {have[tid]['autumn']}")
        except Exception as e:  # a dead link is a printed line, never a crash
            print(f"{n}/{len(todo)} {tid} skipped: {e}")
        if n % 20 == 0:
            json.dump(have, open(OUT, "w"), indent=1, sort_keys=True)
        if not url.startswith("/"):
            time.sleep(3)
    json.dump(have, open(OUT, "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
