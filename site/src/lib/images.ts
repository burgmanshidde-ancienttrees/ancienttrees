// Ported from thumb_url()/img_srcset()/credit_required()/usable_photo(),
// build_site.py:2441-2518. qa.py's image checks (full-resolution Wikimedia
// originals, iNaturalist originals, wiki File: pages as img src) depend on
// every rendered image going through thumbUrl/imgSrcset, same as today.

// The no-photo placeholder mark used in country-page city rows and every
// browse_card() (cities/species/collections indexes, build_site.py:3868-3877,
// 4148-4152): an honest "no photo yet" state rather than an empty grey hole.
export const NO_PHOTO_SVG =
  '<span class="ctry-ph ctry-noph" aria-hidden="true">' +
  '<svg viewBox="0 0 68 64" fill="none"><ellipse cx="34" cy="24" rx="24" ry="16" fill="currentColor"/>' +
  '<circle cx="20" cy="23" r="11" fill="currentColor"/><circle cx="48" cy="23" r="11" fill="currentColor"/>' +
  '<circle cx="34" cy="12" r="11" fill="currentColor"/>' +
  '<path d="M31 62 h5.6 l-1.2-16 h-3.2z" fill="currentColor"/></svg></span>';

function esc(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/** A right-sized image URL for the big three sources, original otherwise. */
export function thumbUrl(url: string, width: number): string {
  try {
    if (url.includes("upload.wikimedia.org/wikipedia/commons/") && !url.includes("/thumb/")) {
      const [head, tail] = splitOnce(url, "/wikipedia/commons/");
      const fname = tail.split("/").pop() ?? "";
      if (!/\.(jpe?g|png|gif)$/i.test(fname)) return url;
      // Wikimedia only serves fixed thumbnail buckets since 2024 (probed
      // 2026-07-31: 250/330/500/960 are live, 400/800 are 400s).
      const buckets = [250, 330, 500, 960];
      let w = buckets.find((b) => width <= b);
      if (w === undefined) w = 960; // cap: largest bucket Wikimedia serves
      return `${head}/wikipedia/commons/thumb/${tail}/${w}px-${fname}`;
    }
    if (url.includes("images.unsplash.com/")) {
      return `${url.split("?")[0]}?q=80&w=${width}&auto=format&fit=crop`;
    }
    const m = url.match(
      /^(https:\/\/(?:static\.inaturalist\.org|inaturalist-open-data\.s3\.amazonaws\.com)\/photos\/[^/]+\/)(original|large|medium)(\.[A-Za-z]+)(.*)$/
    );
    if (m) {
      const size = width <= 500 ? "medium" : "large";
      return `${m[1]}${size}${m[3]}${m[4]}`;
    }
  } catch {
    // fall through to returning the original url
  }
  return url;
}

function splitOnce(s: string, sep: string): [string, string] {
  const i = s.indexOf(sep);
  if (i === -1) return [s, ""];
  return [s.slice(0, i), s.slice(i + sep.length)];
}

/** src/srcset/sizes attribute string for a photo url, ready to spread into an <img>. */
export function imgSrcset(url: string, widths: number[], sizes: string) {
  const seen = new Set<string>();
  const pairs: [string, number][] = [];
  for (const w of widths) {
    const u = thumbUrl(url, w);
    if (!seen.has(u)) {
      seen.add(u);
      pairs.push([u, w]);
    }
  }
  const srcset = pairs.map(([u, w]) => `${u} ${w}w`).join(", ");
  return {
    src: thumbUrl(url, widths[0]),
    srcset,
    sizes,
  };
}

/** HTML attribute string form, for contexts building raw markup rather than JSX-like props. */
export function imgSrcsetAttrs(url: string, widths: number[], sizes: string): string {
  const { src, srcset, sizes: s } = imgSrcset(url, widths, sizes);
  return `src="${esc(src)}" srcset="${esc(srcset)}" sizes="${esc(s)}"`;
}

/** Whether the licence forces a visible on-page credit (Hidde, 2026-07-29:
 * record always, display only when the licence requires it). */
export function creditRequired(licenseStr?: string | null): boolean {
  const lic = (licenseStr ?? "").toLowerCase();
  if (!lic) return true;
  const free = ["cc0", "public domain", "publicdomain", "unsplash", "pdm"];
  return !free.some((f) => lic.includes(f));
}

export interface Photo {
  url?: string | null;
  license?: string | null;
  attribution?: string | null;
  status?: string | null;
}

export interface TreeLike {
  id?: string;
  photo?: Photo | null;
}

/** Return the photo if it has a URL, license and attribution and is cleared
 * for display; otherwise null. One gate for every page type. Unlike the
 * Python version this does not push to a global ERRORS list on a wiki
 * File: page; callers that need build-time validation should check that
 * themselves (see the content collection Zod schema, which is the earlier
 * and stricter place for this in the Astro build). */
export function usablePhoto(tree: TreeLike): Photo | null {
  const photo = tree.photo ?? {};
  if (
    photo.url &&
    photo.license &&
    photo.attribution &&
    (photo.status === "approved" || photo.status === "found_needs_check")
  ) {
    if (photo.url.includes("/wiki/File:")) return null;
    return photo;
  }
  return null;
}

export interface CityEntryLike {
  hero_tree_id?: string | null;
  trees?: TreeLike[];
}

/** The city's face photo url at card size: hero_tree_id first, else the
 * first tree with a usable photo, else null. */
export function cityFace(cityData: CityEntryLike, width = 400): string | null {
  const hero = cityData.hero_tree_id;
  const trees = cityData.trees ?? [];
  if (hero) {
    const t = trees.find((t) => t.id === hero);
    if (t) {
      const p = usablePhoto(t);
      if (p?.url) return thumbUrl(p.url, width);
    }
  }
  for (const t of trees) {
    const p = usablePhoto(t);
    if (p?.url) return thumbUrl(p.url, width);
  }
  return null;
}
