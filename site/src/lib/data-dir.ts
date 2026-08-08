// The repo's data/ directory, Python's output and every content collection's
// input. Deliberately resolved from process.cwd() rather than
// import.meta.url: Vite relocates build-time-only modules like this one into
// dist-astro/.prerender/chunks/ during `astro build`, which breaks any path
// computed relative to the module's own file location (found by an actual
// build failing here). `astro build`/`dev`/`sync` are always invoked with
// cwd = the site/ project root, which import.meta.url is not guaranteed to
// reflect post-bundling, so cwd is the stable anchor.
import path from "node:path";

export const DATA = path.resolve(process.cwd(), "../data");
