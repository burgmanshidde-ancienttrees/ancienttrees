package app.ancienttrees.feed

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test
import java.io.File

class SnapshotTest {
    @Test fun theWholeCatalogueComesBackTheSame() {
        val f = File("../../ios/AncientTrees/AncientTrees/Data/trees.json")
        if (!f.exists()) return
        val parsed = f.bufferedReader().use { FeedParser.trees(it) }
        val bin = File.createTempFile("trees", ".bin")
        Snapshot.write(bin, "k1", parsed.version, parsed.rows)
        val back = Snapshot.read(bin, "k1")!!
        assertEquals(parsed.version, back.first)
        assertEquals(parsed.rows, back.second)
        // Another source is no snapshot at all.
        assertNull(Snapshot.read(bin, "k2"))
        bin.delete()
    }
}
