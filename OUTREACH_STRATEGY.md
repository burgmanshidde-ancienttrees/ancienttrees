# Outreach strategy

Hidde, 2026-10-19: "maak een outreach strategie en start met het aanleggen van een database van emailadressen, dit gaat te ad hoc." This is the plan every outreach batch follows from now on. The rules for how a mail reads stay in drafts/OUTREACH.md (private) and drafts/PITCH_VOICE.md; this file says who, what, how often and how we know it works.

## What outreach is for

Three things, in this order while Google recovery mode lasts:

1. **Backlinks** to pages Google already shows. Authority is the missing piece: our best pages sit at positions 15 to 20.
2. **Attention and users**: an article or a mention that sends people who then open the app.
3. **People who help**: readers and tree people who add trees and photos. Ambassadors come out of this, never out of a cold ask.

## What the first 950 mails taught us

| Worked | Did not |
|---|---|
| News ("the app is out" brought about 14 downloads) | "Become our ambassador" to an organisation |
| A small, true, specific ask ("our page cites you, with a link; a link back would help") | Volume: 162 cold mails in early October, 5 replies |
| People who already love trees | Asking an organisation to become something of ours |
| Local and regional press (Brabants Dagblad, Omrop Fryslân answered) | Big-city desks (no reply yet) |

## The database

`python3 scripts/contacts_db.py` keeps one private file, data/outreach-db.json, with every address we know: group, language, city, the trees that tie us to them, every mail sent, every reply, and a status (ready, mailed, replied, linked, declined, ambassador, do_not_contact). It is rebuilt from the sent log and replies on every `--build`, so it never drifts; notes and link status set by hand survive.

- `--status` shows the table per group.
- `--ready <group> --limit N` is where every batch starts.
- `--set <address> linked=yes linked_url=...` records a backlink when we find one.

Feeders, all code, almost no tokens:

| Feeder | Finds |
|---|---|
| scripts/source_contacts.py | sites our trees cite as a source (about 1,800 domains) |
| scripts/press_desks.py | local newspapers near our cities (good for big cities; small cities need a hand search) |
| the research files data/outreach-contacts-*.json | gardens, societies, councils found by earlier passes |
| our own Supabase | readers who sent a tree or photo |

## The groups, one ask each

| Group | Who | The ask | Per day |
|---|---|---|---|
| source | sites that our tree pages cite, **and only sites a person runs** (blogs, societies, local history, tree enthusiasts; since 2026-10-20 registers, ministries and regional governments are classed council: zero of 29 answered and none would link) | "Our page on <tree> uses yours as a source, with a link; a mention would help these trees get noticed" plus a tree question | 10 |
| press | local and regional desks, **regional before big-city, focus countries, roster cities first** (what answered: Brabants Dagblad, Omrop Fryslân; what did not: the capitals' desks) | the city's most surprising sourced tree fact, then the app as news, photos offered | 3, after the round 1 and 2 readout on 10-21 |
| tourism | official visit-the-city sites of roster cities (new 2026-10-20, Hidde: "start doing all this"); scripts/tourism_sites.py feeds it | our map of the city's old trees as a free resource for their parks or green page; one tree named | 2 |
| guide | independent city guides and walking blogs, the getLISBON model (the one link ask that worked, 2026-09-04); the night run sources them since 2026-10-25 | our map of the city's old trees as a resource for their parks article. **Never a link swap** ("we link to you if you link to us"): Google names link exchanges as a link scheme, the worst thing to be caught at under a spam demotion. A link from our side only where it serves a reader, never as a trade | 2 |
| **nature** (new 2026-10-25, Hidde: "natuurpagina's zijn veel geïnteresseerd om met ons te praten") | nature magazines and websites, national or regional, the Wilder model (published 2026-10-23 with four followed links, after the capitals' news desks never answered) | the story: a stranger's photograph that put a tree on the map, or the country's most surprising tree, with photos offered. **The mail is drafts/nature-template.md** (Hidde, 2026-10-26): open on their article about a tree of ours, which must be a source on that page | 3 |
| **archive** (first while recovery mode holds, 2026-10-24) | people with photographs of our trees that are on no open site: dendrology and tree societies (the Dansk Dendrologisk Forening model), local photographers (Flickr all-rights-reserved photos geotagged at our trees, a city's tree blog), our ambassadors, warm repliers | "may we use your photographs of these trees on their pages, credited to you?", with the list of their trees that have no photograph, demand cut cities first (data/index-kept.json). A yes: licence "Used with permission from <name>; credit required", and the pages return to Google by themselves | 3 |
| society, garden | tree groups, friends-of groups, gardens that own trees | local knowledge: which tree is missing, what did we get wrong | 2 |
| reader | people who sent us a tree or photo | the ambassador invitation for their city (ambassador.py --invite-scan) | as they come |
| council | town halls and registers | only for data or a photo, never a link ask | rarely |

Ambassadors are never asked for links or badges (Hidde, 2026-10-16). Nobody gets a second cold mail; a second mail needs news or a reply.

**Never ask a stranger to go out and photograph a tree** (Hidde, 2026-10-26, on the Lisbon ten: "this is a big ask dont do that"). A cold mail asks only for what the person already has: photographs they already took, a fact they already know. The good opener is news about their own work ("your photograph of <tree> is on its page now, with your name"), then the one tree question.

**Warm repliers (Hidde, 2026-10-20: "go do this"):** the people who answered a mail are the best link source we have, and a second mail to them carries the news that concerns them (their tree live, their correction on the page) and the one plain link ask. Two rules he set the same minute: **read his inbox first** (`outreach_inbox.py`), so a batch mail never lands in the middle of a conversation he is having ("check my inbox before jumping in with random conversation in between"); and **the organisations he is already deep in conversation with get no batch mail at all**: Quercus, the Woodland Trust, the Bomenstichtingen (Amsterdam, Den Haag), Baumkunde. Those threads are his.

## Where the night run looks for the archive group (2026-10-25)

Who holds photographs of our trunks, in the order they pay off. Start from the kept-set cities with the most photo-less trees (on 2026-10-25: Barcelona 42, Chicago 37, Vienna 36, Seville 35, Munich 33, Brussels 31, Portland 31, Krakow 30, Singapore 29, Arnhem 29, Valencia 29; 1,158 in 109 cities).

1. **National and regional dendrology or tree societies**, the Dansk Dendrologisk Forening model (32 Copenhagen pages from one yes). Members photograph remarkable trees for their journals and excursions. Starting points to check: the Nederlandse Dendrologische Vereniging (NL; never the Bomenstichtingen, Hidde's own threads), Belgische Dendrologie Belge (asked 10-25), Deutsche Dendrologische Gesellschaft, Österreichische Dendrologische Gesellschaft, Polskie Towarzystwo Dendrologiczne, Asociación Española de Arboricultura, the Tree Register and the Ancient Tree Forum (UK).
2. **People who published their own photographs of a city's trees**: a book author (Ricard Llerins Bonet, Barcelona, asked 10-25), a monumental-tree blog, a local photographer whose site shows our trunks. Find them from the sources our pages already cite and from the city's newspaper survey.
3. **Arboreta, botanical gardens, cemeteries and friends-of-the-park groups** whose grounds hold several of our trees and who keep a photo library (for example Hoyt Arboretum for Portland, the Morton Arboretum for Chicago).
4. **City heritage-tree programmes** that photograph their listed trees (Portland's Heritage Trees, Singapore's NParks Heritage Trees). These file as `council`; ask for the photographs, not a link.

**Then the nature and guide groups**, once archive has a city's candidates: per focus country, the nature magazines and websites (Wilder's peers), and per kept-set city the independent guides that write about its parks (getLISBON's peers). Same rules: an address the site publishes, `source_url` that page, type `nature` or `guide`.

Not worth the search: national registers and ministries (they do not answer photo asks), tourism offices (no own tree photos), Flickr accounts without a website of their own (no published address).

## Communities: Reddit and Facebook (decided 2026-10-16)

Posts, not mails, and Hidde posts them himself from his own accounts; a session drafts. The full plan, the four example posts and the ask-the-admin messages are on his private page https://claude.ai/artifact/CX8HzNwrwuo9wyKXEAfig4 (local copies drafts/where-to-post.html and drafts/group-messages.md stay out of the repo: they name people).

- **Start when the app is tested and stable**, not before: posting was planned for about a week after 2026-10-16.
- **Order:** Big Tree Seekers (via its admin), r/marijuanaenthusiasts (Reddit's real tree community; r/trees is cannabis), then one city subreddit a week: r/lisbon, r/Edinburgh, r/Munich, r/london. r/bath waits until Bath has more than five trees.
- **Parked at Hidde's wish:** Dutch and Flemish groups and r/Amsterdam (home turf). Product Hunt waits for phase 2. Hacker News: a Show HN drafted 2026-10-23 on Hidde's "lets do 3 then", after the Reddit practice; it replaces the earlier "later or not at all" (drafts/show-hn.md, local). r/SideProject still later.
- **Shape that works:** be open that he built it, lead with one tree (a number in the title, one strong photo with its licence credit), ask which tree is missing, link last or in a comment. Ask the admin or mods first.
- **Reddit:** a fresh account first comments for one to two weeks (10 to 20 useful comments, no links) before any post. **Facebook:** Hidde has no profile; admins are reached by mail instead.
- **Done:** 2026-10-16 the Big Tree Seekers / Big Trees of New York admin and the coordinator of Australia's National Register of Big Trees were mailed in Hidde's own words (log in drafts/OUTREACH.md). Answers decide whether the Facebook posts happen.
- **Measure:** the digest's numbers the morning after, never upvotes.

### Reddit after the first post (r/Lisbon, 2026-10-22)

The first post (1,400 views, 10 upvotes, four strangers naming a tree in four hours, one of them a tree we were missing) settled the shape and the limits. Hidde: "gaat het niet opvallen als wij voor 100 steden ongeveer dezelfde post doen?" Yes, so:

- **Ten posts, then a verdict.** One city a week, only cities Hidde has actually been to (the post is true: "I kept a list"), never from a template: each opens with a real memory of that city, names two trees without a good photo, ends on a question. Five in the Lisbon shape, five with a short list of four or five trees (one sentence each, why he liked it), alternating, so the ten say which shape brings contributions.
- **No link in the post.** One link, once, in a reply to somebody who says they will go; none in any other reply, even when asked (point to that reply). Thank every tip; ask for a photo only when somebody says they live or walk near the tree. Then upvote and stop: too much OP makes the thread Hidde's instead of theirs.
- **A post is for people, not tips** (Hidde, 2026-10-23, after r/sicily gave eight tips and nobody saw the name: "ik kom hier niet voor data", "we hebben genoeg bomen"). Ancient Trees must be named in every thread: the post edit after the first tips ("Edit: thanks for all the tips! I'm adding them to ancienttrees.app"), the bio, and any reply where someone asks. Count per post: visitors from that subreddit in Google Analytics and accounts within seven days; tips are a by-product, views and upvotes do not count.
- **Scale is not Hidde in a hundred subs.** It is ambassadors posting as themselves in their own city (komoot's Pioneer model, Hugo in Lisbon the first): the ten posts are the proof and the invitation. Every tip becomes a lead in data/leads/<city>.json the same day, source "reader tip on r/<city>", no name.
- **Check the sub before naming it** (Hidde, 2026-10-23: "hoe baseer je een strategie als je niet eens checkt of er een reddit groep achter zit"). Reddit blocks our fetches; reddapi.dev/subreddits/<name>/insights gives the member count. Checked 2026-10-23: r/palermo is the FOOTBALL club (1,286); the city sub is r/palermo_city (2,801, from 2022) and the real reach is r/sicily (81,831, bilingual). r/edinburgh 321,259; r/tokyo 898,735; r/glasgow 292,569; r/copenhagen 187,308; r/rome 177,478; r/barcelona 173,959; r/dublin 141,568; r/porto 63,914; r/Lisbon 22,000 (its own sidebar). A post goes to the biggest sub where the city's trees belong; a city sub under 5,000 is not worth a post of its own.
- **The night run does nothing with Reddit** (Hidde, 2026-10-25: "de nachtrun moet niks met reddit doen, dat is verspilde energie"; it had read Reddit since 10-24, found no new comment after the first day, and drafted replies he had already posted). `scripts/community.py` stays as a tool for a session he asks for. What it does: it reads every comment under his posts and new threads about an old tree in the tree subs and the city subs he posted in, from the Arctic Shift archive (Reddit blocks us). Tips become leads, replies are drafted into drafts/batch-community-preview.md, he posts them. A new post of his is registered with `community.py --add <url> --city <slug>`; `--kit <city>` gives the facts for the next post (sub size, trees without a photograph, trees with one), never his memory line. First pass, 2026-10-24: 19 comments under r/Lisbon, 7 he had not answered (one a photograph of the Santa Iria olive he asked for); 10 threads, two worth a reply.
- **A Reddit link is nofollow:** it counts for nothing as a backlink and for something as people who come direct or type the name afterwards, and as a thread that itself ranks for "oldest trees in <city>" with our name in it. Backlinks still come from societies, parks and papers, by mail.

## The daily rhythm

1. `contacts_db.py --build` then `--ready source --limit 15` (and the other groups on their days).
2. Pick the batch: ten to fifteen, focus countries first, the strongest tree tie first.
3. Write each mail in the site's language around one real tree; check every link to our page live, and that the page really links to them.
4. mailcheck, a preview file in drafts/batch-*-preview.md, Hidde reads and says verstuur; his words go into `approved_word`.
5. Send, mark the batch sent_complete, a line in drafts/OUTREACH.md, `private_store.py push`.

Ramp: ten a day this week, up to twenty once replies and bounces look normal. The send script caps at fifty.

## How we know it works

| Measure | How | When |
|---|---|---|
| Replies per group | outreach_inbox.py, then contacts_db status | weekly |
| Live backlinks | fetch each mailed source page and look for ancienttrees.app; record with `--set linked=yes` | a week after each batch |
| Downloads and visits per source | the digest's referrer and App Store source tables | weekly |

A group that brings nothing in two weeks stops. A group that works gets more of the daily number.

## Dates

| Date | What |
|---|---|
| 2026-10-21 | press readout: rounds 1 (big cities) and 2 (small cities) |
| 2026-10-22, 23, 26 | link check for source batches 1, 2 and 3 |
| 2026-10-29 | link check for press round 3 and tourism batch 1 (both sent 2026-10-22) |
| 2026-11-02 | first two-week verdict per group |
