package app.ancienttrees.feed

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/** The iPhone's CollectSheetTests, the same questions asked of the Android port. */
class CollectRulesTest {

    private fun tree(id: String, lat: Double, lng: Double, name: String = id) = Tree(
        id = id, name = name, species = "Oak (Quercus sp.)", age = null, ageShort = null,
        lat = lat, lng = lng, city = "C", citySlug = "c", country = "N",
        neighbourhood = "", access = "", paidEntry = false, transport = "", story = "s",
        storyLatin = emptyList(), howToRecognise = "", url = "/c/$id", precision = Precision.APPROXIMATE,
        photo = null, saves = 0, mini = false,
    )

    // Dam square, and trees at known distances north of it (0.001 deg lat = 111 m).
    private val lat = 52.3731
    private val lng = 4.8922
    private val m100 = tree("m100", lat + 0.0009, lng)
    private val m300 = tree("m300", lat + 0.0027, lng)
    private val km1 = tree("km1", lat + 0.009, lng)
    private val km5 = tree("km5", lat + 0.045, lng)

    @Test fun theCameraIsNeverADeviceFixOnAFallback() {
        assertEquals(CollectRules.Route.Settle(CollectRules.Fix.DEVICE), CollectRules.route(true, true, false))
        assertEquals(CollectRules.Route.AskForThePin, CollectRules.route(true, false, false))
        assertEquals(CollectRules.Route.Settle(CollectRules.Fix.PHOTO), CollectRules.route(false, false, true))
        assertEquals(CollectRules.Route.AskForThePin, CollectRules.route(false, true, false))
    }

    @Test fun nearbyIsFourHundredMetresNearestFirst() {
        assertEquals(listOf("m100", "m300"), CollectRules.nearby(lat, lng, listOf(km1, m300, m100)).map { it.id })
    }

    @Test fun closestIsBeyondNearbyAndWithinThreeKilometres() {
        assertEquals(listOf("km1"), CollectRules.closest(lat, lng, listOf(m100, km1, km5)).map { it.id })
    }

    @Test fun searchIgnoresAccentsAndCase() {
        val ombu = tree("ombu", lat, lng, name = "Ombú of La Cartuja")
        assertEquals(listOf("ombu"), CollectRules.search("OMBU", lat, lng, listOf(ombu, m100)).map { it.id })
        assertTrue(CollectRules.search("o", lat, lng, listOf(ombu)).isEmpty())
    }

    @Test fun distanceTurnsIntoKilometres() {
        assertEquals("40 m", CollectRules.distance(40))
        assertEquals("1.7 km", CollectRules.distance(1672))
    }

    @Test fun compassInEightPoints() {
        assertEquals(0, CollectRules.compass(lat, lng, lat + 0.01, lng))
        assertEquals(2, CollectRules.compass(lat, lng, lat, lng + 0.01))
        assertEquals(1, CollectRules.compass(lat, lng, lat + 0.01, lng + 0.016))
        assertEquals(-1, CollectRules.compass(lat, lng, lat, lng))
    }

    @Test fun oldOnlyAfterABareQuantity() {
        assertEquals(true, CollectRules.ageNeedsOld("roughly 400 years"))
        assertEquals(false, CollectRules.ageNeedsOld("current tree roughly 60 years old, replanted after 1961"))
        assertNull(CollectRules.ageNeedsOld(" "))
    }

    @Test fun placePhraseStopsAtThirtyKilometres() {
        assertEquals(CollectRules.Near.IN, CollectRules.placeKind("Nara", 2.0))
        assertEquals(CollectRules.Near.NEAR, CollectRules.placeKind("Nara", 20.0))
        assertNull(CollectRules.placeKind("Nara", 40.0))
        assertFalse(CollectRules.isFar(lat, lng, m300))
        assertTrue(CollectRules.isFar(lat, lng, km1))
    }
}
