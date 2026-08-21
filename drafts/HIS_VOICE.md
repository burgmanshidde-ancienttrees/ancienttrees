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
