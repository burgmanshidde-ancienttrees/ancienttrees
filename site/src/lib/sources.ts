// Every source the research leans on, read straight off the register files so
// the credits page cannot drift from what was actually imported.
//
// Why this exists (2026-09-03). Forty of the fifty-three registers in
// data/registers/ are published under a licence that obliges attribution, and
// the site named none of them anywhere. That is a debt we owed the moment the
// first one was imported, and the fix is the ordinary one: a credits page,
// generated rather than typed, so importing a register credits it.
//
// Registers do not share a shape and never will (see registers.ts, which makes
// the same point about entries). One is a Dutch municipal GeoJSON, one is a
// Japanese cultural-property CSV, one is a Portuguese WFS, and their wrapper
// keys differ accordingly. So every field here is read by fallback, and a
// register that records no licence at all is thrown rather than published
// silently: the whole point of the page is that the licence is stated.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

export interface SourceCredit {
  /** The register's own name for itself. */
  name: string;
  /** Who to credit, in their own words where they gave them. */
  attribution: string | null;
  /** The licence exactly as recorded at import time, never paraphrased. */
  licence: string;
  /** Where the data actually came from, so a reader can check us. */
  url: string | null;
  country: string;
  /** How many designated trees the file holds. */
  count: number;
  /** Whether that licence carries a share-alike condition, which changes what
   *  we may do with it rather than only what we must say. */
  shareAlike: boolean;
}

/** A handful of the earliest imports predate the wrapper convention and record
 *  no country. Filling it here rather than rewriting a 16,000-entry file for
 *  one key: the fix is cosmetic and the diff would not be. */
const COUNTRY_BY_FILE: Record<string, string> = {
  "amsterdam-bijzondere-bomen": "Netherlands",
  "netherlands-lrmb": "Netherlands",
  "portugal-icnf": "Portugal",
  "hongkong-ovt": "Hong Kong",
  "singapore-heritage-trees": "Singapore",
  "portland-heritage-trees": "United States",
  "massachusetts-dcr-legacy-trees": "United States",
  "quebec-city-arbres-remarquables": "Canada",
};

type Raw = Record<string, unknown>;

function str(v: unknown): string | null {
  return typeof v === "string" && v.trim() ? v.trim() : null;
}

function first(...vals: unknown[]): string | null {
  for (const v of vals) {
    const s = str(v);
    if (s) return s;
  }
  return null;
}

function countOf(d: Raw): number {
  for (const k of ["entries", "trees", "features"]) {
    const v = d[k];
    if (Array.isArray(v)) return v.length;
  }
  const n = d.count ?? d.record_count;
  return typeof n === "number" ? n : 0;
}

/** Share-alike is the one licence property that constrains what we may build,
 *  not merely what we must say, so it is detected rather than remembered. */
function isShareAlike(licence: string): boolean {
  const l = licence.toLowerCase();
  return l.includes("odbl") || l.includes("open database license") ||
    l.includes("-sa") || l.includes("sharealike") || l.includes("share-alike") ||
    l.includes("gelijkdelen");
}

export function sourceCredits(): SourceCredit[] {
  const dir = path.join(DATA, "registers");
  const out: SourceCredit[] = [];
  for (const file of fs.readdirSync(dir).filter((f) => f.endsWith(".json")).sort()) {
    const slug = file.slice(0, -5);
    const d = JSON.parse(fs.readFileSync(path.join(dir, file), "utf8")) as Raw;
    const nested = (typeof d.source === "object" && d.source ? d.source : {}) as Raw;
    const licence = first(d.licence, d.license, d.licence_name, nested.license, nested.licence);
    if (!licence) {
      throw new Error(
        `Register ${file} records no licence. Every register file carries its ` +
        `licence and the sentence proving it (CLAUDE.md, the register layer); ` +
        `a file without one cannot be credited and must not be imported.`,
      );
    }
    const name = first(d.source, nested.name, d.dataset_name, d.register, d.catalogue) ?? slug;
    out.push({
      name,
      attribution: first(d.attribution, nested.publisher, d.authority),
      licence,
      url: first(d.endpoint, d.source_url, d.metadata_url, d.dataset_catalog_url,
        nested.dataset_page, d.download_url, d.wfs),
      country: first(d.country, nested.country) ?? COUNTRY_BY_FILE[slug] ?? "Other",
      count: countOf(d),
      shareAlike: isShareAlike(licence),
    });
  }
  return out;
}

/** The credits grouped the way a reader scans them, by country, biggest first
 *  inside each. */
export function creditsByCountry(): { country: string; sources: SourceCredit[] }[] {
  const by = new Map<string, SourceCredit[]>();
  for (const c of sourceCredits()) {
    const list = by.get(c.country) ?? [];
    list.push(c);
    by.set(c.country, list);
  }
  return [...by.entries()]
    .map(([country, sources]) => ({
      country,
      sources: sources.sort((a, b) => b.count - a.count),
    }))
    .sort((a, b) => a.country.localeCompare(b.country));
}
