// WHICH PLACES HAVE A PAGE (Hidde, 2026-11-05: "ja dat mag", the third step
// of the trim after the question pages and the unread translations).
//
// A place with one tree on the website had two pages saying one thing: the
// place page (a map with one pin and one card) and the tree's own page. The
// place page has carried the robots noindex for every engine since 10-01, so
// no search engine used it, and Google still spent a crawl on it every round
// (Search Console: ~145 requests a day for a site of ~6,500 urls). So a place
// with one tree has no page: /<place> redirects to the tree (redirect-map.ts,
// hard rule 3, no url dies), and the tree page's back arrow and "bigger map"
// go to the explore map at the tree's spot, where the trees around it show
// (Hidde agreed to that exact change, 2026-11-05).
//
// One exception: a place whose page exists in another language the build
// still renders (data/translations-kept.json: Google showed it after 11-01)
// keeps its pages, since those are the pages Google chose.
//
// scripts/thin_pages.py reads PLACE_PAGE_MIN_TREES from this file as text.
import { languagesForCity } from "./i18n";

export const PLACE_PAGE_MIN_TREES = 2;

/** Does a place with this many trees on the website get a page? */
export function placeHasPage(slug: string, webTreeCount: number): boolean {
  if (webTreeCount >= PLACE_PAGE_MIN_TREES) return true;
  return webTreeCount > 0 && languagesForCity(slug).length > 0;
}

/** Where a one-tree place's tree page sends "back" and "bigger map": the
 * explore map at the tree (map.ts reads #map=zoom/lat/lng). */
export function exploreAt(lat: number, lng: number): string {
  return `/explore#map=15/${lat.toFixed(5)}/${lng.toFixed(5)}`;
}
