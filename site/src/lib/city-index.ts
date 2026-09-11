// Who belongs in an index called "cities".
//
// Hidde, 2026-09-11, looking at /cities on his phone between Brisbane (20
// trees) and Hobart (11): "Ik zou in de city lijst wel echt cities alleen
// tonen en niet bomen die random in een park staan." Cooper Creek, Derby and
// the Flinders Ranges each sat there with one tree, formatted exactly like a
// city, because every place on this site is a `data/cities/*.json` file and
// the index printed all of them.
//
// It is the rule blueprint v1.15 already wrote down ("only cities appear on
// /cities") arriving at the data: 582 places render, 345 of them hold fewer
// than four trees, and almost every one of those exists because of the
// single-famous-tree exception of 2026-08-31, which gave a lone famous tree a
// home rather than declaring a city.
//
// So two conditions, both mechanical, neither of them a judgement about any
// particular village:
//
//   1. The place calls itself a city (schema `kind`), so a region, a park or
//      a forest is listed on its country page instead.
//   2. It clears the four-tree floor, OR it is a ranked city in
//      data/city-queue.json.
//
// The second half of (2) is what keeps this honest. Rule 1(0) of the current
// phase opens a ranked city at four or five trees and moves on, so a real
// city is often two trees old for a while: Canberra, Nantes, Liverpool,
// Philadelphia and Turku are cities we are deliberately covering and they
// stay on the list. What drops off is a place that was never a city in the
// first place.
//
// Nothing is hidden by this. A place below the line keeps its page, its map
// pin, its search entry and its row on its country page, and /cities links to
// every one of them in its own section, which is also what stops the five
// places whose country has no country page from being orphaned (qa.py fails
// the deploy on a page nothing links to).
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";
import { renderableTrees, type CityEntry } from "./trees";

/** A place earns its own page at four verified trees (CLAUDE.md, "the count
 * follows the trees"), and that is the same line this index draws. */
export const CITY_INDEX_FLOOR = 4;

let cachedRanked: Set<string> | null = null;

/** Slugs of the cities the queue actually ranks. data/city-queue.json is the
 * single source of the one queue (CITY_QUEUE.md is its readable rendering),
 * so "a city we are deliberately covering" needs no second list here. */
function rankedCitySlugs(): Set<string> {
  if (cachedRanked) return cachedRanked;
  const f = path.join(DATA, "city-queue.json");
  const data = JSON.parse(fs.readFileSync(f, "utf-8"));
  cachedRanked = new Set(
    (data.cities ?? [])
      .filter((c: { rank: number | null; slug?: string }) => c.rank != null && c.slug)
      .map((c: { slug: string }) => c.slug),
  );
  return cachedRanked;
}

/** Is this place a city at all, as opposed to a region, a park or a forest?
 * Missing means city, which is what every file written before v1.15 says. */
export function isCityKind(entry: CityEntry): boolean {
  return (entry.data.kind ?? "city") === "city";
}

/** Does this place belong in the city index itself? */
export function belongsInCityIndex(entry: CityEntry): boolean {
  if (!isCityKind(entry)) return false;
  return renderableTrees(entry).length >= CITY_INDEX_FLOOR || rankedCitySlugs().has(entry.id);
}
