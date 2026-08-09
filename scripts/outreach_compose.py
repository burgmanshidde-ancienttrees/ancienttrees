#!/usr/bin/env python3
"""Compose an outreach batch from data/outreach-contacts.json.

The frame is Hidde's, set in session on 2026-08-09 and it is the whole point:
we are not pitching coverage. We write to the people who look after the trees
and ask them for three things, in this order:

  1. photographs we are missing,
  2. anything we got wrong,
  3. a tree we overlooked.

The third question is the strongest and it is deliberate. Asking for a photo
makes someone a supplier; asking "did we miss one" makes them the expert, and
an expert who corrects your list has joined it. The psychology is old and
plain: people who do you a small favour become invested, and people who are in
something talk about it. What must NEVER appear in this mail is a request for
coverage or a link. The moment a reader suspects the photo question was a
pretext for a publicity question, both die, and the whole approach with them.
A link, if it comes at all, belongs in the reply after we have used their help
and credited them by name.

Specificity is not decoration here, it is the only reason this outperforms
spam. Each mail names the recipient's OWN trees from our data, says which ones
have no photograph, and links to the page those trees sit on. That paragraph is
generated per recipient rather than templated, because a mail that could have
been sent to anyone will read as though it was.

Usage:
  python3 scripts/outreach_compose.py --country Portugal --limit 12 --out drafts/batches/batch-002-pt.json
"""
import argparse
import glob
import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def city_trees():
    """Every published tree, by city slug, with whether it has a photo."""
    out = {}
    for p in glob.glob(os.path.join(ROOT, "data/cities/*.json")):
        d = json.load(open(p))
        slug = os.path.basename(p)[:-5]
        out[slug] = {
            "city": d.get("city", slug),
            "trees": [{"name": t.get("name", ""),
                       "species": t.get("species", ""),
                       "address": (t.get("location") or {}).get("address", ""),
                       "photo": (t.get("photo") or {}).get("status") == "approved"}
                      for t in d.get("trees", [])],
        }
    return out


def theirs(contact, cities):
    """The trees that plausibly belong to this contact's own site.

    Matched on the organisation name appearing in a tree's address or name,
    which is crude and deliberately conservative: a wrong claim ("your garden
    holds these trees") in the first sentence would end the conversation, so a
    contact with no confident match falls back to the city as a whole and the
    mail says 'in your city' instead of 'in your garden'.
    """
    slug = None
    for s, d in cities.items():
        if norm(d["city"]) == norm(contact.get("city", "")):
            slug = s
            break
    if not slug:
        return None, []
    org_words = [w for w in re.split(r"[^\w]+", norm(contact.get("org", ""))) if len(w) > 4]
    hits = []
    for t in cities[slug]["trees"]:
        hay = norm(t["name"] + " " + t["address"])
        if any(w in hay for w in org_words):
            hits.append(t)
    return slug, hits


TEXT = {
    "pt": {
        "subject_site": "As vossas árvores no {org}, e três perguntas",
        "subject_city": "As árvores mais notáveis de {city}, e três perguntas",
        "greet": "Bom dia,",
        "intro": ("Chamo-me Hidde. Reúno em ancienttrees.app as árvores antigas mais notáveis "
                  "das cidades, cada uma com a sua história, a sua localização exacta e um "
                  "percurso a pé que as liga. Tudo é verificado em pelo menos duas fontes "
                  "independentes e é gratuito para consultar."),
        "ours_site": "De {city} publicamos {n} árvores, e {k} delas estão no vosso espaço:",
        "ours_city": "De {city} publicamos {n} árvores, entre elas:",
        "nophoto": ("Destas, {m} não têm fotografia nenhuma. É a nossa maior lacuna e não é "
                    "resolúvel a partir de uma secretária."),
        "ask": ("Três perguntas, e qualquer uma delas já nos ajuda:\n\n"
                "1. Teriam uma fotografia destas árvores que pudéssemos usar, com o crédito "
                "que indicarem?\n"
                "2. Escrevemos algo de errado? A idade, a espécie, o local. Corrigimos no "
                "próprio dia.\n"
                "3. Falta-nos alguma árvore? Ninguém conhece estas árvores melhor do que "
                "quem cuida delas, e é bem provável que tenhamos deixado de fora a mais "
                "interessante."),
        "close": ("A página é esta:\n{url}\n\n"
                  "Se preferirem não receber mais mensagens minhas, basta dizer e não volto "
                  "a escrever.\n\nCom os melhores cumprimentos,\nHidde\nancienttrees.app"),
    },
    "en": {
        "subject_site": "Your trees at {org}, and three questions",
        "subject_city": "The remarkable old trees of {city}, and three questions",
        "greet": "Hello,",
        "intro": ("My name is Hidde. I map the most remarkable old trees of cities at "
                  "ancienttrees.app, each with its story, its exact spot and a walking route "
                  "linking them. Everything is checked against at least two independent "
                  "sources, and it is free to read."),
        "ours_site": "We publish {n} trees for {city}, and {k} of them stand in your grounds:",
        "ours_city": "We publish {n} trees for {city}, among them:",
        "nophoto": ("Of those, {m} have no photograph at all. It is our biggest gap and it is "
                    "not one we can close from a desk."),
        "ask": ("Three questions, and any one of them helps:\n\n"
                "1. Do you have a photograph of these trees we could use, credited however "
                "you ask?\n"
                "2. Did we get anything wrong? The age, the species, the spot. We correct "
                "the same day.\n"
                "3. Have we missed a tree? Nobody knows these trees like the people who look "
                "after them, and there is a good chance we left out the best one."),
        "close": ("The page is here:\n{url}\n\n"
                  "If you would rather not hear from me again, just say so and I will not "
                  "write again.\n\nBest wishes,\nHidde\nancienttrees.app"),
    },
    "nl": {
        "subject_site": "Jullie bomen bij {org}, en drie vragen",
        "subject_city": "De bijzonderste oude bomen van {city}, en drie vragen",
        "greet": "Goedendag,",
        "intro": ("Mijn naam is Hidde. Ik breng op ancienttrees.app de bijzonderste oude bomen "
                  "van steden in kaart, elk met zijn verhaal, de exacte plek en een wandeling "
                  "die ze verbindt. Alles is tegen minstens twee onafhankelijke bronnen "
                  "gecontroleerd en vrij te lezen."),
        "ours_site": "Van {city} publiceren we {n} bomen, en {k} daarvan staan bij jullie:",
        "ours_city": "Van {city} publiceren we {n} bomen, waaronder:",
        "nophoto": ("Van die bomen hebben er {m} helemaal geen foto. Dat is ons grootste gat "
                    "en het is er een die je niet vanachter een bureau dicht."),
        "ask": ("Drie vragen, en aan elk ervan hebben we al iets:\n\n"
                "1. Hebben jullie een foto van deze bomen die we mogen gebruiken, met de "
                "naamsvermelding die jullie willen?\n"
                "2. Hebben we iets fout? De leeftijd, de soort, de plek. We passen het "
                "dezelfde dag aan.\n"
                "3. Missen we een boom? Niemand kent deze bomen zo goed als wie ervoor "
                "zorgt, en de kans is groot dat we juist de mooiste hebben overgeslagen."),
        "close": ("De pagina staat hier:\n{url}\n\n"
                  "Wil je liever niets meer van me horen, zeg het en ik schrijf niet meer.\n\n"
                  "Met vriendelijke groet,\nHidde\nancienttrees.app"),
    },
}
TEXT["it"] = TEXT["es"] = TEXT["de"] = TEXT["ca"] = TEXT["fr"] = TEXT["en"]
for k in ("da", "sv", "no", "fi"):
    TEXT[k] = TEXT["en"]


def compose(contact, cities):
    lang = (contact.get("language") or "en").split("|")[0]
    T = TEXT.get(lang, TEXT["en"])
    slug, hits = theirs(contact, cities)
    if not slug:
        return None
    city = cities[slug]["city"]
    n = len(cities[slug]["trees"])
    pool = hits if hits else cities[slug]["trees"]
    listed = pool[:6]
    lines = []
    for t in listed:
        mark = "" if t["photo"] else "  (nog geen foto)" if lang == "nl" else \
               "  (sem fotografia)" if lang == "pt" else "  (no photograph yet)"
        lines.append("- %s, %s%s" % (t["name"], t["species"], mark))
    missing = sum(1 for t in pool if not t["photo"])

    head = (T["ours_site"].format(city=city, n=n, k=len(hits)) if hits
            else T["ours_city"].format(city=city, n=n))
    body = [T["greet"], "", T["intro"], "", head, "\n".join(lines)]
    if missing:
        body += ["", T["nophoto"].format(m=missing)]
    body += ["", T["ask"], "",
             T["close"].format(url="https://ancienttrees.app/%s" % slug)]
    subject = (T["subject_site"].format(org=contact["org"]) if hits
               else T["subject_city"].format(city=city))
    return {"to": contact["email"], "found_at": contact.get("source_url", ""),
            "outlet": contact["org"], "subject": subject,
            "body": "\n".join(body)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--country")
    ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    contacts = json.load(open(os.path.join(ROOT, "data/outreach-contacts.json")))
    cities = city_trees()
    mails, skipped = [], []
    for c in contacts:
        if a.country and c.get("country") != a.country:
            continue
        if not c.get("email"):
            continue
        m = compose(c, cities)
        if not m:
            skipped.append(c["org"])
            continue
        mails.append(m)
        if len(mails) >= a.limit:
            break
    batch = {
        "batch": os.path.basename(a.out).replace(".json", ""),
        "note": ("Hidde's frame, 2026-08-09: ask for photographs, corrections and the tree we "
                 "missed. Never for coverage or a link. Each mail names the recipient's own "
                 "trees from our data."),
        "status": "draft",
        "mails": mails,
        "approved": None,
    }
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(batch, open(a.out, "w"), ensure_ascii=False, indent=1)
    open(a.out, "a").write("\n")
    print("wrote %s: %d mails" % (a.out, len(mails)))
    if skipped:
        print("skipped (no city match): %s" % ", ".join(skipped[:8]))


if __name__ == "__main__":
    main()
