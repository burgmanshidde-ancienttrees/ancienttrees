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
import path from "node:path";
import { DATA } from "./data-dir";
import { BASE_URL } from "./schema";
import { cityHasQuestionPage } from "./question-page";
import { fitTitle } from "./title";

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
  mappingAll: string;
  missingOrWrong: (city: string) => string;
  tellUs: string;
  goingThere: string;
  downloadTrees: (n: number) => string;
  worksOffline: string;
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
  seenIt: string;
  worthItAsk: (name: string) => string;
  worthItDone: (name: string) => string;
  seenItDone: string;
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
  addPhotoOwnOnly: string;
  /** The lasting state of a photograph somebody sent of this tree, written
   *  beside the control on every later visit (CONVENTIONS.md, "Landing after
   *  you have added something"): waiting, or on the page. Same words as the
   *  app's Sighting.photoState. */
  addPhotoWaiting: string;
  addPhotoOnPage: string;
  /** The link from the acknowledgement to where the photograph now lives. */
  addPhotoSeeMine: string;
  /** The optional second photograph when somebody adds a tree: the sign
   *  beside it, which names the species, often the age and the tree itself
   *  (Hidde, 2026-09-24). Same words as the app's describe form. */
  signPhotoLabel: string;
  signPhotoHint: string;
  signPhotoBtn: string;
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
  homeShelfMeta: (n: number, country: string) => string;
}

const EN: UIStrings = {
  home: "Home",
  backToTrees: (n) => `\u2190 ${n === 1 ? "The tree" : `The ${n} trees`}`,
  treesOnMap: (n) => `${n} ${n === 1 ? "tree" : "trees"} on the map`,
  heading: (c) => `Ancient Trees in ${c}`,
  readMore: "Read more",
  visitedOf: (n, city) => `visited in ${city}`,
  mappingAll: "We are mapping every remarkable tree in the world.",
  missingOrWrong: (city) => `Do you know one in ${city} we are missing, or see a mistake here?`,
  tellUs: "Tell us",
  goingThere: "Going?",
  downloadTrees: (n) => `Download the ${n} trees`,
  worksOffline: "as a map file and open it in Google Maps, Organic Maps or any hiking app. It works offline.",
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
  appPitchTreeTitle: "Collect the trees you stand in front of",
  appPitchTreeBody: "Ticking this one off, walks past several more, and your collection growing city by city: that is the Ancient Trees app.",
  appPitchCityTitle: "Walk them with the app",
  appPitchCityBody: "The walking routes, your saved trees, and the collection of the ones you have stood in front of: the Ancient Trees app.",
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
  photoOpen: "Open the photograph",
  photoPrev: "Previous photograph",
  photoNext: "Next photograph",
  photoNumber: (n, total) => `Photograph ${n} of ${total}`,
  appStoreBadge: "Get Ancient Trees on the App Store",
  openInApp: "Open in the app",
  androidTitle: "We are working on the Android app",
  androidNote: "There is no Android app yet. Leave your email and we will write to you the day there is one.",
  emailLabel: "Email address",
  notifyMe: "Notify me",
  waitlistSent: "You are on the list. We will write to you the day it opens.",
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
  takeMeThere: "Take me there",
  showOnMap: "Show on the map",
  showPhoto: "Show the photograph",
  openFullMap: "Open the full map",
  dirTitle: "Open directions in",
  noPhotoYet: "No photograph yet",
  pinShowUs: "Show us where it is",
  pinTitle: "Where is it really?",
  pinHelp: "Drag the map until the pin sits on the tree.",
  pinZoom: "Zoom in as far as you like. The button wakes up once you have moved it.",
  pinMoved: (m) => `That is ${m} m from where we have it.`,
  pinSend: "The tree is here",
  pinSending: "Sending",
  pinDone: "We will check it and move the pin.",
  pinFailed: "That did not go through. Try again in a moment.",
  pinNeedsAccount: "Sending needs a free account, so we can tell you what your correction changed.",
  cancel: "Cancel",
  appleMaps: "Apple Maps",
  goBack: "Back",
  chipOldest: "Oldest tree",
  googleMaps: "Google Maps",
  seenIt: "I have seen this one",
  worthItAsk: (n) => `Yes, ${n} was worth the visit`,
  worthItDone: (n) => `You found ${n} worth the visit. Tap to undo`,
  seenItDone: "Ticked off",
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
  noPhotoLicence: "Nobody has published a photograph of this tree under a licence we can use.",
  addPhotoBtn: "Add a photo",
  addPhotoBtnQuiet: "Add your own photo",
  photoCanGoHere: "If you have one you took yourself, it can go here.",
  addPhotoSignIn: "Sign in first, then choose your photograph.",
  addPhotoSending: "Sending...",
  addPhotoBadFile: "That picture could not be read. Try another one.",
  addPhotoThanks: "Thank you. We look at every photograph before it goes on a page, and you will hear what happened to yours.",
  addPhotoFailed: "That did not go through. Try again in a moment.",
  addPhotoOwnOnly: "We can only use photographs you took yourself.",
  addPhotoWaiting: "Your photo, waiting for a look",
  addPhotoOnPage: "Your photo is on this page",
  addPhotoSeeMine: "See it in My trees",
  signPhotoLabel: "Is there a sign by the tree?",
  signPhotoHint: "Optional. You can add a photo of the sign as well. It often names the tree, the species and its age.",
  signPhotoBtn: "Add a photo of the sign",
  havePhotographed: "Have you photographed this tree?",
  havePhotographedLine: "If yours shows it better than the picture above, it can take its place, or stand beside it.",
  goNote: "The button above opens directions in your maps app.",
  approxNote: "The pin marks the right spot roughly, not the tree itself. It stands here, but we have not confirmed the precise position on the ground yet.",
  knowExactly: "Know exactly where it is?",
  couldUseHelp: "We could use your help.",
  researchedRemotely: "This page was researched from a distance. If you know this tree, you know things we do not.",
  knowMoreThanUs: "Do you know more than we do?",
  ifOlderTree: (c) => `If you know an older tree in ${c}, or see a mistake here, tell us and we correct it.`,
  citiesCrumb: "Cities",
  citiesTitle: "Every City We Have Mapped",
  citiesHeading: "Every city we have mapped",
  citiesLead: (c, t) => `${c} cities, ${t} trees, each one researched and verified.`,
  citiesDescription: "Every city on the map, by country: the remarkable old trees of each, verified, with their stories and exact spots.",
  exploreTitle: "Ancient Tree Map: every remarkable old tree, one map",
  exploreDescription: "The interactive map of every verified ancient tree on the site, each pin a tree worth standing in front of.",
  exploreHeading: "The ancient tree map",
  exploreNote: "Every pin is a tree worth the walk. Find one near you, or somewhere you are going.",
  exploreWhatH: "What is on this map",
  exploreWhatBody: (t, p, c) => `${t} trees in ${p} places across ${c} countries, every one checked against at least two independent sources before it went on. Each pin opens a tree with its age, its species, why it is worth standing in front of, and directions from where you are.`,
  exploreWalksH: "The tightest walks",
  exploreWalksBody: "A map of scattered pins is a list. What makes an afternoon is trees close enough to walk between, so these are the places where the whole set fits in one stroll:",
  exploreIslandsH: "Islands",
  exploreIslandsBody: "An island is a different kind of day. The trees sit a drive apart rather than a walk, and what you get for the distance is a tree that grows nowhere else: dragon trees, laurel forest that outlived the Ice Age, pines that reach heights the mainland never manages.",
  exploreNotH: "What is not on it, and why",
  exploreNotBody: "Every pin says how precise it is. A tree marked approximate means we know the park but not the trunk, and the page says so rather than sending you to a spot where the tree is not. Trees on private land are left off entirely, as are trees whose own register hides their position, because the people who protect them have a reason. Nothing here is a bulk street-tree inventory: a tree earns a pin by being remarkable, not by existing.",
  exploreBrowse: "Browse another way:",
  homeTitle: "Ancient Trees: remarkable old trees near you, mapped",
  homeDescription: "Find the remarkable old trees around you. Each one verified, each with its story, its exact spot and directions from where you stand.",
  homeHeroLead: "Trees worth the walk,",
  homeHeroEm: "wherever you are.",
  homeSub: "Made for people who love being outside. Find remarkable old trees nearby, explore a few of them in an afternoon, read the story behind each one, and tick off the trees you visit.",
  homeFindH: "The trees near you, right now.",
  homeFindBody: "The map finds the remarkable old trees closest to where you are standing, and points you at the nearest one with a walk time and directions to your phone.",
  homeWalkH: "A route past the ones worth seeing.",
  homeWalkBody: "Only the most remarkable, linked into one walk you can do in an afternoon, each with its story and the month it is at its most spectacular, so you know when to go.",
  homeCollectH: "Tick off the ones you have stood in front of.",
  homeCollectBody: "Check in at the tree and watch your collection grow: trees, cities, species. Rarer and older trees count for more, and badges for a finished city are on their way.",
  homeDirectoryH: "Ancient trees anywhere",
  homeMission: "We are on a mission to map every remarkable tree in the world, and we could use your help. If you know a good tree, or want to map a whole city,",
  homeMissionLink: "tell us about it",
  mapFilterGroup: "Filter the map",
  mapFilterFav: "Favourites",
  mapFilterMine: "My trees",
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
  homeStatOldest: "oldest, yrs",
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
    homeStatOldest: "el más viejo, años",
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
    homeShelfMeta: (n, country) => `${n} árboles \u00b7 ${country}`,
    exploreWalkItem: (n, d) => `${n} árboles en ${d}`,
    citiesCrumb: "Ciudades",
    citiesTitle: "Todas las ciudades del mapa",
    citiesHeading: "Todas las ciudades del mapa",
    citiesLead: (c, t) => `${c} ciudades, ${t} árboles, cada uno investigado y verificado.`,
    citiesDescription: "Todas las ciudades del mapa, por país: los árboles viejos y notables de cada una, verificados, con su historia y su sitio exacto.",
    exploreTitle: "Mapa de árboles históricos del mundo",
    exploreDescription: "El mapa interactivo de todos los árboles históricos verificados del sitio, cada marcador un árbol ante el que merece la pena plantarse.",
    exploreHeading: "El mapa de árboles históricos",
    exploreNote: "Cada marcador es un árbol que merece el paseo. Encuentra uno cerca de ti, o donde vayas a ir.",
    exploreWhatH: "Qué hay en este mapa",
    exploreWhatBody: (t, p, c) => `${t} árboles en ${p} lugares de ${c} países, cada uno contrastado con al menos dos fuentes independientes antes de entrar. Cada marcador abre un árbol con su edad, su especie, por qué merece la pena plantarse ante él y cómo llegar desde donde estás.`,
    exploreWalksH: "Los paseos más compactos",
    exploreWalksBody: "Un mapa de marcadores dispersos es una lista. Lo que hace una tarde son árboles lo bastante cerca como para ir andando de uno a otro, así que estos son los lugares donde el conjunto entero cabe en un solo paseo:",
    exploreIslandsH: "Islas",
    exploreIslandsBody: "Una isla es otro tipo de día. Los árboles están a un trayecto en coche, no a un paseo, y lo que ganas a cambio de la distancia es un árbol que no crece en ningún otro sitio: dragos, laurisilva que sobrevivió a la glaciación, pinos que alcanzan alturas que el continente nunca da.",
    exploreNotH: "Qué no está, y por qué",
    exploreNotBody: "Cada marcador dice hasta qué punto es preciso. Un árbol marcado como aproximado significa que conocemos el parque pero no el tronco, y la página lo dice en vez de mandarte a un sitio donde el árbol no está. Los árboles en terreno privado se quedan fuera por completo, igual que aquellos cuyo propio registro oculta su posición, porque quien los protege tiene sus motivos. Esto no es un inventario masivo del arbolado urbano: un árbol se gana su marcador por ser singular, no por existir.",
    exploreBrowse: "Explora de otra manera:",
    homeTitle: "Ancient Trees: árboles singulares cerca de ti",
    homeDescription: "Encuentra los árboles históricos que tienes alrededor. Cada uno verificado, con su historia, su sitio exacto y cómo llegar desde donde estás.",
    homeHeroLead: "Árboles que merecen el paseo,",
    homeHeroEm: "estés donde estés.",
    homeSub: "Hecho para quien disfruta de estar al aire libre. Encuentra árboles singulares cerca, recorre unos cuantos en una tarde, lee la historia de cada uno y ve marcando los que visitas.",
    homeFindH: "Los árboles que tienes cerca, ahora mismo.",
    homeFindBody: "El mapa encuentra los árboles históricos más cercanos al sitio donde estás y te señala el más próximo, con el tiempo a pie y las indicaciones en tu móvil.",
    homeWalkH: "Una ruta que pasa por los que merecen la pena.",
    homeWalkBody: "Solo los más singulares, enlazados en un paseo que puedes hacer en una tarde, cada uno con su historia y el mes en que está más espectacular, para que sepas cuándo ir.",
    homeCollectH: "Marca aquellos ante los que te has plantado.",
    homeCollectBody: "Marca el árbol cuando estés delante y mira crecer tu colección: árboles, ciudades, especies. Los árboles más raros y más viejos cuentan más, y las insignias por completar una ciudad están en camino.",
    homeDirectoryH: "Árboles históricos en cualquier parte",
    homeMission: "Estamos cartografiando todos los árboles singulares del mundo, y nos vendría bien tu ayuda. Si conoces un buen árbol, o quieres cartografiar una ciudad entera,",
    homeMissionLink: "cuéntanoslo",
    mapFilterGroup: "Filtrar el mapa",
    mapFilterFav: "Favoritos",
    mapFilterMine: "Mis árboles",
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
    takeMeThere: "Cómo llegar",
    showOnMap: "Ver en el mapa",
    showPhoto: "Ver la fotografía",
    openFullMap: "Abrir el mapa completo",
    dirTitle: "Abrir la ruta en",
    noPhotoYet: "Aún no hay fotografía",
    pinShowUs: "Muéstranos dónde está",
    pinTitle: "¿Dónde está en realidad?",
    pinHelp: "Mueve el mapa hasta que el marcador quede sobre el árbol.",
    pinZoom: "Acércate todo lo que quieras. El botón se activa cuando lo hayas movido.",
    pinMoved: (m) => `Está a ${m} m de donde lo tenemos.`,
    pinSend: "El árbol está aquí",
    pinSending: "Enviando",
    pinDone: "Lo comprobaremos y moveremos el marcador.",
    pinFailed: "No se ha podido enviar. Inténtalo de nuevo en un momento.",
    pinNeedsAccount: "Para enviar necesitas una cuenta gratuita, así podemos contarte qué ha cambiado con tu corrección.",
    cancel: "Cancelar",
    appleMaps: "Apple Maps",
    goBack: "Atrás",
    chipOldest: "Árbol más antiguo",
    googleMaps: "Google Maps",
    seenIt: "Ya he visto este",
    worthItAsk: (n) => `Sí, ${n} mereció la visita`,
    worthItDone: (n) => `Te mereció la visita ${n}. Toca para deshacer`,
    seenItDone: "Visitado",
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
    noPhotoLicence: "Nadie ha publicado una fotografía de este árbol con una licencia que podamos usar.",
    addPhotoBtn: "Añadir una foto",
    addPhotoBtnQuiet: "Añade tu propia foto",
    photoCanGoHere: "Si tienes una tomada por ti mismo, puede ir aquí.",
    addPhotoSignIn: "Inicia sesión primero y luego elige tu fotografía.",
    addPhotoSending: "Enviando...",
    addPhotoBadFile: "No se pudo leer esa imagen. Prueba con otra.",
    addPhotoThanks: "Gracias. Revisamos cada fotografía antes de publicarla, y te diremos qué pasó con la tuya.",
    addPhotoFailed: "Eso no se pudo enviar. Inténtalo de nuevo en un momento.",
    addPhotoOwnOnly: "Solo podemos usar fotografías que hayas hecho tú.",
    addPhotoWaiting: "Tu foto, pendiente de revisión",
    addPhotoOnPage: "Tu foto está en esta página",
    addPhotoSeeMine: "Verla en Mis árboles",
    signPhotoLabel: "¿Hay un letrero junto al árbol?",
    signPhotoHint: "Opcional. También puedes añadir una foto del letrero. Suele indicar el nombre del árbol, la especie y su edad.",
    signPhotoBtn: "Añade una foto del letrero",
    havePhotographed: "¿Has fotografiado este árbol?",
    havePhotographedLine: "Si la tuya lo muestra mejor que la foto de arriba, puede ocupar su lugar, o aparecer junto a ella.",
    goNote: "El botón de arriba abre las indicaciones en tu aplicación de mapas.",
    approxNote: "El marcador señala la zona correcta de forma aproximada, no el árbol exacto. Está aquí, pero todavía no hemos confirmado la posición precisa sobre el terreno.",
    knowExactly: "¿Sabes exactamente dónde está?",
    couldUseHelp: "Nos vendría bien tu ayuda.",
    researchedRemotely: "Esta página se investigó a distancia. Si conoces este árbol, sabes cosas que nosotros no sabemos.",
    knowMoreThanUs: "¿Sabes más que nosotros?",
    ifOlderTree: (c) => `Si conoces un árbol más antiguo en ${c}, o ves aquí un error, dínoslo y lo corregimos.`,
    home: "Inicio",
    backToTrees: (n) => `\u2190 ${n === 1 ? "El \u00e1rbol" : `Los ${n} \u00e1rboles`}`,
    treesOnMap: (n) => `${n} ${n === 1 ? "\u00e1rbol" : "\u00e1rboles"} en el mapa`,
    heading: (c) => `\u00c1rboles hist\u00f3ricos de ${c}`,
    readMore: "Leer m\u00e1s",
    visitedOf: (n, city) => `visitados en ${city}`,
    mappingAll: "Estamos cartografiando todos los \u00e1rboles singulares del mundo.",
    missingOrWrong: (city) => `\u00bfConoces uno en ${city} que nos falte, o ves aqu\u00ed un error?`,
    tellUs: "Cu\u00e9ntanoslo",
    goingThere: "\u00bfVas a ir?",
    downloadTrees: (n) => `Descarga los ${n} \u00e1rboles`,
    worksOffline: "como archivo de mapa y \u00e1brelo en Google Maps, Organic Maps o cualquier aplicaci\u00f3n de senderismo. Funciona sin conexi\u00f3n.",
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
    appPitchTreeTitle: "Colecciona los árboles ante los que te plantas",
    appPitchTreeBody: "Marcar este, rutas a pie que pasan por varios más y tu colección creciendo ciudad a ciudad: eso es la aplicación Ancient Trees.",
    appPitchCityTitle: "Recórrelos con la aplicación",
    appPitchCityBody: "Las rutas a pie, tus árboles guardados y la colección de aquellos ante los que ya te has plantado: la aplicación Ancient Trees.",
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
    waitlistSent: "Ya estás en la lista. Te escribiremos el día que esté lista.",
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
    homeStatOldest: "il più vecchio, anni",
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
    homeShelfMeta: (n, country) => `${n} alberi \u00b7 ${country}`,
    exploreWalkItem: (n, d) => `${n} alberi in ${d}`,
    citiesCrumb: "Città",
    citiesTitle: "Tutte le città sulla mappa",
    citiesHeading: "Tutte le città sulla mappa",
    citiesLead: (c, t) => `${c} città, ${t} alberi, ognuno documentato e verificato.`,
    citiesDescription: "Tutte le città sulla mappa, per paese: gli alberi antichi e notevoli di ognuna, verificati, con la loro storia e il punto esatto.",
    exploreTitle: "Mappa degli alberi monumentali del mondo",
    exploreDescription: "La mappa interattiva di tutti gli alberi monumentali verificati del sito, ogni segnaposto un albero davanti a cui vale la pena fermarsi.",
    exploreHeading: "La mappa degli alberi monumentali",
    exploreNote: "Ogni segnaposto è un albero che vale la camminata. Trovane uno vicino a te, o dove stai andando.",
    exploreWhatH: "Che cosa c'è su questa mappa",
    exploreWhatBody: (t, p, c) => `${t} alberi in ${p} luoghi di ${c} paesi, ognuno verificato su almeno due fonti indipendenti prima di finire qui. Ogni segnaposto apre un albero con la sua età, la specie, il motivo per cui vale la pena fermarsi davanti e le indicazioni da dove sei.`,
    exploreWalksH: "Le passeggiate più compatte",
    exploreWalksBody: "Una mappa di segnaposti sparsi è un elenco. Quello che fa un pomeriggio sono alberi abbastanza vicini da andare a piedi dall'uno all'altro, quindi questi sono i posti dove l'insieme intero sta in una sola passeggiata:",
    exploreIslandsH: "Isole",
    exploreIslandsBody: "Un'isola è una giornata di un altro tipo. Gli alberi distano un tragitto in auto invece di una passeggiata, e in cambio della distanza trovi un albero che non cresce da nessun'altra parte: alberi del drago, laurisilva sopravvissuta all'era glaciale, pini che raggiungono altezze che sulla terraferma non si vedono.",
    exploreNotH: "Che cosa non c'è, e perché",
    exploreNotBody: "Ogni segnaposto dice quanto è preciso. Un albero segnato come approssimativo vuol dire che conosciamo il parco ma non il tronco, e la pagina lo scrive invece di mandarti in un punto dove l'albero non c'è. Gli alberi su terreno privato restano fuori del tutto, come quelli di cui il registro stesso nasconde la posizione, perché chi li protegge ha le sue ragioni. Qui non c'è nessun censimento del verde urbano: un albero si guadagna il segnaposto perché è notevole, non perché esiste.",
    exploreBrowse: "Sfoglia in un altro modo:",
    homeTitle: "Ancient Trees: alberi monumentali vicino a te",
    homeDescription: "Trova gli alberi monumentali che hai intorno. Ognuno verificato, con la sua storia, il punto esatto e le indicazioni da dove sei.",
    homeHeroLead: "Alberi che valgono la camminata,",
    homeHeroEm: "ovunque tu sia.",
    homeSub: "Fatto per chi ama stare all'aperto. Trova alberi notevoli lì vicino, guardane qualcuno in un pomeriggio, leggi la storia di ognuno e spunta quelli che visiti.",
    homeFindH: "Gli alberi vicino a te, adesso.",
    homeFindBody: "La mappa trova gli alberi monumentali più vicini al punto in cui sei e ti indica il più prossimo, con il tempo a piedi e le indicazioni sul telefono.",
    homeWalkH: "Un percorso che passa da quelli che valgono.",
    homeWalkBody: "Solo i più notevoli, uniti in una passeggiata che fai in un pomeriggio, ognuno con la sua storia e il mese in cui dà il meglio, così sai quando andare.",
    homeCollectH: "Spunta quelli davanti a cui ti sei fermato.",
    homeCollectBody: "Segna l'albero quando ci sei davanti e guarda crescere la tua collezione: alberi, città, specie. Gli alberi più rari e più vecchi valgono di più, e i distintivi per una città completata stanno arrivando.",
    homeDirectoryH: "Alberi monumentali ovunque",
    homeMission: "Stiamo mappando tutti gli alberi notevoli del mondo, e il tuo aiuto ci serve. Se conosci un bell'albero, o vuoi mappare un'intera città,",
    homeMissionLink: "raccontacelo",
    mapFilterGroup: "Filtra la mappa",
    mapFilterFav: "Preferiti",
    mapFilterMine: "I miei alberi",
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
    takeMeThere: "Portami lì",
    showOnMap: "Mostra sulla mappa",
    showPhoto: "Mostra la fotografia",
    openFullMap: "Apri la mappa completa",
    dirTitle: "Apri il percorso in",
    noPhotoYet: "Ancora nessuna fotografia",
    pinShowUs: "Mostraci dov'è",
    pinTitle: "Dov'è davvero?",
    pinHelp: "Sposta la mappa finché il segnaposto non è sopra l'albero.",
    pinZoom: "Ingrandisci quanto vuoi. Il pulsante si attiva quando l'hai spostato.",
    pinMoved: (m) => `È a ${m} m da dove lo abbiamo noi.`,
    pinSend: "L'albero è qui",
    pinSending: "Invio in corso",
    pinDone: "Lo controlleremo e sposteremo il segnaposto.",
    pinFailed: "Non è andato a buon fine. Riprova tra un momento.",
    pinNeedsAccount: "Per inviare serve un account gratuito, così possiamo dirti cosa ha cambiato la tua correzione.",
    cancel: "Annulla",
    appleMaps: "Apple Maps",
    goBack: "Indietro",
    chipOldest: "Albero più antico",
    googleMaps: "Google Maps",
    seenIt: "L'ho già visto",
    worthItAsk: (n) => `Sì, ${n} valeva la visita`,
    worthItDone: (n) => `Hai trovato ${n} degno della visita. Tocca per annullare`,
    seenItDone: "Visitato",
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
    noPhotoLicence: "Nessuno ha pubblicato una fotografia di questo albero con una licenza che possiamo usare.",
    addPhotoBtn: "Aggiungi una foto",
    addPhotoBtnQuiet: "Aggiungi una tua foto",
    photoCanGoHere: "Se ne hai scattata una tu, può andare qui.",
    addPhotoSignIn: "Accedi prima, poi scegli la tua fotografia.",
    addPhotoSending: "Invio in corso...",
    addPhotoBadFile: "Non è stato possibile leggere questa immagine. Prova con un'altra.",
    addPhotoThanks: "Grazie. Guardiamo ogni fotografia prima che venga pubblicata, e ti diremo cosa ne è stato della tua.",
    addPhotoFailed: "L'invio non è andato a buon fine. Riprova tra poco.",
    addPhotoOwnOnly: "Possiamo usare solo fotografie scattate da te.",
    addPhotoWaiting: "La tua foto, in attesa di essere vista",
    addPhotoOnPage: "La tua foto è su questa pagina",
    addPhotoSeeMine: "Vedila in I miei alberi",
    signPhotoLabel: "C'è un cartello accanto all'albero?",
    signPhotoHint: "Facoltativo. Puoi aggiungere anche una foto del cartello. Spesso indica il nome dell'albero, la specie e l'età.",
    signPhotoBtn: "Aggiungi una foto del cartello",
    havePhotographed: "Hai fotografato questo albero?",
    havePhotographedLine: "Se la tua foto lo mostra meglio di quella qui sopra, può prenderne il posto, o comparire accanto ad essa.",
    goNote: "Il pulsante qui sopra apre le indicazioni nella tua app di mappe.",
    approxNote: "Il segnaposto indica all'incirca la zona giusta, non l'albero esatto. L'albero è qui, ma non abbiamo ancora confermato la posizione precisa sul posto.",
    knowExactly: "Sai esattamente dov'è?",
    couldUseHelp: "Ci farebbe comodo il tuo aiuto.",
    researchedRemotely: "Questa pagina è stata ricostruita a distanza. Se conosci questo albero, sai cose che noi non sappiamo.",
    knowMoreThanUs: "Ne sai più di noi?",
    ifOlderTree: (c) => `Se conosci un albero più antico a ${c}, o vedi qui un errore, faccelo sapere e lo correggiamo.`,
    home: "Home",
    backToTrees: (n) => `\u2190 ${n === 1 ? "L\u2019albero" : `I ${n} alberi`}`,
    treesOnMap: (n) => `${n} ${n === 1 ? "albero" : "alberi"} sulla mappa`,
    heading: (c) => `Alberi monumentali di ${c}`,
    readMore: "Leggi di pi\u00f9",
    visitedOf: (n, city) => `visitati a ${city}`,
    mappingAll: "Stiamo mappando tutti gli alberi notevoli del mondo.",
    missingOrWrong: (city) => `Ne conosci uno a ${city} che ci manca, o vedi un errore qui?`,
    tellUs: "Segnalacelo",
    goingThere: "Ci vai?",
    downloadTrees: (n) => `Scarica i ${n} alberi`,
    worksOffline: "come file di mappa e aprilo in Google Maps, Organic Maps o in qualsiasi app da escursionismo. Funziona anche offline.",
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
    appPitchTreeTitle: "Colleziona gli alberi davanti a cui ti fermi",
    appPitchTreeBody: "Spuntare questo, camminate che ne toccano molti altri e la tua collezione che cresce città dopo città: questa è l'app Ancient Trees.",
    appPitchCityTitle: "Percorrili con l'app",
    appPitchCityBody: "Gli itinerari a piedi, i tuoi alberi salvati e la collezione di quelli davanti a cui ti sei già fermato: l'app Ancient Trees.",
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
    waitlistSent: "Sei in lista. Ti scriveremo il giorno in cui sarà pronta.",
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
    homeStatOldest: "oudste, jaar",
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
    homeShelfMeta: (n, country) => `${n} bomen \u00b7 ${country}`,
    exploreWalkItem: (n, d) => `${n} bomen binnen ${d}`,
    citiesCrumb: "Steden",
    citiesTitle: "Alle steden op de kaart",
    citiesHeading: "Alle steden op de kaart",
    citiesLead: (c, t) => `${c} steden, ${t} bomen, stuk voor stuk uitgezocht en geverifieerd.`,
    citiesDescription: "Alle steden op de kaart, per land: de oude en bijzondere bomen van elke stad, geverifieerd, met hun verhaal en de precieze plek.",
    exploreTitle: "Kaart met monumentale bomen wereldwijd",
    exploreDescription: "De interactieve kaart van alle geverifieerde monumentale bomen op de site, elke speld een boom om voor te gaan staan.",
    exploreHeading: "De kaart met monumentale bomen",
    exploreNote: "Elke speld is een boom die de wandeling waard is. Zoek er een bij jou in de buurt, of op de plek waar je heen gaat.",
    exploreWhatH: "Wat er op deze kaart staat",
    exploreWhatBody: (t, p, c) => `${t} bomen op ${p} plekken in ${c} landen, stuk voor stuk nagetrokken bij minstens twee onafhankelijke bronnen voordat ze erop kwamen. Elke speld opent een boom met zijn leeftijd, zijn soort, waarom hij het waard is om voor te gaan staan, en de route vanaf waar je nu bent.`,
    exploreWalksH: "De kortste wandelingen",
    exploreWalksBody: "Een kaart met verspreide spelden is een lijst. Wat een middag maakt, zijn bomen die dicht genoeg bij elkaar staan om ertussen te lopen, dus dit zijn de plekken waar de hele reeks in één wandeling past:",
    exploreIslandsH: "Eilanden",
    exploreIslandsBody: "Een eiland is een ander soort dag. De bomen liggen een autorit uit elkaar in plaats van een wandeling, en wat je voor die afstand terugkrijgt is een boom die nergens anders groeit: drakenbloedbomen, laurierbos dat de ijstijd overleefde, dennen die hoogtes halen die het vasteland nooit haalt.",
    exploreNotH: "Wat er niet op staat, en waarom",
    exploreNotBody: "Bij elke speld staat hoe precies hij is. Een boom die bij benadering staat aangegeven, betekent dat we het park kennen maar niet de stam, en de pagina zegt dat, in plaats van je naar een plek te sturen waar de boom niet staat. Bomen op privéterrein blijven er helemaal af, net als bomen waarvan het register zelf de positie verbergt, want wie ze beschermt heeft daar een reden voor. Dit is geen complete inventarisatie van het straatgroen: een boom verdient zijn speld doordat hij bijzonder is, niet doordat hij bestaat.",
    exploreBrowse: "Blader op een andere manier:",
    homeTitle: "Ancient Trees: bijzondere oude bomen bij jou in de buurt",
    homeDescription: "Vind de bijzondere oude bomen om je heen. Stuk voor stuk geverifieerd, met hun verhaal, de precieze plek en de route vanaf waar je staat.",
    homeHeroLead: "Bomen die de wandeling waard zijn,",
    homeHeroEm: "waar je ook bent.",
    homeSub: "Gemaakt voor wie graag buiten is. Vind bijzondere oude bomen in de buurt, loop er een paar langs in één middag, lees het verhaal achter elke boom en vink de bomen af die je ziet.",
    homeFindH: "De bomen bij jou in de buurt, nu.",
    homeFindBody: "De kaart zoekt de bijzondere oude bomen die het dichtst bij je staan en wijst je de dichtstbijzijnde aan, met looptijd en de route op je telefoon.",
    homeWalkH: "Een route langs de bomen die het waard zijn.",
    homeWalkBody: "Alleen de bijzonderste, aan elkaar geregen tot één wandeling die je in een middag doet, elk met zijn verhaal en de maand waarin hij op zijn mooist is, zodat je weet wanneer je moet gaan.",
    homeCollectH: "Vink de bomen af waar je voor hebt gestaan.",
    homeCollectBody: "Vink de boom af terwijl je ervoor staat en zie je verzameling groeien: bomen, steden, soorten. Zeldzamere en oudere bomen tellen zwaarder, en badges voor een voltooide stad komen eraan.",
    homeDirectoryH: "Monumentale bomen overal",
    homeMission: "We brengen alle bijzondere bomen ter wereld in kaart, en we kunnen je hulp gebruiken. Ken je een mooie boom, of wil je een hele stad in kaart brengen,",
    homeMissionLink: "laat het ons weten",
    mapFilterGroup: "Kaart filteren",
    mapFilterFav: "Favorieten",
    mapFilterMine: "Mijn bomen",
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
    takeMeThere: "Breng me erheen",
    showOnMap: "Toon op de kaart",
    showPhoto: "Toon de foto",
    openFullMap: "Open de hele kaart",
    dirTitle: "Open de route in",
    noPhotoYet: "Nog geen foto",
    pinShowUs: "Laat ons zien waar hij staat",
    pinTitle: "Waar staat hij echt?",
    pinHelp: "Versleep de kaart tot de speld op de boom staat.",
    pinZoom: "Zoom zo ver in als je wilt. De knop wordt actief zodra je de speld hebt verplaatst.",
    pinMoved: (m) => `Dat is ${m} m van waar wij hem hebben.`,
    pinSend: "De boom staat hier",
    pinSending: "Versturen",
    pinDone: "We controleren het en verplaatsen de speld.",
    pinFailed: "Dat is niet gelukt. Probeer het zo nog eens.",
    pinNeedsAccount: "Versturen kan met een gratis account, zodat we je kunnen laten weten wat je correctie heeft veranderd.",
    cancel: "Annuleren",
    appleMaps: "Apple Maps",
    goBack: "Terug",
    chipOldest: "Oudste boom",
    googleMaps: "Google Maps",
    seenIt: "Deze heb ik gezien",
    worthItAsk: (n) => `Ja, ${n} was de moeite waard`,
    worthItDone: (n) => `Je vond ${n} de moeite waard. Tik om het terug te nemen`,
    seenItDone: "Afgevinkt",
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
    noPhotoLicence: "Niemand heeft een foto van deze boom gepubliceerd met een licentie die wij mogen gebruiken.",
    addPhotoBtn: "Voeg een foto toe",
    addPhotoBtnQuiet: "Voeg je eigen foto toe",
    photoCanGoHere: "Heb je er zelf een gemaakt, dan kan die hier komen.",
    addPhotoSignIn: "Log eerst in en kies dan je foto.",
    addPhotoSending: "Bezig met verzenden...",
    addPhotoBadFile: "Die foto kon niet worden gelezen. Probeer een andere.",
    addPhotoThanks: "Dank je. We bekijken elke foto voordat hij op een pagina komt, en je hoort wat ermee is gebeurd.",
    addPhotoFailed: "Dat is niet gelukt. Probeer het zo weer.",
    addPhotoOwnOnly: "We kunnen alleen foto's gebruiken die je zelf hebt gemaakt.",
    addPhotoWaiting: "Je foto, wacht op een blik",
    addPhotoOnPage: "Je foto staat op deze pagina",
    addPhotoSeeMine: "Bekijk hem bij Mijn bomen",
    signPhotoLabel: "Staat er een bordje bij de boom?",
    signPhotoHint: "Niet verplicht. Je kunt ook een foto van het bordje toevoegen. Vaak staan de naam van de boom, de soort en de leeftijd erop.",
    signPhotoBtn: "Voeg een foto van het bordje toe",
    havePhotographed: "Heb je deze boom gefotografeerd?",
    havePhotographedLine: "Als jouw foto hem beter laat zien dan de foto hierboven, kan die de plek innemen, of ernaast komen te staan.",
    goNote: "De knop hierboven opent de route in je kaartenapp.",
    approxNote: "De speld wijst de juiste plek bij benadering aan, niet de boom zelf. Hij staat hier, maar we hebben de precieze plek ter plaatse nog niet bevestigd.",
    knowExactly: "Weet je precies waar hij staat?",
    couldUseHelp: "We kunnen je hulp gebruiken.",
    researchedRemotely: "Deze pagina is op afstand samengesteld. Als je deze boom kent, weet je dingen die wij niet weten.",
    knowMoreThanUs: "Weet jij meer dan wij?",
    ifOlderTree: (c) => `Ken je een oudere boom in ${c}, of zie je hier een fout, laat het ons weten en we passen het aan.`,
    home: "Home",
    backToTrees: (n) => `\u2190 ${n === 1 ? "De boom" : `De ${n} bomen`}`,
    treesOnMap: (n) => `${n} ${n === 1 ? "boom" : "bomen"} op de kaart`,
    heading: (c) => `Monumentale bomen in ${c}`,
    readMore: "Lees meer",
    visitedOf: (n, city) => `bezocht in ${city}`,
    mappingAll: "We brengen alle bijzondere bomen ter wereld in kaart.",
    missingOrWrong: (city) => `Ken je er een in ${city} die hier mist, of zie je een fout?`,
    tellUs: "Laat het ons weten",
    goingThere: "Ga je erheen?",
    downloadTrees: (n) => `Download de ${n} bomen`,
    worksOffline: "als kaartbestand en open het in Google Maps, Organic Maps of een wandelapp naar keuze. Werkt ook zonder internet.",
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
    appPitchTreeTitle: "Verzamel de bomen waar je voor hebt gestaan",
    appPitchTreeBody: "Deze afvinken, wandelingen langs een stuk of wat andere, en je verzameling die per stad groeit: dat is de Ancient Trees-app.",
    appPitchCityTitle: "Loop ze met de app",
    appPitchCityBody: "De wandelroutes, je bewaarde bomen en de verzameling van de bomen waar je voor hebt gestaan: de Ancient Trees-app.",
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
    waitlistSent: "Je staat op de lijst. We schrijven je op de dag dat hij opengaat.",
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
    homeStatOldest: "ältester, Jahre",
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
    homeShelfMeta: (n, country) => `${n} Bäume \u00b7 ${country}`,
    exploreWalkItem: (n, d) => `${n} Bäume auf ${d}`,
    citiesCrumb: "Städte",
    citiesTitle: "Alle Städte auf der Karte",
    citiesHeading: "Alle Städte auf der Karte",
    citiesLead: (c, t) => `${c} Städte, ${t} Bäume, jeder einzeln recherchiert und geprüft.`,
    citiesDescription: "Alle Städte auf der Karte, nach Land: die alten und bemerkenswerten Bäume jeder Stadt, geprüft, mit ihrer Geschichte und dem genauen Standort.",
    exploreTitle: "Karte alter Bäume weltweit",
    exploreDescription: "Die interaktive Karte aller geprüften alten Bäume auf dieser Seite, jede Markierung ein Baum, vor dem es sich zu stehen lohnt.",
    exploreHeading: "Die Karte der alten Bäume",
    exploreNote: "Jede Markierung ist ein Baum, der den Weg lohnt. Finden Sie einen in Ihrer Nähe, oder dort, wo Sie hinfahren.",
    exploreWhatH: "Was auf dieser Karte steht",
    exploreWhatBody: (t, p, c) => `${t} Bäume an ${p} Orten in ${c} Ländern, jeder einzelne an mindestens zwei unabhängigen Quellen geprüft, bevor er auf die Karte kam. Jede Markierung öffnet einen Baum mit seinem Alter, seiner Art, dem Grund, warum es sich lohnt, vor ihm zu stehen, und der Route von Ihrem Standort aus.`,
    exploreWalksH: "Die kürzesten Runden",
    exploreWalksBody: "Eine Karte mit verstreuten Markierungen ist eine Liste. Einen Nachmittag machen Bäume, die nah genug beieinander stehen, um zu Fuß von einem zum nächsten zu gehen, und das sind die Orte, an denen die ganze Reihe in einen Spaziergang passt:",
    exploreIslandsH: "Inseln",
    exploreIslandsBody: "Eine Insel ist ein Tag anderer Art. Die Bäume liegen eine Autofahrt statt eines Spaziergangs auseinander, und für die Strecke bekommen Sie einen Baum, der sonst nirgends wächst: Drachenbäume, Lorbeerwald, der die Eiszeit überdauert hat, Kiefern in Höhen, die das Festland nie erreicht.",
    exploreNotH: "Was nicht darauf steht, und warum",
    exploreNotBody: "Jede Markierung sagt, wie genau sie ist. Ein Baum, der als ungefähr gekennzeichnet ist, heißt: Wir kennen den Park, aber nicht den Stamm. Die Seite schreibt das, statt Sie an eine Stelle zu schicken, an der der Baum nicht steht. Bäume auf Privatgelände bleiben ganz außen vor, ebenso Bäume, deren eigenes Register die Position verbirgt, denn wer sie schützt, hat einen Grund dafür. Das hier ist kein Straßenbaumkataster: Ein Baum bekommt seine Markierung, weil er bemerkenswert ist, nicht weil er existiert.",
    exploreBrowse: "Anders stöbern:",
    homeTitle: "Ancient Trees: bemerkenswerte alte Bäume in Ihrer Nähe",
    homeDescription: "Finden Sie die bemerkenswerten alten Bäume um Sie herum. Jeder geprüft, mit seiner Geschichte, seinem genauen Standort und der Route von Ihnen aus.",
    homeHeroLead: "Bäume, die den Weg lohnen,",
    homeHeroEm: "wo Sie auch sind.",
    homeSub: "Für alle, die gern draußen sind. Finden Sie bemerkenswerte alte Bäume in der Nähe, sehen Sie sich an einem Nachmittag ein paar davon an, lesen Sie die Geschichte hinter jedem und haken Sie die ab, die Sie besuchen.",
    homeFindH: "Die Bäume in Ihrer Nähe, gerade jetzt.",
    homeFindBody: "Die Karte findet die bemerkenswerten alten Bäume, die Ihrem Standort am nächsten stehen, und zeigt Ihnen den nächstgelegenen, mit Gehzeit und Route aufs Telefon.",
    homeWalkH: "Eine Route an den sehenswerten vorbei.",
    homeWalkBody: "Nur die bemerkenswertesten, zu einem Spaziergang verbunden, den Sie an einem Nachmittag schaffen, jeder mit seiner Geschichte und dem Monat, in dem er am schönsten ist, damit Sie wissen, wann Sie hingehen.",
    homeCollectH: "Haken Sie die ab, vor denen Sie gestanden haben.",
    homeCollectBody: "Haken Sie den Baum vor Ort ab und sehen Sie Ihre Sammlung wachsen: Bäume, Städte, Arten. Seltenere und ältere Bäume zählen mehr, und Abzeichen für eine vollständige Stadt kommen bald.",
    homeDirectoryH: "Alte Bäume überall",
    homeMission: "Wir kartieren alle bemerkenswerten Bäume der Welt, und wir können Ihre Hilfe gebrauchen. Wenn Sie einen guten Baum kennen oder eine ganze Stadt kartieren wollen,",
    homeMissionLink: "sagen Sie es uns",
    mapFilterGroup: "Karte filtern",
    mapFilterFav: "Favoriten",
    mapFilterMine: "Meine Bäume",
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
    takeMeThere: "Route planen",
    showOnMap: "Auf der Karte zeigen",
    showPhoto: "Foto zeigen",
    openFullMap: "Ganze Karte öffnen",
    dirTitle: "Route öffnen in",
    noPhotoYet: "Noch kein Foto",
    pinShowUs: "Zeig uns, wo er steht",
    pinTitle: "Wo steht er wirklich?",
    pinHelp: "Verschiebe die Karte, bis die Markierung auf dem Baum sitzt.",
    pinZoom: "Zoome so weit hinein, wie du willst. Der Knopf wird aktiv, sobald du die Markierung verschoben hast.",
    pinMoved: (m) => `Das sind ${m} m von unserer Position entfernt.`,
    pinSend: "Der Baum steht hier",
    pinSending: "Wird gesendet",
    pinDone: "Wir prüfen es und verschieben die Markierung.",
    pinFailed: "Das hat nicht geklappt. Versuch es gleich noch einmal.",
    pinNeedsAccount: "Zum Senden brauchst du ein kostenloses Konto, damit wir dir sagen können, was deine Korrektur geändert hat.",
    cancel: "Abbrechen",
    appleMaps: "Apple Maps",
    goBack: "Zurück",
    chipOldest: "Ältester Baum",
    googleMaps: "Google Maps",
    seenIt: "Diesen habe ich gesehen",
    worthItAsk: (n) => `Ja, ${n} war den Besuch wert`,
    worthItDone: (n) => `Du fandest ${n} sehenswert. Zum Zurücknehmen tippen`,
    seenItDone: "Abgehakt",
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
    noPhotoLicence: "Von diesem Baum hat noch niemand ein Foto unter einer Lizenz veröffentlicht, die wir nutzen dürfen.",
    addPhotoBtn: "Foto hinzufügen",
    addPhotoBtnQuiet: "Eigenes Foto hinzufügen",
    photoCanGoHere: "Wenn du selbst eines aufgenommen hast, kann es hierhin.",
    addPhotoSignIn: "Melde dich zuerst an und wähle dann dein Foto.",
    addPhotoSending: "Wird gesendet...",
    addPhotoBadFile: "Dieses Bild konnte nicht gelesen werden. Versuch ein anderes.",
    addPhotoThanks: "Danke. Wir sehen uns jedes Foto an, bevor es auf einer Seite erscheint, und du erfährst, was aus deinem geworden ist.",
    addPhotoFailed: "Das hat nicht geklappt. Versuch es gleich noch einmal.",
    addPhotoOwnOnly: "Wir können nur Fotos verwenden, die du selbst gemacht hast.",
    addPhotoWaiting: "Dein Foto, wartet auf einen Blick",
    addPhotoOnPage: "Dein Foto ist auf dieser Seite",
    addPhotoSeeMine: "In Meine Bäume ansehen",
    signPhotoLabel: "Steht ein Schild am Baum?",
    signPhotoHint: "Freiwillig. Du kannst auch ein Foto des Schilds hinzufügen. Oft stehen darauf der Name des Baums, die Art und sein Alter.",
    signPhotoBtn: "Foto des Schilds hinzufügen",
    havePhotographed: "Hast du diesen Baum fotografiert?",
    havePhotographedLine: "Wenn dein Foto ihn besser zeigt als das oben, kann es dessen Platz einnehmen oder daneben stehen.",
    goNote: "Der Knopf oben öffnet die Route in Ihrer Karten-App.",
    approxNote: "Die Markierung zeigt ungefähr den richtigen Bereich an, nicht den Baum selbst. Er steht hier, aber wir haben die genaue Position vor Ort noch nicht bestätigt.",
    knowExactly: "Wissen Sie genau, wo er steht?",
    couldUseHelp: "Wir können Ihre Hilfe gebrauchen.",
    researchedRemotely: "Diese Seite ist aus der Ferne recherchiert. Wenn Sie diesen Baum kennen, wissen Sie Dinge, die wir nicht wissen.",
    knowMoreThanUs: "Wissen Sie mehr als wir?",
    ifOlderTree: (c) => `Wenn Sie in ${c} einen älteren Baum kennen oder hier einen Fehler sehen, sagen Sie es uns und wir korrigieren es.`,
    home: "Start",
    backToTrees: (n) => `\u2190 ${n === 1 ? "Der Baum" : `Die ${n} B\u00e4ume`}`,
    treesOnMap: (n) => `${n} ${n === 1 ? "Baum" : "B\u00e4ume"} auf der Karte`,
    heading: (c) => `Alte B\u00e4ume in ${c}`,
    readMore: "Mehr lesen",
    visitedOf: (n, city) => `in ${city} besucht`,
    mappingAll: "Wir kartieren alle bemerkenswerten B\u00e4ume der Welt.",
    missingOrWrong: (city) => `Kennen Sie einen in ${city}, der hier fehlt, oder sehen Sie einen Fehler?`,
    tellUs: "Sagen Sie es uns",
    goingThere: "Sie fahren hin?",
    downloadTrees: (n) => `Die ${n} B\u00e4ume herunterladen`,
    worksOffline: "als Kartendatei und \u00f6ffnen Sie sie in Google Maps, Organic Maps oder einer Wander-App. Funktioniert auch offline.",
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
    appPitchTreeTitle: "Sammle die Bäume, vor denen du gestanden hast",
    appPitchTreeBody: "Diesen abhaken, Spaziergänge an mehreren weiteren vorbei und deine Sammlung, die Stadt für Stadt wächst: das ist die Ancient-Trees-App.",
    appPitchCityTitle: "Lauf sie mit der App ab",
    appPitchCityBody: "Die Spazierrouten, deine gespeicherten Bäume und die Sammlung derer, vor denen du gestanden hast: die Ancient-Trees-App.",
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
    waitlistSent: "Du stehst auf der Liste. Wir schreiben dir, sobald es losgeht.",
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
    homeStatOldest: "a mais velha, anos",
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
    homeShelfMeta: (n, country) => `${n} árvores \u00b7 ${country}`,
    exploreWalkItem: (n, d) => `${n} árvores em ${d}`,
    citiesCrumb: "Cidades",
    citiesTitle: "Todas as cidades do mapa",
    citiesHeading: "Todas as cidades do mapa",
    citiesLead: (c, t) => `${c} cidades, ${t} árvores, cada uma investigada e verificada.`,
    citiesDescription: "Todas as cidades do mapa, por país: as árvores velhas e notáveis de cada uma, verificadas, com a sua história e o sítio exacto.",
    exploreTitle: "Mapa de árvores antigas de todo o mundo",
    exploreDescription: "O mapa interativo de todas as árvores antigas verificadas do site, cada marcador uma árvore diante da qual vale a pena estar.",
    exploreHeading: "O mapa das árvores antigas",
    exploreNote: "Cada marcador é uma árvore que vale a caminhada. Encontre uma perto de si, ou no sítio para onde vai.",
    exploreWhatH: "O que está neste mapa",
    exploreWhatBody: (t, p, c) => `${t} árvores em ${p} lugares de ${c} países, cada uma confirmada em pelo menos duas fontes independentes antes de entrar. Cada marcador abre uma árvore com a idade, a espécie, a razão por que vale a pena estar diante dela e o caminho a partir de onde está.`,
    exploreWalksH: "Os percursos mais curtos",
    exploreWalksBody: "Um mapa de marcadores dispersos é uma lista. O que faz uma tarde são árvores suficientemente perto umas das outras para ir a pé entre elas, por isso estes são os sítios onde o conjunto todo cabe num só passeio:",
    exploreIslandsH: "Ilhas",
    exploreIslandsBody: "Uma ilha é um dia de outro tipo. As árvores ficam a uma viagem de carro e não a um passeio, e o que ganha pela distância é uma árvore que não cresce em mais lado nenhum: dragoeiros, laurissilva que sobreviveu à era glaciar, pinheiros que atingem alturas que o continente nunca dá.",
    exploreNotH: "O que não está, e porquê",
    exploreNotBody: "Cada marcador diz o quão preciso é. Uma árvore marcada como aproximada quer dizer que conhecemos o parque mas não o tronco, e a página di-lo em vez de o mandar para um sítio onde a árvore não está. As árvores em terreno privado ficam de fora por completo, tal como aquelas cujo próprio registo esconde a posição, porque quem as protege tem uma razão. Isto não é um inventário do arvoredo das ruas: uma árvore ganha o seu marcador por ser notável, não por existir.",
    exploreBrowse: "Explore de outra maneira:",
    homeTitle: "Ancient Trees: árvores notáveis perto de si, no mapa",
    homeDescription: "Encontre as árvores antigas à sua volta. Cada uma verificada, com a sua história, o sítio exacto e o caminho a partir de onde está.",
    homeHeroLead: "Árvores que valem a caminhada,",
    homeHeroEm: "esteja onde estiver.",
    homeSub: "Feito para quem gosta de estar lá fora. Encontre árvores notáveis por perto, veja algumas numa tarde, leia a história de cada uma e vá marcando as que visita.",
    homeFindH: "As árvores perto de si, agora.",
    homeFindBody: "O mapa encontra as árvores antigas mais próximas do sítio onde está e aponta-lhe a mais perto, com o tempo a pé e o caminho no telemóvel.",
    homeWalkH: "Um percurso pelas que valem a visita.",
    homeWalkBody: "Só as mais notáveis, ligadas num passeio que faz numa tarde, cada uma com a sua história e o mês em que está no seu melhor, para saber quando ir.",
    homeCollectH: "Marque aquelas diante das quais já esteve.",
    homeCollectBody: "Marque a árvore quando estiver diante dela e veja a sua coleção crescer: árvores, cidades, espécies. As árvores mais raras e mais velhas contam mais, e os distintivos por uma cidade completa estão a caminho.",
    homeDirectoryH: "Árvores antigas em qualquer lado",
    homeMission: "Estamos a mapear todas as árvores notáveis do mundo, e a sua ajuda seria bem-vinda. Se conhece uma boa árvore, ou quer mapear uma cidade inteira,",
    homeMissionLink: "diga-nos",
    mapFilterGroup: "Filtrar o mapa",
    mapFilterFav: "Favoritas",
    mapFilterMine: "As minhas árvores",
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
    takeMeThere: "Como chegar",
    showOnMap: "Ver no mapa",
    showPhoto: "Ver a fotografia",
    openFullMap: "Abrir o mapa completo",
    dirTitle: "Abrir o percurso em",
    noPhotoYet: "Ainda sem fotografia",
    pinShowUs: "Mostre-nos onde está",
    pinTitle: "Onde está realmente?",
    pinHelp: "Arraste o mapa até o marcador ficar sobre a árvore.",
    pinZoom: "Aproxime o quanto quiser. O botão fica ativo quando tiver movido o marcador.",
    pinMoved: (m) => `Fica a ${m} m de onde a temos.`,
    pinSend: "A árvore está aqui",
    pinSending: "A enviar",
    pinDone: "Vamos verificar e mover o marcador.",
    pinFailed: "Não foi possível enviar. Tente de novo daqui a pouco.",
    pinNeedsAccount: "Para enviar precisa de uma conta gratuita, para lhe podermos dizer o que a sua correção mudou.",
    cancel: "Cancelar",
    appleMaps: "Apple Maps",
    goBack: "Voltar",
    chipOldest: "Árvore mais antiga",
    googleMaps: "Google Maps",
    seenIt: "Já vi esta",
    worthItAsk: (n) => `Sim, ${n} valeu a visita`,
    worthItDone: (n) => `Achaste ${n} digna da visita. Toca para desfazer`,
    seenItDone: "Visitada",
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
    noPhotoLicence: "Ninguém publicou uma fotografia desta árvore com uma licença que possamos usar.",
    addPhotoBtn: "Adicionar uma foto",
    addPhotoBtnQuiet: "Adicione a sua própria foto",
    photoCanGoHere: "Se tiver uma tirada por si, pode ficar aqui.",
    addPhotoSignIn: "Inicie sessão primeiro e depois escolha a sua fotografia.",
    addPhotoSending: "A enviar...",
    addPhotoBadFile: "Não foi possível ler essa imagem. Experimente outra.",
    addPhotoThanks: "Obrigado. Vemos cada fotografia antes de ela ser publicada, e saberá o que aconteceu com a sua.",
    addPhotoFailed: "Isso não foi enviado. Tente novamente daqui a pouco.",
    addPhotoOwnOnly: "Só podemos usar fotografias tiradas por si.",
    addPhotoWaiting: "A sua foto, à espera de ser vista",
    addPhotoOnPage: "A sua foto está nesta página",
    addPhotoSeeMine: "Ver em As minhas árvores",
    signPhotoLabel: "Há uma placa junto à árvore?",
    signPhotoHint: "Opcional. Também pode adicionar uma foto da placa. Muitas vezes indica o nome da árvore, a espécie e a idade.",
    signPhotoBtn: "Adicione uma foto da placa",
    havePhotographed: "Fotografou esta árvore?",
    havePhotographedLine: "Se a sua mostrar melhor do que a foto acima, pode ocupar o lugar dela, ou aparecer ao lado.",
    goNote: "O botão acima abre as indicações na sua aplicação de mapas.",
    approxNote: "O marcador aponta a zona certa de forma aproximada, não a árvore exata. Está aqui, mas ainda não confirmámos a posição precisa no terreno.",
    knowExactly: "Sabe exatamente onde está?",
    couldUseHelp: "A sua ajuda seria bem-vinda.",
    researchedRemotely: "Esta página foi investigada à distância. Se conhece esta árvore, sabe coisas que nós não sabemos.",
    knowMoreThanUs: "Sabe mais do que nós?",
    ifOlderTree: (c) => `Se conhece uma árvore mais antiga em ${c}, ou vê aqui um erro, diga-nos e nós corrigimos.`,
    home: "In\u00edcio",
    backToTrees: (n) => `\u2190 ${n === 1 ? "A \u00e1rvore" : `As ${n} \u00e1rvores`}`,
    treesOnMap: (n) => `${n} ${n === 1 ? "\u00e1rvore" : "\u00e1rvores"} no mapa`,
    heading: (c) => `\u00c1rvores hist\u00f3ricas de ${c}`,
    readMore: "Ler mais",
    visitedOf: (n, city) => `visitadas em ${city}`,
    mappingAll: "Estamos a mapear todas as \u00e1rvores not\u00e1veis do mundo.",
    missingOrWrong: (city) => `Conhece alguma em ${city} que nos falte, ou v\u00ea aqui um erro?`,
    tellUs: "Diga-nos",
    goingThere: "Vai l\u00e1?",
    downloadTrees: (n) => `Descarregue as ${n} \u00e1rvores`,
    worksOffline: "como ficheiro de mapa e abra-o no Google Maps, Organic Maps ou em qualquer aplica\u00e7\u00e3o de caminhadas. Funciona sem liga\u00e7\u00e3o.",
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
    appPitchTreeTitle: "Colecione as árvores diante das quais já esteve",
    appPitchTreeBody: "Marcar esta, percursos a pé que passam por várias outras e a sua coleção a crescer cidade a cidade: é isso a aplicação Ancient Trees.",
    appPitchCityTitle: "Percorra-as com a aplicação",
    appPitchCityBody: "Os percursos a pé, as suas árvores guardadas e a coleção daquelas diante das quais já esteve: a aplicação Ancient Trees.",
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
    waitlistSent: "Já está na lista. Escrevemos-lhe no dia em que abrir.",
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
    homeStatOldest: "le plus vieux, ans",
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
    homeShelfMeta: (n, country) => `${n} arbres \u00b7 ${country}`,
    exploreWalkItem: (n, d) => `${n} arbres sur ${d}`,
    citiesCrumb: "Villes",
    citiesTitle: "Toutes les villes de la carte",
    citiesHeading: "Toutes les villes de la carte",
    citiesLead: (c, t) => `${c} villes, ${t} arbres, chacun recherché et vérifié.`,
    citiesDescription: "Toutes les villes de la carte, par pays : les arbres anciens et remarquables de chacune, vérifiés, avec leur histoire et leur emplacement exact.",
    exploreTitle: "Carte des arbres remarquables du monde",
    exploreDescription: "La carte interactive de tous les arbres remarquables vérifiés du site, chaque point un arbre devant lequel il vaut la peine de s'arrêter.",
    exploreHeading: "La carte des arbres remarquables",
    exploreNote: "Chaque point est un arbre qui vaut le déplacement. Trouvez-en un près de vous, ou là où vous allez.",
    exploreWhatH: "Ce qu'il y a sur cette carte",
    exploreWhatBody: (t, p, c) => `${t} arbres dans ${p} lieux répartis sur ${c} pays, chacun recoupé avec au moins deux sources indépendantes avant d'y figurer. Chaque point ouvre un arbre avec son âge, son espèce, la raison pour laquelle il vaut le détour et l'itinéraire depuis l'endroit où vous êtes.`,
    exploreWalksH: "Les parcours les plus courts",
    exploreWalksBody: "Une carte de points éparpillés est une liste. Ce qui fait un après-midi, ce sont des arbres assez proches pour aller de l'un à l'autre à pied, et voici donc les endroits où l'ensemble tient dans une seule promenade :",
    exploreIslandsH: "Îles",
    exploreIslandsBody: "Une île, c'est une journée d'un autre genre. Les arbres sont séparés par une route plutôt que par une promenade, et ce que la distance vous rend, c'est un arbre qui ne pousse nulle part ailleurs : dragonniers, forêt de lauriers qui a survécu à la glaciation, pins qui atteignent des hauteurs que le continent n'atteint jamais.",
    exploreNotH: "Ce qui n'y est pas, et pourquoi",
    exploreNotBody: "Chaque point indique sa précision. Un arbre marqué approximatif veut dire que nous connaissons le parc mais pas le tronc, et la page le dit au lieu de vous envoyer à un endroit où l'arbre n'est pas. Les arbres sur terrain privé sont entièrement laissés de côté, comme ceux dont le registre lui-même cache la position, parce que ceux qui les protègent ont leurs raisons. Ceci n'est pas un inventaire des arbres de rue : un arbre gagne son point parce qu'il est remarquable, pas parce qu'il existe.",
    exploreBrowse: "Parcourir autrement :",
    homeTitle: "Ancient Trees : arbres remarquables près de vous",
    homeDescription: "Trouvez les vieux arbres remarquables autour de vous. Chacun vérifié, avec son histoire, son emplacement exact et l'itinéraire depuis où vous êtes.",
    homeHeroLead: "Des arbres qui valent le détour,",
    homeHeroEm: "où que vous soyez.",
    homeSub: "Fait pour ceux qui aiment être dehors. Trouvez des arbres remarquables à côté, allez en voir quelques-uns en un après-midi, lisez l'histoire de chacun et cochez ceux que vous visitez.",
    homeFindH: "Les arbres près de vous, tout de suite.",
    homeFindBody: "La carte trouve les vieux arbres remarquables les plus proches de l'endroit où vous vous tenez et vous indique le plus proche, avec le temps de marche et l'itinéraire sur votre téléphone.",
    homeWalkH: "Un parcours qui passe par ceux qui comptent.",
    homeWalkBody: "Seulement les plus remarquables, reliés en une promenade que vous faites en un après-midi, chacun avec son histoire et le mois où il est au mieux, pour savoir quand y aller.",
    homeCollectH: "Cochez ceux devant lesquels vous vous êtes tenu.",
    homeCollectBody: "Cochez l'arbre une fois sur place et regardez votre collection grandir : arbres, villes, espèces. Les arbres plus rares et plus vieux comptent davantage, et les badges pour une ville terminée arrivent bientôt.",
    homeDirectoryH: "Des arbres remarquables partout",
    homeMission: "Nous cartographions tous les arbres remarquables du monde, et votre aide nous serait utile. Si vous connaissez un bel arbre, ou si vous voulez cartographier une ville entière,",
    homeMissionLink: "dites-le-nous",
    mapFilterGroup: "Filtrer la carte",
    mapFilterFav: "Favoris",
    mapFilterMine: "Mes arbres",
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
    takeMeThere: "M'y emmener",
    showOnMap: "Voir sur la carte",
    showPhoto: "Voir la photo",
    openFullMap: "Ouvrir la carte complète",
    dirTitle: "Ouvrir l'itinéraire dans",
    noPhotoYet: "Pas encore de photo",
    pinShowUs: "Montrez-nous où il se trouve",
    pinTitle: "Où est-il vraiment ?",
    pinHelp: "Déplacez la carte jusqu'à ce que le repère soit sur l'arbre.",
    pinZoom: "Zoomez autant que vous voulez. Le bouton s'active dès que vous avez déplacé le repère.",
    pinMoved: (m) => `C'est à ${m} m de notre position.`,
    pinSend: "L'arbre est ici",
    pinSending: "Envoi en cours",
    pinDone: "Nous allons vérifier et déplacer le repère.",
    pinFailed: "L'envoi n'a pas abouti. Réessayez dans un instant.",
    pinNeedsAccount: "L'envoi demande un compte gratuit, pour que nous puissions vous dire ce que votre correction a changé.",
    cancel: "Annuler",
    appleMaps: "Apple Maps",
    goBack: "Retour",
    chipOldest: "Arbre le plus vieux",
    googleMaps: "Google Maps",
    seenIt: "Je l'ai déjà vu",
    worthItAsk: (n) => `Oui, ${n} valait le détour`,
    worthItDone: (n) => `Vous avez trouvé ${n} digne du détour. Touchez pour annuler`,
    seenItDone: "Vu",
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
    noPhotoLicence: "Personne n'a publié de photographie de cet arbre sous une licence que nous pouvons utiliser.",
    addPhotoBtn: "Ajouter une photo",
    addPhotoBtnQuiet: "Ajoutez votre propre photo",
    photoCanGoHere: "Si vous en avez une prise par vous-même, elle peut aller ici.",
    addPhotoSignIn: "Connectez-vous d'abord, puis choisissez votre photo.",
    addPhotoSending: "Envoi en cours...",
    addPhotoBadFile: "Cette image n'a pas pu être lue. Essayez-en une autre.",
    addPhotoThanks: "Merci. Nous regardons chaque photo avant qu'elle ne soit publiée, et vous saurez ce qu'il est advenu de la vôtre.",
    addPhotoFailed: "Cela n'a pas fonctionné. Réessayez dans un instant.",
    addPhotoOwnOnly: "Nous ne pouvons utiliser que des photos que vous avez prises vous-même.",
    addPhotoWaiting: "Votre photo, en attente d'un regard",
    addPhotoOnPage: "Votre photo est sur cette page",
    addPhotoSeeMine: "La voir dans Mes arbres",
    signPhotoLabel: "Y a-t-il un panneau près de l'arbre ?",
    signPhotoHint: "Facultatif. Vous pouvez aussi ajouter une photo du panneau. Il indique souvent le nom de l'arbre, l'espèce et son âge.",
    signPhotoBtn: "Ajoutez une photo du panneau",
    havePhotographed: "Avez-vous photographié cet arbre ?",
    havePhotographedLine: "Si la vôtre le montre mieux que la photo ci-dessus, elle peut prendre sa place, ou apparaître à côté.",
    goNote: "Le bouton ci-dessus ouvre l'itinéraire dans votre application de cartes.",
    approxNote: "Le repère indique approximativement la bonne zone, pas l'arbre exact. Il est bien ici, mais nous n'avons pas encore confirmé la position précise sur le terrain.",
    knowExactly: "Vous savez exactement où il se trouve ?",
    couldUseHelp: "Votre aide nous serait utile.",
    researchedRemotely: "Cette page a été documentée à distance. Si vous connaissez cet arbre, vous savez des choses que nous ignorons.",
    knowMoreThanUs: "Vous en savez plus que nous ?",
    ifOlderTree: (c) => `Si vous connaissez un arbre plus vieux à ${c}, ou si vous voyez une erreur ici, dites-le-nous et nous corrigeons.`,
    home: "Accueil",
    backToTrees: (n) => `\u2190 ${n === 1 ? "L\u2019arbre" : `Les ${n} arbres`}`,
    treesOnMap: (n) => `${n} ${n === 1 ? "arbre" : "arbres"} sur la carte`,
    heading: (c) => `Arbres remarquables de ${c}`,
    readMore: "Lire la suite",
    visitedOf: (n, city) => `visit\u00e9s \u00e0 ${city}`,
    mappingAll: "Nous cartographions tous les arbres remarquables du monde.",
    missingOrWrong: (city) => `Vous en connaissez un \u00e0 ${city} qui manque ici, ou vous voyez une erreur ?`,
    tellUs: "Dites-le-nous",
    goingThere: "Vous y allez ?",
    downloadTrees: (n) => `T\u00e9l\u00e9charger les ${n} arbres`,
    worksOffline: "comme fichier de carte et ouvrez-le dans Google Maps, Organic Maps ou n'importe quelle application de randonn\u00e9e. Fonctionne hors ligne.",
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
    appPitchTreeTitle: "Collectionnez les arbres devant lesquels vous vous êtes tenu",
    appPitchTreeBody: "Cocher celui-ci, des marches qui en longent plusieurs autres, et votre collection qui grandit ville après ville : voilà l'application Ancient Trees.",
    appPitchCityTitle: "Parcourez-les avec l'application",
    appPitchCityBody: "Les itinéraires à pied, vos arbres enregistrés et la collection de ceux devant lesquels vous vous êtes tenu : l'application Ancient Trees.",
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
    waitlistSent: "Vous êtes sur la liste. Nous vous écrirons le jour de l'ouverture.",
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
    homeStatOldest: "最古、年",
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
    homeShelfMeta: (n, country) => `${n}本 \u00b7 ${country}`,
    exploreWalkItem: (n, d) => `${n}本、${d}以内`,
    citiesCrumb: "都市一覧",
    citiesTitle: "地図に載せたすべての都市",
    citiesHeading: "地図に載せたすべての都市",
    citiesLead: (c, t) => `${c}都市、${t}本。いずれも調べ、裏づけを取っています。`,
    citiesDescription: "地図に載せたすべての都市を国別に。各都市の古木と名木を、裏づけを取ったうえで、その由来と正確な場所とともに紹介します。",
    exploreTitle: "古木の地図：見に行く価値のある木を一枚の地図に",
    exploreDescription: "裏づけを取った古木と名木をすべて載せた地図です。ピンの一つひとつが、足を運んで見上げる価値のある木です。",
    exploreHeading: "古木の地図",
    exploreNote: "どのピンも、歩いて見に行く価値のある木です。近くの一本も、これから行く街の一本も探せます。",
    exploreWhatH: "この地図に載っているもの",
    exploreWhatBody: (t, p, c) => `${c}か国${p}か所の${t}本。どれも載せる前に、独立した二つ以上の資料で確認しています。ピンを開くと、その木の樹齢、樹種、見に行く価値のある理由、そして現在地からの行き方が出ます。`,
    exploreWalksH: "まとめて歩ける場所",
    exploreWalksBody: "ピンが散らばった地図は、ただの一覧です。午後の散歩になるのは、木と木が歩いて回れる距離にあるとき。全部を一度の散歩で回れるのは、次の場所です：",
    exploreIslandsH: "島",
    exploreIslandsBody: "島は、また別の一日です。木と木のあいだは歩きではなく車の距離になりますが、その分、ほかでは育たない木に会えます。竜血樹、氷河期を生き延びた照葉樹の森、本土では届かない高さまで伸びる松。",
    exploreNotH: "載せていないもの、その理由",
    exploreNotBody: "ピンにはどのくらい正確かを書いています。「おおよそ」の木は、公園までは分かっていて幹までは特定できていないという意味で、木のない場所へ送る代わりに、そう書いています。私有地の木は載せません。登録簿そのものが位置を伏せている木も同じで、守っている人たちには理由があります。ここは街路樹の全数調査ではありません。ピンがつくのは、その木が特別だからで、存在するからではありません。",
    exploreBrowse: "別の探し方：",
    homeTitle: "Ancient Trees：近くの古木と名木を地図で",
    homeDescription: "身のまわりにある古木と名木を探せます。どれも裏づけを取り、由来、正確な場所、いまいる場所からの行き方をつけています。",
    homeHeroLead: "どこにいても、",
    homeHeroEm: "歩いて会いに行く価値のある木を。",
    homeSub: "外を歩くのが好きな人のためにつくりました。近くの古木や名木を見つけ、午後のうちに何本かを回り、それぞれの由来を読み、訪れた木をチェックしていけます。",
    homeFindH: "いまいる場所のすぐ近くの木。",
    homeFindBody: "地図が、いま立っている場所にいちばん近い古木や名木を探して、最寄りの一本を示します。徒歩の所要時間と、そこまでの道順が手元に出ます。",
    homeWalkH: "見る価値のある木をつないだ道。",
    homeWalkBody: "選び抜いた木だけを、午後のうちに歩ける一本の散歩道につないでいます。それぞれに由来と、いちばん見ごろになる月をつけているので、行く時期も決められます。",
    homeCollectH: "前に立った木をチェックする。",
    homeCollectBody: "木の前に立ったらチェックを入れて、集まっていくのを眺めてください。木、街、樹種。珍しい木や古い木ほど重く数え、街を一つ回りきったときのバッジも近く出ます。",
    homeDirectoryH: "世界中の古木",
    homeMission: "世界中の名木を地図にしていきます。力を貸してもらえると助かります。いい木を知っている方、街ごと地図にしたい方は、",
    homeMissionLink: "お知らせください",
    mapFilterGroup: "地図をしぼり込む",
    mapFilterFav: "お気に入り",
    mapFilterMine: "訪れた木",
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
    pinNeedsAccount: "送信には無料アカウントが必要です。修正で何が変わったかをお知らせするためです。",
    cancel: "キャンセル",
    appleMaps: "Apple マップ",
    goBack: "戻る",
    chipOldest: "最古の木",
    googleMaps: "Google マップ",
    seenIt: "この木は見ました",
    worthItAsk: (n) => `はい、${n}は行く価値がありました`,
    worthItDone: (n) => `${n}を「行く価値あり」としました。タップで取り消し`,
    seenItDone: "訪問済み",
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
    noPhotoLicence: "この木の写真で、私たちが使える許諾のものはまだ公開されていない。",
    addPhotoBtn: "写真を追加",
    addPhotoBtnQuiet: "自分の写真を追加",
    photoCanGoHere: "ご自身で撮った写真があれば、ここに載せられます。",
    addPhotoSignIn: "先にサインインしてから、写真を選んでください。",
    addPhotoSending: "送信中...",
    addPhotoBadFile: "その画像を読み込めませんでした。別の画像でお試しください。",
    addPhotoThanks: "ありがとうございます。掲載前にすべての写真を確認し、その後どうなったかをお知らせします。",
    addPhotoFailed: "送信できませんでした。少し経ってからもう一度お試しください。",
    addPhotoOwnOnly: "使えるのは、ご自身で撮った写真だけです。",
    addPhotoWaiting: "あなたの写真は確認待ちです",
    addPhotoOnPage: "あなたの写真はこのページに掲載されています",
    addPhotoSeeMine: "アカウントで見る",
    signPhotoLabel: "木のそばに案内板はありますか?",
    signPhotoHint: "任意です。案内板の写真も追加できます。木の名前、樹種、樹齢が書かれていることがよくあります。",
    signPhotoBtn: "案内板の写真を追加",
    havePhotographed: "この木を撮影しましたか?",
    havePhotographedLine: "上の写真より良く撮れていれば、それに差し替えるか、並べて掲載します。",
    goNote: "上のボタンで、地図アプリの経路案内が開く。",
    approxNote: "この目印が示すのは、木そのものではなく、おおよその場所である。木はこの一帯にあるが、正確な位置はまだ現地で確認していない。",
    knowExactly: "正確な場所を知っているか。",
    couldUseHelp: "力を貸してほしい。",
    researchedRemotely: "このページは現地に行かずに調べたものである。この木を知っているなら、私たちの知らないことを知っている。",
    knowMoreThanUs: "私たちより詳しいか。",
    ifOlderTree: (c) => `${c}にもっと古い木があるなら、あるいはここに誤りがあるなら、教えてくれれば直す。`,
    home: "\u30db\u30fc\u30e0",
    backToTrees: (n) => `\u2190 ${n}\u672c\u306e\u6a39\u6728`,
    treesOnMap: (n) => `\u5730\u56f3\u4e0a\u306e${n}\u672c`,
    heading: (c) => `${c}\u306e\u53e4\u6a39`,
    readMore: "\u7d9a\u304d\u3092\u8aad\u3080",
    visitedOf: (n, city) => `${city}\u3067\u8a2a\u308c\u305f\u6570`,
    mappingAll: "\u4e16\u754c\u4e2d\u306e\u9280\u91cd\u306a\u6a39\u6728\u3092\u5730\u56f3\u306b\u3057\u3066\u3044\u307e\u3059\u3002",
    missingOrWrong: (city) => `${city}\u3067\u629c\u3051\u3066\u3044\u308b\u6a39\u6728\u3092\u3054\u5b58\u3058\u3067\u3059\u304b\u3001\u307e\u305f\u306f\u8aa4\u308a\u3092\u898b\u3064\u3051\u307e\u3057\u305f\u304b\u3002`,
    tellUs: "\u304a\u77e5\u3089\u305b\u304f\u3060\u3055\u3044",
    goingThere: "\u884c\u304d\u307e\u3059\u304b\u3002",
    downloadTrees: (n) => `${n}\u672c\u5206\u3092\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9`,
    worksOffline: "\u5730\u56f3\u30d5\u30a1\u30a4\u30eb\u3068\u3057\u3066\u3001Google Maps\u3084Organic Maps\u306a\u3069\u3067\u958b\u3051\u307e\u3059\u3002\u30aa\u30d5\u30e9\u30a4\u30f3\u3067\u3082\u4f7f\u3048\u307e\u3059\u3002",
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
    appPitchTreeBody: "この木にチェックを入れ、ほかの何本かを巡る散歩をして、街ごとにコレクションが増えていく。それがAncient Treesのアプリです。",
    appPitchCityTitle: "アプリを持って歩く",
    appPitchCityBody: "散歩コース、保存した木、そして実際に訪れた木のコレクション。Ancient Treesのアプリです。",
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
    waitlistSent: "リストに登録されました。公開日にお知らせします。",
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
    // A TREE page exists only where the city is genuinely translated, since
    // 2026-09-17 dropped the 21,042 fallback ones. City and question pages
    // still render as fallbacks, so those keep all seven. Offering a language
    // whose page was just deleted is how the picker produced 48,629 dead
    // links, and it is the third time in a day that removing pages left the
    // links behind: the pages are the easy half.
    const isTree = !!leafSeg && leafSeg !== "oldest-tree";
    const usable = isTree ? languagesForCity(slug) : langs;
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
    variants[l] = kind === "question"
      ? `/${l}/${slug}/${QUESTION_SLUG[l] ?? "oldest-tree"}`
      : treeSlug ? `/${l}/${slug}/${treeSlug}` : `/${l}/${slug}`;
  }
  return Object.keys(variants).length ? hreflangSet(enPath, variants) : "";
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

/** An untranslated city, dressed in the reader's language.
 *
 * Hidde's call, 2026-09-17: follow the convention. AllTrails serves every trail
 * under /es/ and komoot every tour under /de-de/, with the frame in the
 * reader's language and the content in whatever language it was written in.
 * We had the opposite, translated leaf pages inside an English site, and a
 * reader who landed on /es/cadiz had 19 of 27 links back into English.
 *
 * So this builds a CityTranslation out of the ENGLISH city file. Nothing is
 * translated and nothing is invented: the frame, the navigation, the labels
 * and the buttons come from ui(lang), and the words about the tree stay as
 * they were written. The page carries rel=canonical to the English URL, which
 * is Google's documented answer for the same language on a second URL, and it
 * stays out of the sitemap. It exists to be navigated to, not to rank.
 *
 * The title is deliberately the plain pattern rather than the English page's
 * generated one. That generator lives in [city].astro and weighs an age hook
 * against a count against a length budget; porting it here would be the same
 * rule written twice, for a page that is canonicalised away and never
 * competes. A short honest title is all this page owes anybody.
 */
export function fallbackCityTranslation(city: any): CityTranslation {
  const d = city.data;
  const trees: Record<string, TreeTranslation> = {};
  for (const t of d.trees ?? []) {
    trees[t.id] = {
      name: t.name ?? "",
      species: t.species ?? "",
      age_estimate: t.age_estimate ?? "",
      access: t.access ?? "",
      transport: t.transport ?? "",
      story: t.story ?? "",
    };
  }
  return {
    city: d.city,
    title: `Ancient Trees in ${d.city}`,
    meta_description: d.meta_description ?? "",
    intro: d.intro ?? "",
    // A long park name (Great Smoky Mountains National Park, 36 chars) can
    // push the full phrase past TITLE_MAX with nothing here to shorten it,
    // unlike the English page's own fitTitle chain. Same shorter fallback.
    question_title: fitTitle([`What is the oldest tree in ${d.city}?`, `Oldest tree in ${d.city}`]),
    question_meta: d.question_meta ?? "",
    question_answer: d.question_answer ?? "",
    question_context: d.question_context ?? "",
    faq: Array.isArray(d.faq) ? d.faq : [],
    trees,
  };
}

/** Every city in this language: the real overlays, then the rest as fallbacks.
 * The `fallback` flag is what the page reads to decide its canonical. */
export async function allCityPathsFor(lang: string, allCities: CityLike[]) {
  const real = await translatedCityPaths(lang, allCities);
  const done = new Set(real.map((r: any) => r.params.city));
  const rest = allCities
    .filter((c) => !done.has(c.id))
    .map((city) => ({
      params: { city: city.id },
      props: { city, tr: fallbackCityTranslation(city), fallback: true },
    }));
  return [...real.map((r: any) => ({ ...r, props: { ...r.props, fallback: false } })), ...rest];
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

/** Every question page in this language, real then fallback. */
export async function allQuestionPathsFor(lang: string, allCities: any[], renderableTrees: any) {
  const real = await translatedQuestionPaths(lang, allCities, renderableTrees);
  const done = new Set(real.map((r: any) => r.params.city));
  // main added cityHasQuestionPage while this branch was open: a city only
  // earns a question page once it has enough trees to answer one. The fallback
  // half has to honour it too, or an untranslated city would get a question
  // page its English twin does not have.
  const rest = allCities
    .filter((c) => !done.has(c.id))
    .filter((c) => cityHasQuestionPage(renderableTrees(c).length))
    .map((city) => ({ params: { city: city.id }, props: { city, tr: fallbackCityTranslation(city), fallback: true } }));
  return [...real.map((r: any) => ({ ...r, props: { ...r.props, fallback: false } })), ...rest];
}


interface CityLike { id: string; data: any }

/** getStaticPaths for a language's tree pages. The 150-250 word bar applies in
 * every language, so it is enforced here rather than trusted. */
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
