# Ambassador mails: thanks, what do you think of the list, want to carry it?

Hidde's idea, 2026-10-02. **Since the same evening the Paris mail is the STANDARD invitation and the knock sends it** (`scripts/ambassador.py --invite-scan --send`, signed Ancient Trees) to any reader whose photograph is live in a place without an ambassador; the Paris and Seville readers are the first two. The badge follows their answer. Daniel's mail below is personal and his to send; Leon gets none. Three people
have actually given us trees or photographs and can be reached today. The
Paris reader signed in with Apple, so their address is a privaterelay.appleid.com
one: mail to it only arrives from the ancienttrees.app sender the relay knows
(the one contributor_reply.py uses), never from a personal address.

The ask at the end is the same in all three and it is the one that matters: can
they add more. The tag is offered as a question, never applied.

---

## 1. Paris

<!-- Hidde's own words, 2026-10-02 ("zoiets?"), rendered. The reader of par_031 and par_033; no name known; their address is an Apple relay on the account, so send from the ancienttrees.app sender, never a personal one -->

```
Subject: Your Paris trees

Hi,

Thanks so much for adding the horse chestnut and the Turkey oak of Square René-Le Gall. They are live, for everybody to see.

We would love to make you our ambassador for Paris: somebody who adds photos, checks the facts and helps sharpen the list. What do you think of our list, is it missing any, are some wrong? Let us know if you are up for it.

Thanks,
Hidde
```

## 2. Friedewald and Bad Homburg: no mail

Hidde, 2026-10-02: "to leon dont send because it makes no sense after our conversation". Leon is already in a running thread with him; the scan skips his account (the `*` entry in data/ambassadors.json).

## 3. Copenhagen and Porto: no mail

Hidde, 2026-10-02: "dont email paulo or hans ive had much contact with them just make them ambassador". Hans Erik Lund (Copenhagen) and Paulo V. Araujo (Porto) are made ambassadors directly, named on their city pages, with `python3 scripts/ambassador.py --grant-named`. Neither has an app account; the badge reaches them the day they make one.

## 4. Stockholm

<!-- Daniel Daggfeldt, arborist, Trädmästarna. Third mail in the thread: the first (09-10) answered his corrections, the second (09-24) asked about the app in Prague. Hidde, 2026-10-02: "you can email daniel if you want there is much to gain there". Reply in the same thread, Tina Axelsson stays cc'd as he put her there. Not pre-granted: the mail asks. -->

```
Subject: Re: Stockholm trees

Hi Daniel,

Thanks for the pin on Valkasken and for the corrections to the Prins Eugen oak. Both pages now say what you told us: the oak is the largest in the city, and hollow.

We are starting with ambassadors: one person per city who adds photographs, checks the facts and helps sharpen the list, named on the city's page. Would you be up for Stockholm? You have already done most of it.

Two small asks while you are passing Valkasken: its girth, which nobody has ever written down, and whether Tina's photographs of these trees may go on the pages with her credit. If you have the app on your phone, a photograph from there lands on the page by itself: https://apps.apple.com/nl/app/ancient-trees/id6806177833?l=en-GB

Thanks,
Hidde
```

## 5. When they answer "I was only visiting"

Hidde, 2026-10-02: "people can of course have been on a trip and respond that they're not there anymore but then we can ask them to become of their hometown". The reply, by hand, in the same thread:

```
Thanks for writing back. Which place would you look after? Your own town is the best one, and if it is not on the map yet, the trees you send are how it starts.
```

Then `python3 scripts/ambassador.py --grant <user_id> <place_slug>` once they name one we publish, or a lead for the place if we do not.

## 6. Bad Homburg and Friedewald: Leon, in the thread you already have

<!-- Hidde, 2026-10-02: "Zullen we hun ook beide vragen als ambassadeur? Maar dan met een mail die klopt in het gesprek wat we al hebben met ze?" His account is daa8cd52 (Treehunter); the address is on his account, never written here. English, as the earlier replies to him were. -->

```
Subject: Re: Schöne Eiche

Hi Leon,

Five metres it is: your measurement from last year stands, and the older figure from the Baumkunde thread stays beside it with its year.

Something we are starting: one person per place who looks after its list, adds photographs, checks the facts and says what is missing. You have been doing exactly that for Bad Homburg and Friedewald since the day you found us. Would you want to be named as their ambassador on the pages? If you would rather not be named, it shows inside the app only.

Thanks,
Hidde
```

## 7. Münsterland: Wolfgang Schürmann, in the thread you already have

<!-- Hidde's 2026-09-24 mail asked for his Münster favourite; he answered 2026-10-02 with the Kopfulme in der Beerlage. German, as the thread is. Not pre-granted: the mail asks, and the place is his to name. -->

```
Subject: Re: Kopfulme in der Beerlage

Hallo Wolfgang,

Die Kopfulme in der Beerlage ist ein großartiger Tipp: hohl, begehbar, über fünf Meter Umfang und Naturdenkmal, genau die Sorte Baum, für die Leute einen Umweg machen. Wir nehmen sie auf.

Wir fangen mit etwas Neuem an: pro Ort eine Person, die die Liste im Blick hat, Fotos beisteuert, Fakten prüft und sagt, was fehlt, mit Namen auf der Seite. Für das Münsterland fällt mir niemand ein, der die Bäume besser kennt. Hätten Sie Lust?

Baumstarke Grüße zurück,
Hidde
```

## 8. Florence: Giulia Torta, Orto botanico, in the thread you already have

<!-- She reviewed all seven Orto botanico trees, sent the Himalayan cedar's photograph with the credit she wanted, and the thread is in Italian (Lei). Hidde, 2026-10-02: "kunnen we Giulia ook niet vragen als ambassadeur?" The name on the page can be hers or the museum's; the mail asks which. -->

```
Oggetto: Re: Il cedro dell'Himalaya, online

Buongiorno Giulia,

Stiamo iniziando una cosa nuova: per ogni città una persona che tiene d'occhio la lista, aggiunge fotografie, controlla i fatti e dice cosa manca, con il nome sulla pagina della città. Per Firenze non riesco a immaginare nessuno meglio di Lei: i sette alberi dell'Orto botanico sono già passati tutti dalle Sue mani.

Le andrebbe? Sulla pagina possiamo scrivere il Suo nome oppure quello del Sistema Museale, come preferisce.

Un saluto cordiale,
Hidde
```

## 9. Washington, DC: Jon Pattee, Rock Creek Conservancy, in the thread you already have

<!-- He corrected us in August (Montrose Park and Dumbarton Oaks are National Park Service ground, not theirs) and Hidde wrote back as one tree fan to another asking for suggestions for the DC map. Hidde, 2026-10-02: "mail jon en ales maar wie weet". -->

```
Subject: Re: Rock Creek trees

Hi Jon,

One tree fan to another, a question: each city is getting one person who keeps an eye on its list, adds a photograph now and then, checks the facts and says what is missing. For Washington, you are the first person I thought of, because you were the first to catch us getting something wrong there.

Would you be up for that? Your name would go on the DC page, or the Conservancy's if you would rather. And if there is a tree along Rock Creek that deserves to be on the map and is not, I would still love to hear it.

Thanks either way,
Hidde
```

## 10. Prague: Aleš Rudl, Pražské stromy, in the thread you already have

<!-- He runs Prague's memorial-trees site, which we cite on eight Prague trees; he wrote back in August with corrections and got a thank-you on 2026-09-24 asking for a missing tree. -->

```
Subject: Re: Prague's trees

Hi Aleš,

Your corrections are all in, and Prague is one of the few pages where somebody who actually knows the trees has read every line.

We are starting something: for each city, one person who looks after its list, adds photographs, checks the facts and says what is missing, named on the city's page. For Prague that person is obviously you, if you want it. Pražské stromy would be named beside you, with a link.

Would you be up for it? And if a tree you have written about is still missing here, tell me which and it goes up first.

Thanks,
Hidde
```
