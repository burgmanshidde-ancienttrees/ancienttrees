#!/usr/bin/env python3
"""Write App Store metadata from a drafts file into App Store Connect.

Reads drafts/app-store-metadata-<version>.md (one `## Language` section per
locale, fenced blocks under "Subtitle", "Keywords", "Description" and "What's
new") and writes it to the version in PREPARE_FOR_SUBMISSION through the ASC
API: PATCH on a locale that exists, POST on one that does not. Name stays what
the primary locale carries unless the file names one. Nothing here submits.

    python3 scripts/asc_metadata.py 1.0.3           # dry run, prints the plan
    python3 scripts/asc_metadata.py 1.0.3 --apply

Why a script: subtitle and keywords are locked on a live version and open only
on a new one, and eight locales by hand in Connect is twenty minutes of
pasting per release. The drafts file stays the pasteable source of truth.
"""
import json
import re
import sys
import urllib.request

sys.path.insert(0, "scripts")
from asc_auth import bearer_token  # noqa: E402

APP = "6806177833"
API = "https://api.appstoreconnect.apple.com/v1"
LOCALES = {
    "English (U.K.)": "en-GB", "English (U.S.)": "en-US", "Dutch": "nl-NL",
    "German": "de-DE", "French": "fr-FR", "Spanish": "es-ES", "Italian": "it",
    "Portuguese (Portugal)": "pt-PT", "Japanese": "ja",
}
LIMITS = {"name": 30, "subtitle": 30, "keywords": 100, "description": 4000, "whatsNew": 4000}


def _call(method, url, token, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + token, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r) if r.status != 204 else {}
    except urllib.error.HTTPError as e:
        raise SystemExit("%s %s -> %s\n%s" % (method, url, e.code, e.read().decode()[:600]))


def parse(path):
    """{locale: {field: text}} from the drafts file."""
    text = open(path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", text, re.S | re.M):
        head = m.group(1).strip()
        locale = next((v for k, v in LOCALES.items() if head.startswith(k)), None)
        if not locale:
            continue
        fields = {}
        for fm in re.finditer(r"^(Subtitle|Keywords|Description|What's new)[^\n]*\n\n```\n(.*?)\n```", m.group(2), re.S | re.M):
            key = {"Subtitle": "subtitle", "Keywords": "keywords", "Description": "description", "What's new": "whatsNew"}[fm.group(1)]
            fields.setdefault(key, fm.group(2).strip())
        if locale == "en-US" and "same as U.K." in m.group(2):
            fields["_copy_from"] = "en-GB"
        out[locale] = fields
    # en-US inherits what it does not state.
    if "en-US" in out and out["en-US"].get("_copy_from"):
        base = out[out["en-US"].pop("_copy_from")]
        for k in ("subtitle", "description", "whatsNew"):
            out["en-US"].setdefault(k, base.get(k))
    for locale, f in out.items():
        for k, v in f.items():
            if k in LIMITS and v and len(v) > LIMITS[k]:
                raise SystemExit("%s %s is %d chars, limit %d" % (locale, k, len(v), LIMITS[k]))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit(__doc__)
    version, apply = args[0], "--apply" in sys.argv
    want = parse("drafts/app-store-metadata-%s.md" % version)
    tok = bearer_token()
    vers = [v for v in _call("GET", f"{API}/apps/{APP}/appStoreVersions?limit=5", tok)["data"]
            if v["attributes"]["versionString"] == version and v["attributes"]["appStoreState"] == "PREPARE_FOR_SUBMISSION"]
    if not vers:
        raise SystemExit("no editable version %s in Connect; create it first (sidebar, + next to iOS App)" % version)
    vid = vers[0]["id"]
    infos = [i for i in _call("GET", f"{API}/apps/{APP}/appInfos", tok)["data"]
             if i["attributes"].get("appStoreState") == "PREPARE_FOR_SUBMISSION"]
    if not infos:
        raise SystemExit("no editable app info record")
    iid = infos[0]["id"]
    have_v = {l["attributes"]["locale"]: l for l in _call("GET", f"{API}/appStoreVersions/{vid}/appStoreVersionLocalizations", tok)["data"]}
    have_i = {l["attributes"]["locale"]: l for l in _call("GET", f"{API}/appInfos/{iid}/appInfoLocalizations", tok)["data"]}
    primary_v = have_v.get("en-GB", {}).get("attributes", {})
    primary_i = have_i.get("en-GB", {}).get("attributes", {})

    for locale, f in want.items():
        vattrs = {k: f[k] for k in ("keywords", "description", "whatsNew") if f.get(k)}
        iattrs = {k: f[k] for k in ("subtitle",) if f.get(k)}
        if locale in have_v:
            print("PATCH version %-6s %s" % (locale, ", ".join(vattrs)))
            if apply and vattrs:
                _call("PATCH", f"{API}/appStoreVersionLocalizations/{have_v[locale]['id']}", tok,
                      {"data": {"type": "appStoreVersionLocalizations", "id": have_v[locale]["id"], "attributes": vattrs}})
        else:
            vattrs.setdefault("description", primary_v.get("description"))
            vattrs["supportUrl"] = primary_v.get("supportUrl")
            vattrs["marketingUrl"] = primary_v.get("marketingUrl")
            vattrs["locale"] = locale
            print("POST  version %-6s %s" % (locale, ", ".join(k for k in vattrs if k != "locale")))
            if apply:
                _call("POST", f"{API}/appStoreVersionLocalizations", tok,
                      {"data": {"type": "appStoreVersionLocalizations", "attributes": vattrs,
                                "relationships": {"appStoreVersion": {"data": {"type": "appStoreVersions", "id": vid}}}}})
        if locale not in have_i:
            # Apple creates the app-info record for a new locale when the version record lands.
            have_i = {l["attributes"]["locale"]: l for l in _call("GET", f"{API}/appInfos/{iid}/appInfoLocalizations", tok)["data"]}
        if locale in have_i:
            print("PATCH info    %-6s %s" % (locale, ", ".join(iattrs)))
            if apply and iattrs:
                _call("PATCH", f"{API}/appInfoLocalizations/{have_i[locale]['id']}", tok,
                      {"data": {"type": "appInfoLocalizations", "id": have_i[locale]["id"], "attributes": iattrs}})
        else:
            iattrs["name"] = primary_i.get("name")
            iattrs["privacyPolicyUrl"] = primary_i.get("privacyPolicyUrl")
            iattrs["locale"] = locale
            print("POST  info    %-6s %s" % (locale, ", ".join(k for k in iattrs if k != "locale")))
            if apply:
                _call("POST", f"{API}/appInfoLocalizations", tok,
                      {"data": {"type": "appInfoLocalizations", "attributes": iattrs,
                                "relationships": {"appInfo": {"data": {"type": "appInfos", "id": iid}}}}})
    print("applied" if apply else "dry run; add --apply to write")


if __name__ == "__main__":
    main()
