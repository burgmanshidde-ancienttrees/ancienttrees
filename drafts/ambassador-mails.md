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

<!-- Hidde's own words, 2026-10-02 ("zoiets?"), rendered. The reader of par_031 and par_033; no name known; address jd84vvjkvb@privaterelay.appleid.com, an Apple relay, so send from the ancienttrees.app sender, never a personal one -->

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

<!-- Daniel Daggfeldt, arborist, Trädmästarna, daniel@tradmastarna.se. Third mail in the thread: the first (09-10) answered his corrections, the second (09-24) asked about the app in Prague. Hidde, 2026-10-02: "you can email daniel if you want there is much to gain there". Reply in the same thread, Tina Axelsson stays cc'd as he put her there. Not pre-granted: the mail asks. -->

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
