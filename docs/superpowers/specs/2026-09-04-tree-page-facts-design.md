# Tree page: the block between the photograph and the story

Date: 2026-09-04. Decided with Hidde in session, from mockups at real phone
size (five options, real content, three trees: the Banghak-dong Ginkgo, the
Kongeegen with long values, the Leiden Laburnum with a ticket and an
approximate pin). It went through five options and then three more, and what
ships is the AllTrails page from his own screenshot of the Klompenpad
Netelenburchpad with five amendments he made while looking at it drawn:

1. **Labels on top of their values**, not under ("ik ben voor labels on top").
2. **Two columns, not three.** Age and species side by side, because that is
   the pair he named ("hoe oud is welke soort"), and the location moves to a
   full-width line inside the same block. Three columns were measured
   impossible at 393 pt: "Approximate" leaves the species 46 points.
3. **The blue ticket panel stays** as it is today, standing on its own.
4. **No girth column** ("meet the girth, dat is niet nodig").
5. **The thumbs down goes** ("i agree that we dont need a thumb down"), and
   the count in the summary line is itself the button that casts the vote.

Plus two renames that came out of the same reading: "Pin" becomes "Location"
because pin is our database field and not a word a reader uses, and a tree
somebody added themselves names its city like every other tree instead of
saying "Where you photographed it".

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
- **The place**: the existing `place` string. Tap: `navigator.push =
  .city(slug)`.

  On a tree somebody added themselves this is **the city, linked, exactly as
  on ours**. It used to read "Where you photographed it", on the reasoning
  that nobody had told us a city and inventing one is the thing a location
  field may never do. That reasoning does not hold: we hold the coordinate the
  photograph was taken at, so naming the place is READING it, not inventing
  it, and every reference does exactly that (Apple Photos, Google Photos,
  Strava and iNaturalist all label a coordinate with a place name). Hidde,
  2026-09-04: "waarom staat hier where you photographed it en niet gewoon de
  stad met link gelijk erin zoals de rest?"

  How the name is found, cheapest first: the nearest city in our own catalogue
  within 30 km (the day-trip boundary this project already uses) gives both a
  name and a page to link to. Otherwise `CLGeocoder` is asked once, at save
  time, for the locality, stored on the sighting as plain text and shown
  without a link, since there is no page to open. Offline the field stays
  empty and the segment is simply omitted, filling in on a later open.
  `CLGeocoder` is Apple's own and needs no new dependency.

  The species does NOT appear on this line. It is in the row below, and a fact
  belongs in one place per page: saying it twice is the fault Hidde caught
  three times in one afternoon (the name plus caption plus card, the ask in
  the line plus the ask in the cell, and the common name plus the Latin name
  in one cell).

Every link has a 44 pt tall hit area (`.frame(minHeight: 44)` +
`.contentShape`), which appfit measures; the text itself stays 15 pt. Hidde,
2026-09-04: "they have very small clickable stuff so apparently it can work."

### 3. The block: two columns, then the lines that need words

One bordered block holds everything between the name and the story, in this
order: the two columns, then the location line, then the ticket panel. They
are one object because they answer one question, which is what a reader needs
to know before setting off.

**The columns.** Label on top (13 pt, inkSoft), value under it, one hairline
divider between them. Age takes only the width it needs; the species takes the
rest, which is what lets "Pedunculate Oak" sit on one line where equal halves
wrapped it.

| Column | Value | Label | Notes |
|---|---|---|---|
| Age | `550-830` from `ageMin`/`ageMax`; `550` when only a minimum | Years old | brand 19 bold |
| Age | the `age` string, one line, scaled down | Age | when only a text age exists |
| Age | "Add it" button | Age | own tree, no age |
| Species | `tree.commonName` | Species | brand 16 bold moss, chevron, pushes `.species(...)` |
| Species | "Add it" button | Species | own tree, opens `SpeciesChooser` |

**No Latin name in the block.** `tree.species` carries "Ginkgo (Ginkgo
biloba)" and printing both put the same fact in one cell twice, four lines
high on the Leiden Laburnum. Hidde, 2026-09-04: "die species worden nog steeds
veel te lang, toon minder." The Latin name lives on the species page, one tap
away, which is what the chevron is for.

**No girth and no height column.** Cut on his word; the feed change is
dropped with it.

**The location line.** Full width, inside the block, above the ticket panel,
14 pt, an icon on the left:

- approximate: **"Approximate location."** in semibold, then "Show us where it
  is" underlined in moss, opening `PlacePin`. The whole line is the tap
  target, 44 pt tall.
- exact: "Exact location. The pin marks the trunk." in inkSoft, no action.

It is a line rather than a column because it is the one fact here that needs
words, and it already carries the ask. The gold panel and the separate
sentence about looking around both go.

### 4. Ticket panel

`ticketNote` keeps its wording, its blue and its glyph, and moves inside the
block as its last band, under the location line. Hidde, 2026-09-04: "i did really like the blue icon
ticket thing... it deserves a alone standing warning as it is now." It is the
one thing on this block that decides whether somebody sets off, which is the
panel's job under the principle above.

### 5. Vote: one direction only

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

### 6. Rhythm

The section gap stays 28 (2026-08-26). Inside the header the name-to-summary
gap is 8. The block is one object with no gaps inside it, its bands separated
by hairlines.

### Own trees (`mine != nil`)

The same page, which is the standing rule (Hidde, 2026-08-24: "het is dezelfde
boom pagina als onze bomen alleen dan dat de eindgebruiker de velden kan
invullen"). Every difference is a blank offered rather than a fact stated:

- **Summary line**: the city, linked, as on any tree (see 2 for how the name
  is found). No count, and no species: the species ask lives in the row.
- **Status card** stays directly under the header, where it went on
  2026-09-01, unchanged in wording and colour.
- **The block**: same two columns. Age and species each show an "Add it"
  button when empty, and the age label reads "Age" rather than "Years old"
  since there is no number. The location line reads "Exact location" because
  the pin is where they stood. No ticket panel.
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
- `python3 scripts/copycheck.py` on the new strings ("Approximate location.",
  "Show us where it is", "Exact location. The pin marks the trunk.",
  "Years old").
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

## The rule this page now follows

Written down because it decided every question above, and because a session
that forgets it will re-add a fact in a second place within a week:

**A column states a short value. A line carries words. A panel is for
something that decides whether you set off at all. And a fact appears exactly
once per page.**

## Out of scope

The hero, the map inset, the story length, the access block, the
discover-more chips, the toolbar, the pinned action bar, and the web page's
layout. Girth and height stay out of the feed and off the page. No new page types.
