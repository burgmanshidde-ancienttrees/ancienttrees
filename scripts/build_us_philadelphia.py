"""Build the Philadelphia-area trees (verified and written 2026-11-04) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_us_philadelphia.py            # appends phl_005..009 to philadelphia (4 -> 9), writes media-pennsylvania (3)
    python3 scripts/build_us_philadelphia.py --out DIR  # dry build elsewhere (live places read from data/cities)
then city_names.py, preflight.py, commit by path, push. `--only philadelphia` builds Philadelphia alone.

Sources in data/research/: philadelphia-verified-a.json (phl_005..009: Bartram's Garden, The
Woodlands, Laurel Hill, Hobson Street, Washington Square; all free, all approximate, one source
each), philadelphia-verified-b.json (phl_020 weeping beech at Morris Arboretum, written but HELD:
with it Philadelphia would sit 4 of 10 behind a ticket; add it once more free trees land.
phl_021 wingceltis held, too hard to find), philadelphia-verified-c.json (mdp_001..003, Tyler
Arboretum in Media, paid and well over 30 minutes by transit, so its own place; under four, so
no place page in Google). Place copy in us-philadelphia-places.json. No photographs yet.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None

SOURCES = [
    ("philadelphia-verified-a.json", "philadelphia"),
    ("philadelphia-verified-b.json", "philadelphia"),
    ("philadelphia-verified-c.json", "media-pennsylvania"),
]
HELD = {"phl_020": "paid share: Philadelphia would be 4 of 10 behind a ticket"}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
REPLACE = ["intro", "meta_description", "question_meta", "question_answer", "question_context",
           "hero_tree_id", "oldest_tree_id"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "how_to_recognise",
               "verified_sources", "official_register", "access", "transport", "best_time",
               "photo", "location_precision", "pin_source", "curation_status", "verify_notes",
               "paid_entry"]
PAID_PLACES = {"media-pennsylvania"}
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}


def tree(t, place):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    if not o.get("how_to_recognise") and t.get("recognise"):
        o["how_to_recognise"] = t["recognise"]
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    p = t.get("photo") or {}
    o["photo"] = ({k: p[k] for k in ("url", "license", "attribution", "attribution_url", "status") if p.get(k)}
                  if p.get("status") == "approved" else dict(MISSING))
    o.setdefault("curation_status", "ai_generated")
    if place in PAID_PLACES or t.get("paid_entry"):
        o["paid_entry"] = True
    return o


def write(path, d):
    with open(path, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    places = json.load(open(os.path.join(R, "us-philadelphia-places.json")))
    by_place = {}
    for src, place in SOURCES:
        for t in json.load(open(os.path.join(R, src))):
            if t.get("hold") or t["id"] in HELD:
                continue
            if ONLY and place != ONLY:
                continue
            if not t.get("story"):
                sys.exit(f"{t['id']} has no story; refusing to build")
            by_place.setdefault(place, []).append(tree(t, place))
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
            d["places"].update({s: "Pennsylvania" for s in added})
            with open(sp, "w") as f:
                json.dump(d, f, ensure_ascii=False, indent=1)
                f.write("\n")
            print("us-states.json: added", ", ".join(added))

if __name__ == "__main__":
    main()
