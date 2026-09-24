// Ported from the other_cities computation inside main(), build_site.py:5756-5776.
// The "cities in view" chooser and the /explore favourites ordering both key
// off this list.
import { cityFace } from "./images";
import type { CityEntry } from "./trees";

// Hand-picked favourites, ranked first in the chooser; everything else falls
// back to tree count (build_site.py:5756-5757).
const FAVES = ["lisbon", "cadiz", "porto", "amsterdam", "kyoto", "rome", "palermo", "paris", "london", "barcelona"];

export interface OtherCityEntry {
  slug: string;
  city: string;
  country: string;
  n: number;
  ph: string | null;
  rank: number;
  lat: number;
  lng: number;
}

/** Every other renderable city, with a face photo, a favourites rank, and
 * the average position of ALL its trees (not just renderable ones -
 * matching the Python computation exactly, inconsistency and all). */
export function otherCitiesFor(currentSlug: string, allCities: CityEntry[]): OtherCityEntry[] {
  return allCities
    .filter((e) => e.id !== currentSlug && e.data.trees.length > 0)
    .map((e) => ({
      slug: e.id,
      city: e.data.city,
      country: e.data.country,
      n: e.data.trees.length,
      ph: cityFace(e.data, 400),
      rank: FAVES.includes(e.id) ? FAVES.indexOf(e.id) : 99,
      lat: e.data.trees.reduce((s, t) => s + (t.location.latitude ?? 0), 0) / e.data.trees.length,
      lng: e.data.trees.reduce((s, t) => s + (t.location.longitude ?? 0), 0) / e.data.trees.length,
    }));
}

/** The cities at the foot of a city page: the closest few, not all of them
 * (2026-09-24). That list used to be every other city in city-list order,
 * which was 228 links on every city page and grew with every city opened.
 * Somebody finishing Utrecht wants Amersfoort and Arnhem, not Auckland; the
 * full list lives at /cities, which the foot links to, so no city loses its
 * way in. Distance is measured between the average positions of each city's
 * trees, the same centre the map's city dots use. */
export const NEARBY_CITIES_N = 8;
export function nearbyCitiesFor<T extends { lat: number; lng: number }>(
  centre: { lat: number; lng: number }, others: T[], n = NEARBY_CITIES_N,
): T[] {
  const km = (a: { lat: number; lng: number }, b: { lat: number; lng: number }): number => {
    const x = (a.lng - b.lng) * Math.cos(((a.lat + b.lat) / 2) * Math.PI / 180);
    return 111.32 * Math.hypot(x, a.lat - b.lat);
  };
  return [...others].sort((a, b) => km(centre, a) - km(centre, b)).slice(0, n);
}

/** The average position of a city's trees, the centre nearbyCitiesFor() and
 * otherCitiesFor() both measure from. */
export function cityCentre(d: CityEntry["data"]): { lat: number; lng: number } {
  const n = d.trees.length || 1;
  return {
    lat: d.trees.reduce((s, t) => s + (t.location.latitude ?? 0), 0) / n,
    lng: d.trees.reduce((s, t) => s + (t.location.longitude ?? 0), 0) / n,
  };
}
