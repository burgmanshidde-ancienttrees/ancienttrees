#!/usr/bin/env python3
"""Record the month each Wikimedia Commons lead photograph was taken.

Why (Hidde, 2026-10-13): Discover's season hero said "Autumn is here" over a
green summer photograph. A tree is at its best in some months; its photograph
shows that best only when it was taken in those months. This writes
photo.taken_month (1 to 12) from the file's EXIF DateTimeOriginal on Commons,
so the app can pick a hero whose picture shows the season it names.

Usage:
    python3 scripts/photo_months.py            # fill what is missing
    python3 scripts/photo_months.py --dry-run  # print counts, write nothing

Commons takes 50 titles per query; one query about every three seconds.
"""
import glob
import json
import re
import sys
import time
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "AncientTreesBot/1.0 (https://ancienttrees.app; photo dates)"
MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"])}


def title_of(url):
    """The File: title from an upload.wikimedia.org url, thumb or original."""
    if "upload.wikimedia.org" not in url:
        return None
    parts = urllib.parse.urlparse(url).path.split("/")
    if "thumb" in parts:
        name = parts[parts.index("thumb") + 3]
    else:
        name = parts[-1]
    return "File:" + urllib.parse.unquote(name).replace("_", " ")


def month_of(value):
    """1 to 12 from a Commons DateTimeOriginal value, or None."""
    text = re.sub(r"<[^>]+>", " ", value or "")
    m = re.search(r"\b(1[89]\d\d|20\d\d)[-:/.](\d{1,2})[-:/.]\d{1,2}", text)
    if m and 1 <= int(m.group(2)) <= 12:
        return int(m.group(2))
    for word in re.findall(r"[A-Za-z]+", text):
        if word.lower() in MONTHS:
            return MONTHS[word.lower()]
    return None


def query(titles):
    params = {"action": "query", "format": "json", "prop": "imageinfo",
              "iiprop": "extmetadata", "iiextmetadatafilter": "DateTimeOriginal",
              "titles": "|".join(titles)}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": UA})
    data = json.load(urllib.request.urlopen(req, timeout=20))
    norm = {n["to"]: n["from"] for n in data["query"].get("normalized", [])}
    out = {}
    for page in data["query"].get("pages", {}).values():
        info = (page.get("imageinfo") or [{}])[0]
        value = ((info.get("extmetadata") or {}).get("DateTimeOriginal") or {}).get("value")
        out[norm.get(page["title"], page["title"])] = month_of(value)
    return out


def main():
    dry = "--dry-run" in sys.argv
    files = sorted(glob.glob("data/cities/*.json"))
    wanted = {}
    for f in files:
        for t in json.load(open(f)).get("trees", []):
            p = t.get("photo") or {}
            title = title_of(p.get("url") or "")
            if title and "taken_month" not in p:
                wanted[title] = None
    titles = list(wanted)
    print(f"{len(titles)} Commons photographs without a month")
    if dry:
        return
    for i in range(0, len(titles), 50):
        try:
            wanted.update(query(titles[i:i + 50]))
        except Exception as e:  # one bad batch is not a reason to stop
            print("batch", i // 50, "failed:", e)
        time.sleep(3)
    found = 0
    for f in files:
        d = json.load(open(f))
        changed = False
        for t in d.get("trees", []):
            p = t.get("photo") or {}
            m = wanted.get(title_of(p.get("url") or "") or "")
            if m and "taken_month" not in p:
                p["taken_month"] = m
                changed = True
                found += 1
        if changed:
            with open(f, "w") as fh:
                json.dump(d, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
    print(f"{found} months written")


if __name__ == "__main__":
    main()
