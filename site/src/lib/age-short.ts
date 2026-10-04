// THE AGE ON A CARD, short (Hidde, 2026-10-04: "ik zie vaak lange titels over
// de age long established blabla, kunnen we niet voor de simpelheid op deze
// drukke pagina een paar korte varianten bedenken").
//
// age_estimate is a sentence written for the tree page, with its hedge, its
// basis and its disagreement: "roughly 205 to 215 years, from the register's
// planting band of 1810 to 1820". A third of all trees carry one over 22
// characters, and on a list card it pushed the meta line to three lines. The
// app has answered this since 2026-08-21 in Swift (TreeCard.shortAge): the
// numbers where the data has them, the first clause otherwise. This is that
// rule moved to the server, where it belongs (CLAUDE.md, "a decision travels as
// data"): the website's cards print it and the feed sends it as `age_short`,
// so the app stops deciding it twice. The sentence is not dropped, it moved:
// the tree page one tap away prints it as written.
import type { UIStrings } from "./i18n";

/** Phrases that say nothing a visitor can use on a card. */
const NO_INFO = /^(age )?(undocumented|not |undated|unknown|uncertain|long-established|mature specimen|disputed)/i;
const HEDGES = ["estimated ", "roughly ", "approximately ", "around ", "about ", "over ", "at least ", "likely "];

export function ageShort(tree: any, U?: Pick<UIStrings, "ageYears">, lang = "en"): string | null {
  const years = (n: string) => (U ? U.ageYears(n) : `${n} years`);
  const lo = Number(tree?.age_min) || 0;
  const hi = Number(tree?.age_max) || 0;

  // 1. The figure the sentence itself opens with, after its hedge: "roughly
  //    2,000 years" is 2,000 on the card, not the 1500-2500 its bounds hold.
  //    English sentences only, because the hedge words are English.
  let t = lang === "en" ? String(tree?.age_estimate ?? "").trim() : "";
  for (const h of HEDGES) if (t.toLowerCase().startsWith(h)) { t = t.slice(h.length); break; }
  const said = t.match(/^(\d[\d,]*)(?:\s*(?:-|to)\s*(\d[\d,]*))?\s+years?\b/i);
  if (said) return years(said[2] ? `${said[1]}-${said[2]}` : said[1]);

  // 2. The bounds. A narrow band is one figure with a tilde, because "126-136
  //    years" is precision nobody needs on a card; a wide one stays a range.
  if (lo > 0) {
    if (!(hi > lo)) return years(String(lo));
    if (hi - lo <= Math.max(20, lo * 0.15)) return years(`~${Math.round((lo + hi) / 20) * 10}`);
    return years(`${lo}-${hi}`);
  }

  // 3. No number anywhere: the sentence's first clause, if it says something.
  const p = t.indexOf(" ("); if (p > 0) t = t.slice(0, p);
  const c = t.indexOf(","); if (c > 0) t = t.slice(0, c);
  const s = t.indexOf(";"); if (s > 0) t = t.slice(0, s);
  t = t.trim();
  if (!t || NO_INFO.test(t) || t.length > 24) return null;
  return t;
}
