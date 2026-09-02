// Everything a tree card needs, keyed by tree id.
//
// Convention: our own TreeCard.astro. This is not a second way of showing a
// tree, it is the same card fed by a lookup instead of by a build-time prop.
//
// WHY IT EXISTS (Hidde, 2026-09-02, on his own saved list: "ik weet zeker dat
// hier bomen tussen staan die wel een foto hebben die we nu niet tonen", and
// "we hebben volgens mij een soort van boomcomponenten gemaakt ... die ik
// helemaal niet zie terugkomen op saved trees"). He is right on both, and they
// are one bug. The saved list rendered a tree from a SNAPSHOT taken at the
// moment somebody tapped the heart: the name and url the button carried, plus
// a photo only if the card it was tapped from happened to have one. So a save
// made from the app carried nothing, a save made before 2026-08-18 carried no
// picture, and a photograph added to a tree last night never reached a card
// saved last month. The list was showing what we once knew about a tree
// instead of what we know about it now.
//
// This is CLAUDE.md's answer-versus-rule split (2026-08-25) applied to the
// website's own client-side code rather than to the app: what a tree looks
// like is an ANSWER the site already computes, so it travels; how a meta line
// is composed, which photograph wins, and whether a licence obliges a credit
// are RULES and stay here. Every field below comes from the same helper
// TreeCard.astro calls, so the two cannot disagree.
//
// Deliberately not /api/trees.json, which the app reads: that is 4.5 MB
// because it carries every story, and a page is not going to fetch a story it
// will never print. This is the same trees with the story left out.
//
// The one thing NOT precomputed is "at its best now", which depends on the
// month you are reading in rather than the month we built in. The peak months
// travel and the client compares them with today.
import { getCollection } from "astro:content";
import { cityIsRenderable, renderableTrees, treeSlugsForCity } from "../../lib/trees";
import { usablePhoto, thumbUrl, creditRequired, creditName } from "../../lib/images";

export async function GET() {
  const cities = (await getCollection("cities")).filter(cityIsRenderable);
  const out: Record<string, unknown> = {};

  for (const city of cities) {
    const slugs = treeSlugsForCity(city);
    for (const tree of renderableTrees(city)) {
      const photo = usablePhoto(tree);
      // The same three facts in the same order as TreeCard's meta line, joined
      // here rather than in the browser so a card cannot compose it differently.
      const meta = [tree.species ?? "", tree.age_estimate ?? "", (tree.location?.neighbourhood ?? "")]
        .map((s) => String(s ?? "").trim())
        .filter(Boolean)
        .join(" · ");
      const credit = photo && creditRequired(photo.license) ? creditName(photo.attribution) : null;
      out[tree.id] = {
        n: tree.name,
        u: `/${city.id}/${slugs[tree.id]}`,
        c: city.data.city,
        // Species and country travel as their own fields as well as inside the
        // meta line, because the profile page COUNTS them ("3 species, 1
        // country", the same two numbers the app's My trees screen shows) and
        // counting by splitting a display string on a middot is the kind of
        // rule that quietly disagrees with the app's.
        ...(tree.species ? { sp: tree.species } : {}),
        k: city.data.country,
        // The pin, so a profile can draw somebody's own map without a second
        // request. Two numbers per tree against the 700 KB this file already
        // is, and it is the only place the coordinates could come from: the
        // account stores a tree id and nothing else, deliberately.
        y: tree.location.latitude,
        x: tree.location.longitude,
        ...(meta ? { m: meta } : {}),
        ...(photo?.url
          ? { p: thumbUrl(photo.url, 500), p9: thumbUrl(photo.url, 900) }
          : {}),
        ...(credit ? { cr: `${credit} (${photo!.license})` } : {}),
        ...(tree.best_time?.months?.length ? { bt: tree.best_time.months } : {}),
      };
    }
  }

  return new Response(JSON.stringify(out), { headers: { "Content-Type": "application/json" } });
}
