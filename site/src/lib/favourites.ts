// Our favourite tree cities: the shelf on the homepage and in the app's Discover.
//
// ONE list, decided here and sent in /api/browse.json as `favourites`, so both
// surfaces show the same cities in the same order (the answer-not-rule ruling
// of 2026-08-25). Until 2026-10-02 the website used this hand-picked list and
// the app sorted every city by tree count, which put Leeuwarden, 41 trees and
// not one photograph, in the second slot with a placeholder leaf. Hidde:
// "Don't promote cities like Leeuwarden if they don't have a single photo."
//
// So the rule travels with the list: a city is a favourite only while it has a
// face, the photograph the city page itself wears. A city that loses its last
// photograph drops off the shelf on the next build without anybody noticing.
import type { CollectionEntry } from "astro:content";
import { cityFaceTree, usablePhoto } from "./images";
import { renderableTrees } from "./trees";

export const FAVOURITE_CITIES = ["barcelona", "rome", "paris", "berlin", "amsterdam", "london", "new-york", "lisbon", "vienna", "edinburgh"];

/** The favourites that can actually be shown: in order, only those with a face. */
export function favouriteCitySlugs(cities: CollectionEntry<"cities">[]): string[] {
  const bySlug = new Map(cities.map((c) => [c.id, c]));
  return FAVOURITE_CITIES.filter((slug) => {
    const e = bySlug.get(slug);
    if (!e) return false;
    const face = cityFaceTree({ hero_tree_id: e.data.hero_tree_id, face_tree_id: (e.data as any).face_tree_id, trees: renderableTrees(e) });
    return Boolean(face && usablePhoto(face)?.url);
  });
}

// TREE ISLANDS: the second shelf decided here, on the same terms (Hidde,
// 2026-08-20: "rows like our favourite cities, best tree islands"; built
// 2026-10-04). Places that ARE an island, not cities that happen to stand on
// one, so Palermo and Cagliari stay cities. Same face rule: an island with no
// photograph is not on the shelf, which today keeps Menorca, Mallorca, Maui
// and Okinawa off it until one of their trees gets a picture.
export const FAVOURITE_ISLANDS = ["tenerife", "madeira", "oahu", "crete", "sardinia", "kauai", "menorca", "mallorca", "maui", "hawaii", "okinawa", "yakushima"];

/** The islands that can actually be shown: in order, only those with a face. */
export function islandSlugs(cities: CollectionEntry<"cities">[]): string[] {
  const bySlug = new Map(cities.map((c) => [c.id, c]));
  return FAVOURITE_ISLANDS.filter((slug) => {
    const e = bySlug.get(slug);
    if (!e) return false;
    const face = cityFaceTree({ hero_tree_id: e.data.hero_tree_id, face_tree_id: (e.data as any).face_tree_id, trees: renderableTrees(e) });
    return Boolean(face && usablePhoto(face)?.url);
  });
}

// WHEN A COLLECTION IS IN SEASON, as month numbers (northern hemisphere, which
// is where every one of these trees stands). Discover shows the collection as
// a shelf in those months only, so the screen changes with the year. An
// ANSWER sent in the feed as `months`, never a table copied into Swift.
export const COLLECTION_MONTHS: Record<string, number[]> = {
  "wisteria-and-blossom-worth-a-spring-trip": [3, 4, 5],
  "autumn-harvest-trees": [9, 10],
  "autumn-colour-trees": [10, 11],
  "ginkgos-worth-a-november-trip": [11],
};

/** The collections in season this month, in the table's order. */
export function collectionsInSeason(month: number): string[] {
  return Object.entries(COLLECTION_MONTHS).filter(([, m]) => m.includes(month)).map(([slug]) => slug);
}
