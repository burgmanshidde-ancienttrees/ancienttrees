// Translated-page infrastructure, built 2026-08-10 on Hidde's direction: a
// small Spanish test (Malaga, the one city with measured Spanish search
// demand: "árboles históricos de málaga", 20 impressions at position 74,
// zero clicks) inside a structure that scales to more languages if the test
// works. The long-term shape is the industry-standard one and nothing
// cleverer: language subdirectories (/es/malaga) plus reciprocal hreflang
// links, so Google serves the right language and never reads the pair as
// duplicate content. A translation is an OVERLAY on the English city file:
// data/i18n/<lang>/<slug>.json carries only the translated text, and every
// coordinate, photo, licence and walk stays in the one canonical city file,
// so a pin corrected in English is corrected everywhere.
import fs from "node:fs";
import { isNoindexed } from "./noindex";
import path from "node:path";
import { DATA } from "./data-dir";
import { BASE_URL } from "./schema";
import { cityHasQuestionPage } from "./question-page";

export interface TreeTranslation {
  name: string;
  species: string;
  age_estimate: string;
  access: string;
  transport: string;
  story: string;
}

export interface CityTranslation {
  city: string;
  title: string;
  meta_description: string;
  intro: string;
  question_title: string;
  question_meta: string;
  question_answer: string;
  question_context: string;
  faq: { q: string; a: string }[];
  trees: Record<string, TreeTranslation>;
}

/** Language subdirectories under data/i18n that actually exist. */
export function translatedLanguages(): string[] {
  const dir = path.join(DATA, "i18n");
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter((d) => fs.statSync(path.join(dir, d)).isDirectory());
}

/** City slugs translated into `lang`. */
export function translatedCities(lang: string): string[] {
  const dir = path.join(DATA, "i18n", lang);
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter((f) => f.endsWith(".json")).map((f) => f.slice(0, -5));
}

export function cityTranslation(lang: string, slug: string): CityTranslation | null {
  const p = path.join(DATA, "i18n", lang, `${slug}.json`);
  if (!fs.existsSync(p)) return null;
  return JSON.parse(fs.readFileSync(p, "utf-8")) as CityTranslation;
}

/** The question page's slug per language. English pages live at
 * /{city}/oldest-tree; a translated question page takes the phrase people
 * actually search in that language rather than an English path segment. */
export const QUESTION_SLUG: Record<string, string> = {
  es: "arbol-mas-antiguo",
  it: "albero-piu-antico",
  nl: "oudste-boom",
  de: "aeltester-baum",
  pt: "arvore-mais-antiga",
  fr: "arbre-le-plus-vieux",
  ja: "saiko-rei-no-ki",
};

/** The visible "this page also exists in X" line, in the TARGET language.
 * It sits on the English page, so it has to read as an invitation to a
 * speaker of that language rather than as English telling them a translation
 * exists somewhere. */
export const LANG_INVITE: Record<string, string> = {
  es: "Esta página también está disponible",
  it: "Questa pagina è disponibile anche",
  nl: "Deze pagina is ook beschikbaar",
  de: "Diese Seite gibt es auch",
  pt: "Esta página também está disponível",
  fr: "Cette page est également disponible",
  ja: "このページは次の言語でもご覧いただけます",
};

/** Page chrome, per language.
 *
 * Extracted 2026-08-22 when Contract J went from one language to seven. Until
 * then the Spanish templates carried these ~20 strings inline, which was the
 * right call for a single test and becomes a maintenance bug at seven: the
 * same sentence would live in seven files and drift in six of them.
 *
 * `ui(lang)` falls back to English per KEY rather than per language, so a
 * language ships with whatever is written and shows English for the rest
 * instead of failing to build. That is deliberate and is what Contract J
 * means by chrome debt being named rather than silent: an untranslated button
 * is visible to anyone looking at the page, where a missing one is not.
 *
 * These are UI labels only. Every sentence a reader is meant to READ comes
 * from data/i18n/<lang>/<slug>.json and is hand-written per city.
 */
export interface UIStrings {
  home: string;
  backToTrees: (n: number) => string;
  treesOnMap: (n: number) => string;
  /** The whole H1, not a prefix: Japanese puts the qualifier AFTER the place
   * name, so a prefix plus a city name cannot express it. */
  heading: (city: string) => string;
  readMore: string;
  visitedOf: (n: number, city: string) => string;
  seeCollection: string;
  mappingAll: string;
  missingOrWrong: (city: string) => string;
  tellUs: string;
  faqHeading: string;
  moreOnOldest: string;
  /** City page foot: the eight closest cities, then a link to /cities. */
  nearbyCities: string;
  allCities: string;
  oldestQuestion: (city: string) => string;
  fullAnswer: string;
  suggestTree: string;
  sendIt: string;
  walkRoutes: string;
  inTheApp: string;
  /** The app block that sits low on tree and city pages. Translated on
   *  2026-09-12: it was English-only, so a reader who had read a whole page
   *  in their language met the one paragraph asking something of them in
   *  another. Translation of the copy already on the English page, not new
   *  copy. PRODUCT_COPY.md still governs the English. */
  appPitchTreeTitle: string;
  appPitchTreeBody: string;
  appPitchCityTitle: string;
  appPitchCityBody: string;
  /** The city pitch where hasWalksPage() is false: no walk promised. */
  appPitchCityBodyNoWalks: string;
  getTheApp: string;
  whereAmI: string;
  cardMore: string;
  cardSave: string;
  cardSaved: string;
  walkMoreTrees: (city: string) => string;
  whatElseStands: (city: string) => string;
  allTreesLink: (n: number, city: string) => string;
  orDiscover: string;
  whichIsOldest: (city: string) => string;
  moreTrees: string;
  oldestTreeCrumb: string;
  fullStory: string;
  cityHasMore: (city: string) => string;
  /** The full stop that closes the "more trees in this city" sentence on a
   *  question page. A string rather than a literal because Japanese ends a
   *  sentence with \u3002 and not with a dot. It used to be a clause promising
   *  "with a walking route that passes several of them", which stopped being
   *  true on 2026-09-02 when the walks left the website for the app. */
  sentenceEnd: string;
  /** The photo credit line, label and name together, because the label's
   *  punctuation is part of the language: French wants a space before its
   *  colon and Japanese a full-width one. */
  photoCredit: (credit: string) => string;
  /** The short age on a list card (age-short.ts, 2026-10-04): "250 years",
   *  "135-175 years". The figure arrives already formatted. */
  ageYears: (n: string) => string;
  /** The season chip's words (phenology.ts seasonChip, 2026-10-04): the moment
   *  named in sentence case, shown only while it is true. */
  seasonChip: Record<string, string>;
  /** The "Seen" pill in a card's tag row (2026-10-04), the app's own word. */
  seenChip: string;
  /** The ambassador line under a city intro (2026-10-02): a reader who looks
   *  after the place and consented to be named. Nothing prints without that
   *  consent, so this string is only ever reached with a real name. */
  /** The grey line UNDER the ambassador's name, komoot's person row (2026-10-03,
   *  Hidde: "follow the design way of komoot"): avatar, name in bold, one small
   *  line saying what they are. Where the noun would be gendered the line says
   *  what they do instead, so one string serves any name. */
  ambassadorRole: (place: string) => string;
  /** The open seat, on every city page with no named ambassador (Hidde,
   *  2026-10-04: "Tokyo is looking for an ambassador met een knop"). Name
   *  line, one grey line, the button, and what the button says once sent. */
  ambassadorWanted: (place: string) => string;
  ambassadorWantedLine: string;
  ambassadorApply: string;
  ambassadorApplied: string;
  ambassadorAskTitle: (place: string) => string;
  /** The list of a place's ambassadors, for a screen reader. */
  ambassadorsLabel: string;
  ambassadorAskBody: string;
  /** What an ambassador does, one line each, in the dialog (2026-10-08). */
  ambassadorAskPoints: string[];
  ambassadorAskSend: string;
  ambassadorNotNow: string;
  ambassadorSentTitle: string;
  ambassadorSentBody: string;
  ambassadorWriteTo: (email: string) => string;
  ambassadorDone: string;
  /** The photo viewer, added 2026-09-03. `photoOpen` labels the button the
   *  photograph itself becomes, `photoFull` is the step Wikipedia's Media
   *  Viewer puts one click further in: the original file at full resolution. */
  photoOpen: string;
  /** Paging through a tree's photographs, added 2026-09-12 when trees gained
   *  more than one. `photoNumber` is both the counter in the lightbox and the
   *  label on a thumbnail, so a screen reader hears "Photograph 2 of 3" rather
   *  than a second unnamed button. */
  photoPrev: string;
  photoNext: string;
  photoNumber: (n: number, total: number) => string;
  /** The alt text on Apple's App Store badge, added 2026-09-03. It says what
   * the control DOES, because a screen reader announcing "Download on the App
   * Store badge" describes a picture rather than an action. */
  appStoreBadge: string;
  /** The three-way "get the app" widget, added 2026-09-03 on Hidde's ask: an
   * Android visitor sees a waitlist (there is no Android app), a desktop
   * visitor sees a QR code (the AllTrails convention), an iOS visitor sees
   * the badge above and needs none of these. */
  /** The AllTrails-style download overlay's own two strings (2026-09-03):
   * the title above the QR, and the Android variant's headline. */
  openInApp: string;
  androidTitle: string;
  androidNote: string;
  emailLabel: string;
  notifyMe: string;
  waitlistSent: string;
  scanToOpen: string;
  photoClose: string;
  photoFull: string;
  distanceAway: (d: string) => string;
  /** The factual opening of a tree page's meta description: what it is,
   *  how old, where. Contract B's "answer" half, per language, because
   *  the word order differs and a template cannot be translated word for
   *  word. `age` is already a bare number and may be empty. */
  /** The answer-first opening of a tree page's meta description. `size` is
   *  supplied only when there is no age: a girth or a height in metres, so a
   *  tree nobody has dated still opens on a fact instead of repeating its own
   *  title (2026-09-08). Render the number with this language's own decimal
   *  separator; the caller passes it unformatted for exactly that reason. */
  metaLead: (species: string, age: string, where: string,
             size?: { girth?: number; height?: number }) => string;
  /** The short editorial tag beside a tree's name on a card. Keyed by the
   *  English value in data/cities, because that is what the canonical file
   *  holds; an unlisted label falls back to the English rather than
   *  disappearing, which is what it did before this existed. */
  treeLabels: Record<string, string>;
  labelSpecies: string;
  /** The fact-card row naming the official register a tree is listed in (lib/official-register.ts). */
  labelRegister: string;
  labelGirth: string;
  labelAge: string;
  labelLocation: string;
  labelAccess: string;
  labelGettingThere: string;
  factAge: string;
  /** The label over a numeric age, which carries the unit so the value does
   *  not repeat it (2026-09-04). */
  factYearsOld: string;
  factPin: string;
  /** The line under the two columns: it carries words, which is why it is a
   *  line rather than a column. */
  locApprox: string;
  ticketNeeded: string;
  pinExact: string;
  pinApproximate: string;
  discoverMore: string;
  sourcesHeading: string;
  /** Under the Sources heading. Since 2026-10-22 it also says HOW the story
   *  was made (written with AI, corrected by readers), the disclosure Google's
   *  content guidance asks for where a reader would wonder; the about page
   *  says the same. */
  sourcesLine: string;
  /** Link under the sources to /about (2026-10-01). */
  howWeCheck: string;
  takeMeThere: string;
  /** The app's tree page on the web (2026-09-24): the Open-in-the-app CTA, the
   *  corner map, the maps-app choice and the drag-the-pin correction. */
  showOnMap: string;
  showPhoto: string;
  openFullMap: string;
  dirTitle: string;
  noPhotoYet: string;
  pinShowUs: string;
  pinTitle: string;
  pinHelp: string;
  pinZoom: string;
  pinMoved: (m: number) => string;
  pinSend: string;
  pinSending: string;
  pinDone: string;
  pinFailed: string;
  pinNeedsAccount: string;
  cancel: string;
  /** The two maps apps by the names each language's store gives them. */
  appleMaps: string;
  /** The back arrow on a tree page's photograph (AllTrails' mobile web). */
  goBack: string;
  /** The Discover more chip to a city's question page, a name like the others. */
  chipOldest: string;
  googleMaps: string;
  /** The tree page's collect button, the app's "Collect this tree" word for
   *  word (Hidde, 2026-10-15: "mark as collected is just the wrong wording";
   *  collecting needs a photograph, so it is an act, not a tick). */
  seenIt: string;
  worthItAsk: (name: string) => string;
  worthItDone: (name: string) => string;
  seenItDone: string;
  /** THE COLLECT SHEET on the tree page (2026-10-10, Hidde: "make the collect
   *  this tree and uncollect more consistent on web and app"). The app's
   *  TreeDetail.swift collectChoice, word for word. */
  collectTitle: (n: string) => string;
  collectLead: string;
  collectPhoto: string;
  /** The collect sheet's camera and library buttons on a phone (2026-10-10);
   *  collectPhoto is the one file button a laptop shows. */
  collectCamera: string;
  collectLibrary: string;
  collectNoPhoto: string;
  collectedTitle: (n: string) => string;
  collectedOn: (d: string) => string;
  uncollect: string;
  /** The snackbar after removing, with Undo (2026-10-10). */
  uncollected: string;
  uncollectQ: (n: string) => string;
  uncollectBody: string;
  uncollectYes: string;
  keepIt: string;
  nearbyTrees: string;
  somethingWrong: string;
  suggestAnother: string;
  /** The share control's accessible name. */
  share: string;
  /** What the share button says after it has copied the link, for the
   *  browsers with no system share sheet. Heard rather than read, and still
   *  one of seven languages. */
  shareCopied: string;
  /** The link in the help block. It says what it does rather than naming a
   *  fault, because the worth-it control right above it already asks about
   *  faults and two entry points for one intent is how the English page read
   *  until 2026-09-11. */
  correctDetail: string;
  /** The worth-it control, ported to the other seven languages on 2026-09-12.
   *  Every string here is a TRANSLATION of copy that was already on the
   *  English page, never new copy: the control itself is unchanged. */
  worthVote: (treeName: string) => string;
  worthReport: string;
  worthWhatsWrong: string;
  worthDead: string;
  worthDeadQ: string;
  worthDeadPh: string;
  worthWrongLoc: string;
  worthWrongLocQ: string;
  worthWrongLocPh: string;
  worthWhichTree: string;
  worthWhichTreeQ: string;
  worthWhichTreePh: string;
  worthCouldNotReach: string;
  worthCouldNotReachQ: string;
  worthCouldNotReachPh: string;
  worthTwice: string;
  worthTwiceQ: string;
  worthTwicePh: string;
  worthSomethingElse: string;
  worthSomethingElseQ: string;
  worthSomethingElsePh: string;
  worthThanks: string;
  /** The second thanks, after the optional detail has been sent. It is a
   *  different sentence from worthThanks on purpose: the reader has now given
   *  us something to work with. */
  worthThanksDetail: string;
  worthDetailLabel: string;
  worthSend: string;
  actions: string;
  unknownAge: string;
  approxLocationChip: string;
  noPhotoLicence: string;
  /** The AddPhoto control's own button, read by ADD_PHOTO_JS off a data
   *  attribute rather than hardcoded, so a translated page shows this
   *  language's words instead of silently falling back to English
   *  (REVIEW.md 2026-09-23 WARN: the control shipped English-only). */
  addPhotoBtn: string;
  /** Same control, offered quietly on a tree that already has a photograph. */
  addPhotoBtnQuiet: string;
  /** The second sentence beside noPhotoLicence, now that there is a real
   *  button to point at rather than a dead link to /contribute. */
  photoCanGoHere: string;
  addPhotoSignIn: string;
  addPhotoSending: string;
  addPhotoBadFile: string;
  addPhotoThanks: string;
  addPhotoFailed: string;
  /** One line under the button: only the reader's own photographs (2026-09-24). */
  /** The lasting state of a photograph somebody sent of this tree, written
   *  beside the control on every later visit (CONVENTIONS.md, "Landing after
   *  you have added something"): waiting, or on the page. Same words as the
   *  app's Sighting.photoState. */
  addPhotoWaiting: string;
  /** The heading over a city's day-trip trees (lib/day-trips.ts). */
  dayTripAway: string;
  /** "Jaegersborg Dyrehave, 12 km north". `dir` arrives in English. */
  dayTripWhere: (place: string, km: number, dir: string) => string;
  addPhotoOnPage: string;
  /** Heading over your own photographs of this tree, the app's "Your photograph". */
  yourPhoto: string;
  yourPhotos: string;
  /** Your own photograph's More button, and the sheet that deletes it (Google Maps: More, Delete this photo). */
  photoMore: string;
  photoDeleteTitle: string;
  photoDeleteBody: string;
  photoDeleteBtn: string;
  photoDeleted: string;
  /** The link from the acknowledgement to where the photograph now lives. */
  addPhotoSeeMine: string;
  /** The optional second photograph when somebody adds a tree: the sign
   *  beside it, which names the species, often the age and the tree itself
   *  (Hidde, 2026-09-24). Same words as the app's describe form. */
  havePhotographed: string;
  havePhotographedLine: string;
  goNote: string;
  /** The honesty note on a rough pin. It has to say plainly, in every
   * language, that the marker is the right AREA and not the tree, because a
   * reader who trusts it as exact is already standing in the wrong place. */
  approxNote: string;
  knowExactly: string;
  couldUseHelp: string;
  researchedRemotely: string;
  knowMoreThanUs: string;
  ifOlderTree: (city: string) => string;

  /** The cities index, per language. Added 2026-09-17, after a count of where
   * a translated page actually leads: 19 of the 27 internal links on
   * /es/cadiz dropped the reader back into English, the breadcrumb "Inicio"
   * among them. The references both serve their whole structure per locale
   * (komoot /de-de/discover, AllTrails /es/parques/...), and we served leaf
   * pages with no tree to hang on. This is the first index to exist in every
   * language. */
  citiesCrumb: string;
  citiesTitle: string;
  citiesHeading: string;
  citiesLead: (cities: number, trees: number) => string;
  citiesDescription: string;

  /** The map page, per language. The map is the product (CLAUDE.md, the four
   * verbs), so it is the second index to exist in every language after the
   * cities list. The "browse another way" line deliberately names only the
   * cities index: species, collections and parks have no translated leaf
   * pages yet, and an index that links into English is the dead end this
   * whole structure pass exists to remove. */
  exploreTitle: string;
  exploreDescription: string;
  exploreHeading: string;
  exploreNote: string;
  exploreWhatH: string;
  exploreWhatBody: (trees: number, places: number, countries: number) => string;
  exploreWalksH: string;
  exploreWalksBody: string;
  exploreIslandsH: string;
  exploreIslandsBody: string;
  exploreNotH: string;
  exploreNotBody: string;
  exploreBrowse: string;

  /** The homepage, per language. Scoped deliberately: hero, the value
   * proposition, the four verbs and the city directory, all of which link
   * only to pages that exist in the language. The country, species, park and
   * oldest shelves are left off a translated homepage until their leaf pages
   * are translated, for the same reason the cities index lists only
   * translated cities. */
  homeTitle: string;
  homeDescription: string;
  homeHeroLead: string;
  homeHeroEm: string;
  homeSub: string;
  homeFindH: string;
  homeFindBody: string;
  homeWalkH: string;
  homeWalkBody: string;
  homeCollectH: string;
  homeCollectBody: string;
  homeDirectoryH: string;
  homeMission: string;
  homeMissionLink: string;

  /** The map's chip row. On the list because check_every_language_gets_the_
   * same_controls() (qa.py, 2026-09-12) is about CONTROLS rather than prose:
   * a translated map with an English filter row is the same fault it was
   * written to catch. */
  mapFilterGroup: string;
  mapFilterFav: string;
  /** The one-line confirmation after the bookmark (2026-10-10), and its action. */
  wantAdded: string;
  wantRemoved: string;
  wantView: string;
  wantUndo: string;
  mapFilterMine: string;
  mapFilterSpecies: string;
  mapFilterFree: string;

  /** One entry in the tightest-walks list: how many trees and how far apart.
   * A key rather than bare numbers because dropping the nouns to avoid
   * translating them turned the English from "6 trees, 300 m apart" into
   * "6, 300 m", which is not a shorter sentence, it is a worse one. */
  exploreWalkItem: (trees: number, apart: string) => string;
  /** The homepage's own strings. Added 2026-09-18 with the translated
   * homepage: the 14 that existed covered the prose and none of the chrome,
   * so a translated homepage would have shown Spanish paragraphs under
   * English headings. */
  homeVerbFind: string;
  homeVerbWalk: string;
  homeVerbCollect: string;
  homeNearestChip: string;
  homeMinWalk: (n: number) => string;
  homeWalkChip: string;
  homeTreesCount: (n: number) => string;
  homeAboutTime: string;
  homePhoneTitle: string;
  homeStatTrees: string;
  homeStatCities: string;
  homeStatOldest: string;
  homeCollectedSpecies: string;
  homeDirTopCities: string;
  homeDirCollections: string;
  homeDirOldest: string;
  homeDirTopSpecies: string;
  homeAllCities: (n: number) => string;
  homeAllCollections: string;
  homeOldestOfAll: string;
  homeAllSpecies: (n: number) => string;
  homeFavH: string;
  homeOldestShelfH: string;
  homeCountriesH: string;
  homeAllCountries: string;
  homeSpeciesH: string;
  homeParksH: string;
  homeAllParks: string;
  /** "See all >" at the end of every shelf heading (2026-10-04, the app's
   *  Discover and the App Store's shelves): one label on every row, the
   *  specific one ("All 186 species") rides along as the link's aria-label. */
  seeAll: string;
  /** The tree page since 2026-10-24 (CONVENTIONS.md, "Notes from visitors",
   *  "Getting there is one block", "the map is the picture"). */
  gettingThere: string;
  readLess: string;
  /** Under "No photograph yet" on the map hero: the one ask. */
  noPhotoAsk: string;
  notesHeading: string;
  notesNone: string;
  /** "{tree}" is replaced by a link to the nearest tree that has a note. */
  notesBorrowed: string;
  notesEmptyTitle: string;
  notesEmptyAsk: string;
  noteWrite: string;
  noteEditMine: string;
  photoAddTitle: string;
  photoAddAsk: string;
  noteAsk: string;
  noteSheetTitle: string;
  notePlaceholder: string;
  noteExamples: string;
  noteShownAs: (name: string) => string;
  noteShownAnon: string;
  noteAdd: string;
  noteSave: string;
  noteDelete: string;
  noteSaving: string;
  noteFailed: string;
  noteSignIn: string;
  noteYours: string;
  noteVisitor: string;
  homeShelfMeta: (n: number, country: string) => string;
}

const EN: UIStrings = {
  home: "Home",
  backToTrees: (n) => `\u2190 ${n === 1 ? "The tree" : `The ${n} trees`}`,
  treesOnMap: (n) => `${n} ${n === 1 ? "tree" : "trees"} on the map`,
  heading: (c) => `Ancient Trees in ${c}`,
  readMore: "Read more",
  visitedOf: (n, city) => `visited in ${city}`,
  seeCollection: "See your full collection",
  mappingAll: "We are mapping every remarkable tree in the world.",
  missingOrWrong: (city) => `Do you know one in ${city} we are missing, or see a mistake here?`,
  tellUs: "Tell us",
  faqHeading: "Frequently asked questions",
  moreOnOldest: "More on the oldest tree",
  nearbyCities: "Ancient trees in nearby cities",
  allCities: "Every city on the map",
  oldestQuestion: (city) => `What is the oldest tree in ${city}?`,
  fullAnswer: "The full answer, with a map and how to get there.",
  suggestTree: "Know a tree that belongs on this list?",
  sendIt: "Send it to us",
  walkRoutes: "Walking routes",
  inTheApp: "in the app",
  appPitchTreeTitle: "Collect the trees you visit",
  appPitchTreeBody: "With the app you can tick this one off, find a walk past a few more, and watch your collection grow city by city.",
  appPitchCityTitle: "Visit them with the app",
  appPitchCityBody: "With the app you can follow a walk past these trees, save the ones you want to see, and tick off every one you visit.",
  appPitchCityBodyNoWalks: "With the app you can save the trees you want to see and tick off every one you visit.",
  getTheApp: "Get the app",
  whereAmI: "Where am I",
  cardMore: "Read more and get directions \u2192",
  cardSave: "Save",
  cardSaved: "Saved",
  walkMoreTrees: (c) => `Walk more trees in ${c}`,
  whatElseStands: (c) => `Want to know what else is still standing in ${c}? See`,
  allTreesLink: (n, c) => `the ${n} remarkable trees of ${c}`,
  orDiscover: "or find out",
  whichIsOldest: (c) => `which is the oldest tree in ${c}`,
  moreTrees: "More trees",
  oldestTreeCrumb: "The oldest tree",
  fullStory: "The full story of this tree",
  cityHasMore: (c) => `${c} has more trees worth the visit:`,
  sentenceEnd: ".",
  photoCredit: (credit) => `Photo: ${credit}`,
  ambassadorRole: (place) => `${place} ambassador`,
  ageYears: (n) => `${n} years`,
  seenChip: "Collected",
  seasonChip: { bloom: "In bloom", autumn: "Autumn colour", fruit: "In fruit", leaves: "Fresh leaves", catkins: "Catkins", winter: "Winter shape", peak: "In season" },
  ambassadorWanted: (place) => `${place} is looking for an ambassador`,
  ambassadorWantedLine: "Help us improve this list.",
  ambassadorApply: "Become the ambassador",
  ambassadorApplied: "Request sent.",
  ambassadorAskTitle: (place) => `Become the ambassador for ${place}`,
  ambassadorsLabel: "Ambassadors",
  ambassadorAskBody: "An ambassador helps us get the trees of this place right.",
  ambassadorAskPoints: ["Add photographs of the trees", "Check the facts and tell us which trees are missing", "Help put together walks past them"],
  ambassadorAskSend: "Apply",
  ambassadorNotNow: "Not now",
  ambassadorSentTitle: "Request sent",
  ambassadorSentBody: "We will email you soon with a few questions about the list.",
  ambassadorWriteTo: (email) => `We will write to ${email}.`,
  ambassadorDone: "Done",
  photoOpen: "Open the photograph",
  photoPrev: "Previous photograph",
  photoNext: "Next photograph",
  photoNumber: (n, total) => `Photograph ${n} of ${total}`,
  appStoreBadge: "Get Ancient Trees on the App Store",
  openInApp: "Open in the app",
  androidTitle: "We are working on the Android app",
  androidNote: "There is no Android app yet. Leave your email and we'll let you know the day there is one.",
  emailLabel: "Email address",
  notifyMe: "Notify me",
  waitlistSent: "You are on the list. We'll let you know when the app is on Android.",
  scanToOpen: "Scan this with your phone to open it there.",
  photoClose: "Close",
  photoFull: "See it at full size",
  distanceAway: (d) => `${d} away`,
  treeLabels: {},
  metaLead: (sp, age, where, size) => {
    // "An European Yew" has been shipping on every ageless vowel-initial
    // species since this line was written, because the test is on the LETTER
    // and the article follows the SOUND. "Eu" is the whole of the problem
    // here: European (ash, beech, larch, pear, yew, white elm, hop-hornbeam)
    // and Eucalyptus all start on a consonant "y" sound. Found 2026-09-08 by
    // reading the generated snippets rather than the code.
    const vowel = age ? /^(8|11|18|8\d)$/.test(age)
      : /^[AEIOU]/.test(sp) && !/^Eu/i.test(sp);
    const a = vowel ? "An" : "A";
    const m = size?.girth ? `${size.girth} metres round`
      : size?.height ? `${size.height} metres tall` : "";
    const head = age && sp ? `${a} ${age}-year-old ${sp}`
      : sp && m ? `${a} ${sp} ${m}`
      : sp ? `${a} ${sp}`
      : age ? `${a} ${age}-year-old tree`
      : m ? `A tree ${m}` : "A remarkable tree";
    return `${head} in ${where}.`;
  },
  labelSpecies: "Species",
  labelRegister: "In the official register",
  labelGirth: "Girth",
  labelAge: "Age estimate",
  labelLocation: "Location",
  labelAccess: "Access",
  labelGettingThere: "Getting there",
  factAge: "Age",
  factPin: "Pin",
  factYearsOld: "Years old",
  locApprox: "Approximate location.",
  ticketNeeded: "You need a ticket to see this tree",
  pinExact: "Exact",
  pinApproximate: "Approximate",
  discoverMore: "Discover more",
  sourcesHeading: "Sources",
  sourcesLine: "Where the facts on this page come from. The story was written with AI from these sources, and readers who know the tree correct it.",
    howWeCheck: "How we choose and check trees",
  takeMeThere: "Take me there",
  showOnMap: "Show on the map",
  showPhoto: "Show the photograph",
  openFullMap: "Open the full map",
  dirTitle: "Open directions in",
  noPhotoYet: "No photograph yet",
  pinShowUs: "Show us where it is",
  pinTitle: "Where is it really?",
  pinHelp: "Drag the map until the pin sits on the tree.",
  pinZoom: "Zoom in as far as you like. You can send once you have moved the pin.",
  pinMoved: (m) => `That is ${m} m from where we have it.`,
  pinSend: "The tree is here",
  pinSending: "Sending",
  pinDone: "We will check it and move the pin.",
  pinFailed: "That did not go through. Try again in a moment.",
  pinNeedsAccount: "You need an account to send this, so we can tell you what your correction changed.",
  cancel: "Cancel",
  appleMaps: "Apple Maps",
  goBack: "Back",
  chipOldest: "Oldest tree",
  googleMaps: "Google Maps",
  seenIt: "Collect this tree",
  worthItAsk: (n) => `Yes, ${n} was worth the visit`,
  worthItDone: (n) => `You found ${n} worth the visit. Tap to undo`,
  seenItDone: "Collected",
  collectTitle: (n) => `Collect ${n}`,
  collectLead: "Take a photograph to add it to your trees.",
  collectPhoto: "Choose a photograph",
  collectCamera: "Take a photograph",
  collectLibrary: "Choose from your photos",
  collectNoPhoto: "Collect without a photograph",
  collectedTitle: (n) => `You collected ${n}`,
  collectedOn: (d) => `On ${d}.`,
  uncollect: "Remove from collected",
  uncollected: "Removed from collected",
  uncollectQ: (n) => `Remove ${n} from your collected trees?`,
  uncollectBody: "Your photographs of it stay saved. It leaves My trees until you collect it again.",
  uncollectYes: "Remove",
  keepIt: "Keep it",
  nearbyTrees: "Nearby trees",
  somethingWrong: "Something here is wrong",
  suggestAnother: "Suggest another tree",
  share: "Share",
  shareCopied: "Link copied",
  correctDetail: "Correct a detail on this page",
  worthVote: (n) => `Yes, ${n} was worth the visit`,
  worthReport: "Something's wrong",
  worthWhatsWrong: "What's wrong?",
  worthDead: "It's dead or gone",
  worthDeadQ: "What did you find there? (optional)",
  worthDeadPh: "A stump, a fallen trunk, nothing at all, and when you were there",
  worthWrongLoc: "Wrong location",
  worthWrongLocQ: "Where is it really? (optional)",
  worthWrongLocPh: "A street corner, a landmark, or paste a maps pin",
  worthWhichTree: "Couldn't tell which tree",
  worthWhichTreeQ: "Which one did you look at? (optional)",
  worthWhichTreePh: "The thicker trunk, the one nearest the path, the one by the bench",
  worthCouldNotReach: "Couldn't reach it",
  worthCouldNotReachQ: "What stopped you? (optional)",
  worthCouldNotReachPh: "A locked gate, a fence, opening hours, private land",
  worthTwice: "It's on the map twice",
  worthTwiceQ: "Which other tree is it? (optional)",
  worthTwicePh: "Its name, or where the other pin is",
  worthSomethingElse: "Something else",
  worthSomethingElseQ: "Tell us in a line.",
  worthSomethingElsePh: "What we got wrong, or what we are missing",
  worthThanks: "Thanks, we'll check it.",
  worthThanksDetail: "Thanks, that helps.",
  worthDetailLabel: "Anything that helps us check? (optional)",
  worthSend: "Send",
  actions: "Actions",
  unknownAge: "age unknown",
  approxLocationChip: "pin approximate",
  noPhotoLicence: "We don't have a photograph of this tree yet.",
  addPhotoBtn: "Add a photo",
  addPhotoBtnQuiet: "Add your own photo",
  photoCanGoHere: "If you took one yourself, you can add it here.",
  addPhotoSignIn: "Sign in first, then choose your photograph.",
  addPhotoSending: "Sending...",
  addPhotoBadFile: "That picture could not be read. Try another one.",
  addPhotoThanks: "Thank you. We look at every photograph before it goes on a page, and you will hear what happened to yours.",
  addPhotoFailed: "That did not go through. Try again in a moment.",
  addPhotoWaiting: "Sent to us",
  dayTripAway: "A day trip away",
  dayTripWhere: (place, km, dir) => `${place}, ${km} km ${dir}`,
  addPhotoOnPage: "Your photo is on this page",
  yourPhoto: "Your photograph",
  yourPhotos: "Your photographs",
  photoMore: "More",
  photoDeleteTitle: "Delete this photo?",
  photoDeleteBody: "It leaves your trees. If it is already on the tree's page, it stays there.",
  photoDeleteBtn: "Delete photo",
  photoDeleted: "Photo deleted",
  addPhotoSeeMine: "See it in My trees",
  havePhotographed: "Have you photographed this tree?",
  havePhotographedLine: "If yours shows the tree better, we can put it in place of the picture above, or beside it.",
  goNote: "The button above opens directions in your maps app.",
  approxNote: "The pin marks the area, not the tree itself, so look around this spot.",
  knowExactly: "Know exactly where it is?",
  couldUseHelp: "We could use your help.",
  researchedRemotely: "If you know this tree, you can tell us what we got wrong or left out.",
  knowMoreThanUs: "Do you know more than we do?",
  ifOlderTree: (c) => `If you know an older tree in ${c}, or see a mistake here, tell us and we'll correct it.`,
  citiesCrumb: "Cities",
  citiesTitle: "Every City We Have Mapped",
  citiesHeading: "Every city we have mapped",
  citiesLead: (c, t) => `${c} cities, ${t} trees.`,
  citiesDescription: "Every city on the map, by country: the remarkable old trees of each, verified, with their stories and exact spots.",
  exploreTitle: "Ancient Tree Map: every remarkable old tree, one map",
  exploreDescription: "The interactive map of every verified ancient tree on the site, each pin a tree worth standing in front of.",
  exploreHeading: "The ancient tree map",
  exploreNote: "Every pin is a tree worth the walk. Find one near you, or somewhere you are going.",
  exploreWhatH: "What is on this map",
  exploreWhatBody: (t, p, c) => `${t} trees in ${p} places across ${c} countries. Each pin opens a tree with its age, its species, why it is worth the walk, and directions from where you are.`,
  exploreWalksH: "The tightest walks",
  exploreWalksBody: "In these places the trees are close enough to walk past all of them in one afternoon:",
  exploreIslandsH: "Islands",
  exploreIslandsBody: "On an island the trees are a drive apart rather than a walk, but some grow nowhere else: dragon trees, laurel forest that outlived the Ice Age, pines taller than any on the mainland.",
  exploreNotH: "What is not on it, and why",
  exploreNotBody: "Every pin says how precise it is. A tree marked approximate means we know the park but not the trunk, and its page says so. We leave off trees on private land, and trees whose location is kept secret to protect them. A tree gets a pin because it is remarkable.",
  exploreBrowse: "Browse another way:",
  homeTitle: "Ancient Trees: remarkable old trees near you, mapped",
  homeDescription: "Find the remarkable old trees around you, each with its story, its sources, its exact spot and directions from where you stand.",
  homeHeroLead: "Trees worth the walk,",
  homeHeroEm: "wherever you are.",
  homeSub: "Made for people who love being outside. Find remarkable old trees nearby, walk past a few of them in an afternoon, read the story behind each one, and tick off the ones you visit.",
  homeFindH: "The trees near you, right now.",
  homeFindBody: "You see the remarkable old trees closest to where you are standing, with a walk time and directions to the nearest one.",
  homeWalkH: "A route past the ones worth seeing.",
  homeWalkBody: "The most remarkable trees, linked into one afternoon walk, each with its story and the month it looks its best.",
  homeCollectH: "Tick off the trees you visit.",
  homeCollectBody: "Check in at each tree and watch your collection grow by trees, cities and species. Rarer and older trees count for more.",
  homeDirectoryH: "Ancient trees anywhere",
  homeMission: "We are on a mission to map every remarkable tree in the world, and we could use your help. If you know a good tree, or want to map a whole city,",
  homeMissionLink: "tell us about it",
  mapFilterGroup: "Filter the map",
  mapFilterFav: "Want to visit",
  wantAdded: "Added to Want to visit",
  wantRemoved: "Removed from Want to visit",
  wantView: "View",
  wantUndo: "Undo",
  mapFilterMine: "Collected",
  mapFilterSpecies: "Species",
  mapFilterFree: "Free to visit",
  exploreWalkItem: (n, d) => `${n} trees, ${d} apart`,
  homeVerbFind: "Find",
  homeVerbWalk: "Walk",
  homeVerbCollect: "Collect",
  homeNearestChip: "Nearest to you",
  homeMinWalk: (n) => `${n} min walk`,
  homeWalkChip: "Afternoon walk",
  homeTreesCount: (n) => `${n} trees`,
  homeAboutTime: "about 1h 10m",
  homePhoneTitle: "Your trees",
  homeStatTrees: "trees",
  homeStatCities: "cities",
  homeStatOldest: "years old",
  homeCollectedSpecies: "Collected species",
  homeDirTopCities: "Top cities",
  homeDirCollections: "Collections",
  homeDirOldest: "Oldest trees",
  homeDirTopSpecies: "Top species",
  homeAllCities: (n) => `All ${n} cities`,
  homeAllCollections: "All collections",
  homeOldestOfAll: "The oldest of all",
  homeAllSpecies: (n) => `All ${n} species`,
  homeFavH: "Our favourite tree cities",
  homeOldestShelfH: "The oldest trees we map",
  homeCountriesH: "Countries",
  homeAllCountries: "All countries",
  homeSpeciesH: "Species",
  homeParksH: "Parks",
  homeAllParks: "All parks",
  seeAll: "See all",
  gettingThere: "Getting there",
  readLess: "Read less",
  noPhotoAsk: "Been here? Yours would be the first on this page.",
  notesHeading: "From people who stood here",
  notesNone: "Nobody has written about this tree yet.",
  notesBorrowed: "Nearby, at {tree}, a visitor left this:",
  notesEmptyTitle: "No notes yet",
  notesEmptyAsk: "Did you visit the tree? Leave a note for the next visitor.",
  noteWrite: "Write a note",
  noteEditMine: "Edit your note",
  photoAddTitle: "Your photo here",
  photoAddAsk: "Seen this tree? Show the next visitor how it looks.",
  noteAsk: "Leave a note for the next visitor",
  noteSheetTitle: "A note for the next visitor",
  notePlaceholder: "What should they know? Where to stand, when to come, what you noticed.",
  noteExamples: "For example: “Best seen from the north side around four, when the sun comes through.” Or: “There was a church on this square until 1755.”",
  noteShownAs: (name) => `Shown as ${name} with today's date. Public right away.`,
  noteShownAnon: "Shown as “A visitor” with today's date. Public right away.",
  noteAdd: "Add note",
  noteSave: "Save note",
  noteDelete: "Delete note",
  noteSaving: "Saving...",
  noteFailed: "That did not go through. Try again in a moment.",
  noteSignIn: "Sign in first, then write your note.",
  noteYours: "Your note",
  noteVisitor: "A visitor",
  homeShelfMeta: (n, country) => `${n} trees \u00b7 ${country}`,
};

const TABLE: Record<string, Partial<UIStrings>> = {
  es: {
    homeVerbFind: "Encuentra",
    homeVerbWalk: "Pasea",
    homeVerbCollect: "Colecciona",
    homeNearestChip: "El más cercano a ti",
    homeMinWalk: (n) => `${n} min a pie`,
    homeWalkChip: "Paseo de una tarde",
    homeTreesCount: (n) => `${n} árboles`,
    homeAboutTime: "unos 1h 10m",
    homePhoneTitle: "Tus árboles",
    homeStatTrees: "árboles",
    homeStatCities: "ciudades",
    homeStatOldest: "años",
    homeCollectedSpecies: "Especies coleccionadas",
    homeDirTopCities: "Ciudades destacadas",
    homeDirCollections: "Colecciones",
    homeDirOldest: "Los más viejos",
    homeDirTopSpecies: "Especies destacadas",
    homeAllCities: (n) => `Las ${n} ciudades`,
    homeAllCollections: "Todas las colecciones",
    homeOldestOfAll: "Los más viejos de todos",
    homeAllSpecies: (n) => `Las ${n} especies`,
    homeFavH: "Nuestras ciudades de árboles favoritas",
    homeOldestShelfH: "Los árboles más viejos que cartografiamos",
    homeCountriesH: "Países",
    homeAllCountries: "Todos los países",
    homeSpeciesH: "Especies",
    homeParksH: "Parques",
    homeAllParks: "Todos los parques",
    seeAll: "Ver todo",
    gettingThere: "Cómo llegar",
    readLess: "Leer menos",
    noPhotoAsk: "¿Has estado aquí? La tuya sería la primera en esta página.",
    notesHeading: "De quienes estuvieron aquí",
    notesNone: "Nadie ha escrito todavía sobre este árbol.",
    notesBorrowed: "Cerca, en {tree}, un visitante dejó esto:",
    notesEmptyTitle: "Aún no hay notas",
    notesEmptyAsk: "¿Has visitado el árbol? Deja una nota para el próximo visitante.",
    noteWrite: "Escribir una nota",
    noteEditMine: "Editar tu nota",
    photoAddTitle: "Tu foto aquí",
    photoAddAsk: "¿Has visto este árbol? Enseña al próximo visitante cómo es.",
    noteAsk: "Deja una nota para el próximo visitante",
    noteSheetTitle: "Una nota para el próximo visitante",
    notePlaceholder: "¿Qué debería saber? Dónde ponerse, cuándo venir, qué te llamó la atención.",
    noteExamples: "Por ejemplo: «Se ve mejor desde el lado norte hacia las cuatro, cuando entra el sol». O: «En esta plaza hubo una iglesia hasta 1755».",
    noteShownAs: (name) => `Aparece como ${name} con la fecha de hoy. Pública al instante.`,
    noteShownAnon: "Aparece como «Un visitante» con la fecha de hoy. Pública al instante.",
    noteAdd: "Añadir nota",
    noteSave: "Guardar nota",
    noteDelete: "Eliminar nota",
    noteSaving: "Guardando...",
    noteFailed: "No se ha enviado. Inténtalo de nuevo en un momento.",
    noteSignIn: "Inicia sesión primero y luego escribe tu nota.",
    noteYours: "Tu nota",
    noteVisitor: "Un visitante",
    homeShelfMeta: (n, country) => `${n} árboles \u00b7 ${country}`,
    exploreWalkItem: (n, d) => `${n} árboles en ${d}`,
    citiesCrumb: "Ciudades",
    citiesTitle: "Todas las ciudades del mapa",
    citiesHeading: "Todas las ciudades del mapa",
    citiesLead: (c, t) => `${c} ciudades, ${t} árboles.`,
    citiesDescription: "Todas las ciudades del mapa, por país: los árboles viejos y notables de cada una, verificados, con su historia y su sitio exacto.",
    exploreTitle: "Mapa de árboles históricos del mundo",
    exploreDescription: "El mapa interactivo de todos los árboles históricos verificados del sitio, cada marcador un árbol ante el que merece la pena plantarse.",
    exploreHeading: "El mapa de árboles históricos",
    exploreNote: "Cada marcador es un árbol que merece el paseo. Encuentra uno cerca de ti, o donde vayas a ir.",
    exploreWhatH: "Qué hay en este mapa",
    exploreWhatBody: (t, p, c) => `${t} árboles en ${p} lugares de ${c} países. Cada marcador abre un árbol con su edad, su especie, por qué merece el paseo y cómo llegar desde donde estás.`,
    exploreWalksH: "Los paseos más compactos",
    exploreWalksBody: "En estos lugares los \u00e1rboles est\u00e1n lo bastante cerca como para verlos todos en una sola tarde a pie:",
    exploreIslandsH: "Islas",
    exploreIslandsBody: "En una isla los \u00e1rboles est\u00e1n a un trayecto en coche y no a un paseo, pero algunos no crecen en ning\u00fan otro sitio: dragos, laurisilva que sobrevivi\u00f3 a la glaciaci\u00f3n, pinos m\u00e1s altos que cualquiera del continente.",
    exploreNotH: "Qué no está, y por qué",
    exploreNotBody: "Cada marcador dice hasta qu\u00e9 punto es preciso. Un \u00e1rbol marcado como aproximado significa que conocemos el parque pero no el tronco, y su p\u00e1gina lo dice. Dejamos fuera los \u00e1rboles en terreno privado y los que tienen su ubicaci\u00f3n en secreto para protegerlos. Un \u00e1rbol tiene marcador porque es singular.",
    exploreBrowse: "Explora de otra manera:",
    homeTitle: "Ancient Trees: árboles singulares cerca de ti",
    homeDescription: "Encuentra los árboles históricos que tienes alrededor, cada uno con su historia, sus fuentes, su sitio exacto y cómo llegar desde donde estás.",
    homeHeroLead: "Árboles que merecen el paseo,",
    homeHeroEm: "estés donde estés.",
    homeSub: "Hecho para quien disfruta de estar al aire libre. Encuentra \u00e1rboles singulares cerca, pasa por unos cuantos en una tarde, lee la historia de cada uno y marca los que visitas.",
    homeFindH: "Los árboles que tienes cerca, ahora mismo.",
    homeFindBody: "Ves los \u00e1rboles singulares m\u00e1s cercanos al sitio donde est\u00e1s, con el tiempo a pie y c\u00f3mo llegar al m\u00e1s pr\u00f3ximo.",
    homeWalkH: "Una ruta que pasa por los que merecen la pena.",
    homeWalkBody: "Los \u00e1rboles m\u00e1s singulares, unidos en un paseo de una tarde, cada uno con su historia y el mes en que luce m\u00e1s.",
    homeCollectH: "Marca los árboles que visitas.",
    homeCollectBody: "Marca cada \u00e1rbol cuando est\u00e9s delante y mira crecer tu colecci\u00f3n en \u00e1rboles, ciudades y especies. Los \u00e1rboles m\u00e1s raros y m\u00e1s viejos cuentan m\u00e1s.",
    homeDirectoryH: "Árboles históricos en cualquier parte",
    homeMission: "Estamos cartografiando todos los árboles singulares del mundo, y nos vendría bien tu ayuda. Si conoces un buen árbol, o quieres cartografiar una ciudad entera,",
    homeMissionLink: "cuéntanoslo",
    mapFilterGroup: "Filtrar el mapa",
    mapFilterFav: "Quiero visitar",
    wantAdded: "Añadido a Quiero visitar",
    wantRemoved: "Quitado de Quiero visitar",
    wantView: "Ver",
    wantUndo: "Deshacer",
    mapFilterMine: "Coleccionados",
    mapFilterSpecies: "Especie",
    mapFilterFree: "Gratis",
    treeLabels: {
      "Youngest tree": "El más joven",
      "Urban curiosity": "Curiosidad urbana",
      "Continuously renewed": "Renovado continuamente",
      "Young regrowth": "Rebrote joven",
      "Deliberately planted, not inherited": "Plantado a propósito, no heredado",
      "Young replacement": "Reemplazo joven",
      "Ensemble": "Conjunto",
      "Recent planting, ancient provenance": "Plantación reciente, origen antiguo",
    },
    metaLead: (sp, age, where, size) => {
      const n = (v: number) => String(v).replace(".", ",");
      const m = size?.girth ? `de ${n(size.girth)} m de perímetro`
        : size?.height ? `de ${n(size.height)} m de altura` : "";
      return sp && age ? `${sp} de unos ${age} años en ${where}.`
        : sp && m ? `${sp} ${m} en ${where}.`
        : sp ? `${sp} en ${where}.`
        : age ? `Árbol de unos ${age} años en ${where}.`
        : m ? `Árbol ${m} en ${where}.` : `Árbol singular en ${where}.`;
    },
    distanceAway: (d) => `a ${d}`,
    labelSpecies: "Especie",
    labelRegister: "En el registro oficial",
    labelGirth: "Perímetro",
    labelAge: "Edad estimada",
    labelLocation: "Ubicación",
    labelAccess: "Acceso",
    labelGettingThere: "Cómo llegar",
    factAge: "Edad",
    factPin: "Ubicación",
    factYearsOld: "Años",
    locApprox: "Ubicación aproximada.",
    ticketNeeded: "Necesitas una entrada para ver este árbol",
    pinExact: "Exacta",
    pinApproximate: "Aproximada",
    discoverMore: "Descubre más",
    sourcesHeading: "Fuentes",
    sourcesLine: "De dónde salen los datos de esta página. La historia se escribió con IA a partir de estas fuentes, y los lectores que conocen el árbol la corrigen.",
    howWeCheck: "Cómo elegimos y comprobamos los árboles",
    takeMeThere: "Cómo llegar",
    showOnMap: "Ver en el mapa",
    showPhoto: "Ver la fotografía",
    openFullMap: "Abrir el mapa completo",
    dirTitle: "Abrir la ruta en",
    noPhotoYet: "Aún no hay fotografía",
    pinShowUs: "Muéstranos dónde está",
    pinTitle: "¿Dónde está en realidad?",
    pinHelp: "Mueve el mapa hasta que el marcador quede sobre el árbol.",
    pinZoom: "Ac\u00e9rcate todo lo que quieras. Podr\u00e1s enviarlo cuando hayas movido el marcador.",
    pinMoved: (m) => `Está a ${m} m de donde lo tenemos.`,
    pinSend: "El árbol está aquí",
    pinSending: "Enviando",
    pinDone: "Lo comprobaremos y moveremos el marcador.",
    pinFailed: "No se ha podido enviar. Inténtalo de nuevo en un momento.",
    pinNeedsAccount: "Necesitas una cuenta para enviarlo, as\u00ed podemos contarte qu\u00e9 ha cambiado con tu correcci\u00f3n.",
    cancel: "Cancelar",
    appleMaps: "Apple Maps",
    goBack: "Atrás",
    chipOldest: "Árbol más antiguo",
    googleMaps: "Google Maps",
    seenIt: "Coleccionar este árbol",
    worthItAsk: (n) => `Sí, ${n} mereció la visita`,
    worthItDone: (n) => `Te mereció la visita ${n}. Toca para deshacer`,
    seenItDone: "Coleccionado",
    collectTitle: (n) => `Coleccionar ${n}`,
    collectLead: "Haz una fotografía para añadirlo a tus árboles.",
    collectPhoto: "Elegir una fotografía",
    collectCamera: "Hacer una fotografía",
    collectLibrary: "Elegir de tus fotos",
    collectNoPhoto: "Coleccionar sin fotografía",
    collectedTitle: (n) => `Has coleccionado ${n}`,
    collectedOn: (d) => `El ${d}.`,
    uncollect: "Quitar de coleccionados",
    uncollected: "Quitado de coleccionados",
    uncollectQ: (n) => `¿Quitar ${n} de tus árboles coleccionados?`,
    uncollectBody: "Tus fotografías se quedan guardadas. Sale de Mis árboles hasta que lo vuelvas a coleccionar.",
    uncollectYes: "Quitar",
    keepIt: "Mantenerlo",
    nearbyTrees: "Árboles cercanos",
    somethingWrong: "Aquí hay algo mal",
    suggestAnother: "Sugerir otro árbol",
    share: "Compartir",
    shareCopied: "Enlace copiado",
    correctDetail: "Corregir un detalle de esta página",
    worthVote: (n) => `Sí, ${n} merecía la visita`,
    worthReport: "Algo no está bien",
    worthWhatsWrong: "¿Qué pasa?",
    worthDead: "Está muerto o ya no está",
    worthDeadQ: "¿Qué encontraste allí? (opcional)",
    worthDeadPh: "Un tocón, un tronco caído, nada en absoluto, y cuándo estuviste",
    worthWrongLoc: "Ubicación equivocada",
    worthWrongLocQ: "¿Dónde está en realidad? (opcional)",
    worthWrongLocPh: "Una esquina, un punto de referencia, o pega un pin del mapa",
    worthWhichTree: "No supe cuál era",
    worthWhichTreeQ: "¿Cuál miraste? (opcional)",
    worthWhichTreePh: "El tronco más grueso, el más cercano al camino, el del banco",
    worthCouldNotReach: "No pude llegar",
    worthCouldNotReachQ: "¿Qué te lo impidió? (opcional)",
    worthCouldNotReachPh: "Una verja cerrada, una valla, el horario, terreno privado",
    worthTwice: "Está dos veces en el mapa",
    worthTwiceQ: "¿Cuál es el otro árbol? (opcional)",
    worthTwicePh: "Su nombre, o dónde está el otro marcador",
    worthSomethingElse: "Otra cosa",
    worthSomethingElseQ: "Cuéntanoslo en una línea.",
    worthSomethingElsePh: "En qué nos equivocamos, o qué nos falta",
    worthThanks: "Gracias, lo comprobamos.",
    worthThanksDetail: "Gracias, eso ayuda.",
    worthDetailLabel: "¿Algo que nos ayude a comprobarlo? (opcional)",
    worthSend: "Enviar",
    actions: "Acciones",
    unknownAge: "edad desconocida",
    approxLocationChip: "ubicación aproximada",
    noPhotoLicence: "Todav\u00eda no tenemos una fotograf\u00eda de este \u00e1rbol.",
    addPhotoBtn: "Añadir una foto",
    addPhotoBtnQuiet: "Añade tu propia foto",
    photoCanGoHere: "Si t\u00fa has hecho una, puedes a\u00f1adirla aqu\u00ed.",
    addPhotoSignIn: "Inicia sesión primero y luego elige tu fotografía.",
    addPhotoSending: "Enviando...",
    addPhotoBadFile: "No se pudo leer esa imagen. Prueba con otra.",
    addPhotoThanks: "Gracias. Revisamos cada fotografía antes de publicarla, y te diremos qué pasó con la tuya.",
    addPhotoFailed: "Eso no se pudo enviar. Inténtalo de nuevo en un momento.",
    addPhotoWaiting: "Enviada a nosotros",
    dayTripAway: "A un día de excursión",
    dayTripWhere: (place, km, dir) => `${place}, a ${km} km ${({"north": "al norte", "north-east": "al noreste", "east": "al este", "south-east": "al sureste", "south": "al sur", "south-west": "al suroeste", "west": "al oeste", "north-west": "al noroeste"} as Record<string, string>)[dir] ?? dir}`,
    addPhotoOnPage: "Tu foto está en esta página",
    yourPhoto: "Tu fotografía",
    yourPhotos: "Tus fotografías",
    photoMore: "Más",
    photoDeleteTitle: "¿Eliminar esta foto?",
    photoDeleteBody: "Desaparece de tus árboles. Si ya está en la página del árbol, se queda allí.",
    photoDeleteBtn: "Eliminar foto",
    photoDeleted: "Foto eliminada",
    addPhotoSeeMine: "Verla en Mis árboles",
    havePhotographed: "¿Has fotografiado este árbol?",
    havePhotographedLine: "Si la tuya muestra mejor el \u00e1rbol, podemos ponerla en lugar de la foto de arriba, o a su lado.",
    goNote: "El botón de arriba abre las indicaciones en tu aplicación de mapas.",
    approxNote: "El marcador se\u00f1ala la zona, no el \u00e1rbol en s\u00ed, as\u00ed que busca por aqu\u00ed.",
    knowExactly: "¿Sabes exactamente dónde está?",
    couldUseHelp: "Nos vendría bien tu ayuda.",
    researchedRemotely: "Si conoces este \u00e1rbol, puedes decirnos qu\u00e9 hemos puesto mal o qu\u00e9 falta.",
    knowMoreThanUs: "¿Sabes más que nosotros?",
    ifOlderTree: (c) => `Si conoces un árbol más antiguo en ${c}, o ves aquí un error, dínoslo y lo corregimos.`,
    home: "Inicio",
    backToTrees: (n) => `\u2190 ${n === 1 ? "El \u00e1rbol" : `Los ${n} \u00e1rboles`}`,
    treesOnMap: (n) => `${n} ${n === 1 ? "\u00e1rbol" : "\u00e1rboles"} en el mapa`,
    heading: (c) => `\u00c1rboles hist\u00f3ricos de ${c}`,
    readMore: "Leer m\u00e1s",
    visitedOf: (n, city) => `visitados en ${city}`,
    seeCollection: "Ver tu colecci\u00f3n completa",
    mappingAll: "Estamos cartografiando todos los \u00e1rboles singulares del mundo.",
    missingOrWrong: (city) => `\u00bfConoces uno en ${city} que nos falte, o ves aqu\u00ed un error?`,
    tellUs: "Cu\u00e9ntanoslo",
    faqHeading: "Preguntas frecuentes",
    moreOnOldest: "M\u00e1s sobre el \u00e1rbol m\u00e1s antiguo",
    nearbyCities: "Árboles antiguos en ciudades cercanas",
    allCities: "Todas las ciudades del mapa",
    oldestQuestion: (city) => `\u00bfCu\u00e1l es el \u00e1rbol m\u00e1s antiguo de ${city}?`,
    fullAnswer: "La respuesta completa, con mapa y c\u00f3mo llegar.",
    suggestTree: "\u00bfConoces un \u00e1rbol que merezca estar en esta lista?",
    sendIt: "Env\u00edanoslo",
    walkRoutes: "Rutas a pie",
    inTheApp: "en la aplicaci\u00f3n",
    appPitchTreeTitle: "Colecciona los árboles que visitas",
    appPitchTreeBody: "Con la aplicación puedes marcar este, encontrar una ruta que pasa por unos cuantos más y ver crecer tu colección ciudad a ciudad.",
    appPitchCityTitle: "Visítalos con la aplicación",
    appPitchCityBody: "Con la aplicación puedes seguir una ruta a pie por estos árboles, guardar los que quieres ver y marcar cada uno que visitas.",
    appPitchCityBodyNoWalks: "Con la aplicación puedes guardar los árboles que quieres ver y marcar cada uno que visitas.",
    getTheApp: "Descargar la aplicación",
    whereAmI: "D\u00f3nde estoy",
    cardMore: "Leer m\u00e1s y c\u00f3mo llegar \u2192",
    cardSave: "Guardar",
    cardSaved: "Guardado",
    walkMoreTrees: (c) => `Recorre m\u00e1s \u00e1rboles en ${c}`,
    whatElseStands: (c) => `\u00bfQuieres saber qu\u00e9 m\u00e1s sigue en pie en ${c}? Mira`,
    allTreesLink: (n, c) => `los ${n} \u00e1rboles singulares de ${c}`,
    orDiscover: "o descubre",
    whichIsOldest: (c) => `cu\u00e1l es el \u00e1rbol m\u00e1s antiguo de ${c}`,
    moreTrees: "M\u00e1s \u00e1rboles",
    oldestTreeCrumb: "El \u00e1rbol m\u00e1s antiguo",
    fullStory: "La historia completa de este \u00e1rbol",
    cityHasMore: (c) => `${c} tiene m\u00e1s \u00e1rboles que merecen la visita:`,
    sentenceEnd: ".",
    photoCredit: (credit) => `Foto: ${credit}`,
    ambassadorRole: (place) => `Cuida la lista de ${place}`,
    ageYears: (n) => `${n} años`,
    seenChip: "Coleccionado",
    seasonChip: { bloom: "En flor", autumn: "Color de otoño", fruit: "Con fruto", leaves: "Hojas nuevas", catkins: "Amentos", winter: "Silueta invernal", peak: "En temporada" },
    ambassadorWanted: (place) => `Se busca quien cuide la lista de ${place}`,
    ambassadorWantedLine: "Ayúdanos a mejorar esta lista.",
    ambassadorApply: "Quiero hacerlo",
    ambassadorApplied: "Solicitud enviada.",
    ambassadorAskTitle: (place) => `¿Quieres cuidar la lista de ${place}?`,
    ambassadorsLabel: "Embajadores",
    ambassadorAskBody: "Un embajador nos ayuda a acertar con los \u00e1rboles de este lugar.",
    ambassadorAskPoints: ["Añade fotos de los árboles", "Comprueba los datos y dinos qué árboles faltan", "Ayuda a preparar paseos que pasen por ellos"],
    ambassadorAskSend: "Solicitar",
    ambassadorNotNow: "Ahora no",
    ambassadorSentTitle: "Solicitud enviada",
    ambassadorSentBody: "Pronto te escribiremos con algunas preguntas sobre la lista.",
    ambassadorWriteTo: (email) => `Te escribiremos a ${email}.`,
    ambassadorDone: "Hecho",
    photoOpen: "Abrir la fotografía",
    photoPrev: "Fotografía anterior",
    photoNext: "Fotografía siguiente",
    photoNumber: (n, total) => `Fotografía ${n} de ${total}`,
    appStoreBadge: "Consigue Ancient Trees en el App Store",
    openInApp: "Abrir en la app",
    androidTitle: "Estamos trabajando en la app de Android",
    androidNote: "Todavía no hay una app para Android. Deja tu correo y te escribiremos el día que la haya.",
    emailLabel: "Correo electrónico",
    notifyMe: "Avísame",
    waitlistSent: "Ya est\u00e1s en la lista. Te avisaremos cuando la aplicaci\u00f3n est\u00e9 en Android.",
    scanToOpen: "Escanéalo con tu teléfono para abrirlo ahí.",
    photoClose: "Cerrar",
    photoFull: "Verla a tamaño completo",
  },
  it: {
    homeVerbFind: "Trova",
    homeVerbWalk: "Cammina",
    homeVerbCollect: "Colleziona",
    homeNearestChip: "Il più vicino a te",
    homeMinWalk: (n) => `${n} min a piedi`,
    homeWalkChip: "Passeggiata di un pomeriggio",
    homeTreesCount: (n) => `${n} alberi`,
    homeAboutTime: "circa 1h 10m",
    homePhoneTitle: "I tuoi alberi",
    homeStatTrees: "alberi",
    homeStatCities: "città",
    homeStatOldest: "anni",
    homeCollectedSpecies: "Specie collezionate",
    homeDirTopCities: "Città principali",
    homeDirCollections: "Collezioni",
    homeDirOldest: "Gli alberi più vecchi",
    homeDirTopSpecies: "Specie principali",
    homeAllCities: (n) => `Tutte le ${n} città`,
    homeAllCollections: "Tutte le collezioni",
    homeOldestOfAll: "I più vecchi di tutti",
    homeAllSpecies: (n) => `Tutte le ${n} specie`,
    homeFavH: "Le nostre città di alberi preferite",
    homeOldestShelfH: "Gli alberi più vecchi che mappiamo",
    homeCountriesH: "Paesi",
    homeAllCountries: "Tutti i paesi",
    homeSpeciesH: "Specie",
    homeParksH: "Parchi",
    homeAllParks: "Tutti i parchi",
    seeAll: "Vedi tutti",
    gettingThere: "Come arrivare",
    readLess: "Leggi meno",
    noPhotoAsk: "Sei stato qui? La tua sarebbe la prima su questa pagina.",
    notesHeading: "Da chi è stato qui",
    notesNone: "Nessuno ha ancora scritto di questo albero.",
    notesBorrowed: "Qui vicino, a {tree}, un visitatore ha lasciato questo:",
    notesEmptyTitle: "Ancora nessuna nota",
    notesEmptyAsk: "Hai visitato l'albero? Lascia una nota per il prossimo visitatore.",
    noteWrite: "Scrivi una nota",
    noteEditMine: "Modifica la tua nota",
    photoAddTitle: "La tua foto qui",
    photoAddAsk: "Hai visto questo albero? Mostra al prossimo visitatore com'è.",
    noteAsk: "Lascia una nota per il prossimo visitatore",
    noteSheetTitle: "Una nota per il prossimo visitatore",
    notePlaceholder: "Cosa dovrebbe sapere? Dove mettersi, quando venire, cosa hai notato.",
    noteExamples: "Per esempio: “Si vede meglio dal lato nord verso le quattro, quando entra il sole.” Oppure: “Su questa piazza c'era una chiesa fino al 1755.”",
    noteShownAs: (name) => `Compare come ${name} con la data di oggi. Subito pubblica.`,
    noteShownAnon: "Compare come “Un visitatore” con la data di oggi. Subito pubblica.",
    noteAdd: "Aggiungi nota",
    noteSave: "Salva nota",
    noteDelete: "Elimina nota",
    noteSaving: "Salvataggio...",
    noteFailed: "Non è andata. Riprova tra un momento.",
    noteSignIn: "Prima accedi, poi scrivi la tua nota.",
    noteYours: "La tua nota",
    noteVisitor: "Un visitatore",
    homeShelfMeta: (n, country) => `${n} alberi \u00b7 ${country}`,
    exploreWalkItem: (n, d) => `${n} alberi in ${d}`,
    citiesCrumb: "Città",
    citiesTitle: "Tutte le città sulla mappa",
    citiesHeading: "Tutte le città sulla mappa",
    citiesLead: (c, t) => `${c} città, ${t} alberi.`,
    citiesDescription: "Tutte le città sulla mappa, per paese: gli alberi antichi e notevoli di ognuna, verificati, con la loro storia e il punto esatto.",
    exploreTitle: "Mappa degli alberi monumentali del mondo",
    exploreDescription: "La mappa interattiva di tutti gli alberi monumentali verificati del sito, ogni segnaposto un albero davanti a cui vale la pena fermarsi.",
    exploreHeading: "La mappa degli alberi monumentali",
    exploreNote: "Ogni segnaposto è un albero che vale la camminata. Trovane uno vicino a te, o dove stai andando.",
    exploreWhatH: "Che cosa c'è su questa mappa",
    exploreWhatBody: (t, p, c) => `${t} alberi in ${p} luoghi di ${c} paesi. Ogni segnaposto apre un albero con la sua età, la specie, il motivo per cui vale la passeggiata e le indicazioni da dove sei.`,
    exploreWalksH: "Le passeggiate più compatte",
    exploreWalksBody: "In questi posti gli alberi sono abbastanza vicini da vederli tutti a piedi in un solo pomeriggio:",
    exploreIslandsH: "Isole",
    exploreIslandsBody: "Su un'isola gli alberi distano un tragitto in auto e non una passeggiata, ma alcuni non crescono da nessun'altra parte: alberi del drago, laurisilva sopravvissuta all'era glaciale, pini pi\u00f9 alti di qualsiasi pino sulla terraferma.",
    exploreNotH: "Che cosa non c'è, e perché",
    exploreNotBody: "Ogni segnaposto dice quanto \u00e8 preciso. Un albero segnato come approssimativo vuol dire che conosciamo il parco ma non il tronco, e la sua pagina lo dice. Lasciamo fuori gli alberi su terreno privato e quelli la cui posizione \u00e8 tenuta segreta per proteggerli. Un albero ha un segnaposto perch\u00e9 \u00e8 notevole.",
    exploreBrowse: "Sfoglia in un altro modo:",
    homeTitle: "Ancient Trees: alberi monumentali vicino a te",
    homeDescription: "Trova gli alberi monumentali che hai intorno, ognuno con la sua storia, le sue fonti, il punto esatto e le indicazioni da dove sei.",
    homeHeroLead: "Alberi che valgono la camminata,",
    homeHeroEm: "ovunque tu sia.",
    homeSub: "Fatto per chi ama stare all'aperto. Trova alberi notevoli l\u00ec vicino, passane a vedere qualcuno in un pomeriggio, leggi la storia di ognuno e spunta quelli che visiti.",
    homeFindH: "Gli alberi vicino a te, adesso.",
    homeFindBody: "Vedi gli alberi notevoli pi\u00f9 vicini al punto in cui sei, con il tempo a piedi e le indicazioni per il pi\u00f9 vicino.",
    homeWalkH: "Un percorso che passa da quelli che valgono.",
    homeWalkBody: "Gli alberi pi\u00f9 notevoli, uniti in una passeggiata di un pomeriggio, ognuno con la sua storia e il mese in cui d\u00e0 il meglio.",
    homeCollectH: "Spunta gli alberi che visiti.",
    homeCollectBody: "Segna ogni albero quando ci sei davanti e guarda crescere la tua collezione di alberi, citt\u00e0 e specie. Gli alberi pi\u00f9 rari e pi\u00f9 vecchi valgono di pi\u00f9.",
    homeDirectoryH: "Alberi monumentali ovunque",
    homeMission: "Stiamo mappando tutti gli alberi notevoli del mondo, e il tuo aiuto ci serve. Se conosci un bell'albero, o vuoi mappare un'intera città,",
    homeMissionLink: "raccontacelo",
    mapFilterGroup: "Filtra la mappa",
    mapFilterFav: "Da visitare",
    wantAdded: "Aggiunto a Da visitare",
    wantRemoved: "Tolto da Da visitare",
    wantView: "Vedi",
    wantUndo: "Annulla",
    mapFilterMine: "Collezionati",
    mapFilterSpecies: "Specie",
    mapFilterFree: "Gratis",
    treeLabels: {
      "Youngest tree": "Il più giovane",
      "Urban curiosity": "Curiosità urbana",
      "Continuously renewed": "Rinnovato di continuo",
      "Young regrowth": "Ricaccio giovane",
      "Deliberately planted, not inherited": "Piantato apposta, non ereditato",
      "Young replacement": "Sostituto giovane",
      "Ensemble": "Insieme",
      "Recent planting, ancient provenance": "Impianto recente, origine antica",
    },
    metaLead: (sp, age, where, size) => {
      const n = (v: number) => String(v).replace(".", ",");
      const m = size?.girth ? `di ${n(size.girth)} m di circonferenza`
        : size?.height ? `alto ${n(size.height)} m` : "";
      return sp && age ? `${sp} di circa ${age} anni a ${where}.`
        : sp && m ? `${sp} ${m} a ${where}.`
        : sp ? `${sp} a ${where}.`
        : age ? `Albero di circa ${age} anni a ${where}.`
        : m ? `Albero ${m} a ${where}.` : `Albero monumentale a ${where}.`;
    },
    distanceAway: (d) => `a ${d}`,
    labelSpecies: "Specie",
    labelRegister: "Nel registro ufficiale",
    labelGirth: "Circonferenza",
    labelAge: "Età stimata",
    labelLocation: "Posizione",
    labelAccess: "Accesso",
    labelGettingThere: "Come arrivarci",
    factAge: "Età",
    factPin: "Posizione",
    factYearsOld: "Anni",
    locApprox: "Posizione approssimativa.",
    ticketNeeded: "Serve un biglietto per vedere questo albero",
    pinExact: "Esatta",
    pinApproximate: "Approssimativa",
    discoverMore: "Scopri di più",
    sourcesHeading: "Fonti",
    sourcesLine: "Da dove vengono i dati di questa pagina. La storia è stata scritta con l'IA a partire da queste fonti, e i lettori che conoscono l'albero la correggono.",
    howWeCheck: "Come scegliamo e verifichiamo gli alberi",
    takeMeThere: "Portami lì",
    showOnMap: "Mostra sulla mappa",
    showPhoto: "Mostra la fotografia",
    openFullMap: "Apri la mappa completa",
    dirTitle: "Apri il percorso in",
    noPhotoYet: "Ancora nessuna fotografia",
    pinShowUs: "Mostraci dov'è",
    pinTitle: "Dov'è davvero?",
    pinHelp: "Sposta la mappa finché il segnaposto non è sopra l'albero.",
    pinZoom: "Ingrandisci quanto vuoi. Puoi inviare quando hai spostato il segnaposto.",
    pinMoved: (m) => `È a ${m} m da dove lo abbiamo noi.`,
    pinSend: "L'albero è qui",
    pinSending: "Invio in corso",
    pinDone: "Lo controlleremo e sposteremo il segnaposto.",
    pinFailed: "Non è andato a buon fine. Riprova tra un momento.",
    pinNeedsAccount: "Ti serve un account per inviarlo, cos\u00ec possiamo dirti cosa ha cambiato la tua correzione.",
    cancel: "Annulla",
    appleMaps: "Apple Maps",
    goBack: "Indietro",
    chipOldest: "Albero più antico",
    googleMaps: "Google Maps",
    seenIt: "Colleziona questo albero",
    worthItAsk: (n) => `Sì, ${n} valeva la visita`,
    worthItDone: (n) => `Hai trovato ${n} degno della visita. Tocca per annullare`,
    seenItDone: "Collezionato",
    collectTitle: (n) => `Colleziona ${n}`,
    collectLead: "Scatta una fotografia per aggiungerlo ai tuoi alberi.",
    collectPhoto: "Scegli una fotografia",
    collectCamera: "Scatta una fotografia",
    collectLibrary: "Scegli dalle tue foto",
    collectNoPhoto: "Colleziona senza fotografia",
    collectedTitle: (n) => `Hai collezionato ${n}`,
    collectedOn: (d) => `Il ${d}.`,
    uncollect: "Togli dai collezionati",
    uncollected: "Tolto dai collezionati",
    uncollectQ: (n) => `Togliere ${n} dai tuoi alberi collezionati?`,
    uncollectBody: "Le tue fotografie restano salvate. Esce da I miei alberi finché non lo collezioni di nuovo.",
    uncollectYes: "Togli",
    keepIt: "Tienilo",
    nearbyTrees: "Alberi nei dintorni",
    somethingWrong: "Qui c'è un errore",
    suggestAnother: "Segnala un altro albero",
    share: "Condividi",
    shareCopied: "Link copiato",
    correctDetail: "Correggi un dettaglio di questa pagina",
    worthVote: (n) => `Sì, ${n} valeva la visita`,
    worthReport: "Qualcosa non va",
    worthWhatsWrong: "Che cosa non va?",
    worthDead: "È morto o non c'è più",
    worthDeadQ: "Che cosa hai trovato lì? (facoltativo)",
    worthDeadPh: "Un ceppo, un tronco caduto, niente del tutto, e quando ci sei stato",
    worthWrongLoc: "Posizione sbagliata",
    worthWrongLocQ: "Dov'è davvero? (facoltativo)",
    worthWrongLocPh: "Un angolo di strada, un punto di riferimento, o incolla un pin della mappa",
    worthWhichTree: "Non capivo quale fosse",
    worthWhichTreeQ: "Quale hai guardato? (facoltativo)",
    worthWhichTreePh: "Il tronco più grosso, quello vicino al sentiero, quello accanto alla panchina",
    worthCouldNotReach: "Non sono riuscito ad arrivarci",
    worthCouldNotReachQ: "Che cosa te lo ha impedito? (facoltativo)",
    worthCouldNotReachPh: "Un cancello chiuso, una recinzione, gli orari, terreno privato",
    worthTwice: "È due volte sulla mappa",
    worthTwiceQ: "Quale altro albero è? (facoltativo)",
    worthTwicePh: "Il suo nome, o dove si trova l'altro segnaposto",
    worthSomethingElse: "Altro",
    worthSomethingElseQ: "Raccontacelo in una riga.",
    worthSomethingElsePh: "Che cosa abbiamo sbagliato, o che cosa ci manca",
    worthThanks: "Grazie, controlliamo.",
    worthThanksDetail: "Grazie, questo aiuta.",
    worthDetailLabel: "Qualcosa che ci aiuti a verificare? (facoltativo)",
    worthSend: "Invia",
    actions: "Azioni",
    unknownAge: "età sconosciuta",
    approxLocationChip: "posizione approssimativa",
    noPhotoLicence: "Non abbiamo ancora una fotografia di questo albero.",
    addPhotoBtn: "Aggiungi una foto",
    addPhotoBtnQuiet: "Aggiungi una tua foto",
    photoCanGoHere: "Se ne hai scattata una tu, puoi aggiungerla qui.",
    addPhotoSignIn: "Accedi prima, poi scegli la tua fotografia.",
    addPhotoSending: "Invio in corso...",
    addPhotoBadFile: "Non è stato possibile leggere questa immagine. Prova con un'altra.",
    addPhotoThanks: "Grazie. Guardiamo ogni fotografia prima che venga pubblicata, e ti diremo cosa ne è stato della tua.",
    addPhotoFailed: "L'invio non è andato a buon fine. Riprova tra poco.",
    addPhotoWaiting: "Inviata a noi",
    dayTripAway: "Una gita in giornata",
    dayTripWhere: (place, km, dir) => `${place}, ${km} km ${({"north": "a nord", "north-east": "a nord-est", "east": "a est", "south-east": "a sud-est", "south": "a sud", "south-west": "a sud-ovest", "west": "a ovest", "north-west": "a nord-ovest"} as Record<string, string>)[dir] ?? dir}`,
    addPhotoOnPage: "La tua foto è su questa pagina",
    yourPhoto: "La tua fotografia",
    yourPhotos: "Le tue fotografie",
    photoMore: "Altro",
    photoDeleteTitle: "Eliminare questa foto?",
    photoDeleteBody: "Esce dai tuoi alberi. Se è già sulla pagina dell'albero, resta lì.",
    photoDeleteBtn: "Elimina foto",
    photoDeleted: "Foto eliminata",
    addPhotoSeeMine: "Vedila in I miei alberi",
    havePhotographed: "Hai fotografato questo albero?",
    havePhotographedLine: "Se la tua mostra meglio l'albero, possiamo metterla al posto della foto qui sopra, o accanto.",
    goNote: "Il pulsante qui sopra apre le indicazioni nella tua app di mappe.",
    approxNote: "Il segnaposto indica la zona, non l'albero stesso, quindi guardati intorno qui.",
    knowExactly: "Sai esattamente dov'è?",
    couldUseHelp: "Ci farebbe comodo il tuo aiuto.",
    researchedRemotely: "Se conosci questo albero, puoi dirci cosa abbiamo sbagliato o tralasciato.",
    knowMoreThanUs: "Ne sai più di noi?",
    ifOlderTree: (c) => `Se conosci un albero più antico a ${c}, o vedi qui un errore, faccelo sapere e lo correggiamo.`,
    home: "Home",
    backToTrees: (n) => `\u2190 ${n === 1 ? "L\u2019albero" : `I ${n} alberi`}`,
    treesOnMap: (n) => `${n} ${n === 1 ? "albero" : "alberi"} sulla mappa`,
    heading: (c) => `Alberi monumentali di ${c}`,
    readMore: "Leggi di pi\u00f9",
    visitedOf: (n, city) => `visitati a ${city}`,
    seeCollection: "Vedi la tua collezione completa",
    mappingAll: "Stiamo mappando tutti gli alberi notevoli del mondo.",
    missingOrWrong: (city) => `Ne conosci uno a ${city} che ci manca, o vedi un errore qui?`,
    tellUs: "Segnalacelo",
    faqHeading: "Domande frequenti",
    moreOnOldest: "Altro sull'albero pi\u00f9 antico",
    nearbyCities: "Alberi antichi nelle città vicine",
    allCities: "Tutte le città sulla mappa",
    oldestQuestion: (city) => `Qual \u00e8 l'albero pi\u00f9 antico di ${city}?`,
    fullAnswer: "La risposta completa, con mappa e indicazioni.",
    suggestTree: "Conosci un albero che merita di stare in questo elenco?",
    sendIt: "Inviacelo",
    walkRoutes: "Percorsi a piedi",
    inTheApp: "nell'app",
    appPitchTreeTitle: "Colleziona gli alberi che visiti",
    appPitchTreeBody: "Con l'app puoi spuntare questo, trovare una passeggiata che ne tocca altri e veder crescere la tua collezione città dopo città.",
    appPitchCityTitle: "Visitali con l'app",
    appPitchCityBody: "Con l'app puoi seguire una passeggiata tra questi alberi, salvare quelli che vuoi vedere e spuntare ognuno che visiti.",
    appPitchCityBodyNoWalks: "Con l'app puoi salvare gli alberi che vuoi vedere e spuntare ognuno che visiti.",
    getTheApp: "Scarica l'app",
    whereAmI: "Dove mi trovo",
    cardMore: "Leggi di pi\u00f9 e come arrivare \u2192",
    cardSave: "Salva",
    cardSaved: "Salvato",
    walkMoreTrees: (c) => `Scopri altri alberi a ${c}`,
    whatElseStands: (c) => `Vuoi sapere che altro \u00e8 rimasto in piedi a ${c}? Guarda`,
    allTreesLink: (n, c) => `i ${n} alberi monumentali di ${c}`,
    orDiscover: "oppure scopri",
    whichIsOldest: (c) => `qual \u00e8 l'albero pi\u00f9 antico di ${c}`,
    moreTrees: "Altri alberi",
    oldestTreeCrumb: "L'albero pi\u00f9 antico",
    fullStory: "La storia completa di questo albero",
    cityHasMore: (c) => `${c} ha altri alberi che meritano la visita:`,
    sentenceEnd: ".",
    photoCredit: (credit) => `Foto: ${credit}`,
    ambassadorRole: (place) => `Cura la lista di ${place}`,
    ageYears: (n) => `${n} anni`,
    seenChip: "Collezionato",
    seasonChip: { bloom: "In fiore", autumn: "Colori d'autunno", fruit: "Con frutti", leaves: "Foglie nuove", catkins: "Amenti", winter: "Sagoma invernale", peak: "Di stagione" },
    ambassadorWanted: (place) => `Cerchiamo chi curi la lista di ${place}`,
    ambassadorWantedLine: "Aiutaci a migliorare questa lista.",
    ambassadorApply: "Mi candido",
    ambassadorApplied: "Richiesta inviata.",
    ambassadorAskTitle: (place) => `Vuoi curare la lista di ${place}?`,
    ambassadorsLabel: "Ambasciatori",
    ambassadorAskBody: "Un ambasciatore ci aiuta a raccontare bene gli alberi di questo posto.",
    ambassadorAskPoints: ["Aggiungi foto degli alberi", "Controlla i dati e dicci quali alberi mancano", "Aiuta a preparare passeggiate che li toccano"],
    ambassadorAskSend: "Candidati",
    ambassadorNotNow: "Non ora",
    ambassadorSentTitle: "Richiesta inviata",
    ambassadorSentBody: "Presto ti scriveremo con qualche domanda sulla lista.",
    ambassadorWriteTo: (email) => `Ti scriveremo a ${email}.`,
    ambassadorDone: "Fatto",
    photoOpen: "Apri la fotografia",
    photoPrev: "Fotografia precedente",
    photoNext: "Fotografia successiva",
    photoNumber: (n, total) => `Fotografia ${n} di ${total}`,
    appStoreBadge: "Scarica Ancient Trees su App Store",
    openInApp: "Apri nella app",
    androidTitle: "Stiamo lavorando alla app per Android",
    androidNote: "Non c'è ancora una app per Android. Lascia la tua email e ti scriveremo il giorno in cui ci sarà.",
    emailLabel: "Indirizzo email",
    notifyMe: "Avvisami",
    waitlistSent: "Sei in lista. Ti avviseremo quando l'app sar\u00e0 su Android.",
    scanToOpen: "Scansionalo con il telefono per aprirlo lì.",
    photoClose: "Chiudi",
    photoFull: "Vedila a dimensione intera",
  },
  nl: {
    homeVerbFind: "Vind",
    homeVerbWalk: "Wandel",
    homeVerbCollect: "Verzamel",
    homeNearestChip: "Dichtst bij jou",
    homeMinWalk: (n) => `${n} min lopen`,
    homeWalkChip: "Middagwandeling",
    homeTreesCount: (n) => `${n} bomen`,
    homeAboutTime: "ongeveer 1u 10m",
    homePhoneTitle: "Jouw bomen",
    homeStatTrees: "bomen",
    homeStatCities: "steden",
    homeStatOldest: "jaar oud",
    homeCollectedSpecies: "Verzamelde soorten",
    homeDirTopCities: "Belangrijkste steden",
    homeDirCollections: "Collecties",
    homeDirOldest: "Oudste bomen",
    homeDirTopSpecies: "Belangrijkste soorten",
    homeAllCities: (n) => `Alle ${n} steden`,
    homeAllCollections: "Alle collecties",
    homeOldestOfAll: "De oudste van allemaal",
    homeAllSpecies: (n) => `Alle ${n} soorten`,
    homeFavH: "Onze favoriete bomensteden",
    homeOldestShelfH: "De oudste bomen die we in kaart brengen",
    homeCountriesH: "Landen",
    homeAllCountries: "Alle landen",
    homeSpeciesH: "Soorten",
    homeParksH: "Parken",
    homeAllParks: "Alle parken",
    seeAll: "Alles bekijken",
    gettingThere: "Hoe kom je er",
    readLess: "Minder lezen",
    noPhotoAsk: "Hier geweest? Die van jou zou de eerste op deze pagina zijn.",
    notesHeading: "Van mensen die hier stonden",
    notesNone: "Nog niemand heeft over deze boom geschreven.",
    notesBorrowed: "Vlakbij, bij {tree}, liet een bezoeker dit achter:",
    notesEmptyTitle: "Nog geen notities",
    notesEmptyAsk: "Ben je bij de boom geweest? Laat een notitie achter voor de volgende bezoeker.",
    noteWrite: "Schrijf een notitie",
    noteEditMine: "Bewerk je notitie",
    photoAddTitle: "Jouw foto hier",
    photoAddAsk: "Deze boom gezien? Laat de volgende bezoeker zien hoe hij eruitziet.",
    noteAsk: "Laat een notitie achter voor de volgende bezoeker",
    noteSheetTitle: "Een notitie voor de volgende bezoeker",
    notePlaceholder: "Wat moet die weten? Waar je gaat staan, wanneer je komt, wat je opviel.",
    noteExamples: "Bijvoorbeeld: “Het mooist vanaf de noordkant rond vier uur, als de zon erdoor valt.” Of: “Op dit plein stond tot 1755 een kerk.”",
    noteShownAs: (name) => `Getoond als ${name} met de datum van vandaag. Direct openbaar.`,
    noteShownAnon: "Getoond als “Een bezoeker” met de datum van vandaag. Direct openbaar.",
    noteAdd: "Notitie plaatsen",
    noteSave: "Notitie opslaan",
    noteDelete: "Notitie verwijderen",
    noteSaving: "Opslaan...",
    noteFailed: "Dat is niet gelukt. Probeer het zo nog eens.",
    noteSignIn: "Log eerst in en schrijf dan je notitie.",
    noteYours: "Jouw notitie",
    noteVisitor: "Een bezoeker",
    homeShelfMeta: (n, country) => `${n} bomen \u00b7 ${country}`,
    exploreWalkItem: (n, d) => `${n} bomen binnen ${d}`,
    citiesCrumb: "Steden",
    citiesTitle: "Alle steden op de kaart",
    citiesHeading: "Alle steden op de kaart",
    citiesLead: (c, t) => `${c} steden, ${t} bomen.`,
    citiesDescription: "Alle steden op de kaart, per land: de oude en bijzondere bomen van elke stad, geverifieerd, met hun verhaal en de precieze plek.",
    exploreTitle: "Kaart met monumentale bomen wereldwijd",
    exploreDescription: "De interactieve kaart van alle geverifieerde monumentale bomen op de site, elke speld een boom om voor te gaan staan.",
    exploreHeading: "De kaart met monumentale bomen",
    exploreNote: "Elke speld is een boom die de wandeling waard is. Zoek er een bij jou in de buurt, of op de plek waar je heen gaat.",
    exploreWhatH: "Wat er op deze kaart staat",
    exploreWhatBody: (t, p, c) => `${t} bomen op ${p} plekken in ${c} landen. Elke speld opent een boom met zijn leeftijd, zijn soort, waarom hij de wandeling waard is, en de route vanaf waar je nu bent.`,
    exploreWalksH: "De kortste wandelingen",
    exploreWalksBody: "Op deze plekken staan de bomen dicht genoeg bij elkaar om ze in \u00e9\u00e9n middag allemaal langs te lopen:",
    exploreIslandsH: "Eilanden",
    exploreIslandsBody: "Op een eiland liggen de bomen een autorit uit elkaar in plaats van een wandeling, maar sommige groeien nergens anders: drakenbloedbomen, laurierbos dat de ijstijd overleefde, dennen die hoger worden dan op het vasteland.",
    exploreNotH: "Wat er niet op staat, en waarom",
    exploreNotBody: "Bij elke speld staat hoe precies hij is. Een boom die bij benadering staat aangegeven, betekent dat we het park kennen maar niet de stam, en zijn pagina zegt dat. Bomen op priv\u00e9terrein laten we weg, net als bomen waarvan de plek geheim wordt gehouden om ze te beschermen. Een boom krijgt een speld omdat hij bijzonder is.",
    exploreBrowse: "Blader op een andere manier:",
    homeTitle: "Ancient Trees: bijzondere oude bomen bij jou in de buurt",
    homeDescription: "Vind de bijzondere oude bomen om je heen, elk met zijn verhaal, zijn bronnen, de precieze plek en de route vanaf waar je staat.",
    homeHeroLead: "Bomen die de wandeling waard zijn,",
    homeHeroEm: "waar je ook bent.",
    homeSub: "Gemaakt voor wie graag buiten is. Vind bijzondere oude bomen in de buurt, loop er in \u00e9\u00e9n middag een paar langs, lees het verhaal achter elke boom en vink de bomen af die je bezoekt.",
    homeFindH: "De bomen bij jou in de buurt, nu.",
    homeFindBody: "Je ziet de bijzondere oude bomen die het dichtst bij je staan, met looptijd en de route naar de dichtstbijzijnde.",
    homeWalkH: "Een route langs de bomen die het waard zijn.",
    homeWalkBody: "De bijzonderste bomen, aan elkaar geregen tot \u00e9\u00e9n middagwandeling, elk met zijn verhaal en de maand waarin hij op zijn mooist is.",
    homeCollectH: "Vink de bomen af die je bezoekt.",
    homeCollectBody: "Vink elke boom af terwijl je ervoor staat en zie je verzameling groeien in bomen, steden en soorten. Zeldzamere en oudere bomen tellen zwaarder.",
    homeDirectoryH: "Monumentale bomen overal",
    homeMission: "We brengen alle bijzondere bomen ter wereld in kaart, en we kunnen je hulp gebruiken. Ken je een mooie boom, of wil je een hele stad in kaart brengen,",
    homeMissionLink: "laat het ons weten",
    mapFilterGroup: "Kaart filteren",
    mapFilterFav: "Wil ik bezoeken",
    wantAdded: "Toegevoegd aan Wil ik bezoeken",
    wantRemoved: "Verwijderd uit Wil ik bezoeken",
    wantView: "Bekijk",
    wantUndo: "Ongedaan maken",
    mapFilterMine: "Verzameld",
    mapFilterSpecies: "Soort",
    mapFilterFree: "Gratis",
    treeLabels: {
      "Youngest tree": "Jongste boom",
      "Urban curiosity": "Stadscuriositeit",
      "Continuously renewed": "Steeds vernieuwd",
      "Young regrowth": "Jonge opslag",
      "Deliberately planted, not inherited": "Bewust geplant, niet geërfd",
      "Young replacement": "Jonge vervanger",
      "Ensemble": "Ensemble",
      "Recent planting, ancient provenance": "Recent geplant, oude herkomst",
    },
    metaLead: (sp, age, where, size) => {
      const n = (v: number) => String(v).replace(".", ",");
      const m = size?.girth ? `met een stam van ${n(size.girth)} meter omtrek`
        : size?.height ? `van ${n(size.height)} meter hoog` : "";
      return sp && age ? `${sp} van ongeveer ${age} jaar in ${where}.`
        : sp && m ? `${sp} ${m} in ${where}.`
        : sp ? `${sp} in ${where}.`
        : age ? `Boom van ongeveer ${age} jaar in ${where}.`
        : m ? `Boom ${m} in ${where}.` : `Monumentale boom in ${where}.`;
    },
    distanceAway: (d) => `${d} verderop`,
    labelSpecies: "Soort",
    labelRegister: "In het officiële register",
    labelGirth: "Omtrek",
    labelAge: "Geschatte leeftijd",
    labelLocation: "Locatie",
    labelAccess: "Toegang",
    labelGettingThere: "Ernaartoe",
    factAge: "Leeftijd",
    factPin: "Locatie",
    factYearsOld: "Jaar oud",
    locApprox: "Locatie bij benadering.",
    ticketNeeded: "Je hebt een kaartje nodig om deze boom te zien",
    pinExact: "Exact",
    pinApproximate: "Bij benadering",
    discoverMore: "Ontdek meer",
    sourcesHeading: "Bronnen",
    sourcesLine: "Waar de gegevens op deze pagina vandaan komen. Het verhaal is met AI geschreven op basis van deze bronnen, en lezers die de boom kennen verbeteren het.",
    howWeCheck: "Hoe we bomen kiezen en controleren",
    takeMeThere: "Breng me erheen",
    showOnMap: "Toon op de kaart",
    showPhoto: "Toon de foto",
    openFullMap: "Open de hele kaart",
    dirTitle: "Open de route in",
    noPhotoYet: "Nog geen foto",
    pinShowUs: "Laat ons zien waar hij staat",
    pinTitle: "Waar staat hij echt?",
    pinHelp: "Versleep de kaart tot de speld op de boom staat.",
    pinZoom: "Zoom zo ver in als je wilt. Je kunt versturen zodra je de speld hebt verplaatst.",
    pinMoved: (m) => `Dat is ${m} m van waar wij hem hebben.`,
    pinSend: "De boom staat hier",
    pinSending: "Versturen",
    pinDone: "We controleren het en verplaatsen de speld.",
    pinFailed: "Dat is niet gelukt. Probeer het zo nog eens.",
    pinNeedsAccount: "Om dit te versturen heb je een account nodig, zodat we je kunnen laten weten wat je correctie heeft veranderd.",
    cancel: "Annuleren",
    appleMaps: "Apple Maps",
    goBack: "Terug",
    chipOldest: "Oudste boom",
    googleMaps: "Google Maps",
    seenIt: "Deze boom verzamelen",
    worthItAsk: (n) => `Ja, ${n} was de moeite waard`,
    worthItDone: (n) => `Je vond ${n} de moeite waard. Tik om het terug te nemen`,
    seenItDone: "Verzameld",
    collectTitle: (n) => `${n} verzamelen`,
    collectLead: "Maak een foto om hem aan je bomen toe te voegen.",
    collectPhoto: "Kies een foto",
    collectCamera: "Maak een foto",
    collectLibrary: "Kies uit je foto’s",
    collectNoPhoto: "Verzamelen zonder foto",
    collectedTitle: (n) => `Je hebt ${n} verzameld`,
    collectedOn: (d) => `Op ${d}.`,
    uncollect: "Uit verzameld halen",
    uncollected: "Uit verzameld gehaald",
    uncollectQ: (n) => `${n} uit je verzamelde bomen halen?`,
    uncollectBody: "Je foto’s ervan blijven bewaard. Hij verdwijnt uit Mijn bomen tot je hem opnieuw verzamelt.",
    uncollectYes: "Weghalen",
    keepIt: "Houden",
    nearbyTrees: "Bomen in de buurt",
    somethingWrong: "Hier klopt iets niet",
    suggestAnother: "Nog een boom aandragen",
    share: "Delen",
    shareCopied: "Link gekopieerd",
    correctDetail: "Een detail op deze pagina corrigeren",
    worthVote: (n) => `Ja, ${n} was het waard`,
    worthReport: "Er klopt iets niet",
    worthWhatsWrong: "Wat klopt er niet?",
    worthDead: "Hij is dood of weg",
    worthDeadQ: "Wat trof je er aan? (optioneel)",
    worthDeadPh: "Een stronk, een omgevallen stam, helemaal niets, en wanneer je er was",
    worthWrongLoc: "Verkeerde locatie",
    worthWrongLocQ: "Waar staat hij echt? (optioneel)",
    worthWrongLocPh: "Een straathoek, een herkenningspunt, of plak een kaartpin",
    worthWhichTree: "Ik wist niet welke boom",
    worthWhichTreeQ: "Welke heb je bekeken? (optioneel)",
    worthWhichTreePh: "De dikste stam, die het dichtst bij het pad, die bij het bankje",
    worthCouldNotReach: "Ik kon er niet bij",
    worthCouldNotReachQ: "Wat hield je tegen? (optioneel)",
    worthCouldNotReachPh: "Een hek op slot, een schutting, openingstijden, privéterrein",
    worthTwice: "Hij staat twee keer op de kaart",
    worthTwiceQ: "Welke andere boom is het? (optioneel)",
    worthTwicePh: "De naam, of waar de andere pin staat",
    worthSomethingElse: "Iets anders",
    worthSomethingElseQ: "Vertel het ons in één regel.",
    worthSomethingElsePh: "Wat we fout hebben, of wat we missen",
    worthThanks: "Dank je, we kijken ernaar.",
    worthThanksDetail: "Dank je, daar hebben we wat aan.",
    worthDetailLabel: "Iets wat ons helpt het na te gaan? (optioneel)",
    worthSend: "Versturen",
    actions: "Acties",
    unknownAge: "leeftijd onbekend",
    approxLocationChip: "locatie bij benadering",
    noPhotoLicence: "We hebben nog geen foto van deze boom.",
    addPhotoBtn: "Voeg een foto toe",
    addPhotoBtnQuiet: "Voeg je eigen foto toe",
    photoCanGoHere: "Heb je er zelf een gemaakt, dan kun je hem hier toevoegen.",
    addPhotoSignIn: "Log eerst in en kies dan je foto.",
    addPhotoSending: "Bezig met verzenden...",
    addPhotoBadFile: "Die foto kon niet worden gelezen. Probeer een andere.",
    addPhotoThanks: "Dank je. We bekijken elke foto voordat hij op een pagina komt, en je hoort wat ermee is gebeurd.",
    addPhotoFailed: "Dat is niet gelukt. Probeer het zo weer.",
    addPhotoWaiting: "Naar ons gestuurd",
    dayTripAway: "Een dagje uit",
    dayTripWhere: (place, km, dir) => `${place}, ${km} km ${({"north": "ten noorden", "north-east": "ten noordoosten", "east": "ten oosten", "south-east": "ten zuidoosten", "south": "ten zuiden", "south-west": "ten zuidwesten", "west": "ten westen", "north-west": "ten noordwesten"} as Record<string, string>)[dir] ?? dir}`,
    addPhotoOnPage: "Je foto staat op deze pagina",
    yourPhoto: "Jouw foto",
    yourPhotos: "Jouw foto's",
    photoMore: "Meer",
    photoDeleteTitle: "Deze foto verwijderen?",
    photoDeleteBody: "Hij verdwijnt uit je bomen. Staat hij al op de pagina van de boom, dan blijft hij daar.",
    photoDeleteBtn: "Foto verwijderen",
    photoDeleted: "Foto verwijderd",
    addPhotoSeeMine: "Bekijk hem bij Mijn bomen",
    havePhotographed: "Heb je deze boom gefotografeerd?",
    havePhotographedLine: "Laat jouw foto de boom beter zien, dan kunnen we hem in plaats van de foto hierboven zetten, of ernaast.",
    goNote: "De knop hierboven opent de route in je kaartenapp.",
    approxNote: "De speld wijst het gebied aan, niet de boom zelf, dus kijk hier even rond.",
    knowExactly: "Weet je precies waar hij staat?",
    couldUseHelp: "We kunnen je hulp gebruiken.",
    researchedRemotely: "Ken je deze boom, dan kun je ons laten weten wat er niet klopt of ontbreekt.",
    knowMoreThanUs: "Weet jij meer dan wij?",
    ifOlderTree: (c) => `Ken je een oudere boom in ${c}, of zie je hier een fout, laat het ons weten en we passen het aan.`,
    home: "Home",
    backToTrees: (n) => `\u2190 ${n === 1 ? "De boom" : `De ${n} bomen`}`,
    treesOnMap: (n) => `${n} ${n === 1 ? "boom" : "bomen"} op de kaart`,
    heading: (c) => `Monumentale bomen in ${c}`,
    readMore: "Lees meer",
    visitedOf: (n, city) => `bezocht in ${city}`,
    seeCollection: "Bekijk je hele collectie",
    mappingAll: "We brengen alle bijzondere bomen ter wereld in kaart.",
    missingOrWrong: (city) => `Ken je er een in ${city} die hier mist, of zie je een fout?`,
    tellUs: "Laat het ons weten",
    faqHeading: "Veelgestelde vragen",
    moreOnOldest: "Meer over de oudste boom",
    nearbyCities: "Oude bomen in steden in de buurt",
    allCities: "Alle steden op de kaart",
    oldestQuestion: (city) => `Wat is de oudste boom van ${city}?`,
    fullAnswer: "Het volledige antwoord, met kaart en route.",
    suggestTree: "Ken je een boom die in deze lijst thuishoort?",
    sendIt: "Stuur hem naar ons",
    walkRoutes: "Wandelroutes",
    inTheApp: "in de app",
    appPitchTreeTitle: "Verzamel de bomen die je bezoekt",
    appPitchTreeBody: "Met de app vink je deze af, vind je een wandeling langs nog een paar en zie je je verzameling per stad groeien.",
    appPitchCityTitle: "Bezoek ze met de app",
    appPitchCityBody: "Met de app volg je een wandeling langs deze bomen, bewaar je de bomen die je wilt zien en vink je elke boom af die je bezoekt.",
    appPitchCityBodyNoWalks: "Met de app bewaar je de bomen die je wilt zien en vink je elke boom af die je bezoekt.",
    getTheApp: "Download de app",
    whereAmI: "Waar ben ik",
    cardMore: "Lees meer en route \u2192",
    cardSave: "Bewaren",
    cardSaved: "Bewaard",
    walkMoreTrees: (c) => `Loop langs meer bomen in ${c}`,
    whatElseStands: (c) => `Benieuwd wat er nog meer overeind staat in ${c}? Bekijk`,
    allTreesLink: (n, c) => `de ${n} monumentale bomen van ${c}`,
    orDiscover: "of ontdek",
    whichIsOldest: (c) => `welke de oudste boom van ${c} is`,
    moreTrees: "Meer bomen",
    oldestTreeCrumb: "De oudste boom",
    fullStory: "Het volledige verhaal van deze boom",
    cityHasMore: (c) => `${c} heeft meer bomen die de moeite waard zijn:`,
    sentenceEnd: ".",
    photoCredit: (credit) => `Foto: ${credit}`,
    ambassadorRole: (place) => `Ambassadeur van ${place}`,
    ageYears: (n) => `${n} jaar`,
    seenChip: "Verzameld",
    seasonChip: { bloom: "In bloei", autumn: "Herfstkleur", fruit: "Vruchten", leaves: "Vers blad", catkins: "Katjes", winter: "Wintersilhouet", peak: "Nu op z'n mooist" },
    ambassadorWanted: (place) => `${place} zoekt een ambassadeur`,
    ambassadorWantedLine: "Help ons deze lijst te verbeteren.",
    ambassadorApply: "Ik doe mee",
    ambassadorApplied: "Aanvraag verstuurd.",
    ambassadorAskTitle: (place) => `Ambassadeur worden van ${place}?`,
    ambassadorsLabel: "Ambassadeurs",
    ambassadorAskBody: "Een ambassadeur helpt ons de bomen van deze plek goed te krijgen.",
    ambassadorAskPoints: ["Voeg foto's van de bomen toe", "Controleer de feiten en vertel ons welke bomen ontbreken", "Help wandelingen langs de bomen samen te stellen"],
    ambassadorAskSend: "Aanmelden",
    ambassadorNotNow: "Nu niet",
    ambassadorSentTitle: "Aanvraag verstuurd",
    ambassadorSentBody: "We mailen je binnenkort met een paar vragen over de lijst.",
    ambassadorWriteTo: (email) => `We mailen je op ${email}.`,
    ambassadorDone: "Klaar",
    photoOpen: "Open de foto",
    photoPrev: "Vorige foto",
    photoNext: "Volgende foto",
    photoNumber: (n, total) => `Foto ${n} van ${total}`,
    appStoreBadge: "Download Ancient Trees in de App Store",
    openInApp: "Openen in de app",
    androidTitle: "We werken aan de Android-app",
    androidNote: "Er is nog geen Android-app. Laat je e-mailadres achter en we schrijven je op de dag dat hij er is.",
    emailLabel: "E-mailadres",
    notifyMe: "Laat het me weten",
    waitlistSent: "Je staat op de lijst. We laten het je weten zodra de app op Android staat.",
    scanToOpen: "Scan dit met je telefoon om hem daar te openen.",
    photoClose: "Sluiten",
    photoFull: "Bekijk hem op volledige grootte",
  },
  de: {
    homeVerbFind: "Finden",
    homeVerbWalk: "Gehen",
    homeVerbCollect: "Sammeln",
    homeNearestChip: "Am nächsten bei dir",
    homeMinWalk: (n) => `${n} Min zu Fuß`,
    homeWalkChip: "Nachmittagsspaziergang",
    homeTreesCount: (n) => `${n} Bäume`,
    homeAboutTime: "etwa 1 Std 10 Min",
    homePhoneTitle: "Deine Bäume",
    homeStatTrees: "Bäume",
    homeStatCities: "Städte",
    homeStatOldest: "Jahre alt",
    homeCollectedSpecies: "Gesammelte Arten",
    homeDirTopCities: "Top-Städte",
    homeDirCollections: "Sammlungen",
    homeDirOldest: "Älteste Bäume",
    homeDirTopSpecies: "Top-Arten",
    homeAllCities: (n) => `Alle ${n} Städte`,
    homeAllCollections: "Alle Sammlungen",
    homeOldestOfAll: "Die ältesten von allen",
    homeAllSpecies: (n) => `Alle ${n} Arten`,
    homeFavH: "Unsere liebsten Baumstädte",
    homeOldestShelfH: "Die ältesten Bäume, die wir kartieren",
    homeCountriesH: "Länder",
    homeAllCountries: "Alle Länder",
    homeSpeciesH: "Arten",
    homeParksH: "Parks",
    homeAllParks: "Alle Parks",
    seeAll: "Alle ansehen",
    gettingThere: "Anfahrt",
    readLess: "Weniger lesen",
    noPhotoAsk: "Schon hier gewesen? Deins wäre das erste auf dieser Seite.",
    notesHeading: "Von Leuten, die hier standen",
    notesNone: "Noch niemand hat über diesen Baum geschrieben.",
    notesBorrowed: "Ganz in der Nähe, bei {tree}, hat ein Besucher dies hinterlassen:",
    notesEmptyTitle: "Noch keine Notizen",
    notesEmptyAsk: "Warst du am Baum? Hinterlass eine Notiz für den nächsten Besucher.",
    noteWrite: "Notiz schreiben",
    noteEditMine: "Deine Notiz bearbeiten",
    photoAddTitle: "Dein Foto hier",
    photoAddAsk: "Diesen Baum gesehen? Zeig dem nächsten Besucher, wie er aussieht.",
    noteAsk: "Hinterlass eine Notiz für den nächsten Besucher",
    noteSheetTitle: "Eine Notiz für den nächsten Besucher",
    notePlaceholder: "Was sollte er wissen? Wo man steht, wann man kommt, was dir aufgefallen ist.",
    noteExamples: "Zum Beispiel: „Am schönsten von der Nordseite gegen vier, wenn die Sonne durchkommt.“ Oder: „Auf diesem Platz stand bis 1755 eine Kirche.“",
    noteShownAs: (name) => `Erscheint als ${name} mit dem heutigen Datum. Sofort öffentlich.`,
    noteShownAnon: "Erscheint als „Ein Besucher“ mit dem heutigen Datum. Sofort öffentlich.",
    noteAdd: "Notiz hinzufügen",
    noteSave: "Notiz speichern",
    noteDelete: "Notiz löschen",
    noteSaving: "Wird gespeichert...",
    noteFailed: "Das hat nicht geklappt. Versuch es gleich noch einmal.",
    noteSignIn: "Melde dich zuerst an und schreib dann deine Notiz.",
    noteYours: "Deine Notiz",
    noteVisitor: "Ein Besucher",
    homeShelfMeta: (n, country) => `${n} Bäume \u00b7 ${country}`,
    exploreWalkItem: (n, d) => `${n} Bäume auf ${d}`,
    citiesCrumb: "Städte",
    citiesTitle: "Alle Städte auf der Karte",
    citiesHeading: "Alle Städte auf der Karte",
    citiesLead: (c, t) => `${c} Städte, ${t} Bäume.`,
    citiesDescription: "Alle Städte auf der Karte, nach Land: die alten und bemerkenswerten Bäume jeder Stadt, geprüft, mit ihrer Geschichte und dem genauen Standort.",
    exploreTitle: "Karte alter Bäume weltweit",
    exploreDescription: "Die interaktive Karte aller geprüften alten Bäume auf dieser Seite, jede Markierung ein Baum, vor dem es sich zu stehen lohnt.",
    exploreHeading: "Die Karte der alten Bäume",
    exploreNote: "Jede Markierung ist ein Baum, der den Weg lohnt. Finden Sie einen in Ihrer Nähe, oder dort, wo Sie hinfahren.",
    exploreWhatH: "Was auf dieser Karte steht",
    exploreWhatBody: (t, p, c) => `${t} Bäume an ${p} Orten in ${c} Ländern. Jede Markierung öffnet einen Baum mit seinem Alter, seiner Art, dem Grund, warum sich der Weg lohnt, und der Route von Ihrem Standort aus.`,
    exploreWalksH: "Die kürzesten Runden",
    exploreWalksBody: "An diesen Orten stehen die B\u00e4ume nah genug beieinander, um sie an einem Nachmittag alle zu Fu\u00df abzugehen:",
    exploreIslandsH: "Inseln",
    exploreIslandsBody: "Auf einer Insel liegen die B\u00e4ume eine Autofahrt statt eines Spaziergangs auseinander, aber manche wachsen sonst nirgends: Drachenb\u00e4ume, Lorbeerwald, der die Eiszeit \u00fcberdauert hat, Kiefern, h\u00f6her als jede auf dem Festland.",
    exploreNotH: "Was nicht darauf steht, und warum",
    exploreNotBody: "Jede Markierung sagt, wie genau sie ist. Ein Baum, der als ungef\u00e4hr gekennzeichnet ist, hei\u00dft: Wir kennen den Park, aber nicht den Stamm, und seine Seite sagt das. B\u00e4ume auf Privatgel\u00e4nde lassen wir weg, ebenso B\u00e4ume, deren Standort zu ihrem Schutz geheim gehalten wird. Ein Baum bekommt eine Markierung, weil er bemerkenswert ist.",
    exploreBrowse: "Anders stöbern:",
    homeTitle: "Ancient Trees: bemerkenswerte alte Bäume in Ihrer Nähe",
    homeDescription: "Finden Sie die bemerkenswerten alten Bäume um Sie herum, jeder mit seiner Geschichte, seinen Quellen, seinem genauen Standort und der Route von Ihnen aus.",
    homeHeroLead: "Bäume, die den Weg lohnen,",
    homeHeroEm: "wo Sie auch sind.",
    homeSub: "F\u00fcr alle, die gern drau\u00dfen sind. Finden Sie bemerkenswerte alte B\u00e4ume in der N\u00e4he, gehen Sie an einem Nachmittag an ein paar davon vorbei, lesen Sie die Geschichte hinter jedem und haken Sie die ab, die Sie besuchen.",
    homeFindH: "Die Bäume in Ihrer Nähe, gerade jetzt.",
    homeFindBody: "Sie sehen die bemerkenswerten alten B\u00e4ume, die Ihrem Standort am n\u00e4chsten stehen, mit Gehzeit und Route zum n\u00e4chstgelegenen.",
    homeWalkH: "Eine Route an den sehenswerten vorbei.",
    homeWalkBody: "Die bemerkenswertesten B\u00e4ume, zu einem Nachmittagsspaziergang verbunden, jeder mit seiner Geschichte und dem Monat, in dem er am sch\u00f6nsten ist.",
    homeCollectH: "Haken Sie die Bäume ab, die Sie besuchen.",
    homeCollectBody: "Haken Sie jeden Baum vor Ort ab und sehen Sie Ihre Sammlung an B\u00e4umen, St\u00e4dten und Arten wachsen. Seltenere und \u00e4ltere B\u00e4ume z\u00e4hlen mehr.",
    homeDirectoryH: "Alte Bäume überall",
    homeMission: "Wir kartieren alle bemerkenswerten Bäume der Welt, und wir können Ihre Hilfe gebrauchen. Wenn Sie einen guten Baum kennen oder eine ganze Stadt kartieren wollen,",
    homeMissionLink: "sagen Sie es uns",
    mapFilterGroup: "Karte filtern",
    mapFilterFav: "Will ich besuchen",
    wantAdded: "Zu Will ich besuchen hinzugefügt",
    wantRemoved: "Aus Will ich besuchen entfernt",
    wantView: "Ansehen",
    wantUndo: "Rückgängig",
    mapFilterMine: "Gesammelt",
    mapFilterSpecies: "Art",
    mapFilterFree: "Kostenlos",
    treeLabels: {
      "Youngest tree": "Jüngster Baum",
      "Urban curiosity": "Stadtkuriosität",
      "Continuously renewed": "Fortlaufend erneuert",
      "Young regrowth": "Junger Stockausschlag",
      "Deliberately planted, not inherited": "Bewusst gepflanzt, nicht geerbt",
      "Young replacement": "Junger Ersatz",
      "Ensemble": "Ensemble",
      "Recent planting, ancient provenance": "Junge Pflanzung, alte Herkunft",
    },
    metaLead: (sp, age, where, size) => {
      const n = (v: number) => String(v).replace(".", ",");
      const m = size?.girth ? `mit ${n(size.girth)} m Stammumfang`
        : size?.height ? `von ${n(size.height)} m Höhe` : "";
      return sp && age ? `${sp}, rund ${age} Jahre alt, in ${where}.`
        : sp && m ? `${sp} ${m} in ${where}.`
        : sp ? `${sp} in ${where}.`
        : age ? `Baum, rund ${age} Jahre alt, in ${where}.`
        : m ? `Baum ${m} in ${where}.` : `Bemerkenswerter Baum in ${where}.`;
    },
    distanceAway: (d) => `${d} entfernt`,
    labelSpecies: "Art",
    labelRegister: "Im amtlichen Register",
    labelGirth: "Umfang",
    labelAge: "Geschätztes Alter",
    labelLocation: "Standort",
    labelAccess: "Zugang",
    labelGettingThere: "Anfahrt",
    factAge: "Alter",
    factPin: "Standort",
    factYearsOld: "Jahre alt",
    locApprox: "Ungefährer Standort.",
    ticketNeeded: "Für diesen Baum brauchst du ein Ticket",
    pinExact: "Genau",
    pinApproximate: "Ungefähr",
    discoverMore: "Mehr entdecken",
    sourcesHeading: "Quellen",
    sourcesLine: "Woher die Angaben auf dieser Seite stammen. Die Geschichte wurde mit KI aus diesen Quellen geschrieben, und Leser, die den Baum kennen, korrigieren sie.",
    howWeCheck: "Wie wir Bäume auswählen und prüfen",
    takeMeThere: "Route planen",
    showOnMap: "Auf der Karte zeigen",
    showPhoto: "Foto zeigen",
    openFullMap: "Ganze Karte öffnen",
    dirTitle: "Route öffnen in",
    noPhotoYet: "Noch kein Foto",
    pinShowUs: "Zeig uns, wo er steht",
    pinTitle: "Wo steht er wirklich?",
    pinHelp: "Verschiebe die Karte, bis die Markierung auf dem Baum sitzt.",
    pinZoom: "Zoome so weit hinein, wie du willst. Senden kannst du, sobald du die Markierung verschoben hast.",
    pinMoved: (m) => `Das sind ${m} m von unserer Position entfernt.`,
    pinSend: "Der Baum steht hier",
    pinSending: "Wird gesendet",
    pinDone: "Wir prüfen es und verschieben die Markierung.",
    pinFailed: "Das hat nicht geklappt. Versuch es gleich noch einmal.",
    pinNeedsAccount: "Zum Senden brauchst du ein Konto, damit wir dir sagen k\u00f6nnen, was deine Korrektur ge\u00e4ndert hat.",
    cancel: "Abbrechen",
    appleMaps: "Apple Maps",
    goBack: "Zurück",
    chipOldest: "Ältester Baum",
    googleMaps: "Google Maps",
    seenIt: "Diesen Baum sammeln",
    worthItAsk: (n) => `Ja, ${n} war den Besuch wert`,
    worthItDone: (n) => `Du fandest ${n} sehenswert. Zum Zurücknehmen tippen`,
    seenItDone: "Gesammelt",
    collectTitle: (n) => `${n} sammeln`,
    collectLead: "Mach ein Foto, um ihn zu deinen Bäumen hinzuzufügen.",
    collectPhoto: "Foto auswählen",
    collectCamera: "Foto aufnehmen",
    collectLibrary: "Aus deinen Fotos wählen",
    collectNoPhoto: "Ohne Foto sammeln",
    collectedTitle: (n) => `Du hast ${n} gesammelt`,
    collectedOn: (d) => `Am ${d}.`,
    uncollect: "Aus Gesammelt entfernen",
    uncollected: "Aus Gesammelt entfernt",
    uncollectQ: (n) => `${n} aus deinen gesammelten Bäumen entfernen?`,
    uncollectBody: "Deine Fotos davon bleiben gespeichert. Er verschwindet aus Meine Bäume, bis du ihn wieder sammelst.",
    uncollectYes: "Entfernen",
    keepIt: "Behalten",
    nearbyTrees: "Bäume in der Nähe",
    somethingWrong: "Hier stimmt etwas nicht",
    suggestAnother: "Noch einen Baum vorschlagen",
    share: "Teilen",
    shareCopied: "Link kopiert",
    correctDetail: "Ein Detail auf dieser Seite korrigieren",
    worthVote: (n) => `Ja, ${n} war den Weg wert`,
    worthReport: "Hier stimmt etwas nicht",
    worthWhatsWrong: "Was stimmt nicht?",
    worthDead: "Er ist tot oder weg",
    worthDeadQ: "Was hast du dort vorgefunden? (optional)",
    worthDeadPh: "Einen Stumpf, einen umgestürzten Stamm, gar nichts, und wann du da warst",
    worthWrongLoc: "Falscher Standort",
    worthWrongLocQ: "Wo steht er wirklich? (optional)",
    worthWrongLocPh: "Eine Straßenecke, ein Orientierungspunkt, oder ein Karten-Pin",
    worthWhichTree: "Ich wusste nicht, welcher",
    worthWhichTreeQ: "Welchen hast du angesehen? (optional)",
    worthWhichTreePh: "Den dickeren Stamm, den am Weg, den neben der Bank",
    worthCouldNotReach: "Ich kam nicht hin",
    worthCouldNotReachQ: "Was hat dich aufgehalten? (optional)",
    worthCouldNotReachPh: "Ein verschlossenes Tor, ein Zaun, Öffnungszeiten, Privatgelände",
    worthTwice: "Er ist zweimal auf der Karte",
    worthTwiceQ: "Welcher andere Baum ist das? (optional)",
    worthTwicePh: "Sein Name, oder wo die andere Markierung ist",
    worthSomethingElse: "Etwas anderes",
    worthSomethingElseQ: "Sag es uns in einer Zeile.",
    worthSomethingElsePh: "Was wir falsch haben, oder was uns fehlt",
    worthThanks: "Danke, wir sehen es uns an.",
    worthThanksDetail: "Danke, das hilft.",
    worthDetailLabel: "Etwas, das uns beim Prüfen hilft? (optional)",
    worthSend: "Senden",
    actions: "Aktionen",
    unknownAge: "Alter unbekannt",
    approxLocationChip: "Standort ungefähr",
    noPhotoLicence: "Wir haben noch kein Foto von diesem Baum.",
    addPhotoBtn: "Foto hinzufügen",
    addPhotoBtnQuiet: "Eigenes Foto hinzufügen",
    photoCanGoHere: "Wenn du selbst eines aufgenommen hast, kannst du es hier hinzuf\u00fcgen.",
    addPhotoSignIn: "Melde dich zuerst an und wähle dann dein Foto.",
    addPhotoSending: "Wird gesendet...",
    addPhotoBadFile: "Dieses Bild konnte nicht gelesen werden. Versuch ein anderes.",
    addPhotoThanks: "Danke. Wir sehen uns jedes Foto an, bevor es auf einer Seite erscheint, und du erfährst, was aus deinem geworden ist.",
    addPhotoFailed: "Das hat nicht geklappt. Versuch es gleich noch einmal.",
    addPhotoWaiting: "An uns gesendet",
    dayTripAway: "Ein Tagesausflug",
    dayTripWhere: (place, km, dir) => `${place}, ${km} km ${({"north": "nördlich", "north-east": "nordöstlich", "east": "östlich", "south-east": "südöstlich", "south": "südlich", "south-west": "südwestlich", "west": "westlich", "north-west": "nordwestlich"} as Record<string, string>)[dir] ?? dir}`,
    addPhotoOnPage: "Dein Foto ist auf dieser Seite",
    yourPhoto: "Dein Foto",
    yourPhotos: "Deine Fotos",
    photoMore: "Mehr",
    photoDeleteTitle: "Dieses Foto löschen?",
    photoDeleteBody: "Es verschwindet aus deinen Bäumen. Steht es schon auf der Seite des Baums, bleibt es dort.",
    photoDeleteBtn: "Foto löschen",
    photoDeleted: "Foto gelöscht",
    addPhotoSeeMine: "In Meine Bäume ansehen",
    havePhotographed: "Hast du diesen Baum fotografiert?",
    havePhotographedLine: "Wenn deins den Baum besser zeigt, k\u00f6nnen wir es statt des Fotos oben zeigen oder daneben.",
    goNote: "Der Knopf oben öffnet die Route in Ihrer Karten-App.",
    approxNote: "Die Markierung zeigt den Bereich, nicht den Baum selbst. Schauen Sie sich hier also um.",
    knowExactly: "Wissen Sie genau, wo er steht?",
    couldUseHelp: "Wir können Ihre Hilfe gebrauchen.",
    researchedRemotely: "Wenn Sie diesen Baum kennen, k\u00f6nnen Sie uns sagen, was falsch ist oder fehlt.",
    knowMoreThanUs: "Wissen Sie mehr als wir?",
    ifOlderTree: (c) => `Wenn Sie in ${c} einen älteren Baum kennen oder hier einen Fehler sehen, sagen Sie es uns und wir korrigieren es.`,
    home: "Start",
    backToTrees: (n) => `\u2190 ${n === 1 ? "Der Baum" : `Die ${n} B\u00e4ume`}`,
    treesOnMap: (n) => `${n} ${n === 1 ? "Baum" : "B\u00e4ume"} auf der Karte`,
    heading: (c) => `Alte B\u00e4ume in ${c}`,
    readMore: "Mehr lesen",
    visitedOf: (n, city) => `in ${city} besucht`,
    seeCollection: "Ihre ganze Sammlung ansehen",
    mappingAll: "Wir kartieren alle bemerkenswerten B\u00e4ume der Welt.",
    missingOrWrong: (city) => `Kennen Sie einen in ${city}, der hier fehlt, oder sehen Sie einen Fehler?`,
    tellUs: "Sagen Sie es uns",
    faqHeading: "H\u00e4ufige Fragen",
    moreOnOldest: "Mehr zum \u00e4ltesten Baum",
    nearbyCities: "Alte Bäume in Städten in der Nähe",
    allCities: "Alle Städte auf der Karte",
    oldestQuestion: (city) => `Welcher ist der \u00e4lteste Baum in ${city}?`,
    fullAnswer: "Die vollst\u00e4ndige Antwort, mit Karte und Anfahrt.",
    suggestTree: "Kennen Sie einen Baum, der auf diese Liste geh\u00f6rt?",
    sendIt: "Schicken Sie ihn uns",
    walkRoutes: "Wanderrouten",
    inTheApp: "in der App",
    appPitchTreeTitle: "Sammle die Bäume, die du besuchst",
    appPitchTreeBody: "Mit der App hakst du diesen ab, findest einen Spaziergang an ein paar weiteren vorbei und siehst deine Sammlung Stadt für Stadt wachsen.",
    appPitchCityTitle: "Besuch sie mit der App",
    appPitchCityBody: "Mit der App folgst du einem Spaziergang an diesen Bäumen vorbei, speicherst die, die du sehen willst, und hakst jeden ab, den du besuchst.",
    appPitchCityBodyNoWalks: "Mit der App speicherst du die Bäume, die du sehen willst, und hakst jeden ab, den du besuchst.",
    getTheApp: "App holen",
    whereAmI: "Wo bin ich",
    cardMore: "Mehr lesen und Anfahrt \u2192",
    cardSave: "Merken",
    cardSaved: "Gemerkt",
    walkMoreTrees: (c) => `Mehr B\u00e4ume in ${c} ablaufen`,
    whatElseStands: (c) => `Wissen Sie, was in ${c} sonst noch steht? Sehen Sie`,
    allTreesLink: (n, c) => `die ${n} alten B\u00e4ume von ${c}`,
    orDiscover: "oder finden Sie heraus,",
    whichIsOldest: (c) => `welcher der \u00e4lteste Baum in ${c} ist`,
    moreTrees: "Mehr B\u00e4ume",
    oldestTreeCrumb: "Der \u00e4lteste Baum",
    fullStory: "Die ganze Geschichte dieses Baumes",
    cityHasMore: (c) => `${c} hat weitere B\u00e4ume, die den Weg lohnen:`,
    sentenceEnd: ".",
    photoCredit: (credit) => `Foto: ${credit}`,
    ambassadorRole: (place) => `Betreut die Liste für ${place}`,
    ageYears: (n) => `${n} Jahre`,
    seenChip: "Gesammelt",
    seasonChip: { bloom: "In Blüte", autumn: "Herbstfärbung", fruit: "Früchte", leaves: "Frisches Laub", catkins: "Kätzchen", winter: "Wintersilhouette", peak: "Jetzt am schönsten" },
    ambassadorWanted: (place) => `Wer betreut die Liste für ${place}?`,
    ambassadorWantedLine: "Hilf uns, diese Liste zu verbessern.",
    ambassadorApply: "Ich mache mit",
    ambassadorApplied: "Anfrage gesendet.",
    ambassadorAskTitle: (place) => `Die Liste für ${place} betreuen?`,
    ambassadorsLabel: "Botschafter",
    ambassadorAskBody: "Ein Botschafter hilft uns, die B\u00e4ume dieses Ortes richtig darzustellen.",
    ambassadorAskPoints: ["Füge Fotos der Bäume hinzu", "Prüfe die Angaben und sag uns, welche Bäume fehlen", "Hilf mit, Spaziergänge zu den Bäumen zusammenzustellen"],
    ambassadorAskSend: "Bewerben",
    ambassadorNotNow: "Nicht jetzt",
    ambassadorSentTitle: "Anfrage gesendet",
    ambassadorSentBody: "Wir schreiben dir bald mit ein paar Fragen zur Liste.",
    ambassadorWriteTo: (email) => `Wir schreiben dir an ${email}.`,
    ambassadorDone: "Fertig",
    photoOpen: "Foto öffnen",
    photoPrev: "Vorheriges Foto",
    photoNext: "Nächstes Foto",
    photoNumber: (n, total) => `Foto ${n} von ${total}`,
    appStoreBadge: "Ancient Trees im App Store laden",
    openInApp: "In der App öffnen",
    androidTitle: "Wir arbeiten an der Android-App",
    androidNote: "Es gibt noch keine Android-App. Hinterlasse deine E-Mail-Adresse und wir schreiben dir, sobald es sie gibt.",
    emailLabel: "E-Mail-Adresse",
    notifyMe: "Benachrichtige mich",
    waitlistSent: "Du stehst auf der Liste. Wir sagen dir Bescheid, sobald die App auf Android da ist.",
    scanToOpen: "Scanne dies mit deinem Telefon, um es dort zu öffnen.",
    photoClose: "Schließen",
    photoFull: "In voller Größe ansehen",
  },
  pt: {
    homeVerbFind: "Encontra",
    homeVerbWalk: "Caminha",
    homeVerbCollect: "Coleciona",
    homeNearestChip: "O mais perto de ti",
    homeMinWalk: (n) => `${n} min a pé`,
    homeWalkChip: "Passeio de uma tarde",
    homeTreesCount: (n) => `${n} árvores`,
    homeAboutTime: "cerca de 1h 10m",
    homePhoneTitle: "As tuas árvores",
    homeStatTrees: "árvores",
    homeStatCities: "cidades",
    homeStatOldest: "anos",
    homeCollectedSpecies: "Espécies colecionadas",
    homeDirTopCities: "Cidades principais",
    homeDirCollections: "Coleções",
    homeDirOldest: "Árvores mais velhas",
    homeDirTopSpecies: "Espécies principais",
    homeAllCities: (n) => `Todas as ${n} cidades`,
    homeAllCollections: "Todas as coleções",
    homeOldestOfAll: "As mais velhas de todas",
    homeAllSpecies: (n) => `Todas as ${n} espécies`,
    homeFavH: "As nossas cidades de árvores preferidas",
    homeOldestShelfH: "As árvores mais velhas que mapeamos",
    homeCountriesH: "Países",
    homeAllCountries: "Todos os países",
    homeSpeciesH: "Espécies",
    homeParksH: "Parques",
    homeAllParks: "Todos os parques",
    seeAll: "Ver tudo",
    gettingThere: "Como chegar",
    readLess: "Ler menos",
    noPhotoAsk: "Já esteve aqui? A sua seria a primeira nesta página.",
    notesHeading: "De quem esteve aqui",
    notesNone: "Ainda ninguém escreveu sobre esta árvore.",
    notesBorrowed: "Aqui perto, em {tree}, um visitante deixou isto:",
    notesEmptyTitle: "Ainda sem notas",
    notesEmptyAsk: "Visitou a árvore? Deixe uma nota para o próximo visitante.",
    noteWrite: "Escrever uma nota",
    noteEditMine: "Editar a sua nota",
    photoAddTitle: "A sua foto aqui",
    photoAddAsk: "Viu esta árvore? Mostre ao próximo visitante como ela é.",
    noteAsk: "Deixe uma nota para o próximo visitante",
    noteSheetTitle: "Uma nota para o próximo visitante",
    notePlaceholder: "O que deve saber? Onde ficar, quando vir, o que reparou.",
    noteExamples: "Por exemplo: “Vê-se melhor do lado norte por volta das quatro, quando entra o sol.” Ou: “Nesta praça houve uma igreja até 1755.”",
    noteShownAs: (name) => `Aparece como ${name} com a data de hoje. Pública de imediato.`,
    noteShownAnon: "Aparece como “Um visitante” com a data de hoje. Pública de imediato.",
    noteAdd: "Adicionar nota",
    noteSave: "Guardar nota",
    noteDelete: "Apagar nota",
    noteSaving: "A guardar...",
    noteFailed: "Não foi enviada. Tente de novo daqui a um momento.",
    noteSignIn: "Inicie sessão primeiro e depois escreva a sua nota.",
    noteYours: "A sua nota",
    noteVisitor: "Um visitante",
    homeShelfMeta: (n, country) => `${n} árvores \u00b7 ${country}`,
    exploreWalkItem: (n, d) => `${n} árvores em ${d}`,
    citiesCrumb: "Cidades",
    citiesTitle: "Todas as cidades do mapa",
    citiesHeading: "Todas as cidades do mapa",
    citiesLead: (c, t) => `${c} cidades, ${t} árvores.`,
    citiesDescription: "Todas as cidades do mapa, por país: as árvores velhas e notáveis de cada uma, verificadas, com a sua história e o sítio exacto.",
    exploreTitle: "Mapa de árvores antigas de todo o mundo",
    exploreDescription: "O mapa interativo de todas as árvores antigas verificadas do site, cada marcador uma árvore diante da qual vale a pena estar.",
    exploreHeading: "O mapa das árvores antigas",
    exploreNote: "Cada marcador é uma árvore que vale a caminhada. Encontre uma perto de si, ou no sítio para onde vai.",
    exploreWhatH: "O que está neste mapa",
    exploreWhatBody: (t, p, c) => `${t} árvores em ${p} lugares de ${c} países. Cada marcador abre uma árvore com a idade, a espécie, a razão por que vale o passeio e o caminho a partir de onde está.`,
    exploreWalksH: "Os percursos mais curtos",
    exploreWalksBody: "Nestes lugares as \u00e1rvores est\u00e3o perto o suficiente para as ver todas a p\u00e9 numa s\u00f3 tarde:",
    exploreIslandsH: "Ilhas",
    exploreIslandsBody: "Numa ilha as \u00e1rvores ficam a uma viagem de carro e n\u00e3o a um passeio, mas algumas n\u00e3o crescem em mais lado nenhum: dragoeiros, laurissilva que sobreviveu \u00e0 era glaciar, pinheiros mais altos do que qualquer um no continente.",
    exploreNotH: "O que não está, e porquê",
    exploreNotBody: "Cada marcador diz o qu\u00e3o preciso \u00e9. Uma \u00e1rvore marcada como aproximada quer dizer que conhecemos o parque mas n\u00e3o o tronco, e a p\u00e1gina dela di-lo. Deixamos de fora as \u00e1rvores em terreno privado e aquelas cuja localiza\u00e7\u00e3o \u00e9 mantida em segredo para as proteger. Uma \u00e1rvore tem marcador porque \u00e9 not\u00e1vel.",
    exploreBrowse: "Explore de outra maneira:",
    homeTitle: "Ancient Trees: árvores notáveis perto de si, no mapa",
    homeDescription: "Encontre as árvores antigas à sua volta, cada uma com a sua história, as suas fontes, o sítio exacto e o caminho a partir de onde está.",
    homeHeroLead: "Árvores que valem a caminhada,",
    homeHeroEm: "esteja onde estiver.",
    homeSub: "Feito para quem gosta de estar l\u00e1 fora. Encontre \u00e1rvores not\u00e1veis por perto, passe por algumas numa tarde, leia a hist\u00f3ria de cada uma e marque as que visita.",
    homeFindH: "As árvores perto de si, agora.",
    homeFindBody: "V\u00ea as \u00e1rvores not\u00e1veis mais pr\u00f3ximas do s\u00edtio onde est\u00e1, com o tempo a p\u00e9 e o caminho at\u00e9 \u00e0 mais perto.",
    homeWalkH: "Um percurso pelas que valem a visita.",
    homeWalkBody: "As \u00e1rvores mais not\u00e1veis, ligadas num passeio de uma tarde, cada uma com a sua hist\u00f3ria e o m\u00eas em que est\u00e1 no seu melhor.",
    homeCollectH: "Marque as árvores que visita.",
    homeCollectBody: "Marque cada \u00e1rvore quando estiver diante dela e veja a sua cole\u00e7\u00e3o crescer em \u00e1rvores, cidades e esp\u00e9cies. As \u00e1rvores mais raras e mais velhas contam mais.",
    homeDirectoryH: "Árvores antigas em qualquer lado",
    homeMission: "Estamos a mapear todas as árvores notáveis do mundo, e a sua ajuda seria bem-vinda. Se conhece uma boa árvore, ou quer mapear uma cidade inteira,",
    homeMissionLink: "diga-nos",
    mapFilterGroup: "Filtrar o mapa",
    mapFilterFav: "Quero visitar",
    wantAdded: "Adicionado a Quero visitar",
    wantRemoved: "Removido de Quero visitar",
    wantView: "Ver",
    wantUndo: "Desfazer",
    mapFilterMine: "Colecionadas",
    mapFilterSpecies: "Espécie",
    mapFilterFree: "Grátis",
    treeLabels: {
      "Youngest tree": "A mais nova",
      "Urban curiosity": "Curiosidade urbana",
      "Continuously renewed": "Renovada continuamente",
      "Young regrowth": "Rebento jovem",
      "Deliberately planted, not inherited": "Plantada de propósito, não herdada",
      "Young replacement": "Substituta jovem",
      "Ensemble": "Conjunto",
      "Recent planting, ancient provenance": "Plantação recente, origem antiga",
    },
    metaLead: (sp, age, where, size) => {
      const n = (v: number) => String(v).replace(".", ",");
      const m = size?.girth ? `com ${n(size.girth)} m de perímetro`
        : size?.height ? `com ${n(size.height)} m de altura` : "";
      return sp && age ? `${sp} com cerca de ${age} anos em ${where}.`
        : sp && m ? `${sp} ${m} em ${where}.`
        : sp ? `${sp} em ${where}.`
        : age ? `Árvore com cerca de ${age} anos em ${where}.`
        : m ? `Árvore ${m} em ${where}.` : `Árvore notável em ${where}.`;
    },
    distanceAway: (d) => `a ${d}`,
    labelSpecies: "Espécie",
    labelRegister: "No registo oficial",
    labelGirth: "Perímetro",
    labelAge: "Idade estimada",
    labelLocation: "Localização",
    labelAccess: "Acesso",
    labelGettingThere: "Como chegar",
    factAge: "Idade",
    factPin: "Localização",
    factYearsOld: "Anos",
    locApprox: "Localização aproximada.",
    ticketNeeded: "Precisas de bilhete para ver esta árvore",
    pinExact: "Exacta",
    pinApproximate: "Aproximada",
    discoverMore: "Descobrir mais",
    sourcesHeading: "Fontes",
    sourcesLine: "De onde vêm os dados desta página. A história foi escrita com IA a partir destas fontes, e os leitores que conhecem a árvore corrigem-na.",
    howWeCheck: "Como escolhemos e verificamos as árvores",
    takeMeThere: "Como chegar",
    showOnMap: "Ver no mapa",
    showPhoto: "Ver a fotografia",
    openFullMap: "Abrir o mapa completo",
    dirTitle: "Abrir o percurso em",
    noPhotoYet: "Ainda sem fotografia",
    pinShowUs: "Mostre-nos onde está",
    pinTitle: "Onde está realmente?",
    pinHelp: "Arraste o mapa até o marcador ficar sobre a árvore.",
    pinZoom: "Aproxime o quanto quiser. Pode enviar quando tiver movido o marcador.",
    pinMoved: (m) => `Fica a ${m} m de onde a temos.`,
    pinSend: "A árvore está aqui",
    pinSending: "A enviar",
    pinDone: "Vamos verificar e mover o marcador.",
    pinFailed: "Não foi possível enviar. Tente de novo daqui a pouco.",
    pinNeedsAccount: "Precisa de uma conta para enviar, para lhe podermos dizer o que a sua corre\u00e7\u00e3o mudou.",
    cancel: "Cancelar",
    appleMaps: "Apple Maps",
    goBack: "Voltar",
    chipOldest: "Árvore mais antiga",
    googleMaps: "Google Maps",
    seenIt: "Colecionar esta árvore",
    worthItAsk: (n) => `Sim, ${n} valeu a visita`,
    worthItDone: (n) => `Achaste ${n} digna da visita. Toca para desfazer`,
    seenItDone: "Colecionada",
    collectTitle: (n) => `Colecionar ${n}`,
    collectLead: "Tira uma fotografia para a juntar às tuas árvores.",
    collectPhoto: "Escolher uma fotografia",
    collectCamera: "Tirar uma fotografia",
    collectLibrary: "Escolher das tuas fotos",
    collectNoPhoto: "Colecionar sem fotografia",
    collectedTitle: (n) => `Colecionaste ${n}`,
    collectedOn: (d) => `Em ${d}.`,
    uncollect: "Retirar das colecionadas",
    uncollected: "Retirada das colecionadas",
    uncollectQ: (n) => `Retirar ${n} das tuas árvores colecionadas?`,
    uncollectBody: "As tuas fotografias ficam guardadas. Sai de As minhas árvores até a colecionares de novo.",
    uncollectYes: "Retirar",
    keepIt: "Manter",
    nearbyTrees: "Árvores por perto",
    somethingWrong: "Há aqui um erro",
    suggestAnother: "Sugerir outra árvore",
    share: "Partilhar",
    shareCopied: "Ligação copiada",
    correctDetail: "Corrigir um detalhe desta página",
    worthVote: (n) => `Sim, ${n} valeu a visita`,
    worthReport: "Há aqui algo errado",
    worthWhatsWrong: "O que está errado?",
    worthDead: "Está morta ou já não existe",
    worthDeadQ: "O que encontrou lá? (opcional)",
    worthDeadPh: "Um cepo, um tronco caído, nada de nada, e quando lá esteve",
    worthWrongLoc: "Localização errada",
    worthWrongLocQ: "Onde está na realidade? (opcional)",
    worthWrongLocPh: "Uma esquina, um ponto de referência, ou cole um pin do mapa",
    worthWhichTree: "Não percebi qual era",
    worthWhichTreeQ: "Qual delas viu? (opcional)",
    worthWhichTreePh: "O tronco mais grosso, o mais perto do caminho, o do banco",
    worthCouldNotReach: "Não consegui chegar",
    worthCouldNotReachQ: "O que o impediu? (opcional)",
    worthCouldNotReachPh: "Um portão fechado, uma vedação, horários, terreno privado",
    worthTwice: "Está duas vezes no mapa",
    worthTwiceQ: "Que outra árvore é? (opcional)",
    worthTwicePh: "O nome, ou onde está o outro marcador",
    worthSomethingElse: "Outra coisa",
    worthSomethingElseQ: "Conte-nos numa linha.",
    worthSomethingElsePh: "Aquilo em que erramos, ou o que nos falta",
    worthThanks: "Obrigado, vamos verificar.",
    worthThanksDetail: "Obrigado, isso ajuda.",
    worthDetailLabel: "Algo que nos ajude a verificar? (opcional)",
    worthSend: "Enviar",
    actions: "Ações",
    unknownAge: "idade desconhecida",
    approxLocationChip: "localização aproximada",
    noPhotoLicence: "Ainda n\u00e3o temos uma fotografia desta \u00e1rvore.",
    addPhotoBtn: "Adicionar uma foto",
    addPhotoBtnQuiet: "Adicione a sua própria foto",
    photoCanGoHere: "Se tirou uma, pode acrescent\u00e1-la aqui.",
    addPhotoSignIn: "Inicie sessão primeiro e depois escolha a sua fotografia.",
    addPhotoSending: "A enviar...",
    addPhotoBadFile: "Não foi possível ler essa imagem. Experimente outra.",
    addPhotoThanks: "Obrigado. Vemos cada fotografia antes de ela ser publicada, e saberá o que aconteceu com a sua.",
    addPhotoFailed: "Isso não foi enviado. Tente novamente daqui a pouco.",
    addPhotoWaiting: "Enviada para nós",
    dayTripAway: "Um passeio de um dia",
    dayTripWhere: (place, km, dir) => `${place}, a ${km} km ${({"north": "a norte", "north-east": "a nordeste", "east": "a leste", "south-east": "a sudeste", "south": "a sul", "south-west": "a sudoeste", "west": "a oeste", "north-west": "a noroeste"} as Record<string, string>)[dir] ?? dir}`,
    addPhotoOnPage: "A sua foto está nesta página",
    yourPhoto: "A sua fotografia",
    yourPhotos: "As suas fotografias",
    photoMore: "Mais",
    photoDeleteTitle: "Eliminar esta foto?",
    photoDeleteBody: "Sai das suas árvores. Se já estiver na página da árvore, fica lá.",
    photoDeleteBtn: "Eliminar foto",
    photoDeleted: "Foto eliminada",
    addPhotoSeeMine: "Ver em As minhas árvores",
    havePhotographed: "Fotografou esta árvore?",
    havePhotographedLine: "Se a sua mostrar melhor a \u00e1rvore, podemos p\u00f4-la no lugar da foto acima, ou ao lado.",
    goNote: "O botão acima abre as indicações na sua aplicação de mapas.",
    approxNote: "O marcador indica a zona, n\u00e3o a \u00e1rvore em si, por isso procure por aqui.",
    knowExactly: "Sabe exatamente onde está?",
    couldUseHelp: "A sua ajuda seria bem-vinda.",
    researchedRemotely: "Se conhece esta \u00e1rvore, pode dizer-nos o que est\u00e1 errado ou o que falta.",
    knowMoreThanUs: "Sabe mais do que nós?",
    ifOlderTree: (c) => `Se conhece uma árvore mais antiga em ${c}, ou vê aqui um erro, diga-nos e nós corrigimos.`,
    home: "In\u00edcio",
    backToTrees: (n) => `\u2190 ${n === 1 ? "A \u00e1rvore" : `As ${n} \u00e1rvores`}`,
    treesOnMap: (n) => `${n} ${n === 1 ? "\u00e1rvore" : "\u00e1rvores"} no mapa`,
    heading: (c) => `\u00c1rvores hist\u00f3ricas de ${c}`,
    readMore: "Ler mais",
    visitedOf: (n, city) => `visitadas em ${city}`,
    seeCollection: "Ver a sua cole\u00e7\u00e3o completa",
    mappingAll: "Estamos a mapear todas as \u00e1rvores not\u00e1veis do mundo.",
    missingOrWrong: (city) => `Conhece alguma em ${city} que nos falte, ou v\u00ea aqui um erro?`,
    tellUs: "Diga-nos",
    faqHeading: "Perguntas frequentes",
    moreOnOldest: "Mais sobre a \u00e1rvore mais antiga",
    nearbyCities: "Árvores antigas em cidades próximas",
    allCities: "Todas as cidades do mapa",
    oldestQuestion: (city) => `Qual \u00e9 a \u00e1rvore mais antiga de ${city}?`,
    fullAnswer: "A resposta completa, com mapa e como chegar.",
    suggestTree: "Conhece uma \u00e1rvore que mere\u00e7a estar nesta lista?",
    sendIt: "Envie-nos",
    walkRoutes: "Percursos a p\u00e9",
    inTheApp: "na aplica\u00e7\u00e3o",
    appPitchTreeTitle: "Colecione as árvores que visita",
    appPitchTreeBody: "Com a aplicação pode marcar esta, encontrar um percurso que passa por mais algumas e ver a sua coleção crescer cidade a cidade.",
    appPitchCityTitle: "Visite-as com a aplicação",
    appPitchCityBody: "Com a aplicação pode seguir um percurso a pé por estas árvores, guardar as que quer ver e marcar cada uma que visita.",
    appPitchCityBodyNoWalks: "Com a aplicação pode guardar as árvores que quer ver e marcar cada uma que visita.",
    getTheApp: "Obter a aplicação",
    whereAmI: "Onde estou",
    cardMore: "Ler mais e como chegar \u2192",
    cardSave: "Guardar",
    cardSaved: "Guardado",
    walkMoreTrees: (c) => `Percorra mais \u00e1rvores em ${c}`,
    whatElseStands: (c) => `Quer saber o que mais continua de p\u00e9 em ${c}? Veja`,
    allTreesLink: (n, c) => `as ${n} \u00e1rvores hist\u00f3ricas de ${c}`,
    orDiscover: "ou descubra",
    whichIsOldest: (c) => `qual \u00e9 a \u00e1rvore mais antiga de ${c}`,
    moreTrees: "Mais \u00e1rvores",
    oldestTreeCrumb: "A \u00e1rvore mais antiga",
    fullStory: "A hist\u00f3ria completa desta \u00e1rvore",
    cityHasMore: (c) => `${c} tem mais \u00e1rvores que valem a visita:`,
    sentenceEnd: ".",
    photoCredit: (credit) => `Foto: ${credit}`,
    ambassadorRole: (place) => `Cuida da lista de ${place}`,
    ageYears: (n) => `${n} anos`,
    seenChip: "Colecionada",
    seasonChip: { bloom: "Em flor", autumn: "Cores de outono", fruit: "Com fruto", leaves: "Folhas novas", catkins: "Amentilhos", winter: "Silhueta de inverno", peak: "Na época" },
    ambassadorWanted: (place) => `Procuramos quem cuide da lista de ${place}`,
    ambassadorWantedLine: "Ajude-nos a melhorar esta lista.",
    ambassadorApply: "Quero participar",
    ambassadorApplied: "Pedido enviado.",
    ambassadorAskTitle: (place) => `Quer cuidar da lista de ${place}?`,
    ambassadorsLabel: "Embaixadores",
    ambassadorAskBody: "Um embaixador ajuda-nos a acertar nas \u00e1rvores deste lugar.",
    ambassadorAskPoints: ["Acrescente fotografias das árvores", "Confirme os dados e diga-nos que árvores faltam", "Ajude a preparar passeios que passem por elas"],
    ambassadorAskSend: "Candidatar-me",
    ambassadorNotNow: "Agora não",
    ambassadorSentTitle: "Pedido enviado",
    ambassadorSentBody: "Em breve enviamos-lhe um email com algumas perguntas sobre a lista.",
    ambassadorWriteTo: (email) => `Escrevemos-lhe para ${email}.`,
    ambassadorDone: "Concluído",
    photoOpen: "Abrir a fotografia",
    photoPrev: "Fotografia anterior",
    photoNext: "Fotografia seguinte",
    photoNumber: (n, total) => `Fotografia ${n} de ${total}`,
    appStoreBadge: "Obter Ancient Trees na App Store",
    openInApp: "Abrir na app",
    androidTitle: "Estamos a trabalhar na app para Android",
    androidNote: "Ainda não existe uma app para Android. Deixe o seu email e escrevemos-lhe no dia em que houver.",
    emailLabel: "Endereço de email",
    notifyMe: "Avisem-me",
    waitlistSent: "J\u00e1 est\u00e1 na lista. Avisamos quando a aplica\u00e7\u00e3o estiver no Android.",
    scanToOpen: "Digitalize isto com o seu telefone para o abrir aí.",
    photoClose: "Fechar",
    photoFull: "Ver em tamanho real",
  },
  fr: {
    homeVerbFind: "Trouve",
    homeVerbWalk: "Marche",
    homeVerbCollect: "Collectionne",
    homeNearestChip: "Le plus proche de toi",
    homeMinWalk: (n) => `${n} min à pied`,
    homeWalkChip: "Balade d'un après-midi",
    homeTreesCount: (n) => `${n} arbres`,
    homeAboutTime: "environ 1h 10",
    homePhoneTitle: "Tes arbres",
    homeStatTrees: "arbres",
    homeStatCities: "villes",
    homeStatOldest: "ans",
    homeCollectedSpecies: "Espèces collectionnées",
    homeDirTopCities: "Villes principales",
    homeDirCollections: "Collections",
    homeDirOldest: "Arbres les plus vieux",
    homeDirTopSpecies: "Espèces principales",
    homeAllCities: (n) => `Les ${n} villes`,
    homeAllCollections: "Toutes les collections",
    homeOldestOfAll: "Les plus vieux de tous",
    homeAllSpecies: (n) => `Les ${n} espèces`,
    homeFavH: "Nos villes d'arbres préférées",
    homeOldestShelfH: "Les arbres les plus vieux que nous cartographions",
    homeCountriesH: "Pays",
    homeAllCountries: "Tous les pays",
    homeSpeciesH: "Espèces",
    homeParksH: "Parcs",
    homeAllParks: "Tous les parcs",
    seeAll: "Tout voir",
    gettingThere: "S'y rendre",
    readLess: "Lire moins",
    noPhotoAsk: "Vous êtes venu ici ? La vôtre serait la première sur cette page.",
    notesHeading: "De ceux qui sont venus ici",
    notesNone: "Personne n'a encore écrit sur cet arbre.",
    notesBorrowed: "Tout près, à {tree}, un visiteur a laissé ceci :",
    notesEmptyTitle: "Pas encore de notes",
    notesEmptyAsk: "Vous avez vu l'arbre ? Laissez une note au prochain visiteur.",
    noteWrite: "Écrire une note",
    noteEditMine: "Modifier votre note",
    photoAddTitle: "Votre photo ici",
    photoAddAsk: "Vous avez vu cet arbre ? Montrez au prochain visiteur à quoi il ressemble.",
    noteAsk: "Laissez une note au prochain visiteur",
    noteSheetTitle: "Une note pour le prochain visiteur",
    notePlaceholder: "Que doit-il savoir ? Où se placer, quand venir, ce que vous avez remarqué.",
    noteExamples: "Par exemple : « Le plus beau depuis le côté nord vers seize heures, quand le soleil passe. » Ou : « Il y avait une église sur cette place jusqu'en 1755. »",
    noteShownAs: (name) => `Affichée comme ${name} avec la date du jour. Publique aussitôt.`,
    noteShownAnon: "Affichée comme « Un visiteur » avec la date du jour. Publique aussitôt.",
    noteAdd: "Ajouter la note",
    noteSave: "Enregistrer la note",
    noteDelete: "Supprimer la note",
    noteSaving: "Enregistrement...",
    noteFailed: "Ça n'est pas passé. Réessayez dans un instant.",
    noteSignIn: "Connectez-vous d'abord, puis écrivez votre note.",
    noteYours: "Votre note",
    noteVisitor: "Un visiteur",
    homeShelfMeta: (n, country) => `${n} arbres \u00b7 ${country}`,
    exploreWalkItem: (n, d) => `${n} arbres sur ${d}`,
    citiesCrumb: "Villes",
    citiesTitle: "Toutes les villes de la carte",
    citiesHeading: "Toutes les villes de la carte",
    citiesLead: (c, t) => `${c} villes, ${t} arbres.`,
    citiesDescription: "Toutes les villes de la carte, par pays : les arbres anciens et remarquables de chacune, vérifiés, avec leur histoire et leur emplacement exact.",
    exploreTitle: "Carte des arbres remarquables du monde",
    exploreDescription: "La carte interactive de tous les arbres remarquables vérifiés du site, chaque point un arbre devant lequel il vaut la peine de s'arrêter.",
    exploreHeading: "La carte des arbres remarquables",
    exploreNote: "Chaque point est un arbre qui vaut le déplacement. Trouvez-en un près de vous, ou là où vous allez.",
    exploreWhatH: "Ce qu'il y a sur cette carte",
    exploreWhatBody: (t, p, c) => `${t} arbres dans ${p} lieux répartis sur ${c} pays. Chaque point ouvre un arbre avec son âge, son espèce, la raison pour laquelle il vaut le détour et l'itinéraire depuis l'endroit où vous êtes.`,
    exploreWalksH: "Les parcours les plus courts",
    exploreWalksBody: "Ici, les arbres sont assez proches pour les voir tous \u00e0 pied en un seul apr\u00e8s-midi :",
    exploreIslandsH: "Îles",
    exploreIslandsBody: "Sur une \u00eele, les arbres sont \u00e0 un trajet en voiture plut\u00f4t qu'\u00e0 une promenade, mais certains ne poussent nulle part ailleurs : dragonniers, for\u00eat de lauriers qui a surv\u00e9cu \u00e0 la glaciation, pins plus hauts que tous ceux du continent.",
    exploreNotH: "Ce qui n'y est pas, et pourquoi",
    exploreNotBody: "Chaque point indique sa pr\u00e9cision. Un arbre marqu\u00e9 approximatif veut dire que nous connaissons le parc mais pas le tronc, et sa page le dit. Nous laissons de c\u00f4t\u00e9 les arbres sur terrain priv\u00e9 et ceux dont l'emplacement est gard\u00e9 secret pour les prot\u00e9ger. Un arbre a un point parce qu'il est remarquable.",
    exploreBrowse: "Parcourir autrement :",
    homeTitle: "Ancient Trees : arbres remarquables près de vous",
    homeDescription: "Trouvez les vieux arbres remarquables autour de vous, chacun avec son histoire, ses sources, son emplacement exact et l'itinéraire depuis où vous êtes.",
    homeHeroLead: "Des arbres qui valent le détour,",
    homeHeroEm: "où que vous soyez.",
    homeSub: "Fait pour ceux qui aiment \u00eatre dehors. Trouvez des arbres remarquables \u00e0 c\u00f4t\u00e9, passez en voir quelques-uns en un apr\u00e8s-midi, lisez l'histoire de chacun et cochez ceux que vous visitez.",
    homeFindH: "Les arbres près de vous, tout de suite.",
    homeFindBody: "Vous voyez les vieux arbres remarquables les plus proches de l'endroit o\u00f9 vous \u00eates, avec le temps de marche et l'itin\u00e9raire jusqu'au plus proche.",
    homeWalkH: "Un parcours qui passe par ceux qui comptent.",
    homeWalkBody: "Les arbres les plus remarquables, reli\u00e9s en une promenade d'un apr\u00e8s-midi, chacun avec son histoire et le mois o\u00f9 il est au mieux.",
    homeCollectH: "Cochez les arbres que vous visitez.",
    homeCollectBody: "Cochez chaque arbre une fois sur place et regardez grandir votre collection d'arbres, de villes et d'esp\u00e8ces. Les arbres plus rares et plus vieux comptent davantage.",
    homeDirectoryH: "Des arbres remarquables partout",
    homeMission: "Nous cartographions tous les arbres remarquables du monde, et votre aide nous serait utile. Si vous connaissez un bel arbre, ou si vous voulez cartographier une ville entière,",
    homeMissionLink: "dites-le-nous",
    mapFilterGroup: "Filtrer la carte",
    mapFilterFav: "À visiter",
    wantAdded: "Ajouté à À visiter",
    wantRemoved: "Retiré de À visiter",
    wantView: "Voir",
    wantUndo: "Annuler",
    mapFilterMine: "Collectionnés",
    mapFilterSpecies: "Espèce",
    mapFilterFree: "Gratuit",
    treeLabels: {
      "Youngest tree": "Le plus jeune",
      "Urban curiosity": "Curiosité urbaine",
      "Continuously renewed": "Renouvelé en continu",
      "Young regrowth": "Jeune rejet",
      "Deliberately planted, not inherited": "Planté exprès, non hérité",
      "Young replacement": "Jeune remplaçant",
      "Ensemble": "Ensemble",
      "Recent planting, ancient provenance": "Plantation récente, origine ancienne",
    },
    metaLead: (sp, age, where, size) => {
      const n = (v: number) => String(v).replace(".", ",");
      const m = size?.girth ? `de ${n(size.girth)} m de circonférence`
        : size?.height ? `de ${n(size.height)} m de haut` : "";
      return sp && age ? `${sp} d'environ ${age} ans à ${where}.`
        : sp && m ? `${sp} ${m} à ${where}.`
        : sp ? `${sp} à ${where}.`
        : age ? `Arbre d'environ ${age} ans à ${where}.`
        : m ? `Arbre ${m} à ${where}.` : `Arbre remarquable à ${where}.`;
    },
    distanceAway: (d) => `\u00e0 ${d}`,
    labelSpecies: "Espèce",
    labelRegister: "Au registre officiel",
    labelGirth: "Circonférence",
    labelAge: "Âge estimé",
    labelLocation: "Emplacement",
    labelAccess: "Accès",
    labelGettingThere: "Y aller",
    factAge: "Âge",
    factPin: "Position",
    factYearsOld: "Ans",
    locApprox: "Emplacement approximatif.",
    ticketNeeded: "Il faut un billet pour voir cet arbre",
    pinExact: "Exacte",
    pinApproximate: "Approximative",
    discoverMore: "Découvrir plus",
    sourcesHeading: "Sources",
    sourcesLine: "D’où viennent les informations de cette page. L’histoire a été écrite avec une IA à partir de ces sources, et les lecteurs qui connaissent l’arbre la corrigent.",
    howWeCheck: "Comment nous choisissons et vérifions les arbres",
    takeMeThere: "M'y emmener",
    showOnMap: "Voir sur la carte",
    showPhoto: "Voir la photo",
    openFullMap: "Ouvrir la carte complète",
    dirTitle: "Ouvrir l'itinéraire dans",
    noPhotoYet: "Pas encore de photo",
    pinShowUs: "Montrez-nous où il se trouve",
    pinTitle: "Où est-il vraiment ?",
    pinHelp: "Déplacez la carte jusqu'à ce que le repère soit sur l'arbre.",
    pinZoom: "Zoomez autant que vous voulez. Vous pourrez envoyer d\u00e8s que vous aurez d\u00e9plac\u00e9 le rep\u00e8re.",
    pinMoved: (m) => `C'est à ${m} m de notre position.`,
    pinSend: "L'arbre est ici",
    pinSending: "Envoi en cours",
    pinDone: "Nous allons vérifier et déplacer le repère.",
    pinFailed: "L'envoi n'a pas abouti. Réessayez dans un instant.",
    pinNeedsAccount: "Il vous faut un compte pour l'envoyer, pour que nous puissions vous dire ce que votre correction a chang\u00e9.",
    cancel: "Annuler",
    appleMaps: "Apple Maps",
    goBack: "Retour",
    chipOldest: "Arbre le plus vieux",
    googleMaps: "Google Maps",
    seenIt: "Collectionner cet arbre",
    worthItAsk: (n) => `Oui, ${n} valait le détour`,
    worthItDone: (n) => `Vous avez trouvé ${n} digne du détour. Touchez pour annuler`,
    seenItDone: "Collectionné",
    collectTitle: (n) => `Collectionner ${n}`,
    collectLead: "Prends une photo pour l'ajouter à tes arbres.",
    collectPhoto: "Choisir une photo",
    collectCamera: "Prendre une photo",
    collectLibrary: "Choisir dans tes photos",
    collectNoPhoto: "Collectionner sans photo",
    collectedTitle: (n) => `Tu as collectionné ${n}`,
    collectedOn: (d) => `Le ${d}.`,
    uncollect: "Retirer des collectionnés",
    uncollected: "Retiré des collectionnés",
    uncollectQ: (n) => `Retirer ${n} de tes arbres collectionnés ?`,
    uncollectBody: "Tes photos restent enregistrées. Il quitte Mes arbres jusqu’à ce que tu le collectionnes à nouveau.",
    uncollectYes: "Retirer",
    keepIt: "Le garder",
    nearbyTrees: "Arbres à proximité",
    somethingWrong: "Il y a une erreur ici",
    suggestAnother: "Proposer un autre arbre",
    share: "Partager",
    shareCopied: "Lien copié",
    correctDetail: "Corriger un détail de cette page",
    worthVote: (n) => `Oui, ${n} valait le déplacement`,
    worthReport: "Quelque chose ne va pas",
    worthWhatsWrong: "Qu'est-ce qui ne va pas ?",
    worthDead: "Il est mort ou disparu",
    worthDeadQ: "Qu'avez-vous trouvé sur place ? (facultatif)",
    worthDeadPh: "Une souche, un tronc tombé, rien du tout, et quand vous y étiez",
    worthWrongLoc: "Mauvais emplacement",
    worthWrongLocQ: "Où se trouve-t-il vraiment ? (facultatif)",
    worthWrongLocPh: "Un coin de rue, un repère, ou collez un point de carte",
    worthWhichTree: "Je ne savais pas lequel",
    worthWhichTreeQ: "Lequel avez-vous regardé ? (facultatif)",
    worthWhichTreePh: "Le tronc le plus épais, celui près du chemin, celui près du banc",
    worthCouldNotReach: "Je n'ai pas pu y accéder",
    worthCouldNotReachQ: "Qu'est-ce qui vous a arrêté ? (facultatif)",
    worthCouldNotReachPh: "Un portail fermé, une clôture, les horaires, un terrain privé",
    worthTwice: "Il est deux fois sur la carte",
    worthTwiceQ: "Quel autre arbre est-ce ? (facultatif)",
    worthTwicePh: "Son nom, ou l'emplacement de l'autre repère",
    worthSomethingElse: "Autre chose",
    worthSomethingElseQ: "Dites-le-nous en une ligne.",
    worthSomethingElsePh: "Ce que nous avons faux, ou ce qui nous manque",
    worthThanks: "Merci, nous allons vérifier.",
    worthThanksDetail: "Merci, cela nous aide.",
    worthDetailLabel: "Quelque chose qui nous aide à vérifier ? (facultatif)",
    worthSend: "Envoyer",
    actions: "Actions",
    unknownAge: "âge inconnu",
    approxLocationChip: "position approximative",
    noPhotoLicence: "Nous n'avons pas encore de photographie de cet arbre.",
    addPhotoBtn: "Ajouter une photo",
    addPhotoBtnQuiet: "Ajoutez votre propre photo",
    photoCanGoHere: "Si vous en avez pris une, vous pouvez l'ajouter ici.",
    addPhotoSignIn: "Connectez-vous d'abord, puis choisissez votre photo.",
    addPhotoSending: "Envoi en cours...",
    addPhotoBadFile: "Cette image n'a pas pu être lue. Essayez-en une autre.",
    addPhotoThanks: "Merci. Nous regardons chaque photo avant qu'elle ne soit publiée, et vous saurez ce qu'il est advenu de la vôtre.",
    addPhotoFailed: "Cela n'a pas fonctionné. Réessayez dans un instant.",
    addPhotoWaiting: "Envoyée à nous",
    dayTripAway: "Une excursion d’une journée",
    dayTripWhere: (place, km, dir) => `${place}, à ${km} km ${({"north": "au nord", "north-east": "au nord-est", "east": "à l’est", "south-east": "au sud-est", "south": "au sud", "south-west": "au sud-ouest", "west": "à l’ouest", "north-west": "au nord-ouest"} as Record<string, string>)[dir] ?? dir}`,
    addPhotoOnPage: "Votre photo est sur cette page",
    yourPhoto: "Votre photo",
    yourPhotos: "Vos photos",
    photoMore: "Plus",
    photoDeleteTitle: "Supprimer cette photo ?",
    photoDeleteBody: "Elle quitte tes arbres. Si elle est déjà sur la page de l'arbre, elle y reste.",
    photoDeleteBtn: "Supprimer la photo",
    photoDeleted: "Photo supprimée",
    addPhotoSeeMine: "La voir dans Mes arbres",
    havePhotographed: "Avez-vous photographié cet arbre ?",
    havePhotographedLine: "Si la v\u00f4tre montre mieux l'arbre, nous pouvons la mettre \u00e0 la place de la photo ci-dessus, ou \u00e0 c\u00f4t\u00e9.",
    goNote: "Le bouton ci-dessus ouvre l'itinéraire dans votre application de cartes.",
    approxNote: "Le rep\u00e8re indique la zone, pas l'arbre lui-m\u00eame : cherchez autour de cet endroit.",
    knowExactly: "Vous savez exactement où il se trouve ?",
    couldUseHelp: "Votre aide nous serait utile.",
    researchedRemotely: "Si vous connaissez cet arbre, vous pouvez nous dire ce qui est faux ou ce qui manque.",
    knowMoreThanUs: "Vous en savez plus que nous ?",
    ifOlderTree: (c) => `Si vous connaissez un arbre plus vieux à ${c}, ou si vous voyez une erreur ici, dites-le-nous et nous la corrigerons.`,
    home: "Accueil",
    backToTrees: (n) => `\u2190 ${n === 1 ? "L\u2019arbre" : `Les ${n} arbres`}`,
    treesOnMap: (n) => `${n} ${n === 1 ? "arbre" : "arbres"} sur la carte`,
    heading: (c) => `Arbres remarquables de ${c}`,
    readMore: "Lire la suite",
    visitedOf: (n, city) => `visit\u00e9s \u00e0 ${city}`,
    seeCollection: "Voir toute votre collection",
    mappingAll: "Nous cartographions tous les arbres remarquables du monde.",
    missingOrWrong: (city) => `Vous en connaissez un \u00e0 ${city} qui manque ici, ou vous voyez une erreur ?`,
    tellUs: "Dites-le-nous",
    faqHeading: "Questions fr\u00e9quentes",
    moreOnOldest: "En savoir plus sur l'arbre le plus vieux",
    nearbyCities: "Arbres anciens dans les villes voisines",
    allCities: "Toutes les villes de la carte",
    oldestQuestion: (city) => `Quel est l'arbre le plus vieux de ${city} ?`,
    fullAnswer: "La r\u00e9ponse compl\u00e8te, avec une carte et l'acc\u00e8s.",
    suggestTree: "Vous connaissez un arbre qui a sa place dans cette liste ?",
    sendIt: "Envoyez-le-nous",
    walkRoutes: "Itin\u00e9raires \u00e0 pied",
    inTheApp: "dans l'application",
    appPitchTreeTitle: "Collectionnez les arbres que vous visitez",
    appPitchTreeBody: "Avec l'application, vous pouvez cocher celui-ci, trouver une balade qui passe par quelques autres et voir votre collection grandir ville après ville.",
    appPitchCityTitle: "Visitez-les avec l'application",
    appPitchCityBody: "Avec l'application, vous pouvez suivre une balade qui passe par ces arbres, enregistrer ceux que vous voulez voir et cocher chacun de ceux que vous visitez.",
    appPitchCityBodyNoWalks: "Avec l'application, vous pouvez enregistrer les arbres que vous voulez voir et cocher chacun de ceux que vous visitez.",
    getTheApp: "Obtenir l'application",
    whereAmI: "O\u00f9 suis-je",
    cardMore: "Lire la suite et l’acc\u00e8s \u2192",
    cardSave: "Enregistrer",
    cardSaved: "Enregistr\u00e9",
    walkMoreTrees: (c) => `Parcourez d'autres arbres \u00e0 ${c}`,
    whatElseStands: (c) => `Envie de savoir ce qui tient encore debout \u00e0 ${c} ? Voyez`,
    allTreesLink: (n, c) => `les ${n} arbres remarquables de ${c}`,
    orDiscover: "ou d\u00e9couvrez",
    whichIsOldest: (c) => `quel est l'arbre le plus vieux de ${c}`,
    moreTrees: "Plus d'arbres",
    oldestTreeCrumb: "L'arbre le plus vieux",
    fullStory: "L'histoire compl\u00e8te de cet arbre",
    cityHasMore: (c) => `${c} compte d'autres arbres qui valent le d\u00e9tour :`,
    sentenceEnd: ".",
    photoCredit: (credit) => `Photo\u00a0: ${credit}`,
    ambassadorRole: (place) => `Veille sur la liste de ${place}`,
    ageYears: (n) => `${n} ans`,
    seenChip: "Collectionné",
    seasonChip: { bloom: "En fleurs", autumn: "Couleurs d'automne", fruit: "En fruits", leaves: "Jeunes feuilles", catkins: "Chatons", winter: "Silhouette d'hiver", peak: "De saison" },
    ambassadorWanted: (place) => `Qui veillera sur la liste de ${place}\u00a0?`,
    ambassadorWantedLine: "Aidez-nous à améliorer cette liste.",
    ambassadorApply: "Ça m'intéresse",
    ambassadorApplied: "Demande envoyée.",
    ambassadorAskTitle: (place) => `Veiller sur la liste de ${place}\u00a0?`,
    ambassadorsLabel: "Ambassadeurs",
    ambassadorAskBody: "Un ambassadeur nous aide \u00e0 bien pr\u00e9senter les arbres de ce lieu.",
    ambassadorAskPoints: ["Ajoutez des photos des arbres", "Vérifiez les faits et dites-nous quels arbres manquent", "Aidez à composer des promenades qui passent par eux"],
    ambassadorAskSend: "Postuler",
    ambassadorNotNow: "Pas maintenant",
    ambassadorSentTitle: "Demande envoyée",
    ambassadorSentBody: "Nous vous écrirons bientôt avec quelques questions sur la liste.",
    ambassadorWriteTo: (email) => `Nous vous écrirons à ${email}.`,
    ambassadorDone: "Terminé",
    photoOpen: "Ouvrir la photographie",
    photoPrev: "Photographie précédente",
    photoNext: "Photographie suivante",
    photoNumber: (n, total) => `Photographie ${n} sur ${total}`,
    appStoreBadge: "Télécharger Ancient Trees sur l'App Store",
    openInApp: "Ouvrir dans l'app",
    androidTitle: "Nous travaillons sur l'application Android",
    androidNote: "Il n'y a pas encore d'application Android. Laissez votre email et nous vous écrirons le jour où elle existera.",
    emailLabel: "Adresse email",
    notifyMe: "Prévenez-moi",
    waitlistSent: "Vous \u00eates sur la liste. Nous vous pr\u00e9viendrons quand l'application sera sur Android.",
    scanToOpen: "Scannez ceci avec votre téléphone pour l'ouvrir là-bas.",
    photoClose: "Fermer",
    photoFull: "La voir en taille réelle",
  },
  ja: {
    homeVerbFind: "見つける",
    homeVerbWalk: "歩く",
    homeVerbCollect: "集める",
    homeNearestChip: "いちばん近い木",
    homeMinWalk: (n) => `徒歩${n}分`,
    homeWalkChip: "午後の散歩",
    homeTreesCount: (n) => `${n}本`,
    homeAboutTime: "約1時間10分",
    homePhoneTitle: "あなたの木",
    homeStatTrees: "本",
    homeStatCities: "都市",
    homeStatOldest: "年",
    homeCollectedSpecies: "集めた樹種",
    homeDirTopCities: "主な都市",
    homeDirCollections: "コレクション",
    homeDirOldest: "最も古い木",
    homeDirTopSpecies: "主な樹種",
    homeAllCities: (n) => `${n}都市すべて`,
    homeAllCollections: "コレクション一覧",
    homeOldestOfAll: "すべての中で最も古い木",
    homeAllSpecies: (n) => `${n}種すべて`,
    homeFavH: "お気に入りの木の街",
    homeOldestShelfH: "私たちが地図に載せた最も古い木",
    homeCountriesH: "国",
    homeAllCountries: "国一覧",
    homeSpeciesH: "樹種",
    homeParksH: "公園",
    homeAllParks: "公園一覧",
    seeAll: "すべて見る",
    gettingThere: "行き方",
    readLess: "閉じる",
    noPhotoAsk: "ここに来たことがありますか？あなたの写真がこのページの最初の一枚になります。",
    notesHeading: "ここに立った人から",
    notesNone: "この木について書いた人はまだいません。",
    notesBorrowed: "近くの{tree}に、訪れた人がこんなメモを残しています：",
    notesEmptyTitle: "まだメモはありません",
    notesEmptyAsk: "この木を訪れましたか？次に訪れる人にメモを残しましょう。",
    noteWrite: "メモを書く",
    noteEditMine: "メモを編集",
    photoAddTitle: "あなたの写真をここに",
    photoAddAsk: "この木を見ましたか？次に訪れる人にその姿を見せてください。",
    noteAsk: "次に訪れる人にメモを残す",
    noteSheetTitle: "次に訪れる人へのメモ",
    notePlaceholder: "何を伝えますか？どこから見るか、いつ来るか、気づいたこと。",
    noteExamples: "例：「北側から午後4時ごろ、日が差すときがいちばんきれいです」「この広場には1755年まで教会がありました」",
    noteShownAs: (name) => `${name}として今日の日付で表示されます。すぐに公開されます。`,
    noteShownAnon: "「訪れた人」として今日の日付で表示されます。すぐに公開されます。",
    noteAdd: "メモを追加",
    noteSave: "メモを保存",
    noteDelete: "メモを削除",
    noteSaving: "保存中...",
    noteFailed: "送信できませんでした。しばらくしてからもう一度お試しください。",
    noteSignIn: "先にサインインしてからメモを書いてください。",
    noteYours: "あなたのメモ",
    noteVisitor: "訪れた人",
    homeShelfMeta: (n, country) => `${n}本 \u00b7 ${country}`,
    exploreWalkItem: (n, d) => `${n}本、${d}以内`,
    citiesCrumb: "都市一覧",
    citiesTitle: "地図に載せたすべての都市",
    citiesHeading: "地図に載せたすべての都市",
    citiesLead: (c, t) => `${c}都市、${t}本。`,
    citiesDescription: "地図に載せたすべての都市を国別に。各都市の古木と名木を、裏づけを取ったうえで、その由来と正確な場所とともに紹介します。",
    exploreTitle: "古木の地図：見に行く価値のある木を一枚の地図に",
    exploreDescription: "裏づけを取った古木と名木をすべて載せた地図です。ピンの一つひとつが、足を運んで見上げる価値のある木です。",
    exploreHeading: "古木の地図",
    exploreNote: "どのピンも、歩いて見に行く価値のある木です。近くの一本も、これから行く街の一本も探せます。",
    exploreWhatH: "この地図に載っているもの",
    exploreWhatBody: (t, p, c) => `${c}か国${p}か所の${t}本。ピンを開くと、その木の樹齢、樹種、歩いて見に行く価値のある理由、そして現在地からの行き方が出ます。`,
    exploreWalksH: "まとめて歩ける場所",
    exploreWalksBody: "\u6b21\u306e\u5834\u6240\u3067\u306f\u3001\u6728\u304c\u8fd1\u304f\u306b\u96c6\u307e\u3063\u3066\u3044\u3066\u3001\u5348\u5f8c\u306e\u3046\u3061\u306b\u5168\u90e8\u3092\u6b69\u3044\u3066\u56de\u308c\u307e\u3059\uff1a",
    exploreIslandsH: "島",
    exploreIslandsBody: "\u5cf6\u3067\u306f\u6728\u3068\u6728\u306e\u3042\u3044\u3060\u304c\u6b69\u304d\u3067\u306f\u306a\u304f\u8eca\u306e\u8ddd\u96e2\u306b\u306a\u308a\u307e\u3059\u304c\u3001\u307b\u304b\u3067\u306f\u80b2\u305f\u306a\u3044\u6728\u3082\u3042\u308a\u307e\u3059\u3002\u7adc\u8840\u6a39\u3001\u6c37\u6cb3\u671f\u3092\u751f\u304d\u5ef6\u3073\u305f\u7167\u8449\u6a39\u306e\u68ee\u3001\u672c\u571f\u306e\u3069\u306e\u677e\u3088\u308a\u3082\u9ad8\u3044\u677e\u3002",
    exploreNotH: "載せていないもの、その理由",
    exploreNotBody: "\u30d4\u30f3\u306b\u306f\u3069\u306e\u304f\u3089\u3044\u6b63\u78ba\u304b\u3092\u66f8\u3044\u3066\u3044\u307e\u3059\u3002\u300c\u304a\u304a\u3088\u305d\u300d\u306e\u6728\u306f\u3001\u516c\u5712\u307e\u3067\u306f\u5206\u304b\u3063\u3066\u3044\u3066\u5e79\u307e\u3067\u306f\u7279\u5b9a\u3067\u304d\u3066\u3044\u306a\u3044\u3068\u3044\u3046\u610f\u5473\u3067\u3001\u305d\u306e\u30da\u30fc\u30b8\u306b\u3082\u305d\u3046\u66f8\u3044\u3066\u3044\u307e\u3059\u3002\u79c1\u6709\u5730\u306e\u6728\u3068\u3001\u5b88\u308b\u305f\u3081\u306b\u5834\u6240\u304c\u4f0f\u305b\u3089\u308c\u3066\u3044\u308b\u6728\u306f\u8f09\u305b\u307e\u305b\u3093\u3002\u30d4\u30f3\u304c\u3064\u304f\u306e\u306f\u3001\u305d\u306e\u6728\u304c\u7279\u5225\u3060\u304b\u3089\u3067\u3059\u3002",
    exploreBrowse: "別の探し方：",
    homeTitle: "Ancient Trees：近くの古木と名木を地図で",
    homeDescription: "身のまわりにある古木と名木を探せます。どれも由来と出典、正確な場所、いまいる場所からの行き方をつけています。",
    homeHeroLead: "どこにいても、",
    homeHeroEm: "歩いて会いに行く価値のある木を。",
    homeSub: "外を歩くのが好きな人のためにつくりました。近くの古木や名木を見つけ、午後のうちに何本かを回り、それぞれの由来を読み、訪れた木をチェックしていけます。",
    homeFindH: "いまいる場所のすぐ近くの木。",
    homeFindBody: "\u3044\u307e\u7acb\u3063\u3066\u3044\u308b\u5834\u6240\u306b\u3044\u3061\u3070\u3093\u8fd1\u3044\u53e4\u6728\u3084\u540d\u6728\u304c\u3001\u5f92\u6b69\u306e\u6240\u8981\u6642\u9593\u3068\u6700\u5bc4\u308a\u306e\u4e00\u672c\u307e\u3067\u306e\u9053\u9806\u3068\u4e00\u7dd2\u306b\u8868\u793a\u3055\u308c\u307e\u3059\u3002",
    homeWalkH: "見る価値のある木をつないだ道。",
    homeWalkBody: "\u9078\u3073\u629c\u3044\u305f\u6728\u3092\u3001\u5348\u5f8c\u306e\u3046\u3061\u306b\u6b69\u3051\u308b\u4e00\u672c\u306e\u6563\u6b69\u9053\u306b\u3064\u306a\u3044\u3067\u3044\u307e\u3059\u3002\u305d\u308c\u305e\u308c\u306b\u7531\u6765\u3068\u3001\u3044\u3061\u3070\u3093\u898b\u3054\u308d\u306b\u306a\u308b\u6708\u3092\u3064\u3051\u3066\u3044\u307e\u3059\u3002",
    homeCollectH: "訪れた木をチェックする。",
    homeCollectBody: "\u6728\u306e\u524d\u306b\u7acb\u3063\u305f\u3089\u30c1\u30a7\u30c3\u30af\u3092\u5165\u308c\u3066\u3001\u6728\u3001\u8857\u3001\u6a39\u7a2e\u306e\u30b3\u30ec\u30af\u30b7\u30e7\u30f3\u304c\u5897\u3048\u3066\u3044\u304f\u306e\u3092\u773a\u3081\u3066\u304f\u3060\u3055\u3044\u3002\u73cd\u3057\u3044\u6728\u3084\u53e4\u3044\u6728\u307b\u3069\u91cd\u304f\u6570\u3048\u307e\u3059\u3002",
    homeDirectoryH: "世界中の古木",
    homeMission: "世界中の名木を地図にしていきます。力を貸してもらえると助かります。いい木を知っている方、街ごと地図にしたい方は、",
    homeMissionLink: "お知らせください",
    mapFilterGroup: "地図をしぼり込む",
    mapFilterFav: "行きたい",
    wantAdded: "行きたいに追加しました",
    wantRemoved: "行きたいから削除しました",
    wantView: "見る",
    wantUndo: "元に戻す",
    mapFilterMine: "集めた木",
    mapFilterSpecies: "樹種",
    mapFilterFree: "無料",
    treeLabels: {
      "Youngest tree": "最も若い木",
      "Urban curiosity": "街の変わり種",
      "Continuously renewed": "更新され続けている",
      "Young regrowth": "若い萌芽",
      "Deliberately planted, not inherited": "受け継いだのではなく植えられた",
      "Young replacement": "若い後継",
      "Ensemble": "群",
      "Recent planting, ancient provenance": "植えたのは最近、血筋は古い",
    },
    metaLead: (sp, age, where, size) => {
      const m = size?.girth ? `幹周約${size.girth}mの`
        : size?.height ? `高さ約${size.height}mの` : "";
      return sp && age ? `${where}にある樹齢約${age}年の${sp}。`
        : sp && m ? `${where}にある${m}${sp}。`
        : sp ? `${where}にある${sp}。`
        : age ? `${where}にある樹齢約${age}年の木。`
        : m ? `${where}にある${m}木。` : `${where}にある巨木。`;
    },
    distanceAway: (d) => `${d}\u5148`,
    labelSpecies: "樹種",
    labelRegister: "公式登録",
    labelGirth: "幹回り",
    labelAge: "推定樹齢",
    labelLocation: "場所",
    labelAccess: "見学",
    labelGettingThere: "行き方",
    factAge: "樹齢",
    factPin: "位置",
    factYearsOld: "樹齢",
    locApprox: "おおよその位置です。",
    ticketNeeded: "この木を見るにはチケットが必要です",
    pinExact: "正確",
    pinApproximate: "おおよそ",
    discoverMore: "もっと見る",
    sourcesHeading: "出典",
    sourcesLine: "このページの情報の出どころ。物語はこれらの出典をもとにAIが書き、木を知る読者が直しています。",
    howWeCheck: "木の選び方と確認の方法",
    takeMeThere: "ここへ行く",
    showOnMap: "地図で見る",
    showPhoto: "写真を見る",
    openFullMap: "地図を大きく開く",
    dirTitle: "経路を開くアプリ",
    noPhotoYet: "まだ写真がありません",
    pinShowUs: "正しい場所を教えてください",
    pinTitle: "本当はどこにありますか？",
    pinHelp: "ピンが木の上に来るまで地図を動かしてください。",
    pinZoom: "好きなだけ拡大できます。ピンを動かすとボタンが押せるようになります。",
    pinMoved: (m) => `登録している位置から${m}mです。`,
    pinSend: "木はここにあります",
    pinSending: "送信中",
    pinDone: "確認してピンを移動します。",
    pinFailed: "送信できませんでした。少し経ってからもう一度お試しください。",
    pinNeedsAccount: "\u9001\u4fe1\u306b\u306f\u30a2\u30ab\u30a6\u30f3\u30c8\u304c\u5fc5\u8981\u3067\u3059\u3002\u4fee\u6b63\u3067\u4f55\u304c\u5909\u308f\u3063\u305f\u304b\u3092\u304a\u77e5\u3089\u305b\u3059\u308b\u305f\u3081\u3067\u3059\u3002",
    cancel: "キャンセル",
    appleMaps: "Apple マップ",
    goBack: "戻る",
    chipOldest: "最古の木",
    googleMaps: "Google マップ",
    seenIt: "この木を集める",
    worthItAsk: (n) => `はい、${n}は行く価値がありました`,
    worthItDone: (n) => `${n}を「行く価値あり」としました。タップで取り消し`,
    seenItDone: "集めた",
    collectTitle: (n) => `${n}を集める`,
    collectLead: "写真を撮って、あなたの木に加えましょう。",
    collectPhoto: "写真を選ぶ",
    collectCamera: "写真を撮る",
    collectLibrary: "写真から選ぶ",
    collectNoPhoto: "写真なしで集める",
    collectedTitle: (n) => `${n}を集めました`,
    collectedOn: (d) => `${d}`,
    uncollect: "集めた木から外す",
    uncollected: "集めた木から外しました",
    uncollectQ: (n) => `${n}を集めた木から外しますか？`,
    uncollectBody: "この木の写真は保存されたままです。もう一度集めるまで、あなたの木には表示されません。",
    uncollectYes: "外す",
    keepIt: "そのままにする",
    nearbyTrees: "近くの木",
    somethingWrong: "ここに誤りがある",
    suggestAnother: "別の木を教える",
    share: "共有",
    shareCopied: "リンクをコピーしました",
    correctDetail: "このページの情報を直す",
    worthVote: (n) => `${n}は行く価値がありました`,
    worthReport: "何かがおかしい",
    worthWhatsWrong: "何がおかしいですか",
    worthDead: "枯れている、もうない",
    worthDeadQ: "そこで何を見つけましたか（任意）",
    worthDeadPh: "切り株、倒れた幹、何もなかった、行った時期",
    worthWrongLoc: "場所が違う",
    worthWrongLocQ: "本当はどこにありますか（任意）",
    worthWrongLocPh: "交差点、目印、または地図のピン",
    worthWhichTree: "どの木か分からなかった",
    worthWhichTreeQ: "どの木を見ましたか（任意）",
    worthWhichTreePh: "太いほうの幹、道に近いほう、ベンチのそば",
    worthCouldNotReach: "たどり着けなかった",
    worthCouldNotReachQ: "何に阻まれましたか（任意）",
    worthCouldNotReachPh: "施錠された門、柵、開いている時間、私有地",
    worthTwice: "地図に2回載っている",
    worthTwiceQ: "どの木と同じですか（任意）",
    worthTwicePh: "その木の名前、またはもう一つのピンの場所",
    worthSomethingElse: "その他",
    worthSomethingElseQ: "一行で教えてください",
    worthSomethingElsePh: "こちらの誤り、または足りないこと",
    worthThanks: "ありがとうございます。確認します。",
    worthThanksDetail: "ありがとうございます。助かります。",
    worthDetailLabel: "確認の手がかりになることはありますか（任意）",
    worthSend: "送信",
    actions: "操作",
    unknownAge: "樹齢不明",
    approxLocationChip: "位置は目安",
    noPhotoLicence: "\u3053\u306e\u6728\u306e\u5199\u771f\u306f\u307e\u3060\u3042\u308a\u307e\u305b\u3093\u3002",
    addPhotoBtn: "写真を追加",
    addPhotoBtnQuiet: "自分の写真を追加",
    photoCanGoHere: "ご自身で撮った写真があれば、ここに載せられます。",
    addPhotoSignIn: "先にサインインしてから、写真を選んでください。",
    addPhotoSending: "送信中...",
    addPhotoBadFile: "その画像を読み込めませんでした。別の画像でお試しください。",
    addPhotoThanks: "ありがとうございます。掲載前にすべての写真を確認し、その後どうなったかをお知らせします。",
    addPhotoFailed: "送信できませんでした。少し経ってからもう一度お試しください。",
    addPhotoWaiting: "送信済み",
    dayTripAway: "日帰りで行ける木",
    dayTripWhere: (place, km, dir) => `${place}（中心から${({"north": "北", "north-east": "北東", "east": "東", "south-east": "南東", "south": "南", "south-west": "南西", "west": "西", "north-west": "北西"} as Record<string, string>)[dir] ?? dir}へ${km}km）`,
    addPhotoOnPage: "あなたの写真はこのページに掲載されています",
    yourPhoto: "あなたの写真",
    yourPhotos: "あなたの写真",
    photoMore: "その他",
    photoDeleteTitle: "この写真を削除しますか？",
    photoDeleteBody: "あなたの木から削除されます。すでに木のページに掲載されている場合は、そのまま残ります。",
    photoDeleteBtn: "写真を削除",
    photoDeleted: "写真を削除しました",
    addPhotoSeeMine: "アカウントで見る",
    havePhotographed: "この木を撮影しましたか?",
    havePhotographedLine: "上の写真より良く撮れていれば、それに差し替えるか、並べて掲載します。",
    goNote: "上のボタンで、地図アプリの経路案内が開く。",
    approxNote: "\u3053\u306e\u76ee\u5370\u304c\u793a\u3059\u306e\u306f\u6728\u305d\u306e\u3082\u306e\u3067\u306f\u306a\u304f\u3001\u304a\u304a\u3088\u305d\u306e\u5834\u6240\u3067\u3059\u3002\u3053\u306e\u3042\u305f\u308a\u3092\u63a2\u3057\u3066\u307f\u3066\u304f\u3060\u3055\u3044\u3002",
    knowExactly: "正確な場所を知っているか。",
    couldUseHelp: "力を貸してほしい。",
    researchedRemotely: "\u3053\u306e\u6728\u3092\u77e5\u3063\u3066\u3044\u308b\u306a\u3089\u3001\u9593\u9055\u3063\u3066\u3044\u308b\u70b9\u3084\u8db3\u308a\u306a\u3044\u70b9\u3092\u6559\u3048\u3066\u304f\u3060\u3055\u3044\u3002",
    knowMoreThanUs: "私たちより詳しいか。",
    ifOlderTree: (c) => `${c}にもっと古い木があるなら、あるいはここに誤りがあるなら、教えてください。直します。`,
    home: "\u30db\u30fc\u30e0",
    backToTrees: (n) => `\u2190 ${n}\u672c\u306e\u6a39\u6728`,
    treesOnMap: (n) => `\u5730\u56f3\u4e0a\u306e${n}\u672c`,
    heading: (c) => `${c}\u306e\u53e4\u6a39`,
    readMore: "\u7d9a\u304d\u3092\u8aad\u3080",
    visitedOf: (n, city) => `${city}\u3067\u8a2a\u308c\u305f\u6570`,
    seeCollection: "\u30b3\u30ec\u30af\u30b7\u30e7\u30f3\u3092\u3059\u3079\u3066\u898b\u308b",
    mappingAll: "\u4e16\u754c\u4e2d\u306e\u9280\u91cd\u306a\u6a39\u6728\u3092\u5730\u56f3\u306b\u3057\u3066\u3044\u307e\u3059\u3002",
    missingOrWrong: (city) => `${city}\u3067\u629c\u3051\u3066\u3044\u308b\u6a39\u6728\u3092\u3054\u5b58\u3058\u3067\u3059\u304b\u3001\u307e\u305f\u306f\u8aa4\u308a\u3092\u898b\u3064\u3051\u307e\u3057\u305f\u304b\u3002`,
    tellUs: "\u304a\u77e5\u3089\u305b\u304f\u3060\u3055\u3044",
    faqHeading: "\u3088\u304f\u3042\u308b\u8cea\u554f",
    moreOnOldest: "\u6700\u3082\u53e4\u3044\u6a39\u6728\u306b\u3064\u3044\u3066",
    nearbyCities: "近くの都市の古木",
    allCities: "地図上のすべての都市",
    oldestQuestion: (city) => `${city}\u3067\u6700\u3082\u53e4\u3044\u6a39\u6728\u306f\u3069\u308c\u3067\u3059\u304b\u3002`,
    fullAnswer: "\u5730\u56f3\u3068\u884c\u304d\u65b9\u3092\u542b\u3080\u5b8c\u5168\u306a\u56de\u7b54\u3067\u3059\u3002",
    suggestTree: "\u3053\u306e\u30ea\u30b9\u30c8\u306b\u5165\u308b\u3079\u304d\u6a39\u6728\u3092\u3054\u5b58\u3058\u3067\u3059\u304b\u3002",
    sendIt: "\u304a\u9001\u308a\u304f\u3060\u3055\u3044",
    walkRoutes: "\u5f92\u6b69\u30eb\u30fc\u30c8",
    inTheApp: "\u30a2\u30d7\u30ea\u3067",
    appPitchTreeTitle: "訪れた木を集める",
    appPitchTreeBody: "アプリでは、この木にチェックを入れ、ほかの木も巡る散歩を見つけ、街ごとに増えていくコレクションを眺められます。",
    appPitchCityTitle: "アプリを持って歩く",
    appPitchCityBody: "アプリでは、これらの木を巡る散歩コースをたどり、見たい木を保存し、訪れた木にチェックを入れられます。",
    appPitchCityBodyNoWalks: "アプリでは、見たい木を保存し、訪れた木にチェックを入れられます。",
    getTheApp: "アプリを入手",
    whereAmI: "\u73fe\u5728\u5730",
    cardMore: "\u8a73\u3057\u304f\u898b\u308b\u30fb\u884c\u304d\u65b9 \u2192",
    cardSave: "\u4fdd\u5b58",
    cardSaved: "\u4fdd\u5b58\u6e08\u307f",
    walkMoreTrees: (c) => `${c}\u306e\u4ed6\u306e\u6a39\u6728\u3092\u5DE1\u308b`,
    whatElseStands: (c) => `${c}\u306b\u4ed6\u306b\u4f55\u304c\u6b8b\u3063\u3066\u3044\u308b\u304b\u3054\u89a7\u304f\u3060\u3055\u3044\u3002`,
    allTreesLink: (n, c) => `${c}\u306e\u53e4\u6a39${n}\u672c`,
    orDiscover: "\u307e\u305f\u306f",
    whichIsOldest: (c) => `${c}\u3067\u6700\u3082\u53e4\u3044\u6a39\u6728`,
    moreTrees: "\u4ed6\u306e\u6a39\u6728",
    oldestTreeCrumb: "\u6700\u3082\u53e4\u3044\u6a39\u6728",
    fullStory: "\u3053\u306e\u6a39\u6728\u306e\u8a73\u3057\u3044\u8a71",
    cityHasMore: (c) => `${c}\u306b\u306f\u8a2a\u308c\u308b\u4fa1\u5024\u306e\u3042\u308b\u6a39\u6728\u304c\u307e\u3060\u3042\u308a\u307e\u3059\u3002`,
    sentenceEnd: "\u3002",
    photoCredit: (credit) => `\u5199\u771f\uff1a${credit}`,
    ambassadorRole: (place) => `${place}のアンバサダー`,
    ageYears: (n) => `${n}年`,
    seenChip: "集めた",
    seasonChip: { bloom: "開花中", autumn: "紅葉", fruit: "実り", leaves: "新緑", catkins: "尾状花序", winter: "冬の樹形", peak: "見頃" },
    ambassadorWanted: (place) => `${place}のアンバサダーを募集中`,
    ambassadorWantedLine: "このリストをより良くするために力を貸してください。",
    ambassadorApply: "応募する",
    ambassadorApplied: "申請を送信しました。",
    ambassadorAskTitle: (place) => `${place}のアンバサダーになりますか？`,
    ambassadorsLabel: "アンバサダー",
    ambassadorAskBody: "\u30a2\u30f3\u30d0\u30b5\u30c0\u30fc\u306f\u3001\u3053\u306e\u5834\u6240\u306e\u6728\u3092\u6b63\u3057\u304f\u4f1d\u3048\u308b\u624b\u52a9\u3051\u3092\u3057\u3066\u304f\u308c\u307e\u3059\u3002",
    ambassadorAskPoints: ["木の写真を追加する", "情報を確かめ、足りない木を教える", "木をめぐる散歩コースづくりを手伝う"],
    ambassadorAskSend: "申し込む",
    ambassadorNotNow: "今はしない",
    ambassadorSentTitle: "申請を送信しました",
    ambassadorSentBody: "リストについていくつか質問をメールでお送りします。",
    ambassadorWriteTo: (email) => `${email} 宛にご連絡します。`,
    ambassadorDone: "完了",
    photoOpen: "写真を開く",
    photoPrev: "前の写真",
    photoNext: "次の写真",
    photoNumber: (n, total) => `写真 ${n}/${total}`,
    appStoreBadge: "App StoreでAncient Treesを入手",
    openInApp: "アプリで開く",
    androidTitle: "Android版を開発中です",
    androidNote: "Android版はまだありません。メールアドレスを残していただければ、公開日にお知らせします。",
    emailLabel: "メールアドレス",
    notifyMe: "知らせてほしい",
    waitlistSent: "\u30ea\u30b9\u30c8\u306b\u767b\u9332\u3055\u308c\u307e\u3057\u305f\u3002Android\u7248\u304c\u51fa\u305f\u3089\u304a\u77e5\u3089\u305b\u3057\u307e\u3059\u3002",
    scanToOpen: "スマートフォンでスキャンすると、そちらで開けます。",
    photoClose: "閉じる",
    photoFull: "原寸で見る",
  },
};

/** Chrome strings for `lang`, English wherever that language has no entry. */
export function ui(lang: string): UIStrings {
  return { ...EN, ...(TABLE[lang] ?? {}) };
}

/** The autonym: each language's name written in that language.
 *
 * Was a link phrase ("en espa\u00f1ol", "in het Nederlands") for the sentence
 * this replaces. A picker wants bare names, which is what AllTrails and komoot
 * both show, and which is why a list of them does not read as mixed language:
 * "English \u00b7 Deutsch \u00b7 \u65e5\u672c\u8a9e" is a set of labels, not prose. */
export const LANG_NAME: Record<string, string> = {
  en: "English",
  es: "Espa\u00f1ol",
  it: "Italiano",
  nl: "Nederlands",
  de: "Deutsch",
  pt: "Portugu\u00eas",
  fr: "Fran\u00e7ais",
  ja: "\u65e5\u672c\u8a9e",
};

/** Reciprocal hreflang link tags for a page that exists in English and in
 * `lang`. x-default points at English, the language most of our audience
 * searches in. Both pages must emit the same pair, or Google ignores the
 * annotation entirely: hreflang is only honoured when it is reciprocal. */
export function hreflangLinks(lang: string, enPath: string, langPath: string): string {
  return hreflangSet(enPath, { [lang]: langPath });
}

/** Every language that has an overlay for this city. */
export function languagesForCity(slug: string): string[] {
  return translatedLanguages()
    .filter((l) => fs.existsSync(path.join(DATA, "i18n", l, `${slug}.json`)))
    .sort();
}

/** Reciprocal hreflang for the WHOLE set of variants of one page.
 *
 * The single-alternate version this replaces was correct for exactly as long
 * as there was one translated language. hreflang is only honoured when the
 * annotation is reciprocal AND complete: every variant must list every other
 * variant, itself included. With Spanish alone, "English plus Spanish plus
 * x-default" satisfied that. The moment a city exists in two languages, a
 * page emitting only itself and English describes a set that the other
 * variant contradicts, and Google drops the whole annotation rather than
 * guessing, which is worse than having none.
 *
 * That is not hypothetical at seven languages: Brussels is a Dutch and a
 * French city, Barcelona a Spanish and arguably an Italian-market one. Fixed
 * before the first of them ships rather than after, because a broken
 * annotation is invisible from our side and only shows up as pages quietly
 * not ranking in their own language.
 *
 * `variants` maps language code to that language's path for this same page.
 * The self-referencing tag is included by construction, since the page's own
 * language is one of the keys.
 */
export function hreflangSet(enPath: string, variants: Record<string, string>): string {
  const out = [`<link rel="alternate" hreflang="en" href="${BASE_URL}${enPath}">`];
  for (const lang of Object.keys(variants).sort()) {
    out.push(`<link rel="alternate" hreflang="${lang}" href="${BASE_URL}${variants[lang]}">`);
  }
  out.push(`<link rel="alternate" hreflang="x-default" href="${BASE_URL}${enPath}">`);
  return out.join("\n");
}

/** The full hreflang block for a city page, tree page or question page,
 * covering every language that actually has an overlay for that city. `kind`
 * decides the path shape; the question page is the one whose last segment
 * differs per language, which is why QUESTION_SLUG is consulted here rather
 * than at each call site. */
/** A translated page's own path, converted back to its English one.
 *
 * Stripping the /[lang] prefix is not enough and that cost a build to learn.
 * The question page's last segment is localised on purpose (Contract J: the
 * URL carries the phrase people actually search), so /de/aachen/aeltester-baum
 * strips to /aachen/aeltester-baum, which is not an English path at all. The
 * language picker then pasted the German slug into all seven URLs and qa found
 * 29,686 dead links.
 *
 * Tree and city slugs are identical across languages by design, so the
 * question slug is the only segment that needs translating back. */
export function toEnglishPath(pathname: string, lang: string): string {
  const clean = (pathname.replace(/\/index\.html$/, "").replace(/\.html$/, "") || "/");
  if (lang === "en") return clean;
  const stripped = clean.replace(new RegExp(`^/${lang}(?=/|$)`), "") || "/";
  const seg = stripped.split("/").filter(Boolean);
  if (seg.length === 2 && seg[1] === (QUESTION_SLUG[lang] ?? "")) {
    return `/${seg[0]}/oldest-tree`;
  }
  return stripped;
}

/** Which page types exist under /[lang]/. The single place that knows.
 *
 * Future-proofing, 2026-09-17: when a new page type ships in the seven
 * languages, it is added HERE and the language picker starts offering it on
 * every one of those pages at once. Nothing else needs touching, and no page
 * has to remember whether it has translations.
 *
 * "city" covers a city, its trees and its question page, which is why it is
 * matched last: those paths are one and two segments deep and would otherwise
 * swallow every standing page above them. */
const TRANSLATED_STANDING = new Set(["/", "/cities", "/explore"]);

/** Where this page lives in every language, for the PICKER.
 *
 * Deliberately NOT the same function as hreflangForCity, and the difference is
 * the point. hreflang advertises real translations to Google, so it lists only
 * the languages with an overlay. The picker offers a HUMAN every URL they can
 * actually reach, and since 2026-09-17 that is all seven everywhere, because
 * an untranslated page still renders with the frame in their language. Merging
 * the two would either hide reachable pages from readers or tell Google a
 * fallback is a translation, and both are wrong.
 *
 * Returns an empty object for a page type that has no translated route yet, so
 * the picker simply does not render there rather than offering a 404.
 */
export function pathInEveryLanguage(enPath: string): Record<string, string> {
  const clean = ("/" + enPath.replace(/^\/+|\/+$/g, "")).replace(/\/+/g, "/");
  const langs = translatedLanguages();
  const out: Record<string, string> = {};

  if (TRANSLATED_STANDING.has(clean)) {
    // The homepage is the one member whose clean path IS "/", so appending it
    // would give "/es/" where every other link on the site is written without
    // a trailing slash. qa.py resolves links literally, so the shapes match.
    for (const l of langs) out[l] = clean === "/" ? `/${l}` : `/${l}${clean}`;
    return out;
  }

  const seg = clean.split("/").filter(Boolean);
  if (seg.length === 1 || seg.length === 2) {
    const [slug, leafSeg] = seg;
    const leaf = leafSeg;
    // A one-segment path is only a city if we publish one by that name; this is
    // what keeps /privacy and /sponsor out without naming them.
    if (!fs.existsSync(path.join(DATA, "cities", `${slug}.json`))) return {};
    // A city, tree or question page exists only where the city is genuinely
    // translated: the tree fallbacks went on 2026-09-17 and the city and
    // question fallbacks on 2026-10-09. Offering a language whose page was
    // just deleted is how the picker produced 48,629 dead links, so the one
    // question asked here is whether an overlay exists.
    const usable = languagesForCity(slug);
    for (const l of usable) {
      out[l] = !leaf
        ? `/${l}/${slug}`
        : leaf === "oldest-tree"
          ? `/${l}/${slug}/${QUESTION_SLUG[l] ?? "oldest-tree"}`
          : `/${l}/${slug}/${leaf}`;
    }
    return out;
  }
  return {};
}

export function hreflangForCity(slug: string, kind: "city" | "question", treeSlug?: string): string {
  const langs = languagesForCity(slug);
  const enPath = kind === "question" ? `/${slug}/oldest-tree` : treeSlug ? `/${slug}/${treeSlug}` : `/${slug}`;
  const variants: Record<string, string> = {};
  for (const l of langs) {
    const path = kind === "question"
      ? `/${l}/${slug}/${QUESTION_SLUG[l] ?? "oldest-tree"}`
      : treeSlug ? `/${l}/${slug}/${treeSlug}` : `/${l}/${slug}`;
    // An alternate on the recovery noindex list is left out (2026-10-22).
    // Google drops a noindexed page from an hreflang cluster anyway and still
    // crawls it as an alternate, so naming it only spends crawl on a page we
    // asked Google not to list; TRANSLATIONS_OUT in scripts/thin_pages.py
    // put every translation there. A page with no indexable alternate carries
    // no block at all: a self-only cluster says nothing.
    if (isNoindexed(path)) continue;
    variants[l] = path;
  }
  return Object.keys(variants).length && !isNoindexed(enPath) ? hreflangSet(enPath, variants) : "";
}

/** getStaticPaths for a language's city pages, shared so the per-language
 * route files stay three lines each and the guards below cannot drift apart.
 *
 * The two throws are the guards Contract J relies on. An overlay missing a
 * tree means the English city grew past its translation, and a page silently
 * falling back to an English story would read as sloppiness rather than as
 * the gap it is. The intro word count is Contract C, checked here because a
 * translated intro is written by hand and nothing else would catch it.
 */

/** Languages that do not put spaces between words, so a whitespace token count
 * measures nothing in them and the bars are expressed in characters instead.
 *
 * This lives here, exported, because the first version of it did not: the
 * story bar knew about Japanese and the intro bar did not, and the build died
 * on "ja/tokyo: intro is 1 words". Two checks that must agree, written twice,
 * disagreed within the hour. */
export const UNSPACED = new Set(["ja", "zh", "ko"]);

/** Length of a piece of prose in the unit its language is measured in. */
export function proseLength(text: string, lang: string): number {
  return UNSPACED.has(lang) ? text.length : text.split(/\s+/).filter(Boolean).length;
}

/** The intro bar: 60-100 words, or 150-250 characters where words are not
 * separable. Same intent, different unit. */
export function introBar(lang: string): [number, number] {
  return UNSPACED.has(lang) ? [150, 250] : [60, 100];
}

/** The story bar: 150-250 words, or 350-600 characters. */
export function storyBar(lang: string): [number, number] {
  return UNSPACED.has(lang) ? [350, 600] : [150, 250];
}

export async function translatedCityPaths(lang: string, allCities: CityLike[]) {
  return translatedCities(lang).map((slug) => {
    const city = allCities.find((c) => c.id === slug);
    if (!city) throw new Error(`data/i18n/${lang}/${slug}.json has no matching English city file`);
    const tr = cityTranslation(lang, slug)!;
    const ids = (city.data.trees ?? []).map((t: { id: string }) => t.id);
    for (const id of ids) {
      if (!tr.trees[id]) throw new Error(`${lang}/${slug}: no translation for ${id}; the English city grew past the overlay`);
    }
    const [ilo, ihi] = introBar(lang);
    const iw = proseLength(tr.intro, lang);
    if (iw < ilo || iw > ihi) {
      throw new Error(`${lang}/${slug}: intro is ${iw} ${UNSPACED.has(lang) ? "chars" : "words"}, Contract C requires ${ilo}-${ihi}`);
    }
    return { params: { city: slug }, props: { city, tr } };
  });
}

/** Every city in this language: REAL translations only, since 2026-10-09.
 *
 * The fallback layer of 2026-09-17 (an untranslated city dressed in the
 * reader's language, the English text on a /es/ URL, canonical to English) is
 * gone, on Hidde's "do this" of 2026-10-09. It followed the competitors'
 * whole-site-per-locale convention and it was also 8,025 of the 11,526 pages
 * on the recovery noindex list: seven copies of every English page, which is
 * the scaled shape the September 2026 spam update demoted. Noindex did not
 * make them disappear from Google's crawl, and a noindex beside a canonical to
 * another URL is two instructions on one page. So the pages are not built;
 * every old URL redirects to its English page (redirect-map.ts, hard rule 3),
 * and a city regains its language URL the day a real overlay lands.
 *
 * The chrome keeps the reader's language where a page exists in it (the home,
 * /[lang]/cities, /[lang]/explore, the translated cities) and links an
 * untranslated city at its English URL, exactly as treeHref() has done for
 * tree pages since 2026-09-17. The `fallback` flag stays false everywhere and
 * is kept only so the components need no second edit. */
export async function allCityPathsFor(lang: string, allCities: CityLike[]) {
  const real = await translatedCityPaths(lang, allCities);
  return real.map((r: any) => ({ ...r, props: { ...r.props, fallback: false } }));
}

/** The path a city link takes in this language: the translated page where one
 * exists, the English page otherwise. The one rule for every city link in the
 * translated chrome (cities index, nearby cities, the home), so a removed page
 * can never again leave its links behind (qa found 25,208 dead ones the first
 * time pages went and links stayed, 2026-09-17). */
export function cityHref(lang: string, slug: string): string {
  return lang !== "en" && languagesForCity(slug).includes(lang) ? `/${lang}/${slug}` : `/${slug}`;
}

/** Every tree in this language: real translations, then the rest as fallbacks.
 * Added 2026-09-17 because the city-level fallback alone left 25,208 dead
 * links: a fallback city page links to its trees and its question page, and
 * those did not exist in that language. The convention is a whole site per
 * locale or none of it. */
export async function allTreePathsFor(lang: string, allCities: any[], renderableTrees: any, treeSlugsForCity: any) {
  // Real translations only, on Hidde's call of 2026-09-17 after seeing what the
  // fallback half cost: 21,042 pages that Google is told to ignore, 24 of the
  // 33 minutes a build takes, and the only thing they added was the buttons
  // around an English story being in the reader's language.
  //
  // The 1,106 genuinely translated tree pages are untouched and this grows on
  // its own: translate a city tomorrow and its trees become real translated
  // pages the same day, with no decision to revisit.
  //
  // A city without an overlay therefore links its trees at the ENGLISH URL.
  // treeHref() in TranslatedCityPage and TranslatedTreePage is the one place
  // that decides it, because the first version of this dropped the pages and
  // left the links, and qa found 25,208 dead ones.
  const real = await translatedTreePaths(lang, allCities, renderableTrees, treeSlugsForCity);
  return real.map((r: any) => ({ ...r, props: { ...r.props, fallback: false } }));
}

/** Every question page in this language: real translations only (see allCityPathsFor). */
export async function allQuestionPathsFor(lang: string, allCities: any[], renderableTrees: any) {
  const real = await translatedQuestionPaths(lang, allCities, renderableTrees);
  return real.map((r: any) => ({ ...r, props: { ...r.props, fallback: false } }));
}

export async function translatedTreePaths(lang: string, allCities: any[], renderableTrees: any, treeSlugsForCity: any) {
  const paths: { params: { city: string; tree: string }; props: any }[] = [];
  for (const slug of translatedCities(lang)) {
    const city = allCities.find((c) => c.id === slug);
    if (!city) continue;
    const tr = cityTranslation(lang, slug)!;
    const trees = renderableTrees(city);
    const tslugs = treeSlugsForCity(city);
    for (const tree of trees) {
      const x = tr.trees[tree.id];
      if (!x) throw new Error(`${lang}/${slug}: no translation for ${tree.id}`);
      const [slo, shi] = storyBar(lang);
      const wc = proseLength(x.story, lang);
      if (wc < slo || wc > shi) {
        throw new Error(`${lang}/${slug}/${tslugs[tree.id]}: story is ${wc} ${UNSPACED.has(lang) ? "chars" : "words"}, the bar is ${slo}-${shi} and applies in every language`);
      }
      paths.push({ params: { city: slug, tree: tslugs[tree.id] }, props: { city, tree, x, allTrees: trees, tr } });
    }
  }
  return paths;
}

/** getStaticPaths for a language's question pages.
 *
 * Contract B v1.18 applies in every language: a place with one tree publishes
 * no question page, here for the same reason as in English. No translated
 * city was on one tree the day this was written, so this is a guard against a
 * language overlay outliving the rule rather than a fix for anything live.
 */
export async function translatedQuestionPaths(lang: string, allCities: any[], renderableTrees: any) {
  return translatedCities(lang).flatMap((slug) => {
    const city = allCities.find((c) => c.id === slug);
    if (!city) throw new Error(`data/i18n/${lang}/${slug}.json has no matching English city file`);
    if (!cityHasQuestionPage(renderableTrees(city).length)) return [];
    return [{ params: { city: slug }, props: { city, tr: cityTranslation(lang, slug)! } }];
  });
}
