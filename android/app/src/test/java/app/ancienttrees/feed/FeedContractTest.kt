// The app's own parser against a feed, as ios LiveFeedContract.swift does: the
// bundled copy, the live website, and the awkward rows a feed may hold.

package app.ancienttrees.feed

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File
import java.net.HttpURLConnection
import java.net.URL

class FeedContractTest {

    private val minimal = """
        {"id":"a1","name":"The Oak","species":"Pedunculate Oak (Quercus robur)","lat":52.1,"lng":5.2,
         "city":"Baarn","city_slug":"baarn","country":"Netherlands","story":"Old.","url":"/baarn/oak"}
    """

    private fun feed(vararg rows: String) = """{"version":"v1","count":${rows.size},"trees":[${rows.joinToString(",")}]}"""

    @Test fun aFieldNobodyKnowsChangesNothing() {
        val row = minimal.trim().dropLast(1) + ""","brand_new":{"deep":[1,2]},"another":null}"""
        val parsed = FeedParser.trees(feed(row))
        assertEquals(0, parsed.skipped)
        assertEquals("a1", parsed.rows.single().id)
    }

    @Test fun nullStringsAreEmptyNeverTheWordNull() {
        val row = minimal.trim().dropLast(1) + ""","neighbourhood":null,"transport":null,"access":null}"""
        val t = FeedParser.trees(feed(row)).rows.single()
        assertEquals("", t.neighbourhood)
        assertEquals("", t.transport)
        assertEquals("", t.access)
    }

    @Test fun anUnknownPrecisionIsApproximate() {
        val confirmed = minimal.trim().dropLast(1) + ""","precision":"confirmed"}"""
        val odd = minimal.trim().dropLast(1) + ""","precision":"pretty sure"}"""
        val rows = FeedParser.trees(feed(confirmed, odd, minimal)).rows
        assertEquals(listOf(Precision.CONFIRMED, Precision.APPROXIMATE, Precision.APPROXIMATE), rows.map { it.precision })
    }

    @Test fun oneBadRowCostsOneTree() {
        val parsed = FeedParser.trees(feed(minimal, """{"id":"broken"}"""))
        assertEquals(1, parsed.rows.size)
        assertEquals(1, parsed.skipped)
    }

    @Test fun theCreditFollowsTheServer() {
        fun photo(required: Boolean?, line: String?) =
            Photo("u", "CC BY 2.0", "Serge Melki, via Commons", "Serge Melki", null, null, required, line, null, null)
        assertNull(photo(false, "Serge Melki (CC BY 2.0)").credit)
        assertEquals("Serge Melki (CC BY 2.0)", photo(true, "Serge Melki (CC BY 2.0)").credit)
        assertEquals("Serge Melki · CC BY 2.0", photo(null, null).credit)
    }

    @Test fun plainFreeAccessIsLeftOut() {
        assertTrue(Tree.accessPlainFree("Free, public park"))
        assertFalse(Tree.accessPlainFree("Free, but the gate closes at dusk"))
        assertFalse(Tree.accessPlainFree("Ticket required"))
    }

    // The copy that ships in the app has to read completely.
    private val data = File("../../ios/AncientTrees/AncientTrees/Data")

    @Test fun theBundledCatalogueReadsEveryRow() {
        val trees = FeedParser.trees(File(data, "trees.json").readText())
        assertEquals(0, trees.skipped)
        assertTrue(trees.rows.size > 500)
        assertEquals(0, FeedParser.walks(File(data, "walks.json").readText()).skipped)
        assertEquals(0, FeedParser.species(File(data, "species.json").readText()).skipped)
        assertEquals(0, FeedParser.browse(File(data, "browse.json").readText()).skipped)
    }

    private fun live(path: String): String {
        val c = URL("https://ancienttrees.app$path").openConnection() as HttpURLConnection
        c.connectTimeout = 30_000
        c.readTimeout = 60_000
        val code = c.responseCode
        check(code in 200..299) { "COULD NOT REACH $path (HTTP $code): the site or the runner, not the shape" }
        return c.inputStream.bufferedReader().use { it.readText() }
    }

    @Test fun theLiveFeedsStillFit() {
        val trees = FeedParser.trees(live("/api/trees.json"))
        assertEquals("live trees the app cannot read", 0, trees.skipped)
        assertTrue(trees.rows.size > 500)
        assertTrue("a tree without a position", trees.rows.none { it.lat == 0.0 && it.lng == 0.0 })

        val walks = FeedParser.walks(live("/api/walks.json"))
        assertEquals(0, walks.skipped)
        assertTrue(walks.rows.isNotEmpty())

        val species = FeedParser.species(live("/api/species.json"))
        assertEquals(0, species.skipped)
        assertTrue(species.rows.isNotEmpty())

        val browse = FeedParser.browse(live("/api/browse.json"))
        assertEquals(0, browse.skipped)
        assertTrue(browse.collections.size >= 5)

        assertNotNull(FeedParser.version(live("/api/version.json")))
    }
}
