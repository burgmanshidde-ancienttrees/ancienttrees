// TREES ON ONE SPOT (CONVENTIONS.md, "Two trees on exactly the same spot"; the
// iPhone's stackSpots, the website's spiderfy). Below STACK_ZOOM the first tree
// on a spot stands for it; from it the spot is one bubble with the count, the only
// bubble on this map, and a tap spreads the trees round the spot.

package app.ancienttrees.map

import app.ancienttrees.feed.Tree
import java.util.Locale
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin

object Stacks {
    const val STACK_ZOOM = 14.0

    /** The key of a spot, to about a metre: what "the same place" means here. */
    fun spotKey(lat: Double, lng: Double): String = String.format(Locale.ROOT, "%.5f,%.5f", lat, lng)

    /** Every spot with its trees, the one that gets the pin first. */
    fun spots(trees: List<Tree>): Map<String, List<Tree>> =
        trees.groupBy { spotKey(it.lat, it.lng) }
            .mapValues { (_, t) -> t.sortedBy { PinRules.priority(it.photo != null, it.saves) } }

    /**
     * Where each of [n] spread trees stands, in points from the spot: two side
     * by side, more on a circle from the top; 36 points out, 44 for three and
     * more (a pin is 38 across).
     */
    fun spreadOffsets(n: Int): List<Pair<Float, Float>> {
        val r = if (n <= 2) 36.0 else 44.0
        return (0 until n).map { k ->
            val a = if (n == 2) PI * k else -PI / 2 + k * 2 * PI / n
            (r * cos(a)).toFloat() to (r * sin(a)).toFloat()
        }
    }
}
