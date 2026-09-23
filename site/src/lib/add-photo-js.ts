// A READER'S PHOTOGRAPH OF A TREE WE MAP, sent from the website.
//
// Convention: CONVENTIONS.md, "Adding a photograph of a place, and saying you
// were there". Google Maps puts Add a photo ON THE PLACE, as a contribution
// offered beside checking in rather than as the same act, and counts the two
// separately. So this control sits on the tree's own page and does exactly one
// thing: it sends the photograph. It does NOT tick the tree off, because the
// person may be at a laptop, and the app's own rule already refuses to decide
// "they stood there" from "they have a picture".
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
  var note = document.getElementById('addphoto-note');
  var treeId = box.getAttribute('data-tree-id');
  var treeName = box.getAttribute('data-tree-name') || '';
  var lat = parseFloat(box.getAttribute('data-lat'));
  var lng = parseFloat(box.getAttribute('data-lng'));
  var busy = false;

  function session() {
    try {
      var s = JSON.parse(localStorage.getItem('ancienttrees_session'));
      return (s && s.expires_at > Date.now() / 1000) ? s : null;
    } catch (e) { return null; }
  }

  function say(t) { note.textContent = t; note.hidden = !t; }

  // A uuid, because the sightings table is keyed on the id the CLIENT gives a
  // sighting, so the same one arriving twice is one row rather than two.
  function uuid() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0;
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
  }

  btn.addEventListener('click', function() {
    if (busy) return;
    // The gate is the one the hearts and the worth-it control use: anybody may
    // see it, sending needs the account that lets us write back and that the
    // deletion promise hangs on.
    if (!session()) {
      if (window.atOpenSignIn) window.atOpenSignIn(null, 'feedback');
      say('Sign in first, then choose your photograph.');
      return;
    }
    file.click();
  });

  file.addEventListener('change', function() {
    var f = file.files && file.files[0];
    if (!f || busy) return;
    var s = session();
    if (!s) { say('Sign in first, then choose your photograph.'); return; }
    busy = true; btn.disabled = true; btn.textContent = 'Sending...';
    say('');
    window.atDownsize(f, 1600, function(blob) {
      if (!blob) {
        busy = false; btn.disabled = false; btn.textContent = 'Add a photo';
        say('That picture could not be read. Try another one.');
        return;
      }
      var id = uuid();
      var uid = s.user && s.user.id ? s.user.id : s.user_id;
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
        btn.hidden = true;
        file.value = '';
        say('Thank you. We look at every photograph before it goes on a page, '
            + 'and you will hear what happened to yours.');
        if (window.at) at.track('tree-photo-sent');
      }).catch(function() {
        busy = false; btn.disabled = false; btn.textContent = 'Add a photo';
        say('That did not go through. Try again in a moment.');
      });
    });
  });
})();
</script>
`;
