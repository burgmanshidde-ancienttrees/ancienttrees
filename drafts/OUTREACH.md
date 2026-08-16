# Outreach backlog: who to email, in order

Only Hidde sends these (hard rule 4: never speak as him, never contact anyone
as him). This file exists so a session can prepare drafts and he can spend ten
minutes at a time sending them.

**The reason this list is worth his time and not tokens:** every one of these
does two jobs at once. It asks permission for data we cannot otherwise use, and
it opens a relationship with exactly the kind of organisation that links to
sites using their data. Registers are also the cheapest trees this project can
get, roughly 0.4k tokens per tree against 27k for research, so a yes compounds
for months.

**Backlinks matter now.** Rome sits at position 17-19 with 77 impressions and
zero clicks on a 4,000-word page. That is an authority problem, not a content
problem, and more pages will not fix it. Caveat kept honest: Search Console's
API has no links endpoint, so we cannot measure our backlink count
automatically. The daily digest now prints external referrers (links somebody
actually clicked) and links to the Links report for a manual read.

## Tier 1, send first: data we cannot use without them

| # | Who | Email | Unlocks | Draft | Why now |
|---|---|---|---|---|---|
| 1 | Generalitat de Catalunya, arbres monumentals | arbresmonumentals.tes@gencat.cat | 302 monumental trees + 4,176 olives, per-trunk coordinates | `drafts/catalonia-permission.md` | **Barcelona is #1 in the rollout.** Blocked on nothing but a missing permission sentence: their metadata says only "otherRestrictions". |
| 2 | Woodland Trust, Ancient Tree Inventory | ancienttreeinventory@woodlandtrust.org.uk | 233,000 UK trees, the best register on earth | `drafts/woodland-trust-permission.md` | Unlocks London (currently gated) and Edinburgh. Their EULA forbids our use AND names its own appeal route. |
| 3 | Bomenstichting | info@bomenstichting.nl | ~15,000 Dutch trees with coordinates | `drafts/bomenstichting-permission.md` | Amsterdam is phase 1, and all 13 published Dutch cities deepen from one import. CC-BY-NC, so permission is the only route. |

## Tier 2: data questions rather than permission, still needs a human

| # | Who | What to ask | Unlocks |
|---|---|---|---|
| 4 | Bruxelles Environnement / opendata.bruxelles.be | Whether they can tell us which of the 582 remarkable trees stand on private ground. Their dataset carries no ownership field, which is why we took the map dots down under hard rule 10. | Restores 582 dots and makes Brussels publishable |
| 5 | SPW Wallonie, AHREM | What the three `DOMAINE` codes mean (13,007 / 6,985 / 253), and which records are the ones their own data model says are "positionnes aleatoirement" inside an address perimeter | 20,245 trees, the richest schema found anywhere. Licence is already fine (CC BY 4.0); only rule 10 blocks it. |
| 6 | GDOS Poland (CRFOP) | Confirmation of the data licence. Portal metadata reads CC0 but the licence-condition fields are empty and the site publishes CC BY-SA for its own content. | 117,474 tree monuments, the largest verified pool anywhere |
| 7 | Dipartimento Tutela Ambientale, Roma Capitale | Which of the two near-identical hackberries in the Lecceta at Villa Borghese is the one the citizen registry logs (we hold coordinates and a 4 m girth, they hold the ground). Contacts page: comune.roma.it/web/it/dipartimento-tutela-ambientale-uffici-e-contatti.page | Turns rom_022 from "one of two similar trunks" into a tree somebody can find. They manage the green around the Aranciera and Museo Bilotti, so they are also the right address for anything else in Villa Borghese. |
| 8 | Ufficio Ville, Sovrintendenza Capitolina | The historic villas' own tree knowledge: Borghese, Torlonia, Celimontana, Doria Pamphilj and Sciarra all carry trees we publish. Contacts page: comune.roma.it/web/it/sovrintendenza-capitolina-uffici-e-contatti.page | Rome is our deepest page (24 trees) and takes zero clicks; a municipal link is worth more here than a 25th tree. |

**Both Rome offices came from the Sovrintendenza's own reply of 2026-08-12**,
which answered our question about two trees and named these two as the
competent offices. That reply is a warm thread, not a cold approach: the
first move is `drafts/reply-roma-sovrintendenza.md`, and only if it stalls do
these become separate letters.

## Tier 3: backlinks. Named targets, each with a reason to write

Hidde, 2026-08-08: three addresses is not an outreach programme. Correct, and
the first version of this file listed categories rather than people. The list
below names actual organisations. Addresses marked "find" need one lookup on
their own site; nothing here is invented, because a wrong address is worse than
no address.

**The principle that decides who is on this list.** A cold email asking for a
link is spam and converts near zero. An email telling an organisation that we
have written about THEIR trees, credited them, and linked to them is a
different message entirely, and it is true. So every target below is somewhere
we already feature, cite or credit. That is also why this list is finite: when
we run out of organisations we have a real reason to write to, we stop.

### 3a. The nine gardens and parks that now have their own page

Each of these has a page on our site about their trees, with photographs,
directions and their own history. That page is the email. Ask nothing except
whether they would like to see it, and mention we link to them.

| Organisation | City | Address |
|---|---|---|
| Royal Botanic Garden Edinburgh | Edinburgh | info@rbge.org.uk |
| Real Orto Botanico di Napoli | Naples | robnap@unina.it (site moved to ortobotaniconapoli.it) |
| Giardino dei Semplici (Museo di Storia Naturale, Univ. Firenze) | Florence | segrmuseo@unifi.it |
| York Museums Trust (Museum Gardens) | York | amy.cope@ymt.org.uk (PR officer) |
| Bruxelles Environnement (Parc d'Egmont) | Brussels | info@environnement.brussels |
| Reggia di Caserta (Giardino Inglese) | Caserta | re-ce@cultura.gov.it |
| Schloss Nymphenburg (Bayerische Schlösserverwaltung) | Munich | presse@bsv.bayern.de |
| Parco del Valentino (Città di Torino, Verde Pubblico) | Turin | form only: serviziweb.comune.torino.it/nuova-richiesta-itsm |
| Parque del Retiro (Ayuntamiento de Madrid) | Madrid | parqueshistoricos@madrid.es (historic-parks unit, covers the Retiro) |

### 3b. The registers we cite and credit

We use their data and name them on the page. Several run a "who uses our data"
section, which is the most natural link on the internet.

| Organisation | Country | Address |
|---|---|---|
| RAMI, Registro degli Alberi Monumentali Italiani | Italy | Difor4@masaf.gov.it (the office the RAMI page names) |
| ICNF (Arvoredo de Interesse Publico) | Portugal | geral@icnf.pt |
| Ajuntament de Barcelona, arbrat viari | Spain | permisos_masu@bcn.cat (only published address of Parcs i Jardins) |
| Stadt Wien, data.wien.gv.at | Austria | post@ma41.wien.gv.at (verify) |
| Ville de Paris, Direction des Espaces Verts | France | form only: paris.fr/pages/contact-232 |
| Senatsverwaltung Berlin (Naturdenkmale) | Germany | schutzgebiete@senmvku.berlin.de (the Naturdenkmale desk itself) |
| Govern de les Illes Balears, SITIBSA | Spain | find on caib.es |
| Generalitat Valenciana, ICV | Spain | find on icv.gva.es |

### 3c. Tree organisations and societies

The audience overlap is total and there is no commercial conflict.

| Organisation | Country | Why they would care |
|---|---|---|
| Bomenstichting | NL | Also tier 1; the register ask and the link ask are one email |
| ~~Monumental Trees~~ | intl | **DO NOT SEND (Hidde, 2026-08-09): we are their direct competitor** ("using it is miserable, that is the entire opening", COMPETITION.md). We currently operate quietly within the fact-verification zone their own disclaimer permits, needing nobody's permission; a mail invites them to look at us and close that zone. Nothing to win, our best verification channel to lose. Revisit only from strength, or never. |
| The Tree Register (TROBI) | UK | Champion-tree records; independent of the Woodland Trust |
| European Tree Worker / EAC | EU | Professional arborists across our whole map |
| Arbor Day Foundation | US | Relevant when the US cities open |
| Ancient Yew Group | UK | We publish yews across Europe; a narrow, passionate audience |

### 3d. The local papers that already ran the story

Each of these published a survey of their city's monumental trees, which we
verified against and credit. A follow-up ("a Dutch site mapped your city's
trees and used your survey") is a real story for them, not a favour.

| Paper | City | Note |
|---|---|---|
| Il Piccolo | Trieste | Their survey of 48 monumental trees gave us ages no register carries |
| PadovaOggi | Padua | Their reporting confirmed the last Prato della Valle plane died in 2011 |
| Local press in Setubal | Setubal | The parish's own tree route corroborated nine of our ten entries |

### 3e. The tree sites, blogs and communities we cite as sources

Computed 2026-08-08 from `verified_sources` across all 766 published trees:
every one of these is cited on our pages today, so the email is true on
arrival ("we verified our [city] trees against your work and cite you").
Citation counts included so the strongest hook goes first.

| Site | Language/Country | Cited | Hook |
|---|---|---|---|
| baumkunde.de | DE | 11 trees, 3 cities | German tree database; we cite their records in Berlin, Munich, Vienna coverage |
| bomenbieb.nl | NL | 8 trees, 4 cities | The Bomenstichting's own tree library; rides with the tier-1 email |
| prazskestromy.cz | CZ | 8 trees | Prague's memorial-trees site, run by one dedicated author |
| jardinessinfronteras.com | ES | 9 trees, 4 cities | Spanish garden-history blog, cited across four of our Spanish cities |
| woodwideweb.be | BE | 7 trees | Belgian remarkable-trees site; exactly our audience |
| 100milarvores.pt | PT | 7 trees | Portuguese tree-mapping project; a natural mutual link |
| getlisbon.com | PT | 7 trees | Lisbon city blog whose tree pieces we verified against |
| unjourdeplusaparis.com | FR | 6 trees | Paris city blog, cited on our Paris trees |
| jardinesdelaoliva.wordpress.com | ES | 6 trees, 2 cities | Spanish garden blog |
| hortusleiden.nl | NL | 7 trees | Hortus botanicus Leiden; their trees have our pages |
| heritagetrees.nparks.gov.sg | SG | 7 trees | Singapore's official Heritage Trees register we cite |
| atlasobscura.com | intl | 6 trees, 5 cities | Their entries corroborate ours; community submission is also a channel |
| wastemagazine.es | ES | 7 trees | Spanish nature magazine |

### 3f. More parks departments and registers we cite (extends 3b)

| Organisation | City/Region | Cited |
|---|---|---|
| NYC Parks (Great Trees) | New York | 13 trees |
| Regione Campania, foreste | Campania | 16 trees, 2 cities |
| Regione Lazio | Rome | 10 trees |
| Comune di Roma | Rome | 10 trees |
| Camara Municipal do Porto, ambiente | Porto | 13 trees |
| Uniao das Freguesias de Setubal | Setubal | 10 trees |
| Onroerend Erfgoed | Flanders | 9 trees |
| City of Helsinki | Helsinki | 8 trees |
| Ville de Geneve | Geneva | 6 trees |
| Ayuntamiento de Zaragoza | Zaragoza | 7 trees |
| Comune di Milano | Milan | 6 trees |
| Museo di Capodimonte | Naples | 6 trees |

### What to send them, and it is not a template

One short email each, in the local language where you can, saying what the site
is, that we have written about their trees or used their data, and that we link
to them. Ask whether they would like to look. Do not ask for a link in the first
email: the page itself is the ask, and an organisation that likes it will link
without being told to.

Rough order of value: 3a first (we have the strongest, most flattering hook and
a page to show), then 3b and 3f, then 3c, then 3e, then 3d.

## Tier 4: press. One story, sent one desk at a time

Added 2026-08-08 on Hidde's instruction ("zorg dat we de juiste content klaar
hebben staan om persbureaus mee te benaderen"). The content now exists:
`/collections/europes-oldest-trees-are-immigrants`, built on a finding that
survives checking, four in ten of the ancient trees we map in European cities
are not European species. The pitch, in English and Dutch, is
`drafts/press-pitch.md`. Every figure regenerates with
`python3 scripts/press_numbers.py`, and the spreadsheet a desk will ask for
comes from the same script with `--csv`.

**Not a wire service, and never a blast.** A press agency wants an exclusive or
a wire-ready fact; a small project has neither the reach nor the news hook for
that yet. What works at this size is one desk at a time, in this order:

| Order | Who | Why them |
|---|---|---|
| 1 | One national outlet that runs long nature pieces | The story is a feature, not a news item, and needs 800 words to land |
| 2 | City desks of the cities in the story | Seville, Paris, London, Palermo, Valencia, Berlin all have a named tree in it, and a local tree is a local story |
| 3 | Tree, garden and heritage press | Smallest reach, highest hit rate, and the audience is exactly ours |
| 4 | Only then, if one of the above ran it | A piece that already exists elsewhere is what makes a wire desk answer |

Addresses are deliberately not listed yet: the right desk is a named journalist
who has written about trees or cities recently, and that is a lookup worth
doing per outlet at the moment of sending rather than a list that goes stale.

## Never mail the same address twice unless somebody meant it (Hidde, 2026-08-16)

The rule, and it is enforced in `scripts/outreach_send.py` rather than
remembered: **an address that has ever been mailed is refused.** To write to it
again on purpose, the mail in the batch file carries a `resend_reason` of at
least five words saying why. A bare "follow-up" is refused too, because the
point is that somebody thought about it rather than typed past a guard. The
reason is stored with the send, so the log answers "why did this address get two
mails" without anybody reconstructing it.

Two things make the guard real, and it failed on both before today:

1. **It only knows what is in `data/outreach-sent.json`.** Mail Hidde sends by
   hand used to live only in the table above, which no script reads, so on
   2026-08-16 a batch put the Woodland Trust back on the list eight days after
   his own ask. **Anything sent by hand goes in that file too.**
2. **There was no door.** Until today a deliberate follow-up was skipped exactly
   like an accidental duplicate, which meant the only way to send one was to
   defeat the guard. A rule with no legitimate exception gets worked around.

## De verzendmachine is blijvend (vastgelegd 2026-08-09 op Hidde's verzoek)

Elke sessie kan mailen namens Hidde, en zo werkt het, blijvend:

1. **De credentials staan klaar** in `~/.ancienttrees-mail.env` op zijn
   machine (Gmail app-wachtwoord, buiten de repo). Een sessie draait
   `source ~/.ancienttrees-mail.env` (per sessie opnieuw, het bestand zelf is
   blijvend) en `scripts/outreach_send.py` doet de rest. **Machinegebonden,
   bewust**: een sessie die het bestand niet kan zien draait niet op Hidde's
   Mac en hoort de sleutels NIET te krijgen; geen enkele sessie vraagt hem
   ooit het wachtwoord in een chat te plakken.
2. **Het mandaat-patroon**: de sessie schrijft of toont de batch, Hidde leest
   en zegt "verstuur" (of "goedgekeurd"), de sessie zet de batch-status om en
   verstuurt waar hij bij is. Dat ene woord per batch is geen bureaucratie
   maar het ontwerp: de mails dragen zijn naam, dus hij heeft de tekst gezien
   (hard rule 4). Proven flow: batch 001, 2026-08-08, vijf mails.
3. **De vangrails zitten in de code** en gelden voor elke sessie: geen
   verzending zonder status `approved_by_hidde`, nooit tweemaal hetzelfde
   adres (data/outreach-sent.json), een dagcap, elke verzending gelogd in dit
   bestand.

   **De dagcap ging op 2026-08-09 van tien naar veertig**, op Hidde's woord:
   "vergeet mijn script we mogen zoveel mensen mailen als we zelf bedenken dat
   goed is". Hij is bewust een getal gebleven en niet oneindig, en de reden is
   niet voorzichtigheid maar zijn eigen postvak: deze mails gaan vanaf zijn
   adres, en een uitbarsting koude mail die bounct of als spam wordt gemarkeerd
   beschadigt de reputatie van het domein. Daarna belandt zijn eigen post ook
   in spamfolders, en dat is traag te herstellen en onzichtbaar tot het al
   gebeurd is. De cap houdt een bug tegen die dezelfde lijst vijftig keer
   mailt; hij houdt Hidde niet tegen. Wil een sessie er meer, dan zet ze
   `OUTREACH_DAILY_CAP` voor die run, wat een bewuste handeling is in plaats
   van een vergissing.
4. **Wat een sessie nooit doet**: versturen zonder zijn woord voor die batch,
   en de nachtruns versturen helemaal niets. Wil Hidde ooit volautomatisch
   (zonder tekst-inzage per batch), dan is dat een expliciete nieuwe
   beslissing en wisselt de ondertekening naar "Ancient Trees".

## The opening line (Hidde, 2026-08-10)

**Open with a plain compliment and nothing else.** He read batch 003 and called
the openings AI-generated. The offending shape was a compliment with an
analytical justification bolted on:

> Your yearbook archive is the reason several Copenhagen trees on our site could
> be published rather than left as rumours. For a city with no single
> monumental-tree register, a society that has been recording measurements for
> decades is the only continuous source there is.

His instruction, verbatim: **"Just open with - i love your ... tree!"**, then
sharpened the same day into the line to actually use:

> **I found this tree of yours online and think it's a remarkable tree! My name
> is Hidde...**

No thesis, no "which is interesting because", no explaining why the compliment
is deserved. Every fact, number and piece of reasoning waits until after the
ask. An opening that justifies itself reads as machine-written, because
explaining a compliment is exactly what a machine does when it tries to sound
sincere.

And his version does something mine did not: it is **honest about how we know
the tree**. "The elms flanking the Shaw Memorial are among the very few of that
generation still standing" implies a familiarity we do not have; we researched
it from a distance and have never stood in front of it. "I found this tree of
yours online" says exactly what happened, which is also what every tree page
already tells readers at the bottom ("This page was researched from a
distance"). Writing to the one person who HAS stood in front of it, pretending
otherwise is both dishonest and transparent.

Batches 002 and 003 went out before this was recorded, so 24 mails carry the old
opening. Nothing to do about those; from batch 004 the first line is one plain
sentence.

## The subject line (Hidde, 2026-08-10)

Same move as the opening: from "look what I know about you" to "I need your
help". His instruction: **"Can you help me with building ancienttrees.app or
something."**

So the subject asks for help in plain words rather than announcing a finding.
What it replaces:

| Sent in batch 003 | From batch 004 |
|---|---|
| Six of the ten Boston trees we publish are yours, and none has a photograph | Can you help me with ancienttrees.app? Your Arboretum trees |
| Your yearbook archive is why Copenhagen has a page at all | Can you help me with ancienttrees.app? Copenhagen's old trees |

The trade-off, recorded rather than argued: a bare "Can you help me with
ancienttrees.app?" is the most human and the least openable, because a parks
officer with three hundred unread mails cannot tell whether it concerns him.
Three or four words naming his own tree or city fix that without costing the
tone. If Hidde prefers it bare, it goes bare: it carries his name.

## Rules for all of it

- **Drafts only from me, always.** He sends, from his own address.
- **Honest about the paid tier**, every time. Their licences define commercial
  to include indirect and deferred gain, so a permission won on vagueness dies
  the day the site charges for anything.
- **Two commitments we can make truthfully**, and should: publicly accessible
  trees only, and we honour any location a source deliberately withholds.
- **Offer something back**: a prominent link to their register or garden. It is
  true, it costs nothing, and it is the reciprocity that makes a link natural.
- **Never mass-send.** Each of these is worth writing individually, and the
  moment it reads like a template it stops working and starts costing goodwill.

## Addresses found 2026-08-08

The contact scout read every address below off the organisation's own site
(full detail per target in data/research/outreach-contacts.json: where it was
found, what was form-only, what was Cloudflare-blocked). 24 of 28 have a real
published email; 4 are form-only. Two cautions: Milano only publishes a PEC
address (Transizioneambientale@pec.comune.milano.it), and PEC often rejects
ordinary Gmail, so use the city's contact form if it bounces; and
monumentaltrees.com is Cloudflare-walled, so its contact form needs a normal
browser visit.

Remaining addresses in one place: NYC Parks pressoffice@parks.nyc.gov, Porto
geral@cm-porto.pt, Roma dipartimento.ambiente@comune.roma.it, TROBI
membership@treeregister.org, Ancient Yew Group info@treeregister.org (same
family), Arbor Day elennemann@arborday.org, baumkunde webmaster@baumkunde.de,
prazskestromy prazskestromy@seznam.cz, woodwideweb
woodwideweb.brussels@gmail.com, 100milarvores cre.porto@ucp.pt, getlisbon
contact@getlisbon.com, unjourdeplusaparis contact@unjourdeplusaparis.com,
bomenbieb info@bomenbieb.nl, jardinessinfronteras form-only.

## Log

Record sends and replies here so nobody re-sends and nobody waits on a reply
that already came. Machine sends are also in data/outreach-sent.json, which the
send script enforces dedup against. Batch 001 success test: one reply or
placement within two weeks proves the channel; zero is also an answer. Follow
up politely after three or four weeks, never sooner.

**Batch 001 passed its own test, and not the way it was aimed (2026-08-12).**
DUIC did not run the Utrecht pitch. Else Marie Vonk forwarded it to Oud-Utrecht,
the city's historical society, where Piet van Dijck took it up for the series
"Op pad met Oud-Utrecht", planned for the first half of 2027. Two things worth
carrying into the next press batch. A local paper's editor forwarding a mail to
the people who actually write about the city is a better outcome than a filler
piece, so a pitch to a regional desk should be written so it survives being
passed on, which this one was: it named one tree, one date and one link. And a
placement can land nine months out, which means the press lane is measured over
quarters and cannot be judged on a fortnight of Search Console.


**Batch 002-pt, 2026-08-09.** Twelve mails, Portugal only, in Hidde's frame: a
compliment, what the site is for, then an ask for photographs and for the tree we
missed. Not one word about coverage or a link. Deliberately a test batch of twelve
rather than the whole list: the text is unproven and there is no second first
impression with the same organisation. If a reply comes, the reply is where a link
may arise naturally, after we have used their help and credited them.


**Batch 003-photo-gap, 2026-08-10.** Twelve mails, chosen by the measured gap rather
than by list order. That morning's count showed the top-25 essentially complete on tree
count (only Chicago short, by four) and 94 photographs short, with the whole shortfall in
six cities: Boston 10 of 10 missing, Budapest 12 of 12, Copenhagen 13 of 13, Chicago 6 of
6, Washington DC 13 of 14, New York 15 of 20. Commons has nothing for these, proven by two
viewing passes that judged 35 candidates and approved none. So these go to the people who
hold the trees. Budapest has no verified contact yet and is the obvious hole in this batch.


**Batch 004, 2026-08-10.** Twenty-eight mails, the first in the voice Hidde settled that
afternoon: subject asks for help, opening says we found the tree online and think it is
remarkable. Templated rather than hand-written, which is a real cost and the honest trade
at this size: twelve are worth writing by hand, a hundred and thirty are not, and the
alternative to a template is not sending. It earns its keep by naming each recipient's own
trees and their own photograph gap, and by writing in their language with their city's own
name. Two defects were caught in the dry run and fixed before sending: the German mails
said 'Vienna' instead of 'Wien', and the ownership matcher told Schloss Schoenbrunn it
owned the sequoias of Poetzleinsdorfer Schlosspark because 'schloss' appears in both. Only
why_them is trusted for ownership now. 106 contacts remain; the daily cap is 40.

| Date | To | Ask | Status |
|---|---|---|---|
| 2026-08-10 | Schloss Schönbrunn Kultur- und Betriebsges.m.b.H., info@schoenbrunn.at | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Österreichische Bundesgärten (Bundesgärten Wien, Sch, office@bundesgaerten.at | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Stiftung Preußische Schlösser und Gärten Berlin-Bran, generaldirektion@spsg.de | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Conservatoire et Jardin botaniques de la Ville de Ge, info.jbg@geneve.ch | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Trees New York, info@treesny.org | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | American Forests, info@americanforests.org | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Schloss- und Gartenverwaltung Nymphenburg (Bayerisch, sgvnymphenburg@bsv.bayern.de | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Gartenverwaltung Englischer Garten (Bayerische Schlö, gvenglischergarten@bsv.bayern.de | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Baureferat Gartenbau, Landeshauptstadt München, Gartenbau@muenchen.de | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | MA 42 Wiener Stadtgärten, post@ma42.wien.gv.at | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Grün Berlin GmbH, service@gruen-berlin.de | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Schutzgemeinschaft Deutscher Wald (SDW), Bundesverba, info@sdw.de | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Kuratorium Baum des Jahres / Dr. Silvius Wodarz Stif, info@baum-des-jahres.de | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | City of Boston Parks and Recreation Department, parks@boston.gov | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Svenska Trädföreningen (Swedish Arboricultural Assoc, info@tradforeningen.org | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Bymiljøetaten, Oslo kommune (Oslo Agency for Urban E, postmottak@bym.oslo.kommune.no | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Vereinigung Schweizerischer Stadtgärtnereien und Gar, info@vssg.ch | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Baumkunde.de, webmaster@baumkunde.de | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Baumportal.de (Jowaca), nature@jowaca.de | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Suomen luonnonsuojeluliiton Uudenmaan piiri (Finnish, uusimaa@sll.fi | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Museu de Ciencies Naturals de Barcelona (Jardi Botan, museuciencies@bcn.cat | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Institut Botanic de Barcelona (IBB, CSIC-CMCNB), infoibb@ibb.csic.es | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Reggia di Caserta, re-ce@cultura.gov.it | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Museo e Real Bosco di Capodimonte, mu-cap@cultura.gov.it | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Orto Botanico di Roma (Sapienza Universita di Roma), info-ortobotanico@uniroma1.it | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | RAMI - Il Registro degli Alberi Monumentali d'Italia, info@ilregistrodeglialberi.it | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Istituto Italiano di Studi Germanici (Villa Sciarra), lupoli@studigermanici.it | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Musei in Comune Roma (Sovrintendenza Capitolina, Vil, info@museiincomuneroma.it | Photos, corrections, the tree we missed, batch 004 | **sent** |
| 2026-08-10 | Arnold Arboretum, arbweb@arnarb.harvard.edu | Photos + accession records; 6 of Boston's 10 trees are theirs, all 10 photo-less, batch 003-photo-gap | **sent** |
| 2026-08-10 | Friends of the Public Garden, info@friendsofthepublicgarden.org | Photos + which of the Common's four old elms is which, batch 003-photo-gap | **sent** |
| 2026-08-10 | Central Park Conservancy, press@centralparknyc.org | Photos; 8 of our 20 New York trees are in the Park, 15 without an image, batch 003-photo-gap | **sent** |
| 2026-08-10 | Green-Wood Cemetery, info@green-wood.com | Photos of the sassafras pair + what we missed on their grounds, batch 003-photo-gap | **sent** |
| 2026-08-10 | Brooklyn Botanic Garden, visitorservices@bbg.org | Photos of the Kansas hawthorn + which of their veterans we missed, batch 003-photo-gap | **sent** |
| 2026-08-10 | Casey Trees, conservation@caseytrees.org | Photos; 13 of our 14 Washington trees have none, and they measure champions, batch 003-photo-gap | **sent** |
| 2026-08-10 | Rock Creek Conservancy, info@rockcreekconservancy.org | Photos of Montrose Park and Dumbarton Oaks Park, batch 003-photo-gap | **sent** |
| 2026-08-10 | Dumbarton Oaks Park Conservancy, info@dopark.org | Photos of the beech grove + is the grove's story right, batch 003-photo-gap | **sent**; holding reply 2026-08-13 from Sara Carlson (Fellow): interesting, will circle back with answers. No action needed until they do; a positive first touch from batch 003 |
| 2026-08-10 | The Morton Arboretum, trees@mortonarb.org | Which Chicago trees are we missing; six is fewer than any other big city, batch 003-photo-gap | **sent** |
| 2026-08-10 | Chicago Park District, play@chicagoparkdistrict.com | Photos of the Wooded Island oaks + which park veterans we missed, batch 003-photo-gap | **sent** |
| 2026-08-10 | Dansk Dendrologisk Forening, formand@dendron.dk | Which Copenhagen tree are we missing; their yearbook already corroborated ours, batch 003-photo-gap | **sent** |
| 2026-08-10 | Statens Naturhistoriske Museum, snm@snm.ku.dk | Photos + the Palm House cycad's real age from their accession records, batch 003-photo-gap | **sent** |
| 2026-08-09 | Fundação Mata do Buçaco, gabpresidencia@fmb.pt | Photos + missed trees, all 6 Buçaco trees theirs, 5 without a photo, batch 002-pt | **sent** |
| 2026-08-09 | Parques de Sintra, info@parquesdesintra.pt | Photos + corrections, Pena and Monserrate, the Monserrate pohutukawa has none, batch 002-pt | **sent** |
| 2026-08-09 | Jardim Botânico do Porto, jardimbotanico@mhnc.up.pt | Photos + corrections, 5 Porto trees inside their garden, batch 002-pt | **sent** |
| 2026-08-09 | Jardim Botânico da Ajuda, botanicoajuda@isa.ulisboa.pt | Photos + the Ajuda dragon tree's age, which only they can settle, batch 002-pt | **sent** |
| 2026-08-09 | Dias com árvores (blog), dias.com.arvores@sapo.pt | Which Porto tree are we missing; closest thing in Portugal to what we do, batch 002-pt | **sent** |
| 2026-08-09 | Quercus Núcleo do Porto, porto@quercus.pt | Photos, 12 of our 17 Porto trees have none, batch 002-pt | **sent** |
| 2026-08-09 | Porto Ambiente, geral@portoambiente.pt | Photos, Palácio de Cristal gardens they maintain, batch 002-pt | **sent** |
| 2026-08-09 | Quinta da Regaleira, info.regaleira@cultursintra.pt | Which tree inside their walls deserves a place; we publish none, batch 002-pt | **sent** |
| 2026-08-09 | Paço dos Duques, geral@pacoduques.pt | Photos + what Guimarães is missing; 4 trees feels thin for that city, batch 002-pt | **sent** |
| 2026-08-09 | Junta de Freguesia da Estrela, geral@jf-estrela.pt | Photos, 6 Lisbon trees in their parish, batch 002-pt | **sent** |
| 2026-08-09 | Amigos do Jardim Botânico de Lisboa, amigosdobotanico@gmail.com | Which Lisbon tree are we missing; they run tree walks there, batch 002-pt | **sent** |
| 2026-08-09 | Sociedade Portuguesa de Botânica, spbotanica@gmail.com | Confirm two species identifications we are unsure of, batch 002-pt | **sent** |
| 2026-08-08 | Het Parool, redactie@parool.nl | Amsterdam local pitch (Heimanseik + Plantage walk), batch 001 | **sent** |
| 2026-08-08 | DUIC, redactie@duic.nl | Utrecht local pitch (Uithof linden), batch 001 | **sent**, forwarded by DUIC to Oud-Utrecht; Piet van Dijck replied 2026-08-12 that he is writing it up for "Op pad met Oud-Utrecht", planned first half of 2027. Hidde's reply (drafts/reply-oud-utrecht.md) **sent 2026-08-14** |
| 2026-08-08 | Brabants Dagblad, stadsredactie@bd.nl | Den Bosch local pitch (Bastion Oranje maple), batch 001 | **sent**; Roel replied 2026-08-12 (interested, two objections), Hidde's follow-up (drafts/reply-brabants-dagblad.md) **sent 2026-08-14** after all 11 trees got recognition lines and the Weichselboom photo |
| 2026-08-08 | Haarlems Dagblad, stadsredactie@haarlemsdagblad.nl | Haarlem local pitch (Lodewijk Napoleon beech), batch 001 | **sent** |
| 2026-08-08 | De Gelderlander, redactie@gelderlander.nl | Arnhem local pitch (De Poortwachters), batch 001 | **sent** |
| 2026-08-08 | Generalitat de Catalunya, arbresmonumentals.tes@gencat.cat | Permission to show Catalonia's monumental trees; unlocks Barcelona's trees AND its photos | **sent**, no reply yet |
| 2026-08-16 | National Trust of Western Australia, trust@ntwa.com.au | Licence for the Significant Tree Register (PDF, 24 Perth-metro entries, no coordinates); Perth is rank 7 | **sent** |
| 2026-08-16 | Ontario Urban Forest Council, info@oufc.org | Licence for the Ontario Heritage Tree map; unlocks the 27 public Toronto leads (Toronto is rank 1). Forests Canada owns the layer but publishes no general address, so the mail offers to be redirected | **sent** |
| 2026-08-16 | City of Sydney, Council@cityofsydney.nsw.gov.au | Licence for the Register of Significant Trees; unlocks Sydney (#5) and the best-instrumented register found anywhere | **sent** |
| 2026-08-16 | Bomenstichting, info@bomenstichting.nl | Licence for the Landelijk Register Monumentale Bomen; deepens 13 published Dutch cities | **sent** |
| 2026-08-16 | GDOS Poland, kancelaria@gdos.gov.pl | Which licence applies to CRFOP (metadata says CC0, condition fields empty, site publishes CC BY-SA); 117,474 tree monuments | **sent** |
| 2026-08-08 | Woodland Trust, ancienttreeinventory@woodlandtrust.org.uk | Written permission for ATI data; unlocks London and Edinburgh | **sent**, no reply yet |

**Two things this batch changed, both worth keeping (2026-08-16).** It started
as five mails and went out as three: Hidde remembered mailing the Woodland
Trust, and the table above confirmed both it and Catalonia went on 2026-08-08
with no reply yet. The machine's duplicate guard did not catch that, because it
reads `data/outreach-sent.json` and those two were sent by hand, so they existed
only in this markdown table, which no script reads. Both are now backfilled into
that file. **Anything sent by hand goes in outreach-sent.json as well as here**,
or the guard is blind to exactly the mails a human cared enough to send himself.

And the follow-up timing is unchanged by the near miss: this file's own guidance
is three or four weeks before a polite nudge, so the Woodland Trust and
Catalonia are due around 2026-09-01, not now.

The daily cap went 40 -> 50 on his instruction the same day.

Hidde's own expectation, 2026-08-08: no quick answer from either. Both are
public bodies or a large charity, and a licence question goes to somebody's
inbox rather than a queue. Weeks is normal, silence is not a no, and a polite
follow-up after three or four weeks is reasonable.

**What that means for the work, and it is the important half.** Barcelona and
London are now the only two phase-1 cities whose progress depends on a reply.
Nothing else does. So the plan does not wait: the rollout continues down the
order (Rome, Paris, Berlin, Amsterdam, New York, Lisbon, Vienna, Edinburgh,
Dublin), photos are judged in sessions from the queue we already have, and
Barcelona simply sits where it is, already the deepest city on the site at 32
trees, until somebody in Catalonia answers.

Next to send, when there is a spare ten minutes: the Bomenstichting (tier 1,
unlocks Amsterdam and twelve other Dutch cities), then the nine gardens and
parks in tier 3a, which need no permission at all and exist purely to earn a
link.

## Never tell an organisation the trees are theirs unless they own the ground

Added 2026-08-10, after Jon Pattee of Rock Creek Conservancy replied to batch
003: "those trees are not 'ours' nor do we have photos."

Montrose Park and Dumbarton Oaks Park are National Park Service ground. Rock
Creek Conservancy is a partner and advocate, not the landowner. Our own contact
research had it right, describing "the Rock Creek Park unit they work across",
and the composed mail escalated that into "two of them are in ground you look
after". The hedge was lost between the research and the sentence, which is the
failure to design against: a careful note becomes a confident claim when
somebody rewrites it for tone.

Three rules:

1. **A possessive claim needs a landowner.** An arboretum, a cemetery, a
   botanic garden, a university, a palace estate: these own their trees and
   "six of them are yours" is correct and was correct in the same batch. A
   conservancy, a friends-of group, a society or an association usually does
   not own anything. Contacts now carry `owns_the_trees`; when it is false or
   missing, the mail may not use yours, your trees, or ground you look after.
2. **Ask a friends-of group the question it can actually answer**, which is
   local knowledge: what is missing from the list, and what have we got wrong.
   Never open by asking them for photographs of trees they do not hold.
3. **Check whether a more specific partner exists before writing.** Dumbarton
   Oaks Park has its own conservancy, and it was already in our contact file,
   unmailed. We wrote to the neighbouring charity instead.

The useful thing this bounce surfaced: the landowner in Washington is the
National Park Service, and photographs by US federal employees are public
domain. Thirteen of our fourteen Washington trees have no image, so NPS is the
real photo route there, not the friends groups.

## Confirm who manages THAT park, not the city-wide agency

Second bounce of the same shape in two days, so this is a check rather than a
note. On 2026-08-11 Grün Berlin's Servicecenter replied to batch 004: Treptower
Park is managed by the Straßen- und Grünflächenamt of Bezirk Treptow-Köpenick,
not by them. On 2026-08-10 Rock Creek Conservancy replied to batch 003 saying
the trees were not theirs, because that ground belongs to the National Park
Service.

Both times we picked the plausible umbrella body rather than the actual manager,
and both times the mail then told them the tree was theirs. Grün Berlin does run
many Berlin parks, and Rock Creek Conservancy does work along Rock Creek, so
neither pick was stupid. It was just unchecked.

**The check, before any mail naming a specific park or garden:** find who
manages that named site, not who manages parks in that city. In Germany the
answer is usually the Bezirk or Gemeinde, not the state-level agency. In the US
it is often the National Park Service or a city parks department rather than the
friends group. One search on the park's own name settles it.

**And the opener needs a variant, which is a Hidde decision.** The approved
German line, "Ich bin online auf diesen Baum von Ihnen gestoßen", and the
English "I found this tree of yours online", both assert ownership in the first
sentence. That is right for an arboretum, a botanic garden or a cemetery, and
wrong for everyone else. Until there is a non-owner variant, the same mistake
will keep shipping in the first line of every mail.

## Every thread ends with one open question about a tree

Standing rule from Hidde, 2026-08-11, after a morning of three replies of which
two were a flat no on what we asked.

Photographs, data and research can all be refused. Knowing a good tree cannot.
So whatever the mail says and whatever came back, the last line invites a tree,
in one sentence, never as the reason for writing.

- English: "Just as one tree fan to another, if you have any suggestions for
  cool trees that could be on the map I'd love to hear them and add them."
- German: "Und falls Ihnen unterwegs ein Baum einfällt, der auf die Karte
  gehört: immer her damit."

It costs them nothing, it is the one expertise they certainly have, and it is
the only ask that leaves a thread open after a no. A photograph fills one gap;
a tip is a tree we could never have found, from somebody who stands near it.

Two limits. It goes last and stays one sentence, or a no on the main request
takes it down with it. And when somebody has already volunteered, phrase it as
an invitation rather than an addition to their task list: Wolfgang Schürmann
had just taken the job on, so "falls Ihnen unterwegs ein Baum einfällt" widens
what he might return with, where a list of what would help most would have read
as chasing him on the day he said yes.

## Batch 005, 2026-08-16: 40 mails, his own text, and a category change

Forty tree societies, city tree groups and blogs across NL, BE, PT, ES, CA, IT,
UK and IE. Sent from his own words: he wrote the mail in Dutch in session and I
rendered it into six languages, which is the division of labour HIS_VOICE.md
already records and the third time it has produced the right mail in one pass.

**What changed against batch 004, and why.** The recipients are the change. Of
the 57 mails sent 8 to 10 August, 40 went to gardens, palaces, parks
departments and ministries, and those are the ones that stayed silent; every
useful reply came from a named person who cares about trees personally, and a
municipality does not link out anyway. So batch 005 contains no institution
that manages ground: it is the societies with a newsletter and the bloggers who
already write about exactly this.

**And the mail is shorter and asks for less.** One look at the page, one
personal question ("welke boom mis jij persoonlijk op de site?"), no photograph
request at all. His reasoning, verbatim: "laat maar die fotos kunnen we altijd
in een tweede mail vragen". A first mail that asks for photographs, corrections
and a tip is three jobs for a stranger; a first mail that asks an opinion is
one, and the photographs have a natural second thread if they answer.

Two wordings recorded because he corrected them here: **remarkable is
"opmerkelijk" in Dutch and never "ongelofelijk"** (now a check in
`scripts/mailcheck.py`, so no future draft can carry it), and the mail says
nothing about where he lives.

One mail differs. ICNF's carries an extra sentence about an error in their own
register, three Setubal olives with 2009 in the age column. It is the only
thing in this batch we give rather than ask.

The claim "this tree of yours" survives only where the organisation actually
manages the ground (Fondazione Villa Ghigi). Friends-of groups get their park
named instead, city groups get "in jullie stad", national bodies get the city
named. That distinction is enforced by mailcheck's POSSESSIVE CLAIM check,
which exists because batch 004 told Schoenbrunn it owned trees it does not.

| Date | Who | Ask | Status |
|---|---|---|---|
| 2026-08-16 | 13 Dutch tree groups and blogs (Bomenstichting Den Haag/Amsterdam/Utrecht, Boomwachters Groningen, Haarlemse Bomenwachters, Bomenbond Rijnland, Vrienden van Sonsbeek, Haagse Hofjes, Kring Vrienden 's-Hertogenbosch, IVN, Bomenbieb, Boommade, Bomen Bescherming Amsterdam) | Look at the page, which tree do you personally miss | **sent** |
| 2026-08-16 | 4 Flemish (Bomen Beter Beheren, BOS+, VVOG, wndln) | idem | **sent** |
| 2026-08-16 | 7 Portuguese (Quercus Lisboa and Setubal, LPN, ICNF, Wilder, Naturlink, Lisboa Secreta) | idem, ICNF plus the register error | **sent** |
| 2026-08-16 | 5 Spanish and Catalan (AEA, AEPJP, Bosques sin Fronteras, Plantipodes-AM, Observatori Forestal de Catalunya) | idem | **sent** |
| 2026-08-16 | 6 Italian (Societa Botanica Italiana, ISA Italia, Italia Nostra, Carteinregola, Villa Ghigi, Amici del Parco Trotter) | idem | **sent** |
| 2026-08-16 | 5 UK and Irish (Tree Council, Arboricultural Association, Ancient Tree Forum, Tree Council of Ireland, Kings Weston Action Group) | idem | **sent** |

Built by `scripts/build_batch_005.py`, which reads every tree count from the
live city files at build time so no mail can quote a number that has moved.
66 addresses of the 106 remain unmailed, almost all of them gardens, parks and
municipalities, which is the category this batch deliberately skipped.

**Batch 005's first reply came in nine minutes, and it was a wrong number.**
Rogier Dop answered from haagsehofjes.nl: it is a biscuit company, not the
foundation behind the Heilige Geesthofje where the juttepeer stands. "Ik ben
een koekjesbedrijf, sorry." A correct address on a correctly named site, and
still the wrong organisation, which is a failure mode no amount of care in the
letter can catch. Hidde had the reply sent the same hour (`drafts/reply-haagse-hofjes.md`,
three lines, no tree question, because the man had just said trees are not his
subject). The address and then the whole domain went on the do-not-contact
list, and the contact record is marked blocked with the reason so no future
batch can pick it up. The juttepeer still needs the hofje itself or the Haags
Hofjesberaad; no verified address yet.

**And the second reply was the good kind of no (2026-08-16, Vrienden van Sonsbeek).**
They did not decline the project, they declined being the right desk, and named
the right one: Natuur Centrum Arnhem. That is the DUIC-to-Oud-Utrecht shape
again, which is still the only press result this project has, so it is now
twice that a referral has been worth more than an answer. Both mails went the
same hour: two lines of thanks to Sonsbeek that leave the thread open, and a
first mail to the Natuurcentrum opening with the name that referred us.
The new contact is recorded in `data/outreach-contacts-nl-be.json` with its
provenance, because a referral that lives only in a mail thread is lost the
day the thread scrolls away.

Worth noting for the machinery: the thank-you was the first mail ever sent to
an address already in the register, and it went through the `resend_reason`
door rather than around it. The register now says why that address has two
mails, which is the whole point of the door.
