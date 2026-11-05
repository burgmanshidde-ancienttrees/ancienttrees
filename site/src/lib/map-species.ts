// The species list the map's species chip picks from, one for every map: the
// explore map carries it inline, the city map fetches it (/api/map-species.json)
// and its neighbours' rows in /api/pins.json carry an index into it, so a
// species chosen on a city map means the same trees as on /explore.
//
// An index rather than the name on every tree, because 3,055 copies of a dozen
// common names is 45KB of the same words; the list ships once beside them.
// Ordered by how many trees carry it, which is the only order that helps: 521
// species exist and twelve of them cover a third of the map.
import { getCollection } from "astro:content";
import { cityIsRenderable, renderableTrees } from "./trees";
import { speciesCommon, speciesScientific } from "./species";
import { sciNameHtml } from "./latin";

export interface MapSpecies {
  list: string[];
  index: Map<string, number>;
  /** The Latin under each row of the species sheet, as HTML (latin.ts
   * italics). Every other name a species goes by is 117 KB, so the sheet
   * fetches it from /api/species.json the first time somebody types. */
  latinHtml: string[];
}

let cached: Promise<MapSpecies> | null = null;

export function mapSpecies(): Promise<MapSpecies> {
  if (!cached) cached = build();
  return cached;
}

async function build(): Promise<MapSpecies> {
  const cities = (await getCollection("cities")).filter(cityIsRenderable);
  const count = new Map<string, number>();
  const latin = new Map<string, string>();
  for (const entry of cities) {
    for (const t of renderableTrees(entry)) {
      const s = speciesCommon(t);
      if (!s) continue;
      count.set(s, (count.get(s) ?? 0) + 1);
      const l = speciesScientific(t.species ?? "");
      if (l && !latin.has(s)) latin.set(s, l);
    }
  }
  const list = [...count.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([name]) => name);
  return {
    list,
    index: new Map(list.map((s, i) => [s, i])),
    latinHtml: list.map((s) => {
      const l = latin.get(s);
      return l ? sciNameHtml(l) : "";
    }),
  };
}
