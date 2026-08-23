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

/** Image urls for METADATA only: og:image and schema.org `image`. Never for an
 * `<img>` tag, which must keep going through imgSrcset (qa.py enforces that,
 * and it only inspects img tags, which is why pointing metadata at a bigger
 * file is safe).
 *
 * Why this exists (2026-08-11). Hidde noticed that of 95 city pages only
 * /lisbon showed a tree photograph in Google's results and every other page
 * showed our generic logo. Two causes: city pages never set og:image from
 * their own photo, so they fell back to og-default.png, and NO page declared
 * `image` in its structured data at all, leaving Google to guess. A thumbnail
 * beside a result moves click-through more than any title rewrite, and this
 * site's whole problem is click-through.
 *
 * Returns largest-first, because Google takes the first usable one and wants
 * at least 1200px wide for a prominent image. Wikimedia only serves fixed
 * thumbnail buckets up to 960, so the original is included for the crawler
 * (fetched once, by a robot) while og:image keeps to 960 (fetched by social
 * scrapers, some of which cap around 5MB).
 */
export function metaImageUrls(url: string): string[] {
  const out: string[] = [];
  const big = thumbUrl(url, 960);
  if (url.includes("upload.wikimedia.org/wikipedia/commons/") && url.includes("/thumb/")) {
    // A thumb url points at .../thumb/a/ab/Name.jpg/500px-Name.jpg; the
    // original is that path with the /thumb/ segment and last part removed.
    const [head, tail] = splitOnce(url, "/wikipedia/commons/thumb/");
    const parts = tail.split("/");
    if (parts.length >= 3) out.push(`${head}/wikipedia/commons/${parts.slice(0, -1).join("/")}`);
  } else if (url.includes("upload.wikimedia.org/wikipedia/commons/")) {
    out.push(url);
  }
  const iNat = url.match(
    /^(https:\/\/(?:static\.inaturalist\.org|inaturalist-open-data\.s3\.amazonaws\.com)\/photos\/[^/]+\/)(original|large|medium)(\.[A-Za-z]+)(.*)$/
  );
  if (iNat) out.push(`${iNat[1]}original${iNat[3]}${iNat[4]}`);
  if (!out.includes(big)) out.push(big);
  return [...new Set(out)];
}

/** The single url to hand a social scraper: big enough to render as a card,
 * small enough that nobody refuses to fetch it. */
export function ogImageUrl(url: string): string {
  return thumbUrl(url, 960);
}

function splitOnce(s: string, sep: string): [string, string] {
  const i = s.indexOf(sep);
  if (i === -1) return [s, ""];
  return [s.slice(0, i), s.slice(i + sep.length)];
}

/** The intrinsic pixel width a photo block records, or 0 when unmeasured.
 * scripts/photo_res.py fills it for every photo and CI keeps it filled. */
export function photoWidth(p: unknown): number {
  const w = (p as { width?: number } | null)?.width;
  return typeof w === "number" && w > 0 ? w : 0;
}

/** The pixels a card and a hero need on a 2x screen. Mirrors MIN_CARD/MIN_HERO
 * in scripts/photo_res.py; scripts/qa.py fails a build that breaks the card
 * one, so a soft thumbnail cannot ship unnoticed again (Hidde, 2026-08-21:
 * "i want a sustainable solution ... that i dont have to spot it every time"). */
export const MIN_CARD_PX = 540;
export const MIN_HERO_PX = 960;

/** src/srcset/sizes attribute string for a photo url, ready to spread into an <img>.
 *
 * `intrinsic` is the file's real width. Offering a 960w candidate for a 375px
 * file is not harmless: the browser picks it, gets 375 pixels back, and paints
 * them upscaled. Capping the candidates at what exists keeps the markup honest
 * about the file, which is also what makes the qa check meaningful. */
export function imgSrcset(url: string, widths: number[], sizes: string, intrinsic = 0) {
  const seen = new Set<string>();
  const pairs: [string, number][] = [];
  const capped = intrinsic > 0 ? widths.filter((w) => w <= intrinsic) : widths;
  for (const w of (capped.length ? capped : [Math.min(...widths)])) {
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
export function imgSrcsetAttrs(url: string, widths: number[], sizes: string, intrinsic = 0): string {
  const { src, srcset, sizes: s } = imgSrcset(url, widths, sizes, intrinsic);
  return `src="${esc(src)}" srcset="${esc(srcset)}" sizes="${esc(s)}"`;
}

/** Does this licence legally oblige us to name somebody on the page?
 *
 * Only CC BY and CC BY-SA and their kin do. Everything else does not: our own
 * photographs, CC0, public domain, the Unsplash licence, and a photograph used
 * with the holder's written permission.
 *
 * This used to work the other way round, returning true unless the licence
 * appeared on a short free-list, which put a credit under everything it did not
 * recognise. Hidde, 2026-08-18: "stop met overal spastisch foto verwijzingen
 * onder zetten, ook de foto die ik in de pekingtuin heb toegevoegd heeft geen
 * referentie nodig." His own photograph of the Pekingtuin oak was captioned
 * "Photo: Ancient Trees (Own photograph)", which is the site crediting itself.
 *
 * CLAUDE.md has said since 2026-07-29 that credits are recorded always and
 * DISPLAYED only when the licence requires it. So this is a bug against an
 * existing rule rather than a new rule, and the default belongs the other way:
 * no credit unless something demands one. */
export function creditRequired(licenseStr?: string | null): boolean {
  const lic = (licenseStr ?? "").toLowerCase();
  if (!lic) return false;
  if (lic.includes("cc0") || lic.includes("public domain") || lic.includes("publicdomain")) return false;
  return /\bcc[ -]?by\b/.test(lic) || lic.includes("attribution")
      || lic.includes("share-alike") || lic.includes("sharealike");
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

/** The city's face photo url at card size: the hero tree when it has a photo
 * big enough for the box, else the biggest landscape photograph in the city,
 * else whatever there is.
 *
 * Hero-or-first-found was how a 375px file came to front a city everywhere
 * (Hidde, 2026-08-21, on soft thumbnails in the map sidebar). The rank is the
 * same one the homepage shelves use: enough pixels first, landscape second,
 * widest third, because these boxes are all letterboxes.
 */
export function cityFace(cityData: CityEntryLike, width = 400): string | null {
  const trees = cityData.trees ?? [];
  const rank = (t: TreeLike | undefined) => {
    if (!t) return null;
    const p = usablePhoto(t) as { url?: string; width?: number; height?: number } | null;
    if (!p?.url) return null;
    const w = photoWidth(p);
    const h = p.height ?? 0;
    return { url: p.url, big: w === 0 || w >= MIN_CARD_PX, landscape: w > 0 && h > 0 && w >= h, w };
  };
  const hero = cityData.hero_tree_id
    ? rank(trees.find((t) => t.id === cityData.hero_tree_id)) : null;
  if (hero?.big) return thumbUrl(hero.url, width);
  const best = trees
    .map(rank)
    .filter((c): c is NonNullable<typeof c> => c !== null)
    .sort((a, b) => Number(b.big) - Number(a.big)
      || Number(b.landscape) - Number(a.landscape) || b.w - a.w)[0];
  if (best) return thumbUrl(best.url, width);
  return hero ? thumbUrl(hero.url, width) : null;
}

/** The species card face: the pinned tree when one is set, else the best
 * photograph in the set for a letterbox.
 *
 * This is cityFace's missing twin and it is missing for a reason worth
 * recording. On 2026-08-21 Hidde said the London Plane and Ginkgo cards were
 * showing the wrong pictures, and `face_tree_id` was added so a person could
 * pin one. It was wired into the homepage shelves by hand and nowhere else, so
 * /species went on taking the first photograph it happened to find. Two days
 * later he opened the Horse Chestnut card and got a close-up of red survey
 * paint around a wound, which no ranking could have caught and a pinned face
 * would have.
 *
 * The lesson is the one CLAUDE.md already draws about hearts and the sign-in
 * dialog: parity wired by hand does not survive the page count. One helper,
 * called from every place that draws a species card.
 *
 * `exclude` lets a caller that lays out several shelves at once avoid showing
 * the same photograph twice; a pinned face ignores it, because a person chose
 * that one on purpose.
 */
export function speciesFace(
  faceTreeId: string | null | undefined,
  trees: TreeLike[],
  width = 400,
  exclude?: Set<string>,
): string | null {
  const rank = (t: TreeLike | undefined) => {
    if (!t) return null;
    const p = usablePhoto(t) as { url?: string; width?: number; height?: number } | null;
    if (!p?.url) return null;
    const w = photoWidth(p);
    const h = p.height ?? 0;
    return { url: p.url, big: w === 0 || w >= MIN_CARD_PX, landscape: w > 0 && h > 0 && w >= h, w };
  };
  const pinned = faceTreeId ? rank(trees.find((t) => t.id === faceTreeId)) : null;
  if (pinned) return thumbUrl(pinned.url, width);
  const best = trees
    .map(rank)
    .filter((c): c is NonNullable<typeof c> => c !== null && !(exclude?.has(c.url)))
    .sort((a, b) => Number(b.big) - Number(a.big)
      || Number(b.landscape) - Number(a.landscape) || b.w - a.w)[0];
  return best ? thumbUrl(best.url, width) : null;
}

/** The same face, as a 1x/2x pair for a fixed-size box. A retina screen paints
 * an 86 point sidebar thumbnail with 172 pixels; asking for 86 is what made
 * those look soft. */
export function cityFaceSrcset(cityData: CityEntryLike, boxWidth: number): { src: string; srcset: string } | null {
  const one = cityFace(cityData, boxWidth);
  if (!one) return null;
  const two = cityFace(cityData, boxWidth * 2);
  return { src: one, srcset: two === one ? one + " 1x" : `${one} 1x, ${two} 2x` };
}
