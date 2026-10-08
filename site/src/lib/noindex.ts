// Pages kept out of Google's index while the site recovers from the 09-28
// demotion (Hidde, 2026-10-01: "start with point 1 to 4"). The list is
// data/noindex.json, written by scripts/thin_pages.py: fallback language
// pages, the place pages of places with one to three trees, and question
// pages Search Console never showed. Pages stay live and keep their URLs
// (hard rule 3); noindex only asks Google not to list them, and the sitemap
// drops anything noindexed by itself. deploy.yml regenerates the list before
// every build. Undo by emptying `paths` and removing that step.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

let cache: Set<string> | null = null;
let googleOnly: Set<string> | null = null;

function list(): Set<string> {
  if (cache) return cache;
  const f = path.join(DATA, "noindex.json");
  const doc = fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, "utf-8")) : {};
  const raw = doc.paths ?? {};
  // { path: date first listed }; an array is the first day's shape.
  cache = new Set(Array.isArray(raw) ? raw : Object.keys(raw));
  // THE ENGINE SPLIT (Hidde, 2026-10-08: "Ok do the split"). Paths listed
  // under google_only are tree pages that only Google objects to (no
  // photograph); they carry a googlebot-only tag so Bing, DuckDuckGo and
  // Yahoo keep them. Everything else carries the generic robots tag.
  googleOnly = new Set<string>(Array.isArray(doc.google_only) ? doc.google_only : []);
  return cache;
}

/** The page's own path in the shape the list uses: no .html, no trailing slash. */
export function cleanPath(pathname: string): string {
  return pathname.replace(/\/index\.html$/, "").replace(/\.html$/, "").replace(/\/$/, "") || "/";
}

export function isNoindexed(pathname: string): boolean {
  return list().has(cleanPath(pathname));
}

/** How a page is kept out of the index: "google" (the googlebot tag, Bing keeps
 *  it), "all" (the generic robots tag), or null when it is indexed everywhere. */
export function noindexScope(pathname: string): "google" | "all" | null {
  const p = cleanPath(pathname);
  if (!list().has(p)) return null;
  return googleOnly!.has(p) ? "google" : "all";
}

/** The Google-only paths, for the sitemap Bing is handed and Google never sees. */
export function googleOnlyPaths(): string[] {
  list();
  return [...googleOnly!].sort();
}
