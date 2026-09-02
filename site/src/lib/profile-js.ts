// The profile page's own script: who you are, your counts, and your two lists.
//
// It replaces saved-list-js.ts, which rendered the saved list from a
// localStorage snapshot taken when the heart was tapped. Everything here comes
// from the account (which trees) joined to /api/cards.json (what they are), so
// a photograph added to a tree last night shows on a card saved last month,
// and a save made in the app arrives with a name instead of the word "null".
//
// The counts are Collect.swift's counts, deliberately: trees you have stood in
// front of plus the ones you added, the species among them, the countries. Two
// surfaces answering the same question must not answer it differently.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";

export const PROFILE_JS = `
<script>
(function() {
  var C = window.atCollection;
  if (!C) return;
  var SB = '${SUPABASE_URL}', KEY = '${SUPABASE_KEY}';

  function el(id) { return document.getElementById(id); }
  function setText(id, v) { var n = el(id); if (n) n.textContent = v; }

  function head(token, path) {
    // count=exact with no rows back: PostgREST answers in Content-Range.
    return fetch(SB + path + '&limit=1', { method: 'GET',
      headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + token,
                 'Prefer': 'count=exact', 'Range': '0-0' } })
      .then(function(r) {
        var cr = r.headers.get('content-range') || '';
        var n = parseInt(cr.split('/')[1], 10);
        return isNaN(n) ? 0 : n;
      }).catch(function() { return 0; });
  }

  // WHO. The name they chose, wherever they chose it; the app has had a
  // profile editor since the social half shipped, so somebody who set a name
  // on the phone must see it here rather than an empty page.
  function identity(token) {
    fetch(SB + '/auth/v1/user', { headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + token } })
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(u) {
        if (!u) return;
        var fallback = u.email ? u.email.split('@')[0] : 'Your trees';
        setText('in-handle', fallback);
        var av = el('in-avatar');
        if (av) av.textContent = (fallback[0] || '?').toUpperCase();
        if (!u.id) return;
        fetch(SB + '/rest/v1/profiles?select=display_name,avatar_url&user_id=eq.' + encodeURIComponent(u.id),
              { headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + token } })
          .then(function(r) { return r.ok ? r.json() : null; })
          .then(function(rows) {
            var p = rows && rows[0];
            if (!p) return;
            if (p.display_name) {
              setText('in-handle', p.display_name);
              if (av) av.textContent = p.display_name[0].toUpperCase();
            }
            if (p.avatar_url && av) {
              av.textContent = '';
              av.style.backgroundImage = 'url(' + p.avatar_url.replace(/[()'"]/g, '') + ')';
            }
          }).catch(function() {});
        head(token, '/rest/v1/follows?select=follower&followee=eq.' + encodeURIComponent(u.id))
          .then(function(n) { setText('n-followers', n); });
        head(token, '/rest/v1/follows?select=followee&follower=eq.' + encodeURIComponent(u.id))
          .then(function(n) { setText('n-following', n); });
      }).catch(function() {});
  }

  function list(node, empty, ids, cards, hearted) {
    if (!node) return;
    var known = ids.filter(function(id) { return cards[id]; });
    if (!known.length) {
      node.innerHTML = '';
      node.hidden = true;
      if (empty) empty.hidden = false;
      return;
    }
    if (empty) empty.hidden = true;
    known.sort(function(a, b) { return cards[a].n < cards[b].n ? -1 : 1; });
    node.innerHTML = known.map(function(id) {
      return '<li>' + C.card(id, cards[id], hearted) + '</li>';
    }).join('');
    node.hidden = false;
    if (window.atPaintSaves) window.atPaintSaves();
  }

  function load(token) {
    identity(token);
    Promise.all([C.saves(), C.visited(), C.catalogue()]).then(function(r) {
      var saves = r[0], visited = r[1], cards = r[2];
      list(el('saved-list'), el('saved-empty'), saves, cards, true);
      // My trees holds what you checked in at. The trees you ADDED are
      // rendered under it by my-trees-js, from a different table and behind a
      // signed url, because those photographs are private.
      list(el('visited-list'), null, visited, cards, false);

      // The app's three numbers, from the app's own definitions. Trees adds
      // the sightings count that my-trees-js reports separately.
      var species = {}, countries = {};
      visited.forEach(function(id) {
        var c = cards[id];
        if (!c) return;
        if (c.sp) species[c.sp] = 1;
        if (c.k) countries[c.k] = 1;
      });
      window.atVisitedCount = visited.length;
      setText('n-trees', visited.length + (window.atMineCount || 0));
      setText('n-species', Object.keys(species).length);
      setText('n-countries', Object.keys(countries).length);
      var mineEmpty = el('mine-empty');
      if (mineEmpty) mineEmpty.hidden = Boolean(visited.length || window.atMineCount);
    });
  }

  // my-trees-js calls this once it knows how many trees the person added, so
  // the Trees count is the app's count rather than half of it.
  window.atMineCounted = function(n) {
    window.atMineCount = n;
    setText('n-trees', (window.atVisitedCount || 0) + n);
    var mineEmpty = el('mine-empty');
    if (mineEmpty) mineEmpty.hidden = Boolean((window.atVisitedCount || 0) + n);
  };

  window.atLoadProfile = load;
  var s = C.session();
  if (s) load(s.access_token);
})();
</script>
`;
