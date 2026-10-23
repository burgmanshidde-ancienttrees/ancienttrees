# Season Radar: waarom dit het volgende ontwerp is, en waar het betoog zwak is

Geschreven 2026-10-23, op zijn vraag van 2026-10-22: "mag je me overtuigen waarom
dat de oplossing is volgens jou want ik snap t nog niet". Niets is gebouwd. De
cijfers zijn vanochtend opnieuw uit PostHog gehaald (scripts/posthog.py, alleen
vreemden, onze eigen telefoons eruit zoals de digest dat doet). De referenties
staan in CONVENTIONS.md onder "Telling somebody a tree near them is at its best"
en de mockup naast de referentie in de preview (season-mock).

## 1. De cijfers van vandaag

Installaties per week, en hoeveel van die telefoons op een latere dag terugkwamen.

| week van | telefoons | terug binnen 7 dagen | terug binnen 30 dagen |
|---|---:|---:|---:|
| 30 aug | 13 | 5 | 5 |
| 6 sep | 15 | 3 | 5 |
| 13 sep | 16 | 4 | 7 |
| 20 sep | 13 | 9 | nog niet vol |
| 27 sep | 9 | 5 | nog niet vol |
| 4 okt | 12 | 2 | nog niet vol |
| 11 okt | 14 | 2 van 8 volgroeid | nog niet vol |
| 18 okt | 11 | te vers | te vers |

Wat eruit komt, eerlijk gezegd:

- September bij elkaar: 21 van 57 telefoons terug binnen een week (ongeveer 1 op 3). Oktober tot nu: 4 van 20 (1 op 5). De "1 op 13" uit het gesprek van gisteren haal ik vandaag niet uit de data; het is 1 op 5, met cohorten van 8 tot 16 telefoons. Twee telefoons meer of minder draait het oordeel om.
- Over de hele looptijd sinds 3 september: 103 telefoons. 60 ervan openden de app op precies één dag en nooit meer. 20 op twee dagen. 23 op drie dagen of meer. Zes op de tien installaties zijn dus na dag één weg, en dat is het cijfer dat telt, niet de week-op-week schommeling.
- Wekelijks actieve telefoons: 18 tot 23, elke week sinds begin september, vlak.
- Wat de laatste 28 dagen gebeurde (55 telefoons openden een boom): 837 boompagina's bekeken, 26 keer bewaard (7 telefoons), 22 keer afgevinkt (8 telefoons), 42 foto's (12 telefoons), 25 keer routebeschrijving (13 telefoons). Kijken is er. Bewaren en terugkomen bijna niet.
- Downloads: 1 tot 5 per dag, 19 van 29 uit App Store-zoeken. Een nieuwe telefoon per dag, die in zes van de tien gevallen de volgende dag al weg is.

## 2. De tijdlijn van één gebruiker

Dit is de wandeling uit CLAUDE.md ("walk the user's timeline"), gelopen voor wat
de app vandaag is.

**Eerste minuut.** Iemand zoekt "old trees" in de App Store, installeert, ziet
Discover met "Autumn is here" en zes bomen op hun mooist, tikt een boom open, leest
het verhaal. Dat werkt: 55 van 69 telefoons openden een boom. Hier zit het
probleem niet, en dat is precies wat de tijdlijnregel voorspelt.

**Dag zeven.** Niets. De app heeft geen enkele reden gegeven om terug te komen.
Geen boom is veranderd, niemand heeft iets gezegd, er is geen datum. De
seizoenschip op de kaart staat in de winkelversie zelfs uit (`Launch.season`
luistert naar een testvlag). Wie niet toevallig in de buurt van een boom is, heeft
niets om voor terug te komen. Zes op de tien komen dan ook niet terug.

**Dag dertig.** Wie een boom bewaarde (7 telefoons in 28 dagen) heeft een lijstje.
Maar het lijstje zwijgt. De ginkgo die hij in augustus bewaarde wordt in november
goud en de app weet dat (`best_time`, de fenologie per soort), en zegt niets.

**Het gat.** Drie weken niet geopend, dan een weekend vrij. Welke boom? De app
herinnert zich niets van de persoon, alleen de hartjes. Op de website staat
/in-season; in de app niets dat zegt "nu".

**Het falen.** Vandaag faalt er niets, omdat er niets beloofd wordt. Met een
melding wordt het falen zichtbaar: een melding voor een boom die al kaal is, of
voor een piek die drie weken breed is. Daarover hieronder.

**Wat een gedateerde reden verandert.** Eén melding, op de dag dat een boom die je
bewaarde of een boom bij je thuisstad op zijn mooist is: "The Ginkgo of
Botanisk Hage in Oslo has turned gold. It drops its leaves within days." Dat is op dag
zeven een reden om de app te openen die er nu niet is, op dag dertig een reden
om het lijstje te gebruiken, en in het gat precies het antwoord op "welke boom
dit weekend". Het mechanisme is niet "ga nu". Mensen plannen van ver (zijn eigen
lezing van 2026-10-19: ze scouten vakanties, bewaren voor later, terugkomen meten
we in dertig dagen). De melding is "wanneer te gaan", en Weathernews, die dit
sinds 2015 in Japan doet voor herfstbladeren en kersenbloesem, schrijft het
letterlijk zo: de kleuren blijven weken, plan je uitje op tijd.

Het is ook de enige van de vier betaalde functies die zelf naar de deur klopt.
Offline, wandelingen en het logboek wachten tot iemand de app opent. De melding
komt naar de persoon toe. Daarom is het de retentiehaak en de betaalde functie
tegelijk, en daarom dit eerst en niet de andere drie.

## 3. Wat anderen doen (conventiecheck, bronnen in CONVENTIONS.md)

- **Weathernews 紅葉Ch. en 桜Ch. (Japan).** Het dichtstbijzijnde dat bestaat. Je
  registreert maximaal vijf plekken uit 750, en de dag dat een plek "見頃" (piek)
  bereikt komt om 19:00 een push: "嵐山の紅葉が11月21日に見頃になりました。紅葉狩り
  計画はお早めに!" Sinds 2018 ook bij het begin van het kleuren. Per plek een stadium
  op een schaal van vijf en een voorspelde piekdatum. Opt-in per plek, op de pagina
  van de plek.
- **Audubon Bird Guide.** Push als een vogel van je eigen lijst in de laatste 24 uur
  gemeld is; vraagt eerst de notificatietoestemming. **eBird** doet hetzelfde per
  regio, alleen per mail, dagelijks of per uur, alleen als er iets nieuws is.
  **Merlin** stuurt helemaal geen meldingen over vogels in de buurt.
- **AllTrails.** Geen seizoensmelding. "Trail Conditions" (alleen Plus en Peak) is
  een kaart op de routepagina met het weer van vandaag; het beste seizoen is geen
  veld maar zit in de verslagen van de community. **Strava**: per type een
  schakelaar, niets met tijd of plaats. **PictureThis**: een herinnering per plant,
  ingesteld op de pagina van die plant. **komoot**: niets gevonden.
- **Apple.** Vraag toestemming op het moment dat de reden duidelijk is (na de
  eerste bewaarde boom), niet bij de start. Of stuur de eerste melding
  "provisional": stil in het berichtencentrum, met knoppen Keep en Turn Off, en
  de vraag komt pas als de melding er is.

Wat we overnemen: één boom, één moment, één datum; opt-in per bewaarde boom of per
thuisstad, nooit een algemene "meldingen aan"; de vraag bij het eerste bewaren;
een schakelaar per type in Settings; en nooit op de achtergrondlocatie van de
telefoon (dat doet geen enkele referentie, en onze eigen regel van 2026-10-10
houdt de "je bent 40 m van"-banner alleen in de open app).

## 4. Het tegenbetoog, zonder omwegen

1. **Seizoenspagina's trokken niets in Google (2026-09-24).** Waar: de
   handgemaakte lijsten (herfstkleur, geplant door koningen) kregen bijna geen
   vertoningen, de gegenereerde superlatieven wel. Dat zegt iets over zoekvraag:
   niemand googelt "autumn colour trees Lisbon". Het zegt niets over of iemand die
   de app al heeft terugkomt voor een datum. Maar het is wel een waarschuwing: het
   seizoen is als onderwerp nog nergens bewezen bij ons. Nul van onze cijfers
   bewijst dat mensen hierom geven; alleen Weathernews' tien jaar bewijst dat
   mensen er elders om geven.
2. **De cohorten zijn te klein om iets te bewijzen.** 8 tot 16 telefoons per week.
   Een week met 1 op 3 en een week met 1 op 6 liggen twee telefoons uit elkaar.
   Een maat als "van 1 op 5 naar 1 op 3" is in weken niet te onderscheiden van
   ruis; dat kost maanden, of meer downloads dan we hebben. Dit is het grootste
   gat in het betoog.
3. **De data is per maand, niet per week.** `best_time` zegt "november". Weathernews
   heeft waarnemers in het veld en een datum per plek. Een melding "deze week" uit
   maandgegevens is een belofte die we niet waarmaken, tenzij de melding eerlijk
   per maand spreekt ("this month") of we de datum ophalen uit lezersfoto's
   (fase 1: data verzamelen, een melding die vraagt "is hij al goud? stuur een
   foto" verzamelt precies dat).
4. **Dekking is bewust dun.** 102 soorten hebben een fenologiebestand, 20 een
   moment dat "worth the trip" is, 8 een `peak`-blok dat gedeeld mag worden
   (olijf, moerbei, bittersinaasappel, aardbeiboom, ginkgo, Kaukasische iep, tamme
   kastanje, vleugelnoot). Dat raakt 244 van 3.880 bomen; in november 115. Op
   de 598 pagina's die Google nog toont ligt het aandeel vergelijkbaar. De eerste
   versie is dus een ginkgo-melding in november en een kastanje-melding in oktober,
   niet een jaarrond radar. Dat kan genoeg zijn voor een test; het is niet wat de
   paywalltekst van 2026-08-18 belooft.
5. **Toestemming en Apple.** Een melding vraagt toestemming die de helft weigert als
   je het bij de start vraagt. Provisional lost dat deels op (stil, zonder vraag),
   maar stil betekent ook: niet op het lockscreen. En een push vraagt een
   apparaattoken per account op de server: een nieuwe kolom met persoonsgegevens,
   dus hard list 1, zijn ja.
6. **Bouwkosten en een niet-gevalideerde betaalde laag (hard rule 6).** App:
   toestemming op het juiste moment, token, Settings-rij, de melding opent de
   boom. Server: een dagelijkse taak die piek maal bewaarde bomen maal thuisstad
   uitrekent en via APNs verstuurt (Apple's eigen dienst, geen nieuwe
   afhankelijkheid; Supabase hebben we). Web: dezelfde taak stuurt een mail aan een
   ingelogd account, zodat beide oppervlakken hetzelfde doen vanuit één server.
   Data: het `peak`-blok van 8 naar 20 soorten. Schatting: twee tot drie weken
   sessiewerk plus een paar nachten data, voordat één melding de deur uit kan.
   Niemand heeft nog een cent betaald voor wat dan ook.
7. **Het App Store-evenement zegt niets.** Het herfst-evenement is nooit
   aangemaakt (het wachtte op zijn kaartafbeelding). Downloads liggen vlak op 1
   tot 5 per dag. Er is geen curve om uit te lezen.

## 5. Wat het goedkoop zou bewijzen of ontkrachten, vóór het bouwen

- **Eén handmatige mail aan de 36 accounts** (ondertekend Ancient Trees, zijn ja
  nodig: het is een mail die we niet eerder stuurden): "This week near you: the
  ginkgo at X has turned gold", met de boompagina als link. Meten: hoeveel
  accounts openen de app of de pagina in de 72 uur erna (PostHog `app_open` per
  install, GA op de pagina). Kosten: een ochtend. Dit test het mechanisme (een
  gedateerde reden brengt mensen terug) zonder push, token of toestemming. Met
  36 accounts is ook dit klein, maar het is het enige dat we deze maand kunnen
  weten.
- **De seizoenschip aanzetten in de winkelversie.** `Launch.season` staat uit;
  de kaart toont geen pulserende ginkgo's, de kaart toont geen seizoen. Dat is
  gratis en al ontworpen (2026-08-20, vier effecten). Het meet niets over
  terugkomen, maar het is vreemd om over een seizoensmelding te praten terwijl
  het seizoen in de app onzichtbaar is.
- **Eén vraag in de app, na het bewaren.** "Tell me the week it turns" als
  schakelaar die alleen een vinkje opslaat en nog niets stuurt. Meten: hoeveel
  van de bewaarders zetten hem aan. Kosten: een dag, geen server, geen token. Als
  bijna niemand hem aanzet, is de hele melding een antwoord op een vraag die
  niemand stelt.
- **Niet geschikt als test**: de downloadcurve van het evenement (er is geen
  evenement) en de retentiecohorten (te klein, zie punt 2).

## 6. De pagina om op te beslissen

**Stelling.** Google brengt mensen binnen en retentie beslist of ze blijven; zes
van de tien installaties zijn na dag één weg omdat de app geen reden geeft om
terug te komen. Een gedateerde melding ("deze boom bij jou is nu goud") is de
enige van de vier betaalde functies die zelf naar de persoon toe komt, en is
daarmee retentiehaak en betaalde functie in één. Daarom is dit het volgende
ontwerp, en niet offline, wandelingen of badges.

**De maat.** Zijn eigen maat: terug binnen dertig dagen. Nu 17 van 44 in de
septembercohorten (ongeveer 4 op 10, met daaronder 6 op 10 die nooit terugkomen).
Doel: 6 op 10 terug binnen dertig dagen, gemeten over minstens honderd
installaties, dus pas na een paar maanden leesbaar. Eerder leesbaar: hoeveel
bewaarders zetten de schakelaar aan, en hoeveel ontvangers openen de boom binnen
72 uur na de melding.

**De kleinste versie.** Eén meldingstype: de piek van een bewaarde boom, of de
dichtstbijzijnde piek bij de thuisstad als er niets bewaard is. Eén moment van
vragen: na het eerste bewaren. Eén rij in Settings. Eerst ginkgo en tamme
kastanje (de twee soorten met een piek die er nu aankomt), dan de rest van de
20. Beide oppervlakken uit één servertaak: push in de app, mail op het web voor
een ingelogd account. Geen achtergrondlocatie. Tekst per maand eerlijk zolang de
data per maand is.

**Kosten.** Twee tot drie weken sessiewerk en een paar nachten data voor de
kleinste versie. De goedkope tests hierboven kosten een ochtend tot een dag.

**De vraag die alleen hij kan beantwoorden.** Wil hij dit ontwerpen op de
overtuiging dat Weathernews' mechanisme ook voor bomen werkt, terwijl onze eigen
cijfers het niet kunnen bewijzen voordat het bestaat? En wil hij het als betaalde
functie houden (zoals 2026-08-18 zegt) of eerst gratis aanzetten om te meten of
het mensen terugbrengt, en pas dan de prijs erachter?

## 7. Uitkomst (2026-10-23, zelfde dag)

Hidde: niet overtuigd, en terecht. Het seizoen was een gok voor Plus, een push
is "ooit interessant maar niet het belangrijkst", terugkomen is een maandmaat
zoals bij Polarsteps, en de echte vraag is wat de Plus-stap is als veel mensen
bomen uploaden. Zijn volgorde staat: eerst Google terug en mensen die bomen
toevoegen, Plus pas bij echte gratis tractie (DECISIONS.md 2026-10-23). Wat dit
stuk fout had: weekcohorten van 8 tot 16 telefoons als bewijs, en content (het
seizoen) als betaalde laag. Gebouwd: één rij in de digest onder "Phones back
within 30 days", hoeveel van die telefoons in die dertig dagen iets gaven
(bewaard, afgevinkt, gefotografeerd). Eerst gebouwd op de eerste 24 uur,
verbreed op zijn vraag "hoezo maakt het uit of ze direct wat toevoegen": dat
maakt niet uit. Van de 23 telefoons die op drie dagen of meer terugkwamen gaven
er 10 ooit iets en 13 nooit; de zin "wie terugkomt is wie bijdraagt" klopte
niet.
