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
