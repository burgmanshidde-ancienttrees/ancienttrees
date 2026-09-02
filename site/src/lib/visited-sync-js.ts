// The personal tree log: which trees you have stood in front of.
//
// Hidde's paywall copy sells "Personal Tree Log & Badges: tick off trees
// you've stood in front of ... as your tree journal grows" (DECISIONS.md
// 2026-08-18), and his instruction with it was to make the story true.
//
// IT LIVES IN THE ACCOUNT AND NOWHERE ELSE, since 2026-09-02 (Hidde: "er niets
// meer lokaal wordt opgeslagen. Alles wat wordt opgeslagen, moet op je account
// zijn. Dus zodra je iets liket of wat dan ook, moet dat achter een account
// staan"). Until then it was localStorage first with the account as a copy,
// merged as a union, and that arrangement has now produced the same fault
// twice: a leftover from an old browsing session is indistinguishable from
// something the person meant to keep, and it arrives in their account on the
// next sign-in as a tick they never made.
//
// It also never survived the thing it exists for. Browser storage goes when
// somebody clears their data, does not exist in private browsing, never
// crosses from a phone to a laptop, and Safari on iOS deletes it after seven
// days without a visit, which is exactly the trip this feature is for. A
// journal that does that is not a journal (PRINCIPLES.md #12).
//
// So a check-in needs an account, the same as a save does, and the tick goes
// straight to the visited table. Needs supabase/visited.sql to have been run;
// until then every request 404s, is caught, and a tick simply does not stick,
// which is honest and visible rather than silently local.
//
// The reading and writing live in lib/collection-js.ts, which arrives with
// TREE_ACTIONS_JS on every page that carries a check-in button.
export const VISITED_SYNC_JS = `
<script>
(function() {
  var C = window.atCollection;
  if (!C) return;
  // The account's answer, held for this page only. Never written to storage.
  var seen = null;

  window.atVisited = function() { return seen || []; };
  window.atHasVisited = function(id) { return Boolean(seen && seen.indexOf(id) !== -1); };
  window.atSignedIn = function() { return Boolean(C.session()); };

  // One tree, the moment it is ticked. Painted first, written second: the
  // person should never wait on a network for a tick they just made, and the
  // account is what decides on the next load.
  window.atPushVisited = function(id, on) {
    if (!id || !seen) return;
    var at = seen.indexOf(id);
    if (on === false) { if (at !== -1) seen.splice(at, 1); }
    else if (at === -1) { seen.push(id); }
    C.visit(id, on !== false);
  };

  window.atSyncVisited = function() {
    if (!C.session()) {
      seen = [];
      if (window.atPaintPassport) window.atPaintPassport();
      return;
    }
    C.visited().then(function(list) {
      seen = list;
      if (window.atPaintPassport) window.atPaintPassport();
    });
  };

  window.atSyncVisited();
})();
</script>
`;
