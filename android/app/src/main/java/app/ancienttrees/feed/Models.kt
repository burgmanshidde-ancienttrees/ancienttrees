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
) {
    /** What to show: the set when the feed sent one, otherwise the lead alone. */
    val shots: List<Photo> get() = photos.ifEmpty { listOfNotNull(photo) }

    /** At its best in this month (1 to 12). */
    fun atBest(month: Int): Boolean = month in bestMonths

    val commonName: String get() = species.substringBefore("(").trim()

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

data class TreeCollection(val slug: String, val title: String, val intro: String?, val trees: List<String>)

data class Facet(val slug: String?, val name: String, val face: String?)

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
)

data class Catalogue(
    val version: String,
    val trees: List<Tree>,
    val walks: List<Walk>,
    val species: List<Species>,
    val browse: Browse?,
)
