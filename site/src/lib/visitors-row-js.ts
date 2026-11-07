// NEW FROM VISITORS on the web homepage, the app's Discover row of the same
// name (Kit/NewFromVisitors.swift, Screens/Home.swift; Hidde, 2026-11-06).
//
// Convention: the app's row, which is Unsplash's and Pinterest's creator line
// under a tile. The tile is this page's own shelf card; nothing new is drawn.
//
// The newest photographs visitors sent that went live on one of our trees,
// from the server (supabase/new-from-visitors.sql, anon-readable): one tile
// per tree, newest first, the row only from four tiles so it never stands half
// empty. Under each tile one line: a 16px avatar and the name of a public
// profile (a generated "Green Fig 1965" too, linked like any other; Hidde,
// 2026-11-07), else "A visitor". The name shows to everyone; a tap opens the profile, and signed
// out it asks for a sign-in first, the Instagram and Pinterest way (CLAUDE.md,
// Privacy and accounts). The account id only comes to a signed-in caller, so
// a signed-out page could not link the profile even if it wanted to.
//
// What a tree looks like is baked into the page at build time (#nfv-data),
// only for trees that carry a visitor's photograph: a few dozen, where
// /api/cards.json is 700 KB. A photograph newer than the last build waits for
// the next one, as its place on the tree's own page does. Nothing is kept on
// the device.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";

/** The row shows from this many tiles (NewFromVisitors.minimum). */
export const VISITORS_MIN = 4;

export function visitorsRowJs(visitorWord: string): string {
  return `
<script>
(function () {
  var SB = ${JSON.stringify(SUPABASE_URL)}, KEY = ${JSON.stringify(SUPABASE_KEY)};
  var A_VISITOR = ${JSON.stringify(visitorWord)};
  var MIN = ${VISITORS_MIN};
  function esc(t) { return String(t == null ? '' : t)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function load(token) {
    return fetch(SB + '/rest/v1/rpc/new_from_visitors', {
      method: 'POST',
      headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + (token || KEY), 'Content-Type': 'application/json' },
      body: JSON.stringify({ n: 12 })
    }).then(function (r) { return r.ok ? r.json() : []; }).catch(function () { return []; });
  }
  function paint(rows, cards) {
    var box = document.getElementById('nfv');
    var row = box && box.querySelector('.shelf-row');
    if (!row || !Array.isArray(rows)) return;
    var seen = {}, html = [];
    rows.forEach(function (r) {
      var c = cards[r.tree_id];
      if (!c || seen[r.tree_id]) return;
      seen[r.tree_id] = 1;
      // A generated name prints and links like any other (Hidde, 2026-11-07:
      // "a visitor is weird that its unclickable just give the link to their
      // made up name"); only a private profile, which has no name to give,
      // stays "A visitor".
      var real = r.author_name || null;
      var name = real || A_VISITOR;
      var av = r.author_avatar && real
        ? '<img src="' + esc(r.author_avatar) + '" alt="" loading="lazy">'
        : '<span>' + esc(name.charAt(0)) + '</span>';
      var line = '<span class="nfv-av" aria-hidden="true">' + av + '</span><span class="nfv-name">' + esc(name) + '</span>';
      html.push('<div class="shelf-card nfv-card">' +
        '<a class="nfv-tree" href="' + esc(c.u) + '" data-ev="home-visitors" data-detail="' + esc(r.tree_id) + '">' +
        '<span class="shelf-ph"><img src="' + esc(c.p) + '" alt="" loading="lazy"></span>' +
        '<b>' + esc(c.n) + '</b><span class="shelf-meta">' + esc(c.c) + '</span></a>' +
        (real
          ? (r.author_id
              ? '<a class="nfv-who" href="/profile?u=' + encodeURIComponent(r.author_id) + '">' + line + '</a>'
              : '<button type="button" class="nfv-who nfv-ask" data-sighting="' + esc(r.sighting_id) + '">' + line + '</button>')
          : '<span class="nfv-who">' + line + '</span>') +
        '</div>');
    });
    if (html.length < MIN) return;
    row.innerHTML = html.join('');
    box.hidden = false;
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.nfv-ask');
    if (!b) return;
    // The one door (atCollection.gate): a session the server accepts gets the
    // profile (the page may have painted before it answered); otherwise sign
    // in first, the app's nudge.require(.general).
    var ask = function () { if (window.atOpenSignIn) window.atOpenSignIn(null, null, null); };
    var C = window.atCollection;
    if (!C || !C.gate) { ask(); return; }
    C.gate(function (s) {
      load(s.access_token).then(function (rows) {
        var hit = (rows || []).filter(function (r) { return r.sighting_id === b.dataset.sighting; })[0];
        if (hit && hit.author_id) location.href = '/profile?u=' + encodeURIComponent(hit.author_id);
      });
    }, ask);
  });
  function start() {
    var el = document.getElementById('nfv-data');
    if (!el) return;
    var cards = {};
    try { cards = JSON.parse(el.textContent || '{}'); } catch (e) { return; }
    // The server decides who is signed in (atCollection.gate), never the browser.
    var C = window.atCollection;
    if (C && C.gate) {
      C.gate(function (s) { load(s.access_token).then(function (r) { paint(r, cards); }); },
                    function () { load(null).then(function (r) { paint(r, cards); }); });
    } else {
      load(null).then(function (r) { paint(r, cards); });
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
</script>`;
}
