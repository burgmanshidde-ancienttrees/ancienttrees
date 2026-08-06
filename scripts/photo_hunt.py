#!/usr/bin/env python3
"""Photo candidates by API, not by agent.

The 2026-08-04 retro measured agent photo hunting at 72,000 tokens per usable
photo, the worst ratio the project has produced, because an agent was doing
retrieval. This script does the retrieval for nothing: for every published tree
without a photo it asks Wikimedia Commons twice (geosearch around the pin, then
a name search), keeps only candidates whose licence is open, and writes them to
data/photo-queue.json. A periodic viewing pass then LOOKS at the queued images
and judges them against the Cadiz standard; judgement stays with an agent,
retrieval never goes to one again.

    python3 scripts/photo_hunt.py               # next 40 unchecked trees
    python3 scripts/photo_hunt.py --limit 10
    python3 scripts/photo_hunt.py --recheck     # also re-ask for trees checked before

Empty results are recorded too, so the queue doubles as the ledger of what was
already asked: a tree is only re-asked with --recheck (new uploads do appear).
This is an API sweep, cheap by design; the CURATION.md rule against re-running
exhausted AGENT hunts stands untouched.
"""
import glob
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "photo-queue.json")
API = "https://commons.wikimedia.org/w/api.php"
UA = "AncientTreesBot/1.0 (https://ancienttrees.app; photo candidate sweep)"
OK_LICENCE = ("cc0", "cc by", "cc-by", "public domain", "pdm", "attribution")
BAD_LICENCE = ("nc", "nd")


def api(params):
    params = dict(params, format="json")
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def licence_ok(short):
    """Open licences only; any NC or ND variant disqualifies outright."""
    s = (short or "").lower()
    if any(b in s for b in BAD_LICENCE):
        return False
    return any(g in s for g in OK_LICENCE)


def imageinfo(titles):
    """Batched imageinfo with licence metadata for up to 50 File: titles."""
    if not titles:
        return []
    out = []
    d = api({"action": "query", "titles": "|".join(titles[:50]),
             "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": "800"})
    for page in (d.get("query", {}).get("pages", {}) or {}).values():
        for ii in page.get("imageinfo", []):
            meta = ii.get("extmetadata", {})
            short = (meta.get("LicenseShortName") or {}).get("value", "")
            if not licence_ok(short):
                continue
            out.append({
                "title": page.get("title"),
                "thumb": ii.get("thumburl"),
                "url": ii.get("descriptionurl"),
                "licence": short,
                "author": (meta.get("Artist") or {}).get("value", "")[:120],
            })
    return out


GENERIC_TREE_WORDS = {"tree", "boom", "arbre", "arbol", "árbol", "albero", "arvore",
                      "árvore", "baum", "drzewo", "strom", "trees", "bomen"}


def tree_tokens(tree):
    """Words that make a nearby photo plausibly ABOUT this tree: its name and
    species, in pieces, plus generic tree words in the languages we cover."""
    # ONLY plant words. The tree's name carries its place ("the Millennium
    # Ginkgo of the Stadspark", "the Historic Grounds of Zoo Antwerpen"), and
    # feeding those into a geosearch filter lets through every photograph taken
    # in that park or that city: the sweep queued three trams for one ginkgo and
    # a railway station for a zoo. A geosearch hit earns its place by naming a
    # plant, never by naming the neighbourhood.
    text = str(tree.get("species", "")).lower()
    words = {w.strip("().,") for w in text.split() if len(w.strip("().,")) >= 4}
    return words | GENERIC_TREE_WORDS


def candidates_for(tree):
    loc = tree["location"]
    named, nearby = [], []
    try:
        d = api({"action": "query", "list": "search", "srnamespace": "6",
                 "srsearch": tree["name"], "srlimit": "10"})
        named = [s["title"] for s in d.get("query", {}).get("search", [])]
    except Exception as e:
        print(f"    name search failed: {e}", file=sys.stderr)
    tokens = tree_tokens(tree)
    try:
        d = api({"action": "query", "list": "geosearch", "gsnamespace": "6",
                 "gscoord": f"{loc['latitude']}|{loc['longitude']}",
                 "gsradius": "250", "gslimit": "50"})
        # in a dense city most photos within 250 m are about something else
        # entirely; a geosearch hit only counts if its title mentions the tree,
        # its species, or a tree word at all
        nearby = [g["title"] for g in d.get("query", {}).get("geosearch", [])
                  if any(tok in g["title"].lower() for tok in tokens)]
    except Exception as e:
        print(f"    geosearch failed: {e}", file=sys.stderr)
    seen, uniq = set(), []
    for t in named + nearby:  # name hits first: they are the strongest signal
        if t not in seen and t.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            seen.add(t)
            uniq.append(t)
    try:
        return imageinfo(uniq[:12])
    except Exception as e:
        print(f"    imageinfo failed: {e}", file=sys.stderr)
        return []


def main():
    limit = 40
    recheck = "--recheck" in sys.argv
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    # Without this the sweep works alphabetically through 393 photo-less trees,
    # which is the wrong shape for deepening a named city: Porto publishes 17
    # trees with 4 photos and waiting for the alphabet to reach it is not a plan.
    cities = []
    if "--city" in sys.argv:
        cities = [c.strip().lower()
                  for c in sys.argv[sys.argv.index("--city") + 1].split(",")]

    queue = {}
    if os.path.exists(QUEUE):
        queue = json.load(open(QUEUE))
    entries = queue.setdefault("trees", {})

    todo = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        d = json.load(open(f))
        if cities and d["city"].lower() not in cities:
            continue
        for t in d.get("trees", []):
            if (t.get("photo") or {}).get("url"):
                continue
            if t["id"] in entries and not recheck:
                continue
            todo.append((d["city"], t))

    where = f" in {', '.join(c.title() for c in cities)}" if cities else ""
    print(f"{len(todo)} photo-less trees unchecked{where}; sweeping {min(limit, len(todo))}")
    for city, tree in todo[:limit]:
        cands = candidates_for(tree)
        entries[tree["id"]] = {
            "city": city, "name": tree["name"],
            "checked": time.strftime("%Y-%m-%d"),
            "candidates": cands,
        }
        print(f"  {tree['id']}  {tree['name'][:44]:44s}  {len(cands)} candidate(s)")
        json.dump(queue, open(QUEUE, "w"), indent=1, ensure_ascii=False)
        time.sleep(0.5)  # be polite to the API

    with_c = sum(1 for v in entries.values() if v["candidates"])
    print(f"\nQueue now: {len(entries)} trees swept, {with_c} with at least one open-licence "
          f"candidate. A viewing pass judges them against the Cadiz standard; this "
          f"script never approves anything.")


if __name__ == "__main__":
    main()
