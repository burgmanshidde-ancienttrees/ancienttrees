// Tree-page actions: the sticky bar's tracking and the save heart.
// Direction: Hidde, 2026-08-14 (DECISIONS.md), copying AllTrails' funnel:
// directions primary, the app beside it, and a bookmark that needs no account.
//
// Saves live in localStorage under at_saved_v1 as {id: {n: name, u: url}},
// name and url stored AT SAVE TIME so the /saved page renders from storage
// alone, no index fetch. Same store-local-first doctrine as the passport,
// same honest limit (browser storage is per-device and can be wiped; the
// /saved page says so in one line).
export const TREE_ACTIONS_JS = `
<script>
(function() {
  var KEY = 'at_saved_v1';
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
  document.addEventListener('click', function(e) {
    var d = e.target.closest('.dir-link');
    if (d) { try { at.track('directions'); } catch (err) {} }
    var b = e.target.closest('.save-btn');
    if (!b) return;
    var map = saved();
    if (map[b.dataset.tree]) { delete map[b.dataset.tree]; }
    else {
      map[b.dataset.tree] = { n: b.dataset.name, u: location.pathname };
      try { at.track('save'); } catch (err) {}
      // The moment after a save is the funnel (AllTrails pushes its signup
      // here; until accounts open, the app page is the honest destination).
      var fun = document.querySelector('.save-funnel');
      if (fun) fun.hidden = false;
    }
    try { localStorage.setItem(KEY, JSON.stringify(map)); } catch (err) {}
    paint(map);
  });
})();
</script>
`;
