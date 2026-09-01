// The site-wide tree count, generated and rounded DOWN.
//
// Hidde, 2026-08-23, on putting a number in the app pitch: "en die aantal
// trees gaat natuurlijk de hele tijd omhoog dus hoe doen we dat." Three
// rules, and the second is the one that is easy to get wrong.
//
// 1. NEVER TYPED. It is counted at build time from the same predicate the
//    pages themselves render on, so a night run that adds nine trees moves
//    the number on the next deploy. Hand-typed counts are exactly the error
//    count-promises.ts already guards per city: Florence went to fifteen with
//    three sentences still promising ten.
//
// 2. ROUNDED DOWN, with "over" in front, which is what AllTrails does
//    ("Search over 500,000 trails"). Two reasons, both stronger for us than
//    for them. A rounded-down claim stays TRUE on a cached page, in a
//    screenshot somebody forwards, or in a mail sent three weeks ago. And the
//    sentence stays stable: "Over 1,800" survives until we pass 1,900, so the
//    same string can also be pasted into the App Store listing and outreach
//    mail, which are the two places nothing can generate it for us.
//
// 3. GUARDED. check_tree_count_claims() in scripts/qa.py fails the build on a
//    rendered number followed by "trees" that overstates the real total, so
//    the next person to type one by hand finds out immediately.
import { getCollection } from "astro:content";
import { cityIsRenderable, renderableTrees } from "./trees";

/** Every tree that actually has a page. */
export async function totalTrees(): Promise<number> {
  const cities = (await getCollection("cities")).filter(cityIsRenderable);
  return cities.reduce((n, c) => n + renderableTrees(c).length, 0);
}

/** The count rounded down to the nearest hundred: the number a claim may
 * safely quote. Returns 0 below one hundred, where rounding down says
 * nothing and the caller should print the exact figure instead. */
export async function roundedTrees(): Promise<number> {
  const n = await totalTrees();
  return n < 100 ? 0 : Math.floor(n / 100) * 100;
}

/** "1 tree" / "7 trees". Written 2026-09-01, when nineteen one-tree places
 * went live in a day and every one of them rendered "1 Trees Worth Visiting"
 * in its title tag and "1 trees on the map" over its map. Philadelphia had
 * been reading that way since it opened with Bartram's Ginkgo and nobody had
 * looked. The 2026-08-31 exception makes one-tree places ordinary rather than
 * rare, so the count needs a plural rule rather than nineteen ternaries. */
export function nTrees(n: number): string {
  return `${n} ${n === 1 ? "tree" : "trees"}`;
}
