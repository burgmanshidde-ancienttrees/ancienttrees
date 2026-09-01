import fs from "node:fs";
import path from "node:path";
import { DATA } from "./data-dir";

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


/** The photographs we host ourselves, keyed by their original URL.
 *
 * Wikimedia does not block us and never has; it RATE-LIMITS. Measured
 * 2026-08-27, a burst of 24 thumbnails fetched the way a card grid fetches
 * them came back 13 x HTTP 429 and 11 x 200, which is why the tree
 * photographs stopped loading in the app. Nothing broke: the app grew past a
 * threshold that CURATION.md recorded on 2026-08-08 as "roughly one request
 * every three seconds runs clean".
 *
 * So the copies live under site/public/photos and this map points at them.
 * Read lazily and cached, because thumbUrl() is called thousands of times in
 * a build, and behind a try/catch so a missing manifest degrades to the
 * Wikimedia URL rather than failing the build.
 *
 * It sits HERE rather than in the app because thumbUrl() is the one function
 * both surfaces already share: the website's imgSrcset and the feed's
 * thumb/hero fields both call it, so one change moves both. That is the same
 * rule the feed follows everywhere else, an answer travelling as data instead
 * of a rule written twice.
 */
let VENDORED: Record<string, { base: string; widths: number[] }> | null = null;
function vendored(): Record<string, { base: string; widths: number[] }> {
  if (VENDORED) return VENDORED;
  try {
    VENDORED = JSON.parse(
      fs.readFileSync(path.join(DATA, "photo-manifest.json"), "utf-8")
    ).photos ?? {};
  } catch {
    VENDORED = {};
  }
  return VENDORED!;
}

/** The vendored copy at this width, or null if we do not host one.
 *
 * Only widths we actually have, and never a smaller file standing in for a
 * bigger one. We vendor the CARD size and not the hero, because the rate limit
 * is a burst problem: a grid asks for two dozen images at once and Wikimedia
 * cuts off after about twelve, while a hero is one image on one screen and
 * never bursts. Serving a 500px file where a 960px hero was asked for would
 * trade a fixed bug for a soft photograph, which is the exact complaint that
 * sent the first version of this back. */
function localCopy(url: string, width: number): string | null {
  const hit = vendored()[url];
  if (!hit) return null;
  const w = hit.widths.find((x) => width <= x);
  return w ? `/photos/${hit.base}-${w}.jpg` : null;
}

/** A right-sized image URL for the big three sources, original otherwise. */
export function thumbUrl(url: string, width: number): string {
  // Our own copy wins whenever we have one: same picture, a host that does
  // not rate-limit a card grid into 429s.
  const mine = localCopy(url, width);
  if (mine) return mine;
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

/** The intrinsic width and height a photo block records, or zeros when either
 * is missing.
 *
 * These become the `width` and `height` attributes on the rendered `<img>`, and
 * their only job there is to reserve the space before the file arrives. Without
 * them a tree page paints its story directly under the chips and then throws it
 * down the page the moment the photograph loads: measured on /ede/beuk-marjan
 * on 2026-09-01, 518 pixels at 375 wide and over a thousand on a desktop, with
 * the image above the fold both times. That is a Cumulative Layout Shift, which
 * Google ranks on, and ranking is the binding constraint on this project.
 *
 * The numbers are the file's real dimensions, not the thumbnail's; only the
 * RATIO is used, and a bucketed Wikimedia thumbnail keeps the ratio of the
 * original it was cut from. Zeros mean a photograph nobody has measured yet,
 * and then the markup says nothing rather than something wrong:
 * scripts/photo_res.py fills the pair in on its next pass and the daily digest
 * runs it. Every photo we render carries both today (413 of 413, checked
 * 2026-09-01); this is the honest fallback for the next one added by hand.
 *
 * A caller that uses this MUST let the height be auto in CSS. The height
 * attribute is a presentational hint, so `width: 100%` with a bare height
 * attribute paints a 343 by 4928 smear rather than a photograph. */
export function photoDims(p: unknown): { width: number; height: number } {
  const o = p as { width?: number; height?: number } | null;
  const w = o?.width;
  const h = o?.height;
  return typeof w === "number" && w > 0 && typeof h === "number" && h > 0
    ? { width: w, height: h }
    : { width: 0, height: 0 };
}

/** src/srcset/sizes attribute string for a photo url, ready to spread into an <img>.
 *
 * `intrinsic` is the file's real width. Offering a 960w candidate for a 375px
 * file is not harmless: the browser picks it, gets 375 pixels back, and paints
 * them upscaled. Capping the candidates at what exists keeps the markup honest
 * about the file, which is also what makes the qa check meaningful. */
export function imgSrcset(
  url: string,
  widths: number[],
  sizes: string,
  intrinsic = 0,
  intrinsicHeight = 0,
) {
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
  const out: { src: string; srcset: string; sizes: string; width?: number; height?: number } = {
    src: thumbUrl(url, widths[0]),
    srcset,
    sizes,
  };
  // Both or neither. A width without a height gives the browser no ratio and
  // only a presentational hint, which is worse than saying nothing.
  if (intrinsic > 0 && intrinsicHeight > 0) {
    out.width = intrinsic;
    out.height = intrinsicHeight;
  }
  return out;
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

/** The photographer's name as it should be PRINTED, with the host dropped.
 *
 * "Foo Bar, via Wikimedia Commons" becomes "Foo Bar". CC BY and BY-SA ask for
 * the author and the terms; the host is neither, and it doubled the length of
 * every credit on the site while telling the reader nothing they needed (Hidde,
 * 2026-08-21: "als de foto referentie subtieler kan", and on 2026-08-26, asked
 * which of the two wordings wins: "ingekort natuurlijk").
 *
 * One implementation, because there were two: this rule lived in Swift and the
 * website printed the long form, so the same photograph was credited two ways
 * depending on which screen you held. The website calls this directly and the
 * app reads its output from the feed as `attribution_short`.
 *
 * Where the host is all we have, it stays: a photograph with no attributable
 * name still has to say where it came from.
 */
const CREDIT_HOSTS = [
  ", via Wikimedia Commons", " via Wikimedia Commons", ", Wikimedia Commons",
  ", via Flickr", ", via iNaturalist",
];

export function creditName(attribution?: string | null): string | null {
  const raw = (attribution ?? "").trim();
  if (!raw) return null;
  for (const host of CREDIT_HOSTS) {
    if (raw.endsWith(host)) {
      const shorter = raw.slice(0, raw.length - host.length).trim();
      return shorter || raw;
    }
  }
  return raw;
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

/** One tree ranked as a possible card face. Three properties, because they are
 * all a machine can judge about a photograph: has it enough pixels for the box,
 * is it landscape, and how wide is it. Whether the TREE is the subject is a
 * person's judgement and travels as a pin instead.
 *
 * WHY THIS RETURNS THE TREE and not a url (2026-08-25). Every card face used to
 * be decided as a url, three times over in this file and again on four pages,
 * and the app could not read any of it: it took the first tree with a
 * photograph, so a city's face on a phone was a different picture from the same
 * city's face on the web, and no pin reached the app at all. A tree ID is the
 * thing both surfaces can agree on, because it is data that travels in the feed
 * rather than a rule that has to be written twice.
 */
interface FaceRank<T> {
  tree: T; url: string; big: boolean; landscape: boolean; w: number;
  /** Wider than two to one. Almost nothing that shape is a picture of a tree:
   * it is a valley, a park, a skyline or a stitched panorama, and a card crops
   * it to a letterbox where the tree, if there is one, is a smudge. */
  panorama: boolean;
}

function faceRank<T extends TreeLike>(t: T | undefined): FaceRank<T> | null {
  if (!t) return null;
  const p = usablePhoto(t) as { url?: string; width?: number; height?: number } | null;
  if (!p?.url) return null;
  const w = photoWidth(p);
  const h = p.height ?? 0;
  return { tree: t, url: p.url, big: w === 0 || w >= MIN_CARD_PX,
           landscape: w > 0 && h > 0 && w >= h, w,
           panorama: w > 0 && h > 0 && w / h > 2 };
}

/** The best photograph in a set for a letterbox box: enough pixels first,
 * landscape second, and a stable id third. Panoramas are set aside unless there
 * is nothing else. `exclude` lets a page that lays out several
 * shelves at once avoid printing one photograph twice. */
export function bestFaceTree<T extends TreeLike>(trees: T[], exclude?: Set<string>): T | null {
  const usable = trees
    .map((t) => faceRank(t))
    .filter((c): c is FaceRank<T> => c !== null && !(exclude?.has(c.url)));
  // Panoramas are set aside rather than thrown away. A city whose every
  // photograph is a wide one still needs a face, and a poor face beats an empty
  // card: the whole point of this shelf is that it shows pictures.
  const narrow = usable.filter((c) => !c.panorama);
  const best = (narrow.length ? narrow : usable)
    .sort((a, b) => Number(b.big) - Number(a.big)
      || Number(b.landscape) - Number(a.landscape)
      // STABLE, not widest. The final tiebreaker used to be the widest
      // photograph, and that is worse than random for this job: a wide shot of
      // a place beats a portrait of a tree every single time, so the face of a
      // city became whichever picture had the most pixels rather than whichever
      // showed a tree. Rome wore a staircase and a fountain, Dublin wore a park
      // overview, and Hidde named eight cities and countries in a row before
      // anybody looked at why (2026-08-28).
      //
      // A machine cannot tell a good photograph of a tree from a good
      // photograph of a park. What it can do is stop actively preferring the
      // second. The id is arbitrary and that is the point: arbitrary beats
      // biased, and a person can override any of it by pinning a face.
      // ?? "" because TreeLike.id is optional, and an undefined here is
      // both a type error and a crash. That is the exact shape of the bug that
      // took every deploy down this morning.
      || (a.tree.id ?? "").localeCompare(b.tree.id ?? ""))[0];
  return best ? best.tree : null;
}

/** The tree that fronts a city: its pinned hero when that photograph is big
 * enough for the box, else the best one in the city, else the hero anyway. */
export function cityFaceTree<T extends TreeLike>(
  cityData: { hero_tree_id?: string | null; trees?: T[] },
): T | null {
  const trees = cityData.trees ?? [];
  const hero = cityData.hero_tree_id
    ? faceRank(trees.find((t) => t.id === cityData.hero_tree_id)) : null;
  if (hero?.big) return hero.tree;
  const best = bestFaceTree(trees);
  if (best) return best;
  return hero ? hero.tree : null;
}

/** The tree that fronts a species: the pinned one when a person set it, else
 * the best in the set. A pin ignores `exclude`, because somebody chose it. */
export function speciesFaceTree<T extends TreeLike>(
  faceTreeId: string | null | undefined,
  trees: T[],
  exclude?: Set<string>,
): T | null {
  const pinned = faceTreeId ? faceRank(trees.find((t) => t.id === faceTreeId)) : null;
  if (pinned) return pinned.tree;
  return bestFaceTree(trees, exclude);
}

/** The tree that fronts a park, and this is the weak one: the FIRST tree with a
 * usable photograph, which is the rule every other card here has stopped using.
 * Kept exactly as /parks had it so that moving the choice into the feed changes
 * nothing a reader can see. Improving it is now one edit in one place instead of
 * one per surface, which is the whole point of this module. */
export function parkFaceTree<T extends TreeLike>(trees: T[]): T | null {
  return trees.find((t) => Boolean(usablePhoto(t)?.url)) ?? null;
}

/** The city's face photo url at card size. Thin wrapper over cityFaceTree, so
 * the website renders exactly the picture the feed names. */
export function cityFace(cityData: CityEntryLike, width = 400): string | null {
  const t = cityFaceTree(cityData);
  const url = t ? usablePhoto(t)?.url : null;
  return url ? thumbUrl(url, width) : null;
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
  const t = speciesFaceTree(faceTreeId, trees, exclude);
  const url = t ? usablePhoto(t)?.url : null;
  return url ? thumbUrl(url, width) : null;
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
