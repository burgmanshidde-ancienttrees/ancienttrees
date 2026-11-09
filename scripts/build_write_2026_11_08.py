"""Publish the written trees of the 2026-11-08 write pass into data/cities.

    python3 scripts/build_write_2026_11_08.py [--check]

gui_009 (Guimaraes, written today), hnl_024 (Oahu) and cbr_007 (Penacova, a
new one-tree place) come from their research files. --check prints word
counts and bans only.

Two earlier holds lifted, each on hard rule 10 as it now reads ("paid entry
and bookable tours count as yes"):
- hnl_024 was held because no source settles whether the banyan stands inside
  or outside the ticketed Waikiki Aquarium. Either way anyone can reach it, so
  the access line now says exactly that instead of claiming it is free; the
  story already did.
- cbr_007 was held because Penacova is outside Coimbra's 30-minute day-trip
  bound. It ships as its own place, as its verify notes asked, never as part
  of the Coimbra walk.

Still held, not built here: cdl_001 (kindergarten courtyard, access unproven),
sgz_003 (access text reads as a booking needing permission; wants a sourced
line that the tours are open to anyone).
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "how_to_recognise",
               "verified_sources", "official_register", "access", "paid_entry", "transport", "best_time",
               "photo", "location_precision", "pin_source", "curation_status", "verify_notes"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}
BANNED = ["hidden gem", "must-see", "breathtaking", "nestled", "majestic", "stunning", "iconic",
          "a testament to", "—", "–", "!"]

# slug -> (research file, research id)
PLAN = [("guimaraes", "guimaraes", "gui_009"), ("oahu", "oahu", "hnl_024"), ("penacova", "coimbra", "cbr_007")]

# Preflight: two cities never share an id prefix, and cbr is Coimbra's.
NEW_ID = {"cbr_007": "pcv_001"}

OVERRIDE = {
    "hnl_024": {
        "access": "On the Ewa side of the Waikiki Aquarium, which charges admission. No source settles whether "
                  "the banyan stands inside the aquarium's fence or just outside it, so expect either.",
    },
    "gui_009": {"paid_entry": True},
}

NEW_PLACES = {
    "penacova": {
        "city": "Penacova",
        "country": "Portugal",
        "status": "needs_curation",
        "intro": "The protected tree on Penacova's main square is a roof. On the Terreiro, between the town hall and the courts, "
                 "old wisteria vines carry the Raul Lino pergola, a terrace over the Mondego that Portugal's "
                 "forest service classified as of public interest in 1997. The register put the vines at 97 years "
                 "old in 2015. Spring is the time to come, when they flower.",
        "meta_description": "The Raul Lino wisteria pergola on the Terreiro de Penacova, above the Mondego: "
                            "a protected Chinese wisteria about a century old, in flower in spring.",
        "question_meta": "Penacova's Raul Lino pergola is roofed by a protected Chinese wisteria, "
                         "97 years old by the 2015 register count.",
        "question_answer": "The old tree on Penacova's main square is a Chinese Wisteria (Wisteria sinensis) "
                           "that roofs the Raul Lino pergola on the Terreiro, beside the town hall. Portugal's "
                           "forest service gave its age as 97 when it measured it in 2015.",
        "question_context": "The age is the register's, not a planting record: the ICNF measured the vines in "
                            "2015 and recorded 97 years, which would make them about 108 now. The pergola is said "
                            "to date from 1918, which fits, but no source we read says the vines went in with it. "
                            "A wisteria is a climber, so the register's girth of 2.3 metres is a knot of old stems "
                            "and its height of 3.25 metres is the height of the pergola it covers. The crown is "
                            "3.8 metres across. An older compilation from 2009 gave a girth of 1.95 metres and an "
                            "age of 89, an earlier reading of the same vines rather than a second opinion. The "
                            "state classified the wisteria as of public interest in 1997. The same register lists "
                            "a second wisteria on the terrace, with a girth of 10 centimetres and an age of 11, "
                            "which reads as a young replacement vine or a slip in the data, so it is folded into "
                            "this entry. The vines were recorded alive in June 2026. The pergola stands between "
                            "the town hall and the courts, looking out over the Mondego.",
        "hero_tree_id": "pcv_001",
        "oldest_tree_id": "pcv_001",
        "faq": [
            {"q": "When does the Penacova wisteria flower?",
             "a": "In spring. The parish council describes the old vines over the pergola giving off an "
                  "unmistakable scent then."},
            {"q": "How far is Penacova from Coimbra?",
             "a": "About 14 kilometres, some 23 minutes by car. Buses are slow and infrequent, so check them first."},
        ],
        "trees": [],
    }
}


def check(t):
    errs = []
    n = len(t["story"].split())
    if not 150 <= n <= 250:
        errs.append(f"story {n} words")
    blob = json.dumps(t, ensure_ascii=False)
    for b in BANNED:
        if b.lower() in blob.lower():
            errs.append("banned " + repr(b))
    if len(t.get("how_to_recognise", "")) >= 240:
        errs.append("recognise too long")
    if t.get("hold"):
        errs.append("held: " + t["hold"][:60])
    return n, errs


def main():
    todo = []
    bad = False
    for slug, rfile, rid in PLAN:
        src = json.load(open(os.path.join(R, rfile + "-verified.json"), encoding="utf-8"))
        t = dict(next(x for x in src if isinstance(x, dict) and x.get("id") == rid))
        t.pop("hold", None)
        t.update(OVERRIDE.get(rid, {}))
        n, errs = check(t)
        print(slug, rid, n, "words", errs or "ok")
        bad = bad or bool(errs)
        todo.append((slug, t))
    if bad or "--check" in sys.argv:
        sys.exit(1 if bad else 0)
    for slug, t in todo:
        path = os.path.join(ROOT, "data", "cities", slug + ".json")
        # A new place is this script's own output, so it is rebuilt whole each run.
        if os.path.exists(path) and slug not in NEW_PLACES:
            d = json.load(open(path, encoding="utf-8"))
        else:
            d = json.loads(json.dumps(NEW_PLACES[slug]))
        if t["id"] in {x["id"] for x in d["trees"]}:
            print(t["id"], "already live, skipped")
            continue
        o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
        o["id"] = NEW_ID.get(t["id"], t["id"])
        o.setdefault("photo", dict(MISSING))
        o.setdefault("curation_status", "flagged")
        d["trees"].append(o)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(slug, "added", t["id"], "now", len(d["trees"]))


if __name__ == "__main__":
    main()
