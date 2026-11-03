"""Build the US East trees (verified and written 2026-11-02/03) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_us_east.py            # appends to washington-dc and new-york, writes leesburg
    python3 scripts/build_us_east.py --out DIR  # dry build elsewhere (live places read from data/cities)
then city_names.py, preflight.py, commit by path, push.

Sources in data/research/: us-east-written-*.json (every written tree, each with `place`:
washington-dc, new-york or leesburg; verified in washington-dc-2-verified.json,
dc-suburbs-verified.json, new-york-2-verified.json, new-york-3-verified.json and
leesburg-verified.json) and us-east-places-*.json (place copy: Washington DC and New York
grow, so their intro, meta and question fields are replaced and FAQ items replaced or
appended; Leesburg is new). Approved photographs in us-east-photos.json if it exists (a held
photo never ships). A tree with `hold` set is skipped.
"""
import glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES

STATE = {"washington-dc": "District of Columbia", "new-york": "New York", "leesburg": "Virginia"}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
REPLACE = ["intro", "meta_description", "question_meta", "question_answer", "question_context",
           "hero_tree_id", "oldest_tree_id"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "how_to_recognise",
               "verified_sources", "official_register", "access", "transport", "best_time",
               "photo", "location_precision", "pin_source", "curation_status", "verify_notes",
               "paid_entry"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}
# canonical names where a written file kept a less common one
SPECIES = {"Japanese Zelkova (Zelkova serrata)": "Saw-leaf Zelkova (Zelkova serrata)"}


def tree(t, photos):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["species"] = SPECIES.get(o["species"], o["species"])
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
    return o


def write(path, d):
    with open(path, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    places = {}
    for f in sorted(glob.glob(os.path.join(R, "us-east-places-*.json"))):
        places.update(json.load(open(f)))
    pp = os.path.join(R, "us-east-photos.json")
    photos = json.load(open(pp)) if os.path.exists(pp) else {}
    by_place = {}
    written = [t for f in sorted(glob.glob(os.path.join(R, "us-east-written-*.json"))) for t in json.load(open(f))]
    for t in written:
        if t.get("hold"):
            continue
        if not t.get("story"):
            sys.exit(f"{t['id']} has no story; refusing to build")
        by_place.setdefault(t["place"], []).append(tree(t, photos))
    os.makedirs(OUT, exist_ok=True)
    for slug, ts in by_place.items():
        p = places.get(slug, {})
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
        if len(ids) != len(d["trees"]):
            sys.exit(f"{slug}: duplicate tree ids")
        for k in ("hero_tree_id", "oldest_tree_id", "face_tree_id"):
            if d.get(k) and d[k] not in ids:
                sys.exit(f"{slug}: {k} {d[k]} is not one of its trees")
        write(os.path.join(OUT, slug + ".json"), d)
        print("wrote", slug, len(d["trees"]), "tree(s),", len(ts), "from this pass")
    if OUT == CITIES:  # Contract L: every US place names its state
        sp = os.path.join(ROOT, "data", "us-states.json")
        d = json.load(open(sp))
        added = [s for s in by_place if s not in d["places"]]
        if added:
            d["places"].update({s: STATE[s] for s in added})
            with open(sp, "w") as f:
                json.dump(d, f, ensure_ascii=False, indent=1)
                f.write("\n")
            print("us-states.json: added", ", ".join(added))


if __name__ == "__main__":
    main()
