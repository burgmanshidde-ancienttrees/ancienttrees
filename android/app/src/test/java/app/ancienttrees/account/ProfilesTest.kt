package app.ancienttrees.account

import app.ancienttrees.ui.ProfilePage
import app.ancienttrees.ui.ProfileRoutes
import app.ancienttrees.ui.flagEmoji
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class ProfilesTest {
    @Test fun shortNameKeepsAFirstNameAndAnInitial() {
        assertEquals("Hidde B.", Profiles.shortName("Hidde Burgmans"))
        assertEquals("Hidde", Profiles.shortName("Hidde"))
        assertEquals("Ana S.", Profiles.shortName("Ana Maria  Silva"))
        assertEquals("", Profiles.shortName("  "))
    }

    @Test fun aGeneratedNameIsRecognised() {
        assertTrue(Profiles.isGeneratedName("Mossy Linden 4821"))
        assertFalse(Profiles.isGeneratedName("Hidde B."))
    }

    @Test fun earlyAdopterIsEveryAccountBeforeTheCutoff() {
        assertTrue(EarlyAdopter.rule("2026-08-14T10:02:11Z", null))
        assertTrue(EarlyAdopter.rule("2026-08-14T10:02:11Z", "2027-03-01"))
        assertFalse(EarlyAdopter.rule("2027-03-02T09:00:00Z", "2027-03-01"))
    }

    @Test fun theFlagIsTwoRegionalLetters() {
        assertEquals("🇳🇱", flagEmoji("nl"))
        assertNull(flagEmoji("NLD"))
        assertNull(flagEmoji(null))
    }

    @Test fun theSweepsLaunchArgumentsOpenTheSameScreens() {
        val r = ProfileRoutes(listOf("-tab=2", "-settings", "-privacy"))
        assertEquals(listOf(ProfilePage.Settings, ProfilePage.Privacy), r.stack.toList())
        r.back()
        assertEquals(listOf(ProfilePage.Settings), r.stack.toList())
        assertTrue(ProfileRoutes(listOf("-profile-edit")).editProfile)
        assertFalse(ProfileRoutes(emptyList()).showing)
    }

    @Test fun theDemoAccountWearsItsBadgeAndFlag() {
        val p = Profiles(listOf("-ambassador=Paris", "-country=nl", "-public=off"))
        assertEquals("Paris", p.myPlaces.single().placeName)
        assertEquals("NL", p.myCountry)
        assertEquals(false, p.myPublic)
        assertNull(Profiles(emptyList()).myPublic)
    }
}
