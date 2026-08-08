// Ported from build_sitemap(), build_site.py:5688-5696. Replaces
// @astrojs/sitemap, which was tried first: that plugin always writes
// sitemap-index.xml + sitemap-0.xml (its chunking convention), but Search
// Console is registered against the flat /sitemap.xml this site has always
// served, and robots.txt points at that exact filename too. Found the same
// way as the redirects gap: build the real thing, inspect the output,
// compare against the Python build rather than assume the plugin matches.
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

        const today = new Date().toISOString().slice(0, 10);
        const urls = htmlFiles.map((f) => canonicalFor(path.relative(distRoot, f))).sort();
        const entries = urls.map((u) => `  <url><loc>${u}</loc><lastmod>${today}</lastmod></url>\n`).join("");
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
  if (posixRel === "index.html") return BASE_URL;
  if (posixRel.endsWith("/index.html")) return `${BASE_URL}/${posixRel.slice(0, -"/index.html".length)}`;
  return `${BASE_URL}/${posixRel.slice(0, -".html".length)}`;
}
