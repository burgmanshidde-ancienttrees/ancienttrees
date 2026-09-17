#!/usr/bin/env python3
"""Generate the client secret Apple wants for Sign in with Apple ON THE WEB.

WHY THIS EXISTS, and why it is a script rather than a line in a checklist.
Apple's web client secret is not a value you copy out of a console. It is an
ES256 JWT that YOU sign with the .p8 key Apple hands over once, and Apple caps
its lifetime at six months. When it expires, Apple-on-web stops working with
`invalid_client` and nothing warns anybody: the button simply stops, for
everyone, on a day nobody chose. So this is a chore that comes back twice a
year, and a chore that comes back is worth one command.

The app is UNAFFECTED by all of this. It signs in natively
(/auth/v1/token?grant_type=id_token) where Apple accepts the bundle id and asks
for no secret at all. Only the website's redirect flow needs this.

Deliberately stdlib plus `openssl`, which is on every Mac and on the runner.
PyJWT would be a dependency for one signature, and this project's rule about
tools is to prefer the boring thing that cannot break while nobody is looking.

    python3 scripts/apple_secret.py --p8 ~/Downloads/AuthKey_ABC123XYZ.p8

Team id, services id and key id default to this project's own; the key id is
read out of the filename when it looks like Apple's (AuthKey_<KEYID>.p8).

NEVER COMMIT THE .p8, and never paste it into a chat. It is the whole key to
signing in as this website; anybody holding it can mint these tokens forever.
Keep it where you keep passwords. This script only reads it.
"""
import argparse
import base64
import json
import re
import subprocess
import sys
import time
from pathlib import Path

TEAM_ID = "5EWWC3M8L2"
SERVICES_ID = "app.ancienttrees.web"
SIX_MONTHS = 15777000          # Apple's hard ceiling, in seconds


def b64(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def der_to_raw(der: bytes) -> bytes:
    """openssl signs to DER (SEQUENCE of two INTEGERs); a JWS wants r||s, each
    left-padded to 32 bytes. Getting this wrong produces a token Apple rejects
    as malformed rather than as expired, which is a confusing hour."""
    if der[0] != 0x30:
        raise ValueError("not a DER sequence")
    i = 2 if der[1] < 0x80 else 2 + (der[1] & 0x7F)
    out = b""
    for _ in range(2):
        if der[i] != 0x02:
            raise ValueError("expected a DER integer")
        length = der[i + 1]
        val = der[i + 2:i + 2 + length].lstrip(b"\x00")
        out += val.rjust(32, b"\x00")
        i += 2 + length
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--p8", required=True, help="path to AuthKey_<KEYID>.p8 from Apple")
    ap.add_argument("--key-id", help="Apple's Key ID (read from the filename if omitted)")
    ap.add_argument("--team-id", default=TEAM_ID)
    ap.add_argument("--services-id", default=SERVICES_ID,
                    help="the SERVICES id (the web one), never the bundle id")
    args = ap.parse_args()

    p8 = Path(args.p8).expanduser()
    if not p8.is_file():
        print(f"no such key: {p8}", file=sys.stderr)
        return 1

    key_id = args.key_id
    if not key_id:
        m = re.search(r"AuthKey_([A-Za-z0-9]+)\.p8$", p8.name)
        if not m:
            print("cannot read the Key ID from the filename; pass --key-id",
                  file=sys.stderr)
            return 1
        key_id = m.group(1)

    now = int(time.time())
    header = {"alg": "ES256", "kid": key_id}
    payload = {
        "iss": args.team_id,
        "iat": now,
        "exp": now + SIX_MONTHS,
        "aud": "https://appleid.apple.com",
        "sub": args.services_id,
    }
    signing_input = (b64(json.dumps(header, separators=(",", ":")).encode())
                     + "." + b64(json.dumps(payload, separators=(",", ":")).encode()))

    try:
        der = subprocess.run(
            ["openssl", "dgst", "-sha256", "-sign", str(p8)],
            input=signing_input.encode(), capture_output=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        print("openssl refused the key:\n" + e.stderr.decode(), file=sys.stderr)
        return 1

    token = signing_input + "." + b64(der_to_raw(der))
    expires = time.strftime("%Y-%m-%d", time.localtime(now + SIX_MONTHS))
    print(token)
    print(f"\n  services id : {args.services_id}", file=sys.stderr)
    print(f"  key id      : {key_id}", file=sys.stderr)
    print(f"  EXPIRES     : {expires}  <- Apple-on-web dies that day unless this is re-run",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
