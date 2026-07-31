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
.sc-chip { font-family: var(--sans); font-size: 11px; font-weight: 600; color: var(--moss);
  border: 1px solid var(--moss); border-radius: 999px; padding: 1px 8px 1px 6px; text-transform: capitalize;
  display: inline-flex; align-items: center; gap: 4px; }
.sc-chip svg { width: 13px; height: 13px; flex-shrink: 0; }
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
.explore-page { display: flex; flex-direction: column; height: calc(100vh - var(--header-h)); margin-top: var(--header-h); }
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
.exc-empty { font-size: 13px; color: var(--ink-mid); padding: 0.5rem; }
@media (max-width: 800px) {
  .explore-split { flex-direction: column-reverse; }
  .ex-panel { width: 100%; height: 38vh; border-right: none; border-top: 1px solid var(--cream-dark); }
}
.explore-head { padding: 1.1rem 2rem 0.9rem; display: grid; grid-template-columns: 1fr auto; gap: 0.2rem 1.5rem; align-items: center; }
.explore-head h1 { font-size: 1.45rem; font-weight: 800; letter-spacing: -0.015em; }
.explore-head p { font-size: 13px; color: var(--ink-mid); margin-top: 0.2rem; max-width: 46rem; grid-column: 1; }
.ex-search { grid-column: 2; grid-row: 1 / span 2; display: flex; align-items: center; gap: 0.5rem; background: #fff; border: 1px solid var(--cream-dark); border-radius: 999px; padding: 0.55rem 1rem; min-width: 16rem; box-shadow: var(--shadow); }
.ex-search svg { width: 16px; height: 16px; color: var(--ink-mid); flex-shrink: 0; }
.ex-search input { border: none; outline: none; font-family: var(--sans); font-size: 13.5px; width: 100%; background: transparent; }
@media (max-width: 800px) {
  .explore-head { grid-template-columns: 1fr; }
  .explore-head p { display: none; }
  .ex-search { grid-column: 1; grid-row: auto; min-width: 0; margin-top: 0.4rem; }
}
.explore-now-chip { display: inline-block; background: #F3E4C3; color: #8A6414; font-weight: 700; font-size: 11.5px; border-radius: 999px; padding: 2px 10px; margin-left: 0.4rem; }
.explore-map { flex: 1; min-height: 320px; }
.pop-now { background: #F3E4C3; color: #8A6414; font-weight: 700; font-size: 10px; border-radius: 999px; padding: 1px 8px; }
.appland { position: relative; min-height: calc(100vh - var(--header-h)); display: flex; align-items: center; justify-content: center; padding: 2.5rem 1rem; }
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
.home-hero.poster { position: relative; height: min(78vh, 680px); min-height: 480px; }
.home-hero.poster .hero-bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.hero-scrim { position: absolute; inset: 0; background: linear-gradient(rgba(22,28,15,0.30), rgba(22,28,15,0.55)); pointer-events: none; z-index: 1; }
.hero-center { position: absolute; inset: 0; z-index: 2; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 1rem; pointer-events: none; }
.hero-center > * { pointer-events: auto; }
.hero-center h1 { color: #fff; font-size: clamp(2.1rem, 5.5vw, 3.8rem); font-weight: 800; letter-spacing: -0.02em; line-height: 1.08; margin-bottom: 1.4rem; text-shadow: 0 2px 18px rgba(0,0,0,0.35); }
.hero-center h1 em { color: #F0C876; font-style: normal; }
.poster-search { width: min(640px, 94vw); background: #fff; border-radius: 999px; padding: 0.35rem 0.6rem 0.35rem 0.4rem; align-items: center; gap: 0.15rem; box-shadow: 0 10px 40px rgba(0,0,0,0.28); margin-top: 0; }
.poster-search .search-ico { display: inline-flex; align-items: center; justify-content: center; width: 42px; height: 42px; border: none; background: transparent; color: var(--ink-light); cursor: pointer; }
.poster-search .search-ico svg { width: 20px; height: 20px; }
.poster-search input { border: none; border-radius: 999px; flex: 1; font-size: 16.5px; padding: 0.65rem 0.5rem; }
.poster-search input:focus { outline: none; }
.hero-links { display: flex; gap: 1.8rem; margin-top: 1.3rem; flex-wrap: wrap; justify-content: center; }
.hero-link { background: none; border: none; cursor: pointer; font-family: inherit; color: #fff; font-size: 15.5px; font-weight: 700; text-decoration: underline; text-underline-offset: 4px; }
.home-hero.poster .near-me-result { color: #fff; font-weight: 600; margin-top: 0.9rem; text-shadow: 0 1px 8px rgba(0,0,0,0.4); }
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
.pin-tree { position: relative; width: 44px; height: 44px; border-radius: 50%; background: var(--cream);
  border: 2px solid var(--moss); box-shadow: 0 3px 10px rgba(26,26,20,0.28); cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: transform 0.18s ease, box-shadow 0.18s ease; }
.pin-tree svg { width: 28px; height: 28px; color: var(--moss); transition: color 0.18s ease; }
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
.route-bar { position: absolute; left: 1rem; bottom: 1.6rem; z-index: 5;
  display: flex; gap: 0.5rem; align-items: stretch;
  width: calc(100% - 2rem); max-width: 420px; }
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
  .nav-drop { margin-left: 0; }
  .nav-drop summary { font-size: 13px; padding: 0.35rem 0.2rem; }
  .nav-drop summary .sum-desktop { display: none; }
  .nav-drop summary .sum-mobile { display: inline; }
  .nav-drop-menu { position: fixed; left: 0.75rem; right: 0.75rem; top: 3.4rem; min-width: 0; }
  .bar-links a.bar-cta { padding: 0.35rem 0.6rem; font-size: 12px; white-space: nowrap; }
  .footer-cols { flex-direction: column; gap: 1.5rem; }
  .action-row .go-btn, .action-row .seen-btn { font-size: 13px; padding: 0.6rem 0.9rem; }

  .route-bar { position: fixed; left: 0.75rem; right: 0.75rem;
    bottom: calc(0.75rem + env(safe-area-inset-bottom)); }
  /* The fixed bar would otherwise sit on top of the last tree in the list. */
  .panel { padding-bottom: calc(6rem + env(safe-area-inset-bottom)); }
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
  .stage { position: sticky; top: var(--header-h); height: 32vh; min-height: 200px; z-index: 5; }
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
  <nav class="bar-links"><a href="%%ROOTPATH%%explore" class="only-desktop">Map</a><details class="nav-drop"><summary><span class="sum-desktop">Explore</span><span class="sum-mobile">Menu</span></summary><div class="nav-drop-menu"><a href="%%ROOTPATH%%explore" class="only-mobile"><span class="mi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.6"/></svg></span>Map</a><a href="%%ROOTPATH%%cities"><span class="mi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 21V8l5-3v16M9 21V10l6 2v9M15 21V7l5 2v12"/><path d="M2 21h20"/></svg></span>Cities</a><a href="%%ROOTPATH%%species"><span class="mi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20C6 10 12 4 20 4c0 8-6 14-16 16z"/><path d="M4 20c4-6 8-9 12-11"/></svg></span>Species</a><a href="%%ROOTPATH%%collections"><span class="mi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 4h12a1 1 0 0 1 1 1v16l-7-4-7 4V5a1 1 0 0 1 1-1z"/></svg></span>Collections</a><a href="%%ROOTPATH%%contribute"><span class="mi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/></svg></span>Suggest a tree</a>%%LOGIN_MENU%%</div></details>%%LOGIN%%<a href="%%ROOTPATH%%app" class="bar-cta">Get the app</a></nav>
</header>
%%BODY%%
%%FOOTER%%
%%SCRIPTS%%
%%ANALYTICS%%
</body>
</html>
"""

# Cloudflare Web Analytics: cookieless and aggregate only, so no consent banner
# and no personal data. Chosen over Google Analytics on 2026-07-21 for exactly
# that reason: a consent popup is friction on the street, which is where this
# site has to work. Empty string switches it off everywhere.
ANALYTICS_TOKEN = "fcbbfb8b426c4f6aa2066b00be6454f6"

ANALYTICS_SNIPPET = (
    "<script defer src='https://static.cloudflareinsights.com/beacon.min.js' "
    "data-cf-beacon='{{\"token\": \"{token}\"}}'></script>"
)

FOOTER = """
<footer>
  <div class="footer-cols">
    <div class="footer-col footer-about">
      <span class="footer-logo">Ancient Trees</span>
      <p>The remarkable old trees of the world's great cities: found, verified and mapped, ten per city and never padded. See the ones near you, walk a route past a few, and collect the ones you have stood in front of.</p>
    </div>
    <div class="footer-col">
      <h4>Explore</h4>
      <a href="%%ROOTPATH%%explore">Map</a>
      <a href="%%ROOTPATH%%in-season">In season now</a>
      <a href="%%ROOTPATH%%cities">Cities</a>
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
  <span class="footer-note">&copy; %%YEAR%% Ancient Trees, ancienttrees.app. Map &copy; OpenFreeMap, OpenMapTiles, OpenStreetMap contributors. Photos carry their own credits and open licences.</span>
</footer>
"""

ERRORS = []


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
    m = re.match(r"([\d,]+\+?)", tree.get("age_estimate", ""))
    return m.group(1) if m else str(tree.get("age_min", ""))


def species_common(tree):
    return tree.get("species", "").split(" (")[0]


def meta_from_story(story):
    """Build a meta description from the story's opening sentences, max DESC_MAX."""
    sentences = re.split(r"(?<=[.!?]) ", story)
    out = ""
    for s in sentences:
        if out and len(out) + 1 + len(s) > DESC_MAX:
            break
        out = (out + " " + s).strip()
        if len(out) > DESC_MAX:
            out = out[:DESC_MAX].rsplit(" ", 1)[0].rstrip(",.;:")
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
    "flowers": '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="2" fill="currentColor"/><g fill="currentColor" opacity=".55"><ellipse cx="8" cy="3.4" rx="2" ry="2.6"/><ellipse cx="12.4" cy="6.6" rx="2" ry="2.6" transform="rotate(72 12.4 6.6)"/><ellipse cx="10.7" cy="12" rx="2" ry="2.6" transform="rotate(144 10.7 12)"/><ellipse cx="5.3" cy="12" rx="2" ry="2.6" transform="rotate(216 5.3 12)"/><ellipse cx="3.6" cy="6.6" rx="2" ry="2.6" transform="rotate(288 3.6 6.6)"/></g></svg>',
    "fruit": '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="6" cy="10" r="4" fill="currentColor" opacity=".75"/><circle cx="11" cy="8" r="3.2" fill="currentColor" opacity=".5"/><path d="M6 6 Q7 3 9.5 2.5" stroke="currentColor" stroke-width="1.3" fill="none" stroke-linecap="round"/></svg>',
    "autumn colour": '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5 C11.5 4 13.5 7 13.5 10 A5.5 5.5 0 0 1 2.5 10 C2.5 7 4.5 4 8 1.5z" fill="currentColor" opacity=".7"/><path d="M8 4 v9" stroke="currentColor" stroke-width="1.1"/></svg>',
    "catkins": '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 3 q2 -1 5 -1 q4 0 6 1" stroke="currentColor" stroke-width="1.3" fill="none" stroke-linecap="round"/><path d="M5 3.5 q-.5 4 .5 7 M8 3 q0 5 1 9 M11.5 3.5 q.5 3.5 -.3 6.5" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round" opacity=".65"/></svg>',
    "fresh leaves": '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M13 3 C8 3 4.5 6 4 11 c4.5.5 8-2 9-8z" fill="currentColor" opacity=".65"/><path d="M4.5 13 C6 9.5 9 6.5 12.5 4.5" stroke="currentColor" stroke-width="1.2" fill="none" stroke-linecap="round"/></svg>',
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

    # Month labels, every other one to keep it clean at this width.
    ticks = "".join(
        f'<text x="{pts[i][0]:.1f}" y="{H - 6:.0f}" class="sc-m">{MONTH_ABBR[i]}</text>'
        for i in range(0, 12, 2)
    )

    now_marker = (
        f'<line x1="{now_x:.1f}" y1="{pad_t - 6:.1f}" x2="{now_x:.1f}" y2="{pad_t + plot_h:.1f}" class="sc-now"/>'
        f'<text x="{now_x:.1f}" y="{pad_t - 10:.1f}" class="sc-nowlabel">now</text>'
    )

    kind = season_kind(bt)
    chip = (f'<span class="sc-chip">{KIND_ICONS[kind]}{esc(kind)}</span>'
            if kind else "")
    now_badge = '<span class="best-now">at its best right now</span>' if in_season else ""

    return f"""
<figure class="season">
  <figcaption class="season-head">
    <span>Best time to visit</span>{chip}{now_badge}
  </figcaption>
  <svg viewBox="0 0 {W:.0f} {H:.0f}" class="season-svg" role="img" aria-label="Seasonal peak: {esc(bt['label'])}">
    <path d="{area}" class="sc-area"/>
    <path d="{line}" class="sc-line"/>
    {now_marker}
    <circle cx="{peak_x:.1f}" cy="{peak_y:.1f}" r="4.5" class="sc-peak"/>
    {ticks}
  </svg>
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
    for i, (name, url) in enumerate(items, 1):
        item = url or page_url
        if not item:
            # Catch it at build time rather than weeks later in Search Console.
            ERRORS.append(f"breadcrumb crumb {name!r} has no item URL and no page_url fallback")
        el = {"@type": "ListItem", "position": i, "name": name, "item": item}
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


def city_map_script(markers, center, route=None, other_cities=None):
    data = json.dumps(markers)
    route_coords = json.dumps(
        [[markers[i]["lng"], markers[i]["lat"]] for i in route["order"]]
        if route and len(markers) > 1 else []
    )
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
  if (!chooserOn && z <= 9.5) {{ chooserOn = true; }}
  else if (chooserOn && z >= 10.5) {{ chooserOn = false; }}
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
map.on('moveend', updatePanelMode);
if (markers.length > 1) {{
  var _b = new maplibregl.LngLatBounds();
  markers.forEach(function(m) {{ _b.extend([m.lng, m.lat]); }});
  var _el = document.getElementById('map');
  var _pad = Math.max(30, Math.min(90, Math.floor(Math.min(_el.clientWidth, _el.clientHeight) * 0.16)));
  map.fitBounds(_b, {{ padding: _pad, maxZoom: 14.5, duration: 0 }});
}}

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
    id: 'walk', type: 'line', source: 'walk',
    layout: {{ 'line-cap': 'round', 'line-join': 'round' }},
    paint: {{ 'line-color': '#3D5C1E', 'line-width': 2.5, 'line-opacity': 0.5, 'line-dasharray': [1.5, 2] }}
  }});
}}
if (map.isStyleLoaded()) {{ addWalkLayer(); }} else {{ map.on('styledata', addWalkLayer); }}

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


def home_hero_script(markers, tree_index):
    """The photo-hero homepage script: search only. The map lives at /explore;
    location is asked THERE, in map context, never from the homepage (Hidde,
    2026-07-29: a location prompt from a hero link "slaat nergens op"). Search
    resolves cities first, then tree names."""
    data = json.dumps(markers)
    trees = json.dumps(tree_index)
    return """
<script>
var markers = __CITIES__;
var TREES = __TREES__;
var moreBtn = document.getElementById('more-cities-btn');
if (moreBtn) {
  moreBtn.addEventListener('click', function() {
    document.getElementById('more-cities').hidden = false;
    moreBtn.remove();
  });
}
var sf = document.getElementById('city-search');
if (sf) {
  sf.addEventListener('submit', function(e) {
    e.preventDefault();
    var q = document.getElementById('city-q').value.trim().toLowerCase();
    if (!q) return;
    var hit = markers.find(function(m) { return m.city.toLowerCase() === q; }) ||
              markers.find(function(m) { return m.city.toLowerCase().indexOf(q) === 0; });
    if (hit) { window.location.href = hit.url; return; }
    var tree = TREES.find(function(t) { return t.n.toLowerCase() === q; }) ||
               TREES.find(function(t) { return t.n.toLowerCase().indexOf(q) !== -1; });
    if (tree) { window.location.href = tree.u; return; }
    hit = markers.find(function(m) { return m.city.toLowerCase().indexOf(q) !== -1; });
    if (hit) { window.location.href = hit.url; return; }
    document.getElementById('search-note').innerHTML =
      'Not mapped yet. <a href="contribute">Be the first to map it</a>, or <a href="explore">browse the map</a>.';
  });
}
</script>
""".replace("__CITIES__", data).replace("__TREES__", trees)


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


def usable_photo(tree):
    """Return the photo dict if it has a URL, license and attribution and is
    cleared for display; otherwise None. One gate for every page type."""
    photo = tree.get("photo") or {}
    if (photo.get("url") and photo.get("license") and photo.get("attribution")
            and photo.get("status") in ("approved", "found_needs_check")):
        # A Commons File: page is HTML, not an image; it renders as a broken
        # img. Shipped five times before this check existed.
        if "/wiki/File:" in photo["url"]:
            ERRORS.append(f"{tree.get('id')}: photo url is a wiki File: page, not an image file")
            return None
        return photo
    return None


def load_cities():
    city_list = json.loads((DATA / "city-list.json").read_text())["cities"]
    for entry in city_list:
        f = DATA / "cities" / f"{entry['slug']}.json"
        entry["data"] = json.loads(f.read_text()) if f.exists() else None
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
    bulk inventory) and only the licence this project verified as commercial-reuse-safe."""
    reg_dir = DATA / "registers"
    if not reg_dir.exists():
        return []
    out = []
    for f in sorted(reg_dir.glob("*.json")):
        d = json.loads(f.read_text())
        for t in d.get("trees", []):
            out.append({
                "name": t.get("name_en") or t["name_ja"],
                # English display area falls back to the raw field rather than
                # hiding a tree a translation was missed for (P7: say what you
                # know honestly, never blank).
                "area": t.get("area_en") or t.get("area", ""),
                "prefecture": d["prefecture"],
                "designation": f"{d['prefecture']} Natural Monument",
                "lat": t["latitude"],
                "lng": t["longitude"],
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


def group_trees_by_species(renderable):
    """common_name -> list of (city_entry, tree), preserving city order then age."""
    groups = {}
    for entry in renderable:
        trees = [t for t in entry["data"]["trees"] if tree_is_renderable(t)]
        for t in trees:
            groups.setdefault(species_common(t), []).append((entry, t))
    return groups


SPECIES_MIN_TREES = 3


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


def build_tree_page(city_entry, tree, all_trees, pages, species_pages=None):
    species_pages = species_pages or {}
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

    crumb_items = [
        ("Home", BASE_URL),
        (country, None),
        (city, f"{BASE_URL}/{cslug}"),
        (tree["name"], None),
    ]

    photo = usable_photo(tree)
    photo_html = ""
    og_image = ""
    if photo:
        photo_html = f"""
  <figure class="tree-photo">
    <img {img_srcset(photo['url'], [700, 1100, 1600], "(max-width: 800px) 100vw, 760px")} alt="{esc(tree['name'])}" loading="lazy">
    <figcaption>Photo: {esc(photo['attribution'])} ({esc(photo['license'])})</figcaption>
  </figure>"""
        og_image = f'\n<meta property="og:image" content="{esc(thumb_url(photo["url"], 1200))}">'

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
    season_html = season_curve(tree)

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
    # approximate warning earns a chip. The season story lives in the Best
    # time block below, not as an unexplained label up top.
    precision_chip = ('<span class="chip approx">pin approximate</span>'
                      if location_is_approximate(tree) else '')
    chips = (f'<p class="chip-row"><span class="chip">{esc(tree.get("age_estimate", "age unknown"))}</span>'
             f'<span class="chip">{esc(species_common(tree))}</span>{precision_chip}</p>')
    action_row = f"""
  <div class="action-row">
    <a class="go-btn" href="../app">Check in with the app</a>
    <a class="go-btn ghost" href="https://www.google.com/maps/dir/?api=1&amp;destination={loc['latitude']},{loc['longitude']}" target="_blank" rel="noopener">Take me there</a>
    <a class="action-link" href="../{cslug}#walk">Walk more trees in {esc(city)}</a>
  </div>"""

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
  <p class="go-note">The buttons above open directions and check-ins. {esc(tree.get('transport', ''))}</p>
  {approx_note}
  {facts}
  <h2>Trees nearby</h2>
  <div class="near-cards">{near_cards}</div>
  <div class="cta">Curious what else is standing in {esc(city)}? See <a href="../{cslug}">all {len(all_trees)} remarkable ancient trees in {esc(city)}</a> or find out <a href="oldest-tree">what the oldest tree in {esc(city)} is</a>.{species_line}</div>
  <div class="report"><strong>Help keep this page true.</strong>
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
    scripts = single_pin_script(loc["latitude"], loc["longitude"])

    check_links(canonical, 2 + len(nearby), 4)

    page = render_page(title, description, canonical, body, head_extra, scripts, rootpath)
    pages.append((f"{cslug}/{tslug}.html", page, canonical))
    return tslug


# ------------------------------------------------------------ question pages

def build_question_page(city_entry, collections, pages):
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
                   "de", "del", "della", "der", "du", "la", "le", "el", "van", "dos",
                   "das", "do", "di", "san", "santa"}
        tokens = [w for w in re.findall(r"[A-Za-z']+", old["name"])
                  if w[0].isupper() and w.lower() not in generic]
        if tokens and not any(t.lower() in answer.lower() for t in tokens):
            ERRORS.append(f"{canonical}: question_answer never mentions {old['name']!r} "
                          f"(looked for {tokens}); set oldest_tree_id or rewrite the answer")
        if not (150 <= len(context.split()) <= 200):
            ERRORS.append(f"{canonical}: question_context is {len(context.split())} words, Contract B requires 150-200")

    crumb_items = [
        ("Home", BASE_URL),
        (country, None),
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

def build_city_page(entry, tree_slugs, collections, pages, other_cities=(), species_pages=None):
    species_pages = species_pages or {}
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
    intro = city_data.get("intro")
    if not intro:
        ERRORS.append(f"{canonical}: city intro (60-100 words, unique) is required by Contract C")
        intro = ""
    elif not (60 <= len(intro.split()) <= 100):
        ERRORS.append(f"{canonical}: city intro is {len(intro.split())} words, Contract C requires 60-100")

    crumb_items = [("Home", BASE_URL), (country, None), (city, None)]

    cards = []
    markers = []
    for i, t in enumerate(trees, 1):
        loc = t["location"]
        tslug = tree_slugs[t["id"]]
        label = f'<span class="tree-label">{esc(t["label"])}</span>' if t.get("label") else ""
        cphoto = usable_photo(t)
        photo_block = ""
        if cphoto:
            photo_block = f"""
      <div class="tree-card-photo"><img {img_srcset(cphoto['url'], [500, 900], "(max-width: 800px) 100vw, 560px")} alt="{esc(t['name'])}" loading="lazy"></div>
      <p class="tree-card-credit">Photo: {esc(cphoto['attribution'])} ({esc(cphoto['license'])})</p>"""
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
                        "icon": species_icon(t), "name": t["name"], "id": t["id"]})

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
      <p class="subtle-suggest">Know an ancient tree in {esc(city)} we missed? <a href="{submit_link('tree')}">Suggest it</a>.</p>
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

    # The walk, worked out at build time so a phone never has to compute it.
    route = plan_walking_route([(m["lat"], m["lng"]) for m in markers])
    route_bar = ""
    if route:
        route_url = maps_route_url([(markers[i]["lat"], markers[i]["lng"])
                                    for i in route["order"]])
        hours, mins = divmod(route["minutes"], 60)
        if hours and mins:
            duration = f"{hours}h {mins}m"
        elif hours:
            duration = "1 hour" if hours == 1 else f"{hours} hours"
        else:
            duration = f"{mins} min"
        # Says which trees and how far, because someone who discovers halfway
        # that this was never the full ten is someone we lost.
        label = (f"Walk {route['count']} of these trees"
                 if route["count"] < route["of"] else f"Walk all {route['count']} trees")
        route_bar = f"""
    <div class="route-bar" id="walk">
      <a class="route-go" href="{esc(route_url)}" target="_blank" rel="noopener">
        {label}
        <span class="route-meta">about {route['km']} km, {duration} on foot</span>
      </a>
      <button type="button" class="route-gps" id="gps-btn" aria-pressed="false">Where am I</button>
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
    scripts = city_map_script(markers, (avg_lat, avg_lng), route, other_cities)

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
    title = fit_title([coll["title"]], canonical)
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
        sections.append(f'<h2>{esc(entry["data"]["city"])}</h2>{"".join(rows)}')

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
    return {"slug": slug, "common": common, "scientific": intro_data.get("scientific_name", ""),
            "count": n, "cities": len(by_city)}


def build_species_index(species_cards, published, pages):
    canonical = f"{BASE_URL}/species"
    rootpath = "./"
    title = fit_title(["Ancient Trees by Species", "Browse Ancient Trees by Species"], canonical)
    description = ("Browse the mapped trees by species: the London plane that lines half of "
                  "Europe's streets, the wingnut Amsterdam went to court over, and more.")
    crumb_items = [("Home", BASE_URL), ("Species", None)]

    entries = "".join(
        f"""
      <div class="entry">
        <h3><a href="species/{c['slug']}">{esc(c['common'])}</a> <span class="tree-label">{c['count']} trees</span></h3>
        <p><em>{esc(c['scientific'])}</em>. Mapped across {c['cities']} cit{'y' if c['cities']==1 else 'ies'} so far.</p>
      </div>"""
        for c in species_cards
    )
    city_links = " &middot; ".join(
        f'<a href="{p["slug"]}">{esc(p["city"])}</a>' for p in published
    )
    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>Ancient Trees by Species</h1>
  <div class="prose-block"><p>Cities group these trees by place; collections group them by theme. This page groups them by what they actually are. A species earns a page once the site has mapped at least three of them, so every list here has real depth rather than a lone specimen. More species appear as new cities join the map.</p></div>
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


def build_cities_index(published, pages):
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
    groups = "".join(
        '<div class="dir-group"><h3>%s</h3>%s</div>' % (
            esc(country),
            "".join('<a href="%s">%s <span class="dir-count">%d</span></a>'
                    % (p["slug"], esc(p["city"]), p["count"])
                    for p in sorted(cities, key=lambda x: x["city"])))
        for country, cities in sorted(by_country.items()))
    total = sum(p["count"] for p in published)
    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>Every city we have mapped</h1>
  <p class="answer-first">{len(published)} cities, {total} trees, each one verified and placed. Pick a city for its trees, or open <a href="explore">the map</a> to see what is near you.</p>
  <div class="dir-cols">{groups}</div>
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


def build_collections_index(collections, published, pages):
    """Overview of all collections at /collections."""
    canonical = f"{BASE_URL}/collections"
    rootpath = "./"
    title = fit_title(["Collections: Remarkable Trees by Theme"], canonical)
    description = ("Hand-curated lists that cut across cities: the oldest, the strangest, "
                   "the ones worth a detour. Every entry links to a verified tree.")

    crumb_items = [("Home", BASE_URL), ("Collections", None)]

    entries = []
    for c in collections:
        first_sentence = c["intro"].split(". ")[0] + "."
        entries.append(f"""
      <div class="entry">
        <h3><a href="collections/{c['slug']}">{esc(c['title'])}</a></h3>
        <p>{esc(first_sentence)} {len(c.get('entries', []))} trees, across {len({e['city_slug'] for e in c.get('entries', [])})} cities.</p>
      </div>""")

    city_links = " &middot; ".join(
        f'<a href="{p["slug"]}">{esc(p["city"])}</a>' for p in published
    )

    entries_html = "".join(entries) if entries else (
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
    body = """
<main class="content-page">
  <h1>Privacy</h1>
  <div class="prose-block">
    <p>Ancient Trees is a small independent project. This page describes what data the site handles.</p>
    <h2>Browsing</h2>
    <p>Every page works without an account. The site uses a cookieless visit counter (Cloudflare Web Analytics) that records aggregate page views only; it sets no cookies and cannot identify you. Map tiles load from OpenFreeMap and photos from Wikimedia Commons; those requests reach their servers the way any image on the web does.</p>
    <h2>With an account (once sign-in opens)</h2>
    <p>Signing in stores two things: your email address and your tree collection. The address is used for sign-in links and account service, nothing else. This data is stored with Supabase, on servers in the EU (Frankfurt).</p>
    <p>Two forms store what you type into them, in the same EU database: the app waitlist keeps your email address, used to email you when the app is ready; a tree suggestion keeps what you wrote, including the name you optionally leave for credit. Want either removed? Use the contact address below.</p>
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
      <h1>The walk in your pocket</h1>
      <p class="appland-sub">The website finds the trees. The app we are building is for the walk itself, and there is nothing to download yet; this page is what it will be, and how to hear it first.</p>
      <ol class="appland-steps">
        <li><span class="step-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16v12H4z"/><path d="m4 7 8 6 8-6"/></svg></span><div><strong>Today:</strong> leave your email through the form, with the word "app"</div></li>
        <li><span class="step-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="9" rx="6" ry="5"/><path d="M11.4 20h1.2l-.3-7h-.6z"/></svg></span><div><strong>Meanwhile:</strong> we build, and the site already works well on your phone</div></li>
        <li><span class="step-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.7 5.5 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.8 1-6.1L3.2 9.4l6.1-.9z"/></svg></span><div><strong>Launch day:</strong> you hear it first, before anyone else</div></li>
      </ol>
      <form class="waitlist" id="waitlist">
        <input type="email" id="wl-email" placeholder="you@example.com" aria-label="Your email address" required>
        <button type="submit" class="appland-cta">Keep me posted</button>
      </form>
      <p class="waitlist-note" id="wl-note">We will email you when the app is ready.</p>
    </div>
    <div class="appland-right">
      <h2>The app is going to include</h2>
      <div class="appland-feat"><span class="feat-tile"><svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="22" r="14" fill="none" stroke="#4A6B2A" stroke-width="3"/><circle cx="24" cy="22" r="4" fill="#D9A13F"/><path d="M24 4 v6 M24 34 v6 M6 22 h6 M36 22 h6" stroke="#4A6B2A" stroke-width="2.6" stroke-linecap="round"/></svg></span><div><h3>The trees around you, live</h3><p>Open it anywhere and see the remarkable old trees near you, the nearest one a walk-time away.</p></div></div>
      <div class="appland-feat"><span class="feat-tile"><svg viewBox="0 0 48 48" aria-hidden="true"><ellipse cx="24" cy="19" rx="12" ry="10" fill="#3A5222"/><circle cx="17" cy="18" r="7" fill="#4A6B2A"/><circle cx="31" cy="18" r="7" fill="#4A6B2A"/><circle cx="24" cy="11" r="7" fill="#5B7F35"/><path d="M22.9 40h2.4l-.6-13h-1.2z" fill="#6B4F33"/><circle cx="36" cy="34" r="8" fill="#D9A13F"/><path d="M32.5 34 l2.5 2.5 5 -5" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span><div><h3>Check in at the trunk</h3><p>Stand before a tree and collect it; your collection counts in years of living history.</p></div></div>
      <div class="appland-feat"><span class="feat-tile"><svg viewBox="0 0 48 48" aria-hidden="true"><path d="M12 30 a10 10 0 0 1 2 -19 a12 12 0 0 1 22 3 a8 8 0 0 1 0 16 z" fill="#ECEDE2" stroke="#4A6B2A" stroke-width="2.5"/><path d="M18 36 l-3 5 M26 36 l-3 5 M34 36 l-3 5" stroke="#4A6B2A" stroke-width="2.6" stroke-linecap="round"/></svg></span><div><h3>Works where wifi does not</h3><p>A whole city in your pocket before you leave the hotel; no roaming required.</p></div></div>
      <div class="appland-feat"><span class="feat-tile"><svg viewBox="0 0 48 48" aria-hidden="true"><ellipse cx="20" cy="18" rx="10" ry="8" fill="#D9A13F"/><circle cx="15" cy="16" r="4.5" fill="#E8BC63"/><path d="M19 36h2.4l-.6-12h-1.2z" fill="#6B4F33"/><path d="M33 10 a10 10 0 0 1 5 9 M35.5 6 a15 15 0 0 1 7 13" stroke="#D9A13F" stroke-width="2.6" fill="none" stroke-linecap="round"/></svg></span><div><h3>The season taps you</h3><p>When a tree near you reaches its golden week, the app says so, at exactly the right moment.</p></div></div>
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
    reg_geojson = json.dumps({"type": "FeatureCollection", "features": reg_feats})
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
    cities_json = json.dumps(_city_rows)
    body = f"""
<main class="explore-page">
  <div class="explore-head">
    <h1>The ancient tree map</h1>
    <p>Every tree on the site, each verified, each with its story. Zoom in to a city and pick one; gold means at its best this month.</p>
    <form id="ex-search" class="ex-search" autocomplete="off">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg>
      <input type="text" id="ex-q" list="ex-options" placeholder="Search a city or tree" aria-label="Search a city or tree">
      <datalist id="ex-options">{"".join(f'<option value="{esc(c["city"])}">' for c in json.loads(cities_json))}</datalist>
    </form>
  </div>
  <div class="explore-split">
    <aside id="ex-panel" class="ex-panel" aria-live="polite"></aside>
    <div id="map" class="explore-map"></div>
  </div>
</main>
"""
    script = """
var DATA = __GEOJSON__;
var REGISTERS = __REGISTERS__;
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
var exForm = document.getElementById('ex-search');
if (exForm) {
  exForm.addEventListener('submit', function(e) {
    e.preventDefault();
    var q = document.getElementById('ex-q').value.trim().toLowerCase();
    if (!q) return;
    var hit = CITIES.find(function(c) { return c.city.toLowerCase() === q; }) ||
              CITIES.find(function(c) { return c.city.toLowerCase().indexOf(q) === 0; });
    if (hit) { map.easeTo({center: [hit.lng, hit.lat], zoom: 12, duration: 1200}); return; }
    var tree = DATA.features.find(function(f) {
      return f.properties.name.toLowerCase().indexOf(q) !== -1; });
    if (tree) { map.easeTo({center: tree.geometry.coordinates, zoom: 16, duration: 1200}); }
  });
}
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
  if (REGISTERS.features.length) {
    map.addSource('registers', {type: 'geojson', data: REGISTERS});
    map.addLayer({id: 'register', type: 'circle', source: 'registers',
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
                    .replace("__REGISTERS__", reg_geojson)
                    .replace("__CITIES__", cities_json)
                    .replace("__STYLE__", MAP_STYLE))
    script = f'<script src="{MAPLIBRE_JS}"></script>\n<script>\n' + script + "\n</script>"
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
  var map = {tree: 'tree', city: 'city', home: 'city', correction: 'correction'};
  if (kind && map[kind]) { document.getElementById('sg-kind').value = map[kind]; }
  f.addEventListener('submit', function(e) {
    e.preventDefault();
    var city = document.getElementById('sg-city').value.trim();
    if (!city) return;
    note.textContent = 'Sending...';
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

    city_markers = []
    for p in published:
        lat = sum(m["lat"] for m in p["markers"]) / len(p["markers"])
        lng = sum(m["lng"] for m in p["markers"]) / len(p["markers"])
        city_markers.append({
            "lat": lat, "lng": lng, "label": str(p["count"]),
            "url": p["slug"], "city": p["city"],
        })

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
    FAVOURITE_CITIES = ["lisbon", "cadiz", "porto", "amsterdam", "kyoto",
                        "rome", "palermo", "paris", "london", "barcelona"]
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
    city_options = "".join(f'<option value="{esc(p["city"])}">' for p in published)
    tree_options = "".join(
        f'<option value="{esc(t["name"])}">'
        for entry in (renderable or []) for t in entry["data"]["trees"])
    city_options += tree_options

    body = f"""
<div class="home-hero poster">
  <img class="hero-bg" id="hero-bg" {img_srcset(HERO_PHOTOS[0][0], [1200, 2000, 2800], "100vw")} alt="">
  <div class="hero-scrim"></div>
  <div class="hero-center">
    <h1>Epic old trees, <em>wherever you are</em>.</h1>
    <form id="city-search" class="hero-search poster-search" autocomplete="off">
      <button type="submit" class="search-ico" aria-label="Search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg></button>
      <input type="text" id="city-q" list="city-options" placeholder="Search by city or tree" aria-label="Search for a city">
      <datalist id="city-options">{city_options}</datalist>
    </form>
    <p class="hero-links">
      <a class="hero-link" href="explore">Explore trees near you</a>
    </p>
    <p id="search-note" class="near-me-result"></p>
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
  <p class="dir-more">Not seeing your city? <a href="contribute">Help map it</a>.</p>

</main>
"""
    head_extra = ld_script(site_graph())
    tree_index = []
    for entry in (renderable or []):
        for t in entry["data"]["trees"]:
            tree_index.append({"n": t["name"], "u": f"{entry['slug']}/{slugify(t['name'])}"})
    scripts = home_hero_script(city_markers, tree_index)
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
]

# A tree that gets pulled outright (no replacement, unlike RENAMED_TREE_SLUGS)
# because it turned out unverifiable or possibly on non-visitable private
# land. Its old, possibly-indexed URL redirects to the city page rather than
# 404ing. Entries: (city_slug, old_tree_slug).
REMOVED_TREE_SLUGS = [
    ("lyon", "cedar-of-ile-barbe"),  # lyo_007 pulled 2026-07-29: no source verifies the species claim, and the only garden it could plausibly stand in is the island's private residential half, explicitly non-visitable per the DIREN site classe brochure
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

    for entry in renderable:
        trees = [t for t in entry["data"]["trees"] if tree_is_renderable(t)]
        for tree in trees:
            tree_slugs[tree["id"]] = build_tree_page(entry, tree, trees, pages, species_pages)
        build_question_page(entry, public_collections, pages)
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
        result = build_city_page(entry, tree_slugs, public_collections, pages, other_cities, species_pages)
        if result:
            published.append(result)

    draft_collection_pages = []
    for coll in collections:
        is_draft = coll.get("status") == "needs_curation"
        result = build_collection_page(coll, cities_by_slug, tree_slugs, published, pages, draft=is_draft)
        if is_draft:
            draft_collection_pages.append(result)
    build_collections_index(public_collections, published, pages)
    build_cities_index(published, pages)

    species_cards = []
    for common in sorted(qualifying, key=lambda c: -len(qualifying[c])):
        card = build_species_page(species_intros[common], qualifying[common],
                                  tree_slugs, published, pages)
        species_cards.append(card)
    if species_cards:
        build_species_index(species_cards, published, pages)

    build_contribute_page(published, pages)
    build_privacy_page(pages)
    build_fakedoor_pages(pages)
    # Register layer hidden from users (Hidde, 2026-07-31: "de huidige
    # interactie is het niet, bewaar de informatie"). The data files, the
    # loader and the render path all stay; only this argument is withheld
    # until the layer's interaction is properly designed (BACKLOG, viewport
    # panel). Re-enable by passing registers=registers again.
    build_explore_page(renderable, pages, registers=None)
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
    # Custom domain for GitHub Pages; must survive every rebuild.
    (DIST / "CNAME").write_text(CUSTOM_DOMAIN + "\n")
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
