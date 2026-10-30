// TREES WITH AN APPROXIMATE PIN ON ONE SPOT STAND A FEW METRES APART (Hidde,
// 2026-10-30: "als we toch niet zeker weten waar ze in het park liggen kunnen
// we ze dan niet net zo goed random n beetje verspreiden", and "relatief dicht
// bij elkaar houden - je wilt niet dat ze opeens uit het park zijn").
//
// 99 of the 104 trees that shared a coordinate had an approximate pin: they
// sat on one point because we knew the park and not the trunk, and their page
// already says "Approximate location". A pile drawn as one bubble claimed no
// more than a ring of pins does, and it hid all but one tree. Airbnb's map
// does the same for the same reason: a listing's spot is approximate, so no
// two listings share one (CONVENTIONS.md, "Two trees on exactly the same
// spot", 2026-10-29).
//
// Done once, here, when the data loads, so every web map and the app feed
// (app-feed.ts) draw the same spots and no surface carries the rule itself. A
// confirmed pin never moves; it keeps the centre of its pile. The ring is
// small (SPREAD_M) so a tree never leaves its park, and fixed (by id order),
// so a pin does not wander between builds. A tree that gets a real GPS fix
// leaves the pile and stops being spread by itself.
export const SPREAD_M = 10;

type Loc = { latitude?: number | null; longitude?: number | null };
type T = { id: string; location: Loc; location_precision?: string };

export function spreadSameSpot<X extends T>(trees: X[]): X[] {
  const piles = new Map<string, X[]>();
  for (const t of trees) {
    const { latitude: lat, longitude: lng } = t.location;
    if (lat == null || lng == null) continue;
    const k = lat.toFixed(5) + "," + lng.toFixed(5);
    piles.set(k, [...(piles.get(k) ?? []), t]);
  }
  for (const pile of piles.values()) {
    const loose = pile.filter((t) => t.location_precision !== "confirmed")
      .sort((a, b) => a.id.localeCompare(b.id));
    if (pile.length < 2 || loose.length === 0) continue;
    const lat = pile[0].location.latitude!, lng = pile[0].location.longitude!;
    // Two side by side; more on a circle starting at the top, as the spread
    // stack drew them.
    const n = loose.length;
    const r = n <= 2 ? SPREAD_M : SPREAD_M * 1.2;
    loose.forEach((t, k) => {
      const a = n === 1 ? -Math.PI / 2 : n === 2 ? Math.PI * k : -Math.PI / 2 + (k * 2 * Math.PI) / n;
      const dLat = (r * -Math.sin(a)) / 111320;
      const dLng = (r * Math.cos(a)) / (111320 * Math.cos((lat * Math.PI) / 180));
      t.location = { ...t.location, latitude: +(lat + dLat).toFixed(6), longitude: +(lng + dLng).toFixed(6) };
    });
  }
  return trees;
}
