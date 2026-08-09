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
  location: z.object({
    address: z.string().optional(),
    latitude: z.number().nullable().optional(),
    longitude: z.number().nullable().optional(),
    neighbourhood: z.string().optional(),
  }),
  story: z.string().optional(),
  verified_sources: z.array(z.string()).optional(),
  access: z.string().optional(),
  transport: z.string().optional(),
  photo: photoSchema,
  curation_status: z.enum(["ai_generated", "hidde_approved", "flagged"]).optional(),
  location_precision: z.enum(["confirmed", "approximate"]).optional(),
  label: z.string().optional(),
  notes: z.string().optional(),
  best_time: bestTimeSchema,
  submitted_by: z.string().optional(),
});

const cities = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "../data/cities" }),
  schema: z.object({
    city: z.string(),
    country: z.string(),
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
