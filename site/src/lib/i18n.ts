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
  oldestQuestion: (city: string) => string;
  fullAnswer: string;
  suggestTree: string;
  sendIt: string;
  walkRoutes: string;
  inTheApp: string;
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
  metaLead: (species: string, age: string, where: string) => string;
  /** The short editorial tag beside a tree's name on a card. Keyed by the
   *  English value in data/cities, because that is what the canonical file
   *  holds; an unlisted label falls back to the English rather than
   *  disappearing, which is what it did before this existed. */
  treeLabels: Record<string, string>;
  labelSpecies: string;
  labelAge: string;
  labelLocation: string;
  labelAccess: string;
  labelGettingThere: string;
  factAge: string;
  factPin: string;
  pinExact: string;
  pinApproximate: string;
  discoverMore: string;
  sourcesHeading: string;
  sourcesLine: string;
  takeMeThere: string;
  nearbyTrees: string;
  somethingWrong: string;
  suggestAnother: string;
  actions: string;
  sendYours: string;
  willAppear: string;
  unknownAge: string;
  approxLocationChip: string;
  noPhotoLicence: string;
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
  oldestQuestion: (city) => `What is the oldest tree in ${city}?`,
  fullAnswer: "The full answer, with a map and how to get there.",
  suggestTree: "Know a tree that belongs on this list?",
  sendIt: "Send it to us",
  walkRoutes: "Walking routes",
  inTheApp: "in the app",
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
  metaLead: (sp, age, where) => {
    const vowel = age ? /^(8|11|18|8\d)$/.test(age) : /^[AEIOU]/.test(sp);
    const a = vowel ? "An" : "A";
    const head = age && sp ? `${a} ${age}-year-old ${sp}` : sp ? `${a} ${sp}`
      : age ? `${a} ${age}-year-old tree` : "A remarkable tree";
    return `${head} in ${where}.`;
  },
  labelSpecies: "Species",
  labelAge: "Age estimate",
  labelLocation: "Location",
  labelAccess: "Access",
  labelGettingThere: "Getting there",
  factAge: "Age",
  factPin: "Pin",
  pinExact: "Exact",
  pinApproximate: "Approximate",
  discoverMore: "Discover more",
  sourcesHeading: "Sources",
  sourcesLine: "Where the facts on this page come from.",
  takeMeThere: "Take me there",
  nearbyTrees: "Nearby trees",
  somethingWrong: "Something here is wrong",
  suggestAnother: "Suggest another tree",
  actions: "Actions",
  sendYours: "Send us yours",
  willAppear: "and it will appear on this page.",
  unknownAge: "age unknown",
  approxLocationChip: "pin approximate",
  noPhotoLicence: "Nobody has published a photograph of this tree under a licence we can use.",
  goNote: "The button above opens directions in your maps app.",
  approxNote: "The pin marks the right spot roughly, not the tree itself. It stands here, but we have not confirmed the precise position on the ground yet.",
  knowExactly: "Know exactly where it is?",
  couldUseHelp: "We could use your help.",
  researchedRemotely: "This page was researched from a distance. If you know this tree, you know things we do not.",
  knowMoreThanUs: "Do you know more than we do?",
  ifOlderTree: (c) => `If you know an older tree in ${c}, or see a mistake here, tell us and we correct it.`,
};

const TABLE: Record<string, Partial<UIStrings>> = {
  es: {
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
    metaLead: (sp, age, where) => sp && age ? `${sp} de unos ${age} años en ${where}.`
      : sp ? `${sp} en ${where}.` : age ? `Árbol de unos ${age} años en ${where}.` : `Árbol singular en ${where}.`,
    distanceAway: (d) => `a ${d}`,
    labelSpecies: "Especie",
    labelAge: "Edad estimada",
    labelLocation: "Ubicación",
    labelAccess: "Acceso",
    labelGettingThere: "Cómo llegar",
    factAge: "Edad",
    factPin: "Ubicación",
    pinExact: "Exacta",
    pinApproximate: "Aproximada",
    discoverMore: "Descubre más",
    sourcesHeading: "Fuentes",
    sourcesLine: "De dónde salen los datos de esta página.",
    takeMeThere: "Cómo llegar",
    nearbyTrees: "Árboles cercanos",
    somethingWrong: "Aquí hay algo mal",
    suggestAnother: "Sugerir otro árbol",
    actions: "Acciones",
    sendYours: "Envíanos la tuya",
    willAppear: "y aparecerá en esta página.",
    unknownAge: "edad desconocida",
    approxLocationChip: "ubicación aproximada",
    noPhotoLicence: "Nadie ha publicado una fotografía de este árbol con una licencia que podamos usar.",
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
    oldestQuestion: (city) => `\u00bfCu\u00e1l es el \u00e1rbol m\u00e1s antiguo de ${city}?`,
    fullAnswer: "La respuesta completa, con mapa y c\u00f3mo llegar.",
    suggestTree: "\u00bfConoces un \u00e1rbol que merezca estar en esta lista?",
    sendIt: "Env\u00edanoslo",
    walkRoutes: "Rutas a pie",
    inTheApp: "en la aplicaci\u00f3n",
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
    metaLead: (sp, age, where) => sp && age ? `${sp} di circa ${age} anni a ${where}.`
      : sp ? `${sp} a ${where}.` : age ? `Albero di circa ${age} anni a ${where}.` : `Albero monumentale a ${where}.`,
    distanceAway: (d) => `a ${d}`,
    labelSpecies: "Specie",
    labelAge: "Età stimata",
    labelLocation: "Posizione",
    labelAccess: "Accesso",
    labelGettingThere: "Come arrivarci",
    factAge: "Età",
    factPin: "Posizione",
    pinExact: "Esatta",
    pinApproximate: "Approssimativa",
    discoverMore: "Scopri di più",
    sourcesHeading: "Fonti",
    sourcesLine: "Da dove vengono i dati di questa pagina.",
    takeMeThere: "Portami lì",
    nearbyTrees: "Alberi nei dintorni",
    somethingWrong: "Qui c'è un errore",
    suggestAnother: "Segnala un altro albero",
    actions: "Azioni",
    sendYours: "Mandacela",
    willAppear: "e comparirà su questa pagina.",
    unknownAge: "età sconosciuta",
    approxLocationChip: "posizione approssimativa",
    noPhotoLicence: "Nessuno ha pubblicato una fotografia di questo albero con una licenza che possiamo usare.",
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
    oldestQuestion: (city) => `Qual \u00e8 l'albero pi\u00f9 antico di ${city}?`,
    fullAnswer: "La risposta completa, con mappa e indicazioni.",
    suggestTree: "Conosci un albero che merita di stare in questo elenco?",
    sendIt: "Inviacelo",
    walkRoutes: "Percorsi a piedi",
    inTheApp: "nell'app",
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
    metaLead: (sp, age, where) => sp && age ? `${sp} van ongeveer ${age} jaar in ${where}.`
      : sp ? `${sp} in ${where}.` : age ? `Boom van ongeveer ${age} jaar in ${where}.` : `Monumentale boom in ${where}.`,
    distanceAway: (d) => `${d} verderop`,
    labelSpecies: "Soort",
    labelAge: "Geschatte leeftijd",
    labelLocation: "Locatie",
    labelAccess: "Toegang",
    labelGettingThere: "Ernaartoe",
    factAge: "Leeftijd",
    factPin: "Locatie",
    pinExact: "Exact",
    pinApproximate: "Bij benadering",
    discoverMore: "Ontdek meer",
    sourcesHeading: "Bronnen",
    sourcesLine: "Waar de gegevens op deze pagina vandaan komen.",
    takeMeThere: "Breng me erheen",
    nearbyTrees: "Bomen in de buurt",
    somethingWrong: "Hier klopt iets niet",
    suggestAnother: "Nog een boom aandragen",
    actions: "Acties",
    sendYours: "Stuur hem op",
    willAppear: "en hij komt op deze pagina.",
    unknownAge: "leeftijd onbekend",
    approxLocationChip: "locatie bij benadering",
    noPhotoLicence: "Niemand heeft een foto van deze boom gepubliceerd met een licentie die wij mogen gebruiken.",
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
    oldestQuestion: (city) => `Wat is de oudste boom van ${city}?`,
    fullAnswer: "Het volledige antwoord, met kaart en route.",
    suggestTree: "Ken je een boom die in deze lijst thuishoort?",
    sendIt: "Stuur hem naar ons",
    walkRoutes: "Wandelroutes",
    inTheApp: "in de app",
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
    metaLead: (sp, age, where) => sp && age ? `${sp}, rund ${age} Jahre alt, in ${where}.`
      : sp ? `${sp} in ${where}.` : age ? `Baum, rund ${age} Jahre alt, in ${where}.` : `Bemerkenswerter Baum in ${where}.`,
    distanceAway: (d) => `${d} entfernt`,
    labelSpecies: "Art",
    labelAge: "Geschätztes Alter",
    labelLocation: "Standort",
    labelAccess: "Zugang",
    labelGettingThere: "Anfahrt",
    factAge: "Alter",
    factPin: "Standort",
    pinExact: "Genau",
    pinApproximate: "Ungefähr",
    discoverMore: "Mehr entdecken",
    sourcesHeading: "Quellen",
    sourcesLine: "Woher die Angaben auf dieser Seite stammen.",
    takeMeThere: "Route planen",
    nearbyTrees: "Bäume in der Nähe",
    somethingWrong: "Hier stimmt etwas nicht",
    suggestAnother: "Noch einen Baum vorschlagen",
    actions: "Aktionen",
    sendYours: "Schick sie uns",
    willAppear: "und sie erscheint auf dieser Seite.",
    unknownAge: "Alter unbekannt",
    approxLocationChip: "Standort ungefähr",
    noPhotoLicence: "Von diesem Baum hat noch niemand ein Foto unter einer Lizenz veröffentlicht, die wir nutzen dürfen.",
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
    oldestQuestion: (city) => `Welcher ist der \u00e4lteste Baum in ${city}?`,
    fullAnswer: "Die vollst\u00e4ndige Antwort, mit Karte und Anfahrt.",
    suggestTree: "Kennen Sie einen Baum, der auf diese Liste geh\u00f6rt?",
    sendIt: "Schicken Sie ihn uns",
    walkRoutes: "Wanderrouten",
    inTheApp: "in der App",
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
    metaLead: (sp, age, where) => sp && age ? `${sp} com cerca de ${age} anos em ${where}.`
      : sp ? `${sp} em ${where}.` : age ? `Árvore com cerca de ${age} anos em ${where}.` : `Árvore notável em ${where}.`,
    distanceAway: (d) => `a ${d}`,
    labelSpecies: "Espécie",
    labelAge: "Idade estimada",
    labelLocation: "Localização",
    labelAccess: "Acesso",
    labelGettingThere: "Como chegar",
    factAge: "Idade",
    factPin: "Localização",
    pinExact: "Exacta",
    pinApproximate: "Aproximada",
    discoverMore: "Descobrir mais",
    sourcesHeading: "Fontes",
    sourcesLine: "De onde vêm os dados desta página.",
    takeMeThere: "Como chegar",
    nearbyTrees: "Árvores por perto",
    somethingWrong: "Há aqui um erro",
    suggestAnother: "Sugerir outra árvore",
    actions: "Ações",
    sendYours: "Envie-nos a sua",
    willAppear: "e aparecerá nesta página.",
    unknownAge: "idade desconhecida",
    approxLocationChip: "localização aproximada",
    noPhotoLicence: "Ninguém publicou uma fotografia desta árvore com uma licença que possamos usar.",
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
    oldestQuestion: (city) => `Qual \u00e9 a \u00e1rvore mais antiga de ${city}?`,
    fullAnswer: "A resposta completa, com mapa e como chegar.",
    suggestTree: "Conhece uma \u00e1rvore que mere\u00e7a estar nesta lista?",
    sendIt: "Envie-nos",
    walkRoutes: "Percursos a p\u00e9",
    inTheApp: "na aplica\u00e7\u00e3o",
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
    metaLead: (sp, age, where) => sp && age ? `${sp} d'environ ${age} ans à ${where}.`
      : sp ? `${sp} à ${where}.` : age ? `Arbre d'environ ${age} ans à ${where}.` : `Arbre remarquable à ${where}.`,
    distanceAway: (d) => `\u00e0 ${d}`,
    labelSpecies: "Espèce",
    labelAge: "Âge estimé",
    labelLocation: "Emplacement",
    labelAccess: "Accès",
    labelGettingThere: "Y aller",
    factAge: "Âge",
    factPin: "Position",
    pinExact: "Exacte",
    pinApproximate: "Approximative",
    discoverMore: "Découvrir plus",
    sourcesHeading: "Sources",
    sourcesLine: "D’où viennent les informations de cette page.",
    takeMeThere: "M'y emmener",
    nearbyTrees: "Arbres à proximité",
    somethingWrong: "Il y a une erreur ici",
    suggestAnother: "Proposer un autre arbre",
    actions: "Actions",
    sendYours: "Envoyez-nous la vôtre",
    willAppear: "et elle apparaîtra sur cette page.",
    unknownAge: "âge inconnu",
    approxLocationChip: "position approximative",
    noPhotoLicence: "Personne n'a publié de photographie de cet arbre sous une licence que nous pouvons utiliser.",
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
    oldestQuestion: (city) => `Quel est l'arbre le plus vieux de ${city} ?`,
    fullAnswer: "La r\u00e9ponse compl\u00e8te, avec une carte et l'acc\u00e8s.",
    suggestTree: "Vous connaissez un arbre qui a sa place dans cette liste ?",
    sendIt: "Envoyez-le-nous",
    walkRoutes: "Itin\u00e9raires \u00e0 pied",
    inTheApp: "dans l'application",
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
    metaLead: (sp, age, where) => sp && age ? `${where}にある樹齢約${age}年の${sp}。`
      : sp ? `${where}にある${sp}。` : age ? `${where}にある樹齢約${age}年の木。` : `${where}にある巨木。`,
    distanceAway: (d) => `${d}\u5148`,
    labelSpecies: "樹種",
    labelAge: "推定樹齢",
    labelLocation: "場所",
    labelAccess: "見学",
    labelGettingThere: "行き方",
    factAge: "樹齢",
    factPin: "位置",
    pinExact: "正確",
    pinApproximate: "おおよそ",
    discoverMore: "もっと見る",
    sourcesHeading: "出典",
    sourcesLine: "このページの情報の出どころ。",
    takeMeThere: "ここへ行く",
    nearbyTrees: "近くの木",
    somethingWrong: "ここに誤りがある",
    suggestAnother: "別の木を教える",
    actions: "操作",
    sendYours: "写真を送る",
    willAppear: "と、このページに載る。",
    unknownAge: "樹齢不明",
    approxLocationChip: "位置は目安",
    noPhotoLicence: "この木の写真で、私たちが使える許諾のものはまだ公開されていない。",
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
    oldestQuestion: (city) => `${city}\u3067\u6700\u3082\u53e4\u3044\u6a39\u6728\u306f\u3069\u308c\u3067\u3059\u304b\u3002`,
    fullAnswer: "\u5730\u56f3\u3068\u884c\u304d\u65b9\u3092\u542b\u3080\u5b8c\u5168\u306a\u56de\u7b54\u3067\u3059\u3002",
    suggestTree: "\u3053\u306e\u30ea\u30b9\u30c8\u306b\u5165\u308b\u3079\u304d\u6a39\u6728\u3092\u3054\u5b58\u3058\u3067\u3059\u304b\u3002",
    sendIt: "\u304a\u9001\u308a\u304f\u3060\u3055\u3044",
    walkRoutes: "\u5f92\u6b69\u30eb\u30fc\u30c8",
    inTheApp: "\u30a2\u30d7\u30ea\u3067",
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

interface CityLike { id: string; data: { trees?: { id: string }[] } }

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

/** getStaticPaths for a language's question pages. */
export async function translatedQuestionPaths(lang: string, allCities: any[]) {
  return translatedCities(lang).map((slug) => {
    const city = allCities.find((c) => c.id === slug);
    if (!city) throw new Error(`data/i18n/${lang}/${slug}.json has no matching English city file`);
    return { params: { city: slug }, props: { city, tr: cityTranslation(lang, slug)! } };
  });
}
