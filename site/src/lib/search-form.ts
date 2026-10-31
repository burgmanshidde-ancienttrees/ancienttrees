// The one search interaction (Hidde, 2026-08-01: "ik wil dezelfde interactie
// op home en hier en ik wil dat je die gelijk houdt"). Ported verbatim from
// search_form()/SEARCH_WIDGET_JS, build_site.py:2087-2225. One shared
// /search-index.json, so home and /explore cannot drift apart.
import { ui } from "./i18n";
import { icon } from "./icons";

export function searchForm(ctx: string, inputId: string, formClass: string, withButton = false, placeholder = "Search a city or tree"): string {
  const ico = withButton
    ? '<button type="submit" class="search-ico" aria-label="Search">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">' +
      '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg></button>'
    : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">' +
      '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg>';
  return (
    `<form class="${formClass} at-search" data-ctx="${ctx}" role="search" autocomplete="off">` +
    `${ico}` +
    `<input type="search" id="${inputId}" placeholder="${placeholder}"` +
    ` aria-label="${placeholder}" autocapitalize="off" autocorrect="off" spellcheck="false">` +
    `<div class="ats-drop" hidden></div></form>`
  );
}

/** The widget in the page's language. Only the empty-place answer is
 * translated so far (2026-10-25); the older section heads are still English. */
export function searchWidgetJs(lang = "en"): string {
  const U = ui(lang);
  const S = {
    title: U.emptyPlaceTitle, ask: U.emptyPlaceAsk, add: U.addTree, onMap: U.placeOnMap,
    nearest: U.nearestTree, kmFrom: U.kmFrom, none: U.searchNoMatch,
    explore: lang === "en" ? "/explore" : `/${lang}/explore`,
  };
  return `
<script>
(function() {
  var STR = ${JSON.stringify(S)};
  // Every .at-search on the page gets wired, so a second placement (a header
  // bar, the AllTrails pattern) needs no new script.
  Array.prototype.forEach.call(document.querySelectorAll('form.at-search'), setup);
  function setup(form) {
  if (form.getAttribute('data-ready')) return;
  form.setAttribute('data-ready', '1');
  var input = form.querySelector('input');
  var drop = form.querySelector('.ats-drop');
  var ctx = form.getAttribute('data-ctx');
  var IDX = null, loading = false, rows = [], active = -1;
  // The towns we hold no tree for (places.json, GeoNames), fetched the first
  // time a query matches nothing of ours. lastEmpty remembers what the visitor
  // met, so a search that ends there is logged as a request: until 2026-10-25
  // only a clicked result was ever recorded, and a dead end left no trace.
  var PL = null, plLoading = false, lastEmpty = null;
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
    // A species answers to its common name OR its scientific name (2026-10-03,
    // a reader asked for Latin names). The convention is iNaturalist's
    // autocomplete, which matches either and says which one it matched. Latin
    // matches on the start of any word, so "robur" finds Quercus robur the way
    // a botanist would type it; the common name keeps its start-of-name bar.
    // Its name in any of our languages answers too (s.a, 2026-10-31: Hidde
    // often does not know the English name), on the start of any word, and
    // the row then says which name matched, iNaturalist's matched_term.
    function wordStart(name) { var x = norm(name); return x.indexOf(q) === 0 || x.indexOf(' ' + q) !== -1 || x.indexOf('-' + q) !== -1; }
    IDX.s.forEach(function(s) {
      var l = norm(s.l || '');
      if (norm(s.n).indexOf(q) === 0) species.push({kind: 'species', it: s});
      else if (l && (l.indexOf(q) === 0 || l.indexOf(' ' + q) !== -1)) species.push({kind: 'species', it: s});
      else {
        var hit = (s.a || []).filter(wordStart)[0];
        if (hit) species.push({kind: 'species', it: s, via: hit});
      }
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
    // Two species beside six places, six when no place matched: the app's
    // budget (MapSearch.swift), ported back so "quercus" shows the oaks rather
    // than two of them. The lists were already the same eight rows otherwise.
    var p = places.slice(0, 6);
    out = p.concat(species.slice(0, p.length ? 2 : 6));
    var room = 8 - out.length;
    if (room > 0) out = out.concat(trees.slice(0, Math.min(room, places.length ? 2 : 5)));
    return out;
  }

  function loadPlaces() {
    if (PL || plLoading) return;
    plLoading = true;
    fetch('/places.json').then(function(r) { return r.json(); })
      .then(function(j) { PL = j; if (document.activeElement === input) show(); })
      .catch(function() { plLoading = false; });
  }
  function hide() {
    if (lastEmpty) { at.track('search-' + lastEmpty.kind + '-' + ctx, lastEmpty.q.slice(0, 60)); lastEmpty = null; }
    drop.hidden = true; active = -1;
  }
  function fill(s, v) { return s.replace(/\\{(\\w+)\\}/g, function(m, k) { return v[k] !== undefined ? v[k] : m; }); }
  // One list of our own rows under their heads; lastKind lets a caller
  // continue a section it already opened.
  function listHtml(res, lastKind) {
    return res.map(function(r) {
      var name, sec, head = '';
      if (r.kind === 'country') {
        name = r.it.country;
        sec = r.it.cities + ' cities &middot; ' + r.it.n + ' trees';
      } else if (r.kind === 'city') {
        name = r.it.city;
        sec = r.it.n + (r.it.n === 1 ? ' tree' : ' trees') + ' &middot; ' + escT(r.it.country);
      } else if (r.kind === 'species') {
        name = r.it.n;
        // The scientific name under the common one, in italics, which is how
        // iNaturalist lays out a taxon row; it is also the only way a person
        // who typed the Latin can see why this row answered.
        sec = (r.via ? escT(r.via) + ' &middot; ' : '') +
              (r.it.lh ? r.it.lh + ' &middot; ' : '') + r.it.count + ' mapped';
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
  // A town we hold no tree for: the grey card of an empty notes section (the
  // same ask, the same look), the towns on the map, and the nearest tree
  // (Hidde, 2026-10-25). Only while none of our places begins with the query; a typo that is no
  // town either gets one plain line and no card.
  function emptyAnswer(q, res) {
    var hits = [];
    for (var i = 0; i < PL.p.length && hits.length < 4; i++) {
      var p = PL.p[i];
      if (norm(p[0]).indexOf(q) === 0 || (p[1] && norm(p[1]).indexOf(q) === 0)) hits.push(p);
    }
    if (!hits.length) return '';
    var top = hits[0], html = '';
    // A town with one of our trees inside 5 km is not empty, whatever its name.
    if (top[6] < 0 || top[6] >= 5) {
      lastEmpty = {kind: 'empty', q: q};
      html += '<div class="ats-card td-notes-empty">' +
        '<span class="td-notes-empty-ic" aria-hidden="true">${icon("tree", "regular")}</span>' +
        '<p class="td-notes-empty-t">' + escT(fill(STR.title, {place: top[0]})) + '</p>' +
        '<p class="td-notes-empty-s">' + escT(STR.ask) + '</p>' +
        '<div class="td-notes-empty-act"><a class="addphoto-btn quiet td-note-ask ats-go" data-ev="empty-place-add" href="/contribute?kind=tree&city=' +
        encodeURIComponent(top[0]) + '">${icon("plus", "bold")}<span>' + escT(STR.add) + '</span></a></div></div>';
    }
    // Our places that only contain the letters (Oberndorf for "bern") go: the
    // visitor meant the town. Species and trees follow the nearest tree.
    var ourOther = res.filter(function(r) { return r.kind !== 'city' && r.kind !== 'country'; });
    html += '<div class="ats-head">Places</div>' + hits.map(function(p) {
      return row(p[0], escT(PL.k[p[2]]) + ' &middot; ' + escT(STR.onMap),
                 STR.explore + '#@' + p[3] + ',' + p[4] + ',' + encodeURIComponent(p[0]));
    }).join('');
    if (top[5] >= 0) {
      var t = PL.t[top[5]];
      html += '<div class="ats-head">' + escT(STR.nearest) + '</div>' +
              row(t[0], escT(fill(STR.kmFrom, {km: top[6], place: top[0]})) + ' &middot; ' + escT(t[1]), '/' + t[2]);
    }
    return html + listHtml(ourOther, null);
  }

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
    // The most VISITED pages, not the deepest (Hidde, 2026-09-26): the v field is
    // their search traffic, refreshed daily. Tree count only breaks ties and
    // fills in for pages nobody has visited yet. The app sorts the same way.
    var top = IDX.c.slice().sort(function(a, b) {
      return (b.v || 0) - (a.v || 0) || b.n - a.n;
    }).slice(0, 5);
    html += '<div class="ats-head">Start here</div>';
    html += top.map(function(c) {
      return row(c.city, c.n + (c.n === 1 ? ' tree' : ' trees') + ' &middot; ' + escT(c.country), '/' + c.u);
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
    lastEmpty = null;
    // The empty-place answer comes up when none of OUR places begins with what
    // was typed: "Bern" finds Oberndorf and a linden in Vilnius by their
    // letters, but the visitor meant the town.
    var strong = res.some(function(r) {
      if (r.kind === 'country') return norm(r.it.country).indexOf(q) === 0;
      if (r.kind !== 'city') return false;
      // A name in another language counts only whole: Brno's "Bërno" begins
      // with "bern", and nobody typing Bern means Brno.
      return norm(r.it.city).indexOf(q) === 0 || (r.it.a && r.it.a.some(function(n) { return norm(n) === q; }));
    });
    var html = '';
    if (!strong && q.length >= 3) {
      loadPlaces();
      if (PL) html = emptyAnswer(q, res);
    }
    if (!html) {
      if (!res.length) {
        // Two letters match half the world's towns; wait for a third.
        if (q.length < 3 || !PL) { drop.hidden = true; rows = []; return; }
        lastEmpty = {kind: 'none', q: q};
        html = '<div class="ats-empty">' + escT(fill(STR.none, {q: input.value.trim()})) + '</div>';
      } else {
        html = listHtml(res, null);
      }
    }
    drop.innerHTML = html;
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
    lastEmpty = null;
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
    var b = e.target.closest ? e.target.closest('.ats-go') : null;
    if (b) {
      e.preventDefault();
      at.track(b.getAttribute('data-ev'), norm(input.value.trim()).slice(0, 60));
      lastEmpty = null;
      window.location.href = b.getAttribute('href');
      return;
    }
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
}

export const SEARCH_WIDGET_JS = searchWidgetJs("en");
