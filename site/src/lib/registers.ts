// The register layer (CLAUDE.md, "The register layer", approved 2026-07-29/
// 30): officially designated trees from government registers, shown as
// honestly-labeled map dots. Not our research, not collectible, no own
// pages. Ported from load_registers(), build_site.py:2595-2662.
//
// Registers do not share a shape and never will: one is Japanese cultural-
// property records, one is an Italian ministry spreadsheet, one is a
// Portuguese WFS. So the fields are read by fallback rather than by schema.
// Anything an entry flags as a group (an avenue, a stand) is skipped,
// because a dot has to be a place you can stand.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

export interface RegisterDot {
  name: string;
  area: string;
  designation: string;
  lat: number;
  lng: number;
}

interface RawEntry {
  group?: unknown;
  private?: unknown;
  access_restricted?: unknown;
  latitude?: number | null;
  longitude?: number | null;
  name_en?: string;
  name?: string;
  name_ja?: string;
  name_it?: string;
  name_pt?: string;
  species?: string;
  area_en?: string;
  area?: string;
  comune?: string;
  concelho?: string;
  city?: string;
  place?: string;
  province?: string;
  prefecture?: string;
  designation?: string;
}

/** Every register dot the map may show. Throws (the ratchet: CLAUDE.md's
 * "a register file with no licence block" - a lesson that hit twice, now a
 * build check) on a register file that isn't the wrapper object carrying
 * its licence, proof and entries: a bare list has no licence attached, and
 * an import that skips the wrapper is exactly how unlicensed data would
 * reach the map. */
export function loadRegisters(): RegisterDot[] {
  const regDir = path.join(DATA, "registers");
  if (!fs.existsSync(regDir)) return [];
  const out: RegisterDot[] = [];
  for (const file of fs.readdirSync(regDir).filter((f) => f.endsWith(".json")).sort()) {
    const raw = fs.readFileSync(path.join(regDir, file), "utf-8");
    const d = JSON.parse(raw);
    if (typeof d !== "object" || d === null || Array.isArray(d)) {
      throw new Error(
        `register ${file} is a bare list with no licence block; an import must write the wrapper (see scripts/import_wien.py)`,
      );
    }
    if (d.publish_dots === false) continue;
    const designation: string = d.designation || d.attribution || d.prefecture || "official register";
    const entries: RawEntry[] = [...(d.trees ?? []), ...(d.entries ?? [])];
    for (const t of entries) {
      if (t.group) continue;
      // Hard rule 10, enforced here rather than trusted to each importer.
      if (t.private || t.access_restricted) continue;
      const lat = t.latitude;
      const lng = t.longitude;
      if (lat == null || lng == null) continue;
      const name = t.name_en || t.name || t.name_ja || t.name_it || t.name_pt || t.species || "";
      const area = t.area_en || t.area || t.comune || t.concelho || t.city || t.place || t.province || t.prefecture || "";
      let own = t.designation;
      if (d.prefecture && !own) own = `${d.prefecture} Natural Monument`;
      out.push({ name, area, designation: own || designation, lat, lng });
    }
  }
  return out;
}
