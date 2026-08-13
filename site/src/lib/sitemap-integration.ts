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
        const lastmod = sourceDates(distRoot);
        const fallback = new Date().toISOString().slice(0, 10);
        const urls = htmlFiles.map((f) => canonicalFor(path.relative(distRoot, f))).sort();
        const entries = urls
          .map((u) => `  <url><loc>${u}</loc><lastmod>${lastmod(u) ?? fallback}</lastmod></url>\n`)
          .join("");
        const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${entries}</urlset>\n`;
        fs.writeFileSync(path.join(distRoot, "sitemap.xml"), sitemap);
        fs.writeFileSync(
          path.join(distRoot, "robots.txt"),
          `User-agent: *\nAllow: /\nSitemap: ${BASE_URL}/sitemap.xml\n`
        );
        logger.info(`wrote sitemap.xml with ${urls.length} url(s)`);
      },
    },
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
