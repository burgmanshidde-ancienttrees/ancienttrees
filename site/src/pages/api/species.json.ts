// The season data, so an app can answer "which tree near me is at its best
// right now" without a network call. 34 species, 3 KB gzipped.
//
// It is a separate file from the trees on purpose: phenology is a property of
// a SPECIES in a climate, not of an individual (see CLAUDE.md's calendar
// ruling), so shipping it per tree would repeat the same curve 1,377 times.
// An app joins the two on the species name, exactly as the website does.
//
// The latitude shift the website applies is deliberately NOT baked in here. It
// depends on where the tree stands, the client already knows each tree's
// coordinates, and a feed that pre-shifted would be wrong for every tree in a
// species that spans two climates.
import { loadPhenology } from "../../lib/phenology";
import { feedVersion } from "../../lib/app-feed";

export async function GET() {
  const species = [...loadPhenology().values()];
  const body = JSON.stringify(species);
  const version = await feedVersion(body);
  return new Response(JSON.stringify({ version, count: species.length, species }), {
    headers: { "Content-Type": "application/json" },
  });
}
