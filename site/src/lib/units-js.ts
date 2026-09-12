// Kilometres or miles, on the website.
//
// Hidde, 2026-09-12, on the cross-platform sweep finding that the app reads
// the phone's locale and the website spoke kilometres to everybody: "die mijl
// km optie doe gewoon de benchmark na en bouw."
//
// THE BENCHMARK, looked up rather than remembered (CONVENTIONS.md 2026-09-12).
// Google Maps decides automatically from your region by default and keeps the
// override in settings; on desktop there is no toggle at all and it simply
// follows your account's region. AllTrails and komoot both put one Units
// switch in account settings and apply it to web and app alike. Nobody, on any
// of the three, puts a unit toggle next to a distance on the page. So: decide
// automatically, never ask, and when there is an override it belongs in the
// account rather than in this browser.
//
// WHAT THIS FILE DOES AND DOES NOT DO. It does the automatic half, which is
// the whole of the default behaviour and needs nothing from anybody: the
// reader's own region, read from the browser, no permission prompt, no IP
// lookup, no third-party service, and nothing stored (qa.py's
// check_nothing_is_stored_locally() would refuse a preference in localStorage,
// and it is right to: a setting that lives in one browser is a setting that
// lies on the second device).
//
// It also reads the account's own `profiles.units`, the column the APP writes
// when somebody flips the switch in its profile, so one answer serves both
// surfaces instead of each guessing separately. That column was missing from
// supabase/profiles.sql until today, which means the app's own writes have
// been landing in a column the schema never declared; it is declared now and
// the file has to be run before either surface can store a choice. Until it
// is, the read fails, is caught, and the region decides, which is the right
// behaviour rather than a fallback.
//
// The pages are static, so every distance ships rendered in metric and this
// rewrites the imperial ones in place. A span that carries its own kilometres
// in `data-km` is the whole interface: nothing here parses page text, and a
// new distance anywhere on the site is covered by using the same span.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";

export const UNITS_JS = `
<script>
(function() {
  // Miles for road distance, which is what a reader wants told: the United
  // States, the United Kingdom, Liberia and Myanmar. The UK is on this list on
  // purpose. Apple calls it a third system because it is metric for almost
  // everything and imperial for the road, and a distance to a tree is a road
  // distance; Google Maps shows miles there too.
  var IMPERIAL = ['US', 'GB', 'LR', 'MM'];

  function regionSaysMiles() {
    var langs = (navigator.languages && navigator.languages.length)
      ? navigator.languages : [navigator.language || ''];
    for (var i = 0; i < langs.length; i++) {
      var bits = String(langs[i]).split('-');
      var region = bits.length > 1 ? bits[bits.length - 1].toUpperCase() : '';
      // A bare "en" names no region and must not be guessed at: half the
      // world writes it and only part of that half reads miles.
      if (region.length === 2) return IMPERIAL.indexOf(region) !== -1;
    }
    return false;
  }

  // The app's own arithmetic, copied deliberately rather than improved on, so
  // a tree that is "0.4 mi away" on the phone is not "0.5 mi away" here.
  function miles(km) {
    var mi = km * 0.621371;
    return mi < 0.2 ? Math.round(mi * 5280) + ' ft' : mi.toFixed(1) + ' mi';
  }

  var useMiles = regionSaysMiles();

  // Idempotent on purpose: it always writes the label the current answer
  // implies, never toggles, so calling it again after the account replies or
  // after the map injects a walk line cannot compound.
  function paint() {
    var spans = document.querySelectorAll('.dist[data-km]');
    for (var i = 0; i < spans.length; i++) {
      var km = parseFloat(spans[i].getAttribute('data-km'));
      if (!isFinite(km)) continue;
      spans[i].textContent = useMiles
        ? miles(km) : (spans[i].getAttribute('data-metric') || spans[i].textContent);
    }
  }

  // The city map writes its walk line after this has run, so it repaints
  // through this rather than carrying its own copy of the arithmetic.
  window.atPaintUnits = paint;
  paint();

  function session() {
    try {
      var s = JSON.parse(localStorage.getItem('ancienttrees_session'));
      return (s && s.expires_at > Date.now() / 1000) ? s : null;
    } catch (e) { return null; }
  }

  // WHOSE ROW. The stored session holds a token and an expiry and no user id
  // (signin-js.ts writes exactly three fields), so the id comes out of the
  // token's own "sub" claim. That is free and offline; asking /auth/v1/user
  // for it, which is what /account does, would be a second round trip on
  // every page load for a number nobody is waiting on. The first version of
  // this file read s.user_id, which does not exist, so the account half
  // silently never ran: the same shape of no-op this week has already found
  // three times.
  function whoami(token) {
    try {
      var body = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
      return JSON.parse(decodeURIComponent(escape(atob(body)))).sub || '';
    } catch (e) { return ''; }
  }

  var s = session();
  if (!s) return;
  var uid = whoami(s.access_token);
  if (!uid) return;
  fetch('${SUPABASE_URL}/rest/v1/profiles?select=units&user_id=eq.' + encodeURIComponent(uid), {
    headers: { 'apikey': '${SUPABASE_KEY}', 'Authorization': 'Bearer ' + s.access_token }
  })
    .then(function(r) { return r.ok ? r.json() : []; })
    .then(function(rows) {
      var u = rows && rows[0] && rows[0].units;
      // An explicit choice overrules the region in BOTH directions, which is
      // the case somebody actually hits: a Dutch reader on an American laptop.
      if (u === 'mi' || u === 'km') {
        useMiles = (u === 'mi');
        paint();
      }
    })
    // No column yet, no network, or a stale token. All three mean the same
    // thing: the region already decided and the page is right enough.
    .catch(function() {});
})();
</script>
`;
