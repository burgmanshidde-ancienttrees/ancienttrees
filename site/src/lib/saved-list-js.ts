// The saved-trees list, rendered in the browser from localStorage.
//
// It lives under /account since 2026-08-18 (Hidde: "saved trees is een losse
// pagina en staat niet onder account, dit is totaal niet conventioneel, gooi
// die samen en doe het onder je account"). He is right and it is the
// convention: Strava, AllTrails and Google Maps all keep the saved list inside
// the account area rather than as a sibling of it, because a saved list is
// something you own, not a section of the site.
//
// It cannot use TreeCard.astro, because it renders from localStorage in the
// visitor's browser rather than at build time, so it emits that component's
// markup by hand. Any change to the card has to be made in both places, which
// is a real cost and the reason nothing else does this.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";

export const SAVED_LIST_JS = `

<script>
(function() {
  var list = document.getElementById('saved-list');
  var empty = document.getElementById('saved-empty');
  function localMap() {
    try { return JSON.parse(localStorage.getItem('at_saved_v1') || '{}'); } catch (e) { return {}; }
  }
  // The same card the rest of the site shows (Hidde, 2026-08-18: one component,
  // one way of showing a tree). This page cannot use TreeCard.astro because it
  // renders from localStorage in the browser, so it emits that component's
  // markup instead, and any change to the card has to be made in both places.
  // What it cannot fill is species, age and the photograph: a save stores only
  // a name and a url, so the card renders with those slots empty rather than
  // with invented content. The city name comes from the search index, which is
  // a static file the search box already fetches.
  var CITY = {};
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
  function card(id, it) {
    var city = CITY[it.u] || '';
    // The photograph and the meta line ride along with the save since
    // 2026-08-18, so a saved tree looks like the card it was saved from.
    // Saves made before that carry neither, and those slots stay empty rather
    // than showing a placeholder.
    var meta = it.m ? (city ? it.m + ' \u00b7 ' + city : it.m) : city;
    return '<article class="tree-card tree-card-nonum tree-card-link" data-tree-id="' + esc(id) + '">'
      + (it.p ? '<div class="tree-card-photo"><img src="' + esc(it.p) + '" alt="' + esc(it.n)
                + '" loading="lazy"></div>' : '')
      + '<div class="tree-card-top"><h3 class="tree-name"><a href="' + esc(it.u) + '">'
        + esc(it.n) + '</a></h3></div>'
      + (meta ? '<p class="tree-meta">' + esc(meta) + '</p>' : '')
      + '<p class="tree-more"><a href="' + esc(it.u) + '">Read more and get directions &rarr;</a></p>'
      + '<button class="save-btn heart-btn heart-compact" type="button" data-tree="' + esc(id) + '"'
      + ' data-name="' + esc(it.n) + '" data-url="' + esc(it.u) + '"'
      + ' data-photo="' + esc(it.p || '') + '" data-meta="' + esc(it.m || '') + '"'
      + ' data-l-save="Save" data-l-saved="Saved"'
      + ' aria-pressed="true" aria-label="Saved ' + esc(it.n) + '">'
      + '<svg class="heart" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21C6.5 16.3 3.5 13 3.5 9.6 3.5 7 5.5 5 8 5c1.6 0 3.1.8 4 2.1C12.9 5.8 14.4 5 16 5c2.5 0 4.5 2 4.5 4.6 0 3.4-3 6.7-8.5 11.4z"/></svg>'
      + '<span>Saved</span></button>'
      + '</article>';
  }
  var lastMap = {};
  function render(map) {
    lastMap = map;
    var ids = Object.keys(map);
    if (!ids.length) { list.innerHTML = ''; empty.hidden = false; list.hidden = true; return; }
    empty.hidden = true;
    ids.sort(function(a, b) { return map[a].n < map[b].n ? -1 : 1; });
    list.innerHTML = ids.map(function(id) { return '<li>' + card(id, map[id]) + '</li>'; }).join('');
    list.hidden = false;
    if (window.atPaintSaves) window.atPaintSaves();
  }
  render(localMap());
  // Fill in the city names once, then repaint. A failure here costs a line of
  // context on each card and nothing else.
  fetch('/search-index.json').then(function(r) { return r.json(); }).then(function(j) {
    (j.t || []).forEach(function(row) { CITY['/' + row.u] = row.c; });
    render(lastMap);
  }).catch(function() {});
  // Signed in: the list is the union of this device and the account.
  var s = null;
  try { s = JSON.parse(localStorage.getItem('ancienttrees_session')); } catch (e) {}
  if (!s || s.expires_at <= Date.now() / 1000) return;
  fetch('${SUPABASE_URL}/rest/v1/saves?select=tree_id,name,url', {
    headers: { 'apikey': '${SUPABASE_KEY}', 'Authorization': 'Bearer ' + s.access_token } })
    .then(function(r) { return r.ok ? r.json() : null; })
    .then(function(rows) {
      if (!rows) return;
      var map = localMap();
      rows.forEach(function(r) { if (!map[r.tree_id]) map[r.tree_id] = { n: r.name, u: r.url, p: '', m: '' }; });
      try { localStorage.setItem('at_saved_v1', JSON.stringify(map)); } catch (e) {}
      render(map);
      document.getElementById('saved-sub').textContent = 'Signed in: these follow your account to any device.';
    })
    .catch(function() {});
})();
</script>
`;
