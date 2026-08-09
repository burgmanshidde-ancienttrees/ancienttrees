// /feed.xml, Atom: the newest trees, so blogs, curators and feed readers can
// pick the site up without anyone mailing anyone (Hidde, 2026-08-08: "kunnen
// we niet op andere manieren door blogs feeds etc worden opgepikt dan
// handmatig mailen"). Static XML, no service, no dependency; the only
// passive acquisition channel that exists once and works forever. Ported
// from build_feed()/update_first_seen(), build_site.py:5940-6008.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "../lib/data-dir";
import { slugify } from "../lib/trees";
import { BASE_URL } from "../lib/schema";

// Matches Python's shared esc() = html.escape(str(s), quote=True): always
// escapes the apostrophe too, regardless of whether XML strictly requires
// it in this position (see [city].gpx.ts for the same rule applied to GPX).
function esc(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#x27;");
}

const FIRST_SEEN_PATH = path.join(DATA, "first-seen.json");

/** The date each tree first appeared, maintained by the build itself. Trees
 * carry no publication date, and a feed with invented dates is a fake feed.
 * History was backfilled once from git (2026-08-08); from here every build
 * stamps ids it has not seen with today, in the same commit that adds the
 * tree, so the record cannot drift from the data. */
function updateFirstSeen(cityList: { slug: string }[]): Record<string, string> {
  let first: Record<string, string> = {};
  try {
    first = JSON.parse(fs.readFileSync(FIRST_SEEN_PATH, "utf-8"));
  } catch {
    first = {};
  }
  const today = new Date().toISOString().slice(0, 10);
  let changed = false;
  for (const e of cityList) {
    const f = path.join(DATA, "cities", `${e.slug}.json`);
    if (!fs.existsSync(f)) continue;
    const data = JSON.parse(fs.readFileSync(f, "utf-8"));
    for (const t of data.trees ?? []) {
      if (!(t.id in first)) {
        first[t.id] = today;
        changed = true;
      }
    }
  }
  if (changed) {
    // Code-point order, not locale order: Python's sorted() compares plain
    // strings, and localeCompare would silently reorder (and needlessly
    // rewrite) the file the first time a non-ASCII-adjacent id sorts
    // differently under collation rules than under a byte comparison.
    const sorted = Object.fromEntries(
      Object.entries(first).sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0)),
    );
    fs.writeFileSync(FIRST_SEEN_PATH, JSON.stringify(sorted, null, 1));
  }
  return first;
}

export async function GET() {
  const cityList: { slug: string }[] = JSON.parse(fs.readFileSync(path.join(DATA, "city-list.json"), "utf-8")).cities ?? [];
  const first = updateFirstSeen(cityList);

  const entries: { date: string; tree: any; city: string; cslug: string }[] = [];
  for (const e of cityList) {
    const f = path.join(DATA, "cities", `${e.slug}.json`);
    if (!fs.existsSync(f)) continue;
    const data = JSON.parse(fs.readFileSync(f, "utf-8"));
    for (const t of data.trees ?? []) {
      entries.push({ date: first[t.id] ?? "2026-07-14", tree: t, city: data.city ?? "", cslug: e.slug });
    }
  }
  // Python: entries.sort(key=lambda e: (e[0], e[1]["id"]), reverse=True) -
  // descending by date, then descending by tree id within the same date.
  entries.sort((a, b) => {
    if (a.date !== b.date) return a.date < b.date ? 1 : -1;
    return a.tree.id < b.tree.id ? 1 : -1;
  });

  const items = entries.slice(0, 30).map(({ date, tree, city, cslug }) => {
    const url = `${BASE_URL}/${cslug}/${slugify(tree.name)}`;
    const story = (tree.story ?? "").trim();
    let summary = story.slice(0, 220);
    if (story.length > 220) {
      const idx = summary.lastIndexOf(" ");
      summary = (idx > -1 ? summary.slice(0, idx) : summary) + "...";
    }
    return (
      `  <entry>\n` +
      `    <title>${esc(tree.name)}, ${esc(city)}</title>\n` +
      `    <link href="${url}"/>\n` +
      `    <id>${url}</id>\n` +
      `    <updated>${date}T12:00:00Z</updated>\n` +
      `    <summary>${esc(summary)}</summary>\n` +
      `  </entry>`
    );
  });

  const feed =
    '<?xml version="1.0" encoding="utf-8"?>\n' +
    '<feed xmlns="http://www.w3.org/2005/Atom">\n' +
    `  <title>Ancient Trees: the newest remarkable trees</title>\n` +
    `  <subtitle>The most remarkable ancient trees of the world's cities, newest first, each verified against its sources.</subtitle>\n` +
    `  <link href="${BASE_URL}/feed.xml" rel="self"/>\n` +
    `  <link href="${BASE_URL}"/>\n` +
    `  <id>${BASE_URL}/feed.xml</id>\n` +
    `  <updated>${entries.length ? entries[0].date : "2026-07-14"}T12:00:00Z</updated>\n` +
    items.join("\n") +
    "\n</feed>\n";

  return new Response(feed, { headers: { "Content-Type": "application/atom+xml; charset=utf-8" } });
}
