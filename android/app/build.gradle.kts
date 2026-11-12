import java.util.Properties

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

// THE UPLOAD KEY for Google Play (scripts/android_release.py). Read from the
// environment, else from ~/.ancienttrees-android.env, else local.properties;
// the keystore itself lives at ~/.ancienttrees-android-upload.jks and never in
// the repository (it is public). Without them the release build comes out
// unsigned, which is what CI builds to prove the release still compiles.
// Play App Signing re-signs what reaches a phone; this key only proves the
// upload is ours, and Google can reset it if it is ever lost.
val uploadKey: Map<String, String> = run {
    val keys = listOf(
        "ANCIENTTREES_UPLOAD_STORE_FILE",
        "ANCIENTTREES_UPLOAD_STORE_PASSWORD",
        "ANCIENTTREES_UPLOAD_KEY_ALIAS",
        "ANCIENTTREES_UPLOAD_KEY_PASSWORD",
    )
    val found = HashMap<String, String>()
    val home = File(System.getProperty("user.home"), ".ancienttrees-android.env")
    if (home.exists()) {
        home.readLines().forEach { line ->
            val k = line.substringBefore("=").trim().removePrefix("export ").trim()
            val v = line.substringAfter("=", "").trim().trim('"', '\'')
            if (k in keys && v.isNotEmpty()) found[k] = v
        }
    }
    val local = rootProject.file("local.properties")
    if (local.exists()) {
        val props = Properties().apply { local.inputStream().use { load(it) } }
        keys.forEach { k -> props.getProperty(k)?.takeIf { it.isNotEmpty() }?.let { found[k] = it } }
    }
    keys.forEach { k -> System.getenv(k)?.takeIf { it.isNotEmpty() }?.let { found[k] = it } }
    if (keys.all { it in found } && File(found.getValue(keys[0])).exists()) found else emptyMap()
}

android {
    namespace = "app.ancienttrees"
    compileSdk = 36

    defaultConfig {
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        applicationId = "app.ancienttrees.android"
        minSdk = 26
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0"
    }

    buildFeatures { compose = true }

    signingConfigs {
        if (uploadKey.isNotEmpty()) {
            create("upload") {
                storeFile = File(uploadKey.getValue("ANCIENTTREES_UPLOAD_STORE_FILE"))
                storePassword = uploadKey.getValue("ANCIENTTREES_UPLOAD_STORE_PASSWORD")
                keyAlias = uploadKey.getValue("ANCIENTTREES_UPLOAD_KEY_ALIAS")
                keyPassword = uploadKey.getValue("ANCIENTTREES_UPLOAD_KEY_PASSWORD")
            }
        }
    }

    buildTypes {
        getByName("release") {
            // R8 shrinks and renames; proguard-rules.pro keeps what is found by name.
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            if (uploadKey.isNotEmpty()) signingConfig = signingConfigs.getByName("upload")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    // THE SAME BUNDLED CATALOGUE AS THE IPHONE, read from where release.py
    // refreshes it, so there is no second 13 MB copy in the repository to go
    // stale.
    sourceSets {
        getByName("main") {
            assets.srcDir("../../ios/AncientTrees/AncientTrees/Data")
            // THE MAP'S STYLE AS THE SITE SERVES IT, so a first launch draws pins
            // without waiting on the network for it (map/TreeMapView.kt styleFromDisk).
            assets.srcDir(layout.buildDirectory.dir("generated/mapstyle"))
        }
    }
}

// Bytecode for Java 17, built by whichever JDK runs Gradle (Android Studio's
// own 21 or 25, or CI's 17). No toolchain demand: a demand for an exact JDK the
// Mac does not have is what stopped the first sync (2026-11-10).
kotlin { compilerOptions { jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17) } }

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2025.12.00")
    implementation(composeBom)
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.foundation:foundation")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.activity:activity-compose:1.10.1")
    implementation("androidx.core:core-ktx:1.16.0")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.9.4")
    implementation("androidx.exifinterface:exifinterface:1.3.7")
    // Custom Tabs: Android's in-app browser for Apple and Google sign-in (Account.kt).
    implementation("androidx.browser:browser:1.8.0")
    // MapLibre's attribution dialog is an AppCompat dialog.
    implementation("androidx.appcompat:appcompat:1.7.0")

    // The one map engine, the same one the iPhone app and the website draw with.
    implementation("org.maplibre.gl:android-sdk:13.7.1")
    // Google Play's in-app review card (ui/ReviewAsk.kt; Hidde, 2026-11-10: "prima doe dat").
    implementation("com.google.android.play:review:2.0.2")
    // The iPhone's frosted glass behind the tab bar and the photo buttons: a
    // backdrop blur on Android 12+ (ui/Glass.kt). 1.7.2 is the release built
    // against this app's Compose 1.10 and Kotlin 2.2.21 (hard list 5).
    implementation("dev.chrisbanes.haze:haze:1.7.2")

    testImplementation("junit:junit:4.13.2")
    // The flow walk on the emulator (FlowWalk.kt), the iPhone's FlowWalk.swift.
    androidTestImplementation(composeBom)
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    // 3.7 and 1.7 or later: older Espresso calls InputManager.getInstance, gone on Android 37.
    androidTestImplementation("androidx.test.ext:junit:1.3.0")
    androidTestImplementation("androidx.test:runner:1.7.0")
    androidTestImplementation("androidx.test:core:1.7.0")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.7.0")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
    // Android has org.json built in; a test on the build machine needs a copy.
    testImplementation("org.json:json:20250107")
}

// The two map styles from the website's own assets, copied into the app's assets.
val copyMapStyle by tasks.registering(Sync::class) {
    from("../../site/public/assets") { include("map-style.json", "map-style-dark.json") }
    into(layout.buildDirectory.dir("generated/mapstyle/map-style"))
}
tasks.matching { it.name.startsWith("merge") && it.name.endsWith("Assets") }.configureEach { dependsOn(copyMapStyle) }
tasks.matching { it.name.contains("lint", ignoreCase = true) }.configureEach { mustRunAfter(copyMapStyle) }
