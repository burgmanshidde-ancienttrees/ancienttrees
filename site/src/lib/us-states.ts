// Contract L, US state pages (blueprint v1.22, 2026-09-26, Hidde: "dit klinkt
// slim", then "doe 1 en 2"). The United States is the biggest search country
// and its tree queries are shaped by STATE ("oldest tree in ohio") as often as
// by city, with no page of that shape to land on.
//
// Which place is in which state lives in data/us-states.json, one line per US
// place, rather than being parsed out of addresses at build time: addresses
// here say "SW Park Ave" and "Linda Hall Library", and a guess that sends
// Portland to Nebraska is worse than a missing line. The missing line is
// caught instead: statePlaces() throws on a US place the file does not name,
// so a night run opening a new American place cannot quietly leave it out of
// its state.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

/** The gate, both halves (Contract L). Three trees, and two places, because a
 * one-place state page is that place's page with a state name on it. */
export const STATE_MIN_TREES = 3;
export const STATE_MIN_PLACES = 2;

let cache: Record<string, string> | null = null;

/** Place slug -> state name, for every published US place. */
export function usStateOf(): Record<string, string> {
  if (cache) return cache;
  const f = path.join(DATA, "us-states.json");
  cache = fs.existsSync(f) ? (JSON.parse(fs.readFileSync(f, "utf-8")).places ?? {}) : {};
  return cache!;
}

export function stateSlug(state: string): string {
  return state.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

/** Throws on a published US place with no state line. Called by every page
 * that groups by state, so the build fails where the gap would have shown. */
export function assertEveryUsPlaceHasAState(usPlaceSlugs: string[]): void {
  const map = usStateOf();
  const missing = usPlaceSlugs.filter((s) => !map[s]);
  if (missing.length) {
    throw new Error(
      `data/us-states.json has no state for: ${missing.join(", ")} (Contract L). ` +
      `Add one line per place, "District of Columbia" for DC.`);
  }
}

/** State name -> slug, for exactly the states whose page is built. The
 * country page lists these and a US place page links its own through the
 * breadcrumb, so both ask here and cannot link a state page that does not
 * exist. `cities` must already be filtered to renderable ones. */
export function publishedStatePages(
  cities: { id: string; data: { country: string } }[],
  intros: { data: { state: string; slug: string } }[],
  treeCount: (c: any) => number,
): Map<string, string> {
  const stateOf = usStateOf();
  const out = new Map<string, string>();
  for (const intro of intros) {
    const places = cities.filter((c) => c.data.country === "United States" && stateOf[c.id] === intro.data.state);
    const trees = places.reduce((n, c) => n + treeCount(c), 0);
    if (places.length >= STATE_MIN_PLACES && trees >= STATE_MIN_TREES) out.set(intro.data.state, intro.data.slug);
  }
  return out;
}
