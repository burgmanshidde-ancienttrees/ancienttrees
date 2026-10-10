#!/usr/bin/env python3
"""Every overlay is the one sheet, on the app and on the website.

Hidde, 2026-10-10: "get your act together in designing al these overlays -
please take a look at all of them and start making a consistent design and
remember that for future overlays plz make it a component or something".

The audit that day found 27 small overlays in the app and 13 on the website,
built from four green buttons, three reds, three backdrops, five top paddings
and fixed heights that cut buttons off, with system alerts that looked like a
different app. The design he approved is one sheet: Kit/BrandSheet.swift in
the app, components/Sheet.astro on the website (CONVENTIONS.md, "One sheet for
every overlay"). This check is what keeps the NEXT overlay on it:

  app   no `.alert(` and no `.confirmationDialog(` anywhere. A question is a
        BrandSheet; news is the snackbar (Navigator.snack).
  app   every `.sheet(` and `.fullScreenCover(` presents a view named in
        data/sheet-allow.json, which carries the reason each one is allowed:
        BrandSheet itself, the measured sign-in sheet, and full screens
        (camera, photo viewer, map pin, forms) that are not overlays at all.
        A new sheet that is none of those has to become a BrandSheet or earn a
        line in that file, so an exception is a decision and not a silence.
  web   every `<dialog` under site/src carries class "at-sheet" (which is what
        components/Sheet.astro renders) or a class named in the same file.

Removing this check needs Hidde.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "ios" / "AncientTrees"
SITE = ROOT / "site" / "src"
ALLOW = json.loads((ROOT / "data" / "sheet-allow.json").read_text(encoding="utf-8"))

KEYWORDS = {"if", "let", "var", "switch", "case", "else", "guard", "return", "in",
            "self", "true", "false", "nil", "default", "await", "try", "Task",
            # Containers say nothing about what is presented; look inside.
            "Group", "VStack", "HStack", "ZStack", "NavigationStack", "ScrollView"}
PRESENT = re.compile(r"\.(sheet|fullScreenCover)\(")
FORBIDDEN = re.compile(r"\.(alert|confirmationDialog)\(")
TOKEN = re.compile(r"(\.?)([A-Za-z_][A-Za-z0-9_]*)\s*([({]?)")


def code(line: str) -> str:
    """The line without a trailing // comment (good enough for this file set)."""
    i = line.find("//")
    return line if i < 0 else line[:i]


def content_start(text: str) -> int:
    """Index just past the `{` that opens the presented content: the first `{`
    after the modifier's own parentheses close."""
    depth = 0
    started = False
    for i, ch in enumerate(text):
        if ch == "(":
            depth += 1
            started = True
        elif ch == ")":
            depth -= 1
        elif ch == "{" and started and depth == 0:
            return i + 1
    return -1


def presented(text: str) -> str | None:
    i = content_start(text)
    if i < 0:
        return None
    # Only the content closure itself, up to its own closing brace.
    depth = 1
    end = len(text)
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                end = j
                break
    body = text[i:end]
    first_lower = None
    for m in TOKEN.finditer(body):
        dot, name, _ = m.groups()
        if dot or name in KEYWORDS:
            continue
        if name[0].isupper():
            return name
        if first_lower is None:
            # A closure parameter ("which in") is not the content.
            after = body[m.end():m.end() + 4]
            if after.startswith("in ") or after.startswith("in\n"):
                continue
            first_lower = name
    return first_lower


def check_app() -> list[str]:
    out = []
    names = ALLOW["app"]
    for f in sorted(APP.rglob("*.swift")):
        if "Tests" in f.parts[-2]:
            continue
        lines = f.read_text(encoding="utf-8").splitlines()
        rel = f.relative_to(ROOT)
        for n, raw in enumerate(lines, 1):
            line = code(raw)
            if line.strip().startswith("//") or line.strip().startswith("*"):
                continue
            if FORBIDDEN.search(line):
                out.append(f"{rel}:{n}: a system alert or pop-up menu; use a BrandSheet (a question) or navigator.snack (news): {raw.strip()}")
            if PRESENT.search(line):
                window = "\n".join(code(l) for l in lines[n - 1:n + 14])
                window = window[PRESENT.search(window).start():]
                name = presented(window)
                if name not in names:
                    out.append(f"{rel}:{n}: presents {name!r}, which is neither BrandSheet nor on data/sheet-allow.json: {raw.strip()}")
    return out


DIALOG = re.compile(r"<dialog\b([^>]*)>")


def check_web() -> list[str]:
    out = []
    classes = set(ALLOW["web"])
    for f in sorted(list(SITE.rglob("*.astro")) + list(SITE.rglob("*.ts"))):
        rel = f.relative_to(ROOT)
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            s = line.strip()
            if s.startswith("//") or s.startswith("*") or s.startswith("/*"):
                continue
            for m in DIALOG.finditer(line):
                attrs = m.group(1)
                if "at-sheet" in attrs:
                    continue
                cls = re.search(r'class(?::list)?=["{]([^"}]*)', attrs)
                have = set(re.findall(r"[a-z][a-z0-9-]*", cls.group(1))) if cls else set()
                if not (have & classes):
                    out.append(f"{rel}:{n}: a <dialog> that is not the one sheet; use components/Sheet.astro: {s}")
    return out


def main() -> int:
    bad = check_app() + check_web()
    if bad:
        print("sheetcheck: an overlay that is not the one sheet (Kit/BrandSheet.swift, components/Sheet.astro)")
        print("\n".join(bad))
        return 1
    print("sheetcheck: every overlay is the one sheet, or a full screen on the list")
    return 0


if __name__ == "__main__":
    sys.exit(main())
