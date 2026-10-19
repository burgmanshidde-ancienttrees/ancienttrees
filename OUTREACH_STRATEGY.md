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
| source | sites that our tree pages cite | "Our page on <tree> uses yours as a source, with a link; a mention would help these trees get noticed" plus a tree question | 10 |
| press | local and regional desks | the city's most surprising sourced tree fact, then the app as news, photos offered | 3, after the round 1 and 2 readout on 10-21 |
| guide | city guides and walking blogs | our map of the city's old trees as a resource for their parks article | 2 |
| society, garden | tree groups, friends-of groups, gardens that own trees | local knowledge: which tree is missing, what did we get wrong | 2 |
| reader | people who sent us a tree or photo | the ambassador invitation for their city (ambassador.py --invite-scan) | as they come |
| council | town halls and registers | only for data or a photo, never a link ask | rarely |

Ambassadors are never asked for links or badges (Hidde, 2026-10-16). Nobody gets a second cold mail; a second mail needs news or a reply.

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
| 2026-11-02 | first two-week verdict per group |
