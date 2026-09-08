#!/usr/bin/env python3
"""Has anybody official already said this tree is remarkable?

Written 2026-09-07, for Hidde's question about reader-added trees: "in the end
we want trees people find worth the visit, not an all-trees database. So how do
we check that."

THE SPLIT THIS SCRIPT SITS ON. Deciding whether somebody would cross town for a
tree is judgement and stays judgement. What is NOT judgement, and was being
done by nobody, is asking whether a government already answered it. We hold
59,000-odd register rows with coordinates, and every one of them is a state
body saying this particular tree is monumental, protected or remarkable. A
reader's tree that lands within thirty metres of one of those arrives with an
official source attached: the two-independent-sources bar half met, for free,
before anyone spends a minute looking.

It cuts both ways and the second way matters more. A tree in a country whose
register we hold, standing nowhere near any entry in it, is a tree the state
looked at and did not designate. That is not a refusal, because registers miss
plenty and a reader standing in front of something is evidence too. It is a
reason to spend the judgement somewhere else first.

    python3 scripts/corroborate.py 52.0907 5.1214      # one coordinate
    python3 scripts/corroborate.py --leads             # every reader lead on file

WHAT IT IS NOT. Not a licence check: a register being open enough to IMPORT is
a separate question answered in OPEN_DATA_SURVEY.md, and this only reads what
is already on disk. Not a publish decision: a match makes a lead worth looking
at sooner, never worth skipping the bar.
"""
import argparse
import glob
import json
import math
import os
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTERS = os.path.join(ROOT, "data", "registers")
LEADS = os.path.join(ROOT, "data", "leads", "_sightings.json")

# Metres per degree of latitude. Longitude is scaled by the cosine of the
# latitude at the point, which is accurate enough at the tens-of-metres range
# this script works in and needs no projection library.
M_PER_DEG = 111_320.0


def rows():
    """Every register row that carries a coordinate, flattened.

    Register files disagree about their own shape (some hold `entries`, some
    `trees`, some are a bare list) and about field names, which is what a
    register layer looks like when it comes from thirty different states. The
    two fields every one of them agrees on are latitude and longitude, so those
    are required and everything else is best effort.
    """
    out = []
    for path in sorted(glob.glob(os.path.join(REGISTERS, "*.json"))):
        try:
            with open(path) as fh:
                doc = json.load(fh)
        except Exception:
            continue
        items = doc.get("entries") or doc.get("trees") or (doc if isinstance(doc, list) else [])
        if not isinstance(items, list):
            continue
        source = os.path.basename(path)[:-5]
        designation = (doc.get("designation") if isinstance(doc, dict) else None) or ""
        for r in items:
            if not isinstance(r, dict):
                continue
            lat = r.get("latitude", r.get("lat"))
            lng = r.get("longitude", r.get("lng"))
            if lat is None or lng is None:
                continue
            try:
                lat, lng = float(lat), float(lng)
            except (TypeError, ValueError):
                continue
            out.append({
                "lat": lat, "lng": lng, "source": source, "designation": designation,
                "name": (r.get("name") or r.get("name_it") or r.get("name_cz")
                         or r.get("name_nl") or r.get("nome") or ""),
                "species": (r.get("species") or r.get("species_cz") or r.get("species_nl")
                            or r.get("especie") or ""),
                "girth_cm": r.get("girth_cm"),
                "height_m": r.get("height_m"),
            })
    return out


def metres(lat1, lng1, lat2, lng2):
    dy = (lat2 - lat1) * M_PER_DEG
    dx = (lng2 - lng1) * M_PER_DEG * math.cos(math.radians((lat1 + lat2) / 2))
    return math.hypot(dx, dy)


def nearest(lat, lng, table, within=100.0, limit=3):
    """The closest register entries, nearest first.

    A bounding box first, because 59,000 great-circle calculations per lead is
    a second of nothing when a degree of latitude settles it.
    """
    dlat = within / M_PER_DEG
    dlng = dlat / max(math.cos(math.radians(lat)), 0.01)
    near = [r for r in table
            if abs(r["lat"] - lat) <= dlat and abs(r["lng"] - lng) <= dlng]
    hits = []
    for r in near:
        d = metres(lat, lng, r["lat"], r["lng"])
        if d <= within:
            hits.append({**r, "distance_m": round(d, 1)})
    hits.sort(key=lambda h: h["distance_m"])
    return hits[:limit]


def verdict(hits):
    """One line a person can act on, and never a decision."""
    if not hits:
        return ("unlisted", "no register entry within 100 m: only this reader has "
                            "said it is remarkable, so it needs the normal bar")
    top = hits[0]
    if top["distance_m"] <= 30:
        return ("designated", "a register entry sits %.0f m away (%s%s): an official body "
                              "already calls this one remarkable"
                % (top["distance_m"], top["source"],
                   ", " + top["name"] if top["name"] else ""))
    return ("near", "the nearest register entry is %.0f m away (%s): possibly the same "
                    "tree, possibly its neighbour, so check before leaning on it"
            % (top["distance_m"], top["source"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("coords", nargs="*", type=float, help="latitude longitude")
    ap.add_argument("--leads", action="store_true",
                    help="check every reader lead in data/leads/_sightings.json")
    ap.add_argument("--within", type=float, default=100.0)
    # OFF BY DEFAULT ON --leads, ON BY DEFAULT FOR ONE COORDINATE. The offline
    # half costs nothing and can run over hundreds of leads in a second; the
    # web half is three requests per lead and would be a small flood. So a
    # sweep asks for it explicitly and a single lookup, which is what somebody
    # runs while deciding about one tree, gets it without having to know.
    ap.add_argument("--web", action="store_true",
                    help="also ask Wikipedia and Wikidata (implied for one coordinate)")
    ap.add_argument("--no-web", action="store_true", help="registers only")
    ap.add_argument("--country", help="the country, so the local Wikipedia is searched too")
    a = ap.parse_args()

    table = rows()
    if not a.leads and len(a.coords) != 2:
        ap.error("give a latitude and a longitude, or --leads")

    if a.leads:
        try:
            with open(LEADS) as fh:
                leads = json.load(fh).get("leads", [])
        except Exception:
            print("no reader leads on file yet")
            return 0
        print(f"{len(leads)} reader lead(s) against {len(table)} register rows\n")
        for l in leads:
            lat, lng = l.get("latitude"), l.get("longitude")
            if lat is None or lng is None:
                print(f"  {(l.get('name') or 'unnamed')[:40]:42} no coordinate, cannot check")
                continue
            hits = nearest(lat, lng, table, a.within)
            tag, why = verdict(hits)
            print(f"  {(l.get('name') or 'unnamed')[:40]:42} {tag.upper():11} {why}")
            if a.web and not a.no_web:
                for t, qid, m, lang in wikipedia_trees_near(lat, lng, l.get("country")):
                    print(f"  {'':42} {'WRITTEN UP':11} {lang}.wikipedia: {t} ({qid}) {m} m away")
        return 0

    lat, lng = a.coords
    hits = nearest(lat, lng, table, a.within)
    tag, why = verdict(hits)
    print(f"{tag.upper()}: {why}")
    for h in hits:
        bits = [b for b in (h["name"], h["species"],
                            f"{h['girth_cm']} cm round" if h.get("girth_cm") else None,
                            f"{h['height_m']} m tall" if h.get("height_m") else None) if b]
        print(f"  {h['distance_m']:6.1f} m  {h['source']}  {' | '.join(bits)}")

    if not a.no_web:
        written = wikipedia_trees_near(lat, lng, a.country)
        if written:
            print("\nSomebody has written this one up:")
            for t, qid, m, lang in written:
                print(f"  {m:6d} m  {lang}.wikipedia  {t}  ({qid})")
            print("One source, not two. Worth an hour, not worth shipping on.")
        else:
            print("\nNo encyclopaedia article about a tree within 300 m either.")
    return 0




# ------------------------------------------------------------------------
# ACTIVELY LOOKING, not only reading what we already hold (2026-09-08)
#
# Hidde, after an arborist in Stockholm answered our outreach mail with a tree
# we had missed: "maar naast het register is het een idee om actief te gaan
# zoeken?" Yes, and the same day proved both halves of why.
#
# Everything above this line reads registers already on disk, offline and free.
# That is the cheapest check there is and it is also the narrowest: it can only
# corroborate a tree in a country whose register we happen to have imported.
# Valkasken, the ash on Langholmen that Linnaeus wrote down in the 1740s, has a
# Swedish Wikipedia article of its own and we hold no Swedish register, so the
# offline check said UNLISTED about a tree with three centuries of paper.
#
# So: ask Wikipedia what it knows within a few hundred metres of the pin, then
# ask Wikidata whether any of those articles is about a TREE rather than about
# the bridge or the boat club beside it. That second step is what makes this
# usable in every language at once: `P31 = Q811534` means "individual tree" and
# says so identically in Swedish, Japanese and Portuguese, where a keyword list
# would need maintaining forever and would still miss things.
#
# Measured on the two cases that prompted it, in opposite directions:
#   Valkasken (59.32038, 18.032699)  -> sv:Valkasken at 5 m, P31 Q811534. Found.
#   Nara nra_011 (34.6892, 135.8439) -> temple halls only, no tree anywhere.
# The second is the important one. It is the tree we retired the same morning
# for having no source at all, and this agrees: nobody has written about it.
#
# WHAT THIS IS NOT. Not a publish decision. A Wikipedia article is one source
# and the bar is two, so a hit makes a lead worth an hour rather than worth
# shipping. And a MISS is not a refusal: registers and encyclopaedias both miss
# plenty, and a person standing in front of something is evidence too.
#
# Wikidata's SPARQL endpoint would answer all of this in one query and is not
# used on purpose: on the day this was written it was rate-limiting to one
# request per minute during an outage. The plain MediaWiki API has no such
# problem and degrades to a printed line rather than an exception.

# The language a tree is most likely to be written up in, by the country we
# file it under. English is always searched as well, so this only has to add
# the local wiki. Countries we publish in and nothing else; an unlisted one
# falls back to English, which is a smaller net rather than a broken one.
LOCAL_WIKI = {
    "Netherlands": "nl", "Belgium": "nl", "Italy": "it", "Spain": "es",
    "Japan": "ja", "Germany": "de", "Austria": "de", "Switzerland": "de",
    "Portugal": "pt", "Brazil": "pt", "France": "fr", "Luxembourg": "fr",
    "Poland": "pl", "Czech Republic": "cs", "Slovakia": "sk", "Lithuania": "lt",
    "Latvia": "lv", "Estonia": "et", "Denmark": "da", "Sweden": "sv",
    "Norway": "no", "Finland": "fi", "Iceland": "is", "Greece": "el",
    "Turkey": "tr", "Hungary": "hu", "Bulgaria": "bg", "Romania": "ro",
    "Serbia": "sr", "Croatia": "hr", "Slovenia": "sl", "Cyprus": "el",
    "China": "zh", "Taiwan": "zh", "South Korea": "ko", "Thailand": "th",
    "Mexico": "es", "Peru": "es",
}

# Wikidata classes that mean "this article is about one particular tree".
# Q811534 is `individual tree`; Q10884 is `tree`, which a few older items use
# directly. Anything else nearby is a bridge, a park or a boat club.
TREE_CLASSES = {"Q811534", "Q10884"}
_UA = {"User-Agent": "AncientTrees/1.0 (ancienttrees.app)"}


def _api(url, timeout=20):
    """Every fetch gets a hard timeout and returns None rather than raising.

    CLAUDE.md's own rule after Valencia died twice on a host that accepts a
    connection and never answers: a refusal costs a second, a hang costs the
    window.
    """
    try:
        req = urllib.request.Request(url, headers=_UA)
        return json.load(urllib.request.urlopen(req, timeout=timeout))
    except Exception:
        return None


def wikipedia_trees_near(lat, lng, country=None, radius_m=300):
    """Articles about an individual TREE within radius_m of a coordinate.

    Returns [(title, qid, metres, lang)], nearest first, possibly empty. Never
    raises: a network failure reads as "found nothing", which is the same thing
    a run does with it.
    """
    langs, seen = [], set()
    for lang in (LOCAL_WIKI.get(country or ""), "en"):
        if lang and lang not in seen:
            seen.add(lang)
            langs.append(lang)

    found = []
    for lang in langs:
        q = urllib.parse.urlencode({
            "action": "query", "list": "geosearch", "format": "json",
            "gscoord": "%s|%s" % (lat, lng), "gsradius": int(radius_m), "gslimit": 25})
        doc = _api("https://%s.wikipedia.org/w/api.php?%s" % (lang, q))
        hits = ((doc or {}).get("query") or {}).get("geosearch") or []
        if not hits:
            continue
        titles = [h["title"] for h in hits]
        q2 = urllib.parse.urlencode({
            "action": "query", "prop": "pageprops", "ppprop": "wikibase_item",
            "format": "json", "titles": "|".join(titles)})
        doc2 = _api("https://%s.wikipedia.org/w/api.php?%s" % (lang, q2))
        pages = ((doc2 or {}).get("query") or {}).get("pages") or {}
        qid_of = {p["title"]: (p.get("pageprops") or {}).get("wikibase_item")
                  for p in pages.values()}
        qids = [q for q in qid_of.values() if q]
        if not qids:
            continue
        # 50 entities per call is the documented cap for anonymous callers.
        classes = {}
        for i in range(0, len(qids), 50):
            doc3 = _api("https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({
                "action": "wbgetentities", "props": "claims", "format": "json",
                "ids": "|".join(qids[i:i + 50])}))
            for k, v in ((doc3 or {}).get("entities") or {}).items():
                classes[k] = {c["mainsnak"]["datavalue"]["value"]["id"]
                              for c in (v.get("claims") or {}).get("P31", [])
                              if c["mainsnak"].get("datavalue")}
        for h in hits:
            qid = qid_of.get(h["title"])
            if qid and classes.get(qid, set()) & TREE_CLASSES:
                found.append((h["title"], qid, int(h["dist"]), lang))
    found.sort(key=lambda r: r[2])
    return found


if __name__ == "__main__":
    raise SystemExit(main())
