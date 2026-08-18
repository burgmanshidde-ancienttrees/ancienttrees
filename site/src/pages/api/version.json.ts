// The cheap poll. An app asks this on launch, compares the version with the
// one it already holds, and only pulls /api/trees.json when they differ. A few
// hundred bytes against three quarters of a megabyte, which is the whole point
// of having two files instead of one.
import { getCollection } from "astro:content";
import { cityIsRenderable } from "../../lib/trees";
import { feedTrees, feedVersion } from "../../lib/app-feed";

export async function GET() {
  const cities = (await getCollection("cities")).filter(cityIsRenderable);
  const trees = feedTrees(cities);
  const version = await feedVersion(JSON.stringify(trees));
  const citySlugs = new Set(trees.map((t) => t.city_slug));
  return new Response(JSON.stringify({
    version,
    trees: trees.length,
    cities: citySlugs.size,
    // Where each dataset lives, so a client never hardcodes a path and we can
    // move one without shipping a new build to the store.
    trees_url: "/api/trees.json",
    species_url: "/api/species.json",
    walks_url: "/api/walks.json",
  }), { headers: { "Content-Type": "application/json" } });
}
