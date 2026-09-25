// The line under a tree's name, in its two tappable halves: the place (a
// district in front of the city when there is one) and the country, which
// joins only when no district does, so the line stays one line.
//
// The same rule as TreeDetail.placeParts in the app (Hidde, 2026-09-04, on Old
// Tjikko: "daar moet zweden staan of een stad niet meer"). `neighbourhood`
// holds a district on most trees and a sentence on hundreds of them, so
// anything too long to BE a district name is dropped rather than printed.
// Kept in step with the Swift copy by hand for now; the better home is a field
// in /api/trees.json that the app reads.
export function placeParts(neighbourhood: string | null | undefined, city: string,
                           country: string | null | undefined): { place: string; country: string | null } {
  let n = (neighbourhood ?? "").trim();
  const bracket = n.indexOf("(");
  if (bracket >= 0) n = n.slice(0, bracket).trim();
  if ([...n].length > 28) n = "";
  if (!n) return { place: city, country: country ? country : null };
  return { place: n.toLowerCase().includes(city.toLowerCase()) ? n : `${n}, ${city}`, country: null };
}
