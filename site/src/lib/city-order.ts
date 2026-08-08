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
