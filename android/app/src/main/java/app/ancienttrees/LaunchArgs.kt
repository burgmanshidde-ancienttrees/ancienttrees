// The iPhone's launch arguments (ContentView.swift, MapTab.swift), so the parity
// script opens the same state on both phones: `-open=tree:ath_004`,
// `-select=ath_004`, `-at=37.97,23.72`, `-sheet=full|half|card`, `-search[=lis]`, `-signin`, `-tab=2`.
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

    /** -sheet=full, -sheet=half, -sheet=card, else the peek (MapTab.swift). */
    val sheet: app.ancienttrees.ui.SheetHeight
        get() = when {
            "-sheet=full" in args -> app.ancienttrees.ui.SheetHeight.FULL
            "-sheet=half" in args -> app.ancienttrees.ui.SheetHeight.HALF
            "-sheet=card" in args -> app.ancienttrees.ui.SheetHeight.CARD
            else -> app.ancienttrees.ui.SheetHeight.PEEK
        }

    /** -search opens the map's search empty, -search=lis with that typed. */
    val search: String?
        get() = if ("-search" in args) "" else value("-search")
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

        /**
         * am splits --esa on every comma, so "-at=52.37,4.89" may arrive as two
         * pieces, or with the escaping backslash still in it: put it back together.
         */
        fun normalise(raw: List<String>): List<String> {
            val out = ArrayList<String>()
            for (a in raw.map { it.replace("\\", "") }) {
                val last = out.lastOrNull()
                if (last != null && last.startsWith("-at=") && ',' !in last && a.toDoubleOrNull() != null) {
                    out[out.size - 1] = "$last,$a"
                } else {
                    out.add(a)
                }
            }
            return out
        }

        fun from(intent: Intent?, appInfo: ApplicationInfo): LaunchArgs {
            if (appInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE == 0) return NONE
            return LaunchArgs(normalise(intent?.getStringArrayExtra("args")?.toList().orEmpty()))
        }
    }
}
