// Translated-page infrastructure, built 2026-08-10 on Hidde's direction: a
// small Spanish test (Malaga, the one city with measured Spanish search
// demand: "árboles históricos de málaga", 20 impressions at position 74,
// zero clicks) inside a structure that scales to more languages if the test
// works. The long-term shape is the industry-standard one and nothing
// cleverer: language subdirectories (/es/malaga) plus reciprocal hreflang
// links, so Google serves the right language and never reads the pair as
// duplicate content. A translation is an OVERLAY on the English city file:
// data/i18n/<lang>/<slug>.json carries only the translated text, and every
// coordinate, photo, licence and walk stays in the one canonical city file,
// so a pin corrected in English is corrected everywhere.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";
import { BASE_URL } from "./schema";

export interface TreeTranslation {
  name: string;
  species: string;
  age_estimate: string;
  access: string;
  transport: string;
  story: string;
}

export interface CityTranslation {
  city: string;
  title: string;
  meta_description: string;
  intro: string;
  question_title: string;
  question_meta: string;
  question_answer: string;
  question_context: string;
  faq: { q: string; a: string }[];
  trees: Record<string, TreeTranslation>;
}

/** Language subdirectories under data/i18n that actually exist. */
export function translatedLanguages(): string[] {
  const dir = path.join(DATA, "i18n");
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter((d) => fs.statSync(path.join(dir, d)).isDirectory());
}

/** City slugs translated into `lang`. */
export function translatedCities(lang: string): string[] {
  const dir = path.join(DATA, "i18n", lang);
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter((f) => f.endsWith(".json")).map((f) => f.slice(0, -5));
}

export function cityTranslation(lang: string, slug: string): CityTranslation | null {
  const p = path.join(DATA, "i18n", lang, `${slug}.json`);
  if (!fs.existsSync(p)) return null;
  return JSON.parse(fs.readFileSync(p, "utf-8")) as CityTranslation;
}

/** The question page's slug per language. English pages live at
 * /{city}/oldest-tree; a translated question page takes the phrase people
 * actually search in that language rather than an English path segment. */
export const QUESTION_SLUG: Record<string, string> = {
  es: "arbol-mas-antiguo",
  it: "albero-piu-antico",
  nl: "oudste-boom",
  de: "aeltester-baum",
  pt: "arvore-mais-antiga",
  fr: "arbre-le-plus-vieux",
  ja: "saiko-rei-no-ki",
};

/** The visible "this page also exists in X" line, in the TARGET language.
 * It sits on the English page, so it has to read as an invitation to a
 * speaker of that language rather than as English telling them a translation
 * exists somewhere. */
export const LANG_INVITE: Record<string, string> = {
  es: "Esta página también está disponible",
  it: "Questa pagina è disponibile anche",
  nl: "Deze pagina is ook beschikbaar",
  de: "Diese Seite gibt es auch",
  pt: "Esta página também está disponível",
  fr: "Cette page est également disponible",
  ja: "このページは次の言語でもご覧いただけます",
};

/** The link text inside that line, also in the target language. */
export const LANG_NAME: Record<string, string> = {
  es: "en español",
  it: "in italiano",
  nl: "in het Nederlands",
  de: "auf Deutsch",
  pt: "em português",
  fr: "en français",
  ja: "日本語",
};

/** Reciprocal hreflang link tags for a page that exists in English and in
 * `lang`. x-default points at English, the language most of our audience
 * searches in. Both pages must emit the same pair, or Google ignores the
 * annotation entirely: hreflang is only honoured when it is reciprocal. */
export function hreflangLinks(lang: string, enPath: string, langPath: string): string {
  return [
    `<link rel="alternate" hreflang="en" href="${BASE_URL}${enPath}">`,
    `<link rel="alternate" hreflang="${lang}" href="${BASE_URL}${langPath}">`,
    `<link rel="alternate" hreflang="x-default" href="${BASE_URL}${enPath}">`,
  ].join("\n");
}
