// The name and face people see, who follows whom, and the early-adopter badge:
// the twin of ios Kit/Profiles.swift and Kit/EarlyAdopter.swift, over the same
// Supabase tables and functions (profiles, follows, ambassadors,
// rpc/follow_counts, rpc/public_profile, rpc/suggested_photographers).
//
// Nothing here is kept on the phone (hard rule 11): every value is read from the
// server and forgotten on sign-out. The launch arguments at the bottom are the
// iPhone's own debug scaffolding (-as=, -country=, -ambassador=, -public=,
// -people-demo), read only from a debuggable build through LaunchArgs.

package app.ancienttrees.account

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder
import java.util.Locale

class Profiles(private val args: List<String> = emptyList()) {
    data class Profile(val userId: String, val displayName: String, val avatarUrl: String?)

    data class Ambassador(val userId: String, val placeSlug: String, val placeName: String, val public: Boolean)

    /** Somebody's profile as anybody may see it: only while its owner made it public. */
    data class PublicProfile(
        val userId: String,
        val displayName: String,
        val avatarUrl: String?,
        val country: String?,
        val createdAt: String?,
        val followers: Int,
        val following: Int,
        val ambassador: List<String>,
        val visited: List<String>,
        val saves: List<String>,
    )

    data class Photographer(val place: String, val userId: String, val displayName: String, val avatarUrl: String?, val trees: Int)

    var me by mutableStateOf<Profile?>(null)
        private set
    var meLoaded by mutableStateOf(false)
        private set
    var followers by mutableStateOf(0)
        private set
    var following by mutableStateOf(0)
        private set
    var myPlaces by mutableStateOf<List<Ambassador>>(emptyList())
        private set
    var myCountry by mutableStateOf<String?>(null)
        private set
    var myFlagHidden by mutableStateOf(false)
        private set
    /** Nil until the server answers, so the Privacy settings row never shows a guess. */
    var myPublic by mutableStateOf<Boolean?>(null)
        private set
    val placesByUser = mutableStateMapOf<String, List<Ambassador>>()

    private fun value(key: String): String? = args.firstOrNull { it.startsWith(key) }?.removePrefix(key)

    init {
        value("-as=")?.takeIf { it.isNotEmpty() }?.let { me = Profile(DEMO_ME, it, null) }
        if (DemoPeople.on(args)) {
            val first = DemoPeople.all.first()
            placesByUser[first.userId] = listOf(Ambassador(first.userId, "amsterdam", "Amsterdam", true))
        }
        value("-ambassador=")?.takeIf { it.isNotEmpty() }?.let {
            myPlaces = listOf(Ambassador(me?.userId ?: DEMO_ME, it.lowercase(), it, false))
        }
        value("-public=")?.let { myPublic = it == "on" }
        value("-country=")?.let { myCountry = it.uppercase() }
        applyDemo()
    }

    /** -followers=N, -following=N, -avatar=: the press screenshots' lived-in profile. */
    private fun applyDemo() {
        val name = value("-as=") ?: return
        value("-followers=")?.toIntOrNull()?.let { followers = it }
        value("-following=")?.toIntOrNull()?.let { following = it }
        if (name.isNotEmpty()) me = Profile(DEMO_ME, name, value("-avatar="))
        value("-country=")?.takeIf { it.isNotEmpty() }?.let { myCountry = it.uppercase() }
    }

    // MARK: your own row

    /** Signed out clears; a token that could not be renewed does not (the reads take the publishable key). */
    suspend fun load(userId: String?, token: String?) {
        if (userId == null) {
            me = null; meLoaded = false; followers = 0; following = 0
            return
        }
        get("profiles?select=user_id,display_name,avatar_url&user_id=eq.$userId", token)?.let { rows ->
            me = rows.firstOrNull()?.let(::profile)
            meLoaded = true
        }
        get("ambassadors?select=user_id,place_slug,place_name,public&user_id=eq.$userId", token)?.let { rows ->
            myPlaces = rows.map(::ambassador)
            placesByUser[userId] = myPlaces
        }
        val flag = get("profiles?select=country,flag_hidden&user_id=eq.$userId", token)
        if (flag != null) {
            val row = flag.firstOrNull()
            myCountry = row?.str("country")
            myFlagHidden = row?.optBoolean("flag_hidden", false) ?: false
            // Unchosen, your flag is the phone's region, written once to a row that exists.
            if (row != null && myCountry == null && !myFlagHidden && token != null) {
                countryGuess()?.let { saveCountry(it, userId, token) }
            }
        } else {
            get("profiles?select=country&user_id=eq.$userId", token)?.let { myCountry = it.firstOrNull()?.str("country") }
        }
        get("profiles?select=public&user_id=eq.$userId", token)?.let {
            myPublic = it.firstOrNull()?.optBoolean("public", false) ?: false
        }
        val counts = Supa.send("/rest/v1/rpc/follow_counts", token = token, body = JSONObject().put("uid", userId).toString())
        if (counts.ok) {
            runCatching { JSONArray(counts.body).getJSONObject(0) }.getOrNull()?.let {
                followers = it.optInt("followers")
                following = it.optInt("following")
            }
        }
        applyDemo()
    }

    /** Who you were, forgotten on this phone at sign-out; the row stays the account's. */
    fun forgetLocally() {
        me = null; meLoaded = false; followers = 0; following = 0
        myPlaces = emptyList(); myCountry = null; myFlagHidden = false; myPublic = null
    }

    suspend fun loadAmbassadors(ids: List<String>, token: String?) {
        val wanted = ids.toSet().filter { it !in placesByUser }
        if (wanted.isEmpty() || token == null) return
        val rows = get("ambassadors?select=user_id,place_slug,place_name,public&user_id=in.(${wanted.joinToString(",")})", token)
        for (id in wanted) placesByUser[id] = emptyList()
        rows?.map(::ambassador)?.groupBy { it.userId }?.forEach { (id, list) -> placesByUser[id] = list }
    }

    suspend fun save(name: String, avatarUrl: String?, userId: String, token: String): Boolean {
        val row = JSONObject().put("user_id", userId).put("display_name", name).put("avatar_url", avatarUrl ?: JSONObject.NULL)
        val ok = Supa.send(
            "/rest/v1/profiles?on_conflict=user_id", token = token,
            body = JSONArray().put(row).toString(), prefer = "resolution=merge-duplicates",
        ).ok
        if (ok) me = Profile(userId, name, avatarUrl)
        return ok
    }

    /** Your country, or null for "Don't show", remembered so the default never returns. */
    suspend fun saveCountry(code: String?, userId: String, token: String): Boolean {
        val c: Any = code ?: JSONObject.NULL
        var ok = Supa.send(
            "/rest/v1/profiles?on_conflict=user_id", token = token,
            body = JSONArray().put(JSONObject().put("user_id", userId).put("country", c).put("flag_hidden", code == null)).toString(),
            prefer = "resolution=merge-duplicates",
        ).ok
        if (!ok) {
            ok = Supa.send(
                "/rest/v1/profiles?on_conflict=user_id", token = token,
                body = JSONArray().put(JSONObject().put("user_id", userId).put("country", c)).toString(),
                prefer = "resolution=merge-duplicates",
            ).ok
        }
        if (ok) { myCountry = code; myFlagHidden = code == null }
        return ok
    }

    /** The Public profile switch. True when the server took it. */
    suspend fun savePublic(on: Boolean, userId: String, token: String): Boolean {
        // An upsert on the own row rather than the iPhone's PATCH: HttpURLConnection
        // has no PATCH, and every account has its row since profile-at-signup.sql.
        val ok = Supa.send(
            "/rest/v1/profiles?on_conflict=user_id", token = token,
            body = JSONArray().put(JSONObject().put("user_id", userId).put("public", on)).toString(),
            prefer = "resolution=merge-duplicates,return=minimal",
        ).ok
        if (ok) myPublic = on
        return ok
    }

    // MARK: following

    suspend fun follow(other: String, me: String, token: String): Boolean {
        val ok = Supa.send(
            "/rest/v1/follows", token = token,
            body = JSONArray().put(JSONObject().put("follower", me).put("followee", other)).toString(),
        ).ok
        load(me, token)
        return ok
    }

    suspend fun unfollow(other: String, me: String, token: String): Boolean {
        val ok = Supa.send("/rest/v1/follows?follower=eq.$me&followee=eq.$other", method = "DELETE", token = token).ok
        load(me, token)
        return ok
    }

    suspend fun followerIds(of: String, token: String?): List<String> =
        get("follows?select=follower&followee=eq.$of&limit=200", token)?.mapNotNull { it.str("follower") }.orEmpty()

    suspend fun followingIds(of: String, token: String?): List<String> =
        get("follows?select=followee&follower=eq.$of&limit=200", token)?.mapNotNull { it.str("followee") }.orEmpty()

    /** By the name they chose, the only way to find somebody. */
    suspend fun search(query: String, token: String?): List<Profile> {
        val q = query.trim()
        if (q.length < 2) return emptyList()
        val e = URLEncoder.encode(q, "UTF-8").replace("+", "%20")
        return get("profiles?select=user_id,display_name,avatar_url&display_name=ilike.*$e*&limit=25", token)?.map(::profile).orEmpty()
    }

    suspend fun byIds(ids: List<String>, token: String?): List<Profile> {
        if (ids.isEmpty()) return emptyList()
        return get("profiles?select=user_id,display_name,avatar_url&user_id=in.(${ids.joinToString(",")})", token)?.map(::profile).orEmpty()
    }

    /** Null when private, unknown, or the server cannot say: all three read the same. */
    suspend fun publicProfile(userId: String, token: String?): PublicProfile? {
        DemoPeople.publicProfile(args, userId)?.let { return it }
        val r = Supa.send("/rest/v1/rpc/public_profile", token = token, body = JSONObject().put("uid", userId).toString())
        if (!r.ok) return null
        return runCatching {
            val j = JSONObject(r.body)
            fun list(k: String) = j.optJSONArray(k)?.let { a -> (0 until a.length()).map { a.getString(it) } }.orEmpty()
            PublicProfile(
                userId = j.getString("user_id"),
                displayName = j.optString("display_name"),
                avatarUrl = j.str("avatar_url"),
                country = j.str("country"),
                createdAt = j.str("created_at"),
                followers = j.optInt("followers"),
                following = j.optInt("following"),
                ambassador = list("ambassador"),
                visited = list("visited"),
                saves = list("saves"),
            )
        }.getOrNull()
    }

    suspend fun photographers(places: Map<String, List<String>>, token: String?): List<Photographer> {
        if (places.isEmpty() || token == null) return emptyList()
        val body = JSONObject().put("places", JSONObject().apply { places.forEach { (k, v) -> put(k, JSONArray(v)) } })
        val r = Supa.send("/rest/v1/rpc/suggested_photographers", token = token, body = body.toString())
        if (!r.ok) return emptyList()
        return runCatching {
            val a = JSONArray(r.body)
            (0 until a.length()).map { a.getJSONObject(it) }.map {
                Photographer(it.getString("place"), it.getString("user_id"), it.optString("display_name"), it.str("avatar_url"), it.optInt("trees"))
            }
        }.getOrDefault(emptyList())
    }

    // MARK: inside

    private suspend fun get(path: String, token: String?): List<JSONObject>? {
        val r = Supa.send("/rest/v1/$path", method = "GET", token = token)
        if (!r.ok) return null
        return runCatching { JSONArray(r.body).let { a -> (0 until a.length()).map { a.getJSONObject(it) } } }.getOrNull()
    }

    companion object {
        const val DEMO_ME = "00000000-0000-0000-0000-0000000000ab"

        private fun JSONObject.str(k: String): String? = if (isNull(k) || !has(k)) null else optString(k).takeIf { it.isNotEmpty() }
        private fun profile(j: JSONObject) = Profile(j.getString("user_id"), j.optString("display_name"), j.str("avatar_url"))
        private fun ambassador(j: JSONObject) =
            Ambassador(j.getString("user_id"), j.optString("place_slug"), j.optString("place_name"), j.optBoolean("public"))

        /** Where the phone says you are, never guessed from a bare language. */
        fun countryGuess(): String? = Locale.getDefault().country.takeIf { it.length == 2 && it in Locale.getISOCountries() }

        /** "Hidde Burgmans" -> "Hidde B.": a first name, no surname published (Profiles.shortName). */
        fun shortName(full: String): String {
            val parts = full.split(" ").filter { it.isNotEmpty() }
            val first = parts.firstOrNull() ?: return ""
            if (parts.size == 1) return first.take(40)
            return "$first ${parts.last().take(1)}.".take(40)
        }

        /** "Mossy Linden 4821", the name the server gives an account it has no name for. */
        fun isGeneratedName(name: String): Boolean = Regex("^[A-Z][a-z]+ [A-Z][a-z]+ [0-9]{4}$").matches(name)
    }
}

/** The avatars bucket: one file per person, at a path only they may write (supabase/profiles.sql). */
object Avatars {
    suspend fun upload(jpeg: ByteArray, userId: String, token: String): String? = withContext(Dispatchers.IO) {
        runCatching {
            val c = URL("${Supa.URL_BASE}/storage/v1/object/avatars/$userId/avatar.jpg").openConnection() as HttpURLConnection
            c.requestMethod = "POST"
            c.connectTimeout = 20_000
            c.readTimeout = 30_000
            c.setRequestProperty("apikey", Supa.KEY)
            c.setRequestProperty("Authorization", "Bearer $token")
            c.setRequestProperty("Content-Type", "image/jpeg")
            c.setRequestProperty("x-upsert", "true")
            c.doOutput = true
            c.outputStream.use { it.write(jpeg) }
            val ok = c.responseCode in 200..299
            c.disconnect()
            if (ok) "${Supa.URL_BASE}/storage/v1/object/public/avatars/$userId/avatar.jpg" else null
        }.getOrNull()
    }
}

/**
 * The early-adopter badge (ios Kit/EarlyAdopter.swift): every account opened
 * before the paid tier goes live. Two facts from the server and none from the
 * phone: the account's created_at and the feed's early_adopter_until. The
 * one-time sheet is remembered on the account (early_adopter_seen), the flag
 * the website writes too.
 */
object EarlyAdopter {
    data class Status(val hasBadge: Boolean, val seenSheet: Boolean)

    private const val VERSION = "https://ancienttrees.app/api/version.json"

    /** Null when the server could not be asked: the badge stays off rather than guessing. */
    suspend fun status(token: String): Status? {
        val u = Supa.send("/auth/v1/user", method = "GET", token = token)
        if (!u.ok) return null
        val j = runCatching { JSONObject(u.body) }.getOrNull() ?: return null
        val created = j.optString("created_at").takeIf { it.isNotEmpty() } ?: return null
        val seen = j.optJSONObject("user_metadata")?.optBoolean("early_adopter_seen", false) ?: false
        val cutoff = feedCutoff() ?: return null
        return Status(rule(created, cutoff.value), seen)
    }

    /** Somebody else's account, from the created_at their public profile carries. */
    suspend fun has(createdAt: String?): Boolean {
        val created = createdAt ?: return false
        val cutoff = feedCutoff() ?: return false
        return rule(created, cutoff.value)
    }

    /** ISO dates compare as strings; no cutoff means the window is open. */
    fun rule(createdAt: String, until: String?): Boolean = until == null || createdAt < until

    suspend fun markSeen(token: String) {
        Supa.send("/auth/v1/user", method = "PUT", token = token,
            body = JSONObject().put("data", JSONObject().put("early_adopter_seen", true)).toString())
    }

    /** A box so "the window is open" (null inside) differs from "could not read" (null box). */
    class Cutoff(val value: String?)

    private suspend fun feedCutoff(): Cutoff? = withContext(Dispatchers.IO) {
        runCatching {
            val c = URL(VERSION).openConnection() as HttpURLConnection
            c.connectTimeout = 20_000
            c.readTimeout = 20_000
            val body = c.inputStream.bufferedReader().use { it.readText() }
            c.disconnect()
            val j = JSONObject(body)
            Cutoff(if (j.isNull("early_adopter_until") || !j.has("early_adopter_until")) null else j.getString("early_adopter_until"))
        }.getOrNull()
    }
}

/** Three made-up people behind -people-demo, so Find people and its report sheet can be looked at (DemoPeople.swift). */
object DemoPeople {
    fun on(args: List<String>) = "-people-demo" in args || "-blocked-demo" in args

    val all = listOf(
        Profiles.Profile("00000000-0000-0000-0000-0000000000a1", "Marieke", null),
        Profiles.Profile("00000000-0000-0000-0000-0000000000a2", "Tom", null),
        Profiles.Profile("00000000-0000-0000-0000-0000000000a3", "Sofia", null),
    )

    data class Suggested(val profile: Profiles.Profile, val place: String, val count: Int?, val ambassador: Boolean)

    /** The design page's four rows: two ambassadors, two people who photographed trees in places you saved. */
    val suggestions = listOf(
        Suggested(Profiles.Profile("00000000-0000-0000-0000-0000000000a4", "Hugo V.", null), "Lisbon", null, true),
        Suggested(Profiles.Profile("00000000-0000-0000-0000-0000000000a5", "Loic S.", null), "Paris", null, true),
        Suggested(all[0], "Utrecht", 4, false),
        Suggested(all[1], "Baarn", 2, false),
    )

    fun publicProfile(args: List<String>, userId: String): Profiles.PublicProfile? {
        if (!on(args) || userId != all[0].userId) return null
        return Profiles.PublicProfile(
            userId, "Marieke", null, "NL", "2026-09-01T10:00:00Z", 12, 4, listOf("Amsterdam"),
            listOf("brn_001", "brn_002", "brn_008", "brn_005"), listOf("brn_003", "brn_007"),
        )
    }
}
