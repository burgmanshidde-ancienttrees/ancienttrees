// The shared index behind the one search interaction (search-form.ts), on
// home and /explore. Ported from the search_index block in main(),
// build_site.py:5872-5894.
//
// Deliberately uses UNFILTERED trees (d["trees"], not renderableTrees) for
// both city tree counts and the "t" rows, matching a pre-existing Python
// quirk rather than fixing it mid-migration: a city or tree missing a
// story/location still gets a search row pointing at a URL that may not
// exist. The live widget already tolerates this in production.
import { getCollection } from "astro:content";
import { cityIsRenderable, slugify } from "../lib/trees";
import { groupTreesBySpecies, SPECIES_MIN_TREES } from "../lib/species";
import { byCityListOrderEntry } from "../lib/city-order";
import { citySearchNames } from "../lib/city-aliases";

export async function GET() {
  const allCities = byCityListOrderEntry((await getCollection("cities")).filter(cityIsRenderable));
  const countryIntros = await getCollection("countries");
  const speciesIntros = await getCollection("species");

  const byCountryCount = new Map<string, number>();
  for (const c of allCities) byCountryCount.set(c.data.country, (byCountryCount.get(c.data.country) ?? 0) + 1);
  const countryPages = new Map<string, string>();
  for (const intro of countryIntros) {
    if ((byCountryCount.get(intro.data.country) ?? 0) >= 3) countryPages.set(intro.data.country, intro.data.slug);
  }

  // A city's name in other languages, so the search finds Den Haag as well as
  // The Hague. Shipped on the row rather than as a second lookup table because
  // the widget already walks these rows once per keystroke.
  const searchNames = citySearchNames();

  const c: { city: string; country: string; n: number; u: string; a?: string[] }[] = [];
  const t: { n: string; c: string; u: string }[] = [];
  for (const entry of allCities) {
    const d = entry.data;
    const alt = searchNames[entry.id];
    c.push({ city: d.city, country: d.country, n: d.trees.length, u: entry.id,
             ...(alt && alt.length ? { a: alt } : {}) });
    for (const tree of d.trees) {
      t.push({ n: tree.name, c: d.city, u: `${entry.id}/${slugify(tree.name)}` });
    }
  }

  const k: { country: string; cities: number; n: number; u: string }[] = [];
  for (const [country, cslug] of [...countryPages.entries()].sort((a, b) => a[0].localeCompare(b[0]))) {
    const cities = allCities.filter((e) => e.data.country === country);
    const nTrees = cities.reduce((s, e) => s + e.data.trees.length, 0);
    k.push({ country, cities: cities.length, n: nTrees, u: cslug });
  }

  const introBySlug = new Map(speciesIntros.map((i) => [i.data.common_name, i]));
  const groups = groupTreesBySpecies(allCities);
  const qualifying = [...groups.entries()].filter(
    ([common, members]) => members.length >= SPECIES_MIN_TREES && introBySlug.has(common),
  );
  qualifying.sort((a, b) => b[1].length - a[1].length);
  const s = qualifying.map(([common, members]) => ({
    n: common,
    count: members.length,
    u: `species/${introBySlug.get(common)!.data.slug}`,
  }));

  return new Response(JSON.stringify({ c, k, s, t }), { headers: { "Content-Type": "application/json" } });
}
