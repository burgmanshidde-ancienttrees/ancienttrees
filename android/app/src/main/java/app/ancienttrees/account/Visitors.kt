// NEW FROM VISITORS and the ambassador ask: the server calls Discover makes,
// the Android twin of ios Kit/NewFromVisitors.swift and the ambassador half of
// Kit/Submissions.swift. Nothing is kept on the device: the rows are read each
// time Discover opens, and whether you asked is read from your account.

package app.ancienttrees.account

import org.json.JSONArray
import org.json.JSONObject
import java.net.URLEncoder

object NewFromVisitors {
    /** One photograph a visitor sent that went live; the name and avatar only from a public profile. */
    data class Row(
        val sightingId: String,
        val treeId: String,
        val publishedAt: String,
        val authorName: String?,
        val authorAvatar: String?,
        /** Only to a signed-in caller (supabase/new-from-visitors.sql). */
        val authorId: String?,
    )

    /** The row shows from this many tiles, so it never stands half empty. */
    const val MINIMUM = 4

    private fun JSONObject.text(k: String): String? = if (isNull(k)) null else (opt(k) as? String)

    fun parse(body: String): List<Row> = runCatching {
        val a = JSONArray(body)
        val rows = (0 until a.length()).mapNotNull { i ->
            val o = a.optJSONObject(i) ?: return@mapNotNull null
            Row(
                sightingId = o.text("sighting_id") ?: return@mapNotNull null,
                treeId = o.text("tree_id") ?: return@mapNotNull null,
                publishedAt = o.text("published_at").orEmpty(),
                authorName = o.text("author_name"),
                authorAvatar = o.text("author_avatar"),
                authorId = o.text("author_id"),
            )
        }
        // One tile per tree, its newest photograph.
        val seen = HashSet<String>()
        rows.filter { seen.add(it.treeId) }
    }.getOrDefault(emptyList())

    suspend fun load(token: String?): List<Row> {
        val r = Supa.send("/rest/v1/rpc/new_from_visitors", token = token, body = JSONObject().put("n", 12).toString())
        return if (r.ok) parse(r.body) else emptyList()
    }
}

object AmbassadorAsk {
    private const val PATH = "/rest/v1/submissions"

    suspend fun request(city: String, token: String): Boolean {
        val body = JSONObject()
            .put("kind", "ambassador")
            .put("city", city)
            .put("tree", "")
            .put("why", "ambassador request")
            .put("page", "app")
        return Supa.send(PATH, token = token, body = body.toString(), prefer = "return=minimal").ok
    }

    /** Whether this account already asked for this city, read from the account, never remembered here. */
    suspend fun asked(city: String, token: String?): Boolean {
        if (token == null) return false
        val q = URLEncoder.encode(city, "UTF-8").replace("+", "%20")
        return Supa.rows("$PATH?select=id&kind=eq.ambassador&city=eq.$q&limit=1", token).isNotEmpty()
    }
}
