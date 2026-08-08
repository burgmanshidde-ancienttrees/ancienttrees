// The "published" list build_site.py assembles follows data/city-list.json's
// declared order (load_cities(), build_site.py:5579), not alphabetical.
// That order is curated (tier, priority, notes), so anywhere the Python
// output lists cities in sequence (park page "explore by city", indexes),
// matching it is what keeps output order stable rather than an unexplained
// behavior change. Found by diffing a ported park page against the real
// build: Python's "other cities" list led with Guimaraes/Fukuoka, not
// alphabetically-first Amsterdam/Antwerp/Arnhem.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

let cachedOrder: string[] | null = null;

function loadOrder(): string[] {
  if (cachedOrder) return cachedOrder;
  const f = path.join(DATA, "city-list.json");
  const data = JSON.parse(fs.readFileSync(f, "utf-8"));
  cachedOrder = (data.cities ?? []).map((c: { slug: string }) => c.slug);
  return cachedOrder;
}

/** Sorts items with a `slug` field into data/city-list.json's declared
 * order. Items not found in the list (shouldn't happen for real cities)
 * sort last, stably. */
export function byCityListOrder<T extends { slug: string }>(items: T[]): T[] {
  const order = loadOrder();
  const index = new Map(order.map((slug, i) => [slug, i]));
  return [...items].sort((a, b) => (index.get(a.slug) ?? Infinity) - (index.get(b.slug) ?? Infinity));
}

/** Same ordering, keyed by a content-collection entry's `.id` (the city
 * slug) instead of a `.slug` field. Needed anywhere `getCollection("cities")`
 * output feeds a computation that depends on iteration order BEFORE any
 * display sort is applied: load_cities() (build_site.py:2579-2585) reads
 * city-list.json directly, so every Python list/dict built by walking
 * `renderable` inherits that order, including ties broken by a later
 * stable sort (e.g. build_parks_index's tree-count sort) and any raw,
 * unsorted list a page's JSON-LD ItemList quotes (e.g. /cities's schema
 * graph, which is NOT the alphabetically-grouped list the page displays). */
export function byCityListOrderEntry<T extends { id: string }>(items: T[]): T[] {
  const order = loadOrder();
  const index = new Map(order.map((slug, i) => [slug, i]));
  return [...items].sort((a, b) => (index.get(a.id) ?? Infinity) - (index.get(b.id) ?? Infinity));
}
