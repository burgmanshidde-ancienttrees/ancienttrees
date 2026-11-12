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
# The npm package leaves out a few glyphs the set itself still carries (auto_awesome,
# the set's sparkles, is the one the iPhone's sparkles needs). Those come from
# Google's own repository of the same set, at a pinned commit, on a 24 grid.
GH_COMMIT = "10ecc14790612ca8fd164e3f4ffe9c16fc50d5b7"
GH_URL = ("https://cdn.jsdelivr.net/gh/google/material-design-icons@{c}/symbols/web/{name}/"
          "materialsymbolsrounded/{file}_24px.svg")

# Kotlin name: (Material Symbols name, filled, weight, mirrors in right-to-left)
# The SF Symbol each one stands for is named beside it. Weight 400 is SF's
# regular at the same size; 600 is SF's semibold.
GLYPHS = {
    # THE SYSTEM SIGNS TAKE ANDROID'S FORM (Hidde, 2026-11-10, "Yes, Airbnb's
    # line"; CONVENTIONS.md "One app on iPhone and Android"): back is the arrow,
    # share Android's share, the overflow menu the vertical dots. They come from
    # this same set, which is Android's own.
    "ArrowBack": ("arrow_back", False, 600, True),  # chevron.left on the iPhone, semibold
    "Share": ("share", False, 400, False),  # square.and.arrow.up on the iPhone
    "ShareSemibold": ("share", False, 600, False),
    "MoreVert": ("more_vert", False, 600, False),  # ellipsis.circle on the iPhone, 17 semibold
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
    # 2026-11-11 (visual review, icon rows): glyphs closer to the iPhone's SF Symbol.
    # A set glyph may be turned or flipped to stand as the SF one stands; its
    # shape is never redrawn. Where the set has no match the nearest one is used
    # and listed in data/android-parity.json.
    "Leaf": ("eco", False, 400, False, {"flip": True, "rotate": -25}),  # leaf: the set's leaf, flipped so its tip points up-left and its stem curls out bottom right
    "LeafFill": ("eco", True, 400, False, {"flip": True, "rotate": -25}),  # leaf.fill
    "LeafSemibold": ("eco", False, 600, False, {"flip": True, "rotate": -25}),  # leaf at a chip's .caption2.semibold
    "BookmarkSemibold": ("bookmark", False, 600, False),  # bookmark, chip
    "VerifiedSemibold": ("verified", False, 600, False),  # checkmark.seal, chip
    "TicketSemibold": ("confirmation_number", False, 600, False),  # ticket, chip
    "TurnUpRight": ("reply", False, 400, False, {"flip": True}),  # arrow.turn.up.right: the set's curved reply arrow, turned to point right
    "TurnUpRightSemibold": ("reply", False, 600, False, {"flip": True}),
    "Sparkles": ("auto_awesome", False, 400, False, {"src": "gh"}),  # sparkles
    "SparklesFill": ("auto_awesome", True, 400, False, {"src": "gh"}),  # sparkles.fill
    # sparkle: SF's ONE four-point star (AmbassadorBadge.swift, the early-adopter
    # badge and its sheet). The set has no lone one (searched 0.48.0, 0.48.3 and
    # Google's catalogue, 2026-11-12: spark is not in it), so this is the big
    # star of the set's own auto_awesome, its second absolute subpath, centred
    # (it stands at 9,12 with a reach of 6.575) and scaled to the set's 20 live
    # area. The set's geometry, nothing drawn.
    "Sparkle": ("auto_awesome", True, 400, False,
                {"src": "gh", "part": 1, "centre": (9.0, 12.0), "reach": 6.575}),
    "Building": ("domain", False, 400, False),  # building.2
    "MapPin": ("keep", True, 400, False),  # mappin: the set's pin on a needle (no ball-headed pin in the set)
    "CloseBold": ("close", False, 700, False),  # xmark .bold
    "CheckBold": ("check", False, 700, False),  # checkmark .bold
    "ChevronRightSemibold": ("chevron_right", False, 600, True),  # chevron.right .semibold
    "InfoSemibold": ("info", False, 600, False),  # info.circle, heavier
    "FavoriteSemibold": ("favorite", False, 600, False),  # heart .semibold
    "AddSemibold": ("add", False, 600, False),  # plus .semibold
    "AddBold": ("add", False, 700, False),  # plus .bold
    "BookmarkFillSemibold": ("bookmark", True, 600, False),  # bookmark.fill on a card photo, 15 semibold
    "ThumbUpSemibold": ("thumb_up", False, 600, False),
    "ThumbUpFillSemibold": ("thumb_up", True, 600, False),
    "ThumbDownSemibold": ("thumb_down", False, 600, False),
    "ThumbDownFillSemibold": ("thumb_down", True, 600, False),
    "PhotoLibrarySemibold": ("photo_library", False, 600, False),
    # My trees' gear and Find people: 18 pt .medium (Collect.swift).
    "SettingsMedium": ("settings", False, 500, False),
    "SettingsFillMedium": ("settings", True, 500, False),
    "PersonAddMedium": ("person_add", False, 500, False),
}

# SheetIconTile draws its symbol at 24 semibold (BrandSheet.swift): every glyph a
# tile can carry gets a weight-600 twin, and Sym.semibold() hands the tile the twin.
SEMIBOLD_TWINS = ["Check", "Verified", "VerifiedFill", "Park", "Merge", "Public", "Favorite",
                  "PhotoCamera", "SendFill", "ImageFill", "Image", "MailFill", "Sparkles",
                  "SparklesFill", "NearMe", "PhotoCameraFill", "Leaf", "Info", "Bookmark",
                  "BookmarkFill", "LocationOff", "NearMeDisabled", "Lock", "Delete", "Star",
                  "PhotoLibrary", "TurnUpRight", "Edit", "MapPin", "Map", "Search", "Add",
                  "ChatBubble", "Building", "DirectionsWalk"]
for _n in SEMIBOLD_TWINS:
    _g = GLYPHS[_n]
    GLYPHS.setdefault(_n + "Semibold", (_g[0], _g[1], 600, _g[3], *_g[4:]))

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


def fetch_gh(name, fill, weight):
    """Google's repository: 24 grid, the weight and fill spelled in the file name."""
    axes = (f"wght{weight}" if weight != 400 else "") + ("fill1" if fill else "")
    file = f"{name}_{axes}" if axes else name
    path = CACHE / "gh" / f"{file}.svg"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["curl", "-sfm", "20", "-o", str(path),
                        GH_URL.format(c=GH_COMMIT, name=name, file=file)], check=True)
    svg = path.read_text()
    if 'height="24"' not in svg or 'width="24"' not in svg:
        raise ValueError(f"{file}: unexpected size")
    paths = re.findall(r'<path d="([^"]+)"', svg)
    if not paths:
        raise ValueError(f"{file}: no path")
    return [normalise(p) for p in paths]


def fetch(name, fill, weight, src="npm"):
    if src == "gh":
        return fetch_gh(name, fill, weight)
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
    for kt, (name, fill, weight, mirror, *more) in GLYPHS.items():
        opts = more[0] if more else {}
        src = opts.get("src", "npm")
        ds = fetch(name, fill, weight, src)
        if "part" in opts:
            # One subpath of a glyph: the path split where an absolute move starts.
            whole = " ".join(ds)
            parts = ["M" + x for x in whole.split("M") if x.strip()]
            ds = [parts[opts["part"]].strip()]
        args = ", ".join(f'"{d}"' for d in ds)
        how = (", flipped" if opts.get("flip") else "") + (", from Google's repository" if src == "gh" else "")
        lines.append(f'    /** {name}{" filled" if fill else ""}, weight {weight}{how}. */')
        if "centre" in opts:
            cx, cy = opts["centre"]
            k = 10.0 / opts["reach"]
            lines.append(f'    val {kt}: ImageVector by lazy {{ symbolPart("{kt}", {k:.4f}f, {(12 - cx) * k:.4f}f, '
                         f'{(12 - cy) * k:.4f}f, {args}) }}')
        elif opts or src == "gh":
            port = "24f" if src == "gh" else "960f"
            lines.append(f'    val {kt}: ImageVector by lazy {{ symbolTurned("{kt}", {str(mirror).lower()}, {port}, '
                         f'{str(bool(opts.get("flip"))).lower()}, {float(opts.get("rotate", 0))}f, {args}) }}')
        else:
            lines.append(f'    val {kt}: ImageVector by lazy {{ symbol("{kt}", {str(mirror).lower()}, {args}) }}')
    lines += [
        "",
        "    /** The weight-600 twin of a glyph a sheet tile carries (SheetIconTile: 24 semibold), else the glyph. */",
        "    fun semibold(v: ImageVector): ImageVector = when (v.name) {",
    ]
    for n in SEMIBOLD_TWINS:
        lines.append(f'        "{n}" -> {n}Semibold')
    lines += [
        "        else -> v",
        "    }",
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
        "/** One part of a set glyph on Google's 24 grid, scaled about the centre and moved there. */",
        "private fun symbolPart(name: String, scale: Float, dx: Float, dy: Float, vararg paths: String): ImageVector {",
        "    val b = ImageVector.Builder(name, 24.dp, 24.dp, 24f, 24f)",
        "    b.addGroup(pivotX = 12f, pivotY = 12f, scaleX = scale, scaleY = scale, translationX = dx, translationY = dy)",
        "    for (d in paths) b.addPath(addPathNodes(d), fill = SolidColor(Color.Black))",
        "    b.clearGroup()",
        "    return b.build()",
        "}",
        "",
        "/** A set glyph turned or flipped about its centre, on the npm grid (960) or Google's repository's (24). */",
        "private fun symbolTurned(name: String, mirror: Boolean, port: Float, flip: Boolean, rotate: Float, vararg paths: String): ImageVector {",
        "    val b = ImageVector.Builder(name, 24.dp, 24.dp, port, port, autoMirror = mirror)",
        "    b.addGroup(rotate = rotate, pivotX = port / 2, pivotY = port / 2, scaleX = if (flip) -1f else 1f)",
        "    if (port == 960f) b.addGroup(translationY = 960f)",
        "    for (d in paths) b.addPath(addPathNodes(d), fill = SolidColor(Color.Black))",
        "    if (port == 960f) b.clearGroup()",
        "    b.clearGroup()",
        "    return b.build()",
        "}",
        "",
    ]
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT.relative_to(ROOT)}: {len(GLYPHS)} glyphs")


if __name__ == "__main__":
    main()
