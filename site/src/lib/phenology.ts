// Ported from the phenology/season-chart system, build_site.py:991-1157,
// 2816-3125. This is the tree page's year calendar: a species-level curve
// of "how much there is to see," shifted by latitude, with the tree's own
// best_time marked as a peak. The most intricate piece of the site to port,
// so every constant and function below matches its Python source 1:1.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";
import { speciesCommon } from "./species";
import type { Tree } from "./trees";

function esc(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

export const MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

// The season story left the public site on 2026-08-26 (DECISIONS.md: "the
// whole season story is Plus, the fact included"). Nothing below is deleted:
// the data, the curves and the feed all stay, because the app's Plus is where
// they resurface. This switch only silences what the WEB renders; flipping it
// back is a decision recorded there, not a code cleanup.
export const SEASON_PUBLIC = false;

export const KIND_ICONS: Record<string, string> = {
  "bare silhouette":
    '<svg viewBox="0 0 20 20" fill="none" stroke="#8C8577" stroke-width="1.6" stroke-linecap="round"><path d="M10 18V9"/><path d="M10 11 6 6M10 11l4-5M10 8 7.5 3.5M10 8l2.5-4.5"/></svg>',
  flowers:
    '<svg viewBox="0 0 20 20" aria-hidden="true"><g fill="#E8705F"><ellipse cx="10" cy="4.6" rx="2.6" ry="3.2"/><ellipse cx="15.4" cy="10" rx="3.2" ry="2.6"/><ellipse cx="10" cy="15.4" rx="2.6" ry="3.2"/><ellipse cx="4.6" cy="10" rx="3.2" ry="2.6"/></g><circle cx="10" cy="10" r="2.1" fill="#fff"/></svg>',
  fruit:
    '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="11.6" r="6" fill="#E8A33D"/><path d="M10 5.8 Q10.2 3.4 12.6 2.6" stroke="#7FA653" stroke-width="1.6" fill="none" stroke-linecap="round"/><ellipse cx="13.4" cy="3.4" rx="2.2" ry="1.3" fill="#7FA653" transform="rotate(-24 13.4 3.4)"/><circle cx="8" cy="10" r="1.1" fill="#fff" opacity=".55"/></svg>',
  "autumn colour":
    '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 2 C14.5 5 17 9 17 12.5 A7 7 0 0 1 3 12.5 C3 9 5.5 5 10 2z" fill="#D97843"/><path d="M10 5.5 v11" stroke="#fff" stroke-width="1.2" opacity=".7"/></svg>',
  catkins:
    '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 4 q3 -1.6 6 -1.6 q3.6 0 6 1.6" stroke="#7FA653" stroke-width="1.6" fill="none" stroke-linecap="round"/><g stroke="#C9B458" stroke-width="2.4" stroke-linecap="round"><path d="M6 5 q-.4 4.4 .5 7.6"/><path d="M10 4.6 q0 5.4 .9 9.6"/><path d="M14 5 q.4 3.8 -.3 7"/></g></svg>',
  "fresh leaves":
    '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M16.5 3.5 C10 3.5 5.5 7.5 5 14 c6 .6 10.5 -3 11.5 -10.5z" fill="#7FA653"/><path d="M5.5 16.5 C7.5 12 11.5 8 16 5.5" stroke="#4A6B2A" stroke-width="1.4" fill="none" stroke-linecap="round"/></svg>',
};

const KIND_ALIASES: Record<string, string> = {
  flowering: "flowers",
  blossom: "flowers",
  bloom: "flowers",
  autumn: "autumn colour",
  "fall color": "autumn colour",
  "fall colour": "autumn colour",
  "autumn color": "autumn colour",
};

const KIND_HINTS: [string, string[]][] = [
  ["catkins", ["catkin"]],
  ["flowers", ["flower", "blossom", "bloom", "wisteria"]],
  ["autumn colour", ["autumn", "gold", "golden", "scarlet", "crimson", "turns", "fall colour", "fall color"]],
  ["fruit", ["fruit", "berries", "acorn", "fig ripen", "chestnut drop"]],
  ["fresh leaves", ["fresh leaves", "new leaves", "leaf-out", "unfurl"]],
];

interface BestTime {
  months?: number[];
  label?: string;
  kind?: string;
}

/** Canonical phenology kind for a best_time, or '' when honestly unknown. */
export function seasonKind(bt: BestTime): string {
  let raw = (bt.kind ?? "").trim().toLowerCase();
  if (raw) {
    raw = KIND_ALIASES[raw] ?? raw;
    if (raw in KIND_ICONS) return raw;
    return "";
  }
  const label = (bt.label ?? "").toLowerCase();
  const hits = KIND_HINTS.filter(([, words]) => words.some((w) => label.includes(w)));
  return hits.length === 1 ? hits[0][0] : "";
}

type Pt = [number, number];

/** A rounded SVG path through the points, Catmull-Rom turned into cubics. */
export function smoothPath(points: Pt[]): string {
  if (points.length < 2) return "";
  let d = `M ${points[0][0].toFixed(1)},${points[0][1].toFixed(1)}`;
  for (let i = 0; i < points.length - 1; i++) {
    const p0 = i > 0 ? points[i - 1] : points[i];
    const p1 = points[i];
    const p2 = points[i + 1];
    const p3 = i + 2 < points.length ? points[i + 2] : p2;
    const c1x = p1[0] + (p2[0] - p0[0]) / 6;
    const c1y = p1[1] + (p2[1] - p0[1]) / 6;
    const c2x = p2[0] - (p3[0] - p1[0]) / 6;
    const c2y = p2[1] - (p3[1] - p1[1]) / 6;
    d += ` C ${c1x.toFixed(1)},${c1y.toFixed(1)} ${c2x.toFixed(1)},${c2y.toFixed(1)} ${p2[0].toFixed(1)},${p2[1].toFixed(1)}`;
  }
  return d;
}

/** A 0..1 value for each of the 12 months, humped over the peak(s). */
function seasonIntensities(peakMonths: number[]): number[] {
  const sigma = 1.4;
  const out: number[] = [];
  for (let m = 1; m <= 12; m++) {
    const dist = Math.min(...peakMonths.map((p) => Math.abs(m - p)));
    out.push(Math.exp(-(dist * dist) / (2 * sigma * sigma)));
  }
  return out;
}

/** A seasonal-peak chart for trees whose species has no phenology file:
 * best_time only, in the spirit of PictureThis. */
export function seasonCurve(tree: Tree): string {
  const bt = tree.best_time;
  if (!bt || !bt.label || !bt.months || bt.months.length === 0) return "";

  const peaks = bt.months;
  const vals = seasonIntensities(peaks);
  const now = new Date().getMonth() + 1;
  const inSeason = peaks.includes(now);

  const W = 320.0,
    H = 120.0,
    padT = 22.0,
    padB = 24.0,
    padX = 10.0;
  const plotH = H - padT - padB;
  const step = (W - 2 * padX) / 11.0;
  const pts: Pt[] = vals.map((v, i) => [padX + i * step, padT + (1 - v) * plotH]);

  const line = smoothPath(pts);
  const area = `${line} L ${pts[pts.length - 1][0].toFixed(1)},${(padT + plotH).toFixed(1)} L ${pts[0][0].toFixed(1)},${(padT + plotH).toFixed(1)} Z`;

  let peakI = 0;
  for (let i = 1; i < 12; i++) if (vals[i] > vals[peakI]) peakI = i;
  const [peakX, peakY] = pts[peakI];
  const nowX = pts[now - 1][0];

  const ticks = pts.map(([x], i) => `<text x="${x.toFixed(1)}" y="${(H - 6).toFixed(0)}" class="sc-m">${MONTH_ABBR[i]}</text>`).join("");
  const grid = [0.25, 0.5, 0.75]
    .map((f) => `<line x1="${padX.toFixed(1)}" y1="${(padT + plotH * f).toFixed(1)}" x2="${(W - padX).toFixed(1)}" y2="${(padT + plotH * f).toFixed(1)}" class="sc-grid"/>`)
    .join("");

  const nowMarker =
    `<line x1="${nowX.toFixed(1)}" y1="${(padT - 6).toFixed(1)}" x2="${nowX.toFixed(1)}" y2="${(padT + plotH).toFixed(1)}" class="sc-now"/>` +
    `<text x="${nowX.toFixed(1)}" y="${(padT - 10).toFixed(1)}" class="sc-nowlabel">now</text>`;

  const kind = seasonKind(bt);
  const chip = kind ? `<span class="sc-chip">${KIND_ICONS[kind]}${esc(kind)}</span>` : "";
  let peakBadge = "";
  if (kind) {
    const bx = (peakX / W) * 100;
    const by = (peakY / H) * 100;
    peakBadge = `<span class="sc-peakbadge" style="left:${bx.toFixed(1)}%;top:${by.toFixed(1)}%">${KIND_ICONS[kind]}</span>`;
  }
  const nowBadge = inSeason ? '<span class="best-now">at its best right now</span>' : "";

  return `
<figure class="season">
  <figcaption class="season-head">
    <span>Best time to visit</span>${nowBadge}
  </figcaption>
  <div class="season-plot">
  ${peakBadge}
  <svg viewBox="0 0 ${W.toFixed(0)} ${H.toFixed(0)}" class="season-svg" role="img" aria-label="Seasonal peak: ${esc(bt.label)}">
    ${grid}
    <path d="${area}" class="sc-area"/>
    <path d="${line}" class="sc-line"/>
    ${nowMarker}
    <circle cx="${peakX.toFixed(1)}" cy="${peakY.toFixed(1)}" r="4.5" class="sc-peak"/>
    ${ticks}
  </svg>
  </div>
  <p class="season-legend">${chip}</p>
  <p class="season-label">${esc(bt.label)}</p>
</figure>`;
}

/** One short phrase for the city-page card. */
export function bestTimeShort(tree: Tree): string {
  if (!SEASON_PUBLIC) return "";
  const bt = tree.best_time;
  if (!bt || !bt.label) return "";
  const now = new Date().getMonth() + 1;
  if ((bt.months ?? []).includes(now)) {
    return ' &middot; <span class="best-now-inline">at its best now</span>';
  }
  return "";
}

// ---------------------------------------------------------- species curves

const INTENSITY_WEIGHTS: Record<string, number> = { unseen: 0.0, nice: 0.18, striking: 0.35, "worth the trip": 0.55 };
const BASE_BARE = 0.08,
  BASE_TURN = 0.22,
  BASE_LEAF = 0.38,
  FRESH_LEAF_BONUS = 0.15;
const SHOULDER = 0.4;

interface PhenologyEntry {
  common_name: string;
  leaf?: number[];
  bare?: number[];
  flowers?: number[];
  fruit?: number[];
  colour?: number[];
  intensity?: Record<string, string>;
  flower_label?: string;
  fruit_label?: string;
  colour_label?: string;
  peak?: PhenologyPeak;
  flower_colour?: string;
  /** The single month the MAP lights up, against `flowers`, which is the wider
   * band the season chart draws. Almost every tree flowers for one to three
   * weeks while the band spans two months, so a pin that followed the band
   * would claim sixty-one days for a display of ten (Hidde, 2026-08-21:
   * "bloeien bomen uberhaupt een hele maand?"). Which weeks it is cannot be
   * known: that moves with the year and the place. Which month is likeliest
   * can be, and it rides the same latitude shift as everything else. */
  flower_peak?: number;
  /** How long the display actually lasts, for the reader rather than the map. */
  flower_days?: string;
}

/** The one moment of the year this species is worth a trip for, and what the
 * map should do about it. Only written where `intensity` already rates that
 * moment "worth the trip"; scripts/preflight.py refuses any other. */
export interface PhenologyPeak {
  moment: string;
  months: number[];
  share?: boolean;
  map?: { effect: string; colour: string; pulse?: boolean };
  surfaces?: string[];
  /** Only set on a derived blossom, so the pin can be quieter for a flowering
   * that is merely nice than for one worth crossing town for. */
  level?: string;
}

let cachedPhenology: Map<string, PhenologyEntry> | null = null;

export function loadPhenology(): Map<string, PhenologyEntry> {
  if (cachedPhenology) return cachedPhenology;
  const dir = path.join(DATA, "phenology");
  const out = new Map<string, PhenologyEntry>();
  if (fs.existsSync(dir)) {
    for (const f of fs.readdirSync(dir).sort()) {
      if (!f.endsWith(".json")) continue;
      const e: PhenologyEntry = JSON.parse(fs.readFileSync(path.join(dir, f), "utf-8"));
      out.set(e.common_name, e);
    }
  }
  cachedPhenology = out;
  return out;
}

function shift(months: number[], delta: number): number[] {
  return [...new Set(months.map((m) => (((m - 1 + delta) % 12) + 12) % 12 + 1))].sort((a, b) => a - b);
}

/** The middle month of a phase, handling one that wraps the new year. */
function phaseMid(months: number[]): number | null {
  if (months.length === 0) return null;
  let run = [...months].sort((a, b) => a - b);
  if (run.includes(12) && run.includes(1)) {
    run = run.map((m) => (((m + 5) % 12) + 1)).sort((a, b) => a - b);
    return (((run[Math.floor(run.length / 2)] + 6) % 12) + 1);
  }
  return run[Math.floor(run.length / 2)];
}

export interface Moment {
  kind: string;
  word: string;
  month: number | null;
  label?: string;
}

/** Twelve values for how much there is to see, and the moments behind them.
 * Not normalised per species: an uneventful tree stays low all year. */
export function highlightCurve(ph: PhenologyEntry): [number[], Moment[]] {
  const leaf = new Set(ph.leaf ?? []);
  const bare = new Set(ph.bare ?? []);
  const inten = ph.intensity ?? {};

  const vals: number[] = [];
  for (let m = 1; m <= 12; m++) {
    vals.push(bare.has(m) ? BASE_BARE : leaf.has(m) ? BASE_LEAF : BASE_TURN);
  }
  // The spring flush is a real moment recorded nowhere in the data.
  for (let m = 1; m <= 12; m++) {
    if (leaf.has(m) && bare.has((((m - 2) % 12) + 12) % 12 + 1)) {
      vals[m - 1] += FRESH_LEAF_BONUS;
    }
  }

  const moments: Moment[] = [];
  const specs: [string, string, keyof PhenologyEntry, "flower_label" | "fruit_label" | "colour_label"][] = [
    ["flowers", "flowers", "flowers", "flower_label"],
    ["fruit", "fruit", "fruit", "fruit_label"],
    ["colour", "autumn colour", "colour", "colour_label"],
  ];
  for (const [key, kind, monthsKey, labelKey] of specs) {
    let word = String(inten[key as string] ?? "nice").trim().toLowerCase();
    if (!(word in INTENSITY_WEIGHTS)) word = "nice";
    const weight = INTENSITY_WEIGHTS[word];
    const months = (ph[monthsKey] as number[] | undefined) ?? [];
    if (months.length === 0 || !weight) continue;
    const span = new Set(months);
    for (const m of months) {
      vals[m - 1] += weight;
      for (const n of [(((m - 2) % 12) + 12) % 12 + 1, (m % 12) + 1]) {
        if (!span.has(n)) vals[n - 1] += weight * SHOULDER;
      }
    }
    moments.push({ kind, word, month: phaseMid(months), label: ph[labelKey] });
  }

  return [vals.map((v) => Math.min(1.0, v)), moments];
}

/** The species calendar, shifted for where the tree actually stands. */
export function phenologyFor(tree: Tree, lat: number): PhenologyEntry | null {
  const e = loadPhenology().get(speciesCommon(tree));
  if (!e || Math.abs(lat) < 25) return null;
  // The tropics guard above already used Math.abs; this line did not, and that
  // was the bug (found 2026-08-15 by the Melbourne write pass, live on Hobart
  // since it shipped). Every phenology file is written for the northern year,
  // so a southern tree needs the whole calendar moved half a year, not the
  // one-month warm-climate nudge. Melbourne at -37.8 was reading as a warm
  // NORTHERN city and drawing a curve six months out: bare in July, when a
  // Melbourne elm is in full leaf. A wrong calendar is worse than none, which
  // is exactly why the tropics print nothing at all.
  const away = Math.abs(lat);
  const delta = (lat < 0 ? 6 : 0) + (away < 42 ? -1 : away > 56 ? 1 : 0);
  const out: PhenologyEntry = { ...e };
  for (const k of ["leaf", "flowers", "fruit", "colour", "bare"] as const) {
    const v = e[k];
    if (v && v.length < 12) (out as any)[k] = shift(v, delta);
  }
  // The peak rides the same shift, and forgetting it would be the worse bug of
  // the two: a chart six months out is wrong on a page nobody scrolls to, while
  // a map that lights every ginkgo gold in a Melbourne November is wrong in the
  // one place the whole feature lives. Melbourne's ginkgos turn in May.
  if (e.peak?.months?.length) {
    out.peak = { ...e.peak, months: shift(e.peak.months, delta) };
  }
  if (e.flower_peak) out.flower_peak = shift([e.flower_peak], delta)[0];
  return out;
}

/** What this tree's pin should do, if anything, and when. Null for a species
 * with no peak, and for anything inside the tropics, where phenologyFor
 * already refuses to guess a calendar. */
export function peakFor(tree: Tree, lat: number): PhenologyPeak | null {
  const e = phenologyFor(tree, lat);
  if (!e) return null;
  // The curated moment first: one per species, the thing that species is worth
  // a trip for. Colour, fruit, catkins.
  if (e.peak?.map) return e.peak;
  // Then blossom, which is not curated at all. Hidde, 2026-08-21: "alle bomen
  // die bloeien mogen de animatie van bloei in de kleur van hun bloei, op hun
  // moment." So a flowering species blooms on the map in its own colour, and
  // the only disqualification is that nobody can see it. A plane flowers every
  // April and no one has ever noticed; that is what intensity 'unseen' records.
  const level = e.intensity?.flowers;
  if (e.flower_colour && e.flowers?.length && level && level !== "unseen") {
    return {
      moment: "flowers",
      months: e.flower_peak ? [e.flower_peak] : e.flowers,
      share: level === "worth the trip",
      map: { effect: "blossom", colour: e.flower_colour, pulse: true },
      // A subtle flowering whispers rather than announces. The pin reads the
      // level and dials the halo and the petal count down for 'nice'.
      surfaces: level === "nice" ? ["map"] : ["map", "tree", "city"],
      level,
    };
  }
  return null;
}

/** The year as one chart: how much there is to see, month by month. Falls
 * back to the best_time-only curve when the species has no phenology file. */
export function seasonBlock(tree: Tree, lat: number): string {
  if (!SEASON_PUBLIC) return "";
  const ph = phenologyFor(tree, lat);
  const bt = tree.best_time ?? {};
  const hasBt = Boolean(bt.label && bt.months && bt.months.length > 0);

  if (!ph || !((ph.leaf && ph.leaf.length) || (ph.bare && ph.bare.length))) {
    return hasBt ? seasonCurve(tree) : "";
  }

  const [vals, moments] = highlightCurve(ph);
  if (Math.max(...vals) - Math.min(...vals) < 0.02) {
    if (hasBt) return seasonCurve(tree);
    return '<p class="ph-foot ph-noseason">This tree looks much the same in every month of the year, so there is no season to chart.</p>';
  }

  const now = new Date().getMonth() + 1;
  const peakM = hasBt ? phaseMid(bt.months ?? []) : null;
  const inSeason = hasBt && (bt.months ?? []).includes(now);

  const W = 320.0,
    H = 128.0,
    padT = 30.0,
    padB = 24.0,
    padX = 10.0;
  const plotH = H - padT - padB;
  const step = (W - 2 * padX) / 11.0;
  const pts: Pt[] = vals.map((v, i) => [padX + i * step, padT + (1 - v) * plotH]);
  const line = smoothPath(pts);
  const area = `${line} L ${pts[pts.length - 1][0].toFixed(1)},${(padT + plotH).toFixed(1)} L ${pts[0][0].toFixed(1)},${(padT + plotH).toFixed(1)} Z`;

  const grid = [0.25, 0.5, 0.75]
    .map((f) => `<line x1="${padX.toFixed(1)}" y1="${(padT + plotH * f).toFixed(1)}" x2="${(W - padX).toFixed(1)}" y2="${(padT + plotH * f).toFixed(1)}" class="sc-grid"/>`)
    .join("");
  const ticks = pts.map(([x], i) => `<text x="${x.toFixed(1)}" y="${(H - 6).toFixed(0)}" class="sc-m">${MONTH_ABBR[i]}</text>`).join("");
  const nowX = pts[now - 1][0];
  const nowMarker =
    `<line x1="${nowX.toFixed(1)}" y1="${(padT - 6).toFixed(1)}" x2="${nowX.toFixed(1)}" y2="${(padT + plotH).toFixed(1)}" class="sc-now"/>` +
    `<text x="${nowX.toFixed(1)}" y="${(padT - 10).toFixed(1)}" class="sc-nowlabel">now</text>`;

  function badge(month: number, kind: string): string {
    const [x, y] = pts[month - 1];
    return `<span class="sc-peakbadge" style="left:${((x / W) * 100).toFixed(1)}%;top:${((y / H) * 100).toFixed(1)}%">${KIND_ICONS[kind]}</span>`;
  }

  const badges: string[] = [];
  let peakDot = "";
  const kind = hasBt ? seasonKind(bt) : "";
  if (peakM) {
    const [px, py] = pts[peakM - 1];
    peakDot = `<circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="4.5" class="sc-peak"/>`;
    if (kind) badges.push(badge(peakM, kind));
  }
  for (const mo of moments) {
    if ((mo.word === "striking" || mo.word === "worth the trip") && mo.month !== peakM && mo.month !== null) {
      badges.push(badge(mo.month, mo.kind));
    }
  }

  const keys = moments.map((mo) => `<span class="ph-key">${KIND_ICONS[mo.kind]}${esc(mo.label || mo.kind.charAt(0).toUpperCase() + mo.kind.slice(1))}</span>`).join("");
  const nowBadge = inSeason ? '<span class="best-now">at its best right now</span>' : "";
  const labelLine = hasBt ? `<p class="season-label">${esc(bt.label!)}</p>` : "";

  return `
  <figure class="season phenology">
    <figcaption class="season-head"><span>The tree's year</span>${nowBadge}</figcaption>
    <div class="season-plot">
    ${badges.join("")}
    <svg viewBox="0 0 ${W.toFixed(0)} ${H.toFixed(0)}" class="season-svg" role="img" aria-label="How much there is to see through the year">
      ${grid}
      <path d="${area}" class="sc-area"/>
      <path d="${line}" class="sc-line"/>
      ${nowMarker}
      ${peakDot}
      ${ticks}
    </svg>
    </div>
    <p class="ph-keys">${keys}</p>
    ${labelLine}
    <p class="ph-foot">The line is our estimate of how much there is to see, not a measurement. Typical for this species where this tree stands; exact weeks shift with the year.</p>
  </figure>`;
}

/** The ratchet check (CLAUDE.md QA layer 1): a species that records real
 * moments and still draws a flat curve is a scoring bug, so the build stops. */
export function checkPhenology(): void {
  const errors: string[] = [];
  const entries = [...loadPhenology().entries()].sort(([a], [b]) => a.localeCompare(b));
  for (const [name, e] of entries) {
    const events = (["flowers", "fruit", "colour"] as const).reduce((s, k) => s + (e[k]?.length ?? 0), 0);
    const [vals] = highlightCurve(e);
    if (events && Math.max(...vals) - Math.min(...vals) < 0.02) {
      errors.push(`phenology ${name}: records ${events} seasonal month(s) but the curve is flat, so the chart would say nothing`);
    }
  }
  if (errors.length) throw new Error(errors.join("\n"));
}
