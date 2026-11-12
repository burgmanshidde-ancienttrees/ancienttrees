#!/usr/bin/env python3
"""android_parity.py - the iPhone and Android side by side, screen by screen.

Hidde, 2026-11-10: "ik wil dat je de ios build 42 exact na bouwt qua interactie
en alles ik wil niet alles weer opnieuw aan je moeten vertellen". The iOS app is
the specification (DECISIONS.md 2026-11-10); a screen is done when its iOS and
Android screenshots of the same state sit side by side with no difference
nobody can name a reason for. This makes those pairs and the page he reads.

    python3 scripts/android_parity.py                    # every frame
    python3 scripts/android_parity.py --only tree map    # some frames
    python3 scripts/android_parity.py --no-ios           # reuse the iPhone shots
    python3 scripts/android_parity.py --no-build         # reuse the Android build
    python3 scripts/android_parity.py --check            # only the type and icon check

iPhone shots come from scripts/appsweep.py (the same launch arguments,
SweepFrames.swift), on the iPhone 17 Pro. Android shots come from the running
emulator through adb, launched with the same arguments (LaunchArgs.kt). The
status per screen, its open differences and the differences Android forces live
in data/android-parity.json, which this page shows and never writes.

Writes out/parity/index.html, out/parity/ios/*.png, out/parity/android/*.png.
"""
import argparse
import hashlib
import html
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "parity"
STATUS = ROOT / "data" / "android-parity.json"
SDK = pathlib.Path.home() / "Library" / "Android" / "sdk"
ADB = str(SDK / "platform-tools" / "adb")
JBR = "/Applications/Android Studio.app/Contents/jbr/Contents/Home"
PACKAGE = "app.ancienttrees.android"
ACTIVITY = PACKAGE + "/app.ancienttrees.MainActivity"
IOS_DEVICE = "iPhone 17 Pro"
# appsweep.py stands every frame at Dam square unless the frame names its own
# place, so the Android frame does too.
ORIGIN = "-at=52.3731,4.8922"
# The iPhone simulator's region (defaults read -g AppleLocale: en_NL). Units and
# the profile's country follow the phone's region on both phones, so Android
# stands in the same one, not the emulator's en_US (LaunchArgs.locale).
REGION = "-AppleLocale=en_NL"

# name -> the iPhone's launch arguments, taken from appsweep.py itself (which
# picks real subject trees out of the bundled feed: the longest name with a
# photograph, and so on), so both phones open the very same state. The same
# arguments go to Android; LaunchArgs.kt reads the ones it knows.
sys.path.insert(0, str(ROOT / "scripts"))
import appsweep  # noqa: E402
from emulator_lock import emulator  # noqa: E402

FRAMES = {name: list(args) for name, args, _ in appsweep.screens(appsweep.pick_subjects())}
# The screens with an Android port, in the order the page shows them.
PORTED = ["map", "map-full", "map-bar", "map-pin", "search", "tree", "tree-nophoto", "photo-viewer", "signin",
          "explore", "collection-tab", "collection-tab-full", "own-tree", "profile", "profile-signed-in",
          "profile-edit", "signin-email", "refused", "people", "early-adopter", "early-adopter-sheet",
          "collect-intro", "collect-away", "collect-place", "collect-identify", "collect-ticked", "collect-voted",
          "collect-compare", "collect-describe", "city", "city-map-full", "place-pin", "species", "collection", "species-pick",
          "directions", "review-ask", "contribute", "feedback"]


def run(cmd, **kw):
    return subprocess.run(cmd, check=False, text=True, capture_output=True, **kw)


LIVE_VERSION = "https://ancienttrees.app/api/version.json"


def live_version():
    """The live catalogue's version, or None offline."""
    import urllib.request
    try:
        with urllib.request.urlopen(LIVE_VERSION, timeout=20) as r:
            return json.loads(r.read().decode()).get("version")
    except Exception:
        return None


def wait_for_catalogue(read_head, who, version):
    """Until the phone holds the live catalogue (its download starts with the version).

    THE SAME TREES ON BOTH PHONES (review 2026-11-11: "All 22 trees" on the
    iPhone, "All 23" on Android, other ages). Both apps bundle the very same
    file (android/app/build.gradle.kts reads ios/.../Data as its assets), but
    both read a download over it when they have one and refresh at every launch,
    and the iPhone simulator still held a download from the day before while the
    emulator had today's. So both are brought to the live catalogue before the
    first frame: the app is opened and given time to finish its refresh."""
    if not version:
        print(f"{who}: live version unknown (offline?), frames may show different catalogues")
        return
    for _ in range(45):
        if version in (read_head() or ""):
            return
        time.sleep(2)
    print(f"{who}: still not on the live catalogue {version} after 90 s; frames may differ in trees")


def ios_warm(version):
    """Open the app once on the iPhone and wait for its refresh to land."""
    devices = json.loads(run(["xcrun", "simctl", "list", "devices", "-j"]).stdout or "{}").get("devices", {})
    udid = next((d["udid"] for ds in devices.values() for d in ds if d["name"] == IOS_DEVICE and d.get("isAvailable")), None)
    if not udid:
        return
    run(["xcrun", "simctl", "boot", udid])
    run(["xcrun", "simctl", "launch", udid, appsweep.BUNDLE, ORIGIN, "-no-cover"])

    def head():
        data = run(["xcrun", "simctl", "get_app_container", udid, appsweep.BUNDLE, "data"]).stdout.strip()
        f = pathlib.Path(data) / "Library" / "Application Support" / "catalogue" / "trees.json"
        return f.open().read(80) if data and f.exists() else ""
    wait_for_catalogue(head, "ios", version)
    run(["xcrun", "simctl", "terminate", udid, appsweep.BUNDLE])


def ios(frames, build):
    out = OUT / "ios-sweep"
    ios_warm(live_version())
    for i, name in enumerate(frames):
        cmd = [sys.executable, str(ROOT / "scripts" / "appsweep.py"), "--only", name,
               "--device", IOS_DEVICE, "--out", str(out)]
        if not build or i > 0:
            cmd.append("--no-build")
        r = run(cmd)
        shot = next(out.rglob(f"{name}.png"), None)
        if shot:
            shutil.copy(shot, OUT / "ios" / f"{name}.png")
        else:
            print(f"ios {name}: no screenshot\n{r.stdout[-400:]}{r.stderr[-400:]}")


def android(frames, build):
    """The Android half, under the emulator lock: other sessions share the emulator."""
    with emulator("android_parity"):
        _android(frames, build)


def _android(frames, build):
    if build:
        env = dict(os.environ, JAVA_HOME=JBR, ANDROID_HOME=str(SDK))
        r = run(["./gradlew", "-q", "assembleDebug"], cwd=ROOT / "android", env=env)
        if r.returncode != 0:
            sys.exit("android build failed:\n" + r.stdout[-2000:] + r.stderr[-2000:])
        install_debug()
        # LOCATION GRANTED BEFORE ANY START (2026-11-10, Hidde watching the
        # emulator: the system's location question stood alone over the home
        # screen). A start without -at asks on first open, as the iPhone does;
        # the next frame's force-stop then ends the app and leaves the system's
        # dialog orphaned. The frames stand at a fixed place anyway.
        for perm in ("android.permission.ACCESS_FINE_LOCATION", "android.permission.ACCESS_COARSE_LOCATION"):
            run([ADB, "shell", "pm", "grant", PACKAGE, perm])
        # After an install the system UI restarts the app by itself a moment
        # later, without our extras (a CLEAR_TASK start from systemui, API 37):
        # let that happen before the first frame.
        run([ADB, "shell", "am", "start", "-W", "-n", ACTIVITY])
        time.sleep(10)
    # The live catalogue on the phone before the first frame, as on the iPhone (ios_warm).
    run([ADB, "shell", "am", "start", "-n", ACTIVITY, "--esa", "args", "'" + ORIGIN.replace(",", "\\,") + ",-no-cover'"])
    wait_for_catalogue(lambda: run([ADB, "exec-out", "run-as", PACKAGE, "head", "-c", "80", "files/catalogue/trees.json"]).stdout,
                       "android", live_version())
    # A RELEASE BUILD IGNORES EVERY LAUNCH ARGUMENT (LaunchArgs.from reads them
    # only when the app is debuggable). Found 2026-11-11: another session had left
    # a release build installed, the debug install failed on the signature, and
    # 37 frames were the same default map. So the build on the phone is checked
    # whether or not this run installed it.
    require_debuggable()
    for name in frames:
        run([ADB, "shell", "am", "force-stop", PACKAGE])
        # The sweep's origin FIRST, as appsweep.py launches (ORIGIN, then the
        # frame's own), and the first -at wins on both phones: collect-away
        # stands at Dam square on the iPhone, so it does here too.
        args = [ORIGIN, REGION] + FRAMES[name]
        # am splits --esa on commas; a comma inside one argument (-at=lat,lng)
        # is written \, and the whole list quoted for the device's shell.
        joined = ",".join(a.replace(",", "\\,") for a in args)
        run([ADB, "logcat", "-c"])
        # A fresh task: Recents otherwise brings the last screen back with its old intent.
        run([ADB, "shell", "am", "start", "-W", "--activity-clear-task", "-n", ACTIVITY, "--esa", "args", "'" + joined + "'"])
        # Until the app says its catalogue is read (MainActivity logs it), then
        # time for the tiles and the photographs.
        for _ in range(90):
            if "catalogue" in run([ADB, "logcat", "-d", "-s", "AncientTrees"]).stdout:
                break
            time.sleep(1)
        time.sleep(8)
        png = subprocess.run([ADB, "exec-out", "screencap", "-p"], capture_output=True)
        (OUT / "android" / f"{name}.png").write_bytes(png.stdout)


APK = ROOT / "android/app/build/outputs/apk/debug/app-debug.apk"


def install_debug():
    """Install the debug build, or stop. A build signed with another key (a
    release build another session left, android_release.py --install) refuses
    `install -r` with INSTALL_FAILED_UPDATE_INCOMPATIBLE: that one is uninstalled
    and the debug build installed fresh. Any other failure ends the run."""
    r = run([ADB, "install", "-r", str(APK)])
    if "Success" not in r.stdout:
        why = (r.stdout + r.stderr).strip()
        if "INCOMPATIBLE" in why or "signatures do not match" in why:
            print("android: another build's signature on the phone; uninstalling it for the debug build")
            run([ADB, "uninstall", PACKAGE])
            r = run([ADB, "install", str(APK)])
            why = (r.stdout + r.stderr).strip()
        if "Success" not in r.stdout:
            sys.exit("android: adb install failed, so every frame would show whatever build is on the phone:\n" + why[-1500:])


def require_debuggable():
    flags = run([ADB, "shell", "dumpsys", "package", PACKAGE]).stdout
    line = next((l for l in flags.splitlines() if "flags=[" in l), "")
    if "DEBUGGABLE" not in line:
        sys.exit("android: the build on the phone is not debuggable (a release build?), so it ignores every "
                 "launch argument and every frame would be the default map. Run without --no-build.")


# Frames that are the same picture on the iPhone too, so the same picture on
# Android is no fault: -show-email changes nothing since the email route shows
# by default (Launch.emailSignIn), on both phones.
SAME_ON_BOTH = [{"signin", "signin-email"}]


def identical_frames(frames, folder):
    """Groups of frames whose screenshots are byte for byte the same picture.

    Two launch states that photograph identically mean the arguments did not
    reach the app (a release build, a crash to the launcher, an argument the
    port does not read). A group the iPhone shares (SAME_ON_BOTH) is allowed."""
    by = {}
    for name in frames:
        f = folder / f"{name}.png"
        if f.exists() and f.stat().st_size:
            by.setdefault(hashlib.md5(f.read_bytes()).hexdigest(), []).append(name)
    return [g for g in by.values() if len(g) > 1 and set(g) not in SAME_ON_BOTH]


def page(frames, same=()):
    status = json.loads(STATUS.read_text()) if STATUS.exists() else {}
    forced = status.get("_android_forced", [])
    # scripts/android_spacing.py's measurement, when one was made: the vertical
    # gaps and heights that differ from the iPhone's by more than 2.
    sp_path = OUT / "spacing.json"
    spacing = json.loads(sp_path.read_text()) if sp_path.exists() else {}
    table = []
    rows = []
    for name in frames:
        s = status.get(name, {})
        diffs = "".join(f"<li>{html.escape(d)}</li>" for d in s.get("differences", [])) or "<li>none listed</li>"
        sp = spacing.get(name)
        if not sp:
            cell, sp_html = "not measured", ""
        elif "error" in sp:
            cell, sp_html = sp["error"], ""
        else:
            over = sp["differences"]
            cell = (f"{sp['failing']} failing, " if sp["failing"] else "") + f"{len(over)} over 2 of {sp['measured']}"
            sp_html = "".join(
                f"<li>{'<b>' if r['fails'] else ''}{r['diff']:+g}{'</b>' if r['fails'] else ''} "
                f"{html.escape(r['what'])} (iPhone {r['ios']:g}, Android {r['android']:g})"
                f"{' allowed: ' + html.escape(r['allowed']) if r.get('allowed') else ''}</li>" for r in over) or "<li>all within 2</li>"
            sp_html = f"<h3>Vertical spacing</h3><ul>{sp_html}</ul>"
        table.append(f"<tr><td><a href=\"#{html.escape(name)}\">{html.escape(name)}</a></td>"
                     f"<td>{html.escape(s.get('status', 'not-ported'))}</td><td>{html.escape(cell)}</td></tr>")
        rows.append(f"""
<section id="{html.escape(name)}">
  <h2>{html.escape(name)} <span class="st {html.escape(s.get('status', 'not-ported'))}">{html.escape(s.get('status', 'not-ported'))}</span></h2>
  <div class="pair">
    <figure><img src="ios/{name}.png" alt=""><figcaption>iPhone</figcaption></figure>
    <figure><img src="android/{name}.png" alt=""><figcaption>Android</figcaption></figure>
  </div>
  <h3>Open differences</h3><ul>{diffs}</ul>
  {sp_html}
</section>""")
    same_html = ("<p style=\"background:#FBE9E7;color:#B22222;padding:8px 12px;border-radius:8px\"><b>Not to be trusted:</b> "
                 "these Android frames are the same picture, so their launch arguments did not reach the app: "
                 + html.escape("; ".join(", ".join(g) for g in same)) + "</p>") if same else ""
    forced_html = "".join(f"<li><b>{html.escape(f['what'])}</b>: {html.escape(f['why'])}</li>" for f in forced)
    (OUT / "index.html").write_text(f"""<!doctype html><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Android next to iPhone</title>
<style>
body{{font:15px/1.45 -apple-system,system-ui,sans-serif;margin:0 auto;max-width:980px;padding:16px;color:#26301E}}
h1{{font-size:26px}} h2{{font-size:20px;margin-top:40px}} h3{{font-size:15px;margin:12px 0 4px}}
.pair{{display:flex;gap:16px}} figure{{margin:0;flex:1}} img{{width:100%;border:1px solid #E6E6E6;border-radius:12px}}
figcaption{{text-align:center;color:#5C6350;font-size:13px}}
.st{{font-size:12px;padding:2px 8px;border-radius:99px;background:#F2F2F2;vertical-align:middle}}
table{{border-collapse:collapse;font-size:14px}} td,th{{padding:3px 10px;border-bottom:1px solid #E6E6E6;text-align:left}}
.st.parity{{background:#EDF3E3;color:#4A6B2A}} .st.not-ported{{background:#FBE9E7;color:#B22222}}
</style>
<h1>Android next to iPhone</h1>
<p>Each screen in the same state on both phones. A difference without a reason is a bug.</p>
{same_html}
<h3>What Android itself forces</h3><ul>{forced_html}</ul>
<table><tr><th>Screen</th><th>Status</th><th>Vertical spacing (android_spacing.py)</th></tr>{''.join(table)}</table>
{''.join(rows)}
""")
    print(f"page: {OUT / 'index.html'}")


APP_SRC = ROOT / "android" / "app" / "src" / "main" / "java" / "app" / "ancienttrees"


def check_type_and_icons():
    """Android's text sets in Inter and its icons come from Material Symbols Rounded.

    Hidde, 2026-11-10: "waarom zijn alle lettertypes en iconen anders maak het
    zo veel hetzelfde". SF Pro and SF Symbols ship on Apple platforms only, so
    Android carries the open face and the open set closest to them
    (DECISIONS.md 2026-11-10): Inter, tracked as SF tracks (ui/Text.kt), and
    Material Symbols Rounded, generated by android/generate_symbols.py into
    ui/Symbols.kt. This refuses the ways back to Roboto and Material Icons: the
    material-icons dependency, an androidx.compose.material.icons reference,
    Material's Text imported past our Text, a text field's TextStyle with no
    face, a theme without Inter in its type scale. Run by qa.py on every push.
    Removing it needs Hidde."""
    problems = []
    gradle = ROOT / "android" / "app" / "build.gradle.kts"
    if "material-icons" in gradle.read_text():
        problems.append("android/app/build.gradle.kts: the Material Icons dependency is back; icons come from ui/Symbols.kt")
    theme = APP_SRC / "ui" / "Theme.kt"
    t = theme.read_text() if theme.exists() else ""
    if "R.font.inter_regular" not in t or "typography = Type" not in t or "fontFamily = TextFace" not in t:
        problems.append("ui/Theme.kt: the type scale no longer sets every style in Inter (TextFace); Roboto is the default again")
    if not (APP_SRC / "ui" / "Symbols.kt").exists():
        problems.append("ui/Symbols.kt is gone: run python3 android/generate_symbols.py")
    for f in sorted(APP_SRC.rglob("*.kt")):
        rel = f.relative_to(ROOT)
        src = f.read_text()
        for i, line in enumerate(src.splitlines(), 1):
            if "androidx.compose.material.icons" in line or re.search(r"\bIcons\.(Filled|Outlined|Rounded|Sharp|TwoTone|Default|AutoMirrored)\b", line):
                problems.append(f"{rel}:{i}: Material Icons; use Sym from ui/Symbols.kt (Material Symbols Rounded)")
            if f.name != "Text.kt" and re.search(r"^import androidx\.compose\.material3\.(Text|\*)$", line.strip()):
                problems.append(f"{rel}:{i}: Material's Text sets in Roboto without SF's tracking; use app.ancienttrees.ui.Text")
            if "textStyle = TextStyle(" in line and "fontFamily" not in line:
                problems.append(f"{rel}:{i}: a text field with no face falls back to Roboto; use sfStyle(...)")
            if re.search(r"FontFamily\.(Default|SansSerif)", line):
                problems.append(f"{rel}:{i}: the system face (Roboto); use TextFace")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--no-ios", action="store_true")
    ap.add_argument("--no-android", action="store_true")
    ap.add_argument("--no-build", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    problems = check_type_and_icons()
    for p in problems:
        print("FAIL", p)
    if a.check or problems:
        sys.exit(1 if problems else 0)
    frames = a.only or [f for f in PORTED if f in FRAMES]
    for d in ("ios", "android"):
        (OUT / d).mkdir(parents=True, exist_ok=True)
    if not a.no_android:
        android(frames, build=not a.no_build)
    same = identical_frames(frames, OUT / "android")
    if not a.no_ios:
        ios(frames, build=not a.no_build)
    page(frames, same)
    if same:
        # Refused, not warned: the page above shows them, but a run that made
        # them must not read as a good run.
        sys.exit("android: these frames are the same picture, so their launch arguments did not reach the app: "
                 + "; ".join(", ".join(g) for g in same))


if __name__ == "__main__":
    main()
