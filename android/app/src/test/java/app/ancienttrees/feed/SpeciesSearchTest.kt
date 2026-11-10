package app.ancienttrees.feed

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class SpeciesSearchTest {
    @Test fun accentsAndCaseFold() {
        assertEquals("liskiava", SpeciesSearch.fold(" Liškiava "))
    }

    @Test fun theKindsOfHitInOrder() {
        assertEquals(SpeciesHit.Name, SpeciesSearch.hit("European White Elm", "Ulmus laevis", emptyList(), "elm"))
        assertEquals(SpeciesHit.Latin, SpeciesSearch.hit("European White Elm", "Ulmus laevis", emptyList(), "ulm"))
        val other = SpeciesSearch.hit("European White Elm", "Ulmus laevis", listOf("Orme lisse"), "lis")
        assertTrue(other is SpeciesHit.Other && other.via == "Orme lisse")
        assertEquals(SpeciesHit.Nearly, SpeciesSearch.hit("Sycamore", null, emptyList(), "sycamre"))
        assertNull(SpeciesSearch.hit("Sycamore", null, emptyList(), "oak"))
    }
}
