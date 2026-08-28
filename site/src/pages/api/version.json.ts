// The cheap poll. An app asks this on launch, compares the version with the
// one it already holds, and only pulls /api/trees.json when they differ. A few
// hundred bytes against three quarters of a megabyte, which is the whole point
// of having two files instead of one.
import { getCollection } from "astro:content";
import { cityIsRenderable } from "../../lib/trees";
import { feedTrees, feedVersion } from "../../lib/app-feed";
// EVERY FEED THE APP DOWNLOADS, not just the trees.
//
// The version was a hash of the tree data alone, so a change to any other feed
// was invisible to a phone: it asked this endpoint, saw the same version, and
// never fetched the file that had actually changed. Four city faces were fixed
// on 2026-08-28 and could not reach a single installed app, because a face
// lives in browse.json and browse.json is not the trees.
//
// This is the second time the same shape has bitten. walks.ts already carries
// the note about a phone that "was up to date with a file it had never heard
// of", when browse.json was added and no synced phone ever asked for it.
//
// The routes' own GET handlers are reused rather than their logic copied. A
// second description of what a feed contains, kept here, would drift from the
// real one within a fortnight and then this endpoint would be hashing a guess.
import { GET as browseFeed } from "./browse.json";
import { GET as speciesFeed } from "./species.json";
import { GET as walksFeed } from "./walks.json";

export async function GET() {
  const cities = (await getCollection("cities")).filter(cityIsRenderable);
  const trees = feedTrees(cities);
  const [browse, species, walks] = await Promise.all([
    browseFeed().then((r) => r.text()),
    speciesFeed().then((r) => r.text()),
    walksFeed().then((r) => r.text()),
  ]);
  const version = await feedVersion(JSON.stringify(trees) + browse + species + walks);
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
