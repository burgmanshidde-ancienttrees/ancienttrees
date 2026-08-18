// The dataset an app reads, so new trees reach it without a new build
// (Hidde, 2026-08-18: "hoe zorgen we dat als wij meer bomen vinden dat die
// dan in de app komen zonder dat we een nieuwe app hoeven up te loaden?").
//
// The mechanism, and it is the ordinary one: an app ships with a snapshot so
// it works on first launch and offline, then asks a tiny version file whether
// anything changed, and pulls the full dataset only when it has. Data is not
// code, so none of this touches App Store review; a new SCREEN needs a new
// build, a new tree does not.
//
// One file rather than per-city chunks, measured rather than assumed: 1,377
// trees are 2.36 MB raw and 0.76 MB gzipped, and even several times that stays
// a single comfortable download. Chunking would buy nothing today and cost a
// second thing that can drift out of sync.
//
// The honesty fields ride along on purpose. location_precision travels with
// every tree so an app can say "we know the park, not the trunk" exactly where
// the website says it, and a photo carries its licence and attribution so an
// app cannot show the picture while dropping the credit the licence demands.
import type { CityEntry } from "./trees";
import { renderableTrees, slugify } from "./trees";
import { usablePhoto } from "./images";

export interface FeedTree {
  id: string;
  name: string;
  species: string | null;
  age: string | null;
  lat: number;
  lng: number;
  city: string;
  city_slug: string;
  country: string;
  neighbourhood: string | null;
  access: string | null;
  transport: string | null;
  precision: string | null;
  best_time: unknown;
  story: string | null;
  url: string;
  photo: { url: string; license: string | null; attribution: string | null } | null;
}

export function feedTrees(cities: CityEntry[]): FeedTree[] {
  const out: FeedTree[] = [];
  for (const city of cities) {
    for (const t of renderableTrees(city)) {
      const loc = t.location ?? ({} as any);
      if (loc.latitude == null || loc.longitude == null) continue;
      const p = usablePhoto(t);
      out.push({
        id: t.id,
        name: t.name,
        species: t.species ?? null,
        age: t.age_estimate ?? null,
        lat: loc.latitude,
        lng: loc.longitude,
        city: city.data.city,
        city_slug: city.id,
        country: city.data.country,
        neighbourhood: loc.neighbourhood ?? null,
        access: t.access ?? null,
        transport: t.transport ?? null,
        precision: t.location_precision ?? null,
        best_time: t.best_time ?? null,
        story: t.story ?? null,
        url: `/${city.id}/${slugify(t.name)}`,
        photo: p?.url
          ? { url: p.url, license: p.license ?? null, attribution: p.attribution ?? null }
          : null,
      });
    }
  }
  out.sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  return out;
}

/** A short content hash, so the version changes exactly when the data does
 *  and never merely because a build ran. */
export async function feedVersion(body: string): Promise<string> {
  const bytes = new TextEncoder().encode(body);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].slice(0, 8)
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}
