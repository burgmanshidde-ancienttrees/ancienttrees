#!/usr/bin/env python3
"""A reader's account as the PUBLIC repository may hold it: a keyed code, never the id.

Privacy audit, 2026-10-19 (Hidde: "wat als follow the money ons onderzoekt").
The repository is public, and a reader's account id sat beside the trees they
photographed or sent: in data/cities (contributor_user_id), data/leads
(_sightings.json) and the ambassador invitation lists. Any signed-in account
could turn that id into the person's name. So the files hold ref(uid) instead:
"p_" plus 24 hex of an HMAC whose key only the service key holder can make.

Equality works on codes (is this the same person, is this account gone).
Where the real id is needed, to mail somebody or to ask whether their account
still exists, uid() looks the code up in the list of accounts, which needs
SUPABASE_SERVICE_KEY like every other reader-data script.

The key is derived from the service key, so no new secret travels. Rotating
the service key changes every code: run `python3 scripts/people.py --rekey`
with OLD_SUPABASE_SERVICE_KEY set first, which rewrites the files.

    python3 scripts/people.py <uid>      # print its code
    python3 scripts/people.py --check    # every code in the repo resolves
"""
import hashlib
import hmac
import json
import os
import re
import sys
import urllib.error
import urllib.request

BASE = "https://caimvxiyrtifilimlkqw.supabase.co"
ENV_FILE = os.path.expanduser("~/.ancienttrees-supabase.env")
REF = re.compile(r"^p_[0-9a-f]{24}$")
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)


def service_key(env="SUPABASE_SERVICE_KEY"):
    k = os.environ.get(env)
    if k:
        return k
    if env == "SUPABASE_SERVICE_KEY" and os.path.exists(ENV_FILE):
        with open(ENV_FILE, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip().removeprefix("export ").strip()
                if line.startswith("SUPABASE_SERVICE_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def _ref_key(service=None):
    s = service or service_key()
    if not s:
        return None
    return hashlib.sha256(b"ancienttrees people ref v1:" + s.encode()).digest()


def is_ref(s):
    return isinstance(s, str) and bool(REF.match(s))


def ref(uid, service=None):
    """The code for an account id. A code passes through unchanged; None stays None.
    Raises when there is no key, because writing a raw id is the thing to avoid."""
    if not uid or is_ref(uid):
        return uid
    k = _ref_key(service)
    if k is None:
        raise RuntimeError("people.ref needs SUPABASE_SERVICE_KEY to make a code")
    return "p_" + hmac.new(k, str(uid).strip().lower().encode(), hashlib.sha256).hexdigest()[:24]


_ACCOUNTS = None


def accounts():
    """{code: uid} for every account that exists, or None when the list could
    not be read in full. None is not "nobody": callers must treat it as unknown."""
    global _ACCOUNTS
    if _ACCOUNTS is not None:
        return _ACCOUNTS
    key = service_key()
    if not key:
        return None
    out, page = {}, 1
    while True:
        req = urllib.request.Request(f"{BASE}/auth/v1/admin/users?page={page}&per_page=200",
                                     headers={"apikey": key, "Authorization": f"Bearer {key}"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                users = json.load(r).get("users") or []
        except Exception:
            return None
        for u in users:
            if u.get("id"):
                out[ref(u["id"], key)] = u["id"]
        if len(users) < 200:
            break
        page += 1
    _ACCOUNTS = out
    return out


def uid(code):
    """The account id behind a code, or None when it is gone or unknown.
    A raw id (from Supabase itself, or an old file) passes through."""
    if not code:
        return None
    if not is_ref(code):
        return code
    acc = accounts()
    return acc.get(code) if acc else None


def exists(code):
    """True, False, or None when we could not tell (never read None as gone)."""
    acc = accounts()
    if acc is None:
        return None
    return ref(code) in acc


def _rekey():
    old = service_key("OLD_SUPABASE_SERVICE_KEY")
    if not old:
        sys.exit("--rekey needs OLD_SUPABASE_SERVICE_KEY (the key the codes were made with)")
    acc = accounts()
    if acc is None:
        sys.exit("--rekey could not read the accounts")
    old_to_new = {ref(u, old): c for c, u in acc.items()}
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    n = 0
    for dirpath, _, files in os.walk(os.path.join(root, "data")):
        for f in files:
            if not f.endswith(".json"):
                continue
            p = os.path.join(dirpath, f)
            s = open(p, encoding="utf-8").read()
            new = re.sub(r'"p_[0-9a-f]{24}"', lambda m: '"%s"' % old_to_new.get(m.group(0)[1:-1], m.group(0)[1:-1]), s)
            if new != s:
                open(p, "w", encoding="utf-8").write(new)
                n += 1
    print(f"rekeyed {n} file(s)")


def _check():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    codes = set()
    for dirpath, _, files in os.walk(os.path.join(root, "data")):
        for f in files:
            if f.endswith(".json"):
                codes |= set(re.findall(r'"(p_[0-9a-f]{24})"', open(os.path.join(dirpath, f), encoding="utf-8").read()))
    acc = accounts()
    if acc is None:
        print(f"{len(codes)} code(s) in the repo; accounts unreadable, nothing checked")
        return 0
    gone = [c for c in codes if c not in acc]
    print(f"{len(codes)} code(s) in the repo, {len(codes) - len(gone)} resolve, "
          f"{len(gone)} belong to no account (deleted, or made with another key)")
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--rekey"]:
        _rekey()
    elif sys.argv[1:] == ["--check"]:
        sys.exit(_check())
    else:
        for a in sys.argv[1:]:
            print(ref(a))
