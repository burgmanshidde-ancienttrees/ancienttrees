"""Build the US Gulf Coast live oak pass (verified and written 2026-11-02/03) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_us_live_oaks.py            # appends to mobile.json and charleston.json, writes baton-rouge.json and lafayette-louisiana.json
    python3 scripts/build_us_live_oaks.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/mobile-verified.json (mob_002..mob_004, joins the live Mobile page,
which then reaches four trees), data/research/charleston-verified.json (chs_004, joins the
live Charleston page; its place fields stay as they are), data/research/batonrouge-verified.json
(two trees) and data/research/lafayettelouisiana-verified.json (three trees, the Evangeline Oak
a day trip to St. Martinville), with place fields in data/research/us-live-oaks-places.json.
Baton Rouge and Lafayette stay under four, so their place pages stay out of Google and the
trees go live as tree pages. New Orleans and Savannah passes found nothing new (leads only).
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES

SOURCES = {
    "mobile": "mobile-verified.json",
    "charleston": "charleston-verified.json",
    "baton-rouge": "batonrouge-verified.json",
    "lafayette-louisiana": "lafayettelouisiana-verified.json",
}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "curation_status", "verify_notes", "photo", "photos", "paid_entry"]
PHOTO_FIELDS = ["url", "license", "attribution", "attribution_url", "status", "width", "height", "taken_month"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}
SPECIES = "Southern Live Oak (Quercus virginiana)"
STATES = {"baton-rouge": "Louisiana", "lafayette-louisiana": "Louisiana"}


def shot(p):
    return {k: p[k] for k in PHOTO_FIELDS if p.get(k) is not None}


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    p = o.get("photo") or {}
    # a held photo never ships; the tree goes out photo-less
    o["photo"] = shot(p) if p.get("status") == "approved" else dict(MISSING)
    if "photos" in o:
        o["photos"] = [shot(x) for x in o["photos"] if x.get("status") == "approved"] or None
        if not o["photos"]:
            del o["photos"]
    o.setdefault("curation_status", "ai_generated")
    if o.get("species") != SPECIES:
        sys.exit(f"{o['id']}: species {o.get('species')!r}, expected {SPECIES!r}")
    if len(o["name"]) >= 60:
        sys.exit(f"{o['id']}: name over 60 characters")
    return o


def main():
    places = json.load(open(os.path.join(R, "us-live-oaks-places.json")))
    os.makedirs(OUT, exist_ok=True)
    for slug, src in SOURCES.items():
        ts = [tree(t) for t in json.load(open(os.path.join(R, src))) if not t.get("hold")]
        for t in ts:
            if not t.get("story"):
                sys.exit(f"{t['id']} has no story; refusing to build")
        live = os.path.join(CITIES, slug + ".json")
        path = os.path.join(OUT, slug + ".json")
        p = places.get(slug, {})
        if os.path.exists(live):
            d = json.load(open(live))
            have = {x["id"] for x in d["trees"]}
            trees = d["trees"] + [x for x in ts if x["id"] not in have]
            d.update({k: p[k] for k in PLACE_FIELDS if k in p})
        else:
            if not p:
                sys.exit(f"{slug}: new place without place fields")
            d = {k: p[k] for k in PLACE_FIELDS if k in p}
            trees = ts
        d.setdefault("country", "United States")
        d.setdefault("status", "needs_curation")
        ids = {x["id"] for x in trees}
        for k in ("hero_tree_id", "oldest_tree_id"):
            if k in d and d[k] not in ids:
                sys.exit(f"{slug}: {k} {d.get(k)} is not one of its trees")
        rest = {k: v for k, v in d.items() if k not in PLACE_FIELDS + ["trees"]}
        d = {**{k: d[k] for k in PLACE_FIELDS if k in d}, **rest, "trees": trees}
        json.dump(d, open(path, "w"), ensure_ascii=False, indent=2)
        open(path, "a").write("\n")
        print("wrote", path, len(trees), "tree(s),", len(ts), "from this pass")
    if OUT == CITIES:
        # Contract L: every US place names its state, or the state page build fails
        sp = os.path.join(ROOT, "data", "us-states.json")
        s = json.load(open(sp))
        added = {k: v for k, v in STATES.items() if k not in s["places"]}
        if added:
            s["places"].update(added)
            json.dump(s, open(sp, "w"), ensure_ascii=False, indent=1)
            open(sp, "a").write("\n")
            print("us-states.json: added", ", ".join(added))


if __name__ == "__main__":
    main()
