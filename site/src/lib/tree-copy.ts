// Small text-derivation helpers ported from build_site.py:927-961, 2433-2437, 2782-2789.
import { DESC_MAX } from "./site-config";
import type { Tree } from "./trees";

/** The number a page's title quotes for this tree's age: the figure the
 * age_estimate text itself states, even when a qualifier ("roughly", "over",
 * "traditionally") comes first. Falls back to age_min, string-coerced the
 * way Python's `str(tree.get("age_min", ""))` does: an explicit JSON `null`
 * (age_min present but unknown, e.g. barcelona's Mastic of Hort de l'Avi)
 * stringifies to the literal word "None" rather than an empty string, since
 * dict.get only applies its default when the key is absent, not when the
 * key's value is None. Matching that quirk, not fixing it here, is what
 * keeps this page's title byte-identical with the indexed production page;
 * the ugly title itself is a pre-existing content bug, out of scope for
 * this migration. */
export function ageToken(tree: Tree): string {
  const m = (tree.age_estimate ?? "").match(/(\d[\d,]*\+?)/);
  if (m) return m[1];
  if (tree.age_min === undefined) return "";
  if (tree.age_min === null) return "None";
  return String(tree.age_min);
}

/** Build a meta description from the story's opening sentences, max
 * DESC_MAX, cutting on a word boundary rather than mid-clause. */
export function metaFromStory(story: string): string {
  const sentences = story.split(/(?<=[.!?]) /);
  let out = "";
  for (const s of sentences) {
    if (out && out.length + 1 + s.length > DESC_MAX) break;
    out = (out + " " + s).trim();
    if (out.length > DESC_MAX) {
      const cut = out.slice(0, DESC_MAX - 1);
      const lastSpace = cut.lastIndexOf(" ");
      out = (lastSpace > -1 ? cut.slice(0, lastSpace) : cut).replace(/[,.;:]+$/, "") + "…";
      break;
    }
  }
  return out;
}

/** Every contribution button points at our own form, carrying what the
 * visitor was doing so the form preselects it. */
export function submitLink(kind: "city" | "tree" | "correction"): string {
  return `/contribute?kind=${kind}`;
}

/** Does the pin point at a rough spot rather than the tree itself?
 * location_precision is the only source of truth; a tree that never got
 * the field counts as approximate. */
export function locationIsApproximate(tree: Tree): boolean {
  return (tree.location_precision ?? "approximate") !== "confirmed";
}
