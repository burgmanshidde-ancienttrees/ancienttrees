package app.ancienttrees.account

import app.ancienttrees.ui.Nav
import app.ancienttrees.ui.Page
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
        // The profile pages live on the tab's own stack (Pages.kt), as Route.settings does.
        val nav = Nav(2)
        val r = ProfileRoutes(listOf("-tab=2", "-settings", "-privacy"), nav)
        assertEquals(listOf<Page>(Page.Settings, Page.Privacy), nav.stack.map { it.page })
        r.back()
        assertEquals(listOf<Page>(Page.Settings), nav.stack.map { it.page })
        assertTrue(r.showing)
        assertTrue(ProfileRoutes(listOf("-profile-edit"), Nav(0)).editProfile)
        assertFalse(ProfileRoutes(emptyList(), Nav(0)).showing)
    }

    @Test fun eachTabKeepsItsOwnHistory() {
        val nav = Nav(1)
        nav.push(Page.TreePage("ath_004"))
        nav.tab = 0
        nav.push(Page.Species("Olive"))
        nav.tab = 1
        assertEquals(Page.TreePage("ath_004"), nav.top)
        nav.clear(0)
        assertEquals(1, nav.stacks[1].size)
        nav.push(Page.Settings, onTab = 2)
        ProfileRoutes(emptyList(), nav).clear()
        assertTrue(nav.stacks[2].isEmpty())
    }

    @Test fun theDemoAccountWearsItsBadgeAndFlag() {
        val p = Profiles(listOf("-ambassador=Paris", "-country=nl", "-public=off"))
        assertEquals("Paris", p.myPlaces.single().placeName)
        assertEquals("NL", p.myCountry)
        assertEquals(false, p.myPublic)
        assertNull(Profiles(emptyList()).myPublic)
    }
}
