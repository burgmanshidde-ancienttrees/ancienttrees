"""Build the written-but-unmerged backlog of 2026-11-02 to 11-04 into data/cities.

These trees were verified and written, then held for the 25-a-day pace, which
no longer counts app-only trees (APP FIRST). LOG.md 2026-11-06 lists them as
"no builder; each wants a graft". This is that builder.

    python3 scripts/build_backlog_2026_11_07.py            # writes data/cities/<slug>.json
    python3 scripts/build_backlog_2026_11_07.py --out DIR  # dry build elsewhere

Every place here is new (the script refuses to overwrite a live file). Place
fields come from data/research/backlog-places-2026-11-07.json (written by the
2026-11-07 write pass), data/research/puglia-held-2026-11-02.json, and
data/research/{la-palma,lanzarote}-city.json. Trees come from the research
files; a tree carrying `hold` is skipped. `recognise` becomes
`how_to_recognise`, the field preflight and findable.py read.

Left out on purpose, each with an earlier pass's hold: cdl_001 (Mastrinka,
access unproven), tus_013/014, nyc_085, hnl_024, sgz_003, cbr_007 (Penacova,
outside the day-trip limit).
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "data", "cities")

PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "paid_entry", "transport", "best_time", "how_to_recognise",
               "photo", "photos", "location_precision", "curation_status", "verify_notes"]

# slug -> (research file, [(research id, published id)], place-fields source)
PLAN = {
    "ayutthaya": ("ayutthaya", [("ayu_001", "ayu_001"), ("ayu_002", "ayu_002")], "backlog"),
    "chiang-mai": ("chiang-mai", [("cnx_001", "cnx_001")], "backlog"),
    "sukhothai": ("sukhothai", [("skt_001", "skt_001")], "backlog"),
    "tha-maka": ("tha-maka", [("tmk_001", "tmk_001")], "backlog"),
    "george-town": ("george-town", [("gtw_001", "gtw_001")], "backlog"),
    "horta": ("horta", [("hrt_001", "hrt_001"), ("hrt_002", "hrt_002")], "backlog"),
    "kotor": ("kotor", [("mne_002", "mne_002")], "backlog"),
    "bar": ("kotor", [("mne_001", "mtn_001")], "backlog"),
    "milo": ("milo", [("fzz_001", "fzz_001")], "backlog"),
    "zafferana-etnea": ("zafferana-etnea", [("zaf_001", "zaf_001")], "backlog"),
    "kastela": ("croatia-central-dalmatia", [("cdl_002", "cdl_002")], "backlog"),
    "lecce": ("lecce", [("lcc_001", "lcc_001")], "puglia"),
    "vernole": ("vernole", [("vrn_001", "vrn_001")], "puglia"),
    "martina-franca": ("martina-franca", [("mfr_001", "mfr_001")], "puglia"),
    "la-palma": ("la-palma", [("lpa_001", "lpa_001"), ("lpa_002", "lpa_002"),
                              ("lpa_003", "lpa_003"), ("lpa_004", "lpa_004")], "city:la-palma"),
    "lanzarote": ("lanzarote", [("lnz_001", "lnz_001")], "city:lanzarote"),
}


def load(name):
    return json.load(open(os.path.join(R, name), encoding="utf-8"))


def place_fields(slug, src):
    if src == "backlog":
        return load("backlog-places-2026-11-07.json")["places"][slug]
    if src == "puglia":
        return load("puglia-held-2026-11-02.json")["places"][slug]
    return load(src.split(":", 1)[1] + "-city.json")


# Hard rule 9: one common name per species; cadiz and cagliari say "Dragon Tree".
SPECIES = {"Canary Island Dragon Tree (Dracaena draco)": "Dragon Tree (Dracaena draco)"}
# Ticketed sites, so paid_entry matches what the access line already says.
PAID = {"ayu_001", "mtn_001", "skt_001", "cnx_001"}


def tree(t, new_id):
    t = dict(t)
    t["species"] = SPECIES.get(t.get("species"), t.get("species"))
    if new_id in PAID:
        t["paid_entry"] = True
    if not t.get("how_to_recognise") and t.get("recognise"):
        t["how_to_recognise"] = t["recognise"]
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["id"] = new_id
    o.setdefault("photo", {"url": None, "license": None, "attribution": None, "status": "missing"})
    o.setdefault("curation_status", "flagged")
    return o


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, (rfile, ids, src) in PLAN.items():
        path = os.path.join(OUT, slug + ".json")
        # --rebuild: overwrite this script's own output only (every slug in PLAN
        # was new when it first ran; never use it once a reader has added to one).
        if os.path.exists(path) and OUT.endswith(os.path.join("data", "cities")) and "--rebuild" not in sys.argv:
            sys.exit(f"{path} exists; refusing to overwrite")
        research = load(rfile + "-verified.json")
        by_id = {t.get("id"): t for t in research if isinstance(t, dict)}
        trees = []
        for rid, pid in ids:
            t = by_id.get(rid)
            if not t or not t.get("story") or t.get("hold"):
                print(f"skip {slug}/{rid}: missing, unwritten or held")
                continue
            trees.append(tree(t, pid))
        if not trees:
            print("nothing to build for", slug)
            continue
        p = place_fields(slug, src)
        d = {k: p[k] for k in PLACE_FIELDS if k in p}
        d.setdefault("status", "needs_curation")
        d["trees"] = trees
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(d, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print("wrote", path, len(trees), "tree(s)")


if __name__ == "__main__":
    main()
