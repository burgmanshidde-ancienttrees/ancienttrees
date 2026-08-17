#!/usr/bin/env python3
"""The second look for a city the normal sweep found nothing for.

photo_hunt.py's geosearch only keeps a candidate whose TITLE names a plant, and
that filter is right: without it the queue fills with trams, railway stations
and whatever else stands in the same park. But it has a cost that only shows up
in the cities where it returns nothing at all. Melbourne, Nuremberg, Perugia,
Potsdam, Quebec City, Reykjavik, Thessaloniki, Toronto and Zaragoza came back
from a full sweep on 2026-08-17 with zero candidates between them, and it is not
credible that Commons holds no photograph within 100 metres of any of those
ninety trees. It holds them under titles like "Kontumazgarten 04.jpg".

So this asks the same question with the plant-word filter off and the leash much
shorter: everything geotagged within 100 metres of the pin, plus everything in a
Commons category whose name matches the place the tree stands in. Precision
falls, which is fine, because the ONLY thing downstream of this is a person
looking at the pixels. It is a last resort by name so nobody reaches for it
first: run it when the ordinary sweep is empty, not instead of it.

    python3 scripts/photo_last_resort.py Nuremberg Perugia --radius 100

Writes into the same data/photo-queue.json as photo_hunt.py, marked
`source: "last-resort"` so a later reader knows the title was never vetted.
"""
import glob
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import photo_hunt as HUNT  # noqa: E402

QUEUE = os.path.join(ROOT, "data", "photo-queue.json")
API = "https://commons.wikimedia.org/w/api.php"


def api(params):
    url = API + "?" + urllib.parse.urlencode(dict(params, format="json"))
    req = urllib.request.Request(url, headers={"User-Agent": HUNT.UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


BORING = re.compile(
    r"\b(map|plan|coat of arms|logo|flag|diagram|poster|banner|screenshot|"
    r"interior|altar|organ|fresco|painting|portrait|grave|tomb|plaque|sign|"
    r"stamp|coin|bus|tram|train|locomotive|aerial|panorama|skyline)\b", re.I)
ARCHIVAL = re.compile(r"\bcirca\s*1[89]|\b1[89]\d{2}\b", re.I)


def near_files(lat, lng, radius_m):
    """Every geotagged Commons file within radius_m, title unvetted."""
    try:
        d = api({"action": "query", "list": "geosearch", "gsnamespace": 6,
                 "gscoord": f"{lat}|{lng}", "gsradius": max(radius_m, 10),
                 "gslimit": 40})
    except Exception as e:
        print(f"    geosearch failed: {e}", file=sys.stderr)
        return []
    return [g["title"] for g in d.get("query", {}).get("geosearch", [])]


def place_words(tree):
    """The place half of the tree's name, which is what Commons files things
    under: "The First Beech of Kontumazgarten" -> Kontumazgarten."""
    name = str(tree.get("name") or "")
    tail = re.split(r"\bof\b|\bin\b|\bat\b", name)[-1]
    words = [w for w in re.split(r"[^A-Za-zÀ-ÿ]+", tail) if len(w) >= 5]
    loc = tree.get("location") or {}
    for extra in (loc.get("neighbourhood"), loc.get("address")):
        for w in re.split(r"[^A-Za-zÀ-ÿ]+", str(extra or "")):
            if len(w) >= 6:
                words.append(w)
    seen, out = set(), []
    for w in words:
        if w.lower() not in seen:
            seen.add(w.lower())
            out.append(w)
    return out[:3]


def category_files(words):
    out = []
    for w in words:
        try:
            d = api({"action": "query", "list": "search", "srnamespace": 14,
                     "srsearch": w, "srlimit": 2})
        except Exception:
            continue
        for hit in d.get("query", {}).get("search", []):
            try:
                m = api({"action": "query", "list": "categorymembers",
                         "cmtitle": hit["title"], "cmtype": "file", "cmlimit": 20})
            except Exception:
                continue
            out += [c["title"] for c in m.get("query", {}).get("categorymembers", [])]
        time.sleep(0.5)
    return out


def main():
    cities = [a for a in sys.argv[1:] if not a.startswith("--")]
    radius = 100
    if "--radius" in sys.argv:
        radius = int(sys.argv[sys.argv.index("--radius") + 1])
        cities = [c for c in cities if c != str(radius)]
    if not cities:
        print(__doc__)
        return

    queue = json.load(open(QUEUE))
    entries = queue.setdefault("trees", {})
    lower = {c.lower() for c in cities}

    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        doc = json.load(open(path))
        if doc["city"].lower() not in lower:
            continue
        for tree in doc.get("trees", []):
            if (tree.get("photo") or {}).get("url"):
                continue
            loc = tree.get("location") or {}
            if loc.get("latitude") is None:
                continue
            titles = near_files(loc["latitude"], loc["longitude"], radius)
            if "--categories" in sys.argv:
                # Off by default, and it earned that. A Commons category whose
                # NAME resembles the tree's place is not the tree's place:
                # "The London Plane of Curtain Square" reached the Curtain
                # Theatre and came back with a map of Shakespearean London,
                # which then scored 47 on a filename match because "London" is
                # in both. Worse, category members carry no coordinates, so the
                # one piece of evidence a last-resort candidate is allowed to
                # rest on is exactly what they lack, and everything they add is
                # discarded downstream after being paid for. Geosearch is the
                # honest half of this tool.
                titles += category_files(place_words(tree))
            titles = [t for t in dict.fromkeys(titles)
                      if not BORING.search(t) and not ARCHIVAL.search(t)]
            found = []
            for i in range(0, min(len(titles), 50), 50):
                try:
                    found += HUNT.imageinfo(titles[i:i + 50])
                except Exception as e:
                    print(f"    imageinfo failed: {e}", file=sys.stderr)
            entry = entries.setdefault(tree["id"], {
                "city": doc["city"], "name": tree["name"], "candidates": []})
            entry.setdefault("candidates", [])
            seen = {c.get("url") for c in entry["candidates"]}
            added = 0
            for f in found:
                if f.get("url") in seen:
                    continue
                f["source"] = "last-resort"
                entry["candidates"].append(f)
                added += 1
            entry["last_resort"] = time.strftime("%Y-%m-%d")
            print(f"  {tree['id']}  {tree['name'][:44]:44s}  {added} new")
            json.dump(queue, open(QUEUE, "w"), indent=1, ensure_ascii=False)
            time.sleep(1.0)


if __name__ == "__main__":
    main()
