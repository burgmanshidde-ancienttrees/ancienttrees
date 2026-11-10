plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "app.ancienttrees"
    compileSdk = 36

    defaultConfig {
        applicationId = "app.ancienttrees.android"
        minSdk = 26
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0"
    }

    buildFeatures { compose = true }

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
        }
    }
}

kotlin { jvmToolchain(17) }

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2025.12.00")
    implementation(composeBom)
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.foundation:foundation")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.activity:activity-compose:1.10.1")
    implementation("androidx.core:core-ktx:1.16.0")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.9.4")
    // MapLibre's attribution dialog is an AppCompat dialog.
    implementation("androidx.appcompat:appcompat:1.7.0")

    // The one map engine, the same one the iPhone app and the website draw with.
    implementation("org.maplibre.gl:android-sdk:13.7.1")

    testImplementation("junit:junit:4.13.2")
    // Android has org.json built in; a test on the build machine needs a copy.
    testImplementation("org.json:json:20250107")
}
