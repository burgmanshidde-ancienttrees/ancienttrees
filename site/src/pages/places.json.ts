// Every town of 15,000 people or more, for the search's empty-place answer
// (Hidde, 2026-10-25: a place we hold no tree for is found anyway, and asks
// for its first tree; CONVENTIONS.md "A place we have nothing for"). The
// towns come from data/places-geonames.json (GeoNames, CC BY 4.0, credited on
// /sources; scripts/geonames_places.py). The nearest tree is worked out HERE,
// at every build, so it moves the day a closer tree goes live.
//
// Fetched by search-form.ts only when what was typed matches nothing of ours,
// so the 1 MB never loads for a search that finds a city we have.
import fs from "node:fs";
import path from "node:path";
import { getCollection } from "astro:content";
import { cityIsRenderable, slugify } from "../lib/trees";
import { citySearchNames } from "../lib/city-aliases";
import { DATA } from "../lib/data-dir";

function norm(s: string): string {
  return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
}

export async function GET() {
  const src = JSON.parse(fs.readFileSync(path.join(DATA, "places-geonames.json"), "utf-8")) as {
    countries: string[]; places: [string, string, number, number, number][];
  };
  const cities = (await getCollection("cities")).filter(cityIsRenderable);
  // A town that IS one of our pages is found by /search-index.json already.
  const ours = new Set<string>();
  const alt = citySearchNames();
  for (const e of cities) {
    ours.add(norm(e.data.city));
    for (const a of alt[e.id] ?? []) ours.add(norm(a));
  }
  const trees: { n: string; c: string; u: string; lat: number; lng: number }[] = [];
  for (const e of cities) {
    for (const t of e.data.trees) {
      const lat = t.location.latitude, lng = t.location.longitude;
      if (lat == null || lng == null) continue;
      trees.push({ n: t.name, c: e.data.city, u: `${e.id}/${slugify(t.name)}`, lat, lng });
    }
  }
  const R = Math.PI / 180;
  const used = new Map<number, number>();
  const t: [string, string, string][] = [];
  const p: [string, string, number, number, number, number, number][] = [];
  for (const [name, ascii, ci, lat, lng] of src.places) {
    if (ours.has(norm(name)) || (ascii && ours.has(norm(ascii)))) continue;
    // Nearest by an equirectangular distance, which ranks correctly at the
    // scale that matters; the kilometres shown are haversine.
    const k = Math.cos(lat * R);
    let best = -1, bd = Infinity;
    for (let i = 0; i < trees.length; i++) {
      const dy = trees[i].lat - lat, dx = (trees[i].lng - lng) * k;
      const d = dy * dy + dx * dx;
      if (d < bd) { bd = d; best = i; }
    }
    let ti = -1, km = -1;
    if (best >= 0) {
      const b = trees[best];
      const h = Math.sin(((b.lat - lat) * R) / 2) ** 2 +
        Math.cos(lat * R) * Math.cos(b.lat * R) * Math.sin(((b.lng - lng) * R) / 2) ** 2;
      km = Math.round(12742 * Math.asin(Math.sqrt(h)));
      if (!used.has(best)) { used.set(best, t.length); t.push([b.n, b.c, b.u]); }
      ti = used.get(best)!;
    }
    p.push([name, ascii, ci, lat, lng, ti, km]);
  }
  return new Response(JSON.stringify({ k: src.countries, t, p }), { headers: { "Content-Type": "application/json" } });
}
