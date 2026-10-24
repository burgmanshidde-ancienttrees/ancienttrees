// NOTES FROM VISITORS on a tree page (2026-10-24; CONVENTIONS.md, "Notes from
// visitors on a tree page"). komoot's Tips and AllTrails' reviews in shape:
// one note per person per tree, dated, no replies, no likes, no stars; live
// for everyone the moment it is written (Hidde: "zet gewoon live en we kunnen
// altijd wegmodereren later"), the night run reads it afterwards
// (scripts/tree_notes.py). Table and function: supabase/tree-notes.sql.
//
// What this script does, in order:
//   1. Reads every note on this tree AND on the nearest trees of the same place
//      in one call (tree_notes_for, anon-readable; the name and picture only
//      from a public profile). The page lists this tree's notes; when there are
//      none it borrows the nearest other tree's note as the example (Airbnb's
//      "this host has N reviews", Hidde 2026-10-24: "look at airbnb"), and when
//      the place has none at all it keeps the grey empty card the page rendered.
//   2. Signed in, reads your own row (RLS: own rows only), so your note shows
//      as "Your note" even when your profile is private, and the sheet opens
//      prefilled to edit it.
//   3. The one button opens the sheet; the sheet upserts against
//      (user_id, tree_id), closes, and the list redraws at once.
//
// Every sentence comes from TreeDetail.astro as a data attribute (the same
// pattern as ADD_PHOTO_JS): this script serves eight languages and types none.
// If the table is not there yet (the SQL waits for Hidde's paste), the
// function 404s and the whole section hides rather than show a broken block.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";

export const TREE_NOTES_JS = `
<script>
(function() {
  var sec = document.getElementById('td-notes');
  if (!sec) return;
  var SB = "${SUPABASE_URL}", KEY = "${SUPABASE_KEY}";
  var treeId = sec.getAttribute('data-tree');
  var near = [];
  try { near = JSON.parse(sec.getAttribute('data-near') || '[]'); } catch (e) {}
  var body = sec.querySelector('.td-notes-body');
  var btnsBox = sec.querySelector('.td-notes-btns');
  // The one button lives where the next note will appear: inside the grey
  // empty card while there are none, under the list once there are (Hidde,
  // 2026-10-25). Taken out before the card is kept as the empty state, so
  // redrawing the card never makes a second, dead copy of it.
  if (askBtn && askBtn.parentNode) askBtn.parentNode.removeChild(askBtn);
  var ghost = body.innerHTML;
  function placeAsk() {
    if (!askBtn) return;
    // The app's words: "Edit your note" once you have one.
    var l = askBtn.querySelector('.td-note-ask-l');
    if (l) l.textContent = own ? T('edit-mine') : T('write');
    var act = body.querySelector('.td-notes-empty-act');
    (act || btnsBox || sec).appendChild(askBtn);
  }
  placeAsk();
  var T = function(k) { return sec.getAttribute('data-' + k) || ''; };
  var LOCALE = document.documentElement.lang || 'en';
  var dlg = document.getElementById('note-dlg');
  var field = document.getElementById('note-field');
  var who = document.getElementById('note-who');
  var sendBtn = document.getElementById('note-send');
  var delBtn = document.getElementById('note-del');
  var cancelBtn = document.getElementById('note-cancel');
  var status = document.getElementById('note-status');
  var askBtn = document.getElementById('td-note-ask');
  var own = null;      // {body, created_at} from your own row
  var rows = [];       // every public note on this tree and its neighbours
  var gone = false;    // the function is not there yet

  function session() {
    if (window.atCollection && window.atCollection.session) return window.atCollection.session();
    try {
      var s = JSON.parse(localStorage.getItem('ancienttrees_session'));
      return (s && s.expires_at > Date.now() / 1000) ? s : null;
    } catch (e) { return null; }
  }
  function headers(s, json) {
    var h = { 'apikey': KEY, 'Authorization': 'Bearer ' + (s ? s.access_token : KEY) };
    if (json) h['Content-Type'] = 'application/json';
    return h;
  }
  function dayOf(iso) {
    try { return new Date(iso).toLocaleDateString(LOCALE, { day: 'numeric', month: 'short', year: 'numeric' }); }
    catch (e) { return ''; }
  }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  // The face beside a note: the picture, else the initial, else the leaf for
  // "A visitor" (the bar's round profile picture, 28px; CONVENTIONS 2026-10-20).
  function face(r, mine) {
    var av = el('span', 'td-avatar');
    var name = mine ? null : r.author_name;
    if (r.author_avatar) {
      av.style.backgroundImage = 'url(' + String(r.author_avatar).replace(/[()'"]/g, '') + ')';
    } else if (name) {
      av.textContent = name.trim().charAt(0).toUpperCase();
    } else if (mine && window.atWho && window.atWho.avatar) {
      av.style.backgroundImage = 'url(' + String(window.atWho.avatar).replace(/[()'"]/g, '') + ')';
    } else if (mine && window.atWho && window.atWho.name) {
      av.textContent = window.atWho.name.trim().charAt(0).toUpperCase();
    } else {
      av.className += ' td-avatar-anon';
      av.setAttribute('aria-hidden', 'true');
      av.innerHTML = T('leaf-icon');
    }
    return av;
  }
  function card(r, mine, faded) {
    var li = el('div', 'td-note' + (mine ? ' td-note-mine' : '') + (faded ? ' td-note-borrowed' : ''));
    var meta = el('div', 'td-note-meta');
    var w = el('span', 'td-note-who');
    w.appendChild(face(r, mine));
    w.appendChild(el('b', null, mine ? T('yours') : (r.author_name || T('visitor'))));
    meta.appendChild(w);
    meta.appendChild(el('span', null, dayOf(r.created_at)));
    li.appendChild(meta);
    li.appendChild(el('p', null, r.body));
    return li;
  }
  function sameNote(a, b) {
    return a && b && Math.abs(Date.parse(a.created_at) - Date.parse(b.created_at)) < 2000;
  }
  function render() {
    if (gone) { sec.hidden = true; return; }
    var here = rows.filter(function(r) { return r.tree_id === treeId; });
    var list = [];
    if (own) {
      list.push(card(own, true));
      here = here.filter(function(r) { return !sameNote(r, own); });
    }
    here.forEach(function(r) { list.push(card(r, false)); });
    body.innerHTML = '';
    if (list.length) {
      var ul = el('div', 'td-notes-list');
      list.forEach(function(c) { ul.appendChild(c); });
      body.appendChild(ul);
      placeAsk();
      return;
    }
    // Nobody here yet: the nearest neighbour's note, the real thing, faded,
    // with the line that says whose tree it is, inside the same grey card;
    // else the card as the page rendered it.
    var borrowed = null, from = null;
    for (var i = 0; i < near.length && !borrowed; i++) {
      for (var j = 0; j < rows.length; j++) {
        if (rows[j].tree_id === near[i].id) { borrowed = rows[j]; from = near[i]; break; }
      }
    }
    body.innerHTML = ghost;
    if (borrowed) {
      var box = body.querySelector('.td-notes-empty');
      var ask = box && box.querySelector('.td-notes-empty-s');
      var p = el('p', 'td-notes-none');
      var parts = T('borrowed').split('{tree}');
      p.appendChild(document.createTextNode(parts[0]));
      var a = el('a', null, from.name); a.href = from.url;
      p.appendChild(a);
      p.appendChild(document.createTextNode(parts[1] || ''));
      if (ask) { ask.parentNode.insertBefore(p, ask); ask.parentNode.insertBefore(card(borrowed, false, true), ask); ask.remove(); }
    }
    placeAsk();
  }

  function load() {
    var s = session();
    var ids = [treeId].concat(near.map(function(n) { return n.id; }));
    var all = fetch(SB + '/rest/v1/rpc/tree_notes_for', { method: 'POST', headers: headers(null, true), body: JSON.stringify({ ids: ids }) })
      .then(function(r) {
        if (r.status === 404) { gone = true; return []; }
        return r.ok ? r.json() : [];
      }).catch(function() { return []; });
    var mine = !s ? Promise.resolve(null)
      : fetch(SB + '/rest/v1/tree_notes?select=body,created_at,updated_at&tree_id=eq.' + encodeURIComponent(treeId), { headers: headers(s) })
        .then(function(r) { return r.ok ? r.json() : []; })
        .then(function(a) { return (a && a[0]) || null; })
        .catch(function() { return null; });
    Promise.all([all, mine]).then(function(res) {
      rows = res[0] || [];
      own = res[1];
      render();
    });
  }

  // THE SHEET. Signed out, the gate opens sign-in and nothing else (hard rule
  // 11: the server decides who is signed in).
  function say(t) { if (status) { status.textContent = t; status.hidden = !t; } }
  function open() {
    var go = function(s) {
      field.value = own ? own.body : '';
      sendBtn.textContent = own ? T('save') : T('add');
      if (delBtn) delBtn.hidden = !own;
      say('');
      // Shown as: the display name only when the profile is public, else
      // "A visitor". Read from the profile the gate has already verified.
      who.textContent = T('shown-anon');
      fetch(SB + '/rest/v1/profiles?select=display_name,avatar_url,public&limit=1', { headers: headers(s) })
        .then(function(r) { return r.ok ? r.json() : []; })
        .then(function(a) {
          var p = a && a[0];
          if (!p) return;
          window.atWho = { name: p.display_name, avatar: p.avatar_url, isPublic: !!p.public };
          if (p.public && p.display_name) who.textContent = T('shown-as').replace('{name}', p.display_name);
        }).catch(function() {});
      if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
      setTimeout(function() { try { field.focus(); } catch (e) {} }, 50);
    };
    var out = function() {
      if (window.atOpenSignIn) { try { window.atOpenSignIn(); return; } catch (e) {} }
      if (window.atSnack) window.atSnack(T('signin'));
    };
    // The server decides who is signed in (hard rule 11): one door for
    // every gated tap, never the browser's stored session on its own.
    if (window.atCollection && window.atCollection.gate) window.atCollection.gate(go, out);
    else out();
  }
  function send() {
    var text = (field.value || '').trim();
    if (!text) { field.focus(); return; }
    var s = session();
    if (!s) { say(T('signin')); return; }
    sendBtn.disabled = true; say(T('saving'));
    var nowIso = new Date().toISOString();
    var h = headers(s, true);
    h['Prefer'] = 'resolution=merge-duplicates,return=representation';
    fetch(SB + '/rest/v1/tree_notes?on_conflict=user_id,tree_id', { method: 'POST', headers: h,
      body: JSON.stringify({ tree_id: treeId, body: text, updated_at: nowIso }) })
      .then(function(r) { if (!r.ok) throw new Error('note'); return r.json(); })
      .then(function(a) {
        var row = (a && a[0]) || {};
        own = { body: text, created_at: row.created_at || (own && own.created_at) || nowIso };
        sendBtn.disabled = false;
        dlg.close();
        render();
        try { sec.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); } catch (e) {}
      })
      .catch(function() { sendBtn.disabled = false; say(T('failed')); });
  }
  function remove() {
    var s = session();
    if (!s || !own) return;
    delBtn.disabled = true;
    fetch(SB + '/rest/v1/tree_notes?tree_id=eq.' + encodeURIComponent(treeId), { method: 'DELETE', headers: headers(s) })
      .then(function(r) { if (!r.ok) throw new Error('del'); own = null; delBtn.disabled = false; dlg.close(); load(); })
      .catch(function() { delBtn.disabled = false; say(T('failed')); });
  }
  if (askBtn) askBtn.addEventListener('click', open);
  if (sendBtn) sendBtn.addEventListener('click', send);
  if (delBtn) delBtn.addEventListener('click', remove);
  if (cancelBtn) cancelBtn.addEventListener('click', function() { dlg.close(); });
  load();
})();
</script>
`;
