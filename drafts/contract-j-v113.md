# Proposed: SEO_GEO_BLUEPRINT.md v1.13, Contract J widened

**Status: drafted, NOT applied.** Hard rule 7 says changes to that document
need Hidde's explicit approval and a version bump. This file is the diff
waiting for a yes, so applying it is one edit rather than a rewrite.

**Why now.** Contract J was written 2026-08-10 as a single-city Spanish test.
That test is answering: /es/malaga went from 14 to 132 impressions in six
days, took its first clicks on 08-21, and sits at position 15 on the query
its English twin sits at 75 on. Hidde asked to widen it to six more
languages to find out which are worth investing in.

## The change, in three lines

1. Drop "(v1.10, test scope)" from the heading. The contract now covers any
   `/{lang}/{city}` set, not `/es` alone.
2. Add the per-language question slug table, since `/oldest-tree` must not
   appear as an English path segment in a translated URL. Currently only
   `es: arbol-mas-antiguo` exists in `site/src/lib/i18n.ts`; the other six
   need writing before their first page can build.
3. Name the known debt rather than leaving it silent, which is what the
   existing contract already asks for: site chrome, map popups and the
   season block stay English until a language earns a rollout.

## The languages, and why each is in

| Lang | Cities | Trees | Local-language share of English Wikipedia views | In both AllTrails and komoot |
|---|---:|---:|---:|---|
| es | 14 | 178 | 34% (Barcelona) | yes |
| it | 24 | 281 | 44% (Rome) | yes |
| nl | 16 | 218 | 18% (Amsterdam) | yes |
| de | 9 | 145 | 53% (Vienna) | yes |
| pt | 8 | 100 | measured via Lisbon | yes |
| fr | 6 | 83 | measured via Paris | yes |
| ja | 5 | 53 | 45% (Kyoto), 80% (Fukuoka) | komoot only |

Evidence behind the shares: `data/research/language-demand.json`.

## The measure, recorded BEFORE anything is built

This is the half that made the Malaga test worth running, so it is repeated
rather than assumed:

- Within four weeks of indexing, the translated set exceeds its English
  twin's impressions. Malaga did it in eleven days, 132 against 80.
- And its position on the target-language query beats the English page's.
  Malaga: 15 against 75.
- A language that fails both on two cities gets no rollout, however large
  its supply. Written down now so a good story cannot rescue it later.

## What this does NOT change

Same bars, same numbers: intro 60-100 words, stories 150-250, title max 60,
descriptions max 155, no em dashes, answer-first on the question page.
Hand-written in the target language; mechanically patched text stays
forbidden. Translation stays an overlay, so every coordinate, photo, licence
and walk lives only in the canonical English city file.

## The honest caveat on Japanese

Nobody on this project can read Japanese. The FACTS are safe, because the
overlay carries no coordinates and makes no new claims: it renders a file
that was already verified in English. The PROSE is not checkable by us, so
bad Japanese would ship unnoticed in a way bad Italian would not. Hidde was
told this and asked for Japanese anyway, which is his call to make; it is
recorded here so nobody rediscovers it as a surprise.
