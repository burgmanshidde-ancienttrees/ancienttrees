// Want to go (hearts) and collected trees, held on the server under the account
// (`saves` and `visited`, "account" in data/cross-device.json). The phone keeps
// them in memory only and reads them again at every launch: nothing a person does
// is saved on the device (hard rule 11).

package app.ancienttrees.account

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import org.json.JSONArray
import org.json.JSONObject
import java.net.URLEncoder

class Saves(private val account: Account) {
    var hearts by mutableStateOf<Set<String>>(emptySet())
        private set
    var collected by mutableStateOf<Set<String>>(emptySet())
        private set
    /** When each heart was put on and each tree collected (ms), for My trees' newest-first order. */
    var heartedAt by mutableStateOf<Map<String, Long>>(emptyMap())
        private set
    var collectedAt by mutableStateOf<Map<String, Long>>(emptyMap())
        private set

    suspend fun load() {
        // The stand-in has no account to read; the seeded lanes stay as they are.
        if (account.standIn) return
        val s = account.fresh() ?: run { forget(); return }
        val saveRows = Supa.rows("/rest/v1/saves?select=tree_id,created_at", s.accessToken)
        val visitRows = Supa.rows("/rest/v1/visited?select=tree_id,visited_at", s.accessToken)
        heartedAt = saveRows.mapNotNull { r ->
            r.optString("tree_id").ifEmpty { null }?.let { it to (MyTrees.stamp(r.optString("created_at")) ?: 0L) }
        }.toMap()
        collectedAt = visitRows.mapNotNull { r ->
            r.optString("tree_id").ifEmpty { null }?.let { it to (MyTrees.stamp(r.optString("visited_at")) ?: 0L) }
        }.toMap()
        hearts = heartedAt.keys
        collected = collectedAt.keys
    }

    /** A tree just collected; the server already holds the row. */
    fun noteCollected(treeId: String) {
        collected = collected + treeId
        collectedAt = collectedAt + (treeId to System.currentTimeMillis())
    }

    /**
     * REMOVED AT ONCE, WITH UNDO (TreeDetail.uncollectWithUndo, Hidde 2026-10-10):
     * the tick comes off here and on the server; the photographs stay. Returns
     * the day it was first collected, for Undo, or null when the server said no
     * (then the tick stays, because the server is the record).
     */
    suspend fun uncollect(treeId: String): Long? {
        val s = account.fresh() ?: return null
        val at = collectedAt[treeId] ?: System.currentTimeMillis()
        collected = collected - treeId
        collectedAt = collectedAt - treeId
        if (account.standIn) return at
        val ok = Supa.delete("/rest/v1/visited?tree_id=eq.${URLEncoder.encode(treeId, "UTF-8")}", s.accessToken)
        if (!ok) {
            collected = collected + treeId
            collectedAt = collectedAt + (treeId to at)
            Measure.event("sync_failed", mapOf("tree" to treeId, "why" to "visited"))
            return null
        }
        return at
    }

    /** Undo: the tick back on the day it was first made (Saved.restoreVisited). */
    suspend fun recollect(treeId: String, at: Long): Boolean {
        val s = account.fresh() ?: return false
        collected = collected + treeId
        collectedAt = collectedAt + (treeId to at)
        if (account.standIn) return true
        val ok = Supa.upsert(
            "/rest/v1/visited?on_conflict=user_id,tree_id",
            s.accessToken,
            JSONArray().put(JSONObject().put("user_id", s.userId).put("tree_id", treeId).put("visited_at", Collector.day(java.util.Date(at)))),
        )
        if (!ok) {
            collected = collected - treeId; collectedAt = collectedAt - treeId
            Measure.event("sync_failed", mapOf("tree" to treeId, "why" to "visited"))
        } else {
            Measure.event("tree_visited", mapOf("tree" to treeId))
        }
        return ok
    }

    /** -collected= and -saved=: the sweep's stand-ins, debug builds only, nothing sent. */
    fun seed(collectedIds: List<String>, savedIds: List<String>) {
        val now = System.currentTimeMillis()
        collectedAt = collectedAt + collectedIds.mapIndexed { i, id -> id to now - i }
        heartedAt = heartedAt + savedIds.mapIndexed { i, id -> id to now - i }
        collected = collectedAt.keys
        hearts = heartedAt.keys
    }

    /** Signed out: what this phone showed goes with the account. */
    fun forget() {
        hearts = emptySet()
        collected = emptySet()
        heartedAt = emptyMap()
        collectedAt = emptyMap()
    }

    /**
     * Heart on or off. The screen changes at once and the server is asked; if it
     * says no, the heart goes back, because the server is the record.
     */
    suspend fun toggle(treeId: String): Boolean {
        val s = account.fresh() ?: run { Measure.event("sync_failed", mapOf("tree" to treeId, "why" to "no_session")); return false }
        val on = treeId !in hearts
        hearts = if (on) hearts + treeId else hearts - treeId
        heartedAt = if (on) heartedAt + (treeId to System.currentTimeMillis()) else heartedAt - treeId
        // The stand-in keeps the change on screen, as the iPhone's local save does.
        if (account.standIn) return true
        val id = URLEncoder.encode(treeId, "UTF-8")
        val ok = if (on) {
            Supa.upsert(
                "/rest/v1/saves?on_conflict=user_id,tree_id",
                s.accessToken,
                JSONArray().put(JSONObject().put("user_id", s.userId).put("tree_id", treeId)),
            )
        } else {
            Supa.delete("/rest/v1/saves?tree_id=eq.$id", s.accessToken)
        }
        if (!ok) {
            hearts = if (on) hearts - treeId else hearts + treeId
            heartedAt = if (on) heartedAt - treeId else heartedAt + (treeId to System.currentTimeMillis())
            // PostHog hears when a change did NOT reach the account (ContentView's saved.onMutate).
            Measure.event("sync_failed", mapOf("tree" to treeId, "why" to "saves"))
        } else if (on) {
            Measure.event("tree_saved", mapOf("tree" to treeId))
        }
        return ok
    }
}
