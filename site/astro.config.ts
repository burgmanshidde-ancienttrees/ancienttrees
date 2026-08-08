// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import redirectStubs from "./src/lib/redirect-stubs-integration.ts";

// https://astro.build/config
export default defineConfig({
  site: "https://ancienttrees.app",
  output: "static",
  // Separate from Python's site/dist (scripts/build_site.py's DIST) during
  // the parallel-run migration period, per ARCHITECTURE.md's rollout plan:
  // the two generators must never write the same directory, or one silently
  // clobbers the other's output, as happened once while testing this.
  outDir: "./dist-astro",
  // Astro's default (directory format) would emit london/index.html for the
  // city page and force a trailing-slash canonical; the current site is
  // file-format throughout (london.html), and GitHub Pages would 301 the
  // mismatch. See ARCHITECTURE.md "A routing pitfall".
  build: {
    format: "file",
  },
  // Legacy-URL redirects are written directly to dist/ by this integration,
  // not through Astro's own `redirects` config: that config silently
  // collapses "/padova" and "/padova/" into one file, dropping the
  // trailing-slash form. See redirect-map.ts for the full story.
  integrations: [sitemap(), redirectStubs()],
});