#!/usr/bin/env python3
"""Compose a cold batch to NAMED people that opens on one concrete question.

Why this exists (Hidde, 2026-10-10, "go" on the proposal): the help asks of
2026-10-06 to 10-09 went mostly to general inboxes and asked "can you help,
or do you know somebody who could?". About one in ten answered, and most of
those answers were "I forwarded it" (Leipzig, Amersfoort, Leuven, Ottawa,
Manchester). The replies that brought something were people answering a
concrete question: Kerry Pickett sent three facts about the Preston Twins,
Lenny van Valkenhoef named a plane tree the moment she was asked for her
favourite. So mail 1 now asks exactly that, of a person rather than an inbox:
which tree in your city are we missing.

What it does NOT do: offer the ambassador role (mailcheck refuses that in a
first mail; it comes in mail 2, drafts/ambassador-mails.md), name a price, or
explain how we work.

Input: a contacts file whose rows carry city, slug, language, first_name,
full_name, email (rows without an email are skipped and printed).

    python3 scripts/outreach_named.py data/outreach-contacts-named-2026-10-10.json \
        --batch named-2026-10-10 --out drafts/batches/named-2026-10-10.json
"""
import argparse
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DE_NAMES = {"Munich": "München", "Nuremberg": "Nürnberg", "Cologne": "Köln",
            "Vienna": "Wien", "Zurich": "Zürich"}
LOCAL_NAMES = {
    "nl": {"The Hague": "Den Haag", "Ghent": "Gent", "Brussels": "Brussel"},
    "it": {"Rome": "Roma", "Milan": "Milano", "Florence": "Firenze", "Naples": "Napoli",
           "Sardinia": "Sardegna", "Genoa": "Genova", "Padua": "Padova"},
    "es": {"Palma de Mallorca": "Palma"},
    "fr": {"Geneva": "Genève", "Luxembourg City": "Luxembourg", "Brussels": "Bruxelles"},
}

# Mail 1 in the reader's own language: the same three moves as the English one
# (the page, one tree on it, the question), nothing added.
LOCAL = {
    "nl": ("Welke boom in {city} missen we nog?",
           "Hoi {first},\n\n"
           "We hebben een pagina gemaakt over de bijzondere oude bomen van {city}: {url}. "
           "Daarop staat onder meer {tree}.\n\n"
           "Welke boom in {city} missen we nog? Jij kent ze veel beter dan wij, "
           "en ik hoor graag welke jij zou toevoegen.\n\n"
           "Hoe dan ook bedankt,\nHidde"),
    "it": ("Quale albero di {city} ci manca?",
           "Buongiorno {full},\n\n"
           "abbiamo fatto una pagina sui grandi alberi antichi di {city}: {url}. "
           "Tra gli altri c'è «{tree}».\n\n"
           "Quale albero di {city} ci manca ancora? Lei li conosce molto meglio di noi, "
           "e mi farebbe piacere sapere quale aggiungerebbe.\n\n"
           "Grazie in ogni caso,\nHidde"),
    "es": ("¿Qué árbol de {city} nos falta?",
           "Buenos días, {full}:\n\n"
           "hemos hecho una página sobre los árboles antiguos más notables de {city}: {url}. "
           "Entre otros incluye «{tree}».\n\n"
           "¿Qué árbol de {city} nos falta? Usted los conoce mucho mejor que nosotros, "
           "y me encantaría saber cuál añadiría.\n\n"
           "Gracias en cualquier caso,\nHidde"),
    "fr": ("Quel arbre de {city} nous manque-t-il ?",
           "Bonjour {full},\n\n"
           "nous avons fait une page sur les arbres anciens remarquables de {city} : {url}. "
           "On y trouve notamment « {tree} ».\n\n"
           "Quel arbre de {city} nous manque encore ? Vous les connaissez bien mieux que nous, "
           "et j'aimerais beaucoup savoir lequel vous ajouteriez.\n\n"
           "Merci dans tous les cas,\nHidde"),
}

EN = ("Hi {first},\n\n"
      "We made a page about the remarkable old trees of {city}: {url}. It includes {tree}.\n\n"
      "Which tree in {city} are we missing? You know them far better than we do, "
      "and I'd love to hear the one you would add.\n\n"
      "Thanks either way,\nHidde")
EN_SUBJECT = "Which tree in {city} are we missing?"

DE = ("Guten Tag {full},\n\n"
      "wir haben eine Seite über die besonderen alten Bäume von {city} gemacht: {url}. "
      "Darauf steht unter anderem „{tree}“.\n\n"
      "Welcher Baum in {city} fehlt uns noch? Sie kennen sie viel besser als wir, "
      "und ich würde gern hören, welchen Sie hinzufügen würden.\n\n"
      "Vielen Dank in jedem Fall,\nHidde")
DE_SUBJECT = "Welcher Baum in {city} fehlt uns noch?"


def lead_tree(slug):
    """The tree the mail names: the first one with an approved photograph,
    so the link lands on a page that shows the city at its best."""
    path = os.path.join(ROOT, "data", "cities", slug + ".json")
    city = json.load(open(path, encoding="utf-8"))
    trees = city["trees"]
    pick = next((t for t in trees if (t.get("photo") or {}).get("status") == "approved"), trees[0])
    return city["city"], pick["name"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("contacts")
    ap.add_argument("--batch", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = json.load(open(a.contacts, encoding="utf-8"))["contacts"]
    mails, skipped = [], []
    for r in rows:
        if not r.get("email"):
            skipped.append(r.get("city") or "?")
            continue
        slug = r.get("slug")
        if slug and os.path.exists(os.path.join(ROOT, "data", "cities", slug + ".json")):
            city, tree = lead_tree(slug)
            url = "https://ancienttrees.app/" + slug
        else:
            skipped.append("%s (no published place to point at)" % (r.get("city") or r.get("org")))
            continue
        lang = r.get("language")
        if lang in LOCAL:
            c = LOCAL_NAMES.get(lang, {}).get(city, city)
            t = tree[4:] if tree.startswith("The ") else tree
            if lang == "nl":
                t = "de " + t if tree.startswith("The ") else t
            subj, tmpl = LOCAL[lang]
            body = tmpl.format(first=r.get("first_name") or r.get("full_name"),
                               full=r.get("full_name") or r.get("first_name"), city=c, url=url, tree=t)
            subject = subj.format(city=c)
        elif lang == "de":
            c = DE_NAMES.get(city, city)
            t = tree[4:] if tree.startswith("The ") else tree
            body = DE.format(full=r.get("full_name") or r.get("first_name"), city=c, url=url, tree=t)
            subject = DE_SUBJECT.format(city=c)
        else:
            t = "the " + tree[4:] if tree.startswith("The ") else tree
            body = EN.format(first=r.get("first_name") or r.get("full_name"), city=city, url=url, tree=t)
            subject = EN_SUBJECT.format(city=city)
        mails.append({"to": r["email"].strip(),
                      "outlet": "%s, %s (%s, missing-tree ask)" % (r.get("full_name") or "?", r.get("org") or "?", city),
                      "subject": subject, "body": body,
                      "source_url": r.get("source_url")})
    batch = {"batch": a.batch, "status": "draft",
             "note": "Named people, one concrete question in mail 1 (Hidde, 2026-10-10: go). Awaits his word.",
             "mails": mails}
    json.dump(batch, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("%d mails written to %s; %d rows skipped" % (len(mails), a.out, len(skipped)))
    for s in skipped:
        print("   skip", s)


if __name__ == "__main__":
    main()
