package app.ancienttrees

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class LaunchArgsTest {
    @Test fun theIphonesArgumentsAreRead() {
        val a = LaunchArgs(listOf("-tab=0", "-open=tree:ath_004", "-at=37.97,23.72", "-sheet=full", "-signin"))
        assertEquals(0, a.tab)
        assertEquals("ath_004", a.openTree)
        assertEquals(37.97 to 23.72, a.at)
        assertTrue(a.sheetFull)
        assertTrue(a.signIn)
        assertNull(LaunchArgs(listOf("-open=city:aarhus")).openTree)
    }

    @Test fun aSplitPositionIsPutBackTogether() {
        assertEquals(listOf("-tab=0", "-at=52.3731,4.8922"), LaunchArgs.normalise(listOf("-tab=0", "-at=52.3731", "4.8922")))
        assertEquals(listOf("-at=52.3731,4.8922"), LaunchArgs.normalise(listOf("-at=52.3731\\,4.8922")))
    }

    @Test fun theSheetAndTheSearchAreRead() {
        assertEquals(app.ancienttrees.ui.SheetHeight.HALF, LaunchArgs(listOf("-sheet=half")).sheet)
        assertEquals(app.ancienttrees.ui.SheetHeight.PEEK, LaunchArgs(emptyList()).sheet)
        assertEquals("lis", LaunchArgs(listOf("-search=lis")).search)
        assertEquals("", LaunchArgs(listOf("-search")).search)
        assertNull(LaunchArgs(emptyList()).search)
    }
}
