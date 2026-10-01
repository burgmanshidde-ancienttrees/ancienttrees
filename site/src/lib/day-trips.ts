// Which of a city's trees are a day trip rather than a walk in town.
//
// Approved by Hidde on 2026-09-27 from the Copenhagen mockup ("OK yes, then
// it makes sense"): the city's own trees first, then "A day trip away", one
// group per place with its distance and direction ("Dyrehaven, 11 km north").
// He found it missing from the app on 2026-10-01; it was missing from the
// website too, because it had never been built.
//
// THE RULE LIVES HERE AND ONLY HERE. The answer travels in /api/trees.json as
// `day_trip` on each tree, and the app reads it (CLAUDE.md: a decision
// travels as data, never as a rule written twice).
//
// A tree is a day trip when all three hold, each because the one before it
// alone caught city neighbourhoods (measured across every city on the day):
//   1. it stands 10 km or more from the middle of the city's trees,
//   2. that is at least three times the city's own typical spread, so a city
//      whose trees are spread wide (Seoul, Houston) does not lose half of them,
//   3. its address does not name the city, so Tegel stays Berlin and
//      Brooklyn stays New York.
// And never more than half a city: if most trees are "out", nothing is.

import { haversineKm } from "./walks";

export interface DayTrip {
  /** The place, as a visitor would read it on a sign: "Jaegersborg Dyrehave". */
  place: string;
  /** Whole kilometres from the middle of the city's trees. */
  km: number;
  /** "north", "south-west" and so on, from the middle of the city. */
  dir: string;
}

const MIN_KM = 10;
const SPREAD_FACTOR = 3;
const GROUP_KM = 4;

/** Parts of a city that addresses name instead of the city. */
const CITY_PARTS: Record<string, string[]> = {
  "New York": ["brooklyn", "queens", "bronx", "staten island", "manhattan"],
};

const norm = (s: string) =>
  s.normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase();

const median = (xs: number[]) => {
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
};

function compass(from: [number, number], to: [number, number]): string {
  const dLat = to[0] - from[0];
  const dLng = (to[1] - from[1]) * Math.cos((from[0] * Math.PI) / 180);
  const deg = ((Math.atan2(dLng, dLat) * 180) / Math.PI + 360) % 360;
  return ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"][
    Math.round(deg / 45) % 8
  ];
}

/** The place name a group of trees shares, from their neighbourhood field. */
function placeOf(neighbourhood: string | undefined, address: string | undefined): string {
  const src = (neighbourhood || address || "").split(/[,(]/)[0].trim();
  return src || "Out of town";
}

interface TreeLike {
  id: string;
  location?: { latitude?: number; longitude?: number; neighbourhood?: string; address?: string };
}

/** Tree id to its day-trip label, for the trees that are one. */
export function dayTrips(city: string, trees: TreeLike[]): Map<string, DayTrip> {
  const out = new Map<string, DayTrip>();
  const pts = trees.filter((t) => t.location?.latitude != null && t.location?.longitude != null);
  if (pts.length < 6) return out;
  const centre: [number, number] = [
    median(pts.map((t) => t.location!.latitude!)),
    median(pts.map((t) => t.location!.longitude!)),
  ];
  const dist = new Map(pts.map((t) => [t.id, haversineKm(centre, [t.location!.latitude!, t.location!.longitude!])]));
  const spread = median([...dist.values()]);
  const names = [norm(city), ...(CITY_PARTS[city] ?? [])];
  const far = pts.filter((t) => {
    const k = dist.get(t.id)!;
    const addr = norm(`${t.location?.address ?? ""} ${t.location?.neighbourhood ?? ""}`);
    return k >= MIN_KM && k >= SPREAD_FACTOR * spread && !names.some((n) => addr.includes(n));
  });
  if (far.length === 0 || far.length > pts.length / 2) return out;

  // One label per group of trees standing near each other, so three oaks in
  // one deer park read as one outing rather than three.
  const groups: TreeLike[][] = [];
  for (const t of far) {
    const here: [number, number] = [t.location!.latitude!, t.location!.longitude!];
    const g = groups.find((g) => haversineKm([g[0].location!.latitude!, g[0].location!.longitude!], here) <= GROUP_KM);
    if (g) g.push(t); else groups.push([t]);
  }
  for (const g of groups) {
    const counts = new Map<string, number>();
    for (const t of g) {
      const p = placeOf(t.location?.neighbourhood, t.location?.address);
      counts.set(p, (counts.get(p) ?? 0) + 1);
    }
    const place = [...counts.entries()].sort((a, b) => b[1] - a[1])[0][0];
    const lat = median(g.map((t) => t.location!.latitude!));
    const lng = median(g.map((t) => t.location!.longitude!));
    const label: DayTrip = {
      place,
      km: Math.round(haversineKm(centre, [lat, lng])),
      dir: compass(centre, [lat, lng]),
    };
    for (const t of g) out.set(t.id, label);
  }
  return out;
}

/** The page order: trees in town first, then one group per day-trip place,
 *  nearest first. Each tree keeps its original number, because the map's
 *  markers are numbered in the city's own order. */
export function splitForPage<T extends TreeLike>(city: string, trees: T[]) {
  const trips = dayTrips(city, trees);
  const inTown = trees.filter((t) => !trips.has(t.id));
  const groups = new Map<string, { trip: DayTrip; trees: T[] }>();
  for (const t of trees) {
    const trip = trips.get(t.id);
    if (!trip) continue;
    const key = `${trip.place}|${trip.km}`;
    if (!groups.has(key)) groups.set(key, { trip, trees: [] });
    groups.get(key)!.trees.push(t);
  }
  return { inTown, away: [...groups.values()].sort((a, b) => a.trip.km - b.trip.km) };
}
