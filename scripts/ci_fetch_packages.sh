#!/bin/bash
# Fetch the app's Swift packages on a CI Mac, retried, before anything builds.
#
# 2026-11-08: MapLibre's binary download failed on most macos-15 runners that
# morning. SwiftPM's first try spends ~17 s and fails; every later try fails
# in half a second with "already exists in file system", even after
# ~/Library/Caches/org.swift.swiftpm/artifacts was removed, so something else
# holds the half-file. This clears every SwiftPM cache there is between tries
# and, when a try fails, says what GitHub itself answers for the zip, so a red
# step says whether the download or SwiftPM is at fault.
#
#   bash scripts/ci_fetch_packages.sh
set -u
URL="https://github.com/maplibre/maplibre-native/releases/download/ios-v6.28.0/MapLibre.dynamic.xcframework.zip"
for i in 1 2 3 4; do
  rm -rf ~/Library/Caches/org.swift.swiftpm ~/Library/org.swift.swiftpm \
         ~/Library/Developer/Xcode/DerivedData /tmp/dd/SourcePackages
  if xcodebuild -resolvePackageDependencies \
       -project ios/AncientTrees/AncientTrees.xcodeproj -scheme AncientTrees; then
    echo "packages resolved on try $i"
    exit 0
  fi
  echo "try $i failed; GitHub answers for the MapLibre zip:"
  curl -sS -o /dev/null -L -m 60 -w "  http %{http_code}, %{size_download} bytes, %{time_total}s\n" "$URL" || true
  sleep $((i * 15))
done
echo "::error::could not fetch the packages (MapLibre) in four tries"
exit 1
