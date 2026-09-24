// The trees somebody added themselves, on the website, through EITHER channel.
//
// Two of them exist and this file read one of them until 2026-09-23. The app's
// camera writes to sightings; the website's form writes to submissions, which
// is a postbox nothing on this page had ever opened. The first contributor who
// was not Hidde found that gap by walking into it: one oak in Hessen, sent
// fourteen times across three evenings, ten of those arrivals coming from
// /account, because the thank-you mail says "you can see the trees you added
// on your account" and the account said nothing was there.
//
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
  var sentList = document.getElementById('sent-list');
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

  // What a tree nobody named is called: its species when we know it, the same
  // rule the app applies (Sightings.fallbackName), and the old line only when
  // we know nothing. The species arrives as "Oak (Quercus sp.)" and a heading
  // wants the common half.
  function titleOf(row) {
    if (row.name) return row.name;
    var sp = String(row.species || '').split('(')[0].trim();
    return sp || 'A tree you photographed';
  }

  function card(row) {
    var meta = [row.species, when(row.taken_at)].filter(Boolean).join(' \\u00b7 ');
    var label = LABEL[row.status] || LABEL.mine;
    return '<article class="tree-card tree-card-nonum mine-card" data-id="' + esc(row.id) + '">'
      + '<div class="tree-card-photo mine-photo"' + (row.photo ? '' : ' hidden') + '>'
        + '<img alt="' + esc(titleOf(row)) + '" loading="lazy"></div>'
      + '<div class="tree-card-top"><h3 class="tree-name">' + esc(titleOf(row)) + '</h3></div>'
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
  // tree id -> the words for where your photograph of it stands. The app's
  // Sighting.photoState, word for word, so one photograph reads the same on
  // both surfaces.
  var yourState = {};
  function photoState(status) {
    if (status === 'published') return "Your photo is on the tree's page";
    if (status === 'declined') return '';
    return 'Your photo, waiting for a look';
  }

  function clear() {
    clearSent();
    list.innerHTML = '';
    list.hidden = true;
    if (empty) empty.hidden = true;
    yours = {};
    yourState = {};
    paintYours();
    if (window.atMineCounted) window.atMineCounted(0);
    if (window.atPhotographedCounted) window.atPhotographedCounted(0);
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
    // The state goes on every card of that tree, ours-photographed or not,
    // once, and stays there while it is true (CONVENTIONS.md, "Landing after
    // you have added something").
    Object.keys(yourState).forEach(function(id) {
      var words = yourState[id];
      if (!words) return;
      var cards = document.querySelectorAll('[data-tree-id="' + id.replace(/[^A-Za-z0-9_-]/g, '') + '"]');
      Array.prototype.forEach.call(cards, function(art) {
        if (art.querySelector('.mine-state')) return;
        var p = document.createElement('p');
        p.className = 'mine-state';
        var dot = document.createElement('span');
        dot.className = 'mine-dot';
        p.appendChild(dot);
        p.appendChild(document.createTextNode(words));
        var more = art.querySelector('.tree-more');
        if (more) art.insertBefore(p, more); else art.appendChild(p);
      });
    });
  }

  // WHAT YOU SENT US THROUGH THE FORM. A row in submissions rather than in
  // sightings, so nothing on this page had ever read it: the form is a postbox
  // on the website and the account page only knew about the app's camera.
  //
  // Read with the person's own session and RLS does the rest: the policy on
  // submissions is "auth.uid() = user_id" (supabase/own-data.sql) and there is
  // none for anybody else, so this returns your rows and nobody else's.
  //
  // ONE CARD PER TREE, not per row. Somebody correcting their own tip has no
  // way to edit it, so refining means sending it again, and fourteen rows for
  // one oak would read as fourteen trees. The count goes on the card instead,
  // because it is the honest thing to say and it is what tells somebody the
  // earlier ones did arrive.
  var SENT_STATE = { changed: 'published', open_question: 'checking',
                     holds: 'checking' };

  function sentCard(g) {
    var r = g.newest;
    // A city tip has no tree name, so the city becomes the heading and must
    // not then be repeated as its own subtitle.
    // Unnamed, it is named from where it stands, "A tree in Utrecht", the
    // same rule the app applies to a tree nobody named (2026-09-24).
    var title = r.tree || (r.city ? 'A tree in ' + r.city : 'A tree you told us about');
    var bits = [r.tree ? r.city : '', when(r.created_at)];
    if (g.count > 1) bits.push('sent ' + g.count + ' times');
    var meta = bits.filter(Boolean).join(' \\u00b7 ');
    var label = LABEL[SENT_STATE[r.outcome] || 'sent'];
    return '<article class="tree-card tree-card-nonum mine-card">'
      + '<div class="tree-card-top"><h3 class="tree-name">' + esc(title) + '</h3></div>'
      + (meta ? '<p class="tree-meta">' + esc(meta) + '</p>' : '')
      + '<p class="mine-state"><span class="mine-dot"></span>' + esc(label) + '</p>'
      // The answer we wrote back, where there is one. A label says which of
      // four states it is in; this says what actually happened to the tree,
      // and it is already on the row the person is allowed to read.
      // The split argument is written with a DOUBLED backslash. This whole
      // file is one TypeScript template literal, so a single one is consumed
      // here and the page receives a real newline inside a string literal,
      // which is a syntax error, and a browser drops the entire script tag on
      // one. check_inline_scripts_parse was written for that on 2026-09-18.
      // This comment carries no escape sequence of its own on purpose: the
      // first version of it explained the trap using the broken spelling and
      // fell into it, which the same check caught.
      + (r.reply_text ? '<p class="mine-reply">' + esc(r.reply_text.split('\\n')[0]) + '</p>' : '')
      + '</article>';
  }

  function clearSent() {
    if (sentList) { sentList.innerHTML = ''; sentList.hidden = true; }
    if (window.atSentCounted) window.atSentCounted(0);
  }

  function loadSent(token) {
    if (!sentList) return;
    if (!token) { clearSent(); return; }
    // NOT the rows the app's own camera writes beside a sighting. Adding a
    // tree in the app posts a submissions row carrying that sighting's uuid
    // (CollectSheet.swift, from: "app:collect"), so counting it here
    // would put every photographed tree on this lane twice, which is the
    // exact duplication the 2026-09-11 fix took out. "page" starting with
    // app is the same discriminator contributor_reply.py uses.
    fetch(SB + '/rest/v1/submissions'
          + '?select=id,kind,city,tree,outcome,reply_text,created_at,page'
          + '&kind=in.(tree,city)&order=created_at.desc',
      { headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + token } })
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(rows) {
        if (!rows) return;
        var order = [], byKey = {};
        rows.forEach(function(r) {
          if ((r.page || '').indexOf('app') === 0) return;
          var key = ((r.tree || '') + '|' + (r.city || ''))
            .toLowerCase().replace(/[^a-z0-9|]/g, '');
          if (!byKey[key]) { byKey[key] = { newest: r, count: 0 }; order.push(key); }
          byKey[key].count += 1;
          // The newest row carries the best version of what they typed, and
          // the only outcome we ever set is on one of them, so an answered
          // tip keeps its answer whichever row we answered.
          if (r.outcome && !byKey[key].newest.outcome) byKey[key].newest = r;
        });
        var groups = order.map(function(k) { return byKey[k]; });
        if (window.atSentCounted) window.atSentCounted(groups.length);
        if (!groups.length) { sentList.innerHTML = ''; sentList.hidden = true; return; }
        sentList.innerHTML = groups.map(function(g) {
          return '<li>' + sentCard(g) + '</li>';
        }).join('');
        sentList.hidden = false;
      })
      .catch(function() {});
  }

  function load(token) {
    if (!token) { clear(); return; }
    loadSent(token);
    var cards = window.atCollection ? window.atCollection.catalogue()
                                    : Promise.resolve({});
    var rows = fetch(SB + '/rest/v1/sightings?select=id,tree_id,name,species,status,photo,lat,lng,shared,taken_at'
                     + '&order=taken_at.desc',
      { headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + token } })
      .then(function(r) { return r.ok ? r.json() : null; })
      .catch(function() { return null; });
    var ticked = window.atCollection ? window.atCollection.visited()
                                     : Promise.resolve([]);

    Promise.all([rows, cards, ticked]).then(function(r) {
      var all = r[0], known = r[1] || {}, visitedIds = r[2] || [];
      if (!all) return;
      // A row belongs to one of our trees only when we still map that tree.
      // One we have since retired keeps a card of its own rather than
      // vanishing with the page it pointed at.
      var linked = all.filter(function(row) { return row.tree_id && known[row.tree_id]; });
      var own = all.filter(function(row) { return linked.indexOf(row) === -1; });

      yours = {};
      yourState = {};
      linked.forEach(function(row) {
        if (!row.photo || yours[row.tree_id] !== undefined) return;
        yours[row.tree_id] = '';
        yourState[row.tree_id] = photoState(row.status);
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
                   properties: { name: titleOf(row),
                                 city: 'A tree only you have',
                                 // Its own unlisted page, when there is one.
                                 // A sighting somebody unshared has none, and
                                 // the popup leaves the link off rather than
                                 // pointing at a page that would 404.
                                 url: row.shared === false ? '' : '/t/' + row.id,
                                 got: 1 } };
        }));
      }

      // A photograph of one of our trees that you never ticked off, which is
      // what the tree page's Add a photo sends, has no card in the visited
      // list to land on. It gets our card for that tree here instead, so the
      // photograph you just sent is in My trees rather than nowhere.
      var isTicked = {};
      visitedIds.forEach(function(id) { isTicked[id] = true; });
      var photographed = [];
      linked.forEach(function(row) {
        if (!row.photo || isTicked[row.tree_id] || photographed.indexOf(row.tree_id) !== -1) return;
        photographed.push(row.tree_id);
      });
      var ours = photographed.map(function(id) {
        return '<li>' + window.atCollection.card(id, known[id], false, false) + '</li>';
      });

      if (window.atPhotographedCounted) window.atPhotographedCounted(ours.length);
      if (!own.length && !ours.length) { list.innerHTML = ''; list.hidden = true; return; }
      list.innerHTML = ours.join('')
        + own.map(function(row) { return '<li>' + card(row) + '</li>'; }).join('');
      list.hidden = false;
      paintYours();
      if (window.atPaintSaves) window.atPaintSaves();
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
