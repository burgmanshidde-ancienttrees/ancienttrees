package app.ancienttrees.feed

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class NearbyTest {

    private fun tree(id: String, lat: Double, lng: Double, photo: Boolean = false, saves: Int = 0) = Tree(
        id = id, name = id, species = "Oak (Quercus sp.)", age = null, ageShort = null,
        lat = lat, lng = lng, city = "C", citySlug = "c", country = "N",
        neighbourhood = "", access = "", paidEntry = false, transport = "", story = "s",
        storyLatin = emptyList(), howToRecognise = "", url = "/c/$id", precision = Precision.APPROXIMATE,
        photo = if (photo) Photo("u", null, null, null, null, null, null, null, null, null) else null,
        saves = saves, mini = false,
    )

    private val baarn = tree("baarn", 52.21, 5.29)
    private val utrecht = tree("utrecht", 52.09, 5.12, photo = true)
    private val lisbon = tree("lisbon", 38.72, -9.14, saves = 9)

    @Test fun onlyTheTreesTheMapShows() {
        val nl = ViewBox(50.7, 3.3, 53.6, 7.3)
        val r = Nearby.inView(listOf(baarn, utrecht, lisbon), nl, null)
        assertEquals(2, r.total)
        assertEquals(listOf("utrecht", "baarn"), r.trees.map { it.id })
    }

    @Test fun nearestFirstWhenWeKnowWhereYouAre() {
        val r = Nearby.inView(listOf(utrecht, lisbon, baarn), null, Here(52.22, 5.3))
        assertEquals(listOf("baarn", "utrecht", "lisbon"), r.trees.map { it.id })
    }

    @Test fun theCountIsEveryTreeInViewEvenPastTheList() {
        val many = (1..80).map { tree("t$it", 52.0, 5.0) }
        val r = Nearby.inView(many, null, null, limit = 50)
        assertEquals(50, r.trees.size)
        assertEquals(80, r.total)
    }

    @Test fun aBoxAcrossTheDateLine() {
        val pacific = ViewBox(-30.0, 170.0, 30.0, -170.0)
        assertTrue(pacific.contains(0.0, 179.0))
        assertTrue(pacific.contains(0.0, -175.0))
        assertFalse(pacific.contains(0.0, 0.0))
    }
}
