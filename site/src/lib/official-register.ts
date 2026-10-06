import fs from "node:fs";
import path from "node:path";
// THE OFFICIAL REGISTER A TREE IS LISTED IN, decided once (2026-10-06).
//
// Hidde, on Google's guidance after the 09-28 demotion: a page should carry
// what no AI can make up, and an official register entry is the plainest such
// fact we hold. It sat at the foot of the page as one host name in a source
// list, so nobody saw that a government had designated the tree. This names it
// in the fact card instead.
//
// Convention: Wikipedia's infobox and iNaturalist's observation page both put
// an official designation beside the facts as a labelled row, linked out to the
// authority's own record. Nobody invents a badge for it, and neither do we.
//
// An ANSWER, not a rule (CLAUDE.md, 2026-08-25): the feed carries the result as
// `register`, so the app draws the same row without re-deciding it.
//
// Two kinds of evidence, both already in verified_sources:
// - a URL that is the authority's PER-TREE record (a pattern below). A link to
//   a WFS endpoint, a GeoJSON dump or a register's homepage is not a record a
//   reader can open, so it does not count and gets no link.
// - a citation naming one of our imported registers (data/registers/*.json),
//   which names the register without a link, because inventing one would be
//   worse than not having it.

export interface OfficialRegister {
  name: string;
  url: string | null;
}

const RECORD_PAGES: [RegExp, string][] = [
  [/online\.bunka\.go\.jp\/.*detail\//, "文化遺産オンライン (Agency for Cultural Affairs)"],
  [/kunishitei\.bunka\.go\.jp\/heritage\/detail\//, "国指定文化財等データベース (Agency for Cultural Affairs)"],
  [/kyoju\.biodic\.go\.jp\/.*gtsearchdetail/, "巨樹・巨木林データベース (Ministry of the Environment)"],
  [/crfop\.gdos\.gov\.pl\/.*viewpomnikprzyrody/, "Centralny Rejestr Form Ochrony Przyrody (GDOŚ)"],
  [/inventaris\.onroerenderfgoed\.be\/erfgoedobjecten\//, "Inventaris Onroerend Erfgoed"],
  [/heritagetrees\.nparks\.gov\.sg\/ht-/, "NParks Heritage Trees"],
  [/comune\.milano\.it\/.*\/alberi-monumentali\//, "Alberi monumentali, Comune di Milano"],
  [/mediambient\.gencat\.cat\/.*arbres-monumentals\//, "Arbres monumentals de Catalunya"],
  [/heritage\.go\.kr\/heri\/cul\/culSelectDetail/, "국가유산청 (Korea Heritage Service)"],
  [/drusop\.nature\.cz\/.*pstromy/, "Ústřední seznam ochrany přírody (AOPK ČR)"],
  [/nycgovparks\.org\/.*great-trees/, "NYC Parks Great Trees"],
  [/barcelona\.cat\/.*(trees-of-local-interest|arboles-de-interes-local|arbres-d-interes-local)/, "Arbres d'interès local, Ajuntament de Barcelona"],
  [/geneve\.ch\/.*arbres-particuliers\//, "Arbres remarquables, Ville de Genève"],
];

// A register's own name, short enough for one row: "MASAF, Elenco degli alberi
// monumentali d'Italia (Italy's national ...)" keeps the part before the
// English gloss.
let NAMES: Map<string, string> | null = null;
function registerNames(): Map<string, string> {
  if (NAMES) return NAMES;
  NAMES = new Map();
  try {
    const dir = path.join(process.cwd(), "../data/registers");
    for (const f of fs.readdirSync(dir)) {
      if (!f.endsWith(".json")) continue;
      try {
        const d = JSON.parse(fs.readFileSync(path.join(dir, f), "utf-8"));
        let name = typeof d.source === "string" ? d.source : (d.source?.name ?? "");
        name = String(name).split(/\s\(|[.;]\s|: /)[0].trim();
        if (name.length > 80) name = name.slice(0, 79).trimEnd() + "…";
        if (name) NAMES.set(f.replace(/\.json$/, ""), name);
      } catch { /* a register without a source names nothing */ }
    }
  } catch { /* no registers directory */ }
  return NAMES;
}

export function officialRegister(tree: { verified_sources?: string[]; official_register?: { name?: string; url?: string } }): OfficialRegister | null {
  // Set by an enrichment pass (scripts/enrich.py) that opened the authority's
  // own record for this tree: it wins, because a person checked it.
  const own = tree.official_register;
  if (own?.name) return { name: String(own.name), url: own.url && /^https?:\/\//.test(own.url) ? own.url : null };
  const src = (tree.verified_sources ?? []).map((s) => String(s ?? "").trim()).filter(Boolean);
  for (const s of src) {
    if (!/^https?:\/\//i.test(s)) continue;
    const url = s.split(/\s/)[0];
    for (const [re, name] of RECORD_PAGES) if (re.test(url)) return { name, url };
  }
  const names = registerNames();
  for (const s of src) {
    if (/^https?:\/\//i.test(s)) continue;
    for (const [slug, name] of names) {
      if (new RegExp(`(^|[\\s/(])${slug}(\\.json)?(?=[\\s,()]|$)`).test(s)) return { name, url: null };
    }
  }
  return null;
}
