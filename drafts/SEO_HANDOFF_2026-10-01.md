# SEO handoff, 2026-10-01

## What happened
On 2026-09-28 Google stopped showing ancienttrees.app almost entirely. Impressions went from ~1,900-2,400 a day to 53 (09-28, now FINAL data), 52 (09-29), and Google visitors in our own Cloudflare beacon went from 30-130 a day to **0** on 09-28, 09-29 and 09-30. Total visits held (~180-350/day) because they are mostly direct and /open.

## What was ruled out (evidence: `.github/workflows/seo-diagnose.yml` run 36806675839, plus Hidde's own checks)
| Check | Result |
|---|---|
| Reporting lag | No. 09-28 is final at 53. |
| Manual action | None (Search Console, "Geen problemen gedetecteerd"). |
| Crawl / host | Crawl stats: no host problems, 97% 200 OK (export only runs to 09-15). Robots.txt fine, Googlebot UA gets the same 200 pages. |
| Indexing | URL Inspection on 10 pages: all "Submitted and indexed", /prague crawled 09-29, canonicals correct. Sitemap read 09-27, 0 errors. `site:ancienttrees.app prague` returns our pages. |
| Our own changes | No robots/noindex/canonical/redirect change shipped 09-25 to 09-28. |
| Breadth | Every country, device, top page and query kept 0-2% of impressions. |

**Conclusion: sitewide algorithmic demotion, pages indexed but not ranked.** "ancient trees prague" no longer shows us. Leading suspect: Google's September 2026 spam update (rollout from 09-24, up to two weeks, so until ~10-08), policy most likely **scaled content abuse**.

## Why scaled content fits
- 716 places, **456 with 1-3 trees** (the single-famous-tree exception became most of the site).
- 12,923 page URLs: per place a city page, an oldest-tree page, tree pages, and **7,019 "fallback" language pages** (`/de/<city>`, `/es/<city>/arbol-mas-antiguo` etc.) that repeat the English text on a second URL with canonical to English, linked from the language switcher. Tree-page fallbacks were already removed 2026-09-17 (`allTreePathsFor` in site/src/lib/i18n.ts); **city and question fallbacks still exist** (`allCityPathsFor`, `allQuestionPathsFor`).
- 525 trees on one or no source.
- Secondary suspect: ~300-domain spam link network since 2026-07-24 (Google says it ignores these).

## Done in this session (all on main)
| What | Where | Status |
|---|---|---|
| Ondategi tree name was 62 chars and broke every build/deploy/review since 09-28 | data/cities/ondategi.json, `check_tree_name_fits_a_title()` in preflight | fixed, deploys green since 09-30 |
| Digest lost on a push race | data-digest.yml retry loop | fixed |
| US only for new work | passcheck.py `US_ONLY`, city_queue.py --next, BRIEF_RESEARCH.md (one credible source in the US), CLAUDE.md | live |
| Run budget raised | run_health.py: week 8000, day 1440 | live |
| No new places below four trees | `check_no_new_thin_places()` in preflight, data/thin-places-frozen.json (456 grandfathered), CLAUDE.md pause note | live |
| Noindex proposal | scripts/thin_pages.py -> drafts/noindex-proposal.md, data/noindex-proposal.json | **proposal only, not wired, needs Hidde's yes** |
| IndexNow for Bing/ChatGPT | scripts/indexnow.py, .github/workflows/indexnow.yml, key file site/public/81e2b7f644c7a01071949732c4937da8.txt | runs after each deploy; **full first submission still to do**: dispatch indexnow.yml with all=true once the key file is live (check-in trigger trig_015u7nVwcspRxjtqibzeFjrg fires 04:11 UTC into the old session) |
| Disavow converter | scripts/disavow.py | needs the Search Console Links export |
| Google visitors per day in the digest | daily_digest.py fetch_rum, "From Google" column | from the next digest |
| SEO diagnosis on demand | scripts/seo_diagnose.py, seo-diagnose.yml (workflow_dispatch) | rerun weekly to track recovery |

## Noindex proposal (data/noindex-proposal.json)
| Group | Pages |
|---|---:|
| A. Places with 1-3 trees (451) + their translations | 1,039 |
| B. Real translations of cities whose English twin earns <10 impressions | 98 |
| C. Fallback language pages (English text on a /de/ ... URL) | 7,019 |
| Total, deduplicated | 8,156 of 12,923 |
Correction to apply: Sao Paulo is kept as "earning" (277 impressions) but those are the bot query "peesten municipality 2019"; move it into group A.
Wiring it means a `<meta name="robots" content="noindex">` via Base.astro `headExtra` for listed URLs, excluding them from the sitemap, and touches SEO_GEO_BLUEPRINT.md contracts (hard rule 7: Hidde's yes). Recommended order: group C first (pure duplicates), then A, then B. Alternative for C: stop generating city/question fallbacks entirely like tree fallbacks were on 09-17, but that retires URLs (hard rule 3), so noindex first.

## Open items for Hidde
1. Yes/no on the noindex list (start with group C).
2. Bing Webmaster Tools: sign up, import from Search Console.
3. Search Console -> Links -> export "Top linking sites" -> `python3 scripts/disavow.py export.csv` -> upload drafts/disavow.txt at search.google.com/search-console/disavow-links.
4. Decide what "no months to wait" means (money, date, motivation): it sets how hard to lean on non-Google channels (Bing/ChatGPT, App Store, tree societies, Reddit; drafts only, he sends).

## Recovery expectations
No reconsideration request exists without a manual action. Typical path: clean up now, Google recrawls over weeks (crawl was 50-500 requests/day for ~6k sitemap URLs), the demotion lifts at a later update, often months. Partial recovery is common, full is not guaranteed. Watch: the rollout until ~10-08 (can shift either way), the digest's "From Google" column, and head queries ("ancient trees prague", "oldest tree in lisbon") returning.
