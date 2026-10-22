---
name: reply-mail
description: Draft a reply to somebody who wrote to Ancient Trees (outreach replies in Hidde's inbox, a reader's submission that gets a reply_text, a contributor, press, an organisation). Use whenever a mail, reply, answer or "antwoord" to a person is drafted, rewritten or checked, including "lees de inbox", "beantwoord", "maak een concept", "reply to", and before any reply is shown to Hidde or sent.
---

# Reply to a person

The rules for a reply already exist; this skill only makes sure they are all read, in order, every time. The voice is his, not ours: drafts/HIS_VOICE.md holds his own mails verbatim. Read it in full before the first draft of the session and imitate by proximity, never from the summary below.

## 1. Read before writing

- `drafts/HIS_VOICE.md`, whole file. "THE SHAPE OF A REPLY" and the calibrations at the bottom are the target.
- The thread itself: `source ~/.ancienttrees-mail.env`, then `python3 scripts/outreach_inbox.py --list` (subjects only), then `--read`. Reader submissions: `python3 scripts/inbox.py`.
- What we already sent this address: data/outreach-sent.json (after `python3 scripts/private_store.py sync`). If a tree ask already went out in this thread, this reply does not ask again.
- Every tree they name: look it up in data/cities/ and data/leads/. Know whether it is live, at which URL, and what it lacks to go live.

## 2. Do first, then write

If they corrected us or gave us a tree, change the site first and reply "it is on the page now" with the link. A local expert's account goes on the page as a local account; never argue with them.

## 3. The shape (four to six lines, under 150 words)

1. Thanks and the answer in one line. Thank separately for each thing they gave; close with "Thanks again" when they gave a lot.
2. What changed, as fact. At most one short sorry inside a sentence.
3. Something true about us only if they raised it. Asked which trees we pick: his standard line (HIS_VOICE.md, 2026-10-22).
4. One ask, last, plain, fitted to the person: a tree they know (where exactly it stands, a photo if they walk past), an introduction, a link only in a later reply after their help was used. Drop the ask when they have already given or it was asked earlier in the thread, When they say they are busy or cannot help much: no task for them, but his form instead: "I completely understand", the ways anyone could help as options, "either way, thanks" (HIS_VOICE.md, 2026-10-22).
5. Out. No summary, no promise of what happens next.

Language: theirs. Capitals as any decent letter. "Sie" stays "Sie". Baarn is "zo'n 30 minuten onder Amsterdam". Sign "Hidde" only on a draft he will approve; automated mails are signed Ancient Trees.

## 4. Never

- An App Store link or "what do you think of the app" in a reply (2026-10-15, "verkoopachtig"); in reader mails at all.
- The offer you are declining, written down. Answer what you want, let the rest pass.
- A sentence about what we did not do, unless they said we did.
- How we verify, our method, our progress. never / always / forever / free for. Price, app dates.
- Facts about their own city or field that they know better than we do.
- A task for a volunteer (measuring, permission forms), a link to /contribute.
- A reader's name anywhere public.

## 5. The de-AI pass, before mailcheck

Read the draft once as the recipient and cut:
- sentences that announce the next sentence or explain why a compliment is deserved,
- reassurance nobody asked for (the "anyway" tell),
- the same idea said twice, curatorial words where he would say "cool trees",
- anything over 60 percent of the length that feels right.

Then `python3 scripts/mailcheck.py <draft>` and rewrite until clean. For pitch copy (press, App Store, first mails) also `python3 scripts/pitchcheck.py <draft>`.

## 6. Show it

Write the draft to drafts/reply-<name>-<date>.md: notes for Hidde above a `---` line, the mail body below it (mailcheck reads only the body). In chat, quote the person's latest mail in full, translated to English unless it is English or Dutch, then the draft. His "verstuur" on that text means send now: follow drafts/OUTREACH.md and scripts/outreach_send.py (approved_word set in the same step as the send, never before).

## 7. When he corrects a draft

Record it before the next reply: a mailcheck pattern if it can be grepped, otherwise a dated section in drafts/HIS_VOICE.md with his words. Not a memory note.
