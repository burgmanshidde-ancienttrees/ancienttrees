package app.ancienttrees.feed

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class GeoTest {

    @Test fun amsterdamToUtrechtIsAboutThirtyFiveKilometres() {
        val d = Geo.km(52.3731, 4.8922, 52.0907, 5.1214)
        assertTrue("got $d", d in 34.0..36.0)
    }

    @Test fun distancesReadAsTheIphoneAndWebsiteWriteThem() {
        assertEquals("350 m", Geo.short(0.35, miles = false))
        assertEquals("1.2 km", Geo.short(1.234, miles = false))
        assertEquals("528 ft", Geo.short(0.161, miles = true))
        assertEquals("0.6 mi", Geo.short(1.0, miles = true))
    }

    @Test fun milesOnlyWhereTheRoadIsMeasuredInMiles() {
        assertTrue(Geo.milesFor("US"))
        assertTrue(Geo.milesFor("gb"))
        assertFalse(Geo.milesFor("NL"))
        assertFalse(Geo.milesFor(""))
        assertFalse(Geo.milesFor(null))
    }
}
