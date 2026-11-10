// The iPhone's launch arguments (ContentView.swift, MapTab.swift), so the parity
// script opens the same state on both phones: `-open=tree:ath_004`,
// `-select=ath_004`, `-at=37.97,23.72`, `-sheet=full`, `-signin`, `-tab=2`.
// Read only from a debuggable build, passed as
//   adb shell am start -n app.ancienttrees.android/app.ancienttrees.MainActivity --esa args "-tab=0,-open=tree:ath_004"

package app.ancienttrees

import android.content.Intent
import android.content.pm.ApplicationInfo

data class LaunchArgs(val args: List<String>) {
    private fun value(key: String): String? = args.firstOrNull { it.startsWith("$key=") }?.substringAfter("=")

    val tab: Int? get() = value("-tab")?.toIntOrNull()
    val select: String? get() = value("-select")
    val openTree: String? get() = value("-open")?.takeIf { it.startsWith("tree:") }?.removePrefix("tree:")
    val sheetFull: Boolean get() = "-sheet=full" in args
    val signIn: Boolean get() = "-signin" in args

    /** A fixed position, as the iPhone's sweep stands in Athens without a real fix. */
    val at: Pair<Double, Double>?
        get() = value("-at")?.split(",")?.takeIf { it.size == 2 }?.let { p ->
            val lat = p[0].toDoubleOrNull()
            val lng = p[1].toDoubleOrNull()
            if (lat != null && lng != null) lat to lng else null
        }

    companion object {
        val NONE = LaunchArgs(emptyList())

        fun from(intent: Intent?, appInfo: ApplicationInfo): LaunchArgs {
            if (appInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE == 0) return NONE
            return LaunchArgs(intent?.getStringArrayExtra("args")?.toList().orEmpty())
        }
    }
}
