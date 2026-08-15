#!/usr/bin/env python3
"""Build drafts/batches/batch-005.json: 40 short mails to tree societies and blogs.

Hidde's instruction, 2026-08-15: "make the email short and also do a personal
question like and just to hear your personal opinion which tree do you think we
are missing of your city any personal tips".

So every mail is six short paragraphs at most: who he is and where he lives,
what the site does, the city page with one tree named, the personal question,
and out. No photo request, no correction request, no word about links. One ask,
and it is an opinion, which is the cheapest thing anyone can give.

Each recipient's city, tree count and named tree are read from the live city
files by hand into TARGETS below, so nothing in a mail is generated from a
pattern that could be wrong.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# lang -> (subject, body). {topic} {city} {n} {tree} {url}
T = {
    "en": (
        "Can you help me with ancienttrees.app? {topic}",
        """Hello,

My name is Hidde and I live in Baarn, a small town near Amsterdam. On ancienttrees.app I map the most remarkable old trees of cities, each one with its story and its exact spot, so people have a reason to go outside and stand in front of something old.

For {city} we publish {n} trees, {tree} among them:
{url}

What I would really like is your personal opinion: which tree do you think we are missing in {city}? Any personal tips are very welcome, then I can add them this week.

Thanks either way,
Hidde
ancienttrees.app""",
    ),
    "nl": (
        "Kun je me helpen met ancienttrees.app? {topic}",
        """Hallo,

Mijn naam is Hidde en ik woon in Baarn, een klein stadje vlakbij Amsterdam. Op ancienttrees.app breng ik de mooiste oude bomen van steden in kaart, elke boom met zijn verhaal en de precieze plek, zodat mensen een reden hebben om naar buiten te gaan en voor iets ouds te staan.

Van {city} staan er {n} online, waaronder {tree}:
{url}

Waar ik vooral benieuwd naar ben is jullie persoonlijke mening: welke boom missen wij volgens jullie in {city}? Persoonlijke tips zijn heel welkom, dan voeg ik ze deze week toe.

Bedankt alvast,
Hidde
ancienttrees.app""",
    ),
    "pt": (
        "Pode ajudar-me com o ancienttrees.app? {topic}",
        """Olá,

Chamo-me Hidde e vivo em Baarn, uma pequena cidade perto de Amesterdão. No ancienttrees.app mapeio as árvores antigas mais notáveis das cidades, cada uma com a sua história e o seu local exato, para que as pessoas tenham um motivo para sair e ficar diante de algo antigo.

De {city} publicamos {n} árvores, entre elas {tree}:
{url}

O que gostava mesmo de saber é a vossa opinião pessoal: que árvore acham que nos falta em {city}? Qualquer dica pessoal é muito bem-vinda, e posso acrescentá-la esta semana.

Obrigado de qualquer forma,
Hidde
ancienttrees.app""",
    ),
    "es": (
        "¿Me pueden ayudar con ancienttrees.app? {topic}",
        """Hola,

Me llamo Hidde y vivo en Baarn, un pueblo pequeño cerca de Ámsterdam. En ancienttrees.app cartografío los árboles viejos más notables de las ciudades, cada uno con su historia y su ubicación exacta, para que la gente tenga un motivo para salir y ponerse delante de algo antiguo.

De {city} publicamos {n} árboles, entre ellos {tree}:
{url}

Lo que más me interesa es su opinión personal: ¿qué árbol creen que nos falta en {city}? Cualquier consejo personal es muy bienvenido, y puedo añadirlo esta semana.

Gracias de todos modos,
Hidde
ancienttrees.app""",
    ),
    "ca": (
        "Em podeu ajudar amb ancienttrees.app? {topic}",
        """Hola,

Em dic Hidde i visc a Baarn, un poble petit a prop d'Amsterdam. A ancienttrees.app cartografio els arbres vells més notables de les ciutats, cadascun amb la seva història i el seu lloc exacte, perquè la gent tingui un motiu per sortir i plantar-se davant d'alguna cosa antiga.

De {city} en publiquem {n}, entre ells {tree}:
{url}

El que més m'interessa és la vostra opinió personal: quin arbre creieu que ens falta a {city}? Qualsevol consell personal és benvingut, i el puc afegir aquesta setmana.

Gràcies igualment,
Hidde
ancienttrees.app""",
    ),
    "it": (
        "Può aiutarmi con ancienttrees.app? {topic}",
        """Buongiorno,

Mi chiamo Hidde e vivo a Baarn, un paesino vicino ad Amsterdam. Su ancienttrees.app mappo gli alberi vecchi più notevoli delle città, ognuno con la sua storia e il punto esatto in cui si trova, così che le persone abbiano un motivo per uscire e stare davanti a qualcosa di antico.

Di {city} ne pubblichiamo {n}, tra cui {tree}:
{url}

Quello che mi interessa davvero è la vostra opinione personale: quale albero pensate che ci manchi a {city}? Ogni consiglio personale è molto gradito, e posso aggiungerlo questa settimana.

Grazie comunque,
Hidde
ancienttrees.app""",
    ),
}

B = "https://ancienttrees.app/"

# email, org, lang, topic (subject tail), city, n, tree, url slug, extra line
TARGETS = [
    # Netherlands
    ("info@vriendenvansonsbeek.nl", "Vrienden van Sonsbeek", "nl", "de bomen van Arnhem",
     "Arnhem", 4, "De Poortwachters bij de ingang van Zijpendaal", "arnhem", None),
    ("info@haagsehofjes.nl", "Stichting Haagse Hofjes", "nl", "de oude bomen van Den Haag",
     "Den Haag", 5, "de juttepeer in het Heilige Geesthofje aan de Paviljoensgracht", "the-hague", None),
    ("info@bomenstichtingdenhaag.nl", "Bomenstichting Den Haag", "nl", "de oude bomen van Den Haag",
     "Den Haag", 5, "de juttepeer in het Heilige Geesthofje", "the-hague", None),
    ("algemeen@kringvrienden.nl", "Kring Vrienden van 's-Hertogenbosch", "nl", "de bomen op de vestingwerken",
     "Den Bosch", 11, "de Weichselboom op de Parklaan, die in de oude stadsmuur wortelt", "den-bosch", None),
    ("info@ivn.nl", "IVN Natuureducatie", "nl", "de oude bomen van Nederlandse steden",
     "Nederland", 88, "de Heimanseik in de Plantage in Amsterdam", "netherlands", None),
    ("info@utrechtsebomenstichting.nl", "Utrechtse Bomenstichting", "nl", "de oude bomen van Utrecht",
     "Utrecht", 5, "de Uithof-linde", "utrecht", None),
    ("info@boomwachtersgroningen.nl", "Boomwachters Groningen", "nl", "de oude bomen van Groningen",
     "Groningen", 5, "de eiken op de sterpunten van het Sterrebos", "groningen", None),
    ("mail@bomenstichtingamsterdam.nl", "Bomenstichting afdeling Amsterdam", "nl", "de oude bomen van Amsterdam",
     "Amsterdam", 20, "de Heimanseik in de Plantage", "amsterdam", None),
    ("info@bomenbeschermingamsterdam.nl", "Bomen Bescherming Amsterdam", "nl", "de oude bomen van Amsterdam",
     "Amsterdam", 20, "de platanen van het Leidsebosje", "amsterdam", None),
    ("secretaris@bomenbondrijnland.nl", "Bomenbond Rijnland", "nl", "de oude bomen van Leiden",
     "Leiden", 6, "de Beets-beuk op de Burcht", "leiden", None),
    ("haarlemsebomenwachters@gmail.com", "Haarlemse Bomenwachters", "nl", "de oude bomen van Haarlem",
     "Haarlem", 4, "de beuk waar Lodewijk Napoleon zijn monogram in kerfde", "haarlem", None),
    ("info@bomenbieb.nl", "Bomenbieb", "nl", "bijzondere bomen in Nederland",
     "Nederland", 88, "de juttepeer in het Heilige Geesthofje in Den Haag", "netherlands", None),
    ("info@boommade.nl", "Boommade", "nl", "de oude bomen van Amsterdam",
     "Amsterdam", 20, "de vleugelnoot in het Wertheimpark", "amsterdam", None),
    # Belgium
    ("administratie@bomenbeterbeheren.org", "Bomen Beter Beheren vzw", "nl", "de oude bomen van Antwerpen",
     "Antwerpen", 10, "de zomerlinde van het Rivierenhof", "antwerp", None),
    ("info@bosplus.be", "BOS+", "nl", "de oude bomen van Brussel",
     "Brussel", 20, "de vijvereiken van het Ter Kamerenbos", "brussels", None),
    ("info@vvog.info", "Vereniging voor Openbaar Groen (VVOG)", "nl", "de oude bomen van Antwerpen",
     "Antwerpen", 10, "de bruine beuk bij de Sint-Willibrorduskerk in Berchem", "antwerp", None),
    ("info@wndln.be", "wndln (wandelblog Vlaanderen)", "nl", "een wandeling langs de oude bomen van Brussel",
     "Brussel", 20, "de vijvereiken van het Ter Kamerenbos", "brussels", None),
    # Portugal
    ("lisboa@quercus.pt", "Quercus, Núcleo Regional de Lisboa", "pt", "as árvores de Lisboa",
     "Lisboa", 33, "as oliveiras de Santo Amaro", "lisbon", None),
    ("setubal@quercus.pt", "Quercus, Núcleo Regional de Setúbal", "pt", "as árvores de Setúbal",
     "Setúbal", 10, "as seis araucárias do Largo José Afonso", "setubal", None),
    ("geral@lpn.pt", "Liga para a Protecção da Natureza (LPN)", "pt", "as árvores de Lisboa",
     "Lisboa", 33, "o dragoeiro da Ajuda", "lisbon", None),
    ("geral@icnf.pt", "ICNF", "pt", "as árvores de interesse público que publicamos",
     "Portugal", 95, "as oliveiras de Santo Amaro em Lisboa", "portugal",
     "O vosso registo de Arvoredo de Interesse Público está creditado nas nossas páginas. Uma coisa que encontrámos e que talvez queiram saber: três oliveiras de Setúbal têm 2009 na coluna da idade, que parece ser um ano e não um número de anos."),
    ("geral@wilder.pt", "Wilder", "pt", "as árvores antigas de Lisboa",
     "Lisboa", 33, "o ombú do Largo do Limoeiro", "lisbon", None),
    ("naturlink@naturlink.pt", "Naturlink", "pt", "um passeio pelas árvores de Setúbal",
     "Setúbal", 10, "a melaleuca que cresce de lado", "setubal", None),
    ("lisboa@secretmedianetwork.com", "Lisboa Secreta", "pt", "as árvores escondidas de Lisboa",
     "Lisboa", 33, "a figueira-da-borracha gigante da Mouraria", "lisbon", None),
    # Spain
    ("hola@aearboricultura.org", "Asociación Española de Arboricultura", "es", "los árboles viejos de Sevilla",
     "Sevilla", 20, "el ombú de La Cartuja", "seville", None),
    ("secretaria@aepjp.org", "Asociación Española de Parques y Jardines Públicos", "es", "los árboles del Retiro",
     "Madrid", 17, "el ahuehuete del Parterre", "madrid", None),
    ("bosquessinfronteras@bosquessinfronteras.com", "Bosques sin Fronteras", "es", "los árboles singulares de Valencia",
     "Valencia", 16, "El Titán, el ficus del Parterre", "valencia", None),
    ("info@plantipodes-am.cat", "Plantipodes-AM", "ca", "els arbres monumentals de Barcelona",
     "Barcelona", 46, "l'alzina del carrer de l'Encarnació", "barcelona", None),
    ("observatoriforestal@ctfc.cat", "Observatori Forestal de Catalunya", "ca", "els arbres monumentals de Barcelona",
     "Barcelona", 46, "els garrofers del Park Güell", "barcelona", None),
    # Italy
    ("sbi@unifi.it", "Società Botanica Italiana", "it", "gli alberi antichi di Firenze",
     "Firenze", 22, "il tasso del Micheli nel Giardino dei Semplici", "florence", None),
    ("segreteria@isaitalia.org", "ISA Italia", "it", "i platani dei Giardini Montanelli",
     "Milano", 18, "Il Sacerdote", "milan", None),
    ("italianostra@italianostra.org", "Italia Nostra", "it", "gli alberi delle ville storiche di Roma",
     "Roma", 29, "il ginkgo di Villa Sciarra", "rome", None),
    ("laboratoriocarteinregola@gmail.com", "Laboratorio Carteinregola", "it", "gli alberi di Roma",
     "Roma", 29, "Adonis, il platano della Valle dei Platani a Villa Borghese", "rome", None),
    ("info@villaghigi.it", "Fondazione Villa Ghigi", "it", "gli alberi antichi di Bologna",
     "Bologna", 12, "il cedro dell'Himalaya di Villa Ghigi", "bologna", None),
    ("amicitrotter@gmail.com", "Comitato Amici del Parco Trotter", "it", "la Quercia Rossa del Trotter",
     "Milano", 18, "La Quercia Rossa del Trotter", "milan", None),
    # UK and Ireland
    ("kwactiongroup@gmail.com", "Kings Weston Action Group", "en", "the old trees of Bristol",
     "Bristol", 5, "the Oak of Kings Weston", "bristol", None),
    ("info@treecouncil.org.uk", "The Tree Council", "en", "the old trees of London",
     "London", 23, "the Totteridge Yew", "london", None),
    ("admin@trees.org.uk", "Arboricultural Association", "en", "the old trees of London",
     "London", 23, "the Cheapside Plane", "london", None),
    ("trees@treecouncil.ie", "Tree Council of Ireland", "en", "the old trees of Dublin",
     "Dublin", 17, "the Hungry Tree on Constitution Hill", "dublin", None),
    ("admin@ancienttreeforum.org.uk", "Ancient Tree Forum", "en", "the veteran trees of Edinburgh",
     "Edinburgh", 15, "the Craigmillar Castle yews", "edinburgh", None),
]


def main():
    mails = []
    for email, org, lang, topic, city, n, tree, slug, extra in TARGETS:
        subj_t, body_t = T[lang]
        topic = topic[0].upper() + topic[1:]
        body = body_t.format(city=city, n=n, tree=tree, url=B + slug)
        if extra:
            lines = body.split("\n\n")
            lines.insert(3, extra)
            body = "\n\n".join(lines)
        mails.append({
            "to": email,
            "outlet": org,
            "subject": subj_t.format(topic=topic),
            "body": body,
        })
    batch = {
        "batch": "batch-005",
        "note": ("Hidde, 2026-08-15: short, and one personal question ('just to hear "
                 "your personal opinion which tree do you think we are missing of your "
                 "city, any personal tips'). Tree societies, city tree groups and tree "
                 "blogs only: the categories that answer and that can link. No photo "
                 "ask, no correction ask, no word about links."),
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
