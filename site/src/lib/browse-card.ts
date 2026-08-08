// The one card used by every browse index (cities, species, collections,
// countries, parks). Ported from browse_card()/collection_face(),
// build_site.py:3865-3892.
import { usablePhoto, thumbUrl, NO_PHOTO_SVG, type TreeLike } from "./images";

function esc(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

export function browseCard(href: string, name: string, sub: string, face: string | null): string {
  const ph = face
    ? `<span class="exc-ph"><img src="${esc(face)}" alt="" loading="lazy"></span>`
    : NO_PHOTO_SVG.replace('class="ctry-ph ctry-noph"', 'class="exc-ph ctry-noph"');
  return `<a class="exc-card" href="${href}">${ph}<span class="exc-body"><b>${esc(name)}</b><span>${sub}</span></span></a>`;
}

interface CollectionEntryLike {
  city_slug: string;
  tree_id: string;
}
interface CityLike {
  data: { trees: TreeLike[] };
}

/** First entry in the collection that has a usable photo. */
export function collectionFace(
  entries: CollectionEntryLike[],
  citiesBySlug: Map<string, CityLike>,
): string | null {
  for (const e of entries) {
    const entry = citiesBySlug.get(e.city_slug);
    if (!entry) continue;
    for (const t of entry.data.trees) {
      if (t.id === e.tree_id) {
        const p = usablePhoto(t);
        if (p?.url) return thumbUrl(p.url, 400);
      }
    }
  }
  return null;
}
