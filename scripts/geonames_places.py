#!/usr/bin/env python3
"""Every town of 15,000 people or more, so the search finds a place we hold no
tree for and turns it into an ask (Hidde, 2026-10-25: "moeten we niet alle
logische plaatsen ... vindbaar maken", approved "met GeoNames" the same day).

Source: GeoNames cities15000 (CC BY 4.0, https://www.geonames.org/), a file
we keep, never a service the site calls. The credit sits on /sources.

    curl -m 60 -o out/geonames/cities15000.zip https://download.geonames.org/export/dump/cities15000.zip
    curl -m 30 -o out/geonames/countryInfo.txt https://download.geonames.org/export/dump/countryInfo.txt
    python3 scripts/geonames_places.py

Writes data/places-geonames.json: {"countries": [...], "places": [[name,
ascii or "", country index, lat, lng], ...]}, largest town first, so the first
match the widget meets is the one most people mean. The nearest tree is NOT
stored here: site/src/pages/places.json.ts works it out at every build, so it
can never go stale as trees are added.
"""
import io
import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "out", "geonames")
OUT = os.path.join(ROOT, "data", "places-geonames.json")

# GeoNames' short names where ours differ, so a row says what our pages say.
COUNTRY_NAMES = {"Czechia": "Czech Republic", "Türkiye": "Turkey", "Republic of Korea": "South Korea"}
# Parts of a town (PPLX), historical (PPLH), abandoned (PPLQ, PPLW): not a
# place anybody types to find trees in.
SKIP_CODES = {"PPLX", "PPLH", "PPLQ", "PPLW", "PPLCH"}


def main():
    countries = {}
    with open(os.path.join(SRC, "countryInfo.txt"), encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            cols = line.rstrip("\n").split("\t")
            if len(cols) > 4:
                countries[cols[0]] = COUNTRY_NAMES.get(cols[4], cols[4])
    rows = []
    with zipfile.ZipFile(os.path.join(SRC, "cities15000.zip")) as z:
        with z.open("cities15000.txt") as fh:
            for line in io.TextIOWrapper(fh, encoding="utf-8"):
                c = line.rstrip("\n").split("\t")
                if c[7] in SKIP_CODES or c[8] not in countries:
                    continue
                rows.append((int(c[14] or 0), c[1], c[2], countries[c[8]], float(c[4]), float(c[5])))
    rows.sort(key=lambda r: (-r[0], r[1]))
    names = sorted({r[3] for r in rows})
    idx = {n: i for i, n in enumerate(names)}
    places = [[name, ascii_ if ascii_ != name else "", idx[country], round(lat, 3), round(lng, 3)]
              for _, name, ascii_, country, lat, lng in rows]
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"source": "GeoNames cities15000, CC BY 4.0, geonames.org",
                   "countries": names, "places": places}, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write("\n")
    print("%d places in %d countries -> %s" % (len(places), len(names), os.path.relpath(OUT, ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
