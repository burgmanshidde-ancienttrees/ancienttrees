# Ancient Trees Businessplan
*Laatste update: 19 juli 2026 (funnel aangescherpt, UGC-trigger toegevoegd)*

---

## Missie
Mensen naar buiten krijgen om bijzondere oude bomen te ontdekken in steden wereldwijd. Niet een database voor tree nerds, maar een uitnodiging voor iedereen die verder wil kijken dan de standaard toeristische route.

---

## Het idee
Een ontdekkingsplatform voor bijzondere, oude bomen in steden wereldwijd. Open de kaart, zie de mooiste bomen in je buurt, tik op een boom en lees zijn verhaal, leeftijd en soort. Thuis in Amsterdam of op reis in Palermo. De website is het product voor de massa, de app het product voor de fans.

---

## De funnel (dit is de kern)
1. Iemand bezoekt een stad, zoekt iets als "oldest trees in Lisbon" en landt via Google of een AI-antwoord op een gratis stadspagina
2. De kwaliteit van die pagina wekt de gedachte: hier wil ik meer van zien
3. Een klein percentage van die bezoekers is boomgeek genoeg om de app te willen, en een deel daarvan betaalt
4. Content en app worden door hetzelfde systeem gebouwd: één investering, twee kanalen

De content is dus niet marketing voor de app. De content is het acquisitiekanaal en moet op eigen benen uitstekend zijn (zie SEO_GEO_BLUEPRINT.md voor de kwaliteitscontracten). Hidde is niet de bottleneck van dit systeem: het systeem onderzoekt en schrijft, Hidde bewaakt de kwaliteit.

---

## Product: App A (gecureerde gids)
Bewust gekozen voor de simpele versie:
- Top 10 bijzondere bomen per stad, onderzocht door het systeem, goedgekeurd door Hidde
- Per boom: foto, naam, soort, leeftijd, kort verhaal
- Geen community features in v1, geen upvotes, geen gebruikerssuggesties
- Wel lichte signalen op elke boompagina: correctie melden, foto insturen, "worth the detour". Die voeden Hiddes curatie, ze publiceren nooit direct
- User-generated content pas in v2, met een harde trigger: pas bouwen zodra de site 1.000+ organische bezoekers per maand trekt of de eerste 10 betaalde abonnementen binnen zijn. UGC zonder gebruikers is een lege feature, en ongemodereerde UGC raakt het grootste risico van dit product: één verkeerde locatie of verzonnen feit en het vertrouwen is weg

---

## MVP
Top 10 bomen in de 100 grootste steden wereldwijd. Duizend bomen totaal. Dat is de lanceerversie.

---

## Schaalstrategie
Één nieuwe stad per maand toevoegen. Twee uur werk per stad. Langzame maar consistente groei zonder overweldigend onderhoud.

---

## Content strategie
- Locaties via OpenStreetMap (open source, commercieel herbruikbaar)
- Verhalen en beschrijvingen gegenereerd door Claude, gecureerd door Hidde
- Foto's via Wikimedia Commons (vrij te gebruiken)
- MonumentalTrees.com data mag NIET commercieel gebruikt worden
- Later stadium: mogelijk partnership met MonumentalTrees na bewezen tractie

---

## SEO en distributie
- Geen social media content nodig
- Per stad een cluster van pagina's: stadspagina, boompagina's, vraagpagina ("What is the oldest tree in X?"), plus thematische collecties
- Claude onderzoekt en schrijft, Hidde keurt goed
- Site en app-content zijn hetzelfde werk: één investering, twee kanalen
- Organisch zoekverkeer via Google plus citaties door AI-engines (GEO) als primair acquisitiekanaal. De pagina's zijn daarvoor gebouwd: antwoord in de eerste twee zinnen, alles ook machineleesbaar als schema
- De kwaliteitscontracten staan in SEO_GEO_BLUEPRINT.md; geen pagina gaat live zonder daaraan te voldoen

---

## Businessmodel
- Freemium: twee bomen per stad gratis zichtbaar, rest achter paywall
- Veertien dagen gratis trial voor volledige toegang
- Prijs: €19,99 per jaar (hogere prijs filtert op intent, lagere churn)
- Na Apple commissie 30%: €13,99 netto per subscriber per jaar
- Geen stadspacks: gebruikers willen één beslissing

---

## Financiën
- Vaste kosten: Rork €200 + Apple €8 = €208 per maand
- Break-even: circa 180 jaarlijkse subscribers
- Doel: €2.000 netto per maand
- Daarvoor nodig: circa 1.900 actieve jaarlijkse subscribers
- Realistisch: jaar 1 €300-600/maand, jaar 2 €1.000-2.000/maand

---

## Bouwaanpak
- Tool: Rork Max (native Swift, geen code nodig)
- Hidde bouwt zelf met AI, geen developer
- Tijdsinvestering na launch: max 4 uur per week
- Eerste test: bouw Amsterdam MVP in één weekend om te checken of Rork kaartfunctionaliteit aankan

---

## Constraints
- Geen TikTok of social media content maken
- Max €300 vaste kosten per maand
- Max 4 uur werk per week na launch
- Geen complexe API-afhankelijkheden
- Hidde is zelf de doelgroep

---

## Concurrentiepositie
- MonumentalTrees.com: grote database, lelijk, niet mobiel, zes Twitter posts ooit, klein bereik
- Geen directe concurrent als mooie consumentenapp
- Jij bouwt de toegankelijke versie voor mensen die MonumentalTrees nooit zouden vinden

---

## Nog te valideren
- Vragen 4-10 van investeerderssessie nog niet afgerond
- Zoekvolume blog-content nog niet onderzocht
- Technische haalbaarheid kaartintegratie in Rork nog te testen
- Betalende doelgroep nog niet gevalideerd buiten Hidde zelf

---

## Volgende stap
Bouw Amsterdam MVP in één weekend. Tien bomen, Claude genereert content, Hidde keurt goed. Test of Rork kaartfunctionaliteit aankan voor je verder investeert.

