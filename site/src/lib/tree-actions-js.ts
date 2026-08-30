// Tree-page actions: the sticky bar's tracking and the save heart.
// Direction: Hidde, 2026-08-14 (DECISIONS.md), copying AllTrails' funnel:
// directions primary, the app beside it, and a bookmark that needs no account.
//
// SAVING NEEDS AN ACCOUNT since 2026-08-30 (Hidde: "bewaren moet niet werken
// als je uitgelogd bent"). A signed-out tap opens the sign-in dialog and stores
// nothing. The account is the source of truth; at_saved_v1 survives only as a
// per-device CACHE of it, so the heart never waits on a network, and it is
// written only by somebody who is signed in.
//
// What this replaces: save-local-first with a once-a-visit ask that never
// blocked. That was right with no accounts and wrong with them. Two stores that
// merge as a union is where the drift lives, and browser storage loses a
// collection to seven days of Safari inactivity, which is the trip this is for.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";

export const TREE_ACTIONS_JS = `
<script>
(function() {
  var KEY = 'at_saved_v1';
  var SB = '${SUPABASE_URL}';
  var SBK = '${SUPABASE_KEY}';
  function session() {
    try {
      var s = JSON.parse(localStorage.getItem('ancienttrees_session'));
      return (s && s.expires_at > Date.now() / 1000) ? s : null;
    } catch (e) { return null; }
  }
  function cloud(method, path, body, s) {
    return fetch(SB + path, { method: method,
      headers: { 'apikey': SBK, 'Authorization': 'Bearer ' + s.access_token,
                 'Content-Type': 'application/json', 'Prefer': 'resolution=merge-duplicates' },
      body: body ? JSON.stringify(body) : undefined });
  }
  // Signed in: saves live in both places. Local stays the source of speed
  // (the heart never waits on a network), the cloud makes them portable, and
  // once per tab the two are merged as a union. A union cannot lose a save;
  // a delete only propagates when made while signed in, which is the honest
  // limit of a two-way sync this simple.
  function syncSaves() {
    var s = session();
    if (!s || sessionStorage.getItem('at_saves_synced')) return;
    sessionStorage.setItem('at_saves_synced', '1');
    fetch(SB + '/rest/v1/saves?select=tree_id,name,url', {
      headers: { 'apikey': SBK, 'Authorization': 'Bearer ' + s.access_token } })
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(rows) {
        if (!rows) return;
        var map = saved(), push = [];
        rows.forEach(function(r) { if (!map[r.tree_id]) map[r.tree_id] = { n: r.name, u: r.url }; });
        Object.keys(map).forEach(function(id) {
          if (!rows.some(function(r) { return r.tree_id === id; })) {
            push.push({ tree_id: id, name: map[id].n, url: map[id].u });
          }
        });
        try { localStorage.setItem(KEY, JSON.stringify(map)); } catch (e) {}
        paint(map);
        if (push.length) cloud('POST', '/rest/v1/saves?on_conflict=user_id,tree_id', push, s).catch(function() {});
      })
      .catch(function() {});
  }
  function saved() {
    try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; }
  }
  function paint(map) {
    // fresh query every time: hearts now render inside map popups and other
    // late-added nodes (atPaintSaves below), not only server markup
    document.querySelectorAll('.save-btn').forEach(function(b) {
      var on = Boolean(map[b.dataset.tree]);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      b.querySelector('span').textContent = on
        ? (b.dataset.lSaved || 'Saved') : (b.dataset.lSave || 'Save');
    });
  }
  window.atPaintSaves = function() { paint(saved()); };
  // signin-js calls this after refreshing an expired token: by then this file
  // has already run and concluded there was no session.
  window.atSyncSaves = syncSaves;
  paint(saved());
  syncSaves();
  document.addEventListener('click', function(e) {
    // Directions is tracked once, in Base.astro, off the Google Maps href.
    // Tracking .dir-link here too counted tree-page clicks twice, and only
    // two of the six directions links on the site carry that class anyway.
    var b = e.target.closest('.save-btn');
    if (!b) return;
    // SIGNED OUT SAVES NOTHING, it asks (Hidde, 2026-08-30: "bewaren moet niet
    // werken als je uitgelogd bent", and with it "al die functies moeten mensen
    // naar inloggen pushen").
    //
    // This used to save locally and ask once a visit without ever blocking,
    // which was the right call while there were no accounts and is the wrong
    // one now that there are. Two sources of truth is where the drift lives:
    // the null cards on /account the same day came out of a save whose row was
    // incomplete, and every union merge is another chance to disagree with
    // itself. It is also what browser storage does to a collection: Safari
    // wipes it after seven days without a visit, which is exactly the trip this
    // is for.
    //
    // The ask fires EVERY time now rather than once a session, because it is a
    // gate rather than a nudge and a gate that gives up is not a gate. AllTrails
    // does the same and blocks the save with it.
    var gate = session();
    if (!gate) {
      if (window.atOpenSignIn) window.atOpenSignIn(b.dataset.name);
      return;
    }
    var map = saved();
    if (map[b.dataset.tree]) {
      delete map[b.dataset.tree];
      cloud('DELETE', '/rest/v1/saves?tree_id=eq.' + encodeURIComponent(b.dataset.tree), null, gate).catch(function() {});
    }
    else {
      // data-url is the tree's own page. Falling back to location.pathname is
      // what this did everywhere, and on a city list that is the CITY page, so
      // every tree saved from a list used to link back to the city.
      map[b.dataset.tree] = { n: b.dataset.name, u: b.dataset.url || location.pathname,
                              p: b.dataset.photo || '', m: b.dataset.meta || '' };
      try { at.track('save'); } catch (err) {}
      cloud('POST', '/rest/v1/saves?on_conflict=user_id,tree_id',
        [{ tree_id: b.dataset.tree, name: b.dataset.name,
           url: b.dataset.url || location.pathname }], gate).catch(function() {});
    }
    try { localStorage.setItem(KEY, JSON.stringify(map)); } catch (err) {}
    paint(map);
  });
})();
</script>
`;
