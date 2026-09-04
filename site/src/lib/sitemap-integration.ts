// Ported from build_sitemap(), build_site.py:5688-5696. Replaces
// @astrojs/sitemap, which was tried first: that plugin always writes
// sitemap-index.xml + sitemap-0.xml (its chunking convention), but Search
// Console is registered against the flat /sitemap.xml this site has always
// served, and robots.txt points at that exact filename too. Found the same
// way as the redirects gap: build the real thing, inspect the output,
// compare against the Python build rather than assume the plugin matches.
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import type { AstroIntegration } from "astro";
import { buildRedirectStubs } from "./redirect-map";
import { slugify } from "./slug";
import { QUESTION_SLUG } from "./i18n";

const BASE_URL = "https://ancienttrees.app";


export default function sitemapIntegration(): AstroIntegration {
  return {
    name: "ancienttrees-sitemap",
    hooks: {
      "astro:build:done": async ({ dir, logger }) => {
        const distRoot = dir.protocol === "file:" ? new URL(dir).pathname : String(dir);
        const redirectPaths = new Set(buildRedirectStubs().map((s) => s.outputPath));

        // Redirect stubs are excluded by path (build_sitemap() only ever saw
        // the `pages` list, which never included them). Anything noindexed
        // (account.html, draft collections) is excluded by content, the same
        // heuristic qa.py's orphan check already uses, rather than a
        // hardcoded filename list that would silently miss the next one.
        const htmlFiles = walk(distRoot).filter((f) => {
          if (!f.endsWith(".html")) return false;
          if (redirectPaths.has(path.relative(distRoot, f))) return false;
          const text = fs.readFileSync(f, "utf-8");
          if (text.includes("noindex")) return false;
          return true;
        });

        // lastmod is the date the page's SOURCE last changed, not the date we
        // happened to build. Every URL used to carry today's date, on every
        // build, so a sitemap of 1,222 pages told Google that all of them
        // changed daily. Google only honours lastmod while it is consistently
        // accurate and discounts the whole file when it is not, which is a
        // plausible part of why 349 URLs sat at "Discovered - currently not
        // indexed" on 2026-08-13: found, never crawled. Found by reading the
        // generated sitemap after Hidde pasted that Search Console reason.
        const lastmod = pageDates(distRoot, sourceDates(distRoot));
        const fallback = new Date().toISOString().slice(0, 10);
        const urls = htmlFiles.map((f) => canonicalFor(path.relative(distRoot, f))).sort();
        const entries = urls
          .map((u) => `  <url><loc>${u}</loc><lastmod>${lastmod(u) ?? fallback}</lastmod></url>\n`)
          .join("");
        const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${entries}</urlset>\n`;
        fs.writeFileSync(path.join(distRoot, "sitemap.xml"), sitemap);
        // robots.txt is NOT written here. It used to be, three lines of it,
        // and because this hook runs after Astro has copied public/ into dist
        // it silently overwrote the real file: a robots.txt written to
        // site/public/ on 2026-09-03 reached the live site as the three-line
        // stub, with its crawler policy and its /api/ exclusion gone. The file
        // is prose that gets edited, so it belongs in public/ where it can be
        // read, and one file can only have one owner. Its Sitemap line points
        // at the flat sitemap.xml this hook writes, which is the only thing
        // the two ever had to agree on.
        logger.info(`wrote sitemap.xml with ${urls.length} url(s)`);
      },
    },
  };
}


/** Per-PAGE dates from data/lastmod.json, falling back to per-file git dates.
 *
 * Written 2026-09-04. The per-file date below is right for a page with a file
 * of its own and wrong for a tree, because a city file holds twenty: one
 * commit re-indented 21 city files without changing a fact, another set a
 * field on 139 trees across 69 files, and 2,035 of 4,244 URLs told Google they
 * changed that day. scripts/lastmod.py hashes what each page is actually built
 * from and records the date that hash last moved; this reads the map and only
 * asks git for pages the map does not cover (species, countries, collections,
 * standing pages), which have a file each and are dated right already. The
 * RULE lives in the Python script and only its ANSWER travels here, per the
 * answer-not-rule convention in CLAUDE.md: this function never hashes anything.
 */
function pageDates(
  distRoot: string,
  fallback: (url: string) => string | undefined
): (url: string) => string | undefined {
  const repo = path.resolve(distRoot, "..", "..");
  let entries: Record<string, { h: string; d: string }> = {};
  try {
    entries = JSON.parse(fs.readFileSync(path.join(repo, "data", "lastmod.json"), "utf-8")).entries ?? {};
  } catch {
    return fallback;
  }
  const langs = new Set(Object.keys(QUESTION_SLUG));
  const questionSlugs = new Set(["oldest-tree", ...Object.values(QUESTION_SLUG)]);
  // slug -> id per city, from the same slug rule the pages use.
  const slugIds = new Map<string, Map<string, string>>();
  const idsFor = (city: string): Map<string, string> => {
    const hit = slugIds.get(city);
    if (hit) return hit;
    const m = new Map<string, string>();
    try {
      const doc = JSON.parse(fs.readFileSync(path.join(repo, "data", "cities", `${city}.json`), "utf-8"));
      for (const t of doc.trees ?? []) {
        const loc = t.location ?? {};
        if (t.story && loc.latitude != null && loc.longitude != null && t.id) m.set(slugify(t.name), t.id);
      }
    } catch {
      /* no such city file: the map has nothing for it either */
    }
    slugIds.set(city, m);
    return m;
  };
  return (url: string) => {
    const p = url.replace(BASE_URL, "").replace(/^\//, "").replace(/\/$/, "");
    const seg = p.split("/").filter(Boolean);
    let prefix = "";
    if (seg.length && langs.has(seg[0])) {
      prefix = `${seg.shift()}:`;
    }
    let key: string | undefined;
    if (seg.length === 1) key = `${prefix}city:${seg[0]}`;
    else if (seg.length === 2 && questionSlugs.has(seg[1])) key = `${prefix}q:${seg[0]}`;
    else if (seg.length === 2) {
      const id = idsFor(seg[0]).get(seg[1]);
      if (id) key = `${prefix}tree:${id}`;
    }
    const hit = key ? entries[key] : undefined;
    return hit?.d ?? fallback(url);
  };
}

/** Map a canonical URL to the commit date of the file it is generated from.
 *
 * One `git log` pass over the whole repo, not one per file: 1,222 spawns would
 * dominate the build. Cities and their tree pages date from their own city
 * file, which is exactly right, because a city page changes when a tree is
 * added to it. Species, country and collection pages date from their data file.
 * Standing pages date from their .astro source. Anything unmatched falls back
 * to the build date, which is the old behaviour and is honest for a page whose
 * source we cannot identify.
 *
 * Returns a lookup that yields undefined rather than throwing when git is
 * unavailable (a shallow clone, or a checkout without history), so the build
 * degrades to the old behaviour instead of failing.
 */
function sourceDates(distRoot: string): (url: string) => string | undefined {
  const repo = path.resolve(distRoot, "..", "..");
  // Read from disk, beside the repo path this function already resolves,
  // rather than from process.cwd() at import time: a module-level constant
  // that silently reads an empty directory is a fix that reports success and
  // does nothing, which is how the language table sat unwired for five days.
  const i18nRoot = path.join(repo, "data", "i18n");
  const LANG_DIRS = new Set<string>(
    fs.existsSync(i18nRoot)
      ? fs.readdirSync(i18nRoot).filter((d) => fs.statSync(path.join(i18nRoot, d)).isDirectory())
      : []
  );
  let dates: Map<string, string>;
  try {
    const out = execFileSync(
      "git",
      ["log", "--name-only", "--format=%x00%cI", "--no-merges"],
      { cwd: repo, encoding: "utf-8", maxBuffer: 256 * 1024 * 1024 }
    );
    dates = new Map();
    let current = "";
    for (const line of out.split("\n")) {
      if (line.startsWith("\u0000")) {
        current = line.slice(1, 11);
        continue;
      }
      const f = line.trim();
      if (f && current && !dates.has(f)) dates.set(f, current);
    }
  } catch {
    return () => undefined;
  }
  return (url: string) => {
    const p = url.replace(BASE_URL, "").replace(/^\//, "").replace(/\/$/, "");
    if (!p) return dates.get("site/src/pages/index.astro");
    const seg = p.split("/");
    // A translated page (/fr/paris, /it/rome/some-tree) changes when either its
    // overlay or the English city it renders changes, so it takes the LATER of
    // the two. Without this branch `data/cities/fr.json` never matched and all
    // 496 translated URLs fell through to the build date, which stamped every
    // one of them "today" on every build. That is exactly the pattern this
    // function was written to stop: the header above records that a sitemap
    // claiming daily change on everything gets its lastmod discounted
    // wholesale, and that 349 URLs sat at "Discovered - currently not indexed"
    // while it did. The fix landed for English pages in August and never
    // covered the translations, which did not exist yet. Found 2026-08-27 by
    // reading the live sitemap: English URLs carried six distinct dates,
    // translated URLs carried exactly one.
    if (LANG_DIRS.has(seg[0]) && seg[1]) {
      const overlay = dates.get(`data/i18n/${seg[0]}/${seg[1]}.json`);
      const city = dates.get(`data/cities/${seg[1]}.json`);
      const both = [overlay, city].filter(Boolean) as string[];
      if (both.length) return both.sort()[both.length - 1];
    }
    const candidates = [
      `data/cities/${seg[0]}.json`,
      `data/species/${seg[1] ?? ""}.json`,
      `data/countries/${seg[1] ?? ""}.json`,
      `data/collections/${seg[1] ?? ""}.json`,
      `site/src/pages/${p}.astro`,
      `site/src/pages/${seg[0]}.astro`,
    ];
    for (const c of candidates) {
      const hit = dates.get(c);
      if (hit) return hit;
    }
    return undefined;
  };
}

function walk(dir: string): string[] {
  const out: string[] = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else out.push(full);
  }
  return out;
}

function canonicalFor(relPath: string): string {
  const posixRel = relPath.split(path.sep).join("/");
  // Python's build_sitemap() appends BASE_URL + "/" for the homepage
  // specifically (build_site.py:5256); every other page has no trailing
  // slash. Matched here rather than "fixed", since the canonical tag on
  // the page itself already agrees with this and Search Console is
  // registered against the trailing-slash form.
  if (posixRel === "index.html") return `${BASE_URL}/`;
  if (posixRel.endsWith("/index.html")) return `${BASE_URL}/${posixRel.slice(0, -"/index.html".length)}`;
  return `${BASE_URL}/${posixRel.slice(0, -".html".length)}`;
}
