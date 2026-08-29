#!/usr/bin/env python3
"""Build drafts/batches/batch-007.json.

Same letter as batch 006, including the mention line. What is new is where the
addresses came from: not another hand-scout, but scripts/outreach_scout.py.
--gaps named the 107 published cities with no contact of their own, and --find
read the addresses off the organisations' own contact pages.

Two directories did most of the work, and both are worth remembering. The
Bomenstichting publishes a page listing every local Dutch tree group, which
gave five cities that had nobody. ondalberi.it does the same per Italian
region, which gave Turin, Venice, Padua, Verona, Florence and Lucca.

Spain is back. Both Spanish associations answered batch 005 with an
out-of-office saying the secretariat was shut from 1 to 31 August, so those
mails were never read by anybody. They carry a resend_reason for exactly that.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_batch_006 import T, count, B  # same letter, same eight languages

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Spanish and Catalan were not in batch 006 because Spain was shut for August,
# so they are added here: batch 005's wording plus the mention line batch 006
# introduced.
T = dict(T)
T["es"] = ("¿Me pueden ayudar con ancienttrees.app? {topic}", """Hola,

Me llamo Hidde y estoy construyendo ancienttrees.app, una plataforma para árboles notables. Mi objetivo es entusiasmar a la gente con los árboles viejos y animarla a ir a verlos fuera.

Tenemos {n} árboles en {city} y tenía mucha curiosidad por saber si podrían echar un vistazo a ver si están bien:
{url}

Además me preguntaba: ¿qué árbol echan de menos personalmente en la web?

¡Cualquier ayuda sería muy apreciada!

Y si les parece que el sitio vale la pena, una mención en su página ayudaría enormemente a dar a conocer estos árboles.

Me interesa mucho su opinión sobre el proyecto.

Un saludo cordial,
Hidde""")
T["ca"] = ("Em podeu ajudar amb ancienttrees.app? {topic}", """Hola,

Em dic Hidde i estic construint ancienttrees.app, una plataforma per a arbres notables. El meu objectiu és engrescar la gent amb els arbres vells i animar-la a anar a veure'ls a fora.

De {city} en publiquem {n}, i tenia molta curiositat per saber si hi podríeu fer un cop d'ull per veure si són correctes:
{url}

A més em preguntava: quin arbre trobeu personalment a faltar al web?

Qualsevol ajuda seria molt apreciada!

I si us sembla que el web val la pena, una menció a la vostra pàgina ajudaria enormement a donar a conèixer aquests arbres.

M'interessa molt la vostra opinió sobre el projecte.

Cordialment,
Hidde""")


# email, org, lang, subject tail, city in that language, slug, resend_reason
TARGETS = [
 # Netherlands: five cities that had no contact at all, from the Bomenstichting's own directory
 ("bomenridders-leeuwarden@hotmail.com","Bomenridders Leeuwarden","nl","de oude bomen van Leeuwarden","Leeuwarden","leeuwarden",None),
 ("info@deventerbomenstichting.nl","Deventer Bomenstichting","nl","de oude bomen van Deventer","Deventer","deventer",None),
 ("info@zwollegroenstad.nl","Zwolse Bomenstichting","nl","de oude bomen van Zwolle","Zwolle","zwolle",None),
 ("stadsbomentilburg@gmail.com","Stichting Stadsbomen Tilburg","nl","de oude bomen van Tilburg","Tilburg","tilburg",None),
 ("info@trefpuntgroeneindhoven.nl","Trefpunt Groen Eindhoven","nl","de oude bomen van Eindhoven","Eindhoven","eindhoven",None),
 # Italy, from ondalberi.it's regional directories
 ("salviamoglialbericb@gmail.com","Comitato Salviamo gli Alberi Corso Belgio","it","gli alberi di Torino","Torino","turin",None),
 ("anto.visintin@gmail.com","Associazione Ecopolis Torino","it","gli alberi antichi di Torino","Torino","turin",None),
 ("info@amicoalbero.it","Associazione Amico Albero (Mestre)","it","gli alberi di Venezia","Venezia","venice",None),
 ("salvalalbero@gmail.com","Comitato Difesa Alberi e Territorio","it","gli alberi di Padova","Padova","padua",None),
 ("comitatoavatar@gmail.com","Comitato Avatar degli Alberi","it","gli alberi di Verona","Verona","verona",None),
 ("comitatovivifirenzeverde@gmail.com","Comitato Vivi Firenze Verde","it","gli alberi antichi di Firenze","Firenze","florence",None),
 ("siriana.lapietra@gmail.com","Comitato Verde Pubblico Firenze","it","il verde storico di Firenze","Firenze","florence",None),
 ("presidente@pubblicigiardini.it","Associazione Pubblici Giardini","it","gli alberi dei giardini storici","Firenze","florence",None),
 ("custodibarga@gmail.com","Custodi degli alberi e del suolo (Barga)","it","gli alberi antichi di Lucca","Lucca","lucca",None),
 ("info@ascuoladaglialberi.net","A scuola dagli alberi","it","gli alberi monumentali di Como","Como","como",None),
 ("unusualflorence@gmail.com","Associazione Unusual Address","it","gli alberi monumentali di Firenze","Firenze","florence",None),
 # Czechia, Poland, Denmark, France, UK, international
 ("info@koniklec.cz","ZO CSOP Koniklec","cs","stare stromy Prahy","V Praze","prague",None),
 ("biuro@salamandra.org.pl","Polskie Towarzystwo Ochrony Przyrody Salamandra","pl","drzewa Poznania","w Poznaniu","poznan",None),
 ("dn@dn.dk","Danmarks Naturfredningsforening","en","the old trees of Copenhagen","Copenhagen","copenhagen",None),
 ("vincent@pariszigzag.fr","Paris ZigZag","fr","les arbres remarquables de Paris","Paris","paris",None),
 ("exploringlondon@gmail.com","Exploring London","en","the old trees of London","London","london",None),
 ("info@gianttrees.org","Giant Trees Foundation","en","the biggest old trees we map","London","london",None),
 # Spain, held back from batch 006 because both were shut for August
 ("hola@aearboricultura.org","Asociacion Espanola de Arboricultura","es","los arboles viejos de Sevilla","Sevilla","seville",
  "Their secretariat was closed 1-31 August and answered batch 005 with an out-of-office, so nobody read that mail."),
 ("secretaria@aepjp.org","Asociacion Espanola de Parques y Jardines Publicos","es","los arboles del Retiro","Madrid","madrid",
  "Their office was closed for the whole of August and answered batch 005 with an out-of-office, so nobody read that mail."),
 ("bosquessinfronteras@bosquessinfronteras.com","Bosques sin Fronteras","es","los arboles singulares de Valencia","Valencia","valencia",
  "Sent during the Spanish August closure alongside two associations that answered with out-of-office replies."),
 ("info@plantipodes-am.cat","Plantipodes-AM","ca","els arbres monumentals de Barcelona","Barcelona","barcelona",
  "Sent during the Spanish August closure alongside two associations that answered with out-of-office replies."),
 ("observatoriforestal@ctfc.cat","Observatori Forestal de Catalunya","ca","els arbres monumentals de Barcelona","Barcelona","barcelona",
  "Sent during the Spanish August closure alongside two associations that answered with out-of-office replies."),
]


def main():
    mails = []
    for email, org, lang, topic, city, slug, resend in TARGETS:
        subj, body = T[lang]
        n = count(slug)
        few = n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14)
        m = {"to": email, "outlet": org,
             "subject": subj.format(topic=topic[0].upper() + topic[1:]),
             "body": body.format(n=n, city=city, url=B + slug,
                                 drzewa="drzewa" if few else "drzew",
                                 stromu="stromy" if few else "stromů")}
        if resend:
            m["resend_reason"] = resend
        mails.append(m)
    batch = {"batch": "batch-007",
             "note": ("Batch 006's letter, addresses found by scripts/outreach_scout.py rather than "
                      "by hand. Two directories did most of it: the Bomenstichting's list of local "
                      "Dutch tree groups and ondalberi.it's regional lists of Italian tree "
                      "committees. Spain returns after its August closure."),
             "status": "pending_approval", "mails": mails}
    json.dump(batch, open(os.path.join(ROOT, "drafts", "batches", "batch-007.json"), "w"),
              ensure_ascii=False, indent=1)
    with open(os.path.join(ROOT, "drafts", "batch-007-preview.md"), "w") as f:
        f.write("# batch 007 preview (bodies only, for mailcheck)\n\n---\n\n")
        for m in mails:
            f.write(f"## {m['outlet']} <{m['to']}>\nSubject: {m['subject']}\n\n{m['body']}\n\n\n")
    print(f"batch 007: {len(mails)} mails")


if __name__ == "__main__":
    main()
