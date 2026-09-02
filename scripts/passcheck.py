#!/usr/bin/env python3
"""Everything you must know about a place BEFORE writing a research brief.

Three passes have now been sent out to "open" a city that was already live
(Napoli, Firenze, Munich), each time because a queue entry said new and nobody
checked. Munich alone cost 127,000 tokens to discover the page had existed for
eleven days. The rule to check first has been written down twice and failed
twice, so this is the mechanism instead: one command, run before any brief.

    python3 scripts/passcheck.py Munich
    python3 scripts/passcheck.py Torino          works in the local language too
    python3 scripts/passcheck.py 45.07 7.68      or by coordinate
    python3 scripts/passcheck.py --brief Valencia

--brief prints a complete, paste-ready verification brief: status, ids,
delivery format, the actual register candidates near the place (not a count, a
list), what an earlier pass already found or rejected, and the hosts that hang.
A brief written by this script cannot leave on a false premise, because it is
generated from the same data the premise would have to contradict.

    python3 scripts/passcheck.py --claim Galway --kind verify   before dispatching
    python3 scripts/passcheck.py --release Galway               when merged

--claim records the pass in data/in-flight.json BEFORE it is dispatched, and
--brief refuses a claimed place. This is the other half of the same disease:
passcheck knew what was published, nothing knew what was in flight, and on
2026-08-06 a session and a night run wrote the same nine Padova stories twenty
minutes apart. Claims expire after 4 hours by themselves, so a dead session
cannot block a city. Commit and push the claim, or the night runs cannot see
it: the push is part of the claim.
"""
import datetime
import glob
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import km  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAME_CITY_KM = 20.0
NEAR_PUBLISHED_KM = 0.08  # a register entry this close to a live tree is probably that tree
LEAD_MATCH_KM = 0.025     # ...and this close to a recorded lead is probably that lead

# Local name to our slug, for the cases a name lookup alone would miss. Distance
# is the real test; this only helps the first guess.
def _load_aliases():
    """Local spelling -> the English name this site publishes under.

    Lives in data/city-aliases.json so the build check and this generator read
    one table instead of two that drift: the build refuses to ship a city under
    a local name, and this file needs the same pairs read backwards to find
    register candidates. The inline fallback keeps passcheck working if the data
    file is missing."""
    try:
        p = os.path.join(ROOT, "data", "city-aliases.json")
        with open(p) as fh:
            return json.load(fh)["aliases"]
    except Exception:
        return {"napoli": "naples", "firenze": "florence", "roma": "rome",
                "milano": "milan", "torino": "turin", "genova": "genoa",
                "venezia": "venice", "padova": "padua", "lisboa": "lisbon"}


ALIAS = _load_aliases()

NAME_FIELDS = ("name", "name_en", "name_pt", "name_it", "name_ja", "name_nl",
               "name_eu", "common_fr", "designation")
# Every register spells these differently, and a brief that cannot read them
# prints a wall of bare coordinates. Geneva is the case that forced this: its
# 205 entries carry species_latin, circumference_cm, a real planted year and a
# vitality reading, and the brief showed 204 lines of "(unnamed)" because the
# extractor only knew `species`, `girth_cm` and `age_register`. The whole point
# of a register-led pass is that these four fields arrive for free, so failing
# to print them turns the cheapest kind of pass back into the expensive kind.
SPECIES_FIELDS = ("species", "species_latin", "species_scientific", "species_en",
                  "especie", "essence", "taxon", "scientific_name")


def first_field(t, exact, prefixes=()):
    """First non-empty value among named fields, then any field with these prefixes.

    The prefix half is the whole point, and it exists because enumerating
    spellings failed twice in two days. On 2026-08-16 Geneva's brief printed 204
    bare coordinates because the extractor knew `species` but not
    `species_latin`; the fix added eight spellings. On 2026-08-17 the Slovak
    register, imported the night before, printed 31 bare coordinates because it
    uses `name_sk` and `species_sk`, which were not among the eight. A register
    per country means a language suffix per country, so the list can never be
    finished by hand. Prefixes end the class instead of adding to the list.
    """
    for f in exact:
        if t.get(f):
            return t[f]
    for k in sorted(t):
        if any(k.startswith(p) for p in prefixes) and t.get(k):
            return t[k]
    return None
AGE_FIELDS = ("age_register", "age_band", "age_estimate_years", "age_estimate",
              "age_approx", "planted", "plant_year", "year_planted")
VITALITY_FIELDS = ("vitality", "health", "condition", "etat", "state",
                   "development_stage")
# Girth in metres, from whatever the register happened to publish. Diameter
# fields are converted with pi and the result is still called a girth, because
# that is what the reader of the brief needs; the source unit is the trap here,
# and it has already bitten once (ICNF publishes metres in a column our import
# named girth_cm, so a 2.84 m trunk read as under three centimetres).
GIRTH_FIELDS_M = ("girth_m",)
GIRTH_FIELDS_CM = ("girth_cm", "circumference_cm", "girth", "trunk_girth")
DIAMETER_FIELDS_CM = ("diameter_cm", "dbh_cm")


def girth_m(t):
    import math as _m
    for f in GIRTH_FIELDS_M:
        if t.get(f):
            try:
                return float(t[f])
            except (TypeError, ValueError):
                pass
    for f in GIRTH_FIELDS_CM:
        if t.get(f):
            try:
                return float(t[f]) / 100.0
            except (TypeError, ValueError):
                pass
    for f in DIAMETER_FIELDS_CM:
        if t.get(f):
            try:
                return float(t[f]) * _m.pi / 100.0
            except (TypeError, ValueError):
                pass
    if t.get("dbh_mm"):
        try:
            return float(t["dbh_mm"]) * _m.pi / 1000.0
        except (TypeError, ValueError):
            pass
    return None


PLACE_FIELDS = ("comune", "concelho", "city", "municipality", "place", "locality",
                "lugar", "freguesia", "address", "area", "area_en", "district",
                "neighbourhood", "province", "prefecture", "distrito", "region",
                "arrondissement")


def fold(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def cities():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        d = json.load(open(f))
        trees = d.get("trees") or []
        if not trees:
            continue
        pts = [(t["location"]["latitude"], t["location"]["longitude"]) for t in trees]
        out.append({
            "city": d["city"], "slug": os.path.basename(f)[:-5], "n": len(trees),
            "photos": sum(1 for t in trees if (t.get("photo") or {}).get("url")),
            "approx": sum(1 for t in trees if t.get("location_precision") == "approximate"),
            "spread": max((km(a, b) for a in pts for b in pts), default=0.0),
            "ids": sorted(t["id"] for t in trees),
            "points": pts,
            "lat": sum(p[0] for p in pts) / len(pts),
            "lng": sum(p[1] for p in pts) / len(pts),
        })
    return out


def register_entries():
    """Yield every register entry, normalized: lat, lng, name, species, girth_m,
    age, place, file. Handles both flat entries and GeoJSON features."""
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "registers", "*.json"))):
        d = json.load(open(path))
        if not isinstance(d, dict):
            continue
        fname = os.path.basename(path)
        for t in (d.get("entries") or []) + (d.get("trees") or []):
            if t.get("group"):
                continue
            if "properties" in t and "geometry" in t:
                t = t.get("properties") or {}
            la, lo = t.get("latitude"), t.get("longitude")
            if la is None or lo is None:
                continue
            yield {
                "lat": float(la), "lng": float(lo),
                "name": first_field(t, NAME_FIELDS, ("name_", "nom_", "nombre")),
                "species": first_field(t, SPECIES_FIELDS, ("species_", "espec", "essence")),
                "girth_m": girth_m(t),
                "age": first_field(t, AGE_FIELDS, ("age_", "planted")),
                "vitality": first_field(t, VITALITY_FIELDS, ("vital", "health", "condition")),
                "place": first_field(t, PLACE_FIELDS, ("locality", "localita", "place_",
                                                       "address", "site_")),
                "file": fname,
            }


def candidates_near(lat, lng, radius=SAME_CITY_KM):
    out = []
    for e in register_entries():
        d = km((lat, lng), (e["lat"], e["lng"]))
        if d <= radius:
            e["dist"] = d
            out.append(e)
    return sorted(out, key=lambda e: e["dist"])


_MINED = None


def mined_points():
    """Every tree an earlier pass already judged, with its coordinate and verdict.

    passcheck deduped register candidates against PUBLISHED trees only, so a tree
    a previous pass had already rejected came back in the next brief looking
    fresh. That is not theoretical: the Rome pass of 2026-08-10 spent its whole
    window rediscovering, by hand, that all 38 of its "candidates within 20 km"
    were already leads or blocked entries, and shipped nothing. The join was left
    to the agent to do by NAME, which the project's own rule forbids everywhere
    else, because registers and our own files spell the same tree differently.

    Matching is by coordinate, like the published check, so no spelling can fool
    it. Entries without a coordinate (roughly a third) cannot be matched this way
    and stay listed in the leads section below, unchanged.

    Leads files have never had one enforced coordinate schema, and a pass that
    cannot find the number silently drops the entry rather than erroring, which
    is worse: it looks handled. Proof case, Como, 2026-08-17: a pass spent its
    window re-confirming three "blocked" entries the brief resurfaced as fresh,
    because they carried coordinates under `coordinates_lat_lng` (one entry
    holding all three trees' points as a list of pairs) and
    `coordinates_lat_lng_sample`, neither of which the original `lat`/`lng`/
    `location.*` lookup below knew to read. The SAME pass had already caught
    and logged this exact gap two days earlier (2026-08-15, recorded in this
    city's own leads file) without it being fixed, which is the CLAUDE.md
    ratchet: a lesson on two different days becomes a check, not a third note.
    A repo-wide scan the same day found a `coordinates: [lat, lng]` flat-pair
    shape in 17 more entries across 6 other cities (including this run's own
    freshly written Bratislava leads), silently invisible the same way.
    _extract_coords() below is intentionally permissive about the field name
    and about one point vs many, because the failure mode here is a missed
    match, never a false one (a bad coordinate just fails the near-radius
    check downstream).
    """
    global _MINED
    if _MINED is not None:
        return _MINED
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "leads", "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        for kind in ("leads", "blocked"):
            for e in (d.get(kind) or []):
                if not isinstance(e, dict):
                    continue
                why = (e.get("why_not_published") or e.get("reason")
                       or e.get("why") or e.get("status") or "")
                for lat, lng in _extract_coords(e):
                    out.append({"lat": lat, "lng": lng, "kind": kind,
                                "name": e.get("name", "?"), "why": why,
                                "species": e.get("species", ""),
                                "file": os.path.basename(f)})
    _MINED = out
    return out


def _as_latlng(v):
    """A [lat, lng] or (lat, lng) pair, numeric, or None if it isn't one."""
    if (isinstance(v, (list, tuple)) and len(v) == 2
            and all(isinstance(x, (int, float)) for x in v)):
        return (float(v[0]), float(v[1]))
    return None


def _extract_coords(e):
    """Every coordinate pair findable in one leads/blocked entry, whatever the
    field is called. Known shapes seen across data/leads/*.json: lat/lng,
    latitude/longitude, a location{} sub-object with either, a flat
    `coordinates: [lat, lng]` pair, and Como's `coordinates_lat_lng[_sample]`,
    which can itself be one pair or a list of pairs (one blocked entry
    standing in for several physically distinct trees at the same site).
    """
    loc = e.get("location") if isinstance(e.get("location"), dict) else e
    lat = loc.get("latitude", loc.get("lat"))
    lng = loc.get("longitude", loc.get("lng"))
    if isinstance(lat, (int, float)) and isinstance(lng, (int, float)):
        return [(float(lat), float(lng))]

    for key in ("coordinates", "coordinates_lat_lng", "coordinates_lat_lng_sample"):
        v = e.get(key)
        if v is None:
            continue
        single = _as_latlng(v)
        if single:
            return [single]
        if isinstance(v, list):
            pairs = [p for p in (_as_latlng(item) for item in v) if p]
            if pairs:
                return pairs
    return []


def _genus(species):
    """Every genus named in a species string, lowercased. The cheapest species
    guard there is, and enough: Cedrus is not Brahea.

    Returns a SET, not a single word, because a blocked entry sometimes
    describes several distinct trees at one site in one combined field
    ("American Sycamore (Platanus occidentalis), Southern Magnolia (Magnolia
    grandiflora), Strawberry Tree (Arbutus unedo)" for Como's Villa Saporiti
    grouping). Taking the naive first word of that string gives "american",
    which matches no register candidate's genus and silently defeats the
    match for all three trees it was meant to cover. Genus names in
    parentheses are trusted as the Latin binomial; bare text falls back to
    its own first word so a plain "Platanus occidentalis" still works.
    """
    if not species:
        return set()
    s = str(species)
    parens = re.findall(r"\(([^)]+)\)", s)
    out = set()
    for p in parens:
        words = re.sub(r"[^A-Za-z ]", " ", p).strip().lower().split()
        if words:
            out.add(words[0])
    if not out:
        words = re.sub(r"[^A-Za-z ]", " ", s).strip().lower().split()
        if words:
            out.add(words[0])
    return out


def _looks_latin(species):
    """Does this string name a scientific genus, rather than a vernacular one?

    Latin genus names are capitalised and ours arrive either in parentheses
    ("Pedunculate Oak (Quercus robur)") or as a bare binomial ("Platanus
    occidentalis"). A register's own-language vernacular does not capitalise:
    "dub letny", "magnolia Soulangova", "lipa malolista". So a capitalised
    candidate genus is the test, and it is deliberately cheap rather than a
    taxonomy lookup.
    """
    if not species:
        return False
    s = str(species)
    parens = re.findall(r"\(([^)]+)\)", s)
    for p in parens:
        w = re.sub(r"[^A-Za-z ]", " ", p).strip().split()
        if w and w[0][:1].isupper():
            return True
    if parens:
        return False
    w = re.sub(r"[^A-Za-z ]", " ", s).strip().split()
    return bool(w) and w[0][:1].isupper()


def already_judged(lat, lng, species=None):
    """The lead or blocked entry at this spot, or None. Nearest wins.

    Two guards against a false match, which is the dangerous direction here: a
    wrong hit HIDES a real candidate, while a miss only costs the pass a second
    look. First, the radius is far tighter than the published-tree check (25 m
    against 80 m), because a lead and a register row describing the same tree
    usually come from the same survey and agree closely, while distinct trees in
    a dense park sit tens of metres apart. Second, when both sides name a
    species and the genus differs, it is not the same tree whatever the distance
    says. Both were written after a Himalayan Cedar matched a Mexican Blue Palm
    80 m away in Villa Sciarra.
    """
    g = _genus(species)
    hits = []
    for m in mined_points():
        d = km((lat, lng), (m["lat"], m["lng"]))
        if d > LEAD_MATCH_KM:
            continue
        mg = _genus(m.get("species"))
        # The veto only applies when BOTH sides are naming a Latin genus. A
        # vernacular name in a language we are not comparing against carries no
        # genus information, and letting it veto a coordinate match silently
        # destroys the dedup: on 2026-08-17 the extractor learned to read the
        # Slovak register's `species_sk`, and Bratislava's brief immediately went
        # from 8 unmined candidates to 26, because "dub letny" shares no token
        # with "Pedunculate Oak (Quercus robur)" and every already-judged lead
        # started reading as fresh. A miss costs a second look; a false miss
        # costs a whole pass rediscovering what an earlier one already rejected,
        # which is the Rome window this mechanism exists to prevent.
        if g and mg and _looks_latin(species) and _looks_latin(m.get("species")) \
                and g.isdisjoint(mg):
            continue
        hits.append((d, m))
    return min(hits, key=lambda h: h[0])[1] if hits else None


def centre_from_registers(key):
    """A new city has no coordinates of ours yet. Infer a centre by matching the
    place name against the registers' own locality fields."""
    # Word-bounded, not bare containment. "assen" is inside "kassen" (the
    # greenhouses of Paleis Het Loo), so `--brief Assen` centred on Apeldoorn,
    # 55 km away, and told a night run it was deepening the wrong city. Same
    # shape as the Graz/Grazie miss the docstring above describes, which was
    # left in place because the fallback was called a heuristic. It still is;
    # this only stops it matching inside a longer word, which never was a real
    # match. Found 2026-08-22 while staging Assen.
    if not key:
        return None
    pattern = re.compile(r"(?<![a-z0-9])%s(?![a-z0-9])" % re.escape(key))
    hits = [e for e in register_entries() if pattern.search(fold(e["place"]))]
    if not hits:
        return None
    lats = sorted(e["lat"] for e in hits)
    lngs = sorted(e["lng"] for e in hits)
    return (lats[len(lats) // 2], lngs[len(lngs) // 2])


def centre_from_any_name(arg):
    """Locate a place's centre. Our own coordinate table goes FIRST, because it
    is verified ground truth; the register-substring search that used to run
    first is a heuristic and heuristics produce false positives. Proof case,
    2026-08-17: "graz" (Austria) is a substring of "Grazie" (as in Madonna
    delle Grazie, Le Grazie), an unrelated Italian place name, folded-string
    containment with no word boundary. `key in fold(place)` matched three
    Italian MASAF register entries and centred the whole brief on Ancona
    (43.70,13.90) instead of Graz (47.07,15.44), which would have sent a
    verify pass hunting register trees 900km from the actual city with no
    error message telling it so.
    """
    key = fold(arg)
    reverse = {fold(v): k for k, v in ALIAS.items()}
    candidates = (key, fold(ALIAS.get(key, "")), fold(reverse.get(key, "")))

    coords = os.path.join(ROOT, "data", "city-coords.json")
    if os.path.exists(coords):
        table = json.load(open(coords, encoding="utf-8"))
        folded = {fold(k): v for k, v in table.items()}
        for candidate in candidates:
            hit = folded.get(candidate)
            if hit:
                return (hit[0], hit[1])

    # Fallback for a place not yet in our coordinate table: infer a centre by
    # matching the place name against the registers' own locality fields. A
    # register files its trees under SUBURBS, so Melbourne's 546 entries sit
    # under Hawthorn, Kew and Camberwell and the word Melbourne appears in
    # none of them; this is what finds a real city with no coordinate of its
    # own yet. Same class of bug as the Genoa/Genova alias miss above; that
    # one was a name, this one is a hierarchy. Substring, not word-bounded, so
    # still capable of a Graz-shaped false positive for a place NOT already in
    # city-coords.json; add it there rather than trust a bad match from here.
    for candidate in candidates:
        if not candidate:
            continue
        centre = centre_from_registers(candidate)
        if centre:
            return centre
    return None


def _research_trees(loaded):
    """A *-verified.json is an array, but one pass delivered {"trees": [...]}
    and the pending check crashed instead of reading it. Tolerate both."""
    if isinstance(loaded, dict):
        return loaded.get("trees") or []
    return loaded if isinstance(loaded, list) else []


def pending_research():
    """Research files holding trees that are NOT yet published.

    Exists because "needs a story" is not the same question as "is not
    published", and briefing on the first one sent a write pass after seven
    trees on 2026-08-08 when only three were real: nyc_011-013 and ams_011 had
    been merged into their city files that morning, and the research files were
    stale leftovers nobody had deleted. The pass caught it and refused to write
    duplicates, which is the only reason good live prose was not overwritten.

    The published city file is the truth. A research entry whose id already
    lives in data/cities is finished work, whatever the research file says.

    UNLESS the id is a collision rather than a match, which is the case this
    check got badly wrong on 2026-08-10. A batch was prepared with ids starting
    at bcn_011 from a stale assumption that Barcelona held ten trees; it held
    33, so all eighteen ids belonged to different live trees. Matching on id
    alone, this function reported the whole file as published and told the pass
    to delete it. Thirteen unwritten trees would have gone, and merging as
    briefed would have overwritten eighteen indexed URLs.

    So an id match is only believed when the coordinates agree. Same tree, same
    place; a research entry sitting hundreds of metres from the live tree whose
    id it claims is a collision, and it is reported loudly rather than silently
    counted as done. This is the same rule the register and lead matching
    already follow: position cannot be fooled by a label."""
    live, live_pt, live_all_pts = set(), {}, []
    for f in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        for t in json.load(open(f)).get("trees", []):
            live.add(t["id"])
            loc = t.get("location") or {}
            if loc.get("latitude") is not None:
                pt = (loc["latitude"], loc["longitude"])
                live_pt[t["id"]] = pt
                live_all_pts.append((t["id"], str(t.get("name"))[:46], pt))

    def same_tree(t):
        """Is this research entry really the live tree that holds its id?"""
        pt = live_pt.get(t["id"])
        loc = t.get("location") or {}
        if not pt or loc.get("latitude") is None:
            return True          # cannot tell; trust the id, as before
        return km(pt, (loc["latitude"], loc["longitude"])) <= 0.15

    # A different id can still be the same tree. hee_010 and hil_008
    # (2026-08-28) sat within centimetres of already-published hee_003 and
    # hil_006, same register entry, and a write pass produced a second story
    # for each before the duplicate was noticed by hand. An id match alone
    # cannot catch this because the ids never collided; only the coordinates
    # do. 50m is deliberately tighter than the 150m same_tree() threshold
    # above: that one is asking "is this still the same tree I already know
    # the id for", this is asking "is this an entirely unrelated id that
    # happens to sit on top of a live tree", which needs more confidence to
    # avoid flaring on two genuinely close but different specimens.
    DUPLICATE_KM = 0.05

    def find_duplicate(t):
        loc = t.get("location") or {}
        if loc.get("latitude") is None:
            return None
        pt = (loc["latitude"], loc["longitude"])
        best = None
        for oid, name, opt in live_all_pts:
            if oid == t.get("id"):
                continue
            d = km(pt, opt)
            if d <= DUPLICATE_KM and (best is None or d < best[2]):
                best = (oid, name, d)
        return best

    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "research", "*-verified.json"))):
        try:
            rows = _research_trees(json.load(open(f)))
        except Exception:
            continue
        unpublished, stale, collisions, duplicates = [], 0, [], []
        for t in rows:
            if not t.get("id"):
                continue
            if t["id"] not in live:
                dup = find_duplicate(t)
                if dup:
                    duplicates.append((t, dup))
                else:
                    unpublished.append(t)
            elif same_tree(t):
                stale += 1
            else:
                collisions.append(t)
        if unpublished or stale or collisions or duplicates:
            out.append((os.path.relpath(f, ROOT), unpublished, stale, collisions, duplicates))
    return out


def print_pending():
    rows = pending_research()
    if not rows:
        print("\nNothing pending: every verified tree is published.")
        return
    print("\nVERIFIED BUT NOT YET PUBLISHED (brief a write pass on these, and only these):")
    for path, unpublished, stale, collisions, duplicates in rows:
        if unpublished:
            need = sum(1 for t in unpublished if not t.get("story"))
            print(f"  {path}: {len(unpublished)} unpublished "
                  f"({need} still need a story, {len(unpublished) - need} written and ready to merge)")
            for t in unpublished[:6]:
                print(f"      {t['id']} {str(t.get('name'))[:46]}")
        if duplicates:
            print(f"  !! {path}: {len(duplicates)} entries sit within 50m of an ALREADY-PUBLISHED "
                  f"tree under a DIFFERENT id. Do not write these; check by hand, then fold into "
                  f"a lead marked duplicate and remove from this file.")
            for t, (oid, name, d) in duplicates[:8]:
                print(f"      {t['id']} {str(t.get('name'))[:40]}  -> looks like {oid} {name} "
                      f"({int(d * 1000)}m away)")
        if collisions:
            print(f"  !! {path}: {len(collisions)} entries claim an id that belongs to a "
                  f"DIFFERENT live tree.")
            print(f"     These are NOT published and this file is NOT stale. Merging as-is "
                  f"would overwrite live, indexed trees (hard rule 3).")
            print(f"     Reassign them to free ids before writing or merging:")
            for t in collisions[:8]:
                print(f"      {t['id']} {str(t.get('name'))[:46]}")
        if stale:
            print(f"  {path}: {stale} entries ALREADY PUBLISHED, this file is stale; "
                  f"delete it once the rest is merged")


def _ranked_city_names():
    """Every distinct city name/slug the queue ranks on its own, folded.

    Loaded once, used only to stop the distance fallback below from folding a
    separately-ranked town into a nearby published one just because the two
    happen to sit under SAME_CITY_KM apart. Assisi is the case that found this:
    its own centroid sits about 19 km from Perugia's, under the 20 km bar, so
    --brief assisi resolved to "ALREADY PUBLISHED as Perugia" and would have
    delivered a hermitage and two city gates that are landmarks of Assisi, not
    Perugia, into perugia-verified.json. CITY_QUEUE.md ranks them as two
    different cities with two different slugs for a reason a pure radius
    cannot see: a reader searching one would never accept the other as an
    answer. Returns a dict fold(name-or-slug) -> real name, so a caller can
    tell that a match belongs to a DIFFERENT ranked city than the one nearby.
    """
    try:
        doc = json.load(open(os.path.join(ROOT, "data", "city-queue.json")))
    except Exception:
        return {}
    out = {}
    for c in doc.get("cities", []):
        name = c.get("city")
        if not name:
            continue
        out[fold(name)] = name
        if c.get("slug"):
            out[fold(c["slug"])] = name
    return out


def resolve(arg, live):
    """Returns (match_or_None, coord_or_None). Distance is the real test."""
    coord = None
    parts = arg.replace(",", " ").split()
    if len(parts) == 2:
        try:
            coord = (float(parts[0]), float(parts[1]))
        except ValueError:
            coord = None
    if coord:
        match = min(live, key=lambda c: km(coord, (c["lat"], c["lng"])), default=None)
        if match and km(coord, (match["lat"], match["lng"])) > SAME_CITY_KM:
            match = None
        return match, coord
    key = fold(arg)
    key = fold(ALIAS.get(key, key))
    match = next((c for c in live if fold(c["city"]) == key or fold(c["slug"]) == key), None)
    if match is None:
        # name did not match a live city directly; try locating it via the
        # registers and distance-checking against every live city, which is how
        # Napoli/Naples-class misses get caught even without an alias entry
        coord = centre_from_any_name(arg)
        if coord:
            near = min(live, key=lambda c: km(coord, (c["lat"], c["lng"])), default=None)
            if near and km(coord, (near["lat"], near["lng"])) <= SAME_CITY_KM:
                # Refuse the fold when the queried name is itself a ranked
                # city distinct from `near` (the Assisi/Perugia case): being
                # within SAME_CITY_KM is evidence of a shared register pull
                # radius, not evidence they are the same place.
                ranked = _ranked_city_names()
                queried_ranked = ranked.get(key)
                if queried_ranked and fold(queried_ranked) != fold(near["city"]):
                    return None, coord
                match = near
    return match, coord


INFLIGHT = os.path.join(ROOT, "data", "in-flight.json")


def _now():
    return datetime.datetime.now(datetime.timezone.utc)


def night_run_expiry_hours(default=2.5):
    """How long a night-run claim can possibly be alive, derived not remembered.

    A night-run claim cannot outlive the job holding it, so the honest number is
    the workflow's own cap plus a little slack. Writing it down instead made it
    wrong: this file said "the job is killed at 60 minutes" and set 1.5 hours,
    while timeout-minutes had been 120 since 2026-08-17 (c61b64c). Under a
    two-hour window that expiry frees a city out from under a run that is still
    working on it, which is the opposite of what the claim is for.

    run_health.py already reads this same number the same way. A constant
    describing a value that lives in another file goes stale silently, which is
    the lesson this project has now learned in three separate files."""
    try:
        wf = os.path.join(ROOT, ".github", "workflows", "nightly.yml")
        with open(wf, encoding="utf-8") as fh:
            m = re.search(r"^\s*timeout-minutes:\s*(\d+)", fh.read(), re.M)
        return round(int(m.group(1)) / 60.0 + 0.5, 2) if m else default
    except OSError:
        return default


def load_inflight():
    """The claim file, with expired claims already dropped.

    Returns (doc, live_claims). A claim older than expire_hours is ignored, so a
    session that dies mid-pass cannot block a city forever: the worst case is
    that the next run waits out the remainder of the window.

    A night run's claim expires sooner, and the number is not a preference: the
    job is killed at 60 minutes by timeout-minutes in nightly.yml, so a claim by
    night-run older than 90 minutes CANNOT belong to a pass that is still
    working. Four hours was simply the session number applied to a holder that
    cannot live that long. On 2026-08-15 a run claimed six cities for a write
    pass, ended eleven minutes later having written nothing, and locked the top
    of the queue until noon; under this rule it would have been free by 09:30."""
    try:
        doc = json.load(open(INFLIGHT))
    except Exception:
        return {"expire_hours": 4, "claims": []}, []
    default_hours = doc.get("expire_hours", 4)
    by_holder = dict(doc.get("expire_hours_by_holder", {}))
    by_holder["night-run"] = night_run_expiry_hours()
    live = []
    for c in doc.get("claims", []):
        try:
            at = datetime.datetime.fromisoformat(c["claimed_at"])
            if at.tzinfo is None:
                at = at.replace(tzinfo=datetime.timezone.utc)
        except Exception:
            continue
        age = (_now() - at).total_seconds() / 3600.0
        hours = by_holder.get(c.get("by"), default_hours)
        if age < hours:
            c = dict(c, age_hours=round(age, 1))
            live.append(c)
    return doc, live


def save_inflight(doc, claims):
    doc["claims"] = [{k: v for k, v in c.items() if k != "age_hours"}
                     for c in claims]
    with open(INFLIGHT, "w") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def claims_for(target, live):
    key = fold(target)
    out = []
    for c in live:
        ck = fold(c.get("target", ""))
        # match either spelling: a claim on Padova blocks a pass on Padua
        if ck == key or ALIAS.get(ck) == ALIAS.get(key, key) or \
                ALIAS.get(ck, ck) == key or ck == ALIAS.get(key, key):
            out.append(c)
    return out


def print_inflight(target, live):
    """Print what is being worked on, loudest for the place being asked about."""
    mine = claims_for(target, live) if target else []
    if mine:
        print("\n  !! ALREADY CLAIMED, DO NOT DISPATCH:")
        for c in mine:
            print(f"     {c['target']} ({c['kind']}) claimed by {c.get('by', '?')} "
                  f"{c['age_hours']}h ago")
        print("     Another run is on this right now. Pick a different target, or")
        print("     --release it first if you know that pass is dead.")
    others = [c for c in live if c not in mine]
    if others:
        print("\n  in flight elsewhere: " + ", ".join(
            f"{c['target']}({c['kind']}, {c['age_hours']}h)" for c in others))


def default_holder():
    """Who is claiming: a night run, or THIS session specifically.

    Every local session used to claim as the bare string "session", and on
    2026-08-17 there were three of them running against this one checkout at
    once. That makes the lock transparent exactly between the parties it exists
    to separate: `--brief <place> --as session` satisfies the holder check no
    matter which session actually claimed the place, so two sessions can each
    open a brief for the same city and neither is warned. That is the Padova
    collision the lock was built for, 89,000 tokens for nine stories written
    twice, and the local case was never covered.

    Claude Code exports CLAUDE_CODE_SESSION_ID, so a session can name itself.
    Eight characters is plenty to tell concurrent sessions apart and keeps
    in-flight.json readable. Falls back to the bare "session" when nothing
    identifies us, which is the old behaviour rather than a crash.
    """
    if os.environ.get("GITHUB_RUN_ID"):
        return "night-run"
    sid = (os.environ.get("CLAUDE_CODE_SESSION_ID")
           or os.environ.get("CLAUDE_SESSION_ID") or "")
    return f"session-{sid[:8]}" if sid else "session"


# How many places one holder may have open at once. Two is a working pair: a
# verify running while the previous city's write is merged. Three is already a
# stretch and four is spraying.
MAX_OPEN_CLAIMS = 3


def do_claim(target, kind, by):
    doc, live = load_inflight()

    # The prompt has said "claim only what this window can finish" since
    # 2026-08-13, and it has been ignored twice: fourteen cities claimed that
    # day for zero published, and eight on 2026-08-17 in a twelve-minute run
    # that produced nothing. A claim nobody finishes fences a city off from
    # every other run for up to ninety minutes, so the top of the queue ends up
    # locked behind work that was never done. A lesson that lands twice becomes
    # a mechanism here rather than a third writing of the same sentence.
    mine = [c for c in live if c.get("by") == by]
    if len(mine) >= MAX_OPEN_CLAIMS:
        print(f"REFUSED: you already hold {len(mine)} open claims "
              f"({', '.join(c.get('target', '?') for c in mine)}).")
        print("Finish and release one before claiming another. A claim nobody")
        print("finishes locks that city away from every other run until it expires.")
        print(f"  python3 scripts/passcheck.py --release {mine[0].get('target', '<place>')}")
        return 1

    existing = claims_for(target, live)
    if existing:
        c = existing[0]
        print(f"REFUSED: {c['target']} ({c['kind']}) is already claimed by "
              f"{c.get('by', '?')}, {c['age_hours']}h ago.")
        print("Pick another target, or --release it if that pass is dead.")
        return 1
    live.append({"target": target, "kind": kind, "by": by,
                 "claimed_at": _now().replace(microsecond=0).isoformat()})
    save_inflight(doc, live)
    print(f"CLAIMED {target} ({kind}) by {by}.")
    print("Commit and push data/in-flight.json now, or the night runs cannot see it.")
    print(f"Release it when the output is merged: "
          f"python3 scripts/passcheck.py --release {target}")
    return 0


def do_release(target):
    doc, live = load_inflight()
    keep = [c for c in live if c not in claims_for(target, live)]
    if len(keep) == len(live):
        print(f"no live claim on {target} (already released, or it expired)")
    else:
        print(f"released {target}")
    save_inflight(doc, keep)
    return 0


def print_blocklist():
    bl = os.path.join(ROOT, "data", "fetch-blocklist.json")
    if not os.path.exists(bl):
        return
    hosts = json.load(open(bl))["hosts"]
    print("\nHOSTS THAT COST A WINDOW (they are why every fetch gets a hard timeout):")
    # Two entry schemas exist (the original behaviour/cost/seen fields, and a
    # 2026-08-08 addition using host/noted/symptom); normalize rather than
    # pick one, since a third addition should not break this a second time.
    def desc(v):
        return v.get("behaviour") or v.get("symptom") or ""
    for h, v in sorted(hosts.items(), key=lambda kv: 0 if "hang" in desc(kv[1]) else 1):
        d = desc(v)
        mark = "!!" if "hang" in d else "  "
        print(f" {mark} {h}: {d}. {v['workaround']}")
    print("    Every fetch: curl -m 20 (or timeout= on urllib). A hang burns the "
          "window; a refusal costs a second.")


def print_archived_notes(slug, place):
    """What CURATION.md and LOG.md already said about this place, including
    what has since moved to archive/.

    Hidde, 2026-08-08: "we willen geen bruikbare kennis verwijderen, we moeten
    slim oordelen wat weg kan en niet." Archiving moves nothing out of
    existence, but a file nothing reads is lost in practice, and telling runs
    to remember to grep is exactly the kind of rule this project has watched
    fail twice. So the grep runs here, automatically, at the one moment the
    knowledge matters: the brief. Age decides what moves; relevance decides
    what surfaces.
    """
    import re
    needles = {place.lower(), slug.replace("-", " ").lower()}
    hits = []
    files = [os.path.join(ROOT, f) for f in ("CURATION.md", "LOG.md")]
    files += sorted(glob.glob(os.path.join(ROOT, "archive", "*.md")))
    for f in files:
        if not os.path.exists(f):
            continue
        rel = os.path.relpath(f, ROOT)
        heading = ""
        for line in open(f, encoding="utf-8", errors="ignore"):
            if line.startswith("## "):
                heading = line[3:].strip()
                continue
            low = line.lower()
            # Word boundaries, or "cork" matches "Amur cork tree" and the
            # brief fills with noise the reader learns to skip.
            if any(re.search(r"\b" + re.escape(n) + r"\b", low)
                   for n in needles if len(n) > 3):
                snippet = re.sub(r"\s+", " ", line).strip()
                hits.append((rel, heading, snippet[:150]))
    if not hits:
        return
    print(f"\nALREADY WRITTEN ABOUT {place.upper()} (newest first, "
          f"{len(hits)} mention(s); read before repeating a hunt):")
    seen = set()
    shown = 0
    for rel, heading, snippet in hits:
        if heading in seen:
            continue
        seen.add(heading)
        print(f"  [{rel}] {heading}")
        print(f"      {snippet}")
        shown += 1
        if shown >= 6:
            break
    if len(seen) > shown:
        print(f"  ...and more: grep -ri \"{place}\" CURATION.md LOG.md archive/")


def print_wikidata(slug, pub_pts):
    """The CC0 Wikidata candidates harvested by scripts/wikidata_harvest.py.
    Banked 2026-08-09 (1,185 candidates, 660 with images) and wired here the
    same day, because a feed nothing reads is not a feed. Sitelinked articles
    are where second sources live; an image link is a photo candidate.

    `probably_ours` is a one-time flag set at harvest time (2026-08-09) and
    never updated afterwards, so a candidate published AFTER the harvest still
    reads as fresh forever. Found 2026-08-21: a Lyon verify pass fully
    re-researched Q63253791 (the Anne Frank chestnut) as "1 not already ours"
    and only discovered it was already live as lyo_012 by checking the city
    file directly before banking it. Re-checking proximity against the live
    published points every time this prints, the same way register candidates
    already are, catches this without needing the harvest to ever re-run."""
    try:
        d = json.load(open(os.path.join(ROOT, "data", "research",
                                        "wikidata-candidates.json")))
    except Exception:
        return set()
    block = d.get("cities", {}).get(slug)
    if not block:
        return set()
    fresh = [c for c in block.get("candidates", [])
             if not c.get("probably_ours")
             and not any(km((c["latitude"], c["longitude"]), p) <= NEAR_PUBLISHED_KM
                         for p in pub_pts)]
    if not fresh:
        return set()
    print(f"\nWIKIDATA CANDIDATES (CC0, harvested {block.get('harvested')}): "
          f"{len(fresh)} not already ours; discovery AND corroboration feed.")
    for c in fresh[:12]:
        img = "img" if c.get("image") else "no-img"
        des = f"  [{c['designation']}]" if c.get("designation") else ""
        print(f"  {c['qid']}  {c.get('label','?')[:52]:<54} "
              f"({c['latitude']:.5f},{c['longitude']:.5f}) {img}{des}")
    if len(fresh) > 12:
        print(f"  ...and {len(fresh)-12} more in data/research/wikidata-candidates.json")
    return {c["qid"] for c in fresh}


def print_wikidata_global(centre, pub_pts, already_shown=frozenset(), radius_km=15.0):
    """The broader CC0 Wikidata sweep (data/research/wikidata-remarkable-trees.json,
    19,775 trees worldwide, scripts/scout_next.py's `wikidata_points()` reads the
    same file), searched by radius rather than by per-city key.

    Found 2026-09-01: city_queue.py's OPENABLE-TODAY list counts supply from this
    file, but this brief only ever printed print_wikidata()'s older, 95-city
    harvest (wikidata-candidates.json), which does not cover a single one of the
    cities city_queue calls openable today. A run trusting the brief over the
    queue would see zero candidates and wrongly read that as no supply. This
    function is the missing link: same radius city_queue.py uses (15 km), same
    already-published and already-judged de-dup the register block above applies."""
    try:
        d = json.load(open(os.path.join(ROOT, "data", "research",
                                        "wikidata-remarkable-trees.json")))
    except Exception:
        return
    fresh = []
    for t in d.get("trees", []):
        if t.get("qid") in already_shown:
            continue
        lat, lng = t.get("latitude"), t.get("longitude")
        if lat is None or lng is None:
            continue
        if km(centre, (lat, lng)) > radius_km:
            continue
        if any(km((lat, lng), p) <= NEAR_PUBLISHED_KM for p in pub_pts):
            continue
        if already_judged(lat, lng, t.get("species")):
            continue
        fresh.append(t)
    if not fresh:
        return
    fresh.sort(key=lambda t: km(centre, (t["latitude"], t["longitude"])))
    print(f"\nWIKIDATA CANDIDATES, global sweep (CC0, {radius_km:.0f} km radius): "
          f"{len(fresh)} not already ours or already judged. Leads, not sources:")
    for t in fresh[:12]:
        img = "img" if t.get("commons_image") else "no-img"
        des = f"  [{t['designation']}]" if t.get("designation") else ""
        sp = f"  ({t['species']})" if t.get("species") else ""
        print(f"  {t['qid']}  {(t.get('name') or '?')[:40]:<42} "
              f"({t['latitude']:.5f},{t['longitude']:.5f}) {img}{sp}{des}")
    if len(fresh) > 12:
        print(f"  ...and {len(fresh)-12} more; re-run scout_next.py or filter "
              f"data/research/wikidata-remarkable-trees.json directly.")


def print_leads(slug):
    for kind in ("leads", "research"):
        for f in sorted(glob.glob(os.path.join(ROOT, "data", kind, f"*{slug}*"))):
            rel = os.path.relpath(f, ROOT)
            try:
                d = json.load(open(f))
            except Exception:
                print(f"\nEARLIER PASS NOTES: {rel} (not json; read it before searching)")
                continue
            print(f"\nEARLIER PASS ALREADY WORKED HERE: {rel}")
            if isinstance(d, dict):
                for lead in (d.get("leads") or []):
                    nm = lead.get("name", "?")
                    why = lead.get("why") or lead.get("status") or ""
                    print(f"  lead:    {nm}: {why[:110]}")
                for b in (d.get("blocked") or []):
                    nm = b.get("name", "?")
                    why = b.get("why") or b.get("reason") or ""
                    print(f"  BLOCKED: {nm}: {why[:110]} (never ship; do not re-research)")


def brief(arg, live):
    match, coord = resolve(arg, live)
    slug = match["slug"] if match else fold(arg)
    print(f"=== VERIFICATION BRIEF: {arg} ===")
    print("(generated by scripts/passcheck.py --brief; the facts below come from the")
    print(" project's own data and outrank any queue entry or memory of this place)\n")

    if match:
        centre = (match["lat"], match["lng"])
        nid = f"{match['ids'][-1][:4]}{int(match['ids'][-1][4:]) + 1:03d}"
        print(f"STATUS: ALREADY PUBLISHED as {match['city']} (/{match['slug']}): this is a DEEPEN pass.")
        print(f"  {match['n']} trees live, {match['photos']} with a photo, "
              f"{match['approx']} approximate pins, walk spans {match['spread']:.1f} km")
        print(f"  New entries start at id {nid}. Never edit the city file; deliver to")
        print(f"  data/research/{match['slug']}-verified.json (JSON array, one object per tree).")
    else:
        centre = coord or centre_from_any_name(arg)
        taken = sorted({i[:3] for c in live for i in c["ids"]})
        print("STATUS: NOT published, this would be a NEW city. Floor: 4 verified trees or no page.")
        print(f"  Pick a 3-letter id prefix NOT in: {' '.join(taken)}")
        print(f"  Deliver to data/research/{slug}-verified.json (JSON array, one object per tree).")

    print("\nTHE JOB, and only the job: VERIFY, do not write prose and do not hunt photos.")
    print("  Per candidate: (1) alive now, (2) species + age with two independent sources")
    print("  (one official register counts as one), (3) the exact spot, precision stated")
    print("  honestly. Rules, schema and register pitfalls: read BRIEF_RESEARCH.md at the")
    print("  repo root. Do NOT read CLAUDE.md; everything a verification pass needs is in")
    print("  that one file. APPEND each verified tree to the delivery file AS FOUND,")
    print("  never only at the end.")

    # Checked against every published tree, not just this target's own: a NEW
    # city's centre can sit close enough to an ALREADY published one that a
    # register or Wikidata candidate is actually somebody else's live tree.
    # Found 2026-09-01 dispatching a Jersey City brief: Q1407769 "Hangman's
    # Elm" (40.73190,-73.99860) is nyc_001, 8 km away, and would have printed
    # as fresh because only the target's own (empty, for a new city) point
    # list was ever checked.
    pub_pts = [p for c in live for p in c["points"]]

    if centre:
        cands = candidates_near(*centre)
        for e in cands:
            e["_pub"] = any(km((e["lat"], e["lng"]), p) <= NEAR_PUBLISHED_KM
                            for p in pub_pts)
            e["_judged"] = (None if e["_pub"]
                            else already_judged(e["lat"], e["lng"], e.get("species")))
        unmined = [e for e in cands if not e["_pub"] and not e["_judged"]]
        shown = unmined[:40] + [e for e in cands if e["_pub"] or e["_judged"]][:12]
        shown = sorted(shown, key=lambda e: e["dist"])
        print(f"\nCANDIDATES from official registers, licence already verified "
              f"({len(cands)} within {SAME_CITY_KM:.0f} km of {centre[0]:.4f},{centre[1]:.4f}):")
        print(f"  UNMINED, i.e. not published and not already judged by an earlier pass: "
              f"{len(unmined)} of {len(cands)}.")
        if cands and not unmined:
            print("  Every register tree within reach is already published or already")
            print("  recorded as a lead or blocked. There is no register work left here:")
            print("  new trees would have to come from web research, and a pass that")
            print("  hunts this register again will spend its window confirming that.")
        if not cands:
            print("  none: no imported register covers this area. Verification here is")
            print("  web research; scout the register first if one exists (OPEN_DATA_SURVEY.md).")
        for e in shown:
            already = e["_pub"]
            bits = [f"{e['dist']:4.1f} km", e["name"] or "(unnamed)"]
            if e["species"]:
                bits.append(e["species"])
            if e["girth_m"]:
                bits.append(f"girth {e['girth_m']:.1f} m")
            if e["age"]:
                bits.append(f"age {e['age']}")
            if e.get("vitality"):
                bits.append(str(e["vitality"]))
            bits.append(f"({e['lat']:.5f},{e['lng']:.5f})")
            bits.append(e["file"])
            line = "  " + "  ".join(str(b) for b in bits)
            if already:
                line += "  << within 80 m of a live tree: probably already published, check first"
            elif e["_judged"]:
                j = e["_judged"]
                tag = "BLOCKED" if j["kind"] == "blocked" else "already a lead"
                line += (f"\n        << {tag} by an earlier pass ({j['file']}): "
                         f"{j['why'][:150]}")
            print(line)
        if len(cands) > len(shown):
            print(f"  ...and {len(cands) - len(shown)} more; run passcheck again with a "
                  f"tighter coordinate if the cluster needs them.")
        print("  A register says protected, not worth the walk: judge each. Prefer trees")
        print("  that join a walkable cluster over better trees that stand alone.")
    else:
        print("\nCANDIDATES: no coordinates known for this place (not in any imported")
        print("  register). Give passcheck a coordinate, or accept that this pass is web")
        print("  research from zero and budget accordingly.")

    print_leads(slug)
    shown_qids = print_wikidata(slug, pub_pts) or set()
    if centre:
        print_wikidata_global(centre, pub_pts, shown_qids)
    print_archived_notes(slug, match["city"] if match else arg)
    print_blocklist()

    print("\nDISPATCH: paste this whole brief into the 'verify' subagent (.claude/agents/")
    print("verify.md). That agent definition pins the model to Sonnet, so the tiering is")
    print("mechanical: dispatching any other way is what needs a reason. Stories come")
    print("later from the 'write-stories' agent (Opus), 15 to 20 verified trees at once.")
    print("\nSTOP CONDITION: report what you have after roughly 40 minutes; do not run to")
    print("completeness. A pass never holds a whole city back on its own judgement: it")
    print("delivers what verifies and records the rest as leads with reasons.")
    print("\nWITH YOUR REPORT, return this line for data/agent-costs.json, filled in:")
    print(f'  {{"target": "{arg}", "kind": "verify", "tokens": <total>, "trees": 0, "note": "<one line>"}}')
    return 0


def print_claims():
    """Every claim standing right now, and how close each is to expiring.

    There was no way to ask this, which is why the continuation prompt in
    nightly.yml referenced a flag that did not exist. A run inheriting a window
    needs one question answered before anything else: what did the attempt
    before me lock, and is it mine to finish or to release."""
    doc, live = load_inflight()
    if not live:
        print("No claims standing. Every place is free.")
        return 0
    now = datetime.datetime.now(datetime.timezone.utc)
    default_hours = doc.get("expire_hours", 4)
    by_holder = dict(doc.get("expire_hours_by_holder", {}))
    by_holder["night-run"] = night_run_expiry_hours()
    print("%d claim(s) standing:\n" % len(live))
    for c in sorted(live, key=lambda x: str(x.get("claimed_at", ""))):
        by = c.get("by", "?")
        hours = by_holder.get(by, default_hours)
        left = "?"
        try:
            stamp = c.get("claimed_at") or c.get("at")
            at = datetime.datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))
            mins = hours * 60 - (now - at).total_seconds() / 60.0
            left = "%.0f min left" % mins if mins > 0 else "expiring now"
        except (TypeError, ValueError):
            pass
        print("  %-22s %-7s by %-22s %s" % (c.get("target", "?"), c.get("kind", "?"), by, left))
    print("\nFinish it or release it:")
    print("  python3 scripts/passcheck.py --release <place>")
    return 0


def main():
    args = sys.argv[1:]
    if "--claims" in args:
        return print_claims()
    if "--pending" in args:
        print_pending()
        return 0
    want_brief = "--brief" in args
    args = [a for a in args if a != "--brief"]
    if "--claim" in args:
        args.remove("--claim")
        kind = "verify"
        if "--kind" in args:
            i = args.index("--kind")
            kind = args[i + 1]
            del args[i:i + 2]
        by = default_holder()
        if "--by" in args:
            i = args.index("--by")
            by = args[i + 1]
            del args[i:i + 2]
        if not args:
            print("usage: passcheck.py --claim <place> [--kind verify|write|photo] [--by who]")
            return 1
        return do_claim(" ".join(args), kind, by)
    if "--release" in args:
        args.remove("--release")
        if not args:
            print("usage: passcheck.py --release <place>")
            return 1
        return do_release(" ".join(args))
    if not args:
        print(__doc__)
        return 1
    live = cities()
    arg = " ".join(args)
    _, inflight = load_inflight()
    if want_brief:
        # --as <who> lets the claim HOLDER print the brief for its own pass;
        # anyone else stays refused. Found five minutes after the lock shipped,
        # when it refused its own author the Rome brief he had just claimed.
        # Default to whoever we are, so the holder never has to type --as for
        # its own brief and a DIFFERENT session is still refused. Before this,
        # --as was required and every session answered to "session", which made
        # the lock invisible between concurrent local sessions.
        as_who = default_holder()
        if "--as" in args:
            i = args.index("--as")
            as_who = args[i + 1]
            del args[i:i + 2]
            arg = " ".join(args)
        mine = claims_for(arg, inflight)
        if mine and mine[0].get("by") != as_who:
            c = mine[0]
            print(f"\nREFUSED: no brief for {arg}. It is claimed by "
                  f"{c.get('by', '?')} ({c['kind']}, {c['age_hours']}h ago).")
            print("A brief for a claimed place is how two passes end up doing the")
            print("same work. If this claim is YOURS, rerun with --as "
                  f"{c.get('by', '<who>')}. Otherwise pick another target, or")
            print("--release it if you know that pass is dead.")
            return 1
        return brief(arg, live)

    match, coord = resolve(arg, live)
    print(f"\n=== passcheck: {arg} ===\n")
    if match:
        print(f"  ALREADY PUBLISHED as {match['city']} (/{match['slug']})")
        print(f"  {match['n']} trees, {match['photos']} with a photo, "
              f"{match['approx']} approximate pins, walk spans {match['spread']:.1f} km")
        print(f"  ids {match['ids'][0]} to {match['ids'][-1]}; "
              f"a deepening pass starts at {match['ids'][-1][:4]}{int(match['ids'][-1][4:]) + 1:03d}")
        print(f"  register trees within {SAME_CITY_KM:.0f} km: "
              f"{len(candidates_near(match['lat'], match['lng']))}")
        print("\n  => brief this as DEEPEN. Run with --brief for the paste-ready brief.")
    else:
        print("  NOT published. This would be a new city.")
        if coord:
            print(f"  register trees within {SAME_CITY_KM:.0f} km: {len(candidates_near(*coord))}")
        taken = sorted({i[:3] for c in live for i in c["ids"]})
        print(f"\n  id prefixes already in use ({len(taken)}): {' '.join(taken)}")
        print("  pick three letters that are NOT in that list.")
        print("\n  => run with --brief for the paste-ready brief.")

    print_inflight(arg, inflight)
    print_blocklist()
    slug = match["slug"] if match else fold(arg)
    for kind in ("leads", "research"):
        for f in sorted(glob.glob(os.path.join(ROOT, "data", kind, f"*{slug}*"))):
            try:
                d = json.load(open(f))
                counts = {k: len(v) for k, v in d.items() if isinstance(v, list)} if isinstance(d, dict) else {"items": len(d)}
            except Exception:
                counts = "not json"
            print(f"\n  {kind}: {os.path.relpath(f, ROOT)}  {counts}")
            print("     read it before researching: it says what was already rejected and why")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
