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

    /** -open=mine:<id>: a tree of your own (ContentView .mine). */
    val openMine: String? get() = value("-open")?.takeIf { it.startsWith("mine:") }?.removePrefix("mine:")

    /** -open=city:<slug>: the map looking at that city, its place header in the sheet (ContentView.debugRoute). */
    val openCity: String? get() = value("-open")?.takeIf { it.startsWith("city:") }?.removePrefix("city:")

    /** -open=species:<Common name>: the species page (Species.swift). */
    val openSpecies: String? get() = value("-open")?.takeIf { it.startsWith("species:") }?.removePrefix("species:")

    /** -placepin and -speciespick: the opened tree's pin map and species chooser (TreeDetail.swift). */
    val placePin: Boolean get() = "-placepin" in args
    val speciesPick: Boolean get() = "-speciespick" in args

    /** -mine-demo: two of your own trees, drawn, nothing sent (Sightings.seedDemo). */
    val mineDemo: Boolean get() = "-mine-demo" in args

    /** -lane=want: My trees opens on Want to visit. */
    val laneWant: Boolean get() = "-lane=want" in args

    /** -collected=<ids> and -saved=<ids>: the lanes with trees in them (Saved.seedFromLaunchArguments). */
    val collectedIds: List<String> get() = value("-collected")?.split(",")?.filter { it.isNotBlank() }.orEmpty()
    val savedIds: List<String> get() = value("-saved")?.split(",")?.filter { it.isNotBlank() }.orEmpty()

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

    /** -photo: the opened tree's photograph full screen (TreeDetail.swift). */
    val photo: Boolean get() = "-photo" in args

    /** -collect opens the collect flow; -collect-place and the rest open its steps (Launch.swift). */
    val collectOpen: Boolean get() = "-collect" in args || "-spot" in args || "-add" in args
    val collect: app.ancienttrees.ui.CollectLaunch
        get() = app.ancienttrees.ui.CollectLaunch(
            place = "-collect-place" in args,
            identify = "-collect-identify" in args,
            ticked = "-collect-ticked" in args,
            voted = "-collect-voted" in args,
            compare = "-collect-compare" in args,
            describe = "-collect-describe" in args,
        )

    /** -signed-in: the sweep's stand-in for an account, debug builds only; nothing is sent without a real one. */
    val signedIn: Boolean get() = "-signed-in" in args

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
