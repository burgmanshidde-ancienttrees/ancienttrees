// The browse facets an app needs: collections, parks, countries, species.
//
// Hidde, 2026-08-19: "kijk ook beter naar wat de website allemaal te bieden -
// al die functies moeten een plek krijgen in de app". Four page types existed
// on the website and reached the app through nothing at all, because the feeds
// carried trees, walks and species phenology and stopped there.
//
// One endpoint rather than four, for the same reason app-feed.ts gives for one
// tree file: these are small, they are always wanted together on one Explore
// screen, and four files would be four things that can drift apart.
import { getCollection } from "astro:content";
import { cityIsRenderable, renderableTrees, slugify } from "../../lib/trees";
import { feedVersion } from "../../lib/app-feed";

export async function GET() {
  const cities = (await getCollection("cities")).filter(cityIsRenderable);

  // Which trees exist, so a facet can carry a count and never point at nothing.
  const treesBySlug = new Map<string, any[]>();
  const idToTree = new Map<string, any>();
  for (const city of cities) {
    const ts = renderableTrees(city);
    treesBySlug.set(city.id, ts);
    for (const t of ts) idToTree.set(t.id, { ...t, citySlug: city.id, city: city.data.city, country: city.data.country });
  }

  const collections = (await getCollection("collectionPages"))
    .filter((c) => (c.data.status ?? "published") !== "draft")
    .map((c) => ({
      slug: c.data.slug ?? c.id,
      title: c.data.title,
      intro: c.data.intro,
      // Only entries whose tree is actually live: a collection that lists a
      // retired tree would send somebody to a page that no longer exists.
      trees: (c.data.entries ?? [])
        .map((e) => e.tree_id)
        .filter((id) => idToTree.has(id)),
    }))
    .filter((c) => c.trees.length > 0);

  const parks = (await getCollection("parks")).map((p) => {
    const inCity = treesBySlug.get(p.data.city_slug) ?? [];
    const name = (p.data.park ?? p.data.name ?? "").toLowerCase();
    const trees = inCity.filter((t) =>
      `${t.location?.address ?? ""} ${t.location?.neighbourhood ?? ""}`
        .toLowerCase()
        .includes(name),
    );
    return {
      slug: p.data.slug,
      name: p.data.name ?? p.data.park,
      citySlug: p.data.city_slug,
      intro: p.data.intro,
      trees: trees.map((t) => t.id),
    };
  }).filter((p) => p.trees.length > 0);

  const countries = (await getCollection("countries")).map((c) => {
    const trees = [...idToTree.values()].filter(
      (t) => slugify(t.country ?? "") === (c.data.slug ?? c.id),
    );
    return {
      slug: c.data.slug ?? c.id,
      name: c.data.country,
      intro: c.data.intro,
      count: trees.length,
    };
  }).filter((c) => c.count > 0);

  const species = (await getCollection("species")).map((s) => {
    const trees = [...idToTree.values()].filter(
      (t) => (t.species ?? "").toLowerCase().includes((s.data.common_name ?? "").toLowerCase()),
    );
    return {
      slug: s.data.slug ?? s.id,
      name: s.data.common_name,
      scientific: s.data.scientific_name,
      intro: s.data.intro,
      count: trees.length,
    };
  }).filter((s) => s.count > 0);

  const payload = { collections, parks, countries, species };
  const body = JSON.stringify(payload);
  return new Response(
    JSON.stringify({ version: await feedVersion(body), ...payload }),
    { headers: { "content-type": "application/json; charset=utf-8" } },
  );
}
