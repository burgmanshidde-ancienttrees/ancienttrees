// The shapes the app reads, the Android twin of ios Kit/Models.swift. Fields the
// app does not use yet are simply not read, so a feed that grows breaks nothing.

package app.ancienttrees.feed

enum class Precision {
    CONFIRMED, APPROXIMATE;

    companion object {
        /** Unknown or missing is approximate, never confirmed: a wrong pin is the one error a reader cannot forgive. */
        fun from(raw: String?): Precision = if (raw == "confirmed") CONFIRMED else APPROXIMATE
    }
}

data class Photo(
    val url: String,
    val license: String?,
    val attribution: String?,
    val attributionShort: String?,
    val thumb: String?,
    val hero: String?,
    val creditRequired: Boolean?,
    val creditLine: String?,
    val creditUrl: String?,
    val frame: Double?,
    /** "spring", "summer", "autumn" or "winter" where the tree stands, decided on the server. */
    val season: String? = null,
    /** The month the photograph was taken (1 to 12), where the file said (feed taken_month). */
    val takenMonth: Int? = null,
) {
    val card: String get() = thumb ?: url
    val full: String get() = hero ?: url

    /** The credit to print, or null when the licence asks for none. The server decides (credit_required). */
    val credit: String?
        get() {
            // No answer from the feed: print the credit, which is never wrong.
            if (creditRequired == false) return null
            if (!creditLine.isNullOrEmpty()) return creditLine
            return listOfNotNull(attributionShort ?: attribution, license)
                .joinToString(" · ")
                .ifEmpty { null }
        }
}

data class Tree(
    val id: String,
    val name: String,
    val species: String,
    val age: String?,
    val ageShort: String?,
    val ageMin: Int? = null,
    val ageMax: Int? = null,
    /** On the place's Highlights shelf, decided on the website (lib/highlights.ts). */
    val highlight: Boolean? = null,
    /** Its place on that shelf, 0 first. */
    val highlightRank: Int? = null,
    val lat: Double,
    val lng: Double,
    val city: String,
    val citySlug: String,
    val country: String,
    val neighbourhood: String,
    val access: String,
    val paidEntry: Boolean,
    val transport: String,
    val story: String,
    /** The scientific names as [start, end) UTF-16 offsets, decided by the website. */
    val storyLatin: List<IntRange>,
    val howToRecognise: String,
    val url: String,
    val precision: Precision,
    val photo: Photo?,
    val saves: Int,
    val mini: Boolean,
    /** Every photograph, lead first; the feed sends it only when there is more than one. */
    val photos: List<Photo> = emptyList(),
    /** The tree goes through the seasons, so its page shows the Seasons row. */
    val seasonal: Boolean = false,
    /** The months of its one real peak (best_time), and which chip it wears then. */
    val bestMonths: List<Int> = emptyList(),
    val seasonKey: String? = null,
    /** Round the trunk at chest height, from a register or a plaque (girth_cm). */
    val girthCm: Int? = null,
) {
    /** What to show: the set when the feed sent one, otherwise the lead alone. */
    val shots: List<Photo> get() = photos.ifEmpty { listOfNotNull(photo) }

    /** At its best in this month (1 to 12). */
    fun atBest(month: Int): Boolean = month in bestMonths

    val commonName: String get() = species.substringBefore("(").trim()

    /** An older feed without the field: a tree with a photograph is a highlight (Models.swift isHighlight). */
    val isHighlight: Boolean get() = highlight ?: (photo != null)

    /** The short age a card can carry, or null: a number, never a sentence (TreeRow.swift cardAge). */
    val cardAge: String?
        get() {
            val s = ageShort?.trim()
            if (!s.isNullOrEmpty() && s.any { it.isDigit() }) return s
            val lo = ageMin ?: return null
            if (lo <= 0) return null
            val hi = ageMax
            return if (hi != null && hi > lo) "$lo-$hi years" else "$lo years"
        }

    /** Only when there is something to meet: the same test as the website's and the iPhone's. */
    val showsAccess: Boolean
        get() {
            val a = access.trim()
            if (a.isEmpty()) return false
            return paidEntry || !accessPlainFree(a)
        }

    companion object {
        private val STARTS_FREE = Regex("^free\\b", RegexOption.IGNORE_CASE)
        private val SOMETHING_TO_MEET = Regex(
            "\\d|gate|book|reception|ticket|closed|fenc|private|view|hour|open(ing)? (from|at)|" +
                "permission|ask|entrance|locked|behind|except|but|however|not ",
            RegexOption.IGNORE_CASE,
        )

        fun accessPlainFree(a: String): Boolean =
            STARTS_FREE.containsMatchIn(a) && !SOMETHING_TO_MEET.containsMatchIn(a)
    }
}

data class Walk(
    val city: String,
    val citySlug: String,
    val name: String,
    val trees: List<String>,
    val km: Double,
    val minutes: Int,
    val duration: String,
    /** GeoJSON order, [lng, lat]. Null where no routed line is cached. */
    val shape: List<List<Double>>?,
)

data class Species(
    val commonName: String,
    val leaf: List<Int>,
    val flowers: List<Int>,
    val fruit: List<Int>,
    val colour: List<Int>,
    val bare: List<Int>,
)

data class TreeCollection(
    val slug: String,
    val title: String,
    val intro: String?,
    val trees: List<String>,
    /** The tree whose photograph fronts this list, decided on the website (browse.json face). */
    val face: String? = null,
    /** The months the list is in season (lib/favourites.ts COLLECTION_MONTHS). */
    val months: List<Int> = emptyList(),
)

/** One person named on a city page (Models.swift CityAmbassador). */
data class CityAmbassador(val name: String, val affiliation: String?, val profile: String?)

data class Facet(
    val slug: String?,
    val name: String,
    val face: String?,
    val aka: List<String> = emptyList(),
    val popularity: Int = 0,
    /** Cities only: the people named as its ambassadors, and whether an unnamed one holds the seat. */
    val ambassadors: List<CityAmbassador> = emptyList(),
    val seated: Boolean = false,
)

/** A country, and the mainland box its map opens on when its trees would frame an ocean. */
data class Country(val name: String, val focus: ViewBox?)

/**
 * One feed as read. [skipped] counts rows that could not be read: the app drops
 * only those rows and keeps the rest, while the contract test insists on zero.
 */
data class Parsed<T>(val version: String, val rows: List<T>, val skipped: Int)

data class Browse(
    val version: String,
    val collections: List<TreeCollection>,
    val cities: List<Facet>,
    val skipped: Int,
    val countries: List<Country> = emptyList(),
    /** The website's scientific name per species page (browse.json species). */
    val scientific: Map<String, String> = emptyMap(),
    /** Faces per country and per species (browse.json countries / species `face`). */
    val countryFaces: Map<String, String> = emptyMap(),
    val speciesFaces: Map<String, String> = emptyMap(),
    /** What each species is, the website's Contract F paragraph (browse.json species `intro`; Species.swift). */
    val speciesIntros: Map<String, String> = emptyMap(),
    /** Discover's favourite cities and tree islands, in the website's order (lib/favourites.ts). */
    val favourites: List<String> = emptyList(),
    val islands: List<String> = emptyList(),
)

data class Catalogue(
    val version: String,
    val trees: List<Tree>,
    val walks: List<Walk>,
    val species: List<Species>,
    val browse: Browse?,
    val otherNames: Map<String, List<String>> = emptyMap(),
    /** species.json `names`: every row, mapped or not (Kit/SpeciesSearch.swift speciesDirectory). */
    val directory: List<SpeciesNameRow> = emptyList(),
) {
    // The iPhone's indexes (Kit/Catalogue.swift), built once per catalogue.
    val byId: Map<String, Tree> by lazy { trees.associateBy { it.id } }
    val byCity: Map<String, List<Tree>> by lazy { trees.groupBy { it.citySlug } }
    val byCountry: Map<String, List<Tree>> by lazy { trees.groupBy { it.country } }
    val bySpecies: Map<String, List<Tree>> by lazy { trees.groupBy { it.commonName } }
    /** Common names in alphabetical order, as Catalogue.swift sorts them. */
    val speciesNames: List<String> by lazy { bySpecies.keys.filter { it.isNotEmpty() }.sorted() }
    private val cityFacets: Map<String, Facet> by lazy {
        browse?.cities.orEmpty().filter { it.slug != null }.associateBy { it.slug!! }
    }
    private val countryFacets: Map<String, Country> by lazy { browse?.countries.orEmpty().associateBy { it.name } }
    /** The species page's own name first, else the first tree's (Catalogue.swift scientificByCommon). */
    private val scientific: Map<String, String> by lazy {
        bySpecies.mapNotNull { (common, ts) ->
            if (common.isEmpty()) return@mapNotNull null
            val s = browse?.scientific?.get(common) ?: ts.firstNotNullOfOrNull { t ->
                val open = t.species.indexOf('(')
                val close = if (open >= 0) t.species.indexOf(')', open) else -1
                if (open >= 0 && close > open) t.species.substring(open + 1, close).trim().ifEmpty { null } else null
            }
            s?.let { common to it }
        }.toMap()
    }

    fun tree(id: String): Tree? = byId[id]
    fun trees(inCity: String): List<Tree> = byCity[inCity].orEmpty()
    fun treesInCountry(name: String): List<Tree> = byCountry[name].orEmpty()
    fun treesOfSpecies(common: String): List<Tree> = bySpecies[common].orEmpty()
    fun aka(city: String): List<String> = cityFacets[city]?.aka.orEmpty()
    fun popularity(city: String): Int = cityFacets[city]?.popularity ?: 0
    fun focus(country: String): ViewBox? = countryFacets[country]?.focus
    fun scientificName(common: String): String? = scientific[common]
    /** The species page's paragraph (Catalogue.intro(species:)). */
    fun intro(species: String): String? = browse?.speciesIntros?.get(species)

    val collections: List<TreeCollection> get() = browse?.collections.orEmpty()
    val favourites: List<String> get() = browse?.favourites.orEmpty()
    val islands: List<String> get() = browse?.islands.orEmpty()
    fun ambassadors(city: String): List<CityAmbassador> = cityFacets[city]?.ambassadors.orEmpty()
    fun seated(city: String): Boolean = cityFacets[city]?.seated ?: false
    fun treesOf(c: TreeCollection): List<Tree> = c.trees.mapNotNull { byId[it] }

    // CARD FACES (Catalogue.swift): the website's choice, travelling as a tree
    // id; an older snapshot without one falls back to the first photographed tree.
    fun faceOfCity(slug: String): Tree? =
        cityFacets[slug]?.face?.let { byId[it] } ?: firstPhotographed(trees(slug))
    fun faceOfCountry(name: String): Tree? =
        browse?.countryFaces?.get(name)?.let { byId[it] } ?: firstPhotographed(treesInCountry(name))
    fun faceOfSpecies(common: String): Tree? =
        browse?.speciesFaces?.get(common)?.let { byId[it] } ?: firstPhotographed(treesOfSpecies(common))
    private fun firstPhotographed(set: List<Tree>): Tree? = set.firstOrNull { it.photo != null }

    /** The nearest trees within [withinKm], nearest first (Catalogue.swift nearest). */
    fun nearest(lat: Double, lng: Double, limit: Int, withinKm: Double): List<Pair<Tree, Double>> =
        trees.map { it to Geo.km(lat, lng, it.lat, it.lng) }.filter { it.second <= withinKm }
            .sortedBy { it.second }.take(limit)
}

/** One row of species.json `names` (Kit/SpeciesSearch.swift SpeciesNameRow). */
data class SpeciesNameRow(
    /** Our common name, the one every screen prints (hard rule 9). */
    val c: String,
    /** The Latin. */
    val l: String,
    val a: List<String> = emptyList(),
    /** false: a species met in a lead that we do not map yet. */
    val m: Boolean? = null,
    /** true: a genus, offered as "Oak (Quercus sp.)". */
    val g: Boolean? = null,
) {
    val isMapped: Boolean get() = m != false && g != true
    val isGenus: Boolean get() = g == true
    /** What a reader's tree is called when they pick this row, so it groups with the trees that carry it. */
    val species: String get() = if (isGenus) "$c ($l sp.)" else "$c ($l)"
}
