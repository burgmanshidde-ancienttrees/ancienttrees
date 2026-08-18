// The personal tree log, made to survive a phone.
//
// Hidde's paywall copy sells "Personal Tree Log & Badges: tick off trees
// you've stood in front of ... as your tree journal grows" (DECISIONS.md
// 2026-08-18), and his instruction with it was to make the story true. Ticking
// off has lived in one browser's localStorage since it shipped, which means a
// new phone, a cleared browser or seven days of Safari inactivity wiped a
// collection with no warning and no way back. A journal that does that is not
// a journal, and it is the exact failure PRINCIPLES.md #12 was written about.
//
// So the log syncs the way saves already do, and deliberately identically:
// local stays the source of speed, the cloud makes it portable, and the two
// are merged as a UNION once per tab. A union cannot lose a visit. The honest
// limit is the same one saves have: removing a tree only propagates when it is
// removed while signed in.
//
// Needs supabase/visited.sql run once in the Supabase SQL editor. Until then
// every request here 404s, is caught, and the log simply stays local, which is
// exactly what it did before.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";

export const VISITED_SYNC_JS = `
<script>
(function() {
  var KEY = 'ancienttrees_seen';
  var SB = '${SUPABASE_URL}';
  var SBK = '${SUPABASE_KEY}';

  function session() {
    try {
      var s = JSON.parse(localStorage.getItem('ancienttrees_session'));
      return (s && s.expires_at > Date.now() / 1000) ? s : null;
    } catch (e) { return null; }
  }
  function local() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; }
  }
  function save(list) {
    try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {}
  }
  function cloud(method, path, body, s) {
    return fetch(SB + path, { method: method,
      headers: { 'apikey': SBK, 'Authorization': 'Bearer ' + s.access_token,
                 'Content-Type': 'application/json', 'Prefer': 'resolution=merge-duplicates' },
      body: body ? JSON.stringify(body) : undefined });
  }

  // One tree, the moment it is ticked. Fire and forget: the local write has
  // already happened and the visitor should never wait on a network for a
  // tick they just made.
  window.atPushVisited = function(id, on) {
    var s = session();
    if (!s || !id) return;
    if (on === false) {
      cloud('DELETE', '/rest/v1/visited?tree_id=eq.' + encodeURIComponent(id), null, s)
        .catch(function() {});
      return;
    }
    cloud('POST', '/rest/v1/visited?on_conflict=user_id,tree_id', [{ tree_id: id }], s)
      .catch(function() {});
  };

  window.atSyncVisited = function() {
    var s = session();
    if (!s || sessionStorage.getItem('at_visited_synced')) return;
    sessionStorage.setItem('at_visited_synced', '1');
    fetch(SB + '/rest/v1/visited?select=tree_id', {
      headers: { 'apikey': SBK, 'Authorization': 'Bearer ' + s.access_token } })
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(rows) {
        if (!rows) return;   // table not created yet, or offline: stay local
        var here = local(), theirs = rows.map(function(r) { return r.tree_id; });
        var union = here.slice();
        theirs.forEach(function(id) { if (union.indexOf(id) === -1) union.push(id); });
        var push = here.filter(function(id) { return theirs.indexOf(id) === -1; });
        save(union);
        if (push.length) {
          cloud('POST', '/rest/v1/visited?on_conflict=user_id,tree_id',
                push.map(function(id) { return { tree_id: id }; }), s).catch(function() {});
        }
        if (window.atPaintPassport) window.atPaintPassport();
      })
      .catch(function() {});
  };

  window.atSyncVisited();
})();
</script>
`;
