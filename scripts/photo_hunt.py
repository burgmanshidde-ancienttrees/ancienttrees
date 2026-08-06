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
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _aliases():
    """Local spelling -> English name, shared with build_site.py and
    passcheck.py via data/city-aliases.json. Commons files Padua as Padova."""
    try:
        with open(os.path.join(ROOT, "data", "city-aliases.json")) as fh:
            return json.load(fh)["aliases"]
    except Exception:
        return {}


ALIAS = _aliases()
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


STOPWORDS = {"the", "of", "and", "at", "in", "on", "a", "an", "de", "da", "do",
             "del", "della", "di", "el", "la", "le", "les", "van", "der", "den"}


def place_tokens(tree, city):
    """GEOGRAPHIC words only: the city under every spelling it might be filed
    as, plus the proper nouns of its address and neighbourhood.

    The geosearch half of this sweep is bounded by a radius. The name search was
    not bounded by anything, so it matched species names worldwide: all nine
    candidates for Porto's Metrosidero were Metrosideros in New Zealand, and all
    nine for its Atlas Cedar were cedars in Slovenia, Poland and Bulgaria.
    Eighteen candidates that could never be approved, paid for at viewing-pass
    rates.

    Words from the tree's own name are deliberately NOT used. They read as
    distinctive and are not: "The Magnolia of the Saint" matched a magnolia in
    Saint Louis and another beside Saint-Malo church, and "The Metrosidero of
    the Library" matched Devonport Library in New Zealand. Only a place name
    ties a photograph to a place."""
    species = {w.strip("().,").lower()
               for w in str(tree.get("species", "")).split()}
    words = set()
    # the city under both spellings, because Commons files Padua as Padova and
    # Genoa as Genova; data/city-aliases.json already holds those pairs
    for name in {city} | {k for k, v in ALIAS.items()
                          if v.lower() == str(city).lower()}:
        if name:
            words.add(str(name).lower())
    loc = tree.get("location") or {}
    for extra in (loc.get("neighbourhood"), loc.get("address")):
        for w in str(extra or "").lower().replace(",", " ").replace("'", " ").split():
            w = w.strip("().,")
            if len(w) >= 5 and w not in STOPWORDS and w not in species \
                    and w not in GENERIC_TREE_WORDS and not w.isdigit():
                words.add(w)
    return words


INAT_API = "https://api.inaturalist.org/v1/observations"


def genus_of(tree):
    """The genus from 'European Yew (Taxus baccata)' is 'Taxus'."""
    m = re.search(r"\(([A-Z][a-z]+)", str(tree.get("species", "")))
    return m.group(1) if m else None


def inat_candidates(tree):
    """CC-licensed iNaturalist photos of the same GENUS within 120 m of the pin.

    Built 2026-08-06 on Hidde's ask for a better photo answer than agent
    hunting (measured 43-72k tokens per usable photo) after Rome proved a
    Commons dead end: one candidate across seven photo-less trees. iNaturalist
    observations carry per-photo licences and their own coordinates, so a hit
    both illustrates the tree and corroborates the pin. Genus within 120 m
    rather than species exact, because observers often stop at genus for a
    street tree; the viewing pass still judges identity against the Cadiz
    standard, same as every other source. Obscured locations are skipped in
    the spirit of hard rule 10: if the observer hid the spot, respect it."""
    genus = genus_of(tree)
    loc = tree["location"]
    if not genus:
        return []
    q = urllib.parse.urlencode({
        "lat": loc["latitude"], "lng": loc["longitude"], "radius": 0.12,
        "taxon_name": genus, "photo_license": "cc0,cc-by,cc-by-sa",
        "per_page": 10, "order_by": "votes",
    })
    req = urllib.request.Request(f"{INAT_API}?{q}", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.load(r)
    except Exception as e:
        print(f"    inaturalist failed: {e}", file=sys.stderr)
        return []
    out = []
    for o in d.get("results", []):
        if o.get("geoprivacy") in ("obscured", "private"):
            continue
        taxon = (o.get("taxon") or {}).get("name", "")
        for p in o.get("photos", [])[:2]:
            code = p.get("license_code") or ""
            if not code.startswith("cc"):
                continue
            out.append({
                "title": f"iNat obs {o.get('id')} ({taxon})",
                "thumb": (p.get("url") or "").replace("square", "medium"),
                "url": f"https://www.inaturalist.org/observations/{o.get('id')}",
                "licence": code.upper().replace("CC-", "CC "),
                "author": (p.get("attribution") or "")[:120],
                "source": "inaturalist",
                "obs_location": o.get("location"),
            })
    return out[:6]


WD_CACHE = os.path.join(ROOT, "data", "wikidata-tree-images.json")
WD_RADIUS_M = 15
_WD = []


def haversine_m(a, b):
    R = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = p2 - p1
    dl = math.radians(b[1] - a[1])
    x = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(x))


def wikidata_candidates(tree):
    """The Commons photo Wikidata attaches to the tree standing at this spot.

    The only source here that matches an ENTITY rather than a string: Wikidata
    says this item is that tree and this is its picture. That is why it finds
    Commons photographs our own text search misses, and why it needs no place
    tokens.

    15 metres, and only when exactly one candidate is in range. Both numbers are
    measured rather than chosen: at 200 m the match count looks twice as good
    and is largely wrong, pairing Padua's Goethe Palm with a magnolia cloister
    in the same garden. A dense garden is precisely where this would attach the
    wrong photograph, so an ambiguous match is dropped rather than guessed, and
    the viewing pass still looks at the pixels afterwards."""
    if not _WD:
        try:
            _WD.append(json.load(open(WD_CACHE))["trees"])
        except Exception:
            _WD.append([])
            print("    no wikidata cache; run scripts/wikidata_trees.py", file=sys.stderr)
    loc = tree["location"]
    here = (loc["latitude"], loc["longitude"])
    near = [w for w in _WD[0]
            if abs(w["latitude"] - here[0]) < 0.01 and abs(w["longitude"] - here[1]) < 0.01
            and haversine_m(here, (w["latitude"], w["longitude"])) <= WD_RADIUS_M]
    if len(near) != 1:
        return []
    w = near[0]
    try:
        found = imageinfo([w["commons"]])
    except Exception as e:
        print(f"    wikidata imageinfo failed: {e}", file=sys.stderr)
        return []
    for f in found:
        f["source"] = f"wikidata/{w['qid']}"
        f["title"] = f"{w['commons']} (Wikidata {w['qid']})"
    return found


OPENVERSE_API = "https://api.openverse.org/v1"
_OV_TOKEN = []


def openverse_token():
    """OAuth2 token from the credentials in the environment, fetched once.

    Anonymous Openverse allows 200 requests a day and there are ~390 photo-less
    trees, so the key is the difference between a sweep and two days of sweeps:
    verified credentials lift it to 100/min and 10,000/day. Absent credentials
    are not an error, the source is simply skipped, exactly like the other
    optional secrets in this project."""
    if _OV_TOKEN:
        return _OV_TOKEN[0]
    cid = os.environ.get("OPENVERSE_CLIENT_ID")
    sec = os.environ.get("OPENVERSE_CLIENT_SECRET")
    if not cid or not sec:
        _OV_TOKEN.append(None)
        return None
    body = urllib.parse.urlencode({
        "client_id": cid, "client_secret": sec,
        "grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(
        f"{OPENVERSE_API}/auth_tokens/token/", data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            _OV_TOKEN.append(json.load(r).get("access_token"))
    except Exception as e:
        print(f"    openverse auth failed: {e}", file=sys.stderr)
        _OV_TOKEN.append(None)
    return _OV_TOKEN[0]


def openverse_candidates(tree, city, places):
    """Openly licensed photos from Openverse, which aggregates Flickr and more.

    The third source, added 2026-08-06 because Commons and iNaturalist both came
    back empty for Rome. Kept, but do not expect much from it: measured the day
    it was added, it produced **0 candidates across 49 photo-less trees** in
    Rome, Lisbon, Porto, Padua, London and Brussels.

    The reason is structural and worth remembering before anyone tries a fourth
    text-only source. Openverse has neither coordinates nor taxonomy, so text is
    the only thing to match on, and our tree names are our own inventions: no
    photograph anywhere is titled "The Podocarp of Villa Sciarra". Searching the
    place instead does return plenty (65 images for Villa Sciarra) and they are
    photographs of monuments, market stalls and bronze busts. Feeding those to a
    viewing pass is exactly the 43k-tokens-per-photo waste the geographic filter
    was written to stop.

    It stays because a sweep costs one request per tree against a 10,000/day
    limit, and a well-titled Flickr upload will occasionally match both a plant
    word and a place word. It is not the answer to the photo gap."""
    tok = openverse_token()
    if not tok:
        return []
    name = str(tree.get("name") or "").replace("The ", "", 1)
    q = urllib.parse.urlencode({
        "q": f"{name} {city}".strip(),
        "license": "cc0,by,by-sa",
        "page_size": 8,
    })
    req = urllib.request.Request(
        f"{OPENVERSE_API}/images/?{q}",
        headers={"Authorization": f"Bearer {tok}", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            d = json.load(r)
    except Exception as e:
        print(f"    openverse failed: {e}", file=sys.stderr)
        return []
    out = []
    plant = tree_tokens(tree)
    for it in d.get("results", []):
        hay = f"{it.get('title') or ''} {it.get('tags') or ''}".lower()
        # BOTH, not either. Openverse has no coordinates and no taxonomy, so
        # text is the only signal there is: a place query alone returns the
        # square's market stalls and its bronze busts, and a species query alone
        # returns that species on another continent. Requiring the plant and the
        # place together is the only honest filter available here.
        if not (any(p in hay for p in places) and any(t in hay for t in plant)):
            continue
        lic = (it.get("license") or "").upper()
        out.append({
            "title": f"Openverse: {it.get('title') or it.get('id')}",
            "thumb": it.get("thumbnail") or it.get("url"),
            "url": it.get("foreign_landing_url") or it.get("url"),
            "licence": f"CC {lic} {it.get('license_version') or ''}".strip(),
            "author": (it.get("creator") or "")[:120],
            "source": f"openverse/{it.get('source')}",
        })
    return out[:5]


def candidates_for(tree, city=""):
    loc = tree["location"]
    named, nearby = [], []
    # Hoisted out of the try below: Openverse uses it too, so a Commons outage
    # must not leave it undefined.
    places = place_tokens(tree, city)
    try:
        d = api({"action": "query", "list": "search", "srnamespace": "6",
                 "srsearch": tree["name"], "srlimit": "10"})
        # A hit earns its place by naming the plant AND the place. Dropping
        # everything rather than falling back to unfiltered hits is deliberate:
        # an honest gap costs nothing, and nine wrong-continent candidates cost
        # a viewing pass.
        named = [s["title"] for s in d.get("query", {}).get("search", [])
                 if any(p in s["title"].lower() for p in places)]
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
        commons = imageinfo(uniq[:12])
    except Exception as e:
        print(f"    imageinfo failed: {e}", file=sys.stderr)
        commons = []
    # Commons first (a named, categorized photo is the strongest identity
    # signal there is), then iNaturalist, then Openverse where both are thin.
    # Wikidata first: an entity-to-image link is the strongest identity signal
    # available, stronger even than a Commons category.
    return (wikidata_candidates(tree) + commons + inat_candidates(tree)
            + openverse_candidates(tree, city, places))


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
        cands = candidates_for(tree, city)
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
