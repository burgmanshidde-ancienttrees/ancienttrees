// The collect flow's decisions, ported from ios Screens/CollectSheet.swift (its
// static functions) and Kit/Sightings.swift (the names of a tree only you have).
// Pure, so every one of them is tested on a machine with no camera and no GPS,
// which is the reason the iPhone pulled them out of its view in the first place.

package app.ancienttrees.feed

import java.text.Normalizer
import java.util.Locale
import kotlin.math.abs
import kotlin.math.atan2
import kotlin.math.cos

object CollectRules {
    /** Where a coordinate came from (CollectSheet.Fix), written into the record. */
    enum class Fix(val note: String) {
        DEVICE("GPS, standing at the tree"),
        PHOTO("from the photograph's own location"),
        PLACED("placed on the map by hand"),
    }

    /** CollectSheet.Route: a coordinate we may stand behind, or the pin step. */
    sealed class Route {
        data class Settle(val fix: Fix) : Route()
        data object AskForThePin : Route()
    }

    /** Never DEVICE on a fallback position; a library photo's own coordinate beats ours. */
    fun route(cameraShot: Boolean, locationKnown: Boolean, photoHasCoordinate: Boolean): Route =
        if (cameraShot) {
            if (locationKnown) Route.Settle(Fix.DEVICE) else Route.AskForThePin
        } else {
            if (photoHasCoordinate) Route.Settle(Fix.PHOTO) else Route.AskForThePin
        }

    /** Everything within 400 m, nearest first, at most five (CollectSheet.nearby). */
    fun nearby(lat: Double, lng: Double, trees: List<Tree>): List<Tree> =
        trees.map { it to Geo.km(lat, lng, it.lat, it.lng) }
            .filter { it.second <= 0.4 }
            .sortedBy { it.second }
            .take(5)
            .map { it.first }

    /** Nothing within 400 m: the closest three within three kilometres (CollectSheet.closest). */
    fun closest(lat: Double, lng: Double, trees: List<Tree>): List<Tree> =
        trees.map { it to Geo.km(lat, lng, it.lat, it.lng) }
            .filter { it.second > 0.4 && it.second <= 3.0 }
            .sortedBy { it.second }
            .take(3)
            .map { it.first }

    /** Accents and case do not count, so "ombu" finds the Ombú. */
    fun fold(s: String): String =
        Normalizer.normalize(s, Normalizer.Form.NFD).replace(Regex("\\p{M}+"), "").lowercase(Locale.ROOT)

    /** Our trees by name, nearest first, at most eight; nothing under two letters. */
    fun search(query: String, lat: Double, lng: Double, trees: List<Tree>): List<Tree> {
        val q = fold(query.trim())
        if (q.length < 2) return emptyList()
        return trees.filter { fold(it.name).contains(q) }
            .map { it to Geo.km(lat, lng, it.lat, it.lng) }
            .sortedBy { it.second }
            .take(8)
            .map { it.first }
    }

    /** Further than `nearby` reaches, so picking it says our pin is wrong. */
    fun isFar(lat: Double, lng: Double, t: Tree): Boolean = Geo.km(lat, lng, t.lat, t.lng) > 0.4

    /** "1672 m" is a number to read, "1.7 km" is a distance. */
    fun distance(metres: Int): String =
        if (metres < 1000) "$metres m" else String.format(Locale.ROOT, "%.1f km", metres / 1000.0)

    /**
     * Eight compass points, as an index into north, north-east ... north-west, or
     * -1 when the two points are the same (a pin dropped exactly on a tree).
     */
    fun compass(fromLat: Double, fromLng: Double, toLat: Double, toLng: Double): Int {
        val dLat = toLat - fromLat
        val dLng = (toLng - fromLng) * cos((fromLat + toLat) / 2 * Math.PI / 180)
        if (abs(dLat) < 1e-7 && abs(dLng) < 1e-7) return -1
        val deg = (Math.toDegrees(atan2(dLng, dLat)) + 360) % 360
        return ((deg + 22.5) / 45).toInt() % 8
    }

    /** CollectSheet.agePhrase: " old" only after a bare quantity. */
    fun ageNeedsOld(age: String?): Boolean? {
        val a = age?.trim().orEmpty()
        if (a.isEmpty()) return null
        return !(a.lowercase(Locale.ROOT).contains("old") || a.contains(","))
    }

    /** Sightings.placePhrase: "in Nara" within 5 km of one of our trees there, "near Nara" within 30. */
    enum class Near { IN, NEAR }

    fun placeKind(city: String?, km: Double?): Near? {
        if (city.isNullOrEmpty() || km == null) return null
        return when {
            km <= 5 -> Near.IN
            km <= 30 -> Near.NEAR
            else -> null
        }
    }

    /** The nearest of our trees within [withinKm], for naming a tree only you have. */
    fun nearestTree(lat: Double, lng: Double, trees: List<Tree>, withinKm: Double = 30.0): Pair<Tree, Double>? =
        trees.map { it to Geo.km(lat, lng, it.lat, it.lng) }
            .filter { it.second <= withinKm }
            .minByOrNull { it.second }
}
