package app.ancienttrees.ui

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/** The review ask's timing (ReviewPrompt.swift and its ReviewPromptTests) and the directions links (Directions.swift). */
class SheetsRulesTest {
    private class Mem : ReviewPrompt.Store {
        val sets = HashMap<String, Set<String>>()
        val longs = HashMap<String, Long>()
        val strs = HashMap<String, String>()
        override fun strings(key: String) = sets[key].orEmpty()
        override fun putStrings(key: String, value: Set<String>) { sets[key] = value }
        override fun long(key: String) = longs[key]
        override fun putLong(key: String, value: Long?) { if (value == null) longs.remove(key) else longs[key] = value }
        override fun string(key: String) = strs[key]
        override fun putString(key: String, value: String?) { if (value == null) strs.remove(key) else strs[key] = value }
    }

    private val day = 86_400_000L

    @Test fun threeDifferentTreesLookedAtIsTheFirstMilestone() {
        val p = ReviewPrompt(Mem(), "1.0")
        p.saw("a"); p.saw("a"); p.saw("b")
        assertFalse(p.consider(0))
        p.saw("c")
        assertTrue(p.consider(0))
        assertTrue(p.pending)
    }

    @Test fun aWeekApartAndThreeInALifetime() {
        assertNull(ReviewPrompt.milestone(10, setOf("first"), last = 0, now = 6 * day))
        assertEquals("second", ReviewPrompt.milestone(10, setOf("first"), last = 0, now = 7 * day))
        assertNull(ReviewPrompt.milestone(99, setOf("first", "second", "third"), last = null, now = 0))
        assertEquals("first", ReviewPrompt.milestone(3, emptySet(), last = null, now = 0))
        assertNull(ReviewPrompt.milestone(2, emptySet(), last = null, now = 0))
    }

    @Test fun aYesWaitsForANewerVersionAndFourMonths() {
        val m = Mem()
        val p = ReviewPrompt(m, "1.0")
        listOf("a", "b", "c").forEach(p::saw)
        p.answeredYes(0)
        assertFalse(p.consider(200 * day))
        val newer = ReviewPrompt(m, "1.1")
        assertFalse(newer.consider(119 * day))
        assertTrue(newer.consider(120 * day))
        // Every milestone counts as fired after the yes.
        assertEquals(3, m.strings(ReviewPrompt.FIRED).size)
    }

    @Test fun silencedForTheSweep() {
        val p = ReviewPrompt(Mem(), "1.0", suppressed = true)
        listOf("a", "b", "c").forEach(p::saw)
        assertFalse(p.consider(0))
    }

    @Test fun seenStopsGrowingAtTheLastMilestone() {
        val p = ReviewPrompt(Mem(), "1.0")
        (1..40).forEach { p.saw("t$it") }
        assertEquals(25, p.seenCount)
    }

    @Test fun directionsLinks() {
        assertEquals("https://www.google.com/maps/dir/?api=1&destination=52.1,4.2&travelmode=walking", Directions.googleUrl(52.1, 4.2))
        assertEquals("geo:52.1,4.2?q=52.1,4.2", Directions.geoUri(52.1, 4.2, null))
        assertEquals(Directions.MapsApp.GOOGLE, Directions.MapsApp.from("google"))
        assertNull(Directions.MapsApp.from("apple"))
    }
}
