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
  saveOrTransfer: string;
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
  withWalkingRoute: string;
}

const EN: UIStrings = {
  home: "Home",
  backToTrees: (n) => `\u2190 The ${n} trees`,
  treesOnMap: (n) => `${n} trees on the map`,
  heading: (c) => `Ancient Trees in ${c}`,
  readMore: "Read more",
  visitedOf: (n, city) => `visited in ${city}`,
  saveOrTransfer: "Save or move to another device",
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
  withWalkingRoute: ", with a walking route that passes several of them.",
};

const TABLE: Record<string, Partial<UIStrings>> = {
  es: {
    home: "Inicio",
    backToTrees: (n) => `\u2190 Los ${n} \u00e1rboles`,
    treesOnMap: (n) => `${n} \u00e1rboles en el mapa`,
    heading: (c) => `\u00c1rboles hist\u00f3ricos de ${c}`,
    readMore: "Leer m\u00e1s",
    visitedOf: (n, city) => `visitados en ${city}`,
    saveOrTransfer: "Guardar o pasar a otro dispositivo",
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
    withWalkingRoute: ", con un recorrido a pie que pasa por varios de ellos.",
  },
  it: {
    home: "Home",
    backToTrees: (n) => `\u2190 I ${n} alberi`,
    treesOnMap: (n) => `${n} alberi sulla mappa`,
    heading: (c) => `Alberi monumentali di ${c}`,
    readMore: "Leggi di pi\u00f9",
    visitedOf: (n, city) => `visitati a ${city}`,
    saveOrTransfer: "Salva o trasferisci su un altro dispositivo",
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
    withWalkingRoute: ", con un percorso a piedi che ne tocca diversi.",
  },
  nl: {
    home: "Home",
    backToTrees: (n) => `\u2190 De ${n} bomen`,
    treesOnMap: (n) => `${n} bomen op de kaart`,
    heading: (c) => `Monumentale bomen in ${c}`,
    readMore: "Lees meer",
    visitedOf: (n, city) => `bezocht in ${city}`,
    saveOrTransfer: "Bewaren of naar een ander apparaat overzetten",
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
    withWalkingRoute: ", met een wandelroute die er verschillende aandoet.",
  },
  de: {
    home: "Start",
    backToTrees: (n) => `\u2190 Die ${n} B\u00e4ume`,
    treesOnMap: (n) => `${n} B\u00e4ume auf der Karte`,
    heading: (c) => `Alte B\u00e4ume in ${c}`,
    readMore: "Mehr lesen",
    visitedOf: (n, city) => `in ${city} besucht`,
    saveOrTransfer: "Sichern oder auf ein anderes Ger\u00e4t \u00fcbertragen",
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
    withWalkingRoute: ", mit einem Spaziergang, der an mehreren vorbeif\u00fchrt.",
  },
  pt: {
    home: "In\u00edcio",
    backToTrees: (n) => `\u2190 As ${n} \u00e1rvores`,
    treesOnMap: (n) => `${n} \u00e1rvores no mapa`,
    heading: (c) => `\u00c1rvores hist\u00f3ricas de ${c}`,
    readMore: "Ler mais",
    visitedOf: (n, city) => `visitadas em ${city}`,
    saveOrTransfer: "Guardar ou passar para outro dispositivo",
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
    withWalkingRoute: ", com um percurso a p\u00e9 que passa por v\u00e1rias delas.",
  },
  fr: {
    home: "Accueil",
    backToTrees: (n) => `\u2190 Les ${n} arbres`,
    treesOnMap: (n) => `${n} arbres sur la carte`,
    heading: (c) => `Arbres remarquables de ${c}`,
    readMore: "Lire la suite",
    visitedOf: (n, city) => `visit\u00e9s \u00e0 ${city}`,
    saveOrTransfer: "Enregistrer ou transf\u00e9rer vers un autre appareil",
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
    withWalkingRoute: ", avec un itin\u00e9raire \u00e0 pied qui en relie plusieurs.",
  },
  ja: {
    home: "\u30db\u30fc\u30e0",
    backToTrees: (n) => `\u2190 ${n}\u672c\u306e\u6a39\u6728`,
    treesOnMap: (n) => `\u5730\u56f3\u4e0a\u306e${n}\u672c`,
    heading: (c) => `${c}\u306e\u53e4\u6a39`,
    readMore: "\u7d9a\u304d\u3092\u8aad\u3080",
    visitedOf: (n, city) => `${city}\u3067\u8a2a\u308c\u305f\u6570`,
    saveOrTransfer: "\u4fdd\u5b58\u3059\u308b\u30fb\u5225\u306e\u7aef\u672b\u306b\u79fb\u3059",
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
    withWalkingRoute: "\u5f92\u6b69\u30eb\u30fc\u30c8\u3067\u3044\u304f\u3064\u304b\u3092\u3081\u3050\u308c\u307e\u3059\u3002",
  },
};

/** Chrome strings for `lang`, English wherever that language has no entry. */
export function ui(lang: string): UIStrings {
  return { ...EN, ...(TABLE[lang] ?? {}) };
}

/** The link text inside that line, also in the target language. */
export const LANG_NAME: Record<string, string> = {
  es: "en español",
  it: "in italiano",
  nl: "in het Nederlands",
  de: "auf Deutsch",
  pt: "em português",
  fr: "en français",
  ja: "日本語",
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
export async function translatedCityPaths(lang: string, allCities: CityLike[]) {
  return translatedCities(lang).map((slug) => {
    const city = allCities.find((c) => c.id === slug);
    if (!city) throw new Error(`data/i18n/${lang}/${slug}.json has no matching English city file`);
    const tr = cityTranslation(lang, slug)!;
    const ids = (city.data.trees ?? []).map((t: { id: string }) => t.id);
    for (const id of ids) {
      if (!tr.trees[id]) throw new Error(`${lang}/${slug}: no translation for ${id}; the English city grew past the overlay`);
    }
    const iw = tr.intro.split(/\s+/).filter(Boolean).length;
    if (iw < 60 || iw > 100) throw new Error(`${lang}/${slug}: intro is ${iw} words, Contract C requires 60-100`);
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
      const wc = x.story.split(/\s+/).filter(Boolean).length;
      // Japanese does not space its words, so a token count is meaningless
      // there; the character bar in the brief stands in for it.
      if (lang !== "ja" && (wc < 150 || wc > 250)) {
        throw new Error(`${lang}/${slug}/${tslugs[tree.id]}: story is ${wc} words, the 150-250 bar applies in every language`);
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
