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

**Only what actually ships is named.** Walks, the season story and anything
Plus sit behind flags that are off for every real user (Kit/Launch.swift), so
the mail says trees around you, why it is worth the walk, ticking one off, and
adding one with a photograph. Nothing else.

One line still says iPhone only, because this group never told us what phone
they hold: some of them are on Android and would otherwise be left with a link
they cannot use.

Counts checked today: 2,884 trees across 565 places. Store id 6806177833.

To: the `waitlist` rows with `created_at < 2026-09-03T14:16:33Z`. This session
has no service key, so pulling them is yours or a run's that has one.
Subject: Ancient Trees is out

---

Hi,

You left your address to hear when the app was ready. It is out:

https://apps.apple.com/app/id6806177833

Open it and it shows you the remarkable old trees around you, what you are looking at, and why that one is worth the walk. You can tick off the ones you have stood in front of, and if you find a tree we are missing you can add it with a photograph.

It is iPhone only so far. If you are on Android you stay on the list, and I will write again the day that one exists.

2,884 trees in 565 places, and more every week. If you would rather not hear from me again, say so and I will take you off.

Hidde
https://ancienttrees.app
