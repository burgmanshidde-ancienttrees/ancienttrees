import { TITLE_MAX } from "./site-config";

/** Ported from fit_title(), build_site.py:964-969: first candidate that fits
 * the length budget, or the last candidate if none do (Base.astro's own
 * length check catches that case at build time, same as ERRORS.append did). */
export function fitTitle(candidates: string[]): string {
  for (const c of candidates) {
    if (c.length <= TITLE_MAX) return c;
  }
  return candidates[candidates.length - 1];
}
