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
import { treeSlugsForCity, renderableTrees, oldestTree,
         type CityEntry } from "./trees";

export interface RankMode {
  qualifies: (t: any) => boolean;
  /** Sort keys, highest first. */
  keys: (t: any) => number[];
  bands: { min: number; heading: string }[];
  band: (t: any) => number;
  note: (t: any) => string;
  /**
   * A mode whose unit is a PLACE rather than a tree builds its own rows here,
   * and the per-tree walk above is skipped. One row per city cannot be
   * expressed as a filter over every tree, because the question it asks
   * ("which of this city's trees is the oldest") is answered per city.
   */
  rows?: (citiesBySlug: Map<string, CityEntry>, curatedNote: Map<string, string>) => RankRow[];
  /**
   * Non-numeric banding. Returns the heading a row belongs under; the bands
   * print in the order their first row appears, so the ranking itself decides
   * which country leads rather than an alphabet.
   */
  groupBy?: (r: RankRow) => string;
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
  // Fame, added 2026-09-11 on Hidde's question "moeten we een famous tree
  // collectie maken?". It ranks on what somebody ELSE already did rather than
  // on how big the tree is: the number of language Wikipedias that wrote it up,
  // with their summed monthly reads breaking ties. That order matters more here
  // than on the other rankings, because fame judged by feel is just the trees
  // whoever wrote the list had heard of, which is the error CLAUDE.md records
  // twice already, once for cities and once for which pages to translate.
  //
  // Two languages is the floor, and it is the whole honesty of the page: one
  // local article means somebody documented the tree, which is true of half our
  // map, while a second language means it travelled. scripts/fame.py writes the
  // number and never guesses one, so a tree with no article carries no fame
  // block rather than a zero.
  famous: {
    qualifies: (t) => (t.fame?.langs ?? 0) >= 2,
    keys: (t) => [t.fame?.langs ?? 0, t.fame?.views ?? 0],
    band: (t) => t.fame?.langs ?? 0,
    bands: [
      { min: 10, heading: "Written up in ten languages and more" },
      { min: 5, heading: "Five to nine languages" },
      { min: 3, heading: "Three or four languages" },
      { min: 2, heading: "Two languages" },
    ],
    note: (t) => {
      const n = t.fame?.langs ?? 0;
      const views = t.fame?.views ?? 0;
      const wrote = `Written up in ${n} language${n === 1 ? "" : "s"} on Wikipedia`;
      // Reads are worth printing only when somebody is actually reading: at a
      // few dozen a month the number says less than the article count already
      // did, and printing it would make a quiet tree look measured rather than
      // simply less famous.
      return views >= 100
        ? `${wrote}, read about ${views.toLocaleString("en-GB")} times a month.`
        : `${wrote}.`;
    },
  },
  // One row per PLACE rather than per tree, added 2026-09-18. It is the index
  // of the site's own best-converting page type: /[city]/oldest-tree answers
  // "oldest tree in X", Google completes that phrase for every city tested
  // (BACKLOG.md, 2026-08-04), and nothing gathered those answers in one place.
  //
  // What it replaces is the reason it exists. The page was fifteen entries
  // picked by hand when the site mapped fifteen countries, and its own meta
  // description still said "the 15 countries this site covers" while the map
  // had grown to 46 countries and 626 places. That is the exact staleness
  // v1.13 introduced generated collections to end, applied to the collection
  // that had most to gain from it.
  //
  // It asks trees.ts which tree is oldest rather than deciding for itself, so
  // this page and the city's own question page can never name different trees.
  // The bands are countries, in ranked order, so the country holding the
  // oldest tree leads.
  oldest_per_place: {
    // Never reached: rows() below replaces the per-tree walk entirely.
    qualifies: () => false,
    keys: (t) => [t.age_max ?? 0, t.age_min ?? 0],
    band: (t) => t.age_max ?? 0,
    bands: [],
    note: (t) => {
      const lo = t.age_min ?? 0, hi = t.age_max ?? 0;
      if (lo && hi && hi > lo) return `Roughly ${n(lo)} to ${n(hi)} years old.`;
      if (hi) return `About ${n(hi)} years old.`;
      const est = (t.age_estimate ?? "").trim();
      // No age is not a gap to hide. It is the publish-and-ask rule of
      // 2026-08-13: say we do not know and the reader with a tape measure
      // can tell us, which is worth more than a number we guessed.
      return est || "Age not established. Tell us if you know it.";
    },
    groupBy: (r) => r.country ?? "Elsewhere",
    rows: (citiesBySlug, curatedNote) => {
      const out: (RankRow & { keys: number[] })[] = [];
      for (const [cslug, city] of citiesBySlug) {
        // Every place, including the one-tree ones. Its oldest tree is its
        // only tree, which is still the answer to "the oldest tree in X", and
        // gating on the question page would drop Old Tjikko, the Llangernyw
        // Yew and General Sherman from a list of the oldest trees we map.
        // Rows link to the TREE page in every case, so nothing here depends
        // on whether the place also publishes a question page.
        const trees = renderableTrees(city);
        if (!trees.length) continue;
        const t = oldestTree(trees, city.data);
        const slug = treeSlugsForCity(city)[t.id];
        if (!slug) continue;
        const mode = MODES.oldest_per_place;
        out.push({
          tree: t, citySlug: cslug, city: city.data.city, slug,
          country: city.data.country,
          note: curatedNote.get(t.id) ?? mode.note(t),
          keys: mode.keys(t),
        });
      }
      // Oldest first within the whole list. rankedBands then cuts it by
      // country in first-appearance order, so both the countries and the
      // cities inside them come out oldest first from this one sort.
      out.sort((a, b) => {
        for (let i = 0; i < a.keys.length; i += 1) {
          if (b.keys[i] !== a.keys[i]) return b.keys[i] - a.keys[i];
        }
        return a.city.localeCompare(b.city);
      });
      return out;
    },
  },
};

export interface RankRow {
  tree: any;
  citySlug: string;
  city: string;
  slug: string;
  note: string;
  /** Set by a place-based mode, which bands by it. */
  country?: string;
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
  // A place-based mode builds its own rows: its unit is a city, not a tree.
  if (mode.rows) {
    const rows = mode.rows(citiesBySlug, curatedNote);
    cache.set(coll.data.slug, rows);
    return rows;
  }
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
  // Named bands, in the order the ranking puts them: the band holding the
  // top row leads. Used by the place-based mode, where the heading is a
  // country and no numeric threshold could produce it.
  if (mode.groupBy) {
    const byKey = new Map<string, RankRow[]>();
    for (const r of all) {
      const k = mode.groupBy(r);
      if (!byKey.has(k)) byKey.set(k, []);
      byKey.get(k)!.push(r);
    }
    for (const [k, rows] of byKey) out.push({ heading: `${k} (${rows.length})`, rows });
    return out;
  }
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
