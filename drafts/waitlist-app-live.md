# FOR HIDDE: the waitlist mail, owed since 3 September

LOG.md 2026-09-03 recorded this as yours and the draft as mine, and the draft
never got written. This is it.

**Who gets it, on his ruling of 2026-09-10: only the rows from before the
Android rename.** The device-aware form landed in commit 71244a79 at
2026-09-03T14:16:33Z and deployed minutes later. Everything before that moment
was collected under a general "we will tell you when the app is out", and that
mail is now a week late. Everything after it saw copy that promises a mail the
day an ANDROID app exists, and the iPhone app being live is not that. The
newest row is about four days old, so that half is real and it is not ours to
mail yet.

**The cut is `created_at < 2026-09-03T14:16:33Z`, not the `source` field.**
Source looks like the obvious discriminator and is not trustworthy here:
commits 04af8338 and 49865e1b, both from that same afternoon, record two submit
listeners racing on /app and writing different sources for the same submit,
absorbed silently by the table's unique-email constraint. The timestamp has no
such history.

**The text is his, rendered rather than rewritten (2026-09-10).** He supplied
the substance in his own words and HIS_VOICE.md says what to do with that: he
writes it, I render it. So the shape, the two "supers", the thanks, the ask
back and the honest Android sentence are all his. What I added is the link and
the capitals.

Gone with it: the feature paragraph and the counts. These eleven signed up for
this app and know what it is, and his letter asks them a question instead of
selling them the thing they already asked for.

No opt-out line, matching batch-010-app-launch, which carried none either. At
eleven addresses with a real reply address and a sentence asking them to write
back, this is a letter rather than a mailing.

The link is the store rather than /app, because his own first sentence says
iOS, so nobody is misled, and the people who can install it get one tap.
Store id 6806177833.

To: the `waitlist` rows with `created_at < 2026-09-03T14:16:33Z`, pulled by
`python3 scripts/waitlist_batch.py`. It writes the batch and sends nothing;
outreach_send.py does the rest and refuses any batch not marked
`approved_by_hidde`.
Subject: Ancient Trees is out

---

Hi,

We are super happy to announce that the first version of the app is live on iOS:

https://apps.apple.com/app/id6806177833

Thanks so much for subscribing. It gave the confidence to put more effort into making this tree app.

It is only the first version and we are super curious what you think. What you miss, what you don't like. If anything comes up, let us know and we can improve it. Let's keep in touch.

We are working on the Android version too, but in all honesty it will take a while before that one is finished.

Hidde
https://ancienttrees.app
