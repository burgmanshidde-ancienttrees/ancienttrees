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
const WALK_NAME_MAX = 34;
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
    if (!best || order.length > best[0].length || (order.length === best[0].length && total < best[1])) {
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

/** Cut a long route in half at its midpoint, letting the junction tree
 * belong to both halves, when a route is too long to walk in one go. */
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
  cut = Math.max(WALK_MIN_TREES - 1, Math.min(cut, order.length - WALK_MIN_TREES));
  const first = order.slice(0, cut + 1);
  const second = order.slice(cut);
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
  const walks: Walk[] = [];
  for (const members of walkClusters(points)) {
    if (members.length < WALK_MIN_TREES) continue;
    const sub = members.map((i) => points[i]);
    const route = planWalkingRoute(sub, budgetKm);
    if (!route) continue;
    const order = route.order.map((i) => members[i]);
    for (const leg of splitRoute(order, points)) {
      if (walks.some((w) => tooSimilar(leg, w.order))) continue;
      const km = Math.round(legKm(leg, points) * 10) / 10;
      walks.push({
        order: leg,
        count: leg.length,
        km,
        minutes: Math.round((km / WALKING_KMH) * 60),
        name: walkName(leg, markers),
      });
    }
  }
  for (const w of walks) w.shots = w.order.filter((i) => markers[i].shot).length;
  walks.sort((a, b) => (b.shots ?? 0) - (a.shots ?? 0) || b.count - a.count || a.km - b.km);
  const nameCounts = new Map<string, number>();
  for (const w of walks) if (w.name) nameCounts.set(w.name, (nameCounts.get(w.name) ?? 0) + 1);
  const dupes = new Set([...nameCounts.entries()].filter(([, n]) => n > 1).map(([name]) => name));
  for (const w of walks) if (dupes.has(w.name)) w.name = "";
  return walks;
}

// -------------------------------------------------------------- cached routes

interface WalkRoute {
  shape?: [number, number][];
  km?: number;
  minutes?: number;
  rejected?: boolean;
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
 * Missing file/key or a rejected route falls back to the straight line. */
export function walkRouteFor(citySlug: string, treeIds: string[]): WalkRoute | null {
  const routes = loadWalkRoutes();
  const r = routes[`${citySlug}:${treeIds.join(",")}`];
  if (!r || r.rejected || !r.shape) return null;
  return r;
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
