// What a collection actually holds, for every page that asks.
//
// A GENERATED collection (blueprint v1.13, Hidde 2026-08-21) computes its own
// entry list at build time and carries an empty `entries` array on disk. That
// worked for the collection page itself, which ranked the trees inline, and it
// was silently wrong everywhere else: /collections counted `entries.length` and
// printed "0 trees, 0 cities" on four cards, /api/browse.json dropped a
// collection with no entries outright so the app never saw the tallest, the
// thickest, the autumn or the harvest list at all, and the city, country and
// question pages never cross-linked a tree that only appears in a generated one.
//
// So the ranking lives here rather than in the page, and a consumer asks this
// module what a collection holds instead of reading the file's own array. A
// curated collection still answers with its hand-written entries; nothing about
// those changes.
import { treeSlugsForCity, type CityEntry } from "./trees";

export interface RankMode {
  qualifies: (t: any) => boolean;
  /** Sort keys, highest first. */
  keys: (t: any) => number[];
  bands: { min: number; heading: string }[];
  band: (t: any) => number;
  note: (t: any) => string;
}

function n(x: number): string {
  return x.toLocaleString("en-GB");
}

// Season helpers. best_time is structured data (a month list, a kind, a label
// written per tree), which is what makes a season ranking possible at all: no
// prose is parsed and nothing is inferred.
function bestKind(t: any, k: string): boolean {
  return String(t.best_time?.kind ?? "").toLowerCase() === k;
}

/** The first month inside the season window, or null when the tree peaks outside it. */
function peakMonth(t: any, from: number, to: number): number | null {
  const ms = ((t.best_time?.months ?? []) as number[]).filter((m) => m >= from && m <= to);
  return ms.length ? Math.min(...ms) : null;
}

// The tree's own label, which says what actually happens rather than naming a
// month twice. A tree without one is filtered out rather than given a sentence
// we invented.
function seasonNote(t: any): string {
  const l = String(t.best_time?.label ?? "").trim();
  if (!l) return "";
  const s = l[0].toUpperCase() + l.slice(1);
  return /[.!?]$/.test(s) ? s : `${s}.`;
}

// Five rankings so far, and the shape is deliberately one shape: a filter, an
// order, a set of bands and one line of text per tree. Three rank on a
// measurement (age, girth, height) and two on best_time (autumn colour,
// harvest). A sixth is a config entry plus an intro, not a new page.
export const MODES: Record<string, RankMode> = {
  // Ranked on the LOWER bound of the age, never the upper: a tree recorded as
  // "100 to 500 years" has not been shown to be older than four hundred, and
  // putting it in a list of trees that clear four hundred would be the page
  // making a claim its own data does not.
  oldest: {
    qualifies: (t) => (t.age_min ?? 0) >= 400,
    keys: (t) => [t.age_min ?? 0, t.age_max ?? 0],
    band: (t) => t.age_min ?? 0,
    bands: [
      { min: 1000, heading: "Over a thousand years" },
      { min: 700, heading: "Seven hundred to a thousand years" },
      { min: 500, heading: "Five to seven hundred years" },
      { min: 400, heading: "Four to five hundred years" },
    ],
    note: (t) => {
      const lo = t.age_min ?? 0, hi = t.age_max ?? 0;
      if (lo && hi && hi > lo) return `Roughly ${n(lo)} to ${n(hi)} years old.`;
      if (lo) return `About ${n(lo)} years old.`;
      return (t.age_estimate ?? "").trim();
    },
  },
  // Girth is measured rather than estimated, so this ranking needs no
  // conservative reading: a tape around a trunk is a fact. What it does need
  // is honesty about coverage, which the intro carries: only the trees whose
  // trunk somebody has actually measured can appear.
  thickest: {
    qualifies: (t) => (t.girth_cm ?? 0) >= 400,
    keys: (t) => [t.girth_cm ?? 0],
    band: (t) => t.girth_cm ?? 0,
    bands: [
      { min: 1000, heading: "Ten metres round and more" },
      { min: 700, heading: "Seven to ten metres round" },
      { min: 500, heading: "Five to seven metres round" },
      { min: 400, heading: "Four to five metres round" },
    ],
    note: (t) => {
      const m = (t.girth_cm ?? 0) / 100;
      const arms = Math.max(2, Math.round(m / 1.6));
      return `${m.toFixed(2)} metres round the trunk, about ${arms} people with their arms outstretched.`;
    },
  },
  // Height is the measurement most people picture when they think "big tree",
  // and the one we hold least of: it comes from a register's own survey or a
  // plaque, never from our prose. A tree nobody has measured cannot appear,
  // which the intro says out loud.
  tallest: {
    qualifies: (t) => (t.height_m ?? 0) >= 25,
    keys: (t) => [t.height_m ?? 0],
    band: (t) => t.height_m ?? 0,
    bands: [
      { min: 40, heading: "Forty metres and over" },
      { min: 33, heading: "Thirty-three to forty metres" },
      { min: 28, heading: "Twenty-eight to thirty-three metres" },
      { min: 25, heading: "Twenty-five to twenty-eight metres" },
    ],
    note: (t) => {
      const m = t.height_m ?? 0;
      const floors = Math.max(2, Math.round(m / 3));
      return `${m} metres tall, about the height of a ${floors} storey building.`;
    },
  },
  // The two season rankings, added 2026-09-05. They rank on WHEN rather than on
  // how big, because "how good is this one" is a taste judgement and the
  // reader's real question is which weekend to go. Bands run in calendar order,
  // so the band value is the months left in the window: the descending window
  // the other three modes use then prints September before December without a
  // second mechanism.
  //
  // A tree qualifies only when it carries both a kind and a label, so no line on
  // either page is a sentence we wrote about a tree nobody judged.
  autumn: {
    qualifies: (t) =>
      bestKind(t, "autumn colour") && peakMonth(t, 9, 12) !== null && !!t.best_time?.label,
    keys: (t) => [t.age_min ?? 0, t.girth_cm ?? 0],
    band: (t) => 12 - (peakMonth(t, 9, 12) ?? 12),
    bands: [
      { min: 3, heading: "September" },
      { min: 2, heading: "October" },
      { min: 1, heading: "November" },
      { min: 0, heading: "December" },
    ],
    note: seasonNote,
  },
  // Fruit, nuts and mast: the kind of peak you can pick up off the ground rather
  // than photograph. August to November is the window the data actually holds;
  // a fig in June is a real peak and belongs on its own tree page, not in a
  // collection called the harvest.
  harvest: {
    qualifies: (t) =>
      bestKind(t, "fruit") && peakMonth(t, 8, 11) !== null && !!t.best_time?.label,
    keys: (t) => [t.age_min ?? 0, t.girth_cm ?? 0],
    band: (t) => 11 - (peakMonth(t, 8, 11) ?? 11),
    bands: [
      { min: 3, heading: "August" },
      { min: 2, heading: "September" },
      { min: 1, heading: "October" },
      { min: 0, heading: "November" },
    ],
    note: seasonNote,
  },
};

export interface RankRow {
  tree: any;
  citySlug: string;
  city: string;
  slug: string;
  note: string;
}

export interface CollectionLike {
  data: {
    slug: string;
    generated?: string;
    entries: { city_slug: string; tree_id: string; note: string }[];
  };
}

// One build renders every page, and the city, country and question pages each
// ask this question once per page. Ranking 2,900 trees 200 times over is work
// nobody needs done twice, so the answer is kept.
const cache = new Map<string, RankRow[]>();

/**
 * Every tree a GENERATED collection holds, best first, across all cities.
 * A curated note on a tree in the ranking still wins over the generated line,
 * which is why those hand-written entries stay in the file.
 */
export function rankedRows(
  coll: CollectionLike,
  citiesBySlug: Map<string, CityEntry>,
): RankRow[] {
  const mode = coll.data.generated ? MODES[coll.data.generated] : null;
  if (!mode) return [];
  const hit = cache.get(coll.data.slug);
  if (hit) return hit;

  const curatedNote = new Map(coll.data.entries.map((e) => [e.tree_id, e.note]));
  const all: (RankRow & { keys: number[] })[] = [];
  for (const [cslug, city] of citiesBySlug) {
    const tslugs = treeSlugsForCity(city);
    for (const t of city.data.trees) {
      if (!mode.qualifies(t) || !tslugs[t.id]) continue;
      all.push({
        tree: t, citySlug: cslug, city: city.data.city, slug: tslugs[t.id],
        note: curatedNote.get(t.id) ?? mode.note(t), keys: mode.keys(t),
      });
    }
  }
  all.sort((a, b) => {
    for (let i = 0; i < a.keys.length; i += 1) {
      if (b.keys[i] !== a.keys[i]) return b.keys[i] - a.keys[i];
    }
    return a.tree.name.localeCompare(b.tree.name);
  });
  cache.set(coll.data.slug, all);
  return all;
}

/** The ranking cut into its headed bands, in the order the page prints them. */
export function rankedBands(
  coll: CollectionLike,
  citiesBySlug: Map<string, CityEntry>,
): { heading: string; rows: RankRow[] }[] {
  const mode = coll.data.generated ? MODES[coll.data.generated] : null;
  if (!mode) return [];
  const all = rankedRows(coll, citiesBySlug);
  const out: { heading: string; rows: RankRow[] }[] = [];
  let above = Infinity;
  for (const b of mode.bands) {
    const rows = all.filter((r) => mode.band(r.tree) >= b.min && mode.band(r.tree) < above);
    above = b.min;
    if (rows.length) out.push({ heading: `${b.heading} (${rows.length})`, rows });
  }
  return out;
}

/**
 * What the collection holds, in the shape the file's own `entries` uses, so a
 * caller counting trees, picking a face or looking for a city does not have to
 * know whether the list was curated or computed.
 */
export function collectionEntries(
  coll: CollectionLike,
  citiesBySlug: Map<string, CityEntry>,
): { city_slug: string; tree_id: string; note: string }[] {
  if (!coll.data.generated) return coll.data.entries;
  return rankedRows(coll, citiesBySlug).map((r) => ({
    city_slug: r.citySlug, tree_id: r.tree.id, note: r.note,
  }));
}
