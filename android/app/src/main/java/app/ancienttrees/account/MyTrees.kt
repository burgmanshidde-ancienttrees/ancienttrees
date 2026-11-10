// My trees' server half: your own finds (the `sightings` table and the private
// `sightings` bucket), the trees you sent through the website (`submissions`),
// and your own profile row for the header. Ported from ios Kit/Sightings.swift
// (yoursOnly, newestShotByTree, asTree), Kit/SightingSync.swift (merge, remove,
// publish), Kit/Submissions.swift (Submission.mine) and Kit/Profiles.swift (load).
//
// THE ONE DIFFERENCE FROM THE iPHONE, and it is hard rule 11 rather than taste:
// the iPhone keeps your photographs in a file store and syncs it; Android keeps
// nothing a person did on the device (data/cross-device.json), so every list here
// is read from the account when My trees opens and held in memory only. A
// photograph is fetched with your token when a tile draws it and kept in a
// memory cache that dies with the app.

package app.ancienttrees.account

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import app.ancienttrees.feed.Precision
import app.ancienttrees.feed.Tree
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder
import java.text.SimpleDateFormat
import java.util.Locale
import java.util.TimeZone

/** Sightings.Sighting: a photograph you took, of one of ours or of a tree only you have. */
data class OwnSighting(
    val id: String,
    /** Our tree, when it is one of ours; null when only you have it. */
    val treeId: String?,
    val name: String,
    val note: String = "",
    val species: String? = null,
    val age: String? = null,
    val girthCm: Int? = null,
    val lat: Double,
    val lng: Double,
    /** taken_at, in milliseconds. */
    val date: Long,
    /** The path in the private bucket, or null with no photograph. */
    val photo: String? = null,
    /** mine, sent, checking, published, declined. */
    val status: String = "mine",
    val extras: List<String> = emptyList(),
    val sign: String? = null,
    /** "It is one of these": belongs to no tree yet, so not one of your own finds. */
    val unsure: Boolean = false,
    /** -mine-demo only: which drawn stand-in to show instead of a download. */
    val demo: Int? = null,
) {
    val published: Boolean get() = status == "published"

    /** Sightings.asTree: the same page as ours with your fields in it. */
    fun asTree(): Tree = Tree(
        id = "mine-$id",
        name = oneLine(name),
        species = species.orEmpty(),
        age = age,
        ageShort = null,
        lat = lat,
        lng = lng,
        city = "",
        citySlug = "",
        country = "",
        neighbourhood = "",
        access = "",
        // Your own tree never stands behind a ticket: you were there.
        paidEntry = false,
        transport = "",
        story = note,
        storyLatin = emptyList(),
        howToRecognise = "",
        url = "",
        // You photographed it where you stood.
        precision = Precision.CONFIRMED,
        photo = null,
        saves = 0,
        mini = false,
        girthCm = girthCm,
    )

    companion object {
        /** Sightings.oneLine: a name that arrived on two lines reads as one. */
        fun oneLine(raw: String): String =
            raw.split('\n', '\r', '\t').map { it.trim() }.filter { it.isNotEmpty() }.joinToString(" ")
    }
}

/** Submission.Sent: a tree you sent through the website's form, one per tree. */
data class SentTip(
    val id: Int,
    val tree: String,
    val city: String,
    val outcome: String?,
    val sentAt: Long?,
    val times: Int = 1,
) {
    val title: String get() = tree.ifEmpty { city }
}

/** Your own profile row and the counts beside it (Profiles.load, for "me" only). */
data class MyProfile(
    val displayName: String?,
    val avatarUrl: String?,
    val country: String?,
    val followers: Int,
    val following: Int,
    /** The places you are an ambassador of: (slug, name). */
    val places: List<Pair<String, String>>,
)

class MyTrees(private val account: Account) {
    /** Every sighting the account holds, newest first. */
    var all by mutableStateOf<List<OwnSighting>>(emptyList())
        private set
    var sent by mutableStateOf<List<SentTip>>(emptyList())
        private set
    var profile by mutableStateOf<MyProfile?>(null)
        private set
    /** Bumped on every change, so a page holding a copy reads the new one. */
    var version by mutableIntStateOf(0)
        private set

    /** Sightings.yoursOnly: only the ones nobody else has, newest first. */
    val yoursOnly: List<OwnSighting> get() = all.filter { it.treeId == null && !it.unsure }

    /** Sightings.newestShotByTree: your newest photograph of each of our trees. */
    val newestShotByTree: Map<String, OwnSighting>
        get() {
            val out = LinkedHashMap<String, OwnSighting>()
            for (s in all) {
                val id = s.treeId ?: continue
                if ((s.photo != null || s.demo != null) && id !in out) out[id] = s
            }
            return out
        }

    fun byId(id: String): OwnSighting? = all.firstOrNull { it.id.equals(id, ignoreCase = true) }

    private var loadedFor: String? = null
    private var loadedAt = 0L

    /**
     * What the account holds, read again for another account, after ten minutes,
     * or when asked to (Collect.swift's once-per-account load, 2026-11-04).
     */
    suspend fun load(force: Boolean = false) {
        if (demoSeeded) return
        val s = account.fresh() ?: run { forget(); return }
        if (!force && loadedFor == s.userId && System.currentTimeMillis() - loadedAt < 600_000) return
        val rows = Supa.rows("/rest/v1/sightings?select=*", s.accessToken)
        all = rows.mapNotNull(::parse).sortedByDescending { it.date }
        sent = mine(s.accessToken)
        profile = loadProfile(s.userId, s.accessToken)
        loadedFor = s.userId
        loadedAt = System.currentTimeMillis()
        version++
    }

    /** Signed out: what this phone showed goes with the account. */
    fun forget() {
        if (demoSeeded) return
        all = emptyList()
        sent = emptyList()
        profile = null
        loadedFor = null
        version++
    }

    // MARK: - changing your own tree (TreeDetail's editor and menu)

    /** One field of your tree, changed here at once and on the server; back if it says no. */
    suspend fun update(
        id: String,
        name: String? = null,
        species: String? = null,
        age: String? = null,
        girthCm: Int? = null,
        note: String? = null,
    ): Boolean {
        val was = byId(id) ?: return false
        val now = was.copy(
            name = name ?: was.name,
            species = species ?: was.species,
            age = age ?: was.age,
            // 0 clears it, as Sightings.update(girthCm: 0) does.
            girthCm = if (girthCm == null) was.girthCm else girthCm.takeIf { it > 0 },
            note = note ?: was.note,
        )
        replace(now)
        if (demoSeeded) return true
        val s = account.fresh() ?: run { replace(was); return false }
        val body = JSONObject().put("updated_at", Collector.iso())
        if (name != null) body.put("name", name)
        if (species != null) body.put("species", species)
        if (age != null) body.put("age", age)
        if (girthCm != null) body.put("girth_cm", if (girthCm > 0) girthCm else JSONObject.NULL)
        if (note != null) body.put("note", note)
        val ok = Supa.send(
            "/rest/v1/sightings?user_id=eq.${s.userId}&id=eq.${enc(was.id)}",
            method = "PATCH",
            token = s.accessToken,
            body = body.toString(),
            prefer = "return=minimal",
        ).ok
        if (!ok) replace(was)
        return ok
    }

    /** SightingSync.remove: the files first, then the row. */
    suspend fun remove(id: String): Boolean {
        val was = byId(id) ?: return false
        all = all.filterNot { it.id == was.id }
        version++
        if (demoSeeded) return true
        val s = account.fresh() ?: run { all = (all + was).sortedByDescending { it.date }; return false }
        val files = listOfNotNull(was.photo, was.sign) + was.extras
        for (f in files) deleteObject("sightings", f, s.accessToken)
        deleteObject("shared-sightings", "${s.userId}/${was.id}.jpg", s.accessToken)
        val ok = Supa.delete("/rest/v1/sightings?id=eq.${enc(was.id)}", s.accessToken)
        if (!ok) {
            all = (all + was).sortedByDescending { it.date }
            version++
        }
        return ok
    }

    /**
     * SightingSync.publish: the unlisted page anybody with the link can open, made
     * only when Share is tapped. The photograph is already in the shared bucket
     * (Collector.send puts it there), so this flips the row and returns the link.
     */
    suspend fun publish(id: String): String? {
        val was = byId(id) ?: return null
        if (!demoSeeded) {
            val s = account.fresh() ?: return null
            val ok = Supa.send(
                "/rest/v1/sightings?user_id=eq.${s.userId}&id=eq.${enc(was.id)}",
                method = "PATCH",
                token = s.accessToken,
                body = JSONObject().put("shared", true).toString(),
                prefer = "return=minimal",
            ).ok
            if (!ok) return null
        }
        return shareUrl(was.id)
    }

    /**
     * A further photograph on your own tree (morePhotosRow): to the private bucket
     * beside the first, then the row's extra_photos, as SightingSync.push sends it.
     */
    suspend fun addExtra(id: String, jpeg: ByteArray): Boolean {
        val was = byId(id) ?: return false
        if (was.extras.size >= MAX_EXTRAS || demoSeeded) return false
        val s = account.fresh() ?: return false
        val path = Collector.extraPath(s.userId, was.id, was.extras.size + 1)
        val up = upload(path, jpeg, s.accessToken)
        if (!up) return false
        val extras = was.extras + path
        val ok = Supa.send(
            "/rest/v1/sightings?user_id=eq.${s.userId}&id=eq.${enc(was.id)}",
            method = "PATCH",
            token = s.accessToken,
            body = JSONObject().put("extra_photos", JSONArray(extras)).put("updated_at", Collector.iso()).toString(),
            prefer = "return=minimal",
        ).ok
        if (ok) replace(was.copy(extras = extras))
        return ok
    }

    private fun replace(s: OwnSighting) {
        all = all.map { if (it.id == s.id) s else it }
        version++
    }

    // MARK: - -mine-demo

    private var demoSeeded = false

    /**
     * Sightings.seedDemo: two of your own trees with a drawn photograph each,
     * behind -mine-demo, at the fixed ids -open=mine: addresses. Debug builds
     * only (LaunchArgs reads nothing from a release build); nothing is sent.
     */
    fun seedDemo(lat: Double, lng: Double, name: String? = "test") {
        if (demoSeeded) return
        demoSeeded = true
        val now = System.currentTimeMillis()
        all = DEMO_IDS.mapIndexed { i, id ->
            OwnSighting(
                id = id,
                treeId = null,
                name = listOf("The oak on my street", "The lime by the water")[i],
                lat = lat + 0.004 * (i + 1),
                lng = lng + 0.006 * (i + 1),
                date = now + i,
                demo = i,
            )
        }
        profile = MyProfile(name, null, null, 0, 0, emptyList())
        version++
    }

    // MARK: - reading

    private fun parse(o: JSONObject): OwnSighting? {
        val id = o.optString("id").ifEmpty { return null }
        if (!o.has("lat") || !o.has("lng") || o.isNull("lat") || o.isNull("lng")) return null
        val unsure = o.optJSONArray("unsure_of")?.length()?.let { it > 0 } ?: false
        return OwnSighting(
            id = id,
            treeId = o.str("tree_id"),
            name = o.str("name") ?: "A tree you photographed",
            note = o.str("note").orEmpty(),
            species = o.str("species"),
            age = o.str("age"),
            girthCm = if (o.isNull("girth_cm")) null else o.optInt("girth_cm", 0).takeIf { it > 0 },
            lat = o.optDouble("lat"),
            lng = o.optDouble("lng"),
            date = stamp(o.str("taken_at")) ?: 0L,
            photo = o.str("photo"),
            status = o.str("status") ?: "mine",
            extras = o.optJSONArray("extra_photos")?.let { a -> (0 until a.length()).mapNotNull { a.optString(it).ifEmpty { null } } }.orEmpty(),
            sign = o.str("sign_photo"),
            unsure = unsure,
        )
    }

    /**
     * Submission.mine: yours, newest first, one per tree. Not the rows this app
     * writes beside a sighting of its own (page "app..."): the sighting is that tree.
     */
    private suspend fun mine(token: String): List<SentTip> {
        val rows = Supa.rows(
            "/rest/v1/submissions?select=id,kind,city,tree,outcome,created_at,page&kind=in.(tree,city)&order=created_at.desc",
            token,
        )
        val order = ArrayList<String>()
        val byKey = HashMap<String, SentTip>()
        for (r in rows) {
            if (r.str("page").orEmpty().startsWith("app")) continue
            val tree = r.str("tree").orEmpty()
            val city = r.str("city").orEmpty()
            val key = (tree + "|" + city).lowercase().filter { it.isLetterOrDigit() || it == '|' }
            val outcome = r.str("outcome")
            val have = byKey[key]
            if (have != null) {
                byKey[key] = have.copy(times = have.times + 1, outcome = have.outcome ?: outcome)
                continue
            }
            order.add(key)
            byKey[key] = SentTip(r.optInt("id", 0), tree, city, outcome, stamp(r.str("created_at")))
        }
        return order.mapNotNull { byKey[it] }
    }

    private suspend fun loadProfile(userId: String, token: String): MyProfile {
        val me = Supa.rows("/rest/v1/profiles?select=display_name,avatar_url,country&user_id=eq.$userId", token).firstOrNull()
        val places = Supa.rows("/rest/v1/ambassadors?select=place_slug,place_name&user_id=eq.$userId", token)
            .mapNotNull { r -> r.str("place_slug")?.let { it to (r.str("place_name") ?: it) } }
        val counts = Supa.send("/rest/v1/rpc/follow_counts", token = token, body = JSONObject().put("uid", userId).toString())
        var followers = 0
        var following = 0
        if (counts.ok) {
            runCatching {
                val first = JSONArray(counts.body).getJSONObject(0)
                followers = first.optInt("followers", 0)
                following = first.optInt("following", 0)
            }
        }
        return MyProfile(me?.str("display_name"), me?.str("avatar_url"), me?.str("country"), followers, following, places)
    }

    private suspend fun deleteObject(bucket: String, path: String, token: String) {
        Supa.send("/storage/v1/object/$bucket/$path", method = "DELETE", token = token)
    }

    private suspend fun upload(path: String, jpeg: ByteArray, token: String): Boolean = withContext(Dispatchers.IO) {
        runCatching {
            val c = URL("${Supa.URL_BASE}/storage/v1/object/sightings/$path").openConnection() as HttpURLConnection
            c.requestMethod = "POST"
            c.connectTimeout = 20_000
            c.readTimeout = 60_000
            c.doOutput = true
            c.setRequestProperty("apikey", Supa.KEY)
            c.setRequestProperty("Authorization", "Bearer $token")
            c.setRequestProperty("Content-Type", "image/jpeg")
            c.setRequestProperty("x-upsert", "true")
            try {
                c.outputStream.use { it.write(jpeg) }
                c.responseCode in 200..299
            } finally {
                c.disconnect()
            }
        }.getOrDefault(false)
    }

    /** The photograph's bytes, from the private bucket with your token. */
    suspend fun photoBytes(path: String): ByteArray? {
        val s = account.fresh() ?: return null
        return withContext(Dispatchers.IO) {
            runCatching {
                val c = URL("${Supa.URL_BASE}/storage/v1/object/sightings/$path").openConnection() as HttpURLConnection
                c.connectTimeout = 20_000
                c.readTimeout = 30_000
                c.setRequestProperty("apikey", Supa.KEY)
                c.setRequestProperty("Authorization", "Bearer ${s.accessToken}")
                try {
                    if (c.responseCode !in 200..299) null else c.inputStream.use { it.readBytes() }
                } finally {
                    c.disconnect()
                }
            }.getOrNull()
        }
    }

    companion object {
        val MAX_EXTRAS: Int get() = Collector.MAX_EXTRAS
        val DEMO_IDS = listOf("00000000-0000-0000-0000-0000000000A1", "00000000-0000-0000-0000-0000000000A2")

        /** SightingSync.url: /t and not /t/, the id in lower case. */
        fun shareUrl(id: String) = "https://ancienttrees.app/t?id=" + id.lowercase()

        private fun enc(s: String) = URLEncoder.encode(s, "UTF-8")

        private fun JSONObject.str(key: String): String? =
            if (!has(key) || isNull(key)) null else optString(key).ifEmpty { null }

        /** SightingSync.stamp: a timestamp in either shape Postgres sends, or a bare day. */
        fun stamp(raw: String?): Long? {
            val s = raw?.trim().orEmpty()
            if (s.isEmpty()) return null
            val utc = TimeZone.getTimeZone("UTC")
            val cut = s.replace(Regex("\\.\\d+"), "").replace("+00:00", "Z")
            for (f in listOf("yyyy-MM-dd'T'HH:mm:ssX", "yyyy-MM-dd'T'HH:mm:ss'Z'", "yyyy-MM-dd")) {
                val parsed = runCatching {
                    SimpleDateFormat(f, Locale.ROOT).apply { timeZone = utc }.parse(if (f == "yyyy-MM-dd") cut.take(10) else cut)
                }.getOrNull()
                if (parsed != null) return parsed.time
            }
            return null
        }
    }
}
