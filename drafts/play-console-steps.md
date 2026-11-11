# Google Play: wat jij klikt, in de volgorde van de console

Alles wat zonder jou kon is klaar. De teksten staan in
drafts/play-store-listing.md, de antwoorden op de formulieren in
drafts/play-console-forms.md, het app-bestand en de plaatjes in out/play/ op de
Mac (`python3 scripts/android_release.py` maakt het .aab opnieuw). Dit begint
pas als Google je identiteit heeft bevestigd.

## 1. De app aanmaken

1. play.google.com/console > **Create app**.
2. App name: `Ancient Trees: Old Tree Map`. Default language: **English (United Kingdom) – en-GB**.
3. App or game: **App**. Free or paid: **Free** (een gratis app kan later in-app aankopen krijgen; alleen van gratis naar betaald kan niet).
4. Vink de twee verklaringen aan (Developer Program Policies, US export laws). Dat accepteren is aan jou. **Create app**.

## 2. Dashboard > "Set up your app" (Policy > App content)

Elk punt hieronder staat met het antwoord in drafts/play-console-forms.md.

1. **Privacy policy**: `https://ancienttrees.app/privacy`.
2. **App access**: "All or some functionality is restricted", plak de uitleg voor de reviewer.
3. **Ads**: No.
4. **Content rating**: start de vragenlijst, categorie "All Other App Types", alles Nee behalve "Users can interact": Ja. Submit.
5. **Target audience**: 16-17 en 18+. Niet aantrekkelijk voor kinderen.
6. **News app**: No.
7. **Data safety**: neem de tabel over, type voor type. Delete-URL `https://ancienttrees.app/account`.
8. **Government apps**: No. **Financial features**: geen. **Health**: geen.
9. **Advertising ID**: No.

## 3. Store listing (Grow users > Store presence > Main store listing)

1. **Kies eerst**: categorie (Travel & Local of Maps & Navigation) en het contactadres dat openbaar op de pagina staat. Beide staan als vraag in de listing-draft.
2. Store settings: categorie, contactmail, website `https://ancienttrees.app`.
3. Main store listing: naam, korte en lange beschrijving uit de Engelse sectie.
4. Graphics: `out/play/icon-512.png`, `out/play/feature-graphic-1024x500.png`, en de telefoon-screenshots `out/play/phone-*.png` (in volgorde 1 tot 4).
5. **Translations** > Add your own translation text: en-US, nl-NL, de-DE, fr-FR, es-ES, it-IT, pt-PT, ja-JP, elk met de drie velden uit de draft. De plaatjes mogen voor alle talen dezelfde blijven.
6. Save.

## 4. Gesloten test (verplicht voor een nieuw persoonlijk account)

1. Testing > **Closed testing** > Create track (of de standaard "Alpha").
2. **Testers**: maak een e-maillijst met minstens 12 Google-adressen (liever 15). Wie je zou kunnen vragen staat in de forms-draft; niemand is benaderd.
3. **Create new release**. Bij de eerste upload vraagt Play om **Play App Signing**: kies "Use Google-generated key" (de standaard). Upload `out/play/ancient-trees-0.1.0-1.aab`.
4. Release name mag zo blijven; release notes: één regel, bijvoorbeeld `First test of Ancient Trees on Android.`
5. **Review release** > **Start rollout to Closed testing**. Google keurt het eerst (uren tot een paar dagen).
6. Kopieer de **opt-in link** op de Testers-tab en stuur die naar de testers (de mail zelf schrijven we samen; niets gaat zonder jouw ja).
7. Laat het mij weten zodra de eerste upload erin staat: dan zet ik de sleutel van Play App Signing (Setup > App signing > "App signing key certificate", SHA-256) in `site/public/.well-known/assetlinks.json`, zodat links naar ancienttrees.app in de app openen.

## 5. Na 14 dagen

1. Dashboard > **Apply for production**. Google vraagt hoe je testers vond en wat je met hun feedback deed: houd daarom tijdens de test bij wat ze zeiden.
2. Na goedkeuring: Production > Create new release met hetzelfde of een nieuwer .aab, landen kiezen (alle), **Start rollout**. Een gefaseerde uitrol (bijvoorbeeld 20%) is hetzelfde als op iOS.

## Goed om te weten

- Het upload-sleutelbestand staat op de Mac in `~/.ancienttrees-android-upload.jks`, de wachtwoorden in `~/.ancienttrees-android.env`. Niet in de repository. Zet beide in je wachtwoordmanager of backup: kwijt is herstelbaar (Google kan de uploadsleutel resetten), maar dat kost dagen.
- Versie: de app heet nu 0.1.0 (versionCode 1). Wil je in de winkel 1.0 zien, zeg het; dan zet ik versionName op 1.0.0 voor de eerste upload.
- Elke volgende upload heeft een hoger versionCode nodig; het script leest het uit android/app/build.gradle.kts.
