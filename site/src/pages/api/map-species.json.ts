// The species chip's list for a map that does not carry it inline (the city
// map, 2026-11-01): the names and their Latin as HTML, in the order and with
// the indexes /explore and /api/pins.json use (lib/map-species.ts).
import { mapSpecies } from "../../lib/map-species";

export async function GET() {
  const { list, latinHtml } = await mapSpecies();
  return new Response(JSON.stringify({ names: list, latin: latinHtml }),
                      { headers: { "Content-Type": "application/json" } });
}
