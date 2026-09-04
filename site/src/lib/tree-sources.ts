// The per-tree source list. Written 2026-09-04.
//
// Convention check (CONVENTIONS.md, "Crediting open data"): the same reference
// as /sources, one layer down. Wikipedia, iNaturalist and OpenStreetMap all
// name the sources of an individual record on that record's own page, as a
// short list at the foot of the content, linked out. Nobody invents a format
// for a citation list and neither do we.
//
// Why it exists at all: /sources has said since 2026-09-03 that "each tree page
// lists the exact sources used for that tree", and no page did. We store
// verified_sources on 2,470 of 2,472 trees and rendered them nowhere, so 1,588
// distinct outside websites were being used and credited to nobody. That is a
// debt under every attribution licence we import under, and it was owed before
// anybody asked for a link back.
//
// Two shapes live in the field. Most entries are URLs. 613 are prose citations
// of a register sheet ("italy-masaf.json (sheet 02/A794/BG/03, girth 405cm)"),
// which name a document rather than a page: those render as text, because a
// citation you cannot click is still a citation, and inventing a link for one
// would be worse than not having it.

export interface TreeSource {
  href?: string;
  label: string;
}

// Enough to identify the source, short enough to sit in a list. A path is
// dropped: the host is what a reader recognises and what a credit names.
function hostLabel(url: string): string {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch {
    return url;
  }
}

// A register citation is one long sentence naming a file and a sheet. The file
// path is ours and means nothing to a reader, so it goes; what is left is the
// part that identifies the document.
function textLabel(raw: string): string {
  let s = raw.replace(/^data\/registers\//, "").replace(/\.json/, "");
  if (s.length > 150) s = s.slice(0, 147).trimEnd() + "…";
  return s;
}

// A tree citing two articles on one site rendered the same host twice, which
// reads as a duplicate rather than as two sources (Lisbon's jacarandas cited
// A Mensagem twice on the day this shipped). Where a host repeats, the last
// meaningful path segment is added so the two are told apart.
function pathHint(url: string): string {
  try {
    const parts = new URL(url).pathname.split("/").filter(Boolean);
    const last = parts[parts.length - 1] ?? "";
    const hint = last.replace(/\.\w{2,5}$/, "").replace(/[-_]+/g, " ").trim();
    if (!hint) return "";
    return hint.length > 40 ? hint.slice(0, 39).trimEnd() + "…" : hint;
  } catch {
    return "";
  }
}

export function treeSources(tree: { verified_sources?: string[] }): TreeSource[] {
  const raw = tree.verified_sources ?? [];
  const seen = new Set<string>();
  const out: TreeSource[] = [];
  const hostCount = new Map<string, number>();
  for (const entry of raw) {
    const s = String(entry ?? "").trim();
    if (/^https?:\/\//i.test(s)) {
      const h = hostLabel(s);
      hostCount.set(h, (hostCount.get(h) ?? 0) + 1);
    }
  }
  for (const entry of raw) {
    const s = String(entry ?? "").trim();
    if (!s) continue;
    if (seen.has(s)) continue;
    seen.add(s);
    if (/^https?:\/\//i.test(s)) {
      const h = hostLabel(s);
      const hint = (hostCount.get(h) ?? 0) > 1 ? pathHint(s) : "";
      out.push({ href: s, label: hint ? `${h}, ${hint}` : h });
    } else {
      out.push({ label: textLabel(s) });
    }
  }
  return out;
}
