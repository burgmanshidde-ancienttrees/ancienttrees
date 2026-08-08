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
