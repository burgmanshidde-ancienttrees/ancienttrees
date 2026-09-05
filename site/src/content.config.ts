// Content collections mirroring data/*.json, read directly from the repo's
// data/ directory (Python's output, unchanged). Zod schemas here are the
// earlier, stricter replacement for build_site.py's ERRORS.append() pattern:
// a malformed entry fails at content-load time, before any page template
// runs, rather than after render_page() builds the string.
import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const photoSchema = z
  .object({
    url: z.string().nullable().optional(),
    license: z.string().nullable().optional(),
    attribution: z.string().nullable().optional(),
    status: z.enum(["missing", "found_needs_check", "approved", "held"]).optional(),
    // Recorded by scripts/photo_check.py. Zod strips keys it does not name, so
    // leaving these out meant the app feed shipped 353 photos with null
    // dimensions while the data files held them all along.
    width: z.number().int().nullable().optional(),
    height: z.number().int().nullable().optional(),
    note: z.string().nullable().optional(),
    // A photograph a reader sent us, and the account it came from. Both are
    // named here because zod strips what it does not name, and a stripped
    // contributor_user_id is a photograph that can never be taken down:
    // scripts/photo_takedown.py keeps the deletion promise by asking whether
    // that account still exists, and it can only ask about an id it can see.
    // preflight refuses one without the other in either direction.
    source: z.enum(["contributor"]).nullable().optional(),
    contributor_user_id: z.string().nullable().optional(),
    // Set when the account behind a published photograph was deleted
    // (2026-09-04). The picture stays under the licence in /terms and the
    // person comes off it, so this is the state where a contributor photo
    // legitimately has no contributor_user_id. Named here for the same reason
    // as the two above: zod strips what it does not name, and a stripped flag
    // would send photo_takedown.py back to Supabase every night to ask about
    // an account that is already gone.
    unlinked: z.boolean().nullable().optional(),
  })
  .partial()
  .optional();

const bestTimeSchema = z
  .object({
    months: z.array(z.number().int().min(1).max(12)),
    label: z.string(),
    // CLAUDE.md documents flowers/fruit/autumn colour/catkins/fresh leaves/
    // bare silhouette, but real data also carries "flowering" and "blossom"
    // as synonyms (e.g. data/cities/berlin.json). build_site.py doesn't gate
    // on this value either, it only derives a display icon from it, so this
    // stays a free string rather than a strict enum that would reject valid
    // published trees.
    kind: z.string().optional(),
  })
  .optional();

export const treeSchema = z.object({
  id: z.string(),
  name: z.string(),
  species: z.string(),
  age_estimate: z.string().optional(),
  age_min: z.number().nullable().optional(),
  age_max: z.number().nullable().optional(),
  // Trunk girth at breast height, the one measurement registers agree on and
  // the only "how big" number that is measured rather than estimated. Declared
  // here because zod strips what it does not know, which is why the thickest
  // ranking came out empty the first time it built (2026-08-21).
  girth_cm: z.number().nullable().optional(),
  // Height in metres, from a register's own measurement or a plaque, never
  // read out of our own prose: a story sentence about height is as often
  // about the species, the neighbour, or the tree before a storm took its
  // top off. scripts/heights.py fills it; a hand-read figure wins.
  height_m: z.number().nullable().optional(),
  location: z.object({
    address: z.string().optional(),
    latitude: z.number().nullable().optional(),
    longitude: z.number().nullable().optional(),
    neighbourhood: z.string().optional(),
  }),
  story: z.string().optional(),
  verified_sources: z.array(z.string()).optional(),
  access: z.string().optional(),
  /// True when getting to this tree needs a ticket. Written by
  /// scripts/paid_entry.py from the access prose, and only where that prose is
  /// unambiguous: a badge that tells somebody to pay for a free garden is worse
  /// than no badge.
  paid_entry: z.boolean().optional(),
  transport: z.string().optional(),
  photo: photoSchema,
  curation_status: z.enum(["ai_generated", "hidde_approved", "flagged"]).optional(),
  location_precision: z.enum(["confirmed", "approximate"]).optional(),
  /** Which tree it is, once you are standing there. One plain sentence.
   *
   * Added 2026-08-12 after a journalist at the Brabants Dagblad walked to the
   * Norway Maple of Bastion Oranje and could not tell which tree it was,
   * because several similar ones stand on the same rampart. Our own story on
   * that page already said a second, younger Norway maple grows beside it. We
   * knew and the page still sent him to a spot without telling him what to
   * look at, and his trust in the whole site dropped, which is the correct
   * response.
   *
   * location_precision does not cover this and cannot: it answers WHERE, and
   * this answers WHICH. A pin can be exact to the metre and still useless
   * among five similar trunks. Both are honesty fields and they fail
   * separately.
   *
   * What belongs here: the thing you look at. Relative size against its
   * neighbours, position against a gate, path, bench or building, a fork or
   * lean, a plaque. "It stands alone, there is nothing else near it" is a
   * good value and often the true one. What never belongs here: praise, the
   * species, directions to the spot, or an invented feature. Where a tree
   * genuinely cannot be told apart, say so here rather than leave it empty,
   * because a visitor deserves to know that before the walk rather than
   * after. */
  how_to_recognise: z.string().optional(),
  label: z.string().optional(),
  notes: z.string().optional(),
  best_time: bestTimeSchema,
  // Kept only so old files still validate. NEVER render this and never write a
  // new one: Hidde, 2026-08-11, "privacy technisch echt een no go... ookal is
  // het via formulier niet meer doen nooit". A person's name is not ours to
  // publish, whatever channel it arrived through.
  submitted_by: z.string().optional(),
});

const cities = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "../data/cities" }),
  schema: z.object({
    city: z.string(),
    country: z.string(),
    /** What kind of place this is. A city unless it says otherwise.
     *
     * Blueprint v1.15 (2026-08-28): `[city]` means a PLACE, which may be a
     * city, a region, a national park or a forest, because the trees worth
     * having most often belong to none of the first. General Sherman stands in
     * Sequoia National Park; of sixty famous American trees only nine are
     * within forty kilometres of a city we publish.
     *
     * The only thing this field changes is where the place is LISTED: /cities
     * shows cities, because an index of cities that is not a list of cities is
     * the first step to a page nobody trusts. A region belongs on its country
     * page and in collections. Every contract, title, schema and link minimum
     * is identical either way. */
    kind: z.enum(["city", "region", "park", "forest"]).optional(),
    // What KIND of place this page covers. Added 2026-08-17 with Tenerife, the
    // first island: an island is an ordinary place in the one queue and ships
    // under the existing contracts, but it behaves differently in one way a
    // reader feels immediately, which is that its trees are a drive apart
    // rather than a walk. Explore groups on this; nothing else branches on it,
    // and a missing value means an ordinary city.
    kind: z.enum(["city", "island"]).optional(),
    status: z.enum(["needs_curation", "curated", "published"]).optional(),
    intro: z.string().optional(),
    meta_description: z.string().optional(),
    question_answer: z.string().optional(),
    question_meta: z.string().optional(),
    question_context: z.string().optional(),
    faq: z.array(z.object({ q: z.string(), a: z.string() })).optional(),
    hero_tree_id: z.string().nullable().optional(),
    oldest_tree_id: z.string().nullable().optional(),
    // In practice this is sometimes a boolean and sometimes an editorial
    // note string (e.g. data/cities/zaragoza.json); it's an internal signal,
    // not a rendered field, so accept either rather than reject real data.
    not_ready_to_publish: z.union([z.boolean(), z.string()]).optional(),
    trees: z.array(treeSchema).default([]),
  }),
});

const parks = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "../data/parks" }),
  schema: z.object({
    city_slug: z.string(),
    park: z.string(),
    slug: z.string(),
    name: z.string(),
    title: z.string().optional(),
    meta_description: z.string().optional(),
    intro: z.string(),
    official_name: z.string().optional(),
    official_url: z.string().optional(),
  }),
});

const species = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "../data/species" }),
  schema: z.object({
    common_name: z.string(),
    scientific_name: z.string(),
    slug: z.string(),
    title: z.string().optional(),
    meta_description: z.string().optional(),
    intro: z.string(),
    // The photograph this species shows on a card, by tree id. Ranking on
    // size and shape gets a good picture; it cannot tell a bare winter crown
    // from a tree in leaf, or a street with parked cars from a portrait
    // (Hidde, 2026-08-21, on the London Plane and Ginkgo cards). This is the
    // hero_tree_id a city already has, for the groupings that lacked one.
    face_tree_id: z.string().optional(),
  }),
});

const countries = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "../data/countries" }),
  schema: z.object({
    country: z.string(),
    slug: z.string(),
    article: z.string().optional(),
    title: z.string().optional(),
    meta_description: z.string().optional(),
    intro: z.string(),
    register_note: z.string().optional(),
  }),
});

// Named collectionPages (not "collections") because Astro's content config
// reserves that name for the top-level export mapping every collection.
const collectionPages = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "../data/collections" }),
  schema: z.object({
    slug: z.string(),
    title: z.string(),
    seo_title: z.string().optional(),
    status: z.string().optional(),
    meta_description: z.string().optional(),
    intro: z.string(),
    // A collection whose entry list is COMPUTED rather than curated, the
    // pattern Contract F already uses for species pages (blueprint v1.13,
    // Hidde's yes 2026-08-21). "oldest" ranks every tree whose age's lower
    // bound clears 400 years, oldest first, and re-ranks itself on every
    // build, so finding an older tree updates the page by itself. `entries`
    // stays: a curated note on a tree in the ranking is still used for that
    // tree, so the hand-written lines are not thrown away.
    // "autumn" and "harvest" (2026-09-05) rank on best_time instead of on a
    // measurement: same shape, same contract, a different column of the same
    // data. They exist because season is one of the four verbs and the only
    // one no collection served.
    generated: z
      .enum(["oldest", "thickest", "tallest", "autumn", "harvest"])
      .optional(),
    entries: z.array(
      z.object({
        city_slug: z.string(),
        tree_id: z.string(),
        note: z.string(),
      })
    ),
  }),
});

export const collections = { cities, parks, species, countries, collectionPages };
