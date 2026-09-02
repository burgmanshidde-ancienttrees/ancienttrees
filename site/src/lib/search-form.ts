// The one search interaction (Hidde, 2026-08-01: "ik wil dezelfde interactie
// op home en hier en ik wil dat je die gelijk houdt"). Ported verbatim from
// search_form()/SEARCH_WIDGET_JS, build_site.py:2087-2225. One shared
// /search-index.json, so home and /explore cannot drift apart.
export function searchForm(ctx: string, inputId: string, formClass: string, withButton = false): string {
  const ico = withButton
    ? '<button type="submit" class="search-ico" aria-label="Search">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">' +
      '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg></button>'
    : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">' +
      '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg>';
  return (
    `<form class="${formClass} at-search" data-ctx="${ctx}" role="search" autocomplete="off">` +
    `${ico}` +
    `<input type="search" id="${inputId}" placeholder="Search a city or tree"` +
    ` aria-label="Search a city or tree" autocapitalize="off" autocorrect="off" spellcheck="false">` +
    `<div class="ats-drop" hidden></div></form>`
  );
}

export const SEARCH_WIDGET_JS = `
<script>
(function() {
  // Every .at-search on the page gets wired, so a second placement (a header
  // bar, the AllTrails pattern) needs no new script.
  Array.prototype.forEach.call(document.querySelectorAll('form.at-search'), setup);
  function setup(form) {
  var input = form.querySelector('input');
  var drop = form.querySelector('.ats-drop');
  var ctx = form.getAttribute('data-ctx');
  var IDX = null, loading = false, rows = [], active = -1;
  function norm(s) {
    s = s.toLowerCase();
    try { s = s.normalize('NFD').replace(/[\\u0300-\\u036f]/g, ''); } catch (e) {}
    return s;
  }
  function escT(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
  function load() {
    if (IDX || loading) return;
    loading = true;
    fetch('/search-index.json').then(function(r) { return r.json(); })
      .then(function(j) { IDX = j; if (document.activeElement === input) show(); })
      .catch(function() { loading = false; });
  }
  function results(q) {
    // A hierarchy rather than one flat relevance list, which is what every
    // search-led map product does (Google Maps, AllTrails, Airbnb): places
    // first and always, then species, and an individual tree only when the
    // query is specific enough to be asking for one.
    var out = [];
    var places = [], species = [], trees = [];
    IDX.k.forEach(function(k) {
      var i = norm(k.country).indexOf(q);
      if (i === 0) places.unshift({kind: 'country', it: k});
      else if (i > 0) places.push({kind: 'country', it: k});
    });
    IDX.c.forEach(function(c) {
      var i = norm(c.city).indexOf(q);
      if (i === 0) { places.push({kind: 'city', it: c}); return; }
      // The city's name in other languages (c.a), so Den Haag finds The Hague
      // and Firenze finds Florence. Start-of-name only, the same bar the
      // English name clears at i === 0, because a substring match across ten
      // spellings per city turns two letters into a wall of results. The row
      // still shows the English name: that is what the page is called.
      var alt = c.a && c.a.some(function(n) { return norm(n).indexOf(q) === 0; });
      if (alt) { places.push({kind: 'city', it: c}); return; }
      if (i > 0 || norm(c.country).indexOf(q) === 0) places.push({kind: 'city', it: c});
    });
    IDX.s.forEach(function(s) {
      if (norm(s.n).indexOf(q) === 0) species.push({kind: 'species', it: s});
    });
    // Trees only earn a slot once the query is specific: at least four
    // characters, matching the start of a word in the name, and never
    // crowding out a place that matched.
    if (q.length >= 4) {
      IDX.t.forEach(function(t) {
        var n = norm(t.n);
        if (n.indexOf(q) === 0 || n.indexOf(' ' + q) !== -1) trees.push({kind: 'tree', it: t});
      });
    }
    out = places.slice(0, 6).concat(species.slice(0, 2));
    var room = 8 - out.length;
    if (room > 0) out = out.concat(trees.slice(0, Math.min(room, places.length ? 2 : 5)));
    return out;
  }

  function hide() { drop.hidden = true; active = -1; }

  // The zero-query state: what the dropdown shows the moment the field is
  // focused and still empty (Hidde, 2026-08-14, asking whether it is
  // conventional; it is). Google Maps, Airbnb, AllTrails and Booking all do
  // this, for the same reason it matters here: an empty field asks the
  // visitor to already know what we hold, and nobody arriving knows we have
  // Cadiz. Order is theirs too: what you looked at last, then where you are,
  // then somewhere to start.
  // WHAT YOU LOOKED AT LAST IS GONE (2026-09-02). It was three rows of
  // history kept in localStorage, and Hidde's rule leaves the browser holding
  // nothing but the session token. The rest of the empty state is unchanged
  // and is the half that was doing the work anyway: cities near you, then
  // somewhere to start. An account-backed history is a real feature and can
  // be built the day it is asked for; a browser-local one is exactly the kind
  // of thing this rule is about.
  function recents() { return []; }
  function remember() {}
  function row(name, sub, url, cls) {
    return '<a class="ats-row' + (cls ? ' ' + cls : '') + '" href="' + url + '">' +
           '<b>' + escT(name) + '</b><span>' + sub + '</span></a>';
  }
  function showEmpty() {
    load();
    if (!IDX) return;
    var html = '';
    var rec = recents();
    if (rec.length) {
      html += '<div class="ats-head">Recent</div>';
      html += rec.map(function(r) { return row(r.n, escT(r.s || ''), r.u); }).join('');
    }
    html += '<div class="ats-head">Near you</div>' +
            row('Trees near me', 'open the map at your location', '/explore#near', 'ats-near');
    // "Start here" rather than "Popular": we cannot see what is popular from
    // the browser, and the deepest pages are an honest proxy for the best
    // afternoon. Sorted by tree count, so it maintains itself.
    var top = IDX.c.slice().sort(function(a, b) { return b.n - a.n; }).slice(0, 5);
    html += '<div class="ats-head">Start here</div>';
    html += top.map(function(c) {
      return row(c.city, c.n + ' trees &middot; ' + escT(c.country), '/' + c.u);
    }).join('');
    drop.innerHTML = html;
    drop.hidden = false;
    rows = Array.prototype.slice.call(drop.querySelectorAll('.ats-row'));
    active = -1;
  }

  function show() {
    var q = norm(input.value.trim());
    if (!q) { showEmpty(); return; }
    load();
    if (!IDX) return;
    var res = results(q);
    active = -1;
    if (!res.length) {
      drop.innerHTML = '<div class="ats-empty">Not mapped yet. <a href="/contribute">Be the first to map it</a>.</div>';
    } else {
      var lastKind = null;
      drop.innerHTML = res.map(function(r) {
        var name, sec, head = '';
        if (r.kind === 'country') {
          name = r.it.country;
          sec = r.it.cities + ' cities &middot; ' + r.it.n + ' trees';
        } else if (r.kind === 'city') {
          name = r.it.city;
          sec = r.it.n + ' trees &middot; ' + escT(r.it.country);
        } else if (r.kind === 'species') {
          name = r.it.n;
          sec = r.it.count + ' mapped &middot; every one on the site';
        } else {
          name = r.it.n;
          sec = escT(r.it.c);
        }
        var label = (r.kind === 'country' || r.kind === 'city') ? 'Places'
                  : r.kind === 'species' ? 'Species' : 'Trees';
        if (label !== lastKind) { head = '<div class="ats-head">' + label + '</div>'; lastKind = label; }
        return head + '<a class="ats-row" href="/' + r.it.u + '"><b>' + escT(name) + '</b><span>' + sec + '</span></a>';
      }).join('');
    }
    drop.hidden = false;
    rows = Array.prototype.slice.call(drop.querySelectorAll('.ats-row'));
    rows.forEach(function(a) {
      a.addEventListener('click', function() {
        var b = a.querySelector('b'), sp = a.querySelector('span');
        remember(b ? b.textContent : '', sp ? sp.textContent : '', a.getAttribute('href'));
      });
    });
  }
  function go(row) {
    at.track('search-' + ctx, norm(input.value.trim()).slice(0, 60));
    window.location.href = row.getAttribute('href');
  }
  function mark(i) {
    rows.forEach(function(r) { r.classList.remove('active'); });
    if (i >= 0 && rows[i]) { rows[i].classList.add('active'); rows[i].scrollIntoView({block: 'nearest'}); }
    active = i;
  }
  input.addEventListener('input', show);
  input.addEventListener('focus', function() { load(); show(); });
  input.addEventListener('blur', function() { setTimeout(hide, 150); });
  input.addEventListener('keydown', function(e) {
    if (drop.hidden || !rows.length) return;
    if (e.key === 'ArrowDown') { e.preventDefault(); mark((active + 1) % rows.length); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); mark((active - 1 + rows.length) % rows.length); }
    else if (e.key === 'Escape') { hide(); }
  });
  drop.addEventListener('mousedown', function(e) {
    var a = e.target.closest ? e.target.closest('.ats-row') : null;
    if (a) { e.preventDefault(); go(a); }
  });
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    if (rows.length) { go(rows[active >= 0 ? active : 0]); }
  });
  }
})();
</script>
`;
