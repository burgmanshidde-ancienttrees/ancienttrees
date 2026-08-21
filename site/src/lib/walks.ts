// KEEP THIS, and keep data/walk-routes.json with it. On 2026-08-18 Hidde took
// the walking routes off the web ("die ik niet beschikbaar wil maken op web"),
// so the city pages no longer render a walk picker and no longer call
// planWalks(). He said in the same breath why this file stays: "de functie
// hebben we later dus wel nog nodig voor app dus gooi de info niet weg."
// Walking is one of the product's four verbs and the app is where it lands, so
// this is a feature parked on the shelf, not dead code to tidy away. The route
// cache (data/walk-routes.json), scripts/route_walks.py and
// scripts/walk_planning.py are part of the same shelf.
//
// Ported from the walk-planning system, build_site.py:1231-1530. Works out,
// at build time, every honest walk a city's trees allow: single-link
// clustering (a walk is a chain, not a blob), a nearest-neighbour route
// within a distance budget, splitting routes too long for one afternoon,
// and naming a walk after the place most of its trees share.
import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

const DETOUR_FACTOR = 1.35;
const WALKING_KMH = 4.5;
const WALK_BUDGET_KM = 6.0;
const WALK_MIN_TREES = 3;
const WALK_CLUSTER_M = 900;
export const WALK_NAME_MAX = 34;
const WALK_SPLIT_KM = 3.0;
const WALK_MAX_OVERLAP = 0.5;

type LatLng = [number, number];

export interface WalkMarker {
  lat: number;
  lng: number;
  label: string;
  icon: string;
  name: string;
  id: string;
  area: string;
  shot: boolean;
  /** Months this species peaks (already shifted for latitude), the animation
   * and its colour. Absent for a species with no peak. The month is compared
   * in the browser, not at build time, so a cached page still lights up on the
   * right day. */
  peak?: { months: number[]; effect: string; colour: string; level?: string };
}

export interface Walk {
  order: number[];
  count: number;
  km: number;
  minutes: number;
  name: string;
  shots?: number;
  url?: string;
  shape?: [number, number][];
  duration?: string;
  label?: string;
  combined?: boolean;
}

export function haversineKm(a: LatLng, b: LatLng): number {
  const toRad = (d: number) => (d * Math.PI) / 180;
  const [lat1, lon1, lat2, lon2] = [toRad(a[0]), toRad(a[1]), toRad(b[0]), toRad(b[1])];
  const h = Math.sin((lat2 - lat1) / 2) ** 2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin((lon2 - lon1) / 2) ** 2;
  return 6371.0 * 2 * Math.asin(Math.sqrt(h));
}

/** Find the best walk through a cluster of trees, not through all of them:
 * grows a nearest-neighbour path from every possible start, stops when the
 * next tree would blow the budget, keeps whichever attempt gathered the
 * most trees (shortest wins a tie). */
function planWalkingRoute(points: LatLng[], budgetKm = WALK_BUDGET_KM): { order: number[]; km: number; minutes: number } | null {
  const n = points.length;
  if (n < WALK_MIN_TREES) return null;

  let best: [number[], number] | null = null;
  for (let start = 0; start < n; start++) {
    const unvisited = new Set(Array.from({ length: n }, (_, i) => i));
    unvisited.delete(start);
    const order = [start];
    let total = 0.0;
    let current = start;
    while (unvisited.size > 0) {
      let nxt = -1;
      let nxtDist = Infinity;
      for (const i of unvisited) {
        const d = haversineKm(points[current], points[i]);
        if (d < nxtDist) {
          nxtDist = d;
          nxt = i;
        }
      }
      const step = nxtDist;
      if ((total + step) * DETOUR_FACTOR > budgetKm) break;
      total += step;
      order.push(nxt);
      unvisited.delete(nxt);
      current = nxt;
    }
    if (order.length < WALK_MIN_TREES) continue;
    // An exact tie (a route and its mirror image, same edges summed in
    // opposite order) sums to bit-identical totals in Python's math library
    // but not always in JS's, off by ~1e-13 km of pure floating-point noise.
    // Untreated, that flips which direction wins an otherwise-genuine tie,
    // which then misses data/walk-routes.json's cache key (built from the
    // tree-id order Python picked) and silently falls back to a straight-
    // line estimate instead of the real routed distance. The epsilon is
    // nanometre-scale: far above the observed noise floor, far below any
    // distance difference that should ever decide a real tie.
    const strictlyShorter = total < best?.[1] - 1e-9;
    if (!best || order.length > best[0].length || (order.length === best[0].length && strictlyShorter)) {
      best = [order, total];
    }
  }

  if (!best) return null;
  const [order, total] = best;
  const km = total * DETOUR_FACTOR;
  return { order, km: Math.round(km * 10) / 10, minutes: Math.round((km / WALKING_KMH) * 60) };
}

/** Single-link clustering: trees joined when one is within radius of
 * another. A walk is a chain, not a blob, so this beats k-means/a grid for
 * a ribbon-shaped city like Porto. */
function walkClusters(points: LatLng[], radiusM = WALK_CLUSTER_M): number[][] {
  const n = points.length;
  const seen = new Set<number>();
  const groups: number[][] = [];
  for (let i = 0; i < n; i++) {
    if (seen.has(i)) continue;
    const stack = [i];
    const comp: number[] = [];
    while (stack.length) {
      const k = stack.pop()!;
      if (seen.has(k)) continue;
      seen.add(k);
      comp.push(k);
      for (let j = 0; j < n; j++) {
        if (!seen.has(j) && haversineKm(points[k], points[j]) * 1000 <= radiusM) stack.push(j);
      }
    }
    groups.push(comp.sort((a, b) => a - b));
  }
  return groups;
}

function areaHead(area: string | undefined): string {
  let head = String(area ?? "").split(",")[0];
  head = head.replace(/\([^)]*\)?/g, "");
  head = head.replace(/\s+/g, " ").trim().replace(/^[-/\s]+|[-/\s]+$/g, "");
  return head;
}

/** Name a walk after the place most of its trees share; falls back to "" rather than inventing one. */
function walkName(members: number[], markers: WalkMarker[]): string {
  const counts = new Map<string, number>();
  for (const idx of members) {
    const head = areaHead(markers[idx].area);
    if (head.length >= 3) counts.set(head, (counts.get(head) ?? 0) + 1);
  }
  if (counts.size === 0) return "";
  // A compound parish and its short form are one place: fold a name that is
  // contained in a longer one into the longer, then re-vote (build_site.py:1362-1366).
  const merged = new Map<string, number>();
  for (const [name, n] of counts) {
    const parent = [...counts.keys()].find((o) => o !== name && o.toLowerCase().includes(name.toLowerCase()));
    const key = parent ?? name;
    merged.set(key, (merged.get(key) ?? 0) + n);
  }
  let best = "";
  let hits = -1;
  for (const [name, n] of merged) {
    if (n > hits || (n === hits && name.length < best.length)) {
      best = name;
      hits = n;
    }
  }
  if (hits < 2 || hits * 3 < members.length) return "";
  return best.length <= WALK_NAME_MAX ? best : "";
}

function legKm(order: number[], points: LatLng[]): number {
  let total = 0;
  for (let i = 0; i < order.length - 1; i++) total += haversineKm(points[order[i]], points[order[i + 1]]);
  return total * DETOUR_FACTOR;
}

/** Cut a long route in half at its midpoint, into two DISJOINT halves, when
 * a route is too long to walk in one go. The first version let the junction
 * tree belong to both halves; Hidde saw the result on Amsterdam and called
 * it: two walks whose lines are welded together at the shared tree read as
 * ONE walk on the overview map (2026-08-08). So the halves are now disjoint,
 * and the way to walk both is the explicit "Both walks" choice planWalks
 * adds when the whole route is still a doable afternoon. */
function splitRoute(order: number[], points: LatLng[], depth = 0): number[][] {
  const km = legKm(order, points);
  if (depth >= 2 || km <= WALK_SPLIT_KM || order.length < WALK_MIN_TREES * 2) return [order];
  const half = km / DETOUR_FACTOR / 2;
  let run = 0;
  let cut = Math.floor(order.length / 2);
  for (let i = 0; i < order.length - 1; i++) {
    run += haversineKm(points[order[i]], points[order[i + 1]]);
    if (run >= half) {
      cut = i;
      break;
    }
  }
  cut = Math.max(WALK_MIN_TREES - 1, Math.min(cut, order.length - WALK_MIN_TREES - 1));
  const first = order.slice(0, cut + 1);
  const second = order.slice(cut + 1); // disjoint: no shared tree
  if (first.length < WALK_MIN_TREES || second.length < WALK_MIN_TREES) return [order];
  return [...splitRoute(first, points, depth + 1), ...splitRoute(second, points, depth + 1)];
}

function tooSimilar(a: number[], b: number[]): boolean {
  const sa = new Set(a);
  const sb = new Set(b);
  const inter = [...sa].filter((x) => sb.has(x)).length;
  return inter / Math.min(sa.size, sb.size) > WALK_MAX_OVERLAP;
}

/** Every honest walk in a city, not just the best one. */
export function planWalks(markers: WalkMarker[], budgetKm = WALK_BUDGET_KM): Walk[] {
  const points: LatLng[] = markers.map((m) => [m.lat, m.lng]);
  // The chaining radius, with a fallback measured on 2026-08-08. At 900 m,
  // 30 of 91 cities had no walk at all, and 11 of them (London, Venice,
  // Copenhagen, The Hague among them) get their first walk at 1500 m: their
  // trees stand 1.0-1.5 km apart, which is still an afternoon in a big
  // city. But 1500 m globally welds Paris, Vienna, Naples and Nice's named
  // walks into one blob each. So the wider radius applies ONLY to a city
  // that would otherwise have no walk: cities with walks keep them exactly
  // as they are, and a first walk beats no walk.
  let groups = walkClusters(points);
  if (!groups.some((g) => g.length >= WALK_MIN_TREES)) groups = walkClusters(points, 1500);
  const walks: Walk[] = [];
  for (const members of groups) {
    if (members.length < WALK_MIN_TREES) continue;
    const sub = members.map((i) => points[i]);
    const route = planWalkingRoute(sub, budgetKm);
    if (!route) continue;
    const order = route.order.map((i) => members[i]);
    let kept = 0;
    for (const leg of splitRoute(order, points)) {
      if (walks.some((w) => tooSimilar(leg, w.order))) continue;
      kept++;
      const km = Math.round(legKm(leg, points) * 10) / 10;
      walks.push({
        order: leg,
        count: leg.length,
        km,
        minutes: Math.round((km / WALKING_KMH) * 60),
        name: walkName(leg, markers),
      });
    }
    // A split cluster's halves are disjoint (Hidde, 2026-08-08: welded lines
    // read as one walk on the overview map).
    //
    // NO COMBINED "BOTH WALKS" OPTION. Removed 2026-08-11. It was the longest
    // thing on every page and it contradicted the split that had just been
    // made: Porto offered all 18 trees over 4.0 km, Barcelona 14 over 3.5,
    // Lisbon 11 over 4.5. It could never have been realistic by construction:
    // the chip only appears when a route was split, and a route is only split
    // above WALK_SPLIT_KM, so it is always longer than the distance we call
    // too long for an afternoon. Mirrors scripts/walk_planning.py.
  }

  for (const w of walks) w.shots = w.order.filter((i) => markers[i].shot).length;
  walks.sort((a, b) => (b.shots ?? 0) - (a.shots ?? 0) || b.count - a.count || a.km - b.km);
  // Two walks under one name tells a visitor nothing. Blanking both was the
  // first fix and it was too blunt: the commonest cause is a split, where a
  // route over WALK_SPLIT_KM is cut in half, both halves sit in the same place
  // and so both lose the name of it. Barcelona shipped "Walk 2" and "Walk 3"
  // for the two halves of Montjuic, and you cannot choose between things with
  // no names. So separate them by where they are, and blank only if even that
  // cannot tell them apart. Mirrors _walk_name/plan_walks in
  // scripts/walk_planning.py; the two must stay in step.
  // Collapse a name that CONTAINS another walk's name onto the shorter one.
  // Porto had "Lordelo do Ouro e Massarelos" beside "Massarelos" (a merged
  // civil parish next to one of its halves) and Vienna "Innere Stadt /
  // Landstrasse border" beside "Innere Stadt". Measured 2026-08-11: the only
  // two such cases in 95 cities. Collapsing turns them into ordinary
  // duplicates, which the compass rule below then names short and
  // recognisably, which is the standard Hidde asked for.
  for (const w of walks) {
    if (!w.name) continue;
    const shorter = walks
      .filter((o) => o.name && o.name !== w.name && w.name.toLowerCase().includes(o.name.toLowerCase()))
      .map((o) => o.name);
    if (shorter.length) w.name = shorter.reduce((a, b) => (b.length < a.length ? b : a));
  }

  const byName = new Map<string, Walk[]>();
  for (const w of walks) if (w.name) (byName.get(w.name) ?? byName.set(w.name, []).get(w.name)!).push(w);
  for (const [name, group] of byName) {
    if (group.length < 2) continue;
    const cents = group.map((w) => {
      const la = w.order.reduce((s, i) => s + markers[i].lat, 0) / w.order.length;
      const lo = w.order.reduce((s, i) => s + markers[i].lng, 0) / w.order.length;
      return [la, lo] as const;
    });
    const lats = cents.map((c) => c[0]);
    const lngs = cents.map((c) => c[1]);
    const midLat = lats.reduce((a, b) => a + b, 0) / lats.length;
    const midLng = lngs.reduce((a, b) => a + b, 0) / lngs.length;
    const spreadNS = Math.max(...lats) - Math.min(...lats);
    const spreadEW = (Math.max(...lngs) - Math.min(...lngs)) * Math.cos((midLat * Math.PI) / 180);
    group.forEach((w, i) => {
      const [la, lo] = cents[i];
      if (spreadEW >= spreadNS && spreadEW > 0) w.name = `${name} ${lo >= midLng ? "east" : "west"}`;
      else if (spreadNS > 0) w.name = `${name} ${la >= midLat ? "north" : "south"}`;
      else w.name = "";
    });
    const labels = group.map((w) => w.name);
    for (const w of group) if (labels.filter((l) => l === w.name).length > 1) w.name = "";
  }
  return walks;
}

// -------------------------------------------------------------- cached routes

interface WalkRoute {
  shape?: [number, number][];
  km?: number;
  minutes?: number;
  rejected?: boolean;
  /** Set only on the object this module returns, never stored in the cache
   * file itself: true when the hit came from the reversed-order fallback
   * key, so the caller knows to reverse its own walk order (and therefore
   * its members list and its Google Maps directions URL) to stay
   * consistent with the direction this cached route was actually recorded
   * in. The shape/km/minutes need no such correction, a walking route and
   * its mirror cover the same physical path either way. */
  reversed?: boolean;
}

let cachedRoutes: Record<string, WalkRoute> | null = null;

function loadWalkRoutes(): Record<string, WalkRoute> {
  if (cachedRoutes) return cachedRoutes;
  const f = path.join(DATA, "walk-routes.json");
  if (!fs.existsSync(f)) {
    cachedRoutes = {};
    return cachedRoutes;
  }
  const data = JSON.parse(fs.readFileSync(f, "utf-8"));
  cachedRoutes = data.routes ?? {};
  return cachedRoutes!;
}

/** Real pedestrian geometry per walk, cached by scripts/route_walks.py.
 * Missing file/key or a rejected route falls back to the straight line.
 *
 * Also tries the reversed tree-id order before giving up. The cache key is
 * the exact order plan_walking_route's nearest-neighbour search picked for
 * a cluster, and that search sometimes has to break a genuine tie between
 * a route and its exact mirror image (same edges, opposite direction) by
 * whichever total is fractionally smaller. That fraction is femtometre-
 * scale floating-point noise, not a real distance, and JS and Python's
 * math libraries don't produce identical noise for the same inputs, so the
 * two languages can pick opposite directions for the same walk. A walking
 * route and its reverse are the same physical path either way (same km,
 * same minutes, and the drawn line looks identical regardless of which end
 * of the polyline coordinates start from), so falling back to the reversed
 * key recovers the real routed distance instead of silently degrading to a
 * straight-line estimate over an arbitrary tie-break disagreement. */
export function walkRouteFor(citySlug: string, treeIds: string[]): WalkRoute | null {
  const routes = loadWalkRoutes();
  let r = routes[`${citySlug}:${treeIds.join(",")}`];
  let reversed = false;
  if (!r) {
    r = routes[`${citySlug}:${[...treeIds].reverse().join(",")}`];
    reversed = true;
  }
  if (!r || r.rejected || !r.shape) return null;
  return reversed ? { ...r, reversed: true } : r;
}

/** Match Python's implicit float formatting for a walk's km figure: every
 * km value there is a Python float (either round(x, 1), or read straight
 * from data/walk-routes.json's "km": 0.0-style fields), and str(float)
 * always shows at least one decimal, even for a whole number (str(2.0) ==
 * "2.0"). JS numbers have no separate float type and drop the trailing
 * zero, which showed up as a real page-text diff against the Python build
 * (Krakow's degenerate 0.0 km walk rendering as "0 km"). Only whole numbers
 * need help: JS's default number-to-string already matches Python's str()
 * for the general case, since both use the shortest round-trip decimal for
 * an IEEE 754 double. */
export function kmLabel(km: number): string {
  return Number.isInteger(km) ? km.toFixed(1) : String(km);
}

export function humanDuration(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const mins = Math.round(minutes) % 60;
  if (hours && mins) return `${hours}h ${mins}m`;
  if (hours) return hours === 1 ? "1 hour" : `${hours} hours`;
  return `${mins} min`;
}

/** Hands turn-by-turn navigation to the visitor's own maps app. Google's URL
 * scheme takes at most 9 waypoints. */
export function mapsRouteUrl(orderedPoints: LatLng[]): string {
  if (orderedPoints.length < 2) return "";
  const pts = orderedPoints.map(([lat, lng]) => `${lat.toFixed(6)},${lng.toFixed(6)}`);
  const origin = pts[0];
  const destination = pts[pts.length - 1];
  let middle = pts.slice(1, -1);
  if (middle.length > 9) {
    const step = middle.length / 9.0;
    middle = Array.from({ length: 9 }, (_, i) => middle[Math.floor(i * step)]);
  }
  let url = `https://www.google.com/maps/dir/?api=1&travelmode=walking&origin=${origin}&destination=${destination}`;
  if (middle.length) url += `&waypoints=${middle.join("|")}`;
  return url;
}
