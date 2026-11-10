// What a reader tells us about a tree, ported from ios Kit/WorthIt.swift,
// Kit/VoteCounts.swift, Kit/Submissions.swift and Kit/TreeNotes.swift: the
// "worth the visit" thumb, the report chips, the report form and the notes from
// people who stood there. The server holds all of it; this phone holds it in
// memory for the session only (hard rule 11, data/cross-device.json).

package app.ancienttrees.account

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import org.json.JSONArray
import org.json.JSONObject
import java.time.Instant
import java.time.OffsetDateTime

/** Submission.swift: one row in `submissions`, accepted on the publishable key. */
object Submission {
    private const val PATH = "/rest/v1/submissions"

    suspend fun feedback(city: String, tree: String, why: String, token: String?): Boolean =
        post(JSONObject().put("kind", "feedback").put("city", city).put("tree", tree).put("why", why).put("page", "app"), token)

    /** The report form (Contribute.swift, about one tree): a correction from that tree's page. */
    suspend fun correction(city: String, tree: String, locationHint: String, why: String, page: String, token: String?): Boolean =
        post(
            JSONObject().put("kind", "correction").put("city", city).put("tree", tree)
                .put("location_hint", locationHint).put("why", why).put("page", page),
            token,
        )

    private suspend fun post(body: JSONObject, token: String?): Boolean =
        Supa.send(PATH, token = token, body = body.toString(), prefer = "return=minimal").ok

    /** WorthIt's tree field: "<id> (<name>)", which MyVotes reads the id back out of. */
    fun treeField(id: String, name: String) = "$id ($name)"
}

/** VoteCounts.swift: how many found each tree worth the visit, read once per launch. */
class VoteCounts {
    private var byTree by mutableStateOf<Map<String, Int>>(emptyMap())
    private var loaded = false

    suspend fun loadOnce() {
        if (loaded) return
        loaded = true
        val r = Supa.send("/rest/v1/rpc/tree_vote_counts", body = "{}")
        if (!r.ok) return
        byTree = runCatching {
            val a = JSONArray(r.body)
            (0 until a.length()).associate { i ->
                val o = a.getJSONObject(i)
                o.getString("tree_id") to o.optInt("up", 0)
            }
        }.getOrDefault(emptyMap())
    }

    /** Only a count of one or more; nothing is better than "0". */
    fun up(treeId: String): Int? = byTree[treeId]?.takeIf { it >= 1 }

    fun record(treeId: String, from: String, to: String) {
        var n = byTree[treeId] ?: 0
        if (from == "up") n = maxOf(0, n - 1)
        if (to == "up") n += 1
        byTree = byTree + (treeId to n)
    }
}

/** MyVotes: your own thumbs and reports, read back from your rows on the server. */
class MyVotes {
    var byTree by mutableStateOf<Map<String, String>>(emptyMap())
        private set
    var reports by mutableStateOf<Map<String, String>>(emptyMap())
        private set
    var detailed by mutableStateOf<Set<String>>(emptySet())
        private set

    fun vote(treeId: String) = byTree[treeId].orEmpty()
    fun hasReported(treeId: String) = treeId in reports
    fun reason(treeId: String) = reports[treeId].orEmpty()
    fun hasDetailed(treeId: String) = treeId in detailed

    fun setVote(treeId: String, value: String) {
        byTree = if (value.isEmpty()) byTree - treeId else byTree + (treeId to value)
    }

    fun markReported(treeId: String, reason: String) {
        reports = reports + (treeId to reason)
        detailed = detailed - treeId
    }

    fun markDetailed(treeId: String) {
        detailed = detailed + treeId
    }

    fun forget() {
        byTree = emptyMap(); reports = emptyMap(); detailed = emptySet()
    }

    suspend fun load(token: String?) {
        if (token == null) return forget()
        val rows = Supa.rows("/rest/v1/submissions?select=tree,kind,why&kind=eq.feedback&order=created_at.asc", token)
        val found = HashMap<String, String>()
        val said = HashMap<String, String>()
        val saidMore = HashSet<String>()
        for (row in rows) {
            val field = row.optString("tree")
            val why = row.optString("why")
            val tree = treeId(field)
            if (tree.isEmpty() || why.isEmpty()) continue
            when {
                why.startsWith("report detail") -> saidMore.add(tree)
                why.startsWith("report") -> {
                    saidMore.remove(tree)
                    said[tree] = if (": " in why) why.substringAfter(":").trim() else ""
                }
                why.startsWith("vote undone") -> found.remove(tree)
                why == "worth it" -> found[tree] = "up"
                why == "not worth it" -> found[tree] = "down"
            }
        }
        byTree = found
        reports = said
        detailed = saidMore
    }

    companion object {
        fun treeId(field: String): String = field.split(" ", limit = 2).firstOrNull().orEmpty()
    }
}

/** TreeNotes.swift: the notes on one tree, and yours. */
class TreeNotes {
    data class Note(val treeId: String, val body: String, val createdAt: String, val authorName: String?, val authorAvatar: String?) {
        val date: Instant get() = parseDate(createdAt)
    }

    data class Mine(val body: String, val createdAt: String) {
        val date: Instant get() = parseDate(createdAt)
    }

    var all by mutableStateOf<List<Note>>(emptyList())
        private set
    var mine by mutableStateOf<Mine?>(null)
        private set
    /** The table is not there (404): the section draws nothing. */
    var gone by mutableStateOf(false)
        private set

    fun here(tree: String): List<Note> = all.filter { it.treeId == tree && !isMine(it) }

    private fun isMine(n: Note): Boolean {
        val m = mine ?: return false
        return kotlin.math.abs(n.date.epochSecond - m.date.epochSecond) < 2
    }

    suspend fun load(tree: String, token: String?) {
        val r = Supa.send("/rest/v1/rpc/tree_notes_for", body = JSONObject().put("ids", JSONArray(listOf(tree))).toString())
        if (r.code == 404) {
            gone = true
        } else if (r.ok) {
            all = parse(r.body)
        }
        mine = if (token != null) {
            Supa.rows("/rest/v1/tree_notes?select=body,created_at&tree_id=eq.$tree", token).firstOrNull()?.let {
                Mine(it.optString("body"), it.optString("created_at"))
            }
        } else {
            null
        }
    }

    suspend fun save(tree: String, body: String, token: String): Boolean {
        val now = Instant.now().toString()
        val ok = Supa.send(
            "/rest/v1/tree_notes?on_conflict=user_id,tree_id",
            token = token,
            body = JSONObject().put("tree_id", tree).put("body", body).put("updated_at", now).toString(),
            prefer = "resolution=merge-duplicates,return=minimal",
        ).ok
        if (ok) mine = Mine(body, mine?.createdAt ?: now)
        return ok
    }

    suspend fun delete(tree: String, token: String): Boolean {
        val ok = Supa.delete("/rest/v1/tree_notes?tree_id=eq.$tree", token)
        if (ok) {
            mine?.let { m -> all = all.filterNot { it.treeId == tree && kotlin.math.abs(it.date.epochSecond - m.date.epochSecond) < 2 } }
            mine = null
        }
        return ok
    }

    companion object {
        fun parse(body: String): List<Note> = runCatching {
            val a = JSONArray(body)
            (0 until a.length()).map { i ->
                val o = a.getJSONObject(i)
                Note(
                    o.getString("tree_id"),
                    o.getString("body"),
                    o.getString("created_at"),
                    o.optString("author_name").takeIf { it.isNotEmpty() && it != "null" },
                    o.optString("author_avatar").takeIf { it.isNotEmpty() && it != "null" },
                )
            }
        }.getOrDefault(emptyList())

        fun parseDate(iso: String): Instant =
            runCatching { OffsetDateTime.parse(iso).toInstant() }.getOrElse { runCatching { Instant.parse(iso) }.getOrElse { Instant.now() } }
    }
}
