#!/usr/bin/env python3
"""Grep a draft mail for the four ways I keep spoiling Hidde's letters.

Hidde, 2026-08-11, on finding "Thanks for the correction, and sorry for the
wrong assumption. That is Park Service ground and I should not have called it
yours" in a reply he was about to send: "stop met zo fucking onderdanig zijn en
onthou dat." He had corrected the same habit twice that morning already, and I
had written it into memory in between, and then did it again. A note that fails
three times is not a note problem, so this is the mechanism instead: run it
before saving any draft.

    python3 scripts/mailcheck.py drafts/reply-rock-creek.md
    python3 scripts/mailcheck.py drafts/*.md

It checks the body only, after the --- separator, because the notes above it
are mine to Hidde and may say anything.

Four failure modes, all recorded, all mine:

1. GROVELLING. Apologising, thanking for a correction, or narrating my own
   error. One short acknowledgement is the whole of it; three is a posture.
   His rule: modesty is not honesty, and he is asking these people for
   something, so a man who introduces himself as nothing gets treated as
   nothing.
2. SELF-DIMINISHING. "Just me", "only a hobby", "no funding" as apology rather
   than fact. State what the thing IS, not what it lacks.
3. FOREVER-PROMISES. never/always/free forever. Pricing is his and undecided,
   and in a letter to a named third party it is a commitment somebody can hold
   him to.
4. PROCESS-PITCHING. Nobody outside this project cares how we verify. Say what
   they get.
5. DECLINING WHAT THEY OFFERED. Somebody offers a call we do not want. Write
   the refusal down and the mail becomes a rejection letter; talk past it and
   answer the half we do want, and nothing is lost.
6. ASKING TWICE. The same ask to somebody who already had it reads as need.
7. PROMISING UNNAMED WORK. "I'll take care of the rest" commits to nothing and
   invents an arrangement nobody asked for.
8. FORM LINK IN A LIVE THREAD. Never send a person who is already writing to us
   off to /contribute. They reply; that is the channel.

What it CANNOT check is the positive half, which is where his own drafts win,
so read this before writing rather than only after. A mail of his GIVES before
it asks: a concrete personal detail ("ik woon in baarn een klein stadje vlakbij
amsterdam", not "in the Netherlands"), a criticism turned into an intention
rather than guilt ("kom ze graag eens bekijken"), the reason behind a
limitation instead of an apology for it ("vandaar dat ik met hoofdsteden
begin"), and only then the asks, numbered out loud ("op twee manieren"),
phrased generically enough that nobody is put on the spot ("is er een duits
register" rather than "may we have yours"), with the payoff inside the ask
("dan kan ik die stad morgen toevoegen"). His own mails are collected verbatim in drafts/HIS_VOICE.md; read those
rather than rules about them, and imitate by proximity.
"""
import glob
import re
import sys

BODY_SPLIT = re.compile(r"^---\s*$", re.M)

CHECKS = [
    # NOT an apology ban. Hidde rewrote a reply himself on 2026-08-11 and it
    # opens "Thanks for your reply - and sorry for the wrong assumption." One
    # short sorry inside a sentence is human and he uses it. My first version of
    # this check flagged his own writing, which is how I learned I had
    # overcorrected: what he struck was three apologies stacked, plus narrating
    # my own error back at the reader. So flag the SELF-NARRATION always, and
    # the stacking only past one.
    ("SELF-NARRATING THE ERROR", [
        r"I should not have", r"I shouldn't have", r"I was wrong to",
        r"\bmy (?:mistake|error|bad)\b", r"forgive me",
        r"I hope (?:you don't mind|this is ok|that's alright)",
        r"if (?:that's|that is) (?:ok|alright|acceptable)",
        r"I'd be (?:very )?grateful", r"I would be (?:very )?grateful",
    ]),
    ("SELF-DIMINISHING", [
        r"\bit(?:'s| is) just me\b", r"\bjust a (?:hobby|side project|small)",
        r"\bonly a\b", r"\bnothing special\b", r"\bearns nothing\b",
        r"\bno funding\b(?!.{0,40}institution)", r"\bI'm no expert\b",
        r"\bhumble\b", r"\bsmall project\b",
    ]),
    ("FOREVER-PROMISE", [
        r"\bnever (?:be )?(?:charge|paid|behind)", r"\bfree forever\b",
        r"\balways (?:be )?free\b", r"\bnever for\b", r"\bwill never\b",
        r"\bforever\b",
    ]),
    # Third time in two days that a careful research note became a possessive
    # claim in the composed mail, and the third time the recipient corrected it.
    # Rock Creek ("ground you look after": it is Park Service land). Grün Berlin
    # ("einer davon ist Ihrer": Treptower Park is the Bezirk's). Baumkunde
    # ("2 davon sind Ihre"), where the note actually said these two trees lack a
    # photo on OUR page, and Klaus checked their register and found the
    # Kaisereiche was never in it, only a Kaiserulme. So: any sentence claiming
    # the trees belong to the reader has to be justified against
    # `owns_the_trees` in the contact file before it is sent.
    ("POSSESSIVE CLAIM (check owns_the_trees)", [
        r"davon (?:sind|ist) Ihre?r?", r"\b(?:are|is) yours\b",
        r"tree of yours", r"Baum von Ihnen", r"Bäume von Ihnen",
        r"your trees\b", r"ground you look after", r"in your care",
    ]),
    # Hidde, 2026-08-15: "remarkable = opmerkelijk in het nederlands.
    # ongelofelijke bomen nooit gebruiken is raar." The English word is
    # remarkable everywhere; the Dutch word is opmerkelijk, never ongelofelijk.
    ("WRONG WORD FOR REMARKABLE", [
        r"ongelo[fo]?[fv]?elijk", r"ongelooflijk",
        r"incredible tree", r"árvores incríveis", r"árboles increíbles",
        r"arbres increïbles", r"alberi incredibili",
    ]),
    # Hidde, 2026-08-21, on a reply to Quercus Lisboa that said in so many
    # words "por agora não é preciso marcarmos uma conversa": "wat een lomp
    # antwoord... dit is veel te direct dat moet je gewoon professioneel
    # negeren of overheen praten." She had offered a meeting; he wanted the
    # promotion and the tips and not the meeting, and the way to get that is to
    # answer the parts he wants and let the rest go unmentioned. Writing the
    # refusal down turns a warm reply into a rejection letter, and it does it
    # in the sentence a person remembers.
    ("DECLINING WHAT THEY OFFERED", [
        r"(?:not (?:really )?(?:necessary|needed)|no need|don't think we need|"
        r"niet nodig|geen behoefte|hoeft niet|n(?:ã|a)o (?:é|e) preciso|n(?:ã|a)o ser(?:á|a) necess(?:á|a)rio|"
        r"n(?:ã|a)o vejo necessidade|no hace falta|no es necesario|nicht n(?:ö|oe)tig|"
        r"kein Bedarf)"
        r"[^.!?\n]{0,70}"
        r"(?:call|meeting|chat|conversation|talk|gesprek|afspraak|belletje|"
        r"conversa|reuni(?:ã|a)o|encontro|llamada|reuni(?:ó|o)n|Gespr(?:ä|ae)ch|Termin)",
        r"(?:call|meeting|chat|conversation|gesprek|afspraak|conversa|"
        r"reuni(?:ã|a)o|reuni(?:ó|o)n|Gespr(?:ä|ae)ch)"
        r"[^.!?\n]{0,70}"
        r"(?:is not (?:necessary|needed)|isn't necessary|n(?:ã|a)o (?:é|e) preciso|"
        r"niet nodig|hoeft niet|nicht n(?:ö|oe)tig)",
    ]),
    # Hidde, 2026-08-21, on "Diga-me o que precisa de mim e eu trato do resto":
    # "wij regelen de rest, wat moet er dan geregeld worden, haal maar weg."
    # A sentence that promises unnamed work is filler wearing a suit: it commits
    # to nothing, it invents an arrangement neither side asked for, and it makes
    # the writer sound busy rather than useful. Say the concrete thing or say
    # nothing.
    ("PROMISING UNNAMED WORK", [
        r"(?:trato|tratamos) do resto", r"o resto (?:fico|ficamos) (?:eu|n(?:ó|o)s)",
        r"(?:de rest|het overige) regel ik", r"regel ik verder",
        r"I(?:'ll| will) (?:take care of|handle|sort out) the rest",
        r"leave the rest to me", r"del resto me encargo",
        r"den Rest (?:mache|erledige) ich",
        r"(?:zeg maar|diga-me|dime|sag mir|tell me) (?:maar )?(?:wat|o que|lo que|was|what)"
        r"[^.!?\n]{0,40}(?:nodig|precisa|necesita|brauchen|need)",
    ]),
    # Hidde, 2026-08-21: "vraag gewoon om fotos, stuur ze niet perse naar die
    # contribute pagina." Somebody who has already written to us is the best
    # channel we will ever have with them, and pointing them at a web form
    # turns a correspondent back into a stranger filling in fields. The form is
    # for readers arriving cold; a live thread answers by replying.
    ("FORM LINK IN A LIVE THREAD", [
        r"ancienttrees\.app/contribute",
    ]),
    ("PROCESS-PITCHING", [
        r"two independent sources", r"\bwe verify\b", r"\bour (?:process|method|workflow)\b",
        r"\bcross-referenc", r"\bevery tree is (?:checked|verified)\b",
    ]),
]


ASK_PATTERNS = [
    r"\blink\b", r"\blinken\b", r"\blinkje\b", r"\bmention\b",
    r"\bverlinken\b", r"\bliga(?:ç|c)(?:ã|a)o\b", r"\bhiperliga(?:ç|c)(?:ã|a)o\b",
    r"\bmen(?:ç|c)(?:ã|a)o\b", r"\bdivulga", r"\benlace\b", r"\bVerweis\b",
]


def repeated_ask_hits(text, body):
    """The same ask, twice, to the same person. Hidde, 2026-08-21: "je vraagt
    twee keer om een link dat is te desperate."

    A first mail asks; a reply that asks again for the thing already asked for
    reads as need rather than as an offer, and need is the one posture that
    loses these people. The check is mechanical because the memory is: any
    address already in data/outreach-sent.json has HAD the ask, so a draft to
    that address repeating it is the second time whether or not this session
    remembers the first. Addresses are read from the whole file, notes
    included, because a reply draft names the recipient in its notes."""
    import json
    import os
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "outreach-sent.json")
    try:
        sent = json.load(open(path, encoding="utf-8")).get("sent", [])
    except Exception:
        return []
    already = {}
    for row in sent:
        if not isinstance(row, dict):
            continue
        addr = (row.get("to") or "").lower()
        if addr:
            already.setdefault(addr, row.get("date", "?"))
    # A reply CAN legitimately carry an ask the first mail did not, and the
    # cheap way to tell those apart is to make the writer say so in one line
    # above the separator, where the notes to Hidde live:
    #     mailcheck-ok: asking-twice - she offered the divulgação herself
    # A check that has to be argued with in writing stays a check; one that
    # fires on every reply to a contacted address becomes noise.
    if re.search(r"^mailcheck-ok:\s*asking-twice\b.+\S", text, re.M | re.I):
        return []
    named = [(a, d) for a, d in already.items() if a in text.lower()]
    # One recipient only. A reply is to a person; a file naming five addresses
    # is a contact table or a template, and warning on those is how a check
    # becomes noise nobody reads.
    if len(named) != 1:
        return []
    hits = []
    for addr, date in named:
        for pat in ASK_PATTERNS:
            m = re.search(pat, body, re.I)
            if m:
                line = body.splitlines()[body[:m.start()].count("\n")].strip()
                hits.append(("ASKING TWICE (%s got the ask %s)" % (addr, date),
                             m.group(0), line[:96]))
                break
    return hits


def body_of(text):
    parts = BODY_SPLIT.split(text, maxsplit=1)
    return parts[1] if len(parts) > 1 else text


def check(path):
    text = open(path, encoding="utf-8").read()
    body = body_of(text)
    hits = []
    for label, patterns in CHECKS:
        for pat in patterns:
            for m in re.finditer(pat, body, re.I):
                line = body[:m.start()].count("\n") + 1
                snippet = body.splitlines()[line - 1].strip()
                hits.append((label, m.group(0), snippet[:96]))
    # Stacked apologies: one is fine, two is a posture.
    sorries = re.findall(r"\bsorry\b|\bapolog\w*|thanks for the correction|"
                         r"thank you for correcting", body, re.I)
    if len(sorries) > 1:
        hits.append(("STACKED APOLOGIES", ", ".join(sorries),
                     f"{len(sorries)} in one mail; keep one, cut the rest"))
    if "—" in body or "–" in body:
        hits.append(("EM DASH", "—", "hard rule 3: never, anywhere"))
    # Only a real letter gets the capitals check: a file with no --- separator
    # is a reference or template collection, and HIS_VOICE.md exists precisely
    # to quote his own lower-case chat messages verbatim.
    if BODY_SPLIT.search(text):
        hits += lowercase_hits(body)
    hits += repeated_ask_hits(text, body)
    return hits


def lowercase_hits(body):
    """A mail that opens in lower case. Hidde, 2026-08-12: "waarom gebruik je
    geen hoofdletters, kun je dat vanaf nu doen als elk fatsoenlijk persoon."

    My fault came from HIS_VOICE.md, which listed "lower case openings" as a
    trait to imitate. It read his chat typing as his letter voice. He types fast
    to me; a letter under his name to a journalist or a city office is his
    shopfront. So this flags sentence starts, not stylistic lower case inside a
    line, and it tolerates one because a signature or a stray line should not
    fail a mail on its own.

    A sentence start is the first word of a paragraph, or the word after a full
    stop, question mark or exclamation mark. NOT the first word of every line:
    the first version of this check counted wrapped lines, so a normal
    paragraph broken at 80 characters failed on its own continuations and every
    reference file in drafts/ lit up. Deliberately blind to urls, list markers
    and anything starting with a digit, which is where the rest of the false
    positives live."""
    starts, bad = [], []
    prev = ""
    for para in re.split(r"\n\s*\n", body):
        para = " ".join(l.strip() for l in para.strip().split("\n"))
        if not para or para.startswith(("http", "-", "*", ">", "|")) or para[0].isdigit():
            continue
        # German, Czech and Polish letters continue the sentence after the
        # salutation comma, so "Guten Tag," / "Dobry den," is correctly
        # followed by a lower-case word. Flagging that taught nobody anything
        # about Hidde's voice and would have forced wrong orthography into
        # forty mails (found 2026-08-22 building batch 006). The rule is
        # narrow on purpose: only the paragraph DIRECTLY after a line ending
        # in a comma is exempt, and only its first word.
        if prev.endswith(","):
            starts += [x for x in re.split(r"(?<=[.!?])\s+", para)[1:] if x]
            prev = para
            continue
        prev = para
        starts.append(para)
        starts += [s for s in re.split(r"(?<=[.!?])\s+", para)[1:] if s]
    for s in starts:
        w = s.split()[0] if s.split() else ""
        if not w or not w[0].isalpha() or not w[0].islower():
            continue
        if w.lower().startswith(("ancienttrees", "http", "www")):
            continue
        bad.append(s[:60])
    if len(bad) > 1:
        return [("LOWER-CASE SENTENCES", "%d sentence(s)" % len(bad),
                 "%s ... capitals, per his 2026-08-12 ruling" % bad[0])]
    return []


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    paths = [p for a in args for p in (glob.glob(a) or [a])]
    bad = 0
    for p in paths:
        hits = check(p)
        if not hits:
            print(f"  clean  {p}")
            continue
        bad += 1
        print(f"\n  {len(hits)} problem(s) in {p}")
        for label, found, snippet in hits:
            print(f"    {label:18s} {found!r}")
            print(f"       {snippet}")
    if bad:
        print("\nRewrite before this goes anywhere. One short acknowledgement is")
        print("the whole apology; say what the thing is, not what it lacks; make")
        print("no promise about price; and never explain how we work.")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
