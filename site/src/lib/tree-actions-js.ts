// The save heart, on every page that shows a tree.
//
// Direction: Hidde, 2026-08-14 (DECISIONS.md), copying AllTrails' funnel:
// directions primary, the app beside it, a heart on the card.
//
// SAVING NEEDS AN ACCOUNT since 2026-08-30 (Hidde: "bewaren moet niet werken
// als je uitgelogd bent"). A signed-out tap opens the sign-in dialog and
// stores nothing.
//
// AND NOTHING IS STORED ON THE DEVICE since 2026-09-02 (Hidde: "ik wil dat je
// ervoor zorgt dat er niets meer lokaal wordt opgeslagen. Alles wat wordt
// opgeslagen, moet op je account zijn"). The gate was right and the CACHE
// behind it was not: at_saved_v1 kept its own copy of every save and merged it
// into the account as a union on the next sign-in, so saves made in a browser
// long before the gate existed arrived in his account as trees he had never
// kept. A union cannot lose a save, which was the argument for it, and it also
// cannot tell a save from a leftover.
//
// So there is one store, the account, and the heart paints from it. That costs
// one request per page before the hearts are right, which is the honest price
// of a single source of truth and is what every product that syncs a list
// pays. In exchange a delete is a delete on every device, which the union
// could never manage.
//
// lib/collection-js.ts owns the reading and writing, and is PREPENDED here
// rather than imported page by page. Nine page types render a heart, and a
// dependency every one of them has to remember to include is a dependency one
// of them will forget: that is exactly how the Spanish city page shipped
// hearts with no sign-in dialog on 2026-08-14.
import { COLLECTION_JS } from "./collection-js";

export const TREE_ACTIONS_JS = COLLECTION_JS + `
<script>
(function() {
  var C = window.atCollection;
  if (!C) return;
  // The account's answer, held for this page only. Never written to storage.
  var mine = null;

  function paint() {
    document.querySelectorAll('.save-btn').forEach(function(b) {
      var on = Boolean(mine && mine[b.dataset.tree]);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      b.querySelector('span').textContent = on
        ? (b.dataset.lSaved || 'Saved') : (b.dataset.lSave || 'Save');
    });
    // The city map's pins wear the same heart (2026-09-12). One answer, two
    // paintings, so a save on a card lights its pin without a reload.
    if (window.atPaintPinFaves) window.atPaintPinFaves();
  }
  window.atHasSaved = function(id) { return Boolean(mine && mine[id]); };
  function load() {
    if (!C.session()) { mine = {}; paint(); return; }
    C.saves().then(function(list) {
      mine = {};
      list.forEach(function(id) { mine[id] = true; });
      paint();
    });
  }
  // Hearts render inside map popups and other nodes added after this ran.
  window.atPaintSaves = paint;
  // signin-js calls this after refreshing an expired token, and the account
  // page calls it the moment a fresh sign-in lands in the url hash: by then
  // this file has already run and concluded there was nobody signed in.
  window.atSyncSaves = load;
  load();

  // THE TICK, beside the heart and handled the same way (2026-09-12).
  //
  // It reads and writes through visited-sync-js.ts rather than keeping a
  // second copy of the account's list: one request per page, one answer, and
  // the city map's pins and passport counter paint from the same one. A page
  // that renders a .seen-btn must therefore ship VISITED_SYNC_JS as well, and
  // qa.py's check_tick_has_its_wiring() refuses one without the other.
  function paintSeen() {
    document.querySelectorAll('.seen-btn').forEach(function(b) {
      var on = Boolean(window.atHasVisited && window.atHasVisited(b.dataset.tree));
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      var t = b.querySelector('.seen-text');
      if (t) t.textContent = on ? (b.dataset.lDone || 'Ticked off')
                                : (b.dataset.lSeen || 'I have seen this one');
    });
  }
  window.atPaintSeen = paintSeen;
  paintSeen();

  document.addEventListener('click', function(e) {
    var s = e.target.closest('.seen-btn');
    if (!s) return;
    e.stopPropagation();
    // The same gate the heart carries, for the same reason: a log that lives
    // in a browser is not a log (PRINCIPLES.md #12, and 2026-09-02).
    if (!C.session()) {
      if (window.atOpenSignIn) window.atOpenSignIn(s.dataset.name);
      return;
    }
    // NO PROXIMITY CHECK. DECISIONS.md 2026-08-20: "GPS proximity is a BONUS,
    // never a gate." The dead handler this replaces asked the browser where
    // you were and refused a tick from more than a few metres out, which
    // tells somebody standing under the tree that they are not there.
    var on = !(window.atHasVisited && window.atHasVisited(s.dataset.tree));
    if (window.atPushVisited) window.atPushVisited(s.dataset.tree, on);
    if (on) { try { at.track('visit'); } catch (err) {} }
    paintSeen();
    if (window.atPaintPassport) window.atPaintPassport();
  });

  document.addEventListener('click', function(e) {
    // Directions is tracked once, in Base.astro, off the Google Maps href.
    var b = e.target.closest('.save-btn');
    if (!b) return;
    // SIGNED OUT SAVES NOTHING, it asks (Hidde, 2026-08-30: "al die functies
    // moeten mensen naar inloggen pushen"). Every time rather than once a
    // visit, because it is a gate rather than a nudge and a gate that gives up
    // is not a gate. AllTrails blocks the save the same way.
    if (!C.session()) {
      if (window.atOpenSignIn) window.atOpenSignIn(b.dataset.name);
      return;
    }
    if (!mine) mine = {};
    var id = b.dataset.tree, on = !mine[id];
    // Painted first and written second, so the heart answers the finger at
    // once. If the write fails the next page load tells the truth, which is
    // the right way round: the account decides, the screen only reports.
    if (on) { mine[id] = true; try { at.track('save'); } catch (err) {} }
    else { delete mine[id]; }
    paint();
    C.save(id, on);
  });
})();
</script>
`;
