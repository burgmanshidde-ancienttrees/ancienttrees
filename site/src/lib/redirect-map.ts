// Computes the same redirect set as scripts/build_site.py's build_redirects()
// (build_site.py:5303), read from the same data files, so both generators
// agree on every old URL that must keep resolving (hard rule 3: nothing
// irreversible in public). This runs at build time in plain Node, via the
// redirectStubsIntegration (see redirect-stubs-integration.ts).
//
// Astro's own `redirects` config was tried first (it does synthesize
// meta-refresh HTML for output: 'static', which is the same shape
// redirect_stub() hand-writes). It was dropped for one concrete reason,
// found by building and inspecting the output: Astro treats "/padova" and
// "/padova/" as the same route internally and only ever materializes one
// physical file, silently dropping the trailing-slash form. The current
// site writes both `padova.html` and `padova/index.html` as genuinely
// separate files, because GitHub Pages resolves a trailing-slash request
// differently from a bare one (qa.py's resolves() encodes exactly this).
// Losing one of them is a silent 404 on an old, possibly-indexed URL, so
// this writes the stub files directly instead of trusting the framework's
// route de-duplication.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

const BASE_URL = "https://ancienttrees.app";

export interface RedirectStub {
  /** Path of the HTML file to write, relative to dist/. */
  outputPath: string;
  /** href used in the page itself: relative to outputPath's own directory. */
  targetRelative: string;
  /** Absolute canonical URL of the destination. */
  canonical: string;
  title: string;
}

// A city published under the wrong name keeps its old URL resolving.
// Mirrors RENAMED_CITY_SLUGS, build_site.py:5298.
const RENAMED_CITY_SLUGS: [string, string][] = [["padova", "padua"]];

// A tree that gets renamed keeps its old URL resolving.
// Mirrors RENAMED_TREE_SLUGS, build_site.py:5276.
const RENAMED_TREE_SLUGS: [string, string, string][] = [
  ["london", "queen-elizabeths-oak", "lon_005"],
  ["vienna", "stock-im-eisen", "vie_002"],
  ["barcelona", "plane-trees-of-la-rambla", "bcn_008"],
  ["dublin", "sculpted-cypress", "dub_007"],
  ["rome", "quercia-del-tasso", "rom_001"],
  ["berlin", "bellevue-oak", "ber_006"],
  ["athens", "trees-of-kaisariani-monastery", "ath_010"],
  ["prague", "platan-u-kostela-sv-klimenta-nove-mlyny", "prg_017"],
];

// A tree that turned out to already be published under a different city
// keeps its old URL resolving, pointed at the surviving page there.
// pot_005/pot_006 (2026-08-16): Potsdam's two Pfaueninsel oaks duplicated
// Berlin's already-published ber_012 and ber_011 (same register ids,
// coordinates within 15m, same sources); Berlin's copies are the fuller,
// earlier-sourced entries and survive. See REVIEW.md 2026-08-16 BLOCKER
// and data/leads/potsdam.json's blocked entries.
const CROSS_CITY_MERGED_TREE_SLUGS: [string, string, string, string][] = [
  ["potsdam", "door-oak-of-pfaueninsel", "berlin", "ber_012"],
  ["potsdam", "schlosswiese-oak-of-pfaueninsel", "berlin", "ber_011"],
];

// A tree pulled outright, no replacement. Mirrors REMOVED_TREE_SLUGS,
// build_site.py:5290.
// muc_015-018 (2026-08-13): a writing pass on 2026-08-12 re-wrote four
// Schlosspark Nymphenburg register entries that were already published as
// muc_011-014, giving the same four physical trees two ids and two pages
// each. The earlier ids (with address/age/best_time filled in) survive;
// these four newer, thinner duplicates were removed from data/cities/munich.json.
// warsaw/sowinskis-linden (war_003, 2026-08-17): Poland's own GDOS register
// (reproduced on Polish Wikipedia's Pomniki przyrody w Warszawie) records
// this exact monument, at this exact location, blown down by wind in 1986,
// searched for and not found in a 2004 field survey, and formally delisted
// in 2012. The story published here (from a general "oldest trees" listicle
// describing it as living, ~190 years old) was never checked against the
// official record. Hard rule 2: a tree known to be dead never ships. Pulled
// rather than fabricating a replacement at the same slug.
// las-vegas lvg_002/004/008 (2026-08-20): published the day before as Nevada
// state champions and pulled on size after Hidde asked what exactly we had put
// there if none of it is old. Every fact verified; they were simply too small
// to be worth a walk. At 51, 79 and 102 cm round they were among the smallest
// trees on the site, against a median of 375, and the 51 cm podocarpus was the
// smallest of all 1435. The eight that stay have a reason to stand there: the
// two big Winchester Park eucalypts, the mulberry students actually meet under,
// the one native, and the three anomalies of a species growing where it should
// not. Stories and sources kept in data/leads/las-vegas.json.
const REMOVED_TREE_SLUGS: [string, string][] = [
  ["las-vegas", "weeping-camperdown-elm-at-carlson"],
  ["las-vegas", "buddhist-pine-of-white-hall"],
  ["las-vegas", "texas-olive-behind-the-paint-shop"],
  ["lyon", "cedar-of-ile-barbe"],
  ["munich", "copper-beech-of-nymphenburg"],
  ["munich", "nymphenburg-lime"],
  ["munich", "fern-leaved-beech-of-nymphenburg"],
  ["munich", "weeping-beech-of-nymphenburg"],
  ["warsaw", "sowinskis-linden"],
];

// Ported verbatim from slugify(), build_site.py:918. Order matters: strip
// quotes and a leading "the " BEFORE the NFKD/ASCII fold, same as the Python.
function slugify(name: string): string {
  let s = name.toLowerCase().replace(/'/g, "").replace(/’/g, "");
  if (s.startsWith("the ")) s = s.slice(4);
  s = s
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^\x00-\x7F]/g, "");
  s = s.replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  return s;
}

function treeIsRenderable(t: any): boolean {
  const loc = t.location ?? {};
  return Boolean(t.story) && loc.latitude != null && loc.longitude != null;
}

// Mirrors the real gate in build_city_page (build_site.py:3423): a city page
// renders once it has at least one renderable tree.
function loadPublishedCitySlugs(): string[] {
  const citiesDir = path.join(DATA, "cities");
  if (!fs.existsSync(citiesDir)) return [];
  const out: string[] = [];
  for (const file of fs.readdirSync(citiesDir)) {
    if (!file.endsWith(".json")) continue;
    const data = JSON.parse(fs.readFileSync(path.join(citiesDir, file), "utf-8"));
    const trees = (data.trees ?? []).filter(treeIsRenderable);
    if (trees.length === 0) continue;
    out.push(path.basename(file, ".json"));
  }
  return out;
}

function cityName(slug: string): string {
  const file = path.join(DATA, "cities", `${slug}.json`);
  if (!fs.existsSync(file)) return slug;
  return JSON.parse(fs.readFileSync(file, "utf-8")).city ?? slug;
}

function treeSlugsForCity(citySlug: string): Record<string, string> {
  const file = path.join(DATA, "cities", `${citySlug}.json`);
  if (!fs.existsSync(file)) return {};
  const data = JSON.parse(fs.readFileSync(file, "utf-8"));
  const out: Record<string, string> = {};
  for (const t of (data.trees ?? []).filter(treeIsRenderable)) {
    out[t.id] = slugify(t.name);
  }
  return out;
}

/** Every redirect stub the build must write, mirroring build_redirects(). */
export function buildRedirectStubs(): RedirectStub[] {
  const stubs: RedirectStub[] = [];
  const published = loadPublishedCitySlugs();
  const publishedSet = new Set(published);

  for (const slug of published) {
    const canonical = `${BASE_URL}/${slug}`;
    const title = `Moved: Ancient Trees in ${cityName(slug)}`;
    stubs.push({ outputPath: `cities/${slug}/index.html`, targetRelative: `../../${slug}`, canonical, title });
    stubs.push({ outputPath: `${slug}/index.html`, targetRelative: `../${slug}`, canonical, title });
  }
  stubs.push({
    outputPath: "collections/index.html",
    targetRelative: "../collections",
    canonical: `${BASE_URL}/collections`,
    title: "Moved: Collections",
  });
  stubs.push({
    outputPath: "species/index.html",
    targetRelative: "../species",
    canonical: `${BASE_URL}/species`,
    title: "Moved: Species",
  });
  // /plus was a sibling fakedoor page, closed 2026-07-29 a day after going
  // public; stays resolvable per hard rule 3. Mirrors build_site.py:4499.
  stubs.push({
    outputPath: "plus.html",
    targetRelative: "./app",
    canonical: `${BASE_URL}/app`,
    title: "Moved: The Ancient Trees app",
  });

  for (const [citySlug, oldSlug, treeId] of RENAMED_TREE_SLUGS) {
    const slugs = treeSlugsForCity(citySlug);
    const newSlug = slugs[treeId];
    if (!newSlug || newSlug === oldSlug) continue;
    stubs.push({
      outputPath: `${citySlug}/${oldSlug}.html`,
      targetRelative: newSlug,
      canonical: `${BASE_URL}/${citySlug}/${newSlug}`,
      title: "Moved: this tree",
    });
  }

  for (const [oldSlug, newSlug] of RENAMED_CITY_SLUGS) {
    if (!publishedSet.has(newSlug)) continue;
    const canonical = `${BASE_URL}/${newSlug}`;
    const title = `Moved: Ancient Trees in ${cityName(newSlug)}`;
    stubs.push({ outputPath: `${oldSlug}.html`, targetRelative: newSlug, canonical, title });
    stubs.push({ outputPath: `${oldSlug}/index.html`, targetRelative: `../${newSlug}`, canonical, title });
    stubs.push({
      outputPath: `${oldSlug}/oldest-tree.html`,
      targetRelative: `../${newSlug}/oldest-tree`,
      canonical: `${BASE_URL}/${newSlug}/oldest-tree`,
      title,
    });
    const slugs = treeSlugsForCity(newSlug);
    for (const treeSlug of Object.values(slugs)) {
      stubs.push({
        outputPath: `${oldSlug}/${treeSlug}.html`,
        targetRelative: `../${newSlug}/${treeSlug}`,
        canonical: `${BASE_URL}/${newSlug}/${treeSlug}`,
        title: "Moved: this tree",
      });
    }
  }

  for (const [oldCitySlug, oldSlug, newCitySlug, treeId] of CROSS_CITY_MERGED_TREE_SLUGS) {
    if (!publishedSet.has(newCitySlug)) continue;
    const slugs = treeSlugsForCity(newCitySlug);
    const newSlug = slugs[treeId];
    if (!newSlug) continue;
    stubs.push({
      outputPath: `${oldCitySlug}/${oldSlug}.html`,
      targetRelative: `../${newCitySlug}/${newSlug}`,
      canonical: `${BASE_URL}/${newCitySlug}/${newSlug}`,
      title: "Moved: this tree",
    });
  }

  for (const [citySlug, oldSlug] of REMOVED_TREE_SLUGS) {
    if (!publishedSet.has(citySlug)) continue;
    stubs.push({
      outputPath: `${citySlug}/${oldSlug}.html`,
      targetRelative: `../${citySlug}`,
      canonical: `${BASE_URL}/${citySlug}`,
      title: "Moved: this tree",
    });
  }

  return stubs;
}

/** Mirrors redirect_stub(), build_site.py:5261, byte for byte in structure. */
export function renderRedirectStub(targetRel: string, canonical: string, title: string): string {
  const esc = (s: string) =>
    s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  return (
    `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">` +
    `<meta http-equiv="refresh" content="0; url=${targetRel}">` +
    `<link rel="canonical" href="${canonical}">` +
    `<title>${esc(title)}</title>` +
    `<script>window.location.replace("${targetRel}");</script></head>` +
    `<body><p>This page moved to <a href="${targetRel}">${canonical}</a>.</p></body></html>`
  );
}
