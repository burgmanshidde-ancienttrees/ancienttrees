// The streaming reader against the whole catalogue: the same trees as reading
// it whole, and the awkward text a row may hold.

package app.ancienttrees.feed

import org.junit.Assert.assertEquals
import org.junit.Test
import java.io.File
import java.io.StringReader

class RowScannerTest {
    @Test fun bracesAndQuotesInsideStringsAreText() {
        val json = """{"count":2,"version":"v9","trees":[{"id":"a","story":"a } ] { \" tricky"},{"id":"b","n":{"x":[1,{"y":2}]}}],"after":[{"id":"no"}]}"""
        val r = RowScanner.scan(StringReader(json), "trees")
        assertEquals("v9", r.version)
        assertEquals(2, r.rows.size)
        assertEquals("a", org.json.JSONObject(r.rows[0]).getString("id"))
        assertEquals("a } ] { \" tricky", org.json.JSONObject(r.rows[0]).getString("story"))
        assertEquals(2, org.json.JSONObject(r.rows[1]).getJSONObject("n").getJSONArray("x").getJSONObject(1).getInt("y"))
    }

    @Test fun theBundledCatalogueReadsRowByRowAsItDoesWhole() {
        val f = File("../../ios/AncientTrees/AncientTrees/Data/trees.json")
        if (!f.exists()) return
        val streamed = f.bufferedReader().use { FeedParser.trees(it) }
        val whole = org.json.JSONObject(f.readText())
        assertEquals(whole.getString("version"), streamed.version)
        assertEquals(whole.getJSONArray("trees").length(), streamed.rows.size)
        assertEquals(0, streamed.skipped)
        assertEquals(whole.getJSONArray("trees").getJSONObject(0).getString("id"), streamed.rows[0].id)
    }
}
