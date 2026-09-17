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
  return renderableTreeCount >= QUESTION_PAGE_MIN_TREES;
}
