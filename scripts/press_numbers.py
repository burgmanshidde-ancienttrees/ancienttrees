#!/usr/bin/env python3
"""The numbers in drafts/press-pitch.md, recomputed from the published data.

A journalist who checks a figure and finds it stale never writes again, so the
pitch quotes nothing that this script cannot reproduce on the day it is sent.
Run it before sending; if a number moved, fix the pitch, not the number.

  python3 scripts/press_numbers.py          # the figures
  python3 scripts/press_numbers.py --csv    # + press-trees.csv to send along

One judgement lives in here rather than in the data, and it is stated openly:
NON_NATIVE is a hand-made list of species with no native European range. It is
deliberately conservative. Species native to a corner of Europe are NOT on it
even when they read as exotic (Oriental plane grows wild in Greece and the
Balkans, Turkish hazel and Caucasian wingnut reach the continent's edges), so
the headline percentage understates rather than flatters.
"""
import argparse
import csv
import glob
import json
import os
import re
import unicodedata
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EUROPE = {
    "United Kingdom", "Italy", "Netherlands", "Spain", "Portugal", "Poland",
    "France", "Belgium", "Greece", "Germany", "Austria", "Czech Republic",
    "Ireland", "Denmark", "Sweden", "Finland", "Hungary", "Croatia", "Serbia",
    "Romania", "Switzerland", "Norway", "Slovenia", "Slovakia", "Bulgaria",
    "Estonia", "Latvia", "Lithuania",
}

# Species with no native European range. Origin noted so the CSV can carry it
# and a desk can check the claim per tree rather than trusting the total.
NON_NATIVE = {
    "London Plane": "hybrid, arose in cultivation, no wild population",
    "Ginkgo": "China", "Camphor Tree": "East Asia",
    "Japanese Pagoda Tree": "China", "Southern Magnolia": "southeastern USA",
    "Coast Redwood": "California", "Giant Sequoia": "California",
    "Cedar of Lebanon": "Lebanon, Syria, Turkey", "Himalayan Cedar": "Himalaya",
    "Atlas Cedar": "North Africa", "Deodar Cedar": "Himalaya",
    "Persian Ironwood": "Iran, Azerbaijan", "Black Locust": "eastern USA",
    "Chinaberry": "South Asia", "Shellbark Hickory": "eastern USA",
    "Osage Orange": "south-central USA", "Bald Cypress": "southeastern USA",
    "Montezuma Cypress": "Mexico", "Mexican Cypress": "Mexico, Central America",
    "Tulip Tree": "eastern USA", "Silk Tree": "Asia",
    "Chilean Wine Palm": "Chile", "Canary Island Date Palm": "Canary Islands",
    "Mexican Blue Palm": "Mexico", "Norfolk Island Hibiscus": "Australia",
    "Australian Banyan": "Australia", "Moreton Bay Fig": "Australia",
    "Silky Oak": "Australia", "Jacaranda": "South America",
    "Ombu": "South America", "Dragon Tree": "Macaronesia",
    "Chusan Palm": "China", "Empress Tree": "China",
    "Chinese Windmill Palm": "China", "Honey Locust": "central USA",
    "Northern Catalpa": "central USA", "Southern Catalpa": "southeastern USA",
    "Red Oak": "eastern North America", "Black Walnut": "eastern USA",
    "American Sycamore": "eastern USA", "Blue Gum": "Australia",
    "Tree of Heaven": "China", "Weeping Willow": "China",
    "Black Mulberry": "southwest Asia", "White Mulberry": "China",
    "Avocado": "Mexico", "Loquat": "China", "Japanese Cedar": "Japan",
    "Monkey Puzzle": "Chile, Argentina", "Rubber Fig": "South Asia",
    "False Kapok": "South America", "Date Palm": "North Africa, west Asia",
    "California Fan Palm": "California", "Pecan": "southern USA",
}


def tree_slug(name):
    """The same slug build_site.py gives a tree page, so the CSV links land."""
    s = name.lower().replace("'", "").replace("\u2019", "")
    if s.startswith("the "):
        s = s[4:]
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def load():
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "data/cities/*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        d["_slug"] = os.path.basename(p)[:-5]
        out.append(d)
    return out


def base_name(species):
    return species.split("(")[0].strip()


def city_sheet(cities, name):
    """A localized press fact sheet: the raw material for pitching ONE city's
    desk its own story, which lands far more often than a continental statistic.

    Hidde, 2026-08-08, on the immigrants angle: "ik kan me niet voorstellen dat
    iemand iets met dit press verhaal gaat doen". He was right about the lead:
    a feature with no local face is a slow-news-day gamble. What local desks
    run is their own oldest tree, so every pitch to a city desk starts from
    this sheet instead. Facts only, no prose: the pitch stays hand-written per
    outlet, per the never-mass-send rule in OUTREACH.md.
    """
    key = name.lower()
    match = next((c for c in cities
                  if c["city"].lower() == key or c["_slug"] == key), None)
    if not match:
        print(f"no published city matches {name!r}")
        return 1
    trees = match["trees"]
    slug = match["_slug"]
    print(f"PRESS FACT SHEET: {match['city']}, {match['country']}")
    print(f"  page: https://ancienttrees.app/{slug}   trees: {len(trees)}")
    dated = sorted((t for t in trees if t.get("age_min")),
                   key=lambda t: -(t.get("age_min") or 0))
    if dated:
        t = dated[0]
        loc = t.get("location", {})
        print(f"\n  OLDEST: {t['name']}, {t.get('age_estimate', '?')}, "
              f"{t['species']}")
        print(f"    where: {loc.get('address', '')[:70]}")
        print(f"    page:  https://ancienttrees.app/{slug}/{tree_slug(t['name'])}")
        print(f"    story opens: {t.get('story', '')[:180]}...")
    photos = [t for t in trees if (t.get("photo") or {}).get("url")]
    print(f"\n  IMAGES: {len(photos)} of {len(trees)} trees have an "
          f"openly licensed photo (licence + credit on each tree page)")
    seasonal = [(t, t["best_time"]) for t in trees if t.get("best_time")]
    for t, bt in seasonal[:3]:
        months = ",".join(str(m) for m in bt.get("months", []))
        print(f"  SEASONAL HOOK: {t['name']}: {bt.get('label', '')} "
              f"(months {months})")
    nn_sp = [t for t in trees
             if t["species"].split("(")[0].strip() in NON_NATIVE]
    if nn_sp:
        print(f"  LOCAL IMMIGRANTS ANGLE: {len(nn_sp)} of {len(trees)} are "
              f"non-native species")
    print(f"\n  Every figure above regenerates from the published data; the "
          f"pitch itself is written by hand per outlet, never a template.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", action="store_true",
                    help="also write press-trees.csv for a journalist")
    ap.add_argument("--city", metavar="NAME",
                    help="print a localized press fact sheet for one city")
    args = ap.parse_args()

    if args.city:
        return city_sheet(load(), args.city)

    cities = load()
    trees = [(c, t) for c in cities for t in c["trees"]]
    eu = [(c, t) for c, t in trees if c["country"] in EUROPE]
    nn = [(c, t) for c, t in eu if base_name(t["species"]) in NON_NATIVE]

    print(f"Published: {len(trees)} trees, {len(cities)} cities, "
          f"{len({c['country'] for c in cities})} countries")
    print(f"In European cities: {len(eu)} trees across "
          f"{len({c['city'] for c, t in eu})} cities")
    print()
    print(f"HEADLINE: {len(nn)} of {len(eu)} trees in European cities are not "
          f"native European species = {100 * len(nn) / len(eu):.0f}%")
    print(f"          across {len({c['city'] for c, t in nn})} of "
          f"{len({c['city'] for c, t in eu})} European cities")

    plane = [(c, t) for c, t in eu if base_name(t["species"]) == "London Plane"]
    print(f"          London plane: {len(plane)} trees in "
          f"{len({c['city'] for c, t in plane})} cities, the commonest of all")
    print()

    counts = Counter(base_name(t["species"]) for c, t in nn)
    print("Top arrivals:")
    for s, n in counts.most_common(8):
        where = len({c["city"] for c, t in nn if base_name(t["species"]) == s})
        print(f"  {n:>3} trees in {where:>2} cities  {s} ({NON_NATIVE[s]})")

    dated = [(c, t) for c, t in nn if t.get("age_min")]
    dated.sort(key=lambda x: -(x[1].get("age_min") or 0))
    print("\nOldest arrivals:")
    for c, t in dated[:5]:
        print(f"  {t.get('age_estimate', '?'):<26} {t['name']} ({c['city']})")

    shots = sum(1 for c, t in trees if (t.get("photo") or {}).get("url"))
    print(f"\nImages: {shots} of {len(trees)} trees carry an openly licensed "
          f"photograph, each with its licence and required credit recorded.")

    if args.csv:
        path = os.path.join(ROOT, "press-trees.csv")
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["city", "country", "tree", "species", "origin",
                        "age_estimate", "latitude", "longitude",
                        "location_precision", "page", "photo_licence",
                        "photo_credit", "sources"])
            for c, t in trees:
                sp = base_name(t["species"])
                loc = t.get("location") or {}
                ph = t.get("photo") or {}
                slug = tree_slug(t["name"])
                w.writerow([
                    c["city"], c["country"], t["name"], t["species"],
                    NON_NATIVE.get(sp, "native to Europe"
                                   if c["country"] in EUROPE else ""),
                    t.get("age_estimate", ""), loc.get("latitude", ""),
                    loc.get("longitude", ""), t.get("location_precision", ""),
                    f"https://ancienttrees.app/{c['_slug']}/{slug}",
                    ph.get("license", ""), ph.get("attribution", ""),
                    " | ".join(t.get("verified_sources") or []),
                ])
        print(f"\nwrote {path} ({len(trees)} rows)")


if __name__ == "__main__":
    main()
