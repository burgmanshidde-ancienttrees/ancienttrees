// Cache-busting for the one asset that changes and is served from a fixed
// path (Hidde, 2026-08-18, on being shown the failure: "als dat werkt doe maar
// dan").
//
// The bug this closes is not theoretical, it happened during the same
// session's own verification. style.css sits in public/ at /assets/style.css,
// which Astro copies through untouched, so its URL never changes however much
// the file does. A returning visitor gets fresh HTML and a cached stylesheet,
// and the two disagree: on 2026-08-18 that pairing rendered /explore's map as
// an empty grey rectangle, because the new markup met the old positioning
// rules. It resolves itself when the cache expires and it recurs on every
// layout change, which is the worst shape a bug can have: intermittent, brief,
// and invisible to whoever shipped it.
//
// A content hash in the query string is the whole fix. The URL changes exactly
// when the bytes change, so a visitor refetches exactly when they must and
// never otherwise. Astro's own asset pipeline would hash the filename instead,
// which is marginally stronger, but it means moving the stylesheet out of
// public/ and letting Vite split and inline it, and this file is linked by one
// line in one layout. The cheap fix closes the whole hole.
//
// Evaluated once per build: a module-level const, not a function called per
// page, so 300 pages cost one read.
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

/** A short content hash of a file in public/, or "" if it cannot be read. */
function hashOf(relative: string): string {
  try {
    // cwd is site/ during astro build/dev/sync, the same anchor data-dir.ts
    // relies on and for the same reason.
    const file = path.resolve(process.cwd(), "public", relative);
    return crypto.createHash("sha1").update(fs.readFileSync(file)).digest("hex").slice(0, 10);
  } catch {
    // A missing file is the build's problem to report, not this module's. An
    // unfingerprinted link still works; it is only stale-prone.
    return "";
  }
}

const styleHash = hashOf("assets/style.css");

/** The stylesheet URL to link, fingerprinted when the file could be read. */
export const STYLE_HREF = styleHash
  ? `/assets/style.css?v=${styleHash}`
  : "/assets/style.css";
