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

// Sign in with Apple ON THE WEB (2026-09-12, Hidde: "why is apple login not
// available on mobile web? Everything should be consistent across platform").
//
// The honest answer to his question is two things stacked, and only one of them
// was ours. The button was never built here: the app got Apple on 2026-08-20
// and the web dialog got Google the same day, which is the both-surfaces rule
// failing in the same file that already confesses to it once, about the Google
// mark staying a bare pill here for a fortnight after it was fixed in the app.
//
// The second half is why it was never one line away. The APP signs in with
// Apple natively, POST /auth/v1/token?grant_type=id_token, and that flow needs
// nothing from Apple but the bundle id listed in Supabase's authorized client
// ids. The WEB has no native credential to present, so it takes the ordinary
// OAuth redirect, /auth/v1/authorize?provider=apple, exactly as Google does.
// That flow authenticates US to Apple, and Apple will not accept a bundle id
// for it: it needs a SERVICES ID, which is a second identifier registered for
// the web half, plus a .p8 signing key. Both live in Hidde's Apple Developer
// account and neither can be created from here.
//
// So the flag, and it is false until he has done that. Everything else is
// built and wired: flipping this one word puts the button on the dialog and on
// /account, in all eight languages. It is false rather than absent because a
// sign-in button that bounces the visitor to a Supabase error page is the dead
// check-in button of 2026-07-29 all over again, and that one shipped on 345
// pages because nobody pressed it.
//
// What he has to do, once, in two consoles:
//   1. developer.apple.com, Identifiers, new SERVICES ID (say
//      app.ancienttrees.web). Enable Sign in with Apple, Configure, and give it
//      ancienttrees.app as the domain and
//      https://caimvxiyrtifilimlkqw.supabase.co/auth/v1/callback as the return
//      URL.
//   2. Keys, new key with Sign in with Apple enabled. Apple hands over the .p8
//      ONCE and never again.
//   3. Supabase, Authentication, Providers, Apple: the Services ID goes in
//      client ids BEFORE the bundle id that is already there, and the key
//      details produce the secret. Order matters, it is what avoids Apple's
//      "unacceptable audience in id_token".
// Then flip this to true. The bundle id staying in that list is what keeps the
// app's native sign-in working, so this adds a route rather than moving one.
export const APPLE_SIGNIN = false;

// Cloudflare Web Analytics: cookieless and aggregate only, chosen 2026-07-21
// specifically because it needs no consent banner. build_site.py:849.
export const ANALYTICS_TOKEN = "fcbbfb8b426c4f6aa2066b00be6454f6";

// The project identity, never the owner's name (Hidde, 2026-08-01).
// build_site.py:847.
export const CONTACT_EMAIL = "info@ancienttrees.app";

// Where "Sponsor this project" sends people. Hidde opened the page himself on
// 2026-08-26, which is the only way it could happen: a payment provider means
// his name, his bank details and his agreement to somebody's terms (hard
// rules 2 and 5). Ko-fi takes no platform fee on donations and the money runs
// through his own PayPal; the amounts and any tiers live in his dashboard,
// which is where pricing belongs.
//
// Setting this string is the switch. Empty means no button, a noindexed
// sponsor page and no footer link, so nothing half-built ever faces a reader.
export const SPONSOR_URL = "https://ko-fi.com/ancienttrees";

// The iOS app, live in the App Store since 2026-09-03 (id looked up through
// Apple's own iTunes lookup rather than remembered). Two things read this: the
// smart app banner in Base.astro, and every download button on the site.
//
// The team id is the other half of the pair and it belongs to the universal
// links rather than to any page: it is what
// site/public/.well-known/apple-app-site-association hands Apple so the OS
// knows this domain and that app are the same product.
export const APP_STORE_ID = "6806177833";
export const APP_STORE_URL = `https://apps.apple.com/app/id${APP_STORE_ID}`;
export const APP_BUNDLE_ID = "app.ancienttrees.AncientTrees";
export const APPLE_TEAM_ID = "5EWWC3M8L2";

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

// build_site.py:85-88. Still plain <script>/<link> tags rather than the
// maplibre-gl npm package, so the island's behaviour stays byte-for-byte what
// Python shipped (worker loading, CSS, version) with no bundler-mediated
// difference. What changed on 2026-08-16 is the HOST: these are the same
// v4.7.1 files, vendored into site/public/assets and served from our own
// origin instead of unpkg.com.
//
// Three reasons, in the order they matter here. Privacy: unpkg saw the IP and
// user-agent of every visitor to every page with a map, which is most of the
// site, and the privacy page states we run no third-party tracking. Speed: a
// deferred script still needs its own DNS lookup and TLS handshake to a
// foreign host, while our own origin is already connected by the time the
// parser reaches this tag. Reliability: an unpkg outage took the maps out on
// every page, and the map is the product.
//
// Same bytes, so no behaviour changes; the smoke test asserts maps construct.
// Upgrading MapLibre now means re-fetching both files at the new version and
// renaming them here, which is deliberate: the version is visible in the
// filename rather than hidden in a URL nobody reads.
export const MAPLIBRE_JS = "/assets/maplibre-gl-4.7.1.js";
export const MAPLIBRE_CSS = "/assets/maplibre-gl-4.7.1.css";
// Our own style, generated by scripts/build_map_style.py from OpenFreeMap's
// positron and served from our own origin. Same tiles, same glyphs, same
// sprite, same attribution: a restyle rather than a new dependency.
//
// positron spends 20 layers on roads and 1 on parks, which for a site about
// trees standing in parks hides the content: on the stock style the Vondelpark
// is the same grey as the buildings around it. Regenerate with the script, do
// not hand-edit the JSON.
export const MAP_STYLE = "/assets/map-style.json";

// The map credit, passed to every map as customAttribution rather than left to
// the style file (2026-09-12). The style DOES carry it on its openmaptiles
// source, and MapLibre still rendered an empty control on the city pages: the
// source is declared by TileJSON url, and the attribution that comes back with
// the resolved TileJSON wins over the one written in the style. Measured on the
// deployed site: /explore showed the credit, /lisbon showed nothing at all, from
// the same style file. customAttribution is not conditional on any of that.
//
// It matters more than it looks. City and tree pages render without a footer,
// so with an empty control those pages credited OpenStreetMap nowhere and had
// no route to /sources either. The link at the end is that route, and it is
// where Valhalla and FOSSGIS are named.
export const MAP_CREDIT =
  'Map &copy; <a href="https://openfreemap.org" target="_blank" rel="noopener">OpenFreeMap</a>, '
  + '<a href="https://www.openmaptiles.org/" target="_blank" rel="noopener">OpenMapTiles</a>, '
  + '<a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'
  + ' contributors. <a href="/sources">Sources</a>';
