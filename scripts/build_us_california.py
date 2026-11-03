"""Build the California trees (verified and written 2026-11-02/03) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_us_california.py            # appends to los-angeles and san-diego, writes oakland, glen-ellen, sebastopol
    python3 scripts/build_us_california.py --out DIR  # dry build elsewhere (live places read from data/cities)
then city_names.py, preflight.py, commit by path, push.

Sources in data/research/: los-angeles-verified.json (lax_014..016; lax_013 there is old and
already live), los-angeles-east-verified.json (lax_030..032), san-diego-verified.json
(sdg_007..011, the Coronado heritage cluster), oakland-verified.json (oak_001..004),
santa-rosa-verified.json (snm_001..002 for glen-ellen, srs_001 for sebastopol; Santa Rosa
itself yielded none). Place copy in us-california-places.json; approved photographs in
us-california-photos.json (a held photo never ships). Los Angeles and San Diego grow, so
their intro, meta and question fields are replaced and new FAQ items appended. Oakland is
new with four trees; Glen Ellen (2) and Sebastopol (1) stay out of Google until four.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES

SOURCES = [
    ("los-angeles-verified.json", "los-angeles"),
    ("los-angeles-east-verified.json", "los-angeles"),
    ("san-diego-verified.json", "san-diego"),
    ("oakland-verified.json", "oakland"),
    ("santa-rosa-verified.json", None),  # each tree names its place
]
PLACE_OF = {"sonoma": "glen-ellen"}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
REPLACE = ["intro", "meta_description", "question_meta", "question_answer", "question_context",
           "hero_tree_id", "oldest_tree_id"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "how_to_recognise",
               "verified_sources", "official_register", "access", "transport", "best_time",
               "photo", "location_precision", "pin_source", "curation_status", "verify_notes",
               "paid_entry"]
PAID = {"lax_032", "snm_001", "snm_002"}  # mission garden ticket; state park vehicle fee
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}


def tree(t, photos):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    if not o.get("how_to_recognise") and t.get("recognise"):
        o["how_to_recognise"] = t["recognise"]
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    p = photos.get(o["id"]) or {}
    if p.get("status") == "approved":
        o["photo"] = {k: p[k] for k in ("url", "license", "attribution", "attribution_url") if p.get(k)}
        o["photo"]["status"] = "approved"
    else:
        o["photo"] = dict(MISSING)
    o.setdefault("curation_status", "ai_generated")
    if o["id"] in PAID:
        o["paid_entry"] = True
    return o


def write(path, d):
    with open(path, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    places = json.load(open(os.path.join(R, "us-california-places.json")))
    pp = os.path.join(R, "us-california-photos.json")
    photos = json.load(open(pp)) if os.path.exists(pp) else {}
    by_place = {}
    for src, slug in SOURCES:
        for t in json.load(open(os.path.join(R, src))):
            if t.get("id") == "lax_013" or t.get("hold"):
                continue
            place = slug or PLACE_OF.get(t.get("place"), t.get("place"))
            if not t.get("story"):
                sys.exit(f"{t['id']} has no story; refusing to build")
            by_place.setdefault(place, []).append(tree(t, photos))
    os.makedirs(OUT, exist_ok=True)
    for slug, ts in by_place.items():
        p = places[slug]
        live = os.path.join(CITIES, slug + ".json")
        if os.path.exists(live):
            d = json.load(open(live))
            have = {x["id"] for x in d["trees"]}
            new = [x for x in ts if x["id"] not in have]
            if not new:
                print("already in", live)
                continue
            d["trees"] += new
            for k in REPLACE:
                if p.get(k):
                    d[k] = p[k]
            for f in d.get("faq", []):
                if f["q"] in p.get("faq_replace", {}):
                    f["a"] = p["faq_replace"][f["q"]]
            asked = {f["q"] for f in d.get("faq", [])}
            d.setdefault("faq", []).extend(f for f in p.get("faq_add", []) if f["q"] not in asked)
        else:
            d = {k: p[k] for k in PLACE_FIELDS if k in p}
            d.setdefault("country", "United States")
            d.setdefault("status", "needs_curation")
            d["trees"] = ts
        ids = {x["id"] for x in d["trees"]}
        for k in ("hero_tree_id", "oldest_tree_id"):
            if d.get(k) and d[k] not in ids:
                sys.exit(f"{slug}: {k} {d[k]} is not one of its trees")
        write(os.path.join(OUT, slug + ".json"), d)
        print("wrote", slug, len(d["trees"]), "tree(s),", len(ts), "from this pass")
    if OUT == CITIES:  # Contract L: every US place names its state
        sp = os.path.join(ROOT, "data", "us-states.json")
        d = json.load(open(sp))
        added = [s for s in by_place if s not in d["places"]]
        if added:
            d["places"].update({s: "California" for s in added})
            with open(sp, "w") as f:
                json.dump(d, f, ensure_ascii=False, indent=1)
                f.write("\n")
            print("us-states.json: added", ", ".join(added))


if __name__ == "__main__":
    main()
