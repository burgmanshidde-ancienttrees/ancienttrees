// APP FIRST (Hidde, 2026-11-05: "dit is mss wel de moeite omdat we dan
// hopelijk via de app meer bomen gefotografeerd worden").
//
// A new tree of our own lives in the app before it lives on the website. It
// is in every app feed (browse, trees, walks, version) from the day it is
// written, so people with the app find it, walk to it and photograph it; it
// gets no web page, pin, card, sitemap or search-index line until a reader
// has added to it. Then the page appears, and under the reader cut
// (thin_pages.py READER_ONLY) it is indexable from its first day.
//
// Why: Google took the site back on 2026-11-04 after three days of showing
// it again, open and tagged pages alike, so the judgement is site-level and
// our noindex clean-up had not reached it. Search Console's crawl stats read
// ~145 requests a day, 38% of them discovery of pages we had just made. A
// noindexed page still costs Google a visit; a page that does not exist costs
// nothing. So new trees add nothing to what Google has to read, and the
// first pages Google sees of them carry a reader's photograph.
//
// The rule, in one place for the website (here) and once for the scripts
// (scripts/findable.py app_only(), the same three tests), as renderable() is:
//   1. not in data/web-freeze-baseline.json (the 4,046 trees live on
//      2026-11-05, which keep their pages, hard rule 3);
//   2. no reader signal on the tree (a sighting id, a contributor's
//      photograph, a stranger's public tip), the same test as reader_added();
//   3. no visible reader's note (data/tree-notes-live.json).
// Any one of those puts the tree on the web. APP_FIRST false puts every tree
// on the web again; flipping it is Hidde's.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

export const APP_FIRST = true;

// PINS, NOT PAGES (Hidde, 2026-11-06, before the Guardian piece: "put all pins
// live of the app only trees and let me see if that makes the total experience
// still work"). Half of the UK was missing from the web map (131 trees on the
// web, 122 app-only). An app-only tree now stands on every map that reads
// /api/pins.json or the explore map's features, and a tap opens its card
// (photo, name, species, age, place, save); the card carries no link because
// there is no page, and says the story is in the app. Still no page, no
// sitemap line, no search-index line: pins are data, not URLs, so Google gets
// nothing new to crawl. qa's check_an_app_only_tree_stays_off_the_web reads
// this switch. False takes the pins off again.
export const APP_ONLY_PINS = true;

let baseline: Set<string> | null = null;
let noted: Set<string> | null = null;
// Released by Hidde (data/app-first-released.json): app-only trees that get
// their pages anyway. 2026-11-06, every app-only UK tree before the Guardian
// piece ("lift limit once! this is exceptional curcumstance"). The same file
// scripts/findable.py app_only() reads.
let released: Set<string> | null = null;

function load(): void {
  if (baseline && noted && released) return;
  try {
    const doc = JSON.parse(fs.readFileSync(path.join(DATA, "app-first-released.json"), "utf-8"));
    released = new Set<string>(doc.ids ?? []);
  } catch {
    released = new Set<string>();
  }
  try {
    const doc = JSON.parse(fs.readFileSync(path.join(DATA, "web-freeze-baseline.json"), "utf-8"));
    baseline = new Set<string>(doc.ids ?? []);
  } catch {
    // No baseline means no tree is held back: the website shows everything,
    // which is the older behaviour and never a broken build.
    baseline = null;
  }
  try {
    const doc = JSON.parse(fs.readFileSync(path.join(DATA, "tree-notes-live.json"), "utf-8"));
    noted = new Set<string>(doc.trees ?? []);
  } catch {
    noted = new Set<string>();
  }
}

/** The reader_added() test of scripts/findable.py, verbatim in spirit: a
 * sighting id on the tree or its photograph, a contributor's photograph, or
 * a stranger's public tip. */
export function readerSignal(t: any): boolean {
  if (t?.found_by_reader?.tip) return true;
  const blob = JSON.stringify(t ?? {});
  return blob.includes('"sighting_id"') || blob.includes('"contributor_user_id"');
}

/** In the app, not yet on the website. */
export function treeIsAppOnly(t: any): boolean {
  if (!APP_FIRST) return false;
  load();
  if (!baseline) return false;
  if (baseline.has(t?.id)) return false;
  if (released!.has(t?.id)) return false;
  if (readerSignal(t)) return false;
  if (noted!.has(t?.id)) return false;
  return true;
}
