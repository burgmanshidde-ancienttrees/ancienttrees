package app.ancienttrees.feed

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test

/** Discover's shelves follow Home.swift buildShelves() rule for rule. */
class ShelvesTest {

    private fun tree(
        id: String, lat: Double, lng: Double, city: String = "Amsterdam", slug: String = "amsterdam",
        photo: Boolean = true, best: List<Int> = emptyList(), taken: Int? = null, ageMin: Int? = null,
    ) = Tree(
        id = id, name = id, species = "Pedunculate Oak (Quercus robur)", age = null, ageShort = ageMin?.let { "$it years" },
        ageMin = ageMin,
        lat = lat, lng = lng, city = city, citySlug = slug, country = "Netherlands",
        neighbourhood = "", access = "", paidEntry = false, transport = "", story = "s",
        storyLatin = emptyList(), howToRecognise = "", url = "/$slug/$id", precision = Precision.APPROXIMATE,
        photo = if (photo) Photo("u", null, null, null, null, null, null, null, null, null, takenMonth = taken) else null,
        saves = 0, mini = false, bestMonths = best,
    )

    private fun catalogue(vararg ts: Tree, browse: Browse? = null) =
        Catalogue("v", ts.toList(), emptyList(), emptyList(), browse)

    @Test fun theSeasonWordFlipsOnTheSouthernHalf() {
        assertEquals(Season.AUTUMN, Shelves.seasonWord(11, south = false))
        assertEquals(Season.SPRING, Shelves.seasonWord(11, south = true))
        assertEquals(Season.WINTER, Shelves.seasonWord(1, south = false))
        assertEquals(Season.SUMMER, Shelves.seasonWord(1, south = true))
    }

    @Test fun theHeroShowsTheSeasonItNames() {
        // The nearer tree's photograph was taken in summer, so it cannot front autumn.
        val near = tree("near", 52.37, 4.89, best = listOf(10, 11), taken = 7)
        val far = tree("far", 51.0, 4.0, best = listOf(10, 11), taken = 11)
        val s = Shelves.build(catalogue(near, far), 52.37, 4.89, located = true, month = 11)
        assertEquals("far", s.season?.hero?.id)
        assertEquals(2, s.season?.count)
        assertEquals(1, s.season?.near)
        assertEquals(listOf("near"), s.best.map { it.id })
    }

    @Test fun noHeroWithoutAPhotographOfItsSeason() {
        val t = tree("t", 52.37, 4.89, best = listOf(11), taken = null)
        assertNull(Shelves.build(catalogue(t), 52.37, 4.89, true, 11).season)
    }

    @Test fun theCityYouAreInLeadsTheCities() {
        val a = tree("a", 41.38, 2.17, city = "Barcelona", slug = "barcelona")
        val b = tree("b", 52.37, 4.89)
        val browse = Browse("v", emptyList(), listOf(Facet("barcelona", "Barcelona", "a"), Facet("amsterdam", "Amsterdam", "b")), 0,
            favourites = listOf("barcelona", "amsterdam"))
        val here = Shelves.build(catalogue(a, b, browse = browse), 52.37, 4.89, located = true, month = 11)
        assertEquals(listOf("amsterdam", "barcelona"), here.cities.map { it.slug })
        assertEquals("amsterdam" to "Amsterdam", here.here)
        // Without a fix nobody is anywhere: the website's order, no seat.
        val nowhere = Shelves.build(catalogue(a, b, browse = browse), 52.37, 4.89, located = false, month = 11)
        assertEquals(listOf("barcelona", "amsterdam"), nowhere.cities.map { it.slug })
        assertNull(nowhere.here)
    }

    @Test fun oldestByTheLowEndOfTheRange() {
        val wide = tree("wide", 52.0, 5.0, ageMin = 200)
        val dated = tree("dated", 52.0, 5.0, ageMin = 900)
        val s = Shelves.build(catalogue(wide, dated), 52.0, 5.0, true, 11)
        assertEquals("dated", s.records.first().tree.id)
    }

    @Test fun inSeasonListsFirstAndOneFacePerPhotograph() {
        val t1 = tree("t1", 52.0, 5.0)
        val t2 = tree("t2", 52.0, 5.0)
        val cols = listOf(
            TreeCollection("kings", "Kings", null, listOf("t1"), face = "t1"),
            TreeCollection("same-face", "Same", null, listOf("t1"), face = "t1"),
            TreeCollection("ginkgo", "Ginkgos", null, listOf("t2"), face = "t2", months = listOf(11)),
            TreeCollection("tallest-trees", "Tallest", null, listOf("t2"), face = "t2"),
        )
        val s = Shelves.build(catalogue(t1, t2, browse = Browse("v", cols, emptyList(), 0)), 52.0, 5.0, true, 11)
        assertEquals(listOf("ginkgo", "kings"), s.lists.map { it.collection.slug })
    }

    @Test fun theTailIsEveryPhotographedTreeNotShownNearestFirst() {
        val near = tree("near", 52.37, 4.89)
        val far = tree("far", 40.0, 4.0)
        val bare = tree("bare", 52.37, 4.89, photo = false)
        val s = Shelves.build(catalogue(far, bare, near), 52.37, 4.89, true, 11)
        assertEquals(listOf("near", "far"), s.tail.map { it.id })
    }
}
