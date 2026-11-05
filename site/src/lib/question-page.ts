// Contract B's one rule about WHICH cities get a question page, in a module
// with no Astro dependency so both users can import it: the page routes and
// the city pages that link to them, and redirect-map.ts, which runs as a
// build integration before Astro's content collections exist and so cannot
// import trees.ts. Same reasoning as slug.ts, and for the same reason: two
// copies of one rule is how a fix lands in only one of them.
//
// Why the rule exists (Hidde, 2026-09-17, on the Search Console report of 36
// pages crawled and not indexed): a question page needs a question. With one
// tree in the place there is no choice to make, so /lebec/oldest-tree, the
// Lebec city page and the Peter Lebeck Oak's own page were three URLs
// paraphrasing one oak, and Google indexed one and filed the other two. That
// is Google reading it correctly. 328 of 609 published places held exactly
// one tree on the day this was written, so the pattern was ~650 surplus URLs
// spending the crawl budget of a site with no backlinks.
//
// His ruling, and the shape of it matters: "ze verdienen ze niet - maar
// uiteindelijk komen er meer bomen in grote steden - in afgelegen plekken
// weghalen". So the rule is keyed to the tree count rather than to a list of
// places: a place that grows to a second tree gets its question page back on
// the next build, with no list anywhere to maintain and nobody to remember.

/** Renderable trees a place needs before "what is the oldest tree here" is a
 * question rather than a restatement of its only tree page. */
export const QUESTION_PAGE_MIN_TREES = 2;

/** Does a place with this many renderable trees publish a question page?
 *
 * The English page, the seven translated ones, and the links on the city and
 * tree pages all ask this, so they cannot drift apart. Note the tree page's
 * chip has asked `allTrees.length > 1` since long before this rule was
 * written, which is the same line; it now reads it from here.
 */
export function cityHasQuestionPage(renderableTreeCount: number): boolean {
  if (QUESTION_PAGES_OFF) return false;
  return renderableTreeCount >= QUESTION_PAGE_MIN_TREES;
}

/** QUESTION PAGES OFF (Hidde, 2026-11-05: "de website hard terugtrimmen").
 *
 * Google took the site back on 11-04 after three days of showing it again,
 * open and tagged pages alike: a site-level judgement, and the clean-up of
 * October had not reached it because Google reads this site at ~145
 * requests a day and a noindexed page still costs one of them every round.
 * A page that does not exist costs nothing. The 439 question pages (English
 * and seven languages) repeat their city page's FAQ, and every one of them
 * has carried the robots noindex since 2026-10-01, so nothing a reader can
 * find changes: the FAQ stays on the city page, and every question URL
 * redirects to its city page (redirect-map.ts; hard rule 3, no URL dies).
 * scripts/thin_pages.py reads this constant from the file, so the noindex
 * list stops naming pages that no longer exist. False brings them all back
 * on the next build; the switch is Hidde's. */
export const QUESTION_PAGES_OFF = true;
