// How much each city page is actually visited, for the search box's empty
// state on web and app (Hidde, 2026-09-26: "niet met de meeste bomen maar de
// meest bezochte pagina's", and "dit geldt voor app en web").
//
// Read from data/city-queue.json, which the daily digest refreshes from
// Search Console: clicks in the last ten days, then impressions. It is the one
// per-page visit figure we store; Cloudflare's beacon only reaches DATA.md as a
// top list. Clicks weigh a thousand impressions, so a page people chose beats
// a page Google merely showed.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

let cached: Map<string, number> | null = null;

/** Slug -> a popularity score; absent when the page has had no search traffic. */
export function cityPopularity(): Map<string, number> {
  if (cached) return cached;
  cached = new Map();
  const f = path.join(DATA, "city-queue.json");
  if (!fs.existsSync(f)) return cached;
  const data = JSON.parse(fs.readFileSync(f, "utf-8"));
  for (const c of data.cities ?? []) {
    const score = (c.clicks_10d ?? 0) * 1000 + (c.impressions_10d ?? 0);
    if (c.slug && score > 0) cached.set(c.slug, score);
  }
  return cached;
}
