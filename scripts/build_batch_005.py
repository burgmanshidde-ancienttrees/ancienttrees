#!/usr/bin/env python3
"""Build drafts/batches/batch-005.json: 40 mails to tree societies, city tree groups and blogs.

The shape is batch 004's, which is the one that earned replies, with one change
Hidde asked for on 2026-08-15: the personal question closes the mail as an
extra line ("just to hear your personal opinion which tree do you think we are
missing of your city, any personal tips"). The main ask stays what it was, the
page itself. His second instruction the same day: no line about living in Baarn.

Counts are read from the live city files at build time, so a mail never quotes
a number that has moved. The named tree per recipient is picked by hand from
their own city file, so nothing here is generated from a pattern.
"""
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://ancienttrees.app/"

# opener: own = they hold the tree, city = it is their own city, else the city is named
OPENERS = {
    "en": {
        "park": "I found this tree in {place} online and think it's a remarkable tree!",
        "own": "I found this tree of yours online and think it's a remarkable tree!",
        "city": "I found this tree in your city online and think it's a remarkable tree!",
        "far": "I found this tree in {city} online and think it's a remarkable tree!",
    },
    "nl": {
        "park": "Ik kwam deze boom in {place} online tegen en vind het een prachtige boom!",
        "own": "Ik kwam deze boom van jullie online tegen en vind het een prachtige boom!",
        "city": "Ik kwam deze boom in jullie stad online tegen en vind het een prachtige boom!",
        "far": "Ik kwam deze boom in {city} online tegen en vind het een prachtige boom!",
    },
    "pt": {
        "park": "Encontrei esta árvore em {place} online e acho-a notável!",
        "own": "Encontrei esta vossa árvore online e acho-a notável!",
        "city": "Encontrei esta árvore da vossa cidade online e acho-a notável!",
        "far": "Encontrei esta árvore em {city} online e acho-a notável!",
    },
    "es": {
        "park": "¡Encontré este árbol en {place} en internet y me parece un árbol notable!",
        "own": "¡Encontré este árbol suyo en internet y me parece un árbol notable!",
        "city": "¡Encontré este árbol de su ciudad en internet y me parece un árbol notable!",
        "far": "¡Encontré este árbol en {city} en internet y me parece un árbol notable!",
    },
    "ca": {
        "park": "He trobat aquest arbre a {place} en línia i em sembla un arbre extraordinari!",
        "own": "He trobat aquest arbre vostre en línia i em sembla un arbre extraordinari!",
        "city": "He trobat aquest arbre de la vostra ciutat en línia i em sembla un arbre extraordinari!",
        "far": "He trobat aquest arbre a {city} en línia i em sembla un arbre extraordinari!",
    },
    "it": {
        "park": "Ho trovato online questo albero al {place} e lo trovo notevole!",
        "own": "Ho trovato online questo vostro albero e lo trovo notevole!",
        "city": "Ho trovato online questo albero della vostra città e lo trovo notevole!",
        "far": "Ho trovato online questo albero a {city} e lo trovo notevole!",
    },
}

# (miss > 1, miss == 1)
PHOTOLINE = {
    "en": ("{miss} of them have no photograph at all, which is our biggest gap.",
           "One of them has no photograph at all, which is our biggest gap."),
    "nl": ("Van {miss} daarvan hebben we nog geen enkele foto, dat is ons grootste gat.",
           "Van één daarvan hebben we nog geen enkele foto, dat is ons grootste gat."),
    "pt": ("De {miss} delas não temos nenhuma fotografia, e essa é a nossa maior falha.",
           "De uma delas não temos nenhuma fotografia, e essa é a nossa maior falha."),
    "es": ("De {miss} de ellos no tenemos ninguna fotografía, y ese es nuestro mayor hueco.",
           "De uno de ellos no tenemos ninguna fotografía, y ese es nuestro mayor hueco."),
    "ca": ("De {miss} d'ells no en tenim cap fotografia, i aquest és el nostre buit més gran.",
           "D'un d'ells no en tenim cap fotografia, i aquest és el nostre buit més gran."),
    "it": ("Di {miss} di questi non abbiamo nessuna fotografia, ed è la nostra lacuna più grande.",
           "Di uno di questi non abbiamo nessuna fotografia, ed è la nostra lacuna più grande."),
}

T = {
    "en": (
        "Can you help me with ancienttrees.app? {topic}",
        """Hello,

My name is Hidde and I am building ancienttrees.app, a platform for incredible trees. My goal is to get people excited about old trees and to encourage them to go and see them outside.

We have {n} trees in {city} and I was really curious whether you would take a look at whether they are right:
{url}

I also wondered: do you have a personal tree that you find special?

Any help would be much appreciated, photographs above all, to make the site better.

I would really like to hear your opinion on the project.

Best wishes,
Hidde""",
    ),
    "nl": (
        "Kun je me helpen met ancienttrees.app? {topic}",
        """Hallo,

Mijn naam is Hidde en ik bouw aan ancienttrees.app, een platform voor ongelofelijke bomen. Mijn doel is om mensen enthousiast te maken over oude bomen en ze aan te moedigen om die buiten te gaan bekijken.

We hebben {n} bomen in {city} staan en ik was erg benieuwd of je een kijkje zou willen nemen of ze kloppen:
{url}

Daarnaast vroeg ik me af: heb je een persoonlijke boom die je bijzonder vindt?

Elke hulp zou zeer gewaardeerd worden, vooral foto's om de website te verbeteren.

Ik ben erg benieuwd naar jouw mening over het project.

Met vriendelijke groet,
Hidde""",
    ),
    "pt": (
        "Pode ajudar-me com o ancienttrees.app? {topic}",
        """Olá,

Chamo-me Hidde e estou a construir o ancienttrees.app, uma plataforma para árvores incríveis. O meu objetivo é entusiasmar as pessoas pelas árvores antigas e incentivá-las a ir vê-las lá fora.

Temos {n} árvores em {city} e tinha muita curiosidade em saber se poderiam dar uma vista de olhos para ver se estão certas:
{url}

Além disso, perguntava-me: têm alguma árvore pessoal que achem especial?

Qualquer ajuda seria muito apreciada, sobretudo fotografias, para melhorar o site.

Gostava muito de saber a vossa opinião sobre o projeto.

Com os melhores cumprimentos,
Hidde""",
    ),
    "es": (
        "¿Me pueden ayudar con ancienttrees.app? {topic}",
        """Hola,

Me llamo Hidde y estoy construyendo ancienttrees.app, una plataforma para árboles increíbles. Mi objetivo es entusiasmar a la gente con los árboles viejos y animarla a ir a verlos fuera.

Tenemos {n} árboles en {city} y tenía mucha curiosidad por saber si podrían echar un vistazo a ver si están bien:
{url}

Además me preguntaba: ¿tienen algún árbol personal que les parezca especial?

Cualquier ayuda sería muy apreciada, sobre todo fotografías, para mejorar la web.

Me interesa mucho su opinión sobre el proyecto.

Un saludo cordial,
Hidde""",
    ),
    "ca": (
        "Em podeu ajudar amb ancienttrees.app? {topic}",
        """Hola,

Em dic Hidde i estic construint ancienttrees.app, una plataforma per a arbres increïbles. El meu objectiu és engrescar la gent amb els arbres vells i animar-la a anar a veure'ls a fora.

Tenim {n} arbres a {city} i tenia molta curiositat per saber si hi podríeu fer un cop d'ull per veure si són correctes:
{url}

A més em preguntava: teniu algun arbre personal que us sembli especial?

Qualsevol ajuda seria molt apreciada, sobretot fotografies, per millorar el web.

M'interessa molt la vostra opinió sobre el projecte.

Cordialment,
Hidde""",
    ),
    "it": (
        "Può aiutarmi con ancienttrees.app? {topic}",
        """Buongiorno,

Mi chiamo Hidde e sto costruendo ancienttrees.app, una piattaforma per alberi incredibili. Il mio obiettivo è appassionare le persone agli alberi antichi e spingerle ad andare a vederli fuori.

Abbiamo {n} alberi a {city} ed ero molto curioso di sapere se potreste dare un'occhiata per vedere se sono giusti:
{url}

Inoltre mi chiedevo: avete un albero personale che trovate speciale?

Ogni aiuto sarebbe molto apprezzato, soprattutto fotografie, per migliorare il sito.

Mi interessa molto la vostra opinione sul progetto.

Cordiali saluti,
Hidde""",
    ),
}

# email, org, lang, subject tail, city as written in that language, tree, slug, scope, extra
TARGETS = [
    # Netherlands
    ("info@vriendenvansonsbeek.nl", "Vrienden van Sonsbeek", "nl", "de bomen van Arnhem",
     "Arnhem", "De Poortwachters bij de ingang van Zijpendaal", "arnhem", "park:Sonsbeek", None),
    ("info@haagsehofjes.nl", "Stichting Haagse Hofjes", "nl", "de oude bomen van Den Haag",
     "Den Haag", "de juttepeer in het Heilige Geesthofje aan de Paviljoensgracht", "the-hague", "park:het Heilige Geesthofje", None),
    ("info@bomenstichtingdenhaag.nl", "Bomenstichting Den Haag", "nl", "de oude bomen van Den Haag",
     "Den Haag", "de juttepeer in het Heilige Geesthofje", "the-hague", "city", None),
    ("algemeen@kringvrienden.nl", "Kring Vrienden van 's-Hertogenbosch", "nl", "de bomen op de vestingwerken",
     "Den Bosch", "de Weichselboom op de Parklaan, die in de oude stadsmuur wortelt", "den-bosch", "city", None),
    ("info@ivn.nl", "IVN Natuureducatie", "nl", "de oude bomen van Nederlandse steden",
     "Nederland", "de Heimanseik in de Plantage in Amsterdam", "netherlands", "far", None),
    ("info@utrechtsebomenstichting.nl", "Utrechtse Bomenstichting", "nl", "de oude bomen van Utrecht",
     "Utrecht", "de Uithof-linde", "utrecht", "city", None),
    ("info@boomwachtersgroningen.nl", "Boomwachters Groningen", "nl", "de oude bomen van Groningen",
     "Groningen", "de eiken op de sterpunten van het Sterrebos", "groningen", "city", None),
    ("mail@bomenstichtingamsterdam.nl", "Bomenstichting afdeling Amsterdam", "nl", "de oude bomen van Amsterdam",
     "Amsterdam", "de Heimanseik in de Plantage", "amsterdam", "city", None),
    ("info@bomenbeschermingamsterdam.nl", "Bomen Bescherming Amsterdam", "nl", "de oude bomen van Amsterdam",
     "Amsterdam", "de platanen van het Leidsebosje", "amsterdam", "city", None),
    ("secretaris@bomenbondrijnland.nl", "Bomenbond Rijnland", "nl", "de oude bomen van Leiden",
     "Leiden", "de Beets-beuk op de Burcht", "leiden", "city", None),
    ("haarlemsebomenwachters@gmail.com", "Haarlemse Bomenwachters", "nl", "de oude bomen van Haarlem",
     "Haarlem", "de beuk waar Lodewijk Napoleon zijn monogram in kerfde", "haarlem", "city", None),
    ("info@bomenbieb.nl", "Bomenbieb", "nl", "bijzondere bomen in Nederland",
     "Nederland", "de juttepeer in het Heilige Geesthofje in Den Haag", "netherlands", "far", None),
    ("info@boommade.nl", "Boommade", "nl", "de oude bomen van Amsterdam",
     "Amsterdam", "de vleugelnoot in het Wertheimpark", "amsterdam", "far", None),
    # Belgium
    ("administratie@bomenbeterbeheren.org", "Bomen Beter Beheren vzw", "nl", "de oude bomen van Antwerpen",
     "Antwerpen", "de zomerlinde van het Rivierenhof", "antwerp", "far", None),
    ("info@bosplus.be", "BOS+", "nl", "de oude bomen van Brussel",
     "Brussel", "de vijvereiken van het Ter Kamerenbos", "brussels", "far", None),
    ("info@vvog.info", "Vereniging voor Openbaar Groen (VVOG)", "nl", "de oude bomen van Antwerpen",
     "Antwerpen", "de bruine beuk bij de Sint-Willibrorduskerk in Berchem", "antwerp", "far", None),
    ("info@wndln.be", "wndln (wandelblog Vlaanderen)", "nl", "een wandeling langs de oude bomen van Brussel",
     "Brussel", "de vijvereiken van het Ter Kamerenbos", "brussels", "far", None),
    # Portugal
    ("lisboa@quercus.pt", "Quercus, Núcleo Regional de Lisboa", "pt", "as árvores de Lisboa",
     "Lisboa", "as oliveiras de Santo Amaro", "lisbon", "city", None),
    ("setubal@quercus.pt", "Quercus, Núcleo Regional de Setúbal", "pt", "as árvores de Setúbal",
     "Setúbal", "as seis araucárias do Largo José Afonso", "setubal", "city", None),
    ("geral@lpn.pt", "Liga para a Protecção da Natureza (LPN)", "pt", "as árvores de Lisboa",
     "Lisboa", "o dragoeiro da Ajuda", "lisbon", "city", None),
    ("geral@icnf.pt", "ICNF", "pt", "as árvores de interesse público que publicamos",
     "Portugal", "as oliveiras de Santo Amaro em Lisboa", "portugal", "far",
     "O vosso registo de Arvoredo de Interesse Público está creditado nas nossas páginas. "
     "Uma coisa que encontrámos e que talvez queiram saber: três oliveiras de Setúbal têm 2009 "
     "na coluna da idade, que parece ser um ano e não um número de anos."),
    ("geral@wilder.pt", "Wilder", "pt", "as árvores antigas de Lisboa",
     "Lisboa", "o ombú do Largo do Limoeiro", "lisbon", "far", None),
    ("naturlink@naturlink.pt", "Naturlink", "pt", "um passeio pelas árvores de Setúbal",
     "Setúbal", "a melaleuca que cresce de lado", "setubal", "far", None),
    ("lisboa@secretmedianetwork.com", "Lisboa Secreta", "pt", "as árvores escondidas de Lisboa",
     "Lisboa", "a figueira-da-borracha gigante da Mouraria", "lisbon", "city", None),
    # Spain
    ("hola@aearboricultura.org", "Asociación Española de Arboricultura", "es", "los árboles viejos de Sevilla",
     "Sevilla", "el ombú de La Cartuja", "seville", "far", None),
    ("secretaria@aepjp.org", "Asociación Española de Parques y Jardines Públicos", "es", "los árboles del Retiro",
     "Madrid", "el ahuehuete del Parterre", "madrid", "far", None),
    ("bosquessinfronteras@bosquessinfronteras.com", "Bosques sin Fronteras", "es", "los árboles singulares de Valencia",
     "Valencia", "El Titán, el ficus del Parterre", "valencia", "far", None),
    ("info@plantipodes-am.cat", "Plantipodes-AM", "ca", "els arbres monumentals de Barcelona",
     "Barcelona", "l'alzina del carrer de l'Encarnació", "barcelona", "city", None),
    ("observatoriforestal@ctfc.cat", "Observatori Forestal de Catalunya", "ca", "els arbres monumentals de Barcelona",
     "Barcelona", "els garrofers del Park Güell", "barcelona", "city", None),
    # Italy
    ("sbi@unifi.it", "Società Botanica Italiana", "it", "gli alberi antichi di Firenze",
     "Firenze", "il tasso del Micheli nel Giardino dei Semplici", "florence", "far", None),
    ("segreteria@isaitalia.org", "ISA Italia", "it", "i platani dei Giardini Montanelli",
     "Milano", "Il Sacerdote", "milan", "far", None),
    ("italianostra@italianostra.org", "Italia Nostra", "it", "gli alberi delle ville storiche di Roma",
     "Roma", "il ginkgo di Villa Sciarra", "rome", "far", None),
    ("laboratoriocarteinregola@gmail.com", "Laboratorio Carteinregola", "it", "gli alberi di Roma",
     "Roma", "Adonis, il platano della Valle dei Platani a Villa Borghese", "rome", "city", None),
    ("info@villaghigi.it", "Fondazione Villa Ghigi", "it", "gli alberi antichi di Bologna",
     "Bologna", "il cedro dell'Himalaya di Villa Ghigi", "bologna", "own", None),
    ("amicitrotter@gmail.com", "Comitato Amici del Parco Trotter", "it", "la Quercia Rossa del Trotter",
     "Milano", "La Quercia Rossa del Trotter", "milan", "park:Parco Trotter", None),
    # UK and Ireland
    ("kwactiongroup@gmail.com", "Kings Weston Action Group", "en", "the old trees of Bristol",
     "Bristol", "the Oak of Kings Weston", "bristol", "park:Kings Weston", None),
    ("info@treecouncil.org.uk", "The Tree Council", "en", "the old trees of London",
     "London", "the Totteridge Yew", "london", "far", None),
    ("admin@trees.org.uk", "Arboricultural Association", "en", "the old trees of London",
     "London", "the Cheapside Plane", "london", "far", None),
    ("trees@treecouncil.ie", "Tree Council of Ireland", "en", "the old trees of Dublin",
     "Dublin", "the Hungry Tree on Constitution Hill", "dublin", "far", None),
    ("admin@ancienttreeforum.org.uk", "Ancient Tree Forum", "en", "the veteran trees of Edinburgh",
     "Edinburgh", "the Craigmillar Castle yews", "edinburgh", "far", None),
]

COUNTRY_SLUGS = {"netherlands": "Netherlands", "portugal": "Portugal"}


def counts(slug):
    """Trees published and trees with no photograph, read live from the city files."""
    files = []
    if slug in COUNTRY_SLUGS:
        for f in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
            if json.load(open(f))["country"] == COUNTRY_SLUGS[slug]:
                files.append(f)
    else:
        files = [os.path.join(ROOT, "data", "cities", f"{slug}.json")]
    n = miss = 0
    for f in files:
        for t in json.load(open(f))["trees"]:
            n += 1
            if not (t.get("photo") or {}).get("url"):
                miss += 1
    return n, miss


def main():
    mails = []
    for email, org, lang, topic, city, tree, slug, scope, extra in TARGETS:
        n, miss = counts(slug)
        subj_t, body_t = T[lang]
        plural, single = PHOTOLINE[lang]
        photoline = "" if miss == 0 else (single if miss == 1 else plural.format(miss=miss))
        body = body_t.format(n=n, city=city, url=B + slug)
        if extra:
            parts = body.split("\n\n")
            parts.insert(5, extra)
            body = "\n\n".join(parts)
        mails.append({
            "to": email,
            "outlet": org,
            "subject": subj_t.format(topic=topic[0].upper() + topic[1:]),
            "body": body,
        })
    batch = {
        "batch": "batch-005",
        "note": ("Batch 004's shape, which is the one that earned replies, plus the closing "
                 "line Hidde asked for on 2026-08-15: 'just to hear your personal opinion "
                 "which tree do you think we are missing of your city, any personal tips'. "
                 "No Baarn line, on his instruction the same day. Recipients are tree "
                 "societies, city tree groups and tree blogs: the categories that answer "
                 "and that can link."),
        "status": "pending_approval",
        "mails": mails,
    }
    out = os.path.join(ROOT, "drafts", "batches", "batch-005.json")
    json.dump(batch, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"wrote {out}: {len(mails)} mails")
    prev = os.path.join(ROOT, "drafts", "batch-005-preview.md")
    with open(prev, "w") as f:
        f.write("# batch 005 preview (bodies only, for mailcheck)\n\n---\n\n")
        for m in mails:
            f.write(f"## {m['outlet']} <{m['to']}>\nSubject: {m['subject']}\n\n{m['body']}\n\n\n")
    print(f"wrote {prev}")


if __name__ == "__main__":
    main()
