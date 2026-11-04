// FIND PEOPLE ON THE WEBSITE (2026-10-28), the app's PeopleView (Screens/
// People.swift) in the one sheet. Hidde asked how somebody finds a profile or
// a friend on the web; the answer was that they could not. Benchmarked in
// CONVENTIONS.md ("Finding somebody on the web, and sharing your own
// profile"): Strava and Polarsteps share a profile link from your own
// profile, AllTrails searches members by name. Shown to Hidde as a page and
// built on his yes.
//
// Three ways in, one sheet (#people-sheet on /account):
//   the round person-plus button   -> search, plus Share your profile
//   the followers count            -> who follows you, Follow back
//   the following count            -> who you follow
//
// Same rules as the app: search by the name somebody chose and nothing else
// (no browsing everybody), never yourself, blocked people at the end with no
// Follow, the same three labels on the pill. Every write goes through the one
// gate and the reader's own session; nothing is kept in the browser.
//
// SUGGESTED (2026-11-04, Hidde: "i like all your proposals please build"),
// the app's Kit/SuggestedPeople.swift: under the empty field, ambassadors with
// a public profile (the places you saved or collected first), then public
// profiles who photographed trees there (rpc suggested_photographers,
// supabase/suggested-people.sql; without it, the ambassadors alone). Never
// you, never somebody you blocked, never somebody you follow. Gone the
// moment you type; loaded again every time the sheet opens.
//
// SHARE YOUR PROFILE shares /profile?u=<id>. A phone gets the browser's own
// share sheet (Web Share), as the app gets iOS's; a computer copies the link
// and says so in the snackbar. A private profile asks first, with the words
// the settings page already uses.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";
import { icon } from "./icons";

// The seal the city page's ambassador row wears (AmbassadorLine.astro).
const SEAL = icon("seal-check", "fill", "ic").replace(/'/g, '"');

export const PEOPLE_JS = `
<script>
(function() {
  var SB = '${SUPABASE_URL}', KEY = '${SUPABASE_KEY}';
  var C = window.atCollection;
  var dlg = document.getElementById('people-sheet');
  if (!dlg || !C) return;
  function el(id) { return document.getElementById(id); }
  function esc(t) { return String(t == null ? '' : t).replace(/[&<>"]/g, function(c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  var me = null, token = null, mode = 'search';
  var following = {}, blocked = {}, isPublic = false, hasName = false;

  function api(method, path, body) {
    var h = { 'apikey': KEY, 'Authorization': 'Bearer ' + token };
    if (body) { h['Content-Type'] = 'application/json'; h['Prefer'] = 'return=minimal'; }
    return fetch(SB + path, { method: method, headers: h, body: body ? JSON.stringify(body) : undefined });
  }
  function rows(path) {
    return api('GET', path).then(function(r) { return r.ok ? r.json() : []; }).catch(function() { return []; });
  }
  // Who you are and what you follow, asked again on every open: a follow
  // made on the phone a minute ago is on this list too (hard rule 11).
  function load(s) {
    token = s.access_token;
    var who = me ? Promise.resolve(me)
      : fetch(SB + '/auth/v1/user', { headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + token } })
          .then(function(r) { return r.ok ? r.json() : null; })
          .then(function(u) { me = u && u.id; return me; });
    return who.then(function(id) {
      if (!id) return;
      return Promise.all([
        rows('/rest/v1/follows?select=followee&follower=eq.' + id + '&limit=200'),
        rows('/rest/v1/blocks?select=blocked&blocker=eq.' + id),
        rows('/rest/v1/profiles?select=public,display_name&user_id=eq.' + id)
      ]).then(function(r) {
        following = {}; blocked = {};
        r[0].forEach(function(x) { following[x.followee] = true; });
        r[1].forEach(function(x) { blocked[x.blocked] = true; });
        isPublic = Boolean(r[2][0] && r[2][0].public);
        hasName = Boolean(r[2][0] && r[2][0].display_name);
      });
    });
  }

  // SUGGESTED. The same order as SuggestedPeople.build in the app.
  var DATA = {};
  try { DATA = JSON.parse((el('people-data') || {}).textContent || '{}'); } catch (e) {}
  var sug = [], pinsCity = null;
  function treeCities() {
    if (pinsCity) return Promise.resolve(pinsCity);
    return fetch('/api/pins.json').then(function(r) { return r.ok ? r.json() : []; }).catch(function() { return []; })
      .then(function(rows) {
        pinsCity = {};
        rows.forEach(function(r) { pinsCity[r[0]] = r[3]; });
        return pinsCity;
      });
  }
  function reasonShot(n, place) {
    var box = el('people-sug');
    var t = n === 1 ? box.getAttribute('data-one') : box.getAttribute('data-photographed').replace('9999', String(n));
    return t.replace('%place%', place);
  }
  function loadSuggestions() {
    sug = [];
    Promise.all([
      rows('/rest/v1/saves?select=tree_id&user_id=eq.' + me),
      rows('/rest/v1/visited?select=tree_id&user_id=eq.' + me),
      treeCities()
    ]).then(function(r) {
      var city = r[2], count = {};
      r[0].concat(r[1]).forEach(function(x) { var c = city[x.tree_id]; if (c) count[c] = (count[c] || 0) + 1; });
      var places = Object.keys(count).sort(function(a, b) { return count[b] - count[a] || (a < b ? -1 : 1); });
      var rank = {};
      places.forEach(function(p, i) { rank[p] = i; });
      var want = {};
      places.slice(0, 6).forEach(function(p) {
        want[p] = Object.keys(city).filter(function(id) { return city[id] === p; });
      });
      var shots = places.length
        ? fetch(SB + '/rest/v1/rpc/suggested_photographers', { method: 'POST',
            headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
            body: JSON.stringify({ places: want }) })
            .then(function(x) { return x.ok ? x.json() : []; }).catch(function() { return []; })
        : Promise.resolve([]);
      return shots.then(function(ph) {
        var amb = (DATA.ambassadors || []);
        var mine = amb.filter(function(a) { return rank[a.slug] != null; })
          .sort(function(a, b) { return rank[a.slug] - rank[b.slug]; });
        var others = amb.filter(function(a) { return rank[a.slug] == null; });
        function row(a) { return { user_id: a.id, display_name: a.name, reason: a.role, seal: true }; }
        ph = (Array.isArray(ph) ? ph : []).sort(function(a, b) {
          var l = rank[a.place] == null ? 1e9 : rank[a.place], q = rank[b.place] == null ? 1e9 : rank[b.place];
          return l - q || b.trees - a.trees;
        }).map(function(x) {
          return { user_id: x.user_id, display_name: x.display_name, avatar_url: x.avatar_url,
                   reason: reasonShot(x.trees, (DATA.places || {})[x.place] || x.place), seal: false };
        });
        var seen = {}, out = [];
        mine.map(row).concat(ph, others.map(row)).forEach(function(p) {
          if (p.user_id === me || blocked[p.user_id] || !p.display_name || seen[p.user_id]) return;
          seen[p.user_id] = true; out.push(p);
        });
        // Somebody you follow leaves the list (Instagram; Hidde, 2026-11-04);
        // a Follow tapped here keeps its row until the sheet opens again.
        out = out.filter(function(p) { return !following[p.user_id]; }).slice(0, 12);
        if (!out.length) return;
        // The name and picture as their owner set them today.
        return rows('/rest/v1/profiles?select=user_id,display_name,avatar_url&user_id=in.('
                    + out.map(function(p) { return p.user_id; }).join(',') + ')').then(function(ps) {
          var byId = {};
          ps.forEach(function(p) { byId[p.user_id] = p; });
          out.forEach(function(p) {
            var f = byId[p.user_id];
            if (!f) return;
            if (f.display_name) p.display_name = f.display_name;
            p.avatar_url = f.avatar_url;
          });
          sug = out;
          paintSuggestions();
        });
      });
    });
  }
  function paintSuggestions() {
    var box = el('people-sug');
    var show = mode === 'search' && !el('people-q').value.trim() && sug.length > 0;
    box.hidden = !show;
    // The results list keeps its height for typing; not under suggestions.
    el('people-list').hidden = show;
    if (!show) return;
    el('people-sug-list').innerHTML = sug.map(rowHtml).join('');
  }

  function step(name) {
    dlg.querySelectorAll('.people-step').forEach(function(d) { d.hidden = d.getAttribute('data-step') !== name; });
  }
  function open(m) {
    mode = m;
    C.gate(function(s) {
      load(s).then(function() {
        step('list');
        el('people-h').textContent = el('people-h').getAttribute('data-' + m);
        var search = m === 'search';
        el('people-search').hidden = !search;
        el('people-share').hidden = !search;
        el('people-q').value = '';
        paint([]);
        if (!dlg.open) dlg.showModal();
        el('people-sug').hidden = true; el('people-list').hidden = false;
        if (search) { empty(); loadSuggestions(); setTimeout(function() { el('people-q').focus(); }, 50); }
        else list(m);
      });
    }, function() { if (window.atOpenSignIn) window.atOpenSignIn(); });
  }

  // The app's empty lines, word for word (People.swift emptyLine).
  // An empty search says nothing: the field's placeholder already does.
  function empty(text) {
    var e = el('people-empty');
    var typed = el('people-q').value.trim();
    if (!text && mode === 'search' && !typed) { e.hidden = true; return; }
    e.textContent = text || e.getAttribute('data-' + (mode === 'search' ? 'none' : mode));
    e.hidden = false;
  }

  function list(m) {
    var path = m === 'followers'
      ? '/rest/v1/follows?select=follower&followee=eq.' + me + '&limit=200'
      : '/rest/v1/follows?select=followee&follower=eq.' + me + '&limit=200';
    rows(path).then(function(r) {
      var ids = r.map(function(x) { return x.follower || x.followee; });
      if (!ids.length) { empty(); return; }
      rows('/rest/v1/profiles?select=user_id,display_name,avatar_url&user_id=in.(' + ids.join(',') + ')')
        .then(function(ps) {
          var byId = {};
          ps.forEach(function(p) { byId[p.user_id] = p; });
          // Somebody who follows you before choosing a name is still there.
          paint(ids.map(function(id) { return byId[id] || { user_id: id, display_name: '' }; }));
        });
    });
  }

  var timer = null;
  el('people-q').addEventListener('input', function() {
    clearTimeout(timer);
    var q = this.value.trim();
    paintSuggestions();
    timer = setTimeout(function() {
      if (q.length < 2) { paint([]); empty(); return; }
      rows('/rest/v1/profiles?select=user_id,display_name,avatar_url&display_name=ilike.*'
           + encodeURIComponent(q) + '*&limit=25')
        .then(function(ps) {
          if (el('people-q').value.trim() !== q) return;
          if (!ps.length) { paint([]); empty(); return; }
          paint(ps);
        });
    }, 250);
  });

  function label(id) {
    if (following[id]) return el('people-list').getAttribute('data-following');
    return el('people-list').getAttribute(mode === 'followers' ? 'data-back' : 'data-follow');
  }
  function paint(ps) {
    var others = ps.filter(function(p) { return p.user_id !== me; });
    // Blocked people last, dimmed, with no Follow (People.swift visible).
    others = others.filter(function(p) { return !blocked[p.user_id]; })
      .concat(others.filter(function(p) { return blocked[p.user_id]; }));
    el('people-empty').hidden = others.length > 0;
    el('people-list').innerHTML = others.map(rowHtml).join('');
  }
  // One row for search, the two lists and Suggested (People.swift personRow).
  function rowHtml(p) {
    var noName = el('people-list').getAttribute('data-noname');
    var name = p.display_name || '';
    var seal = p.seal ? '<span class="people-seal" aria-hidden="true">${SEAL}</span>' : '';
    var av = p.avatar_url
      ? '<span class="people-av" style="background-image:url(' + esc(String(p.avatar_url).replace(/[()'"]/g, '')) + ')">' + seal + '</span>'
      : '<span class="people-av">' + esc(name.charAt(0).toUpperCase()) + seal + '</span>';
    var pill = blocked[p.user_id] ? ''
      : '<button type="button" class="people-pill' + (following[p.user_id] ? ' on' : '') + '" data-id="' + esc(p.user_id) + '" aria-pressed="' + (following[p.user_id] ? 'true' : 'false') + '">' + esc(label(p.user_id)) + '</button>';
    var text = p.reason
      ? '<span class="people-text"><span class="people-name">' + esc(name) + '</span><span class="people-reason">' + esc(p.reason) + '</span></span>'
      : '<span class="people-name' + (name ? '' : ' none') + '">' + esc(name || noName) + '</span>';
    return '<li class="' + (blocked[p.user_id] ? 'is-blocked' : '') + '"><a class="people-who" href="/profile?u=' + encodeURIComponent(p.user_id) + '">' + av
      + text + '</a>' + pill + '</li>';
  }

  dlg.addEventListener('click', function(e) {
    var b = e.target.closest('.people-pill');
    if (!b) return;
    var id = b.getAttribute('data-id');
    C.gate(function(s) {
      token = s.access_token;
      var on = !!following[id];
      b.disabled = true;
      var req = on
        ? api('DELETE', '/rest/v1/follows?follower=eq.' + me + '&followee=eq.' + id)
        : api('POST', '/rest/v1/follows', { follower: me, followee: id });
      req.then(function(r) {
        b.disabled = false;
        if (!r.ok) return;
        if (on) delete following[id]; else following[id] = true;
        b.classList.toggle('on', !on);
        b.setAttribute('aria-pressed', on ? 'false' : 'true');
        b.textContent = label(id);
        // The same person may stand in Suggested and in the results.
        dlg.querySelectorAll('.people-pill[data-id="' + id + '"]').forEach(function(o) {
          o.classList.toggle('on', !on); o.setAttribute('aria-pressed', on ? 'false' : 'true'); o.textContent = label(id);
        });
        var n = el('n-following');
        if (n) n.textContent = Math.max(0, (parseInt(n.textContent, 10) || 0) + (on ? -1 : 1));
      }).catch(function() { b.disabled = false; });
    }, function() { if (window.atOpenSignIn) window.atOpenSignIn(); });
  });

  // SHARE YOUR PROFILE.
  function share() {
    var url = location.origin + '/profile?u=' + encodeURIComponent(me);
    if (window.at && at.shareUrl) { url = at.shareUrl(url, 'profile'); }
    if (window.at && at.track) { at.track('share_tapped', 'profile'); }
    var text = el('people-share').getAttribute('data-text');
    var phone = window.matchMedia && matchMedia('(pointer: coarse)').matches;
    function copy() {
      var done = function() { if (window.atSnack) window.atSnack(el('people-share').getAttribute('data-copied')); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, function() {});
    }
    if (phone && navigator.share) {
      // Refused when the tap is too long ago (right after Make public): copy.
      navigator.share({ text: text, url: url }).catch(function(err) { if (err && err.name === 'NotAllowedError') copy(); });
      return;
    }
    copy();
  }
  el('people-share').addEventListener('click', function() {
    C.gate(function(s) {
      token = s.access_token;
      if (isPublic) { share(); return; }
      // A public profile shows a name, and no profiles row exists until
      // somebody sets one: the name first, where it is set.
      if (!hasName) {
        dlg.close();
        if (window.atSnack) window.atSnack(el('people-share').getAttribute('data-name'),
          el('people-share').getAttribute('data-settings'), '/account/settings');
        return;
      }
      step('ask');
    }, function() { if (window.atOpenSignIn) window.atOpenSignIn(); });
  });
  el('people-pub-yes').addEventListener('click', function() {
    var b = this; b.disabled = true;
    api('PATCH', '/rest/v1/profiles?user_id=eq.' + me, { public: true })
      .then(function(r) {
        b.disabled = false;
        if (!r.ok) return;
        isPublic = true;
        step('list');
        share();
      }).catch(function() { b.disabled = false; });
  });
  el('people-pub-no').addEventListener('click', function() { step('list'); });

  el('people-open').addEventListener('click', function() { open('search'); });
  el('n-followers-btn').addEventListener('click', function() { open('followers'); });
  el('n-following-btn').addEventListener('click', function() { open('following'); });
})();
</script>
`;
