// THE FILTER ROW, once for every map that carries it: /explore in every
// language and the city map (Hidde, 2026-11-01: "put the filters also on city
// map"). The chips themselves are components/MapFilters.astro; this is what
// they do. It used to live inside exploreMapScript() and nowhere else, so a
// city map had no way to say "only what I can visit for free".
//
// Ships as text inside a map script, like PINS_JS. The page hands over three
// things (atMapFilters below): how to redraw with the filter applied, the trees
// it can count species on, and the species list, which the explore map carries
// inline and the city map fetches when the chip is first opened.
import { icon } from "./icons";

export function mapFiltersJs(): string {
  return `
// ---- THE FILTER ROW (2026-09-12).
//
// Convention, looked up rather than invented (CONVENTIONS.md): Google Maps
// puts a scrolling row of capsule chips over the top of the map and nothing
// else; AllTrails and Airbnb put a Filters BUTTON that opens a sheet, which is
// the right shape for eight filters and the wrong one for four. Our own app
// draws the chip row, so the website draws the same row: same capsules, same
// words, same order. The app's row today is the walk chip, Favourites, My
// trees and Species (MapTab.swift has Hidde's reasons for the cuts); the
// website takes that row minus the walk chip, which is Plus, plus FREE TO
// VISIT (Hidde, 2026-09-12: "ik zou nog wel een filter willen bouwen voor
// betaalde bomen waar je een ticket voor moet kopen - dat je die weg kunt
// halen").
var FILTERS = { free: false, fav: false, mine: false, sp: -1 };
function filtersOn() {
  return FILTERS.free || FILTERS.fav || FILTERS.mine || FILTERS.sp >= 0;
}
// p: a tree's properties, {id, paid, sp}.
function keepsTree(p) {
  if (FILTERS.free && p.paid) return false;
  if (FILTERS.sp >= 0 && p.sp !== FILTERS.sp) return false;
  if (FILTERS.fav && !(window.atHasSaved && window.atHasSaved(p.id))) return false;
  if (FILTERS.mine && !(window.atHasVisited && window.atHasVisited(p.id))) return false;
  return true;
}
// A number only while a filter is on. The map's own copy carries no counts
// on purpose (2026-07-29), and this is not copy: it is the answer to what
// you just pressed, and zero has to be sayable.
function atFilterCount(n) {
  var note = document.getElementById('mf-count');
  if (!note) return;
  note.hidden = !filtersOn();
  note.textContent = n === 0 ? 'No trees match' : (n === 1 ? '1 tree' : n + ' trees');
}
function atFiltEsc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
// o.apply(): redraw with FILTERS applied. o.items(): [{sp, c: [lng, lat]}]
// for every tree the map holds. o.ready(cb): calls cb once the globals
// SPECIES and SPECIES_L (names and their Latin as HTML) are set. o.map(): the
// map, or null before it exists.
//
// CALLED BEFORE THE MAP (2026-10-07): MapLibre throws where WebGL is
// unavailable, and everything after the constructor then never runs. A chip
// that cannot ask for sign-in because the map failed is the dead control
// Hidde keeps finding; it asks first.
function atMapFilters(o) {
  // Both lists live in the account, so both chips need one. Signed out they
  // ask rather than emptying the map, which is the rule Hidde set for the
  // app's own two: "als je uitgelogd op favourites of my trees filter klikt
  // moet er ook een inlog scherm opkomen." AND THE SERVER DECIDES whether
  // there is an account, through the one door every gated tap uses
  // (atCollection.gate, 2026-10-05).
  function toggleFilter(b, f) {
    FILTERS[f] = !FILTERS[f];
    b.classList.toggle('is-on', FILTERS[f]);
    b.setAttribute('aria-pressed', FILTERS[f] ? 'true' : 'false');
    o.apply();
  }
  document.querySelectorAll('.mf[data-f]').forEach(function(b) {
    b.addEventListener('click', function() {
      var f = b.dataset.f;
      if ((f === 'fav' || f === 'mine') && !FILTERS[f]) {
        var C = window.atCollection;
        var ask = function() {
          // Signed out: sign in and come back with THIS chip on, rather than
          // landing on an unfiltered map having been asked for nothing.
          if (window.atOpenSignIn) window.atOpenSignIn(b.dataset.label || b.textContent.trim(), null, { kind: 'filter', filter: f });
        };
        if (C && C.gate) C.gate(function() { toggleFilter(b, f); }, ask);
        else ask();
        return;
      }
      toggleFilter(b, f);
    });
  });
  // Back from signing in with a chip to switch on (signin-js hands it over).
  if (window.atPendingFilter) {
    var pf = window.atPendingFilter; window.atPendingFilter = null;
    var pb = document.querySelector('.mf[data-f="' + pf + '"]');
    var PC = window.atCollection;
    if (pb && !FILTERS[pf] && PC && PC.gate) {
      // After the saved and seen lists have arrived, or the filter keeps nothing.
      var jobs = [];
      if (window.atSyncSaves) jobs.push(Promise.resolve(window.atSyncSaves()));
      if (window.atSyncVisited) jobs.push(Promise.resolve(window.atSyncVisited()));
      PC.gate(function() { Promise.all(jobs).then(function() { toggleFilter(pb, pf); }).catch(function() {}); }, function() {});
    }
  }
  // The account's two lists arrive after this runs, so a chip pressed while
  // they are still in flight repaints when they land.
  window.atRefilterMap = o.apply;

  // The species chip wears the chosen species, the way the app's does
  // (FilterChipLabel(label: filters.species ?? "Species")), and opens the
  // species sheet: the app's SpeciesPicker, row for row (Hidde, 2026-10-31,
  // "cross platform always"). Species on the map in view first, then by how
  // many we map; typing answers to the name, the Latin, every other name it
  // goes by and one letter off, best match first, the way
  // Kit/SpeciesSearch.swift does. The row says which name answered. Tapping
  // the chosen species again turns it off, as in the app.
  var spWrap = document.getElementById('mf-species-wrap');
  var spLabel = document.getElementById('mf-species-label');
  var spSheet = document.getElementById('sp-sheet');
  var spQ = document.getElementById('sp-q');
  var spList = document.getElementById('sp-list');
  var spEmpty = document.getElementById('sp-empty');
  var spAnyBtn = document.getElementById('sp-any');
  if (!(spWrap && spSheet && spQ && spList)) return;
  var spAnyText = spLabel ? spLabel.textContent : '';
  var SP_TICK = ${JSON.stringify(icon("check", "bold"))};
  var spNames = null, spLoading = false, spOrder = [], spCount = [], spPlain = [];
  var spFold = function(s) {
    s = String(s).toLowerCase();
    try { s = s.normalize('NFD').replace(/[\\u0300-\\u036f]/g, ''); } catch (e) {}
    return s.trim();
  };
  var spWords = function(f) { return f.split(/[ ('-]+/).filter(Boolean); };
  var spStarts = function(name, q) {
    var n = spFold(name);
    return n.indexOf(q) === 0 || spWords(n).some(function(w) { return w.indexOf(q) === 0; });
  };
  var spDist = function(a, b) {
    if (Math.abs(a.length - b.length) > 1) return 2;
    var prev = [], cur, i, j;
    for (j = 0; j <= b.length; j++) prev.push(j);
    for (i = 1; i <= a.length; i++) {
      cur = [i];
      for (j = 1; j <= b.length; j++) {
        cur.push(Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)));
      }
      prev = cur;
    }
    return prev[b.length];
  };
  // Five letters at least: below that one letter off matches half the list.
  var spNearly = function(name, q) {
    if (q.length < 5) return false;
    return spWords(spFold(name)).some(function(w) {
      for (var len = q.length - 1; len <= q.length + 1; len++) {
        if (len > 0 && len <= w.length && spDist(q, w.slice(0, len)) <= 1) return true;
      }
      return false;
    });
  };
  // [rank, the other name that answered]: 0 name, 1 Latin, 2 another name, 3 nearly.
  var spHit = function(i, q) {
    if (!q) return [0, ''];
    var c = SPECIES[i], l = spPlain[i], other = (spNames && spNames[c]) || [], k;
    if (spStarts(c, q)) return [0, ''];
    if (l && spStarts(l, q)) return [1, ''];
    for (k = 0; k < other.length; k++) if (spStarts(other[k], q)) return [2, other[k]];
    if (spNearly(c, q) || (l && spNearly(l, q))) return [3, ''];
    for (k = 0; k < other.length; k++) if (spNearly(other[k], q)) return [2, other[k]];
    return null;
  };
  var spRender = function() {
    var q = spFold(spQ.value), rows = [];
    spOrder.forEach(function(i, pos) {
      var h = spHit(i, q);
      if (h) rows.push({ i: i, pos: pos, r: h[0], via: h[1] });
    });
    rows.sort(function(a, b) { return a.r - b.r || a.pos - b.pos; });
    if (spAnyBtn) spAnyBtn.hidden = FILTERS.sp < 0;
    if (spEmpty) spEmpty.hidden = rows.length > 0;
    spList.innerHTML = rows.map(function(row) {
      var i = row.i, sub = (row.via ? atFiltEsc(row.via) + (SPECIES_L[i] ? ' &middot; ' : '') : '') + SPECIES_L[i];
      return '<li><button type="button" class="sp-row" data-i="' + i + '">' +
        '<span class="sp-txt"><span class="sp-n">' + atFiltEsc(SPECIES[i]) + '</span>' +
        (sub ? '<span class="sp-sub">' + sub + '</span>' : '') + '</span>' +
        (FILTERS.sp === i ? '<span class="sp-tick">' + SP_TICK + '</span>' : '<span class="sp-c">' + spCount[i] + '</span>') +
        '</button></li>';
    }).join('');
  };
  var spLoad = function() {
    if (spNames || spLoading) return;
    spLoading = true;
    fetch('/api/species.json').then(function(r) { return r.json(); }).then(function(j) {
      spNames = {};
      (j.names || []).forEach(function(r) { if (r.m !== false && !r.g) spNames[r.c] = r.a || []; });
      if (spQ.value) spRender();
    }).catch(function() { spLoading = false; });
  };
  var spChoose = function(i) {
    FILTERS.sp = i;
    spWrap.classList.toggle('is-on', i >= 0);
    if (spLabel) spLabel.textContent = i < 0 ? spAnyText : SPECIES[i];
    o.apply();
    spSheet.close();
  };
  spWrap.addEventListener('click', function() {
    o.ready(function() {
      spPlain = SPECIES_L.map(function(h) { return h.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&'); });
      // Only the species this map holds, counted now: the city map's
      // neighbours arrive after the page does.
      spCount = SPECIES.map(function() { return 0; });
      // What is around you first, as the app's picker leads with what is on
      // the map: counted when the sheet opens, against the map as it stands.
      var near = {}, b = null, m = o.map();
      try { b = m && m.getBounds(); } catch (e) {}
      o.items().forEach(function(t) {
        if (t.sp === undefined || t.sp === null || t.sp < 0) return;
        spCount[t.sp]++;
        if (b && t.c[0] !== null && b.contains(t.c)) near[t.sp] = 1;
      });
      spOrder = SPECIES.map(function(_, i) { return i; }).filter(function(i) { return spCount[i] > 0; }).sort(function(a, b) {
        return (near[b] ? 1 : 0) - (near[a] ? 1 : 0) || spCount[b] - spCount[a] || a - b;
      });
      spQ.value = '';
      spRender();
      spLoad();
      spSheet.showModal();
      spList.scrollTop = 0;
      // The keyboard only where there is one to spare: on a phone it would
      // cover the list before anybody has looked at it (the app's .searchable
      // does not focus either).
      if (window.matchMedia('(pointer: fine)').matches) spQ.focus(); else spQ.blur();
    });
  });
  spQ.addEventListener('input', function() { spLoad(); spRender(); });
  spList.addEventListener('click', function(e) {
    var btn = e.target.closest && e.target.closest('.sp-row');
    if (!btn) return;
    var i = parseInt(btn.getAttribute('data-i'), 10);
    spChoose(FILTERS.sp === i ? -1 : i);
  });
  if (spAnyBtn) spAnyBtn.addEventListener('click', function() { spChoose(-1); });
}
`;
}
