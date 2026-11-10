package app.ancienttrees.map

import app.ancienttrees.feed.Photo
import app.ancienttrees.feed.Precision
import app.ancienttrees.feed.Tree
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File
import kotlin.math.abs
import kotlin.math.hypot

class StacksAndShapesTest {

    private fun tree(id: String, lat: Double, lng: Double, photo: Boolean = false) = Tree(
        id = id, name = id, species = "Oak (Quercus sp.)", age = null, ageShort = null,
        lat = lat, lng = lng, city = "C", citySlug = "c", country = "N",
        neighbourhood = "", access = "", paidEntry = false, transport = "", story = "s",
        storyLatin = emptyList(), howToRecognise = "", url = "/c/$id", precision = Precision.APPROXIMATE,
        photo = if (photo) Photo("u", null, null, null, null, null, null, null, null, null) else null,
        saves = 0, mini = false,
    )

    @Test fun treesWithinAMetreShareASpotAndThePhotographLeads() {
        val spots = Stacks.spots(listOf(tree("a", 38.7, -9.2), tree("b", 38.700001, -9.2, photo = true), tree("c", 38.8, -9.2)))
        assertEquals(2, spots.size)
        assertEquals(listOf("b", "a"), spots[Stacks.spotKey(38.7, -9.2)]!!.map { it.id })
    }

    @Test fun aSpreadStandsClearOfTheSpot() {
        for (n in 2..6) {
            val offsets = Stacks.spreadOffsets(n)
            assertEquals(n, offsets.size)
            assertTrue(offsets.all { (x, y) -> abs(hypot(x, y) - (if (n <= 2) 36f else 44f)) < 0.01f })
        }
    }

    @Test fun theStackZoomIsTheWebsites() {
        val web = File("../../site/src/lib/map.ts").readText()
        val zoom = Regex("""export const STACK_ZOOM = ([0-9.]+);""").find(web)!!.groupValues[1].toDouble()
        assertEquals(zoom, Stacks.STACK_ZOOM, 0.0)
    }

    @Test fun theShapesAreTheWebsites() {
        val ts = File("../../site/src/lib/species-icons.ts").readText()
        val web = Regex("""\["(\w+)", \[([^\]]*)\]\]""").findAll(ts).map { m ->
            m.groupValues[1] to Regex("\"([^\"]+)\"").findAll(m.groupValues[2]).map { it.groupValues[1] }.toList()
        }.toList()
        assertEquals(web, SpeciesIcons.archetypes)
        assertEquals("oak", SpeciesIcons.archetype("Pedunculate Oak"))
        assertEquals("plane", SpeciesIcons.archetype("London Plane"))
        assertEquals("broadleaf", SpeciesIcons.archetype("Sweet Chestnut"))
        assertTrue(SpeciesIcons.archetypes.all { it.first in SpeciesIcons.icons })
    }
}
