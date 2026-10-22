---
name: product-copy
description: Write or change any sentence a visitor reads inside the product (website UI strings in site/src/lib/i18n.ts, text in .astro components and pages, the iOS app's Text/Label/Button strings, empty states, sheets, cards, settings rows, app pitches). Use whenever such a string is added, rewritten or checked, including "pas de tekst aan", "deze zin loopt scheef", "klinkt als AI", "copy for the button/card/sheet", and before showing new UI copy to Hidde. Not for tree stories (TONE_OF_VOICE.md) or mails (reply-mail).
---

# Product copy

A sentence in the product tells a person what they can do, in the words a person would use. The machine-written shapes slip in because they sound finished. This skill is the order to work in; the rules themselves live in the files below.

## 1. Read before writing

- `PRODUCT_COPY.md`, whole file (short). The five rules and the bad/good pairs.
- For copy a stranger reads to decide whether we are interesting (app pitch, store text, the /app page, a hero line): the PAIRS in `drafts/PITCH_VOICE.md` as well.
- The strings around the one you are changing, in the same component. Match their length and voice.

## 2. Write it once, plainly

- The reader is the subject. Say what they get, then stop.
- Use the product's own verbs: find, walk, save, tick off, collect. "The ones you visited", never "the ones you have stood in front of".
- Every claim must be true of the product today (an ask the reader cannot do is false). No count typed into a string.

## 3. The de-AI pass

Read it aloud as a stranger holding a phone and cut:
- a list held back behind a colon so the name lands as a reveal ("X, Y and Z: the Ancient Trees app"). Name it first.
- a moral or summary after the point ("That is how...", "That's the idea").
- defining by denying ("not a map, just..."), "whether you're...", a padded group of three.
- a pronoun whose noun is in another component ("Walk them" on a card that never said what "them" is).
- abstract nouns where a verb would do, stacked "of the ... of the".
- anything that talks about us: our data, our process, what we are building.

If a shorter sentence says the same thing, take the shorter one.

## 4. Every language in the same change

Change the English in `UIStrings` (site/src/lib/i18n.ts) and rewrite es/it/nl/de/pt/fr/ja from the new meaning, not word for word from the old translation. Nothing typed into markup. When the app shows the same thing, change its string in the same change.

## 5. Check and look

- `python3 scripts/copycheck.py` (both surfaces; it also runs after every edit and before every push).
- For pitch copy: `python3 scripts/pitchcheck.py --text "..."`.
- Render it and look at it at 375px before calling it done (eyes rule).

## 6. When Hidde says a sentence is off

Record it before the next reply: if the shape can be grepped, add it to `AI_SHAPES` or `TICS` in scripts/copycheck.py with his words in the comment; otherwise add the pair to PRODUCT_COPY.md. Then grep the product for the same shape and fix every copy of it, not only the one he saw.
