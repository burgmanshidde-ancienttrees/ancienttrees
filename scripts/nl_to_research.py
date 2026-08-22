#!/usr/bin/env python3
"""Turn register candidates into a research file the verify pass can finish.

The register already answers species, planting band, location, access and
owner. What it cannot answer is whether the tree is still standing (LRMB is
the 2024 edition) and whether a second source exists. So this writes the
skeleton with every register fact in `verify_notes`, and leaves exactly those
two questions for an agent, which is what makes a register-backed verify pass
cost almost nothing.

It picks a WALK rather than a list: the densest cluster within the given
radius, best-scored trees first, because a page of six trees scattered over
nine kilometres is not an afternoon out.
"""
import json, sys, argparse, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nl_candidates as N

def prefix(city):
    w = re.sub(r"[^a-z]", "", city.lower())
    return w[:3]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("city")
    p.add_argument("--n", type=int, default=7)
    p.add_argument("--km", type=float, default=3.0)
    a = p.parse_args()

    trees = N.load(a.city)
    groups = N.cluster(trees, km=a.km)
    for g in groups:
        g.sort(key=N.score, reverse=True)
    # the walk: the cluster holding the most trees, tightened by score
    g = max(groups, key=lambda x: (len(x), sum(N.score(t) for t in x)))
    picked = g[: a.n]

    slug = a.city.lower().replace(" ", "-").replace("'", "")
    px = prefix(a.city)
    out = []
    for i, t in enumerate(picked, 1):
        notes = []
        notes.append("LRMB register nr %s, entry name %r." % (t["nr"], t["register_name"]))
        notes.append("Register planting band %s, so age is a BAND and must not be sharpened."
                     % t["planted_band"])
        notes.append("Register calls it visitable (visitable=ja), owner category %s, setting %s."
                     % (t["owner_category"], t["setting"]))
        if t["honour_class"] == "ja":
            notes.append("EREKLASSE: the register's own top designation, 99 trees nationally.")
        if t["own_name"]:
            notes.append("The register records a name for this tree: %r." % t["own_name"])
        if t["form"]:
            notes.append("Form: %s." % t["form"])
        if t["site_history"]:
            notes.append("Register history of the PLACE (not of the tree, do not bridge): %s"
                         % t["site_history"].replace("\n", " ").strip())
        notes.append("TO VERIFY: (1) is it still standing in 2026, the register is the 2024 "
                     "edition; (2) a second independent source, and if none exists say so, the "
                     "tree still ships flagged; (3) that the pin lands on the tree rather than "
                     "the address centroid.")
        out.append({
            "id": "%s_%03d" % (px, i),
            "name": None,
            "species": t["species"] or "TO ESTABLISH: register name %r" % t["register_name"],
            "age_estimate": t["age_estimate"],
            "age_min": t["age_min"], "age_max": t["age_max"],
            "location": {"address": t["place"], "latitude": t["latitude"],
                         "longitude": t["longitude"], "neighbourhood": None},
            "verified_sources": ["https://www.monumentalebomen.nl/"],
            "access": None, "transport": None,
            "photo": {"url": None, "license": None, "attribution": None, "status": "missing"},
            "curation_status": "flagged",
            "location_precision": "approximate",
            "verify_notes": " ".join(notes),
        })
    os.makedirs("data/research", exist_ok=True)
    path = "data/research/%s-verified.json" % slug
    json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
    span = max((N.haversine(x["latitude"], x["longitude"], y["latitude"], y["longitude"])
                for x in picked for y in picked), default=0)
    print("%s: %d trees, %.1f km across -> %s" % (a.city, len(out), span, path))

if __name__ == "__main__":
    main()
