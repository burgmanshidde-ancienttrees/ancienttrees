# Google Play store listing, 2026-11-11

For Play Console, Grow users > Store presence > Main store listing. Fenced
blocks are the copy; the lines around them are notes for Hidde. Based on
drafts/app-store-metadata-1.0.3.md, the iPhone listing he approved: the same
names per language and the same description, because the Android app has the
same screens (36 of 39 matched on 2026-11-10, the map in PR #48). Every line of
the description was checked against the Android app: the map and search
(MapTab, MapSearch), directions (Directions.kt), "At their best now", the
records and the tree cities on Discover, collecting with a photograph
(CollectSheet), Want to visit (MyTrees), and adding a tree that is not on the
map (DraftTree).

Play's limits: app name 30, short description 80, full description 4000.
Play indexes all three (unlike Apple, which reads no description), so the short
description is the one new line here. It is his own verb from PITCH_VOICE.md
("Explore remarkable old trees around you") plus the fourth verb, collect.
`python3 scripts/play_listing_check.py` counts every field and runs pitchcheck.

## Two things for you to choose

- **Category.** Play has no "Navigation" for apps like ours outside Maps &
  Navigation. The two that fit: **Travel & Local** (AllTrails and komoot sit
  there) or **Maps & Navigation**. Which one?
- **Contact email** shown on the listing (Play requires one, it is public).
  info@ancienttrees.app is the address on the privacy page; is that the one?

Fixed, no choice: website https://ancienttrees.app, privacy policy
https://ancienttrees.app/privacy. Tags: up to five from Play's list, picked in
the console (Travel & Local offers "Travel guide", "Maps", "Outdoors").

## English (United Kingdom), the default language (en-GB)

App name, 27/30:

```
Ancient Trees: Old Tree Map
```

Short description, 71/80:

```
Explore remarkable old trees around you and collect the ones you visit.
```

Full description:

```
While visiting Lisbon and walking through its parks, I kept stumbling on huge, beautiful old trees and wanted a way to find more of them. That became Ancient Trees: a map of remarkable trees worth a visit, wherever you are.

A yew older than the church beside it, a plane tree it takes four people to hug, an oak that has seen everything happen on its street.

FIND
• The old trees near you, on a map
• Search by place, species or name
• Directions to the trunk

DISCOVER
• The trees at their best this month, wherever you are
• The oldest, tallest and thickest trees
• Tree cities around the world

COLLECT
• Photograph a tree you are standing in front of to add it to your collection
• Keep a list of the trees you want to visit
• Add a tree that is not on the map yet
```

## English (United States), en-US

Same name, short description and description as en-GB. Add it as a
translation so the US storefront reads its own language entry.

## Dutch, nl-NL

App name, 25/30:

```
Ancient Trees: Oude bomen
```

Short description:

```
Ontdek bijzondere oude bomen om je heen en verzamel de bomen die je bezoekt.
```

Full description:

```
Toen ik Lissabon bezocht en door de parken wandelde, kwam ik steeds enorme, prachtige oude bomen tegen en wilde ik een manier om er meer te vinden. Zo ontstond Ancient Trees: een kaart van bijzondere bomen die een bezoek waard zijn, waar je ook bent.

Een taxus ouder dan de kerk ernaast, een plataan waar vier mensen hun armen omheen moeten slaan, een eik die alles heeft gezien wat er in zijn straat gebeurde.

VINDEN
• De oude bomen bij jou in de buurt, op een kaart
• Zoeken op plaats, soort of naam
• Een route naar de stam

ONTDEKKEN
• De bomen die deze maand op hun mooist zijn, waar je ook bent
• De oudste, hoogste en dikste bomen
• Bomensteden over de hele wereld

VERZAMELEN
• Fotografeer een boom waar je voor staat om hem aan je verzameling toe te voegen
• Houd een lijst bij van bomen die je wilt bezoeken
• Voeg een boom toe die nog niet op de kaart staat
```

## German, de-DE

App name, 25/30:

```
Ancient Trees: Alte Bäume
```

Short description:

```
Entdecke besondere alte Bäume um dich herum und sammle die, die du besuchst.
```

Full description:

```
Als ich Lissabon besuchte und durch die Parks spazierte, stieß ich immer wieder auf riesige, wunderschöne alte Bäume und wollte einen Weg finden, mehr davon zu entdecken. So entstand Ancient Trees: eine Karte besonderer Bäume, die einen Besuch wert sind, wo immer du bist.

Eine Eibe, älter als die Kirche daneben, eine Platane, die vier Menschen kaum umarmen können, eine Eiche, die alles gesehen hat, was in ihrer Straße geschah.

FINDEN
• Die alten Bäume in deiner Nähe, auf einer Karte
• Suche nach Ort, Art oder Name
• Der Weg bis zum Stamm

ENTDECKEN
• Die Bäume, die diesen Monat am schönsten sind, wo immer du bist
• Die ältesten, höchsten und dicksten Bäume
• Baumstädte auf der ganzen Welt

SAMMELN
• Fotografiere einen Baum, vor dem du stehst, und er kommt in deine Sammlung
• Führe eine Liste der Bäume, die du besuchen willst
• Füge einen Baum hinzu, der noch nicht auf der Karte ist
```

## French, fr-FR

App name, 27/30:

```
Ancient Trees: Vieux arbres
```

Short description:

```
Explorez les vieux arbres remarquables autour de vous et collectionnez-les.
```

Full description:

```
En visitant Lisbonne et en me promenant dans ses parcs, je tombais sans cesse sur d'immenses et magnifiques vieux arbres, et je voulais un moyen d'en trouver d'autres. C'est devenu Ancient Trees : une carte des arbres remarquables qui valent le détour, où que vous soyez.

Un if plus vieux que l'église voisine, un platane qu'il faut quatre personnes pour entourer, un chêne qui a tout vu de ce qui s'est passé dans sa rue.

TROUVER
• Les vieux arbres près de vous, sur une carte
• Recherche par lieu, espèce ou nom
• L'itinéraire jusqu'au tronc

DÉCOUVRIR
• Les arbres à leur plus beau ce mois-ci, où que vous soyez
• Les arbres les plus vieux, les plus hauts et les plus gros
• Des villes d'arbres partout dans le monde

COLLECTIONNER
• Photographiez un arbre devant lequel vous vous tenez pour l'ajouter à votre collection
• Gardez une liste des arbres que vous voulez visiter
• Ajoutez un arbre qui n'est pas encore sur la carte
```

## Spanish, es-ES

App name, 29/30:

```
Ancient Trees: Árboles viejos
```

Short description:

```
Explora árboles viejos singulares a tu alrededor y colecciona los que visitas.
```

Full description:

```
Visitando Lisboa y paseando por sus parques, no paraba de encontrarme con árboles viejos enormes y preciosos, y quería una forma de encontrar más. Así nació Ancient Trees: un mapa de árboles singulares que merecen una visita, estés donde estés.

Un tejo más antiguo que la iglesia de al lado, un plátano que hacen falta cuatro personas para abrazar, un roble que ha visto todo lo que ha pasado en su calle.

ENCONTRAR
• Los árboles viejos cerca de ti, en un mapa
• Busca por lugar, especie o nombre
• Indicaciones hasta el tronco

DESCUBRIR
• Los árboles en su mejor momento este mes, estés donde estés
• Los árboles más viejos, más altos y más gruesos
• Ciudades de árboles de todo el mundo

COLECCIONAR
• Fotografía un árbol frente al que estás para añadirlo a tu colección
• Lleva una lista de los árboles que quieres visitar
• Añade un árbol que aún no está en el mapa
```

## Italian, it-IT

App name, 30/30:

```
Ancient Trees: Alberi secolari
```

Short description:

```
Esplora gli alberi secolari intorno a te e colleziona quelli che visiti.
```

Full description:

```
Visitando Lisbona e passeggiando nei suoi parchi, continuavo a imbattermi in alberi antichi enormi e bellissimi, e volevo un modo per trovarne altri. Così è nato Ancient Trees: una mappa di alberi straordinari che valgono una visita, ovunque tu sia.

Un tasso più antico della chiesa accanto, un platano che servono quattro persone per abbracciare, una quercia che ha visto tutto ciò che è successo nella sua strada.

TROVA
• Gli alberi secolari vicino a te, su una mappa
• Cerca per luogo, specie o nome
• Le indicazioni fino al tronco

SCOPRI
• Gli alberi al loro meglio questo mese, ovunque tu sia
• Gli alberi più antichi, più alti e più grandi
• Città degli alberi in tutto il mondo

COLLEZIONA
• Fotografa un albero davanti a cui ti trovi per aggiungerlo alla tua collezione
• Tieni una lista degli alberi che vuoi visitare
• Aggiungi un albero che non è ancora sulla mappa
```

## Portuguese (Portugal), pt-PT

Play keeps pt-PT and pt-BR apart; the app's Portuguese is European, as on the
iPhone. A Brazilian entry can copy this one later.

App name, 30/30:

```
Ancient Trees: Árvores antigas
```

Short description:

```
Explore árvores antigas notáveis à sua volta e colecione as que visita.
```

Full description:

```
Ao visitar Lisboa e passear pelos seus jardins, dava constantemente com árvores antigas enormes e lindíssimas, e queria uma forma de encontrar mais. Assim nasceu a Ancient Trees: um mapa de árvores notáveis que merecem uma visita, esteja onde estiver.

Um teixo mais velho do que a igreja ao lado, um plátano que são precisas quatro pessoas para abraçar, um carvalho que viu tudo o que aconteceu na sua rua.

ENCONTRAR
• As árvores antigas perto de si, num mapa
• Pesquise por local, espécie ou nome
• Direções até ao tronco

DESCOBRIR
• As árvores no seu melhor este mês, esteja onde estiver
• As árvores mais antigas, mais altas e mais grossas
• Cidades de árvores em todo o mundo

COLECIONAR
• Fotografe uma árvore à sua frente para a juntar à sua coleção
• Guarde uma lista das árvores que quer visitar
• Adicione uma árvore que ainda não está no mapa
```

## Japanese, ja-JP

App name:

```
Ancient Trees: 巨樹マップ
```

Short description:

```
近くの見事な古木を探して、訪れた木をコレクションしよう。
```

Full description:

```
リスボンを訪れて公園を歩いていると、何度も大きく美しい古木に出会いました。もっと見つける方法がほしくて生まれたのがAncient Trees。どこにいても、訪れる価値のある見事な木がわかる地図です。

隣の教会より古いイチイ、四人でやっと囲めるプラタナス、通りで起きたすべてを見てきたオーク。

見つける
• 近くの古木を地図で
• 場所・樹種・名前で検索
• 幹までの道案内

発見する
• 今月見ごろの木を、どこにいても
• いちばん古い木、高い木、太い木
• 世界各地の木の名所の街

集める
• 目の前の木を撮影してコレクションに追加
• 行きたい木をリストに保存
• まだ地図にない木を追加
```

## Graphics, in out/play/ on the Mac

- `icon-512.png`: the app icon, 512 by 512, from the iPhone's AppIcon art.
- `feature-graphic-1024x500.png`: the logo with its name on the site's own
  ground, made only from site/public/assets/press/ancienttrees-logo-with-name.png.
  It is plain on purpose: Play shows it behind a video or at the top of the
  listing, and a photograph of a tree there is a design decision that is yours.
- `phone-*.png`: phone screenshots, 1080 by 1920, from the release build on the
  emulator, signed out, the same scenes as the iPhone listing.
