// Every tree's place on the map and nothing else, for the city map to draw the
// trees of other places (Hidde, 2026-11-01: a city map is the explore map
// pointed at one city, so zoomed out it shows every tree in view, and a tap
// opens the tree). Fetched once and cached; the card's words come from
// /api/cards.json the moment a tree is tapped, as on /explore.
//
// Rows rather than GeoJSON: [id, lng, lat, city slug, pin priority], about a
// sixth of the size. The same trees /explore draws (ExploreMap.astro).
import { getCollection } from "astro:content";
import { cityIsRenderable } from "../../lib/trees";
import { usablePhoto } from "../../lib/images";
import { pinPriority } from "../../lib/map";
import { savesOf } from "../../lib/saves";

export async function GET() {
  const cities = (await getCollection("cities")).filter(cityIsRenderable);
  const rows: [string, number, number, string, number][] = [];
  for (const entry of cities) {
    for (const t of entry.data.trees) {
      const { longitude: x, latitude: y } = t.location;
      if (x == null || y == null) continue;
      rows.push([t.id, Math.round(x * 1e5) / 1e5, Math.round(y * 1e5) / 1e5, entry.id,
                 pinPriority(Boolean(usablePhoto(t)), savesOf(t.id))]);
    }
  }
  return new Response(JSON.stringify(rows), { headers: { "Content-Type": "application/json" } });
}
