// Your collection, read from your account and from nowhere else.
//
// WHAT THIS REPLACES, and why it is one file instead of the two it grew from
// (Hidde, 2026-09-02): "ik wil dat je ervoor zorgt dat er niets meer lokaal
// wordt opgeslagen. Alles wat wordt opgeslagen, moet op je account zijn. Dus
// zodra je iets liket of wat dan ook, moet dat achter een account staan."
//
// Saving was already account-gated (2026-08-30), but the SAVE ITSELF was still
// written to localStorage as a cache, and a cache with its own history is a
// second source of truth. Three faults came out of that one decision, and he
// found all three in a morning:
//
//   * Saves made in one browser before the gate existed were unioned INTO his
//     account on the next sign-in, so his account page filled up with trees he
//     had never deliberately kept ("ik zie nog steeds heel veel saved trees").
//   * A card rendered from the snapshot taken when the heart was tapped, so a
//     tree that has a photograph today showed none if it had none then, and a
//     save made in the app carried no name at all ("ik weet zeker dat hier
//     bomen tussen staan die wel een foto hebben die we nu niet tonen").
//   * That snapshot was drawn by hand-written markup instead of the one tree
//     card, so the saved list was the only place on the site where a tree does
//     not look like a tree ("een soort van boomkaart die ik helemaal niet zie
//     terugkomen op saved trees").
//
// So: the account holds WHICH trees, /api/cards.json holds WHAT THEY ARE, and
// this file joins the two. Nothing is remembered on the device. The only thing
// still in localStorage anywhere is the session token, which is not a saved
// tree, it is the account.
//
// Convention: Strava, AllTrails and Google Maps all keep the saved list inside
// the account and all render a saved item with the same card the rest of the
// product uses. See CONVENTIONS.md, "What signing out takes with it": signing
// out takes the list off the screen and the next sign-in brings it all back,
// because it lives in the account rather than on the glass.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";

export const COLLECTION_JS = `
<script>
window.atCollection = (function() {
  var SB = '${SUPABASE_URL}', KEY = '${SUPABASE_KEY}';
  // In memory for the life of this page only. Deliberately not sessionStorage:
  // that is storage too, and the rule is the rule.
  var cardsWait = null;

  // The server's verdict on the stored session: null until it answers, then
  // true or false. A session the server refused is no session, whatever the
  // browser still holds (2026-10-05, the sixth time Hidde saw a heart work
  // signed out).
  var confirmed = null;
  function session() {
    if (confirmed === false) return null;
    try {
      var s = JSON.parse(localStorage.getItem('ancienttrees_session'));
      return (s && s.access_token && s.expires_at > Date.now() / 1000) ? s : null;
    } catch (e) { return null; }
  }
  // THE SERVER DECIDES WHO IS SIGNED IN, NEVER THE BROWSER (Hidde, 2026-10-02:
  // "I can still do thumbs up save and collect tree without being logged in
  // on the website ... close this gap forever! No local storage!"). Until
  // tonight every script here trusted a session object in localStorage by its
  // own expires_at: a token revoked elsewhere, a deleted account or a hand
  // edited value painted the whole site signed in, hearts lit on tap, and the
  // refused write was swallowed. So: a stored session is CHECKED with Supabase
  // once per page load, any write the server refuses forgets it, and
  // forgetting repaints every control and the bar and opens the sign-in
  // dialog. The smoke test plants a fake session and clicks Save to prove it.
  function forget() {
    try { localStorage.removeItem('ancienttrees_session'); } catch (e) {}
    try { delete document.documentElement.dataset.signedIn; } catch (e) {}
    if (window.atPaintNav) { try { window.atPaintNav(false); } catch (e) {} }
    try { document.dispatchEvent(new CustomEvent('at:signedout')); } catch (e) {}
  }
  function refused(r) {
    if (r && (r.status === 401 || r.status === 403)) {
      forget();
      if (window.atOpenSignIn) { try { window.atOpenSignIn(); } catch (e) {} }
      return true;
    }
    return false;
  }
  var verified = null;
  function verify() {
    if (verified) return verified;
    var s = session();
    if (!s) return (verified = Promise.resolve(false));
    verified = fetch(SB + '/auth/v1/user', { headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + s.access_token } })
      .then(function(r) {
        if (r.status === 401 || r.status === 403) { confirmed = false; forget(); return false; }
        confirmed = r.ok;
        return r.ok;
      })
      .catch(function() { confirmed = true; return true; });   // offline: keep the session, the next write decides
    return verified;
  }
  // EVERY GATED TAP GOES THROUGH HERE: save, seen, vote, photo, report. It
  // acts only once the server has said this session is real; otherwise it
  // opens sign-in and does nothing else. One door, so no control can trust the
  // browser on its own again.
  function gate(onIn, onOut) {
    verify().then(function(ok) {
      var s = ok && session();
      if (s) onIn(s); else onOut();
    });
  }
  window.atGate = gate;
  function api(path, s, opts) {
    opts = opts || {};
    var h = { 'apikey': KEY, 'Authorization': 'Bearer ' + s.access_token };
    if (opts.body) { h['Content-Type'] = 'application/json'; h['Prefer'] = 'resolution=merge-duplicates'; }
    return fetch(SB + path, { method: opts.method || 'GET', headers: h,
                              body: opts.body ? JSON.stringify(opts.body) : undefined })
      .then(function(r) { refused(r); return r; });
  }
  verify();
  // What a tree IS, answered by the website rather than remembered by the
  // browser. One request, held for this page, shared by every caller.
  function catalogue() {
    if (cardsWait) return cardsWait;
    cardsWait = fetch('/api/cards.json')
      .then(function(r) { return r.ok ? r.json() : {}; })
      .catch(function() { return {}; });
    return cardsWait;
  }
  function esc(t) { return String(t == null ? '' : t)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }

  // THE SAME CARD AS EVERYWHERE ELSE. It cannot literally be TreeCard.astro,
  // which renders at build time, so it emits that component's markup from the
  // component's own data: the meta line arrives composed, the photograph
  // arrives at the two widths TreeCard asks for, and the credit arrives only
  // when the licence obliges one. Nothing here decides any of that.
  // "visited" adds the "Seen" badge over the photo, the same per-tree signal
  // TreeCard.swift's own "ticked" view draws (a filled checkmark-seal capsule,
  // top left) whenever saved.isVisited(tree.id) is true, regardless of
  // which list the card happens to render in. Web had no such badge and
  // "hearted" used to be one blanket value for a WHOLE list rather than each
  // card's own true state, so My trees and Favourites read as the same
  // unmarked card everywhere (Hidde, 2026-09-03).
  function card(id, c, hearted, visited) {
    var meta = c.m || '';
    if (c.c) meta = meta ? meta + ' \\u00b7 ' + c.c : c.c;
    // The season chip (phenology.ts seasonChipHtml, 2026-10-04): the moment's
    // own name and tint, on the photograph when there is one. English, as the
    // rest of this card is; the key arrives from /api/cards.json.
    var chip = '';
    var words = { bloom: 'In bloom', autumn: 'Autumn colour', fruit: 'In fruit', leaves: 'Fresh leaves',
                  catkins: 'Catkins', winter: 'Winter shape' };
    // No key, no chip: an unnamed "In season" said nothing (2026-10-05).
    if (c.bt && words[c.sk] && c.bt.indexOf(new Date().getMonth() + 1) !== -1) {
      chip = '<span class="best-now-inline sn-chip sn-' + c.sk + '">' + words[c.sk] + '</span>';
    }
    // The tag row (TreeCard.astro, 2026-10-04): season first, then Seen.
    var seen = visited ? '<span class="tree-card-seen">'
      + '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="#4A6B2A"/><path d="M7.5 12.5l3 3 6-6.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
      + '<span>Seen</span></span>' : '';
    var tags = (chip || seen) ? '<div class="tag-row' + (c.p ? '' : ' tag-row-under') + '">' + chip + seen + '</div>' : '';
    var on = hearted !== false;
    // The card heart (TreeCard.astro, 2026-10-04): on the photograph, or at
    // the end of the name row when there is none. No action row, no "Read
    // more": the whole card is the link.
    var HEART = ''
      + '<button class="save-btn heart-btn heart-card" type="button" data-tree="' + esc(id) + '"'
      + ' data-name="' + esc(c.n) + '" data-url="' + esc(c.u) + '"'
      + ' data-l-save="Save" data-l-saved="Saved"'
      + ' aria-pressed="' + (on ? 'true' : 'false') + '"'
      + ' aria-label="' + (on ? 'Saved ' : 'Save ') + esc(c.n) + '">'
      + '<svg class="heart" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21C6.5 16.3 3.5 13 3.5 9.6 3.5 7 5.5 5 8 5c1.6 0 3.1.8 4 2.1C12.9 5.8 14.4 5 16 5c2.5 0 4.5 2 4.5 4.6 0 3.4-3 6.7-8.5 11.4z"/></svg>'
      + '<span class="sr-only">' + (on ? 'Saved' : 'Save') + '</span></button>'
      ;
    return '<article class="tree-card tree-card-nonum tree-card-link" data-tree-id="' + esc(id) + '">'
      + (c.p ? '<div class="tree-card-photo">'
               + '<img src="' + esc(c.p) + '" srcset="'
               + esc(c.p) + ' 500w, ' + esc(c.p9 || c.p) + ' 900w" '
               + 'sizes="(max-width: 800px) 100vw, 560px" alt="' + esc(c.n)
               + '" loading="lazy">' + HEART + tags + '</div>' : '')
      + (c.cr ? '<p class="tree-card-credit">Photo: ' + esc(c.cr) + '</p>' : '')
      + '<div class="tree-card-top">' + (c.p ? '' : HEART) + '<h3 class="tree-name"><a href="' + esc(c.u) + '">'
        + esc(c.n) + '</a></h3></div>'
      + (c.p ? '' : tags)
      + (meta ? '<p class="tree-meta">' + meta + '</p>' : '')
      + '</article>';
  }

  function ids(path) {
    var s = session();
    if (!s) return Promise.resolve([]);
    return api(path, s)
      .then(function(r) { return r.ok ? r.json() : []; })
      .then(function(rows) { return (rows || []).map(function(r) { return r.tree_id; }); })
      .catch(function() { return []; });
  }

  return {
    session: session,
    forget: forget,
    verify: verify,
    gate: gate,
    catalogue: catalogue,
    card: card,
    esc: esc,
    /** Tree ids this account has saved. Signed out: nothing, and no request. */
    saves: function() { return ids('/rest/v1/saves?select=tree_id'); },
    /** Tree ids this account has checked in at. */
    visited: function() { return ids('/rest/v1/visited?select=tree_id'); },
    save: function(id, on) {
      var s = session();
      if (!s) return Promise.resolve(false);
      var p = on
        ? api('/rest/v1/saves?on_conflict=user_id,tree_id', s, { method: 'POST', body: [{ tree_id: id }] })
        : api('/rest/v1/saves?tree_id=eq.' + encodeURIComponent(id), s, { method: 'DELETE' });
      return p.then(function(r) { return r.ok; }).catch(function() { return false; });
    },
    visit: function(id, on) {
      var s = session();
      if (!s) return Promise.resolve(false);
      var p = on
        ? api('/rest/v1/visited?on_conflict=user_id,tree_id', s, { method: 'POST', body: [{ tree_id: id }] })
        : api('/rest/v1/visited?tree_id=eq.' + encodeURIComponent(id), s, { method: 'DELETE' });
      return p.then(function(r) { return r.ok; }).catch(function() { return false; });
    }
  };
})();
</script>
`;
