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
}
