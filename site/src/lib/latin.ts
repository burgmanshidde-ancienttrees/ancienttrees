// SCIENTIFIC NAMES IN ITALICS, wherever a reader meets one (2026-10-12).
//
// Asked for by the Director of the National Botanic Gardens of Ireland, reading
// our Dublin page: "On an editorial note please put the latin names in
// Italics." It is the botanical convention, and it is how iNaturalist and every
// herbarium print a name: genus and epithet italic; the hybrid sign, the rank
// words (sp., var., subsp., f.) and a cultivar in quotes stay upright.
//
// A name sits in three kinds of text: the species field ("European Yew (Taxus
// baccata)"), a species intro's scientific_name, and the story prose, which is
// plain text in data/cities and in every overlay language. So this does not
// edit data. It finds names at render time, and it only finds names it KNOWS:
// a genus and an epithet that our own species fields and species intros
// already use. "London plane" is a capitalised word and a lowercase one, and
// it is not Latin; a pattern alone would have italicised it.
//
// The app gets the same answer, not the same rule: app-feed.ts sends the
// italic runs of each story as UTF-16 ranges (latinRanges), so the two
// surfaces cannot disagree about what is Latin.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

// Words the harvest below would take for Latin, found by reading what it took
// from every species field on 2026-10-12. A handful of brackets carry English
// ("English landscape park", "Ginkgo and Giant Sequoia", "likely Pedunculate
// Oak, Quercus robur"), and a capitalised word before a comma or a cultivar
// looks like a lone genus.
const NOT_GENERA = new Set(["English", "Napoleonic", "Mediterranean", "Croix", "Rousse", "Noda",
  "Elm", "Group", "Lime", "Linden", "Oak", "Pelt", "Poplar", "Tristis", "Sato", "Zakura", "Giant", "Van"]);
const NOT_EPITHETS = new Set(["and", "or", "per", "with", "the", "identifies", "likely", "presumed",
  "possibly", "weeping", "form", "species", "listed", "recorded"]);

// Words that sit inside a name and stay upright.
const RANKS = ["subsp.", "ssp.", "var.", "f.", "sp.", "spp.", "cv.", "syn."];

interface Lexicon { genera: Set<string>; epithets: Set<string>; re: RegExp }
let lexicon: Lexicon | null = null;

function harvest(sci: string, genera: Set<string>, epithets: Set<string>): void {
  // Every "Genus epithet" (or "Genus x epithet") pair in a bracket's text, and
  // every bare "Genus sp." / "Genus 'Cultivar'".
  const pair = /(?:^|[\s(,;/])([A-Z][a-z]{2,})\s+(?:[x×]\s+)?([a-z][a-z-]{2,})\b/g;
  for (const m of sci.matchAll(pair)) {
    if (NOT_GENERA.has(m[1]) || NOT_EPITHETS.has(m[2])) continue;
    genera.add(m[1]);
    epithets.add(m[2]);
  }
  const bare = /(?:^|[\s(,;/+])([A-Z][a-z]{2,})(?=\s+(?:sp\.|spp\.|[x×]\s|['"‘“])|\s*$|,)/g;
  for (const m of sci.matchAll(bare)) if (!NOT_GENERA.has(m[1])) genera.add(m[1]);
  // A hybrid's second parent written without its genus: "Tilia platyphyllos x
  // euchlora", "Cedrus libani x deodara".
  for (const m of sci.matchAll(/\s[x×]\s+([a-z][a-z-]{2,})\b/g)) epithets.add(m[1]);
  // The epithet after a rank word is Latin by construction.
  for (const m of sci.matchAll(/\b(?:subsp|ssp|var|f)\.\s+([a-z][a-z-]{2,})\b/g)) epithets.add(m[1]);
}

/** The bracketed half of a species field: "European Yew (Taxus baccata)" ->
 * "Taxus baccata". Both bracket shapes, as the Japanese overlays use （ ）. */
export function bracketed(species: string): string | null {
  const m = /[(（]([^)）]+)[)）]/.exec(species ?? "");
  return m ? m[1].trim() : null;
}

function load(): Lexicon {
  if (lexicon) return lexicon;
  const names: string[] = [];
  const citiesDir = path.join(DATA, "cities");
  for (const f of fs.readdirSync(citiesDir)) {
    if (!f.endsWith(".json")) continue;
    const doc = JSON.parse(fs.readFileSync(path.join(citiesDir, f), "utf-8"));
    for (const t of doc.trees ?? []) {
      const b = bracketed(t.species ?? "");
      if (b) names.push(b);
    }
  }
  const speciesDir = path.join(DATA, "species");
  for (const f of fs.readdirSync(speciesDir)) {
    if (!f.endsWith(".json")) continue;
    const doc = JSON.parse(fs.readFileSync(path.join(speciesDir, f), "utf-8"));
    if (doc.scientific_name) names.push(doc.scientific_name);
  }
  lexicon = buildLexicon(names);
  return lexicon;
}

/** The detector, from the scientific names we already hold. */
export function buildLexicon(names: string[]): Lexicon {
  const genera = new Set<string>();
  const epithets = new Set<string>();
  for (const n of names) harvest(n, genera, epithets);

  const alt = (s: Set<string>) => [...s].sort((a, b) => b.length - a.length).join("|");
  const G = `(?:${alt(genera)})`;
  const E = `(?:${alt(epithets)})`;
  const X = `\\s+[x\\u00d7]\\s+`;
  const RANK = `\\s+(?:subsp|ssp|var|f)\\.\\s+[a-z][a-z-]{2,}`;
  // In order of preference, longest shape first:
  //   Genus [x] epithet [x [Genus] epithet] [rank epithet]
  //   P. epithet                       (an abbreviated genus, "P. spachiana")
  //   Genus sp. / spp.
  //   Genus 'Cultivar'                 (the genus alone is italic)
  //   genus Genus                      (prose naming a genus as one)
  const name =
    `${G}(?:${X}|\\s+)${E}(?:${X}(?:${G}\\s+)?${E})?(?:${RANK})?` +
    `|\\b[A-Z]\\.\\s${E}(?:${RANK})?` +
    `|${G}\\s+spp?\\.` +
    `|${G}(?=\\s+['"\\u2018\\u201c])` +
    `|(?<=\\bgenus\\s)${G}`;
  // Word boundaries by hand: \b is ASCII-only and "Croix-Rousse" must not
  // offer "Rousse" as a genus.
  const re = new RegExp(`(?<![\\p{L}\\-])(?:${name})(?![\\p{L}])`, "gu");
  return { genera, epithets, re };
}

function esc(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

/** The italic runs inside one matched name, as [start, end) offsets relative
 * to the match: every word except the hybrid sign and the rank words. */
function runsIn(name: string): [number, number][] {
  const out: [number, number][] = [];
  let open = -1, last = -1;
  for (const m of name.matchAll(/\S+/g)) {
    const w = m[0];
    const upright = w === "x" || w === "×" || RANKS.includes(w);
    if (upright) {
      if (open >= 0) { out.push([open, last]); open = -1; }
    } else {
      if (open < 0) open = m.index!;
      last = m.index! + w.length;
    }
  }
  if (open >= 0) out.push([open, last]);
  return out;
}

/** Italic runs in `text` as [start, end) UTF-16 offsets, in order. */
export function latinRanges(text: string): [number, number][] {
  if (!text) return [];
  const { re } = load();
  const out: [number, number][] = [];
  re.lastIndex = 0;
  for (const m of text.matchAll(re)) {
    for (const [a, b] of runsIn(m[0])) out.push([m.index! + a, m.index! + b]);
  }
  return out;
}

/** `text` escaped for HTML, with every scientific name in it italic. */
export function latinHtml(text: string): string {
  if (!text) return "";
  let html = "", at = 0;
  for (const [a, b] of latinRanges(text)) {
    html += esc(text.slice(at, a)) + `<i lang="la">${esc(text.slice(a, b))}</i>`;
    at = b;
  }
  return html + esc(text.slice(at));
}

/** A scientific name on its own (a species intro's scientific_name, the
 * bracket of a species field): every word italic but the upright ones and a
 * cultivar in quotes, even where the lexicon has never seen the genus. */
export function sciNameHtml(sci: string): string {
  if (!sci) return "";
  const parts: { s: string; it: boolean }[] = [];
  for (const m of sci.matchAll(/['"\u2018\u201c][^'"\u2019\u201d]*['"\u2019\u201d]|\s+|[^\s]+/g)) {
    const w = m[0];
    const it = !/^\s/.test(w) && !/^['"\u2018\u201c]/.test(w)
      && w !== "x" && w !== "\u00d7" && !RANKS.includes(w);
    parts.push({ s: w, it });
  }
  // Join neighbouring italic words, and the spaces between them, into one run.
  let html = "";
  for (let i = 0; i < parts.length; i++) {
    if (!parts[i].it) { html += esc(parts[i].s); continue; }
    let run = parts[i].s;
    while (i + 2 < parts.length && /^\s+$/.test(parts[i + 1].s) && parts[i + 2].it) {
      run += parts[i + 1].s + parts[i + 2].s;
      i += 2;
    }
    html += `<i lang="la">${esc(run)}</i>`;
  }
  return html;
}
