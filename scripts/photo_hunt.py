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
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(ROOT, "scripts"))
from geo import km  # noqa: E402


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
# Bump this whenever the MATCHING rules change (which titles count as a hit),
# and every negative recorded under an older number is asked again on the next
# sweep, exhausted ones included.
#
# Why it exists (2026-08-13). A viewing pass marks a tree `exhausted` when every
# candidate it was shown was unusable, and the script then refuses to re-ask,
# even under --recheck. That is right when the source really is empty and
# catastrophic when our own filter was hiding the answer: "tree" is a substring
# of "street", so street signs came in while the tree's own nickname was thrown
# out, and 58 trees were written off on a sample nobody could have judged
# correctly. Tested after the fix on eight of them: seven produced candidates
# the old filter had never shown. A verdict about the world, drawn from a tool,
# is only as old as the tool.
# A candidate photographed more than this far from the tree is a different
# tree, whatever its title says.
FAR_KM = 25

SWEEP_VERSION = 5
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


def _plain(s):
    """Commons files its Artist field as HTML. Strip the markup BEFORE
    truncating, or a half-closed <a href=...> tag ends up in a photo credit on
    the site, which is how Genoa's camphor was first credited on 2026-08-13."""
    import html as _html
    return _html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip().strip(",")[:120]


def imageinfo(titles):
    """Batched imageinfo with licence metadata for up to 50 File: titles."""
    if not titles:
        return []
    out = []
    d = api({"action": "query", "titles": "|".join(titles[:50]),
             "prop": "imageinfo|coordinates|categories", "iiprop": "url|extmetadata",
             "iiurlwidth": "800", "cllimit": "500"})
    for page in (d.get("query", {}).get("pages", {}) or {}).values():
        for ii in page.get("imageinfo", []):
            meta = ii.get("extmetadata", {})
            short = (meta.get("LicenseShortName") or {}).get("value", "")
            if not licence_ok(short):
                continue
            coord = (page.get("coordinates") or [{}])[0]
            out.append({
                "title": page.get("title"),
                "thumb": ii.get("thumburl"),
                "url": ii.get("descriptionurl"),
                "licence": short,
                "author": _plain((meta.get("Artist") or {}).get("value", "")),
                "lat": coord.get("lat"),
                "lng": coord.get("lon"),
                "cats": " ".join(c.get("title", "") for c in page.get("categories") or []),
            })
    return out


GENERIC_TREE_WORDS = {"tree", "boom", "arbre", "arbol", "árbol", "albero", "arvore",
                      "árvore", "baum", "drzewo", "strom", "trees", "bomen",
                      # Words meaning "protected natural monument", which is how
                      # a photographer who knew what they were looking at titles
                      # the file. These name a designation rather than a plant,
                      # and they are the strongest signal in the whole list.
                      "naturdenkmal", "naturdenkmale", "pomnik",
                      "monumentale", "monumentaal", "monumental", "singular",
                      "stablo",
                      # And the LOCAL name of common species. The filter matched
                      # our own English species field, so "Naturdenkmal Linde in
                      # der Grünanlage Hallerwiese", a CC0 photograph standing 9
                      # metres from our Nuremberg pin, was thrown away because we
                      # file that tree as "Lime (Tilia sp.)" and the German for
                      # lime is Linde. That is a whole class of miss, and it
                      # falls hardest on exactly the cities where nobody writes
                      # in English.
                      # Only tokens of five characters or more, because
                      # mentions() anchors just the END of a token to a word
                      # boundary: "den" is inside "garden", "es" ends every
                      # plural, "pin" is inside "Chopin". A four-letter plant
                      # word buys one city and poisons the queue for all of
                      # them, which is the same substring trap that let street
                      # signs in as trees on 2026-08-13.
                      "linde", "tilleul", "tiglio",
                      "eiche", "chene", "chêne", "quercia", "roble",
                      "buche", "hetre", "hêtre", "faggio",
                      "platane", "platan", "platano", "plátano",
                      "kastanie", "kastanje", "castagno", "castano", "castaño",
                      "kasztanowiec", "esche", "frene", "frêne", "frassino",
                      "fresno", "olivo", "oliveira", "olivier", "olijfboom",
                      "weide", "saule", "salice", "sauce", "wierzba",
                      "ahorn", "erable", "érable", "acero",
                      "bouleau", "betulla", "abedul", "brzoza",
                      "zeder", "cedre", "cèdre", "cedro", "ceder",
                      "ginkgo", "sequoia", "magnolia", "cipresso",
                      "cyprys", "cipres", "ciprés", "zypresse", "taxus"}


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
    return km(a, b) * 1000


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
        if not (any(mentions(hay, p) for p in places)
                and any(mentions(hay, t) for t in plant)):
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


# Common nouns that look distinctive because they are long, and are not. A
# name token only earns the standalone lane below if it is a proper noun
# nobody else's photograph would carry by accident.
NOT_DISTINCTIVE = {
    "cathedral", "monastery", "cemetery", "botanical", "botanic", "gardens",
    "garden", "memorial", "monument", "avenue", "boulevard", "entrance",
    "hospital", "university", "railway", "station", "quarter", "district",
    "riverside", "waterfront", "churchyard", "courtyard", "esplanade",
    "promenade", "vineyard", "orchard", "playground", "graveyard", "arboretum",
    "millennium", "centenary", "historic", "ancient", "veteran", "twisted",
    "gnarled", "hollow", "weeping", "giant", "grande", "grand",
}

# Titles that are near-certainly not a photograph of a tree, even when the
# words line up. All observed in the queue on 2026-08-13: street signs and a
# street light matched their square's name, and the viewing pass would have
# paid to look at each one.
JUNK_TITLE = re.compile(
    r"street sign|straatnaambord|naambord|signpost|street light|straatlantaarn"
    r"|logo|coat of arms|wapen van|kaart |\bmap\b|plattegrond|schild|plaque",
    re.I)


def name_tokens(tree):
    """The one-word proper nouns in a tree's own name, if it has any.

    Why this lane exists (2026-08-13). Den Bosch's Weichselboom had zero
    candidates after a full sweep, and one search on the word "Weichselboom"
    found a CC BY photograph of exactly that tree, name plate in frame. The
    file was reached by the existing name search and then DISCARDED, because a
    hit had to name both a plant and a place and the title is simply
    "Weichselboom (3000295248).jpg": no place in it at all.

    That both-words rule is right for a name we constructed ("The Magnolia of
    the Saint" really does match a magnolia in Saint Louis), and wrong for a
    name the world already uses. A single long proper noun is different in kind:
    nobody titles an unrelated photograph "Weichselboom", "Willemslinde" or
    "Olifantsiep". So a token of eight characters or more that is not a species
    word, not a generic tree word and not one of the long common nouns above
    stands on its own, and a title carrying it counts as a hit without needing a
    place word too.

    One more cut, measured the same hour: a token that ALSO appears in the
    tree's address is a street or park name, not a nickname, and Dutch towns
    share those wholesale. "Parklaan" standing alone returned a Parklaan in
    Groningen, Amstelveen, Rotterdam, Haarlem and Sittard. So an address word
    goes back to needing a place word beside it, and only a name the address
    does not contain stands alone.
    """
    species = {w.strip("().,").lower()
               for w in str(tree.get("species", "")).split()}
    loc = tree.get("location") or {}
    addr = f"{loc.get('address') or ''} {loc.get('neighbourhood') or ''}".lower()
    solo, place_like = set(), set()
    for raw in str(tree.get("name") or "").replace("'", " ").split():
        w = raw.strip("().,").lower()
        if len(w) < 8 or w in STOPWORDS or w in species \
                or w in GENERIC_TREE_WORDS or w in NOT_DISTINCTIVE or w.isdigit():
            continue
        (place_like if w in addr else solo).add(w)
    return solo, place_like


def mentions(hay, token):
    """Does this title actually contain that word?

    Substring matching cost us a viewing pass on 2026-08-13: "tree" is inside
    "street", so every street sign, street light and streetcorner within 250 m
    of a pin counted as a photograph of a tree. Anchoring the END of the token
    to a word boundary fixes that ("tree" in "street" is followed by a t, so it
    fails) while keeping the compounds that matter here, because Dutch and
    German glue the plant word on the end: Kastanjeboom, Lindeboom,
    Kastanienbaum all still match boom and baum."""
    return re.search(re.escape(token) + r"\b", hay) is not None


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
        plant = tree_tokens(tree)
        # BOTH a place word and a plant word, the same bar Openverse uses.
        # Place alone was not enough: the 2026-08-07 viewing pass paid to look
        # at a parked Vespa, a museum sarcophagus, a concert stage and two
        # streets of buildings, all of which named a Roman or Barcelona street
        # correctly and contained no tree at all.
        # A distinctive one-word name stands on its own; everything else still
        # has to name a plant AND a place. See name_tokens() for why.
        solo, place_like = name_tokens(tree)

        # A street name proves nothing on its own: Parklaan standing alone
        # returned a Parklaan in Groningen, Amstelveen, Rotterdam, Haarlem and
        # Sittard. It has to be the street AND the city, so the city words are
        # kept apart from the rest of the place words here.
        city_words = {str(city).lower()} | {k.lower() for k, v in ALIAS.items()
                                            if v.lower() == str(city).lower()}
        # A city often signs itself with a name our own city field never uses:
        # Den Bosch files its photographs under 's-Hertogenbosch, which is in
        # every address and in no alias table. The last comma-separated part of
        # the address is that name, so it counts as a city word too. Without
        # this the street-name lane threw away "Casinotuin 's-Hertogenbosch.jpg",
        # which is the tree's own garden, correctly named, in the right town.
        tail = str((tree.get("location") or {}).get("address") or "").split(",")[-1]
        for w in tail.lower().replace("'", " ").replace("-", " ").split():
            w = w.strip("().,")
            if len(w) >= 5 and w not in STOPWORDS:
                city_words.add(w)

        def keeps(title):
            t = title.lower()
            # A .png/.svg is a map, a diagram or a logo, never a photograph
            # of a tree: "Barcelona Pedralbes.png" (a district locator map)
            # was queued against three separate trees on 2026-08-21.
            if t.endswith((".png", ".svg", ".gif")) or " map" in t or "locator" in t:
                return False
            if any(mentions(t, r) for r in solo):
                return True                      # a nickname nobody else uses
            in_city = any(mentions(t, c) for c in city_words)
            if in_city and any(mentions(t, r) for r in place_like):
                return True                      # a street name, in the right city
            return (any(mentions(t, p) for p in places)
                    and any(mentions(t, w) for w in plant))

        named = [s["title"] for s in d.get("query", {}).get("search", [])
                 if keeps(s["title"])]
        # A second query per distinctive token, because searching the whole
        # constructed name ranks the file we want below the species' own photos.
        for token in sorted(solo | place_like)[:2]:
            try:
                d2 = api({"action": "query", "list": "search", "srnamespace": "6",
                          "srsearch": token, "srlimit": "8"})
            except Exception as e:
                print(f"    token search failed: {e}", file=sys.stderr)
                continue
            named += [s["title"] for s in d2.get("query", {}).get("search", [])
                      if token in s["title"].lower() and keeps(s["title"])]
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
                  if any(mentions(g["title"].lower(), tok) for tok in tokens)]
    except Exception as e:
        print(f"    geosearch failed: {e}", file=sys.stderr)
    seen, uniq = set(), []
    for t in named + nearby:  # name hits first: they are the strongest signal
        if JUNK_TITLE.search(t):
            continue
        if t not in seen and t.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            seen.add(t)
            uniq.append(t)
    try:
        commons = imageinfo(uniq[:12])
    except Exception as e:
        print(f"    imageinfo failed: {e}", file=sys.stderr)
        commons = []
    # A file that carries its own coordinates settles the question no word
    # match can. Added 2026-08-13 after the name lane, which lets a distinctive
    # nickname stand without a place word, offered "14 Furmanska Street, Lviv"
    # for Ljubljana's Furmanska Lipa and a Buenos Aires faculty for Zaragoza's.
    # A wrong continent is not a judgement call. Files with no coordinates pass:
    # most Commons files have none, and absence is not evidence.
    # Two ways a Commons file can prove it belongs to this place, and it needs
    # one of them. Its own coordinates within FAR_KM, or our city or country
    # named in its title or its categories. Commons categorises by place almost
    # without exception, which is why this works where the filename does not:
    # the Weichselboom file is titled with nothing but the tree's name and sits
    # in "Unidentified subjects in the Netherlands", while "14 Furmanska Street,
    # Lviv" sits in Lviv's categories and is gone.
    # The city and the country, under every spelling, and NOTHING else. Address
    # words are too generous here: Zaragoza's olive stands at the Facultad de
    # Medicina, and "Facultad" alone let in six faculties in Buenos Aires and
    # Mexico City.
    country = str((tree.get("_country") or "")).lower()
    here = {w for w in ({str(city).lower(), country} |
                        {k.lower() for k, v in ALIAS.items()
                         if v.lower() == str(city).lower()}) if len(w) >= 4}
    near = []
    for c in commons:
        if c.get("lat") is not None and c.get("lng") is not None:
            if km((loc["latitude"], loc["longitude"]), (c["lat"], c["lng"])) <= FAR_KM:
                near.append(c)
            continue
        hay = f"{c.get('title', '')} {c.get('cats', '')}".lower()
        if any(mentions(hay, w) for w in here):
            near.append(c)
    commons = near
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
        # Matches the city NAME or its slug, because the slug is what a
        # caller has to hand (it is the filename and the URL) and passing it
        # used to match nothing and report "0 photo-less trees unchecked",
        # which reads as a finished sweep rather than a typo. 2026-09-01.
        slug = os.path.basename(f)[:-5]
        if cities and d["city"].lower() not in cities and slug not in cities:
            continue
        for t in d.get("trees", []):
            if (t.get("photo") or {}).get("url"):
                continue
            prev = entries.get(t["id"])
            if prev and not recheck and prev.get("sweep") == SWEEP_VERSION:
                continue
            # A hunt marked exhausted stays exhausted, even under --recheck.
            # Set when a viewing pass has looked at every candidate and found
            # the source genuinely empty for this tree (par_017's nine were all
            # OTHER cities' Anne Frank trees), so only a NEW source can close
            # the gap and re-sweeping the same APIs buys nothing. --force
            # overrides, for the day a new source really does appear.
            if prev and prev.get("exhausted") and "--force" not in sys.argv \
                    and prev.get("sweep") == SWEEP_VERSION:
                continue
            # candidates_for() proves a candidate's place from the city AND the
            # country, so the tree has to carry its country with it.
            t = dict(t, _country=d.get("country", ""))
            todo.append((d["city"], t))

    where = f" in {', '.join(c.title() for c in cities)}" if cities else ""
    print(f"{len(todo)} photo-less trees unchecked{where}; sweeping {min(limit, len(todo))}")
    for city, tree in todo[:limit]:
        cands = candidates_for(tree, city)
        # Never clobber what a viewing pass already decided. Re-sweeping used
        # to overwrite the whole entry, which threw away every "rejected:
        # street scene, no tree in frame" verdict an Opus pass had paid for,
        # and the next pass then judged the same images again. Judged
        # candidates are kept and only genuinely new URLs are added.
        prev = entries.get(tree["id"]) or {}
        kept = [c for c in prev.get("candidates", []) if c.get("judged")]
        seen = {c.get("url") or c.get("thumb") for c in kept}
        fresh = [c for c in cands if (c.get("url") or c.get("thumb")) not in seen]
        entries[tree["id"]] = {
            "city": city, "name": tree["name"],
            "checked": time.strftime("%Y-%m-%d"),
            "sweep": SWEEP_VERSION,
            "candidates": kept + fresh,
        }
        if prev.get("exhausted"):
            entries[tree["id"]]["exhausted"] = prev["exhausted"]
        note = f", {len(kept)} judged kept" if kept else ""
        print(f"  {tree['id']}  {tree['name'][:44]:44s}  "
              f"{len(fresh)} new candidate(s){note}")
        json.dump(queue, open(QUEUE, "w"), indent=1, ensure_ascii=False)
        time.sleep(0.5)  # be polite to the API

    with_c = sum(1 for v in entries.values() if v["candidates"])
    print(f"\nQueue now: {len(entries)} trees swept, {with_c} with at least one open-licence "
          f"candidate. A viewing pass judges them against the Cadiz standard; this "
          f"script never approves anything.")


if __name__ == "__main__":
    main()
