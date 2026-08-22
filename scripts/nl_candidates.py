#!/usr/bin/env python3
"""Pick publishable candidates for a Dutch city out of the LRMB register.

Hidde, 2026-08-22: "zoek de top 25 steden die groot zijn en waar bomen van
staan in dit register en we nog 0 van op de website hebben staan en ga ze
maken". This is the deterministic half of that, so no agent ever spends
tokens on arithmetic. It filters, translates, dates, clusters and ranks;
what it cannot do is judge whether a tree is worth the walk, find the second
source, or write the story.

Three things it enforces that a pass would otherwise have to remember:

  - visitable == "ja" only. Hard rule 10 is answered by the register itself,
    which is the whole reason this register is cheap.
  - n_trees == 1 only. A row saying 60 is a beech hedge, and an avenue is not
    a collectible point (CLAUDE.md, the Rambla test).
  - Species names come from SPECIES below, which matches what the site
    already publishes, because hard rule 9 groups the species pages on the
    exact string.

The register's `history` field describes the SITE, not the tree. It is passed
through as context and labelled as such, because joining it to the tree is
the bridge claim CLAUDE.md names as the way invented stories actually get
written here.
"""
import json, math, sys, argparse, os, re

_REG_CACHE = {}

def _register():
    if "d" not in _REG_CACHE:
        _REG_CACHE["d"] = json.load(open(REG))
    return _REG_CACHE["d"]

def looks_felled(history):
    """The register's own test for an entry whose history says THIS tree is gone.

    The regex lives in the register file rather than here, because it was
    derived from the register's prose and belongs with it. Hidde's rule is
    "we doen niet aan dode bomen", and a filter that runs beats a filter
    somebody has to remember on tree 400 of 1029.
    """
    if not history:
        return False
    rx = _register().get("dead_entries_regex")
    return bool(rx and re.search(rx, history, re.I))

REG = "data/registers/netherlands-lrmb.json"
THIS_YEAR = 2026

# Dutch register name -> the exact string the site already uses.
SPECIES = {
 "bruine beuk": "Copper Beech (Fagus sylvatica f. purpurea)",
 "beuk": "European Beech (Fagus sylvatica)",
 "gewone beuk": "European Beech (Fagus sylvatica)",
 "treurbeuk": "Weeping Beech (Fagus sylvatica 'Pendula')",
 "witte paardenkastanje": "Horse Chestnut (Aesculus hippocastanum)",
 "paardenkastanje": "Horse Chestnut (Aesculus hippocastanum)",
 "rode paardenkastanje": "Red Horse Chestnut (Aesculus x carnea)",
 "zomereik": "Pedunculate Oak (Quercus robur)",
 "wintereik": "Sessile Oak (Quercus petraea)",
 "amerikaanse eik": "Northern Red Oak (Quercus rubra)",
 "moeraseik": "Pin Oak (Quercus palustris)",
 "gewone plataan": "London Plane (Platanus x acerifolia)",
 "oosterse plataan": "Oriental Plane (Platanus orientalis)",
 "hollandse linde": "Common Lime (Tilia x europaea)",
 "zomerlinde": "Large-leaved Lime (Tilia platyphyllos)",
 "winterlinde": "Small-leaved Lime (Tilia cordata)",
 "zilverlinde": "Silver Lime (Tilia tomentosa)",
 "krimlinde": "Crimean Lime (Tilia x euchlora)",
 "hollandse iep": "Dutch Elm (Ulmus x hollandica)",
 "pluimiep": "Dutch Elm (Ulmus x hollandica)",
 "gladde iep": "Field Elm (Ulmus minor)",
 "ruwe iep": "Wych Elm (Ulmus glabra)",
 "canadese populier": "Canadian Poplar (Populus x canadensis)",
 "zwarte populier": "Black Poplar (Populus nigra)",
 "valse acacia": "Black Locust (Robinia pseudoacacia)",
 "zilveresdoorn": "Silver Maple (Acer saccharinum)",
 "gewone esdoorn": "Sycamore (Acer pseudoplatanus)",
 "noorse esdoorn": "Norway Maple (Acer platanoides)",
 "treurwilg": "Weeping Willow (Salix babylonica)",
 "schietwilg": "White Willow (Salix alba)",
 "tamme kastanje": "Sweet Chestnut (Castanea sativa)",
 "gewone es": "European Ash (Fraxinus excelsior)",
 "treures": "Weeping Ash (Fraxinus excelsior 'Pendula')",
 "kaukasische vleugelnoot": "Caucasian Wingnut (Pterocarya fraxinifolia)",
 "moerascypres": "Bald Cypress (Taxodium distichum)",
 "trompetboom": "Southern Catalpa (Catalpa bignonioides)",
 "libanonceder": "Cedar of Lebanon (Cedrus libani)",
 "atlasceder": "Atlas Cedar (Cedrus atlantica)",
 "venijnboom": "European Yew (Taxus baccata)",
 "taxus": "European Yew (Taxus baccata)",
 "zwarte walnoot": "Black Walnut (Juglans nigra)",
 "okkernoot": "Common Walnut (Juglans regia)",
 "walnoot": "Common Walnut (Juglans regia)",
 "japanse notenboom": "Ginkgo (Ginkgo biloba)",
 "ginkgo": "Ginkgo (Ginkgo biloba)",
 "mammoetboom": "Giant Sequoia (Sequoiadendron giganteum)",
 "watercipres": "Dawn Redwood (Metasequoia glyptostroboides)",
 "haagbeuk": "Hornbeam (Carpinus betulus)",
 "zoete kers": "Wild Cherry (Prunus avium)",
 "magnolia": "Magnolia (Magnolia sp.)",
 "ruwe berk": "Silver Birch (Betula pendula)",
 "grove den": "Scots Pine (Pinus sylvestris)",
 "oostenrijkse den": "Austrian Pine (Pinus nigra)",
 "zwarte moerbei": "Black Mulberry (Morus nigra)",
 "witte moerbei": "White Mulberry (Morus alba)",
 "tulpenboom": "Tulip Tree (Liriodendron tulipifera)",
 "acacia": "Black Locust (Robinia pseudoacacia)",
 "linde": "Lime (Tilia sp.)",
 "iep": "Elm (Ulmus sp.)",
 "eik": "Oak (Quercus sp.)",
 "plataan": "Plane (Platanus sp.)",
 "amberboom": "Sweet Gum (Liquidambar styraciflua)",
 "colorado zilverspar": "White Fir (Abies concolor)",
 "kaukasische spar": "Oriental Spruce (Picea orientalis)",
 "moerascipres": "Bald Cypress (Taxodium distichum)",
 "papier moerbei": "Paper Mulberry (Broussonetia papyrifera)",
 "papiermoerbei": "Paper Mulberry (Broussonetia papyrifera)",
 "valse christusdoorn": "Honey Locust (Gleditsia triacanthos)",
 "vederesdoorn": "Box Elder (Acer negundo)",
 "vleugelnoot": "Caucasian Wingnut (Pterocarya fraxinifolia)",
 "zwarte berk": "River Birch (Betula nigra)",
 "zilverspar": "Silver Fir (Abies alba)",
 "fijnspar": "Norway Spruce (Picea abies)",
 "douglasspar": "Douglas Fir (Pseudotsuga menziesii)",
 "lariks": "Larch (Larix sp.)",
 "japanse lariks": "Japanese Larch (Larix kaempferi)",
 "europese lariks": "European Larch (Larix decidua)",
 "gewone robinia": "Black Locust (Robinia pseudoacacia)",
 "italiaanse populier": "Lombardy Poplar (Populus nigra 'Italica')",
 "witte abeel": "White Poplar (Populus alba)",
 "grauwe abeel": "Grey Poplar (Populus x canescens)",
 "gewone vlier": "Elder (Sambucus nigra)",
 "meidoorn": "Hawthorn (Crataegus sp.)",
 "veldesdoorn": "Field Maple (Acer campestre)",
 "japanse kers": "Japanese Cherry (Prunus serrulata)",
 "sierkers": "Ornamental Cherry (Prunus sp.)",
 "treurbeuk ": "Weeping Beech (Fagus sylvatica 'Pendula')",
 "zuilbeuk": "Dawyck Beech (Fagus sylvatica 'Dawyck')",
 "hemelboom": "Tree of Heaven (Ailanthus altissima)",
 "christusdoorn": "Honey Locust (Gleditsia triacanthos)",
 "notenboom": "Common Walnut (Juglans regia)",
 "els": "Alder (Alnus sp.)",
 "zwarte els": "Black Alder (Alnus glutinosa)",
 "berk": "Birch (Betula sp.)",
 "esdoorn": "Maple (Acer sp.)",
 "populier": "Poplar (Populus sp.)",
 "wilg": "Willow (Salix sp.)",
 "es": "Ash (Fraxinus sp.)",
 "beukenhaag": "European Beech (Fagus sylvatica)",
}

def haversine(a, b, c, d):
    R = 6371.0
    p1, p2 = math.radians(a), math.radians(c)
    dp, dl = math.radians(c - a), math.radians(d - b)
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(h))

def species_of(name):
    """Longest matching Dutch name wins, so 'bruine beuk' beats 'beuk'."""
    n = (name or "").strip().lower()
    n = re.sub(r"[\"'].*", "", n).strip()
    best = None
    for dutch, canon in SPECIES.items():
        if n == dutch or n.startswith(dutch + " ") or (" " + dutch) in (" " + n):
            if best is None or len(dutch) > len(best[0]):
                best = (dutch, canon)
    return best[1] if best else None

def own_name(name):
    """The register sometimes appends the tree's own name to the species."""
    n = (name or "").strip()
    m = re.search(r"[\"'](.+?)[\"']", n)
    if m:
        return m.group(1).strip()
    low = n.lower()
    for dutch in sorted(SPECIES, key=len, reverse=True):
        if low.startswith(dutch) and len(n) > len(dutch) + 2:
            return n[len(dutch):].strip(" ,-")
    return None

def ages(band):
    try:
        a, b = band.split("-")
        lo, hi = int(a), int(b)
    except Exception:
        return None, None, None
    amin, amax = THIS_YEAR - hi, THIS_YEAR - lo
    if amax - amin <= 10:
        est = "roughly %d years, from a registered planting date around %d" % (
            round((amin + amax) / 2 / 5) * 5, hi)
    else:
        est = "roughly %d to %d years, from the register's planting band of %s" % (
            round(amin / 10) * 10, round(amax / 10) * 10, band)
    return amin, amax, est

def load(city):
    d = _register()["entries"]
    out = []
    for e in d:
        if e.get("municipality") != city:
            continue
        if (e.get("visitable") or "").lower() != "ja":
            continue
        if e.get("n_trees") != 1:
            continue
        if not e.get("latitude"):
            continue
        if looks_felled(e.get("history")):
            continue
        sp = species_of(e.get("name"))
        amin, amax, est = ages(e.get("planted_band") or "")
        out.append({
            "nr": e["nr"], "register_name": e.get("name"), "own_name": own_name(e.get("name")),
            "species": sp, "species_unmapped": None if sp else e.get("name"),
            "age_min": amin, "age_max": amax, "age_estimate": est,
            "planted_band": e.get("planted_band"),
            "latitude": e["latitude"], "longitude": e["longitude"],
            "place": e.get("place"), "setting": e.get("setting"),
            "owner_category": e.get("owner_category"), "honour_class": e.get("honour_class"),
            "form": e.get("form"), "reason": e.get("reason"),
            "site_history": e.get("history"),
        })
    return out

def cluster(trees, km=2.0):
    left, groups = list(trees), []
    while left:
        seed = left.pop(0)
        g = [seed]
        again = True
        while again:
            again = False
            for t in list(left):
                if any(haversine(t["latitude"], t["longitude"], o["latitude"], o["longitude"]) <= km for o in g):
                    g.append(t); left.remove(t); again = True
        groups.append(g)
    groups.sort(key=len, reverse=True)
    return groups

def score(t):
    s = 0
    if t["honour_class"] == "ja": s += 40
    if t["age_min"]: s += min(t["age_min"] / 5, 40)
    if t["own_name"]: s += 12
    if t["setting"] in ("park", "landgoed", "begraafplaats", "plein"): s += 10
    if t["site_history"]: s += 6
    if t["species"]: s += 6
    return s

def main():
    p = argparse.ArgumentParser()
    p.add_argument("city")
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--save", action="store_true", help="write data/leads/<slug>-register.json")
    a = p.parse_args()

    trees = load(a.city)
    if not trees:
        print("no visitable single trees in the register for %r" % a.city); return 1
    groups = cluster(trees)
    for g in groups:
        g.sort(key=score, reverse=True)

    print("# %s: %d visitable single register trees, %d walkable clusters" % (a.city, len(trees), len(groups)))
    print("# the register is ONE source. A second is still needed, or the tree ships flagged.")
    print("# `site history` is about the PLACE. Never write that the tree dates from it.\n")

    picked, shown = [], 0
    for i, g in enumerate(groups, 1):
        if shown >= a.top: break
        span = max((haversine(x["latitude"], x["longitude"], y["latitude"], y["longitude"])
                    for x in g for y in g), default=0)
        take = g[: max(0, a.top - shown)]
        print("## cluster %d: %d trees, %.1f km across" % (i, len(g), span))
        for t in take:
            picked.append(t); shown += 1
            print("  %-46s %s" % (t["species"] or ("?? " + str(t["species_unmapped"])), t["age_estimate"] or "no band"))
            print("    %s" % t["place"])
            print("    %.5f, %.5f   %s%s%s" % (
                t["latitude"], t["longitude"], t["setting"] or "",
                "  EREKLASSE" if t["honour_class"] == "ja" else "",
                "  name: " + t["own_name"] if t["own_name"] else ""))
            if t["site_history"]:
                print("    site history: %s" % t["site_history"][:220])
            print()
        if len(g) > len(take):
            print("  (%d more in this cluster)\n" % (len(g) - len(take)))

    unmapped = [t for t in trees if not t["species"]]
    if unmapped:
        print("# %d rows whose Dutch name is not in SPECIES yet: %s" % (
            len(unmapped), ", ".join(sorted({t["species_unmapped"] for t in unmapped})[:12])))

    if a.save:
        slug = a.city.lower().replace(" ", "-").replace("'", "")
        os.makedirs("data/leads", exist_ok=True)
        path = "data/leads/%s-register.json" % slug
        json.dump({"city": a.city, "source": "netherlands-lrmb",
                   "note": "visitable single trees, register is one source",
                   "candidates": trees}, open(path, "w"), indent=1, ensure_ascii=False)
        print("\nwrote %s (%d)" % (path, len(trees)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
