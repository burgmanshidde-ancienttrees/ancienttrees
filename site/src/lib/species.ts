// Ported from species_common()/group_trees_by_species()/check_species_names(),
// build_site.py:941-942, 2741-2765, 2978-2997.
import type { CityEntry, Tree } from "./trees";
import { treeIsRenderable } from "./trees";

export const SPECIES_MIN_TREES = 3;
export const COUNTRY_MIN_CITIES = 3;

/** "European Yew (Taxus baccata)" -> "European Yew". */
export function speciesCommon(tree: Tree): string {
  return (tree.species ?? "").split(" (")[0];
}

export interface SpeciesMember {
  city: CityEntry;
  tree: Tree;
}

/** common_name -> members, preserving city order then age. Also checks that
 * no tree id is reused across two different cities, since tree ids are the
 * join key for species and collection pages (found: Cordoba and Cork both
 * started "cor_", 2026-08-03). */
export function groupTreesBySpecies(renderable: CityEntry[]): Map<string, SpeciesMember[]> {
  const idCity = new Map<string, string>();
  for (const entry of renderable) {
    for (const t of entry.data.trees) {
      const other = idCity.get(t.id);
      if (other && other !== entry.id) {
        throw new Error(`tree id ${t.id} is used by both ${other} and ${entry.id}`);
      }
      idCity.set(t.id, entry.id);
    }
  }

  const groups = new Map<string, SpeciesMember[]>();
  for (const entry of renderable) {
    for (const t of entry.data.trees.filter(treeIsRenderable)) {
      const key = speciesCommon(t);
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key)!.push({ city: entry, tree: t });
    }
  }
  return groups;
}

/** Hard rule 9: one canonical common name per species. Florence once
 * carried a Deodar Cedar and a Himalayan Cedar as the same tree twice. */
export function checkSpeciesNames(cities: CityEntry[]): void {
  const byLatin = new Map<string, Map<string, string[]>>();
  for (const entry of [...cities].sort((a, b) => a.id.localeCompare(b.id))) {
    for (const t of entry.data.trees) {
      const sp = t.species ?? "";
      const m = sp.match(/\(([^)]+)\)/);
      if (!m || m.index === undefined) continue;
      const common = sp.slice(0, m.index).trim();
      const latin = m[1].trim();
      if (!byLatin.has(latin)) byLatin.set(latin, new Map());
      const commons = byLatin.get(latin)!;
      if (!commons.has(common)) commons.set(common, []);
      commons.get(common)!.push(entry.id);
    }
  }
  const errors: string[] = [];
  for (const [latin, commons] of [...byLatin.entries()].sort(([a], [b]) => a.localeCompare(b))) {
    if (commons.size > 1) {
      const spread = [...commons.entries()]
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([c, v]) => {
          const uniq = [...new Set(v)].sort();
          return `${JSON.stringify(c)} in ${uniq[0]}${uniq.length > 1 ? " and others" : ""}`;
        })
        .join("; ");
      errors.push(`species ${latin} uses ${commons.size} common names, hard rule 9 allows one: ${spread}`);
    }
  }
  if (errors.length) throw new Error(errors.join("\n"));
}
