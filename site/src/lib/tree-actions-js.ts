// Tree-page actions: the sticky bar's tracking and the save heart.
// Direction: Hidde, 2026-08-14 (DECISIONS.md), copying AllTrails' funnel:
// directions primary, the app beside it, and a bookmark that needs no account.
//
// Saves live in localStorage under at_saved_v1 as {id: {n: name, u: url}},
// name and url stored AT SAVE TIME so the /saved page renders from storage
// alone, no index fetch. Same store-local-first doctrine as the passport,
// same honest limit (browser storage is per-device and can be wiped; the
// /saved page says so in one line).
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
  var btns = document.querySelectorAll('.save-btn');
  function paint(map) {
    btns.forEach(function(b) {
      var on = Boolean(map[b.dataset.tree]);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      b.querySelector('span').textContent = on ? 'Saved' : 'Save';
    });
  }
  paint(saved());
  syncSaves();
  document.addEventListener('click', function(e) {
    var d = e.target.closest('.dir-link');
    if (d) { try { at.track('directions'); } catch (err) {} }
    var b = e.target.closest('.save-btn');
    if (!b) return;
    var map = saved();
    if (map[b.dataset.tree]) {
      delete map[b.dataset.tree];
      var ds = session();
      if (ds) cloud('DELETE', '/rest/v1/saves?tree_id=eq.' + encodeURIComponent(b.dataset.tree), null, ds).catch(function() {});
    }
    else {
      map[b.dataset.tree] = { n: b.dataset.name, u: location.pathname };
      try { at.track('save'); } catch (err) {}
      var cs = session();
      if (cs) cloud('POST', '/rest/v1/saves?on_conflict=user_id,tree_id',
        [{ tree_id: b.dataset.tree, name: b.dataset.name, url: location.pathname }], cs).catch(function() {});
      // AllTrails converges every gated tap on one signup surface; ours is
      // this dialog, and until accounts open its ask is the app. Shown on the
      // FIRST save only: the save itself always works instantly and locally,
      // and a modal on every save would be nagging, not a funnel.
      if (!cs && window.atOpenSignIn && !localStorage.getItem('at_save_dialog_seen')) {
        localStorage.setItem('at_save_dialog_seen', '1');
        window.atOpenSignIn();
      }
    }
    try { localStorage.setItem(KEY, JSON.stringify(map)); } catch (err) {}
    paint(map);
  });
})();
</script>
`;
