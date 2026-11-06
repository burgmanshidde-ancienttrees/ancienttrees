"""Build the Northern Ireland and Scottish Highlands pass (verified and written 2026-11-04) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_uk_ni_highlands.py                  # appends to belfast.json, writes the new places
    python3 scripts/build_uk_ni_highlands.py --out DIR        # dry build elsewhere
    python3 scripts/build_uk_ni_highlands.py --only belfast,castlewellan   # pace-sized parts
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/{belfast,ni-estates,inverness,highlands-west}-verified.json (trees with
stories), place fields in data/research/uk-ni-highlands-places.json, photo verdicts in
data/research/uk-ni-highlands-photos.json (looked at 2026-11-04; only `approved` ever ships).
Belfast grows from five to eight and its intro and meta are replaced by the rewritten ones.
Castlewellan has four trees and gets a place page; every other place is one or two trees, so its
place page stays out of Google and the trees go live as tree pages. Aviemore and Speyside found
nothing that ships (data/leads/aviemore.json); Beauly's priory elm fell in 2023. Woodland Trust
Ancient Tree Inventory not used.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES
ONLY = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None

FILES = ["belfast-verified.json", "ni-estates-verified.json", "inverness-verified.json",
         "highlands-west-verified.json"]
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "pin_source", "curation_status", "verify_notes", "photo", "paid_entry"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}
# one canonical common name per species, as the live cities spell it (hard rule 9)
SPECIES = {
    "Common Yew (Taxus baccata)": "European Yew (Taxus baccata)",
    "English Yew (Taxus baccata)": "European Yew (Taxus baccata)",
    "Common Beech (Fagus sylvatica)": "European Beech (Fagus sylvatica)",
    "European Silver Fir (Abies alba)": "Silver Fir (Abies alba)",
}


def tree(t, photos):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["species"] = SPECIES.get(o["species"], o["species"])
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    p = photos.get(o["id"])
    if p:
        o["photo"] = {k: p[k] for k in ("url", "license", "attribution", "attribution_url") if p.get(k)}
        o["photo"]["status"] = "approved"
    else:
        o["photo"] = dict(MISSING)
    o.setdefault("curation_status", "ai_generated")
    if not o.get("paid_entry"):
        o.pop("paid_entry", None)
    if len(o["name"]) >= 60:
        sys.exit(f"{o['id']}: name over 60 characters")
    if not o.get("story"):
        sys.exit(f"{o['id']} has no story; refusing to build")
    if "—" in json.dumps(o, ensure_ascii=False):
        sys.exit(f"{o['id']}: em dash")
    return o


def main():
    places = json.load(open(os.path.join(R, "uk-ni-highlands-places.json")))
    pf = os.path.join(R, "uk-ni-highlands-photos.json")
    photos = json.load(open(pf)).get("approved", {}) if os.path.exists(pf) else {}
    by_place = {}
    for src in FILES:
        for t in json.load(open(os.path.join(R, src))):
            if not isinstance(t, dict):
                continue
            if t.get("hold"):
                print("HELD", t["id"], t["hold"])
                continue
            by_place.setdefault(t["place"], []).append(tree(t, photos))
    os.makedirs(OUT, exist_ok=True)
    for slug, ts in by_place.items():
        if ONLY and slug not in ONLY:
            continue
        live = os.path.join(CITIES, slug + ".json")
        path = os.path.join(OUT, slug + ".json")
        p = places.get(slug, {})
        if os.path.exists(live):
            d = json.load(open(live))
            mine = {x["id"] for x in ts}
            trees = [x for x in d["trees"] if x["id"] not in mine] + ts
            for k in PLACE_FIELDS:
                if p.get(k):
                    d[k] = p[k]
        else:
            if not p.get("intro"):
                sys.exit(f"{slug}: new place without place fields")
            d = {k: p[k] for k in PLACE_FIELDS if k in p}
            trees = ts
        d.setdefault("country", "United Kingdom")
        d.setdefault("status", "needs_curation")
        tids = {x["id"] for x in trees}
        for k in ("hero_tree_id", "oldest_tree_id"):
            if k in d and d[k] not in tids:
                sys.exit(f"{slug}: {k} {d.get(k)} is not one of its trees")
        if "—" in json.dumps({k: d.get(k) for k in PLACE_FIELDS}, ensure_ascii=False):
            sys.exit(f"{slug}: em dash in place copy")
        rest = {k: v for k, v in d.items() if k not in PLACE_FIELDS + ["trees"]}
        d = {**{k: d[k] for k in PLACE_FIELDS if k in d}, **rest, "trees": trees}
        with open(path, "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("wrote", path, len(trees), "tree(s),", len(ts), "from this pass")


if __name__ == "__main__":
    main()
