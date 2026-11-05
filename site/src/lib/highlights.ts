// WHICH TREES OF A PLACE ARE ITS HIGHLIGHTS (Hidde, 2026-11-05, direction C
// of the city page: a shelf of highlights above the list of every tree).
//
// One rule, decided here and sent as data: the website's city page draws its
// Highlights from this, and the app reads `highlight` and `highlight_rank` on
// each tree in the feed (lib/app-feed.ts), so neither client decides it.
//
// The rule (Hidde, same day: "has a photograph plus these things", "for now
// keep it to 10", "make your best decision which to pick based on these
// factors and make it automatic, and sometimes an ambassador can change it"):
//   1. Only a tree with a photograph: a highlight is a picture.
//   2. An ambassador's picks first, in their order (data/highlight-picks.json,
//      {place slug: [tree ids]}; empty until ambassadors get a control).
//   3. Then by what readers did with the tree, counts only (data/tree-saves.json,
//      scripts/tree_saves.py nightly): a "Worth the visit" vote and a visible
//      note count 3 each, a reader's photograph 2, a Want to visit save 1. A
//      vote or a note is someone saying the walk was worth it; a save is only
//      an intention.
//   4. Ties, which today is nearly every tree, go to the oldest documented age,
//      then the page's own order.
//   5. At most 10.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";
import { usablePhoto, type TreeLike } from "./images";
import { savesOf, worthOf, notesOf } from "./saves";

export const HIGHLIGHT_MAX = 10;

let picks: Record<string, string[]> | null = null;
function picksFor(place: string): string[] {
  if (!picks) {
    try {
      const doc = JSON.parse(fs.readFileSync(path.join(DATA, "highlight-picks.json"), "utf-8"));
      picks = doc.picks ?? {};
    } catch {
      picks = {};
    }
  }
  return picks![place] ?? [];
}

function readerPhotos(t: any): number {
  const all = [t.photo, ...(Array.isArray(t.photos) ? t.photos : [])];
  const seen = new Set<string>();
  let n = 0;
  for (const p of all) {
    if (!p || p.source !== "contributor" || !p.url || seen.has(p.url)) continue;
    seen.add(p.url);
    n += 1;
  }
  return n;
}

/** What readers did with this tree, weighted (rule 3 above). */
export function readerScore(t: any): number {
  return 3 * worthOf(t.id) + 3 * notesOf(t.id) + 2 * readerPhotos(t) + savesOf(t.id);
}

function oldest(t: any): number {
  return Number(t.age_max) || Number(t.age_min) || 0;
}

/** The place's highlights, best first: tree id -> rank (0 is the first). */
export function highlightRanks(place: string, trees: TreeLike[]): Map<string, number> {
  const shot = trees.filter((t) => Boolean(usablePhoto(t)?.url)) as any[];
  const pinned = picksFor(place);
  const order = new Map(shot.map((t, i) => [t.id, i]));
  const ranked = [...shot].sort((a, b) => {
    const pa = pinned.indexOf(a.id), pb = pinned.indexOf(b.id);
    if (pa !== pb) return (pa < 0 ? Infinity : pa) - (pb < 0 ? Infinity : pb);
    const s = readerScore(b) - readerScore(a);
    if (s) return s;
    const o = oldest(b) - oldest(a);
    if (o) return o;
    return order.get(a.id)! - order.get(b.id)!;
  });
  return new Map(ranked.slice(0, HIGHLIGHT_MAX).map((t, i) => [t.id, i]));
}

/** The place's highlights as trees, best first. */
export function highlightsOf<T extends TreeLike>(place: string, trees: T[]): T[] {
  const ranks = highlightRanks(place, trees);
  return trees.filter((t: any) => ranks.has(t.id)).sort((a: any, b: any) => ranks.get(a.id)! - ranks.get(b.id)!);
}
