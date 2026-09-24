// The sign-in dialog, in the languages we publish content in.
//
// Why this exists. SignInModal.astro carried its copy in a ternary,
// `const T = es ? {...} : {...}`, written during the one-city Spanish test in
// August. When the rollout went to seven languages a `lang` prop was bolted
// onto it and the copy was never widened, so `lang === "es"` took the Spanish
// branch and everything else took the English one. The dialog renders on all
// 31 translated city and tree pages, so a German, Japanese, Italian, Dutch,
// French or Portuguese reader who tapped a heart met an English dialog,
// including the sentence saying what personal data we hold.
//
// It is the same fault ui-strings.ts was written for the day before, one
// component further in, and it is fixed the same way: a Record typed by Lang,
// so a language missing from this table stops the build instead of shipping
// English to somebody who cannot read it.
//
// The copy follows PRODUCT_COPY.md rather than TONE_OF_VOICE.md: these are the
// twenty words somebody reads while holding the thing, so the reader is the
// subject, the sentence says what they can do, and we name ourselves where we
// act. Japanese follows the 常体 of the ja block in i18n.ts.
//
// Two strings carry weight and must say the same thing in every language.
// `fine` is our statement of what personal data we hold: the email address,
// the trees you save, the trees you photograph, and that continuing means
// agreeing to the Terms and the Privacy notice. It is never softened,
// shortened or turned into reassurance, and both anchors stay. `sentBody2`
// carries three facts a person needs: the link works once, it expires in
// fifteen minutes, and it brings them back where they were.
import type { Lang } from "./ui-strings";

export interface SignInStrings {
  /** The generic heading, when no tree is named. */
  title: string;
  /** The generic subtitle. */
  sub: string;
  /** The subtitle when a tree is named. %s is the tree's name; put it where
   *  the grammar of the language wants it. */
  subNamed: string;
  /** The heading when the dialog opens from a vote, correction or report. */
  titleFeedback: string;
  titleExpired: string;
  subExpired: string;
  subFeedback: string;
  /** The heading when the dialog opens BY ITSELF on the contribute flow, which
   *  it does for anybody not signed in (2026-09-24). It has to say what the
   *  person came to do, because they did not press anything to get here. */
  titleContribute: string;
  subContribute: string;
  /** An example address, in the local convention. */
  placeholder: string;
  send: string;
  google: string;
  /** Apple's own wording, in Apple's own localisation of it. It renders only
   *  where APPLE_SIGNIN is on, and it is filled in every language regardless,
   *  so the day that flag flips no reader meets an English button. */
  apple: string;
  /** The headline a PHONE gets, where continuing in the app is the offer.
   *  AllTrails' own sheet: "AllTrails werkt beter in de app". */
  appTitle: string;
  /** Their "Ga verder in de app": the loud button on a phone. */
  openApp: string;
  /** Their "Verdergaan met e-mail": a BUTTON on the second screen, not a
   *  field. The field only appears once somebody has asked for it. */
  emailBtn: string;
  /** The grey button that reveals the typed route, AllTrails' "Meer opties".
   *  It hides the email field until somebody asks for it, which is what keeps
   *  the closed sheet down to two choices. */
  more: string;
  or: string;
  app: string;
  /** What we store, plus the Terms and Privacy links. Both anchors required. */
  fine: string;
  sentTitle: string;
  /** Wraps the address: sentBody1 + <strong>address</strong> + sentBody2, so a
   *  language that puts the address before the verb splits it that way. */
  sentBody1: string;
  sentBody2: string;
  /** Labels a screen reader gets, which were English on every page until
   *  2026-09-02. */
  close: string;
  emailLabel: string;
}

export const SIGNIN: Record<Lang, SignInStrings> = {
  en: {
    title: "Keep your trees on every device",
    sub: "An account keeps what you collect and save.",
    subNamed: "Sign in to save %s. An account keeps what you collect, on every device you use.",
    titleFeedback: "Sign in to have your say",
    titleExpired: "That link has expired",
    subExpired: "A sign-in link works once, within the hour. You can ask for a new one below.",
    subFeedback: "Every vote, correction and tip gets checked and answered, and your account is how the answer reaches you.",
    titleContribute: "You need an account to add a tree",
    subContribute: "Your account keeps the trees you send, so you can see what happened to each one.",
    placeholder: "you@example.com",
    send: "Email me a sign-in link",
    google: "Continue with Google",
    apple: "Continue with Apple",
    appTitle: "Ancient Trees works better in the app",
    openApp: "Continue in the app",
    emailBtn: "Continue with email",
    more: "More options",
    or: "or",
    app: "Get the app",
    // An absolute about what we hold stood here until 2026-08-28, and it had
    // been false since saves, profiles and follows arrived. The app's sign-in
    // sheet said the same thing and was corrected the same hour; both surfaces
    // say what we hold and let the list be the limit.
    fine: 'We store your email address and what you collect: the trees you save and the ones you photograph. By continuing you agree to the <a href="/terms">Terms</a> and the <a href="/privacy">Privacy</a> notice.',
    sentTitle: "Check your inbox",
    sentBody1: "We sent a sign-in link to ",
    sentBody2: ". It works once, expires in 15 minutes, and brings you straight back here.",
    close: "Close",
    emailLabel: "Email address",
  },
  es: {
    title: "Tus árboles en todos tus dispositivos",
    sub: "Una cuenta gratuita, un email, sin contraseña. Tus árboles guardados te siguen a cualquier dispositivo.",
    subNamed: "Inicia sesión para guardar %s. Una cuenta gratuita, un email, sin contraseña, y tus árboles te siguen a todas partes.",
    titleFeedback: "Inicia sesión para opinar",
    titleExpired: "Ese enlace ha caducado",
    subExpired: "Un enlace de acceso funciona una vez, durante una hora. Puedes pedir uno nuevo aquí abajo.",
    subFeedback: "Cada voto, corrección y sugerencia se comprueba y se responde, y tu cuenta es como te llega la respuesta.",
    titleContribute: "Necesitas una cuenta para añadir un árbol",
    subContribute: "Tu cuenta guarda los árboles que envías, así que puedes ver qué pasó con cada uno.",
    placeholder: "tu@ejemplo.com",
    send: "Envíame un enlace de acceso",
    google: "Continuar con Google",
    apple: "Continuar con Apple",
    appTitle: "Ancient Trees funciona mejor en la app",
    openApp: "Continuar en la app",
    emailBtn: "Continuar con email",
    more: "Más opciones",
    or: "o",
    // Read "Consigue acceso anticipado" until 2026-09-02, which is "Get early
    // access". Hidde changed the English back to "Get the app" on 2026-08-24
    // ("why would you do that, change it back") and the Spanish was missed.
    app: "Descarga la app",
    fine: 'Guardamos tu dirección de email y lo que coleccionas: los árboles que guardas y los que fotografías. Al continuar aceptas las <a href="/terms">Condiciones</a> y la <a href="/privacy">Privacidad</a>.',
    sentTitle: "Mira tu bandeja de entrada",
    sentBody1: "Hemos enviado un enlace de acceso a ",
    sentBody2: ". Funciona una vez, caduca en 15 minutos y te trae de vuelta aquí.",
    close: "Cerrar",
    emailLabel: "Dirección de email",
  },
  it: {
    title: "I tuoi alberi su ogni dispositivo",
    sub: "Un account conserva quello che raccogli e salvi.",
    subNamed: "Accedi per salvare %s. Un account conserva quello che raccogli, su ogni dispositivo che usi.",
    titleFeedback: "Accedi per dire la tua",
    titleExpired: "Quel link è scaduto",
    subExpired: "Un link di accesso funziona una volta, entro un'ora. Puoi chiederne uno nuovo qui sotto.",
    subFeedback: "Controlliamo e rispondiamo a ogni voto, correzione e segnalazione, e la risposta ti arriva sul tuo account.",
    titleContribute: "Serve un account per aggiungere un albero",
    subContribute: "Il tuo account conserva gli alberi che invii, così puoi vedere che fine ha fatto ciascuno.",
    placeholder: "tu@esempio.com",
    send: "Inviami un link di accesso",
    google: "Continua con Google",
    apple: "Continua con Apple",
    appTitle: "Ancient Trees funziona meglio nell'app",
    openApp: "Continua nell'app",
    emailBtn: "Continua con l'email",
    more: "Altre opzioni",
    or: "o",
    app: "Scarica l'app",
    fine: 'Conserviamo il tuo indirizzo email e quello che raccogli: gli alberi che salvi e quelli che fotografi. Continuando accetti i <a href="/terms">Termini</a> e l\'informativa sulla <a href="/privacy">Privacy</a>.',
    sentTitle: "Controlla la posta",
    sentBody1: "Abbiamo inviato un link di accesso a ",
    sentBody2: ". Funziona una volta sola, scade tra 15 minuti e ti riporta esattamente qui.",
    close: "Chiudi",
    emailLabel: "Indirizzo email",
  },
  nl: {
    title: "Je bomen op elk apparaat",
    sub: "Met een account houd je wat je verzamelt en bewaart.",
    subNamed: "Log in om %s te bewaren. Met een account houd je wat je verzamelt, op elk apparaat dat je gebruikt.",
    titleFeedback: "Log in om je mening te geven",
    titleExpired: "Die link is verlopen",
    subExpired: "Een inloglink werkt één keer, binnen een uur. Je kunt hieronder een nieuwe aanvragen.",
    subFeedback: "We controleren en beantwoorden elke stem, correctie en tip, en via je account krijg je het antwoord.",
    titleContribute: "Je hebt een account nodig om een boom toe te voegen",
    subContribute: "Je account bewaart de bomen die je stuurt, zodat je kunt zien wat er met elke boom is gebeurd.",
    placeholder: "jij@voorbeeld.nl",
    send: "Mail me een inloglink",
    google: "Doorgaan met Google",
    apple: "Doorgaan met Apple",
    appTitle: "Ancient Trees werkt beter in de app",
    openApp: "Ga verder in de app",
    emailBtn: "Verdergaan met e-mail",
    more: "Meer opties",
    or: "of",
    app: "Download de app",
    fine: 'We bewaren je e-mailadres en wat je verzamelt: de bomen die je bewaart en de bomen die je fotografeert. Als je doorgaat ga je akkoord met de <a href="/terms">Voorwaarden</a> en de <a href="/privacy">Privacyverklaring</a>.',
    sentTitle: "Kijk in je inbox",
    sentBody1: "We hebben een inloglink gestuurd naar ",
    sentBody2: ". Hij werkt één keer, verloopt na 15 minuten en brengt je terug naar deze pagina.",
    close: "Sluiten",
    emailLabel: "E-mailadres",
  },
  de: {
    title: "Deine Bäume auf jedem Gerät",
    sub: "Ein Konto behält, was du sammelst und speicherst.",
    subNamed: "Melde dich an, um %s zu speichern. Ein Konto behält, was du sammelst, auf jedem Gerät, das du benutzt.",
    titleFeedback: "Melde dich an, um mitzureden",
    titleExpired: "Dieser Link ist abgelaufen",
    subExpired: "Ein Anmeldelink funktioniert einmal, innerhalb einer Stunde. Unten kannst du einen neuen anfordern.",
    subFeedback: "Wir prüfen und beantworten jede Stimme, jede Korrektur und jeden Hinweis, und über dein Konto erreicht dich die Antwort.",
    titleContribute: "Für einen neuen Baum brauchst du ein Konto",
    subContribute: "Dein Konto behält die Bäume, die du schickst, damit du siehst, was aus jedem geworden ist.",
    placeholder: "du@beispiel.de",
    send: "Schick mir einen Anmeldelink",
    google: "Weiter mit Google",
    apple: "Weiter mit Apple",
    appTitle: "Ancient Trees funktioniert besser in der App",
    openApp: "Weiter in der App",
    emailBtn: "Weiter mit E-Mail",
    more: "Weitere Optionen",
    or: "oder",
    app: "App laden",
    fine: 'Wir speichern deine E-Mail-Adresse und was du sammelst: die Bäume, die du speicherst, und die, die du fotografierst. Wenn du fortfährst, stimmst du den <a href="/terms">AGB</a> und der <a href="/privacy">Datenschutzerklärung</a> zu.',
    sentTitle: "Schau in dein Postfach",
    sentBody1: "Wir haben einen Anmeldelink an ",
    sentBody2: " geschickt. Er funktioniert einmal, läuft nach 15 Minuten ab und bringt dich direkt hierher zurück.",
    close: "Schließen",
    emailLabel: "E-Mail-Adresse",
  },
  pt: {
    title: "As tuas árvores em todos os dispositivos",
    sub: "Uma conta mantém o que colecionas e guardas.",
    subNamed: "Inicia sessão para guardar %s. Uma conta mantém o que colecionas, em todos os dispositivos que usas.",
    titleFeedback: "Inicia sessão para dar a tua opinião",
    titleExpired: "Esse link expirou",
    subExpired: "Um link de acesso funciona uma vez, dentro de uma hora. Podes pedir um novo aqui em baixo.",
    subFeedback: "Verificamos e respondemos a cada voto, correção e sugestão, e a resposta chega-te através da tua conta.",
    titleContribute: "Precisa de uma conta para adicionar uma árvore",
    subContribute: "A sua conta guarda as árvores que envia, para poder ver o que aconteceu a cada uma.",
    placeholder: "tu@exemplo.com",
    send: "Envia-me um link de acesso",
    google: "Continuar com Google",
    apple: "Continuar com Apple",
    appTitle: "O Ancient Trees funciona melhor na app",
    openApp: "Continuar na app",
    emailBtn: "Continuar com email",
    more: "Mais opções",
    or: "ou",
    app: "Obter a app",
    fine: 'Guardamos o teu endereço de email e o que colecionas: as árvores que guardas e as que fotografas. Ao continuares, aceitas os <a href="/terms">Termos</a> e a <a href="/privacy">Privacidade</a>.',
    sentTitle: "Vê a tua caixa de entrada",
    sentBody1: "Enviámos um link de acesso para ",
    sentBody2: ". Funciona uma vez, expira em 15 minutos e traz-te de volta a esta página.",
    close: "Fechar",
    emailLabel: "Endereço de email",
  },
  fr: {
    title: "Vos arbres sur tous vos appareils",
    sub: "Un compte conserve ce que vous collectionnez et enregistrez.",
    subNamed: "Connectez-vous pour enregistrer %s. Un compte conserve ce que vous collectionnez, sur tous les appareils que vous utilisez.",
    titleFeedback: "Connectez-vous pour donner votre avis",
    titleExpired: "Ce lien a expiré",
    subExpired: "Un lien de connexion fonctionne une fois, dans l'heure. Vous pouvez en demander un nouveau ci-dessous.",
    subFeedback: "Nous vérifions et répondons à chaque vote, correction et suggestion, et la réponse vous parvient par votre compte.",
    titleContribute: "Il vous faut un compte pour ajouter un arbre",
    subContribute: "Votre compte conserve les arbres que vous envoyez, pour que vous puissiez voir ce qu'il est advenu de chacun.",
    placeholder: "vous@exemple.com",
    send: "Envoyez-moi un lien de connexion",
    google: "Continuer avec Google",
    apple: "Continuer avec Apple",
    appTitle: "Ancient Trees fonctionne mieux dans l'app",
    openApp: "Continuer dans l'app",
    emailBtn: "Continuer avec l'e-mail",
    more: "Plus d'options",
    or: "ou",
    app: "Télécharger l'app",
    fine: 'Nous conservons votre adresse email et ce que vous collectionnez : les arbres que vous enregistrez et ceux que vous photographiez. En continuant, vous acceptez les <a href="/terms">Conditions</a> et la <a href="/privacy">Confidentialité</a>.',
    sentTitle: "Regardez votre boîte mail",
    sentBody1: "Nous avons envoyé un lien de connexion à ",
    sentBody2: ". Il fonctionne une seule fois, expire dans 15 minutes et vous ramène directement ici.",
    close: "Fermer",
    emailLabel: "Adresse email",
  },
  ja: {
    title: "どの端末でも見られる自分の木",
    sub: "アカウントがあれば、集めた木も保存した木も残る。",
    subNamed: "サインインすると%sを保存できる。アカウントがあれば、集めた木は使うどの端末にも残る。",
    titleFeedback: "サインインして意見を伝える",
    titleExpired: "このリンクは期限切れです",
    subExpired: "サインインリンクは1時間以内に1回だけ使えます。下から新しいリンクをリクエストできます。",
    subFeedback: "投票も訂正も情報も、すべて確認して返事をする。返事はアカウントに届く。",
    titleContribute: "木を追加するにはアカウントが必要です",
    subContribute: "アカウントが送った木を保存するので、それぞれがどうなったかを確認できます。",
    placeholder: "sample@example.com",
    send: "サインインのリンクを送る",
    google: "Googleで続ける",
    apple: "Appleで続ける",
    appTitle: "Ancient Trees はアプリのほうが快適",
    openApp: "アプリで続ける",
    emailBtn: "メールで続ける",
    more: "その他の方法",
    or: "または",
    app: "アプリを入手",
    fine: '私たちが保管するのは、メールアドレスと、集めたもの、つまり保存した木と撮影した木である。続けると<a href="/terms">利用規約</a>と<a href="/privacy">プライバシー</a>に同意したことになる。',
    sentTitle: "受信トレイを確認する",
    sentBody1: "サインインのリンクを ",
    sentBody2: " に送った。リンクは一度だけ使えて、15分で期限が切れ、いまいたページに戻る。",
    close: "閉じる",
    emailLabel: "メールアドレス",
  },
};

/** The dialog's copy for a page's language. An unlisted language gets the
 *  WHOLE English object rather than English filled in key by key: a dialog in
 *  two languages reads as a fault, where an English one reads as a choice. */
export function signInCopy(lang: string | undefined): SignInStrings {
  return SIGNIN[(lang ?? "en") as Lang] ?? SIGNIN.en;
}
