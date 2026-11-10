// Reads the feeds off ancienttrees.app. org.json comes with Android, so this
// needs no library, and a field nobody asks for is a field nobody can trip over.
//
// One difference from the iPhone on purpose: Swift gives up on a whole array at
// the first row it cannot read, and here one bad row costs one tree. An app that
// is only caught up once a quarter has to survive a feed it has never seen.

package app.ancienttrees.feed

import org.json.JSONArray
import org.json.JSONObject

object FeedParser {

    /** optString turns a JSON null into the word "null" on Android, so every read goes through here. */
    private fun JSONObject.text(key: String): String? =
        if (isNull(key)) null else (opt(key) as? String)

    private fun JSONObject.need(key: String): String =
        text(key) ?: throw IllegalArgumentException("missing $key")

    private fun JSONObject.number(key: String): Double? =
        if (isNull(key)) null else (opt(key) as? Number)?.toDouble()

    private fun JSONObject.needNumber(key: String): Double =
        number(key) ?: throw IllegalArgumentException("missing $key")

    private fun JSONObject.flag(key: String): Boolean? =
        if (isNull(key)) null else (opt(key) as? Boolean)

    private fun JSONObject.strings(key: String): List<String> {
        val a = optJSONArray(key) ?: return emptyList()
        return (0 until a.length()).mapNotNull { i -> a.opt(i) as? String }
    }

    private fun JSONObject.ints(key: String): List<Int> {
        val a = optJSONArray(key) ?: return emptyList()
        return (0 until a.length()).mapNotNull { i -> (a.opt(i) as? Number)?.toInt() }
    }

    private fun <T> rows(a: JSONArray?, read: (JSONObject) -> T): Pair<List<T>, Int> {
        if (a == null) return emptyList<T>() to 0
        val out = ArrayList<T>(a.length())
        var skipped = 0
        for (i in 0 until a.length()) {
            try {
                out.add(read(a.getJSONObject(i)))
            } catch (_: Exception) {
                skipped++
            }
        }
        return out to skipped
    }

    fun version(json: String): String = JSONObject(json).getString("version")

    fun trees(json: String): Parsed<Tree> = trees(java.io.StringReader(json))

    /** Row by row (RowScanner): the catalogue is read without ever holding it whole. */
    fun trees(reader: java.io.Reader): Parsed<Tree> {
        val scanned = RowScanner.scan(reader, "trees")
        // Rows are independent: read them on every core, each slice in order.
        val rows = scanned.rows
        val cores = Runtime.getRuntime().availableProcessors().coerceIn(1, 8)
        val slice = (rows.size + cores - 1) / cores
        val parts = arrayOfNulls<List<Tree?>>(cores)
        val threads = (0 until cores).map { k ->
            Thread {
                val from = k * slice
                val to = minOf(rows.size, from + slice)
                parts[k] = (from until to).map { i -> runCatching { tree(JSONObject(rows[i])) }.getOrNull() }
            }.also { it.start() }
        }
        threads.forEach { it.join() }
        val all = parts.flatMap { it.orEmpty() }
        val out = all.filterNotNull()
        val skipped = all.size - out.size
        return Parsed(scanned.version ?: throw IllegalArgumentException("missing version"), out, skipped)
    }

    fun walks(json: String): Parsed<Walk> {
        val root = JSONObject(json)
        val (walks, skipped) = rows(root.optJSONArray("walks"), ::walk)
        return Parsed(root.getString("version"), walks, skipped)
    }

    fun species(json: String): Parsed<Species> {
        val root = JSONObject(json)
        val (species, skipped) = rows(root.optJSONArray("species")) { o ->
            Species(
                commonName = o.need("common_name"),
                leaf = o.ints("leaf"),
                flowers = o.ints("flowers"),
                fruit = o.ints("fruit"),
                colour = o.ints("colour"),
                bare = o.ints("bare"),
            )
        }
        return Parsed(root.getString("version"), species, skipped)
    }

    /** Every other name a species we map goes by (species.json `names`, rows c/l/a/m/g): search only. */
    fun otherNames(json: String): Map<String, List<String>> {
        val a = JSONObject(json).optJSONArray("names") ?: return emptyMap()
        val out = HashMap<String, MutableList<String>>()
        for (i in 0 until a.length()) {
            val o = a.optJSONObject(i) ?: continue
            val c = o.text("c") ?: continue
            if (o.flag("m") == false || o.flag("g") == true) continue
            out.getOrPut(c) { ArrayList() }.addAll(o.strings("a"))
        }
        return out
    }

    /** Every row of species.json `names`, for the chooser's "Not on the map yet" (SpeciesSearch.swift). */
    fun directory(json: String): List<SpeciesNameRow> {
        val a = JSONObject(json).optJSONArray("names") ?: return emptyList()
        return (0 until a.length()).mapNotNull { i ->
            val o = a.optJSONObject(i) ?: return@mapNotNull null
            val c = o.text("c") ?: return@mapNotNull null
            SpeciesNameRow(c, o.text("l").orEmpty(), o.strings("a"), o.flag("m"), o.flag("g"))
        }
    }

    fun browse(json: String): Browse {
        val root = JSONObject(json)
        val (collections, a) = rows(root.optJSONArray("collections")) { o ->
            TreeCollection(
                o.need("slug"), o.need("title"), o.text("intro"), o.strings("trees"),
                face = o.text("face"), months = o.ints("months"),
            )
        }
        val (cities, b) = rows(root.optJSONArray("cities")) { o ->
            Facet(
                o.text("slug"), o.need("name"), o.text("face"),
                aka = o.strings("aka"),
                popularity = o.number("popularity")?.toInt() ?: 0,
                ambassadors = o.optJSONArray("ambassadors")?.let { a ->
                    (0 until a.length()).mapNotNull { i ->
                        val p = a.optJSONObject(i) ?: return@mapNotNull null
                        val n = p.text("name") ?: return@mapNotNull null
                        CityAmbassador(n, p.text("affiliation"), p.text("profile"))
                    }
                }.orEmpty(),
                seated = o.flag("seated") ?: false,
            )
        }
        val (countries, c) = rows(root.optJSONArray("countries")) { o ->
            val f = o.optJSONArray("focus")
            val box = if (f != null && f.length() == 2) {
                val sw = f.optJSONArray(0)
                val ne = f.optJSONArray(1)
                if (sw != null && ne != null && sw.length() == 2 && ne.length() == 2) {
                    // [[west, south], [east, north]] on the wire.
                    ViewBox(south = sw.getDouble(1), west = sw.getDouble(0), north = ne.getDouble(1), east = ne.getDouble(0))
                } else {
                    null
                }
            } else {
                null
            }
            Country(o.need("name"), box)
        }
        val countryFaces = HashMap<String, String>()
        root.optJSONArray("countries")?.let { arr ->
            for (i in 0 until arr.length()) {
                val o = arr.optJSONObject(i) ?: continue
                val n = o.text("name") ?: continue
                o.text("face")?.let { countryFaces[n] = it }
            }
        }
        val speciesFaces = HashMap<String, String>()
        val sci = HashMap<String, String>()
        val intros = HashMap<String, String>()
        root.optJSONArray("species")?.let { arr ->
            for (i in 0 until arr.length()) {
                val o = arr.optJSONObject(i) ?: continue
                val n = o.text("name") ?: continue
                o.text("scientific")?.takeIf { it.isNotEmpty() }?.let { sci[n] = it }
                o.text("face")?.let { speciesFaces[n] = it }
                o.text("intro")?.takeIf { it.isNotEmpty() }?.let { intros[n] = it }
            }
        }
        return Browse(
            root.getString("version"), collections, cities, a + b + c, countries, sci,
            countryFaces = countryFaces, speciesFaces = speciesFaces, speciesIntros = intros,
            favourites = root.strings("favourites"), islands = root.strings("islands"),
        )
    }

    private fun photo(o: JSONObject?): Photo? {
        if (o == null) return null
        val url = o.text("url") ?: return null
        return Photo(
            url = url,
            license = o.text("license"),
            attribution = o.text("attribution"),
            attributionShort = o.text("attribution_short"),
            thumb = o.text("thumb"),
            hero = o.text("hero"),
            creditRequired = o.flag("credit_required"),
            creditLine = o.text("credit_line"),
            creditUrl = o.text("credit_url"),
            frame = o.number("frame"),
            season = o.text("season"),
            takenMonth = o.number("taken_month")?.toInt(),
        )
    }

    private fun latinRuns(o: JSONObject): List<IntRange> {
        val a = o.optJSONArray("story_latin") ?: return emptyList()
        return (0 until a.length()).mapNotNull { i ->
            val run = a.optJSONArray(i) ?: return@mapNotNull null
            val start = run.optInt(0, -1)
            val end = run.optInt(1, -1)
            if (run.length() == 2 && start >= 0 && end > start) start until end else null
        }
    }

    private fun tree(o: JSONObject): Tree {
        val lat = o.needNumber("lat")
        val lng = o.needNumber("lng")
        return Tree(
            id = o.need("id"),
            name = o.need("name"),
            species = o.need("species"),
            age = o.text("age"),
            ageShort = o.text("age_short"),
            ageMin = o.number("age_min")?.toInt(),
            ageMax = o.number("age_max")?.toInt(),
            highlight = o.flag("highlight"),
            highlightRank = o.number("highlight_rank")?.toInt(),
            lat = lat,
            lng = lng,
            city = o.need("city"),
            citySlug = o.need("city_slug"),
            country = o.need("country"),
            neighbourhood = o.text("neighbourhood").orEmpty(),
            access = o.text("access").orEmpty(),
            paidEntry = o.flag("paid_entry") ?: false,
            transport = o.text("transport").orEmpty(),
            story = o.need("story"),
            storyLatin = latinRuns(o),
            howToRecognise = o.text("how_to_recognise").orEmpty(),
            url = o.need("url"),
            precision = Precision.from(o.text("precision")),
            photo = photo(o.optJSONObject("photo")),
            saves = o.number("saves")?.toInt() ?: 0,
            mini = o.flag("mini") ?: false,
            photos = o.optJSONArray("photos")?.let { a ->
                (0 until a.length()).mapNotNull { i -> photo(a.optJSONObject(i)) }
            }.orEmpty(),
            seasonal = o.flag("seasonal") ?: false,
            bestMonths = o.optJSONObject("best_time")?.ints("months").orEmpty(),
            seasonKey = o.text("season_key"),
            girthCm = o.number("girth_cm")?.toInt()?.takeIf { it > 0 },
        )
    }

    private fun walk(o: JSONObject): Walk {
        val shape = o.optJSONArray("shape")?.let { a ->
            (0 until a.length()).mapNotNull { i ->
                val p = a.optJSONArray(i) ?: return@mapNotNull null
                if (p.length() == 2) listOf(p.getDouble(0), p.getDouble(1)) else null
            }
        }
        return Walk(
            city = o.need("city"),
            citySlug = o.need("city_slug"),
            name = o.need("name"),
            trees = o.strings("trees"),
            km = o.needNumber("km"),
            minutes = o.needNumber("minutes").toInt(),
            duration = o.need("duration"),
            shape = shape,
        )
    }

    /** All four feeds into one catalogue. Trees and walks must read; species and browse may fail alone. */
    fun catalogue(trees: String, walks: String, species: String?, browse: String?): Catalogue =
        catalogue(java.io.StringReader(trees), walks, species, browse)

    fun catalogue(trees: java.io.Reader, walks: String, species: String?, browse: String?): Catalogue =
        catalogue(trees(trees), walks, species, browse)

    fun catalogue(t: Parsed<Tree>, walks: String, species: String?, browse: String?): Catalogue {
        val w = walks(walks)
        check(t.rows.isNotEmpty()) { "no readable trees" }
        return Catalogue(
            version = t.version,
            trees = t.rows,
            walks = w.rows,
            species = species?.let { runCatching { species(it).rows }.getOrNull() }.orEmpty(),
            browse = browse?.let { runCatching { browse(it) }.getOrNull() },
            otherNames = species?.let { runCatching { otherNames(it) }.getOrNull() }.orEmpty(),
            directory = species?.let { runCatching { directory(it) }.getOrNull() }.orEmpty(),
        )
    }
}
