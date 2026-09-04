# Tree page: the block between the photograph and the story

Date: 2026-09-04. Decided with Hidde in session, from mockups at real phone
size (five options, real content, three trees: the Banghak-dong Ginkgo, the
Kongeegen with long values, the Leiden Laburnum with a ticket and an
approximate pin). He chose option E, the AllTrails page as his own screenshot
of the Klompenpad Netelenburchpad shows it, with three changes he made after
seeing it drawn: the blue ticket panel stays as it is today, the thumbs down
goes ("i agree that we dont need a thumb down"), and the count in the summary
line is itself the button that casts the vote.

Surface: the iOS app, `Screens/TreeDetail.swift`. The website keeps its chip
row for now; see "Both surfaces" below.

## What was wrong

Hidde, 2026-09-04, on the Banghak-dong Ginkgo page: "the UI design of this page
is really a waste... the alignment of the age etc especially if things have two
rows... the pin sentence takes up too much space the thumbs up and down also
and bad designed." Then, on the mockups: the species appeared three times
(name, caption, fact card), and the header took more room than it needed.

Three causes, all in the block between the hero and the story:

1. The fact card put the value above its label. A value that wraps
   ("Pedunculate Oak", "up to 1,500 years") pushed its own label down, so
   "Age", "Species" and "Pin" sat at three heights. The only value that ever
   wraps is the species, because it is a word rather than a number.
2. The approximate-pin note was a tinted panel with a separate 44 pt button,
   restating a fact the card above had already said ("Approximate").
3. The vote sat above the story as two 66 by 50 pt grey pills, half again the
   size of any comparable control in the reference apps.

## The benchmark (recorded so it is not redone)

- **AllTrails trail page** (Hidde's screenshot, 2026-09-04): name; one small
  underlined summary line, rating · difficulty · place, every item a link; a
  stat row of SHORT values with the value on top and the label under it, thin
  dividers, columns sized to content; the description. Reviews lower down.
  Note the correction: an earlier draft claimed AllTrails puts the label on
  top. It does not. Value-on-top works for them because no value is a word.
- **Google Maps**: rating and count in the summary line under the name; the
  "Rate & Review" prompt (five empty stars) lower on the page. "Temporarily
  closed" is a coloured word in the summary, not a panel; "Suggest an edit" is
  a plain list row.
- **Apple Maps**: thumbs up and down in small circles, in a section low on the
  card.
- **Airbnb**: no stat columns; one dot-separated line of facts under the
  title; highlight rows with icon, bold line, grey line, no tint.
- **App Store info strip**: label above value, thin dividers. The other valid
  convention; not chosen because Hidde chose AllTrails.

The principle that fell out: **a column states a short value, a link line
carries the words, a panel is reserved for something that changes whether you
set off at all.**

## The design

Top to bottom, replacing `header`, `facts`, `approximateNote` and the position
of `WorthItView`. Everything else on the page (hero, ticket panel, story,
access block, discover-more chips, credit, pinned action bar, toolbar) is
unchanged.

### 1. Name

As today: `tree.name`, brand 30 bold.

### 2. Summary line

One line directly under the name, 15 pt, three underlined links separated by
middle dots, wrapping onto a second line when it must:

    👍 120 · Ginkgo · Banghak-dong, Seoul

- **The count, which is also the button.** Thumbs-up glyph and
  `counts.up(tree.id)`, underlined. Tapping it casts the vote: the glyph
  fills, the number goes up by one, tapping again takes it back. This is
  Strava's kudos and Instagram's like, where the number sits ON the control;
  nothing anywhere draws a number that is only a number beside a separate
  button that casts. Hidde asked exactly this on 2026-09-04 ("how does someone
  add a thumb up by clicking the 17"), and it is the same control as the one
  after the story, drawn small. Both read and write the same
  `at_worthit_<id>` state, so they are never out of step.
  Shown only when the count is positive, which is what `VoteCounts.up` already
  returns (2026-08-27, a zero beside a thumb on a tree we chose reads as a
  verdict). When there is no count the segment is omitted and the line starts
  at the species; the control after the story is then the only way in, which
  is right, because an empty count is not a control worth advertising.
- **The species**: `tree.commonName`. Tap: `navigator.push = .species(...)`,
  as the fact chip does today. The full name with the Latin
  (`tree.species`) moves off this page; it is on the species page one tap
  away. On a tree of your own with no species, this segment is the existing
  "What kind of tree is it?" button.
- **The place**: the existing `place` string. Tap: `navigator.push =
  .city(slug)` for the tree's city. On a tree of your own it stays the plain
  text "Where you photographed it", not a link.

Every link has a 44 pt tall hit area (`.frame(minHeight: 44)` +
`.contentShape`), which appfit measures; the text itself stays 15 pt. Hidde,
2026-09-04: "they have very small clickable stuff so apparently it can work."

### 3. Stat row

Values on top (brand 21 bold), labels under (14 pt, inkSoft), 1 pt hairline
dividers between columns, columns sized to their content with 16 pt padding,
no card, no icons, never wrapping. Only short values are allowed in it:

| Column | Value | Label | When |
|---|---|---|---|
| Age | `550-830` from `ageMin`/`ageMax`; `550` when only a minimum | Years old | numbers exist |
| Age | the `age` string as written, `.lineLimit(1)` scaled down | Age | only a text age exists |
| Age | "Add it" button | Age | own tree, no age (as today) |
| Species | never | | it is a word; it lives on the summary line |
| Girth | `12.6 m` | Girth | the feed carries `girth_cm` (see 6) |
| Pin | `Exact` / `Approximate` | Pin | always |

A tree with no age at all shows "not recorded" under "Age", as `shortAge`
does today. No "Free" column: free is the site's default and is not said.

### 4. Ticket panel

Unchanged: `ticketNote`, the blue panel with the ticket glyph, above the pin
ask, below the stat row. Hidde, 2026-09-04: "i did really like the blue icon
ticket thing... it deserves a alone standing warning as it is now." It is the
one thing on this block that decides whether somebody sets off, which is the
panel's job under the principle above.

### 5. Pin ask

Replaces the gold panel. Shown only when `tree.precision.needsWarning`. One
line, 14 pt inkSoft, the scope glyph, then:

    Approximate pin. Show us where it is

"Show us where it is" is underlined, moss, and opens `PlacePin` as today. The
whole line is the tap target, 44 pt tall. The longer sentence ("You may have
to look around once you are there") goes; the stat row already says
Approximate and the story's FAQ says the rest on the web.

### 6. Girth in the feed

`site/src/pages/api/trees.json.ts` gains `girth_cm` and `height_m` per tree
where the city file has them (1,035 and 501 trees on 2026-09-04). This is an
ANSWER travelling in the feed, not a rule (CLAUDE.md, the both-surfaces
mechanism). The app decodes both as optional `Int?`/`Double?`; the stat row
shows girth as metres with one decimal when present and nothing when absent.
Height is decoded but not shown on this page yet: three columns is the row.
Feed additions pass `feedshape.py` (additions are ignored) and
`LiveFeedContract` needs the two optionals added to the model it decodes.

### 7. Vote: one direction only

`WorthItView` moves below the story, above the access block, and loses its
thumbs down. Hidde, 2026-09-04: "i agree that we dont need a thumb down."
Every reference offers a single positive act and routes the negative to a
report, which this page already has twice: the toolbar's report menu and the
"Something's wrong" chips.

What the control becomes: the question on the left, one 44 pt capsule on the
right with the thumbs-up glyph and the count, hairline border on the page
ground, `.buttonStyle(.plain)`, brand 15 semibold, tabular digits. Filled
glyph and moss tint when this account has voted. Tap casts, tap again undoes,
exactly as today.

What this changes in the data, and it changes less than it looks. The vote
still writes a `feedback` row to `submissions`; "worth it" is the only value
now written, and `vote undone` still compensates it. `MyVotes.load` keeps
reading "not worth it" from history, because rows already in the table stay
true and a person who voted down last month must still see their own vote
reflected. `VoteCounts.down` stays in the model and stops being drawn.

The follow-up chips, the detail field and the thank-you lines are untouched.
The chips no longer appear automatically after a vote (they were triggered by
the thumbs down); they hang off the existing "Something's wrong" entry
points.

### 8. Rhythm

The section gap stays 28 (2026-08-26). Inside the header the name-to-summary
gap is 6. The pin ask hugs the stat row (or the ticket panel when there is
one) at 12 rather than 28, because it is a footnote to the row, not a section.

### Own trees (`mine != nil`)

The same page, which is the standing rule (Hidde, 2026-08-24: "het is dezelfde
boom pagina als onze bomen alleen dan dat de eindgebruiker de velden kan
invullen"). Every difference is a blank offered rather than a fact stated:

- **Summary line**: the species segment is the existing "What kind of tree is
  it?" button, moss with a plus glyph, opening `SpeciesChooser`. The place
  segment is the plain grey "Where you photographed it", not a link, because
  nobody has told us a city and inventing one is the thing a location field
  may never do. No count.
- **Status card** stays directly under the header, where it went on
  2026-09-01, unchanged in wording and colour.
- **Stat row**: same row, same shape. Age shows the "Add it" button when
  empty, labelled "Age" rather than "Years old" since there is no number.
  Pin as today. No girth column.
- **No ticket panel and no vote**, as today: a vote on whether your own tree
  was worth the visit is a question to nobody.
- **Story** is the existing "What makes this tree special?" blank.

### Both surfaces

The website's tree page keeps its chip row (age, species, "pin approximate")
and its ticket note; those already say things once. The count-high summary
line is app-only for now because the web hides counts entirely (DECISIONS.md
2026-08-14); if the web starts showing counts, it adopts this same line.
Girth in the feed serves both surfaces the day either wants it.

## Testing and gates

- `python3 scripts/appsweep.py` and `python3 scripts/appfit.py` on the tree
  screen (`-open`), both phones: no SMALL (the summary links and the pin ask
  need their 44 pt frames), no CLIPPED on the Kongeegen and Laburnum cases,
  no DRIFT between the name, the summary line, the stat row and the story.
- `python3 scripts/copycheck.py` on the new strings ("Approximate pin. Show
  us where it is", "Years old").
- `python3 scripts/netcheck.py` (no network change, but it runs in pre-push).
- Look at the screens: Ginkgo (short, approximate), Kongeegen (long species,
  exact, girth), Laburnum (ticket + approximate + long species), an own tree
  with no species and no age. These are the four the mockups drew.
- The two vote controls agree: cast from the summary line, and the capsule
  after the story shows it cast, and the reverse.
- `FlowWalk` still finds a way back from the tree page; the new links push
  onto the same stack as the old chip did.

## Records to write with the build

- `CONVENTIONS.md`: written already, "A detail page's facts, and a count you
  can tap (2026-09-04)".
- `DECISIONS.md` 2026-09-04: the principle (column states, link line carries
  words, panel decides the trip) and Hidde's ticket ruling.
- `LOG.md`: what changed on the page.

## Out of scope

The hero, the map inset, the story length, the access block, the
discover-more chips, the toolbar, the pinned action bar, and the web page's
layout. Height is decoded but not displayed. No new page types.
