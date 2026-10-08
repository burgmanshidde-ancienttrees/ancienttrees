/** The district for the breadcrumb under a tree's name, or null (Hidde,
 * 2026-10-08: "Japan - Tokyo - neighbourhood is the build up"). The line reads
 * broad to narrow, country, city, district, the order every breadcrumb uses
 * (AllTrails' trail page, Tripadvisor, Wikipedia's location line). Same
 * cleaning as before: a bracketed note goes, anything too long to be a
 * district name is prose and goes, and a district that IS the city adds
 * nothing. Read by the app's TreeDetail.placeCrumbs, which mirrors it. */
export function placeDistrict(neighbourhood: string | null | undefined, city: string): string | null {
  let n = (neighbourhood ?? "").trim();
  const bracket = n.indexOf("(");
  if (bracket >= 0) n = n.slice(0, bracket).trim();
  if (!n || [...n].length > 28) return null;
  if (n.toLowerCase() === city.toLowerCase()) return null;
  return n;
}
