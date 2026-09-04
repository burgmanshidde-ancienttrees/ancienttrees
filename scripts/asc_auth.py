"""asc_auth.py - App Store Connect API bearer tokens.

Reads the three pieces from data ~/.ancienttrees-appstoreconnect.env (key id,
issuer id, path to the .p8 private key), which nothing in this repo holds
directly per hard rule 5's "gear for us" carve-out: read-only, costs nothing,
never touches reader data, nothing it does reaches the built site.

The App Store Connect API takes a short-lived ES256 JWT, not the key itself.
Apple caps a token's lifetime at 20 minutes; this asks for 15 to leave room.
"""
import base64
import json
import os
import time

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils


def _b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


# THE FILE READS ITSELF, so nobody has to remember to source it.
#
# Everything here already lives in ~/.ancienttrees-appstoreconnect.env by this
# project's own convention (credentials outside the repo). Requiring a `source`
# first turned a missing shell line into a WRONG ANSWER rather than an error on
# 2026-09-04: release.py asks this module for the last uploaded build, and
# without the variables it falls back silently to the project file's number,
# which was 8 while Apple already held 9. The archive would have been built,
# and only Apple would have said no.
#
# Only fills what is not already set, so an explicit export and CI's secrets
# both still win.
def _load_env_file(path="~/.ancienttrees-appstoreconnect.env"):
    try:
        with open(os.path.expanduser(path), encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export "):
                    line = line[len("export "):]
                if "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v
    except OSError:
        pass


def _env(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        _load_env_file()
        v = os.environ.get(name)
    if not v:
        raise SystemExit(
            "%s is not set. Run: source ~/.ancienttrees-appstoreconnect.env"
            % name)
    return v


def _load_private_key() -> bytes:
    # Two ways to supply it: a path (local machine, the file this project's
    # convention keeps outside the repo) or the PEM content itself (CI,
    # where the key lives as a GitHub secret rather than a file on disk).
    inline = os.environ.get("ASC_PRIVATE_KEY")
    if inline:
        return inline.encode()
    key_path = os.path.expanduser(_env("ASC_PRIVATE_KEY_PATH"))
    if not os.path.isfile(key_path):
        raise SystemExit("ASC_PRIVATE_KEY_PATH does not exist: %s" % key_path)
    with open(key_path, "rb") as f:
        return f.read()


def bearer_token(ttl_seconds: int = 900) -> str:
    key_id = _env("ASC_KEY_ID")
    issuer_id = _env("ASC_ISSUER_ID")
    private_key = serialization.load_pem_private_key(_load_private_key(), password=None)

    now = int(time.time())
    header = {"alg": "ES256", "kid": key_id, "typ": "JWT"}
    payload = {
        "iss": issuer_id,
        "iat": now,
        "exp": now + ttl_seconds,
        "aud": "appstoreconnect-v1",
    }
    signing_input = "%s.%s" % (
        _b64url(json.dumps(header, separators=(",", ":")).encode()),
        _b64url(json.dumps(payload, separators=(",", ":")).encode()),
    )
    # cryptography's EC signer returns a DER-encoded (r, s) pair; a JWS
    # ES256 signature is the two 32-byte big-endian integers concatenated,
    # so it has to be unpacked and repacked rather than used as-is.
    der_sig = private_key.sign(signing_input.encode(), ec.ECDSA(hashes.SHA256()))
    r, s = utils.decode_dss_signature(der_sig)
    raw_sig = r.to_bytes(32, "big") + s.to_bytes(32, "big")
    return "%s.%s" % (signing_input, _b64url(raw_sig))


if __name__ == "__main__":
    print(bearer_token())
