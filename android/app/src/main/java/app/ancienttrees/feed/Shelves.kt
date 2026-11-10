// Discover's shelves, worked out once per catalogue and place: a line-by-line
// port of HomeView.buildShelves() in ios Screens/Home.swift, where every rule
// below carries Hidde's ruling and date. Nothing is decided here that the
// iPhone does not decide the same way.

package app.ancienttrees.feed

data class CityCard(val slug: String, val name: String, val country: String, val count: Int)
data class CountryCard(val name: String, val count: Int, val photo: Tree?)
data class SpeciesCard(val name: String, val count: Int, val photo: Tree?)

/** The tile of a record: its label, its tree, and where it opens. */
data class Record(val kind: Kind, val label: String?, val tree: Tree, val collection: String?) {
    enum class Kind { OLDEST, THICKEST, TALLEST }
}

data class ListCard(val collection: TreeCollection, val face: Tree)

/** The season where you stand (Home.swift Shelves.season). */
data class SeasonHero(val word: Season, val hero: Tree, val count: Int, val near: Int)

enum class Season { SPRING, SUMMER, AUTUMN, WINTER }

data class Shelves(
    val season: SeasonHero? = null,
    val best: List<Tree> = emptyList(),
    val cities: List<CityCard> = emptyList(),
    val here: Pair<String, String>? = null,
    val countries: List<CountryCard> = emptyList(),
    val islands: List<CityCard> = emptyList(),
    val species: List<SpeciesCard> = emptyList(),
    val records: List<Record> = emptyList(),
    val lists: List<ListCard> = emptyList(),
    val tail: List<Tree> = emptyList(),
) {
    companion object {
        /** The season's word on your half of the world (Hidde, 2026-10-09). */
        fun seasonWord(month: Int, south: Boolean): Season {
            val m = if (south) (month + 5) % 12 + 1 else month
            return when (m) {
                in 3..5 -> Season.SPRING
                in 6..8 -> Season.SUMMER
                in 9..11 -> Season.AUTUMN
                else -> Season.WINTER
            }
        }

        /** The generated rankings, already The records (Home.swift `generated`). */
        private val GENERATED = setOf(
            "tallest-trees", "thickest-trees", "trees-older-than-400-years",
            "the-oldest-tree-in-every-country-we-map",
        )

        fun build(c: Catalogue, lat: Double, lng: Double, located: Boolean, month: Int): Shelves {
            // THE WEBSITE'S SHELF, in the website's order (feed `favourites`),
            // never every city by count (Hidde, 2026-10-02).
            fun card(slug: String): CityCard? {
                val ts = c.trees(slug)
                val first = ts.firstOrNull() ?: return null
                return CityCard(slug, first.city, first.country, ts.size)
            }
            val favourites = c.favourites.mapNotNull { card(it) }
            val cities = (
                if (favourites.isNotEmpty()) favourites
                else c.byCity.keys.mapNotNull { card(it) }.filter { c.faceOfCity(it.slug) != null }.sortedByDescending { it.count }
                ).toMutableList()

            // Distance once per tree, not once per comparison.
            val ranked = c.trees.map { it to Geo.km(lat, lng, it.lat, it.lng) }.sortedBy { it.second }

            // THE SEASON WHERE YOU ARE (Hidde, 2026-10-10). Without a fix the
            // north is assumed, the half where most of the map is.
            val south = located && lat < 0
            val atBest = ranked.filter { (t, _) -> month in t.bestMonths && (t.lat < 0) == south }
            val bestPhotographed = atBest.filter { it.first.photo != null }.map { it.first }
            // THE PICTURE SHOWS THE SEASON IT NAMES (Hidde, 2026-10-13).
            val hero = bestPhotographed.firstOrNull { t ->
                val m = t.photo?.takenMonth ?: return@firstOrNull false
                m in t.bestMonths
            }
            val season = hero?.let {
                val near = if (located) atBest.count { it.second <= 20 } else 0
                SeasonHero(seasonWord(month, south), it, atBest.size, near)
            }
            val best = bestPhotographed.filter { it.id != hero?.id }.take(6)

            // The city you are standing in, for its open ambassador seat. Only with a real fix.
            var here: Pair<String, String>? = null
            if (located) {
                c.nearest(lat, lng, limit = 1, withinKm = 30.0).firstOrNull()?.first?.let { t ->
                    here = t.citySlug to t.city
                    // THE CITY YOU ARE IN LEADS THE CITIES ROW (Hidde, 2026-10-13),
                    // still only with a photographed face.
                    val own = card(t.citySlug)
                    if (c.faceOfCity(t.citySlug)?.photo != null && own != null) {
                        cities.removeAll { it.slug == own.slug }
                        cities.add(0, own)
                    }
                }
            }

            val countries = c.byCountry.map { (name, ts) -> CountryCard(name, ts.size, c.faceOfCountry(name)) }
                .filter { it.photo?.photo != null }
                .sortedByDescending { it.count }
            val islands = c.islands.mapNotNull { card(it) }.filter { c.faceOfCity(it.slug)?.photo != null }
            // 24, eight to a row across the three rows (Hidde, 2026-10-12).
            val species = c.bySpecies.map { (name, ts) -> SpeciesCard(name, ts.size, c.faceOfSpecies(name)) }
                .filter { it.photo?.photo != null }
                .sortedByDescending { it.count }
                .take(24)

            // THE RECORDS: oldest by the LOW end of the range, the thickest and the tallest.
            val records = ArrayList<Record>()
            c.trees.filter { it.photo != null && (it.ageMin ?: 0) > 0 }.maxByOrNull { it.ageMin ?: 0 }?.let { t ->
                records.add(Record(Record.Kind.OLDEST, t.ageShort, t, null))
            }
            fun first(slug: String): ListCard? {
                val col = c.collections.firstOrNull { it.slug == slug } ?: return null
                val t = c.treesOf(col).firstOrNull { it.photo != null } ?: return null
                return ListCard(col, t)
            }
            first("thickest-trees")?.let { (col, t) ->
                val label = t.girthCm?.let { g ->
                    val m = g / 100.0
                    if (m >= 10) String.format(java.util.Locale.US, "%.0f m", m) else String.format(java.util.Locale.US, "%.1f m", m)
                }
                records.add(Record(Record.Kind.THICKEST, label, t, col.slug))
            }
            first("tallest-trees")?.let { (col, t) -> records.add(Record(Record.Kind.TALLEST, null, t, col.slug)) }

            // LISTS WITH AN OPINION: the hand-made collections, the ones in season first.
            val lists = ArrayList<ListCard>()
            c.collections.withIndex()
                .filter { it.value.slug !in GENERATED }
                .mapNotNull { (i, col) ->
                    val t = col.face?.let { c.tree(it) }?.takeIf { it.photo != null } ?: return@mapNotNull null
                    Triple(i, col, t)
                }
                .sortedWith { a, b ->
                    val ia = month in a.second.months
                    val ib = month in b.second.months
                    if (ia == ib) a.first.compareTo(b.first) else if (ia) -1 else 1
                }
                // One face per photograph: two lists fronted by the same yew read as a mistake.
                .forEach { (_, col, t) ->
                    if (lists.size < 12 && lists.none { it.face.id == t.id }) lists.add(ListCard(col, t))
                }

            // MORE TREES NEAR YOU (Hidde, 2026-10-10): every photographed tree not already on the page.
            val shown = best.map { it.id }.toMutableSet()
            hero?.let { shown.add(it.id) }
            val tail = ranked.map { it.first }.filter { it.photo != null && it.id !in shown }

            return Shelves(season, best, cities, here, countries, islands, species, records, lists, tail)
        }
    }
}
