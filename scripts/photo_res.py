#!/usr/bin/env python3
"""What size is each photograph REALLY, and is it big enough for where we show it.

Written 2026-08-21 after Hidde spotted pixelated thumbnails three times in one
day (the country mosaic, the species shelf, the map sidebar) and asked for a
solution that stops him having to spot them at all.

The cause was never the markup: srcset and sizes were right. It is that a
source file can simply be smaller than the box we paint it in. A 307 pixel
wide Commons file rendered in a 211 point card on a retina screen is asked for
422 physical pixels and has 307, so the browser upscales and it looks soft. No
amount of `sizes` tuning fixes a file that does not have the pixels.

So: measure the intrinsic size once, store it beside the url, and let both
surfaces refuse to put a small file in a big box. Wikimedia answers exactly
and free through its own API; everything else gets its header read from the
first bytes of the file.

    python3 scripts/photo_res.py            # measure what is missing, write it
    python3 scripts/photo_res.py --report   # measure nothing, just say what hurts

Every photo block gains "width" and "height". A run adding a photo does not
have to think about it: this script fills the gap on its next pass, and
scripts/qa.py refuses a render site that would upscale.
"""
import glob
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "AncientTrees/1.0 (https://ancienttrees.app; photo size check)"}

# What each render site asks of a photograph, in physical pixels, on a 2x
# screen. The card is the widest box a thumbnail lands in (a shelf card is
# ~211 CSS px on desktop, ~270 on a phone), the hero is the tree page.
MIN_CARD = 540
MIN_HERO = 960


def jpeg_png_size(data):
    """Intrinsic size from the first bytes of a JPEG or PNG."""
    if data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            m = data[i + 1]
            if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
                i += 2
                continue
            seg = int.from_bytes(data[i + 2:i + 4], "big")
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                     0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h = int.from_bytes(data[i + 5:i + 7], "big")
                w = int.from_bytes(data[i + 7:i + 9], "big")
                return w, h
            i += 2 + seg
    return None


def by_header(url):
    try:
        req = urllib.request.Request(url, headers={**UA, "Range": "bytes=0-131071"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return jpeg_png_size(r.read(131072))
    except Exception:
        return None


def commons_sizes(urls):
    """Ask Commons for the real size of many files at once."""
    out = {}
    titles = {}
    for u in urls:
        m = re.search(r"upload\.wikimedia\.org/wikipedia/commons/(?:thumb/)?[0-9a-f]/[0-9a-f]{2}/([^/]+)", u)
        if m:
            titles["File:" + urllib.parse.unquote(m.group(1))] = u
    keys = list(titles)
    for i in range(0, len(keys), 40):
        chunk = keys[i:i + 40]
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "prop": "imageinfo",
            "iiprop": "size", "titles": "|".join(chunk)})
        try:
            req = urllib.request.Request(
                "https://commons.wikimedia.org/w/api.php?" + q, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.load(r)
        except Exception as e:
            print("  commons api failed: %s" % str(e)[:80], file=sys.stderr)
            continue
        for page in (d.get("query", {}).get("pages", {}) or {}).values():
            ii = (page.get("imageinfo") or [{}])[0]
            t = page.get("title")
            if t in titles and ii.get("width"):
                out[titles[t]] = (ii["width"], ii["height"])
    return out


def main():
    report_only = "--report" in sys.argv
    files = sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json")))
    photos = []          # (path, doc, tree)
    for path in files:
        doc = json.load(open(path, encoding="utf-8"))
        for t in doc["trees"]:
            p = t.get("photo") or {}
            if p.get("url"):
                photos.append((path, doc, t))

    need = [t for _, _, t in photos if not t["photo"].get("width")]
    print("%d photographs, %d without a measured size" % (len(photos), len(need)))

    if need and not report_only:
        wiki = commons_sizes([t["photo"]["url"] for t in need])
        print("  Commons answered for %d" % len(wiki))
        for t in need:
            u = t["photo"]["url"]
            size = wiki.get(u) or by_header(u)
            if size:
                t["photo"]["width"], t["photo"]["height"] = size
        touched = {}
        for path, doc, t in photos:
            if t["photo"].get("width"):
                touched[path] = doc
        for path, doc in touched.items():
            json.dump(doc, open(path, "w", encoding="utf-8"),
                      indent=2, ensure_ascii=False)
            open(path, "a", encoding="utf-8").write("\n")
        print("  wrote sizes into %d city files" % len(touched))

    small_card, small_hero, unknown = [], [], []
    for _, doc, t in photos:
        p = t["photo"]
        w = p.get("width")
        if not w:
            unknown.append((doc["city"], t["name"]))
        elif w < MIN_CARD:
            small_card.append((doc["city"], t["name"], w))
        elif w < MIN_HERO:
            small_hero.append((doc["city"], t["name"], w))

    print("\ntoo small for a card (<%dpx): %d" % (MIN_CARD, len(small_card)))
    for c, n, w in sorted(small_card, key=lambda x: x[2])[:15]:
        print("  %4dpx  %-16s %s" % (w, c, n[:44]))
    print("card-ready but soft as a hero (<%dpx): %d" % (MIN_HERO, len(small_hero)))
    print("still unmeasured: %d" % len(unknown))
    return 0


if __name__ == "__main__":
    sys.exit(main())
