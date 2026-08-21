# Contributor reply loop — design

Date: 2026-08-21. Ruled by Hidde in session: "this process of user giving
input is one of the core features of our platform and must be treated with
care - we should thank them ask out their email if they want to give and give
back to them what we changed." The Toulouse elm correction of 2026-08-20 is
the case that proved the gap: a reader argued leaf hairs with us, was right
about the tree they looked at, improved the page, and never heard back.

## What this is

Close the loop on reader input, in two mails:

1. **The thank-you**, automatic, within a couple of hours of a submission
   that carries an email address. Templated. Thanks them, says what we are
   building together, promises we will look into it and come back, invites
   more input.
2. **The result**, written by the run that processes the submission, from its
   own verification record. Says what their input changed, or what we checked
   and why nothing changed. Sent the same way.

Both from press@ancienttrees.app as "Ancient Trees", never as Hidde
(hard rule 4; same model as outreach, approved 2026-08-08: the machine
writes, sends and logs). Standing approval for these two mail kinds was
given by Hidde in this session: they are warm replies to a person who wrote
to us first and asked to hear back.

## Form changes (site/src/pages/contribute.astro)

- New optional `email` field. Label: "Want to hear what your tip changed?
  Leave your email and we'll tell you. We use it for nothing else."
- Double-submit fix: disable the submit button on press, show the sending
  state on the button (convention; the Toulouse correction arrived as three
  identical rows because nothing stopped the extra presses).
- The worth-it thumbs stay frictionless: no email ask there (convention:
  Google Maps and AllTrails ask nothing on a thumb).

## The worth-it control (site/src/components/WorthIt.astro)

Hidde, same session: accidental thumbs must be undoable, and a
thumbs-down should surface the why-options. This REVISES his 2026-08-16
split ruling knowingly, via the post-rating-follow-up convention (app
stores, Uber): the vote stays complete on its own, the why is optional
and appears after, so nobody is interrogated to vote and nobody with a
reason has to hunt.

- **Thumbs are toggle buttons with a visible selected state** (his words:
  "buttons to press and than it selects and than unpress"). Press: counts
  and shows selected, persisted per browser as today. Press again:
  unselects and undoes. Press the other thumb: switches the vote.
- **Undo writes a compensating row** rather than deleting anything: same
  table, naming the direction it cancels ("vote undone: not worth it"),
  so whoever counts votes subtracts it from that tree's tally. No RLS
  change, no anonymous deletes. The digest and Step 0b treat undo rows as
  bookkeeping, never as feedback to verify.
- **After a thumbs-down only**, the existing "What's wrong?" chips unfold
  as an optional "Care to say why?": three fault chips, "Something else"
  to the prefilled form (where the email field and reply loop begin), and
  a plain dismiss. The vote already counted; touching none of it is fine.
- The standalone "Something's wrong" button stays: an up-voter with a
  wrong pin still needs a way in that is not a down-vote.
- Per-change eyes rule applies when built: rendered, 375px and desktop.

## Mail 1 copy (template, final unless Hidde edits)

> Subject: Thank you, we received your tree tip
>
> Thank you. Your input is very valuable: a real person telling us about a
> real tree is the best thing this project receives. Together we're building
> the best database of remarkable trees there is, and the point of it all is
> getting people outside, standing in front of something old and epic.
>
> We check everything against independent sources, so give us a little time.
> We'll come back to you with what your input changed. And please feel free
> to send more: a tree you love, a correction, a photo. They all make the
> map better.
>
> Ancient Trees, ancienttrees.app

Subject varies by kind: tip / correction / feedback. No em dashes, no
forever-promises, no builder-speak, mailcheck.py greps it before sending.

## Mail 2, the answer: three outcomes, never a dismissal

Ruled by Hidde in the same session: "even if we're not sure i think we
should email back with questions rather than dismissing it." So the run
that processes a submission records an `outcome` (new column on
submissions) and the mail follows it:

- **changed**: "Your input changed the page", what changed, the link, the
  invitation to send more.
- **holds**: the checks confirmed our data. Never worded as "you were
  wrong": the mail shows the work and turns it into a question, because
  the reader stood there and we never have. The Prague pattern: here is
  the register entry and the matching coordinate; what made the spot feel
  wrong; a photo would settle it.
- **open question**: sources cannot settle it. Ask for the specific
  missing piece (which of the two elms, a trunk photo, a girth).

Their answer comes back through a link in the mail to /contribute,
prefilled with the tree, so the thread flows into Supabase where runs
already look. A plain email reply lands in the press@ mailbox, which only
Hidde reads; he forwards it into a session. No run ever reads his mail.

Every exchange is logged in the tree's verify_notes so the next run
continues the thread, and a second report on an already-checked tree
reopens the question (the Prague run's own stipulation, now a rule).

Composed per submission from the verification record, one short specific
paragraph. mailcheck.py gates it like any outreach draft. The processing
rules themselves (Step 0b) are unchanged: verify first, never treat a
claim as fact. Submissions without an email still get the full
verification; the page change is their answer.

## Sending mechanics

- New script `scripts/contributor_reply.py`, reusing outreach_send.py's
  guardrails: dry-run default, sent-log, do-not-contact list beats
  everything, daily cap shared with outreach.
- State per submission row: `thanked_at`, `replied_at` (columns on the
  submissions table), so no reader is ever mailed twice for one row and a
  re-run is safe. Double-submit duplicate rows (same day, kind, tree, city,
  text) get one thank-you, not three.
- Runs at each night knock and at the digest, so the thank-you lands within
  roughly two hours. No mail service enters the product (hard rule 5): the
  site keeps posting to Supabase exactly as today.
- FOR HIDDE, the one thing only he can do: put the OUTREACH_SMTP_* secrets
  into GitHub Actions so CI can send; they live only on his machine today.
  Until then the script runs in his sessions and queues honestly in between.

## Personal data (hard rule 1)

His ask in this session is the explicit yes for one new personal-data
column: `email` on submissions. Bounds, all binding:

- Used only to reply about that reader's own submissions. Never rendered,
  never for marketing, never shared.
- Deleted on request; the privacy page gains one factual sentence stating
  what we store and why, in the page's usual plain voice.
- The never-publish-a-name rule is untouched.

## QA

- mailcheck.py gates both mail kinds.
- The form change gets the per-change eyes rule: looked at rendered, 375px
  and desktop, before reporting done.
- Digest: the thank-you/reply counts join the night-shift accounting via the
  sent-log, no new table.

## Both surfaces (the 2026-08-21 rule, applied to this feature)

The principle is one loop on web and app alike: input is thanked, verified,
answered, never dismissed. Per surface:

- **Contribute + email field**: the app's contribute screen (`-contribute`)
  gets the same optional email field with the same label, posting to the
  same Supabase table, in the same build pass as the web form.
- **Worth-it thumbs**: the app has NO vote control today (checked
  2026-08-21: TreeDetail only mentions the idea in a comment). It arrives
  with this build, born with the toggle design (select, unpress to undo,
  down-vote unfolds the optional why-chips), native in form, identical in
  behaviour, on the tree detail screen where the web shows it. The screens
  it lands on are ones appsweep already photographs.
- **The mails** are surface-independent by nature: one reply loop,
  whichever surface the submission came from.

## Out of scope

Accounts for contributors, an inbox, threading beyond one reply per
submission, instant (in-product) mail, email on the worth-it control.
