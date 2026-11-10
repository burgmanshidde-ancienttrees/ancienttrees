package app.ancienttrees.ui

import app.ancienttrees.account.OwnSighting
import org.junit.Assert.assertEquals
import org.junit.Test

/** CollectSheet.yoursNear: your own trees within 30 m, nearest first, at most two. */
class YoursNearTest {
    private fun own(id: String, metresNorth: Double) =
        OwnSighting(id = id, treeId = null, name = id, lat = 52.0 + metresNorth / 111_320.0, lng = 5.0, date = 0L)

    @Test
    fun offersOnlyTreesWithinThirtyMetresNearestFirst() {
        val got = yoursNear(52.0, 5.0, listOf(own("far", 45.0), own("b", 20.0), own("a", 5.0)))
        assertEquals(listOf("a", "b"), got.map { it.id })
    }

    @Test
    fun offersAtMostTwo() {
        val got = yoursNear(52.0, 5.0, listOf(own("a", 1.0), own("b", 2.0), own("c", 3.0)))
        assertEquals(listOf("a", "b"), got.map { it.id })
    }

    @Test
    fun nothingNearIsEmpty() {
        assertEquals(emptyList<OwnSighting>(), yoursNear(52.0, 5.0, listOf(own("far", 31.0))))
    }
}
