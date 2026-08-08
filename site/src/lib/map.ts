// Ported from map_head()/country_map_script()/single_pin_script(),
// build_site.py:1199-1230ish, 4045-4101. Raw <script>/<link> tags loading
// MapLibre from a CDN, matching the current site exactly rather than going
// through the bundled npm package (see site-config.ts's note on MAPLIBRE_JS).
import { MAPLIBRE_JS, MAPLIBRE_CSS, MAP_STYLE } from "./site-config";

export function mapHead(): string {
  return `<link rel="stylesheet" href="${MAPLIBRE_CSS}">`;
}

export interface CountryMapCity {
  slug: string;
  city: string;
  count: number;
  markers: { lat: number; lng: number }[];
}

/** One green dot per mapped city, click goes to its page. Deliberately the
 * simplest map on the site: at country zoom the job is orientation, not
 * detail. */
export function countryMapScript(cities: CountryMapCity[]): string {
  const centre = (c: CountryMapCity): [number, number] => [
    c.markers.reduce((s, m) => s + m.lng, 0) / c.markers.length,
    c.markers.reduce((s, m) => s + m.lat, 0) / c.markers.length,
  ];
  const data = {
    type: "FeatureCollection",
    features: cities.map((c) => ({
      type: "Feature",
      geometry: { type: "Point", coordinates: centre(c) },
      properties: { slug: c.slug, city: c.city, n: String(c.count) },
    })),
  };
  return `
<script src="${MAPLIBRE_JS}"></script>
<script>
var CITIES = ${JSON.stringify(data)};
var map = new maplibregl.Map({
  container: 'map', style: '${MAP_STYLE}',
  center: [0, 0], zoom: 3, renderWorldCopies: false,
  attributionControl: { compact: true }
});
map.addControl(new maplibregl.NavigationControl());
var b = new maplibregl.LngLatBounds();
CITIES.features.forEach(function(f) { b.extend(f.geometry.coordinates); });
var touched = false;
function fit() { if (!touched) { map.fitBounds(b, { padding: 48, maxZoom: 9, duration: 0 }); } }
map.on('dragstart', function() { touched = true; });
map.on('zoomstart', function(e) { if (e.originalEvent) { touched = true; } });
new ResizeObserver(function() { map.resize(); fit(); }).observe(document.getElementById('map'));
map.on('load', function() {
  fit();
  map.addSource('cities', {type: 'geojson', data: CITIES});
  map.addLayer({id: 'city-dot', type: 'circle', source: 'cities',
    paint: {'circle-color': '#4A6B2A', 'circle-opacity': 0.92, 'circle-radius': 15,
            'circle-stroke-width': 2, 'circle-stroke-color': '#F6F2E9'}});
  map.addLayer({id: 'city-n', type: 'symbol', source: 'cities',
    layout: {'text-field': ['get', 'n'], 'text-font': ['Noto Sans Regular'],
             'text-size': 12, 'text-allow-overlap': true},
    paint: {'text-color': '#F6F2E9'}});
  map.addLayer({id: 'city-name', type: 'symbol', source: 'cities',
    layout: {'text-field': ['get', 'city'], 'text-font': ['Noto Sans Regular'],
             'text-size': 12, 'text-offset': [0, 1.6], 'text-anchor': 'top'},
    paint: {'text-color': '#26301E', 'text-halo-color': '#F6F2E9', 'text-halo-width': 1.4}});
  map.on('click', 'city-dot', function(e) {
    window.location.href = '/' + e.features[0].properties.slug;
  });
  map.on('mouseenter', 'city-dot', function() { map.getCanvas().style.cursor = 'pointer'; });
  map.on('mouseleave', 'city-dot', function() { map.getCanvas().style.cursor = ''; });
});
</script>
`;
}

/** "the Netherlands" in a sentence, "The Netherlands" at its start. */
export function countryName(intro: { country: string; article?: string }, capital = false): string {
  const art = intro.article;
  if (!art) return intro.country;
  const displayArt = capital ? art.charAt(0).toUpperCase() + art.slice(1) : art;
  return `${displayArt} ${intro.country}`;
}
