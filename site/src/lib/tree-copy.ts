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
  const said = tree.age_estimate ?? "";

  // A title may not state an age our own data refuses to state. Hard rule 2,
  // found 2026-08-28 while chasing a click-through problem that turned out not
  // to exist: the Drago's field reads "disputed: a modern study puts it near
  // 700 years, popular tradition says 1,000 years or more" and its title read
  // "700 Year Old Dragon Tree", flattening a dispute our own sentence names
  // into a fact, in the one line a searcher reads before deciding.
  //
  // 21 pages did that. Athens' olive is "300-2,500 years (disputed)" and said
  // 300; Crete's is "contested: at least 2,000, possibly up to 4,000" and said
  // 2,000. Picking one end of a disputed range and printing it flat is the
  // same error the softening rule elsewhere exists to stop.
  if (/\b(disputed|contested)\b/i.test(said)) return null;

  const nums = [...said.matchAll(/(\d[\d,]*\+?)/g)].map((m) => m[1]);
  const lo = tree.age_min ?? null;
  const hi = tree.age_max ?? null;
  if (lo || hi) {
    const inRange = nums.find((n) => {
      const v = parseInt(n.replace(/[,+]/g, ""), 10);
      return (!lo || v >= lo) && (!hi || v <= hi);
    });
    if (inRange) return inRange;

    // The sentence offers no usable number, so the old code reached for
    // age_min instead and printed a figure the age field never contains. 211
    // pages did that. Aarhus reads "not documented" and said "100 Year Old";
    // Alicante reads "over a century" and said "90 Year Old", which is not
    // merely overconfident but lower than the data claims. age_min is a bound
    // for sorting and filtering, not a statement anybody wrote down, and a
    // title is a statement.
    return null;
  }
  return nums[0] ?? null;
}

/** Build a meta description from the story's opening sentences, max
 * DESC_MAX, cutting on a word boundary rather than mid-clause. */
export function metaFromStory(story: string, budget: number = DESC_MAX): string {
  const sentences = story.split(/(?<=[.!?]) /);
  let out = "";
  for (const s of sentences) {
    const candidate = out ? out + " " + s : s;
    if (candidate.length <= budget) {
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
        if (next.replace(/[,;:]+$/, "").length > budget) break;
        built = next;
      }
      built = built.trim().replace(/[,;:]+$/, "");
      if (built.length >= 60) {
        out = built;
        break;
      }
    }
    const cut = candidate.slice(0, budget - 1);
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

/** A meta description that ANSWERS before it hooks, which is what Contract B
 *  has asked for since v1.0 and what the implementation never did.
 *
 *  Until 2026-09-02 a tree page's description was the story's opening, and a
 *  story opens with its surprise. El Drago Milenario, which takes 11
 *  impressions a day for its own name, offered searchers "Nobody can date this
 *  tree, and nobody is going to." True, well written, and no use at all to
 *  somebody deciding whether to click: it says nothing about what the tree is,
 *  where it stands, or whether they can go. Measured across the pages losing
 *  the most clicks, every one of them led with a hook and buried the answer.
 *
 *  So: the facts first, in the order a searcher wants them, then as much of the
 *  story as fits. The tail reuses metaFromStory, which already knows how to cut
 *  on a clause boundary rather than mid-thought.
 */
export function metaForTree(tree: {
  species?: string; age_estimate?: string;
  location?: { neighbourhood?: string | null; address?: string | null } | null;
  story?: string;
}, cityName: string,
   lead: (species: string, age: string, where: string) => string,
   overrides?: { species?: string; age_estimate?: string; story?: string }): string {
  // Both bracket shapes: the Japanese overlays write the binomial inside a
  // full-width （ ）, so splitting on "(" alone left "スギ（Cryptomeria
  // japonica）" in the snippet and spent thirty characters on Latin nobody
  // searched for.
  const rawSpecies = (overrides?.species ?? tree.species ?? "")
    .split(/[(\uff08]/)[0].trim();
  // "Mixed species" is our placeholder for an ensemble, not a name, and it
  // reads as a database field rather than as a tree.
  const species = rawSpecies && !/^mixed species$/i.test(rawSpecies) ? rawSpecies : "";
  const ageText = (overrides?.age_estimate ?? tree.age_estimate ?? "").trim();
  const age = /not documented|unknown|undated|not established/i.test(ageText)
    ? "" : (ageText.replace(/,/g, "").match(/\d{2,4}/) ?? [""])[0];

  const loc = tree.location ?? {};
  const area = (loc.neighbourhood ?? "").split("/")[0].split(",")[0].trim()
    || (loc.address ?? "").split(",")[0].trim();
  const where = area && !area.toLowerCase().includes(cityName.toLowerCase())
    ? `${area}, ${cityName}` : cityName;

  const opening = lead(species, age, where);
  const room = DESC_MAX - opening.length - 1;
  const story = overrides?.story ?? tree.story ?? "";
  const tail = room >= 45 ? metaFromStory(story, room) : "";
  return tail ? `${opening} ${tail}` : opening;
}
