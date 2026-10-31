// A TREE'S PHOTOGRAPHS BY SEASON (Hidde, 2026-10-31; CONVENTIONS.md "A tree's
// photographs by season, and the empty season as an ask"). The goal is shared:
// every visitor sees every tree in all four seasons, so a tile shows anybody's
// photograph of that season and an empty one asks whoever is standing there.
//
// Decided once, here, and sent to the app in the feed (`season` on each
// photograph, `seasonal` on the tree), so the two surfaces never disagree
// about which tree has seasons or which season a photograph shows.
import { phenologyByName } from "./phenology";
import { speciesCommon } from "./species";
import type { Tree } from "./trees";

export type Season = "spring" | "summer" | "autumn" | "winter";
export const SEASONS: Season[] = ["spring", "summer", "autumn", "winter"];

// Only for a species without a phenology file: the genera that change visibly
// through the year. The evergreen exceptions inside a deciduous genus (holm and
// cork oak, live oak) are listed first and win.
const EVERGREEN = ["quercus ilex", "quercus suber", "quercus virginiana", "quercus coccifera", "magnolia grandiflora",
  "prunus lusitanica", "prunus laurocerasus"];
const DECIDUOUS = ["quercus robur", "quercus petraea", "quercus rubra", "quercus cerris", "quercus pubescens",
  "quercus alba", "quercus frainetto", "quercus pyrenaica", "quercus faginea", "fagus", "tilia", "platanus",
  "acer", "ulmus", "fraxinus", "castanea", "aesculus", "ginkgo", "salix", "populus", "carpinus", "prunus",
  "malus", "pyrus", "juglans", "morus", "betula", "larix", "taxodium", "metasequoia", "liriodendron",
  "robinia", "sophora", "styphnolobium", "catalpa", "zelkova", "celtis", "gleditsia", "sorbus", "alnus",
  "paulownia", "pterocarya", "liquidambar", "nyssa", "cercis", "wisteria", "diospyros"];

/** Inside the tropics there is no row: a year there is not four seasons. */
export function outsideTropics(lat: number | null | undefined): boolean {
  return typeof lat === "number" && Math.abs(lat) >= 25;
}

/** Whether this tree goes through the seasons: deciduous, outside the tropics. */
export function isSeasonal(tree: Tree, lat: number | null | undefined): boolean {
  if (!outsideTropics(lat)) return false;
  const habit = phenologyByName(speciesCommon(tree))?.habit;
  if (habit) return habit === "deciduous";
  const latin = (tree.species ?? "").toLowerCase();
  if (EVERGREEN.some((g) => latin.includes(g))) return false;
  return DECIDUOUS.some((g) => latin.includes(g));
}

/** Meteorological seasons, flipped south of the equator. Null without a month. */
export function seasonOfMonth(month: number | null | undefined, lat: number): Season | null {
  if (!month || month < 1 || month > 12) return null;
  const north = month >= 3 && month <= 5 ? 0 : month <= 8 && month >= 6 ? 1 : month >= 9 && month <= 11 ? 2 : 3;
  return SEASONS[lat < 0 ? (north + 2) % 4 : north];
}
