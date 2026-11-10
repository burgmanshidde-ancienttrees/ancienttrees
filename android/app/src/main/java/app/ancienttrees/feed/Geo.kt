// Distance on the sphere and how it is written, the twin of ios Kit/Geo.swift and
// Kit/Units.swift, and of the website's units-js.ts: the same tree is "0.4 mi"
// on every surface.

package app.ancienttrees.feed

import java.util.Locale
import kotlin.math.asin
import kotlin.math.cos
import kotlin.math.min
import kotlin.math.roundToInt
import kotlin.math.sin
import kotlin.math.sqrt

object Geo {
    private const val EARTH_RADIUS_KM = 6371.0

    /** Miles for road distance: the United States, the United Kingdom, Liberia and Myanmar. */
    private val IMPERIAL = setOf("US", "GB", "LR", "MM")

    fun km(lat1: Double, lng1: Double, lat2: Double, lng2: Double): Double {
        val dLat = Math.toRadians(lat2 - lat1)
        val dLng = Math.toRadians(lng2 - lng1)
        val h = sin(dLat / 2) * sin(dLat / 2) +
            sin(dLng / 2) * sin(dLng / 2) * cos(Math.toRadians(lat1)) * cos(Math.toRadians(lat2))
        return 2 * EARTH_RADIUS_KM * asin(min(1.0, sqrt(h)))
    }

    /** From the phone's region, never guessed from a bare language. */
    fun milesFor(region: String?): Boolean = region?.uppercase() in IMPERIAL

    fun short(km: Double, miles: Boolean): String =
        if (!miles) {
            if (km < 1) "${(km * 1000).roundToInt()} m" else String.format(Locale.ROOT, "%.1f km", km)
        } else {
            val mi = km * 0.621371
            if (mi < 0.2) "${(mi * 5280).roundToInt()} ft" else String.format(Locale.ROOT, "%.1f mi", mi)
        }
}
