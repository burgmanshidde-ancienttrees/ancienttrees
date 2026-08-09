#!/usr/bin/env python3
"""Core Web Vitals per page type, from Google's own PageSpeed Insights API.

Built 2026-08-09. The beacon reports one summary number for the whole site
(p90 page load 5.2 seconds on 2026-08-08) and 72 percent of our search
clicks come from phones, so a slow page type is not a detail here. One
number for 1,139 pages cannot say WHICH type is slow, and the types are
genuinely different animals: a city page boots a map, a tree page is mostly
text and one image, /explore loads every pin on the site.

Free, no key and no account at this volume, which under hard rule 5 as
Hidde sharpened it on 2026-08-09 makes it gear rather than a dependency:
nothing it does reaches the built site, and if the API disappears we lose a
number, not a page.

It reports two things per URL, and the difference between them matters:
  - LAB (Lighthouse): one simulated load on a throttled mid-range phone.
    Reproducible, available for every page, and not what any human saw.
  - FIELD (CrUX): what real Chrome users actually experienced over 28 days.
    The truth, when it exists, and it does not exist for a page without
    enough traffic, which is most of ours. An absent field score is
    information too: it means almost nobody has loaded that page.

Usage:
  python3 scripts/pagespeed.py                  # one URL per page type
  python3 scripts/pagespeed.py /rome /lisbon    # specific paths
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://ancienttrees.app"
API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

# One representative page per type, because the point is to compare types
# rather than pages. Chosen as the ones people actually land on: /lisbon and
# /porto lead our Search Console pages, /explore is the product.
DEFAULT = [
    ("home", "/"),
    ("city", "/lisbon"),
    ("tree", "/lisbon/cypress-of-principe-real"),
    ("question", "/lisbon/oldest-tree"),
    ("map", "/explore"),
    ("app", "/app"),
]


def run(path, strategy="mobile"):
    url = API + "?" + urllib.parse.urlencode({
        "url": BASE + path, "strategy": strategy,
        "category": "performance"})
    req = urllib.request.Request(url, headers={"User-Agent": "AncientTrees/1.0"})
    for attempt in (1, 2, 3):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and attempt < 3:
                time.sleep(12 * attempt)   # the free tier rate-limits; wait it out
                continue
            return {"_error": "HTTP %s" % e.code}
        except Exception as e:
            if attempt < 3:
                time.sleep(6)
                continue
            return {"_error": str(e)[:60]}


def read(d):
    if "_error" in d:
        return None
    lh = d.get("lighthouseResult") or {}
    audits = lh.get("audits") or {}

    def ms(key):
        v = (audits.get(key) or {}).get("numericValue")
        return round(v) if v is not None else None
    score = ((lh.get("categories") or {}).get("performance") or {}).get("score")
    out = {
        "score": round(score * 100) if score is not None else None,
        "lcp": ms("largest-contentful-paint"),
        "cls": ((audits.get("cumulative-layout-shift") or {}).get("numericValue")),
        "tbt": ms("total-blocking-time"),
        "field": None,
    }
    cr = d.get("loadingExperience") or {}
    m = cr.get("metrics") or {}
    if m:
        out["field"] = {
            "lcp": (m.get("LARGEST_CONTENTFUL_PAINT_MS") or {}).get("percentile"),
            "cls": (m.get("CUMULATIVE_LAYOUT_SHIFT_SCORE") or {}).get("percentile"),
            "verdict": cr.get("overall_category"),
        }
    return out


def verdict(lcp):
    """Google's own thresholds, so the table says good/poor rather than a number
    the reader has to know how to judge."""
    if lcp is None:
        return "?"
    return "good" if lcp <= 2500 else ("needs work" if lcp <= 4000 else "POOR")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    targets = [(p.strip("/") or "home", p) for p in args] if args else DEFAULT
    print("PageSpeed Insights, mobile. LAB is a simulated mid-range phone;")
    print("FIELD is what real Chrome users saw over 28 days, absent when a page")
    print("has too little traffic, which is itself worth knowing.\n")
    print("%-10s %-34s %5s %8s %7s %7s  %s" % (
        "type", "path", "score", "LCP", "CLS", "TBT", "field"))
    for name, path in targets:
        r = read(run(path))
        if not r:
            print("%-10s %-34s   fetch failed" % (name, path[:34]))
            continue
        f = r["field"]
        fs = "no field data" if not f else "%s, LCP %sms" % (
            (f.get("verdict") or "?").lower(), f.get("lcp"))
        print("%-10s %-34s %5s %5sms %7s %5sms  %s   %s" % (
            name, path[:34], r["score"], r["lcp"],
            ("%.3f" % r["cls"]) if r["cls"] is not None else "-",
            r["tbt"], fs, verdict(r["lcp"])))
        time.sleep(2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
