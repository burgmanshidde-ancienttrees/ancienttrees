#!/usr/bin/env python3
"""How fast our most-seen pages are, by Google's own measure (Core Web Vitals).

    python3 scripts/page_speed.py            measure now
    python3 scripts/page_speed.py --if-due   measure only when the last time
                                             is 7+ days old (page-speed.yml)
    python3 scripts/page_speed.py --light    the quality line's verdict

Hidde, 2026-11-04 ("please add the three quality lines"). Ten pages: home
and the nine published cities with the most Google impressions in the last
ten days (data/city-queue.json, impressions_10d, which the digest's promote()
keeps current). Each goes through Google's PageSpeed Insights API, mobile:
the field numbers real Chrome visitors gave (CrUX) when Google has enough of
them, else the lab run's (with Total Blocking Time standing in for INP, as
Google's own lab report does). The newest row per page is kept in
data/page-speed.json, small and committed.

PSI_API_KEY: the API without a key shares one daily quota with every other
keyless caller in the world and answered 429 on 2026-11-04, so in practice it
needs a key. None is created here (no accounts); without one the script says
so, writes nothing, and the light stays grey "needs a PageSpeed key".

Good, Google's thresholds: LCP 2.5 s, CLS 0.1, INP 200 ms (TBT 200 ms in the
lab). Orange when a page is over one of them, red when the median of the ten
is.
"""
import datetime
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, "data", "page-speed.json")
QUEUE = os.path.join(ROOT, "data", "city-queue.json")
SITE = "https://ancienttrees.app"
API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
DUE_DAYS = 7
GOOD = {"lcp_ms": 2500, "cls": 0.1, "inp_ms": 200}


def pages(n=10):
    try:
        cities = json.load(open(QUEUE, encoding="utf-8"))["cities"]
    except (OSError, ValueError, KeyError):
        cities = []
    live = [c for c in cities if c.get("status") == "published" and c.get("slug")]
    live.sort(key=lambda c: -(c.get("impressions_10d") or 0))
    return ["/"] + ["/" + c["slug"] for c in live[:n - 1]]


def load():
    try:
        return json.load(open(STORE, encoding="utf-8"))
    except (OSError, ValueError):
        return {"_note": "Core Web Vitals of our ten most-seen pages, newest run only "
                         "(scripts/page_speed.py, weekly).", "pages": []}


def measure(path, key):
    q = {"url": SITE + path, "strategy": "mobile", "category": "performance"}
    if key:
        q["key"] = key
    with urllib.request.urlopen(API + "?" + urllib.parse.urlencode(q), timeout=120) as r:
        d = json.load(r)
    lab = d.get("lighthouseResult", {})
    audits = lab.get("audits", {})
    field = (d.get("loadingExperience") or {}).get("metrics") or {}
    row = {"path": path, "date": datetime.date.today().isoformat(),
           "score": round((lab.get("categories", {}).get("performance", {}).get("score") or 0) * 100)}
    if "LARGEST_CONTENTFUL_PAINT_MS" in field and "CUMULATIVE_LAYOUT_SHIFT_SCORE" in field:
        row["source"] = "field"
        row["lcp_ms"] = field["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"]
        row["cls"] = field["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"] / 100.0
        inp = field.get("INTERACTION_TO_NEXT_PAINT", {}).get("percentile")
        row["inp_ms"] = inp if inp is not None else round(audits.get("total-blocking-time", {}).get("numericValue", 0))
    else:
        row["source"] = "lab"
        row["lcp_ms"] = round(audits.get("largest-contentful-paint", {}).get("numericValue", 0))
        row["cls"] = round(audits.get("cumulative-layout-shift", {}).get("numericValue", 0), 3)
        row["inp_ms"] = round(audits.get("total-blocking-time", {}).get("numericValue", 0))
    return row


def last_date(store):
    dates = [r.get("date") for r in store.get("pages", []) if r.get("date")]
    return datetime.date.fromisoformat(max(dates)) if dates else None


def run(if_due=False):
    store = load()
    last = last_date(store)
    if if_due and last and (datetime.date.today() - last).days < DUE_DAYS:
        print("page_speed: measured %s, not due yet" % last)
        return 0
    key = os.environ.get("PSI_API_KEY", "").strip()
    rows = []
    for p in pages():
        try:
            rows.append(measure(p, key))
            print("page_speed: %s %s" % (p, rows[-1]))
        except urllib.error.HTTPError as e:
            print("page_speed: %s HTTP %d%s" % (p, e.code, "" if key else " (no PSI_API_KEY; the keyless quota is shared)"))
            if e.code == 429:
                break
        except Exception as e:
            print("page_speed: %s failed (%s)" % (p, str(e)[:80]))
        time.sleep(2)
    if not rows:
        print("page_speed: nothing measured, the file is unchanged")
        return 0
    store["pages"] = rows
    with open(STORE, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=1)
        f.write("\n")
    print("page_speed: %d page(s) written to data/page-speed.json" % len(rows))
    return 0


def over(row):
    return [k for k, lim in GOOD.items() if row.get(k) is not None and row[k] > lim]


def light():
    store = load()
    rows = store.get("pages", [])
    if not rows:
        return "grey", "page speed (needs a PageSpeed key)"
    last = last_date(store)
    age = (datetime.date.today() - last).days if last else 99
    if age > 2 * DUE_DAYS:
        return "grey", "page speed last measured %d days ago (unknown now)" % age
    medians = {k: statistics.median(r[k] for r in rows if r.get(k) is not None) for k in GOOD}
    bad_median = [k for k, v in medians.items() if v > GOOD[k]]
    names = {"lcp_ms": "LCP", "cls": "CLS", "inp_ms": "INP"}
    if bad_median:
        return "red", "median page too slow on %s" % ", ".join(names[k] for k in bad_median)
    slow = [r for r in rows if over(r)]
    if slow:
        return "orange", "%d of %d pages over Google's good line (%s %s)" % (
            len(slow), len(rows), slow[0]["path"], ", ".join(names[k] for k in over(slow[0])))
    return "green", ""


def main():
    if "--light" in sys.argv:
        print("%s: %s" % light())
        return 0
    return run(if_due="--if-due" in sys.argv)


if __name__ == "__main__":
    raise SystemExit(main())
