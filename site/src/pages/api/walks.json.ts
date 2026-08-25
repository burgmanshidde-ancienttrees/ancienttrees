// The curated walks, for a client that promises them.
//
// Hidde's paywall copy (DECISIONS.md 2026-08-18) sells "Curated Tree Walks:
// hand-picked routes connecting the most remarkable trees in any city", and
// his instruction with it was "we moeten dit verhaal waar gaan maken". The
// walks existed as data and as a planner all along, and on the same day they
// left the web, which left them reachable by nothing at all. This is the file
// that makes the promise servable.
//
// Everything here is computed at build time by the same planner the website
// used: single-link clustering so a walk is a chain rather than a blob, a
// nearest-neighbour order inside a distance budget, and a name taken from the
// place most of its trees share. Where scripts/route_walks.py has cached a
// real routed shape, that shape rides along, so a client draws the street a
// walker actually follows instead of straight lines between trunks.
import { getCollection } from "astro:content";
import { cityIsRenderable, walkableTrees } from "../../lib/trees";
import { planWalks, walkRouteFor, humanDuration, kmLabel, type WalkMarker } from "../../lib/walks";
import { speciesIcon } from "../../lib/species-icons";
import { usablePhoto } from "../../lib/images";
import { feedVersion } from "../../lib/app-feed";

export async function GET() {
  const cities = (await getCollection("cities")).filter(cityIsRenderable);
  const out: any[] = [];

  for (const city of cities) {
    const trees = walkableTrees(city).filter(
      (t) => t.location?.latitude != null && t.location?.longitude != null,
    );
    if (trees.length < 2) continue;

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

    for (const w of planWalks(markers)) {
      let order = w.order;
      let shape = w.shape;
      let km = w.km;
      let minutes = w.minutes;
      const routed = walkRouteFor(city.id, order.map((i) => trees[i].id));
      if (routed) {
        // A cache hit through the reversed-order fallback means our own
        // tie-break picked the opposite direction from what route_walks.py
        // recorded; reverse before deriving anything from the order, or the
        // walk would be served start-to-end backwards.
        if (routed.reversed) order = [...order].reverse();
        shape = routed.shape;
        km = routed.km ?? km;
        minutes = routed.minutes ?? minutes;
      }
      out.push({
        city: city.data.city,
        city_slug: city.id,
        name: w.name || `${city.data.city} walk`,
        trees: order.map((i) => trees[i].id),
        count: w.count,
        km: Number(kmLabel(km)),
        minutes: Math.round(minutes),
        duration: humanDuration(minutes),
        // True when this walk is the union of two smaller ones, so a client
        // can offer the legs separately rather than showing near-duplicates.
        combined: Boolean(w.combined),
        // [lng, lat] pairs along the street, when a real route was cached.
        shape: shape ?? null,
      });
    }
  }

  out.sort((a, b) => (a.city_slug < b.city_slug ? -1 : a.city_slug > b.city_slug ? 1 : b.count - a.count));
  const body = JSON.stringify(out);
  const version = await feedVersion(body);
  return new Response(JSON.stringify({ version, count: out.length, walks: out }), {
    headers: { "Content-Type": "application/json" },
  });
}
