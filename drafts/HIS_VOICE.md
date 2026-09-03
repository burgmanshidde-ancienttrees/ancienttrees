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
