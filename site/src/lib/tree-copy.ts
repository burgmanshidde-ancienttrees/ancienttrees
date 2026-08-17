// Small text-derivation helpers ported from build_site.py:927-961, 2433-2437, 2782-2789.
import { DESC_MAX, DESC_MIN } from "./site-config";
import type { Tree } from "./trees";

/** The number a page's title quotes for this tree's age: the figure the
 * age_estimate text itself states, even when a qualifier ("roughly", "over",
 * "traditionally") comes first. Falls back to age_min, or null when neither
 * source gives a real number, matching build_site.py's post-2026-08-09
 * age_token() (origin/main 2d7ffbc): `age_min = tree.get("age_min"); return
 * str(age_min) if age_min else None`. Callers must guard on this being
 * truthy before building a "N Year Old" title candidate — the earlier
 * version of both this function and its callers had no such guard, which is
 * how three published pages shipped with the literal text "None Year Old
 * Tree" when age_min was explicitly null (an f-string interpolating Python's
 * None object). Fixed at the source now, not papered over in the title. */
export function ageToken(tree: Tree): string | null {
  // Every number in the sentence, not just the first, and then the one that
  // is actually an AGE. Taking the first match shipped a planting year as an
  // age on 70 trees across 30 cities: Boston's Shaw Memorial Elms read "1772
  // Year Old English Elm" from the string "planted between 1772 and 1812, so
  // roughly 214 to 254 years old", and Rome's hackberries read "1600 Year
  // Old" for a tree its own data puts at 300-400. Caught by the fresh-eyes
  // reviewer on 2026-08-10, live, and made louder that morning when the city
  // page titles started quoting this same function.
  //
  // age_min/age_max are the tree's own bounds and are the arbiter: prefer a
  // number from the sentence that falls inside them, fall back to age_min
  // when the sentence offers no such number, and only trust the raw first
  // match when the tree carries no range at all.
  const nums = [...(tree.age_estimate ?? "").matchAll(/(\d[\d,]*\+?)/g)].map((m) => m[1]);
  const lo = tree.age_min ?? null;
  const hi = tree.age_max ?? null;
  if (lo || hi) {
    const inRange = nums.find((n) => {
      const v = parseInt(n.replace(/[,+]/g, ""), 10);
      return (!lo || v >= lo) && (!hi || v <= hi);
    });
    if (inRange) return inRange;
    return lo ? String(lo) : hi ? String(hi) : null;
  }
  return nums[0] ?? null;
}

/** Build a meta description from the story's opening sentences, max
 * DESC_MAX, cutting on a word boundary rather than mid-clause. */
export function metaFromStory(story: string): string {
  const sentences = story.split(/(?<=[.!?]) /);
  let out = "";
  for (const s of sentences) {
    const candidate = out ? out + " " + s : s;
    if (candidate.length <= DESC_MAX) {
      out = candidate;
      continue;
    }
    // The next sentence does not fit whole. Stopping here was the original
    // behaviour and it left a third of the snippet empty: an opening sentence
    // of 90 characters followed by an 80-character one produced a 90-character
    // description against a 155 limit, and 377 of 893 tree pages sat under 110
    // characters on 2026-08-09, some as short as 19. Google shows roughly 155,
    // and what it shows is the whole of the click decision, so unused room is
    // unread reason to go. Below DESC_MIN we take the clause and cut it on a
    // word boundary; at or above it we stop clean, because a whole sentence
    // reads better than a trailing ellipsis when there is already enough.
    if (out.length >= DESC_MIN) break;
    // Before truncating mid-thought, try the sentence's own clause boundaries.
    // Measured 2026-08-17: 999 of 1285 tree pages get here, because their first
    // sentence alone exceeds DESC_MAX, and the snippet Google shows is the whole
    // of the click decision. A clause that ends where the writer put a comma
    // reads as a finished thought; a cut at the 154th character does not. This
    // rescues 353 of the 999 and leaves the rest on the old behaviour, so it can
    // only improve a page, never worsen one.
    //
    // The real fix is upstream and is a writing rule, not a template one:
    // TONE_OF_VOICE principle 1 asks for an opening under 20 words, and 999
    // stories are not. This buys back what it can without rewriting them.
    if (!out) {
      const clauses = candidate.split(/(?<=[,;:]) /);
      let built = "";
      for (const c of clauses) {
        const next = built ? built + " " + c : c;
        if (next.replace(/[,;:]+$/, "").length > DESC_MAX) break;
        built = next;
      }
      built = built.trim().replace(/[,;:]+$/, "");
      if (built.length >= 60) {
        out = built;
        break;
      }
    }
    const cut = candidate.slice(0, DESC_MAX - 1);
    const lastSpace = cut.lastIndexOf(" ");
    out = (lastSpace > -1 ? cut.slice(0, lastSpace) : cut).replace(/[,.;:]+$/, "") + "…";
    break;
  }
  return out;
}

/** Every contribution button points at our own form, carrying what the
 * visitor was doing so the form preselects it. From 2026-08-14 it also
 * carries WHERE they were doing it: Hidde's complaint, that "something is
 * wrong here" led to a form that asked which city and which tree "terwijl je
 * dat in principe kan halen uit de pagina waar ik vandaan kom". The page
 * knows; the reader never types it again. */
export function submitLink(
  kind: "city" | "tree" | "correction" | "press",
  city?: string,
  tree?: string,
): string {
  const q = new URLSearchParams({ kind });
  if (city) q.set("city", city);
  if (tree) q.set("tree", tree);
  return `/contribute?${q.toString()}`;
}

/** Does the pin point at a rough spot rather than the tree itself?
 * location_precision is the only source of truth; a tree that never got
 * the field counts as approximate. */
export function locationIsApproximate(tree: Tree): boolean {
  return (tree.location_precision ?? "approximate") !== "confirmed";
}
