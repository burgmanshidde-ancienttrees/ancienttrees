// The walks a city page and a city's walks page both need.
//
// One implementation, because two would drift and the city page has to know
// whether the walks page exists before it may link to it. scripts/qa.py fails
// the deploy on a page nothing links to, and it fails just as hard on a link
// to a page that was never built, so the two questions have to be answered by
// the same function.
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

/// Enough on the page to be worth a page: five tree entries across its walks,
/// the same floor Contract H puts on a park, because below that the city page
/// serves the reader better than a walks page wearing its name.
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

/// True when this city earns a walks page. The city page asks this before it
/// puts a link on itself.
export function hasWalksPage(city: CityEntry): boolean {
  const walks = pageWalksFor(city);
  return walks.reduce((n, w) => n + w.trees.length, 0) >= WALKS_PAGE_MIN_TREES;
}
