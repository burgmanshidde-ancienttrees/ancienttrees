// The list under the map: the trees the map shows, Airbnb's count ("22 trees",
// the website's treesInView). Nearest first when we know where the person is;
// otherwise the order the pins are given, photographs and readers' saves first.

package app.ancienttrees.feed

import app.ancienttrees.map.PinRules

data class ViewBox(val south: Double, val west: Double, val north: Double, val east: Double) {
    fun contains(lat: Double, lng: Double): Boolean {
        if (lat < south || lat > north) return false
        // A box across the date line has its west edge east of its east edge.
        return if (west <= east) lng in west..east else lng >= west || lng <= east
    }
}

data class Here(val lat: Double, val lng: Double)

data class InView(val trees: List<Tree>, val total: Int)

object Nearby {
    const val LIST_LIMIT = 50

    fun inView(trees: List<Tree>, box: ViewBox?, here: Here?, limit: Int = LIST_LIMIT): InView {
        val seen = if (box == null) trees else trees.filter { box.contains(it.lat, it.lng) }
        val ordered = if (here != null) {
            seen.sortedBy { Geo.km(here.lat, here.lng, it.lat, it.lng) }
        } else {
            seen.sortedWith(compareBy<Tree>({ PinRules.priority(it.photo != null, it.saves) }, { it.name }))
        }
        return InView(ordered.take(limit), seen.size)
    }
}
