// Ported from park_key()/group_trees_by_park(), build_site.py:2700-2738.
// A park is not a field on a tree; it's derived from the neighbourhood/
// address text matching a keyword list, which is why the intro file's
// "park" value must match this function's output exactly (load_park_intros
// keys itself on (city_slug, park), build_site.py:3904).
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";
import type { CityEntry, Tree } from "./trees";
import { treeIsRenderable } from "./trees";

// Widened 2026-09-18 while measuring our coverage of the world's best-known
// parks (scripts/park_demand.py). Six words were missing and the gap was
// invisible because it fails silently: a tree whose address names no listed
// word simply has no park, and no page is ever short of anything. What it cost:
// "parque" is the Spanish and Portuguese word for park and was not here, so
// Parque de Maria Luisa in Seville held ten mapped trees and could not become a
// page, and "retiro" is in this list only because somebody patched that one
// Madrid case rather than the word behind it. "garten" was missing while
// "schlosspark" and "stadtpark" were present, which hid the Englischer Garten
// and Nuremberg's Kontumazgarten. Adding them groups 147 trees that had no park
// at all and takes three parks over Contract H's five-tree gate.
//
// Only words the data actually justifies are here: an unused word is a false
// positive waiting to happen. Bare "forest" is deliberately left out, because
// English street and district names are full of it (Forest Hills, Forest Road)
// while "foret" and "floresta" are not. The same risk already lives in "park",
// which reads a car park as a park; the fix for those is the address text.
const PARK_WORDS = [
  "park",
  "parque",
  "garden",
  "garten",
  "jardin",
  "jardim",
  "giardin",
  "parc",
  "parco",
  "tuin",
  "plantsoen",
  "villa ",
  "orto",
  "botanic",
  "bois",
  "bosque",
  "foret",
  "forêt",
  "floresta",
  "hortus",
  "schlosspark",
  "stadtpark",
  "retiro",
  "arboret",
];

/** Parks no keyword can see, from data/park-names.json.
 *
 * The word list above is the right mechanism for the thousands of places whose
 * name says they are a park, and it cannot work for a place whose name does
 * not: Margaret Island, the Pfaueninsel, Montjuic, the National Mall. No word
 * that would catch those is safe to add, because "island" is a substring of
 * Islandbridge and "mall" of Smallbrook Street.
 *
 * Read once per build. The file carries the bar a name has to clear and why
 * each one is in; scripts/pagegaps.py reads the same file and
 * check_park_words_match() in preflight compares the two. */
let EXPLICIT: Set<string> | null = null;

function explicitParks(): Set<string> {
  if (EXPLICIT) return EXPLICIT;
  EXPLICIT = new Set<string>();
  try {
    const f = path.join(DATA, "park-names.json");
    if (fs.existsSync(f)) {
      const d = JSON.parse(fs.readFileSync(f, "utf-8"));
      for (const name of Object.keys(d.parks ?? {})) EXPLICIT.add(name.toLowerCase());
    }
  } catch {
    // A missing or broken file means no explicit parks, never a failed build:
    // the keyword list is the mechanism and this is the supplement.
  }
  return EXPLICIT;
}

export const PARK_MIN_TREES = 5;

/** The named park a tree stands in, or null. Reads neighbourhood first,
 * address second: the clause before the first comma, parentheticals
 * stripped. */
export function parkKey(tree: Tree): string | null {
  const loc = tree.location ?? {};
  const heads: string[] = [];
  for (const field of [loc.neighbourhood, loc.address]) {
    let head = String(field ?? "").split(",")[0];
    head = head.replace(/\([^)]*\)?/g, "");
    head = head.replace(/\s+/g, " ").trim().replace(/^[-/\s]+|[-/\s]+$/g, "");
    if (head.length < 4) continue;
    if (PARK_WORDS.some((w) => head.toLowerCase().includes(w))) return head;
    heads.push(head);
  }
  // Only once no field named a park by a keyword, because a keyword match is
  // the more specific answer: a Montjuic tree whose address names the Jardi
  // Botanic Historic belongs to that garden and not to the hill. Exact match,
  // since the near misses are real places of their own ("Pfaueninsel ferry
  // landing", "Kalopanagiotis village").
  const explicit = explicitParks();
  for (const head of heads) {
    if (explicit.has(head.toLowerCase())) return head;
  }
  return null;
}

/** The key that identifies one park: its city plus the name derived from its
 * trees. It is a function because it existed twice with two different
 * separators, a NUL byte here and a plain space on every page, and nothing
 * broke for as long as nobody did a real lookup across the two. /api/browse.json
 * did one on 2026-08-25 and the parks facet came back empty: 467 groups, 24
 * intros, zero matches, and no error anywhere.
 *
 * The separator stays a NUL, because it is the one character a park name cannot
 * contain, but it is written as an escape so it can be seen. */
export function parkGroupKey(citySlug: string, parkName: string): string {
  return `${citySlug}\u0000${parkName}`;
}

export interface ParkGroup {
  citySlug: string;
  parkName: string;
  city: CityEntry;
  trees: Tree[];
}

/** (city_slug, park name) -> group, mirroring group_trees_by_park(). */
export function groupTreesByPark(cities: CityEntry[]): Map<string, ParkGroup> {
  const groups = new Map<string, ParkGroup>();
  for (const city of cities) {
    for (const t of city.data.trees) {
      if (!treeIsRenderable(t)) continue;
      const name = parkKey(t);
      if (!name) continue;
      const key = parkGroupKey(city.id, name);
      let g = groups.get(key);
      if (!g) {
        g = { citySlug: city.id, parkName: name, city, trees: [] };
        groups.set(key, g);
      }
      g.trees.push(t);
    }
  }
  return groups;
}
