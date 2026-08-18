// Every mapped tree, for an app to download and keep. See lib/app-feed.ts for
// why this is one file and what the honesty fields are doing in it.
import { getCollection } from "astro:content";
import { cityIsRenderable } from "../../lib/trees";
import { feedTrees, feedVersion } from "../../lib/app-feed";

export async function GET() {
  const cities = (await getCollection("cities")).filter(cityIsRenderable);
  const trees = feedTrees(cities);
  const body = JSON.stringify(trees);
  const version = await feedVersion(body);
  return new Response(JSON.stringify({ version, count: trees.length, trees }), {
    headers: { "Content-Type": "application/json" },
  });
}
