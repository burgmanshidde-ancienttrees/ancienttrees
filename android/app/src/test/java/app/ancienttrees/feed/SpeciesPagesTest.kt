package app.ancienttrees.feed

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

/** The species page's paragraph and the chooser's "Not on the map yet" read the feed as the iPhone does. */
class SpeciesPagesTest {

    private val species = """
        {"version":"v","species":[],"names":[
          {"c":"Pedunculate Oak","l":"Quercus robur","a":["Zomereik"]},
          {"c":"European Hornbeam","l":"Carpinus betulus","a":["Haagbeuk"],"m":false},
          {"c":"Oak","l":"Quercus","a":["Eik"],"g":true},
          {"c":"Holm Oak","l":"Quercus ilex","m":false}
        ]}
    """.trimIndent()

    private val browse = """
        {"version":"v","collections":[],"cities":[],"countries":[],
         "species":[{"name":"Pedunculate Oak","scientific":"Quercus robur","intro":"What an oak is."}]}
    """.trimIndent()

    private val oak = Tree(
        id = "a", name = "A", species = "Pedunculate Oak (Quercus robur)", age = null, ageShort = null, ageMin = null,
        lat = 52.0, lng = 5.0, city = "Baarn", citySlug = "baarn", country = "Netherlands",
        neighbourhood = "", access = "", paidEntry = false, transport = "", story = "s",
        storyLatin = emptyList(), howToRecognise = "", url = "/baarn/a", precision = Precision.APPROXIMATE,
        photo = null, saves = 0, mini = false, bestMonths = emptyList(),
    )

    private fun catalogue() = Catalogue(
        "v", listOf(oak), emptyList(), emptyList(), FeedParser.browse(browse),
        otherNames = FeedParser.otherNames(species), directory = FeedParser.directory(species),
    )

    @Test fun theSpeciesPageCarriesItsParagraph() {
        assertEquals("What an oak is.", catalogue().intro("Pedunculate Oak"))
    }

    @Test fun aKindWeDoNotMapAnswersByItsOtherName() {
        val hits = catalogue().unmappedSpecies("haag").map { it.first.c }
        assertEquals(listOf("European Hornbeam"), hits)
    }

    @Test fun aGenusLeadsWhenItTiesAndKeepsItsSpForm() {
        val hits = catalogue().unmappedSpecies("quercus")
        assertEquals("Oak", hits.first().first.c)
        assertEquals("Oak (Quercus sp.)", hits.first().first.species)
        assertTrue(hits.none { it.first.c == "Pedunculate Oak" })
    }

    @Test fun oneLetterIsNotASearch() {
        assertTrue(catalogue().unmappedSpecies("q").isEmpty())
    }
}
