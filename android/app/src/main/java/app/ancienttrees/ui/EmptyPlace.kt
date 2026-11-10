// A place we have no trees for becomes an ask to add one (Hidde, 2026-10-25),
// ported from ios Screens/EmptyPlace.swift.
//
// Google Maps and Apple Maps answer a search for any real town, whatever their
// own data holds there. The iPhone finds the town through Apple's own
// MKLocalSearch (localities only); Android uses the platform's own
// android.location.Geocoder (Google's geocoder on Play phones, no extra library
// or service, hard list 5), keeping only answers that name a locality.

package app.ancienttrees.ui

import android.content.Context
import android.location.Address
import android.location.Geocoder
import android.os.Build
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.Geo
import app.ancienttrees.feed.Tree
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull
import java.util.Locale
import kotlin.coroutines.resume

/** A real town the geocoder knows, which may hold none of our trees. */
data class RealPlace(val name: String, val country: String, val lat: Double, val lng: Double) {
    val id: String get() = "$name|$country|${(lat * 100).toInt()}|${(lng * 100).toInt()}"
}

object EmptyPlace {
    /** Zoom 11 or so: a town and the country lanes around it. */
    const val SPAN_METRES = 20_000.0

    /**
     * Towns matching the query, localities only, at most five. Empty on any
     * failure (offline, no geocoder on the phone), which the screen reads as
     * "nothing matches", the honest thing to say when nothing came back.
     */
    suspend fun lookup(context: Context, query: String): List<RealPlace> {
        if (!Geocoder.isPresent()) return emptyList()
        val g = Geocoder(context.applicationContext, Locale.getDefault())
        val found: List<Address> = withTimeoutOrNull(8_000) {
            if (Build.VERSION.SDK_INT >= 33) {
                suspendCancellableCoroutine { cont ->
                    runCatching {
                        g.getFromLocationName(query, 10, object : Geocoder.GeocodeListener {
                            override fun onGeocode(addresses: MutableList<Address>) { if (cont.isActive) cont.resume(addresses) }
                            override fun onError(errorMessage: String?) { if (cont.isActive) cont.resume(emptyList()) }
                        })
                    }.onFailure { if (cont.isActive) cont.resume(emptyList()) }
                }
            } else {
                withContext(Dispatchers.IO) {
                    @Suppress("DEPRECATION")
                    runCatching { g.getFromLocationName(query, 10).orEmpty() }.getOrDefault(emptyList())
                }
            }
        }.orEmpty()
        return towns(found.map { Town(it.locality, it.countryName, it.latitude, it.longitude) })
    }

    /** One geocoder answer, free of Android so the filter is testable. */
    data class Town(val locality: String?, val country: String?, val lat: Double, val lng: Double)

    /** Localities only, one per name and country, at most five. */
    fun towns(found: List<Town>): List<RealPlace> {
        val seen = HashSet<String>()
        val out = ArrayList<RealPlace>()
        for (a in found) {
            val name = a.locality?.ifBlank { null } ?: continue
            val country = a.country.orEmpty()
            if (!seen.add("$name|$country")) continue
            out.add(RealPlace(name, country, a.lat, a.lng))
        }
        return out.take(5)
    }

    /** The nearest tree in our catalogue to a point, and how far. */
    fun nearest(c: Catalogue, lat: Double, lng: Double): Pair<Tree, Double>? =
        c.trees.map { it to Geo.km(lat, lng, it.lat, it.lng) }.minByOrNull { it.second }

    /** "27 km", "3.4 km": whole numbers once the decimal stops meaning anything. */
    fun distance(km: Double, metric: Boolean = true): String {
        val v = if (metric) km else km * 0.621371
        val u = if (metric) "km" else "mi"
        return if (v < 10) String.format(Locale.US, "%.1f %s", v, u) else "${Math.round(v)} $u"
    }
}
