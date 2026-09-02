// The trees somebody added themselves, on the website.
//
// Hidde, 2026-09-02, asked whether the person can reach their own tree at all:
// "de gebruiker zelf kan er ook bij toch?" They could not. A sighting lived on
// the phone and in a private table, and the website had no idea it existed, so
// somebody who photographed twenty trees saw an account page that knew only
// about the ones they had hearted.
//
// It reads the same rows the app writes (supabase/sightings.sql) with the
// person's own session, which is the whole of the access control: the RLS
// policy on that table is "auth.uid() = user_id" and there is no policy
// anywhere that lets one account read another's. Signed out, this renders
// nothing and asks for nothing.
//
// THE PHOTOGRAPHS ARE IN A PRIVATE BUCKET and stay there. Each one is fetched
// through a signed url that lasts an hour, which is the same route the app
// uses. Nothing here makes anything public.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";

export const MY_TREES_JS = `

<script>
(function() {
  var SB = "${SUPABASE_URL}", KEY = "${SUPABASE_KEY}";
  var list = document.getElementById('mine-list');
  var empty = document.getElementById('mine-empty');
  if (!list) return;

  // The app's own words for what has happened to a tree you offered
  // (Sightings.Status.label). Copied rather than reworded: the two surfaces
  // must not describe one state in two ways.
  var LABEL = { mine: 'Yours', sent: 'Sent to us', checking: 'Being checked',
                published: 'On the map', declined: 'Not this time' };

  function esc(t) { return String(t == null ? '' : t)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }

  function when(iso) {
    var d = new Date(iso);
    if (isNaN(d)) return '';
    return d.toLocaleDateString(undefined, { day: 'numeric', month: 'long', year: 'numeric' });
  }

  function card(row) {
    var meta = [row.species, when(row.taken_at)].filter(Boolean).join(' \\u00b7 ');
    var label = LABEL[row.status] || LABEL.mine;
    return '<article class="tree-card tree-card-nonum mine-card" data-id="' + esc(row.id) + '">'
      + '<div class="tree-card-photo mine-photo"' + (row.photo ? '' : ' hidden') + '>'
        + '<img alt="' + esc(row.name) + '" loading="lazy"></div>'
      + '<div class="tree-card-top"><h3 class="tree-name">' + esc(row.name || 'A tree you photographed') + '</h3></div>'
      + (meta ? '<p class="tree-meta">' + esc(meta) + '</p>' : '')
      + '<p class="mine-state"><span class="mine-dot"></span>' + esc(label) + '</p>'
      + '</article>';
  }

  // An hour is long enough to look at a page and short enough that a url
  // copied out of the markup is worth nothing tomorrow.
  function sign(token, path, img) {
    fetch(SB + '/storage/v1/object/sign/sightings/' + path, {
      method: 'POST',
      headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + token,
                 'Content-Type': 'application/json' },
      body: JSON.stringify({ expiresIn: 3600 })
    }).then(function(r) { return r.ok ? r.json() : null; })
      .then(function(j) {
        if (!j || !j.signedURL) return;
        img.src = j.signedURL.indexOf('http') === 0 ? j.signedURL
                                                    : SB + '/storage/v1' + j.signedURL;
      }).catch(function() {});
  }

  function clear() {
    list.innerHTML = '';
    list.hidden = true;
    if (empty) empty.hidden = true;
    if (window.atMineCounted) window.atMineCounted(0);
  }

  function load(token) {
    if (!token) { clear(); return; }
    fetch(SB + '/rest/v1/sightings?select=id,name,species,status,photo,taken_at&order=taken_at.desc', {
      headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + token } })
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(rows) {
        if (!rows) return;
        if (window.atMineCounted) window.atMineCounted(rows.length);
        if (!rows.length) { list.hidden = true; return; }
        list.innerHTML = rows.map(function(row) { return '<li>' + card(row) + '</li>'; }).join('');
        list.hidden = false;
        rows.forEach(function(row) {
          if (!row.photo) return;
          var el = list.querySelector('[data-id="' + row.id + '"] img');
          if (el) sign(token, row.photo, el);
        });
      })
      .catch(function() {});
  }

  // Named on the window so the page's own sign-in and sign-out can call them.
  // A fresh sign-in arrives in the url hash AFTER this file has run, and
  // without this the person who just signed in would be looking at the
  // signed-out line under a page that knows perfectly well who they are.
  //
  // And signing out takes the trees off the screen with it, which is what
  // Strava, AllTrails and Google Maps all do: the device shows the signed-out
  // app, and everything comes back on the next sign-in because it lives in the
  // account. See CONVENTIONS.md, "What signing out takes with it".
  window.atLoadMine = load;
  window.atClearMine = clear;

  var s = null;
  try { s = JSON.parse(localStorage.getItem('ancienttrees_session')); } catch (e) {}
  if (!s || !s.access_token || s.expires_at <= Date.now() / 1000) { clear(); return; }
  load(s.access_token);
})();
</script>
`;
