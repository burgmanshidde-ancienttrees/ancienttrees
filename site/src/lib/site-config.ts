// Ported from the constants at the top of build_site.py (lines 55-90).
export const BASE_URL = "https://ancienttrees.app";

// The account track (Hidde, 2026-07-26): flipping this is his call, made in
// a session, never by a run. Flipped True 2026-07-30 once account deletion
// was verified end-to-end. build_site.py:68.
export const AUTH_ENABLED = true;

// Hidde's Supabase project (2026-07-28). The publishable key is public by
// design. build_site.py:70-71.
export const SUPABASE_URL = "https://caimvxiyrtifilimlkqw.supabase.co";
export const SUPABASE_KEY = "sb_publishable_qOTuw-LCejk2VhO2J6aXGQ_6X2O2mgb";

// Cloudflare Web Analytics: cookieless and aggregate only, chosen 2026-07-21
// specifically because it needs no consent banner. build_site.py:849.
export const ANALYTICS_TOKEN = "fcbbfb8b426c4f6aa2066b00be6454f6";

// The project identity, never the owner's name (Hidde, 2026-08-01).
// build_site.py:847.
export const CONTACT_EMAIL = "info@ancienttrees.app";

export const TITLE_MAX = 60;
export const DESC_MAX = 155;
// The floor a generated description should reach before it is allowed to stop
// on a sentence boundary. Google renders roughly 155 characters and that text
// is the entire click decision; anything much under 110 is both flagged by
// audit tools and, more to the point, leaves reason-to-go unread. 120 sits
// deliberately above that flag so a description clears it rather than grazing
// it. Only metaFromStory uses this: hand-written city and question copy is
// already comfortably long and is not padded to a number.
export const DESC_MIN = 120;

// build_site.py:85-88. Loaded from a CDN via plain <script>/<link> tags,
// same as the current site, rather than bundled through the maplibre-gl npm
// package: this keeps the island's behavior byte-for-byte identical to what
// Python already ships (worker loading, CSS, version) instead of introducing
// a bundler-mediated difference. Revisit once there's a reason to.
export const MAPLIBRE_JS = "https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js";
export const MAPLIBRE_CSS = "https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css";
export const MAP_STYLE = "https://tiles.openfreemap.org/styles/positron";
