package app.ancienttrees.feed

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test

class WebLinkTest {
    private val look = WebLink.Lookup(
        treeId = { if (it == "/lisbon/ajuda-dragon-tree") "lis_001" else null },
        isCity = { it == "lisbon" },
        countryName = { if (it == "portugal") "Portugal" else null },
        speciesName = { if (it == "dragon-tree") "Dragon Tree" else null },
    )

    private fun p(path: String, q: Map<String, String> = emptyMap(), f: String? = null) = WebLink.parse(path, q, f, look)

    @Test fun theIphonesRoutes() {
        assertEquals(LinkTarget.TreeAt("lis_001"), p("/lisbon/ajuda-dragon-tree"))
        assertEquals(LinkTarget.TreeAt("lis_001"), p("/pt/lisbon/ajuda-dragon-tree"))
        assertEquals(LinkTarget.City("lisbon"), p("/lisbon"))
        assertEquals(LinkTarget.Country("Portugal"), p("/portugal"))
        assertEquals(LinkTarget.SpeciesAt("Dragon Tree"), p("/species/dragon-tree"))
        assertEquals(LinkTarget.Collection("ancient-oaks"), p("/collections/ancient-oaks"))
        assertEquals(LinkTarget.Map, p("/explore"))
        assertEquals(LinkTarget.TreeAt("lis_002"), p("/open", mapOf("tree" to "lis_002")))
        assertEquals(LinkTarget.City("porto"), p("/open", mapOf("city" to "porto")))
        val id = "0F8FAD5B-D9CB-469F-A165-70867728950E"
        assertEquals(LinkTarget.Shared(id.lowercase()), p("/t", mapOf("id" to id)))
        assertEquals(LinkTarget.Person(id.lowercase()), p("/profile", mapOf("u" to id)))
    }

    @Test fun anAppOnlyTreesAddress() {
        assertEquals(LinkTarget.TreeAt("lis_099"), p("/lisbon", f = "tree=lis_099"))
    }

    @Test fun whatTheAppHasNoScreenForStaysOnTheWeb() {
        assertNull(p("/privacy"))
        assertNull(p("/t", mapOf("id" to "nope")))
        assertNull(p("/"))
    }

    @Test fun slugsAreTheWebsites() {
        assertEquals("dragon-tree", WebLink.slugify("Dragon Tree"))
        assertEquals("sao-paulo", WebLink.slugify("São Paulo"))
        assertEquals("hague", WebLink.slugify("The Hague"))
    }
}
