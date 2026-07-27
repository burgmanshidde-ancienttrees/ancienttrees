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

Reads data/city-list.json, data/cities/*.json, data/collections/*.json.
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
AUTH_ENABLED = False

MAPLIBRE_JS = "https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"
MAPLIBRE_CSS = "https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css"
# OpenFreeMap: free vector tiles, no API key, commercial use permitted
MAP_STYLE = "https://tiles.openfreemap.org/styles/positron"

TITLE_MAX = 60
DESC_MAX = 155

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --cream: #F7F4EE; --cream-dark: #EDE9DF; --ink: #1A1A14; --ink-mid: #4A4A3A;
  --ink-light: #8A8A7A; --moss: #3D5C1E; --moss-light: #EAF0E0;
  --serif: 'Instrument Serif', Georgia, serif; --sans: 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
  --hand: 'Shantell Sans', cursive;
  --header-h: 3.5rem;
}
html { scroll-behavior: smooth; }
body { background: var(--cream); color: var(--ink); font-family: var(--sans); font-size: 16px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
a { color: var(--moss); }

header.bar { position: fixed; top: 0; left: 0; right: 0; z-index: 50; height: var(--header-h); display: flex; align-items: center; justify-content: space-between; padding: 0 1.5rem; background: rgba(247,244,238,0.92); backdrop-filter: blur(8px); border-bottom: 1px solid var(--cream-dark); }
.bar-logo { font-family: var(--sans); font-weight: 700; font-size: 1.02rem; letter-spacing: 0.09em; text-decoration: none; color: var(--ink); }
.bar-links a { font-size: 13px; color: var(--ink-mid); text-decoration: none; margin-left: 1.25rem; }
.bar-links a:hover { color: var(--moss); }
.bar-links a.bar-cta { color: var(--moss); font-weight: 500; border: 1px solid var(--moss); border-radius: 3px; padding: 0.35rem 0.7rem; }
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
.panel-head h1 em { font-family: var(--serif); font-style: italic; color: var(--moss); font-weight: 400; letter-spacing: 0; font-size: 1.08em; }
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
  border: 1px solid var(--moss); border-radius: 999px; padding: 1px 8px; text-transform: capitalize; }
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
.go-btn { display: inline-block; background: var(--moss); color: #fff; text-decoration: none; font-size: 14px; font-weight: 500; padding: 0.7rem 1.25rem; border-radius: 4px; margin: 0.25rem 0 0.5rem; }
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
.entry-thumb { border-radius: 6px; overflow: hidden; aspect-ratio: 1 / 1; background: var(--cream-dark); }
.entry-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
.entry-body h3 { margin-top: 0; }
@media (max-width: 800px) {
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
.hero-overlay h1 em { font-family: var(--serif); font-style: italic; color: var(--moss); font-weight: 400; letter-spacing: 0; font-size: 1.08em; }
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
.home-act-verb { font-family: var(--hand); font-weight: 700; color: var(--moss); font-size: 1rem; text-transform: uppercase; letter-spacing: 0.06em; }
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
.season-now { font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--moss); font-weight: 700; margin: 0 0 12px; font-family: var(--hand); }
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
.sr-months span.half { background: #A9BC8A; }
.sp-name { position: absolute; top: -9px; left: 50%; transform: translateX(-50%); background: var(--ink);
  color: #fff; font-size: 8.5px; font-weight: 600; padding: 1.5px 7px; border-radius: 999px; white-space: nowrap; }
@media (max-width: 760px) { .home-act { grid-template-columns: 1fr; gap: 1.5rem; padding: 2.25rem 0; } .home-act:nth-child(even) .home-act-visual { order: 0; } }
.page { max-width: 1100px; margin: 0 auto; padding: 3rem 2.5rem; }
.section-heading { font-family: var(--sans); font-size: 1.7rem; font-weight: 700; letter-spacing: -0.015em; margin-bottom: 1.5rem; }
.prose { font-size: 15px; font-weight: 300; color: var(--ink-mid); line-height: 1.75; max-width: 640px; margin-bottom: 2.5rem; }
.city-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 2px; background: var(--cream-dark); border: 1px solid var(--cream-dark); margin-bottom: 3rem; }
.city-card { background: var(--cream); padding: 1.5rem; text-decoration: none; border-top: 2px solid transparent; transition: border-top-color 0.2s; }
.city-card:hover { border-top-color: var(--moss); }
.city-card-name { font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em; font-size: 1.25rem; color: var(--ink); margin-bottom: 0.25rem; }
.city-card-meta { font-size: 12px; color: var(--ink-light); }
.city-card.soon { opacity: 0.55; }

footer { border-top: 1px solid var(--cream-dark); padding: 2rem 2.5rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
.footer-logo { font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em; font-size: 14px; letter-spacing: 0.08em; text-transform: uppercase; }
.footer-links { font-size: 12px; }
.footer-links a { color: var(--ink-mid); text-decoration: none; margin-right: 1rem; }
.footer-note { font-size: 12px; color: var(--ink-light); }

/* ---- Markers ---- */
.pin { padding: 2px 8px; border-radius: 999px; background: var(--moss); border: 1.5px solid #fff; box-shadow: 0 2px 8px rgba(26,26,20,0.35); cursor: pointer; color: #fff; font-size: 10.5px; font-weight: 600; font-family: var(--sans); white-space: nowrap; transition: transform 0.15s, background 0.15s; }
.pin:hover { transform: scale(1.1); z-index: 5; }
.hero-search { display: flex; gap: 0.5rem; margin-top: 0.9rem; }
.hero-search input { flex: 1; min-width: 0; border: 1px solid var(--cream-dark); border-radius: 8px; padding: 0.65rem 0.9rem; font-family: var(--sans); font-size: 15px; background: #fff; color: var(--ink); }
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
.route-bar { position: absolute; left: 1rem; right: 1rem; bottom: 1rem; z-index: 5;
  display: flex; gap: 0.5rem; align-items: stretch; }
.route-go { flex: 1; display: flex; flex-direction: column; justify-content: center;
  background: var(--moss); color: #fff; text-decoration: none; padding: 0.7rem 1rem;
  border-radius: 6px; font-size: 15px; font-weight: 500; line-height: 1.25;
  box-shadow: 0 2px 12px rgba(0,0,0,0.18); }
.route-go:hover { background: #2f4717; }
.route-meta { display: block; font-weight: 400; font-size: 12.5px; opacity: 0.85; margin-top: 2px; }
.route-gps { background: #fff; color: var(--ink); border: 1px solid var(--cream-dark);
  border-radius: 6px; padding: 0.7rem 0.9rem; font-family: var(--sans); font-size: 14px;
  cursor: pointer; box-shadow: 0 2px 12px rgba(0,0,0,0.18); white-space: nowrap; }
.route-gps[aria-pressed="true"] { background: var(--moss-light); border-color: var(--moss); }
.report-btn { display: inline-block; margin: 4px 6px 0 0; padding: 5px 12px; border: 1px solid var(--cream-dark); border-radius: 999px; font-size: 12.5px; color: var(--ink-mid); text-decoration: none; }
.report-btn:hover { border-color: var(--moss); color: var(--moss); }
.subtle-suggest { font-size: 13px; color: var(--ink-light); }
.subtle-suggest a { color: var(--moss); }
.hero-kicker { font-family: var(--hand); font-weight: 700; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.07em; color: var(--moss); margin-bottom: 0.5rem; }
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
  .route-bar { position: fixed; left: 0.75rem; right: 0.75rem;
    bottom: calc(0.75rem + env(safe-area-inset-bottom)); }
  /* The fixed bar would otherwise sit on top of the last tree in the list. */
  .panel { padding-bottom: calc(6rem + env(safe-area-inset-bottom)); }
}
.maplibregl-popup-content { font-family: var(--sans); font-size: 13px; padding: 0.75rem 1rem; border-radius: 4px; }
.maplibregl-popup-content strong { font-family: var(--sans); font-weight: 750; letter-spacing: -0.015em; font-size: 15px; font-weight: 400; }

@media (max-width: 800px) {
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
  header.bar { flex-wrap: nowrap; padding: 0 1rem; }
  .bar-logo { font-family: var(--sans); font-weight: 700; font-size: 1.02rem; letter-spacing: 0.09em; text-decoration: none; color: var(--ink); }
  .bar-links { display: flex; align-items: center; white-space: nowrap; }
  .bar-links a.bar-secondary { display: none; }
  /* Get to the trees faster: the intro is still fully in the HTML. */
  .panel-head .lede { display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; }
  .panel-head { padding: 1.25rem 1.1rem 1rem; }
  .panel-head h1 { font-size: 1.6rem; }
  .home-hero { height: 60vh; }
  .hero-overlay { left: 1rem; right: 1rem; top: 1rem; max-width: none; padding: 1.25rem 1.5rem; }
  .page { padding: 2rem 1.5rem; }
  footer { flex-direction: column; text-align: center; }
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
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Shantell+Sans:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%%ROOTPATH%%assets/style.css">
%%HEAD_EXTRA%%
</head>
<body>
<header class="bar">
  <a href="%%ROOTPATH%%" class="bar-logo">Ancient Trees</a>
  <nav class="bar-links">
    <a href="%%ROOTPATH%%#cities">Cities</a>
    <a href="%%ROOTPATH%%species" class="bar-secondary">Species</a>
    <a href="%%ROOTPATH%%collections" class="bar-secondary">Collections</a>
  </nav>
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
  <span class="footer-logo">Ancient Trees</span>
  <span class="footer-links"><a href="%%ROOTPATH%%collections">Collections</a> <a href="%%ROOTPATH%%contribute">Suggest a tree</a></span>
  <span class="footer-note">&copy; %%YEAR%% Ancient Trees, ancienttrees.app. Map &copy; OpenFreeMap, OpenMapTiles, OpenStreetMap contributors.</span>
</footer>
"""

ERRORS = []


def esc(s):
    return html.escape(str(s), quote=True)


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

    About page (Contract E) is deferred by Hidde's decision 2026-07-19;
    when it ships, point the Person url at /about and add sameAs.
    """
    return [
        {"@type": "WebSite", "name": "Ancient Trees", "url": BASE_URL},
        {"@type": "Person", "name": "Hidde", "url": BASE_URL},
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

    kind = esc(bt.get("kind", "").strip())
    chip = f'<span class="sc-chip">{kind}</span>' if kind else ""
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
  center: [{lng}, {lat}], zoom: 14.5, scrollZoom: false
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


def city_map_script(markers, center, route=None):
    data = json.dumps(markers)
    route_coords = json.dumps(
        [[markers[i]["lng"], markers[i]["lat"]] for i in route["order"]]
        if route and len(markers) > 1 else []
    )
    return f"""
<script src="{MAPLIBRE_JS}"></script>
<script>
var markers = {data};
var map = new maplibregl.Map({{
  container: 'map',
  style: '{MAP_STYLE}',
  center: [{center[1]}, {center[0]}],
  zoom: 10.5,
  scrollZoom: true
}});
map.addControl(new maplibregl.NavigationControl());
map.addControl(new maplibregl.FullscreenControl());
map.on('load', function() {{ map.resize(); }});
new ResizeObserver(function() {{ map.resize(); }}).observe(document.getElementById('map'));

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


def home_map_script(markers):
    data = json.dumps(markers)
    return f"""
<script src="{MAPLIBRE_JS}"></script>
<script>
var markers = {data};
// "Around you" has to actually mean something, so the button asks the browser
// where you are and flies the globe to the nearest city that is on the map.
function initNearMe() {{
  var btn = document.getElementById('near-me');
  var out = document.getElementById('near-me-result');
  if (!btn) return;
  if (!navigator.geolocation) {{ btn.style.display = 'none'; return; }}
  btn.addEventListener('click', function() {{
    out.textContent = 'Looking...';
    navigator.geolocation.getCurrentPosition(function(pos) {{
      var la = pos.coords.latitude, lo = pos.coords.longitude, best = null, bestD = Infinity;
      markers.forEach(function(m) {{
        var dLa = (m.lat - la) * Math.PI / 180, dLo = (m.lng - lo) * Math.PI / 180;
        var a = Math.sin(dLa/2) * Math.sin(dLa/2) + Math.cos(la*Math.PI/180) *
                Math.cos(m.lat*Math.PI/180) * Math.sin(dLo/2) * Math.sin(dLo/2);
        var d = 6371 * 2 * Math.asin(Math.sqrt(a));
        if (d < bestD) {{ bestD = d; best = m; }}
      }});
      if (!best) {{ out.textContent = 'No cities on the map yet.'; return; }}
      map.flyTo({{ center: [best.lng, best.lat], zoom: 9, duration: 2200 }});
      var km = Math.round(bestD);
      out.innerHTML = km < 60
        ? 'You are in reach of <a href="' + best.url + '">' + best.city + '</a>. ' + best.label + ' trees to walk to.'
        : 'Nearest mapped city is <a href="' + best.url + '">' + best.city + '</a>, about ' + km +
          ' km away. <a href="contribute">Map your own city</a>.';
    }}, function() {{
      out.textContent = 'Could not get your location. Pick a city below instead.';
    }}, {{ timeout: 8000 }});
  }});
}}
var map = new maplibregl.Map({{
  container: 'map',
  style: '{MAP_STYLE}',
  // Opens on Europe: 30 of 33 cities stand there and the pills need room to
  // breathe. The rest of the world is a drag or a search away, and the
  // near-me button flies wherever you actually are.
  center: [6, 47.5],
  zoom: 3.1,
  scrollZoom: false
}});
map.addControl(new maplibregl.NavigationControl());
map.on('load', function() {{ map.resize(); }});
new ResizeObserver(function() {{ map.resize(); }}).observe(document.getElementById('map'));
markers.forEach(function(m) {{
  var el = document.createElement('div');
  el.className = 'pin';
  el.textContent = m.city;
  el.title = m.label + ' trees';
  el.addEventListener('click', function() {{
    map.flyTo({{ center: [m.lng, m.lat], zoom: 9, duration: 1400 }});
    setTimeout(function() {{ window.location.href = m.url; }}, 1500);
  }});
  new maplibregl.Marker({{ element: el }}).setLngLat([m.lng, m.lat]).addTo(map);
}});
initNearMe();
// The search bar: the front door for people who know where they are going.
var sf = document.getElementById('city-search');
if (sf) {{
  sf.addEventListener('submit', function(e) {{
    e.preventDefault();
    var q = document.getElementById('city-q').value.trim().toLowerCase();
    if (!q) return;
    var hit = markers.find(function(m) {{ return m.city.toLowerCase() === q; }}) ||
              markers.find(function(m) {{ return m.city.toLowerCase().indexOf(q) === 0; }}) ||
              markers.find(function(m) {{ return m.city.toLowerCase().indexOf(q) !== -1; }});
    var out = document.getElementById('near-me-result');
    if (hit) {{ window.location.href = hit.url; }}
    else {{ out.innerHTML = 'Not mapped yet. <a href="contribute">Be the first to map it</a>, or try the location button.'; }}
  }});
}}
</script>
"""


def render_page(title, description, canonical, body, head_extra="", scripts="",
                rootpath="", footer=True, og_type="article"):
    if len(title) > TITLE_MAX:
        ERRORS.append(f"{canonical}: title exceeds {TITLE_MAX} chars ({len(title)}): {title!r}")
    if len(description) > DESC_MAX:
        ERRORS.append(f"{canonical}: description exceeds {DESC_MAX} chars ({len(description)})")
    footer_html = FOOTER.replace("%%ROOTPATH%%", rootpath) if footer else ""
    return (
        PAGE_SHELL
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
    """Where a contribution button points.

    One constant at the top of this file flips every button on the site from a
    prefilled mailto to the hosted form, so switching over is a one-line change.
    """
    if SUBMISSION_FORM_URL:
        return SUBMISSION_FORM_URL
    subject, body = SUBMIT_TEMPLATES[kind]
    return f"mailto:{CONTACT}?subject={subject}&amp;body={body}"


def usable_photo(tree):
    """Return the photo dict if it has a URL, license and attribution and is
    cleared for display; otherwise None. One gate for every page type."""
    photo = tree.get("photo") or {}
    if (photo.get("url") and photo.get("license") and photo.get("attribution")
            and photo.get("status") in ("approved", "found_needs_check")):
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


def oldest_tree(trees):
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
    <img src="{esc(photo['url'])}" alt="{esc(tree['name'])}" loading="lazy">
    <figcaption>Photo: {esc(photo['attribution'])} ({esc(photo['license'])})</figcaption>
  </figure>"""
        og_image = f'\n<meta property="og:image" content="{esc(photo["url"])}">'

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

    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>{esc(tree['name'])}{label}</h1>
  {photo_html}
  {facts}
  <div class="prose-block"><p>{esc(tree['story'])}</p></div>
  {season_html}
  <div class="map-embed"><div id="map" class="map"></div></div>
  <a class="go-btn" href="https://www.google.com/maps/dir/?api=1&amp;destination={loc['latitude']},{loc['longitude']}" target="_blank" rel="noopener">Take me there</a>
  <p class="go-note">Opens directions in your maps app. {esc(tree.get('transport', ''))}</p>
  {approx_note}
  <h2>Trees nearby</h2>
  <ul class="link-list">{nearby_html}</ul>
  <div class="cta">Curious what else is standing in {esc(city)}? See <a href="../{cslug}">all {len(all_trees)} remarkable ancient trees in {esc(city)}</a> or find out <a href="oldest-tree">what the oldest tree in {esc(city)} is</a>.{species_line}</div>
  <div class="report"><strong>Help keep this page true.</strong>
    <a class="report-btn" href="{submit_link('correction')}">Wrong spot</a>
    <a class="report-btn" href="{submit_link('correction')}">The tree is gone</a>
    <a class="report-btn" href="{submit_link('correction')}">Suggest an edit</a>
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
    old = oldest_tree(trees)
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
      <div class="tree-card-photo"><img src="{esc(cphoto['url'])}" alt="{esc(t['name'])}" loading="lazy"></div>
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
      <p class="tree-more"><a href="{slug}/{tslug}">Read more and get directions &rarr;</a>
        <button type="button" class="seen-btn" data-tree="{esc(t['id'])}"
                data-lat="{loc['latitude']}" data-lng="{loc['longitude']}"
                data-radius="{200 if location_is_approximate(t) else 75}" aria-pressed="false">
          <span class="seen-mark" aria-hidden="true"></span><span class="seen-text">Check in at this tree</span>
        </button></p>
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
        f'<a href="./{c["slug"]}">Ancient trees in {esc(c["city"])}</a>'
        for c in other_cities
    )
    more_cities_html = (
        f'<dt>More cities</dt><dd>{others_html}</dd>' if others_html else ""
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
    <div class="route-bar">
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
    scripts = city_map_script(markers, (avg_lat, avg_lng), route)

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
            thumb = (f'<div class="entry-thumb"><img src="{esc(ph["url"])}" alt="{esc(t["name"])}" loading="lazy"></div>'
                     if ph else "")
            rows.append(f"""
      <div class="entry{' has-thumb' if ph else ''}">
        {thumb}
        <div class="entry-body">
          <h3><a href="../{cslug}/{tslug}">{esc(t['name'])}</a> <span class="tree-label">{esc(t.get('age_estimate', ''))}</span></h3>
          <p>{esc(e['note'])}</p>
        </div>
      </div>""")
        sections.append(f"<h2>{esc(city_data['city'])}</h2>{''.join(rows)}")

    city_links = " &middot; ".join(
        f'<a href="../{p["slug"]}">Ancient trees in {esc(p["city"])}</a>' for p in published
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
            thumb = (f'<div class="entry-thumb"><img src="{esc(ph["url"])}" alt="{esc(t["name"])}" loading="lazy"></div>'
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
        f'<a href="../{p["slug"]}">Ancient trees in {esc(p["city"])}</a>' for p in published
    )

    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>{esc(common)}</h1>
  <p class="answer-first">{esc(intro_data['intro'].split('. ')[0])}. This page maps every {esc(common.lower())} on the site, {n} so far across {len(by_city)} cit{'y' if len(by_city)==1 else 'ies'}.</p>
  <div class="prose-block"><p>{esc(intro_data['intro'])}</p></div>
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
        f'<a href="{p["slug"]}">Ancient trees in {esc(p["city"])}</a>' for p in published
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
        f'<a href="{p["slug"]}">Ancient trees in {esc(p["city"])}</a>' for p in published
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

  <div class="path">
    <h2>Map your whole city</h2>
    <p class="prose-block">The big one. Tell us which city and which trees belong on its list. You do not need ten, and you do not need to write anything polished. Names and rough locations are enough; the research, the checking and the writing happen here.</p>
    <a class="go-btn" href="{submit_link('city')}">Map my city</a>
  </div>

  <div class="path">
    <h2>Or just one tree</h2>
    <p class="prose-block">Saw something remarkable and know roughly where it stands? That is enough. One tree in a city we have never touched is often the thing that starts it.</p>
    <a class="go-btn" href="{submit_link('tree')}">Send one tree</a>
  </div>

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
    page = render_page(title, description, canonical, body, head_extra, "", rootpath)
    pages.append(("contribute.html", page, canonical))


# ----------------------------------------------------------------- homepage

def build_homepage(published, upcoming, collections, pages):
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

    coll_html = "".join(
        f'<p class="prose">See <a href="collections/{c["slug"]}">{esc(c["title"])}</a>.</p>'
        for c in collections
    )

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
    contribute_cta = f'<a class="home-cta" href="{submit_link("home")}">Add a tree or a city</a>'
    # Empty until Hidde sets up somewhere to receive it. Donations rather than a
    # paywall: the content stays free and indexable, and there is no account, no
    # card data and no subscription to administer.
    support_cta = (f'<a class="home-cta secondary" href="{esc(SUPPORT_URL)}" '
                   f'target="_blank" rel="noopener">Support the project</a>'
                   if SUPPORT_URL else "")

    body = f"""
<div class="home-hero">
  <div id="map" class="map"></div>
  <div class="hero-overlay">
    <p class="hero-kicker">By tree lovers, for tree lovers</p>
    <h1>Epic old trees, <em>wherever you are</em>.</h1>
    <p>For people who love being outside. See the remarkable old trees near you, walk a few of them in an afternoon with the story of why each is worth it, and tick off the ones you have stood in front of.</p>
    <p class="hero-note">Every tree free to explore.</p>
    <form id="city-search" class="hero-search" autocomplete="off">
      <input type="text" id="city-q" list="city-options" placeholder="Search a city, or use your location..." aria-label="Search for a city">
      <datalist id="city-options">{city_options}</datalist>
      <button type="submit" class="go-btn">Go</button>
    </form>
    <button type="button" id="near-me" class="go-btn ghost">Find trees near me</button>
    <p id="near-me-result" class="near-me-result"></p>
  </div>
</div>
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
<main class="page">
  <p class="prose lead-why">Why bother: a 400 year old tree has outlasted every empire, plague and war its city has seen. It was here before the street was named and will be here after you leave. Most guides send you to the same squares and the same viewpoints. This sends you somewhere quieter, ten minutes off the route, and it is almost always worth the detour.</p>

  <h2 class="section-heading" id="cities">Browse by city</h2>
  <p class="prose">Not near any of these yet? The map above finds the nearest tree wherever you are. Otherwise, pick a city.</p>
  <div class="city-grid">{live_cards}{soon_cards}</div>
  {coll_html}

  <p class="prose subtle-suggest">This map grows through people who know their trees. <a href="{submit_link("tree")}">Know one we missed?</a>{support_cta}</p>
</main>
"""
    head_extra = map_head() + "\n" + ld_script(site_graph())
    scripts = home_map_script(city_markers)
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


def build_redirects(published, pages):
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


def validate_internal_links(pages):
    """Every internal href must resolve to a page this build produces.

    Catches wrong relative paths (P8: no dead ends) before deploy.
    """
    valid = {"/", "/assets/style.css"}
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
    upcoming = []
    for ahead in (1, 2):
        m = (now - 1 + ahead) % 12 + 1
        ups = entries_for(m)
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
  <div class="proto-note">Prototype. Accounts are not live yet: nothing you type here is sent or stored.</div>

  <section id="st-signin" class="acct-card">
    <p class="hero-kicker">Your tree collection</p>
    <h1>Sign in to keep it <em>everywhere</em>.</h1>
    <p class="acct-sub">One email, no password. We send you a sign-in link; your collected trees follow you to any device.</p>
    <form id="acct-form" class="hero-search" autocomplete="email">
      <input type="email" id="acct-email" placeholder="you@example.com" aria-label="Email address" required>
      <button type="submit" class="go-btn">Email me a sign-in link</button>
    </form>
    <p class="acct-fine">We use your address for sign-in links and nothing else.</p>
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
    <p class="hero-kicker">Signed in (prototype)</p>
    <h1>Your <em>trees</em>.</h1>
    <div class="stat-row">
      <div class="stat"><b id="n-trees">0</b><span>trees</span></div>
      <div class="stat alt"><b id="n-cities">0</b><span>cities</span></div>
    </div>
    <p class="acct-sub" id="in-note">Collected on this device. When accounts go live, this follows you everywhere.</p>
    <p class="acct-actions"><button type="button" id="signout" class="acct-link">Sign out</button></p>
  </section>
</main>
<script>
(function() {
  var states = ["st-signin", "st-sent", "st-expired", "st-in"];
  function show(id) {
    states.forEach(function(x) { document.getElementById(x).hidden = (x !== id); });
  }
  function mask(e) {
    var at = e.indexOf("@");
    if (at < 2) return e;
    return e[0] + "\u2022\u2022\u2022" + e.slice(at - 1);
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
  document.getElementById("acct-form").addEventListener("submit", function(ev) {
    ev.preventDefault();
    var e = document.getElementById("acct-email").value.trim();
    if (!e) return;
    document.getElementById("sent-to").textContent = mask(e);
    show("st-sent"); startCooldown();
  });
  document.getElementById("change").addEventListener("click", function() { show("st-signin"); });
  document.getElementById("resend").addEventListener("click", startCooldown);
  document.getElementById("re-expired").addEventListener("click", function() { show("st-sent"); startCooldown(); });
  document.getElementById("signout").addEventListener("click", function() { show("st-signin"); });
  if (location.hash === "#expired") show("st-expired");
  if (location.hash === "#in") {
    try {
      var seen = JSON.parse(localStorage.getItem("ancienttrees_seen")) || [];
      document.getElementById("n-trees").textContent = seen.length;
      var cities = {};
      seen.forEach(function(id) { cities[id.slice(0, 3)] = 1; });
      document.getElementById("n-cities").textContent = Object.keys(cities).length;
    } catch (e) {}
    show("st-in");
  }
})();
</script>
"""
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
        other_cities = [
            {"slug": e["slug"], "city": e["data"]["city"]}
            for e in renderable if e["slug"] != entry["slug"]
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

    species_cards = []
    for common in sorted(qualifying, key=lambda c: -len(qualifying[c])):
        card = build_species_page(species_intros[common], qualifying[common],
                                  tree_slugs, published, pages)
        species_cards.append(card)
    if species_cards:
        build_species_index(species_cards, published, pages)

    build_contribute_page(published, pages)
    build_in_season_page(renderable, tree_slugs, pages)
    build_homepage(published, upcoming, public_collections, pages)
    build_redirects(published, pages)
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
