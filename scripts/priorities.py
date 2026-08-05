#!/usr/bin/env python3
"""Write PRIORITIES.md: what we have, how good it is, and what to do next.

Hidde, 2026-08-05: "ik raak een beetje de weg kwijt welke steden we goed hebben
gedaan, welke het interessantst zijn om op te pakken". So this is one generated
page instead of a memory, and it can be regenerated whenever the picture moves.

Three things get measured per published city, because they are what makes a page
worth opening: how many trees, how many carry a photo, and how tight the walk is.
Spread is the honest one. Cadiz spans 600 metres and reads as an afternoon;
Kyoto spans 35 km and does not, however good its trees are.

Sources found by the 2026-08-05 sweep are folded in by hand, because they are
verdicts on documents rather than anything a script can measure. Their evidence
sits in data/research/walks/ and data/research/_tree_walks_*.md.

    python3 scripts/priorities.py
"""
import glob
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cluster_register import load, cluster, km  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "PRIORITIES.md")
SAME_CITY_KM = 20.0

# Verdicts from the tree-walk sweep, 2026-08-05. GOLD means a source names trees
# individually with a location, so a pass is verify-and-write rather than search.
SOURCES = {
    "Paris": ("GOLD", "185 remarkable trees, ODbL, per tree: planting year, address, girth, height, coordinates"),
    "Brussels": ("GOLD", "582 trees, CC BY 4.0, plus three real tree walks in Ixelles"),
    "Vienna": ("GOLD", "434 Naturdenkmaeler, CC BY 4.0, plus a Baumkataster giving planting year and girth"),
    "Seville": ("GOLD", "2022 municipal inventory: WGS84 per tree, ownership, full dendrometry, and tree condition"),
    "Zaragoza": ("GOLD", "city book, 57 fichas with GPS and ownership stated per tree"),
    "Valencia": ("GOLD", "five municipal walking routes over 508 geolocated monumental trees"),
    "Madrid": ("GOLD", "regional catalogue, 280 trees with coordinates, 59 in the city, exclusion annex doubles as a dead list"),
    "Turin": ("GOLD", "official tourist-board route, 13.9 km, all 15 designated trees named, GPX download"),
    "Rome": ("GOLD", "Roma Capitale itineraries plus the Lazio decree, 212 rows parsed, 57 in the comune"),
    "Milan": ("GOLD", "13 monumental trees each with its own page carrying coordinates, plus a labelled trail in Parco Sempione"),
    "Naples": ("GOLD", "Campania's list embeds 417 rows, 55 in the comune, each linking a scheda with GPS and dimensions"),
    "Florence": ("GOLD", "comune PDF, 29 rows with coordinates and an ownership column, 14 of them private"),
    "Prague": ("GOLD", "three tree-by-tree walking routes with maps, over an official register of 196"),
    "Munich": ("GOLD", "117 Naturdenkmaeler covering about 200 trees, with species, address and coordinates"),
    "Barcelona": ("GOLD", "208-tree municipal register already imported, plus itineraries with CSV export"),
    "Genoa": ("GOLD", "Liguria states CC BY outright, the clearest licence in Italy; 25 geolocated stops found"),
    "Berlin": ("STRONG", "708 monuments, 638 trees, but spread over 12 Bezirke: pick one district, not the city"),
    "Utrecht": ("STRONG", "a 5 km route, 30 trees, each with Latin name and planting year"),
    "Amsterdam": ("STRONG", "free 2025 booklet, 30 centre trees, but no text layer so it needs eyes or OCR"),
    "Porto": ("STRONG", "eight municipal guided walks already cluster the city; trees unnamed publicly, ICNF fills that"),
    "Lisbon": ("WEAK", "the good artefact is a paid print book; free web has nothing tree by tree"),
    "Lyon": ("WEAK", "about 50 exceptional trees asserted, no published list"),
    "Budapest": ("WEAK", "100 curated notable trees inside a 236,000-tree cadastre, behind a JavaScript map"),
    "Bologna": ("WEAK", "7 to 9 designated trees in the comune: clears the floor, will not reach ten"),
    "Palermo": ("WEAK", "43 in the comune but the regional PDF 404s and the geoportal has a broken TLS chain"),
    "Bordeaux": ("WEAK", "1,763 designated points under Licence Ouverte with no species, name or age"),
    "Venice": ("NONE", "the whole Veneto register is about 110 trees and the provincial ones are mainland"),
    "Hamburg": ("NONE", "eleven Naturdenkmale in total and exactly one is a tree"),
    "Marseille": ("NONE", "the open data API returns zero tree datasets"),
    "Bilbao": ("NONE", "five designated specimens in all of Bizkaia, the flagships beyond the day-trip boundary"),
}

TOURIST = {  # hand-made, same list as backlog.py
    "roma", "firenze", "venezia", "milano", "napoli", "torino", "bologna", "verona",
    "siena", "pisa", "lucca", "palermo", "catania", "genova", "padova", "ravenna",
    "bergamo", "como", "assisi", "perugia", "trieste", "lecce", "matera", "rimini",
    "ferrara", "mantova", "parma", "modena", "cagliari", "siracusa", "taormina",
    "sorrento", "bolzano", "trento", "urbino", "orvieto", "viterbo", "caserta",
    "lisboa", "porto", "sintra", "coimbra", "braga", "guimaraes", "guimarães",
    "evora", "faro", "aveiro", "cascais", "tomar", "viana do castelo",
    "sevilla", "granada", "malaga", "málaga", "cordoba", "córdoba", "cadiz",
    "cádiz", "barcelona", "madrid", "valencia", "jaen", "huelva", "ronda", "almeria",
}


def published():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        d = json.load(open(f))
        trees = d.get("trees") or []
        if not trees:
            continue
        pts = [(t["location"]["latitude"], t["location"]["longitude"]) for t in trees]
        spread = max((km(a, b) for a in pts for b in pts), default=0.0)
        out.append({
            "city": d["city"], "country": d.get("country", ""),
            "slug": os.path.basename(f)[:-5], "n": len(trees),
            "photos": sum(1 for t in trees if (t.get("photo") or {}).get("url")),
            "approx": sum(1 for t in trees if t.get("location_precision") == "approximate"),
            "flagged": sum(1 for t in trees if t.get("curation_status") == "flagged"),
            "spread": spread,
            "lat": sum(p[0] for p in pts) / len(pts),
            "lng": sum(p[1] for p in pts) / len(pts),
        })
    return out


def register_supply(cities):
    """How many register trees sit within reach of each published city, and what
    walkable clusters exist in places we do not publish."""
    near = {c["slug"]: 0 for c in cities}
    fresh = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "registers", "*.json"))):
        pts, _ = load(path)
        if not pts:
            continue
        country = json.load(open(path)).get("country", "")
        for g in cluster(pts, 2.0):
            if len(g) < 4:
                continue
            lat = sum(pts[i]["lat"] for i in g) / len(g)
            lng = sum(pts[i]["lng"] for i in g) / len(g)
            best, best_d = None, 1e9
            for c in cities:
                d = km((lat, lng), (c["lat"], c["lng"]))
                if d < best_d:
                    best, best_d = c, d
            places = sorted({pts[i]["place"] for i in g if pts[i]["place"]})
            if best_d <= SAME_CITY_KM:
                near[best["slug"]] += len(g)
            else:
                fresh.append({
                    "n": len(g), "country": country,
                    "place": places[0] if places else f"{lat:.3f},{lng:.3f}",
                    "spread": max(km((pts[i]["lat"], pts[i]["lng"]), (pts[j]["lat"], pts[j]["lng"]))
                                  for i in g for j in g),
                    "tourist": any(p.lower() in TOURIST for p in places),
                })
    return near, fresh


def score_deepen(c, supply):
    """What is worth reopening: a good source, plenty of register trees waiting,
    and a page that is currently thin."""
    src = SOURCES.get(c["city"], ("", ""))[0]
    s = {"GOLD": 40, "STRONG": 22, "WEAK": 6}.get(src, 0)
    s += min(supply, 200) / 4.0
    s += max(0, 10 - c["n"]) * 2
    s += max(0, c["n"] - c["photos"]) * 1.5
    if c["spread"] > 8:
        s += 6  # a scattered city needs a tighter second walk more than anything
    return s


def main():
    cities = published()
    supply, fresh = register_supply(cities)
    # What actually changed today is the tree COUNT, not the file. A single
    # species rename touched almost every city file this afternoon and would
    # otherwise mark the whole site as worked on.
    base = os.popen("cd %s && git log --until='2026-08-05 00:00' -1 --format=%%H" % ROOT).read().strip()
    before = {}
    if base:
        listing = os.popen("cd %s && git ls-tree -r --name-only %s -- data/cities/" % (ROOT, base)).read().split()
        for f in listing:
            slug = os.path.basename(f)[:-5]
            raw = os.popen("cd %s && git show %s:%s" % (ROOT, base, f)).read()
            try:
                before[slug] = len(json.loads(raw).get("trees") or [])
            except Exception:
                pass
    today_slugs = {c["slug"]: (before.get(c["slug"]), c["n"])
                   for c in cities if before.get(c["slug"]) != c["n"]}

    L = []
    A = L.append
    A("# Priorities: what we have, and what to do next")
    A("")
    A("Generated by `python3 scripts/priorities.py`. Regenerate it rather than trusting it "
      "to stay true. Measured fields come from the data; the source verdicts come from the "
      "2026-08-05 tree-walk sweep, whose evidence is in `data/research/walks/`.")
    A("")
    A(f"**{len(cities)} places live, {sum(c['n'] for c in cities)} trees, "
      f"{sum(c['photos'] for c in cities)} with a photo.**")
    A("")

    A("## Touched today")
    A("")
    A("| place | trees | photos | walk | note |")
    A("|---|---|---|---|---|")
    for c in sorted(cities, key=lambda c: -c["n"]):
        if c["slug"] not in today_slugs:
            continue
        was, now = today_slugs[c["slug"]]
        note = "new today" if was is None else f"grew from {was} to {now}"
        A(f"| **{c['city']}** | {c['n']} | {c['photos']} | {c['spread']:.1f} km | {note} |")
    A("")

    A("## The best pages we have")
    A("")
    A("Ranked on what makes a page worth opening: a tight walk, enough trees, and photos.")
    A("")
    A("| place | trees | photos | walk spans | approximate pins |")
    A("|---|---|---|---|---|")
    good = [c for c in cities if c["n"] >= 5 and c["spread"] <= 3.5]
    for c in sorted(good, key=lambda c: (-(c["photos"] / max(c["n"], 1)), c["spread"]))[:12]:
        A(f"| {c['city']} | {c['n']} | {c['photos']} | {c['spread']:.1f} km | {c['approx']} |")
    A("")

    A("## Weakest published pages")
    A("")
    A("Live, and thin. A visitor arriving here from search gets least.")
    A("")
    A("| place | trees | photos | walk spans | why it is weak |")
    A("|---|---|---|---|---|")
    for c in sorted(cities, key=lambda c: (c["photos"] / max(c["n"], 1), -c["spread"]))[:10]:
        why = []
        if c["photos"] == 0:
            why.append("no photo at all")
        elif c["photos"] < c["n"] / 3:
            why.append("almost no photos")
        if c["spread"] > 10:
            why.append("not a walk, a driving tour")
        if c["approx"] > c["n"] / 2:
            why.append("most pins approximate")
        A(f"| {c['city']} | {c['n']} | {c['photos']} | {c['spread']:.1f} km | {', '.join(why) or 'thin'} |")
    A("")

    A("## The next 50, ranked")
    A("")
    A("Deepening a live page beats opening a new one when the supply is there: the page "
      "furniture already exists, the URL already ranks, and nothing new has to be written "
      "around it. `D` is deepen, `N` is new.")
    A("")
    A("| # | | place | why | supply |")
    A("|---|---|---|---|---|")
    rows = []
    for c in cities:
        s = score_deepen(c, supply.get(c["slug"], 0))
        if s <= 12:
            continue
        src, note = SOURCES.get(c["city"], ("", ""))
        why = note or f"{c['n']} published, {c['photos']} with a photo"
        rows.append((s, "D", c["city"], why, f"{supply.get(c['slug'], 0)} register trees nearby"))
    for f in fresh:
        s = (30 if f["tourist"] else 8) + min(f["n"], 30) + max(0, 4 - f["spread"]) * 3
        src, note = SOURCES.get(f["place"], ("", ""))
        if src == "GOLD":
            s += 30
        rows.append((s, "N", f["place"], note or f"{f['n']} register trees within {f['spread']:.1f} km",
                     f"{f['n']} in one cluster"))
    for city, (src, note) in SOURCES.items():
        if src in ("GOLD", "STRONG") and not any(r[2] == city for r in rows):
            rows.append((45 if src == "GOLD" else 25, "N", city, note, "source found, no register imported"))
    seen = set()
    rank = 0
    for s, kind, place, why, sup in sorted(rows, key=lambda r: -r[0]):
        if place in seen:
            continue
        seen.add(place)
        rank += 1
        if rank > 50:
            break
        A(f"| {rank} | {kind} | **{place}** | {why} | {sup} |")
    A("")
    A("Reading it: supply is candidate supply, never what ships. A walk is four to eight "
      "trees inside about two kilometres, the floor of four verified trees stands, and a "
      "cluster that thins out under verification gets no page.")
    A("")

    open(OUT, "w").write("\n".join(L) + "\n")
    print(f"wrote {OUT} ({len(L)} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
