#!/usr/bin/env python3
"""Write android/.../ui/Symbols.kt: the app's icons, from Material Symbols Rounded.

The iPhone draws SF Symbols, which Apple licenses for Apple platforms only. Of
the open sets, Material Symbols Rounded came closest to them side by side
(2026-11-10, DECISIONS.md): rounded ends like SF, a weight axis to match SF's
regular and semibold, and a drawn filled twin for every glyph, which the
iPhone leans on (the selected tab, bookmark.fill, camera.fill,
checkmark.seal.fill). Lucide has no filled twins. One set, never mixed, and
every glyph comes from it: nothing here is drawn by hand. Back, share and
the overflow menu take Android's form (Airbnb's line, DECISIONS.md 2026-11-10).

Each glyph is fetched from the published npm package at a pinned version and
turned into a Compose ImageVector. Run again after changing GLYPHS:

    python3 android/generate_symbols.py

Licence: Apache 2.0 (android/ICONS-LICENSE-APACHE.txt).
"""
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "android/app/src/main/java/app/ancienttrees/ui/Symbols.kt"
CACHE = ROOT / "out/tmp/material-symbols"
VERSION = "0.48.0"
URL = "https://cdn.jsdelivr.net/npm/@material-symbols/svg-{w}@{v}/rounded/{name}.svg"

# Kotlin name: (Material Symbols name, filled, weight, mirrors in right-to-left)
# The SF Symbol each one stands for is named beside it. Weight 400 is SF's
# regular at the same size; 600 is SF's semibold.
GLYPHS = {
    # THE SYSTEM SIGNS TAKE ANDROID'S FORM (Hidde, 2026-11-10, "Yes, Airbnb's
    # line"; CONVENTIONS.md "One app on iPhone and Android"): back is the arrow,
    # share Android's share, the overflow menu the vertical dots. They come from
    # this same set, which is Android's own.
    "ArrowBack": ("arrow_back", False, 400, True),  # chevron.left on the iPhone
    "Share": ("share", False, 400, False),  # square.and.arrow.up on the iPhone
    "ShareSemibold": ("share", False, 600, False),
    "MoreVert": ("more_vert", False, 400, False),  # ellipsis.circle / ellipsis on the iPhone
    "ChevronRight": ("chevron_right", False, 400, True),  # chevron.right
    "KeyboardArrowDown": ("keyboard_arrow_down", False, 400, False),  # chevron.down
    "UnfoldMore": ("unfold_more", False, 400, False),  # chevron.up.chevron.down
    "Check": ("check", False, 400, False),  # checkmark
    "CheckSemibold": ("check", False, 600, False),
    "CheckCircleFill": ("check_circle", True, 400, False),  # checkmark.circle.fill
    "Close": ("close", False, 600, False),  # xmark (always semibold or bold on the iPhone)
    "Add": ("add", False, 400, False),  # plus
    "AddCircle": ("add_circle", False, 400, False),  # plus.circle
    "AddCircleFill": ("add_circle", True, 400, False),  # plus.circle.fill
    "Search": ("search", False, 400, False),  # magnifyingglass
    "SearchSemibold": ("search", False, 600, False),
    "Map": ("map", False, 400, False),  # map
    "MapFill": ("map", True, 400, False),  # map.fill
    "Eco": ("eco", False, 400, False),  # leaf
    "EcoFill": ("eco", True, 400, False),  # leaf.fill
    "Park": ("park", False, 400, False),  # tree
    "PhotoCamera": ("photo_camera", False, 400, False),  # camera
    "PhotoCameraSemibold": ("photo_camera", False, 600, False),
    "PhotoCameraFill": ("photo_camera", True, 400, False),  # camera.fill
    "PhotoCameraFillSemibold": ("photo_camera", True, 600, False),
    "PhotoLibrary": ("photo_library", False, 400, False),  # photo.on.rectangle
    "Image": ("image", False, 400, False),  # photo
    "ImageFill": ("image", True, 400, False),
    "Bookmark": ("bookmark", False, 400, False),  # bookmark
    "BookmarkFill": ("bookmark", True, 400, False),  # bookmark.fill
    "Verified": ("verified", False, 400, False),  # checkmark.seal
    "VerifiedFill": ("verified", True, 400, False),  # checkmark.seal.fill
    "Feedback": ("feedback", False, 400, False),  # exclamationmark.bubble
    "FeedbackSemibold": ("feedback", False, 600, False),
    "TurnRight": ("turn_right", False, 400, False),  # arrow.turn.up.right, Take me there
    "TurnRightSemibold": ("turn_right", False, 600, False),
    "StarShineFill": ("star_shine", True, 400, False),  # sparkles
    "Public": ("public", False, 400, False),  # globe.europe.africa
    "PersonFill": ("person", True, 400, False),  # person.fill
    "Person": ("person", False, 400, False),  # person
    "PersonAdd": ("person_add", False, 400, False),  # person.badge.plus
    "Settings": ("settings", False, 400, False),  # gearshape
    "SettingsFill": ("settings", True, 400, False),  # gearshape.fill
    "Straighten": ("straighten", False, 400, False),  # ruler
    "Lock": ("lock", False, 400, False),  # lock
    "ThumbUp": ("thumb_up", False, 400, False),
    "ThumbUpFill": ("thumb_up", True, 400, False),
    "ThumbDown": ("thumb_down", False, 400, False),
    "ThumbDownFill": ("thumb_down", True, 400, False),
    "PinDrop": ("pin_drop", False, 400, False),  # mappin.and.ellipse
    "LocationOnFill": ("location_on", True, 400, False),  # mappin
    "NearMe": ("near_me", False, 400, False),  # location
    "NearMeFill": ("near_me", True, 400, False),  # location.fill
    "NearMeDisabled": ("near_me_disabled", False, 400, False),  # location.slash
    "LocationOff": ("location_off", False, 400, False),  # mappin.slash
    "Info": ("info", False, 400, False),  # info.circle
    "Help": ("help", False, 400, False),  # questionmark.circle
    "HelpFill": ("help", True, 400, False),  # questionmark.circle.fill
    "Edit": ("edit", False, 400, False),  # pencil
    "EditSquare": ("edit_square", False, 400, False),  # square.and.pencil
    "Delete": ("delete", False, 400, False),  # trash
    "CalendarMonth": ("calendar_month", False, 400, False),  # calendar
    "Apartment": ("apartment", False, 400, False),  # building.2
    "LocationCity": ("location_city", False, 400, False),
    "ConfirmationNumber": ("confirmation_number", False, 400, False),  # ticket
    "ConfirmationNumberFill": ("confirmation_number", True, 400, False),  # ticket.fill
    "Visibility": ("visibility", False, 400, False),  # eye
    "Star": ("star", False, 400, False),  # star
    "NorthEast": ("north_east", False, 400, False),  # arrow.up.right
    "History": ("history", False, 400, False),  # clock.arrow.circlepath
    "Favorite": ("favorite", False, 400, False),  # heart
    "Description": ("description", False, 400, False),  # doc.text
    "Draft": ("draft", False, 400, False),  # doc
    "Circle": ("circle", False, 400, False),  # circle
    "Chat": ("chat", False, 400, True),  # text.bubble
    "ChatBubble": ("chat_bubble", False, 400, True),  # bubble.left
    "Cancel": ("cancel", False, 400, False),  # xmark.circle
    "CancelFill": ("cancel", True, 400, False),  # xmark.circle.fill
    "Tram": ("tram", False, 400, False),  # tram
    "OpenInFull": ("open_in_full", False, 400, False),  # arrow.up.left.and.arrow.down.right
    "MailFill": ("mail", True, 400, False),  # envelope.fill
    "DirectionsWalk": ("directions_walk", False, 400, True),  # figure.walk
    "SendFill": ("send", True, 400, True),  # paperplane.fill
    "Merge": ("merge", False, 400, False),  # arrow.triangle.merge
}

NUMBER = re.compile(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")


def normalise(d):
    """Spell every number apart ("9-9-21" is three numbers to SVG)."""
    out, i = [], 0
    while i < len(d):
        ch = d[i]
        if ch.isalpha():
            out.append(ch)
            i += 1
        elif ch in " ,\t\n":
            i += 1
        else:
            m = NUMBER.match(d, i)
            if not m:
                raise ValueError(f"cannot read {d[i:i + 12]!r}")
            out.append(m.group(0))
            i = m.end()
    return " ".join(out)


def fetch(name, fill, weight):
    file = f"{name}-fill" if fill else name
    path = CACHE / f"w{weight}" / f"{file}.svg"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["curl", "-sfm", "20", "-o", str(path),
                        URL.format(w=weight, v=VERSION, name=file)], check=True)
    svg = path.read_text()
    if 'viewBox="0 -960 960 960"' not in svg:
        raise ValueError(f"{file}: unexpected viewBox")
    paths = re.findall(r'<path d="([^"]+)"', svg)
    if not paths:
        raise ValueError(f"{file}: no path")
    return [normalise(p) for p in paths]


def main():
    lines = [
        "// GENERATED by android/generate_symbols.py from Material Symbols Rounded",
        f"// {VERSION} (Apache 2.0, android/ICONS-LICENSE-APACHE.txt). Do not edit by hand.",
        "",
        "package app.ancienttrees.ui",
        "",
        "import androidx.compose.ui.graphics.Color",
        "import androidx.compose.ui.graphics.SolidColor",
        "import androidx.compose.ui.graphics.vector.ImageVector",
        "import androidx.compose.ui.graphics.vector.addPathNodes",
        "import androidx.compose.ui.unit.dp",
        "",
        "/** The app's icons, one set: Material Symbols Rounded, each the glyph closest to the iPhone's SF Symbol. */",
        "object Sym {",
    ]
    for kt, (name, fill, weight, mirror) in GLYPHS.items():
        ds = fetch(name, fill, weight)
        args = ", ".join(f'"{d}"' for d in ds)
        lines.append(f'    /** {name}{" filled" if fill else ""}, weight {weight}. */')
        lines.append(f'    val {kt}: ImageVector by lazy {{ symbol("{kt}", {str(mirror).lower()}, {args}) }}')
    lines += [
        "}",
        "",
        "private fun symbol(name: String, mirror: Boolean, vararg paths: String): ImageVector {",
        "    val b = ImageVector.Builder(name, 24.dp, 24.dp, 960f, 960f, autoMirror = mirror)",
        "    // The set draws on a viewBox of 0 -960 960 960: one group moves it into view.",
        "    b.addGroup(translationY = 960f)",
        "    for (d in paths) b.addPath(addPathNodes(d), fill = SolidColor(Color.Black))",
        "    b.clearGroup()",
        "    return b.build()",
        "}",
        "",
    ]
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT.relative_to(ROOT)}: {len(GLYPHS)} glyphs")


if __name__ == "__main__":
    main()
