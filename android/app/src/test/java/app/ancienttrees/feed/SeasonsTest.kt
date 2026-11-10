package app.ancienttrees.feed

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class SeasonsTest {

    private fun photo(season: String?) = Photo("u$season", null, null, null, null, null, null, null, null, null, season)

    private fun tree(seasonal: Boolean, vararg photos: Photo) = Tree(
        id = "t", name = "t", species = "Oak (Quercus robur)", age = null, ageShort = null,
        lat = 52.0, lng = 5.0, city = "C", citySlug = "c", country = "N",
        neighbourhood = "", access = "", paidEntry = false, transport = "", story = "s",
        storyLatin = emptyList(), howToRecognise = "", url = "/c/t", precision = Precision.CONFIRMED,
        photo = photos.firstOrNull(), saves = 0, mini = false, photos = photos.toList(), seasonal = seasonal,
        bestMonths = listOf(10, 11), seasonKey = "autumn",
    )

    @Test fun theSeasonFlipsSouthOfTheEquator() {
        assertEquals("autumn", Seasons.now(11, 52.0))
        assertEquals("spring", Seasons.now(11, -33.9))
        assertEquals("winter", Seasons.now(1, 40.0))
    }

    @Test fun eachTileIsTheFirstPhotographOfItsSeason() {
        val t = tree(true, photo("autumn"), photo("spring"), photo("autumn"))
        val tiles = Seasons.tiles(t)
        assertEquals(listOf("spring", "summer", "autumn", "winter"), tiles.map { it.key })
        assertEquals(listOf(1, null, 0, null), tiles.map { it.first })
        assertEquals(2, tiles[2].count)
        assertTrue(tiles[2].lead)
    }

    @Test fun noRowWithoutSeasonsOrPhotographs() {
        assertTrue(Seasons.tiles(tree(false, photo("autumn"))).isEmpty())
        assertTrue(Seasons.tiles(tree(true)).isEmpty())
    }

    @Test fun bestTimeIsReadFromTheFeed() {
        val row = """{"id":"a","name":"A","species":"Oak (Quercus sp.)","lat":1,"lng":2,"city":"C","city_slug":"c",
            "country":"N","story":"s","url":"/c/a","seasonal":true,"season_key":"autumn",
            "best_time":{"months":[10,11],"label":"Autumn colour","kind":"colour"},
            "photos":[{"url":"x","season":"autumn"},{"url":"y","season":"winter"}]}"""
        val t = FeedParser.trees("""{"version":"v","trees":[$row]}""").rows.single()
        assertTrue(t.atBest(10))
        assertEquals("autumn", t.seasonKey)
        assertEquals(listOf("autumn", "winter"), t.shots.map { it.season })
    }
}
