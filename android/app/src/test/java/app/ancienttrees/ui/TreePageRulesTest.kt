package app.ancienttrees.ui

import app.ancienttrees.account.MyVotes
import app.ancienttrees.account.TreeNotes
import app.ancienttrees.feed.FeedParser
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

/** The tree page's rules, each the Swift's own (TreeDetail.swift, WorthIt.swift, TreeNotes.swift). */
class TreePageRulesTest {
    @Test fun theDistrictLineDropsSentencesAndTheCityItself() {
        assertEquals("Groenoord", placeDistrict("Groenoord", "Leiden"))
        assertEquals("Belém", placeDistrict("Belém (near the monastery)", "Lisbon"))
        assertNull(placeDistrict("leiden", "Leiden"))
        assertNull(placeDistrict("In the walled garden behind the old botanical institute", "Leiden"))
        assertNull(placeDistrict("  ", "Leiden"))
    }

    @Test fun collectTakesOverWithin200MetresAndLetsGoOnlyPast250() {
        assertFalse(staysNear(false, null))
        assertTrue(staysNear(false, 0.2))
        assertFalse(staysNear(false, 0.22))
        assertTrue(staysNear(true, 0.24))
        assertFalse(staysNear(true, 0.26))
    }

    @Test fun theDistanceInTheButton() {
        assertEquals("350 m", farLabel(0.34))
        assertEquals("2.4 km", farLabel(2.43))
        assertEquals("17 km", farLabel(16.6))
    }

    @Test fun girthInMetresWithoutTrailingZeros() {
        assertEquals("6", metres(600))
        assertEquals("2.4", metres(240))
        assertEquals("3.15", metres(315))
    }

    @Test fun aVoteRowNamesItsTreeFirst() {
        assertEquals("ath_004", MyVotes.treeId("ath_004 (The Plane of Hippocrates)"))
    }

    @Test fun notesReadNullNamesAsAVisitor() {
        val rows = TreeNotes.parse(
            """[{"tree_id":"a","body":"Full gold.","created_at":"2026-11-01T10:00:00.123+00:00","author_name":null,"author_avatar":null},
               {"tree_id":"a","body":"Sundays.","created_at":"2026-11-02T10:00:00+00:00","author_name":"Rita M.","author_avatar":null}]""",
        )
        assertEquals(2, rows.size)
        assertNull(rows[0].authorName)
        assertEquals("Rita M.", rows[1].authorName)
        assertTrue(rows[1].date.isAfter(rows[0].date))
    }

    @Test fun girthComesFromTheFeed() {
        val f = File("../../ios/AncientTrees/AncientTrees/Data/trees.json")
        if (!f.exists()) return
        val trees = f.bufferedReader().use { FeedParser.trees(it) }.rows
        // Not every feed carries a girth yet; where one does, it is a positive number.
        trees.mapNotNull { it.girthCm }.forEach { assertTrue(it > 0) }
    }
}
