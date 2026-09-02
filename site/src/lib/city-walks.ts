// The walks a page may MENTION, and the test for whether it has any.
//
// It fed /[city]/walks (Contract K) until 2026-09-02, when Hidde took the
// walks off the website for good and pointed every walk control at the app
// overlay instead. What survives is the gate: a page may say the word "walk"
// to a reader only where walks actually exist, and that answer has to come
// from the same computation the app's own walks feed uses, or the website
// advertises a route the app does not have.
import { walkableTrees, type CityEntry, type Tree } from "./trees";
import { speciesIcon } from "./species-icons";
import { usablePhoto } from "./images";
import { planWalks, walkRouteFor, humanDuration, kmLabel, type WalkMarker } from "./walks";

export interface PageWalk {
  name: string;
  km: number;
  minutes: number;
  duration: string;
  trees: Tree[];
}

/// Enough walking to be worth mentioning: five tree entries across a city's
/// walks, the same floor Contract H puts on a park. Below it, what the app
/// would offer is a stroll between two trees, and promising a "walk" for that
/// is the kind of small over-claim a reader only has to be caught by once.
export const WALKS_PAGE_MIN_TREES = 5;

export function pageWalksFor(city: CityEntry): PageWalk[] {
  const trees = walkableTrees(city).filter(
    (t) => t.location?.latitude != null && t.location?.longitude != null,
  );
  if (trees.length < 2) return [];

  const markers: WalkMarker[] = trees.map((t, i) => ({
    lat: t.location.latitude!,
    lng: t.location.longitude!,
    label: String(i + 1),
    icon: speciesIcon(t),
    name: t.name,
    id: t.id,
    area: (t.location.neighbourhood ?? "").trim(),
    shot: Boolean(usablePhoto(t)),
  }));

  const out: PageWalk[] = [];
  for (const w of planWalks(markers)) {
    // A combined walk is the union of two smaller ones. The app offers it as a
    // longer option; on a page it reads as a near-duplicate of the two it is
    // made of, so the legs are what gets listed.
    if (w.combined) continue;
    let order = w.order;
    let km = w.km;
    let minutes = w.minutes;
    const routed = walkRouteFor(city.id, order.map((i) => trees[i].id));
    if (routed) {
      if (routed.reversed) order = [...order].reverse();
      km = routed.km ?? km;
      minutes = routed.minutes ?? minutes;
    }
    out.push({
      name: w.name || `${city.data.city} walk`,
      km: Number(kmLabel(km)),
      minutes: Math.round(minutes),
      duration: humanDuration(minutes),
      trees: order.map((i) => trees[i]),
    });
  }
  return out.sort((a, b) => b.trees.length - a.trees.length);
}

/// True when this city has walks worth pointing a reader at. The city and tree
/// pages ask this before they show a walk control at all.
export function hasWalksPage(city: CityEntry): boolean {
  const walks = pageWalksFor(city);
  return walks.reduce((n, w) => n + w.trees.length, 0) >= WALKS_PAGE_MIN_TREES;
}
