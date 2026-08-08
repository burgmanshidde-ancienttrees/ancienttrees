# Press pitch: the immigrants story

Written 2026-08-08. Only Hidde sends this (hard rule 4). Every number below is
computed from our own published data and re-checkable with one command:
`python3 scripts/press_numbers.py`. If a number has drifted since, regenerate
before sending: a journalist who checks and finds a mismatch never writes again.

**Why this angle and not another.** Three were tested against the data on
2026-08-08. The walkability ranking is already a page and reads as a listicle.
The "trees survive on sacred ground" angle looked strong at 26 percent and did
not survive checking: the match was picking up street names like Plantage
Kerklaan and administrative parishes in Setubal, so it was dropped rather than
published. What held up under the strictest counting is this one, and it is
also the most surprising: **four in ten of the ancient trees we map in European
cities are not European species.**

## The pitch, English, for a foreign desk or environment desk

**Subject: Four in ten of Europe's ancient city trees are foreigners**

Hello,

I map the oldest and most remarkable trees in the world's cities at
ancienttrees.app, one tree at a time, with sources for each. Somewhere around
780 trees in 91 cities now.

Counting the ones standing in European cities turned up something I did not
expect: 271 of 686, four in ten, are species that are not native to Europe. The
most common of all is a tree that exists nowhere in the wild. The London plane,
which we map 62 times across 35 cities, is a chance hybrid of an American and
an Asian parent that appeared in a nursery in the 1600s and became the default
street tree of half the continent.

The individual arrivals are better than the statistic. Seville has an ombu
whose seeds are said to have come back from South America with Christopher
Columbus's son around 1529. Paris's oldest tree, planted 1601, grew from seed
posted out of the Appalachians to the king's herbalist. London has a black
mulberry from James I's failed attempt to start a British silk industry, which
failed because silkworms will not eat black mulberry leaves.

The full list, with locations and sources:
https://ancienttrees.app/collections/europes-oldest-trees-are-immigrants

Happy to send the underlying data as a spreadsheet, and a good number of the
photographs are openly licensed and reusable with attribution. If a local angle
helps, I can pull the same count for one country or one city.

Hidde
ancienttrees.app

## De pitch, Nederlands, voor een NL-redactie

**Onderwerp: Vier op de tien oude bomen in Europese steden zijn geen Europeanen**

Beste redactie,

Ik breng op ancienttrees.app de oudste en bijzonderste bomen van steden in
kaart, boom voor boom, met bronnen per boom. Inmiddels zo'n 780 bomen in 91
steden.

Toen ik de Europese steden apart telde kwam er iets uit dat ik niet verwachtte:
271 van de 686 bomen, vier op de tien, zijn soorten die hier niet vandaan
komen. De meest voorkomende is een boom die in het wild helemaal niet bestaat.
De gewone plataan, bij ons 62 keer in 35 steden, is een toevallige kruising van
een Amerikaanse en een Aziatische ouder die in de zeventiende eeuw in een
kwekerij ontstond en daarna de standaardstraatboom van half Europa werd.

De losse verhalen zijn nog beter dan het cijfer. In Sevilla staat een ombu
waarvan de zaden volgens de overlevering rond 1529 met de zoon van Columbus uit
Zuid-Amerika meekwamen. De oudste boom van Parijs, geplant in 1601, groeide uit
zaad dat vanuit de Appalachen naar de hofkruidkundige werd gestuurd.

De hele lijst, met locaties en bronnen:
https://ancienttrees.app/collections/europes-oldest-trees-are-immigrants

Ik stuur de onderliggende data desgewenst als spreadsheet, en een flink deel
van de foto's is vrij van rechten met bronvermelding. Voor een Nederlandse
invalshoek kan ik dezelfde telling voor Nederland of voor Amsterdam maken.

Hidde
ancienttrees.app

## What to have ready when someone answers

- **The spreadsheet.** `python3 scripts/press_numbers.py --csv` writes
  `press-trees.csv`: every tree, city, country, species, origin, age, and its
  page. Send that, not a PDF.
- **Images.** 328 trees carry an openly licensed photograph. The licence and
  the required credit are recorded per tree and must travel with the image; a
  desk that strips the credit off a CC BY photo puts the licence in breach, so
  say it in the mail rather than assuming.
- **The honest caveats, offered before they are asked.** The count is of the
  trees we have published, not of every old tree in Europe, and the map is
  denser in some countries than others because open tree registers are. Ages
  are as sourced, and where sources disagree the page says so. Saying this
  first is what makes the rest credible.

## Who to send it to

Not a wire service first. The order that works for a small project: one
national outlet that already runs long nature pieces, then the city desks of
the cities that come out best in the story, then the tree and garden press.
Named targets belong in OUTREACH.md beside the backlink list, and this pitch
is one email at a time, never a blast.
