#!/usr/bin/env python3
"""Cache every Wikidata item that is an individual tree with a photo and a pin.

10,953 of them at the time of writing. This is the only photo source found so
far that ties an IMAGE to an ENTITY rather than to a string: Wikidata says "this
item is that tree and this is its picture", which is exactly what Commons text
search and Openverse cannot do. Measured against our own pins on 2026-08-06, a
15 metre radius matched 93 published trees, 19 of them with no photo, and only
8 ambiguous.

The images themselves live on Commons, so these are Commons photographs our own
search and geosearch fail to find, because nobody titles a photograph the way we
name a tree.

Run it to refresh the cache; scripts/photo_hunt.py reads the file and never
queries Wikidata itself, so a sweep costs nothing here.

    python3 scripts/wikidata_trees.py

Q811534 is "individual tree", and the query walks subclasses so national
monument classes come along too.
"""
import json
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "wikidata-tree-images.json"
ENDPOINT = "https://query.wikidata.org/sparql"
UA = "AncientTrees/wikidata-cache (https://ancienttrees.app)"

# Labels are deliberately NOT requested. Asking the label service for all
# 10,953 rows returns a truncated body that fails to parse, three times out of
# three; the id, the pin and the image are all this needs.
QUERY = """
SELECT ?t ?img ?coord WHERE {
  ?t wdt:P31/wdt:P279* wd:Q811534 .
  ?t wdt:P18 ?img .
  ?t wdt:P625 ?coord .
}
"""


def commons_title(img_url):
    """Special:FilePath/Foo%20bar.jpg -> File:Foo bar.jpg, which imageinfo takes."""
    tail = img_url.rsplit("/", 1)[-1]
    return "File:" + urllib.parse.unquote(tail).replace("_", " ")


def main():
    url = ENDPOINT + "?" + urllib.parse.urlencode({"query": QUERY, "format": "json"})
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "application/sparql-results+json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)

    trees = []
    for b in d["results"]["bindings"]:
        try:
            lng, lat = [float(x) for x in
                        b["coord"]["value"].replace("Point(", "").replace(")", "").split()]
        except (KeyError, ValueError):
            continue
        trees.append({
            "qid": b["t"]["value"].rsplit("/", 1)[-1],
            "latitude": round(lat, 6),
            "longitude": round(lng, 6),
            "commons": commons_title(b["img"]["value"]),
        })
    trees.sort(key=lambda t: t["qid"])
    OUT.write_text(json.dumps({
        "source": "Wikidata, items that are an individual tree (Q811534 and subclasses) carrying both an image (P18) and coordinates (P625)",
        "endpoint": ENDPOINT,
        "licence": "The Wikidata FACTS are CC0. Each IMAGE keeps its own Commons licence, which photo_hunt.py looks up per file and which decides whether the photo may ship at all.",
        "fetched": date.today().isoformat(),
        "note": "A cache, not a register: these are not trees we publish, they are photo leads keyed to a position.",
        "trees": trees,
    }, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(trees)} wikidata trees with image and pin -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
