// The register layer's GeoJSON, fetched rather than inlined into /explore:
// there are thousands of these and they would otherwise be the heaviest
// thing on the page, loaded before the map the visitor actually came for.
// Ported from the REGISTER_ASSET block in build_explore_page(),
// build_site.py:4537-4550.
import { loadRegisters } from "../../lib/registers";

export async function GET() {
  const registers = loadRegisters();
  const features = registers.map((r) => ({
    type: "Feature",
    geometry: {
      type: "Point",
      // Rounded to five decimals, about a metre, far finer than a register
      // pin deserves; saves a fifth of the file. toFixed(), not
      // Math.round(x*1e5)/1e5: the multiply-then-round loses precision
      // right at the rounding boundary (-2.099695 rounded to -2.09969
      // instead of Python's correctly-rounded -2.0997), because toFixed()
      // is specified to round the double's true value, not a rescaled one.
      coordinates: [Number(r.lng.toFixed(5)), Number(r.lat.toFixed(5))],
    },
    properties: { name: r.name, area: r.area, designation: r.designation },
  }));
  const geojson = JSON.stringify({ type: "FeatureCollection", features });
  return new Response(geojson, { headers: { "Content-Type": "application/json" } });
}
