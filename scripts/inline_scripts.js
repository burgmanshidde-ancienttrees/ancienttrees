// Does every inline <script> in the built site actually parse?
//
// Written 2026-09-18, after the whole sign-in script was dead on every page of
// the site and not one gate said so. A regex written into a TypeScript template
// literal lost a backslash on its way out, the emitted file carried
// `replace(//+$/, '')`, and the browser refused the ENTIRE script tag. With it
// went atOpenSignIn, the save heart's funnel, the drag-to-dismiss and the
// magic-link catcher. The build passed, qa passed, preflight passed, the smoke
// test passed, because a broken inline script is silent: the browser drops it
// and renders the page perfectly.
//
// Why node and not Python: this is the only thing in the toolchain that can
// answer "would a browser accept this". vm.Script compiles without running, so
// nothing here executes site code.
//
// Why one process rather than one per page: qa is a gate, and spawning node
// 15,000 times costs seven minutes. Walking the tree in node costs seconds, so
// EVERY page is checked rather than a sample, and no clever sampling rule has
// to be trusted. An earlier attempt sampled by path shape and kept 1,072 pages,
// because every city page sits at the root and so each looked unique.
//
// Usage: node scripts/inline_scripts.js <dist-dir>
// Prints one line per failure, nothing when clean, exit 1 when it found any.
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const dist = process.argv[2];
if (!dist) {
  console.error("usage: node scripts/inline_scripts.js <dist-dir>");
  process.exit(2);
}

// Non-greedy, and it skips anything with a src= (nothing to parse here) and
// JSON-LD (data, not code, and it is not JavaScript).
const SCRIPT = /<script(?![^>]*\bsrc=)([^>]*)>([\s\S]*?)<\/script>/g;

let failures = 0;
let pages = 0;
let scripts = 0;
// One page is enough to prove a shared constant is broken, and a whole-site
// listing of the same fault is noise. Report each distinct message once, with
// the first page that carries it and how many pages in total do.
const seen = new Map();

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (entry.name.endsWith(".html")) check(full);
  }
}

function check(file) {
  const html = fs.readFileSync(file, "utf8");
  pages++;
  let m;
  SCRIPT.lastIndex = 0;
  while ((m = SCRIPT.exec(html)) !== null) {
    const attrs = m[1] || "";
    const body = m[2].trim();
    if (!body) continue;
    if (/type\s*=\s*["']?application\/ld\+json/i.test(attrs)) continue;
    scripts++;
    try {
      // A module is parsed differently; nothing here ships as one, and if that
      // ever changes this is the line that has to learn about it.
      new vm.Script(body, { filename: file });
    } catch (e) {
      failures++;
      const why = String(e.message).split("\n")[0];
      const rel = path.relative(dist, file);
      if (seen.has(why)) seen.get(why).count++;
      else seen.set(why, { first: rel, count: 1 });
    }
  }
}

walk(dist);

for (const [why, info] of seen) {
  console.log(
    `${info.first}: an inline script does not parse, so the browser drops all ` +
      `of it (${why}). ${info.count} page(s) carry it.`
  );
}
console.error(`inline scripts: ${scripts} checked on ${pages} pages, ${failures} broken`);
process.exit(seen.size ? 1 : 0);
