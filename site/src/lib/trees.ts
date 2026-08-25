// Shared tree-level helpers used across contracts. Single source so
// redirect-map.ts, parks.ts, species.ts etc. don't each carry their own
// copy of the same logic ported from build_site.py.
import type { CollectionEntry } from "astro:content";
import { haversineKm } from "./walks";

export type Tree = CollectionEntry<"cities">["data"]["trees"][number];
export type CityData = CollectionEntry<"cities">["data"];
export type CityEntry = CollectionEntry<"cities">;

/** Ported verbatim from tree_is_renderable(), build_site.py:2275. */
export function treeIsRenderable(t: Tree): boolean {
  const loc = t.location ?? {};
  return Boolean(t.story) && loc.latitude != null && loc.longitude != null;
}

/** Ported verbatim from slugify(), build_site.py:918. Order matters: strip
 * quotes and a leading "the " BEFORE the NFKD/ASCII fold. */
export function slugify(name: string): string {
  let s = name.toLowerCase().replace(/'/g, "").replace(/’/g, "");
  if (s.startsWith("the ")) s = s.slice(4);
  s = s
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^\x00-\x7F]/g, "");
  s = s.replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  return s;
}

/** A city "renders" (has a page) once it has at least one renderable tree,
 * mirroring build_city_page's actual gate (build_site.py:3423). */
export function cityIsRenderable(city: CityEntry): boolean {
  return city.data.trees.some(treeIsRenderable);
}

export function renderableTrees(city: CityEntry): Tree[] {
  return city.data.trees.filter(treeIsRenderable);
}

/** Human distance between two tree locations: "350 m" or "2.1 km".
 * Ported from haversine()/dist_label(), build_site.py:911-915,972-975. */
export function distLabel(
  a: { latitude: number; longitude: number },
  b: { latitude: number; longitude: number }
): string {
  const m = haversineKm([a.latitude, a.longitude], [b.latitude, b.longitude]) * 1000;
  return m < 1000 ? `${Math.round(m / 10) * 10} m` : `${(m / 1000).toFixed(1)} km`;
}

/** Every renderable tree's slug within a city, id -> slug. Mirrors the
 * tree_slugs dict build_site.py assembles once per build (build_site.py:5719,
 * 5754). */
export function treeSlugsForCity(city: CityEntry): Record<string, string> {
  const out: Record<string, string> = {};
  for (const t of renderableTrees(city)) {
    out[t.id] = slugify(t.name);
  }
  return out;
}

/** Highest age_max wins, unless the city names its answer explicitly via
 * oldest_tree_id (build_site.py:2768-2779). Amsterdam's Hortus cycad
 * out-ages the Heimanseik but is a potted cycad, not a tree. */
export function oldestTree(trees: Tree[], cityData?: { oldest_tree_id?: string | null }): Tree {
  if (cityData?.oldest_tree_id) {
    const named = trees.find((t) => t.id === cityData.oldest_tree_id);
    if (named) return named;
  }
  return trees.reduce((best, t) => ((t.age_max ?? 0) > (best.age_max ?? 0) ? t : best));
}

/** Trees a WALK may pass.
 *
 * Not the ones behind a ticket (Hidde, 2026-08-24: "die betaalde bomen niet
 * meenemen in de wandelingen"). A route that asks for two tickets on the way is
 * not an afternoon out, and the walk is the product rather than the list. They
 * keep their place on the map and on the city page, marked; they simply do not
 * get somebody standing at a gate with a card in their hand.
 */
export function walkableTrees(city: CityEntry): Tree[] {
  return renderableTrees(city).filter((t) => !t.paid_entry);
}
