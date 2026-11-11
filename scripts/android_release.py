#!/usr/bin/env python3
"""android_release.py - the Android app as Google Play takes it: a signed .aab.

Builds `bundleRelease` (R8 on, app/build.gradle.kts) signed with the upload key
from ~/.ancienttrees-android.env (keystore ~/.ancienttrees-android-upload.jks,
both outside the repository, never committed), checks the signature, and copies
the bundle to out/play/ancient-trees-<versionName>-<versionCode>.aab for the
Play Console upload.

    python3 scripts/android_release.py              # the signed .aab
    python3 scripts/android_release.py --apk        # also a signed release .apk, for the emulator
    python3 scripts/android_release.py --install    # --apk, then install it on the emulator (lock taken)
    python3 scripts/android_release.py --fingerprint  # the upload key's SHA-256 only

Exit 1 when the key is missing, the build fails, or the bundle is unsigned.
CI builds the same bundle unsigned (android.yml, job release) to catch a broken
release build; only this script, on the Mac with the key, makes the upload.
"""
import pathlib
import re
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

ROOT = pathlib.Path(__file__).resolve().parent.parent
ANDROID = ROOT / "android"
SDK = pathlib.Path.home() / "Library" / "Android" / "sdk"
JBR = pathlib.Path("/Applications/Android Studio.app/Contents/jbr/Contents/Home")
ENV = pathlib.Path.home() / ".ancienttrees-android.env"
OUT = ROOT / "out" / "play"


def key():
    if not ENV.exists():
        sys.exit(f"no upload key: {ENV} is missing")
    k = {}
    for line in ENV.read_text().splitlines():
        a, _, b = line.strip().removeprefix("export ").partition("=")
        if a and b:
            k[a.strip()] = b.strip().strip('"').strip("'")
    if not pathlib.Path(k.get("ANCIENTTREES_UPLOAD_STORE_FILE", "")).exists():
        sys.exit("no upload key: the keystore named in " + str(ENV) + " is missing")
    return k


def keytool():
    for p in (JBR / "bin" / "keytool", pathlib.Path("/usr/bin/keytool")):
        if p.exists():
            return str(p)
    sys.exit("no keytool")


def fingerprint(k):
    out = subprocess.run(
        [keytool(), "-list", "-v", "-keystore", k["ANCIENTTREES_UPLOAD_STORE_FILE"],
         "-storepass", k["ANCIENTTREES_UPLOAD_STORE_PASSWORD"], "-alias", k["ANCIENTTREES_UPLOAD_KEY_ALIAS"]],
        capture_output=True, text=True, check=True).stdout
    m = re.search(r"SHA256:\s*([0-9A-F:]+)", out)
    return m.group(1) if m else ""


def version():
    s = (ANDROID / "app" / "build.gradle.kts").read_text()
    name = re.search(r'versionName\s*=\s*"([^"]+)"', s).group(1)
    code = re.search(r"versionCode\s*=\s*(\d+)", s).group(1)
    return name, code


def gradle(*tasks):
    env = dict(__import__("os").environ, ANDROID_HOME=str(SDK))
    if JBR.exists():
        env["JAVA_HOME"] = str(JBR)
    r = subprocess.run(["./gradlew", "-q", *tasks], cwd=ANDROID, env=env)
    if r.returncode:
        sys.exit("gradle failed: " + " ".join(tasks))


def signed_by_upload_key(path, fp):
    """jarsigner prints the signer's certificate; its SHA-256 must be the upload key's."""
    out = subprocess.run([keytool(), "-printcert", "-jarfile", str(path)], capture_output=True, text=True).stdout
    m = re.search(r"SHA256:\s*([0-9A-F:]+)", out)
    return bool(m) and m.group(1) == fp


def main():
    args = sys.argv[1:]
    k = key()
    fp = fingerprint(k)
    print("upload key SHA-256: " + fp)
    if "--fingerprint" in args:
        return
    apk = "--apk" in args or "--install" in args
    gradle("bundleRelease", *(["assembleRelease"] if apk else []))
    name, code = version()
    OUT.mkdir(parents=True, exist_ok=True)
    aab = ANDROID / "app" / "build" / "outputs" / "bundle" / "release" / "app-release.aab"
    if not signed_by_upload_key(aab, fp):
        sys.exit("the bundle is not signed with the upload key")
    dest = OUT / f"ancient-trees-{name}-{code}.aab"
    shutil.copy2(aab, dest)
    print(f"bundle: {dest.relative_to(ROOT)} ({dest.stat().st_size // 1024} KB), signed with the upload key")
    if apk:
        built = ANDROID / "app" / "build" / "outputs" / "apk" / "release" / "app-release.apk"
        dest_apk = OUT / f"ancient-trees-{name}-{code}.apk"
        shutil.copy2(built, dest_apk)
        print(f"apk: {dest_apk.relative_to(ROOT)} ({dest_apk.stat().st_size // 1024} KB)")
        if "--install" in args:
            from emulator_lock import emulator
            adb = str(SDK / "platform-tools" / "adb")
            with emulator("android_release"):
                # A debug build has another signature: it goes first, or the install is refused.
                subprocess.run([adb, "uninstall", "app.ancienttrees.android"], capture_output=True)
                r = subprocess.run([adb, "install", "-r", str(dest_apk)])
                if r.returncode:
                    sys.exit("install failed")
            print("installed the release build on the emulator")


if __name__ == "__main__":
    main()
