# R8 for the release build (app/build.gradle.kts). MapLibre, AndroidX, Compose
# and Play's review library ship their own consumer rules; the app reads its
# feeds with Android's built-in org.json and finds nothing by reflection, so
# what is left is keeping a crash readable.

# Line numbers in crash traces; Play reads the mapping file the bundle carries.
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile

# MapLibre's native code calls back into Java by name.
-keep class org.maplibre.** { *; }
-dontwarn org.maplibre.**
