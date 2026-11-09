"""Build the source-led passes of 2026-11-09 into data/cities (app only under APP FIRST).

Michigan (Detroit, Ann Arbor, Lansing), Cleveland, three California places (Sacramento, Santa
Cruz, Long Beach) and ten churchyard yews in Surrey, Sussex and Hampshire, each its own place.
Reno, Boise and Des Moines found nothing that ships; Kansas City's smoketree has no recognition
line and stays out (data/research/kansas-city-verified.json). Detroit's two Elmwood trees are held
until a pin exists, and Long Beach's figs are the live lax_016, so neither place is built yet.

    python3 scripts/build_source_led_2026_11_09.py            # writes the new places
    python3 scripts/build_source_led_2026_11_09.py --out DIR  # dry build elsewhere
    python3 scripts/build_source_led_2026_11_09.py --only detroit,ann-arbor
then city_names.py, preflight.py, commit by path, push. A tree marked "hold" stays out.

Sources: data/research/<slug>-verified.json, southeast-england-yews-verified.json (one row per
place, `place.slug`), place fields in us-source-led-places.json and uk-yews-2026-11-09-places.json.
Woodland Trust Ancient Tree Inventory not used.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES
ONLY = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None

STATES = {"detroit": "Michigan", "ann-arbor": "Michigan", "lansing": "Michigan", "cleveland": "Ohio",
          "sacramento": "California", "santa-cruz": "California", "long-beach": "California"}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "pin_source", "curation_status", "verify_notes", "paid_entry"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    o["photo"] = dict(MISSING)
    o.setdefault("curation_status", "ai_generated")
    if not re.fullmatch(r"[^()]+ \([A-Z][a-z]+ [a-z'\"A-Z][^()]*\)", o.get("species", "")):
        sys.exit(f"{o['id']}: species {o.get('species')!r} is not 'Common (Latin)'")
    if len(o["name"]) >= 60:
        sys.exit(f"{o['id']}: name over 60 characters")
    if not o.get("story"):
        sys.exit(f"{o['id']} has no story; refusing to build")
    if not (o.get("location_precision") == "confirmed" or o.get("how_to_recognise")):
        sys.exit(f"{o['id']}: no photo, confirmed pin or recognition line")
    if "—" in json.dumps(o, ensure_ascii=False):
        sys.exit(f"{o['id']}: em dash")
    return o


def groups():
    for slug in STATES:
        yield slug, [t for t in json.load(open(os.path.join(R, slug + "-verified.json"))) if not t.get("hold")]
    for t in json.load(open(os.path.join(R, "southeast-england-yews-verified.json"))):
        if not t.get("hold"):
            yield t["place"]["slug"], [t]


def main():
    places = {}
    for f in ("us-source-led-places.json", "uk-yews-2026-11-09-places.json"):
        places.update(json.load(open(os.path.join(R, f))))
    os.makedirs(OUT, exist_ok=True)
    built = set()
    for slug, rows in groups():
        if ONLY and slug not in ONLY:
            continue
        if not rows:
            continue
        if os.path.exists(os.path.join(CITIES, slug + ".json")):
            sys.exit(f"{slug}: already a live place; this builder only writes new ones")
        p = places.get(slug)
        if not p:
            sys.exit(f"{slug}: new place without place fields")
        ts = [tree(t) for t in rows]
        ids = {x["id"] for x in ts}
        for k in ("hero_tree_id", "oldest_tree_id"):
            if p.get(k) not in ids:
                sys.exit(f"{slug}: {k} {p.get(k)} is not one of its trees")
        d = {**{k: p[k] for k in PLACE_FIELDS if k in p}, "trees": ts}
        path = os.path.join(OUT, slug + ".json")
        with open(path, "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        built.add(slug)
        print("wrote", path, len(ts), "tree(s)")
    if OUT == CITIES:
        # Contract L: every US place names its state, or the state page build fails
        sp = os.path.join(ROOT, "data", "us-states.json")
        s = json.load(open(sp))
        added = {k: v for k, v in STATES.items() if k not in s["places"] and k in built}
        if added:
            s["places"].update(added)
            with open(sp, "w") as f:
                json.dump(s, f, ensure_ascii=False, indent=1)
                f.write("\n")
            print("us-states.json: added", ", ".join(added))


if __name__ == "__main__":
    main()
