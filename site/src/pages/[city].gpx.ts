// Ported from build_city_gpx(), build_site.py:3751-3777. One waypoint per
// tree: the whole city's trees on a phone, working offline, no app install.
import { getCollection } from "astro:content";
import { cityIsRenderable, renderableTrees } from "../lib/trees";
import { BASE_URL } from "../lib/schema";

function esc(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

export async function getStaticPaths() {
  const allCities = (await getCollection("cities")).filter(cityIsRenderable);
  return allCities.map((city) => ({ params: { city: city.id }, props: { city } }));
}

export async function GET({ props }: { props: { city: Awaited<ReturnType<typeof getCollection<"cities">>>[number] } }) {
  const { city } = props;
  const trees = renderableTrees(city);
  const pts = trees.map((t) => {
    const loc = t.location;
    const desc = `${t.species ?? ""}. ${t.age_estimate ?? ""}. ${t.access ?? ""}`;
    return `  <wpt lat="${loc.latitude}" lon="${loc.longitude}">\n    <name>${esc(t.name)}</name>\n    <desc>${esc(desc.trim())}</desc>\n  </wpt>`;
  });
  const gpx =
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<gpx version="1.1" creator="Ancient Trees" xmlns="http://www.topografix.com/GPX/1/1">\n' +
    `  <metadata><name>Ancient Trees in ${esc(city.data.city)}</name><link href="${BASE_URL}/${city.id}"><text>ancienttrees.app</text></link></metadata>\n` +
    pts.join("\n") +
    "\n</gpx>\n";
  return new Response(gpx, { headers: { "Content-Type": "application/gpx+xml" } });
}
