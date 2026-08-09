// Every figure the press page quotes, computed from the published data.
// Ported from press_numbers(), build_site.py:4524-4583. Contract I's
// distinguishing rule: not one number on that page is typed by hand. The
// non-native list is the single judgement in here, and it is deliberately
// conservative: species with any native European range are left off even
// when they read as exotic, so the headline understates rather than
// flatters. It is the same list scripts/press_numbers.py uses for the
// pitch, kept here so the page and the pitch cannot drift apart.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";
import { speciesCommon } from "./species";
import type { Tree } from "./trees";

const EUROPE = new Set([
  "United Kingdom", "Italy", "Netherlands", "Spain", "Portugal", "Poland",
  "France", "Belgium", "Greece", "Germany", "Austria", "Czech Republic",
  "Ireland", "Denmark", "Sweden", "Finland", "Hungary", "Croatia",
  "Serbia", "Romania", "Switzerland", "Norway", "Slovenia", "Slovakia",
  "Bulgaria", "Estonia", "Latvia", "Lithuania",
]);

const NON_NATIVE = new Set([
  "London Plane", "Ginkgo", "Camphor Tree", "Japanese Pagoda Tree",
  "Southern Magnolia", "Coast Redwood", "Giant Sequoia",
  "Cedar of Lebanon", "Himalayan Cedar", "Atlas Cedar", "Deodar Cedar",
  "Persian Ironwood", "Black Locust", "Chinaberry", "Shellbark Hickory",
  "Osage Orange", "Bald Cypress", "Montezuma Cypress", "Mexican Cypress",
  "Tulip Tree", "Silk Tree", "Chilean Wine Palm",
  "Canary Island Date Palm", "Mexican Blue Palm",
  "Norfolk Island Hibiscus", "Australian Banyan", "Moreton Bay Fig",
  "Silky Oak", "Jacaranda", "Ombu", "Dragon Tree", "Chusan Palm",
  "Empress Tree", "Chinese Windmill Palm", "Honey Locust",
  "Northern Catalpa", "Southern Catalpa", "Red Oak", "Black Walnut",
  "American Sycamore", "Blue Gum", "Tree of Heaven", "Weeping Willow",
  "Black Mulberry", "White Mulberry", "Avocado", "Loquat",
  "Japanese Cedar", "Monkey Puzzle", "Rubber Fig", "False Kapok",
  "Date Palm", "California Fan Palm", "Pecan",
]);

export interface PressNumbers {
  trees: number;
  cities: number;
  countries: number;
  eu_trees: number;
  eu_cities: number;
  nn: number;
  nn_pct: number;
  nn_cities: number;
  plane: number;
  plane_cities: number;
  species: number;
  photos: number;
  sourced: number;
}

/** press_numbers(cities) is called with build_site.py's FULL, unfiltered
 * city-list.json roster, not just the published/renderable subset, so this
 * reads city-list.json directly rather than using the "cities" content
 * collection (which only surfaces entries that already have a data file).
 * That includes the exact quirk it inherits: `countries` counts distinct
 * data.country values among entries that HAVE a data file, but every entry
 * WITHOUT one contributes Python's `None` to that same set (from
 * `(e.get("data") or {}).get("country")`), collapsing into one extra
 * "unknown" member rather than being skipped. Matched here, not fixed. */
export function pressNumbers(): PressNumbers {
  const listPath = path.join(DATA, "city-list.json");
  const cityList: { slug: string }[] = JSON.parse(fs.readFileSync(listPath, "utf-8")).cities ?? [];

  const entries: { city: string | null; country: string | null; tree: Tree }[] = [];
  const countries = new Set<string | null>();
  for (const e of cityList) {
    const f = path.join(DATA, "cities", `${e.slug}.json`);
    if (!fs.existsSync(f)) {
      countries.add(null);
      continue;
    }
    const data = JSON.parse(fs.readFileSync(f, "utf-8"));
    countries.add(data.country ?? null);
    for (const t of data.trees ?? []) {
      entries.push({ city: data.city ?? null, country: data.country ?? null, tree: t });
    }
  }

  const eu = entries.filter((e) => e.country && EUROPE.has(e.country));
  const nn = eu.filter((e) => NON_NATIVE.has(speciesCommon(e.tree)));
  const plane = eu.filter((e) => speciesCommon(e.tree) === "London Plane");
  const cityOf = (e: { city: string | null }) => e.city;

  return {
    trees: entries.length,
    cities: cityList.length,
    countries: countries.size,
    eu_trees: eu.length,
    eu_cities: new Set(eu.map(cityOf)).size,
    nn: nn.length,
    nn_pct: eu.length ? Math.round((100 * nn.length) / eu.length) : 0,
    nn_cities: new Set(nn.map(cityOf)).size,
    plane: plane.length,
    plane_cities: new Set(plane.map(cityOf)).size,
    species: new Set(entries.map((e) => speciesCommon(e.tree))).size,
    photos: entries.filter((e) => e.tree.photo?.url).length,
    sourced: entries.filter((e) => (e.tree.verified_sources?.length ?? 0) > 0).length,
  };
}
