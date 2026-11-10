# Compliance review, every seven days

Due, not on a weekday, like the code review. review.yml runs it when the newest `## YYYY-MM-DD compliance` heading in REVIEW.md is seven or more days old, or there is none.

Hidde, 2026-11-10, after asking for a lawyer's audit himself ("wees een lawyer en geef ons een audit"), which found the privacy page six weeks behind the product: "hoe zorgen we dat er om de zoveel tijd een compliancy check is want ik vraag dit nu random". The mechanical half runs on every push (scripts/privacycheck.py: every table, service and GDPR must named on the privacy page). This is the human half: are those sentences still TRUE, and did anything this week create a new legal question.

You review; you never fix product or copy. Write only REVIEW.md, data/compliance.json and one line of LOG.md.

## What to read

- What changed in the last seven days: `git log --since=7.days --stat -- supabase site/src ios/AncientTrees/AncientTrees scripts/mailer.py scripts/outreach_compose.py`, and DECISIONS.md and LOG.md for the same days. A new table, a new field shown to other people, a new mail, a new service, a new kind of photo or text from outside: those are what this review is for.
- site/src/pages/privacy.astro and site/src/pages/terms.astro, whole, against what the week's changes do. Every sentence that is no longer true is a finding.
- data/compliance.json first: an open row is not reported again, and a `declined` row is NEVER raised again, in any wording, unless the product itself changes in a way that makes it worse (Hidde, 2026-11-10, declining the 33 accounts made public on 2026-10-29: "dit risico accepteer ik negeer dit vanaf nu").

## What to look for

- **Privacy (GDPR, the Dutch Telecommunicatiewet)**: personal data shown to more people than before, a default that opens rather than closes, data kept without a stated period, a new processor (a service that receives reader data), tracking on a device without consent, anything a deleted account leaves behind other than what the terms name.
- **Copyright and database rights**: a photograph without a recorded open licence or written permission, a credit that drops the author, licence or source the licence asks for, text copied from a source rather than written from it, a register imported without a licence verdict in OPEN_DATA_SURVEY.md, anything from monumentaltrees.com beyond a fact.
- **Given photos and words**: a photo someone mailed us that went up without their yes (qa refuses one without `permission`; check the week's new ones are real yeses, not filled in to pass), a sentence from a mail quoted on a page without `quote_ok` in data/outreach-words.json.
- **Mail**: a first mail without a way to say no (mailcheck refuses it; check that the drafted batches pass), an address not published by its owner, a person mailed again after saying no.
- **Promises**: copy that promises what the product does not do, or "free forever"-type claims (CLAUDE.md, What this is).
- **Children and safety**: anything that invites a reader onto private land or to harm a tree (hard rule 10, the stories rule).

Verify by reading the code or the page; three real findings beat ten guesses. Say which law or licence clause each one touches, in a few words.

## Where it goes

1. data/compliance.json, one row per new finding: `{"id": "<short-slug>", "owner": "hidde|session", "first_seen": "YYYY-MM-DD", "status": "open", "summary": "<one sentence>", "law": "<the rule it touches>", "fix": "<one sentence>"}`. `hidde` when it needs his decision (a default, a policy, a mail he sends), `session` when a session can fix it without him (a sentence on the privacy page that is no longer true, a missing credit link).
2. REVIEW.md, at the top, under `## YYYY-MM-DD compliance` (the next due date is read from this heading, so write it even when nothing is found): one line per new finding, its id and summary. Nothing new: the heading and "Nothing new."
3. LOG.md, one line at the top of today's entry, only when there is a new `hidde` row: `For Hidde: compliance review, <n> point(s) wait for your word (data/compliance.json).`
4. Commit those files only, message `Compliance review: <n> new finding(s)`, and push (`git pull --rebase` and push again when main moved).

## Who acts on it

- `session` rows: the night run at rung 2 when the fix is a sentence on the privacy or terms page that is plainly false (rewrite it to what the product does, run `python3 scripts/privacycheck.py`, set the row fixed with the commit). Anything else waits for a session.
- `hidde` rows: never a run. They keep the quality line orange until he decides; the session that discusses one with him records his words in the row.
