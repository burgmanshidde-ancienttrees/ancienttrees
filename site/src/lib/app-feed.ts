// The dataset an app reads, so new trees reach it without a new build
// (Hidde, 2026-08-18: "hoe zorgen we dat als wij meer bomen vinden dat die
// dan in de app komen zonder dat we een nieuwe app hoeven up te loaden?").
//
// The mechanism, and it is the ordinary one: an app ships with a snapshot so
// it works on first launch and offline, then asks a tiny version file whether
// anything changed, and pulls the full dataset only when it has. Data is not
// code, so none of this touches App Store review; a new SCREEN needs a new
// build, a new tree does not.
//
// One file rather than per-city chunks, measured rather than assumed: 1,377
// trees are 2.36 MB raw and 0.76 MB gzipped, and even several times that stays
// a single comfortable download. Chunking would buy nothing today and cost a
// second thing that can drift out of sync.
//
// The honesty fields ride along on purpose. location_precision travels with
// every tree so an app can say "we know the park, not the trunk" exactly where
// the website says it, and a photo carries its licence and attribution so an
// app cannot show the picture while dropping the credit the licence demands.
import type { CityEntry } from "./trees";
import { peakFor } from "./phenology";
import { renderableTrees, slugify } from "./trees";
import { usablePhoto, thumbUrl, cardUrl, creditRequired, creditName, creditText } from "./images";
import { BASE_URL } from "./schema";

/** The feed is read by an app on somebody's phone, which has no page to
 * resolve a relative path against. thumbUrl() returns "/photos/..." for the
 * photographs we host ourselves, so the feed absolutises. The website does
 * not: a relative src is correct there and one byte shorter. */
function absolute(u: string): string {
  return u.startsWith("/") ? `${BASE_URL}${u}` : u;
}

/** The one line every feed carries, because a JSON file travels further than
 *  a page does and arrives with no footer attached to it. It says who the
 *  records belong to and where the terms are, so nobody can take the dataset
 *  for open data by accident. Records, not facts: a fact about a tree belongs
 *  to nobody, the checked collection of them is ours. */
export const FEED_LICENCE =
  "(c) Ancient Trees, ancienttrees.app. Verified records, not open data: " +
  "reuse by permission, see ancienttrees.app/terms and ancienttrees.app/sources. " +
  "Photographs carry their own licences and credits, given per tree.";

export interface FeedTree {
  id: string;
  name: string;
  species: string | null;
  age: string | null;
  /// Numeric bounds where the city file has them: the app sorts an
  /// "oldest trees" shelf on these, which a prose age cannot do.
  age_min: number | null;
  age_max: number | null;
  lat: number;
  lng: number;
  city: string;
  city_slug: string;
  country: string;
  neighbourhood: string | null;
  access: string | null;
  /// Getting there needs a ticket. The app puts a mark on the pin and the
  /// walk planner leaves these out.
  paid_entry?: boolean;
  transport: string | null;
  precision: string | null;
  best_time: unknown;
  /** The species' one peak of the year, already shifted for this tree's
   * latitude, with the animation its pin should run. One field, computed once
   * on the server, so the app and the website light up the same tree on the
   * same day rather than each deciding for itself (Hidde, 2026-08-21: app en
   * web gelijk trekken). Null where the species has no peak, and inside the
   * tropics, where phenologyFor refuses to guess a calendar at all. */
  peak: { months: number[]; effect: string; colour: string; level?: string } | null;
  story: string | null;
  url: string;
  /** The photograph, with the two sizes a client actually paints and the
   * licence question already answered.
   *
   * `thumb` and `hero` exist because the app had its own copy of thumbUrl(),
   * hand-ported into Swift, and the first version of that port asked Wikimedia
   * for 800px and got a 400 back on every request: Wikimedia has served only
   * fixed buckets since 2024, the website had already probed which ones are
   * live, and a second implementation had to learn it again. A resolved url is
   * data. A bucket table is a rule, and a rule written twice drifts.
   *
   * `credit_required` is the same argument with a smaller blast radius. The web
   * asks whether the LICENCE obliges a name; the app's own version asked
   * whether the string contains "BY", which credits "Provided by the Fundacao
   * Mata do Bucaco" for a licence that obliges nothing. Four live photographs
   * disagreed across the two surfaces. */
  photo: { url: string; license: string | null; attribution: string | null;
            width: number | null; height: number | null;
            thumb: string; hero: string; credit_required: boolean;
            attribution_short: string | null; credit_line: string | null } | null;
}

export function feedTrees(cities: CityEntry[]): FeedTree[] {
  const out: FeedTree[] = [];
  for (const city of cities) {
    for (const t of renderableTrees(city)) {
      const loc = t.location ?? ({} as any);
      if (loc.latitude == null || loc.longitude == null) continue;
      const p = usablePhoto(t);
      out.push({
        id: t.id,
        name: t.name,
        species: t.species ?? null,
        age: t.age_estimate ?? null,
        age_min: (t as any).age_min ?? null,
        age_max: (t as any).age_max ?? null,
        lat: loc.latitude,
        lng: loc.longitude,
        city: city.data.city,
        city_slug: city.id,
        country: city.data.country,
        neighbourhood: loc.neighbourhood ?? null,
        access: t.access ?? null,
        ...(t.paid_entry ? { paid_entry: true } : {}),
        transport: t.transport ?? null,
        precision: t.location_precision ?? null,
        best_time: t.best_time ?? null,
        peak: (() => {
          const pk = peakFor(t, loc.latitude);
          return pk?.map ? { months: pk.months, effect: pk.map.effect, colour: pk.map.colour, ...(pk.level ? { level: pk.level } : {}) } : null;
        })(),
        story: t.story ?? null,
        url: `/${city.id}/${slugify(t.name)}`,
        photo: p?.url
          ? {
              url: p.url,
              license: p.license ?? null,
              attribution: p.attribution ?? null,
              // So a client can lay out a list before the first byte of image
              // arrives, and can tell when a file changed underneath us.
              width: (p as any).width ?? null,
              height: (p as any).height ?? null,
              // Card size and full-width size, resolved here so no client
              // needs to know how Wikimedia names a thumbnail.
              thumb: absolute(cardUrl(p.url)),
              // 1280, not 960. A hero fills the width of the phone, which is
              // about 1180 physical pixels on a 3x screen, and 960 was not a
              // considered choice: it was the largest Wikimedia width anyone
              // here had probed. 1280 and 1920 are served too (re-probed
              // 2026-09-03), so the cap was ours rather than theirs.
              //
              // Only the hero moves. A hero is one image on one screen and
              // never bursts, which is why it may come straight from Wikimedia;
              // the card is what a shelf loads by the dozen and it stays on our
              // own domain at the width we host.
              hero: absolute(thumbUrl(p.url, 1280)),
              credit_required: creditRequired(p.license),
              // The name as it should be PRINTED, host dropped. The trimming
              // rule lived in Swift and the website printed the long form, so
              // one photograph was credited two ways (Hidde, 2026-08-26, asked
              // which wins: "ingekort natuurlijk").
              attribution_short: creditName(p.attribution),
              // The finished line, name and terms together, because the app
              // was joining those two itself and a gift breaks that join: its
              // licence field is a sentence ("Provided by Paulo V. Araujo
              // (Dias com Arvores), all rights reserved") rather than a label,
              // so the phone printed the giver's name twice and the words "all
              // rights reserved" under a photograph he gave us. An answer in
              // the feed, not a rule written twice.
              credit_line: creditText(p.attribution, p.license),
            }
          : null,
      });
    }
  }
  out.sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  return out;
}

/** A short content hash, so the version changes exactly when the data does
 *  and never merely because a build ran. */
export async function feedVersion(body: string): Promise<string> {
  const bytes = new TextEncoder().encode(body);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].slice(0, 8)
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}
