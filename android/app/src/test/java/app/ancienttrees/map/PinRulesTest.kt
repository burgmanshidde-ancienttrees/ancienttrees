package app.ancienttrees.map

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

class PinRulesTest {

    private val web = File("../../site/src/lib/map.ts").readText()

    private fun webNumber(name: String): Double =
        Regex("""export const $name = ([0-9.]+);""").find(web)!!.groupValues[1].toDouble()

    @Test fun theNumbersAreTheWebsites() {
        assertEquals(webNumber("PIN_DISTANCE"), PinRules.PIN_DISTANCE.toDouble(), 0.0)
        assertEquals(webNumber("FAR_ZOOM"), PinRules.FAR_ZOOM.toDouble(), 0.0)
        assertEquals(webNumber("FAR_PIN_DISTANCE"), PinRules.FAR_PIN_DISTANCE.toDouble(), 0.0)
        assertEquals(webNumber("MINI_RADIUS"), PinRules.MINI_RADIUS.toDouble(), 0.0)
        assertEquals(webNumber("WORLD_MIN_ZOOM"), PinRules.WORLD_MIN_ZOOM, 0.0)
    }

    @Test fun aPhotographBeatsSavesAndSavesBreakTies() {
        assertTrue(PinRules.priority(true, 0) < PinRules.priority(false, 500))
        assertTrue(PinRules.priority(true, 3) < PinRules.priority(true, 1))
    }

    @Test fun thePaddingKeepsTheDistance() {
        assertEquals(1f, PinRules.padding(PinRules.PIN_DISTANCE), 0f)
        assertEquals(26f, PinRules.padding(PinRules.FAR_PIN_DISTANCE), 0f)
    }
}
