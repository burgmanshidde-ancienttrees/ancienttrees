// A READER'S PHOTOGRAPH OF A TREE WE MAP, sent from the website.
//
// Convention: CONVENTIONS.md, "Adding a photograph of a place, and saying you
// were there". Google Maps puts Add a photo ON THE PLACE, as a contribution
// offered beside checking in rather than as the same act, and counts the two
// separately. So this control sits on the tree's own page and does exactly one
// thing: it sends the photograph. On its own it does NOT tick the tree off,
// because the person may be at a laptop. Sent from the collect sheet
// (window.atAddPhoto(true), 2026-10-10) it does, because there the person has
// just said they are collecting it: the app's "Take a photograph" in the same
// sheet does the same.
//
// WHY THE WEBSITE NEEDED THIS AT ALL. The photo-less tree page has said "Send
// us yours and it goes on this page" since it was written, linking to
// /contribute, which has no file field of any kind. The site could set a
// profile picture and not take a photograph of a tree. It was found on
// 2026-09-23 by asking what the first contributor from outside could actually
// have sent us: two oaks in a park he lives near, four trees there with no
// picture between them, and no way to hand one over.
//
// IT WRITES THE SAME ROW THE APP WRITES, into sightings, so nothing downstream
// has to learn a second shape: sightings_inbox.py queues it on the next knock,
// a viewing pass looks at the pixels against the Cadiz standard, and
// sightings_publish.py puts it on the page with source contributor and the
// contributor id that carries the deletion promise. Nothing is published by
// the upload itself.
//
// THE COORDINATE IS OURS AND IS MARKED AS OURS. The row needs a lat and lng
// and a browser has no idea where the person is, so it carries the tree's own
// position. That is a trap worth naming: CLAUDE.md lets a reader's GPS fix
// upgrade a pin of ours that admits it is approximate, and a pin confirmed
// from a copy of itself would be exactly the circular evidence the bridge-claim
// rule exists to stop. The note says where the number came from, in words, on
// the row.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";

export const ADD_PHOTO_JS = `
<script>
(function() {
  var box = document.getElementById('addphoto');
  if (!box) return;
  var SB = "${SUPABASE_URL}", KEY = "${SUPABASE_KEY}";
  var btn = document.getElementById('addphoto-btn');
  var file = document.getElementById('addphoto-file');
  // The camera's own input (capture="environment"): the collect sheet's "Take
  // a photograph" opens the camera directly, "Choose from your photos" the
  // library, the way the app's two buttons do (2026-10-10).
  var cam = document.getElementById('addphoto-camera');
  var note = document.getElementById('addphoto-note');
  var treeId = box.getAttribute('data-tree-id');
  var treeName = box.getAttribute('data-tree-name') || '';
  var lat = parseFloat(box.getAttribute('data-lat'));
  var lng = parseFloat(box.getAttribute('data-lng'));
  var busy = false;
  // Looked up once, in this language, by AddPhoto.astro (same pattern as
  // WORTHIT_JS's data-thanks-detail): this script is shared by all seven
  // languages and must never hardcode a sentence, which is exactly how the
  // control shipped English-only on every translated tree page (REVIEW.md
  // 2026-09-23 WARN).
  var msgSignIn = box.getAttribute('data-msg-signin') || 'Sign in first, then choose your photograph.';
  var msgSending = box.getAttribute('data-msg-sending') || 'Sending...';
  var msgBadFile = box.getAttribute('data-msg-badfile') || 'That picture could not be read. Try another one.';
  var msgThanks = box.getAttribute('data-msg-thanks') || 'Thank you. We look at every photograph before it goes on a page, and you will hear what happened to yours.';
  var msgFailed = box.getAttribute('data-msg-failed') || 'That did not go through. Try again in a moment.';
  var msgOnPage = box.getAttribute('data-msg-onpage') || 'Your photo is on this page';
  var msgSeeMine = box.getAttribute('data-msg-seemine') || 'See it in My trees';
  // The button's own label, in whichever language rendered it (quiet or not),
  // read back from the DOM rather than guessed, so resetting it after a busy
  // or failed state never reverts to the English default on a translated page.
  var originalLabel = btn.textContent;

  function session() {
    // The one answer, verified with the server (collection-js), when it is on the page.
    if (window.atCollection && window.atCollection.session) return window.atCollection.session();
    try {
      var s = JSON.parse(localStorage.getItem('ancienttrees_session'));
      return (s && s.expires_at > Date.now() / 1000) ? s : null;
    } catch (e) { return null; }
  }

  // WHO, from the token itself (2026-10-12). The stored session holds the
  // tokens and nothing else (signin-js), so s.user.id was undefined on every
  // web upload: the file went to "undefined/...", the storage policy refused
  // it as somebody else's folder, and every photograph sent from the website
  // ended in "That did not go through". The JWT's sub claim is the user id.
  function userId(s) {
    if (s.user && s.user.id) return s.user.id;
    if (s.user_id) return s.user_id;
    try {
      var b = s.access_token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
      while (b.length % 4) b += '=';
      return JSON.parse(atob(b)).sub || null;
    } catch (e) { return null; }
  }

  function say(t) { note.textContent = t; note.hidden = !t; }

  // The acknowledgement plus the way to the list that now holds it: one line,
  // beside the control, never a dialog (CONVENTIONS.md, "Landing after you
  // have added something").
  function sayWithLink(t) {
    say(t + ' ');
    var a = document.createElement('a');
    a.href = '/account';
    a.textContent = msgSeeMine;
    note.appendChild(a);
  }

  // AND THE STATE, on every later visit. A photograph you sent of this tree
  // is written here while it waits and once it is on the page, which is what
  // the app's tree page says under your photographs. Your own rows only: the
  // policy on sightings is auth.uid() = user_id.
  // YOUR PHOTOGRAPHS OF THIS TREE (2026-10-12), the app's yourPhotos strip:
  // every photograph you sent of this tree, newest first, from your own rows
  // (the policy on sightings is auth.uid() = user_id), each through a signed
  // url that lasts an hour, the route My trees uses. And the one upgrade
  // worth announcing beside the button: yours went on the page.
  var yours = document.getElementById('td-yours');
  var LOCALE = document.documentElement.lang || 'en';
  function dayOf(iso) {
    try { return new Date(iso).toLocaleDateString(LOCALE, { day: 'numeric', month: 'short', year: 'numeric' }); }
    catch (e) { return ''; }
  }
  function paintYours(n) {
    if (!yours) return;
    yours.querySelector('.td-yours-h').textContent =
      n === 1 ? yours.getAttribute('data-one') : yours.getAttribute('data-many');
    yours.hidden = n === 0;
  }
  function addShot(url, iso, first) {
    if (!yours) return;
    var row = yours.querySelector('.td-yours-row');
    var fig = document.createElement('a');
    fig.className = 'td-yours-shot';
    fig.href = url; fig.target = '_blank'; fig.rel = 'noopener';
    var img = document.createElement('img');
    img.src = url; img.alt = ''; img.loading = 'lazy';
    var cap = document.createElement('span');
    cap.textContent = dayOf(iso);
    fig.appendChild(img); fig.appendChild(cap);
    if (first && row.firstChild) row.insertBefore(fig, row.firstChild); else row.appendChild(fig);
    paintYours(row.children.length);
  }
  function sign(token, path, then) {
    fetch(SB + '/storage/v1/object/sign/sightings/' + path, {
      method: 'POST',
      headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
      body: JSON.stringify({ expiresIn: 3600 })
    }).then(function(r) { return r.ok ? r.json() : null; })
      .then(function(j) {
        if (!j || !j.signedURL) { then(null); return; }
        then(j.signedURL.indexOf('http') === 0 ? j.signedURL : SB + '/storage/v1' + j.signedURL);
      }).catch(function() { then(null); });
  }
  (function state() {
    var s = session();
    if (!s || !treeId) return;
    fetch(SB + '/rest/v1/sightings?select=status,photo,taken_at&photo=not.is.null&tree_id=eq.'
          + encodeURIComponent(treeId) + '&order=taken_at.desc&limit=12',
      { headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + s.access_token } })
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(rows) {
        if (!rows || !rows.length) return;
        // Signed one by one but placed in order: each lands in its own slot.
        var slots = rows.map(function() { return null; });
        var done = 0;
        rows.forEach(function(row, i) {
          sign(s.access_token, row.photo, function(url) {
            slots[i] = url; done++;
            if (done === rows.length) {
              slots.forEach(function(u, k) { if (u) addShot(u, rows[k].taken_at, false); });
            }
          });
        });
        if (busy || !note.hidden) return;
        // Only the upgrade is announced (2026-10-08): no "Sent to us" while
        // it waits, nothing after a no. The app's Sighting.photoState.
        if (rows[0].status !== 'published') return;
        sayWithLink(msgOnPage);
      }).catch(function() {});
  })();

  // A uuid, because the sightings table is keyed on the id the CLIENT gives a
  // sighting, so the same one arriving twice is one row rather than two.
  function uuid() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0;
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
  }

  // THE COLLECT SHEET'S WAY IN (2026-10-10). The sheet opened behind the one
  // door already, so the picker is opened straight from this tap, inside the
  // gesture a browser insists on for a file picker. collect says the photograph
  // also collects the tree once it has gone through.
  var collecting = false;
  window.atAddPhoto = function(collect, mode) {
    if (busy) return;
    var input = (mode === 'camera' && cam) ? cam : file;
    if (session()) { collecting = Boolean(collect); input.click(); }
    else { btn.click(); collecting = Boolean(collect); }
  };

  btn.addEventListener('click', function() {
    if (busy) return;
    collecting = false;
    // The gate is the one the hearts and the worth-it control use: anybody may
    // see it, sending needs the account that lets us write back and that the
    // deletion promise hangs on.
    // The one door (atCollection.gate, 2026-10-05): the server says whether
    // there is an account, never the browser.
    var C = window.atCollection;
    var ask = function() {
      // The sign-in sheet is the whole answer; a sentence under the button
      // saying the same thing was clutter (Hidde, 2026-09-24). Only where the
      // sheet is missing does the page say it in words.
      if (window.atOpenSignIn) window.atOpenSignIn(null, 'feedback');
      else say(msgSignIn);
    };
    if (C && C.gate) C.gate(function() { file.click(); }, ask);
    else if (session()) file.click(); else ask();
  });

  function picked(from) {
    var f = from.files && from.files[0];
    if (!f || busy) return;
    var s = session();
    if (!s) { say(msgSignIn); return; }
    busy = true; btn.disabled = true; btn.textContent = msgSending;
    say('');
    if (collecting && window.atSnack) window.atSnack(msgSending, null, null, true);
    window.atDownsize(f, 1600, function(blob) {
      if (!blob) {
        busy = false; btn.disabled = false; btn.textContent = originalLabel;
        say(msgBadFile);
        if (collecting && window.atSnack) window.atSnack(msgBadFile);
        return;
      }
      var id = uuid();
      var uid = userId(s);
      if (!uid) { busy = false; btn.disabled = false; btn.textContent = originalLabel;
        say(msgSignIn); if (collecting && window.atSnack) window.atSnack(msgSignIn); collecting = false; return; }
      var path = encodeURIComponent(uid) + '/' + id + '.jpg';
      fetch(SB + '/storage/v1/object/sightings/' + path, {
        method: 'POST',
        headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + s.access_token,
                   'Content-Type': 'image/jpeg', 'x-upsert': 'true' },
        body: blob
      }).then(function(r) {
        // The FILE first and the row second, so a failed upload never leaves a
        // row pointing at nothing. The avatar upload does the same.
        if (!r.ok) throw new Error('upload');
        return fetch(SB + '/rest/v1/sightings', {
          method: 'POST',
          headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + s.access_token,
                     'Content-Type': 'application/json', 'Prefer': 'return=minimal' },
          body: JSON.stringify({
            id: id, tree_id: treeId, name: treeName,
            lat: lat, lng: lng, photo: uid + '/' + id + '.jpg',
            note: 'Photograph sent from this tree\\u2019s page on the website. '
                  + 'The position on this row is the tree\\u2019s own published '
                  + 'coordinate, not a device fix, and is not evidence about the pin.'
          })
        });
      }).then(function(r) {
        if (!r || !r.ok) throw new Error('row');
        try { addShot(URL.createObjectURL(blob), new Date().toISOString(), true); } catch (e) {}
        btn.hidden = true;
        file.value = ''; if (cam) cam.value = '';
        sayWithLink(msgThanks);
        if (collecting && window.atPushVisited) {
          if (!(window.atHasVisited && window.atHasVisited(treeId))) {
            window.atPushVisited(treeId, true);
            try { at.track('visit'); } catch (err) {}
          }
          if (window.atPaintSeen) window.atPaintSeen();
          var sb = document.querySelector('.seen-btn');
          if (window.atSnack) window.atSnack((sb && sb.getAttribute('data-l-done')) || 'Collected',
            msgSeeMine, '/account');
        }
        collecting = false;
        if (window.at) at.track('tree-photo-sent');
      }).catch(function() {
        busy = false; btn.disabled = false; btn.textContent = originalLabel;
        say(msgFailed);
        if (collecting && window.atSnack) window.atSnack(msgFailed);
        collecting = false;
      });
    });
  }
  file.addEventListener('change', function() { picked(file); });
  if (cam) cam.addEventListener('change', function() { picked(cam); });
})();
</script>
`;
