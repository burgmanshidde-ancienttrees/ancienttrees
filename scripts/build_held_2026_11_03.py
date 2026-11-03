"""Publish the trees written 2026-11-02/03 and held for the 25-a-day pace: Gran Canaria, Sintra, Tavira.

    python3 scripts/build_held_2026_11_03.py            # writes into data/cities
    python3 scripts/build_held_2026_11_03.py --out DIR  # dry build elsewhere

The Azores and Angra do Heroismo trees of the same pass go through scripts/build_azores_2.py.
Then city_names.py, preflight.py, commit each city by path, push.

PACE: on 2026-11-03 at 06:30 UTC the 24-hour count stood at 34 own trees (Bali 5 at 13:33 UTC,
the eight tourist places 17 at 14:06 UTC, Pamplona 11 at 15:29 UTC on 11-02). These twelve
(4 + 1 + 1 here, 4 + 2 from build_azores_2.py) fit under 25 only after about 14:10 UTC on 11-03,
when the count drops to 11. Run preflight first; it says.
Trial run 2026-11-03: with all twelve applied, preflight's only failure was the pace.

Sources:
  gran-canaria  data/research/grancanaria-verified.json gcn_006, gcn_008, gcn_009, gcn_010
                (gcn_007, the San Telmo figs, is HELD: approximate pin inside a park and no
                photograph, so not findable; it ships once a photo or a per-tree pin is found)
                place copy from data/research/gran-canaria-2-places.json
  sintra        data/research/sintra-verified.json sin_006, place copy from the same places file
  tavira        data/research/algarve-verified.json tav_001 with its place block (new place, one tree;
                mnq_004 in that file is left to scripts/build_algarve.py)
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES

PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "how_to_recognise",
               "verified_sources", "official_register", "access", "transport", "best_time",
               "photo", "location_precision", "pin_source", "curation_status", "paid_entry",
               "notes", "verify_notes"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}
REPLACE = ["intro", "meta_description", "question_meta", "question_answer", "question_context"]


def tree(t, age_basis=None):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    p = o.get("photo") or {}
    o["photo"] = {k: v for k, v in p.items() if v is not None} if p.get("status") == "approved" else dict(MISSING)
    o.setdefault("curation_status", "ai_generated")
    if age_basis and o.get("age_min") is not None:
        o.setdefault("age_basis", age_basis)
    if not o.get("story"):
        sys.exit("%s has no story; refusing to build" % o["id"])
    return o


def write(path, d):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")


def merge(slug, new_trees, copy):
    live = os.path.join(CITIES, slug + ".json")
    d = json.load(open(live, encoding="utf-8"))
    have = {x["id"] for x in d["trees"]}
    add = [x for x in new_trees if x["id"] not in have]
    if not add:
        print("already in", live)
        return
    d["trees"] += add
    for k in REPLACE:
        if k in copy:
            d[k] = copy[k]
    if copy.get("question_context_append") and copy["question_context_append"].strip() not in d.get("question_context", ""):
        d["question_context"] = d.get("question_context", "") + copy["question_context_append"]
    qs = {f["q"] for f in d.get("faq", [])}
    for f in copy.get("faq_add", []):
        if f["q"] not in qs:
            d.setdefault("faq", []).append(f)
    write(os.path.join(OUT, slug + ".json"), d)
    print("wrote", slug, len(d["trees"]), "tree(s), +%d" % len(add))


PT_SIN_006 = {
    "name": "O Plátano do Pátio do Convento dos Capuchos",
    "species": "Plátano (Platanus x acerifolia)",
    "age_estimate": "não documentada",
    "access": "Entrada paga. O Convento dos Capuchos é um monumento da Parques de Sintra; horários e preços em https://www.parquesdesintra.pt/en/plan-your-visit/opening-times-and-prices/.",
    "transport": "Na estrada de Sintra para Colares, na Serra de Sintra, bem fora do centro da vila; de autocarro ou de carro.",
    "story": "Num convento construído dentro de um dos bosques mais antigos de Sintra, este plátano é uma das poucas árvores que alguém plantou. O site de turismo da Câmara Municipal aponta três exemplares notáveis cultivados pelo homem no Convento dos Capuchos, o plátano frondoso que cobre o pátio do convento, um velho freixo no pátio de entrada e buxos invulgarmente grandes ao longo dos caminhos. À volta deles está a mata, e a mesma página diz que os seus velhos carvalhos são provavelmente o exemplo mais importante da antiga floresta de montanha de Sintra.\n\nO convento foi erguido em 1560 e estava abandonado em 1834. Ninguém registou quando o plátano foi plantado, e nunca se publicou o perímetro, a altura ou a idade, por isso a idade fica em aberto. Se souber, diga-nos.\n\nTambém a espécie assenta nessa única página. Há visitantes que descrevem uma árvore grande no centro do Pátio das Cruzes, o primeiro espaço onde se entra, com três cruzes que lembram o Gólgota. Não lhe dão nome, e um blogue diz que essa árvore é um sobreiro. Se o Pátio das Cruzes é o pátio do plátano ou o pátio de entrada do freixo, nenhuma fonte o diz. Quem lá estiver pode resolver a questão com uma fotografia.\n\nO convento é um monumento da Parques de Sintra com entrada paga, por isso confirme horários e preços antes de ir. Fica na estrada de Sintra para Colares, na Serra de Sintra, bem fora da vila, e chega-se de autocarro ou de carro.",
}


def pt_sintra():
    """The pt overlay must carry every Sintra tree or the build refuses; counts go from five to six."""
    p = os.path.join(ROOT, "data", "i18n", "pt", "sintra.json")
    d = json.load(open(p, encoding="utf-8"))
    if "sin_006" in d["trees"]:
        return
    d["trees"]["sin_006"] = PT_SIN_006
    d["meta_description"] = d["meta_description"].replace("As cinco árvores mais notáveis de Sintra", "Seis árvores notáveis de Sintra")
    d["question_meta"] = d["question_meta"].replace("mais quatro árvores", "mais cinco árvores")
    d["title"] = d["title"].replace("as 5 mais notáveis", "as 6 mais notáveis")
    d["question_context"] += (" Uma sexta árvore, o plátano que cobre o pátio do Convento dos Capuchos, na Serra de Sintra,"
                              " não está classificada, e a entrada no convento é paga.")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("pt/sintra overlay: sin_006 added")


def main():
    os.makedirs(OUT, exist_ok=True)
    places = json.load(open(os.path.join(R, "gran-canaria-2-places.json"), encoding="utf-8"))

    gc = json.load(open(os.path.join(R, "grancanaria-verified.json"), encoding="utf-8"))
    want = ["gcn_006", "gcn_008", "gcn_009", "gcn_010"]
    merge("gran-canaria", [tree(t, "source") for t in gc if t.get("id") in want], places["gran-canaria"])

    si = json.load(open(os.path.join(R, "sintra-verified.json"), encoding="utf-8"))
    merge("sintra", [tree(t) for t in si if t.get("id") == "sin_006"], places["sintra"])
    if OUT == CITIES:
        pt_sintra()

    alg = json.load(open(os.path.join(R, "algarve-verified.json"), encoding="utf-8"))
    tav = [tree(t) for t in alg["trees"] if t.get("id") == "tav_001"]
    path = os.path.join(CITIES, "tavira.json")
    if os.path.exists(path):
        print("tavira exists; not rebuilt")
    else:
        p = alg["places"]["tavira"]
        d = {k: p[k] for k in PLACE_FIELDS if k in p}
        d["trees"] = tav
        write(os.path.join(OUT, "tavira.json"), d)
        print("wrote tavira 1 tree(s)")


if __name__ == "__main__":
    main()
