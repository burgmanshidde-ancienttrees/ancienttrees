// The browse facets an app needs: cities, collections, parks, countries, species.
//
// Hidde, 2026-08-19: "kijk ook beter naar wat de website allemaal te bieden -
// al die functies moeten een plek krijgen in de app". Four page types existed
// on the website and reached the app through nothing at all, because the feeds
// carried trees, walks and species phenology and stopped there.
//
// One endpoint rather than four, for the same reason app-feed.ts gives for one
// tree file: these are small, they are always wanted together on one Explore
// screen, and four files would be four things that can drift apart.
//
// EVERY FACET NAMES ITS FACE (2026-08-25). Hidde, on a species card fronted by
// a photograph of a fountain: "do you save the thumbnails between app and web
// and make sure we use the same ones?" We did not. The website ranks the
// photographs in a set and honours a hand-set pin; the app took the first tree
// with a picture, because the feed carried no answer for it to read. So the
// same city could wear two different faces depending on which screen you were
// holding, and a pin fixed one of them.
//
// `face` is a TREE ID, not a url: the app already holds every tree with its
// photo, its licence and its pixel size, so an id is smaller, it survives a
// photograph being swapped, and it cannot disagree with the picture on the
// website. The choice itself is made once, in site/src/lib/images.ts, by the
// same functions the website's own pages call.
//
// The facet memberships are the website's own too, via groupTreesBySpecies and
// groupTreesByPark. They used to be re-derived here with a substring match,
// which put every Small-leaved Lime in the Lime facet and made the app's counts
// quietly disagree with the website's.
import { getCollection } from "astro:content";
import { cityIsRenderable, renderableTrees, slugify, type CityEntry } from "../../lib/trees";
import { cityFaceTree, speciesFaceTree, parkFaceTree, usablePhoto } from "../../lib/images";
import { groupTreesBySpecies } from "../../lib/species";
import { groupTreesByPark } from "../../lib/parks";
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

  /** A face only travels when the tree behind it is live and its photograph is
   * usable, so the app never looks up an id the feed does not carry. */
  const faceId = (t: { id?: string } | null): string | null =>
    t?.id && idToTree.has(t.id) ? t.id : null;

  const cityFacets = cities.map((c) => ({
    slug: c.id,
    name: c.data.city,
    country: c.data.country,
    count: (treesBySlug.get(c.id) ?? []).length,
    // The city page, the map sidebar, /cities, /countries and the app all show
    // this one picture now. hero_tree_id is how a person overrides it.
    face: faceId(cityFaceTree({ hero_tree_id: c.data.hero_tree_id, trees: renderableTrees(c) })),
  }));

  const collections = (await getCollection("collectionPages"))
    .filter((c) => (c.data.status ?? "published") !== "draft")
    .map((c) => {
      const ids = (c.data.entries ?? [])
        .map((e) => e.tree_id)
        // Only entries whose tree is actually live: a collection that lists a
        // retired tree would send somebody to a page that no longer exists.
        .filter((id) => idToTree.has(id));
      return {
        slug: c.data.slug ?? c.id,
        title: c.data.title,
        intro: c.data.intro,
        trees: ids,
        // The curated order is somebody's judgement, so the first entry with a
        // photograph wins rather than the widest one. Same rule as
        // collectionFace() on /collections.
        face: ids.find((id) => Boolean(usablePhoto(idToTree.get(id))?.url)) ?? null,
      };
    })
    .filter((c) => c.trees.length > 0);

  // The website's own park grouping, keyed the way /parks keys its intros.
  const parkGroups = groupTreesByPark(cities);
  const parks = (await getCollection("parks")).map((p) => {
    const g = parkGroups.get(`${p.data.city_slug} ${p.data.park}`);
    const trees = g?.trees ?? [];
    return {
      slug: p.data.slug,
      name: p.data.name ?? p.data.park,
      citySlug: p.data.city_slug,
      intro: p.data.intro,
      trees: trees.map((t) => t.id),
      face: faceId(parkFaceTree(trees)),
    };
  }).filter((p) => p.trees.length > 0);

  const countries = (await getCollection("countries")).map((c) => {
    const trees = [...idToTree.values()].filter(
      (t) => slugify(t.country ?? "") === (c.data.slug ?? c.id),
    );
    // The biggest city's face, which is what /countries shows: a country is
    // introduced by its strongest place, not by whichever tree sorted first.
    const inCountry = cities
      .filter((x) => x.data.country === c.data.country)
      .sort((a, b) => renderableTrees(b).length - renderableTrees(a).length
        || a.data.city.localeCompare(b.data.city));
    let face: string | null = null;
    for (const city of inCountry) {
      face = faceId(cityFaceTree({ hero_tree_id: city.data.hero_tree_id, trees: renderableTrees(city) }));
      if (face) break;
    }
    return {
      slug: c.data.slug ?? c.id,
      name: c.data.country,
      intro: c.data.intro,
      count: trees.length,
      face,
    };
  }).filter((c) => c.count > 0);

  // Species membership by exact common name, the website's own grouping. The
  // count filter that /species applies (three trees) is a decision about which
  // CARDS to print, not about which species exist, so it stays on that page:
  // the app still needs a face and an intro for a species page it can reach
  // from any tree.
  const speciesMembers = groupTreesBySpecies(cities as CityEntry[]);
  const species = (await getCollection("species")).map((s) => {
    const members = speciesMembers.get(s.data.common_name ?? "") ?? [];
    return {
      slug: s.data.slug ?? s.id,
      name: s.data.common_name,
      scientific: s.data.scientific_name,
      intro: s.data.intro,
      count: members.length,
      // face_tree_id is a person saying "this photograph, not that one", and it
      // is the only thing that can tell a portrait from a close-up of bark.
      face: faceId(speciesFaceTree(s.data.face_tree_id, members.map((m) => m.tree))),
    };
  }).filter((s) => s.count > 0);

  const payload = { cities: cityFacets, collections, parks, countries, species };
  const body = JSON.stringify(payload);
  return new Response(
    JSON.stringify({ version: await feedVersion(body), ...payload }),
    { headers: { "content-type": "application/json; charset=utf-8" } },
  );
}
