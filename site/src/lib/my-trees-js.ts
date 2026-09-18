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
//
// TWO KINDS OF SIGHTING, and until 2026-09-11 this file treated them as one.
// A photograph taken while ticking off a tree WE map carries that tree's id;
// one taken while adding a tree only you have carries none. Rendering both as
// cards of their own put Hidde's own photograph of the Sudajii at the Omiya
// gate in a second card below our card for the same tree, which showed no
// photograph at all, and counted that one tree twice. His question was the
// obvious one: "waarom zie ik hier niet de foto die ik heb gemaakt in de app
// bij m'n eigen boom."
//
// So a tree-linked photograph goes ON that tree's card, and the app, which
// hides these rows entirely (Sightings.yoursOnly filters treeId == nil), shows
// it on the tree's page for the same reason. Which photograph wins where both
// exist is the Google Maps convention: the place keeps its own picture and
// yours is yours (CONVENTIONS.md, "Your own photograph of a place somebody
// else maps"). So yours fills an empty slot, and where we publish one already,
// ours stays.
//
// A linked row whose tree we no longer map keeps a card of its own, because
// the alternative is a photograph that silently disappears.
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
  function sign(token, path, then) {
    fetch(SB + '/storage/v1/object/sign/sightings/' + path, {
      method: 'POST',
      headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + token,
                 'Content-Type': 'application/json' },
      body: JSON.stringify({ expiresIn: 3600 })
    }).then(function(r) { return r.ok ? r.json() : null; })
      .then(function(j) {
        if (!j || !j.signedURL) return;
        then(j.signedURL.indexOf('http') === 0 ? j.signedURL
                                               : SB + '/storage/v1' + j.signedURL);
      }).catch(function() {});
  }

  // YOUR PHOTOGRAPH ON OUR CARD. tree id -> signed url, painted onto whatever
  // cards are on the screen now and again whenever the profile redraws them,
  // because the two lists arrive from two requests and either can land first.
  var yours = {};

  function clear() {
    list.innerHTML = '';
    list.hidden = true;
    if (empty) empty.hidden = true;
    yours = {};
    paintYours();
    if (window.atMineCounted) window.atMineCounted(0);
    if (window.atAddMyPins) window.atAddMyPins([]);
  }

  function paintYours() {
    Object.keys(yours).forEach(function(id) {
      var url = yours[id];
      if (!url) return;
      var cards = document.querySelectorAll('[data-tree-id="' + id.replace(/[^A-Za-z0-9_-]/g, '') + '"]');
      Array.prototype.forEach.call(cards, function(art) {
        // Ours wins where we have one, which is the Google Maps reading: the
        // place keeps its own picture. An empty slot is where yours goes.
        if (art.querySelector('.tree-card-photo')) return;
        var box = document.createElement('div');
        box.className = 'tree-card-photo tree-card-yours-photo';
        var img = document.createElement('img');
        img.src = url;
        img.loading = 'lazy';
        var named = art.querySelector('.tree-name');
        img.alt = 'Your photograph of ' + ((named && named.textContent) || 'this tree');
        var tag = document.createElement('span');
        tag.className = 'tree-card-yours';
        tag.textContent = 'Your photograph';
        box.appendChild(img);
        box.appendChild(tag);
        art.insertBefore(box, art.firstChild);
      });
    });
  }

  function load(token) {
    if (!token) { clear(); return; }
    var cards = window.atCollection ? window.atCollection.catalogue()
                                    : Promise.resolve({});
    var rows = fetch(SB + '/rest/v1/sightings?select=id,tree_id,name,species,status,photo,lat,lng,shared,taken_at'
                     + '&order=taken_at.desc',
      { headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + token } })
      .then(function(r) { return r.ok ? r.json() : null; })
      .catch(function() { return null; });

    Promise.all([rows, cards]).then(function(r) {
      var all = r[0], known = r[1] || {};
      if (!all) return;
      // A row belongs to one of our trees only when we still map that tree.
      // One we have since retired keeps a card of its own rather than
      // vanishing with the page it pointed at.
      var linked = all.filter(function(row) { return row.tree_id && known[row.tree_id]; });
      var own = all.filter(function(row) { return linked.indexOf(row) === -1; });

      yours = {};
      linked.forEach(function(row) {
        if (!row.photo || yours[row.tree_id]) return;
        yours[row.tree_id] = '';
        sign(token, row.photo, function(url) {
          yours[row.tree_id] = url;
          paintYours();
        });
      });

      // The count is the app's count: trees you stood in front of plus trees
      // only you have. A tree you ticked off AND photographed is one tree, and
      // it was being counted twice here until 2026-09-11.
      if (window.atMineCounted) window.atMineCounted(own.length);
      // And your own trees go on the map beside them, which the app's Collect
      // map has always drawn and this one did not.
      if (window.atAddMyPins) {
        window.atAddMyPins(own.filter(function(row) {
          return typeof row.lat === 'number' && typeof row.lng === 'number';
        }).map(function(row) {
          return { type: 'Feature',
                   geometry: { type: 'Point', coordinates: [row.lng, row.lat] },
                   properties: { name: row.name || 'A tree you photographed',
                                 city: 'A tree only you have',
                                 // Its own unlisted page, when there is one.
                                 // A sighting somebody unshared has none, and
                                 // the popup leaves the link off rather than
                                 // pointing at a page that would 404.
                                 url: row.shared === false ? '' : '/t/' + row.id,
                                 got: 1 } };
        }));
      }

      if (!own.length) { list.innerHTML = ''; list.hidden = true; return; }
      list.innerHTML = own.map(function(row) { return '<li>' + card(row) + '</li>'; }).join('');
      list.hidden = false;
      own.forEach(function(row) {
        if (!row.photo) return;
        var el = list.querySelector('[data-id="' + row.id + '"] img');
        if (el) sign(token, row.photo, function(url) { el.src = url; });
      });
    });
  }

  // Called by profile-js every time it redraws a list, so a photograph landing
  // before the cards do still finds them.
  window.atPaintMine = paintYours;

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
