// THE TREE IN ALL FOUR SEASONS (CONVENTIONS.md, "A tree's photographs by season,
// and the empty season as an ask"; the iPhone's seasonsRow, the website's same
// row). Each season's tile is the first photograph the feed filed under it.

package app.ancienttrees.feed

object Seasons {
    val KEYS = listOf("spring", "summer", "autumn", "winter")

    data class Tile(val key: String, val first: Int?, val count: Int, val lead: Boolean)

    /** The season now where the tree stands: meteorological, flipped south of the equator. */
    fun now(month: Int, lat: Double): String {
        var k = when (month) {
            in 3..5 -> 0
            in 6..8 -> 1
            in 9..11 -> 2
            else -> 3
        }
        if (lat < 0) k = (k + 2) % 4
        return KEYS[k]
    }

    /** The row, or empty where the tree has no seasons or no photograph. */
    fun tiles(tree: Tree): List<Tile> {
        val shots = tree.shots
        if (!tree.seasonal || shots.isEmpty()) return emptyList()
        return KEYS.map { k ->
            val first = shots.indexOfFirst { it.season == k }.takeIf { it >= 0 }
            Tile(k, first, shots.count { it.season == k }, shots.first().season == k)
        }
    }
}
