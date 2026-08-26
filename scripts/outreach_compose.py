#!/usr/bin/env python3
"""Compose an outreach batch from data/outreach-contacts.json, in Hidde's voice.

Rewritten 2026-08-10 after he read batch 003 and called the openings
AI-generated. The old version paid a compliment and then explained why the
compliment was deserved, which is what a machine does when it tries to sound
sincere. His replacement, to use near-verbatim:

    Subject: Can you help me with ancienttrees.app? <their tree or city>
    I found this tree of yours online and think it's a remarkable tree!
    My name is Hidde...

That opening is also the honest one. We research from a distance and have
never stood in front of these trees, so a knowing first line pretends at a
familiarity we do not have, in a mail addressed to the one person who does.
Every tree page already tells readers the same thing at the bottom.

What must never appear: any request for coverage, a mention or a link. The
ask is photographs, corrections, and the tree we missed. A link, if it comes
at all, arises in the reply after their help is used and credited.

Templated on purpose here, and that is a real cost. Twelve mails are worth
writing by hand; a hundred and thirty are not, and the alternative to a
template is not sending. So the template earns its keep by being specific
where it counts: each mail names the recipient's own trees from our data and
says how many of them we publish without a photograph, both true and both
different per recipient.

Usage:
  python3 scripts/outreach_compose.py --limit 28 --out drafts/batches/batch-004.json
  python3 scripts/outreach_compose.py --country Netherlands --limit 20 --out ...
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


# English name -> the name the recipient uses. Built by inverting
# data/city-aliases.json, whose keys are local spellings, plus the handful of
# per-language forms that file has no reason to carry (it exists to stop the
# SITE publishing "Firenze"; a German mail to Schonbrunn saying "Vienna"
# needs the opposite direction). A mail that calls the recipient's own city by
# a foreign name undoes the work the first line just did.
def local_names():
    a = json.load(open(os.path.join(ROOT, "data/city-aliases.json")))["aliases"]
    inv = {}
    for local, eng in a.items():
        inv.setdefault(eng.title(), local.title())
    inv.update({"Vienna": "Wien", "Munich": "München", "Cologne": "Köln",
                "Geneva": "Genève", "Zurich": "Zürich", "Brussels": "Brussel",
                "The Hague": "Den Haag", "Copenhagen": "København",
                "Lisbon": "Lisboa", "Seville": "Sevilla", "Naples": "Napoli",
                "Rome": "Roma", "Florence": "Firenze", "Milan": "Milano",
                "Turin": "Torino", "Genoa": "Genova", "Venice": "Venezia",
                "Padua": "Padova", "Prague": "Praha", "Antwerp": "Antwerpen",
                "Warsaw": "Warszawa", "Athens": "Athina"})
    return inv


LOCAL = None


def cities():
    out = {}
    for p in glob.glob(os.path.join(ROOT, "data/cities/*.json")):
        d = json.load(open(p))
        out[os.path.basename(p)[:-5]] = {
            "city": d.get("city", ""),
            "trees": [{"name": t.get("name", ""),
                       "photo": (t.get("photo") or {}).get("status") == "approved"}
                      for t in d.get("trees", [])],
        }
    return out


def their_trees(contact, all_cities):
    """The recipient's own trees, matched conservatively.

    A wrong claim in the first paragraph ("your grounds hold these") ends the
    conversation with the one person who knows it is wrong, so a contact
    without a confident match falls back to the city's list and the mail says
    "in <city>" rather than "yours".
    """
    slug = next((s for s, d in all_cities.items()
                 if norm(d["city"]) == norm(contact.get("city", ""))), None)
    if not slug:
        return None, [], False
    # ONLY why_them, never the organisation's own name. Matching org words
    # against tree names claimed four Vienna trees for Schloss Schoenbrunn
    # including "The Giant Sequoias of Poetzleinsdorfer Schlosspark", because
    # "schloss" appears in both. Telling a palace it owns a tree in another
    # park is the one error that ends the conversation with the only person
    # who knows it is wrong. why_them was written by the research pass from
    # our own data and names the trees explicitly, so it is the only source
    # trusted here; without a match the mail speaks of the city, not of "yours".
    why = norm(contact.get("why_them", ""))
    hits = [t for t in all_cities[slug]["trees"] if norm(t["name"]) in why]
    return slug, (hits or all_cities[slug]["trees"]), bool(hits)


T = {
 "en": {
  "subj": "Can you help me with ancienttrees.app? {what}",
  "hi": "Hello,",
  "open": "I found this tree of yours online and think it's a remarkable tree!",
  "open_many": "I found these trees of yours online and think they are remarkable!",
  "open_plain": "I found this tree online and think it's a remarkable tree!",
  "open_many_plain": "I found these trees online and think they are remarkable!",
  "who": ("My name is Hidde. I map the most remarkable old trees of cities at "
          "ancienttrees.app, each with its story, its exact spot and a walk linking "
          "them, so people have a reason to go outside and stand in front of "
          "something old."),
  "ours": "We publish {n} trees for {city}:",
  "yours": "We publish {n} trees for {city}, and {k} of them are yours:",
  "yours_one": "We publish {n} trees for {city}, and one of them is yours:",
  "gap": "{m} of them have no photograph at all, which is our biggest gap.",
  "names": "(those are the names we use on the page, in English)",
  "ask": ("Two things would really help. Do you have photographs we could use, "
          "credited however you ask? And did we get anything wrong, or miss a tree "
          "that belongs on the list? You know these trees and we only found them "
          "online."),
  "end": ("The page is here:\n{url}\n\nIf you would rather not hear from me again, "
          "just say so.\n\nBest wishes,\nHidde\nancienttrees.app"),
 },
 "nl": {
  "subj": "Kun je me helpen met ancienttrees.app? {what}",
  "hi": "Goedendag,",
  "open": "Ik kwam deze boom van jullie online tegen en vind het een bijzondere boom!",
  "open_many": "Ik kwam deze bomen van jullie online tegen en vind ze bijzonder!",
  "open_plain": "Ik kwam deze boom online tegen en vind het een bijzondere boom!",
  "open_many_plain": "Ik kwam deze bomen online tegen en vind ze bijzonder!",
  "who": ("Mijn naam is Hidde. Ik breng op ancienttrees.app de bijzonderste oude bomen "
          "van steden in kaart, elk met zijn verhaal, de exacte plek en een wandeling "
          "die ze verbindt, zodat mensen een reden hebben om naar buiten te gaan en "
          "voor iets ouds te gaan staan."),
  "ours": "Van {city} publiceren we {n} bomen:",
  "yours": "Van {city} publiceren we {n} bomen, en {k} daarvan staan bij jullie:",
  "yours_one": "Van {city} publiceren we {n} bomen, en een daarvan staat bij jullie:",
  "gap": "Van die bomen hebben er {m} helemaal geen foto, en dat is ons grootste gat.",
  "names": "(dat zijn de namen die wij op de pagina gebruiken, in het Engels)",
  "ask": ("Twee dingen zouden echt helpen. Hebben jullie foto's die we mogen gebruiken, "
          "met de naamsvermelding die jullie willen? En hebben we iets fout, of missen "
          "we een boom die erbij hoort? Jullie kennen deze bomen, wij hebben ze alleen "
          "online gevonden."),
  "end": ("De pagina staat hier:\n{url}\n\nWil je liever niets meer van me horen, zeg "
          "het en ik schrijf niet meer.\n\nMet vriendelijke groet,\nHidde\nancienttrees.app"),
 },
 "pt": {
  "subj": "Pode ajudar-me com o ancienttrees.app? {what}",
  "hi": "Bom dia,",
  "open": "Encontrei esta árvore vossa online e acho-a uma árvore notável!",
  "open_many": "Encontrei estas árvores vossas online e acho-as notáveis!",
  "open_plain": "Encontrei esta árvore online e acho-a uma árvore notável!",
  "open_many_plain": "Encontrei estas árvores online e acho-as notáveis!",
  "who": ("Chamo-me Hidde. Reúno em ancienttrees.app as árvores antigas mais notáveis "
          "das cidades, cada uma com a sua história, a localização exacta e um percurso "
          "a pé que as liga, para dar às pessoas uma razão para sair e ir estar diante "
          "de uma coisa antiga."),
  "ours": "De {city} publicamos {n} árvores:",
  "yours": "De {city} publicamos {n} árvores, e {k} delas são vossas:",
  "yours_one": "De {city} publicamos {n} árvores, e uma delas é vossa:",
  "gap": "Destas, {m} não têm qualquer fotografia, e essa é a nossa maior falha.",
  "names": "(são os nomes que usamos na página, em inglês)",
  "ask": ("Duas coisas ajudariam muito. Teriam fotografias que pudéssemos usar, com o "
          "crédito que indicarem? E escrevemos alguma coisa errada, ou falta-nos uma "
          "árvore que devesse lá estar? Vocês conhecem estas árvores; nós apenas as "
          "encontrámos online."),
  "end": ("A página é esta:\n{url}\n\nSe preferirem não receber mais mensagens minhas, "
          "basta dizerem.\n\nCom os melhores cumprimentos,\nHidde\nancienttrees.app"),
 },
 "es": {
  "subj": "¿Puede ayudarme con ancienttrees.app? {what}",
  "hi": "Buenos días,",
  "open": "¡Encontré este árbol suyo por internet y me parece un árbol extraordinario!",
  "open_many": "¡Encontré estos árboles suyos por internet y me parecen extraordinarios!",
  "open_plain": "¡Encontré este árbol por internet y me parece un árbol extraordinario!",
  "open_many_plain": "¡Encontré estos árboles por internet y me parecen extraordinarios!",
  "who": ("Me llamo Hidde. Reúno en ancienttrees.app los árboles viejos más singulares "
          "de las ciudades, cada uno con su historia, su ubicación exacta y un paseo que "
          "los enlaza, para dar a la gente un motivo para salir y ponerse delante de "
          "algo antiguo."),
  "ours": "De {city} publicamos {n} árboles:",
  "yours": "De {city} publicamos {n} árboles, y {k} de ellos son suyos:",
  "yours_one": "De {city} publicamos {n} árboles, y uno de ellos es suyo:",
  "gap": "De ellos, {m} no tienen ninguna fotografía, y ese es nuestro mayor vacío.",
  "names": "(son los nombres que usamos en la página, en inglés)",
  "ask": ("Dos cosas ayudarían mucho. ¿Tendrían fotografías que pudiéramos usar, con el "
          "crédito que indiquen? ¿Y hemos escrito algo mal, o nos falta un árbol que "
          "debería estar? Ustedes conocen estos árboles; nosotros solo los encontramos "
          "por internet."),
  "end": ("La página está aquí:\n{url}\n\nSi prefieren no recibir más mensajes míos, "
          "basta con decirlo.\n\nUn saludo cordial,\nHidde\nancienttrees.app"),
 },
 "it": {
  "subj": "Può aiutarmi con ancienttrees.app? {what}",
  "hi": "Buongiorno,",
  "open": "Ho trovato questo vostro albero online e lo trovo un albero straordinario!",
  "open_many": "Ho trovato questi vostri alberi online e li trovo straordinari!",
  "open_plain": "Ho trovato questo albero online e lo trovo un albero straordinario!",
  "open_many_plain": "Ho trovato questi alberi online e li trovo straordinari!",
  "who": ("Mi chiamo Hidde. Raccolgo su ancienttrees.app gli alberi antichi più notevoli "
          "delle città, ognuno con la sua storia, il punto esatto e una passeggiata che "
          "li collega, per dare alle persone un motivo per uscire e mettersi davanti a "
          "qualcosa di antico."),
  "ours": "Di {city} pubblichiamo {n} alberi:",
  "yours": "Di {city} pubblichiamo {n} alberi, e {k} sono vostri:",
  "yours_one": "Di {city} pubblichiamo {n} alberi, e uno è vostro:",
  "gap": "Di questi, {m} non hanno alcuna fotografia, ed è la nostra lacuna più grande.",
  "names": "(sono i nomi che usiamo sulla pagina, in inglese)",
  "ask": ("Due cose aiuterebbero molto. Avreste fotografie che potremmo usare, con il "
          "credito che preferite? E abbiamo scritto qualcosa di sbagliato, o ci manca un "
          "albero che dovrebbe esserci? Voi conoscete questi alberi; noi li abbiamo solo "
          "trovati online."),
  "end": ("La pagina è questa:\n{url}\n\nSe preferite non ricevere più mie messaggi, "
          "basta dirlo.\n\nCordiali saluti,\nHidde\nancienttrees.app"),
 },
 "de": {
  "subj": "Können Sie mir mit ancienttrees.app helfen? {what}",
  "hi": "Guten Tag,",
  "open": "Ich bin online auf diesen Baum von Ihnen gestoßen und finde ihn bemerkenswert!",
  "open_many": "Ich bin online auf diese Bäume von Ihnen gestoßen und finde sie bemerkenswert!",
  "open_plain": "Ich bin online auf diesen Baum gestoßen und finde ihn bemerkenswert!",
  "open_many_plain": "Ich bin online auf diese Bäume gestoßen und finde sie bemerkenswert!",
  "who": ("Mein Name ist Hidde. Auf ancienttrees.app kartiere ich die bemerkenswertesten "
          "alten Bäume von Städten, jeden mit seiner Geschichte, dem genauen Standort und "
          "einem Spaziergang, der sie verbindet, damit Menschen einen Grund haben, nach "
          "draußen zu gehen und vor etwas Altem zu stehen."),
  "ours": "Für {city} veröffentlichen wir {n} Bäume:",
  "yours": "Für {city} veröffentlichen wir {n} Bäume, {k} davon sind Ihre:",
  "yours_one": "Für {city} veröffentlichen wir {n} Bäume, einer davon ist Ihrer:",
  "gap": "Davon haben {m} überhaupt kein Foto, und das ist unsere größte Lücke.",
  "names": "(so nennen wir sie auf der Seite, auf Englisch)",
  "ask": ("Zwei Dinge würden sehr helfen. Hätten Sie Fotos, die wir verwenden dürften, "
          "mit der Nennung, die Sie wünschen? Und haben wir etwas falsch geschrieben oder "
          "einen Baum übersehen, der dazugehört? Sie kennen diese Bäume; wir haben sie nur "
          "online gefunden."),
  "end": ("Die Seite finden Sie hier:\n{url}\n\nWenn Sie nichts mehr von mir hören möchten, "
          "sagen Sie einfach Bescheid.\n\nMit freundlichen Grüßen,\nHidde\nancienttrees.app"),
 },
}
T["ca"] = T["es"]
T["fr"] = T["en"]
for k in ("da", "sv", "no", "fi"):
    T[k] = T["en"]


# HIS letter, the default since 2026-08-26. Batches 005 and 006 went out in
# Hidde's own words, approved by him twice, and batch 006 added the mention
# line he asked for himself. Those letters are copied VERBATIM per language
# from the approved batches; nothing below is my prose except the Spanish
# mention line (Spain was deliberately absent from 006, so his letter never
# existed in Spanish with that line) and the short "{k} of them in your
# grounds" clause used only when the recipient actually holds the trees
# (why_them names them and owns_the_trees is not false). The older template
# above stays available as --style trees for photo-ask batches.
HIS = {
 "en": {
  "subj": "Can you help me with ancienttrees.app? The old trees of {city}",
  "body": ("Hello,\n\n"
           "My name is Hidde and I am building ancienttrees.app, a platform for "
           "remarkable trees. My goal is to get people excited about old trees and "
           "to encourage them to go and see them outside.\n\n"
           "We have {n} trees in {city}{theirs} and I was really curious whether "
           "you would take a look at whether they are right:\n{url}\n\n"
           "I also wondered: which tree do you personally think is missing?\n\n"
           "Any help would be much appreciated!\n\n"
           "And if you think the site is worth it, a mention on your website would "
           "help enormously to get these trees noticed.\n\n"
           "I would really like to hear your opinion on the project.\n\n"
           "Best wishes,\nHidde"),
  "theirs": ", {k} of them in your grounds,",
  "theirs_one": ", one of them in your grounds,",
 },
 "nl": {
  "subj": "Kun je me helpen met ancienttrees.app? De oude bomen van {city}",
  "body": ("Hallo,\n\n"
           "Mijn naam is Hidde en ik bouw aan ancienttrees.app, een platform voor "
           "opmerkelijke bomen. Mijn doel is om mensen enthousiast te maken over "
           "oude bomen en ze aan te moedigen om die buiten te gaan bekijken.\n\n"
           "We hebben {n} bomen in {city} staan{theirs} en ik was erg benieuwd of "
           "je een kijkje zou willen nemen of ze kloppen:\n{url}\n\n"
           "Daarnaast vroeg ik me af: welke boom mis jij persoonlijk op de site?\n\n"
           "Elke hulp zou zeer gewaardeerd worden!\n\n"
           "En als je de site de moeite waard vindt: een vermelding op jullie "
           "website zou enorm helpen om deze bomen onder de aandacht te brengen.\n\n"
           "Ik ben erg benieuwd naar jouw mening over het project.\n\n"
           "Met vriendelijke groet,\nHidde"),
  "theirs": ", waarvan {k} bij jullie,",
  "theirs_one": ", waarvan één bij jullie,",
 },
 "pt": {
  "subj": "Pode ajudar-me com o ancienttrees.app? As árvores de {city}",
  "body": ("Olá,\n\n"
           "Chamo-me Hidde e estou a construir o ancienttrees.app, uma plataforma "
           "para árvores notáveis. O meu objetivo é entusiasmar as pessoas pelas "
           "árvores antigas e incentivá-las a ir vê-las lá fora.\n\n"
           "Temos {n} árvores em {city}{theirs} e tinha muita curiosidade em saber "
           "se poderiam dar uma vista de olhos para ver se estão certas:\n{url}\n\n"
           "Além disso, perguntava-me: que árvore acham pessoalmente que falta no "
           "site?\n\n"
           "Qualquer ajuda seria muito apreciada!\n\n"
           "E se acharem o site útil, uma menção no vosso site ajudaria imenso a "
           "dar a conhecer estas árvores.\n\n"
           "Gostava muito de saber a vossa opinião sobre o projeto.\n\n"
           "Com os melhores cumprimentos,\nHidde"),
  "theirs": ", {k} delas no vosso recinto,",
  "theirs_one": ", uma delas no vosso recinto,",
 },
 "es": {
  "subj": "¿Me pueden ayudar con ancienttrees.app? Los árboles viejos de {city}",
  "body": ("Hola,\n\n"
           "Me llamo Hidde y estoy construyendo ancienttrees.app, una plataforma "
           "para árboles notables. Mi objetivo es entusiasmar a la gente con los "
           "árboles viejos y animarla a ir a verlos fuera.\n\n"
           "Tenemos {n} árboles en {city}{theirs} y tenía mucha curiosidad por "
           "saber si podrían echar un vistazo a ver si están bien:\n{url}\n\n"
           "Además me preguntaba: ¿qué árbol echan de menos personalmente en la "
           "web?\n\n"
           "¡Cualquier ayuda sería muy apreciada!\n\n"
           "Y si les parece que la web merece la pena, una mención en su página "
           "web ayudaría enormemente a dar a conocer estos árboles.\n\n"
           "Me interesa mucho su opinión sobre el proyecto.\n\n"
           "Un saludo cordial,\nHidde"),
  "theirs": ", {k} de ellos en su recinto,",
  "theirs_one": ", uno de ellos en su recinto,",
 },
 "it": {
  "subj": "Può aiutarmi con ancienttrees.app? Gli alberi di {city}",
  "body": ("Buongiorno,\n\n"
           "Mi chiamo Hidde e sto costruendo ancienttrees.app, una piattaforma per "
           "alberi notevoli. Il mio obiettivo è appassionare le persone agli alberi "
           "antichi e spingerle ad andare a vederli fuori.\n\n"
           "Abbiamo {n} alberi a {city}{theirs} ed ero molto curioso di sapere se "
           "potreste dare un'occhiata per vedere se sono giusti:\n{url}\n\n"
           "Inoltre mi chiedevo: quale albero pensate personalmente che manchi sul "
           "sito?\n\n"
           "Ogni aiuto sarebbe molto apprezzato!\n\n"
           "E se il sito vi sembra utile, una menzione sul vostro sito aiuterebbe "
           "moltissimo a far conoscere questi alberi.\n\n"
           "Mi interessa molto la vostra opinione sul progetto.\n\n"
           "Cordiali saluti,\nHidde"),
  "theirs": ", {k} dei quali da voi,",
  "theirs_one": ", uno dei quali da voi,",
 },
 "de": {
  "subj": "Können Sie mir mit ancienttrees.app helfen? Die alten Bäume von {city}",
  "body": ("Guten Tag,\n\n"
           "mein Name ist Hidde und ich baue ancienttrees.app, eine Plattform für "
           "bemerkenswerte Bäume. Mein Ziel ist es, Menschen für alte Bäume zu "
           "begeistern und sie dazu zu bringen, hinauszugehen und sie anzuschauen.\n\n"
           "Wir haben {n} Bäume in {city}{theirs} und mich würde sehr "
           "interessieren, ob Sie einmal nachsehen würden, ob sie stimmen:\n{url}\n\n"
           "Außerdem habe ich mich gefragt: welcher Baum fehlt Ihnen persönlich "
           "auf der Seite?\n\n"
           "Über jede Hilfe würde ich mich sehr freuen!\n\n"
           "Und falls Sie die Seite für nützlich halten: eine Erwähnung auf Ihrer "
           "Website würde enorm helfen, diese Bäume bekannt zu machen.\n\n"
           "Ihre Meinung zu dem Projekt interessiert mich sehr.\n\n"
           "Mit freundlichen Grüßen,\nHidde"),
  "theirs": ", {k} davon bei Ihnen,",
  "theirs_one": ", einer davon bei Ihnen,",
 },
}
HIS["ca"] = HIS["es"]
HIS["fr"] = HIS["en"]
for k in ("da", "sv", "no", "fi", "cs", "pl"):
    HIS[k] = HIS["en"]


def compose_letter(contact, all_cities):
    lang = (contact.get("language") or "en").split("|")[0]
    t = HIS.get(lang, HIS["en"])
    slug, pool, theirs = their_trees(contact, all_cities)
    if not slug:
        return None
    if contact.get("owns_the_trees") is False:
        theirs = False
    city = all_cities[slug]["city"]
    if lang != "en":
        city = LOCAL.get(city, city)
    k = len(pool) if theirs else 0
    clause = ""
    if theirs:
        clause = (t["theirs_one"] if k == 1 else t["theirs"]).format(k=k)
    body = t["body"].format(n=len(all_cities[slug]["trees"]), city=city,
                            theirs=clause,
                            url="https://ancienttrees.app/%s" % slug)
    subject = t["subj"].format(city=city).strip()
    # Porto takes the article in Portuguese: "as árvores do Porto", "no Porto".
    # Batch 006 already went out saying "do Porto" in its subject.
    if lang == "pt" and city == "Porto":
        subject = subject.replace("de Porto", "do Porto")
        body = body.replace("em Porto", "no Porto")
    return {"to": contact["email"], "found_at": contact.get("source_url", ""),
            "outlet": contact["org"], "subject": subject, "body": body}


def compose(contact, all_cities):
    lang = (contact.get("language") or "en").split("|")[0]
    t = T.get(lang, T["en"])
    slug, pool, theirs = their_trees(contact, all_cities)
    if not slug:
        return None
    # "This tree of yours" is a claim, and mailcheck's POSSESSIVE CLAIM check
    # exists because a wrong one went to Berlin (the Kaisereiche that was never
    # in their register). The old code claimed possession in the opening line
    # of EVERY mail, including the ones whose own body fell back to "we publish
    # n trees for <city>" because nothing matched. Possessive language now
    # needs the same justification everywhere: a why_them match, and never
    # against an explicit owns_the_trees: false in the contact file.
    if contact.get("owns_the_trees") is False:
        theirs = False
    city = all_cities[slug]["city"]
    if lang != "en":
        city = LOCAL.get(city, city)
    listed = pool[:6]
    missing = sum(1 for x in pool if not x["photo"])
    what = city if not theirs else (listed[0]["name"] if len(listed) == 1 else city)

    if theirs:
        opening = t["open"] if len(listed) == 1 else t["open_many"]
    else:
        opening = t["open_plain"] if len(listed) == 1 else t["open_many_plain"]
    body = [t["hi"], "",
            opening, "",
            t["who"], "",
            (t["yours_one"] if theirs and len(listed) == 1 else t["yours"] if theirs else t["ours"]).format(
                city=city, n=len(all_cities[slug]["trees"]), k=len(listed)),
            "\n".join("- " + x["name"] for x in listed)]
    if lang != "en":
        body.append(t["names"])
    if missing:
        body += ["", t["gap"].format(m=missing)]
    body += ["", t["ask"], "", t["end"].format(url="https://ancienttrees.app/%s" % slug)]
    return {"to": contact["email"], "found_at": contact.get("source_url", ""),
            "outlet": contact["org"], "subject": t["subj"].format(what=what).strip(),
            "body": "\n".join(body)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--country")
    ap.add_argument("--limit", type=int, default=28)
    ap.add_argument("--style", choices=["letter", "trees"], default="letter",
                    help="letter: Hidde's own batch-005/006 letter (default). "
                         "trees: the older photo-and-corrections template.")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    done = {r["to"].lower() for r in json.load(open(os.path.join(ROOT, "data/outreach-sent.json")))["sent"]}
    contacts = json.load(open(os.path.join(ROOT, "data/outreach-contacts.json")))
    global LOCAL
    LOCAL = local_names()
    all_cities = cities()
    mails, skipped = [], []
    for c in contacts:
        if a.country and c.get("country") != a.country:
            continue
        if not c.get("email") or c["email"].lower() in done:
            continue
        m = (compose_letter if a.style == "letter" else compose)(c, all_cities)
        if not m:
            skipped.append(c["org"])
            continue
        mails.append(m)
        if len(mails) >= a.limit:
            break
    batch = {"batch": os.path.basename(a.out).replace(".json", ""),
             "note": ("Hidde's own letter from batches 005/006, with his mention line, "
                      "verbatim per language. Where the recipient holds the trees the "
                      "middle sentence says so, justified by why_them and owns_the_trees."
                      if a.style == "letter" else
                      "Hidde's voice, 2026-08-10: subject asks for help, opening says we found "
                      "the tree online and think it is remarkable. No word about coverage or "
                      "links; the ask is photographs, corrections, and the tree we missed."),
             "status": "draft", "mails": mails, "approved": None}
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(batch, open(a.out, "w"), ensure_ascii=False, indent=1)
    open(a.out, "a").write("\n")
    print("wrote %s: %d mails" % (a.out, len(mails)))
    if skipped:
        print("skipped (no city match): %d, e.g. %s" % (len(skipped), ", ".join(skipped[:5])))


if __name__ == "__main__":
    main()
