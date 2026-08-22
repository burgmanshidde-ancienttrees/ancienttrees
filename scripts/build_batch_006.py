#!/usr/bin/env python3
"""Build drafts/batches/batch-006.json: 40 mails, Hidde's own text, eight languages.

Same letter as batch 005, which he wrote himself on 2026-08-15 and which is
the version that earned a 12 percent reply rate. Four languages are new here
(French, Polish, Czech, German) because batch 006 goes where we publish and
hold no contact at all: France is 83 trees and Poland, Czechia and Australia
were zero.

Who is on it, and why, from the measured record (scripts/outreach_stats.py):
small groups attached to ONE place answer, big institutions' general inboxes
do not. Gardens and palaces are 0 of 12; friends-of groups, conservancies and
city tree societies are where every useful reply came from. So this batch is
societies, blogs and friends-of groups, plus a handful of churches and parks
that hold one of our trees themselves.

Spain is deliberately absent: both Spanish associations answered batch 005
with an out-of-office saying the secretariat is shut from 1 to 31 August.
Writing again before September would burn the address for nothing.

Counts come from the live city files at build time.
"""
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://ancienttrees.app/"

T = {
 "nl": ("Kun je me helpen met ancienttrees.app? {topic}", """Hallo,

Mijn naam is Hidde en ik bouw aan ancienttrees.app, een platform voor opmerkelijke bomen. Mijn doel is om mensen enthousiast te maken over oude bomen en ze aan te moedigen om die buiten te gaan bekijken.

We hebben {n} bomen in {city} staan en ik was erg benieuwd of je een kijkje zou willen nemen of ze kloppen:
{url}

Daarnaast vroeg ik me af: welke boom mis jij persoonlijk op de site?

Elke hulp zou zeer gewaardeerd worden!

En als je de site de moeite waard vindt: een vermelding op jullie website zou enorm helpen om deze bomen onder de aandacht te brengen.

Ik ben erg benieuwd naar jouw mening over het project.

Met vriendelijke groet,
Hidde"""),
 "en": ("Can you help me with ancienttrees.app? {topic}", """Hello,

My name is Hidde and I am building ancienttrees.app, a platform for remarkable trees. My goal is to get people excited about old trees and to encourage them to go and see them outside.

We have {n} trees in {city} and I was really curious whether you would take a look at whether they are right:
{url}

I also wondered: which tree do you personally think is missing?

Any help would be much appreciated!

And if you think the site is worth it, a mention on your website would help enormously to get these trees noticed.

I would really like to hear your opinion on the project.

Best wishes,
Hidde"""),
 "fr": ("Pouvez-vous m'aider avec ancienttrees.app ? {topic}", """Bonjour,

Je m'appelle Hidde et je construis ancienttrees.app, une plateforme consacrée aux arbres remarquables. Mon but est de donner aux gens le goût des vieux arbres et l'envie d'aller les voir dehors.

Nous avons {n} arbres à {city} et j'étais très curieux de savoir si vous accepteriez d'y jeter un oeil pour voir si tout est juste :
{url}

Je me demandais aussi : quel arbre vous manque-t-il personnellement sur le site ?

Toute aide serait très appréciée !

Et si vous trouvez le site utile, une mention sur votre site aiderait énormément à faire connaître ces arbres.

Votre avis sur le projet m'intéresse beaucoup.

Cordialement,
Hidde"""),
 "pl": ("Czy możecie mi pomóc z ancienttrees.app? {topic}", """Dzień dobry,

Nazywam się Hidde i tworzę ancienttrees.app, platformę poświęconą niezwykłym drzewom. Chcę zarazić ludzi starymi drzewami i zachęcić ich, żeby poszli je zobaczyć na własne oczy.

Mamy {n} {drzewa} {city} i bardzo mnie ciekawi, czy zechcielibyście rzucić okiem, czy wszystko się zgadza:
{url}

Zastanawiałem się też: jakiego drzewa Waszym zdaniem brakuje na stronie?

Każda pomoc byłaby bardzo cenna!

A jeśli uznacie stronę za wartościową, wzmianka na Waszej stronie ogromnie pomogłaby tym drzewom zaistnieć.

Bardzo jestem ciekaw Waszej opinii o projekcie.

Z pozdrowieniami,
Hidde"""),
 "cs": ("Můžete mi pomoci s ancienttrees.app? {topic}", """Dobrý den,

jmenuji se Hidde a stavím ancienttrees.app, platformu o pozoruhodných stromech. Chci lidi nadchnout pro staré stromy a přimět je, aby se za nimi vypravili ven.

{city} máme {n} {stromu} a moc by mě zajímalo, jestli byste se podívali, zda je to tak správně:
{url}

Napadlo mě také: který strom vám na webu osobně chybí?

Jakákoli pomoc by mi hodně pomohla!

A pokud vám web přijde užitečný, zmínka na vašich stránkách by těmto stromům nesmírně pomohla.

Velmi mě zajímá váš názor na projekt.

S pozdravem,
Hidde"""),
 "de": ("Können Sie mir mit ancienttrees.app helfen? {topic}", """Guten Tag,

mein Name ist Hidde und ich baue ancienttrees.app, eine Plattform für bemerkenswerte Bäume. Mein Ziel ist es, Menschen für alte Bäume zu begeistern und sie dazu zu bringen, hinauszugehen und sie anzuschauen.

Wir haben {n} Bäume in {city} und mich würde sehr interessieren, ob Sie einmal nachsehen würden, ob sie stimmen:
{url}

Außerdem habe ich mich gefragt: welcher Baum fehlt Ihnen persönlich auf der Seite?

Über jede Hilfe würde ich mich sehr freuen!

Und falls Sie die Seite für nützlich halten: eine Erwähnung auf Ihrer Website würde enorm helfen, diese Bäume bekannt zu machen.

Ihre Meinung zu dem Projekt interessiert mich sehr.

Mit freundlichen Grüßen,
Hidde"""),
 "it": ("Può aiutarmi con ancienttrees.app? {topic}", """Buongiorno,

Mi chiamo Hidde e sto costruendo ancienttrees.app, una piattaforma per alberi notevoli. Il mio obiettivo è appassionare le persone agli alberi antichi e spingerle ad andare a vederli fuori.

Abbiamo {n} alberi a {city} ed ero molto curioso di sapere se potreste dare un'occhiata per vedere se sono giusti:
{url}

Inoltre mi chiedevo: quale albero pensate personalmente che manchi sul sito?

Ogni aiuto sarebbe molto apprezzato!

E se il sito vi sembra utile, una menzione sul vostro sito aiuterebbe moltissimo a far conoscere questi alberi.

Mi interessa molto la vostra opinione sul progetto.

Cordiali saluti,
Hidde"""),
 "pt": ("Pode ajudar-me com o ancienttrees.app? {topic}", """Olá,

Chamo-me Hidde e estou a construir o ancienttrees.app, uma plataforma para árvores notáveis. O meu objetivo é entusiasmar as pessoas pelas árvores antigas e incentivá-las a ir vê-las lá fora.

Temos {n} árvores em {city} e tinha muita curiosidade em saber se poderiam dar uma vista de olhos para ver se estão certas:
{url}

Além disso, perguntava-me: que árvore acham pessoalmente que falta no site?

Qualquer ajuda seria muito apreciada!

E se acharem o site útil, uma menção no vosso site ajudaria imenso a dar a conhecer estas árvores.

Gostava muito de saber a vossa opinião sobre o projeto.

Com os melhores cumprimentos,
Hidde"""),
}

# email, org, lang, subject tail, city as written in that language, slug
TARGETS = [
 # France: 83 trees published, no contact anywhere until now
 ("a_arbres@arbres.org", "Association A.R.B.R.E.S.", "fr", "les arbres de Paris", "Paris", "paris"),
 ("secretariat@sfa-asso.fr", "Societe francaise d'arboriculture", "fr", "les vieux arbres de Paris", "Paris", "paris"),
 ("lestetardsarboricoles@yahoo.fr", "Les tetards arboricoles", "fr", "les arbres de Bordeaux", "Bordeaux", "bordeaux"),
 ("contact@unjourdeplusaparis.com", "Un jour de plus a Paris", "fr", "les arbres remarquables de Paris", "Paris", "paris"),
 # Poland
 ("klubgaja@klubgaja.pl", "Klub Gaja", "pl", "drzewa Krakowa", "w Krakowie", "krakow"),
 ("biuro@eko.org.pl", "Fundacja EkoRozwoju", "pl", "drzewa Wrocławia", "we Wrocławiu", "wroclaw"),
 ("biuro@pracownia.org.pl", "Pracownia na rzecz Wszystkich Istot", "pl", "stare drzewa Krakowa", "w Krakowie", "krakow"),
 # Czechia
 ("stromroku@nadacepartnerstvi.cz", "Nadace Partnerstvi (Strom roku)", "cs", "stromy v Brně", "V Brně", "brno"),
 ("prazskestromy@seznam.cz", "Prazske stromy (Ales Rudl)", "cs", "pražské stromy", "V Praze", "prague"),
 ("info@arboristika.cz", "Arboristicka akademie", "cs", "staré stromy Prahy", "V Praze", "prague"),
 # Australia
 ("enquiries@trees.org.au", "Arboriculture Australia", "en", "the old trees of Melbourne", "Melbourne", "melbourne"),
 ("heritageservices@ntwa.com.au", "National Trust of Western Australia", "en", "the significant trees of Perth", "Perth", "perth"),
 ("conservation@nattrust.com.au", "National Trust of Australia (Victoria)", "en", "the significant trees of Melbourne", "Melbourne", "melbourne"),
 ("advocacy@nationaltrust.com.au", "National Trust of Australia (NSW)", "en", "the significant trees of Sydney", "Sydney", "sydney"),
 # UK and Ireland
 ("info@treeregister.org", "The Tree Register (TROBI)", "en", "the old trees of London", "London", "london"),
 ("bristoltreeforum@gmail.com", "Bristol Tree Forum", "en", "the old trees of Bristol", "Bristol", "bristol"),
 ("info@conservationfoundation.co.uk", "The Conservation Foundation (Morus Londinium)", "en", "London's old trees", "London", "london"),
 ("mail@avonwildlifetrust.org.uk", "Avon Wildlife Trust", "en", "the old trees of Bristol", "Bristol", "bristol"),
 ("info@treesforcities.org", "Trees for Cities", "en", "the old trees of London", "London", "london"),
 ("admin@totteridgechurch.org.uk", "St Andrew's Church, Totteridge", "en", "the Totteridge Yew", "London", "london"),
 ("info@stcuthbertschurch.org.uk", "St Cuthbert's Parish Church, Edinburgh", "en", "the old trees of Edinburgh", "Edinburgh", "edinburgh"),
 ("office@dendrology.org", "International Dendrology Society", "en", "the old trees of London", "London", "london"),
 # Germany
 ("ddg-web@web.de", "Deutsche Dendrologische Gesellschaft", "de", "die alten Bäume Berlins", "Berlin", "berlin"),
 ("kontakt@bmsgb.de", "Baumschutzgemeinschaft Berlin", "de", "die alten Bäume Berlins", "Berlin", "berlin"),
 # Italy
 ("info@apgi.it", "APGI, Associazione Parchi e Giardini d'Italia", "it", "gli alberi di Roma", "Roma", "rome"),
 ("info@villaserra.it", "Parco Storico di Villa Serra di Comago", "it", "gli alberi antichi di Genova", "Genova", "genoa"),
 ("comunicazione@villadurazzopallavicini.it", "Parco di Villa Durazzo Pallavicini", "it", "gli alberi antichi di Genova", "Genova", "genoa"),
 # Portugal
 ("cre.porto@ucp.pt", "100milarvores", "pt", "as árvores do Porto", "Porto", "porto"),
 ("contact@getlisbon.com", "GetLisbon", "pt", "as árvores de Lisboa", "Lisboa", "lisbon"),
 ("geota@geota.pt", "GEOTA", "pt", "as árvores de Lisboa", "Lisboa", "lisbon"),
 ("geral@aph.pt", "Associacao Portuguesa de Horticultura", "pt", "as árvores do Porto", "Porto", "porto"),
 ("geral@plantarumaarvore.org", "Plantar uma Arvore", "pt", "as árvores de Lisboa", "Lisboa", "lisbon"),
 ("comunicacao@quercus.pt", "Quercus (comunicacao nacional)", "pt", "as árvores de Portugal", "Portugal", "portugal"),
 # Netherlands and Belgium
 ("bureau@knnv.nl", "KNNV", "nl", "de oude bomen van Nederland", "Nederland", "netherlands"),
 ("info@artis.nl", "ARTIS", "nl", "de Heimanseik, de oudste boom van Amsterdam", "Amsterdam", "amsterdam"),
 ("secretariaatgroenesteeg@gmail.com", "Begraafplaats Groenesteeg, Leiden", "nl", "de oude bomen van Leiden", "Leiden", "leiden"),
 ("info@natuurpunt.be", "Natuurpunt", "nl", "de oude bomen van Antwerpen", "Antwerpen", "antwerp"),
 ("rivierenhof@provincieantwerpen.be", "Provincie Antwerpen, domein Rivierenhof", "nl", "de zomerlinde van het Rivierenhof", "Antwerpen", "antwerp"),
 ("middelheimmuseum@antwerpen.be", "Middelheimmuseum", "nl", "de oude bomen van Antwerpen", "Antwerpen", "antwerp"),
 ("woodwideweb.brussels@gmail.com", "woodwideweb.be", "nl", "de oude bomen van Brussel", "Brussel", "brussels"),
]

COUNTRY = {"portugal": "Portugal", "netherlands": "Netherlands"}


def count(slug):
    if slug in COUNTRY:
        n = 0
        for f in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
            d = json.load(open(f))
            if d["country"] == COUNTRY[slug]:
                n += len(d["trees"])
        return n
    return len(json.load(open(os.path.join(ROOT, "data", "cities", f"{slug}.json")))["trees"])


def main():
    mails = []
    for email, org, lang, topic, city, slug in TARGETS:
        subj, body = T[lang]
        n = count(slug)
        # 2-4 take the nominative plural, 5 and up the genitive: "4 drzewa"
        # but "16 drzew", "3 stromy" but "17 stromu". Getting this wrong is
        # the kind of mistake a native reader notices in the first line.
        few = n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14)
        mails.append({
            "to": email, "outlet": org,
            "subject": subj.format(topic=topic[0].upper() + topic[1:]),
            "body": body.format(n=n, city=city, url=B + slug,
                                drzewa="drzewa" if few else "drzew",
                                stromu="stromy" if few else "stromů"),
        })
    batch = {
        "batch": "batch-006",
        "note": ("Hidde's own letter from batch 005, in eight languages. Aimed at the "
                 "category the measured record says answers: societies, blogs and groups "
                 "attached to one place. France, Poland, Czechia and Australia had no "
                 "contact at all. Spain is deliberately absent until September, because "
                 "both Spanish associations answered with a holiday closure."),
        "status": "pending_approval",
        "mails": mails,
    }
    json.dump(batch, open(os.path.join(ROOT, "drafts", "batches", "batch-006.json"), "w"),
              ensure_ascii=False, indent=1)
    with open(os.path.join(ROOT, "drafts", "batch-006-preview.md"), "w") as f:
        f.write("# batch 006 preview (bodies only, for mailcheck)\n\n---\n\n")
        for m in mails:
            f.write(f"## {m['outlet']} <{m['to']}>\nSubject: {m['subject']}\n\n{m['body']}\n\n\n")
    print(f"batch 006: {len(mails)} mails")


if __name__ == "__main__":
    main()
