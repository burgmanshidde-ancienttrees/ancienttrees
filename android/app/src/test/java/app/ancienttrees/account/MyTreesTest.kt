package app.ancienttrees.account

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Test

/** The rules My trees reads its lists by (Sightings.swift, SightingSync.swift). */
class MyTreesTest {
    @Test
    fun stampReadsEveryShapeTheDatabaseSends() {
        // Postgres's own microseconds, our own string without a fraction, and a bare day.
        assertEquals(1762776000000L, MyTrees.stamp("2025-11-10T12:00:00.123456+00:00"))
        assertEquals(1762776000000L, MyTrees.stamp("2025-11-10T12:00:00Z"))
        assertNotNull(MyTrees.stamp("2025-11-10"))
        assertNull(MyTrees.stamp(""))
        assertNull(MyTrees.stamp(null))
    }

    @Test
    fun aNameOnTwoLinesReadsAsOne() {
        assertEquals("The oak on my street", OwnSighting.oneLine("The oak\non my street "))
    }

    @Test
    fun yourTreeIsConfirmedAndFreeAndKeepsItsFields() {
        val t = OwnSighting(id = "A1", treeId = null, name = "Oak", species = "Pedunculate Oak (Quercus robur)",
            girthCm = 420, lat = 52.0, lng = 4.0, date = 0L).asTree()
        assertEquals("Pedunculate Oak", t.commonName)
        assertEquals(420, t.girthCm)
        assertEquals(false, t.paidEntry)
        assertEquals(app.ancienttrees.feed.Precision.CONFIRMED, t.precision)
    }

    @Test
    fun theShareLinkIsTheUnlistedPageInLowerCase() {
        assertEquals("https://ancienttrees.app/t?id=00000000-0000-0000-0000-0000000000a1", MyTrees.shareUrl(MyTrees.DEMO_IDS[0]))
    }
}
