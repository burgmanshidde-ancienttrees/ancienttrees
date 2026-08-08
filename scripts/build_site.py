#!/usr/bin/env python3
"""Static site generator for ancienttrees.app.

Builds the four content layers from SEO_GEO_BLUEPRINT.md:
  Contract A  tree pages       /[city]/[tree-slug]
  Contract B  question pages   /[city]/oldest-tree
  Contract C  city pages       /[city]
  Contract D  collection pages /collections/[slug]
  Contract E  about page       /about

Pages are validated against the Layer 2 contracts (title length,
description length, schema presence, internal link minima) before
anything is written. A page that fails validation fails the build.

URLs are extensionless (london.html is served at /london by GitHub
Pages). Old /cities/[slug]/ URLs get redirect stubs.

Reads data/city-list.json, data/cities/*.json, data/collections/*.json,
data/registers/*.json (the register layer: government-designated trees
shown as unlinked, unverified map dots, see CLAUDE.md).
Writes site/dist/. No dependencies beyond the Python 3.9 stdlib.

Usage: python3 scripts/build_site.py
"""

import json
import html
import math
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DIST = ROOT / "site" / "dist"
BASE_URL = "https://ancienttrees.app"
CUSTOM_DOMAIN = "ancienttrees.app"
CONTACT = "hello@ancienttrees.app"

# Paste the public submission form URL here and every contribution button on the
# site switches from a prefilled mailto to the form. Left empty, the site falls
# back to mailto so nothing is ever a dead end.
SUBMISSION_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSd2zQdm6YxndPLk9Ms8Z3YAfA-vymDZs4SDkFQZtJWzj4sb3g/viewform"

# The same form's responses, published as a public CSV. The research runs read
# this to pick up submissions without Hidde in the loop; see CLAUDE.md Step 0b.
# Do not collect email addresses in the form: this sheet is world-readable, and
# the submitter's name is published as a credit anyway.
SUBMISSIONS_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRND_8GK5Pa2Y14STlWuVHwtgyn4quT3E0EcplJ6qqIgHWWzglH_7ZXerP9O3V7xhh-ZqUL9fhlypNx/pub?gid=1337691418&single=true&output=csv"

# Where people can chip in: Patreon, Ko-fi, Buy Me a Coffee, whatever Hidde
# picks. Paste the public page URL here and the button appears on the homepage.
# Deliberately a donation link rather than a paywall, so the content stays free
# and indexable and nobody has to hold a card number or a subscriber list.
# Only Hidde can create this: it is his money and his account (hard list 2).
SUPPORT_URL = ""

# The account track (Hidde, 2026-07-26): the login ships as an unlinked,
# noindexed prototype until his Supabase project and privacy page exist.
# Flipping this to True is his call, made in a session, never by a run.
# Flipped True on 2026-07-30: account deletion verified end-to-end by machine
# (create -> sign in -> delete_user rpc 204 -> user_not_found), which was the
# gate Hidde set before login could go public.
AUTH_ENABLED = True
# Hidde's Supabase project (2026-07-28). The publishable key is public by design.
SUPABASE_URL = "https://caimvxiyrtifilimlkqw.supabase.co"
SUPABASE_KEY = "sb_publishable_qOTuw-LCejk2VhO2J6aXGQ_6X2O2mgb"

# The hero photo (Hidde, 2026-07-29): one fixed image, no rotation. He picked
# the Kevin Young frame and dropped the bank; new candidates only when he
# brings them. Kevin Young, Unsplash License (free incl. commercial, no credit
# required on-page); attribution recorded here per hard rule 4. The visible
# credit overlay was removed on his instruction, which the Unsplash License
# permits; CC tree photos elsewhere keep their visible credits, those licences
# do require them.
HERO_PHOTOS = [
    ("https://images.unsplash.com/photo-1422393682802-921122338109?q=80&w=2400&auto=format&fit=crop",
     "Photo: Kevin Young, Unsplash"),
]

MAPLIBRE_JS = "https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"
MAPLIBRE_CSS = "https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css"
# OpenFreeMap: free vector tiles, no API key, commercial use permitted
MAP_STYLE = "https://tiles.openfreemap.org/styles/positron"

TITLE_MAX = 60
DESC_MAX = 155

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  /* Direction A "Growth Rings" palette, chosen by Hidde 2026-07-27. Interim
     identity: one type family (Gabarito), emphasis via weight and colour,
     never via a second typeface. --serif and --hand are kept as names only
     so nothing breaks, but they now point at the same family on purpose. */
  --cream: #FFFFFF; --cream-dark: #ECEAE3; --ink: #26301E; --ink-mid: #5C6350;
  --ink-light: #8A8B80; --moss: #4A6B2A; --moss-light: #EDF3E3; --surface: #F7F6F1; --shadow: 0 1px 3px rgba(26,32,18,0.08), 0 4px 14px rgba(26,32,18,0.05); --gold: #D9A13F;
  --serif: 'Gabarito', system-ui, sans-serif; --sans: 'Gabarito', system-ui, sans-serif;
  --hand: 'Gabarito', system-ui, sans-serif;
  --header-h: 3.5rem;
}
html { scroll-behavior: smooth; }
body { background: var(--cream); color: var(--ink); font-family: var(--sans); font-size: 16px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
a { color: var(--moss); }

header.bar { box-shadow: 0 1px 0 rgba(26,32,18,0.06); position: fixed; top: 0; left: 0; right: 0; z-index: 50; height: var(--header-h); display: flex; align-items: center; justify-content: space-between; padding: 0 1.5rem; background: rgba(247,244,238,0.92); backdrop-filter: blur(8px); border-bottom: 1px solid var(--cream-dark); }
.bar-logo { display: inline-flex; align-items: center; gap: 0.5rem; font-family: var(--sans); font-weight: 800; font-size: 1.02rem; letter-spacing: 0.07em; text-decoration: none; color: var(--ink); }
.bar-links a { font-size: 13px; color: var(--ink-mid); text-decoration: none; margin-left: 1.25rem; }
.bar-links a:hover { color: var(--moss); }
.bar-links a.bar-login { font-weight: 700; color: var(--ink); }
.bar-links a.bar-cta { color: #fff; background: var(--moss); font-weight: 700; border: 1px solid var(--moss); border-radius: 999px; padding: 0.45rem 1rem; }
.nav-drop { display: inline-block; position: relative; margin-left: 1.25rem; }
.nav-drop summary { font-size: 13px; color: var(--ink-mid); cursor: pointer; list-style: none; }
.nav-drop summary::-webkit-details-marker { display: none; }
.nav-drop summary::after { content: " ▾"; font-size: 10px; }
.nav-drop[open] summary { color: var(--moss); }
.nav-drop-menu { position: absolute; right: 0; top: 2rem; background: #fff; border: none; border-radius: 16px; box-shadow: 0 6px 30px rgba(26,32,18,0.16); padding: 0.6rem 0; min-width: 13rem; z-index: 40; }
.nav-drop-menu a { display: flex; align-items: center; gap: 0.7rem; padding: 0.5rem 1.1rem; margin: 0; font-size: 13.5px; font-weight: 600; color: var(--ink); }
.nav-drop-menu .mi { display: inline-flex; align-items: center; justify-content: center; width: 30px; height: 30px; border-radius: 50%; background: var(--surface); color: var(--ink); flex-shrink: 0; }
.nav-drop-menu .mi svg { width: 16px; height: 16px; }
.nav-drop-menu a:hover { background: var(--cream); }
.only-mobile { display: none; }
/* The header, as Hidde wants it (2026-08-01): Map stands alone in the bar
   because the map is the product, Explore holds the browse facets with their
   icons, and account plus the CTA close the row. Everything collapses into
   the one Menu below 800px. Specificity note, the actual bug behind "login
   and map twice": .nav-drop-menu a outranks a bare .only-mobile, so the
   hide has to be scoped to the same depth or it silently loses. */
.nav-drop-menu a.only-mobile { display: none; }
.nav-drop summary .sum-mobile { display: none; }
.bar-links a.bar-cta:hover { background: var(--moss); color: #fff; }
.city-card.soon:hover { opacity: 1; border-top-color: var(--moss); }
.city-card-cta { font-size: 12px; color: var(--moss); font-weight: 500; margin-top: 0.35rem; }
.path { border: 1px solid var(--cream-dark); border-radius: 6px; padding: 1.4rem 1.6rem; margin: 1.25rem 0; }
.path h2 { margin-top: 0; }
.path .go-btn { margin-top: 0.75rem; }

/* ---- City page: split layout, map is the stage ---- */
.split { display: flex; height: 100vh; padding-top: var(--header-h); }
.panel { width: 30rem; max-width: 45vw; height: 100%; overflow-y: auto; background: var(--cream); border-right: 1px solid var(--cream-dark); flex-shrink: 0; }
.panel-head { padding: 2rem 1.75rem 1.5rem; border-bottom: 1px solid var(--cream-dark); }
.eyebrow { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--ink-light); margin-bottom: 0.75rem; }
.panel-head h1 { font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em; font-size: 1.9rem; font-weight: 400; line-height: 1.2; margin-bottom: 0.75rem; }
.panel-head h1 em { font-style: normal; color: var(--moss); font-weight: 800; letter-spacing: 0; }
.lede { font-size: 14px; font-weight: 300; color: var(--ink-mid); line-height: 1.7; }
.notice { background: var(--moss-light); border-left: 3px solid var(--moss); padding: 0.7rem 1rem; font-size: 12px; color: var(--ink-mid); margin-top: 1rem; }
.stage { flex: 1; position: relative; }
.stage .map { position: absolute; inset: 0; width: 100%; height: 100%; }

.tree-card { padding: 1.75rem; border-bottom: 1px solid var(--cream-dark); cursor: pointer; border-left: 3px solid transparent; transition: border-color 0.2s, background 0.2s; }
.tree-card:hover { background: #fbf9f5; }
.tree-card.active { border-left-color: var(--moss); background: #fbf9f5; }
.tree-card-photo { margin: 0 0 1rem; border-radius: 8px; overflow: hidden; aspect-ratio: 3 / 2; background: var(--cream-dark); }
.tree-card-photo img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 0.4s ease; }
.tree-card:hover .tree-card-photo img { transform: scale(1.04); }
.tree-card-credit { font-size: 10px; color: var(--ink-light); margin: -0.6rem 0 0.85rem; }
.tree-card-top { display: flex; align-items: baseline; gap: 0.75rem; margin-bottom: 0.4rem; }
.tree-num { font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em; font-size: 1.1rem; color: var(--moss); flex-shrink: 0; width: 1.4rem; }
.tree-name { font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em; font-size: 1.35rem; font-weight: 400; line-height: 1.25; }
.tree-label { display: inline-block; font-size: 10px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-mid); background: var(--cream-dark); border-radius: 2px; padding: 0.15rem 0.45rem; margin-left: 0.6rem; vertical-align: middle; white-space: nowrap; }
.tree-meta { font-size: 12px; color: var(--ink-light); margin: 0 0 0.6rem 2.15rem; }
.best-now, .best-now-inline { display: inline-block; background: var(--moss); color: #fff;
  font-size: 11px; font-weight: 600; padding: 1px 7px; border-radius: 999px;
  margin-left: 6px; letter-spacing: 0.02em; text-transform: uppercase; }
.best-now-inline { margin-left: 0; }
/* Seasonal peak chart, in the spirit of PictureThis but in our own skin. */
.season { margin: 2rem 0; background: #fff; border: 1px solid var(--cream-dark);
  border-radius: 10px; padding: 1.1rem 1.25rem 0.9rem; }
.season-head { display: flex; align-items: center; gap: 0.5rem; font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em;
  font-size: 1.05rem; color: var(--ink); margin-bottom: 0.5rem; }
.sc-chip { font-family: var(--sans); font-size: 12.5px; font-weight: 700; color: var(--ink);
  background: #fff; border: 1px solid var(--cream-dark); border-radius: 999px; padding: 5px 12px 5px 9px;
  text-transform: capitalize; display: inline-flex; align-items: center; gap: 6px; }
.sc-chip svg { width: 16px; height: 16px; flex-shrink: 0; }
.season-plot { position: relative; }
.sc-peakbadge { position: absolute; transform: translate(-50%, -130%); background: #fff;
  border-radius: 10px; padding: 5px; box-shadow: 0 2px 10px rgba(26,32,18,0.14); line-height: 0; }
.sc-peakbadge svg { width: 18px; height: 18px; }
.sc-grid { stroke: var(--cream-dark); stroke-width: 1; opacity: 0.6; }
.season-legend { margin-top: 0.5rem; }
.season-svg { width: 100%; height: auto; display: block; overflow: visible; }
.sc-area { fill: var(--moss-light); }
.sc-line { fill: none; stroke: var(--moss); stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; }
.sc-peak { fill: var(--moss); stroke: #fff; stroke-width: 2; }
.sc-now { stroke: var(--ink-light); stroke-width: 1; stroke-dasharray: 2 3; }
.sc-nowlabel { fill: var(--ink-light); font-family: var(--sans); font-size: 9px; text-anchor: middle; text-transform: uppercase; letter-spacing: 0.05em; }
.sc-m { fill: var(--ink-light); font-family: var(--sans); font-size: 9px; text-anchor: middle; }
.season-label { margin: 0.4rem 0 0; font-size: 13.5px; color: var(--ink-mid); }
/* Overview shows a teaser; the full story lives on the tree page. The whole
   text stays in the HTML so crawlers and AI engines still read it. */
.tree-story { font-size: 14px; font-weight: 300; color: var(--ink-mid); line-height: 1.7; margin: 0 0 0.7rem 2.15rem;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
.tree-more { font-size: 13px; font-weight: 500; margin: 0 0 0 2.15rem; }
.tree-more a { text-decoration: none; }
.tree-more a:hover { text-decoration: underline; }
.panel-foot { padding: 1.75rem; font-size: 13px; color: var(--ink-mid); }
.subtle-suggest b { color: var(--ink); font-weight: 700; }
.panel-foot h2 { font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em; font-size: 1.25rem; font-weight: 400; margin-bottom: 0.75rem; }
.panel-foot dt { font-weight: 500; margin-top: 1rem; }
.panel-foot dd { font-weight: 300; margin-top: 0.3rem; }
.panel-foot .suggest { border-top: 1px solid var(--cream-dark); margin-top: 1.5rem; padding-top: 1.25rem; color: var(--ink-light); }

/* ---- Content pages (tree, question, collection, about) ---- */
.content-page { max-width: 700px; margin: 0 auto; padding: calc(var(--header-h) + 2.25rem) 1.5rem 3.5rem; }
.crumbs { font-size: 12px; color: var(--ink-light); margin-bottom: 1.25rem; }
.crumbs a { color: var(--ink-light); text-decoration: none; }
.crumbs a:hover { color: var(--moss); }
.content-page h1 { font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em; font-size: 2.1rem; font-weight: 400; line-height: 1.2; margin-bottom: 1rem; }
.content-page h2 { font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em; font-size: 1.4rem; font-weight: 400; margin: 2.25rem 0 0.75rem; }
.content-page h3 { font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em; font-size: 1.15rem; font-weight: 400; margin: 1.5rem 0 0.35rem; }
.answer-first { font-size: 1.05rem; line-height: 1.75; margin-bottom: 1rem; }
.prose-block p { font-size: 15px; font-weight: 300; color: var(--ink-mid); line-height: 1.75; margin-bottom: 1rem; }
.facts { display: grid; grid-template-columns: max-content 1fr; gap: 0.4rem 1.5rem; background: var(--cream-dark); padding: 1.25rem 1.5rem; border-radius: 4px; margin: 1.5rem 0; }
.facts dt { font-size: 10px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-light); padding-top: 3px; }
.facts dd { font-size: 13px; color: var(--ink); }
.tree-photo { margin: 1.5rem 0; }
.tree-photo img { width: 100%; display: block; border-radius: 4px; }
.tree-photo figcaption { font-size: 11px; color: var(--ink-light); margin-top: 0.45rem; }
.go-btn { display: inline-block; background: var(--moss); color: #fff; text-decoration: none; font-size: 14px; font-weight: 700; padding: 0.75rem 1.5rem; border-radius: 999px; margin: 0.25rem 0 0.5rem; }
.go-btn.ghost { background: transparent; border: 1.5px solid var(--moss); color: var(--moss); }
.chip-row { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.35rem 0 1rem; }
.chip { font-size: 12px; font-weight: 600; background: var(--cream-dark); border-radius: 999px; padding: 4px 12px; color: var(--ink-mid); }
.chip.ok { background: var(--moss-light); color: var(--moss); }
.chip.approx { border: 1.5px dashed var(--ink-light); background: transparent; }
.chip.gold { background: #F3E4C3; color: #8A6414; }
.action-row { display: flex; gap: 0.6rem; flex-wrap: wrap; align-items: center; margin: 0.75rem 0 1.25rem; }
.action-row .go-btn { margin: 0; }
.action-row .seen-btn { float: none; cursor: pointer; font-family: inherit; font-size: 14px; font-weight: 700; background: var(--moss); color: #fff; border: 1px solid var(--moss); border-radius: 999px; padding: 0.75rem 1.5rem; }
.action-row .seen-btn[aria-pressed="true"] { background: var(--moss-light); color: var(--moss); }
.action-link { font-size: 13.5px; font-weight: 600; color: var(--moss); text-decoration: none; }
.near-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; margin: 0.5rem 0 1rem; list-style: none; padding: 0; }
.near-card { display: block; background: #fff; border: none; box-shadow: var(--shadow); border-radius: 16px; padding: 14px 16px; text-decoration: none; color: var(--ink); transition: box-shadow 0.15s; }
.near-card:hover { box-shadow: 0 2px 6px rgba(26,32,18,0.12), 0 8px 22px rgba(26,32,18,0.09); }
.near-card b { display: block; font-size: 14px; font-weight: 700; margin-bottom: 2px; }
.near-card span { font-size: 12px; color: var(--ink-light); }
.go-btn:hover { background: #2f4717; }
.go-note { font-size: 12px; color: var(--ink-light); margin-bottom: 1.5rem; }
.take-with-you { background: var(--cream-dark); border-radius: 4px; padding: 1.1rem 1.4rem; margin: 1.5rem 0; font-size: 13px; }
.take-with-you a { font-weight: 500; }
.approx-note { font-size: 12px; color: var(--ink-mid); background: var(--cream-dark); border-radius: 4px; padding: 0.7rem 0.9rem; margin: -0.6rem 0 1.5rem; }
.report { background: var(--moss-light); border-left: 3px solid var(--moss); border-radius: 0 4px 4px 0; padding: 1rem 1.3rem; margin: 2.5rem 0 0; font-size: 13px; }
.map-embed { position: relative; height: 340px; border-radius: 4px; overflow: hidden; margin: 1.75rem 0; border: 1px solid var(--cream-dark); }
.map-embed .map { position: absolute; inset: 0; width: 100%; height: 100%; }
.faq dt { font-weight: 500; font-size: 15px; margin-top: 1.25rem; }
.faq dd { font-size: 14px; font-weight: 300; color: var(--ink-mid); margin-top: 0.35rem; line-height: 1.7; }
.cta { background: var(--moss-light); border-left: 3px solid var(--moss); padding: 1.1rem 1.4rem; border-radius: 0 4px 4px 0; margin: 2rem 0; font-size: 14px; }
.entry { margin-bottom: 1.6rem; }
.entry p { font-size: 14px; font-weight: 300; color: var(--ink-mid); line-height: 1.7; margin-top: 0.25rem; }
/* Image first, text second: a thumbnail leads the row where a photo exists. */
.entry.has-thumb { display: grid; grid-template-columns: 96px 1fr; gap: 1rem; align-items: start; }
.coll-city { color: inherit; text-decoration: none; }
.coll-city:hover { color: var(--moss); }
.coll-citycta { margin: 0.4rem 0 2rem; font-size: 13.5px; font-weight: 700; }
.coll-citycta a { color: var(--moss); }
.entry-thumb { border-radius: 6px; overflow: hidden; aspect-ratio: 1 / 1; background: var(--cream-dark); }
.entry-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
.entry-body h3 { margin-top: 0; }
@media (max-width: 800px) {
  .bar-logo { font-size: 0.92rem; letter-spacing: 0.04em; white-space: nowrap; }
  .bar-logo svg { width: 20px; height: 18px; }
  .bar-links { display: flex; align-items: center; gap: 0.55rem; }
  .bar-links a { margin-left: 0; }
  .only-desktop { display: none !important; }
  .only-mobile { display: block; }
  .nav-drop-menu a.only-mobile { display: flex; }
  .nav-drop { margin-left: 0; }
  .nav-drop summary { font-size: 13px; padding: 0.35rem 0.2rem; }
  .nav-drop summary .sum-desktop { display: none; }
  .nav-drop summary .sum-mobile { display: inline; }
  .nav-drop-menu { position: fixed; left: 0.75rem; right: 0.75rem; top: 3.4rem; min-width: 0; }
  .bar-links a.bar-cta { padding: 0.35rem 0.6rem; font-size: 12px; white-space: nowrap; }
  .footer-cols { flex-direction: column; gap: 1.5rem; }
  .action-row .go-btn, .action-row .seen-btn { font-size: 13px; padding: 0.6rem 0.9rem; }

  .entry.has-thumb { grid-template-columns: 72px 1fr; gap: 0.8rem; }
}
.suggest { font-size: 13px; color: var(--ink-light); border-top: 1px solid var(--cream-dark); padding-top: 1.25rem; margin-top: 2.5rem; }
ul.link-list { list-style: none; }
ul.link-list li { margin-bottom: 0.5rem; font-size: 14px; }

/* ---- Homepage ---- */
.home-hero { position: relative; height: 72vh; min-height: 420px; margin-top: var(--header-h); }
.home-hero .map { position: absolute; inset: 0; width: 100%; height: 100%; }
.hero-overlay { position: absolute; top: 1.5rem; left: 1.5rem; z-index: 10; background: rgba(247,244,238,0.95); backdrop-filter: blur(8px); border: 1px solid var(--cream-dark); border-radius: 4px; padding: 1.75rem 2rem; max-width: 26rem; box-shadow: 0 4px 24px rgba(26,26,20,0.08); }
.hero-overlay h1 { font-family: var(--sans); font-size: 2rem; font-weight: 800; letter-spacing: -0.02em; line-height: 1.12; margin-bottom: 0.6rem; }
.hero-overlay h1 em { font-style: normal; color: var(--moss); font-weight: 800; letter-spacing: 0; }
.hero-overlay p { font-size: 13px; font-weight: 300; color: var(--ink-mid); line-height: 1.65; }
.hero-overlay .go-btn { border: none; font-family: var(--sans); cursor: pointer; margin-top: 0.9rem; }
.near-me-result { font-size: 12px; margin-top: 0.6rem; min-height: 1em; }
/* Find / walk / collect: the product told as three acts, in our own skin.
   Validated by AllTrails and Polarsteps, both of which lead with three
   capability sections. See PRINCIPLES.md and COMPETITION.md. */
.home-acts { max-width: 1040px; margin: 0 auto; padding: 2rem 1.5rem 0; }
.home-act { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center; padding: 3rem 0; border-top: 1px solid var(--cream-dark); }
.home-act:first-child { border-top: none; }
.home-act:nth-child(even) .home-act-visual { order: -1; }
.home-act-verb { font-family: var(--sans); font-weight: 800; color: var(--moss); font-size: 1rem; text-transform: uppercase; letter-spacing: 0.06em; }
.home-act h2 { font-family: var(--sans); font-weight: 800; letter-spacing: -0.02em; font-size: 1.9rem; margin: 0.35rem 0 0.7rem; line-height: 1.1; }
.home-act-copy p { color: var(--ink-mid); font-size: 1.05rem; max-width: 42ch; }
/* The three acts, drawn in one illustrated system instead of photographs.
   Reference: Polarsteps' stats-that-grow presentation, in our own cream and
   moss. Find and Walk share a stylised map card; Collect is a phone with the
   species grid as our "collected flags". */
.hav-card { position: relative; margin: 0; aspect-ratio: 4 / 3; border-radius: 16px; overflow: hidden;
  background: #EFEDE3; border: 1px solid var(--cream-dark); box-shadow: 0 18px 40px rgba(26,26,20,0.10); }
.hav-card svg.scene { position: absolute; inset: 0; width: 100%; height: 100%; }
.hav-chip { position: absolute; left: 14px; bottom: 14px; display: flex; align-items: center; gap: 9px;
  background: rgba(255,255,255,0.95); border-radius: 10px; padding: 9px 13px; font-size: 13px;
  color: var(--ink); box-shadow: 0 4px 16px rgba(0,0,0,0.14); }
.hav-chip strong { display: block; font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.04em;
  color: var(--moss); font-weight: 600; }
.hav-dot { width: 12px; height: 12px; border-radius: 50%; background: #1E6FD9;
  box-shadow: 0 0 0 5px rgba(30,111,217,0.22); flex: none; }
.map-pin { position: absolute; width: 34px; height: 34px; border-radius: 50%; background: var(--cream);
  border: 2px solid var(--moss); display: flex; align-items: center; justify-content: center;
  color: var(--moss); box-shadow: 0 3px 9px rgba(26,26,20,0.22); transform: translate(-50%,-50%); }
.map-pin svg { width: 21px; height: 21px; }
.map-pin.me { width: 16px; height: 16px; background: #1E6FD9; border: 2.5px solid #fff;
  box-shadow: 0 0 0 6px rgba(30,111,217,0.2); }
.map-pin .n { position: absolute; top: -6px; right: -6px; min-width: 15px; height: 15px; border-radius: 8px;
  background: var(--moss); color: #fff; font-size: 9.5px; font-weight: 700; display: flex;
  align-items: center; justify-content: center; border: 1.5px solid var(--cream); }
/* Collect: the phone. */
.hav-phone { margin: 0 auto; width: min(78%, 300px); background: var(--ink); border-radius: 30px;
  padding: 10px; box-shadow: 0 22px 44px rgba(26,26,20,0.24); }
.hav-screen { background: #fff; border-radius: 22px; padding: 16px 14px 18px; }
.hav-screen h4 { font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em; font-size: 1.05rem; margin: 0 0 10px; }
.stat-row { display: flex; gap: 8px; margin-bottom: 12px; }
.stat { flex: 1; border-radius: 12px; padding: 10px 8px; text-align: center; background: var(--moss-light); }
.stat.alt { background: #F3EFE2; }
.stat b { display: block; font-family: var(--sans); font-weight: 700; letter-spacing: -0.01em; font-size: 1.45rem; color: var(--moss); line-height: 1.1; }
.stat span { font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--ink-mid); }
.hav-screen h5 { font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--ink-light);
  margin: 0 0 8px; font-weight: 600; }
.sp-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 7px; }
.sp { position: relative; aspect-ratio: 1; border-radius: 50%; display: flex; align-items: center;
  justify-content: center; background: var(--moss-light); color: var(--moss); }
.sp svg { width: 68%; height: 68%; }
.sp.dim { background: #F0EEE6; color: #C9C5B6; }
.season-card { background: #fff; border: 1px solid var(--cream-dark); border-radius: 16px; padding: 1.2rem 1.3rem; box-shadow: 0 18px 40px rgba(26,26,20,0.10); }
.season-now { font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--moss); font-weight: 800; margin: 0 0 12px; font-family: var(--sans); }
.sr-row { display: flex; align-items: center; gap: 12px; padding: 9px 0; border-top: 1px solid #F0EDE3; }
.sr-row:first-of-type { border-top: none; }
.sr-row .sp { width: 40px; flex: none; }
.sr-body { flex: 1; min-width: 0; }
.sr-body b { display: block; font-size: 0.95rem; font-weight: 600; }
.sr-body i { font-style: normal; font-size: 0.8rem; color: var(--ink-light); }
.sr-row.dim .sr-body b { color: var(--ink-light); font-weight: 500; }
.hav-badge-inline { background: var(--moss); color: #fff; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; padding: 3px 9px; border-radius: 999px; }
.sr-when { font-size: 11px; color: var(--ink-light); border: 1px solid var(--cream-dark); border-radius: 999px; padding: 2px 9px; }
.sr-months { display: flex; gap: 4px; margin-top: 12px; }
.sr-months span { flex: 1; height: 5px; border-radius: 3px; background: #EFEDE3; }
.sr-months span.on { background: var(--moss); }
.sr-link { margin: 12px 0 0; font-size: 0.85rem; }
.sr-link a { color: var(--moss); font-weight: 600; text-decoration: none; }
.sr-link a:hover { text-decoration: underline; }
.account-page { max-width: 480px; }
.proto-note { background: #FDF6E3; border: 1px solid #EADFA9; border-radius: 8px; padding: 8px 12px; font-size: 12.5px; color: #7A6A2F; margin-bottom: 1.4rem; }
.acct-card h1 { margin-bottom: 0.5rem; }
.acct-sub { color: var(--ink-mid); margin-bottom: 1.1rem; }
.acct-fine { font-size: 12px; color: var(--ink-light); margin-top: 0.7rem; }
.acct-actions { display: flex; gap: 0.75rem; align-items: center; margin-top: 0.5rem; }
.acct-link { background: none; border: none; padding: 0; font-family: var(--sans); font-size: 13.5px; color: var(--moss); text-decoration: underline; cursor: pointer; }
.acct-link.danger { color: #9c3f2f; }
.sr-months span.half { background: #A9BC8A; }
.sp-name { position: absolute; top: -9px; left: 50%; transform: translateX(-50%); background: var(--ink);
  color: #fff; font-size: 8.5px; font-weight: 600; padding: 1.5px 7px; border-radius: 999px; white-space: nowrap; }
@media (max-width: 760px) { .home-act { grid-template-columns: 1fr; gap: 1.5rem; padding: 2.25rem 0; } .home-act:nth-child(even) .home-act-visual { order: 0; } }
.page { max-width: 1100px; margin: 0 auto; padding: 3rem 2.5rem; }
.section-heading { font-family: var(--sans); font-size: 1.7rem; font-weight: 700; letter-spacing: -0.015em; margin-bottom: 1.5rem; }
.prose { font-size: 15px; font-weight: 300; color: var(--ink-mid); line-height: 1.75; max-width: 640px; margin-bottom: 2.5rem; }
.city-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 2px; background: var(--cream-dark); border: 1px solid var(--cream-dark); margin-bottom: 3rem; }
.explore-page { margin-top: var(--header-h); }
/* The app part (head + split) fills exactly one screen; anything after it, like
   the prose section, lives below the fold. The prose used to sit INSIDE the
   fixed-height flex column, which squeezed the split to 20px and let the map's
   own min-height paint over the text that followed. */
.explore-app { display: flex; flex-direction: column; height: calc(100vh - var(--header-h)); }
.explore-split { display: flex; flex: 1; min-height: 0; }
.ex-panel { width: 360px; flex-shrink: 0; overflow-y: auto; background: #fff; border-right: 1px solid var(--cream-dark); padding: 0.9rem; }
.exc-cityhead { display: flex; align-items: baseline; justify-content: space-between; gap: 0.75rem; margin: 0.2rem 0.2rem 0.8rem; }
.exc-cityhead h2 { font-size: 1.05rem; font-weight: 800; letter-spacing: -0.01em; }
.exc-cityhead a { font-size: 12.5px; font-weight: 700; color: var(--moss); white-space: nowrap; }
.exc-card { display: flex; gap: 0.7rem; align-items: center; padding: 0.45rem; border-radius: 12px; text-decoration: none; color: var(--ink); }
.exc-card:hover { background: var(--surface); }
.exc-ph { width: 86px; height: 62px; border-radius: 9px; overflow: hidden; flex-shrink: 0; background: var(--cream-dark); }
.exc-ph img { width: 100%; height: 100%; object-fit: cover; display: block; }
.exc-body b { display: block; font-size: 14.5px; font-weight: 750; }
.exc-body span { font-size: 12.5px; color: var(--ink-mid); }
.exc-row { display: block; padding: 0.5rem 0.45rem; border-radius: 9px; text-decoration: none; color: var(--ink); }
.exc-row:hover { background: var(--surface); }
.exc-row b { font-size: 13.5px; font-weight: 700; }
.exc-row span { display: block; font-size: 12px; color: var(--ink-mid); }
.exc-now { font-size: 10.5px; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 0.04em; }
.cindex-country { font-size: 1.05rem; font-weight: 800; margin: 1.6rem 0 0.6rem; }
.cindex-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 0.35rem 1rem; }
.exc-empty { font-size: 13px; color: var(--ink-mid); padding: 0.5rem; }
@media (max-width: 800px) {
  .explore-split { flex-direction: column-reverse; }
  .ex-panel { width: 100%; height: 38vh; border-right: none; border-top: 1px solid var(--cream-dark); }
}
.explore-head { padding: 1.1rem 2rem 0.9rem; display: grid; grid-template-columns: 1fr auto; gap: 0.2rem 1.5rem; align-items: center; }
.explore-head h1 { font-size: 1.45rem; font-weight: 800; letter-spacing: -0.015em; }
.explore-head p { font-size: 13px; color: var(--ink-mid); margin-top: 0.2rem; max-width: 46rem; grid-column: 1; }
/* One search component, one look (Hidde, 2026-08-01: the home experience and
   the one above the map should be the same thing). The pill lives on
   .at-search itself, so a new placement inherits it instead of inventing its
   own; .poster-search only scales it up for the photo hero. */
.at-search { position: relative; display: flex; align-items: center; gap: 0.15rem; background: #fff; border-radius: 999px; padding: 0.3rem 0.5rem 0.3rem 0.35rem; box-shadow: 0 6px 22px rgba(26,32,18,0.13); }
.at-search > svg { width: 20px; height: 20px; color: var(--ink-light); flex-shrink: 0; margin-left: 0.55rem; }
.at-search .search-ico { display: inline-flex; align-items: center; justify-content: center; width: 42px; height: 42px; border: none; background: transparent; color: var(--ink-light); cursor: pointer; }
.at-search .search-ico svg { width: 20px; height: 20px; }
.at-search input { border: none; outline: none; background: transparent; flex: 1; min-width: 0; font-family: var(--sans); font-size: 16px; padding: 0.6rem 0.6rem; color: var(--ink); }
.ex-search { grid-column: 2; grid-row: 1 / span 2; width: min(30rem, 100%); }
.at-search { position: relative; }
.at-search input::-webkit-search-decoration { display: none; }
.ats-drop { position: absolute; top: calc(100% + 8px); left: 0; right: 0; background: #fff; border-radius: 14px; box-shadow: 0 14px 44px rgba(0,0,0,0.22); overflow: hidden; overflow-y: auto; max-height: min(21rem, 55vh); z-index: 80; text-align: left; }
.ats-row { display: block; padding: 0.55rem 1.1rem; text-decoration: none; color: var(--ink); font-family: var(--sans); }
.ats-row b { display: block; font-size: 14.5px; font-weight: 600; }
.ats-row span { display: block; font-size: 12.5px; color: var(--ink-mid); }
.ats-row.active, .ats-row:hover { background: #F1EFE8; }
.ats-head { padding: 0.5rem 1.1rem 0.15rem; font-family: var(--sans); font-size: 10.5px; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase; color: var(--ink-light); }
.ats-empty { padding: 0.75rem 1.1rem; font-family: var(--sans); font-size: 13px; color: var(--ink-mid); }
.ats-empty a { color: var(--moss); }
/* Country page: the ranked-list form (Hidde, 2026-08-01, the PictureThis
   Top-50 pattern): rank numeral, photo, name, one honest sub-line, chevron. */
.ctry-list { margin: 0.5rem 0 2rem; }
.ctry-row { display: flex; align-items: center; gap: 0.9rem; padding: 0.7rem 0.2rem; border-bottom: 1px solid var(--cream-dark); text-decoration: none; color: var(--ink); }
.ctry-row:last-child { border-bottom: none; }
.ctry-rank { font-family: var(--sans); font-size: 20px; font-weight: 700; color: var(--moss); min-width: 1.6rem; text-align: center; flex-shrink: 0; }
.ctry-ph { display: block; width: 78px; height: 62px; border-radius: 10px; overflow: hidden; background: var(--cream-dark); flex-shrink: 0; }
.ctry-ph img { width: 100%; height: 100%; object-fit: cover; display: block; }
.ctry-noph { display: flex; align-items: center; justify-content: center; color: #CFCEC4; }
.ctry-noph svg { width: 30px; height: 28px; }
.ctry-body { flex: 1; min-width: 0; font-family: var(--sans); }
.ctry-body b { display: block; font-size: 16px; font-weight: 600; }
.ctry-body span { display: block; font-size: 12.5px; color: var(--ink-mid); margin-top: 2px; }
.ctry-chev { color: var(--ink-light); font-size: 26px; line-height: 1; flex-shrink: 0; padding-right: 0.2rem; }
.ctry-row:hover .ctry-body b { text-decoration: underline; }
.phenology .season-head { margin-bottom: 0.2rem; }
.ph-keys { display: flex; flex-wrap: wrap; gap: 0.4rem 0.9rem; margin: 0.5rem 0 0; }
.ph-key { display: inline-flex; align-items: center; gap: 0.35rem; font-family: var(--sans); font-size: 12px; color: var(--ink-mid); }
.ph-key svg { width: 15px; height: 15px; flex-shrink: 0; }
.ph-foot { margin: 0.5rem 0 0; font-family: var(--sans); font-size: 11px; color: var(--ink-light); line-height: 1.5; }
.sp-citylink { color: inherit; text-decoration: none; }
.sp-citylink:hover { text-decoration: underline; }
.collect-dialog { border: none; border-radius: 16px; padding: 1.5rem 1.6rem; margin: auto; max-width: 26rem; width: calc(100vw - 3rem); box-shadow: 0 18px 60px rgba(0,0,0,0.3); font-family: var(--sans); color: var(--ink); }
.collect-dialog::backdrop { background: rgba(38, 48, 30, 0.45); }
.collect-dialog h3 { font-size: 1.15rem; margin-bottom: 0.5rem; }
.collect-dialog p { font-size: 14px; font-weight: 300; color: var(--ink-mid); line-height: 1.65; }
.collect-actions { display: flex; gap: 0.6rem; margin-top: 1.1rem; flex-wrap: wrap; }
@media (max-width: 800px) {
  .explore-head { grid-template-columns: 1fr; }
  .explore-head p { display: none; }
  .ex-search { grid-column: 1; grid-row: auto; min-width: 0; margin-top: 0.4rem; }
}
.explore-now-chip { display: inline-block; background: #F3E4C3; color: #8A6414; font-weight: 700; font-size: 11.5px; border-radius: 999px; padding: 2px 10px; margin-left: 0.4rem; }
.explore-map { flex: 1; min-height: 320px; }
/* The map is the page; this sits under it, for readers and for search engines
   that cannot read a canvas. Never above the fold. */
.explore-prose { padding: 2rem 2rem 3rem; max-width: 48rem; font-family: var(--sans); }
.explore-prose h2 { font-size: 1.05rem; font-weight: 750; letter-spacing: -0.01em; margin: 1.4rem 0 0.4rem; }
.explore-prose h2:first-child { margin-top: 0; }
.explore-prose p { font-size: 14.5px; font-weight: 300; color: var(--ink-mid); line-height: 1.7; margin-bottom: 0.5rem; }
.explore-prose a { color: var(--moss); }
.explore-prose-more { margin-top: 1.2rem; font-size: 13.5px; }
@media (max-width: 800px) { .explore-prose { padding: 1.5rem 1.1rem 2.5rem; } }
.pop-now { background: #F3E4C3; color: #8A6414; font-weight: 700; font-size: 10px; border-radius: 999px; padding: 1px 8px; }
.appland { position: relative; display: flex; align-items: center; justify-content: center; padding: 5rem 1rem; }
.appland-bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; filter: brightness(0.82); }
.appland-card { position: relative; z-index: 1; background: #fff; border-radius: 24px; box-shadow: 0 18px 60px rgba(0,0,0,0.3); max-width: 62rem; width: 100%; display: grid; grid-template-columns: 1.05fr 1fr; gap: 2.5rem; padding: 2.75rem 3rem; }
.appland-left h1 { font-size: 2.1rem; font-weight: 800; letter-spacing: -0.02em; line-height: 1.12; margin: 0.9rem 0 0.6rem; }
.appland-sub { font-size: 14.5px; color: var(--ink-mid); line-height: 1.6; margin-bottom: 1.4rem; }
.appland-steps { list-style: none; padding: 0; margin: 0 0 1.6rem; }
.appland-steps li { display: flex; gap: 0.8rem; align-items: flex-start; font-size: 13.5px; color: var(--ink-mid); padding: 0.5rem 0; }
.appland-steps strong { color: var(--ink); }
.step-ico { display: inline-flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 50%; background: var(--moss-light); color: var(--moss); flex-shrink: 0; }
.step-ico svg { width: 17px; height: 17px; }
.waitlist { display: flex; gap: 0.5rem; margin-top: 0.4rem; flex-wrap: wrap; }
.waitlist input { flex: 1 1 12rem; min-width: 0; border: 1px solid var(--cream-dark); border-radius: 999px;
  padding: 0.75rem 1.1rem; font-family: var(--sans); font-size: 14px; background: #fff; }
.waitlist input:focus { outline: 2px solid var(--moss); outline-offset: 1px; }
.waitlist-note { font-size: 12px; color: var(--ink-light); margin-top: 0.5rem; }
.appland-cta { display: inline-block; background: var(--ink); color: #fff; font-weight: 700; font-size: 15px; text-decoration: none; border-radius: 999px; padding: 0.95rem 2.4rem; }
.appland-right h2 { font-size: 13px; font-weight: 600; letter-spacing: 0.02em; color: var(--ink-light); margin-bottom: 0.4rem; }
.appland-feat { display: flex; gap: 1rem; align-items: flex-start; padding: 1.05rem 0; border-bottom: 1px solid var(--cream-dark); }
.appland-feat:last-child { border-bottom: none; }
.feat-tile { display: inline-flex; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 12px; background: var(--surface); flex-shrink: 0; }
.feat-tile svg { width: 34px; height: 34px; }
.appland-feat h3 { font-size: 14.5px; font-weight: 800; margin-bottom: 0.15rem; }
.appland-feat p { font-size: 12.5px; color: var(--ink-mid); line-height: 1.5; }
@media (max-width: 800px) {
  .appland { padding: 1rem 0.6rem; }
  .appland-card { grid-template-columns: 1fr; padding: 1.6rem 1.3rem; gap: 1.4rem; border-radius: 20px; }
  .appland-left h1 { font-size: 1.6rem; }
}
.shelf { padding: 1.4rem 2rem 0.6rem; max-width: 74rem; margin: 0 auto; }
.shelf-head { display: flex; align-items: baseline; justify-content: space-between; gap: 1rem; margin-bottom: 0.9rem; }
.shelf-head h2 { font-size: 1.35rem; font-weight: 800; letter-spacing: -0.015em; }
.shelf-head a { font-size: 13.5px; font-weight: 700; color: var(--moss); text-decoration: underline; text-underline-offset: 3px; }
.shelf-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.shelf-row-wide { display: flex; overflow-x: auto; gap: 16px; scroll-snap-type: x mandatory; padding-bottom: 0.5rem; }
.shelf-row-wide .shelf-card { flex: 0 0 calc(20% - 13px); min-width: 180px; scroll-snap-align: start; }
.shelf-card { display: block; text-decoration: none; color: var(--ink); }
.shelf-ph { position: relative; display: block; aspect-ratio: 4 / 3; border-radius: 16px; overflow: hidden; box-shadow: var(--shadow); margin-bottom: 0.6rem; background: var(--surface); }
.shelf-ph img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.25s; }
.shelf-card:hover .shelf-ph img { transform: scale(1.04); }
.shelf-now { position: absolute; top: 10px; left: 10px; background: #F3E4C3; color: #8A6414; font-size: 10.5px; font-weight: 700; border-radius: 999px; padding: 3px 10px; }
.shelf-card b { display: block; font-size: 15px; font-weight: 800; line-height: 1.3; }
.shelf-meta { display: block; font-size: 12.5px; color: var(--ink-mid); margin-top: 2px; }
@media (max-width: 800px) {
  .shelf { padding: 1.2rem 1rem 0.4rem; }
  .shelf-head { flex-direction: column; align-items: flex-start; gap: 0.15rem; }
  .shelf-head h2 { font-size: 1.25rem; }
  .shelf-row { display: flex; overflow-x: auto; gap: 12px; scroll-snap-type: x mandatory; padding-bottom: 0.5rem; }
  .shelf-card { flex: 0 0 72%; scroll-snap-align: start; }
}
.dir-cols { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 1.25rem 2rem; margin: 0.75rem 0 0.5rem; }
.dir-group h3 { font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--ink-light); margin-bottom: 0.35rem; }
.dir-group a { display: block; font-size: 13.5px; color: var(--ink-mid); text-decoration: none; padding: 0.15rem 0; }
.dir-group a:hover { color: var(--moss); }
.dir-more { font-size: 13px; color: var(--ink-mid); margin-top: 0.75rem; }
.dir-morelink { font-weight: 700; color: var(--moss) !important; margin-top: 0.3rem; }
.dir-morebtn { display: block; background: none; border: none; padding: 0.15rem 0; font-family: var(--sans); font-size: 13.5px; text-align: left; cursor: pointer; }
.dir-count { color: var(--ink-light); font-size: 12px; margin-left: 0.35rem; }
.dir-cols { grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); }
.dir-all { margin-top: 1.25rem; }
.dir-all summary { font-size: 13.5px; font-weight: 700; color: var(--moss); cursor: pointer; }
.dir-all .dir-cols { margin-top: 0.9rem; }
.city-card { background: var(--cream); padding: 1.5rem; text-decoration: none; border-top: 2px solid transparent; transition: border-top-color 0.2s; }
.city-card:hover { border-top-color: var(--moss); }
.city-card-name { font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em; font-size: 1.25rem; color: var(--ink); margin-bottom: 0.25rem; }
.city-card-meta { font-size: 12px; color: var(--ink-light); }
.city-card.soon { opacity: 0.55; }

footer { border-top: 1px solid var(--cream-dark); padding: 2.5rem 2.5rem 2rem; }
.footer-cols { display: flex; gap: 3rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
.footer-about { max-width: 20rem; }
.footer-about p { font-size: 13px; color: var(--ink-mid); line-height: 1.6; margin-top: 0.6rem; }
.footer-col h4 { font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--ink-light); margin-bottom: 0.6rem; }
.footer-col a { display: block; font-size: 13px; color: var(--ink-mid); text-decoration: none; padding: 0.2rem 0; }
.footer-col a:hover { color: var(--moss); }
.footer-logo { font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em; font-size: 14px; letter-spacing: 0.08em; text-transform: uppercase; }
.footer-links { font-size: 12px; }
.footer-links a { color: var(--ink-mid); text-decoration: none; margin-right: 1rem; }
.footer-note { font-size: 12px; color: var(--ink-light); }

/* ---- Markers ---- */
.pin { padding: 2px 8px; border-radius: 999px; background: var(--moss); border: 1.5px solid #fff; box-shadow: 0 2px 8px rgba(26,26,20,0.35); cursor: pointer; color: #fff; font-size: 10.5px; font-weight: 600; font-family: var(--sans); white-space: nowrap; transition: transform 0.15s, background 0.15s; }
.pin:hover { transform: scale(1.1); z-index: 5; }
.hero-search { display: flex; gap: 0.5rem; margin-top: 0.9rem; }
/* Hero height, benchmarked (Hidde, 2026-08-01: "staat wel erg weinig boven de
   fold"). AllTrails, Komoot and the rest of the discovery category land their
   hero around 55-65% of the viewport and let the next section peek above the
   fold on purpose: the peek is what tells a visitor there is more, and a
   full-height hero is the one thing that reliably stops people scrolling.
   62vh capped at 560px, so the value proposition always shows. */
.home-hero.poster { position: relative; height: min(62vh, 560px); min-height: 380px; }
.home-hero.poster .hero-bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.hero-scrim { position: absolute; inset: 0; background: linear-gradient(rgba(22,28,15,0.30), rgba(22,28,15,0.55)); pointer-events: none; z-index: 1; }
.hero-center { position: absolute; inset: 0; z-index: 2; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 1rem; pointer-events: none; }
.hero-center > * { pointer-events: auto; }
.hero-center h1 { color: #fff; font-size: clamp(2.1rem, 5.5vw, 3.8rem); font-weight: 800; letter-spacing: -0.02em; line-height: 1.08; margin-bottom: 1.4rem; text-shadow: 0 2px 18px rgba(0,0,0,0.35); }
.hero-center h1 em { color: #F0C876; font-style: normal; }
.poster-search { width: min(640px, 94vw); padding: 0.35rem 0.6rem 0.35rem 0.4rem; box-shadow: 0 10px 40px rgba(0,0,0,0.28); margin-top: 0; }
.poster-search input { font-size: 16.5px; padding: 0.65rem 0.5rem; }
.hero-links { display: flex; gap: 1.8rem; margin-top: 1.3rem; flex-wrap: wrap; justify-content: center; }
.hero-link { background: none; border: none; cursor: pointer; font-family: inherit; color: #fff; font-size: 15.5px; font-weight: 700; text-decoration: underline; text-underline-offset: 4px; }
.home-hero.poster .near-me-result { color: #fff; font-weight: 600; margin-top: 0.9rem; text-shadow: 0 1px 8px rgba(0,0,0,0.4); }
.mission { max-width: 44rem; margin: 2.5rem auto 0; padding: 1.6rem 2rem 0; border-top: 1px solid var(--cream-dark); text-align: center; }
.mission p { font-family: var(--sans); font-size: 14.5px; font-weight: 300; color: var(--ink-mid); line-height: 1.7; }
.mission b { font-weight: 700; color: var(--ink); }
.mission a, .footer-about a { color: var(--moss); }
.footer-about p a { display: inline; margin: 0; }
.report-line { font-size: 13px; font-weight: 300; color: var(--ink-mid); margin: 0.3rem 0 0.7rem; line-height: 1.6; }
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; max-width: 62rem; margin: 0 auto; padding: 0.4rem 2rem 2.4rem; }
.step { display: block; text-decoration: none; color: var(--ink); font-family: var(--sans); text-align: center; }
.step-ico { display: inline-flex; align-items: center; justify-content: center; width: 46px; height: 46px; border-radius: 50%; background: var(--moss-light); color: var(--moss); margin-bottom: 0.6rem; }
.step-ico svg { width: 22px; height: 22px; }
.step b { display: block; font-size: 1.05rem; font-weight: 700; margin-bottom: 0.25rem; }
.step span:last-child { display: block; font-size: 13.5px; font-weight: 300; color: var(--ink-mid); line-height: 1.6; max-width: 19rem; margin: 0 auto; }
.step:hover b { text-decoration: underline; }
@media (max-width: 800px) {
  .steps { grid-template-columns: 1fr; gap: 1.4rem; padding: 0.2rem 1.5rem 1.8rem; text-align: left; }
  .step { display: grid; grid-template-columns: 46px 1fr; column-gap: 0.9rem; text-align: left; align-items: start; }
  .step-ico { grid-row: 1 / span 2; margin-bottom: 0; }
  .step b { margin-bottom: 0.1rem; }
  .step span:last-child { max-width: none; margin: 0; }
}
.hero-sub { padding: 1.6rem 2rem; text-align: center; }
.hero-sub p { max-width: 44rem; margin: 0 auto; font-size: 14.5px; color: var(--ink-mid); line-height: 1.65; }
.hero-search input { border-radius: 999px; flex: 1; min-width: 0; border: 1px solid var(--cream-dark); border-radius: 8px; padding: 0.65rem 0.9rem; font-family: var(--sans); font-size: 15px; background: #fff; color: var(--ink); }
.hero-search input:focus { outline: 2px solid var(--moss); border-color: var(--moss); }
.hero-search .go-btn { margin-top: 0; }
.go-btn.ghost { background: none; color: var(--moss); border: 1px solid var(--moss); }
.pin:hover { transform: scale(1.15); }
.pin.active { background: var(--ink); transform: scale(1.25); z-index: 5; }

/* Tree pins: a drawn silhouette instead of a number, so the map reads as a
   place full of trees rather than a numbered list. */
.pin-tree { position: relative; width: 34px; height: 34px; border-radius: 50%; background: var(--cream);
  border: 2px solid var(--moss); box-shadow: 0 3px 10px rgba(26,26,20,0.28); cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: transform 0.18s ease, box-shadow 0.18s ease; }
.pin-tree svg { width: 21px; height: 21px; color: var(--moss); transition: color 0.18s ease; }
.pin-tree:hover { transform: scale(1.12); box-shadow: 0 5px 16px rgba(26,26,20,0.34); }
.pin-tree.active { background: var(--moss); transform: scale(1.2); z-index: 5; }
.pin-tree.active svg { color: var(--cream); }
.pin-rank { position: absolute; top: -3px; right: -3px; min-width: 17px; height: 17px; border-radius: 9px;
  background: var(--ink); color: #fff; font-family: var(--sans); font-size: 10px; font-weight: 600;
  line-height: 17px; text-align: center; border: 2px solid var(--cream); }
.pin-tree.active .pin-rank { background: var(--cream); color: var(--ink); border-color: var(--moss); }
/* The walk. On a phone this sits fixed at the bottom, because that is where a
   thumb is when someone is standing in the street holding a coffee. */
/* Compact floating card, not a full-width bar: the map and its attribution
   stay visible, and "Where am I" never collides with the map edge. */
/* The walks block: the picker sits directly above the directions bar, so the
   choice and its consequence read as one control. AllTrails' convention of a
   route card carrying distance and duration up front, sized for our one page. */
.walks { position: absolute; left: 1rem; bottom: 1.6rem; z-index: 5;
  width: calc(100% - 2rem); max-width: 420px; }
.walk-picker { display: flex; gap: 0.4rem; margin-bottom: 0.5rem;
  overflow-x: auto; scrollbar-width: none; padding-bottom: 2px; }
.walk-picker::-webkit-scrollbar { display: none; }
.walk-pick { flex: 0 0 auto; cursor: pointer; text-align: left;
  background: #fff; color: var(--ink);
  border: 1px solid var(--cream-dark); border-radius: 11px;
  padding: 0.45rem 0.7rem; font-family: var(--sans); line-height: 1.2;
  box-shadow: 0 2px 10px rgba(0,0,0,0.14); }
.walk-pick.is-on { background: var(--moss); color: #fff; border-color: var(--moss); }
.walk-pick-name { display: block; font-size: 13.5px; font-weight: 600; }
.walk-pick-meta { display: block; font-size: 11.5px; opacity: 0.75; margin-top: 1px; }
.tree-noph { display: flex; gap: 1.1rem; align-items: center; margin: 0 0 1.5rem;
  padding: 1.1rem 1.25rem; background: var(--surface); border-radius: 14px; }
.tree-noph-art { flex-shrink: 0; width: 62px; height: 62px; color: var(--moss);
  display: inline-flex; align-items: center; justify-content: center; opacity: 0.9; }
.tree-noph-art svg { width: 100%; height: 100%; fill: currentColor; }
.tree-noph figcaption { font-size: 13.5px; line-height: 1.45; color: var(--ink-mid); }
.tree-noph figcaption b { display: block; color: var(--ink); font-size: 15px; margin-bottom: 2px; }
.route-name { display: block; font-size: 12.5px; font-weight: 600; opacity: 0.9; }
/* Not on the chosen walk: dimmed, never hidden. Every tree stays in the
   document for a reader and a crawler; only the emphasis moves. */
.pin-off { opacity: 0.35; }
.card-off { opacity: 0.5; }
.route-bar { position: relative; z-index: 5;
  display: flex; gap: 0.5rem; align-items: stretch; width: 100%; }
.route-go { flex: 1; display: flex; flex-direction: column; justify-content: center;
  background: var(--moss); color: #fff; text-decoration: none; padding: 0.7rem 1.1rem;
  border-radius: 12px; font-size: 15px; font-weight: 500; line-height: 1.25;
  box-shadow: 0 2px 12px rgba(0,0,0,0.18); }
.route-go:hover { background: #2f4717; }
.route-meta { display: block; font-weight: 400; font-size: 12.5px; opacity: 0.85; margin-top: 2px; }
.route-gps { background: #fff; color: var(--ink); border: 1px solid var(--cream-dark);
  border-radius: 12px; padding: 0.7rem 0.9rem; font-family: var(--sans); font-size: 14px;
  cursor: pointer; box-shadow: 0 2px 12px rgba(0,0,0,0.18); white-space: nowrap; }
.route-gps[aria-pressed="true"] { background: var(--moss-light); border-color: var(--moss); }
.suggest-form { display: flex; flex-direction: column; gap: 0.9rem; margin: 1.5rem 0; max-width: 34rem; }
.suggest-form label { font-size: 13.5px; font-weight: 700; display: flex; flex-direction: column; gap: 0.35rem; }
.sg-hint { font-weight: 400; color: var(--ink-light); font-size: 12.5px; }
.suggest-form input, .suggest-form select, .suggest-form textarea { font-family: var(--sans); font-size: 14px; padding: 0.65rem 0.85rem; border: 1px solid var(--cream-dark); border-radius: 10px; background: #fff; }
.suggest-form input:focus, .suggest-form select:focus, .suggest-form textarea:focus { outline: 2px solid var(--moss); outline-offset: 1px; }
.suggest-form .go-btn { align-self: flex-start; cursor: pointer; border: none; font-family: inherit; }
.sg-note { font-size: 13px; color: var(--ink-mid); min-height: 1em; }
.report-btn { display: inline-block; margin: 4px 6px 0 0; padding: 5px 12px; border: 1px solid var(--cream-dark); border-radius: 999px; font-size: 12.5px; color: var(--ink-mid); text-decoration: none; }
.report-btn:hover { border-color: var(--moss); color: var(--moss); }
.subtle-suggest { font-size: 13px; color: var(--ink-light); }
.subtle-suggest a { color: var(--moss); }
.hero-kicker { font-family: var(--sans); font-weight: 800; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.07em; color: var(--moss); margin-bottom: 0.5rem; }
.hero-note { margin-top: 0.75rem; font-size: 13px; color: var(--ink-light); }
.home-cta { display: inline-block; background: var(--moss); color: #fff; text-decoration: none;
  padding: 0.6rem 1.1rem; border-radius: 6px; font-size: 14px; font-weight: 500; margin-right: 0.5rem; }
.home-cta:hover { background: #2f4717; }
.home-cta.secondary { background: none; color: var(--moss); border: 1px solid var(--moss); }
.home-cta.secondary:hover { background: var(--moss-light); }
/* The passport. A visited tree goes green on the map and on its card. */
.seen-btn { float: right; display: inline-flex; align-items: center; gap: 0.4rem;
  background: none; border: 1px solid var(--cream-dark); border-radius: 999px;
  padding: 0.3rem 0.75rem; font-family: var(--sans); font-size: 12.5px;
  color: var(--ink-mid); cursor: pointer; transition: all 0.15s; }
.seen-btn:hover { border-color: var(--moss); color: var(--moss); }
.seen-mark { width: 13px; height: 13px; border-radius: 50%; border: 1.5px solid currentColor;
  display: inline-block; position: relative; }
.seen-btn[aria-pressed="true"] { background: var(--moss); border-color: var(--moss); color: #fff; }
.seen-btn[aria-pressed="true"] .seen-mark { background: #fff; border-color: #fff; }
.seen-btn[aria-pressed="true"] .seen-mark::after { content: ''; position: absolute;
  left: 4px; top: 1px; width: 3px; height: 7px; border: solid var(--moss);
  border-width: 0 1.5px 1.5px 0; transform: rotate(45deg); }
.pin-tree.seen { color: var(--moss); }
.pin-tree.seen .pin-rank { background: var(--moss); color: #fff; }
.passport { margin-top: 0.9rem; font-size: 13px; color: var(--ink-mid);
  background: var(--moss-light); border-radius: 6px; padding: 0.6rem 0.85rem; }
.passport strong { color: var(--moss); font-weight: 600; }
.passport.complete { background: var(--moss); color: #fff; }
.passport.complete strong { color: #fff; }
.passport-total { display: block; font-size: 12px; opacity: 0.8; margin-top: 2px; }
.passport-save { display: block; margin-top: 6px; background: none; border: none; padding: 0;
  font-family: var(--sans); font-size: 12px; color: var(--moss); text-decoration: underline;
  cursor: pointer; text-align: left; }
.passport.complete .passport-save { color: #fff; }
.pin-me { width: 16px; height: 16px; border-radius: 50%; background: #1E6FD9;
  border: 3px solid #fff; box-shadow: 0 0 0 4px rgba(30,111,217,0.25); }
@media (max-width: 800px) {
  .bar-logo { font-size: 0.92rem; letter-spacing: 0.04em; white-space: nowrap; }
  .bar-logo svg { width: 20px; height: 18px; }
  .bar-links { display: flex; align-items: center; gap: 0.55rem; }
  .bar-links a { margin-left: 0; }
  .only-desktop { display: none !important; }
  .only-mobile { display: block; }
  .nav-drop-menu a.only-mobile { display: flex; }
  .nav-drop { margin-left: 0; }
  .nav-drop summary { font-size: 13px; padding: 0.35rem 0.2rem; }
  .nav-drop summary .sum-desktop { display: none; }
  .nav-drop summary .sum-mobile { display: inline; }
  .nav-drop-menu { position: fixed; left: 0.75rem; right: 0.75rem; top: 3.4rem; min-width: 0; }
  .bar-links a.bar-cta { padding: 0.35rem 0.6rem; font-size: 12px; white-space: nowrap; }
  .footer-cols { flex-direction: column; gap: 1.5rem; }
  .action-row .go-btn, .action-row .seen-btn { font-size: 13px; padding: 0.6rem 0.9rem; }

  .walks { position: fixed; left: 0.75rem; right: 0.75rem; width: auto;
    bottom: calc(0.75rem + env(safe-area-inset-bottom)); }
  .route-bar { position: relative; left: auto; right: auto; bottom: auto; }
  /* The fixed bar would otherwise sit on top of the last tree in the list.
     Measured at 375px: the bar alone is 96px, and a walk picker above it takes
     the block to 132px, so a city with several walks needs the extra room. */
  .panel { padding-bottom: calc(6rem + env(safe-area-inset-bottom)); }
  .panel:has(~ .stage .walk-picker),
  .split:has(.walk-picker) .panel { padding-bottom: calc(9.5rem + env(safe-area-inset-bottom)); }
}
.maplibregl-popup-content { font-family: var(--sans); font-size: 13px; padding: 0.75rem 1rem; border-radius: 4px; }
.maplibregl-popup-content strong { font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em; font-size: 15px; font-weight: 400; }

@media (max-width: 800px) {
  .bar-logo { font-size: 0.92rem; letter-spacing: 0.04em; white-space: nowrap; }
  .bar-logo svg { width: 20px; height: 18px; }
  .bar-links { display: flex; align-items: center; gap: 0.55rem; }
  .bar-links a { margin-left: 0; }
  .only-desktop { display: none !important; }
  .only-mobile { display: block; }
  .nav-drop-menu a.only-mobile { display: flex; }
  .nav-drop { margin-left: 0; }
  .nav-drop summary { font-size: 13px; padding: 0.35rem 0.2rem; }
  .nav-drop summary .sum-desktop { display: none; }
  .nav-drop summary .sum-mobile { display: inline; }
  .nav-drop-menu { position: fixed; left: 0.75rem; right: 0.75rem; top: 3.4rem; min-width: 0; }
  .bar-links a.bar-cta { padding: 0.35rem 0.6rem; font-size: 12px; white-space: nowrap; }
  .footer-cols { flex-direction: column; gap: 1.5rem; }
  .action-row .go-btn, .action-row .seen-btn { font-size: 13px; padding: 0.6rem 0.9rem; }

  .split { flex-direction: column-reverse; height: auto; }
  .panel { width: 100%; max-width: none; height: auto; overflow: visible; border-right: none; }
  /* Smaller map on phones: the list is what people scan, the map is context. */
  .stage { position: sticky; top: var(--header-h); height: 42vh; height: 42svh; min-height: 300px; z-index: 5; }
  .crumbs { display: none; }
  .tree-card { padding: 1.25rem 1.1rem; }
  .tree-meta, .tree-story, .tree-more { margin-left: 0; }
  .tree-card-photo { aspect-ratio: 16 / 10; }
  .bar-links a { margin-left: 0.7rem; font-size: 12px; }
  .bar-links a.bar-cta { padding: 0.3rem 0.5rem; }
  /* Keep the bar on one line on phones: secondary links stay reachable from
     the homepage and from the pages themselves. */
  header.bar { box-shadow: 0 1px 0 rgba(26,32,18,0.06); flex-wrap: nowrap; padding: 0 1rem; }
  .bar-logo { display: inline-flex; align-items: center; gap: 0.5rem; font-family: var(--sans); font-weight: 800; font-size: 1.02rem; letter-spacing: 0.07em; text-decoration: none; color: var(--ink); }
  .bar-links { display: flex; align-items: center; white-space: nowrap; }
  .bar-links a.bar-secondary { display: none; }
  /* Get to the trees faster: the intro is still fully in the HTML. */
  .panel-head .lede { display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; }
  .panel-head { padding: 1.25rem 1.1rem 1rem; }
  .panel-head h1 { font-size: 1.6rem; }
  .home-hero { height: 60vh; }
  /* Phones measure vh against the tall viewport, so the same number reads
     bigger than it is; svh is what the visitor actually sees. */
  .home-hero.poster { height: min(56svh, 460px); min-height: 340px; }
  .hero-overlay { left: 1rem; right: 1rem; top: 1rem; max-width: none; padding: 1.25rem 1.5rem; }
  .page { padding: 2rem 1.5rem; }

}
"""

PAGE_SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="google-site-verification" content="uVA_hyHOJQWM3wH90g2QwP5qw2pk1WlPrtZ-lZKq2Hc">
<title>%%TITLE%%</title>
<meta name="description" content="%%DESCRIPTION%%">
<link rel="canonical" href="%%CANONICAL%%">
<meta property="og:title" content="%%TITLE%%">
<meta property="og:description" content="%%DESCRIPTION%%">
<meta property="og:type" content="%%OGTYPE%%">
<meta property="og:url" content="%%CANONICAL%%">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@400..900&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 68 64"><ellipse cx="34" cy="24" rx="24" ry="16" fill="%233A5222"/><circle cx="20" cy="23" r="11" fill="%234A6B2A"/><circle cx="48" cy="23" r="11" fill="%234A6B2A"/><circle cx="34" cy="12" r="11" fill="%235B7F35"/><path d="M31 62 h5.6 l-1.2-16 h-3.2z" fill="%236B4F33"/></svg>'>
<link rel="stylesheet" href="%%ROOTPATH%%assets/style.css">
%%HEAD_EXTRA%%
</head>
<body>
<header class="bar">
  <a href="%%ROOTPATH%%" class="bar-logo"><svg width="25" height="22" viewBox="0 0 68 64" fill="none" aria-hidden="true"><ellipse cx="34" cy="24" rx="24" ry="16" fill="#3A5222"/><circle cx="20" cy="23" r="11" fill="#4A6B2A"/><circle cx="48" cy="23" r="11" fill="#4A6B2A"/><circle cx="34" cy="12" r="11" fill="#5B7F35"/><circle cx="25" cy="15" r="7" fill="#86A34D"/><circle cx="51" cy="14" r="3.2" fill="#D9A13F"/><path d="M31 62 h5.6 l-1.2-16 c2.6-1.8 5.4-4.4 7-6.6 l-1.6-1.4 c-1.8 2-4 3.8-5.6 4.6 l-.3-5.8 h-2 l-.4 8.4 c-1.6-.9-3.6-2.7-5-4.4 l-1.6 1.4 c1.8 2.5 4.4 4.9 6.4 6z" fill="#6B4F33"/></svg><span>Ancient Trees</span></a>
  <nav class="bar-links"><a href="%%ROOTPATH%%explore" class="only-desktop">Map</a><details class="nav-drop"><summary><span class="sum-desktop">Explore</span><span class="sum-mobile">Menu</span></summary><div class="nav-drop-menu"><a href="%%ROOTPATH%%explore" class="only-mobile"><span class="mi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.6"/></svg></span>Map</a><a href="%%ROOTPATH%%cities"><span class="mi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 21V8l5-3v16M9 21V10l6 2v9M15 21V7l5 2v12"/><path d="M2 21h20"/></svg></span>Cities</a><a href="%%ROOTPATH%%countries"><span class="mi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 3 2.6 15 0 18M12 3c-2.6 3-2.6 15 0 18"/></svg></span>Countries</a><a href="%%ROOTPATH%%species"><span class="mi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20C6 10 12 4 20 4c0 8-6 14-16 16z"/><path d="M4 20c4-6 8-9 12-11"/></svg></span>Species</a><a href="%%ROOTPATH%%parks"><span class="mi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22V12"/><path d="M12 12c0-4 3-7 7-7 0 4-3 7-7 7z"/><path d="M12 12c0-3.5-2.5-6-6-6 0 3.5 2.5 6 6 6z"/></svg></span>Parks</a><a href="%%ROOTPATH%%collections"><span class="mi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 4h12a1 1 0 0 1 1 1v16l-7-4-7 4V5a1 1 0 0 1 1-1z"/></svg></span>Collections</a><a href="%%ROOTPATH%%contribute"><span class="mi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/></svg></span>Suggest a tree</a>%%LOGIN_MENU%%</div></details>%%LOGIN%%<a href="%%ROOTPATH%%app" class="bar-cta">Get the app</a></nav>
</header>
%%BODY%%
%%FOOTER%%
<script>
window.at = window.at || {};
at.track = function(name, detail) {
  try {
    if (localStorage.getItem('at_notrack') === '1') { return; }
    var ev = {name: String(name).slice(0, 40), path: location.pathname.slice(0, 120)};
    if (detail) { ev.detail = String(detail).slice(0, 60); }
    var body = JSON.stringify(ev);
    navigator.sendBeacon
      ? navigator.sendBeacon('SB_URL/rest/v1/events?apikey=SB_KEY',
          new Blob([body], {type: 'application/json'}))
      : fetch('SB_URL/rest/v1/events', {method: 'POST', keepalive: true,
          headers: {'apikey': 'SB_KEY', 'Content-Type': 'application/json',
                    'Prefer': 'return=minimal'}, body: body});
  } catch (e) {}
};
document.addEventListener('click', function(e) {
  var a = e.target && e.target.closest ? e.target.closest('a, button') : null;
  if (!a) return;
  var h = a.getAttribute('href') || '';
  if (h.indexOf('google.com/maps/dir') !== -1) { at.track('directions'); }
  else if (h.indexOf('/app') === 0 || h === 'app' || h === '../app' || h === './app') { at.track('app-cta'); }
});
</script>
%%SCRIPTS%%
%%ANALYTICS%%
</body>
</html>
"""

# Cloudflare Web Analytics: cookieless and aggregate only, so no consent banner
# and no personal data. Chosen over Google Analytics on 2026-07-21 for exactly
# that reason: a consent popup is friction on the street, which is where this
# site has to work. Empty string switches it off everywhere.
# The project identity, never the owner's name (Hidde, 2026-08-01: "ik wil
# mijn naam niet noemen dus dat email adres"). Set up as a forward at the
# registrar; nothing on the site or in a reply ever needs his own address.
CONTACT_EMAIL = "info@ancienttrees.app"

ANALYTICS_TOKEN = "fcbbfb8b426c4f6aa2066b00be6454f6"

# The owner's own visits were most of the traffic (Hidde, 2026-08-01: "deze 60
# directe bezoeken zijn wss allemaal door mij gedaan"), which makes the numbers
# a mirror rather than a measurement. Visiting any page with ?notrack=1 sets a
# flag in that browser; from then on neither the Cloudflare beacon nor our own
# events fire there. ?notrack=0 undoes it. Per browser and per device, because
# a cookieless setup has nothing else to recognise, and stored in localStorage
# rather than a cookie so no consent question appears.
ANALYTICS_SNIPPET = (
    "<script>\n"
    "(function() {{\n"
    "  try {{\n"
    "    var p = new URLSearchParams(location.search);\n"
    "    if (p.get('notrack') === '1') {{ localStorage.setItem('at_notrack', '1'); }}\n"
    "    else if (p.get('notrack') === '0') {{ localStorage.removeItem('at_notrack'); }}\n"
    "    if (localStorage.getItem('at_notrack') === '1') {{ return; }}\n"
    "  }} catch (e) {{}}\n"
    "  var s = document.createElement('script');\n"
    "  s.defer = true;\n"
    "  s.src = 'https://static.cloudflareinsights.com/beacon.min.js';\n"
    "  s.setAttribute('data-cf-beacon', '{{\"token\": \"{token}\"}}');\n"
    "  document.head.appendChild(s);\n"
    "}})();\n"
    "</script>"
)

FOOTER = """
<footer>
  <div class="footer-cols">
    <div class="footer-col footer-about">
      <span class="footer-logo">Ancient Trees</span>
      <p>We are on a mission to map every remarkable tree in the world, and we could use your help. If you know a good tree, or spot a mistake on one of these pages, <a href="%%ROOTPATH%%contribute">tell us</a>. We work on this database every day.</p>
    </div>
    <div class="footer-col">
      <h4>Explore</h4>
      <a href="%%ROOTPATH%%explore">Map</a>
      <a href="%%ROOTPATH%%in-season">In season now</a>
      <a href="%%ROOTPATH%%cities">Cities</a>
      <a href="%%ROOTPATH%%countries">Countries</a>
      <a href="%%ROOTPATH%%species">Species</a>
      <a href="%%ROOTPATH%%collections">Collections</a>
    </div>
    <div class="footer-col">
      <h4>Ancient Trees</h4>
      <a href="%%ROOTPATH%%app">The app</a>
      <a href="%%ROOTPATH%%contribute">Suggest a tree</a>
      <a href="%%ROOTPATH%%privacy">Privacy</a>
    </div>
  </div>
  <span class="footer-note">&copy; %%YEAR%% Ancient Trees, ancienttrees.app. Map &copy; OpenFreeMap, OpenMapTiles, OpenStreetMap contributors. Walking routes by Valhalla via FOSSGIS, on OpenStreetMap data. Photos carry their own credits and open licences.</span>
</footer>
"""

ERRORS = []
REGISTER_ASSET = ""  # the register layer's GeoJSON, written beside the page


def esc(s):
    return html.escape(str(s), quote=True)


def dist_label(a_loc, b_loc):
    """Human distance between two tree locations: '350 m' or '2.1 km'."""
    m = haversine((a_loc["latitude"], a_loc["longitude"]),
                  (b_loc["latitude"], b_loc["longitude"])) * 1000
    return "%d m" % (round(m / 10) * 10) if m < 1000 else "%.1f km" % (m / 1000)


def slugify(name):
    s = name.lower().replace("'", "").replace("’", "")
    if s.startswith("the "):
        s = s[4:]
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def age_token(tree):
    """The number a page's title quotes for this tree's age.

    Must be the number the age_estimate text itself states, even when a
    qualifier ("roughly", "over", "traditionally") comes first: re.match
    anchored the search to the start of the string, so "roughly 440 years"
    silently fell back to age_min (a range bound never meant to be quoted
    on its own) instead of the 440 the text actually says (fresh-eyes
    review, 2026-08-06, found on 43 cities including a case with no title
    number in the text at all)."""
    m = re.search(r"(\d[\d,]*\+?)", tree.get("age_estimate", ""))
    return m.group(1) if m else str(tree.get("age_min", ""))


def species_common(tree):
    return tree.get("species", "").split(" (")[0]


def meta_from_story(story):
    """Build a meta description from the story's opening sentences, max DESC_MAX.

    A single sentence longer than the limit used to be cut mid-clause, which
    silently threw away whatever the sentence was building toward (fresh-eyes
    review, 2026-08-02: a description that stopped at "a single word" without
    ever saying the word). Now it cuts on a word boundary and marks the cut."""
    sentences = re.split(r"(?<=[.!?]) ", story)
    out = ""
    for s in sentences:
        if out and len(out) + 1 + len(s) > DESC_MAX:
            break
        out = (out + " " + s).strip()
        if len(out) > DESC_MAX:
            out = out[:DESC_MAX - 1].rsplit(" ", 1)[0].rstrip(",.;:") + "\u2026"
            break
    return out


def fit_title(candidates, page):
    for c in candidates:
        if len(c) <= TITLE_MAX:
            return c
    ERRORS.append(f"{page}: no title candidate fits {TITLE_MAX} chars: {candidates[-1]!r}")
    return candidates[-1]


def haversine(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def site_graph():
    """Site-level WebSite + Person schema, on every page.

    Owner-privacy rule (Hidde, 2026-07-28): no personal name anywhere public,
    so the site-level entity is the Organization, not a Person. The About page
    and Person schema stay parked until Hidde explicitly reopens them.
    """
    return [
        {"@type": "WebSite", "name": "Ancient Trees", "url": BASE_URL},
        {"@type": "Organization", "name": "Ancient Trees", "url": BASE_URL},
    ]


MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def season_intensities(peak_months):
    """A 0..1 value for each of the 12 months, humped over the peak.

    Derived from the peak months rather than asked of a run, because nobody can
    honestly hand-score twelve numbers per tree. A gaussian falloff, and
    deliberately non-wrapping: a ginkgo is gold in November and bare in June, it
    is not faintly gold in June, so December does not bleed back into summer.
    """
    sigma = 1.4
    out = []
    for m in range(1, 13):
        dist = min(abs(m - p) for p in peak_months)
        out.append(math.exp(-(dist * dist) / (2 * sigma * sigma)))
    return out


# The phenology vocabulary (Hidde, 2026-07-29, his PictureThis point: say WHY
# a tree peaks, not just when). Five kinds, each with a small icon. `kind` in
# best_time is authoritative; where it is missing the build derives one from
# unambiguous words in the label, and derives nothing when in doubt. Runs
# backfill the field properly per Step 3.
KIND_ICONS = {
    "bare silhouette": '<svg viewBox="0 0 20 20" fill="none" stroke="#8C8577" stroke-width="1.6" stroke-linecap="round"><path d="M10 18V9"/><path d="M10 11 6 6M10 11l4-5M10 8 7.5 3.5M10 8l2.5-4.5"/></svg>',
    # PictureThis grammar (Hidde, 2026-08-01: "deze vorm en iconen meer
    # namaken"): each kind carries its own colour; rounded, friendly forms.
    "flowers": '<svg viewBox="0 0 20 20" aria-hidden="true"><g fill="#E8705F"><ellipse cx="10" cy="4.6" rx="2.6" ry="3.2"/><ellipse cx="15.4" cy="10" rx="3.2" ry="2.6"/><ellipse cx="10" cy="15.4" rx="2.6" ry="3.2"/><ellipse cx="4.6" cy="10" rx="3.2" ry="2.6"/></g><circle cx="10" cy="10" r="2.1" fill="#fff"/></svg>',
    "fruit": '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="11.6" r="6" fill="#E8A33D"/><path d="M10 5.8 Q10.2 3.4 12.6 2.6" stroke="#7FA653" stroke-width="1.6" fill="none" stroke-linecap="round"/><ellipse cx="13.4" cy="3.4" rx="2.2" ry="1.3" fill="#7FA653" transform="rotate(-24 13.4 3.4)"/><circle cx="8" cy="10" r="1.1" fill="#fff" opacity=".55"/></svg>',
    "autumn colour": '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 2 C14.5 5 17 9 17 12.5 A7 7 0 0 1 3 12.5 C3 9 5.5 5 10 2z" fill="#D97843"/><path d="M10 5.5 v11" stroke="#fff" stroke-width="1.2" opacity=".7"/></svg>',
    "catkins": '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 4 q3 -1.6 6 -1.6 q3.6 0 6 1.6" stroke="#7FA653" stroke-width="1.6" fill="none" stroke-linecap="round"/><g stroke="#C9B458" stroke-width="2.4" stroke-linecap="round"><path d="M6 5 q-.4 4.4 .5 7.6"/><path d="M10 4.6 q0 5.4 .9 9.6"/><path d="M14 5 q.4 3.8 -.3 7"/></g></svg>',
    "fresh leaves": '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M16.5 3.5 C10 3.5 5.5 7.5 5 14 c6 .6 10.5 -3 11.5 -10.5z" fill="#7FA653"/><path d="M5.5 16.5 C7.5 12 11.5 8 16 5.5" stroke="#4A6B2A" stroke-width="1.4" fill="none" stroke-linecap="round"/></svg>',
}
KIND_ALIASES = {
    "flowering": "flowers", "blossom": "flowers", "bloom": "flowers",
    "autumn": "autumn colour", "fall color": "autumn colour",
    "fall colour": "autumn colour", "autumn color": "autumn colour",
}
KIND_HINTS = [
    ("catkins", ("catkin",)),
    ("flowers", ("flower", "blossom", "bloom", "wisteria")),
    ("autumn colour", ("autumn", "gold", "golden", "scarlet", "crimson", "turns", "fall colour", "fall color")),
    ("fruit", ("fruit", "berries", "acorn", "fig ripen", "chestnut drop")),
    ("fresh leaves", ("fresh leaves", "new leaves", "leaf-out", "unfurl")),
]


def season_kind(bt):
    """Canonical phenology kind for a best_time, or '' when honestly unknown."""
    raw = (bt.get("kind") or "").strip().lower()
    if raw:
        raw = KIND_ALIASES.get(raw, raw)
        if raw in KIND_ICONS:
            return raw
        ERRORS.append(f"unknown best_time.kind {raw!r}; allowed: {sorted(KIND_ICONS)}")
        return ""
    label = (bt.get("label") or "").lower()
    hits = [k for k, words in KIND_HINTS if any(w in label for w in words)]
    return hits[0] if len(hits) == 1 else ""


def smooth_path(points):
    """A rounded SVG path through the points, Catmull-Rom turned into cubics."""
    if len(points) < 2:
        return ""
    d = f"M {points[0][0]:.1f},{points[0][1]:.1f}"
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1, p2 = points[i], points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2
        c1x = p1[0] + (p2[0] - p0[0]) / 6
        c1y = p1[1] + (p2[1] - p0[1]) / 6
        c2x = p2[0] - (p3[0] - p1[0]) / 6
        c2y = p2[1] - (p3[1] - p1[1]) / 6
        d += f" C {c1x:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d


def season_curve(tree):
    """A seasonal peak chart, in the spirit of PictureThis but in our own skin.

    The strongest reason a page gives someone to leave the house, turned from a
    line of text into a curve across the year with the peak marked and a 'you
    are here' dot for the current month. Only trees with a real season get one;
    evergreens and ancient yews carry no best_time and no chart appears.
    """
    bt = tree.get("best_time")
    if not bt or not bt.get("label") or not bt.get("months"):
        return ""

    peaks = bt["months"]
    vals = season_intensities(peaks)
    now = date.today().month
    in_season = now in peaks

    W, H, pad_t, pad_b, pad_x = 320.0, 120.0, 22.0, 24.0, 10.0
    plot_h = H - pad_t - pad_b
    step = (W - 2 * pad_x) / 11.0
    pts = [(pad_x + i * step, pad_t + (1 - v) * plot_h) for i, v in enumerate(vals)]

    line = smooth_path(pts)
    area = line + f" L {pts[-1][0]:.1f},{pad_t + plot_h:.1f} L {pts[0][0]:.1f},{pad_t + plot_h:.1f} Z"

    peak_i = max(range(12), key=lambda i: vals[i])
    peak_x, peak_y = pts[peak_i]
    now_x = pts[now - 1][0]

    # All twelve month labels plus light gridlines (the PictureThis frame).
    ticks = "".join(
        f'<text x="{pts[i][0]:.1f}" y="{H - 6:.0f}" class="sc-m">{MONTH_ABBR[i]}</text>'
        for i in range(12)
    )
    grid = "".join(
        f'<line x1="{pad_x:.1f}" y1="{pad_t + plot_h * f:.1f}" x2="{W - pad_x:.1f}" y2="{pad_t + plot_h * f:.1f}" class="sc-grid"/>'
        for f in (0.25, 0.5, 0.75)
    )

    now_marker = (
        f'<line x1="{now_x:.1f}" y1="{pad_t - 6:.1f}" x2="{now_x:.1f}" y2="{pad_t + plot_h:.1f}" class="sc-now"/>'
        f'<text x="{now_x:.1f}" y="{pad_t - 10:.1f}" class="sc-nowlabel">now</text>'
    )

    kind = season_kind(bt)
    chip = (f'<span class="sc-chip">{KIND_ICONS[kind]}{esc(kind)}</span>'
            if kind else "")
    peak_badge = ""
    if kind:
        # PictureThis form: a white rounded badge with the kind icon floating
        # at the curve's peak. Positioned in % so it scales with the svg.
        bx = peak_x / W * 100
        by = peak_y / H * 100
        peak_badge = (f'<span class="sc-peakbadge" style="left:{bx:.1f}%;top:{by:.1f}%">'
                      f'{KIND_ICONS[kind]}</span>')
    now_badge = '<span class="best-now">at its best right now</span>' if in_season else ""

    return f"""
<figure class="season">
  <figcaption class="season-head">
    <span>Best time to visit</span>{now_badge}
  </figcaption>
  <div class="season-plot">
  {peak_badge}
  <svg viewBox="0 0 {W:.0f} {H:.0f}" class="season-svg" role="img" aria-label="Seasonal peak: {esc(bt['label'])}">
    {grid}
    <path d="{area}" class="sc-area"/>
    <path d="{line}" class="sc-line"/>
    {now_marker}
    <circle cx="{peak_x:.1f}" cy="{peak_y:.1f}" r="4.5" class="sc-peak"/>
    {ticks}
  </svg>
  </div>
  <p class="season-legend">{chip}</p>
  <p class="season-label">{esc(bt['label'])}</p>
</figure>"""


def best_time_short(tree):
    """One short phrase for the city-page card, without the full sentence."""
    bt = tree.get("best_time")
    if not bt or not bt.get("label"):
        return ""
    now = date.today().month
    if now in (bt.get("months") or []):
        return ' &middot; <span class="best-now-inline">at its best now</span>'
    return ""


def breadcrumb_schema(items, page_url=None):
    # Google requires every ListItem to carry an "item". Crumbs without a page of
    # their own (a country, and the current page itself) fall back to the page's
    # own canonical URL, which is what Google's own docs prescribe for the last
    # crumb. Passing page_url is what makes those crumbs valid; without it they
    # are dropped, which is the "Missing field item" error Search Console flagged.
    elements = []
    last = len(items)
    for i, (name, url) in enumerate(items, 1):
        el = {"@type": "ListItem", "position": i, "name": name}
        if url:
            el["item"] = url
        elif i == last and page_url:
            # Only the final crumb may fall back to this page: that is what
            # Google's docs prescribe. An intermediate crumb doing the same
            # claimed the country WAS this tree page (fresh-eyes review,
            # 2026-08-02). A ListItem with a name and no item is valid.
            el["item"] = page_url
        elements.append(el)
    return {"@type": "BreadcrumbList", "itemListElement": elements}


def breadcrumb_html(items, rootpath):
    parts = []
    for name, url in items:
        if url:
            rel = url.replace(BASE_URL + "/", rootpath) if url != BASE_URL else rootpath
            rel = rel or rootpath or "."
            parts.append(f'<a href="{rel if rel else "."}">{esc(name)}</a>')
        else:
            parts.append(esc(name))
    return '<nav class="crumbs">' + " &rsaquo; ".join(parts) + "</nav>"


def ld_script(graph):
    payload = {"@context": "https://schema.org", "@graph": graph}
    return f'<script type="application/ld+json">{json.dumps(payload)}</script>'


def map_head():
    return f'<link rel="stylesheet" href="{MAPLIBRE_CSS}">'


def single_pin_script(lat, lng, label="1"):
    return f"""
<script src="{MAPLIBRE_JS}"></script>
<script>
var map = new maplibregl.Map({{
  container: 'map', style: '{MAP_STYLE}',
  center: [{lng}, {lat}], zoom: 14.5, scrollZoom: false,
  attributionControl: {{ compact: true }}
}});
map.addControl(new maplibregl.NavigationControl());
map.on('load', function() {{ map.resize(); }});
var el = document.createElement('div');
el.className = 'pin';
el.textContent = '{label}';
new maplibregl.Marker({{ element: el }}).setLngLat([{lng}, {lat}]).addTo(map);
</script>
"""


def haversine_km(a, b):
    """Straight line distance between two (lat, lng) points, in kilometres."""
    lat1, lng1 = math.radians(a[0]), math.radians(a[1])
    lat2, lng2 = math.radians(b[0]), math.radians(b[1])
    h = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lng2 - lng1) / 2) ** 2)
    return 2 * 6371.0 * math.asin(math.sqrt(h))


# Streets do not run in straight lines, so the crow-flies total always
# understates a real walk. 1.35 is the usual rule of thumb for dense European
# city centres. The number shown to a visitor is deliberately rounded and
# labelled "about", because promising 3.8 km and delivering 4.6 is the kind of
# small lie that loses trust on a hot afternoon.
DETOUR_FACTOR = 1.35
WALKING_KMH = 4.5


# A real afternoon on foot. Beyond this it stops being a walk and starts being
# a day out, and the honest move is to offer fewer trees rather than a number
# nobody will act on.
WALK_BUDGET_KM = 6.0
WALK_MIN_TREES = 3


def plan_walking_route(points, budget_km=WALK_BUDGET_KM):
    """Find the best walk through a cluster of trees, not through all of them.

    Routing through every tree only works in a compact city. London's ten are
    scattered from Totteridge to Kew: a single path is 69 km, which is not a
    walk and would make the site look like it cannot read its own data. So this
    grows a nearest neighbour path from each possible start and stops when the
    next tree would blow the budget, then keeps whichever attempt gathered the
    most trees (shortest wins a tie).

    Returns None when no honest walk exists, and the page then simply has no
    route bar. Fewer trees is a fine answer; a fake one is not.
    """
    n = len(points)
    if n < WALK_MIN_TREES:
        return None

    best = None
    for start in range(n):
        unvisited = set(range(n))
        unvisited.remove(start)
        order, total, current = [start], 0.0, start
        while unvisited:
            nxt = min(unvisited, key=lambda i: haversine_km(points[current], points[i]))
            step = haversine_km(points[current], points[nxt])
            if (total + step) * DETOUR_FACTOR > budget_km:
                break
            total += step
            order.append(nxt)
            unvisited.remove(nxt)
            current = nxt
        if len(order) < WALK_MIN_TREES:
            continue
        # More trees beats a shorter walk; between equals, take the shorter.
        if best is None or (len(order), -total) > (len(best[0]), -best[1]):
            best = (order, total)

    if best is None:
        return None

    order, total = best
    km = total * DETOUR_FACTOR
    return {
        "order": order,
        "count": len(order),
        "of": n,
        "km": round(km, 1),
        "minutes": int(round(km / WALKING_KMH * 60)),
    }


WALK_CLUSTER_M = 900       # two trees belong to the same walk if this close
WALK_NAME_STOP = {"the", "of", "de", "di", "da", "del", "della", "van", "op",
                  "and", "en", "a", "an", "in", "at", "on"}


def _walk_clusters(points, radius_m=WALK_CLUSTER_M):
    """Single-link clustering: trees joined when one is within radius of another.

    Chosen over k-means or a fixed grid because a walk is a chain, not a blob.
    Porto's seventeen trees run as a 1.6 km ribbon along the hill: any method
    that wants round clusters splits it, and single-link keeps it whole."""
    n = len(points)
    seen, groups = set(), []
    for i in range(n):
        if i in seen:
            continue
        stack, comp = [i], []
        while stack:
            k = stack.pop()
            if k in seen:
                continue
            seen.add(k)
            comp.append(k)
            for j in range(n):
                if j not in seen and haversine_km(points[k], points[j]) * 1000 <= radius_m:
                    stack.append(j)
        groups.append(sorted(comp))
    return groups


WALK_NAME_MAX = 34


def _area_head(area):
    """The place name out of a neighbourhood field.

    Three shapes appear in the data and all three need flattening, or one place
    counts as several and no name ever wins a vote: a trailing clause
    ("Parco Treves de' Bonfili, on Padua's walls"), a parenthetical that varies
    per tree ("Orto Botanico (arboretum section)" beside plain "Orto Botanico"),
    and a compound parish written both long and short ("Lordelo do Ouro e
    Massarelos" beside "Massarelos")."""
    head = str(area or "").split(",")[0]
    head = re.sub(r"\([^)]*\)?", "", head)          # drop parentheticals, even unclosed
    head = re.sub(r"\s+", " ", head).strip(" -/")
    return head


def _walk_name(members, markers):
    """Name a walk after the place most of its trees share.

    Falls back to nothing rather than inventing a name: an unnamed walk still
    says how many trees and how far, which is the part a visitor acts on. The
    place name is used whole, never trimmed to a word count: cutting "Lordelo
    do Ouro e Massarelos" to four words produced "Lordelo do Ouro e"."""
    counts = {}
    for idx in members:
        head = _area_head(markers[idx].get("area"))
        if len(head) >= 3:
            counts[head] = counts.get(head, 0) + 1
    if not counts:
        return ""
    # A compound parish and its short form are one place: fold a name that is
    # contained in a longer one into the longer, then re-vote.
    merged = {}
    for name, n in counts.items():
        parent = next((o for o in counts
                       if o != name and name.lower() in o.lower()), None)
        merged[parent or name] = merged.get(parent or name, 0) + n
    best, hits = max(merged.items(), key=lambda kv: (kv[1], -len(kv[0])))
    # A plurality, with a floor, so one tree never names a walk of eight.
    if hits < 2 or hits * 3 < len(members):
        return ""
    return best if len(best) <= WALK_NAME_MAX else ""


WALK_SPLIT_KM = 3.0      # past this a walk stops being an afternoon and becomes a route
COMBINED_MAX_KM = 6.0    # up to here "Both walks" is still offered as one outing
WALK_MAX_OVERLAP = 0.5   # two walks may never be more than half the same trees


def _leg_km(order, points):
    """Walking distance along an ordered route, detour factor included."""
    total = sum(haversine_km(points[order[i]], points[order[i + 1]])
                for i in range(len(order) - 1))
    return total * DETOUR_FACTOR


def _split_route(order, points, depth=0):
    """Cut a long route in half at its midpoint, into two DISJOINT halves.

    Hidde, 2026-08-08, having noticed walks are built as disjoint clusters:
    "you can use the same tree in several walks, does that open options?" It
    opens exactly one worth having. Eighteen cities had a single walk over
    2.5 km, Prague at 6.0 km and 79 minutes, which is a route rather than an
    afternoon. Splitting at the middle gives two real walks.

    The first version let the junction tree belong to both halves. Hidde saw
    the result on Amsterdam the same day and called it: two walks whose lines
    are welded together at the shared tree read as ONE walk on the overview
    map. So the halves are now disjoint, and the way to walk both is the
    explicit "Both walks" choice plan_walks adds when the whole route is
    still a doable afternoon.

    What it deliberately does NOT do is manufacture variety. Sharing trees
    freely would let any city be sliced into four walks that are the same trees
    wearing hats, which is the padding rule applied to walks instead of counts:
    Cadiz has five trees in 600 metres and should have one walk, not four.
    So a split happens only when a route is too long to walk in one go, and
    only while both halves still clear WALK_MIN_TREES."""
    km = _leg_km(order, points)
    if depth >= 2 or km <= WALK_SPLIT_KM or len(order) < WALK_MIN_TREES * 2:
        return [order]
    # cut where the accumulated distance passes halfway
    run, half, cut = 0.0, km / DETOUR_FACTOR / 2, len(order) // 2
    for i in range(len(order) - 1):
        run += haversine_km(points[order[i]], points[order[i + 1]])
        if run >= half:
            cut = i
            break
    cut = max(WALK_MIN_TREES - 1, min(cut, len(order) - WALK_MIN_TREES - 1))
    first, second = order[:cut + 1], order[cut + 1:]   # disjoint: no shared tree
    if len(first) < WALK_MIN_TREES or len(second) < WALK_MIN_TREES:
        return [order]
    return _split_route(first, points, depth + 1) + _split_route(second, points, depth + 1)


def _too_similar(a, b):
    """True when two walks are more than half the same trees."""
    sa, sb = set(a), set(b)
    return len(sa & sb) / min(len(sa), len(sb)) > WALK_MAX_OVERLAP

def plan_walks(markers, budget_km=WALK_BUDGET_KM):
    """Every honest walk in a city, not just the best one.

    Hidde, 2026-08-06: a city like Rome should offer a few walks to choose
    from, inside the one page, never as pages of their own. So each cluster
    that holds enough trees gets its own route, and a city with one cluster
    behaves exactly as it always did.

    Returns walks sorted by tree count, longest first, each with its member
    indexes in walking order. Returns [] when no cluster clears the bar, and
    the page then has no route bar at all, which stays the honest answer."""
    points = [(m["lat"], m["lng"]) for m in markers]
    walks, combined = [], []
    for members in _walk_clusters(points):
        if len(members) < WALK_MIN_TREES:
            continue
        sub = [points[i] for i in members]
        route = plan_walking_route(sub, budget_km)
        if not route:
            continue
        order = [members[i] for i in route["order"]]
        kept = 0
        for leg in _split_route(order, points):
            if any(_too_similar(leg, w["order"]) for w in walks):
                continue
            kept += 1
            km = round(_leg_km(leg, points), 1)
            walks.append({
                "order": leg,
                "count": len(leg),
                "km": km,
                "minutes": int(round(km / WALKING_KMH * 60)),
                "name": _walk_name(leg, markers),
            })
        # A split cluster's halves are disjoint (Hidde, 2026-08-08: welded
        # lines read as one walk on the overview). The full route survives as
        # an explicit choice when it is still a doable afternoon, so the
        # visitor with the whole day loses nothing.
        if kept > 1:
            km_full = round(_leg_km(order, points), 1)
            if km_full <= COMBINED_MAX_KM:
                combined.append({
                    "order": order,
                    "count": len(order),
                    "km": km_full,
                    "minutes": int(round(km_full / WALKING_KMH * 60)),
                    "name": "Both walks" if kept == 2 else f"All {kept} walks",
                    "combined": True,
                })
    # Photographed trees first, then size. Sorting on size alone put Barcelona's
    # worst walk in front: the ten Pedralbes trees are its tightest cluster and
    # also its newest, imported from the municipal register two days before this
    # was written, so not one of them had a photograph while a Montjuic walk with
    # four sat hidden behind a chip. Rome had the same shape. A visitor decides
    # from the pictures whether an afternoon is worth it, so the walk that leads
    # is the one they can see, and every other walk is still one tap away.
    for w in walks:
        w["shots"] = sum(1 for i in w["order"] if markers[i].get("shot"))
    walks.sort(key=lambda w: (-w["shots"], -w["count"], w["km"]))
    # Two walks under one name tells a visitor nothing and quietly implies the
    # second is somewhere else. Vienna produced two "Innere Stadt" walks.
    dupes = {w["name"] for w in walks
             if w["name"] and sum(1 for x in walks if x["name"] == w["name"]) > 1}
    for w in walks:
        if w["name"] in dupes:
            w["name"] = ""
    # The combined option rides last, after its parts, never as the lead walk.
    for w in combined:
        w["shots"] = sum(1 for i in w["order"] if markers[i].get("shot"))
    walks.extend(combined)
    return walks


def load_walk_routes():
    """Real pedestrian geometry per walk, cached by scripts/route_walks.py.

    Missing file, missing key or a rejected route all fall back to the straight
    line, which is why this never blocks a build: the routes are an enrichment,
    not a dependency."""
    f = DATA / "walk-routes.json"
    if not f.exists():
        return {}
    return json.loads(f.read_text()).get("routes", {})


WALK_ROUTES = None


def walk_route_for(city_slug, tree_ids):
    global WALK_ROUTES
    if WALK_ROUTES is None:
        WALK_ROUTES = load_walk_routes()
    r = WALK_ROUTES.get(city_slug + ":" + ",".join(tree_ids))
    if not r or r.get("rejected") or not r.get("shape"):
        return None
    return r


def human_duration(minutes):
    hours, mins = divmod(int(minutes), 60)
    if hours and mins:
        return f"{hours}h {mins}m"
    if hours:
        return "1 hour" if hours == 1 else f"{hours} hours"
    return f"{mins} min"


def maps_route_url(ordered_points):
    """Hand the actual turn by turn navigation to the visitor's own maps app.

    Deliberately not a routing API: that would be a new third party dependency
    (hard rule 5) and a running cost, to reproduce something every phone
    already does well. Google's URL scheme takes at most 9 waypoints, so the
    middle is trimmed if a city ever carries more than eleven trees.
    """
    if len(ordered_points) < 2:
        return ""
    pts = ["{:.6f},{:.6f}".format(lat, lng) for lat, lng in ordered_points]
    origin, destination, middle = pts[0], pts[-1], pts[1:-1]
    if len(middle) > 9:
        step = len(middle) / 9.0
        middle = [middle[int(i * step)] for i in range(9)]
    url = ("https://www.google.com/maps/dir/?api=1&travelmode=walking"
           f"&origin={origin}&destination={destination}")
    if middle:
        url += "&waypoints=" + "|".join(middle)
    return url


def city_map_script(markers, center, route=None, other_cities=None, walks=None):
    data = json.dumps(markers)
    route_coords = json.dumps(
        [[markers[i]["lng"], markers[i]["lat"]] for i in route["order"]]
        if route and len(markers) > 1 else []
    )
    # Every walk's line and metadata, so switching between them is a local
    # redraw rather than a page load or a fetch.
    walks_json = json.dumps([{
        # the real pavement line when we have one, else the honest straight hint
        "coords": w.get("shape") or [[markers[i]["lng"], markers[i]["lat"]] for i in w["order"]],
        "members": w["order"],
        "url": w.get("url", ""),
        "label": w.get("label", ""),
        "name": w.get("name", ""),
        "meta": f"about {w['km']} km, {w.get('duration', '')} on foot",
        "combined": bool(w.get("combined")),
    } for w in (walks or [])])
    # One continuous world (Hidde, 2026-07-31): zoom out far enough on any
    # city map and the OTHER cities pop in as the same green dots /explore
    # uses, each a click away. Layer capped at maxzoom 9 so a city view
    # stays clean.
    other_cities_json = json.dumps({
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [c["lng"], c["lat"]]},
            "properties": {"slug": c["slug"], "city": c["city"], "n": c["n"]},
        } for c in (other_cities or [])],
    })
    _ranked = sorted(other_cities or [], key=lambda c: (c.get("rank", 99), -c["n"]))
    chooser_cities_json = json.dumps(
        [{"url": c["slug"], "city": c["city"], "country": c["country"],
          "n": c["n"], "ph": c.get("ph"), "lat": c["lat"], "lng": c["lng"]}
         for c in _ranked])
    return f"""
<script src="{MAPLIBRE_JS}"></script>
<script>
var markers = {data};
var map = new maplibregl.Map({{
  container: 'map',
  style: '{MAP_STYLE}',
  center: [{center[1]}, {center[0]}],
  zoom: 10.5,
  scrollZoom: true,
  attributionControl: {{ compact: true }}
}});
map.addControl(new maplibregl.NavigationControl());
map.addControl(new maplibregl.FullscreenControl());
map.on('load', function() {{ map.resize(); }});
new ResizeObserver(function() {{ map.resize(); }}).observe(document.getElementById('map'));
var OTHER_CITIES = {other_cities_json};
if (OTHER_CITIES.features.length) {{
  map.on('load', function() {{
    if (map.getSource('othercities')) {{ return; }}
    map.addSource('othercities', {{type: 'geojson', data: OTHER_CITIES}});
    map.addLayer({{id: 'othercity', type: 'circle', source: 'othercities', maxzoom: 9,
      paint: {{'circle-color': '#4A6B2A', 'circle-opacity': 0.92, 'circle-radius': 13,
              'circle-stroke-width': 2, 'circle-stroke-color': '#F6F2E9'}}}});
    map.addLayer({{id: 'othercity-n', type: 'symbol', source: 'othercities', maxzoom: 9,
      layout: {{'text-field': ['get', 'n'], 'text-font': ['Noto Sans Regular'], 'text-size': 11,
               'text-allow-overlap': true}},
      paint: {{'text-color': '#F6F2E9'}}}});
    map.on('click', 'othercity', function(e) {{
      window.location.href = '/' + e.features[0].properties.slug;
    }});
    map.on('mouseenter', 'othercity', function() {{ map.getCanvas().style.cursor = 'pointer'; }});
    map.on('mouseleave', 'othercity', function() {{ map.getCanvas().style.cursor = ''; }});
  }});
}}
// One map (Hidde, 2026-07-31, the Groningen articulation): zoom out on a
// city page and the panel itself becomes the city chooser, same cards as
// /explore; zoom back in and the trees return. The static page Google sees
// never changes; this is presentation only.
var CHOOSER_CITIES = {chooser_cities_json};
var cityPanel = document.querySelector('.panel');
var chooserBox = null;
var chooserOn = false;
var homeZoom = null;
function ensureChooserBox() {{
  if (chooserBox) {{ return chooserBox; }}
  chooserBox = document.createElement('div');
  chooserBox.className = 'panel-chooser';
  chooserBox.style.display = 'none';
  cityPanel.appendChild(chooserBox);
  return chooserBox;
}}
function chooserCard(c) {{
  var ph = c.ph ? '<span class="exc-ph"><img src="' + c.ph + '" alt="" loading="lazy"></span>' : '<span class="exc-ph exc-noph"></span>';
  return '<a class="exc-card" href="/' + c.url + '">' + ph +
         '<span class="exc-body"><b>' + c.city + '</b>' +
         '<span>' + c.n + ' trees &middot; ' + c.country + '</span></span></a>';
}}
function updatePanelMode() {{
  if (!cityPanel || !CHOOSER_CITIES.length) {{ return; }}
  var z = map.getZoom();
  // Thresholds sit relative to the city's own opening zoom: on a phone a
  // sprawling city fits at z~9.4, and a fixed 9.5 line put fresh page loads
  // straight into chooser mode (the Paris bug, 2026-08-01). The chooser is
  // for people who deliberately zoomed OUT of the opening view.
  var onAt = homeZoom === null ? 9.5 : Math.min(9.5, homeZoom - 1.2);
  if (!chooserOn && z <= onAt) {{ chooserOn = true; }}
  else if (chooserOn && z >= onAt + 1) {{ chooserOn = false; }}
  var box = ensureChooserBox();
  for (var i = 0; i < cityPanel.children.length; i++) {{
    var el = cityPanel.children[i];
    if (el !== box) {{ el.style.display = chooserOn ? 'none' : ''; }}
  }}
  if (chooserOn) {{
    var b = map.getBounds();
    var inview = CHOOSER_CITIES.filter(function(c) {{ return b.contains([c.lng, c.lat]); }});
    box.innerHTML = '<div class="exc-cityhead"><h2>Cities in view</h2></div>' +
      (inview.length ? inview.slice(0, 10).map(chooserCard).join('')
                     : '<p class="exc-empty">No other mapped cities in view yet. Keep zooming out.</p>');
    box.style.display = '';
  }} else {{
    box.style.display = 'none';
  }}
}}
if (markers.length > 1) {{
  var _b = new maplibregl.LngLatBounds();
  markers.forEach(function(m) {{ _b.extend([m.lng, m.lat]); }});
  var _el = document.getElementById('map');
  var _pad = Math.max(30, Math.min(90, Math.floor(Math.min(_el.clientWidth, _el.clientHeight) * 0.16)));
  map.fitBounds(_b, {{ padding: _pad, maxZoom: 14.5, duration: 0 }});
  homeZoom = map.getZoom();
}}
// Registered AFTER the opening fitBounds on purpose: its zero-duration jump
// fires moveend synchronously, and a listener armed before homeZoom exists
// re-creates the Paris bug on any wide city (Cork proved it).
map.on('moveend', updatePanelMode);

var pins = [];
var activeIdx = -1;

function setActive(idx, fly, scroll) {{
  if (activeIdx >= 0) {{
    pins[activeIdx].classList.remove('active');
    document.getElementById('tree-' + (activeIdx + 1)).classList.remove('active');
  }}
  activeIdx = idx;
  var m = markers[idx];
  pins[idx].classList.add('active');
  var card = document.getElementById('tree-' + (idx + 1));
  card.classList.add('active');
  if (scroll) {{ card.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }}); }}
  if (fly) {{ map.flyTo({{ center: [m.lng, m.lat], zoom: 14.5, duration: 1200 }}); }}
}}

var bounds = new maplibregl.LngLatBounds();
markers.forEach(function(m, idx) {{
  var el = document.createElement('div');
  el.className = 'pin-tree';
  el.title = m.name;
  el.innerHTML = '<svg viewBox="0 0 40 40" fill="currentColor" aria-hidden="true">' + m.icon + '</svg>'
               + '<span class="pin-rank">' + m.label + '</span>';
  el.addEventListener('click', function(e) {{
    e.stopPropagation();
    setActive(idx, true, true);
  }});
  new maplibregl.Marker({{ element: el }}).setLngLat([m.lng, m.lat]).addTo(map);
  pins.push(el);
  bounds.extend([m.lng, m.lat]);
}});
if (markers.length > 1) {{ map.fitBounds(bounds, {{ padding: 70, maxZoom: 13 }}); }}

document.querySelectorAll('.tree-card').forEach(function(card, idx) {{
  card.addEventListener('click', function(e) {{
    if (e.target.closest('a')) {{ return; }}
    setActive(idx, true, false);
  }});
}});

// The walking line. Deliberately drawn as a dashed hint, not a solid path:
// it is the order to walk them in, not the streets to take. Real turn by turn
// is handed to the visitor's own maps app by the button underneath.
// Hung on the style rather than on 'load', which waits for every tile. On a
// slow connection in a park, 'load' can be a long time coming or never arrive,
// and the walking line is exactly what that visitor needs first.
var routeCoords = {route_coords};
function addWalkLayer() {{
  if (routeCoords.length < 2 || map.getSource('walk')) {{ return; }}
  map.addSource('walk', {{
    type: 'geojson',
    data: {{ type: 'Feature', geometry: {{ type: 'LineString', coordinates: routeCoords }} }}
  }});
  map.addLayer({{
    id: 'walk-casing', type: 'line', source: 'walk',
    layout: {{ 'line-cap': 'round', 'line-join': 'round' }},
    paint: {{ 'line-color': '#fff', 'line-width': 8, 'line-opacity': 0.85 }}
  }});
  map.addLayer({{
    id: 'walk', type: 'line', source: 'walk',
    layout: {{ 'line-cap': 'round', 'line-join': 'round' }},
    paint: {{ 'line-color': '#3D5C1E', 'line-width': 4.5, 'line-opacity': 0.95,
              'line-dasharray': [1.4, 1.1] }}
  }});
}}
if (map.isStyleLoaded()) {{ addWalkLayer(); }} else {{ map.on('styledata', addWalkLayer); }}

// Every walk drawn faintly at once, and each one clickable, the way a maps app
// offers you two or three greyed routes and lets you pick (Hidde, 2026-08-08).
// Before this the city view showed one line and the others were invisible until
// you found the chips, so a city with four walks looked like a city with one.
// The wide transparent layer underneath is the touch target: a 2.5px dashed
// line is not something anybody hits with a thumb.
function addAllWalksLayer() {{
  if (WALKS.length < 2 || map.getSource('walks-all')) {{ return; }}
  map.addSource('walks-all', {{
    type: 'geojson',
    // The combined option is the sum of lines already on the map: drawing it
    // grey as well would double every segment, so only the real walks show.
    data: {{ type: 'FeatureCollection', features: WALKS.map(function(w, i) {{
      return {{ type: 'Feature', properties: {{ idx: i }},
               geometry: {{ type: 'LineString', coordinates: w.coords }} }};
    }}).filter(function(f) {{ return !WALKS[f.properties.idx].combined; }}) }}
  }});
  map.addLayer({{
    id: 'walks-all-hit', type: 'line', source: 'walks-all',
    layout: {{ 'line-cap': 'round', 'line-join': 'round' }},
    paint: {{ 'line-color': '#000', 'line-width': 16, 'line-opacity': 0.001 }}
  }});
  map.addLayer({{
    id: 'walks-all-casing', type: 'line', source: 'walks-all',
    layout: {{ 'line-cap': 'round', 'line-join': 'round' }},
    paint: {{ 'line-color': '#fff', 'line-width': 7, 'line-opacity': 0.7 }}
  }});
  map.addLayer({{
    id: 'walks-all', type: 'line', source: 'walks-all',
    layout: {{ 'line-cap': 'round', 'line-join': 'round' }},
    paint: {{ 'line-color': '#4b5563', 'line-width': 3.5, 'line-opacity': 0.8,
              'line-dasharray': [1.4, 1.1] }}
  }});
  map.on('click', 'walks-all-hit', function(e) {{
    if (e.features && e.features.length) {{ selectWalk(e.features[0].properties.idx); }}
  }});
  map.on('mouseenter', 'walks-all-hit', function() {{ map.getCanvas().style.cursor = 'pointer'; }});
  map.on('mouseleave', 'walks-all-hit', function() {{ map.getCanvas().style.cursor = ''; }});
}}
function setAllWalksFilter(activeIdx) {{
  // Hide the grey copy of whatever is selected, so the chosen walk shows once
  // in green rather than twice in two colours.
  if (!map.getLayer('walks-all')) {{ return; }}
  // Selecting the combined option hides every grey copy: its green line
  // covers all of them, and grey under green reads as a third walk.
  var f = activeIdx < 0 ? null
        : (WALKS[activeIdx] && WALKS[activeIdx].combined) ? ['==', ['get', 'idx'], -1]
        : ['!=', ['get', 'idx'], activeIdx];
  map.setFilter('walks-all', f);
  map.setFilter('walks-all-hit', f);
  if (map.getLayer('walks-all-casing')) {{ map.setFilter('walks-all-casing', f); }}
}}
if (map.isStyleLoaded()) {{ addAllWalksLayer(); }} else {{ map.on('styledata', addAllWalksLayer); }}

// Several walks in one city, chosen inside this page (Hidde, 2026-08-06:
// never a page per walk). Picking one redraws the line, retargets the
// directions button and dims the pins that are not on it. Nothing is removed
// from the document: every tree stays in the HTML for a reader and a crawler,
// only the emphasis moves.
var WALKS = {walks_json};
var wantCoords = [];
function drawWalk(coords) {{
  // Guarded because map.getSource throws outright while the style is still
  // loading, and the first draw runs the moment the page does.
  //
  // The deferred branch redraws wantCoords rather than the coords captured
  // when it was queued. Without that, the on-load hint line wins a race it
  // should lose: it waits for styledata, the visitor picks a different walk
  // in the meantime, and the late callback paints the first walk's line back
  // over the chosen one. The dimming and the labels updated, the line did not.
  wantCoords = coords;
  // Updating an existing source is always safe, so try that FIRST and only
  // fall back to waiting on the style. The previous order gated everything
  // behind map.isStyleLoaded(), which stays false whenever the tile style has
  // not finished (offline, slow connection, a blocked tile host), so switching
  // walks silently failed to move the line while the dimming and the labels
  // updated normally. getSource itself throws before the style exists, hence
  // the try.
  var src = null;
  try {{ src = map.getSource('walk'); }} catch (e) {{ src = null; }}
  if (src) {{
    src.setData({{ type: 'Feature', geometry: {{ type: 'LineString', coordinates: coords }} }});
    return;
  }}
  if (!map.isStyleLoaded()) {{
    map.once('styledata', function() {{ drawWalk(wantCoords); }});
    return;
  }}
  addWalkLayer();
}}
function selectWalk(idx) {{
  var w = WALKS[idx];
  if (!w) {{ return; }}
  activeWalk = idx;
  setAllWalksFilter(idx);
  routeCoords = w.coords;
  drawWalk(w.coords);
  var go = document.getElementById('route-go');
  if (go) {{ go.href = w.url; }}
  var lab = document.getElementById('route-label');
  if (lab) {{ lab.textContent = w.label; }}
  var meta = document.getElementById('route-meta');
  if (meta) {{ meta.textContent = w.meta; }}
  var nm = document.querySelector('.route-name');
  if (nm) {{ nm.textContent = w.name; nm.hidden = !w.name; }}
  var on = {{}};
  w.members.forEach(function(i) {{ on[i] = true; }});
  pins.forEach(function(el, i) {{ el.classList.toggle('pin-off', !on[i]); }});
  document.querySelectorAll('.tree-card').forEach(function(card, i) {{
    card.classList.toggle('card-off', !on[i]);
  }});
  document.querySelectorAll('.walk-pick').forEach(function(b, i) {{
    b.classList.toggle('is-on', i === idx);
    b.setAttribute('aria-pressed', i === idx ? 'true' : 'false');
  }});
  if (w.coords.length > 1) {{
    var bb = new maplibregl.LngLatBounds();
    w.coords.forEach(function(c) {{ bb.extend(c); }});
    map.fitBounds(bb, {{ padding: 70, maxZoom: 15 }});
  }}
}}
// The city first, a walk only when asked. Hidde, 2026-08-08: "when opening a
// city it focusses on 1 walk instead of the entire city". Selecting a walk on
// load dimmed most of the map and zoomed into one corner before the visitor
// had chosen anything, which hid the city they came to see. Now the page opens
// on every tree, and picking a walk is a deliberate act the visitor can undo.
var activeWalk = -1;
function showWholeCity() {{
  activeWalk = -1;
  setAllWalksFilter(-1);
  drawWalk([]);
  pins.forEach(function(el) {{ el.classList.remove('pin-off'); }});
  document.querySelectorAll('.tree-card').forEach(function(card) {{
    card.classList.remove('card-off');
  }});
  document.querySelectorAll('.walk-pick').forEach(function(b) {{
    b.classList.remove('is-on');
    b.setAttribute('aria-pressed', 'false');
  }});
  // The bar goes back to the lead walk too, or deselecting leaves it naming a
  // walk no chip shows as chosen ("Both walks" with nothing selected).
  var w0 = WALKS[0];
  if (w0) {{
    routeCoords = w0.coords;
    var go = document.getElementById('route-go');
    if (go) {{ go.href = w0.url; }}
    var lab = document.getElementById('route-label');
    if (lab) {{ lab.textContent = w0.label; }}
    var meta = document.getElementById('route-meta');
    if (meta) {{ meta.textContent = w0.meta; }}
    var nm = document.querySelector('.route-name');
    if (nm) {{ nm.textContent = w0.name; nm.hidden = !w0.name; }}
  }}
  if (markers.length > 1) {{ map.fitBounds(bounds, {{ padding: 70, maxZoom: 13 }}); }}
}}
document.querySelectorAll('.walk-pick').forEach(function(btn) {{
  btn.addEventListener('click', function() {{
    var idx = parseInt(btn.getAttribute('data-walk'), 10);
    if (idx === activeWalk) {{ showWholeCity(); }} else {{ selectWalk(idx); }}
  }});
}});
// One walk: draw it, since there is nothing to choose between. Several: leave
// the green line empty and let the grey alternatives speak, or the lead walk
// would appear twice, once grey and once green, while no chip is selected.
if (WALKS.length === 1 && WALKS[0].coords.length > 1) {{
  drawWalk(WALKS[0].coords);
}} else if (WALKS.length > 1) {{
  drawWalk([]);
}}

// The passport. Which trees you have stood in front of, kept in LocalStorage on
// your own phone. No account, no server, nothing leaves the device: that is not
// a limitation to work around later, it is why this can exist at all without
// holding anyone's personal data. Collected across every city, so a trip to
// Tokyo adds to the same tally as a walk in Amsterdam.
var SEEN_KEY = 'ancienttrees_seen';

function readSeen() {{
  try {{ return JSON.parse(localStorage.getItem(SEEN_KEY)) || []; }}
  catch (e) {{ return []; }}
}}
function writeSeen(list) {{
  try {{ localStorage.setItem(SEEN_KEY, JSON.stringify(list)); }} catch (e) {{}}
}}

function paintPassport() {{
  var seen = readSeen();
  var here = 0;
  markers.forEach(function(m, idx) {{
    var got = seen.indexOf(m.id) !== -1;
    if (got) {{ here++; }}
    pins[idx].classList.toggle('seen', got);
  }});
  document.querySelectorAll('.seen-btn').forEach(function(btn) {{
    var got = seen.indexOf(btn.dataset.tree) !== -1;
    btn.setAttribute('aria-pressed', got ? 'true' : 'false');
    btn.querySelector('.seen-text').textContent = got ? 'Visited' : 'Check in at this tree';
  }});
  var box = document.getElementById('passport');
  if (box) {{
    document.getElementById('passport-count').textContent = here;
    box.hidden = here === 0;
    box.classList.toggle('complete', here === markers.length);
    var total = document.getElementById('passport-total');
    if (seen.length > here) {{
      total.textContent = seen.length + ' trees in total, across every city.';
    }} else if (here === markers.length) {{
      total.textContent = 'Every tree here. Go find another city.';
    }} else {{
      total.textContent = '';
    }}
  }}
}}

// You have to actually be there. A tick box anyone can click from the sofa
// collects nothing and, worse, does nothing for the one thing this site is for,
// which is getting a person to stand in front of a tree. So a check in asks the
// browser where you are and refuses politely if you are not close.
// The radius is generous on purpose: GPS in a street canyon is good to tens of
// metres, and a pin we have marked approximate gets 200m rather than 75m,
// because refusing someone who is genuinely standing at the tree would be our
// mistake charged to them.
function metresBetween(lat1, lng1, lat2, lng2) {{
  var R = 6371000, p = Math.PI / 180;
  var a = Math.sin((lat2 - lat1) * p / 2) * Math.sin((lat2 - lat1) * p / 2)
        + Math.cos(lat1 * p) * Math.cos(lat2 * p)
        * Math.sin((lng2 - lng1) * p / 2) * Math.sin((lng2 - lng1) * p / 2);
  return 2 * R * Math.asin(Math.sqrt(a));
}}

function flash(btn, msg, ms) {{
  var t = btn.querySelector('.seen-text'), was = t.textContent;
  t.textContent = msg;
  setTimeout(function() {{ if (t.textContent === msg) {{ t.textContent = was; }} }}, ms || 4000);
}}

document.querySelectorAll('.seen-btn').forEach(function(btn) {{
  btn.addEventListener('click', function(e) {{
    e.stopPropagation();
    var id = btn.dataset.tree;
    var seen = readSeen();

    // Undoing never needs proof: if you ticked it by mistake, that is yours to fix.
    if (seen.indexOf(id) !== -1) {{
      seen.splice(seen.indexOf(id), 1);
      writeSeen(seen);
      paintPassport();
      return;
    }}

    if (!navigator.geolocation) {{
      flash(btn, 'This browser cannot check where you are');
      return;
    }}
    flash(btn, 'Checking where you are...', 20000);
    navigator.geolocation.getCurrentPosition(function(pos) {{
      var away = metresBetween(pos.coords.latitude, pos.coords.longitude,
                               parseFloat(btn.dataset.lat), parseFloat(btn.dataset.lng));
      if (away <= parseFloat(btn.dataset.radius)) {{
        var list = readSeen();
        if (list.indexOf(id) === -1) {{ list.push(id); }}
        writeSeen(list);
        paintPassport();
      }} else {{
        var far = away > 2000 ? Math.round(away / 1000) + ' km' : Math.round(away) + ' m';
        flash(btn, 'Still ' + far + ' away. Check in at the tree.', 6000);
      }}
    }}, function(err) {{
      flash(btn, err.code === 1 ? 'Location needed to check in' : 'Could not find you. Try again.', 6000);
    }}, {{ enableHighAccuracy: true, maximumAge: 30000, timeout: 15000 }});
  }});
}});

// Browser storage is not a safe place to keep something someone cares about.
// It goes when they clear their data, it does not exist in private browsing, it
// never reaches their laptop, and Safari on iOS deletes it after seven days
// without a visit, which is exactly a three week trip. So the passport can be
// turned into a plain link: bookmark it, mail it to yourself, open it on
// another phone. No account, nothing stored anywhere but in the link itself.
if (location.hash.indexOf('#trees=') === 0) {{
  var incoming = decodeURIComponent(location.hash.slice(7)).split(',').filter(Boolean);
  if (incoming.length) {{
    var merged = readSeen();
    incoming.forEach(function(id) {{ if (merged.indexOf(id) === -1) {{ merged.push(id); }} }});
    writeSeen(merged);
    history.replaceState(null, '', location.pathname + location.search);
  }}
}}

var saveBtn = document.getElementById('passport-save');
if (saveBtn) {{
  saveBtn.addEventListener('click', function() {{
    var link = location.origin + location.pathname + '#trees=' + encodeURIComponent(readSeen().join(','));
    function done(msg) {{
      saveBtn.textContent = msg;
      setTimeout(function() {{ saveBtn.textContent = 'Save or move to another device'; }}, 4000);
    }}
    if (navigator.share) {{
      navigator.share({{ title: 'My trees', url: link }}).then(function() {{ done('Saved'); }},
                                                              function() {{}});
    }} else if (navigator.clipboard) {{
      navigator.clipboard.writeText(link).then(function() {{ done('Link copied. Bookmark it or mail it to yourself.'); }},
                                               function() {{ window.prompt('Copy this link:', link); }});
    }} else {{
      window.prompt('Copy this link:', link);
    }}
  }});
}}

paintPassport();

// "Where am I": browser geolocation only, nothing stored and nothing sent
// anywhere. The dot lives in the page and dies with it.
var gpsBtn = document.getElementById('gps-btn');
var meMarker = null, watchId = null;
if (gpsBtn && navigator.geolocation) {{
  gpsBtn.addEventListener('click', function() {{
    if (watchId !== null) {{
      navigator.geolocation.clearWatch(watchId);
      watchId = null;
      if (meMarker) {{ meMarker.remove(); meMarker = null; }}
      gpsBtn.setAttribute('aria-pressed', 'false');
      gpsBtn.textContent = 'Where am I';
      return;
    }}
    gpsBtn.textContent = 'Finding you...';
    watchId = navigator.geolocation.watchPosition(function(pos) {{
      var here = [pos.coords.longitude, pos.coords.latitude];
      if (!meMarker) {{
        var dot = document.createElement('div');
        dot.className = 'pin-me';
        meMarker = new maplibregl.Marker({{ element: dot }}).setLngLat(here).addTo(map);
        map.flyTo({{ center: here, zoom: 15, duration: 1000 }});
      }} else {{
        meMarker.setLngLat(here);
      }}
      gpsBtn.setAttribute('aria-pressed', 'true');
      gpsBtn.textContent = 'Hide me';
    }}, function(err) {{
      gpsBtn.textContent = err.code === 1 ? 'Location blocked' : 'Location unavailable';
      watchId = null;
      setTimeout(function() {{ gpsBtn.textContent = 'Where am I'; }}, 3000);
    }}, {{ enableHighAccuracy: true, maximumAge: 10000, timeout: 10000 }});
  }});
}} else if (gpsBtn) {{
  gpsBtn.hidden = true;
}}
</script>
"""


def home_hero_script():
    """The photo-hero homepage script. The map lives at /explore; location is
    asked THERE, in map context, never from the homepage (Hidde, 2026-07-29:
    a location prompt from a hero link "slaat nergens op"). Search is the
    shared SEARCH_WIDGET_JS component, identical to /explore."""
    return """
<script>
var moreBtn = document.getElementById('more-cities-btn');
if (moreBtn) {
  moreBtn.addEventListener('click', function() {
    document.getElementById('more-cities').hidden = false;
    moreBtn.remove();
  });
}
</script>
"""


# The one search interaction (Hidde, 2026-08-01: "ik wil dezelfde interactie
# op home en hier en ik wil dat je die gelijk houdt"). The convention every
# search-led product uses (AllTrails, Google Maps, Airbnb): suggestions appear
# UNDER the field while you type, and tapping one takes you straight there.
# The native datalist is gone on purpose: iOS renders it as a half-broken
# QuickType strip, which is exactly what felt unnatural. One component, one
# shared /search-index.json, so home and explore cannot drift apart.
def search_form(ctx, input_id, form_class, with_button=False):
    ico = ('<button type="submit" class="search-ico" aria-label="Search">'
           '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">'
           '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg></button>'
           if with_button else
           '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
           '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg>')
    return (f'<form class="{form_class} at-search" data-ctx="{ctx}" role="search" autocomplete="off">'
            f'{ico}'
            f'<input type="search" id="{input_id}" placeholder="Search a city or tree"'
            f' aria-label="Search a city or tree" autocapitalize="off" autocorrect="off" spellcheck="false">'
            f'<div class="ats-drop" hidden></div></form>')


SEARCH_WIDGET_JS = """
<script>
(function() {
  // Every .at-search on the page gets wired, so a second placement (a header
  // bar, the AllTrails pattern) needs no new script.
  Array.prototype.forEach.call(document.querySelectorAll('form.at-search'), setup);
  function setup(form) {
  var input = form.querySelector('input');
  var drop = form.querySelector('.ats-drop');
  var ctx = form.getAttribute('data-ctx');
  var IDX = null, loading = false, rows = [], active = -1;
  function norm(s) {
    s = s.toLowerCase();
    try { s = s.normalize('NFD').replace(/[\\u0300-\\u036f]/g, ''); } catch (e) {}
    return s;
  }
  function escT(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
  function load() {
    if (IDX || loading) return;
    loading = true;
    fetch('/search-index.json').then(function(r) { return r.json(); })
      .then(function(j) { IDX = j; if (document.activeElement === input) show(); })
      .catch(function() { loading = false; });
  }
  function results(q) {
    // A hierarchy rather than one flat relevance list, which is what every
    // search-led map product does (Google Maps, AllTrails, Airbnb): places
    // first and always, then species, and an individual tree only when the
    // query is specific enough to be asking for one.
    var out = [];
    var places = [], species = [], trees = [];
    IDX.k.forEach(function(k) {
      var i = norm(k.country).indexOf(q);
      if (i === 0) places.unshift({kind: 'country', it: k});
      else if (i > 0) places.push({kind: 'country', it: k});
    });
    IDX.c.forEach(function(c) {
      var i = norm(c.city).indexOf(q);
      if (i === 0) places.push({kind: 'city', it: c});
      else if (i > 0 || norm(c.country).indexOf(q) === 0) places.push({kind: 'city', it: c});
    });
    IDX.s.forEach(function(s) {
      if (norm(s.n).indexOf(q) === 0) species.push({kind: 'species', it: s});
    });
    // Trees only earn a slot once the query is specific: at least four
    // characters, matching the start of a word in the name, and never
    // crowding out a place that matched.
    if (q.length >= 4) {
      IDX.t.forEach(function(t) {
        var n = norm(t.n);
        if (n.indexOf(q) === 0 || n.indexOf(' ' + q) !== -1) trees.push({kind: 'tree', it: t});
      });
    }
    out = places.slice(0, 6).concat(species.slice(0, 2));
    var room = 8 - out.length;
    if (room > 0) out = out.concat(trees.slice(0, Math.min(room, places.length ? 2 : 5)));
    return out;
  }

  function hide() { drop.hidden = true; active = -1; }
  function show() {
    var q = norm(input.value.trim());
    if (!q) { hide(); return; }
    load();
    if (!IDX) return;
    var res = results(q);
    active = -1;
    if (!res.length) {
      drop.innerHTML = '<div class="ats-empty">Not mapped yet. <a href="/contribute">Be the first to map it</a>.</div>';
    } else {
      var lastKind = null;
      drop.innerHTML = res.map(function(r) {
        var name, sec, head = '';
        if (r.kind === 'country') {
          name = r.it.country;
          sec = r.it.cities + ' cities &middot; ' + r.it.n + ' trees';
        } else if (r.kind === 'city') {
          name = r.it.city;
          sec = r.it.n + ' trees &middot; ' + escT(r.it.country);
        } else if (r.kind === 'species') {
          name = r.it.n;
          sec = r.it.count + ' mapped &middot; every one on the site';
        } else {
          name = r.it.n;
          sec = escT(r.it.c);
        }
        var label = (r.kind === 'country' || r.kind === 'city') ? 'Places'
                  : r.kind === 'species' ? 'Species' : 'Trees';
        if (label !== lastKind) { head = '<div class="ats-head">' + label + '</div>'; lastKind = label; }
        return head + '<a class="ats-row" href="/' + r.it.u + '"><b>' + escT(name) + '</b><span>' + sec + '</span></a>';
      }).join('');
    }
    drop.hidden = false;
    rows = Array.prototype.slice.call(drop.querySelectorAll('.ats-row'));
  }
  function go(row) {
    at.track('search-' + ctx, norm(input.value.trim()).slice(0, 60));
    window.location.href = row.getAttribute('href');
  }
  function mark(i) {
    rows.forEach(function(r) { r.classList.remove('active'); });
    if (i >= 0 && rows[i]) { rows[i].classList.add('active'); rows[i].scrollIntoView({block: 'nearest'}); }
    active = i;
  }
  input.addEventListener('input', show);
  input.addEventListener('focus', function() { load(); show(); });
  input.addEventListener('blur', function() { setTimeout(hide, 150); });
  input.addEventListener('keydown', function(e) {
    if (drop.hidden || !rows.length) return;
    if (e.key === 'ArrowDown') { e.preventDefault(); mark((active + 1) % rows.length); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); mark((active - 1 + rows.length) % rows.length); }
    else if (e.key === 'Escape') { hide(); }
  });
  drop.addEventListener('mousedown', function(e) {
    var a = e.target.closest ? e.target.closest('.ats-row') : null;
    if (a) { e.preventDefault(); go(a); }
  });
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    if (rows.length) { go(rows[active >= 0 ? active : 0]); }
  });
  }
})();
</script>
"""


def render_page(title, description, canonical, body, head_extra="", scripts="",
                rootpath="", footer=True, og_type="article"):
    if len(title) > TITLE_MAX:
        ERRORS.append(f"{canonical}: title exceeds {TITLE_MAX} chars ({len(title)}): {title!r}")
    if len(description) > DESC_MAX:
        ERRORS.append(f"{canonical}: description exceeds {DESC_MAX} chars ({len(description)})")
    footer_html = FOOTER.replace("%%ROOTPATH%%", rootpath) if footer else ""
    # Guard: script text passed without <script> tags renders as visible page
    # text (shipped once, on every tree page). Catch it at build time.
    if scripts:
        outside = re.sub(r"<script\b.*?</script>", "", scripts, flags=re.S)
        if re.search(r"\(function\(\)|=>|document\.|localStorage", outside):
            ERRORS.append(f"{canonical}: bare JavaScript outside <script> tags would render as text")
    login_link = ('<a href="%%ROOTPATH%%account" class="bar-login only-desktop">Log in</a>'
                  if AUTH_ENABLED else "")
    login_menu = ('<a href="%%ROOTPATH%%account" class="only-mobile"><span class="mi">'
                  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
                  'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/>'
                  '<path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg></span>Log in</a>'
                  if AUTH_ENABLED else "")
    page_html = (
        PAGE_SHELL
        .replace("SB_URL", SUPABASE_URL)
        .replace("SB_KEY", SUPABASE_KEY)
        .replace("%%LOGIN_MENU%%", login_menu)
        .replace("%%LOGIN%%", login_link)
        .replace("%%TITLE%%", esc(title))
        .replace("%%DESCRIPTION%%", esc(description))
        .replace("%%CANONICAL%%", canonical)
        .replace("%%OGTYPE%%", og_type)
        .replace("%%ROOTPATH%%", rootpath)
        .replace("%%HEAD_EXTRA%%", head_extra)
        .replace("%%BODY%%", body)
        .replace("%%FOOTER%%", footer_html)
        .replace("%%SCRIPTS%%", scripts)
        .replace("%%ANALYTICS%%",
                 ANALYTICS_SNIPPET.format(token=ANALYTICS_TOKEN) if ANALYTICS_TOKEN else "")
        .replace("%%YEAR%%", str(date.today().year))
    )
    return page_html


def check_links(page, count, minimum):
    if count < minimum:
        ERRORS.append(f"{page}: {count} internal links, contract minimum is {minimum}")


def tree_is_renderable(tree):
    loc = tree.get("location") or {}
    return bool(tree.get("story")) and loc.get("latitude") is not None and loc.get("longitude") is not None


# Map pins are drawn, not numbered. Twenty-eight species would be twenty-eight
# inconsistent drawings, so trees are grouped into a handful of silhouettes that
# read at pin size. Because every tree already carries a species, this gives 100%
# pin coverage without depending on photo sourcing.
SPECIES_ICONS = {
    # Bold, species-true silhouettes, one or two opacity layers for depth.
    # All currentColor so the pin colour-flip (moss / cream on active) keeps
    # working. Drawn for legibility at 28px.
    "broadleaf": (
        '<path opacity=".45" d="M20 5c-5 0-8 3-9 6-3 .5-5 3-5 6 0 4 3 7 7 7h14c4 0 7-3 7-7 0-3-2-5.5-5-6-1-3-4-6-9-6z"/>'
        '<path d="M20 8c-4.5 0-7.5 2.5-8.5 5.5C8.5 14 6.5 16 6.5 19c0 3.5 3 6 6.5 6h14c3.5 0 6.5-2.5 6.5-6 0-3-2-5-5-5.5C27.5 10.5 24.5 8 20 8z"/>'
        '<path d="M18.8 38h2.4l-.7-13h-1z"/>'
    ),
    "oak": (
        '<path opacity=".45" d="M8 20c-2-1-3-3-2.5-5C4 13 5 10 8 9.5 8.5 6.5 11.5 5 14 6c1.5-2.5 6-3.5 8.5-1.5C26 3 30 4.5 30.5 8c3 0 5 2.5 4.5 5.5 1.5 1.5 1.5 4.5-.5 6z"/>'
        '<path d="M9.5 21.5c-2.5-.5-4-3-3-5.5-1-2 .5-4.5 3-5C10 8.5 12.5 7 15 8c2-2.5 6-2.5 8 0 2.5-1 5.5.5 6 3 2.5.5 4 3 3 5-1 2.5-2.5 4-5 4.5z"/>'
        '<path d="M17.5 38h5l-1.2-9 4.5-4-1-1.5-4 3-.3-6h-1.5l-.3 6-4-3-1 1.5 4.5 4z"/>'
        '<ellipse opacity=".45" cx="29" cy="24" rx="1.6" ry="2.2"/>'
    ),
    "plane": (
        '<path opacity=".45" d="M20 3c-6 0-10 3.5-10.5 8-2.5 1-4 3.5-4 6 0 4 3 6.5 6.5 6.5h16c3.5 0 6.5-2.5 6.5-6.5 0-2.5-1.5-5-4-6C30 6.5 26 3 20 3z"/>'
        '<path d="M20 6c-5 0-8.5 3-9 7-2 .8-3.5 2.7-3.5 5 0 3 2.5 5.5 5.5 5.5h14c3 0 5.5-2.5 5.5-5.5 0-2.3-1.5-4.2-3.5-5-.5-4-4-7-9-7z"/>'
        '<path d="M19 38h2.2l-.5-14.5h-1.2z"/>'
        '<path d="M14 23.5l-.3 3.2m0 0a1.8 1.8 0 101.8 1.8 1.8 1.8 0 00-1.8-1.8z"/>'
        '<path opacity=".45" d="M26.5 23.5l.3 2.2m0 0a1.6 1.6 0 101.6 1.6 1.6 1.6 0 00-1.6-1.6z"/>'
    ),
    "ginkgo": (
        '<path opacity=".45" d="M20 4C11 6 6 13 6.5 21c.3 4 2.5 7 5.5 9l8-9.5L28 30c3-2 5.2-5 5.5-9C34 13 29 6 20 4z"/>'
        '<path d="M20 7c-7 1.8-11 7.5-10.7 14 .2 3 1.7 5.6 4 7.3L19.5 21l.5-11 .5 11 6.2 7.3c2.3-1.7 3.8-4.3 4-7.3C31 14.5 27 8.8 20 7z"/>'
        '<path d="M19 38h2l-.4-10h-1.2z"/>'
    ),
    "cedar": (
        '<path d="M8 13h24l-7-5H15z"/>'
        '<path opacity=".45" d="M6 20h28l-6.5-4.5h-15z"/>'
        '<path d="M4.5 27h31l-7-4.5H11.5z"/>'
        '<path d="M19 38h2.4l-.6-11h-1.2z"/>'
    ),
    "pine": (
        '<path opacity=".45" d="M20 3C11 3 5.5 8 5 13.5 8 16 13.5 17.5 20 17.5S32 16 35 13.5C34.5 8 29 3 20 3z"/>'
        '<path d="M20 5.5c-7.5 0-12.5 4-13 8.5 2.7 2 7.5 3 13 3s10.3-1 13-3c-.5-4.5-5.5-8.5-13-8.5z"/>'
        '<path d="M18.5 38h3.5c-1-7-1.2-13-.7-21l-1.8-.2c-.8 8-1 14.5-1 21.2z" transform="rotate(-4 20 27)"/>'
    ),
    "cypress": (
        '<path opacity=".45" d="M20 2c-5 5-8 12-8 20 0 6 3 11 8 13 5-2 8-7 8-13 0-8-3-15-8-20z"/>'
        '<path d="M20 5c-4 4.5-6.3 10.5-6.3 17 0 5 2.4 9.2 6.3 11 3.9-1.8 6.3-6 6.3-11 0-6.5-2.3-12.5-6.3-17z"/>'
        '<path d="M19.2 38h1.6v-3h-1.6z"/>'
    ),
    "yew": (
        '<path opacity=".45" d="M20 8C10 8 3.5 14 3.5 21c0 5 4 9 10 9h13c6 0 10-4 10-9 0-7-6.5-13-16.5-13z"/>'
        '<path d="M20 11c-8.5 0-14 5-14 10.5 0 4 3.3 7 8 7h12c4.7 0 8-3 8-7C34 16 28.5 11 20 11z"/>'
        '<path d="M15 38h2.5l.5-10h-1.5zM22.5 38H25l-1-10h-1.5zM19 38h2v-9h-2z"/>'
    ),
    "sequoia": (
        '<path opacity=".45" d="M20 1c-4 6-6.5 14-6.5 22 0 5 1.5 9 4 11.5h5c2.5-2.5 4-6.5 4-11.5C26.5 15 24 7 20 1z"/>'
        '<path d="M20 4.5c-3 5-5 11.5-5 18.5 0 4.5 1.3 8 3.2 10h3.6c1.9-2 3.2-5.5 3.2-10 0-7-2-13.5-5-18.5z"/>'
        '<path d="M16 38h8l-1.5-5h-5z"/>'
    ),
    "fig": (
        '<path opacity=".45" d="M20 4C10.5 4 4 10 4 17c0 5 3.5 8.5 8.5 9h15c5-.5 8.5-4 8.5-9 0-7-6.5-13-16-13z"/>'
        '<path d="M20 7C11.5 7 6 12 6 17.5c0 4 3 7 7 7.5h14c4-.5 7-3.5 7-7.5C34 12 28.5 7 20 7z"/>'
        '<path d="M14 38h12c-.5-2.5-1.5-4-3-5.5l-1-7.5h-4l-1 7.5c-1.5 1.5-2.5 3-3 5.5z"/>'
        '<path opacity=".45" d="M12 38l2-4.5 1.5 1L14.5 38zM28 38l-2-4.5-1.5 1 1 3.5z"/>'
    ),
    "wingnut": (
        '<path opacity=".45" d="M20 4C11 4 5 9.5 5 16c0 4.5 3 8 7.5 8.5h15C32 24 35 20.5 35 16c0-6.5-6-12-15-12z"/>'
        '<path d="M20 7c-7.5 0-13 4.5-13 10 0 3.5 2.5 6.5 6 7h14c3.5-.5 6-3.5 6-7 0-5.5-5.5-10-13-10z"/>'
        '<path d="M19 38h2l-.4-14h-1.2z"/>'
        '<path opacity=".45" d="M12.5 24.5h1.2v3.5a1.4 1.4 0 11-1.2 0zM26.3 24.5h1.2v5a1.4 1.4 0 11-1.2 0z"/>'
        '<path d="M23 24.5h1.2v7a1.4 1.4 0 11-1.2 0z"/>'
    ),
    "wisteria": (
        '<path d="M8 10c4-4.5 12-6 17-3.5 4 2 7 5.5 7.5 10l-2 .8C29.5 13.5 27 11 24 9.5 20 7.5 13.5 8.5 10 12z"/>'
        '<path opacity=".45" d="M13 12.5a3.2 5.5 0 103.2 5.5 3.2 5.5 0 00-3.2-5.5z"/>'
        '<path d="M20 13.5a3.5 6.5 0 103.5 6.5 3.5 6.5 0 00-3.5-6.5z"/>'
        '<path opacity=".45" d="M27 12a3 5 0 103 5 3 5 0 00-3-5z"/>'
        '<path d="M8.5 38h2.5c.5-9 .5-18-.5-27l-2 .3c1 9 .8 17.7 0 26.7z"/>'
    ),
    "rosette": (
        '<path d="M18.5 38h3l-1-16h-1z"/>'
        '<path d="M20 22c-1-6-4.5-10-10-11 4-1.5 8 0 10 3-1-5 1-9 5-11-1 4 .5 8 3 10 2-3.5 6-5 9.5-4-4.5 2.5-7 5.5-7.5 9-.5-.5-5-.5-10 4z" transform="translate(0,1)"/>'
        '<path opacity=".45" d="M20 23c-3.5-2.5-8-3-11.5-1 3.5 1 6.5 2.5 8.5 5zM20 23c3.5-2.5 8-3 11.5-1-3.5 1-6.5 2.5-8.5 5z"/>'
    ),
    "pagoda": (
        '<path opacity=".45" d="M12 10a6 4.5 0 106 4.5A6 4.5 0 0012 10zM28 10a6 4.5 0 106 4.5 6 4.5 0 00-6-4.5z"/>'
        '<path d="M20 5a7.5 5.5 0 107.5 5.5A7.5 5.5 0 0020 5z"/>'
        '<path d="M13 16.5a6.5 5 0 106.5 5 6.5 5 0 00-6.5-5z"/>'
        '<path opacity=".45" d="M27 16.5a6.5 5 0 106.5 5 6.5 5 0 00-6.5-5z"/>'
        '<path d="M19 38h2.2l-.5-12h-1.2z"/>'
    ),
    "olive": (
        '<path opacity=".45" d="M13 15a6 5 0 106 5 6 5 0 00-6-5zM26 12a6.5 5.5 0 106.5 5.5A6.5 5.5 0 0026 12z"/>'
        '<path d="M19 9a6.5 5.5 0 106.5 5.5A6.5 5.5 0 0019 9z"/>'
        '<path d="M17 38h5c-.5-3.5-1.5-6-3.5-8.5 2-2 2.5-4.5 2-7.5l-2 .3c.4 2.5 0 4.5-1.8 6.2-1.5-2-2.2-4.2-2.2-7h-2c0 3.5 1 6.5 3 9-.3 2.7.5 5 1.5 7.5z"/>'
    ),
}

SPECIES_ARCHETYPES = [
    ("ginkgo", ("ginkgo",)),
    ("plane", ("plane",)),
    ("wingnut", ("wingnut",)),
    ("wisteria", ("wisteria",)),
    ("sequoia", ("sequoia", "redwood")),
    ("cedar", ("cedar", "bald cypress", "montezuma", "fir", "spruce", "larch")),
    ("pine", ("pine",)),
    ("yew", ("yew",)),
    ("cypress", ("cypress",)),
    ("fig", ("fig", "ombú", "ombu", "rubber", "banyan", "camphor")),
    ("olive", ("olive", "elaeagnus")),
    ("rosette", ("palm", "cycad", "dragon")),
    ("pagoda", ("pagoda", "locust", "robinia", "acacia", "albizia")),
    ("oak", ("oak",)),
]


def species_icon(tree):
    """Pick the silhouette for a tree. Falls back to a broadleaf crown, which is
    what most of these city trees actually are."""
    name = species_common(tree).lower()
    for key, needles in SPECIES_ARCHETYPES:
        if any(n in name for n in needles):
            return SPECIES_ICONS[key]
    return SPECIES_ICONS["broadleaf"]


SUBMIT_TEMPLATES = {
    "city": (
        "I want to map my city",
        "Which city?%0D%0A%0D%0A"
        "The trees you would put on its list (as many as you know, a name and rough location each is plenty):%0D%0A"
        "1.%0D%0A2.%0D%0A3.%0D%0A%0D%0A"
        "Anything that makes this city's trees particular? (a species that thrives here, a park, a local habit)%0D%0A%0D%0A"
        "How do you know the city? (you live there, you grew up there, you walk it often)%0D%0A%0D%0A"
        "Your name, for the credit:%0D%0A",
    ),
    "tree": (
        "A tree you are missing",
        "Tree name or description:%0D%0A%0D%0A"
        "City:%0D%0A%0D%0A"
        "Where exactly is it? (street, park, or a Google Maps link, the more precise the better)%0D%0A%0D%0A"
        "Why is it remarkable? (age, size, story, anything you know)%0D%0A%0D%0A"
        "How do you know about it? (link, book, local knowledge)%0D%0A%0D%0A"
        "Photo: attach it if you took it yourself%0D%0A%0D%0A"
        "Your name, for the credit:%0D%0A",
    ),
    "correction": (
        "A correction",
        "Which page or tree?%0D%0A%0D%0A"
        "What is wrong?%0D%0A%0D%0A"
        "How do you know? (a link or local knowledge both count)%0D%0A",
    ),
}


def submit_link(kind):
    """Every contribution button on the site points at our own form
    (Hidde, 2026-07-31: "de Google Form wil ik killen"), carrying what the
    visitor was doing so the form preselects it."""
    return f"/contribute?kind={kind}"



def thumb_url(url, width):
    """A right-sized image URL for the big three sources, original otherwise.

    Hidde, 2026-07-31 ("doe je uberhaupt resolutie aanpassen aan grootte?"):
    we did not, and shipped 6000px originals into 300px cards. Wikimedia,
    Unsplash and iNaturalist all resize on the fly via the URL, free."""
    try:
        if "upload.wikimedia.org/wikipedia/commons/" in url and "/thumb/" not in url:
            head, tail = url.split("/wikipedia/commons/", 1)
            fname = tail.rsplit("/", 1)[-1]
            if not re.search(r"\.(jpe?g|png|gif)$", fname, re.I):
                return url
            # Wikimedia only serves fixed thumbnail buckets since 2024
            # (probed 2026-07-31: 250/330/500/960 are live, 400/800 are 400s).
            for bucket in (250, 330, 500, 960):
                if width <= bucket:
                    width = bucket
                    break
            else:
                width = 960  # cap: 960 is the largest bucket Wikimedia serves;
                # a 960px thumb beats shipping the multi-MB original
            return f"{head}/wikipedia/commons/thumb/{tail}/{width}px-{fname}"
        if "images.unsplash.com/" in url:
            return f"{url.split('?')[0]}?q=80&w={width}&auto=format&fit=crop"
        m = re.match(r"(https://(?:static\.inaturalist\.org|inaturalist-open-data\.s3\.amazonaws\.com)/photos/[^/]+/)(original|large|medium)(\.[A-Za-z]+)(.*)", url)
        if m:
            size = "medium" if width <= 500 else "large"
            return f"{m.group(1)}{size}{m.group(3)}{m.group(4)}"
    except Exception:
        pass
    return url


def img_srcset(url, widths, sizes):
    """src/srcset/sizes attribute string for a photo url."""
    seen, pairs = set(), []
    for w in widths:
        u = thumb_url(url, w)
        if u not in seen:
            seen.add(u)
            pairs.append((u, w))
    cands = ", ".join(f"{esc(u)} {w}w" for u, w in pairs)
    return (f'src="{esc(thumb_url(url, widths[0]))}" '
            f'srcset="{cands}" sizes="{esc(sizes)}"')


def credit_required(license_str):
    """Whether the licence forces a visible on-page credit (Hidde, 2026-07-29:
    record always, display only when the licence requires it). CC0, public
    domain and the Unsplash License require none, so those lines are noise on
    the page and come off; CC BY and BY-SA keep theirs, because that credit is
    the price of the photo and stripping it would breach the licence."""
    lic = (license_str or "").lower()
    if not lic:
        return True
    free = ("cc0", "public domain", "publicdomain", "unsplash", "pdm")
    return not any(f in lic for f in free)


def usable_photo(tree):
    """Return the photo dict if it has a URL, license and attribution and is
    cleared for display; otherwise None. One gate for every page type."""
    photo = tree.get("photo") or {}
    # Three statuses, and the middle one was doing two jobs. "approved" means a
    # run looked at the pixels. "found_needs_check" means it found something
    # plausible and could not look, and it still renders, because Hidde's
    # 2026-08-06 ruling is that we do not hold a page back over a risk a reader
    # can correct. "held" is the marker that was missing: kept in the file,
    # deliberately not published, for a photo we must not show yet.
    if (photo.get("url") and photo.get("license") and photo.get("attribution")
            and photo.get("status") in ("approved", "found_needs_check")):
        # A Commons File: page is HTML, not an image; it renders as a broken
        # img. Shipped five times before this check existed.
        if "/wiki/File:" in photo["url"]:
            ERRORS.append(f"{tree.get('id')}: photo url is a wiki File: page, not an image file")
            return None
        return photo
    return None


def city_face(entry, width=400):
    """The city's face photo url at card size: hero_tree_id first, else the
    first tree with a usable photo, else None. One definition for the
    favourites shelf, the choosers and the cities index."""
    hero = entry["data"].get("hero_tree_id")
    if hero:
        for t in entry["data"]["trees"]:
            if t["id"] == hero and usable_photo(t):
                return thumb_url(usable_photo(t)["url"], width)
    for t in entry["data"]["trees"]:
        if usable_photo(t):
            return thumb_url(usable_photo(t)["url"], width)
    return None


def _fold_name(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def city_aliases():
    """Local spelling -> the English name this site publishes under.

    Shared with scripts/passcheck.py so there is one table rather than two that
    drift. See data/city-aliases.json for why the direction matters."""
    f = DATA / "city-aliases.json"
    if not f.exists():
        return {}
    return json.loads(f.read_text()).get("aliases", {})


def check_city_names(city_list):
    """Refuse to ship a city under its local name when English uses another.

    Every page here is written in English and its readers search in English, so
    the site says Florence and Naples. This shipped wrong twice: the brief
    generator once translated names in the wrong direction (2026-08-06), and the
    same day a city went live as Padova while every other Italian city on the
    site used its English name. Per CLAUDE.md's ratchet, a lesson that lands
    twice becomes a build check rather than a third note. Removing this check
    needs Hidde."""
    alias = city_aliases()
    for entry in city_list:
        d = entry.get("data")
        if not d:
            continue
        for value, field in ((d.get("city", ""), "city name"),
                             (entry.get("slug", ""), "slug")):
            english = alias.get(_fold_name(value))
            if english and _fold_name(english) != _fold_name(value):
                ERRORS.append(
                    f"{entry.get('slug')}: {field} is {value!r}, but this site "
                    f"publishes in English, where it is {english.title()!r}. "
                    f"Rename it and add the old slug to RENAMED_CITY_SLUGS so "
                    f"the live URL keeps resolving, or remove the pair from "
                    f"data/city-aliases.json if English really does use {value!r}.")


def load_cities():
    city_list = json.loads((DATA / "city-list.json").read_text())["cities"]
    for entry in city_list:
        f = DATA / "cities" / f"{entry['slug']}.json"
        entry["data"] = json.loads(f.read_text()) if f.exists() else None
    check_city_names(city_list)
    return city_list


def load_collections():
    coll_dir = DATA / "collections"
    if not coll_dir.exists():
        return []
    return [json.loads(f.read_text()) for f in sorted(coll_dir.glob("*.json"))]


def load_registers():
    """The register layer (CLAUDE.md, 'The register layer', approved 2026-07-29/30):
    officially designated trees from government registers, shown as honestly-labeled
    map dots. Not our research, not collectible, no own pages. Each data/registers/*.json
    already carries only trees a register itself calls monumental/remarkable (never a
    bulk inventory) and only the licence this project verified as commercial-reuse-safe.

    Registers do not share a shape and never will: one is Japanese cultural-property
    records, one is an Italian ministry spreadsheet, one is a Portuguese WFS. So the
    fields are read by fallback rather than by schema. Anything an entry flags as a
    group (an avenue, a stand) is skipped, because a dot has to be a place you can
    stand."""
    reg_dir = DATA / "registers"
    if not reg_dir.exists():
        return []
    out = []
    for f in sorted(reg_dir.glob("*.json")):
        d = json.loads(f.read_text())
        if not isinstance(d, dict):
            # A register file is an object carrying its licence, its proof and
            # its entries. A bare list has no licence attached, and an import
            # that skips the wrapper is exactly how unlicensed data would reach
            # the map. Refuse it loudly rather than reading it.
            ERRORS.append(f"register {f.name} is a bare list with no licence block; "
                          f"an import must write the wrapper (see scripts/import_wien.py)")
            continue
        if d.get("publish_dots") is False:
            # Paris is ODbL, which is share-alike for derived databases, and the
            # map publishes exactly such a file. Held back until Hidde decides
            # whether our own register export may carry ODbL terms: that is a
            # question about how this project licenses what it publishes, so it
            # is his, not a run's. The data is imported and usable for research.
            continue
        designation = (d.get("designation") or d.get("attribution")
                       or d.get("prefecture") or "official register")
        for t in d.get("trees", []) + d.get("entries", []):
            if t.get("group"):
                continue
            # Hard rule 10, enforced here rather than trusted to each importer.
            # A register that records ownership or access lets us honour it; one
            # that records neither is handled at the file level with
            # publish_dots, as Brussels is. Keeping the data and withholding the
            # dot are different decisions, and only the dot can send someone to
            # a stranger's garden.
            if t.get("private") or t.get("access_restricted"):
                continue
            lat, lng = t.get("latitude"), t.get("longitude")
            if lat is None or lng is None:
                continue
            name = (t.get("name_en") or t.get("name") or t.get("name_ja")
                    or t.get("name_it") or t.get("name_pt") or t.get("species") or "")
            area = (t.get("area_en") or t.get("area") or t.get("comune")
                    or t.get("concelho") or t.get("city") or t.get("place")
                    or t.get("province") or t.get("prefecture") or "")
            own = t.get("designation")
            if d.get("prefecture") and not own:
                own = f"{d['prefecture']} Natural Monument"
            out.append({
                "name": name,
                # English display area falls back to the raw field rather than
                # hiding a tree a translation was missed for (P7: say what you
                # know honestly, never blank).
                "area": area,
                "designation": own or designation,
                "lat": lat,
                "lng": lng,
            })
    return out


def load_species_intros():
    """Hand-written intros keyed by common_name. A species page can't publish
    without one (Contract F, P3)."""
    sp_dir = DATA / "species"
    if not sp_dir.exists():
        return {}
    out = {}
    for f in sorted(sp_dir.glob("*.json")):
        s = json.loads(f.read_text())
        out[s["common_name"]] = s
    return out


def load_country_intros():
    """Hand-written country intros keyed by country name. Contract G: no page
    without one, same gate as species (P3, no templated country pages)."""
    c_dir = DATA / "countries"
    if not c_dir.exists():
        return {}
    out = {}
    for f in sorted(c_dir.glob("*.json")):
        d = json.loads(f.read_text())
        out[d["country"]] = d
    return out


def country_name(intro_data, capital=False):
    """'the Netherlands' in a sentence, 'The Netherlands' at its start."""
    art = intro_data.get("article")
    name = intro_data["country"]
    if not art:
        return name
    return f"{art.capitalize() if capital else art} {name}"


PARK_WORDS = ("park", "garden", "jardin", "jardim", "giardin", "parc", "parco",
              "tuin", "villa ", "orto", "botanic", "bois", "hortus", "schlosspark",
              "stadtpark", "retiro")
PARK_MIN_TREES = 5


def park_key(tree):
    """The named park a tree stands in, or None.

    Read from the neighbourhood first and the address second, taking the clause
    before the first comma and dropping parentheticals, the same flattening the
    walk namer uses: one Orto Botanico was four different places until
    "(arboretum section)" was stripped."""
    loc = tree.get("location") or {}
    for field in (loc.get("neighbourhood"), loc.get("address")):
        head = str(field or "").split(",")[0]
        head = re.sub(r"\([^)]*\)?", "", head)
        head = re.sub(r"\s+", " ", head).strip(" -/")
        if len(head) >= 4 and any(w in head.lower() for w in PARK_WORDS):
            return head
    return None


def group_trees_by_park(renderable):
    """(city_slug, park name) -> (city_entry, park, [trees]), biggest first.

    A park is a place you spend an afternoon, which is why the bar is higher
    than the species bar of three: below five trees a park page is a thin page
    wearing a park's name, and the city page already serves it better."""
    groups = {}
    for entry in renderable:
        for t in entry["data"]["trees"]:
            if not tree_is_renderable(t):
                continue
            name = park_key(t)
            if not name:
                continue
            groups.setdefault((entry["slug"], name), (entry, name, []))[2].append(t)
    return groups


def group_trees_by_species(renderable):
    """common_name -> list of (city_entry, tree), preserving city order then age."""
    groups = {}
    # Tree ids are the join key for species and collection pages, so two cities
    # sharing an id prefix silently point each other's URLs at the wrong city
    # (Cordoba and Cork both started cor_, caught 2026-08-03).
    _id_city = {}
    for entry in renderable:
        for t in entry["data"]["trees"]:
            other = _id_city.get(t["id"])
            if other and other != entry["slug"]:
                ERRORS.append(f"tree id {t['id']} is used by both {other} and {entry['slug']}")
            _id_city[t["id"]] = entry["slug"]

    for entry in renderable:
        trees = [t for t in entry["data"]["trees"] if tree_is_renderable(t)]
        for t in trees:
            groups.setdefault(species_common(t), []).append((entry, t))
    return groups


MONTHS_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
SPECIES_MIN_TREES = 3
COUNTRY_MIN_CITIES = 3  # Contract G: fewer cities and a country page is a city duplicate


def oldest_tree(trees, city_data=None):
    """Highest age_max wins, unless the city names its answer explicitly.

    oldest_tree_id exists for cities where the mechanical winner is the wrong
    answer: Amsterdam's Hortus cycad out-ages the Heimanseik but is a potted
    cycad, not a tree, and the hand-written answer rightly names the oak. The
    build cross-checks that the chosen tree appears in question_answer."""
    if city_data and city_data.get("oldest_tree_id"):
        named = [t for t in trees if t["id"] == city_data["oldest_tree_id"]]
        if named:
            return named[0]
    return max(trees, key=lambda t: t.get("age_max") or 0)


def location_is_approximate(tree):
    """Does the pin point at a rough spot rather than the tree itself?

    location_precision is the only source of truth. A tree that never got the
    field counts as approximate: the warning next to the directions button
    costs a visitor nothing, a missing warning costs them a wasted walk.
    """
    return tree.get("location_precision", "approximate") != "confirmed"


# ---------------------------------------------------------------- tree pages


COLLECT_JS = """
<script>
(function() {
  var btn = document.getElementById('collect-btn');
  var dlg = document.getElementById('collect-dialog');
  if (!btn) return;
  if (dlg && dlg.showModal) {
    btn.addEventListener('click', function() {
      at.track('collect-open');
      dlg.showModal();
    });
    document.getElementById('collect-close').addEventListener('click', function() { dlg.close(); });
    dlg.addEventListener('click', function(e) { if (e.target === dlg) { dlg.close(); } });
  } else {
    btn.addEventListener('click', function() { window.location.href = '../app'; });
  }
})();
</script>
"""


PHENOLOGY = {}


def load_phenology():
    """Per-species year calendars (Hidde, 2026-08-02: every tree should carry a
    calendar that is correct, not just a single peak). Phenology is a property
    of the species in a climate, so it lives per species and gets shifted by
    latitude at render time. A species without a file simply shows no calendar,
    the same honest gap as a missing photo."""
    d = DATA / "phenology"
    if not d.exists():
        return {}
    out = {}
    for f in sorted(d.glob("*.json")):
        e = json.loads(f.read_text())
        out[e["common_name"]] = e
    return out


def _shift(months, delta):
    return sorted({((m - 1 + delta) % 12) + 1 for m in months})


# How loud a moment actually is, in plain words (Hidde, 2026-08-05). The old
# curve drew leaf cover, which made every evergreen a straight line, and a
# straight line says nothing. This draws how much there is to SEE, so a moment
# has to carry a judgement: a ginkgo flowers in April and nobody can tell, and
# it turns gold in November and people cross town for it. `nice` is the default
# on purpose, because a species nobody has judged yet should get no false peak.
INTENSITY_WEIGHTS = {
    "unseen": 0.0,
    "nice": 0.18,
    "striking": 0.35,
    "worth the trip": 0.55,
}
# Baselines: bare is nearly nothing, in leaf is a decent afternoon, and the
# turn months sit between the two.
BASE_BARE, BASE_TURN, BASE_LEAF, FRESH_LEAF_BONUS = 0.08, 0.22, 0.38, 0.15
SHOULDER = 0.4  # the month either side of a moment, so a peak rises and falls


def phase_mid(months):
    """The middle month of a phase, handling one that wraps the new year."""
    if not months:
        return None
    run = sorted(months)
    if 12 in run and 1 in run:
        run = sorted(((m + 5) % 12) + 1 for m in run)
        return ((run[len(run) // 2] + 6) % 12) + 1
    return run[len(run) // 2]


def highlight_curve(ph):
    """Twelve values for how much there is to see, and the moments behind them.

    Not normalised per species: a genuinely uneventful tree stays low all year,
    because if every species reached full height the peak would stop meaning
    anything. Same argument as scarcity on best_time.
    """
    leaf = set(ph.get("leaf") or [])
    bare = set(ph.get("bare") or [])
    inten = ph.get("intensity") or {}

    vals = [BASE_BARE if m in bare else (BASE_LEAF if m in leaf else BASE_TURN)
            for m in range(1, 13)]
    # The spring flush is a real moment and it is recorded nowhere in the data.
    for m in range(1, 13):
        if m in leaf and ((m - 2) % 12) + 1 in bare:
            vals[m - 1] += FRESH_LEAF_BONUS

    moments = []
    for key, kind, label_key in (("flowers", "flowers", "flower_label"),
                                 ("fruit", "fruit", "fruit_label"),
                                 ("colour", "autumn colour", "colour_label")):
        word = str(inten.get(key, "nice")).strip().lower()
        if word not in INTENSITY_WEIGHTS:
            ERRORS.append(f"unknown phenology intensity {word!r} for {ph.get('common_name')}; "
                          f"allowed: {sorted(INTENSITY_WEIGHTS)}")
            word = "nice"
        weight = INTENSITY_WEIGHTS[word]
        months = ph.get(key) or []
        if not months or not weight:
            continue
        span = set(months)
        for m in months:
            vals[m - 1] += weight
            for n in (((m - 2) % 12) + 1, (m % 12) + 1):
                if n not in span:
                    vals[n - 1] += weight * SHOULDER
        moments.append({"kind": kind, "word": word, "month": phase_mid(months),
                        "label": ph.get(label_key)})

    return [min(1.0, v) for v in vals], moments


# Two checks born from one afternoon of merging six register passes (2026-08-05).
# Both failures were live before anyone noticed, both are mechanical, and both
# cost a human twenty minutes to find by reading pages. The build finds them now.

NUMBER_WORDS = {w: n for n, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
_N = "|".join(NUMBER_WORDS)
# Three shapes, each deliberately narrow. A page counts other things all the
# time ("the two trees frame two kinds of longevity", "only four trees in the
# whole city carry the designation"), so only a phrase that can just about
# only mean "this is how many trees this page has" is allowed to fail a build.
SUMMARY = ("meta_description", "question_meta")
ALL_COPY = ("intro", "meta_description", "question_meta", "question_answer",
            "question_context", "faq")
_PROMISE = [
    # "Naples's ten most remarkable trees"
    (re.compile(r"\b(%s)\s+(?:most|remarkable)\b" % _N, re.I), lambda n: {n}, ALL_COPY),
    # "its story, and nine more". One or two trees are named before it. Only in
    # the two summary fields: in body prose "five more planted by the residents"
    # is Bath counting the five planes inside a single entry.
    (re.compile(r"\b(%s)\s+more\b" % _N, re.I), lambda n: {n + 1, n + 2}, SUMMARY),
    # "six of the ten trees on this list", "none of these ten need a ticket"
    (re.compile(r"\bof the\s+(%s)\s+trees?\b" % _N, re.I), lambda n: {n}, ALL_COPY),
    (re.compile(r"\b(?:these|the)\s+(%s)\s+"
                r"(?:are|is|need|needs|were|was|stand|stands|remain|listed|below)\b" % _N, re.I),
     lambda n: {n}, ALL_COPY),
    # "All sixteen are free to see", "All sixteen trees on this list". Vienna
    # grew to nineteen with both of these live in the intro and FAQ while the
    # meta fields were caught: the second time this class slipped in one day,
    # so per the ratchet it becomes pattern rather than vigilance. Anchored on
    # trees/are/stand/need so "all five trunks" inside an entry stays legal.
    (re.compile(r"\ball\s+(%s)\s+(?:trees?|are|stand|need|needs|remain)\b" % _N, re.I),
     lambda n: {n}, ALL_COPY),
]


def check_count_promises(city_data, canonical):
    """A city that grows past ten must stop promising ten.

    Florence went to fifteen with three separate sentences still saying ten, one
    of them a FAQ answer counting which six of the ten were free. The title is
    generated and corrected itself; the hand-written copy did not, and nothing
    was watching it."""
    n = len(city_data.get("trees") or [])
    fields = [(k, city_data.get(k, "")) for k in
              ("intro", "meta_description", "question_meta", "question_answer",
               "question_context")]
    for f in city_data.get("faq") or []:
        fields += [("faq", f.get("q", "")), ("faq", f.get("a", ""))]
    for key, text in fields:
        if not text:
            continue
        for rx, allowed, scope in _PROMISE:
            if key not in scope:
                continue
            for m in rx.finditer(text):
                word = next(g for g in m.groups() if g)
                claims = allowed(NUMBER_WORDS[word.lower()])
                if min(claims) < 4 or n in claims:
                    continue
                ERRORS.append(
                    f"{canonical}: copy still promises "
                    f"{'/'.join(str(c) for c in sorted(claims))} trees but the city has "
                    f"{n} ({m.group(0)!r})")


def check_species_names(cities):
    """Hard rule 9: one canonical common name per species, or the species pages
    split. Florence carried a Deodar Cedar and a Himalayan Cedar, the same tree
    twice, and Celtis australis was living under three names across the corpus."""
    by_latin = {}
    for entry in sorted(cities, key=lambda e: e["slug"]):
        slug, data = entry["slug"], entry.get("data") or {}
        for t in data.get("trees") or []:
            sp = t.get("species") or ""
            m = re.search(r"\(([^)]+)\)", sp)
            if not m:
                continue
            common = sp[:m.start()].strip()
            by_latin.setdefault(m.group(1).strip(), {}).setdefault(common, []).append(slug)
    for latin, commons in sorted(by_latin.items()):
        if len(commons) > 1:
            spread = "; ".join(f"{c!r} in {sorted(set(v))[0]}" + (" and others" if len(set(v)) > 1 else "")
                               for c, v in sorted(commons.items()))
            ERRORS.append(f"species {latin} uses {len(commons)} common names, hard rule 9 "
                          f"allows one: {spread}")
    # And the mirror, which the check above cannot see: ONE common name under
    # several Latin spellings splits the same species just as badly. Found
    # 2026-08-08 while counting species for a press story: "London Plane" was
    # living as Platanus x acerifolia, x hispanica, acerifolia and hispanica at
    # once, 62 trees that should be one species page and were four groups.
    # Single-tree ensembles that deliberately name several species are exempt.
    by_common = {}
    for entry in sorted(cities, key=lambda e: e["slug"]):
        slug, data = entry["slug"], entry.get("data") or {}
        for t in data.get("trees") or []:
            sp = t.get("species") or ""
            m = re.search(r"\(([^)]+)\)", sp)
            latin = m.group(1).strip() if m else ""
            if not m or "," in latin or " and " in latin:
                continue
            # A cultivar, form, subspecies or variety of the same binomial is
            # not a split, it is a legitimately finer record: York's
            # Fagus sylvatica 'Miltonensis' belongs with Edinburgh's beech.
            # Only a different binomial under one common name is the bug, and
            # that is always a synonym nobody reconciled (Sophora japonica
            # beside Styphnolobium japonicum).
            binomial = re.split(r"\s+(?:'|f\.|subsp\.|var\.|ssp\.)", latin)[0].strip()
            # Some parentheticals describe a place rather than name a species
            # ("Mixed species (Napoleonic public garden)"): a binomial is a
            # capitalised genus and a lowercase epithet, and nothing else.
            if not re.match(r"^[A-Z][a-z]+ (x )?[a-z-]+$", binomial):
                continue
            common = sp[:m.start()].strip()
            by_common.setdefault(common, {}).setdefault(binomial, []).append(slug)
    for common, latins in sorted(by_common.items()):
        if len(latins) > 1:
            spread = "; ".join(f"{l!r} in {sorted(set(v))[0]}"
                               + (" and others" if len(set(v)) > 1 else "")
                               for l, v in sorted(latins.items()))
            ERRORS.append(f"species {common!r} carries {len(latins)} scientific names, "
                          f"hard rule 9 allows one: {spread}")


def check_phenology():
    """The ratchet for the bug this replaces (CLAUDE.md QA layer 1): a species
    that records real moments and still draws a straight line is a scoring bug
    or an intensity block set to unseen across the board. Either way the page
    would show a flat chart that says nothing, so the build stops instead."""
    for name, e in sorted(PHENOLOGY.items()):
        for key in e.get("intensity") or {}:
            if key not in ("flowers", "fruit", "colour"):
                ERRORS.append(f"phenology {name}: unknown intensity key {key!r}")
        events = sum(len(e.get(k) or []) for k in ("flowers", "fruit", "colour"))
        vals, _ = highlight_curve(e)
        if events and max(vals) - min(vals) < 0.02:
            ERRORS.append(f"phenology {name}: records {events} seasonal month(s) but the "
                          f"curve is flat, so the chart would say nothing")


def phenology_for(tree, lat):
    """The species calendar, shifted for where the tree actually stands. South
    of about 42N spring runs a month early and leaves hang on later; north of
    56N the reverse. Tropical latitudes get nothing: the temperate pattern
    would simply be wrong there, and a wrong calendar is worse than none."""
    e = PHENOLOGY.get(species_common(tree))
    if not e or abs(lat) < 25:
        return None
    delta = -1 if lat < 42 else (1 if lat > 56 else 0)
    out = dict(e)
    for k in ("leaf", "flowers", "fruit", "colour", "bare"):
        if e.get(k) and len(e[k]) < 12:
            out[k] = _shift(e[k], delta)
    return out


def season_block(tree, lat):
    """The year as one chart: how much there is to see, month by month.

    This is one figure where the page used to stack two (a best_time peak chart
    and a leaf-cover year chart), which made the same promise twice in a row.
    The curve is the seasonal highlight score from the species phenology, the
    marked peak is the tree's own best_time, and the icons sit on the months
    each thing actually happens. A tree whose species has no phenology file
    falls back to the older best_time-only curve rather than losing its chart.
    """
    ph = phenology_for(tree, lat)
    bt = tree.get("best_time") or {}
    has_bt = bool(bt.get("label") and bt.get("months"))

    if not ph or not (ph.get("leaf") or ph.get("bare")):
        return season_curve(tree) if has_bt else ""

    vals, moments = highlight_curve(ph)
    if max(vals) - min(vals) < 0.02:
        # A species with nothing to show is an honest gap, like a missing photo.
        if has_bt:
            return season_curve(tree)
        return ('<p class="ph-foot ph-noseason">This tree looks much the same in '
                'every month of the year, so there is no season to chart.</p>')

    now = date.today().month
    peak_m = phase_mid(bt.get("months") or []) if has_bt else None
    in_season = has_bt and now in bt["months"]

    W, H, pad_t, pad_b, pad_x = 320.0, 128.0, 30.0, 24.0, 10.0
    plot_h = H - pad_t - pad_b
    step = (W - 2 * pad_x) / 11.0
    pts = [(pad_x + i * step, pad_t + (1 - v) * plot_h) for i, v in enumerate(vals)]
    line = smooth_path(pts)
    area = line + f" L {pts[-1][0]:.1f},{pad_t + plot_h:.1f} L {pts[0][0]:.1f},{pad_t + plot_h:.1f} Z"

    grid = "".join(
        f'<line x1="{pad_x:.1f}" y1="{pad_t + plot_h * f:.1f}" x2="{W - pad_x:.1f}" y2="{pad_t + plot_h * f:.1f}" class="sc-grid"/>'
        for f in (0.25, 0.5, 0.75))
    ticks = "".join(
        f'<text x="{pts[i][0]:.1f}" y="{H - 6:.0f}" class="sc-m">{MONTH_ABBR[i]}</text>'
        for i in range(12))
    now_x = pts[now - 1][0]
    now_marker = (
        f'<line x1="{now_x:.1f}" y1="{pad_t - 6:.1f}" x2="{now_x:.1f}" y2="{pad_t + plot_h:.1f}" class="sc-now"/>'
        f'<text x="{now_x:.1f}" y="{pad_t - 10:.1f}" class="sc-nowlabel">now</text>')

    def badge(month, kind):
        x, y = pts[month - 1]
        return (f'<span class="sc-peakbadge" style="left:{x / W * 100:.1f}%;top:{y / H * 100:.1f}%">'
                f'{KIND_ICONS[kind]}</span>')

    # The marked peak follows best_time, even where the curve tops out
    # elsewhere: that field is a judgement about this tree and it outranks a
    # score derived from the species.
    badges, peak_dot = [], ""
    kind = season_kind(bt) if has_bt else ""
    if peak_m:
        px, py = pts[peak_m - 1]
        peak_dot = f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" class="sc-peak"/>'
        if kind:
            badges.append(badge(peak_m, kind))
    # Only the loud moments get their own icon, so the chart does not crowd.
    for mo in moments:
        if mo["word"] in ("striking", "worth the trip") and mo["month"] != peak_m:
            badges.append(badge(mo["month"], mo["kind"]))

    keys = "".join(
        '<span class="ph-key">%s%s</span>' % (KIND_ICONS[mo["kind"]],
                                               esc(mo["label"] or mo["kind"].capitalize()))
        for mo in moments)
    now_badge = '<span class="best-now">at its best right now</span>' if in_season else ""
    label_line = f'<p class="season-label">{esc(bt["label"])}</p>' if has_bt else ""

    return """
  <figure class="season phenology">
    <figcaption class="season-head"><span>The tree's year</span>%s</figcaption>
    <div class="season-plot">
    %s
    <svg viewBox="0 0 %.0f %.0f" class="season-svg" role="img" aria-label="How much there is to see through the year">
      %s
      <path d="%s" class="sc-area"/>
      <path d="%s" class="sc-line"/>
      %s
      %s
      %s
    </svg>
    </div>
    <p class="ph-keys">%s</p>
    %s
    <p class="ph-foot">The line is our estimate of how much there is to see, not a measurement. Typical for this species where this tree stands; exact weeks shift with the year.</p>
  </figure>""" % (now_badge, "".join(badges), W, H, grid, area, line,
                  now_marker, peak_dot, ticks, keys, label_line)


def build_tree_page(city_entry, tree, all_trees, pages, species_pages=None, country_pages=None):
    species_pages = species_pages or {}
    country_pages = country_pages or {}
    city_data = city_entry["data"]
    city = city_data["city"]
    country = city_data["country"]
    cslug = city_entry["slug"]
    tslug = slugify(tree["name"])
    loc = tree["location"]
    age = age_token(tree)
    canonical = f"{BASE_URL}/{cslug}/{tslug}"
    rootpath = "../"

    title = fit_title([
        f"{tree['name']}: {age} Year Old {species_common(tree)} in {city}",
        f"{tree['name']}: {age} Year Old Tree in {city}",
        f"{tree['name']} in {city}",
        tree["name"],
    ], canonical)
    description = meta_from_story(tree["story"])
    story_wc = len(tree["story"].split())
    if not (150 <= story_wc <= 250):
        ERRORS.append(f"{canonical}: story is {story_wc} words, CLAUDE.md Step 3 requires 150-250")

    others = [t for t in all_trees if t["id"] != tree["id"]]
    others.sort(key=lambda t: haversine(
        (loc["latitude"], loc["longitude"]),
        (t["location"]["latitude"], t["location"]["longitude"])))
    nearby = others[:3]

    # Contract G: the country crumb becomes a link the moment its page exists.
    country_url = f"{BASE_URL}/{country_pages[country]}" if country in country_pages else None
    crumb_items = [
        ("Home", BASE_URL),
        (country, country_url),
        (city, f"{BASE_URL}/{cslug}"),
        (tree["name"], None),
    ]

    photo = usable_photo(tree)
    photo_html = ""
    og_image = ""
    if photo:
        credit_line = (f"<figcaption>Photo: {esc(photo['attribution'])} ({esc(photo['license'])})</figcaption>"
                       if credit_required(photo.get("license")) else "")
        photo_html = f"""
  <figure class="tree-photo">
    <img {img_srcset(photo['url'], [700, 1100, 1600], "(max-width: 800px) 100vw, 760px")} alt="{esc(tree['name'])}" loading="lazy">
    {credit_line}
  </figure>"""
        og_image = f'\n<meta property="og:image" content="{esc(thumb_url(photo["url"], 1200))}">'
    else:
        # 432 of 759 trees have no open-licence photograph, and most never will:
        # by 2026-08-08 four sources had been tried and three further lanes tested
        # to destruction, and the conclusion was that these trees are simply not
        # photographed by anybody under a licence we can use. So the page stops
        # having a hole where an image belongs and gets something drawn instead,
        # using the species silhouette the map pins already use. It is not a
        # placeholder pretending to be a photo: it says which species this is,
        # which is real information, and invites the one source that can still
        # close the gap.
        photo_html = f"""
  <figure class="tree-noph">
    <span class="tree-noph-art" aria-hidden="true"><svg viewBox="0 0 40 40">{species_icon(tree)}</svg></span>
    <figcaption>
      <b>{esc(species_common(tree))}</b>
      <span>Nobody has published a photograph of this tree under a licence we can use.
      <a href="../contribute">Send us yours</a> and it goes on this page with your name on it.</span>
    </figcaption>
  </figure>"""

    # Honest where it costs the visitor something: an approximate pin means
    # standing in the right park without finding the tree.
    approx_note = (
        '<p class="approx-note">The pin marks the right spot roughly, not the tree itself. '
        'It stands here, but we have not confirmed the precise position on the ground yet. '
        f'<a href="{submit_link("correction")}">Know exactly where it is?</a></p>'
        if location_is_approximate(tree) else ""
    )

    label = f'<span class="tree-label">{esc(tree["label"])}</span>' if tree.get("label") else ""
    facts = f"""
<dl class="facts">
  <dt>Species</dt><dd>{esc(tree.get('species', ''))}</dd>
  <dt>Age estimate</dt><dd>{esc(tree.get('age_estimate', 'unknown'))}</dd>
  <dt>Location</dt><dd>{esc(loc.get('address', ''))} ({esc(loc.get('neighbourhood', ''))})</dd>
  <dt>Access</dt><dd>{esc(tree.get('access', ''))}</dd>
  <dt>Getting there</dt><dd>{esc(tree.get('transport', ''))}</dd>
</dl>"""
    nearby_html = "".join(
        f'<li><a href="{slugify(t["name"])}">{esc(t["name"])}, '
        f'{esc(t.get("age_estimate", ""))} ({esc(t["location"].get("neighbourhood", ""))})</a></li>'
        for t in nearby
    )

    sp_common = species_common(tree)
    sp_slug = species_pages.get(sp_common)
    species_line = (
        f' It is a {esc(sp_common)}; see <a href="../species/{sp_slug}">every {esc(sp_common.lower())} on the site</a>.'
        if sp_slug else ""
    )

    # Sprint 1 of PRODUCT_IA.md (2026-07-28): the do-buttons live above the
    # story (Atlas Obscura's law), the chips answer the first three questions
    # at a glance, and nearby becomes cards with distances so no page dead-ends.
    # Chips answer what a visitor asks, nothing else (Hidde, 2026-07-29:
    # "pin confirmed, is dat informatie voor de gebruiker of voor ons twee?").
    # A confirmed pin is the normal case and says nothing; only the
    # approximate warning earns a chip. The season story lives in the year
    # chart below, not as an unexplained label up top.
    season_html = season_block(tree, loc['latitude'])
    precision_chip = ('<span class="chip approx">pin approximate</span>'
                      if location_is_approximate(tree) else '')
    chips = (f'<p class="chip-row"><span class="chip">{esc(tree.get("age_estimate", "age unknown"))}</span>'
             f'<span class="chip">{esc(species_common(tree))}</span>{precision_chip}</p>')
    # "Collect this tree" with an explainer on tap (Hidde, 2026-08-01:
    # "Collect this tree klinkt goed en eigenlijk wil je uitleg scheme als je
    # er op klikt"): the button opens a small dialog saying what collecting
    # is and that it lives in the app, then funnels to /app. Browsers
    # without <dialog> go straight to /app, the old behaviour.
    action_row = f"""
  <div class="action-row">
    <button class="go-btn" id="collect-btn" type="button">Collect this tree</button>
    <a class="go-btn ghost" href="https://www.google.com/maps/dir/?api=1&amp;destination={loc['latitude']},{loc['longitude']}" target="_blank" rel="noopener">Take me there</a>
    <a class="action-link" href="../{cslug}#walk">Walk more trees in {esc(city)}</a>
  </div>
  <dialog id="collect-dialog" class="collect-dialog">
    <h3>Keep the trees you have stood in front of</h3>
    <p>Collecting is the game of Ancient Trees: stand in front of a tree like this one, tick it off, and your collection of old giants grows city by city. It lives in the Ancient Trees app, along with walking routes past several trees.</p>
    <div class="collect-actions">
      <a class="go-btn" href="../app">Get the app</a>
      <button class="go-btn ghost" type="button" id="collect-close">Not now</button>
    </div>
  </dialog>"""

    near_cards = "".join(
        f'<a class="near-card" href="{slugify(t["name"])}"><b>{esc(t["name"])}</b>'
        f'<span>{esc(t.get("age_estimate", ""))} &middot; {dist_label(loc, t["location"])} away</span></a>'
        for t in nearby
    )

    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>{esc(tree['name'])}{label}</h1>
  {chips}
  {photo_html}
  {action_row}
  <div class="prose-block"><p>{esc(tree['story'])}</p></div>
  {season_html}
  <div class="map-embed"><div id="map" class="map"></div></div>
  <p class="go-note">The buttons above open directions and collecting. {esc(tree.get('transport', ''))}</p>
  {approx_note}
  {facts}
  <h2>Trees nearby</h2>
  <div class="near-cards">{near_cards}</div>
  <div class="cta">Curious what else is standing in {esc(city)}? See <a href="../{cslug}">all {len(all_trees)} remarkable ancient trees in {esc(city)}</a> or find out <a href="oldest-tree">what the oldest tree in {esc(city)} is</a>.{species_line}</div>
  <div class="report"><strong>We could use your help.</strong>
    <p class="report-line">This page was researched from a distance. If you know this tree, you know things we do not.</p>
    <a class="report-btn" href="{submit_link('correction')}">Something is wrong here</a>
    <a class="report-btn" href="{submit_link('tree')}">Suggest another tree</a></div>
</main>
"""

    graph = site_graph() + [
        {
            "@type": "TouristAttraction",
            "name": tree["name"],
            "description": tree["story"][:300],
            "isAccessibleForFree": "free" in tree.get("access", "").lower(),
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": loc["latitude"],
                "longitude": loc["longitude"],
            },
        },
        breadcrumb_schema(crumb_items, canonical),
    ]
    head_extra = map_head() + og_image + "\n" + ld_script(graph)
    scripts = single_pin_script(loc["latitude"], loc["longitude"]) + COLLECT_JS

    check_links(canonical, 2 + len(nearby), 4)

    page = render_page(title, description, canonical, body, head_extra, scripts, rootpath)
    pages.append((f"{cslug}/{tslug}.html", page, canonical))
    return tslug


# ------------------------------------------------------------ question pages

def build_question_page(city_entry, collections, pages, country_pages=None):
    country_pages = country_pages or {}
    city_data = city_entry["data"]
    city = city_data["city"]
    country = city_data["country"]
    cslug = city_entry["slug"]
    trees = [t for t in city_data["trees"] if tree_is_renderable(t)]
    old = oldest_tree(trees, city_data)
    oslug = slugify(old["name"])
    loc = old["location"]
    age = age_token(old)
    canonical = f"{BASE_URL}/{cslug}/oldest-tree"
    rootpath = "../"
    question = f"What is the oldest tree in {city}?"

    title = fit_title([
        f"What Is the Oldest Tree in {city}? ({old['name']}, {age} Years)",
        f"What Is the Oldest Tree in {city}? ({age} Years Old)",
        f"What Is the Oldest Tree in {city}?",
    ], canonical)
    description = city_data.get("question_meta") or city_data.get("question_answer", "")[:DESC_MAX]
    answer = city_data.get("question_answer", "")
    context = city_data.get("question_context", "")
    if not answer or not context:
        ERRORS.append(f"{canonical}: question_answer and question_context must be written per city (Contract B)")
    else:
        # Title, pin and read-more link all follow `old`; an answer naming a
        # different tree ships a self-contradicting page (Amsterdam and Tokyo
        # did). Paraphrase is fine, so we only require one distinctive proper
        # noun from the tree's name to appear in the answer.
        generic = {"the", "of", "and", "tree", "trees", "oak", "yew", "yews", "ginkgo",
                   "olive", "olives", "plane", "planes", "cedar", "cypress", "linden",
                   "lime", "ficus", "pine", "elm", "ash", "beech", "chestnut", "wood",
                   "grove", "ring", "garden", "gardens", "old", "great", "monumental",
                   "king", "queen", "prince", "princess", "royal", "grand", "giant",
                   "ancient", "sacred", "holy", "wishing", "guardian",
                   "de", "del", "della", "der", "du", "la", "le", "el", "van", "dos",
                   "das", "do", "di", "san", "santa"}
        tokens = [w for w in re.findall(r"[A-Za-z']+", old["name"])
                  if w[0].isupper() and w.lower() not in generic]
        if tokens and not any(t.lower() in answer.lower() for t in tokens):
            ERRORS.append(f"{canonical}: question_answer never mentions {old['name']!r} "
                          f"(looked for {tokens}); set oldest_tree_id or rewrite the answer")
        if not (150 <= len(context.split()) <= 200):
            ERRORS.append(f"{canonical}: question_context is {len(context.split())} words, Contract B requires 150-200")

    country_url = f"{BASE_URL}/{country_pages[country]}" if country in country_pages else None
    crumb_items = [
        ("Home", BASE_URL),
        (country, country_url),
        (city, f"{BASE_URL}/{cslug}"),
        ("Oldest tree", None),
    ]

    related = [f for f in city_data.get("faq", []) if "oldest" not in f["q"].lower()][:3]
    faq_entities = [{
        "@type": "Question", "name": question,
        "acceptedAnswer": {"@type": "Answer", "text": answer},
    }] + [{
        "@type": "Question", "name": f["q"],
        "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
    } for f in related]

    city_collections = [c for c in collections if any(e["city_slug"] == cslug for e in c.get("entries", []))]
    coll = city_collections[0] if city_collections else None
    coll_link = (
        f'<p class="prose-block">One of {esc(city)}\'s trees also appears in '
        f'<a href="../collections/{coll["slug"]}">{esc(coll["title"])}</a>, a themed collection spanning several cities.</p>'
        if coll else
        '<p class="prose-block">See more <a href="../collections">themed collections</a> of remarkable trees.</p>'
    )

    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>{esc(question)}</h1>
  <p class="answer-first">{esc(answer)}</p>
  <div class="map-embed"><div id="map" class="map"></div></div>
  <div class="prose-block"><p>{esc(context)}</p></div>
  <div class="cta">Read <a href="{oslug}">the full story of {esc(old['name'])}</a>, or see <a href="../{cslug}">all {len(trees)} remarkable ancient trees in {esc(city)}</a>.</div>
  {coll_link}
</main>
"""

    graph = site_graph() + [
        {"@type": "FAQPage", "mainEntity": faq_entities},
        breadcrumb_schema(crumb_items, canonical),
    ]
    head_extra = map_head() + "\n" + ld_script(graph)
    scripts = single_pin_script(loc["latitude"], loc["longitude"])

    check_links(canonical, 3, 3)

    page = render_page(title, description, canonical, body, head_extra, scripts, rootpath)
    pages.append((f"{cslug}/oldest-tree.html", page, canonical))


# ---------------------------------------------------------------- city pages

def build_city_page(entry, tree_slugs, collections, pages, other_cities=(), species_pages=None,
                    country_pages=None):
    species_pages = species_pages or {}
    country_pages = country_pages or {}
    city_data = entry["data"]
    city = city_data["city"]
    country = city_data["country"]
    slug = entry["slug"]
    trees = [t for t in city_data.get("trees", []) if tree_is_renderable(t)]
    if not trees:
        return None
    canonical = f"{BASE_URL}/{slug}"
    rootpath = "./"

    title = fit_title([
        f"Ancient Trees in {city}: {len(trees)} Remarkable Trees Worth Visiting",
        f"Ancient Trees in {city}: {len(trees)} Trees Worth Visiting",
        f"Ancient Trees in {city}",
    ], canonical)
    description = city_data.get("meta_description") or (
        f"The oldest and most remarkable trees in {city}, {country}: "
        f"verified locations, real stories, and how to reach each one."
    )
    check_count_promises(city_data, canonical)
    intro = city_data.get("intro")
    if not intro:
        ERRORS.append(f"{canonical}: city intro (60-100 words, unique) is required by Contract C")
        intro = ""
    elif not (60 <= len(intro.split()) <= 100):
        ERRORS.append(f"{canonical}: city intro is {len(intro.split())} words, Contract C requires 60-100")

    # Contract G: the country crumb becomes a link the moment its page exists.
    country_url = f"{BASE_URL}/{country_pages[country]}" if country in country_pages else None
    crumb_items = [("Home", BASE_URL), (country, country_url), (city, None)]

    cards = []
    markers = []
    for i, t in enumerate(trees, 1):
        loc = t["location"]
        tslug = tree_slugs[t["id"]]
        label = f'<span class="tree-label">{esc(t["label"])}</span>' if t.get("label") else ""
        cphoto = usable_photo(t)
        photo_block = ""
        if cphoto:
            card_credit = (f'<p class="tree-card-credit">Photo: {esc(cphoto["attribution"])} ({esc(cphoto["license"])})</p>'
                           if credit_required(cphoto.get("license")) else "")
            photo_block = f"""
      <div class="tree-card-photo"><img {img_srcset(cphoto['url'], [500, 900], "(max-width: 800px) 100vw, 560px")} alt="{esc(t['name'])}" loading="lazy"></div>
      {card_credit}"""
        cards.append(f"""
    <article class="tree-card" id="tree-{i}">
      {photo_block}
      <div class="tree-card-top">
        <span class="tree-num">{i}</span>
        <h2 class="tree-name">{esc(t['name'])}{label}</h2>
      </div>
      <p class="tree-meta">{esc(t.get('species', ''))} &middot; {esc(t.get('age_estimate', 'age unknown'))} &middot; {esc(loc.get('neighbourhood', ''))}{best_time_short(t)}</p>""")
        cards[-1] += f"""
      <p class="tree-story">{esc(t['story'])}</p>
      <p class="tree-more"><a href="{slug}/{tslug}">Read more and get directions &rarr;</a></p>
    </article>"""
        markers.append({"lat": loc["latitude"], "lng": loc["longitude"], "label": str(i),
                        "icon": species_icon(t), "name": t["name"], "id": t["id"],
                        "area": (loc.get("neighbourhood") or "").strip(),
                        "shot": bool(cphoto)})

    faq = city_data.get("faq", [])
    if not faq:
        ERRORS.append(f"{canonical}: FAQ block (3-4 real questions) is required by Contract C")
    faq_html = "".join(f"<dt>{esc(f['q'])}</dt><dd>{esc(f['a'])}</dd>" for f in faq)

    city_collections = [c for c in collections if any(e["city_slug"] == slug for e in c.get("entries", []))]
    coll = city_collections[0] if city_collections else None
    if coll:
        n = sum(1 for e in coll.get("entries", []) if e["city_slug"] == slug)
        phrase = "One of these trees" if n == 1 else f"{n} of these trees"
        verb = "appears" if n == 1 else "appear"
        coll_link_html = (
            f'<dt>More like this</dt><dd>{phrase} also {verb} in '
            f'<a href="collections/{coll["slug"]}">{esc(coll["title"])}</a>.</dd>'
        )
    else:
        coll_link_html = '<dt>More like this</dt><dd>Browse <a href="collections">themed collections</a> of remarkable trees.</dd>'
    others_html = " &middot; ".join(
        f'<a href="./{c["slug"]}">{esc(c["city"])}</a>'
        for c in other_cities
    )
    more_cities_html = (
        f'<dt>Ancient trees in more cities</dt><dd>{others_html}</dd>' if others_html else ""
    )

    # Species page pass (PRODUCT_TODO item 6): a city page links onward to a
    # species page when 3+ of its own trees share that species, the same
    # threshold that gates the species page's existence (Contract F).
    species_here = {}
    for t in trees:
        species_here.setdefault(species_common(t), 0)
        species_here[species_common(t)] += 1
    city_species_links = [
        (common, species_pages[common]) for common, n in species_here.items()
        if n >= 3 and common in species_pages
    ]
    species_links_html = (
        '<dt>Species on this list</dt><dd>' + " &middot; ".join(
            f'<a href="species/{sp_slug}">Every {esc(common.lower())} on the site</a>'
            for common, sp_slug in city_species_links
        ) + '</dd>'
        if city_species_links else ""
    )

    panel_foot = f"""
    <div class="panel-foot">
      <p class="subtle-suggest"><b>We are mapping every remarkable tree in the world.</b> Know one in {esc(city)} we missed, or spot a mistake here? <a href="{submit_link('tree')}">Tell us</a>.</p>
      <div class="take-with-you">
        <strong>Going there?</strong> <a href="{slug}.gpx" download>Download all {len(trees)} trees</a> as a map file and open it in Google Maps, Organic Maps or any hiking app. Works offline, no app needed.
      </div>
      <h2>Frequently asked</h2>
      <dl class="faq">
        {faq_html}
        <dt>More on the oldest tree</dt>
        <dd><a href="{slug}/oldest-tree">What is the oldest tree in {esc(city)}?</a> The full answer, with map and directions.</dd>
        {species_links_html}
        {coll_link_html}
        {more_cities_html}
      </dl>
      <p class="suggest">Know a tree that belongs on this list? <a href="{submit_link('tree')}">Send it in</a>. Suggestions feed curation; the list itself stays editorial.</p>
    </div>"""

    graph = site_graph() + [
        {
            "@type": "ItemList",
            "name": title,
            "itemListElement": [
                {
                    "@type": "ListItem", "position": i,
                    "name": t["name"],
                    "url": f"{BASE_URL}/{slug}/{tree_slugs[t['id']]}",
                    "item": {
                        "@type": "TouristAttraction",
                        "name": t["name"],
                        "description": t["story"][:200],
                        "geo": {
                            "@type": "GeoCoordinates",
                            "latitude": t["location"]["latitude"],
                            "longitude": t["location"]["longitude"],
                        },
                    },
                }
                for i, t in enumerate(trees, 1)
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [{
                "@type": "Question", "name": f["q"],
                "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
            } for f in faq],
        },
        breadcrumb_schema(crumb_items, canonical),
    ]
    head_extra = map_head() + "\n" + ld_script(graph)

    avg_lat = sum(m["lat"] for m in markers) / len(markers)
    avg_lng = sum(m["lng"] for m in markers) / len(markers)

    # The walks, worked out at build time so a phone never has to compute it.
    # Several per city where the trees allow it (Hidde, 2026-08-06: walks live
    # inside the city page, never as pages of their own).
    walks = plan_walks(markers)
    route = walks[0] if walks else None
    route_bar = ""
    if route:
        for w in walks:
            w["url"] = maps_route_url([(markers[i]["lat"], markers[i]["lng"])
                                       for i in w["order"]])
            # A real pedestrian route where one is cached, which also makes the
            # distance and the duration true rather than a straight line times
            # a detour guess.
            routed = walk_route_for(slug, [trees[i]["id"] for i in w["order"]])
            if routed:
                w["shape"] = routed["shape"]
                w["km"] = routed["km"]
                w["minutes"] = routed["minutes"]
            w["duration"] = human_duration(w["minutes"])
            w["label"] = (f"Walk {w['count']} of these trees"
                          if w["count"] < len(markers) else f"Walk all {w['count']} trees")
        chooser = ""
        if len(walks) > 1:
            # Every walk is a real button in the served HTML, so the choice is
            # visible without JavaScript and to a crawler.
            btns = "".join(
                # No chip starts active: the page opens on the whole city, so a
                # highlighted chip would promise a focus that is not applied.
                f'<button type="button" class="walk-pick" '
                f'data-walk="{i}" aria-pressed="false">'
                f'<span class="walk-pick-name">{esc(w["name"] or f"Walk {i + 1}")}</span>'
                f'<span class="walk-pick-meta">{w["count"]} trees &middot; {w["km"]} km</span>'
                f'</button>' for i, w in enumerate(walks))
            real = sum(1 for w in walks if not w.get("combined"))
            plural = "walks" if real > 1 else "walk"
            chooser = (f'<div class="walk-picker" role="group" '
                       f'aria-label="{real} {plural} in {esc(city)}">{btns}</div>')
        first = walks[0]
        name_bit = f'<span class="route-name">{esc(first["name"])}</span>' if first["name"] else ""
        route_bar = f"""
    <div class="walks" id="walk">{chooser}
      <div class="route-bar">
        <a class="route-go" id="route-go" href="{esc(first['url'])}" target="_blank" rel="noopener">
          {name_bit}<span id="route-label">{first['label']}</span>
          <span class="route-meta" id="route-meta">about {first['km']} km, {first['duration']} on foot</span>
        </a>
        <button type="button" class="route-gps" id="gps-btn" aria-pressed="false">Where am I</button>
      </div>
    </div>"""

    body = f"""
<div class="split">
  <aside class="panel">
    <div class="panel-head">
      {breadcrumb_html(crumb_items, rootpath)}
      <p class="eyebrow">{esc(country)}</p>
      <h1>Ancient Trees in <em>{esc(city)}</em></h1>
      <p class="lede">{esc(intro)}</p>
      <p class="passport" id="passport" hidden>
        <strong><span id="passport-count">0</span> of {len(trees)}</strong> visited in {esc(city)}
        <span class="passport-total" id="passport-total"></span>
        <button type="button" class="passport-save" id="passport-save">Save or move to another device</button>
      </p>
    </div>
    {''.join(cards)}
    {panel_foot}
  </aside>
  <div class="stage">
    <div id="map" class="map"></div>
    {route_bar}
  </div>
</div>
"""
    scripts = city_map_script(markers, (avg_lat, avg_lng), route, other_cities, walks)

    link_count = len(trees) + 1 + 1 + len(other_cities) + len(city_species_links)
    check_links(canonical, link_count, 12)

    page = render_page(title, description, canonical, body, head_extra, scripts,
                       rootpath="./", footer=False)
    pages.append((f"{slug}.html", page, canonical))
    return {"slug": slug, "city": city, "country": country, "count": len(trees),
            "markers": markers, "canonical": canonical}


# ---------------------------------------------------------- collection pages

def build_collection_page(coll, cities_by_slug, tree_slugs, published, pages, draft=False):
    slug = coll["slug"]
    canonical = f"{BASE_URL}/collections/{slug}"
    rootpath = "../"
    # The title tag targets the query, the H1 keeps the editorial line
    # (Hidde, 2026-08-01, blueprint v1.6). Falls back when no seo_title exists.
    title = fit_title([coll.get("seo_title", ""), coll["title"]], canonical)
    description = coll.get("meta_description", "")

    crumb_items = [("Home", BASE_URL), ("Collections", f"{BASE_URL}/collections"), (coll["title"], None)]

    grouped = {}
    for e in coll.get("entries", []):
        grouped.setdefault(e["city_slug"], []).append(e)

    sections = []
    entry_count = 0
    list_elements = []
    for cslug, entries in grouped.items():
        city_data = cities_by_slug[cslug]["data"]
        trees_by_id = {t["id"]: t for t in city_data["trees"]}
        rows = []
        for e in entries:
            t = trees_by_id[e["tree_id"]]
            tslug = tree_slugs[t["id"]]
            entry_count += 1
            list_elements.append({
                "@type": "ListItem", "position": entry_count,
                "name": t["name"], "url": f"{BASE_URL}/{cslug}/{tslug}",
            })
            ph = usable_photo(t)
            thumb = (f'<div class="entry-thumb"><img {img_srcset(ph["url"], [300, 600], "140px")} alt="{esc(t["name"])}" loading="lazy"></div>'
                     if ph else "")
            rows.append(f"""
      <div class="entry{' has-thumb' if ph else ''}">
        {thumb}
        <div class="entry-body">
          <h3><a href="../{cslug}/{tslug}">{esc(t['name'])}</a> <span class="tree-label">{esc(t.get('age_estimate', ''))}</span></h3>
          <p>{esc(e['note'])}</p>
        </div>
      </div>""")
        # The whole section leads to the city, not just the one tree shown
        # (Hidde, 2026-07-30): a collection entry should make you want to
        # go, and the city page with its map is where you decide that.
        sections.append(
            f'<h2><a class="coll-city" href="../{cslug}">{esc(city_data["city"])}</a></h2>'
            + "".join(rows)
            + f'<p class="coll-citycta"><a href="../{cslug}">See all {len(city_data["trees"])} trees in {esc(city_data["city"])} on the map &rarr;</a></p>')

    city_links = " &middot; ".join(
        f'<a href="../{p["slug"]}">{esc(p["city"])}</a>' for p in published
    )

    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>{esc(coll['title'])}</h1>
  <div class="prose-block"><p>{esc(coll['intro'])}</p></div>
  {''.join(sections)}
  <p class="suggest">Explore by city: {city_links}</p>
</main>
"""

    graph = site_graph() + [
        {"@type": "ItemList", "name": coll["title"], "itemListElement": list_elements},
        breadcrumb_schema(crumb_items, canonical),
    ]
    head_extra = ld_script(graph)
    if draft:
        # Contract D: a draft is never linked publicly until Hidde approves.
        # Built anyway so there is a stable URL to review; kept out of pages
        # (and therefore the sitemap and every internal nav) until then, same
        # pattern as the account prototype below.
        head_extra += '\n<meta name="robots" content="noindex, nofollow">'

    check_links(canonical, entry_count + len(published), entry_count + min(3, len(published)))

    page = render_page(title, description, canonical, body, head_extra, "", rootpath)
    if draft:
        return (slug, page)
    pages.append((f"collections/{slug}.html", page, canonical))
    return canonical


def build_city_gpx(entry, trees, pages):
    """One waypoint per tree, loadable in any maps or hiking app.

    This is what turns the page into something you can carry: the whole city's
    trees on your phone, working offline, no app install.
    """
    city = entry["data"]["city"]
    slug = entry["slug"]
    pts = []
    for t in trees:
        loc = t["location"]
        desc = f"{t.get('species', '')}. {t.get('age_estimate', '')}. {t.get('access', '')}"
        pts.append(
            f'  <wpt lat="{loc["latitude"]}" lon="{loc["longitude"]}">\n'
            f'    <name>{esc(t["name"])}</name>\n'
            f'    <desc>{esc(desc.strip())}</desc>\n'
            f'  </wpt>'
        )
    gpx = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<gpx version="1.1" creator="Ancient Trees" xmlns="http://www.topografix.com/GPX/1/1">\n'
        f'  <metadata><name>Ancient Trees in {esc(city)}</name>'
        f'<link href="{BASE_URL}/{slug}"><text>ancienttrees.app</text></link></metadata>\n'
        + "\n".join(pts) + "\n</gpx>\n"
    )
    pages.append((f"{slug}.gpx", gpx, None))


def build_species_page(intro_data, members, tree_slugs, published, pages):
    """members: list of (city_entry, tree) for this species, already gated to 3+."""
    slug = intro_data["slug"]
    common = intro_data["common_name"]
    canonical = f"{BASE_URL}/species/{slug}"
    rootpath = "../"
    title = fit_title([
        intro_data.get("title", ""),
        f"{common}: Ancient {common}s You Can Visit",
        f"Ancient {common} Trees",
        common,
    ], canonical)
    description = intro_data.get("meta_description", "")

    crumb_items = [("Home", BASE_URL), ("Species", f"{BASE_URL}/species"), (common, None)]

    # group members by city, in published-city order
    order = {p["slug"]: i for i, p in enumerate(published)}
    by_city = {}
    for entry, t in members:
        by_city.setdefault(entry["slug"], (entry, []))[1].append(t)
    sections = []
    list_elements = []
    n = 0
    for cslug in sorted(by_city, key=lambda s: order.get(s, 99)):
        entry, trees = by_city[cslug]
        trees = sorted(trees, key=lambda t: -(t.get("age_max") or 0))
        rows = []
        for t in trees:
            tslug = tree_slugs[t["id"]]
            loc = t["location"]
            n += 1
            list_elements.append({
                "@type": "ListItem", "position": n,
                "name": t["name"], "url": f"{BASE_URL}/{cslug}/{tslug}",
            })
            ph = usable_photo(t)
            thumb = (f'<div class="entry-thumb"><img {img_srcset(ph["url"], [300, 600], "140px")} alt="{esc(t["name"])}" loading="lazy"></div>'
                     if ph else "")
            rows.append(f"""
      <div class="entry{' has-thumb' if ph else ''}">
        {thumb}
        <div class="entry-body">
          <h3><a href="../{cslug}/{tslug}">{esc(t['name'])}</a> <span class="tree-label">{esc(t.get('age_estimate',''))}</span></h3>
          <p>{esc(loc.get('neighbourhood',''))}. {esc(t['story'].split('. ')[0])}.</p>
        </div>
      </div>""")
        sections.append(f'<h2><a class="sp-citylink" href="../{cslug}">{esc(entry["data"]["city"])}</a></h2>{"".join(rows)}')

    city_links = " &middot; ".join(
        f'<a href="../{p["slug"]}">{esc(p["city"])}</a>' for p in published
    )

    # The answer-first line borrows the intro's first sentence, so the body
    # continues from the second one; printing the full intro repeated it.
    first_sentence = intro_data["intro"].split(". ")[0] + "."
    intro_rest = intro_data["intro"][len(first_sentence):].lstrip()
    body_intro = f'<div class="prose-block"><p>{esc(intro_rest)}</p></div>' if intro_rest else ""
    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>{esc(common)}</h1>
  <p class="answer-first">{esc(first_sentence)} This page maps every {esc(common.lower())} on the site, {n} so far across {len(by_city)} cit{'y' if len(by_city)==1 else 'ies'}.</p>
  {body_intro}
  {''.join(sections)}
  <p class="suggest">Explore by city: {city_links} &middot; or browse <a href="../species">all species</a>.</p>
</main>
"""
    graph = site_graph() + [
        {"@type": "ItemList", "name": f"{common} trees", "itemListElement": list_elements},
        breadcrumb_schema(crumb_items, canonical),
    ]
    head_extra = ld_script(graph)
    check_links(canonical, n + len(published) + 1, n + min(2, len(published)) + 1)
    page = render_page(title, description, canonical, body, head_extra, "", rootpath)
    pages.append((f"species/{slug}.html", page, canonical))
    face = None
    for _entry, _t in members:
        _p = usable_photo(_t)
        if _p:
            face = thumb_url(_p["url"], 400)
            break
    return {"slug": slug, "common": common, "scientific": intro_data.get("scientific_name", ""),
            "count": n, "cities": len(by_city), "face": face}


def browse_card(href, name, sub, face):
    """The one card used by every browse index (cities, species, collections):
    photo, name, one honest sub-line. Same component, so the facets read as
    siblings instead of three different pages."""
    if face:
        ph = f'<span class="exc-ph"><img src="{esc(face)}" alt="" loading="lazy"></span>'
    else:
        ph = ('<span class="exc-ph ctry-noph" aria-hidden="true">'
              '<svg viewBox="0 0 68 64" fill="none"><ellipse cx="34" cy="24" rx="24" ry="16" fill="currentColor"/>'
              '<circle cx="20" cy="23" r="11" fill="currentColor"/><circle cx="48" cy="23" r="11" fill="currentColor"/>'
              '<circle cx="34" cy="12" r="11" fill="currentColor"/>'
              '<path d="M31 62 h5.6 l-1.2-16 h-3.2z" fill="currentColor"/></svg></span>')
    return (f'<a class="exc-card" href="{href}">{ph}'
            f'<span class="exc-body"><b>{esc(name)}</b><span>{sub}</span></span></a>')


def collection_face(coll, cities_by_slug):
    """First entry in the collection that has a usable photo."""
    for e in coll.get("entries", []):
        entry = cities_by_slug.get(e["city_slug"])
        if not entry or not entry.get("data"):
            continue
        for t in entry["data"]["trees"]:
            if t["id"] == e.get("tree_id"):
                p = usable_photo(t)
                if p:
                    return thumb_url(p["url"], 400)
    return None


def load_park_intros():
    """Hand-written park intros, the publish gate a park page shares with a
    species page: no intro, no page, so nothing ships as templated filler (P3)."""
    d = DATA / "parks"
    if not d.exists():
        return {}
    out = {}
    for f in sorted(d.glob("*.json")):
        j = json.loads(f.read_text())
        out[(j["city_slug"], j["park"])] = j
    return out


def build_park_page(intro, entry, trees, tree_slugs, published, pages):
    """One park, its trees, and what makes standing in it worth an afternoon."""
    slug = intro["slug"]
    name = intro.get("name") or intro["park"]
    city = entry["data"]["city"]
    cslug = entry["slug"]
    canonical = f"{BASE_URL}/parks/{slug}"
    title = fit_title([intro.get("title", ""),
                       f"Ancient Trees in {name}, {city}",
                       f"{name}: Ancient Trees"], canonical)
    description = intro.get("meta_description", "")
    crumb_items = [("Home", BASE_URL), ("Parks", f"{BASE_URL}/parks"), (name, None)]

    trees = sorted(trees, key=lambda t: -(t.get("age_max") or 0))
    rows, list_elements = [], []
    for i, t in enumerate(trees, 1):
        tslug = tree_slugs[t["id"]]
        list_elements.append({"@type": "ListItem", "position": i,
                              "name": t["name"], "url": f"{BASE_URL}/{cslug}/{tslug}"})
        ph = usable_photo(t)
        thumb = (f'<div class="entry-thumb"><img {img_srcset(ph["url"], [300, 600], "140px")} '
                 f'alt="{esc(t["name"])}" loading="lazy"></div>' if ph else "")
        rows.append(f"""
      <div class="entry{' has-thumb' if ph else ''}">
        {thumb}
        <div class="entry-body">
          <h3><a href="../{cslug}/{tslug}">{esc(t['name'])}</a> <span class="tree-label">{esc(t.get('age_estimate',''))}</span></h3>
          <p>{esc(t['species'])}. {esc(t['story'].split('. ')[0])}.</p>
        </div>
      </div>""")

    first = intro["intro"].split(". ")[0] + "."
    rest = intro["intro"][len(first):].lstrip()
    rest_html = f'<div class="prose-block"><p>{esc(rest)}</p></div>' if rest else ""
    other = [q for q in published if q["slug"] != cslug][:6]
    other_links = " &middot; ".join(f'<a href="../{q["slug"]}">{esc(q["city"])}</a>' for q in other)
    # The reciprocity OUTREACH.md promises has to actually exist on the page:
    # opening hours, tickets and closures are theirs to state, not ours.
    official_line = ""
    if intro.get("official_url"):
        official_line = (
            f'<p class="suggest">Opening times and visitor information: '
            f'<a href="{esc(intro["official_url"])}" rel="noopener">'
            f'{esc(intro.get("official_name") or "the official site")}</a>.</p>')
    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, "../")}
  <h1>Ancient Trees in {esc(name)}</h1>
  <p class="lede">{esc(first)}</p>
  {rest_html}
  <p class="suggest">All {len(trees)} stand in <a href="../{cslug}">{esc(city)}</a>, which maps {len(entry['data']['trees'])} remarkable trees in total.</p>
  {"".join(rows)}
  {official_line}
  <p class="suggest">More parks worth the walk: <a href="../parks">every park we map</a>. Or explore by city: {other_links}</p>
</main>
"""
    graph = site_graph() + [breadcrumb_schema(crumb_items, canonical),
                             {"@type": "ItemList", "name": f"Ancient trees in {name}",
                             "itemListElement": list_elements}]
    page = render_page(title, description, canonical, body, ld_script(graph),
                       "", rootpath="../")
    check_links(canonical, len(trees) + 2 + len(other), 8)
    pages.append((f"parks/{slug}.html", page, canonical))
    return {"slug": slug, "name": name, "city": city, "city_slug": cslug,
            "count": len(trees),
            "face": next((thumb_url(usable_photo(t)["url"], 400)
                          for t in trees if usable_photo(t)), None)}


def build_parks_index(cards, unbuilt, published, pages):
    canonical = f"{BASE_URL}/parks"
    title = fit_title(["Ancient Trees by Park and Garden",
                       "The Parks and Gardens With the Best Trees"], canonical)
    description = ("The parks and botanical gardens where several remarkable old trees stand "
                   "together, from Madrid's Retiro to the oldest botanical garden in the world.")
    crumb_items = [("Home", BASE_URL), ("Parks", None)]
    entries = '<div class="cindex-grid">%s</div>' % "".join(
        browse_card(f"parks/{c['slug']}", c["name"],
                    f"{c['count']} trees &middot; {c['city']}", c.get("face"))
        for c in cards)
    # No near-miss list. Hidde, 2026-08-08: "that section doesn't add much, I
    # would just delete that and automatically add more if we find more." He is
    # right that a wall of parks holding three or four trees, each linked to a
    # city page rather than to itself, gave a reader nothing they came for. The
    # page grows on its own as parks reach the bar.
    more = ""
    city_links = " &middot; ".join(f'<a href="{p["slug"]}">{esc(p["city"])}</a>' for p in published[:12])
    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, "./")}
  <h1>Ancient Trees by Park and Garden</h1>
  <div class="prose-block"><p>Some parks are worth an afternoon on their own, because several remarkable old trees stand within a few minutes of each other. A botanical garden founded in 1545 and still on its original ground. A royal park that stayed private for two hundred years, which is why its trees are old. An English garden planted for a queen with species nobody in the country had grown before. Each of these holds enough to fill a walk.</p></div>
  {entries}
  {more}
  <p class="suggest">Or explore by city: {city_links}</p>
</main>
"""
    graph = site_graph() + [{"@type": "ItemList", "name": "Parks and gardens",
                             "itemListElement": [
                                 {"@type": "ListItem", "position": i, "name": c["name"],
                                  "url": f"{BASE_URL}/parks/{c['slug']}"}
                                 for i, c in enumerate(cards, 1)]}]
    page = render_page(title, description, canonical, body, ld_script(graph), "", rootpath="./")
    check_links(canonical, len(cards) + len(city_links.split("&middot;")), 8)
    pages.append(("parks.html", page, canonical))


def build_species_index(species_cards, published, pages):
    canonical = f"{BASE_URL}/species"
    rootpath = "./"
    title = fit_title(["Ancient Trees by Species", "Browse Ancient Trees by Species"], canonical)
    description = ("Browse the mapped trees by species: the London plane that lines half of "
                  "Europe's streets, the wingnut Amsterdam went to court over, and more.")
    crumb_items = [("Home", BASE_URL), ("Species", None)]

    # Browse facets get the same photo-card grid as /cities: a list of names is
    # a database view, and a species is chosen by the look of the tree.
    entries = '<div class="cindex-grid">%s</div>' % "".join(
        browse_card(f"species/{c['slug']}", c["common"],
                    f"{c['count']} trees &middot; {c['cities']} cities", c.get("face"))
        for c in species_cards)
    city_links = " &middot; ".join(
        f'<a href="{p["slug"]}">{esc(p["city"])}</a>' for p in published
    )
    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>Ancient Trees by Species</h1>
  <div class="prose-block"><p>Cities group these trees by place; collections group them by theme. This page groups them by what they actually are. A London plane in Barcelona and a London plane in Warsaw are the same tree living two different lives, and reading them side by side tells you something a city page cannot: how long the species lives, what it does in autumn, and which cities planted it when.</p></div>
  {entries}
  <p class="suggest">Or explore by city: {city_links}</p>
</main>
"""
    graph = site_graph() + [
        {"@type": "ItemList", "name": "Tree species",
         "itemListElement": [
             {"@type": "ListItem", "position": i, "name": c["common"],
              "url": f"{BASE_URL}/species/{c['slug']}"}
             for i, c in enumerate(species_cards, 1)]},
        breadcrumb_schema(crumb_items, canonical),
    ]
    head_extra = ld_script(graph)
    page = render_page(title, description, canonical, body, head_extra, "", rootpath)
    pages.append(("species.html", page, canonical))


def country_map_script(cities):
    """The country map: one green dot per mapped city, click goes to its page.
    Deliberately the simplest map on the site (no clustering, no season layer):
    at country zoom the job is orientation, not detail."""
    def centre(c):
        ms = c["markers"]
        return [sum(m["lng"] for m in ms) / len(ms), sum(m["lat"] for m in ms) / len(ms)]
    data = json.dumps({
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": centre(c)},
            "properties": {"slug": c["slug"], "city": c["city"], "n": str(c["count"])},
        } for c in cities],
    })
    return f"""
<script src="{MAPLIBRE_JS}"></script>
<script>
var CITIES = {data};
var map = new maplibregl.Map({{
  container: 'map', style: '{MAP_STYLE}',
  center: [0, 0], zoom: 3, renderWorldCopies: false,
  attributionControl: {{ compact: true }}
}});
map.addControl(new maplibregl.NavigationControl());
var b = new maplibregl.LngLatBounds();
CITIES.features.forEach(function(f) {{ b.extend(f.geometry.coordinates); }});
// Fit on load AND on resize until the visitor takes over: fitting against a
// container that has not reached its final size lands the country at half
// the right zoom, which is what it did on the first build.
var touched = false;
function fit() {{ if (!touched) {{ map.fitBounds(b, {{ padding: 48, maxZoom: 9, duration: 0 }}); }} }}
map.on('dragstart', function() {{ touched = true; }});
map.on('zoomstart', function(e) {{ if (e.originalEvent) {{ touched = true; }} }});
new ResizeObserver(function() {{ map.resize(); fit(); }}).observe(document.getElementById('map'));
map.on('load', function() {{
  fit();
  map.addSource('cities', {{type: 'geojson', data: CITIES}});
  map.addLayer({{id: 'city-dot', type: 'circle', source: 'cities',
    paint: {{'circle-color': '#4A6B2A', 'circle-opacity': 0.92, 'circle-radius': 15,
            'circle-stroke-width': 2, 'circle-stroke-color': '#F6F2E9'}}}});
  map.addLayer({{id: 'city-n', type: 'symbol', source: 'cities',
    layout: {{'text-field': ['get', 'n'], 'text-font': ['Noto Sans Regular'],
             'text-size': 12, 'text-allow-overlap': true}},
    paint: {{'text-color': '#F6F2E9'}}}});
  map.addLayer({{id: 'city-name', type: 'symbol', source: 'cities',
    layout: {{'text-field': ['get', 'city'], 'text-font': ['Noto Sans Regular'],
             'text-size': 12, 'text-offset': [0, 1.6], 'text-anchor': 'top'}},
    paint: {{'text-color': '#26301E', 'text-halo-color': '#F6F2E9', 'text-halo-width': 1.4}}}});
  map.on('click', 'city-dot', function(e) {{
    window.location.href = '/' + e.features[0].properties.slug;
  }});
  map.on('mouseenter', 'city-dot', function() {{ map.getCanvas().style.cursor = 'pointer'; }});
  map.on('mouseleave', 'city-dot', function() {{ map.getCanvas().style.cursor = ''; }});
}});
</script>
"""


def build_country_page(intro_data, country_cities, entries_by_slug, tree_slugs,
                       published, collections, pages):
    """Contract G. The pyramid's middle tier: tree -> city -> country.

    Form follows the country-page convention of AllTrails, Komoot and Atlas
    Obscura (region map, then a ranked list of destinations as photo cards,
    then one highlighted entry), in the ranked-list shape Hidde picked on
    2026-08-01. Publish gate: 3+ published cities AND a hand-written intro."""
    slug = intro_data["slug"]
    country = intro_data["country"]
    disp = country_name(intro_data)
    canonical = f"{BASE_URL}/{slug}"
    rootpath = "./"

    total = sum(c["count"] for c in country_cities)
    title = fit_title([
        f"Ancient Trees in {disp}: {len(country_cities)} Cities to Explore",
        f"Ancient Trees in {disp}: {len(country_cities)} Cities",
        intro_data.get("title", ""),
        f"Ancient Trees in {country}",
    ], canonical)
    description = intro_data.get("meta_description", "")

    crumb_items = [("Home", BASE_URL), (country, None)]

    # Cities ranked by how much of each is mapped: honest and self-explaining,
    # unlike a taste ranking nobody can check.
    ranked = sorted(country_cities, key=lambda c: (-c["count"], c["city"]))

    # The oldest tree in the country, by the most defensible reading: highest
    # lower bound first, so a wide guess never outranks a documented age.
    oldest, oldest_city = None, None
    for c in country_cities:
        entry = entries_by_slug[c["slug"]]
        for t in entry["data"]["trees"]:
            if not tree_is_renderable(t):
                continue
            key = (t.get("age_min") or 0, t.get("age_max") or 0)
            if oldest is None or key > (oldest.get("age_min") or 0, oldest.get("age_max") or 0):
                oldest, oldest_city = t, c

    rows = []
    for i, c in enumerate(ranked, 1):
        entry = entries_by_slug[c["slug"]]
        face = city_face(entry, 300)
        # No photo yet is an honest state, not a broken one: the placeholder
        # carries the mark rather than sitting there as an empty grey hole.
        ph = (f'<span class="ctry-ph"><img src="{esc(face)}" alt="" loading="lazy"></span>'
              if face else '<span class="ctry-ph ctry-noph" aria-hidden="true">'
                           '<svg viewBox="0 0 68 64" fill="none"><ellipse cx="34" cy="24" rx="24" ry="16" fill="currentColor"/>'
                           '<circle cx="20" cy="23" r="11" fill="currentColor"/><circle cx="48" cy="23" r="11" fill="currentColor"/>'
                           '<circle cx="34" cy="12" r="11" fill="currentColor"/>'
                           '<path d="M31 62 h5.6 l-1.2-16 h-3.2z" fill="currentColor"/></svg></span>')
        city_oldest = max((t for t in entry["data"]["trees"] if tree_is_renderable(t)),
                          key=lambda t: (t.get("age_min") or 0, t.get("age_max") or 0), default=None)
        sub = f'{c["count"]} trees'
        if city_oldest:
            sub += f' &middot; oldest {esc(city_oldest.get("age_estimate", ""))}'
        rows.append(
            f'<a class="ctry-row" href="{c["slug"]}">'
            f'<span class="ctry-rank">{i}</span>{ph}'
            f'<span class="ctry-body"><b>{esc(c["city"])}</b><span>{sub}</span></span>'
            f'<span class="ctry-chev" aria-hidden="true">&rsaquo;</span></a>')

    oldest_block = ""
    if oldest is not None:
        tslug = tree_slugs[oldest["id"]]
        ph = usable_photo(oldest)
        thumb = (f'<div class="entry-thumb"><img {img_srcset(ph["url"], [300, 600], "140px")}'
                 f' alt="{esc(oldest["name"])}" loading="lazy"></div>' if ph else "")
        oldest_block = f"""
  <h2>The oldest tree mapped in {esc(disp)}</h2>
  <div class="entry{' has-thumb' if ph else ''}">
    {thumb}
    <div class="entry-body">
      <h3><a href="{oldest_city['slug']}/{tslug}">{esc(oldest['name'])}</a> <span class="tree-label">{esc(oldest.get('age_estimate',''))}</span></h3>
      <p>{esc(oldest['location'].get('neighbourhood',''))}, {esc(oldest_city['city'])}. {esc(oldest['story'].split('. ')[0])}.</p>
    </div>
  </div>"""

    country_slugs = {c["slug"] for c in country_cities}
    rel_colls = [c for c in collections
                 if any(e["city_slug"] in country_slugs for e in c.get("entries", []))]
    coll_line = ""
    if rel_colls:
        links = " &middot; ".join(
            f'<a href="collections/{c["slug"]}">{esc(c["title"])}</a>' for c in rel_colls[:3])
        coll_line = f'Trees from {esc(disp)} also appear in {links}. '

    register_note = ""
    if intro_data.get("register_note"):
        register_note = f'<p class="notice">{esc(intro_data["register_note"])}</p>'

    first_sentence = intro_data["intro"].split(". ")[0] + "."
    intro_rest = intro_data["intro"][len(first_sentence):].lstrip()
    oldest_line = ""
    if oldest is not None:
        oldest_line = (f' The oldest of them is {esc(oldest["name"])} in {esc(oldest_city["city"])}, '
                       f'at {esc(oldest.get("age_estimate", "an uncertain age"))}.')

    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>Ancient trees in {esc(disp)}</h1>
  <p class="answer-first">{esc(first_sentence)} This page maps {total} remarkable trees across {len(country_cities)} cities in {esc(disp)}, each one researched and verified.{oldest_line}</p>
  <div class="prose-block"><p>{esc(intro_rest)}</p></div>
  <div class="map-embed"><div id="map" class="map"></div></div>
  <h2>Every mapped city in {esc(disp)}</h2>
  <div class="ctry-list">{"".join(rows)}</div>
  {oldest_block}
  {register_note}
  <p class="suggest">{coll_line}See <a href="cities">every city on the map</a>, or <a href="explore">open the map</a> to find what is near you.</p>
</main>
"""
    list_elements = [
        {"@type": "ListItem", "position": i, "name": c["city"],
         "url": f"{BASE_URL}/{c['slug']}"} for i, c in enumerate(ranked, 1)]
    graph = site_graph() + [
        {"@type": "CollectionPage", "name": f"Ancient trees in {disp}",
         "description": description, "url": canonical},
        {"@type": "ItemList", "name": f"Cities in {disp}", "itemListElement": list_elements},
        breadcrumb_schema(crumb_items, canonical),
    ]
    head_extra = map_head() + "\n" + ld_script(graph)
    check_links(canonical, len(ranked) + 2, len(ranked) + 2)
    page = render_page(title, description, canonical, body, head_extra,
                       country_map_script(country_cities), rootpath)
    pages.append((f"{slug}.html", page, canonical))
    face = None
    for c in ranked:
        f = city_face(entries_by_slug[c["slug"]], 400)
        if f:
            face = f
            break
    return {"slug": slug, "display": country_name(intro_data, capital=True),
            "cities": len(country_cities), "trees": total, "face": face}


def build_countries_index(country_cards, published, pages):
    """The missing hop: country pages existed but nothing linked to them, so
    they were orphans (Hidde, 2026-08-04: "I'm missing the whole country
    view"). This is the page the Explore menu now points at."""
    canonical = f"{BASE_URL}/countries"
    rootpath = "./"
    title = fit_title(["Ancient Trees by Country", "Browse Ancient Trees by Country"], canonical)
    description = ("Every country on the map, with the cities and trees mapped in each: "
                   "Japan's shrine camphors, Spain's imported giants, Portugal's register.")
    crumb_items = [("Home", BASE_URL), ("Countries", None)]
    cards = "".join(
        browse_card(c["slug"], c["display"],
                    f'{c["cities"]} cities &middot; {c["trees"]} trees', c.get("face"))
        for c in country_cards)
    total_c = sum(c["cities"] for c in country_cards)
    total_t = sum(c["trees"] for c in country_cards)
    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>Ancient trees by country</h1>
  <p class="answer-first">{total_c} cities across {len(country_cards)} countries, {total_t} remarkable trees between them. Every country plants differently and protects differently, and it shows in what survived. Or go straight to <a href="cities">the city list</a>.</p>
  <div class="cindex-grid">{cards}</div>
</main>
"""
    graph = site_graph() + [
        {"@type": "ItemList", "name": "Countries",
         "itemListElement": [{"@type": "ListItem", "position": i, "name": c["display"],
                              "url": f"{BASE_URL}/{c['slug']}"}
                             for i, c in enumerate(country_cards, 1)]},
        breadcrumb_schema(crumb_items, canonical)]
    check_links(canonical, len(country_cards) + 1, 2)
    page = render_page(title, description, canonical, body, ld_script(graph), "", rootpath)
    pages.append(("countries.html", page, canonical))


def build_cities_index(published, pages, faces=None):
    """Every mapped city, grouped by country, at /cities.

    Built 2026-07-30 when the by-country block left the homepage (Hidde:
    "all 37 cities by country makes absolutely no sense" there). It is the
    right content in the wrong place: a directory page wants it, a living
    room does not. Keeps the full list crawlable in one hop from the nav."""
    canonical = f"{BASE_URL}/cities"
    rootpath = "./"
    title = fit_title(["Every City We Have Mapped", "Ancient Trees by City"], canonical)
    description = ("Every city on the map, by country: the remarkable old trees of each, "
                   "verified, with their stories and exact spots.")
    crumb_items = [("Home", BASE_URL), ("Cities", None)]

    by_country = {}
    for p in published:
        by_country.setdefault(p["country"], []).append(p)
    def _card(p):
        face = (faces or {}).get(p["slug"])
        ph = (f'<span class="exc-ph"><img src="{esc(face)}" alt="" loading="lazy"></span>'
              if face else '<span class="exc-ph exc-noph"></span>')
        return (f'<a class="exc-card" href="{p["slug"]}">{ph}'
                f'<span class="exc-body"><b>{esc(p["city"])}</b>'
                f'<span>{p["count"]} trees</span></span></a>')
    groups = "".join(
        '<h2 class="cindex-country">%s</h2><div class="cindex-grid">%s</div>' % (
            esc(country),
            "".join(_card(p) for p in sorted(cities, key=lambda x: x["city"])))
        for country, cities in sorted(by_country.items()))
    total = sum(p["count"] for p in published)
    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>Every city we have mapped</h1>
  <p class="answer-first">{len(published)} cities, {total} trees, each one researched and verified. Pick a city for its trees, or open <a href="explore">the map</a> to see what is near you.</p>
  {groups}
</main>
"""
    graph = site_graph() + [
        {"@type": "ItemList", "name": "Cities",
         "itemListElement": [
             {"@type": "ListItem", "position": i, "name": p["city"],
              "url": f"{BASE_URL}/{p['slug']}"}
             for i, p in enumerate(published, 1)]},
        breadcrumb_schema(crumb_items, canonical),
    ]
    check_links(canonical, len(published) + 2, 4)
    page = render_page(title, description, canonical, body, ld_script(graph), "", rootpath)
    pages.append(("cities.html", page, canonical))


def build_collections_index(collections, published, pages, cities_by_slug=None):
    """Overview of all collections at /collections."""
    cities_by_slug = cities_by_slug or {}
    canonical = f"{BASE_URL}/collections"
    rootpath = "./"
    title = fit_title(["Collections: Remarkable Trees by Theme"], canonical)
    description = ("Hand-curated lists that cut across cities: the oldest, the strangest, "
                   "the ones worth a detour. Every entry links to a verified tree.")

    crumb_items = [("Home", BASE_URL), ("Collections", None)]

    entries = []
    for c in collections:
        n_cities = len({e["city_slug"] for e in c.get("entries", [])})
        entries.append(browse_card(
            f"collections/{c['slug']}", c["title"],
            f"{len(c.get('entries', []))} trees &middot; {n_cities} cities",
            collection_face(c, cities_by_slug)))

    city_links = " &middot; ".join(
        f'<a href="{p["slug"]}">{esc(p["city"])}</a>' for p in published
    )

    entries_html = ('<div class="cindex-grid">%s</div>' % "".join(entries)) if entries else (
        '<div class="prose-block"><p>The first collections are drafted and being reviewed. '
        "None are public yet; check back as the map grows.</p></div>"
    )

    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>Collections</h1>
  <div class="prose-block"><p>Cities organise these trees by place. Collections organise them by what makes them worth the trip: age, strangeness, the stories they carry. Each one is hand-curated, and every entry links to a verified tree with its own map and directions. More collections are added as the map grows.</p></div>
  {entries_html}
  <p class="suggest">Explore by city instead: {city_links}</p>
</main>
"""
    graph = site_graph() + [
        {
            "@type": "ItemList",
            "name": "Collections",
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": c["title"],
                 "url": f"{BASE_URL}/collections/{c['slug']}"}
                for i, c in enumerate(collections, 1)
            ],
        },
        breadcrumb_schema(crumb_items, canonical),
    ]
    head_extra = ld_script(graph)
    page = render_page(title, description, canonical, body, head_extra, "", rootpath)
    pages.append(("collections.html", page, canonical))


def build_privacy_page(pages):
    """The privacy page, text approved by Hidde 2026-07-28 ("prima dit").
    Boring and factual on his instruction: no forever-promises, no personal
    name or location, no contact address (his explicit choice, the formal
    thinness of which is recorded in CLAUDE.md); deletion is self-service."""
    canonical = f"{BASE_URL}/privacy"
    body = f"""
<main class="content-page">
  <h1>Privacy</h1>
  <div class="prose-block">
    <p>Ancient Trees is a small independent project. This page describes what data the site handles.</p>
    <h2>Browsing</h2>
    <p>Every page works without an account. The site uses a cookieless visit counter (Cloudflare Web Analytics) that records aggregate page views only; it sets no cookies and cannot identify you. Map tiles load from OpenFreeMap and photos from Wikimedia Commons; those requests reach their servers the way any image on the web does.</p>
    <h2>With an account (once sign-in opens)</h2>
    <p>Signing in stores two things: your email address and your tree collection. The address is used for sign-in links and account service, nothing else. This data is stored with Supabase, on servers in the EU (Frankfurt).</p>
    <p>The site also counts, anonymously, which buttons get used (for example how often a directions button is clicked). These counts contain no names, no addresses, no identifiers and no cookies; they cannot be traced to anyone.</p>
    <p>Two forms store what you type into them, in the same EU database: the app waitlist keeps your email address, used to email you when the app is ready; a tree suggestion keeps what you wrote, including the name you optionally leave for credit. Want either removed? Use the contact address below.</p>
    <h2>Contact</h2>
    <p>Questions about any of this, or want something removed? <a href="contribute?kind=privacy">Send a privacy request</a> and say what you want removed. It reaches the people who run this site, and nothing else is needed from you.</p>

    <h2>Deleting</h2>
    <p>Your account page has a delete option. It removes your email address and your collection.</p>
    <h2>Changes</h2>
    <p>When this page changes, the date below changes with it.</p>
    <p><em>Last updated: 28 July 2026</em></p>
  </div>
</main>
"""
    page = render_page("Privacy", "What data Ancient Trees handles.",
                       canonical, body, rootpath="./")
    pages.append(("privacy.html", page, canonical))



APPLAND_BODY = """
<div class="appland">
  <!-- Taylor Cole, Unsplash License (no on-page credit required; recorded here
       per hard rule 4). Replaced the Greenwich chestnut (CC BY-SA) on Hidde's
       2026-07-29 no-visible-credit instruction: BY-SA requires the credit, the
       Unsplash License does not, so the photo changed instead of the licence
       being broken. -->
  <img class="appland-bg" APPLAND_SRCSET alt="">
  <div class="appland-card">
    <div class="appland-left">
      <span class="chip gold">Coming soon</span>
      <h1>Every ancient tree, in your pocket</h1>
      <p class="appland-sub">Open it wherever you happen to be and it finds the remarkable old trees within walking distance, strings the good ones into one afternoon, and tells you what you are standing in front of when you get there. Every tree you visit is one you keep.</p>
      <form class="waitlist" id="waitlist">
        <input type="email" id="wl-email" placeholder="you@example.com" aria-label="Your email address" required>
        <button type="submit" class="appland-cta">Tell me first</button>
      </form>
      <p class="waitlist-note" id="wl-note">Leave your email and you are on the list we write to the day it opens. One email. Nothing else.</p>
    </div>
    <div class="appland-right">
      <h2>What you will be able to do</h2>
      <div class="appland-feat"><span class="feat-tile"><svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="22" r="14" fill="none" stroke="#4A6B2A" stroke-width="3"/><circle cx="24" cy="22" r="4" fill="#D9A13F"/><path d="M24 4 v6 M24 34 v6 M6 22 h6 M36 22 h6" stroke="#4A6B2A" stroke-width="2.6" stroke-linecap="round"/></svg></span><div><h3>Find the ones near you</h3><p>It opens on where you are and shows the remarkable old trees around you, closest first, with the walk to each.</p></div></div>
      <div class="appland-feat"><span class="feat-tile"><svg viewBox="0 0 48 48" aria-hidden="true"><ellipse cx="24" cy="19" rx="12" ry="10" fill="#3A5222"/><circle cx="17" cy="18" r="7" fill="#4A6B2A"/><circle cx="31" cy="18" r="7" fill="#4A6B2A"/><circle cx="24" cy="11" r="7" fill="#5B7F35"/><path d="M22.9 40h2.4l-.6-13h-1.2z" fill="#6B4F33"/><circle cx="36" cy="34" r="8" fill="#D9A13F"/><path d="M32.5 34 l2.5 2.5 5 -5" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span><div><h3>Collect the ones you visit</h3><p>Stand in front of a tree, tick it off, and watch a collection build itself city by city and country by country.</p></div></div>
      <div class="appland-feat"><span class="feat-tile"><svg viewBox="0 0 48 48" aria-hidden="true"><path d="M12 30 a10 10 0 0 1 2 -19 a12 12 0 0 1 22 3 a8 8 0 0 1 0 16 z" fill="#ECEDE2" stroke="#4A6B2A" stroke-width="2.5"/><path d="M18 36 l-3 5 M26 36 l-3 5 M34 36 l-3 5" stroke="#4A6B2A" stroke-width="2.6" stroke-linecap="round"/></svg></span><div><h3>Keep going without a signal</h3><p>Save a city before you set off, so the map still works in the middle of a park with one bar.</p></div></div>
      <div class="appland-feat"><span class="feat-tile"><svg viewBox="0 0 48 48" aria-hidden="true"><ellipse cx="20" cy="18" rx="10" ry="8" fill="#D9A13F"/><circle cx="15" cy="16" r="4.5" fill="#E8BC63"/><path d="M19 36h2.4l-.6-12h-1.2z" fill="#6B4F33"/><path d="M33 10 a10 10 0 0 1 5 9 M35.5 6 a15 15 0 0 1 7 13" stroke="#D9A13F" stroke-width="2.6" fill="none" stroke-linecap="round"/></svg></span><div><h3>Catch a tree at its best</h3><p>Some trees are only worth the trip in one month of the year. You get a nudge when one of those near you hits its week.</p></div></div>
    </div>
  </div>
</div>
"""

def build_fakedoor_pages(pages):
    """The app: an honest coming-soon page (Hidde, 2026-07-28). It exists to
    measure real interest via the cookieless path counts and to collect
    volunteers via the existing form. Hard rules kept: no price anywhere
    (rule 2), nothing promised as available today, every tree stays free to
    explore.

    Plus existed as a sibling door until 2026-07-29, when Hidde closed it
    ("plus komt nog te vroeg... delete everything around plus"). Its url had
    been public for a day, so /plus stays resolvable as a redirect to /app
    per the Barcelona bcn_008 precedent instead of 404ing."""
    canonical = f"{BASE_URL}/app"
    body = APPLAND_BODY.replace("{form}", esc(submit_link("tree")))
    body = body.replace("APPLAND_SRCSET", img_srcset(
        "https://images.unsplash.com/photo-1690269112887-da7d1f1ea6f3", [1200, 2000, 2800], "100vw"))
    # The waitlist lives on our own page and posts to Hidde's Supabase, which
    # replaces the Google Form for this one job (Hidde, 2026-07-30: "just a
    # simple add your email address here"). Insert-only by design: the table
    # grants anon INSERT and nothing else, so nobody can read the list back.
    body += """
<script>
(function() {
  var f = document.getElementById('waitlist'), note = document.getElementById('wl-note');
  if (!f) return;
  f.addEventListener('submit', function(e) {
    e.preventDefault();
    var email = document.getElementById('wl-email').value.trim();
    if (!email) return;
    note.textContent = 'Sending...';
    at.track('waitlist-submit');
    fetch('SB_URL/rest/v1/waitlist', {
      method: 'POST',
      headers: {'apikey': 'SB_KEY', 'Content-Type': 'application/json',
                'Prefer': 'return=minimal'},
      body: JSON.stringify({email: email, source: 'app'})
    }).then(function(r) {
      if (r.ok || r.status === 409) {
        f.hidden = true;
        note.textContent = 'You are on the list. We will email you when the app is ready.';
      } else {
        note.textContent = 'That did not go through. Try again in a moment.';
      }
    }).catch(function() {
      note.textContent = 'No connection. Try again in a moment.';
    });
  });
})();
</script>
""".replace('SB_URL', SUPABASE_URL).replace('SB_KEY', SUPABASE_KEY)
    page = render_page("The Ancient Trees app",
                       "The iOS app we are building for the walk itself.",
                       canonical, body, rootpath="./")
    pages.append(("app.html", page, canonical))
    pages.append(("plus.html",
                  redirect_stub("./app", f"{BASE_URL}/app",
                                "Moved: The Ancient Trees app"), None))



def build_explore_page(all_cities, pages, registers=None):
    """One map, every tree (PRODUCT_IA follow-up, 2026-07-28). GeoJSON circle
    layers with native clustering: fast at 341 trees and at 3,000. Trees whose
    best_time includes the build month render gold, the season made visible.
    The nav item "Map" points here; the homepage hero stays the front door.

    The register layer (CLAUDE.md, approved 2026-07-29/30) renders as a second,
    visually quieter source: small hollow grey dots, no clustering (the pilot
    is 28 points), no link out since these carry no own page, and a popup that
    always states the required honesty label verbatim."""
    import datetime as _dt
    month = _dt.date.today().month
    feats = []
    for entry in all_cities:
        cslug = entry["slug"]
        for t in entry["data"]["trees"]:
            loc = t["location"]
            bt = t.get("best_time") or {}
            feats.append({
                "type": "Feature",
                "geometry": {"type": "Point",
                             "coordinates": [loc["longitude"], loc["latitude"]]},
                "properties": {
                    "name": t["name"],
                    "url": f"{cslug}/{slugify(t['name'])}",
                    "cs": cslug,
                    "city": entry["data"]["city"],
                    "age": t.get("age_estimate", ""),
                    "now": 1 if month in (bt.get("months") or []) else 0,
                },
            })
    geojson = json.dumps({"type": "FeatureCollection", "features": feats})
    reg_feats = [{
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [r["lng"], r["lat"]]},
        "properties": {"name": r["name"], "area": r["area"],
                       "designation": r["designation"]},
    } for r in (registers or [])]
    # Written beside the page rather than into it (see the fetch in the script
    # below): coordinates rounded to five decimals, about a metre, which is far
    # finer than a register pin deserves and saves a fifth of the file.
    for f in reg_feats:
        f["geometry"]["coordinates"] = [round(c, 5) for c in f["geometry"]["coordinates"]]
    global REGISTER_ASSET
    REGISTER_ASSET = "" if not reg_feats else json.dumps({"type": "FeatureCollection", "features": reg_feats},
                                ensure_ascii=False, separators=(",", ":"))
    canonical = f"{BASE_URL}/explore"
    # No counts in this copy (Hidde, 2026-07-29): "je moet nadenken dat alles
    # wat je maakt ooit gaat bestaan uit miljoenen bomen." A sentence that
    # brags about 13 or 345 stops working at 10,000; this one never will.
    # The panel's city cards need a face and a rank: hero photo per the
    # Cadiz standard where set, favourites first (the homepage list), then
    # tree count. Thumbs at 400 keep 70+ cards light.
    _FAVES = ["lisbon", "cadiz", "porto", "amsterdam", "kyoto",
              "rome", "palermo", "paris", "london", "barcelona"]
    def _city_face(e):
        hero = e["data"].get("hero_tree_id")
        if hero:
            for t in e["data"]["trees"]:
                if t["id"] == hero and usable_photo(t):
                    return usable_photo(t)["url"]
        for t in e["data"]["trees"]:
            ph = usable_photo(t)
            if ph:
                return ph["url"]
        return None
    _city_rows = []
    for e in all_cities:
        trees = e["data"]["trees"]
        if not trees:
            continue
        face = _city_face(e)
        _city_rows.append({
            "city": e["data"]["city"], "url": e["slug"],
            "country": e["data"]["country"], "n": len(trees),
            "lat": sum(t["location"]["latitude"] for t in trees) / len(trees),
            "lng": sum(t["location"]["longitude"] for t in trees) / len(trees),
            "ph": thumb_url(face, 400) if face else None,
            "rank": _FAVES.index(e["slug"]) if e["slug"] in _FAVES else 99,
        })
    _city_rows.sort(key=lambda r: (r["rank"], -r["n"]))
    # The map page carried 142 words, most of them navigation, and ranked at
    # position 15 for "ancient tree map" despite an exact-match title and 800
    # inbound links. A map with no text is a page search engines cannot read.
    # Written from the data so the numbers cannot drift from the map itself.
    _tree_total = sum(r["n"] for r in _city_rows)
    _countries = sorted({e["data"].get("country", "") for e in all_cities if e["data"].get("trees")})
    _tightest = sorted(
        ({"city": e["data"]["city"], "slug": e["slug"], "n": len(e["data"]["trees"]),
          "spread": max((haversine_km((a["location"]["latitude"], a["location"]["longitude"]),
                                      (b["location"]["latitude"], b["location"]["longitude"]))
                         for a in e["data"]["trees"] for b in e["data"]["trees"]), default=0.0)}
         for e in all_cities if len(e["data"].get("trees") or []) >= 5),
        key=lambda c: c["spread"])[:6]
    _walks = ", ".join(
        f'<a href="{c["slug"]}">{esc(c["city"])}</a> ({c["n"]} trees, {c["spread"] * 1000:.0f} m apart)'
        if c["spread"] < 1 else
        f'<a href="{c["slug"]}">{esc(c["city"])}</a> ({c["n"]} trees, {c["spread"]:.1f} km apart)'
        for c in _tightest)
    explore_prose = f"""
  <section class="explore-prose">
    <h2>What is on this map</h2>
    <p>{_tree_total} trees in {len(_city_rows)} places across {len(_countries)} countries, every one
    checked against at least two independent sources before it went on. Each pin opens a tree with its
    age, its species, why it is worth standing in front of, and directions from where you are. Gold
    pins are trees at their seasonal best this month.</p>
    <h2>The tightest walks</h2>
    <p>A map of scattered pins is a list. What makes an afternoon is trees close enough to walk
    between, so these are the places where the whole set fits in one stroll: {_walks}.</p>
    <h2>What is not on it, and why</h2>
    <p>Every pin says how precise it is. A tree marked approximate means we know the park but not the
    trunk, and the page says so rather than sending you to a spot where the tree is not. Trees on
    private land are left off entirely, as are trees whose own register hides their position, because
    the people who protect them have a reason. Nothing here is a bulk street-tree inventory: a tree
    earns a pin by being remarkable, not by existing.</p>
    <p class="explore-prose-more">Browse another way: <a href="cities">all cities</a>,
    <a href="species">by species</a>, <a href="collections">curated collections</a>, or
    <a href="in-season">what is at its best right now</a>.</p>
  </section>"""
    cities_json = json.dumps(_city_rows)
    body = f"""
<main class="explore-page">
  <div class="explore-app">
    <div class="explore-head">
      <h1>The ancient tree map</h1>
      <p>Every tree on the site, each verified, each with its story. Zoom in to a city and pick one; gold means at its best this month.</p>
      {search_form("explore", "ex-q", "ex-search")}
    </div>
    <div class="explore-split">
      <aside id="ex-panel" class="ex-panel" aria-live="polite"></aside>
      <div id="map" class="explore-map"></div>
    </div>
  </div>
  {explore_prose}
</main>
"""
    script = """
var DATA = __GEOJSON__;
var CITIES = __CITIES__;
// One world only (Hidde, 2026-07-29: "ik hoef niet 2 werelden te zien").
var map = new maplibregl.Map({
  container: 'map', style: '__STYLE__',
  center: [8, 48], zoom: 3.4, minZoom: 1.3,
  renderWorldCopies: false,
  attributionControl: {compact: true}
});
map.addControl(new maplibregl.NavigationControl());
new ResizeObserver(function() { map.resize(); }).observe(document.getElementById('map'));
// Location is asked HERE, in map context, never on the homepage.
map.addControl(new maplibregl.GeolocateControl({
  positionOptions: { enableHighAccuracy: true },
  showUserLocation: true, fitBoundsOptions: { maxZoom: 13.5 }
}));
// Open where the visitor is, without asking for anything (Hidde,
// 2026-07-30). The browser's own timezone gives a region for free: no
// permission prompt, no IP lookup, no third-party service, nothing stored.
// The Geolocate button above is still there for an exact fix.
var REGIONS = {
  'Europe/Amsterdam': [4.9, 52.37], 'Europe/Brussels': [4.35, 50.85],
  'Europe/London': [-0.13, 51.51], 'Europe/Dublin': [-6.26, 53.35],
  'Europe/Lisbon': [-9.14, 38.72], 'Europe/Madrid': [-3.7, 40.42],
  'Europe/Paris': [2.35, 48.86], 'Europe/Berlin': [13.4, 52.52],
  'Europe/Rome': [12.5, 41.9], 'Europe/Vienna': [16.37, 48.21],
  'Europe/Prague': [14.42, 50.09], 'Europe/Athens': [23.73, 37.98],
  'Europe/Warsaw': [21.01, 52.23], 'Europe/Istanbul': [28.98, 41.01],
  'Asia/Tokyo': [139.69, 35.69], 'Asia/Singapore': [103.82, 1.35],
  'Asia/Bangkok': [100.5, 13.75], 'America/New_York': [-74.0, 40.71],
  'Atlantic/Reykjavik': [-21.9, 64.15]
};
try {
  var tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
  if (REGIONS[tz]) { map.jumpTo({center: REGIONS[tz], zoom: 9}); }
  else if (tz && tz.indexOf('Europe/') === 0) { map.jumpTo({center: [10, 50], zoom: 4}); }
} catch (e) {}
function initTreeLayers() {
  if (map.getSource('trees')) { return; }
  map.addSource('trees', {type: 'geojson', data: DATA, cluster: true,
                          clusterMaxZoom: 11, clusterRadius: 42});
  // The season heartbeat: a soft pulse behind trees at their peak, the
  // recorded pulsing-pin idea (BACKLOG) in its cheapest honest form.
  map.addLayer({id: 'tree-pulse', type: 'circle', source: 'trees',
    filter: ['all', ['!', ['has', 'point_count']], ['==', ['get', 'now'], 1]],
    paint: {'circle-color': '#D9A13F', 'circle-opacity': 0.35, 'circle-radius': 9}});
  map.addLayer({id: 'clusters', type: 'circle', source: 'trees',
    filter: ['has', 'point_count'],
    paint: {'circle-color': '#4A6B2A', 'circle-opacity': 0.92,
            'circle-radius': ['step', ['get', 'point_count'], 14, 10, 18, 30, 24],
            'circle-stroke-width': 2, 'circle-stroke-color': '#F6F2E9'}});
  map.addLayer({id: 'cluster-count', type: 'symbol', source: 'trees',
    filter: ['has', 'point_count'],
    layout: {'text-field': ['get', 'point_count_abbreviated'],
             'text-font': ['Noto Sans Regular'], 'text-size': 12},
    paint: {'text-color': '#F6F2E9'}});
  map.addLayer({id: 'tree', type: 'circle', source: 'trees',
    filter: ['!', ['has', 'point_count']],
    paint: {'circle-color': ['case', ['==', ['get', 'now'], 1], '#D9A13F', '#4A6B2A'],
            'circle-radius': ['case', ['==', ['get', 'now'], 1], 9, 7],
            'circle-stroke-width': 2, 'circle-stroke-color': '#F6F2E9'}});
  // The register layer: officially designated trees from a government
  // register, not our own research. Visually quieter than the curated
  // trees on purpose (small, hollow, grey) so the two layers read as
  // different kinds of thing, not competing dots. No clustering (small
  // pilot count); no click-through URL, since these carry no own page.
  // Fetched rather than inlined: there are thousands of these and they would
  // otherwise be the heaviest thing on the page, loaded before the map the
  // visitor actually came for. They also only appear from zoom 8, because a
  // grey haze over Europe at world zoom tells nobody anything.
  if (!map.getSource('registers')) {
    fetch('assets/registers.json').then(function(r) { return r.json(); }).then(function(data) {
      if (!data.features.length || map.getSource('registers')) { return; }
      map.addSource('registers', {type: 'geojson', data: data});
      map.addLayer({id: 'register', type: 'circle', source: 'registers', minzoom: 8,
        paint: {'circle-color': 'rgba(0,0,0,0)', 'circle-radius': 5,
                'circle-stroke-width': 1.5, 'circle-stroke-color': '#8A8578'}});
      map.on('click', 'register', function(e) {
        var p = e.features[0].properties;
        new maplibregl.Popup({offset: 10})
          .setLngLat(e.features[0].geometry.coordinates)
          .setHTML('<strong>' + p.name + '</strong><br>' + p.designation +
                   (p.area ? ' &middot; ' + p.area : '') +
                   '<br><em>From the official register, not yet verified by us.</em>')
          .addTo(map);
      });
      map.on('mouseenter', 'register', function() { map.getCanvas().style.cursor = 'pointer'; });
      map.on('mouseleave', 'register', function() { map.getCanvas().style.cursor = ''; });
    }).catch(function() { /* the map works without this layer */ });
  }
  // One map experience, not two (Hidde, 2026-07-30): the world map is the
  // launcher, the city page (map plus tree list) is the destination. A
  // cluster that is entirely one city's trees opens that city's page; only
  // a multi-city cluster zooms. getClusterLeaves/ExpansionZoom are Promises
  // in MapLibre v4 (the old callback form failed silently once).
  map.on('click', 'clusters', function(e) {
    var f = map.queryRenderedFeatures(e.point, {layers: ['clusters']})[0];
    var src = map.getSource('trees');
    src.getClusterLeaves(f.properties.cluster_id, 1000, 0).then(function(leaves) {
      var cities = {};
      leaves.forEach(function(l) { cities[l.properties.cs] = true; });
      var keys = Object.keys(cities);
      if (keys.length === 1) { window.location.href = keys[0]; return; }
      src.getClusterExpansionZoom(f.properties.cluster_id).then(function(zoom) {
        map.easeTo({center: f.geometry.coordinates, zoom: zoom + 0.5, duration: 700});
      });
    });
  });
  map.on('click', 'tree', function(e) {
    var p = e.features[0].properties;
    var badge = p.now == 1 ? ' <span class="pop-now">at its best now</span>' : '';
    new maplibregl.Popup({offset: 12})
      .setLngLat(e.features[0].geometry.coordinates)
      .setHTML('<strong>' + p.name + '</strong>' + badge + '<br>' + p.age + ' &middot; ' + p.city +
               '<br><a href="' + p.url + '">See this tree &rarr;</a> &middot; ' +
               '<a href="' + p.cs + '">All ' + p.city + ' trees &rarr;</a>')
      .addTo(map);
  });
  ['clusters', 'tree'].forEach(function(l) {
    map.on('mouseenter', l, function() { map.getCanvas().style.cursor = 'pointer'; });
    map.on('mouseleave', l, function() { map.getCanvas().style.cursor = ''; });
  });
}
map.on('style.load', initTreeLayers);
if (map.isStyleLoaded()) { initTreeLayers(); }
// ---- The city chooser (Hidde, 2026-07-31, final form: "waarom kom ik
// dan niet direct op de City Page?"). The map is where you choose; the
// city page is the city experience, full stop. The panel lists up to ten
// cities in view, most likely first, and every click goes straight there.
var panel = document.getElementById('ex-panel');
function fmtCard(c) {
  var ph = c.ph ? '<span class="exc-ph"><img src="' + c.ph + '" alt="" loading="lazy"></span>' : '<span class="exc-ph exc-noph"></span>';
  return '<a class="exc-card" href="' + c.url + '">' + ph +
         '<span class="exc-body"><b>' + c.city + '</b>' +
         '<span>' + c.n + ' trees &middot; ' + c.country + '</span></span></a>';
}
function renderPanel() {
  if (!panel) return;
  var b = map.getBounds();
  var cities = CITIES.filter(function(c) { return b.contains([c.lng, c.lat]); });
  if (!cities.length) {
    panel.innerHTML = '<p class="exc-empty">No mapped cities in view. Zoom out, or <a href="contribute">be the first to map one here</a>.</p>';
    return;
  }
  var head = cities.length === 1 ? cities[0].city : 'Cities in view';
  panel.innerHTML = '<div class="exc-cityhead"><h2>' + head + '</h2></div>' +
    cities.slice(0, 10).map(fmtCard).join('');
}
map.on('moveend', renderPanel);
map.on('load', renderPanel);
renderPanel();

// The pulse: radius and opacity breathe on a 2s cycle. Paint-property
// animation only, no per-frame data churn; stops costing anything when the
// tab is hidden because rAF pauses.
(function pulse(ts) {
  if (map.getLayer && map.getLayer('tree-pulse')) {
    var t = (ts % 2000) / 2000;
    map.setPaintProperty('tree-pulse', 'circle-radius', 9 + t * 9);
    map.setPaintProperty('tree-pulse', 'circle-opacity', 0.4 * (1 - t));
  }
  requestAnimationFrame(pulse);
})(0);
"""
    script = (script.replace("__GEOJSON__", geojson)
                    .replace("__CITIES__", cities_json)
                    .replace("__STYLE__", MAP_STYLE))
    script = f'<script src="{MAPLIBRE_JS}"></script>\n<script>\n' + script + "\n</script>" + SEARCH_WIDGET_JS
    page = render_page("Ancient Tree Map: every remarkable old tree, one map",
                       "The interactive map of every verified ancient tree on the site, with the ones at their seasonal best highlighted.",
                       canonical, body, head_extra=map_head(), rootpath="./", scripts=script)
    pages.append(("explore.html", page, canonical))


def build_contribute_page(published, pages):
    """The flywheel's front door: readers send trees, the nightly run verifies
    and writes them up. Deliberately asks for the few things that make a
    submission verifiable, because unverifiable ones cannot be published."""
    canonical = f"{BASE_URL}/contribute"
    rootpath = "./"
    title = fit_title(["Become Your City's Tree Guide",
                       "Map Your City's Ancient Trees"], canonical)
    description = ("Know the remarkable old trees of your city? Put them on the map. "
                   "Every submission is verified against independent sources before it goes live.")
    crumb_items = [("Home", BASE_URL), ("Suggest a tree", None)]

    city_links = " &middot; ".join(
        f'<a href="{p["slug"]}">{esc(p["city"])}</a>' for p in published
    )

    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>Become your city's tree guide</h1>
  <p class="answer-first">This map is missing far more cities than it has, and the trees that matter most are the ones locals already know about. If you know your city's remarkable old trees, you can put them on the map and be credited for it.</p>
  <div class="prose-block">
    <p>Research from a distance finds the famous trees. It misses the one on the corner that everyone in the neighbourhood walks past, the one with the story attached, the one that is only obvious if you live there. That gap is why this page exists.</p>
    <p>Everything sent in gets checked against independent sources, and the location gets verified, because a wrong pin is worse than a missing tree. Confirmed trees get their own page with your credit on the city. What cannot be confirmed waits instead of going live half-true. To be straight with you about what you get: your name on the city you mapped, not a login or a profile. Those may come later.</p>
  </div>

  <form id="suggest" class="suggest-form" autocomplete="off">
    <label>What are you sending?
      <select id="sg-kind">
        <option value="tree">One remarkable tree</option>
        <option value="city">My city's trees</option>
        <option value="correction">A correction to something on the site</option>
        <option value="privacy">A privacy request (remove what I sent in)</option>
      </select>
    </label>
    <label>Which city?
      <input type="text" id="sg-city" required placeholder="Utrecht">
    </label>
    <label>The tree, or trees
      <input type="text" id="sg-tree" placeholder="The plane on the church square">
    </label>
    <label>Where does it stand? <span class="sg-hint">A street, a park, or a Google Maps link. The single most useful thing you can give us.</span>
      <input type="text" id="sg-where" placeholder="Domplein, next to the cathedral entrance">
    </label>
    <label>Why is it remarkable?
      <textarea id="sg-why" rows="3" placeholder="Old, huge, a story attached, or simply the tree everyone knows"></textarea>
    </label>
    <label>Your name, for the credit <span class="sg-hint">Optional. Shown on the city page when your tree goes live.</span>
      <input type="text" id="sg-name" placeholder="First name is fine">
    </label>
    <button type="submit" class="go-btn">Send it in</button>
    <p class="sg-note" id="sg-note"></p>
  </form>

  <h2>What helps most</h2>
  <ul class="link-list">
    <li><strong>Where exactly it stands.</strong> A street corner, a park entrance, or a dropped pin from Google Maps. The single most useful thing you can give us.</li>
    <li><strong>Why it is remarkable.</strong> Old, enormous, strange, or tied to a local story.</li>
    <li><strong>How you know.</strong> A link, a book, a plaque, or just that you grew up next to it.</li>
    <li><strong>A photo you took yourself,</strong> if you have one. We can only publish photos that are yours to share or openly licensed.</li>
  </ul>

  <h2>Or fix something</h2>
  <div class="prose-block">
    <p>Spotted a wrong location, an age that looks off, or a tree that has fallen since we wrote about it? Those corrections are just as valuable. <a href="{submit_link('correction')}">Send a correction</a> and say what is wrong.</p>
  </div>
  <p class="suggest">Cities on the map so far: {city_links}</p>
</main>
"""
    graph = site_graph() + [breadcrumb_schema(crumb_items, canonical)]
    head_extra = ld_script(graph)
    SUGGEST_JS = """
<script>
(function() {
  var f = document.getElementById('suggest'), note = document.getElementById('sg-note');
  if (!f) return;
  var params = new URLSearchParams(location.search);
  var kind = params.get('kind');
  var map = {tree: 'tree', city: 'city', home: 'city', correction: 'correction', privacy: 'privacy'};
  if (kind && map[kind]) { document.getElementById('sg-kind').value = map[kind]; }
  f.addEventListener('submit', function(e) {
    e.preventDefault();
    var city = document.getElementById('sg-city').value.trim();
    if (!city) return;
    note.textContent = 'Sending...';
    at.track('suggestion-submit');
    fetch('SB_URL/rest/v1/submissions', {
      method: 'POST',
      headers: {'apikey': 'SB_KEY', 'Content-Type': 'application/json', 'Prefer': 'return=minimal'},
      body: JSON.stringify({
        kind: document.getElementById('sg-kind').value,
        city: city,
        tree: document.getElementById('sg-tree').value.trim(),
        location_hint: document.getElementById('sg-where').value.trim(),
        why: document.getElementById('sg-why').value.trim(),
        name: document.getElementById('sg-name').value.trim(),
        page: document.referrer || null
      })
    }).then(function(r) {
      if (r.ok) {
        f.hidden = true;
        note.textContent = 'Thank you. Everything sent in is verified against independent sources; confirmed trees go live with your credit.';
      } else {
        note.textContent = 'That did not go through. Try again in a moment.';
      }
    }).catch(function() { note.textContent = 'No connection. Try again in a moment.'; });
  });
})();
</script>
""".replace('SB_URL', SUPABASE_URL).replace('SB_KEY', SUPABASE_KEY)
    page = render_page(title, description, canonical, body, head_extra, SUGGEST_JS, rootpath)
    pages.append(("contribute.html", page, canonical))


# ----------------------------------------------------------------- homepage

def build_homepage(published, upcoming, collections, pages, renderable=None, species_slugs=None):
    title = "Ancient Trees: remarkable old trees near you, mapped"
    description = ("Find the remarkable old trees around you. Ten per city, each verified, "
                   "each with its story, its exact spot and directions from where you stand.")

    # The four-column "anywhere" block, straight from the AllTrails reference
    # (top cities / parks / trails / POIs becomes top cities / species /
    # collections / oldest trees). Hidde spotted the compressed first version
    # in one second; the reference-compare rule exists because of it.
    # Equal-length columns (Hidde, 2026-07-29: "laten we die rijen even lang
    # maken"): nine links plus a more-link each. Species has only three pages
    # so far; the short column closes the row instead of leaving a hole
    # mid-grid.
    # Cities: nine visible, the next ten revealed by a button (Hidde,
    # 2026-07-30). The by-country fold that used to sit under this block is
    # gone: "all 37 cities by country makes absolutely no sense" on a
    # homepage. /cities remains the full crawlable index.
    ranked_cities = sorted(published, key=lambda x: -x["count"])
    cities_col = "".join('<a href="%s">%s</a>' % (p["slug"], esc(p["city"]))
                         for p in ranked_cities[:9])
    more_cities = "".join('<a href="%s">%s</a>' % (p["slug"], esc(p["city"]))
                          for p in ranked_cities[9:19])
    species_col = "".join('<a href="species/%s">%s</a>' % (sl, esc(cn))
                          for cn, sl in (species_slugs or []))
    species_col += '<a class="dir-morelink" href="species">All species</a>'
    coll_col = "".join('<a href="collections/%s">%s</a>' % (esc(c["slug"]), esc(c["title"]))
                       for c in (collections or [])[:9])
    coll_col += '<a class="dir-morelink" href="collections">All collections</a>'
    oldest = []
    for entry in (renderable or []):
        for t in entry["data"]["trees"]:
            if t.get("age_max"):
                oldest.append((t["age_max"], t["name"], entry["slug"], slugify(t["name"])))
    oldest.sort(key=lambda x: -x[0])
    trees_col = "".join('<a href="%s/%s">%s</a>' % (cs, ts, esc(name))
                        for _, name, cs, ts in oldest[:10])
    more_block = (
        '<span id="more-cities" hidden>%s</span>'
        '<button type="button" class="dir-morelink dir-morebtn" id="more-cities-btn">Show 10 more</button>'
        '<a class="dir-morelink" href="cities">All %d cities</a>' % (more_cities, len(published))
    ) if more_cities else '<a class="dir-morelink" href="cities">All %d cities</a>' % len(published)
    directory_html = (
        '<div class="dir-cols">'
        + '<div class="dir-group"><h3>Top cities</h3>%s%s</div>' % (cities_col, more_block)
        + '<div class="dir-group"><h3>Collections</h3>%s</div>' % coll_col
        + '<div class="dir-group"><h3>Oldest trees</h3>%s</div>' % trees_col
        + '<div class="dir-group"><h3>Top species</h3>%s</div>' % species_col
        + '</div>')

    live_cards = "".join(
        f"""<a class="city-card" href="{p['slug']}">
      <div class="city-card-name">{esc(p['city'])}</div>
      <div class="city-card-meta">{esc(p['country'])} &middot; {p['count']} trees</div>
    </a>"""
        for p in published
    )
    soon_cards = "".join(
        f"""<a class="city-card soon" href="contribute">
      <div class="city-card-name">{esc(c['city'])}</div>
      <div class="city-card-meta">{esc(c['country'])} &middot; not mapped yet</div>
      <div class="city-card-cta">Be the first to map it</div>
    </a>"""
        for c in upcoming
    )


    # The two card shelves (Hidde, 2026-07-28, the AllTrails "Local favorites"
    # grammar): photo cards or nothing; a shelf with no photo-worthy content
    # stays off the page rather than degrading into text links.
    import datetime as _dt
    _month = _dt.date.today().month
    tree_by_id = {}
    for entry in (renderable or []):
        for t in entry["data"]["trees"]:
            tree_by_id[t["id"]] = (entry, t)

    # Tree of the month (Hidde, 2026-07-31: "logischere taal; tree of the
    # month: the blooming wingnut of the yellowing ginkgo"). When one species
    # dominates the month's peaks, the shelf becomes that species' moment and
    # shows its best specimens; otherwise it falls back to the generic title.
    candidates = []
    for entry in (renderable or []):
        for t in entry["data"]["trees"]:
            bt = t.get("best_time") or {}
            ph = usable_photo(t)
            if _month in (bt.get("months") or []) and ph:
                candidates.append((entry, t, bt, ph))

    KIND_VERB = {"flowers": "blooming", "catkins": "blooming", "fruit": "fruiting",
                 "autumn colour": "turning", "fresh leaves": "unfurling"}

    def _season_card(entry, t, bt, ph):
        return (f'<a class="shelf-card" href="{entry["slug"]}/{slugify(t["name"])}">'
                f'<span class="shelf-ph"><img {img_srcset(ph["url"], [400, 800], "(max-width: 800px) 72vw, 20vw")} alt="" loading="lazy">'
                f'<span class="shelf-now">at its best now</span></span>'
                f'<b>{esc(t["name"])}</b>'
                f'<span class="shelf-meta">{esc(entry["data"]["city"])} &middot; {esc(bt.get("label", ""))}</span></a>')

    season_shelf = ""
    if len(candidates) >= 2:
        by_species = {}
        for c in candidates:
            by_species.setdefault(species_common(c[1]), []).append(c)
        dominant, group = max(by_species.items(), key=lambda kv: len(kv[1]))
        # NOT `title`: that variable is the homepage's <title> further down,
        # and shadowing it once shipped the shelf caption as the tab title.
        shelf_title = "At their best right now"
        picked = candidates
        if len(group) >= 2:
            # "the yellowing ginkgo": verb from the kind, short name from the
            # common name's last word (Caucasian Wingnut -> wingnut).
            kinds = [season_kind(c[2]) for c in group]
            kind = next((k for k in kinds if k), "")
            verb = KIND_VERB.get(kind)
            short = dominant.split()[-1].lower()
            if verb:
                shelf_title = f"Tree of the month: the {verb} {esc(short)}"
                picked = group
        season_shelf = (
            f'<section class="shelf"><div class="shelf-head"><h2>{shelf_title}</h2>'
            '<a href="in-season">See everything in season</a></div>'
            '<div class="shelf-row">' + "".join(_season_card(*c) for c in picked[:4]) + '</div></section>')

    # Our favourite tree cities (Hidde, 2026-07-31): ten cards in the prime
    # shelf spot. The list is HIS to curate; this order mixes the pages search
    # already rewards with the pages he is proudest of (Cadiz is the photo
    # calibration city). Reorder or swap on his word, no code beyond the list.
    #
    # Revised 2026-08-08, on Hidde's rule rather than on walk quality: "the ones
    # with most trees, most walks and highest on our go to market strategy (aka
    # most tourist)". So the sort is tourism tier first (phase 1 of the rollout,
    # then phase 2), then tree count, then how many walks the city offers.
    #
    # An earlier version of this list ranked on photo coverage and dropped
    # London and Kyoto for having no walk. His ordering puts them back: the
    # shelf carries the strategy, and photos come later. London leads the
    # rollout and Kyoto is a phase-2 city, so both belong here even while their
    # trees are too scattered to connect.
    FAVOURITE_CITIES = ["barcelona", "rome", "paris", "berlin", "amsterdam",
                        "london", "new-york", "lisbon", "vienna", "edinburgh"]
    by_slug = {e["slug"]: e for e in (renderable or [])}
    fav_cards = []
    for cs in FAVOURITE_CITIES:
        e = by_slug.get(cs)
        if not e:
            continue
        # hero_tree_id (optional, per city JSON): which tree's photo is the
        # city's face on shelves. Hidde, 2026-07-31: a camellia close-up is a
        # fine photo for that tree but "niet als hoofdfoto" for Porto.
        photo = None
        hero = e["data"].get("hero_tree_id")
        if hero:
            for t in e["data"]["trees"]:
                if t["id"] == hero:
                    photo = usable_photo(t)
        if not photo:
            for t in e["data"]["trees"]:
                photo = usable_photo(t)
                if photo:
                    break
        if not photo:
            continue
        fav_cards.append(
            f'<a class="shelf-card" href="{cs}">'
            f'<span class="shelf-ph"><img {img_srcset(photo["url"], [400, 800], "(max-width: 800px) 72vw, 20vw")} alt="" loading="lazy"></span>'
            f'<b>{esc(e["data"]["city"])}</b>'
            f'<span class="shelf-meta">{len(e["data"]["trees"])} trees &middot; {esc(e["data"]["country"])}</span></a>')
    fav_shelf = ""
    if len(fav_cards) >= 4:
        fav_shelf = (
            '<section class="shelf"><div class="shelf-head"><h2>Our favourite tree cities</h2>'
            '<a href="cities">All cities</a></div>'
            '<div class="shelf-row shelf-row-wide">' + "".join(fav_cards[:10]) + '</div></section>')

    coll_cards = []
    shelf_photos_used = set()
    for c in collections or []:
        photo = None
        n_cities = len({e["city_slug"] for e in c.get("entries", [])})
        for e in c.get("entries", []):
            pair = tree_by_id.get(e["tree_id"])
            p = pair and usable_photo(pair[1])
            if p and p["url"] not in shelf_photos_used:
                photo = p
                break
        if not photo:
            continue
        shelf_photos_used.add(photo["url"])
        coll_cards.append(
            f'<a class="shelf-card" href="collections/{esc(c["slug"])}">'
            f'<span class="shelf-ph"><img {img_srcset(photo["url"], [400, 800], "(max-width: 800px) 72vw, 20vw")} alt="" loading="lazy"></span>'
            f'<b>{esc(c["title"])}</b>'
            f'<span class="shelf-meta">{len(c.get("entries", []))} trees &middot; {n_cities} cities</span></a>')
    coll_shelf = ""
    if coll_cards:
        coll_shelf = (
            '<section class="shelf"><div class="shelf-head"><h2>Collections</h2>'
            '<a href="collections">All collections</a></div>'
            '<div class="shelf-row">' + "".join(coll_cards[:4]) + '</div></section>')

    def _icon(k):
        return f'<svg viewBox="0 0 40 40" fill="currentColor" aria-hidden="true">{SPECIES_ICONS[k]}</svg>'
    find_pin_1=_icon("plane"); find_pin_2=_icon("wingnut"); find_pin_3=_icon("broadleaf")
    walk_pin_1=_icon("oak"); walk_pin_2=_icon("plane"); walk_pin_3=_icon("ginkgo"); walk_pin_4=_icon("yew")
    radar_icon_1=_icon("ginkgo"); radar_icon_2=_icon("ginkgo"); radar_icon_3=_icon("wisteria")
    _m=[0,0,0,.5,.5,0,.5,.5,0,.5,1,0]
    radar_months="".join('<span class="%s"></span>'%("on" if v==1 else "half" if v==.5 else "") for v in _m)
    lit=["oak","plane","ginkgo","yew","cedar","olive"]; dim=["pine","cypress","fig","wisteria"]
    collected_species="".join(
        f'<span class="sp{"" if k in lit else " dim"}">{_icon(k)}'
        + ('<span class="sp-name">Ginkgo</span>' if k=="ginkgo" else "") + '</span>'
        for k in lit+dim)
    body = f"""
<div class="home-hero poster">
  <img class="hero-bg" id="hero-bg" {img_srcset(HERO_PHOTOS[0][0], [1200, 2000, 2800], "100vw")} alt="">
  <div class="hero-scrim"></div>
  <div class="hero-center">
    <h1>Trees worth the walk, <em>wherever you are</em>.</h1>
    {search_form("home", "city-q", "hero-search poster-search", with_button=True)}
    <p class="hero-links">
      <a class="hero-link" href="explore">Explore trees near you</a>
    </p>
  </div>
</div>
<section class="hero-sub">
  <p>For people who love being outside. See the remarkable old trees near you, walk a few of them in an afternoon with the story of why each is worth it, and tick off the ones you have stood in front of. Every tree free to explore.</p>
</section>
{fav_shelf}
<section class="home-acts">
  <div class="home-act">
    <div class="home-act-copy">
      <span class="home-act-verb">Find</span>
      <h2>The trees near you, right now.</h2>
      <p>The map finds the remarkable old trees closest to where you are standing, and points you at the nearest one with a walk time and directions to your phone.</p>
    </div>
    <figure class="home-act-visual hav-card">
      <svg class="scene" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
        <path d="M-10 80 L410 60" stroke="#E2DFD2" stroke-width="14"/>
        <path d="M-10 190 L410 210" stroke="#E2DFD2" stroke-width="18"/>
        <path d="M120 -10 L100 310" stroke="#E2DFD2" stroke-width="12"/>
        <path d="M300 -10 L330 310" stroke="#E2DFD2" stroke-width="14"/>
        <path d="M150 95 Q 220 70 290 110 Q 310 170 240 185 Q 160 195 145 150 Z" fill="#E4EAD5"/>
        <path d="M-10 250 Q 120 235 410 265 L410 310 L-10 310 Z" fill="#DCE7EF"/>
      </svg>
      <span class="map-pin" style="left:30%;top:28%">{find_pin_1}</span>
      <span class="map-pin" style="left:63%;top:44%">{find_pin_2}</span>
      <span class="map-pin" style="left:44%;top:74%">{find_pin_3}</span>
      <span class="map-pin me" style="left:52%;top:58%"></span>
      <figcaption class="hav-chip"><span class="hav-dot"></span>
        <span><strong>Nearest to you</strong>The Wertheimpark Wingnut &middot; 6 min walk</span></figcaption>
    </figure>
  </div>
  <div class="home-act">
    <div class="home-act-copy">
      <span class="home-act-verb">Walk</span>
      <h2>A route past the ones worth seeing.</h2>
      <p>Only the most remarkable, linked into one walk you can do in an afternoon, each with its story and the month it is at its most spectacular, so you know when to go.</p>
    </div>
    <figure class="home-act-visual hav-card">
      <svg class="scene" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
        <path d="M-10 120 L410 100" stroke="#E2DFD2" stroke-width="16"/>
        <path d="M200 -10 L190 310" stroke="#E2DFD2" stroke-width="12"/>
        <path d="M40 200 Q 140 240 300 215 Q 380 200 420 230" stroke="#E2DFD2" stroke-width="14" fill="none"/>
        <path d="M250 40 Q 340 30 380 80 Q 370 140 290 130 Q 240 110 250 40 Z" fill="#E4EAD5"/>
        <path d="M76 234 C 120 200 96 150 150 132 C 210 112 232 150 268 96 C 290 62 320 70 340 84"
          stroke="#3D5C1E" stroke-width="3.5" fill="none" stroke-dasharray="1 9" stroke-linecap="round"/>
      </svg>
      <span class="map-pin" style="left:19%;top:78%">{walk_pin_1}<span class="n">1</span></span>
      <span class="map-pin" style="left:37.5%;top:44%">{walk_pin_2}<span class="n">2</span></span>
      <span class="map-pin" style="left:67%;top:32%">{walk_pin_3}<span class="n">3</span></span>
      <span class="map-pin" style="left:85%;top:28%">{walk_pin_4}<span class="n">4</span></span>
      <figcaption class="hav-chip"><span><strong>Afternoon walk</strong>4 trees &middot; 5.2 km &middot; about 1h 10m</span></figcaption>
    </figure>
  </div>
  <div class="home-act">
    <div class="home-act-copy">
      <span class="home-act-verb">Season</span>
      <h2>See them at their best.</h2>
      <p>Every tree has a moment: the ginkgo's golden week, ten days of blossom, a month of catkins. The radar shows what is at its best around you right now, so you go at exactly the right time.</p>
    </div>
    <div class="home-act-visual season-card">
      <h5 class="season-now">At their best in November</h5>
      <div class="sr-row"><span class="sp">{radar_icon_1}</span><span class="sr-body"><b>The Zenpukuji Ginkgo</b><i>turning deep gold</i></span><span class="hav-badge-inline">now</span></div>
      <div class="sr-row"><span class="sp">{radar_icon_2}</span><span class="sr-body"><b>Meiji Jingu Gaien Avenue</b><i>the whole street gold</i></span><span class="hav-badge-inline">now</span></div>
      <div class="sr-row dim"><span class="sp dim">{radar_icon_3}</span><span class="sr-body"><b>Kameido Tenjin Wisteria</b><i>hanging in flower</i></span><span class="sr-when">May</span></div>
      <div class="sr-months">{radar_months}</div>
      <p class="sr-link"><a href="in-season">See what is at its best this month &rarr;</a></p>
    </div>
  </div>
  <div class="home-act">
    <div class="home-act-copy">
      <span class="home-act-verb">Collect</span>
      <h2>Tick off the ones you have stood in front of.</h2>
      <p>Check in at the tree and watch your collection grow: trees, cities, species. Rarer and older trees count for more, and badges for a finished city are on their way.</p>
    </div>
    <div class="home-act-visual" style="background:none;border:none;box-shadow:none;padding:0">
      <div class="hav-phone"><div class="hav-screen">
        <h4>Your trees</h4>
        <div class="stat-row">
          <div class="stat"><b>23</b><span>trees</span></div>
          <div class="stat alt"><b>6</b><span>cities</span></div>
          <div class="stat"><b>2000</b><span>oldest, yrs</span></div>
        </div>
        <h5>Collected species</h5>
        <div class="sp-grid">{collected_species}</div>
      </div></div>
    </div>
  </div>
</section>
{season_shelf}
{coll_shelf}
<main class="page">
  <h2 class="section-heading" id="cities">Ancient trees anywhere</h2>
  {directory_html}
  <div class="mission">
    <p>We are on a mission to map every remarkable tree in the world, and we could use your help. If you know a good tree, or want to map a whole city, <a href="contribute">tell us about it</a>. If you spot a mistake, tell us that too. We work on this database every day.</p>
  </div>

</main>
"""
    head_extra = ld_script(site_graph())
    scripts = home_hero_script() + SEARCH_WIDGET_JS
    page = render_page(title, description, BASE_URL + "/", body, head_extra, scripts,
                       rootpath="./", og_type="website")
    pages.append(("index.html", page, BASE_URL + "/"))


# ------------------------------------------------------------ redirect stubs

def redirect_stub(target_rel, canonical, title):
    return (
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        f'<meta http-equiv="refresh" content="0; url={target_rel}">'
        f'<link rel="canonical" href="{canonical}">'
        f'<title>{esc(title)}</title>'
        f'<script>window.location.replace("{target_rel}");</script></head>'
        f'<body><p>This page moved to <a href="{target_rel}">{canonical}</a>.</p></body></html>'
    )


# A tree that gets renamed (its id kept, per the dead-tree-replacement rule in
# CLAUDE.md Step 1) changes URL, since tree slugs are derived from the name.
# Entries here keep the old, possibly-indexed URL resolving. Add one whenever
# a tree's name changes: (city_slug, old_tree_slug, tree_id).
RENAMED_TREE_SLUGS = [
    ("london", "queen-elizabeths-oak", "lon_005"),      # -> Sweet Chestnut of Greenwich Park, 2026-07-27
    ("vienna", "stock-im-eisen", "vie_002"),             # -> Ginkgo of the Schubert Monument, 2026-07-27
    ("barcelona", "plane-trees-of-la-rambla", "bcn_008"),  # -> Silk Tree of the Ciutadella, 2026-07-26 (never got a redirect until now)
    ("dublin", "sculpted-cypress", "dub_007"),           # -> Many-Trunked Holm Oak of St Anne's Park, 2026-07-27
    ("rome", "quercia-del-tasso", "rom_001"),            # -> Ginkgo of Villa Sciarra, 2026-07-27
    ("berlin", "bellevue-oak", "ber_006"),                # -> Mahlsdorf Village Lime, 2026-07-29
    ("athens", "trees-of-kaisariani-monastery", "ath_010"),  # -> Rubber Fig of Drosopoulou Street, 2026-08-02 (collectible-point failure)
]

# A tree that gets pulled outright (no replacement, unlike RENAMED_TREE_SLUGS)
# because it turned out unverifiable or possibly on non-visitable private
# land. Its old, possibly-indexed URL redirects to the city page rather than
# 404ing. Entries: (city_slug, old_tree_slug).
REMOVED_TREE_SLUGS = [
    ("lyon", "cedar-of-ile-barbe"),  # lyo_007 pulled 2026-07-29: no source verifies the species claim, and the only garden it could plausibly stand in is the island's private residential half, explicitly non-visitable per the DIREN site classe brochure
]

# A city published under the wrong name keeps its old URL resolving, because
# hard rule 3 says nothing irreversible in public and a retired URL is exactly
# that. Entries: (old_slug, new_slug). Every page under the old slug redirects:
# the city page, its question page, and each tree.
RENAMED_CITY_SLUGS = [
    ("padova", "padua"),  # 2026-08-06, hours after publication: every other Italian city here uses its English name (Florence, Naples, Turin), and English readers search Padua
]


def build_redirects(published, pages, tree_slugs=None):
    """Old /cities/[slug]/ URLs redirect to the contract URLs, and
    /[slug]/ with a trailing slash redirects to the canonical /[slug]."""
    for p in published:
        title = f"Moved: Ancient Trees in {p['city']}"
        pages.append((f"cities/{p['slug']}/index.html",
                      redirect_stub(f"../../{p['slug']}", p["canonical"], title), None))
        pages.append((f"{p['slug']}/index.html",
                      redirect_stub(f"../{p['slug']}", p["canonical"], title), None))
    pages.append(("collections/index.html",
                  redirect_stub("../collections", f"{BASE_URL}/collections",
                                "Moved: Collections"), None))
    pages.append(("species/index.html",
                  redirect_stub("../species", f"{BASE_URL}/species",
                                "Moved: Species"), None))
    if tree_slugs:
        for city_slug, old_slug, tree_id in RENAMED_TREE_SLUGS:
            new_slug = tree_slugs.get(tree_id)
            if not new_slug or new_slug == old_slug:
                continue
            pages.append((f"{city_slug}/{old_slug}.html",
                          redirect_stub(new_slug, f"{BASE_URL}/{city_slug}/{new_slug}",
                                        "Moved: this tree"), None))
    # A city that changed name keeps every old URL alive: the city page, its
    # question page and each of its trees.
    by_slug = {p["slug"]: p for p in published}
    for old_slug, new_slug in RENAMED_CITY_SLUGS:
        p = by_slug.get(new_slug)
        if not p:
            continue
        title = f"Moved: Ancient Trees in {p['city']}"
        pages.append((f"{old_slug}.html",
                      redirect_stub(new_slug, p["canonical"], title), None))
        pages.append((f"{old_slug}/index.html",
                      redirect_stub(f"../{new_slug}", p["canonical"], title), None))
        pages.append((f"{old_slug}/oldest-tree.html",
                      redirect_stub(f"../{new_slug}/oldest-tree",
                                    f"{BASE_URL}/{new_slug}/oldest-tree", title), None))
        # `published` is slimmed by this point and carries no trees, so read the
        # city file for its ids rather than trusting the entry to hold them.
        cf = DATA / "cities" / f"{new_slug}.json"
        city_trees = json.loads(cf.read_text())["trees"] if cf.exists() else []
        for t in city_trees:
            ts = (tree_slugs or {}).get(t["id"])
            if not ts:
                continue
            pages.append((f"{old_slug}/{ts}.html",
                          redirect_stub(f"../{new_slug}/{ts}",
                                        f"{BASE_URL}/{new_slug}/{ts}",
                                        "Moved: this tree"), None))

    city_slug_by_slug = {p["slug"]: p["slug"] for p in published}
    for city_slug, old_slug in REMOVED_TREE_SLUGS:
        if city_slug not in city_slug_by_slug:
            continue
        pages.append((f"{city_slug}/{old_slug}.html",
                      redirect_stub(f"../{city_slug}", f"{BASE_URL}/{city_slug}",
                                    "Moved: this tree"), None))


def validate_internal_links(pages):
    """Every internal href must resolve to a page this build produces.

    Catches wrong relative paths (P8: no dead ends) before deploy.
    """
    # account.html is written straight to DIST by build_account_page (outside
    # the pages list, deliberately out of the sitemap), but nav links to it
    # once AUTH_ENABLED is on, so the checker must know it exists.
    valid = {"/", "/assets/style.css", "/account", "/account.html"}
    for relpath, _, _ in pages:
        url = "/" + relpath
        valid.add(url)
        if url.endswith("/index.html"):
            valid.add(url[: -len("index.html")])
        elif url.endswith(".html"):
            valid.add(url[:-5])

    for relpath, content, _ in pages:
        # Only markup is checked. Links a script builds at runtime are not
        # statically resolvable, and scanning them yields false positives.
        content = re.sub(r"<script\b.*?</script>", "", content, flags=re.S)
        page_url = "/" + relpath
        if page_url.endswith("/index.html"):
            page_url = page_url[: -len("index.html")]
        elif page_url.endswith(".html"):
            page_url = page_url[:-5]
        if page_url == "/index":
            page_url = "/"
        for href in re.findall(r'href="([^"]+)"', content):
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = urlparse(urljoin(page_url, href)).path
            if target not in valid:
                ERRORS.append(f"{page_url}: broken internal link {href!r} resolves to {target}")


MONTH_FULL = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]


def build_in_season_page(renderable, tree_slugs, pages):
    """The bloom page: what is at its best right now, as a plain list.

    Approved by Hidde 2026-07-26 ("een in bloom pagina, en een lijst prima").
    Static is honest here: the site rebuilds many times a day, so the current
    month stays current. A month with nothing in season leads with what is
    coming instead of an empty page."""
    now = date.today().month
    cur_name = MONTH_FULL[now - 1]

    def entries_for(month):
        out = []
        for entry in renderable:
            city = entry["data"]["city"]
            cslug = entry["slug"]
            for t in entry["data"]["trees"]:
                bt = t.get("best_time") or {}
                if month in (bt.get("months") or []) and t["id"] in tree_slugs:
                    out.append((city, cslug, t, bt.get("label", "")))
        return out

    current = entries_for(now)
    current_ids = {t["id"] for _, _, t, _ in current}
    upcoming = []
    for ahead in (1, 2):
        m = (now - 1 + ahead) % 12 + 1
        # A tree already at its best now is news today, not next month:
        # repeating it under "Coming in August" reads as a bug.
        ups = [e for e in entries_for(m) if e[2]["id"] not in current_ids]
        if ups:
            upcoming.append((MONTH_FULL[m - 1], ups))

    def rows(items):
        by_city = {}
        for city, cslug, t, label in items:
            by_city.setdefault((city, cslug), []).append((t, label))
        parts = []
        for (city, cslug), ts in sorted(by_city.items()):
            lis = "".join(
                f'<li><a href="{cslug}/{tree_slugs[t["id"]]}">{esc(t["name"])}</a>, {esc(label)}</li>'
                for t, label in ts)
            parts.append(f'<h3><a href="{cslug}">{esc(city)}</a></h3><ul class="link-list">{lis}</ul>')
        return "".join(parts)

    n = len(current)
    title = fit_title([f"Trees at Their Best in {cur_name}",
                       f"In Season: Trees at Their Best in {cur_name}"],
                      f"{BASE_URL}/in-season")
    if current:
        answer = (f"{n} of the mapped trees are at their best in {cur_name}: "
                  "this is the list, city by city, with what you will actually see.")
    else:
        answer = (f"No mapped tree peaks in {cur_name}, honestly. "
                  "Here is what is coming next, so you can plan the walk that is worth it.")
    description = (f"Which remarkable old trees are worth visiting in {cur_name}? " + answer)[:DESC_MAX]

    body_parts = ['<main class="content-page">',
                  breadcrumb_html([("Home", BASE_URL), ("In season", None)], "./"),
                  f'<h1>Trees at their best in <em>{esc(cur_name)}</em></h1>',
                  f'<p class="answer-first">{esc(answer)}</p>']
    if current:
        body_parts.append(rows(current))
    for mname, ups in upcoming:
        body_parts.append(f'<h2>Coming in {esc(mname)}</h2>')
        body_parts.append(rows(ups))
    body_parts.append('<p class="suggest">Every peak here is species-real: blossom, catkins or autumn colour, never filler. Trees that look the same all year, the yews and the evergreens, are honestly absent.</p>')
    body_parts.append('</main>')
    body = "\n".join(body_parts)

    canonical = f"{BASE_URL}/in-season"
    link_count = n + sum(len(u) for _, u in upcoming) + len({c for c, _, _, _ in current})
    check_links(canonical, link_count, min(8, max(link_count, 1)))
    graph = site_graph() + [
        {"@type": "ItemList", "name": f"Trees at their best in {cur_name}",
         "itemListElement": [
             {"@type": "ListItem", "position": i, "name": t["name"],
              "url": f"{BASE_URL}/{cslug}/{tree_slugs[t['id']]}"}
             for i, (city, cslug, t, label) in enumerate(current, 1)]},
        breadcrumb_schema([("Home", BASE_URL), ("In season", None)], canonical),
    ]
    page = render_page(title, description, canonical, body, ld_script(graph), "", rootpath="./")
    pages.append(("in-season.html", page, canonical))


def build_account_page():
    """The sign-in flow, built to the common magic-link pattern before any
    backend exists: email in, check-your-inbox with masked address and a
    resend cooldown, an expired-link recovery, and the signed-in shell that
    shows the visitor's real on-device collection. Written straight to DIST,
    kept out of the sitemap and noindexed while AUTH_ENABLED is False."""
    body = """
<main class="content-page account-page">

  <section id="st-signin" class="acct-card">
    <p class="hero-kicker">Your tree collection</p>
    <h1>Sign in to keep it <em>everywhere</em>.</h1>
    <p class="acct-sub">One email, no password. We send you a sign-in link; your collected trees follow you to any device.</p>
    <form id="acct-form" class="hero-search" autocomplete="email">
      <input type="email" id="acct-email" placeholder="you@example.com" aria-label="Email address" required>
      <button type="submit" class="go-btn">Email me a sign-in link</button>
    </form>
    <p class="acct-fine">We store only your email address, for sign-in links and nothing else, and you can delete your account at any time. <a href="privacy">Privacy</a></p>
  </section>

  <section id="st-sent" class="acct-card" hidden>
    <h1>Check your <em>inbox</em>.</h1>
    <p class="acct-sub">We sent a sign-in link to <strong id="sent-to"></strong>. It works once and expires in 15 minutes.</p>
    <p class="acct-actions">
      <button type="button" id="resend" class="go-btn ghost" disabled>Resend (<span id="cool">30</span>)</button>
      <button type="button" id="change" class="acct-link">Use a different address</button>
    </p>
  </section>

  <section id="st-expired" class="acct-card" hidden>
    <h1>That link has <em>expired</em>.</h1>
    <p class="acct-sub">Links work once and briefly, to keep your account safe. One tap gets you a fresh one.</p>
    <p class="acct-actions"><button type="button" id="re-expired" class="go-btn">Send a new link</button></p>
  </section>

  <section id="st-in" class="acct-card" hidden>
    <p class="hero-kicker">Signed in</p>
    <h1>Your <em>trees</em>.</h1>
    <p class="acct-sub"><strong id="in-email"></strong></p>
    <div class="stat-row">
      <div class="stat"><b id="n-trees">0</b><span>trees</span></div>
      <div class="stat alt"><b id="n-cities">0</b><span>cities</span></div>
    </div>
    <p class="acct-sub" id="in-note">Your collected trees are saved on this device. The app brings them to all your devices.</p>
    <p class="acct-actions"><button type="button" id="signout" class="acct-link">Sign out</button></p>
    <p class="acct-actions"><button type="button" id="del-acct" class="acct-link danger">Delete my account</button></p>
  </section>
</main>
<script>
(function() {
  var SB = "SUPABASE_URL_TOKEN";
  var KEY = "SUPABASE_KEY_TOKEN";
  var states = ["st-signin", "st-sent", "st-expired", "st-in"];
  function show(id) {
    states.forEach(function(x) { document.getElementById(x).hidden = (x !== id); });
  }
  function mask(e) {
    var at = e.indexOf("@");
    if (at < 2) return e;
    return e[0] + "\u2022\u2022\u2022" + e.slice(at - 1);
  }
  var lastEmail = "";
  function sendLink(email, done) {
    fetch(SB + "/auth/v1/otp?redirect_to=" + encodeURIComponent(location.origin + location.pathname), {
      method: "POST",
      headers: { "apikey": KEY, "Content-Type": "application/json" },
      body: JSON.stringify({ email: email, create_user: true })
    }).then(function(r) { done(r.ok); }).catch(function() { done(false); });
  }
  var cooldown = null;
  function startCooldown() {
    var btn = document.getElementById("resend"), n = 30;
    btn.disabled = true;
    clearInterval(cooldown);
    cooldown = setInterval(function() {
      n--; document.getElementById("cool").textContent = n;
      if (n <= 0) { clearInterval(cooldown); btn.disabled = false; btn.textContent = "Resend link"; }
    }, 1000);
  }
  function localStats() {
    try {
      var seen = JSON.parse(localStorage.getItem("ancienttrees_seen")) || [];
      document.getElementById("n-trees").textContent = seen.length;
      var cities = {};
      seen.forEach(function(id) { cities[id.slice(0, 3)] = 1; });
      document.getElementById("n-cities").textContent = Object.keys(cities).length;
    } catch (e) {}
  }
  function signedIn(session) {
    try { localStorage.setItem("ancienttrees_session", JSON.stringify(session)); } catch (e) {}
    fetch(SB + "/auth/v1/user", { headers: { "apikey": KEY, "Authorization": "Bearer " + session.access_token } })
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(u) {
        if (u && u.email) document.getElementById("in-email").textContent = u.email;
      })
      .catch(function() {});
    localStats();
    show("st-in");
  }
  function parseHash() {
    var h = {};
    location.hash.slice(1).split("&").forEach(function(kv) {
      var p = kv.split("=");
      if (p[0]) h[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || "");
    });
    return h;
  }
  var h = parseHash();
  if (h.access_token) {
    history.replaceState(null, "", location.pathname);
    signedIn({
      access_token: h.access_token,
      refresh_token: h.refresh_token || "",
      expires_at: Math.floor(Date.now() / 1000) + parseInt(h.expires_in || "3600", 10)
    });
  } else if (h.error_code === "otp_expired" || h.error === "access_denied") {
    history.replaceState(null, "", location.pathname);
    show("st-expired");
  } else {
    try {
      var s = JSON.parse(localStorage.getItem("ancienttrees_session"));
      if (s && s.expires_at > Date.now() / 1000) signedIn(s);
    } catch (e) {}
  }
  document.getElementById("acct-form").addEventListener("submit", function(ev) {
    ev.preventDefault();
    var e = document.getElementById("acct-email").value.trim();
    if (!e) return;
    lastEmail = e;
    sendLink(e, function(ok) {
      if (ok) {
        document.getElementById("sent-to").textContent = mask(e);
        show("st-sent"); startCooldown();
      } else {
        document.getElementById("acct-email").setCustomValidity("That did not work; try again in a minute.");
        document.getElementById("acct-form").reportValidity();
        setTimeout(function() { document.getElementById("acct-email").setCustomValidity(""); }, 3000);
      }
    });
  });
  document.getElementById("change").addEventListener("click", function() { show("st-signin"); });
  document.getElementById("resend").addEventListener("click", function() {
    if (lastEmail) sendLink(lastEmail, function() {});
    startCooldown();
  });
  document.getElementById("re-expired").addEventListener("click", function() {
    if (lastEmail) { sendLink(lastEmail, function() {}); document.getElementById("sent-to").textContent = mask(lastEmail); }
    show(lastEmail ? "st-sent" : "st-signin"); if (lastEmail) startCooldown();
  });
  document.getElementById("signout").addEventListener("click", function() {
    try {
      var s = JSON.parse(localStorage.getItem("ancienttrees_session"));
      if (s) fetch(SB + "/auth/v1/logout", { method: "POST",
        headers: { "apikey": KEY, "Authorization": "Bearer " + s.access_token } }).catch(function() {});
    } catch (e) {}
    try { localStorage.removeItem("ancienttrees_session"); } catch (e) {}
    show("st-signin");
  });
  // Account deletion: calls the delete_user() SECURITY DEFINER function in
  // Supabase (runs as owner, deletes auth.users row for auth.uid() only).
  // Two clicks on purpose; no dialog dependency. The on-device collection in
  // ancienttrees_seen is deliberately left alone: it was never on the server.
  var delBtn = document.getElementById("del-acct");
  var delArmed = false;
  delBtn.addEventListener("click", function() {
    if (!delArmed) {
      delArmed = true;
      delBtn.textContent = "This permanently deletes your account and email. Click again to confirm.";
      return;
    }
    var s = null;
    try { s = JSON.parse(localStorage.getItem("ancienttrees_session")); } catch (e) {}
    if (!s) { show("st-signin"); return; }
    fetch(SB + "/rest/v1/rpc/delete_user", { method: "POST",
      headers: { "apikey": KEY, "Authorization": "Bearer " + s.access_token,
                 "Content-Type": "application/json" }, body: "{}" })
      .then(function(r) {
        if (r.ok) {
          try { localStorage.removeItem("ancienttrees_session"); } catch (e) {}
          delArmed = false;
          delBtn.textContent = "Delete my account";
          show("st-signin");
        } else {
          delBtn.textContent = "Deletion failed. Try again, or email us via the privacy page.";
        }
      })
      .catch(function() {
        delBtn.textContent = "Deletion failed (network). Try again.";
      });
  });
})();
</script>
"""
    body = body.replace("SUPABASE_URL_TOKEN", SUPABASE_URL).replace("SUPABASE_KEY_TOKEN", SUPABASE_KEY)
    page = render_page("Sign in to Ancient Trees", "Keep your tree collection on every device.",
                       f"{BASE_URL}/account", body,
                       head_extra='<meta name="robots" content="noindex, nofollow">',
                       rootpath="./")
    (DIST / "account.html").write_text(page)


def build_sitemap(pages):
    today = date.today().isoformat()
    urls = [canonical for _, _, canonical in pages if canonical]
    entries = "".join(
        f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls
    )
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}</urlset>\n'
    (DIST / "sitemap.xml").write_text(sitemap)
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")


def main():
    cities = load_cities()
    collections = load_collections()
    registers = load_registers()
    # Contract D: a draft (needs_curation) never gets linked publicly until
    # Hidde approves it. Only non-draft collections feed the homepage, city,
    # question and index pages; drafts still get their own page (see the
    # draft_collection_pages handling below), just unlinked and noindexed.
    public_collections = [c for c in collections if c.get("status") != "needs_curation"]
    species_intros = load_species_intros()
    global PHENOLOGY
    PHENOLOGY = load_phenology()
    check_phenology()
    check_species_names(cities)
    country_intros = load_country_intros()
    cities_by_slug = {c["slug"]: c for c in cities}
    pages = []  # (relative path, html, canonical or None)

    published = []
    upcoming = []
    tree_slugs = {}

    renderable = []
    for entry in cities:
        if entry["data"] and any(tree_is_renderable(t) for t in entry["data"].get("trees", [])):
            renderable.append(entry)
        elif entry["tier"] == 1:
            upcoming.append(entry)

    # Which species qualify for a page: 3+ renderable trees AND a hand-written intro.
    species_groups = group_trees_by_species(renderable)
    qualifying = {
        common: members for common, members in species_groups.items()
        if len(members) >= SPECIES_MIN_TREES and common in species_intros
    }
    species_pages = {common: species_intros[common]["slug"] for common in qualifying}

    # Which countries qualify for a page (Contract G): 3+ renderable cities AND
    # a hand-written intro. Known before any city page renders, so the city
    # breadcrumb can link its country in the same pass.
    country_counts = {}
    for e in renderable:
        country_counts[e["data"]["country"]] = country_counts.get(e["data"]["country"], 0) + 1
    country_pages = {
        c: country_intros[c]["slug"] for c in country_intros
        if country_counts.get(c, 0) >= COUNTRY_MIN_CITIES
    }
    city_slugs = {e["slug"] for e in renderable}
    for c, cslug in country_pages.items():
        if cslug in city_slugs:
            ERRORS.append(f"country slug {cslug!r} ({c}) collides with a city slug (Contract G)")

    for entry in renderable:
        trees = [t for t in entry["data"]["trees"] if tree_is_renderable(t)]
        for tree in trees:
            tree_slugs[tree["id"]] = build_tree_page(entry, tree, trees, pages, species_pages, country_pages)
        build_question_page(entry, public_collections, pages, country_pages)
        _FAVES = ["lisbon", "cadiz", "porto", "amsterdam", "kyoto",
                  "rome", "palermo", "paris", "london", "barcelona"]
        def _face(e):
            hero = e["data"].get("hero_tree_id")
            if hero:
                for t in e["data"]["trees"]:
                    if t["id"] == hero and usable_photo(t):
                        return thumb_url(usable_photo(t)["url"], 400)
            for t in e["data"]["trees"]:
                if usable_photo(t):
                    return thumb_url(usable_photo(t)["url"], 400)
            return None
        other_cities = [
            {"slug": e["slug"], "city": e["data"]["city"],
             "country": e["data"]["country"], "n": len(e["data"]["trees"]),
             "ph": _face(e),
             "rank": _FAVES.index(e["slug"]) if e["slug"] in _FAVES else 99,
             "lat": sum(t["location"]["latitude"] for t in e["data"]["trees"]) / len(e["data"]["trees"]),
             "lng": sum(t["location"]["longitude"] for t in e["data"]["trees"]) / len(e["data"]["trees"])}
            for e in renderable if e["slug"] != entry["slug"] and e["data"]["trees"]
        ]
        build_city_gpx(entry, trees, pages)
        result = build_city_page(entry, tree_slugs, public_collections, pages, other_cities,
                                 species_pages, country_pages)
        if result:
            published.append(result)

    draft_collection_pages = []
    for coll in collections:
        is_draft = coll.get("status") == "needs_curation"
        result = build_collection_page(coll, cities_by_slug, tree_slugs, published, pages, draft=is_draft)
        if is_draft:
            draft_collection_pages.append(result)
    build_collections_index(public_collections, published, pages, cities_by_slug)
    build_cities_index(published, pages, {e['slug']: city_face(e) for e in renderable})

    entries_by_slug = {e["slug"]: e for e in renderable}
    country_cards = []
    for country in sorted(country_pages):
        card = build_country_page(country_intros[country],
                                  [p for p in published if p["country"] == country],
                                  entries_by_slug, tree_slugs, published,
                                  public_collections, pages)
        if card:
            country_cards.append(card)
    if country_cards:
        country_cards.sort(key=lambda c: -c["trees"])
        build_countries_index(country_cards, published, pages)

    species_cards = []
    for common in sorted(qualifying, key=lambda c: -len(qualifying[c])):
        card = build_species_page(species_intros[common], qualifying[common],
                                  tree_slugs, published, pages)
        species_cards.append(card)
    if species_cards:
        build_species_index(species_cards, published, pages)

    # Parks and gardens (Contract H): a park earns a page at PARK_MIN_TREES
    # trees plus a hand-written intro, the same publish gate species pages use.
    park_intros = load_park_intros()
    park_groups = group_trees_by_park(renderable)
    park_cards, parks_unbuilt = [], []
    for (cslug, name), (entry, _nm, ptrees) in sorted(
            park_groups.items(), key=lambda kv: -len(kv[1][2])):
        if len(ptrees) >= PARK_MIN_TREES and (cslug, name) in park_intros:
            park_cards.append(build_park_page(park_intros[(cslug, name)], entry,
                                              ptrees, tree_slugs, published, pages))
        elif len(ptrees) >= PARK_MIN_TREES:
            # Qualifies on trees, has no intro yet, so it cannot ship (P3: no
            # templated copy). The reader is no longer told about it, so the
            # build tells US instead, or a park would wait forever unseen.
            parks_unbuilt.append((len(ptrees), entry["data"]["city"], name, cslug))
    if park_cards:
        build_parks_index(park_cards, parks_unbuilt, published, pages)
    if parks_unbuilt:
        print(f"\n  {len(parks_unbuilt)} park(s) have {PARK_MIN_TREES}+ trees and no intro yet "
              f"(write data/parks/<slug>.json to publish):")
        for n, city, name, _cs in sorted(parks_unbuilt, reverse=True):
            print(f"    {n} trees  {city}: {name}")

    build_contribute_page(published, pages)
    build_privacy_page(pages)
    build_fakedoor_pages(pages)
    # The register layer is on again (Hidde, 2026-08-05: "zet de tweede
    # kaartlaag maar aan, ik ben benieuwd hoe het eruit ziet en het kan me
    # inspireren hoe dan te ontwerpen"). He switched it off on 2026-07-31
    # because the interaction was not right, and that objection still stands:
    # this is grey dots to look at and think about, not a finished design.
    # Two things keep it honest meanwhile. It appears only from zoom 8, so the
    # world map stays our own verified trees rather than a haze over Europe,
    # and it is fetched as assets/registers.json rather than inlined, because
    # 6,266 dots have no business being the heaviest thing on the page.
    build_explore_page(renderable, pages, registers=registers)
    build_in_season_page(renderable, tree_slugs, pages)
    species_slugs = sorted((common, slugify(common)) for common in qualifying) if qualifying else []
    build_homepage(published, upcoming, public_collections, pages,
                   renderable=renderable, species_slugs=species_slugs)
    build_redirects(published, pages, tree_slugs)
    validate_internal_links(pages)

    if ERRORS:
        print(f"BUILD FAILED: {len(ERRORS)} contract violation(s), nothing deployed\n")
        for e in ERRORS:
            print(f"  - {e}")
        sys.exit(1)

    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "assets").mkdir(parents=True)
    (DIST / "assets" / "style.css").write_text(CSS)
    # Written here, not while the page is built: DIST is wiped and recreated
    # at this point, so anything written earlier disappears.
    if REGISTER_ASSET:
        (DIST / "assets" / "registers.json").write_text(REGISTER_ASSET)
    # Custom domain for GitHub Pages; must survive every rebuild.
    (DIST / "CNAME").write_text(CUSTOM_DOMAIN + "\n")
    # One shared index behind the one search interaction on home and /explore.
    # Places first, then species, then individual trees, because that is what
    # people actually type: our own Search Console queries are almost entirely
    # place-shaped ("amsterdam trees", "albero roma", "york museum gardens")
    # and only rarely a tree by name (Hidde, 2026-08-04).
    search_index = {"c": [], "k": [], "s": [], "t": []}
    for entry in renderable:
        d = entry["data"]
        search_index["c"].append({"city": d["city"], "country": d["country"],
                                  "n": len(d["trees"]), "u": entry["slug"]})
        for t in d["trees"]:
            search_index["t"].append({"n": t["name"], "c": d["city"],
                                      "u": f"{entry['slug']}/{slugify(t['name'])}"})
    for country, cslug in sorted(country_pages.items()):
        n_cities = sum(1 for e in renderable if e["data"]["country"] == country)
        n_trees = sum(len(e["data"]["trees"]) for e in renderable
                      if e["data"]["country"] == country)
        search_index["k"].append({"country": country, "cities": n_cities,
                                  "n": n_trees, "u": cslug})
    for common in sorted(qualifying, key=lambda c: -len(qualifying[c])):
        search_index["s"].append({"n": common, "count": len(qualifying[common]),
                                  "u": f"species/{species_intros[common]['slug']}"})
    (DIST / "search-index.json").write_text(json.dumps(search_index))
    for relpath, content, _ in pages:
        out = DIST / relpath
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content)
    build_sitemap(pages)
    # After the wipe and the sitemap on purpose: the account prototype exists
    # on disk but not in the sitemap, unlinked and noindexed (AUTH_ENABLED).
    build_account_page()
    # Same pattern for collection drafts (Contract D): on disk at a stable
    # URL for review, noindexed, kept out of the sitemap and every nav link.
    if draft_collection_pages:
        (DIST / "collections").mkdir(parents=True, exist_ok=True)
        for slug, draft_page in draft_collection_pages:
            (DIST / "collections" / f"{slug}.html").write_text(draft_page)

    n_trees = sum(p["count"] for p in published)
    print(f"Built {len(pages)} page(s) into {DIST}: "
          f"{len(published)} city, {n_trees} tree, {len(published)} question, "
          f"{len(public_collections)} public collection(s), "
          f"{len(draft_collection_pages)} draft collection(s) (unlinked, needs_curation), "
          f"homepage. All contracts validated.")
    for p in published:
        print(f"  - {p['city']}: {p['count']} trees")


if __name__ == "__main__":
    main()
