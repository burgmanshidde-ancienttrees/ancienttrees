# How Hidde actually writes: his own mails, verbatim

Not rules about his voice. His sentences. Written 2026-08-11 after a day in
which eight separate rules about his register were recorded and every next
draft still failed on a new axis. Rules produce a reconstruction; proximity
produces a voice. **Read this before drafting, and imitate by proximity.**

## The division of labour that works

Three times today he supplied a few lines and the mail was right immediately.
Every draft I built from principles had to be rewritten. So:

- **He writes the substance**, even roughly, even with typos.
- **I render it**: into the other language, with the facts checked, the link
  verified, the claim confirmed true, and `mailcheck.py` run over it.
- **My value in a mail is not the prose.** It is knowing the tree is already
  live and at which URL, that the register never held the Kaisereiche, that
  the conservancy does not own that ground, that a name may not be published,
  that a blog carries no licence. That is the half he cannot do quickly and
  the half that keeps him out of trouble.

When drafting cold is unavoidable, **aim for 60% of the length that feels
right**. Every draft of mine has been too long; adding is easier than cutting.

## His own mails

**To Jon Pattee, Rock Creek Conservancy, after a correction (English):**

> Hi Jon,
>
> Thanks for your reply - and sorry for the wrong assumption. Just as one tree fan to another - if you have any suggestions for cool trees that could be on the DC map I'd love to hear from them and add them to the list.
>
> Thanks either way,
> Hidde

**To Wolfgang Schürmann, Baumkunde.de (Dutch, for me to render in German):**

> hoi wolfgang - ik woon in baarn een klein stadje vlakbij amsterdam in nederland. ik heb de duitse bomen nog weinig gezien maar kom ze graag eens bekijken.
>
> ik probeer met deze app data vanuit allerlei registers bij elkaar te brengen. vandaar dat ik emt hoofdsteden begin. maar uiteindelijk zal ik het liefst alle steden toevoegen.
>
> Je zou me op twee manieren kunnen helpen. is er een duits register waarvan ik data kan gebruiken over bomen. En heb je persoonlijk tips voor de mooiste bomen in munster? dan kan ik die stad morgen toevoegen!
>
> Dank voor de hulp so far en fijne avond

**To Paulo Araujo, Dias com Arvores (Dutch, for me to render in Portuguese):**

> paula super bedankt voor je mail.
> ik heb de boom gelijk toegeveogd zie link.
>
> Ik zie je verdere commentaar graag tegemoet. Mocht je nog andere bomen vinden missen - of tips hebben voor andere portugeze stede hoor ik het graag.
>
> ik ben aan het begin van mijn werk om alle regisers aan elkaar te koppelen en hoop uiteindelijk alle steden toe te veogen dus alle hul pis welkom

**To the Woodland Trust, opening a reply he rewrote himself:**

> thanks for coming back to me so cquickly. www.ancienttrees.app is live now as a website and im working on making an ios and android app at the moment while gathering data.

## What is audibly true of all four

Short sentences, often run together. Exclamation marks where he means them.
Contractions and typos, because he is typing, not composing. He gives something
before he asks: where he lives, what he has already done, why he starts with
capitals. An ask is one sentence with no justification attached, and often
carries its payoff ("dan kan ik die stad morgen toevoegen!"). He closes warmly
and briefly.

**Capitals, ruled 2026-08-12: "waarom gebruik je geen hoofdletters, kun je dat
vanaf nu doen als elk fatsoenlijk persoon".** This paragraph used to open with
"Lower case openings" as a trait to copy, and that was the wrong lesson pulled
from the right evidence. He types quickly to ME, in chat, where lower case is
speed. A letter going out under his name to a journalist, a register moderator
or a city office is not that; it is his shopfront, and a mail that opens
"hoi roel, ik ben er nog even ingedoken" reads as careless rather than warm.
So: sentences start with a capital, names and places carry theirs, and
`mailcheck.py` fails a draft body that does not. Everything else here stands.
Copy the shortness, the directness, the giving-before-asking, and his typos in
the sense of unfussy phrasing, never in the sense of leaving a mail unpolished.

And what is absent: no sentence that announces what the next sentence will do,
no apology beyond a single inline sorry, no explanation of how the site works,
no claim about what will never happen.

## Two ways I made a reply lomp (2026-08-21, Quercus Lisboa)

Silvia Moutinho of Quercus wrote back warmly, offered to look at the Lisbon
trees, offered to promote the platform at one of their field activities, and
offered a conversation. Hidde wanted the promotion and the tips and not the
conversation. My draft said so out loud: "por agora não é preciso marcarmos
uma conversa". His verdict: "wow wat een lomp antwoord... dit is veel te direct
dat moet je gewoon professioneel negeren of overheen praten."

**Never write down the offer you are declining.** Answer the parts you want,
warmly and concretely, and leave the rest unmentioned. Nobody chases a reply
for the paragraph that was not in it, and a mail that refuses something is
remembered for the refusal. If the meeting matters to them they will ask again,
and then it is a real question rather than one you invented and rejected.

**One ask per mail, and only one.** The same draft asked for a link on their
site and then pointed at /contribute and then put a third url under the
signature. "Je vraagt twee keer om een link dat is te desperate." Two asks read
as need, and need is the posture that loses these people. Where the other side
has already offered something, the ask is not a new one at all: accept theirs
and name the form it could take, following their lead rather than opening a
second front.

**And no sentence that promises to arrange something unnamed.** The rewrite
still ended the paragraph with "diga-me o que precisa de mim e eu trato do
resto", and he cut it: "wij regelen de rest, wat moet er dan geregeld worden,
haal maar weg." There was nothing to arrange, so the sentence was there to
sound willing. It is the same fault as the sentence that announces what the
next sentence will do, and the same fix: say the concrete thing or say nothing.

**And never point a live correspondent at the contribute form.** "Vraag gewoon
om fotos, stuur ze niet perse naar die contribute pagina." A person who has
written to us is the best channel there is; a form turns them back into a
stranger filling in fields, and their photograph arrives without the thread it
belongs to. Ask in the mail, let them reply to the mail.

All four are now in `scripts/mailcheck.py` (DECLINING WHAT THEY OFFERED,
ASKING TWICE, PROMISING UNNAMED WORK, FORM LINK IN A LIVE THREAD); ASKING
TWICE reads
data/outreach-sent.json so it knows what this address was already asked.

## Ask plainly, and never dress our ask as their benefit (Hidde, 2026-08-29)

A draft to Blarney Castle asked for a link like this: "a lot of people arrive
at Blarney for the castle and have no idea the yew and the red cedar are there.
If a mention or a link somewhere on your site would fit, it would help those
trees get looked at, and I would be glad of it either way." His answer: **"feels
a bit deceiving, just ask for help."**

He is right and it generalises. The link is for US. Presenting it as a favour to
the trees, or to their visitors, is a way of not asking while still asking, and
a reader who spots it trusts the rest of the mail less. The plain version is one
sentence and says what it wants: "And one ask, plainly: would a link to us fit
somewhere on your site? It would help a lot in getting the map found."

Note what this does NOT contradict. Batch 006's mention line frames the ask
around the trees on purpose, and that line is true of the recipients: every one
of them is a tree society whose own purpose is getting trees noticed. The
failure here is different, and worth naming precisely: **inventing a benefit to
them that we do not know they want**, in order to avoid saying we want
something. When the benefit is real, name it. When the thing is simply an ask,
ask.

## Do not answer a charge nobody made (Hidde, 2026-08-31)

The City of Sydney declined to licence their register, politely, and gave their
reason. The draft reply told them "none of the Sydney trees we publish came
from the Register anyway". His verdict: **"you sound like a child defending
that we didn't use the register."**

Nobody had accused us of anything. The sentence existed to make us look clean,
and the word "anyway" is the tell: it answers an objection that was never
raised. This is the defensive habit already recorded in memory, and it survives
best inside otherwise good mails, so the check is a question rather than a
word. Before a sentence about what we did NOT do, ask: did they say we did?
If not, cut it.

## THE SHAPE OF A REPLY (Hidde, 2026-08-31: "onthou deze vorm")

Read this before writing any answer to somebody who has written to us. It is
distilled from a fortnight of his corrections, and every line below is one he
actually made.

**Four to six lines. Under 150 words.** If it is longer, something is being
defended, explained or sold. The good ones this fortnight run 89 to 130 words;
the ones he sent back were 228 and 359.

**The order.**

1. **Thanks, and the answer, in one line.** No compliment with a justification
   bolted on, and never their own title recited back at them ("venant du
   président de l'association qui a créé le label" was struck).
2. **What changed, if they corrected us.** Say it as fact, name what the page
   says now, and stop. One short sorry inside a sentence is the whole apology.
3. **What is true about us, only if they raised it.** The paid tier, the
   distance we work from, the app. Plainly, no defence.
4. **One ask, last, in plain words.** "Would a link to us fit somewhere on your
   site?" beats any version that explains how it would help them. One ask, not
   two.
5. **Out.** No summary line, no promise about what happens next.

**Never in a reply.** A sentence about what we did NOT do, unless they said we
did. A forever-promise about price, unless he made it himself that day. A
number for the price, a date for the app. How we verify anything. A second ask
because the first one felt small. A benefit invented on their behalf.

**Do first, then write.** Every reply that landed well this fortnight reported
a change that had already shipped: the lorry out of the Olifantsiep, the five
Amsterdam trees pulled, Park Guell's access corrected, the cedar photograph
live. "Fixed, here it is" is worth more than any paragraph of intent.


## Do not brief the expert who wrote to you (Hidde, 2026-09-18)

Hugo Verissimo of Quercus Lisboa, an arborist, wrote that he would pick a zone
of Lisbon where trees are already mapped, photograph them for us and share the
walk on their channels. My draft handed him a route out of our own walk planner
(eleven trees on a line, Campo Santana to the Jardim da Parada, 4.5 km), the
22 Lisbon trees without a photograph, and a yes to the promotion. His verdict:
**"dit hele stuk hoeft niet - dat weet hij beter dan ons."**

Two separate faults, and the first is the one I keep making. **Facts we hold
are not automatically a gift.** He lives there, he does this for a living, and
he had already said he would choose the zone with care; our route is then not
help, it is a stranger marking his homework, and it is the longest paragraph in
the letter. The test before any paragraph of ours: does he know this better
than we do?

And the second: **do not confirm what somebody already told you they would
do.** He said he would photograph and promote. Writing "yes please" to that
adds nothing and reads as though it needed our permission.

What this does NOT retire: giving before asking. His own mails still open with
where he lives and what he has already done. The difference is that those are
facts about US, which the reader cannot have, rather than facts about THEIR
city, which they already hold.

## The app is live, so say so (Hidde, 2026-09-03)

"onze app staat live dus vertel dat en we zijn beniewud wat ie er van vindt",
and then, so it is not one mail: "stuur dat nu altijd maar mee met de komende
mailtjes."

So every outbound mail from here carries two things: that the app is live, and
that we want to know what they think of it.

https://apps.apple.com/nl/app/ancient-trees/id6806177833?l=en-GB

Note it is a real question rather than a second ask, which is why it survives
the one-ask rule: we are not asking them to do anything, we are asking what
they made of it. Keep it to one line and let the link stand on its own.

**One exception so far, and he named it himself the same hour: "behalve naar
paulo die heeft gezegd dat ie geen tel heeft."** Paulo Araujo told us on
2026-09-02 that he has no smartphone, cheerfully, and inviting him again would
read as not having listened. The exceptions live in `NO_APP_LINK` in
scripts/mailcheck.py, which fails any draft written from today without the
link and skips anybody on that list.

## Follow the local expert, do not correct them (Hidde, 2026-10-09)

Kerry Pickett answered the Brighton help-ask with three facts about the Preston Twins. Two did not hold up against what I could find online (the manor had left the bishops by 1613, and Seaford used the elm vaccine before Brighton did), and my reply said so politely and asked for her source. His verdict: **"ga niet in discussie hij is een lokale held volg hem en zeg dat we het hebben veranderd."**

Somebody who has lived beside a tree for decades and answered our cold mail is worth more than a web search. Put what they gave on the page, written as a local account rather than as our own claim, keep any doubt in verify_notes, and reply "it is on the page now". A reply that checks their homework is a reply they never answer again. Hard rule 2 still holds, which is why the page says "local accounts" rather than presenting the fact as ours.

## Five corrections in one afternoon (Hidde, 2026-10-13: "learn from my feedback plz")

Each is the 10-10 rule below, broken in a new way. Read this section before drafting any reply.

1. **A tree they name is a tree to finish, not a lead to file.** I wrote Simon (Friends of Cammo) "both are on our list now". Hidde: "wees niet zo lui met dingen in leads zetten". Ask what it lacks to go live: where exactly it stands.
2. **Ask only what someone does in passing.** "Do you have a photograph we may use, with your name under it?" was "weird". His version: if you ever walk past, a photo with our app would be amazing. "If anyone ever measured the trunks" got "wtf": never give a volunteer a task (mailcheck now refuses measuring asks).
3. **A referral is a thread, not an end.** Sally sent us to Gavin Coates and I replied "Thanks, I'll ask him." Hidde: "kunnen we niet meer uit sally halen". Ask for the introduction, and ask for her own tree.
4. **Say plainly what we look for; do not flatter their work.** My "After painting so many of them, I'd love to hear your favourite" became "we're just looking for remarkable old trees in Hong Kong. Any favourite of yours we should add to the platform?" Correct the misunderstanding (she thought we only wanted wall trees) by stating what we want, then the ask.
5. **Take a suggestion warmly and leave the door open.** To Noeleen's "get an expert botanical review" he wrote: "Thanks for your feedback, and good idea, we're going to follow that up. If you have any other tips about the platform, they're all welcome, we've only just started." Also Judith: thank her for forwarding, never "I already knew that one" ("niet bijdehand doen").

## Thank them more than once (Hidde, 2026-10-19: "zeg vaker bedankt")

On a reply to a reader who reported a dead yew and had sent photographs of two other trees. Thank them for each thing they gave, in its own sentence (the report, the photographs), and close with "Thanks again". Generous thanks is not the repeated thanks the copy-check warns about: that is the same thank-you pasted twice for one thing.

## The tree ask goes once per thread (Hidde, 2026-10-20)

A thank-you to Richard Weddle (he had pointed us to the Glasgow Treelovers) closed with "Is there a Glasgow tree of your own?", though our first reply had already asked for help adding trees. His verdict: **"just say thank you, stop asking for more tree input when this already happened earlier in the conversation."** Read the thread before adding the ask. If it was asked once, the reply is a thank-you and stops. mailcheck's ASKING TWICE catches it.

## Every reply activates, with the ask that fits the person (Hidde, 2026-10-10)

"we moeten mensen een beetje activeren naar of de app downloaden of controleren of ambassadeur. net wat gepast is." A thank-you alone ends the thread. Close every reply with the one ask that fits who they are: a forester or arborist is asked which tree we miss; a local enthusiast is asked to check the list or offered the ambassador role (described honestly, see drafts/ambassador-mails.md); somebody walking past trees is pointed at the app. One of them, never all three.


## Calibration 2026-10-15: a careful expert who asks who we are (Dr. Joachim Bauer, SDW Koeln)

Hidde rewrote my draft, which answered Bauer's questions as facts about the data and then asked for his list. His version: "Ik ben Hidde, ik woon in Baarn, vlak bij Amsterdam. En laat ik gelijk eerlijk zijn: ik ben geen bomenexpert, maar een fan van bomen." Then honesty that the selection criteria are still being found ("bomen die de moeite waard zijn om een detour voor te nemen"), the goal (not botanically perfect, but a large public interested in trees), and the ask turned into a request for his opinion and advice, with help finding trees last. Lesson: when an expert is wary, answer as a person and ask for his judgement; do not defend the method or ask for his material first.

## Calibration 2026-10-21: a network that offers to cooperate (Harald von der Stein, N-BfB Koeln)

Harald asked what would help and how we picture working together. My draft listed what we look for, asked for three trees and left the cooperation unanswered. Hidde rewrote it: thank him for the long reply and for wanting to help; we are still building, so trees, locations, photos and stories all help; sharing the app in their newsletter or a link on their site helps enormously; walks one day, still the future; an online call is welcome, in English or Dutch since he speaks no German. Lesson: when someone offers cooperation and asks how, answer every part of the question generously; their offer is the occasion for the newsletter and link ask, and a call they hinted at is accepted, not stepped around.

## When they say they have little time, ask for nothing (Hidde, 2026-10-22)

Katherine (National Trust Victoria) wrote that the Trust is "very time poor" and could not offer a person, while still offering to look for a sort of tree if we named one. My draft took that offer up and asked her to pick a handful of trees from the Register. His verdict: **"she kind of turned down the offer, so asking this is a bit too much. You do that more often: if they already state it's too much, don't ask for more."**

Then he wrote the paragraph himself and named the strategy: **"telling them how they can help but expecting nothing and staying kind."**

> I completely understand your time constraints. If someone does have time, telling us which trees are missing, or taking a photo with the app when walking past one, really helps. That's why we built the iOS app: [link]
>
> What would also really help is sharing the app on your website or in an email, so more people go out and take pictures.
>
> Either way, thanks for your help so far, and have a lovely day.

So when somebody says they are busy but leaves an opening: first say you understand, without a "but". Then name the ways anyone could help as options ("if someone does have time"), not as a task for them: missing trees, a photo with the app in passing, sharing the app on their site or in a mail. Close with "either way, thanks" so nothing hangs on it. The App Store link belongs here, in the sentence about the photo ("het is geen harde weigering, je moet m goed plaatsen"): a reason beside it, never as a plug on its own at the end. mailcheck lets it through only in that paragraph. Never set them a specific job (pick a handful, check the list). This is the one place where more than one way to help is fine, because nothing is being asked of them in particular.

## His standard intro: who we are (Hidde, 2026-10-22; replaced for first mails 2026-10-29)

**A first mail to a stranger uses the agreed text, word for word, and nothing new** (Hidde, 2026-10-29, on the Ottawa archive mail's Lisbon line: "use my personal words or once we agreed on instead of making up new sentences that again feel ai"):

> My name is Hidde, I live in Baarn near Amsterdam. I'm building Ancient Trees, a worldwide map of remarkable old trees worth a walk. My goal is to get people excited about old trees and get them outside to go and see them.

then the one thing that concerns them, the ask, "Thanks,\nHidde", and Wilder only as the P.S. in its agreed form (drafts/nature-template.md). The Lisbon origin story stays out of first mails; it is in the Wilder article. Two sentences for who and what ("this sentence is way to long", same day). The only sentences a session writes itself are the ones about their trees and the ask; everything around them is copied. mailcheck's ORIGIN STORY IN A FIRST MAIL and INTRO IN ONE LONG SENTENCE.

The Peter Raggers intro below is kept for replies to someone who asked who we are.

When a mail has to say who we are (a first mail, or somebody who asked), reuse the intro sent to Peter Raggers on 2026-10-21. Hidde: "the intro you gave to Peter yesterday was better, please remember that one and reuse." My "I'm Hidde, I live in Baarn, about 30 minutes from Amsterdam" on its own "makes no sense": where he lives only works joined to what he does ("and I work on Ancient Trees").

- NL (as sent to Peter): "Ik ben Hidde, ik woon in Baarn en werk aan Ancient Trees, een website en app met bijzondere oude bomen die de moeite waard zijn om naartoe te lopen. Het begon in Lissabon, waar ik tijdens werkreizen door de parken liep en me verwonderde over de oude jacaranda's en vijgenbomen. Ik ben geen bomenexpert, maar wel een grote fan, en ik wil het voor anderen makkelijker maken om zulke bomen te zien."
- EN: "I'm Hidde, I live in Baarn in the Netherlands, about 30 minutes from Amsterdam, and work on Ancient Trees, a website and app with remarkable old trees worth walking to. It started in Lisbon, where I walked through the parks on work trips and wondered at the old jacarandas and fig trees. I'm not a tree expert, but a big fan, and I want to make it easier for others to see trees like these."

Outside the Netherlands add "in the Netherlands, about 30 minutes from Amsterdam" after Baarn (Hidde, 2026-10-22, on the reply to Stacey in Glasgow: "the 30 min from amsterdam is relevant, its not relevant for dutch peeps"). A Dutch mail never mentions Amsterdam: Baarn is enough. mailcheck's AMSTERDAM IN A DUTCH MAIL. The intro already says "worth walking to", so the standard line below is for when they ask which trees, not stacked on top of the intro.

## Open with a sorry when we may have misled them (Hidde, 2026-10-22: "leer menselijk worden")

Stacey (Glasgow) asked where he is based and whether he has a connection to Glasgow or Scotland. I cut his sorry because she had not accused us of anything. His verdict: "ik zou wel openen met iets van een verontschuldiging als ik die impressie heb gemaakt". When their question shows our mail may have given a wrong impression, the reply opens with one short sorry for it, in the thanks line: "Thanks for your reply, and sorry if my mail gave the impression that I'm from Glasgow." This is not the "answer a charge nobody made" fault: that one defends us, this one is a person being polite. One sorry, at the start, then the answer.

## His standard ask to an expert: judge the list (Hidde, 2026-10-22)

My ask to John Beetham ("Which trees in Melbourne, or anywhere in Australia, do you think we are missing?") was "not very strong". He rewrote it: show the page as work in progress, ask them to judge the selection both ways (are these good, what is missing, what does not belong), then photos as a later wish, and out kindly.

> I've been working on the Melbourne page, and you can see where it stands, with 16 trees so far, here:
> https://ancienttrees.app/melbourne
>
> I was hoping you could help me improve this list. Have a look at the trees I've selected so far: do you agree they're good ones? Are some missing, or do some not deserve to be there?
>
> Eventually I could really use some help finding or taking photos of these trees.
>
> Either way, have a lovely day,
> Hidde

Why it is stronger: it asks for their judgement on something concrete we made, which an expert enjoys giving, instead of an open "what are we missing", which asks them to do the search. Use this for anyone who knows a city's trees (first mails and help asks), with the city and count filled in.

## His standard line: which trees, and for whom (Hidde, 2026-10-22)

When somebody asks what counts as "ancient", or which trees we pick, use his line, not a list of criteria. He has used it before and wants it as the standard. Its first outing was to Dr. Bauer (2026-10-15), who passed it on to Harald von der Stein, and Harald then offered to cooperate.

- EN, verbatim, nothing added before or after it (Hidde, 2026-10-22: "gebruik dit gewoon veel sympathieker"): "For now the definition is a tree worth walking to. For tree experts, but just as much to get a wider public excited about going outside to see one."
- NL: "De definitie is voor nu: een boom die het waard is om voor om te lopen. Voor boomexperts, maar juist ook om een breder publiek enthousiast te maken om naar buiten te gaan."
- DE (as sent to Bauer): "Am Ende geht es mir um Bäume, für die sich ein Umweg lohnt und die man gern besucht. Mein Ziel ist, ein größeres Publikum für Bäume zu begeistern."

The line works because it is a definition anyone can test by standing in front of a tree. Do not add biggest, oldest or rarest as a checklist after it. If they offered one of those, take up the offer in the ask instead.

## Calibration 2026-10-25: following up someone who offered to be ambassador

New York, Buçaco and Porto pressed "become the ambassador" and got the automatic mail with the three-task list, then went quiet. My follow-up gave the full standard intro and asked for their favourite tree. His verdict: **"the mail is rubbish. they had the list of things to do"**, and he wrote it himself:

> hi name, thanks again for wanting to help make the list for city better. im super curious about what you think of the list so far but also the product in general. the product is quite new so any feedback is super relvant for me. either way thanks for the help again and looking forward to stay in touch the comming time. Thanks, Hidde

Lesson: someone who already offered and already has the tasks is not a stranger to introduce yourself to or to give a new question. Thank them again for wanting to help, ask what they think of the list AND the product, say it is new so their feedback matters, and close with "either way" and staying in touch. No intro, no link, no new ask. Use their first name when their sign-in gave one.

And when he hands over his own text, **fix grammar, spelling and capitals only**. My render swapped "the coming time" for "in the coming weeks" and, in Portuguese, "the product" for "Ancient Trees"; his verdict: "je hebt de mail niet beter gemaakt ... minder authentiek, kun je mijn woorden alleen grammaticaal verbeteren". His words, his "super", his phrasing stay; a translation follows his words as closely as the language allows.

## Calibration 2026-10-15: a journalist who asked who you are (Wibren, Omrop Fryslan)

I added a Leeuwarden line (34 trees live) and the app link to his own short answer. His verdict: "dat van leeuwarden weet hij al, dat van die app hoeft er ook niet in." A journalist asking about the person gets the person: answer his questions, give the phone number, stop. Do not add what he already knows, and the app line is not automatic in a press reply. (Superseded 2026-10-22: a Dutch mail mentions no Amsterdam at all; see "His standard intro".)

## Calibration 2026-10-22: a Reddit post to a city subreddit (r/Lisbon)

My draft had a bold-free but numbered ask list, "Two things I could use help with:", and register names in brackets; Hidde said Reddit readers spot AI text and "je moet echt je best doen als mij over te komen". He wrote his own:

> I'm mapping Lisbon's oldest trees - any suggestions?
>
> I used to travel a lot for work and loved visiting the parks when I had some time to kill. Since then I've been keeping a list of old trees worth a visit. There are 36 so far. Jardim da Estrela and Jardim Botânico da Ajuda were my favourite parks.
>
> A few of the oldest ones still don't have a good photo though. The big plane tree at Hospital Pulido Valente in Lumiar (apparently 364 years old) and the olive in Santa Iria de Azoia, which is supposed to be almost 3000 years old. If anyone lives near one of those I'd love a photo.

Lesson for every post where a stranger reads him: start from his life, not the product ("time to kill" on work trips); name places he liked, not facts we hold; numbers rounded and hedged the way a person repeats what they read ("apparently", "supposed to be almost 3000"); short plain paragraphs, no bold, no lists, no colon reveals; at most two asks, and end on a question. No link in a subreddit that bans self promotion; it goes in a comment when somebody asks. Draft in this shape and let him put one sentence of his own in before it goes out.

## Calibration 2026-10-23: a one-line answer in a Reddit thread (lov-a, "are you using ArcGIS?")

My draft: "No, it's my own little map. I started from the national list of protected trees and add the ones people tell me about, like in this thread." His: **"no i made this myself starting from the national list of protected trees and adding new ones myself"**. Two things went: "little" (self-diminishing, the mailcheck habit in a new coat) and "like in this thread" (a flourish that compliments the thread back). What stays is the plain fact, said once, "myself" twice because that is the answer to the question. A comment reply is one sentence that answers what was asked and stops.

Same thread, same day, on telling xpto47 how to spot the Bensaúde cork oak. My "you'll know it by the thick cracked cork bark" stated it as knowledge. His: **"ik heb m ook niet gezien maar je schijnt hem te kunnen herkennen aan"**. So: "I haven't seen it myself either, but apparently you can tell it by the thick, cracked cork bark." He has not stood there, and a stranger on Reddit can tell; what we read is said as read ("apparently"), the way the post itself says "apparently 364 years old".

## Calibration 2026-10-23: the list-shaped city post (r/sicily), his cut

My draft gave every bullet a fact ("half of it sick so go while it's there", "where people have left notes since 1992", "planted over a Roman mosaic"). He kept the fact on two bullets only, the two that are the hook (the Orto Botanico crown, the 2,000-year chestnut he has not seen), and cut the rest to names: "The ficus on Piazza Marina", "The dragon tree at Villa Malfitano". His close: "Which ones should I add and photos of the trees would be great :) Thanks!" So: in a list post the bullets are names, a fact only where it makes someone click, and the ask is one plain sentence with a smiley, not two sentences.

## Calibration 2026-10-23: replies under a tip thread (r/sicily)

Two lessons from his own hand. (1) Photos: my drafts asked nearly every tipster for a photo; Hidde: "is het niet gek om iedereen om fotos te vragen als ze overduidelijk ze niet hebben". The post already asks once; a reply asks the one thing that person can know (where in the park, can you walk in), never a photo by reflex. Hidde, 2026-10-24, on the drafts that then asked nobody: "we can do photo requests if its natural". So ask when this person plausibly stood there and could have one (they visited, walked past, "was just there"), and skip it for a memory, a hearsay tip or a link. Same day: "i rather not answer if you just make conversational comments that dont go anywhere". A comment gets a reply only when the reply moves a tree forward (a spot, access, a photo, a page link); a remark, a challenge or a passing question gets none. (2) AI: when someone in the thread raises AI, he says it plainly himself: **"Thanks! To be honest, I did consult ai to improve the list but think in the end humans are way better in doing it"**. True to the product (every tree page says the story was written with AI), said once, no defence.


## To a Commons photographer whose photos lead our pages (2026-10-26, his own text, "doe ze zo")

> Hi,
>
> Just to let you know: we happily use three of your Lisbon photos on Ancient Trees. My name is Hidde and I'm building Ancient Trees to map all old trees worth a detour, to get a broader audience to enjoy nature.
>
> These are online
>
> <links>
>
> Thanks for taking them! And very curious what you think of the platform.
>
> Thanks,
> Hidde (ancienttrees.app)

No ask beyond their opinion. He replaced my version, which ended on a request for more photos.

## Calibration 2026-10-27: a guest article for a magazine (Crann, Declan O'Brien)

The sent article is drafts/crann-article-2026-10-final.md, its covering mail drafts/reply-declan-crann-2026-10-27.md; start any later article or press piece from it. What he changed, in his words or his edits:

- **The covering mail is three lines and hands the editor control**: "Sure, I got right to it. Here's a first version about 600 words. I'm not a writer or an editor, so please tell me honestly what you think and change whatever you like." Photo credits listed plainly beneath; signed "Let me know what you think, Hidde". No extra ask (he cut the King Oak photo request).
- **He is "a Dutch tree fan", not "a designer"**: he struck "I'm a designer" from the body, and the standfirst followed.
- **"Ticked off" is out ("i dont lik ticked off")**: the product verbs are find, walk and collect.
- **No invented plans**: "I'm planning a trip to Ireland" was his own line and he withdrew it ("im not planning a trip"); never write a visit, trip or memory he has not given.
- **Title and standfirst never repeat a phrase** ("worth a detour" twice "does really overlap"); "worth a visit" was the same echo.
- **A fact in his article is checked against the cited source, word by word** ("is this bullsht how did yo come up with this?" on the King Oak): the brief's "bow to the ground" and "the owning family" went beyond Wikipedia and its Irish Examiner and Irish Times sources, and were replaced.
- His own story sentences (Palermo fig, Lisbon parks, "not a tree expert, just a big fan", "Each tree has a story that only locals know") stay verbatim; edits to them are grammar only.

## Calibration 2026-10-27: a last word from them is not a reason to write (four drafts, one kept)

I drafted four replies from the owed list: an ambassador ask to James Kearney (UNLV, mid-way through sending photos), a thank-you to Andreas Groeger for "no photos, sorry", a thank-you plus a product question to Ines (Wilder) for explaining her Bucaco test, and a reply to Fred van Holland, who declined the ambassador role. His verdict: **"all these mails are unnecessary except the one to fred."** Then he gave Fred's content himself: thank him, say we understand, without any pressure a tip or photo is more than welcome, thanks again for the help.

Lessons. (1) The owed list counts who wrote last, not who is owed: a short closing line (no photos, a clarification, "will do") needs no reply, and a thank-you to it only adds a mail. (2) Do not open a new ask (ambassador) with someone who is in the middle of giving; let them finish. (3) A person who says no to a role still gets the door left open, in his words: "zonder enige druk", a tip or a photo "meer dan welkom", and thanks for the help.

## Calibration 2026-10-27: accepting an offer to write for them (Esther, Bezoek Ede)

My "laat maar weten wanneer het jullie uitkomt" became his **"laat maar weten wanneer ik iets kan aanleveren?"**. When someone offers us a guest piece, the yes says what we will do (deliver something), not that we wait for their convenience.


## Calibration 2026-10-28: say it is a worldwide map (archive asks)

On the NDV draft: **"mss goed om te noemen dat het een wereldwijde kaart is in de opening want mensen denken ah nederlandse kaart hebben we al"**. A cold mail to a local or national organisation says in its opening sentence that Ancient Trees is a worldwide map (with the city count), so they do not file it as one more map of their own country.


## Calibration 2026-10-28: his own typed text stays as he typed it (Northern Woodlands)

When Hidde writes a mail himself for an outlet that refuses AI-written pitches, I do not correct it: **"hou mijn spelfouten en letterlijke tekst aan dan lijkt t geen ai"**. Give his text back verbatim; at most point out a wrong address or a broken link.
