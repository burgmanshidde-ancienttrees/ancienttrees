#!/usr/bin/env python3
"""Does this photograph contradict what we say about the tree?

Hidde asked for it as step 4 of the collect-flow work, 2026-09-07, and the
question he actually asked was "do we do an ai check on the photo to check
species and location". The answer that came out of benchmarking is narrower
than the question, and the narrowing is the whole design:

EVERY REFERENCE APP IDENTIFIES A SPECIES. WE NEED AN INDIVIDUAL. Merlin, Seek,
iNaturalist and PictureThis all answer "what kind of thing is this". Run that on
the photograph Hidde took in Nara and it returns Cryptomeria japonica with high
confidence, which we already knew, and which is equally true of the two other
cedars within two hundred metres. Species recognition cannot tell one trunk from
another, so it cannot confirm a find.

WHAT IT CAN DO IS DISAGREE. If somebody photographs an oak while standing at our
cedar's pin, something is wrong: their match, our species, or our coordinate.
That is worth knowing and no other check we have would catch it. So this never
approves anything. It reports what it sees and whether that fits the record, and
a person still looks at the pixels before a photograph ships. A confirmer would
be a machine deciding what goes on the site; a contradiction detector is a
second pair of eyes that only ever raises its hand.

    python3 scripts/photo_check.py            # every queued photograph
    python3 scripts/photo_check.py --dry-run  # print the prompts, call nothing

WHERE IT RUNS. On our own machines, over photographs people have already sent
us, never in the app. That keeps the app's promise intact (nothing a reader
takes goes to a third party from their phone) and puts the check where the
judging happens anyway.

COST AND CREDENTIALS. It needs ANTHROPIC_API_KEY, which is Hidde's to provide
and Hidde's to pay for (hard rule 5). Without one this prints a line and exits
cleanly, the same way the sightings inbox behaves without a Supabase key.
Roughly a cent or two per photograph at current Opus rates, on a queue that
holds single figures a day.
"""
import argparse
import base64
import json
import mimetypes
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "sighting-queue.json")
MODEL = "claude-opus-5"

# The question, and the shape of the answer. Deliberately three fields: what it
# can see, whether that fits, and one sentence a human can act on. No score, no
# confidence percentage: a number invites somebody to set a threshold and stop
# looking, which is the failure this whole file is written to avoid.
SCHEMA = {
    "type": "json_schema",
    "schema": {
        "type": "object",
        "properties": {
            "shows": {
                "type": "string",
                "description": "What is actually in the photograph, in one sentence: "
                               "the tree, its form, and what is around it.",
            },
            "fits": {
                "type": "string",
                "enum": ["yes", "unclear", "no"],
                "description": "Whether the photograph is consistent with the record. "
                               "'no' only for a real contradiction, such as a "
                               "different kind of tree or a setting that cannot be "
                               "the one described. 'unclear' when the photograph "
                               "simply does not show enough.",
            },
            "note": {
                "type": "string",
                "description": "One sentence for the person who will judge this. "
                               "If it fits, say what in the photograph matches. If "
                               "not, say exactly what disagrees.",
            },
        },
        "required": ["shows", "fits", "note"],
        "additionalProperties": False,
    },
}

SYSTEM = (
    "You are checking a photograph a reader sent to Ancient Trees against the "
    "record we hold for a tree. You are NOT deciding whether it gets published "
    "and you are not identifying which individual tree it is: several trees of "
    "one species often stand within metres of each other and a photograph "
    "cannot settle that. Your job is narrower and more useful. Say what the "
    "photograph shows, and say whether anything in it CONTRADICTS the record. "
    "A different kind of tree, a setting that cannot be the one described, a "
    "young street tree where the record describes a veteran: those are "
    "contradictions worth raising. Not being able to tell is 'unclear', which "
    "is a perfectly good answer and the honest one most of the time. Never "
    "invent detail you cannot see."
)


def record(e):
    """What we claim about this tree, as the prompt sees it."""
    bits = [f"Tree: {e.get('tree_name') or '(unnamed)'}",
            f"Species we record: {e.get('species') or 'not recorded'}",
            f"Place: {e.get('city') or 'unknown'}"]
    if e.get("how_to_recognise"):
        bits.append(f"How we say to recognise it: {e['how_to_recognise']}")
    if e.get("match") == "distance":
        bits.append(f"Matched only by distance, {e.get('distance_m')} m from our pin, "
                    f"so the tree in the photograph may be a neighbour.")
    return "\n".join(bits)


def check(client, e, path):
    media = mimetypes.guess_type(path)[0] or "image/jpeg"
    with open(path, "rb") as fh:
        data = base64.standard_b64encode(fh.read()).decode("utf-8")
    r = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM,
        thinking={"type": "adaptive"},
        output_config={"format": SCHEMA},
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": media, "data": data}},
            {"type": "text", "text": record(e)},
        ]}],
    )
    # A refusal returns HTTP 200 with no usable content, so it is checked before
    # anything reads the blocks. On photographs of trees it should never fire;
    # treating it as "we did not check this one" is the honest fallback.
    if getattr(r, "stop_reason", None) == "refusal":
        return {"fits": "unclear", "shows": "", "note": "the model declined to answer"}
    text = next(b.text for b in r.content if b.type == "text")
    out = json.loads(text)
    u = r.usage
    out["_tokens"] = [u.input_tokens, u.output_tokens]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="print what would be asked and call nothing")
    a = ap.parse_args()

    try:
        with open(QUEUE) as fh:
            doc = json.load(fh)
    except Exception:
        print("photo_check: no sighting queue on disk")
        return 0
    queue = doc.get("queue", [])
    todo = [e for e in queue if e.get("file") and not e.get("ai")]
    if not todo:
        print(f"photo_check: nothing to check ({len(queue)} in the queue)")
        return 0

    if a.dry_run:
        for e in todo:
            print(f"--- {e['sighting_id'][:8]}  {e.get('file')}")
            print(record(e))
            print()
        print(f"{len(todo)} photograph(s) would be checked on {MODEL}")
        return 0

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("photo_check: ANTHROPIC_API_KEY absent, nothing checked. "
              "It is a paid key and Hidde's to add (hard rule 5); "
              "--dry-run shows what would be asked.")
        return 0
    try:
        import anthropic
    except ImportError:
        print("photo_check: the anthropic package is not installed here")
        return 0

    client = anthropic.Anthropic()
    checked = 0
    for e in todo:
        path = os.path.join(ROOT, e["file"])
        if not os.path.exists(path):
            continue
        try:
            e["ai"] = check(client, e, path)
            checked += 1
        except Exception as exc:
            print(f"  {e['sighting_id'][:8]}: {exc.__class__.__name__}: {str(exc)[:90]}")
    with open(QUEUE, "w") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"photo_check: {checked} checked on {MODEL}")
    for e in todo:
        ai = e.get("ai")
        if ai:
            print(f"  {e['sighting_id'][:8]}  {ai['fits'].upper():8} {ai['note'][:90]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
