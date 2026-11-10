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

    fun trees(json: String): Parsed<Tree> {
        val root = JSONObject(json)
        val (trees, skipped) = rows(root.optJSONArray("trees"), ::tree)
        return Parsed(root.getString("version"), trees, skipped)
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

    fun browse(json: String): Browse {
        val root = JSONObject(json)
        val (collections, a) = rows(root.optJSONArray("collections")) { o ->
            TreeCollection(o.need("slug"), o.need("title"), o.text("intro"), o.strings("trees"))
        }
        val (cities, b) = rows(root.optJSONArray("cities")) { o ->
            Facet(o.text("slug"), o.need("name"), o.text("face"))
        }
        return Browse(root.getString("version"), collections, cities, a + b)
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
    fun catalogue(trees: String, walks: String, species: String?, browse: String?): Catalogue {
        val t = trees(trees)
        val w = walks(walks)
        check(t.rows.isNotEmpty()) { "no readable trees" }
        return Catalogue(
            version = t.version,
            trees = t.rows,
            walks = w.rows,
            species = species?.let { runCatching { species(it).rows }.getOrNull() }.orEmpty(),
            browse = browse?.let { runCatching { browse(it) }.getOrNull() },
        )
    }
}
