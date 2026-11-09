"""Build the six empty top-60 US cities (verified and written 2026-11-04) into data/cities.

Birmingham (Alabama), Huntsville (Alabama), Lexington (Kentucky), St. Louis, Cincinnati,
and Indianapolis (which had one tree, the Kile Oak). Held for the 25-a-day pace when
written. The session that publishes runs:
    python3 scripts/build_us_empty_cities.py            # writes five new places, appends to indianapolis
    python3 scripts/build_us_empty_cities.py --out DIR  # dry build elsewhere
    python3 scripts/build_us_empty_cities.py --only cincinnati,st-louis   # a slice, for the pace
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/<slug>-verified.json per place, place fields in
data/research/us-empty-cities-places.json. A tree marked "hold" stays out.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES
ONLY = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None

SOURCES = {
    "birmingham-alabama": "birmingham-alabama-verified.json",
    "huntsville-alabama": "huntsville-alabama-verified.json",
    "lexington-kentucky": "lexington-kentucky-verified.json",
    "st-louis": "st-louis-verified.json",
    "cincinnati": "cincinnati-verified.json",
    "indianapolis": "indianapolis-verified.json",
}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise", "recognise",
               "location_precision", "curation_status", "verify_notes", "photo", "photos", "paid_entry"]
PHOTO_FIELDS = ["url", "license", "attribution", "attribution_url", "status", "width", "height", "taken_month"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}
STATES = {"birmingham-alabama": "Alabama", "huntsville-alabama": "Alabama",
          "lexington-kentucky": "Kentucky", "st-louis": "Missouri", "cincinnati": "Ohio",
          "indianapolis": "Indiana"}


def shot(p):
    return {k: p[k] for k in PHOTO_FIELDS if p.get(k) is not None}


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    p = o.get("photo") or {}
    # a photo nobody approved never ships; the tree goes out photo-less
    o["photo"] = shot(p) if p.get("status") == "approved" else dict(MISSING)
    if "photos" in o:
        o["photos"] = [shot(x) for x in o["photos"] if x.get("status") == "approved"]
        if not o["photos"]:
            del o["photos"]
    o.setdefault("curation_status", "ai_generated")
    if not re.fullmatch(r"[^()]+ \([A-Z][a-z]+ [a-z][^()]*\)", o.get("species", "")):
        sys.exit(f"{o['id']}: species {o.get('species')!r} is not 'Common (Latin)'")
    if len(o["name"]) >= 60:
        sys.exit(f"{o['id']}: name over 60 characters")
    if not o.get("story"):
        sys.exit(f"{o['id']} has no story; refusing to build")
    return o


def main():
    places = json.load(open(os.path.join(R, "us-empty-cities-places.json")))
    os.makedirs(OUT, exist_ok=True)
    for slug, src in SOURCES.items():
        if ONLY and slug not in ONLY:
            continue
        f = os.path.join(R, src)
        if not os.path.exists(f):
            continue
        ts = [tree(t) for t in json.load(open(f)) if not t.get("hold") and t.get("story")]
        if not ts:
            continue
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
        added = {k: v for k, v in STATES.items() if k not in s["places"] and (not ONLY or k in ONLY)}
        if added:
            s["places"].update(added)
            json.dump(s, open(sp, "w"), ensure_ascii=False, indent=1)
            open(sp, "a").write("\n")
            print("us-states.json: added", ", ".join(added))


if __name__ == "__main__":
    main()
