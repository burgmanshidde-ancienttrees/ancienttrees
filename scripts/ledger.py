#!/usr/bin/env python3
"""The city coverage ledger, as a page Hidde can open whenever he likes.

Hidde, 2026-08-16, on the first one: "can we keep this ledger somewhere and keep
it up to date or is that heavy on the token side i like to look at it more
often".

It is not heavy. Every number here already exists in `data/city-queue.json`,
which `scripts/city_queue.py` rewrites on every night run, so this file is a
rendering job rather than a research job: deterministic Python, no model, no
tokens. `city_queue.py` calls it at the end of its own run, so LEDGER.html is
never staler than the queue it is drawn from.

Two things it deliberately does NOT do. It does not fetch anything, so it cannot
fail a run or hang on a host. And it does not publish itself: the Artifact copy
is republished from a session when somebody asks, because publishing is an
outward-facing act and a cron job should not be doing it unattended.

    python3 scripts/ledger.py          # rewrite LEDGER.html
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "city-queue.json")
OUT = os.path.join(ROOT, "LEDGER.html")

CSS = """<style>
:root{
  --ground:#F6F7F4; --surface:#FFFFFF; --ink:#1A1F1B; --muted:#6B7269;
  --faint:#9AA096; --line:#DFE3DA; --accent:#2E5E42;
  --attention:#A8621C; --attention-soft:#F0DFC9; --zero:#C4C9BE;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
  --sans:ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --ground:#12150F; --surface:#1A1E17; --ink:#E9ECE3; --muted:#9AA394;
  --faint:#6E7668; --line:#2B3128; --accent:#84BC97;
  --attention:#D79A56; --attention-soft:#3A2C18; --zero:#3A4036;
}}
:root[data-theme="dark"]{
  --ground:#12150F; --surface:#1A1E17; --ink:#E9ECE3; --muted:#9AA394;
  --faint:#6E7668; --line:#2B3128; --accent:#84BC97;
  --attention:#D79A56; --attention-soft:#3A2C18; --zero:#3A4036;
}
*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font-family:var(--sans);
  margin:0;padding:2.2rem 1.4rem 4rem;line-height:1.5;
  -webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}
.wrap{max-width:1080px;margin:0 auto;display:flex;flex-direction:column;gap:1.9rem}
header{display:flex;flex-direction:column;gap:.5rem}
.eyebrow{font-size:.72rem;letter-spacing:.13em;text-transform:uppercase;color:var(--muted)}
h1{font-family:var(--serif);font-weight:600;font-size:clamp(1.9rem,4.4vw,2.7rem);
  margin:0;text-wrap:balance;letter-spacing:-.012em}
.sub{color:var(--muted);max-width:64ch;font-size:.95rem}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:.7rem}
.tile{background:var(--surface);border:1px solid var(--line);border-radius:3px;
  padding:.85rem .95rem;display:flex;flex-direction:column;gap:.15rem}
.tile .n{font-family:var(--serif);font-size:1.75rem;line-height:1.1}
.tile .k{font-size:.7rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.tile .note{font-size:.76rem;color:var(--faint)}
.tile.warn .n{color:var(--attention)}
.controls{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}
input[type=search]{font:inherit;background:var(--surface);color:var(--ink);
  border:1px solid var(--line);border-radius:3px;padding:.42rem .6rem;min-width:200px}
.chip{font:inherit;font-size:.82rem;background:var(--surface);color:var(--muted);
  border:1px solid var(--line);border-radius:999px;padding:.32rem .78rem;cursor:pointer}
.chip[aria-pressed=true]{background:var(--accent);border-color:var(--accent);color:var(--ground)}
.chip:focus-visible,th button:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:3px;background:var(--surface)}
table{border-collapse:collapse;width:100%;font-size:.86rem;min-width:720px}
thead th{position:sticky;top:0;background:var(--surface);border-bottom:1px solid var(--line);
  text-align:left;padding:0;z-index:2}
th button{font:inherit;font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);background:none;border:0;padding:.6rem .55rem;width:100%;
  text-align:inherit;cursor:pointer}
th.num{text-align:right} th.num button{text-align:right}
td{padding:.4rem .55rem;border-bottom:1px solid var(--line);vertical-align:middle}
tbody tr:last-child td{border-bottom:0}
td.num{text-align:right;font-variant-numeric:tabular-nums}
.city{font-weight:600}
.country{color:var(--faint);font-size:.78rem}
.bar{position:relative;height:5px;border-radius:3px;background:var(--zero);
  min-width:46px;overflow:hidden;display:block}
.bar i{position:absolute;inset:0 auto 0 0;background:var(--accent);border-radius:3px}
.dash{color:var(--faint)}
.flag{display:inline-block;font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;
  padding:.1rem .38rem;border-radius:2px;background:var(--attention-soft);color:var(--attention)}
.count{color:var(--muted);font-size:.82rem}
footer{color:var(--faint);font-size:.78rem;max-width:70ch}
@media (max-width:640px){body{padding:1.4rem .8rem 3rem}}
.rule{margin:2.2rem 0 1rem;padding:1.2rem 1.4rem;background:var(--surface);
  border-radius:12px;border:1px solid rgba(0,0,0,.07)}
.rule h2{margin:0 0 .6rem;font-size:1.05rem}
.rule p{margin:.5rem 0;color:var(--muted);line-height:1.55}
.rule-table{border-collapse:collapse;margin:.6rem 0}
.rule-table td{padding:.3rem .9rem .3rem 0;color:var(--muted)}
.rule-table td:last-child{text-align:right;color:var(--ink)}
</style>"""


def build():
    with open(QUEUE, encoding="utf-8") as fh:
        cities = json.load(fh)["cities"]
    rows = sorted(
        ([c["rank"], c["city"], c.get("country") or "", c.get("trees", 0),
          c.get("target") or 10, c.get("photos", 0),
          c.get("impressions_10d") or 0, c.get("clicks_10d") or 0,
          c.get("register") or 0]
         for c in cities if c.get("rank")), key=lambda r: r[0])

    live = [r for r in rows if r[3] > 0]
    trees = sum(r[3] for r in rows)
    photos = sum(r[5] for r in rows)
    imp = sum(r[6] for r in rows)
    clicks = sum(r[7] for r in rows)
    silent = sum(1 for r in live if r[6] == 0)
    nophoto = sum(1 for r in live if r[5] == 0)
    ctr = ("%.1f%%" % (clicks / imp * 100)) if imp else "n/a"
    pct_photo = ("%d%%" % round(photos / trees * 100)) if trees else "n/a"

    # The generated stamp is the date the queue was last rebuilt, taken from
    # the file itself rather than from the clock, so the page never claims to
    # be fresher than its data.
    import datetime
    stamp = datetime.date.fromtimestamp(os.path.getmtime(QUEUE)).strftime("%d %B %Y")

    tiles = [
        ("Ranked cities", len(rows), "%d live, %d not started" % (len(live), len(rows) - len(live)), False),
        ("Trees", "{:,}".format(trees), "on ranked cities", False),
        ("Photographs", "{:,}".format(photos), "%s of trees" % pct_photo, False),
        ("Impressions", "{:,}".format(imp), "%d clicks, %s CTR" % (clicks, ctr), False),
        ("Live, never seen", silent, "pages with zero impressions", True),
        ("Live, no photo", nophoto, "of %d live cities" % len(live), True),
    ]
    tilehtml = "".join(
        '<div class="tile%s"><span class="k">%s</span><span class="n">%s</span>'
        '<span class="note">%s</span></div>' % (" warn" if w else "", k, n, note)
        for k, n, note, w in tiles)

    return """<title>City Coverage Ledger</title>
%s
<div class="wrap">
<header>
  <div class="eyebrow">Ancient Trees &middot; %s</div>
  <h1>City Coverage Ledger</h1>
  <p class="sub">Every ranked city, what it holds and what search does with it.
  Search figures are Google impressions and clicks over a ten-day window, the only
  per-page traffic the project measures.</p>
</header>
<section class="tiles">%s</section>
<div class="controls">
  <input type="search" id="q" placeholder="Filter by city or country" aria-label="Filter by city or country">
  <button class="chip" data-f="all" aria-pressed="true">All</button>
  <button class="chip" data-f="live" aria-pressed="false">Live</button>
  <button class="chip" data-f="todo" aria-pressed="false">Not started</button>
  <button class="chip" data-f="nophoto" aria-pressed="false">Live, no photo</button>
  <button class="chip" data-f="silent" aria-pressed="false">Live, no impressions</button>
  <span class="count" id="count"></span>
</div>
<div class="tablewrap">
<table>
<thead><tr>
  <th class="num"><button data-s="0">#</button></th>
  <th><button data-s="1">City</button></th>
  <th class="num"><button data-s="3">Trees</button></th>
  <th><button data-s="3">To target</button></th>
  <th class="num"><button data-s="5">Photos</button></th>
  <th class="num"><button data-s="6">Impr.</button></th>
  <th><button data-s="6">Search</button></th>
  <th class="num"><button data-s="7">Clicks</button></th>
  <th class="num"><button data-s="8">Register</button></th>
</tr></thead>
<tbody id="rows"></tbody>
</table>
</div>
<section class="rule">
<h2>What the machine works on, and how far it takes a city</h2>
<p><strong>First: open the cities that have no trees yet</strong>, to ten, as fast as they
go. Set 19 August 2026, reading this very table: a new city taken to ten is a page that
can start ranking, while a thirtieth tree in a city we already cover is marginal. Cities
with no register behind them count here too; from-zero research is normally off and is on
for these because they were named.</p>
<p><strong>Then deepen</strong>, to one of three numbers:</p>
<table class="rule-table">
<tr><td>new city or village, not yet confirmed by Search Console</td><td><b>10</b></td></tr>
<tr><td>confirmed city</td><td><b>20</b></td></tr>
<tr><td>confirmed big city, 8,000+ travel demand</td><td><b>30</b></td></tr>
</table>
<p>Thirty is the ceiling everywhere. A page that needs fifty is a page padded past the
point where every entry deserves its spot, and that exclusivity is the product. Every
target is a ceiling and a stopping point, never a quota: the moment the next tree gets
hard to find, the city is finished for now. Cadiz at five is finished work.</p>
</section>
<footer>Trees, photographs and register supply are counted from the project's own
data. Impressions and clicks come from Search Console and are a ten-day window, so a
zero means the page was not served in that window rather than that it does not exist.
Register supply counts designated trees within reach of the city, not trees we publish.
Regenerated by scripts/ledger.py whenever the city queue is rebuilt.</footer>
</div>
<script>
const ROWS = %s;
let sortKey = 0, sortDir = 1, filter = 'all', query = '';
const tb = document.getElementById('rows'), countEl = document.getElementById('count');
const maxImp = Math.max(1, ...ROWS.map(r => r[6]));

function bar(val, max){
  const pct = max > 0 ? Math.min(100, Math.round(val / max * 100)) : 0;
  return '<span class="bar"><i style="width:' + pct + '%%"></i></span>';
}
function passes(r){
  if (query && !(r[1] + ' ' + r[2]).toLowerCase().includes(query)) return false;
  if (filter === 'live') return r[3] > 0;
  if (filter === 'todo') return r[3] === 0;
  if (filter === 'nophoto') return r[3] > 0 && r[5] === 0;
  if (filter === 'silent') return r[3] > 0 && r[6] === 0;
  return true;
}
function render(){
  const rows = ROWS.filter(passes).sort((a, b) => {
    const x = a[sortKey], y = b[sortKey];
    if (typeof x === 'string') return x.localeCompare(y) * sortDir;
    return (x - y) * sortDir;
  });
  countEl.textContent = rows.length + ' of ' + ROWS.length + ' cities';
  tb.innerHTML = rows.map(r => {
    const [rank, city, country, trees, target, photos, imp, clicks, reg] = r;
    const toTarget = trees === 0 ? '<span class="dash">not started</span>'
      : bar(Math.min(trees, target), target);
    const search = imp === 0
      ? (trees > 0 ? '<span class="flag">never served</span>' : '<span class="dash">&mdash;</span>')
      : bar(imp, maxImp);
    return '<tr>' +
      '<td class="num">' + rank + '</td>' +
      '<td><span class="city">' + city + '</span> <span class="country">' + country + '</span></td>' +
      '<td class="num">' + (trees || '<span class="dash">0</span>') + '</td>' +
      '<td>' + toTarget + '</td>' +
      '<td class="num">' + (photos ? photos : (trees > 0 ? '<span class="flag">0</span>' : '<span class="dash">&mdash;</span>')) + '</td>' +
      '<td class="num">' + (imp || '<span class="dash">0</span>') + '</td>' +
      '<td>' + search + '</td>' +
      '<td class="num">' + (clicks || '<span class="dash">0</span>') + '</td>' +
      '<td class="num">' + (reg || '<span class="dash">&mdash;</span>') + '</td>' +
      '</tr>';
  }).join('');
}
document.querySelectorAll('th button').forEach(b => b.addEventListener('click', () => {
  const k = +b.dataset.s;
  sortDir = (k === sortKey) ? -sortDir : (k === 1 ? 1 : -1);
  sortKey = k; render();
}));
document.querySelectorAll('.chip').forEach(c => c.addEventListener('click', () => {
  document.querySelectorAll('.chip').forEach(o => o.setAttribute('aria-pressed', o === c));
  filter = c.dataset.f; render();
}));
document.getElementById('q').addEventListener('input', e => {
  query = e.target.value.trim().toLowerCase(); render();
});
render();
</script>""" % (CSS, stamp, tilehtml,
                json.dumps(rows, ensure_ascii=False, separators=(",", ":")))


def main():
    html = build()
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("LEDGER.html rewritten (%d bytes)" % len(html))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
