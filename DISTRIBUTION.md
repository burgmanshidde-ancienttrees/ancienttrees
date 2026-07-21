# Getting visitors

Written 2026-07-21. The site has had essentially none, and every funnel improvement below step 1 multiplies zero.

## The honest situation

The domain is new. Search will not send meaningful traffic for three to six months no matter what anyone does, because that is how long a new site takes to earn trust for queries like "oldest tree in Paris". So traffic in the next weeks comes from exactly one thing: telling people it exists.

That splits the work cleanly. **Everything except pressing post is automatable, and pressing post is Hidde's**, because a message under his name is his reputation. Drafts below are ready to paste. Change the voice freely, they are a starting point, not a script.

## Who this is actually for

Not "people who like trees" in general. The person who converts is **someone already out of the house in a city they are exploring**, with an afternoon and no fixed plan. That is why the site is in English and stays that way: a visitor to Lisbon searching in English is far more likely to walk to a tree than a local who has walked past it for years. Distribution should aim at that person, and at the people who like the *idea* of that person.

## Now: three posts, this week

Ranked by expected return for the effort.

### 1. Reddit, r/Amsterdam

The single best fit: local, curious, English-speaking, and receptive to "I made a thing about your city". Reddit punishes anything that reads as marketing, so the value goes **in the post**, and the link is almost an afterthought.

> **Title:** I mapped the ten oldest trees in Amsterdam. The oldest is 275 and stands inside Artis.
>
> I have been putting together a map of remarkable old trees, city by city, and Amsterdam was the one I most wanted to get right. A few things I did not know before:
>
> - The oldest tree in the city is a pedunculate oak in Artis, around 275 years old. It took root about a century before the zoo existed.
> - There is a cycad in the Hortus Botanicus that predates the Netherlands as a country.
> - The plane trees on Lomanstraat grew into each other and form a tunnel most people cycle through without looking up.
> - Amsterdam's oldest tree is young by European standards. London has yews over a thousand years old. The reason is peat, fire and war: little here gets left alone for long.
>
> Full list with locations, stories and a walking route that links seven of them in about 5.5 km: [link]
>
> It is free, there are no accounts and no ads. Some of the pins are only approximate and the site says so where that is true. If you know exactly where one of these stands, or know a tree that should be on the list, I would genuinely like to hear it.

**Where else the same post works:** r/thenetherlands, and later r/london, r/paris, r/rome, r/lisbon with the city swapped. Space them out by a week or two.

### 2. Show HN

Hacker News rewards the things this project happens to be: static, no trackers, no accounts, open data, honest about its own uncertainty. That last one is the hook, not the trees.

> **Title:** Show HN: Ancient Trees, the most remarkable old trees in five cities, mapped
>
> I have been mapping remarkable old trees city by city: ten per city, each with its history, an exact location where I could confirm one, and a walking route linking the ones close enough to do in an afternoon.
>
> Two things I decided early that shaped the rest. Every pin records whether its position is confirmed or approximate, and the page says so plainly next to the directions button, because sending someone to the wrong corner of a park is the one mistake that loses them for good. And there are no accounts, no cookies and no third-party trackers, so nothing needs a consent banner.
>
> It is a single Python script generating static HTML, MapLibre and OpenFreeMap for the maps, hosted on GitHub Pages. Research and verification are automated: each run has to find two independent sources for a tree's existence, species and age before it publishes, and flags what it cannot confirm rather than guessing.
>
> Five cities so far, ninety-five to go. Corrections welcome, that is the whole point.

### 3. A Dutch tree or nature community

Lower volume, much higher quality of attention, and the people most likely to send corrections and new trees, which is worth more than clicks. Candidates: Bomenstichting, local IVN branches, urban ecology and Amsterdam history groups on Facebook, and the Ancient Tree Forum in the UK for the London page.

Same content as the Reddit post, but lead with the correction invitation rather than the map. These people know things we do not, and being asked is flattering where being marketed at is not.

## Soon: local press

One email, one shot, worth more than everything above combined if it lands. The story is not the website, it is the person: someone quietly catalogued the oldest living things in the city and gave it away for free.

Targets: Het Parool (stadsredactie), AT5, Pakhuis de Zwijger, local Amsterdam newsletters.

> **Onderwerp:** De tien oudste bomen van Amsterdam, in kaart gebracht
>
> Beste redactie,
>
> Ik heb de tien oudste en opvallendste bomen van Amsterdam in kaart gebracht, met hun geschiedenis en precieze locatie. De oudste is een zomereik in Artis van ongeveer 275 jaar, die er al stond voordat de dierentuin bestond. In de Hortus staat een cycadee die ouder is dan Nederland als land.
>
> Wat mij tijdens het uitzoeken opviel: Amsterdam is naar Europese maatstaven een jonge bomenstad. Londen heeft taxussen van meer dan duizend jaar. Dat verschil zegt iets over de stad zelf, gebouwd op afgegraven veen en steeds opnieuw verwoest door brand en oorlog. Wat hier overleefde, deed dat met opzet: achter een hek, onder glas, of op een gazon dat een architect ontwierp.
>
> De kaart staat op ancienttrees.app, is gratis, heeft geen advertenties en verzamelt geen gegevens. Er staat ook een wandelroute langs zeven van de tien.
>
> Als het interessant is voor de stadsredactie loop ik graag een keer mee langs een paar van deze bomen.
>
> Met vriendelijke groet,
> Hidde

**Send this yourself.** Nothing on this project may go out under Hidde's name without Hidde sending it.

## Long: what runs the machine while nobody is posting

This is the part that does not need Hidde, and it is where most of the eventual traffic comes from.

- **Coverage.** Every city is more surface area for search. Ninety-five to go.
- **The question pages.** "What is the oldest tree in [city]" is a real query with weak competition, and there is one page per city aimed straight at it. These will likely be the first pages to rank, ahead of the city pages.
- **Photos.** The weakest link. A page without an image loses the click in search results and cannot be shared visually at all, which rules out every image-led channel. Twelve of fifty trees currently have one.
- **Seasonality.** Not built. When a tree is at its best is knowledge nobody else publishes, it converts "nice" into "this weekend", and it comes free alongside research already being done.

## What to expect

Modest numbers, and that is the point. A good Reddit post might bring a few hundred people in a day and then stop. That is not a business, but it is the first real evidence about whether anyone cares, whether they click the walking route, and whether a single person sends a correction. Those three numbers are worth more right now than another twenty cities.
