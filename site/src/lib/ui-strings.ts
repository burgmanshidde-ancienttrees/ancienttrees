// The interface, in the languages we publish content in.
//
// Why this exists. On 2026-09-02 we had 663 hand-translated trees across 31
// sets, and every one of them sat inside an English frame: /es/seville served
// Spanish stories under a nav reading Map, Cities, Countries, Species, and
// buttons saying "Suggest a tree" and "Get the app". A reader who arrived from
// Google in Spanish met their own language in the middle of the page and
// somebody else's around the edges.
//
// Convention check (CONVENTIONS.md, "Switching the language of a page", read
// 2026-09-02): komoot ships its interface in 14 languages and AllTrails in 12,
// both translating the chrome into every locale they serve. Neither translates
// its own brand name, and neither do we: "Ancient Trees" stays "Ancient Trees"
// the way komoot stays komoot.
//
// The rule for adding a string here: every language gets an entry or the type
// stops compiling. A half-translated interface is worse than an English one,
// because an English nav is a consistent choice and a mixed nav is a fault.
export type Lang = "en" | "es" | "it" | "nl" | "de" | "pt" | "fr" | "ja";

export interface UiStrings {
  map: string;
  explore: string;
  browse: string;
  cities: string;
  countries: string;
  species: string;
  parks: string;
  collections: string;
  yours: string;
  savedTrees: string;
  yourAccount: string;
  suggestTree: string;
  sponsor: string;
  getApp: string;
  theApp: string;
  account: string;
  menu: string;
  support: string;
  privacy: string;
  terms: string;
  /** The credits page. Forty of our registers are published under a licence
   *  that obliges attribution, so this link is an obligation rather than a
   *  courtesy, and it belongs in every language the footer speaks. */
  sources: string;
  /** The footer's own paragraph. A sentence rather than a label, and it is the
   *  one piece of chrome that says what this site is for, so it is worth
   *  saying in the reader's language rather than only in ours. */
  footerAbout: string;
  /** The link inside that sentence. */
  tellUs: string;
}

export const UI: Record<Lang, UiStrings> = {
  en: {
    map: "Map", explore: "Explore", browse: "Browse", cities: "Cities",
    countries: "Countries", species: "Species", parks: "Parks",
    collections: "Collections", yours: "Yours", savedTrees: "Saved trees",
    yourAccount: "Your account", suggestTree: "Suggest a tree",
    sponsor: "Sponsor this project", getApp: "Download the app", theApp: "The app",
    account: "Account", menu: "Menu", support: "Support", privacy: "Privacy",
    terms: "Terms",
    sources: "Sources",
    footerAbout: "We are on a mission to map every remarkable tree in the world, and we could use your help. If you know a good tree, or spot a mistake on one of these pages, {link}. We work on this database every day.",
    tellUs: "tell us",
  },
  es: {
    map: "Mapa", explore: "Explorar", browse: "Navegar", cities: "Ciudades",
    countries: "Países", species: "Especies", parks: "Parques",
    collections: "Colecciones", yours: "Tu perfil", savedTrees: "Árboles guardados",
    yourAccount: "Tu cuenta", suggestTree: "Propón un árbol",
    sponsor: "Apoya este proyecto", getApp: "Descarga la app", theApp: "La app",
    account: "Cuenta", menu: "Menú", support: "Ayuda", privacy: "Privacidad",
    terms: "Términos",
    sources: "Fuentes",
    footerAbout: "Queremos cartografiar todos los árboles notables del mundo, y nos vendría bien tu ayuda. Si conoces un buen árbol, o ves un error en alguna de estas páginas, {link}. Trabajamos en esta base de datos todos los días.",
    tellUs: "cuéntanoslo",
  },
  it: {
    map: "Mappa", explore: "Esplora", browse: "Sfoglia", cities: "Città",
    countries: "Paesi", species: "Specie", parks: "Parchi",
    collections: "Collezioni", yours: "Il tuo profilo", savedTrees: "Alberi salvati",
    yourAccount: "Il tuo account", suggestTree: "Segnala un albero",
    sponsor: "Sostieni il progetto", getApp: "Scarica l'app", theApp: "L'app",
    account: "Account", menu: "Menu", support: "Assistenza", privacy: "Privacy",
    terms: "Termini",
    sources: "Fonti",
    footerAbout: "Vogliamo mappare tutti gli alberi monumentali del mondo, e ci serve una mano. Se conosci un albero che merita, o trovi un errore in queste pagine, {link}. Lavoriamo a questo archivio ogni giorno.",
    tellUs: "scrivicelo",
  },
  nl: {
    map: "Kaart", explore: "Ontdekken", browse: "Bladeren", cities: "Steden",
    countries: "Landen", species: "Soorten", parks: "Parken",
    collections: "Collecties", yours: "Jouw profiel", savedTrees: "Bewaarde bomen",
    yourAccount: "Je account", suggestTree: "Boom aandragen",
    sponsor: "Steun dit project", getApp: "Download de app", theApp: "De app",
    account: "Account", menu: "Menu", support: "Hulp", privacy: "Privacy",
    terms: "Voorwaarden",
    sources: "Bronnen",
    footerAbout: "We willen elke bijzondere boom ter wereld in kaart brengen, en daar kunnen we hulp bij gebruiken. Ken je een goede boom, of zie je een fout op een van deze pagina's, {link}. We werken elke dag aan deze database.",
    tellUs: "laat het ons weten",
  },
  de: {
    map: "Karte", explore: "Entdecken", browse: "Stöbern", cities: "Städte",
    countries: "Länder", species: "Arten", parks: "Parks",
    collections: "Sammlungen", yours: "Dein Profil", savedTrees: "Gemerkte Bäume",
    yourAccount: "Dein Konto", suggestTree: "Baum vorschlagen",
    sponsor: "Projekt unterstützen", getApp: "App laden", theApp: "Die App",
    account: "Konto", menu: "Menü", support: "Hilfe", privacy: "Datenschutz",
    terms: "AGB",
    sources: "Quellen",
    footerAbout: "Wir wollen jeden bemerkenswerten Baum der Welt kartieren, und dabei können wir Hilfe gebrauchen. Wenn du einen guten Baum kennst oder auf einer dieser Seiten einen Fehler siehst, {link}. Wir arbeiten jeden Tag an dieser Datenbank.",
    tellUs: "schreib uns",
  },
  pt: {
    map: "Mapa", explore: "Explorar", browse: "Navegar", cities: "Cidades",
    countries: "Países", species: "Espécies", parks: "Parques",
    collections: "Coleções", yours: "O teu perfil", savedTrees: "Árvores guardadas",
    yourAccount: "A tua conta", suggestTree: "Sugerir uma árvore",
    sponsor: "Apoiar o projeto", getApp: "Obter a app", theApp: "A app",
    account: "Conta", menu: "Menu", support: "Ajuda", privacy: "Privacidade",
    terms: "Termos",
    sources: "Fontes",
    footerAbout: "Queremos mapear todas as árvores notáveis do mundo, e damos jeito a ajuda. Se conhece uma boa árvore, ou encontra um erro numa destas páginas, {link}. Trabalhamos nesta base de dados todos os dias.",
    tellUs: "diga-nos",
  },
  fr: {
    map: "Carte", explore: "Explorer", browse: "Parcourir", cities: "Villes",
    countries: "Pays", species: "Espèces", parks: "Parcs",
    collections: "Collections", yours: "Votre profil", savedTrees: "Arbres enregistrés",
    yourAccount: "Votre compte", suggestTree: "Proposer un arbre",
    sponsor: "Soutenir le projet", getApp: "Télécharger l'app", theApp: "L'app",
    account: "Compte", menu: "Menu", support: "Aide", privacy: "Confidentialité",
    terms: "Conditions",
    sources: "Sources",
    footerAbout: "Nous voulons cartographier tous les arbres remarquables du monde, et un coup de main ne serait pas de refus. Si vous connaissez un bel arbre, ou repérez une erreur sur l'une de ces pages, {link}. Nous travaillons sur cette base tous les jours.",
    tellUs: "dites-le-nous",
  },
  ja: {
    map: "地図", explore: "さがす", browse: "一覧", cities: "都市",
    countries: "国", species: "樹種", parks: "公園",
    collections: "コレクション", yours: "マイページ", savedTrees: "保存した木",
    yourAccount: "アカウント設定", suggestTree: "木を教える",
    sponsor: "このプロジェクトを支援", getApp: "アプリを入手", theApp: "アプリ",
    account: "アカウント", menu: "メニュー", support: "ヘルプ", privacy: "プライバシー",
    terms: "利用規約",
    sources: "出典",
    footerAbout: "世界じゅうの見に行く価値のある木を地図にしたいと思っている。力を貸してほしい。よい木を知っている場合や、このページに誤りを見つけた場合は、{link}。このデータベースは毎日更新している。",
    tellUs: "知らせてほしい",
  },
};

/** The strings for a page's language, falling back to English for anything we
 *  do not publish content in. A fallback is never a mixed nav: it returns the
 *  whole English set rather than filling gaps string by string. */
export function chrome(lang: string | undefined): UiStrings {
  return UI[(lang ?? "en") as Lang] ?? UI.en;
}
