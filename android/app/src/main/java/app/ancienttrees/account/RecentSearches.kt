// RECENT SEARCHES under the empty search field, the twin of ios
// Kit/RecentSearches.swift (Hidde, 2026-11-04: "i like all your proposals please
// build"). Google Maps, Instagram and Apple Maps list recent picks under an empty
// field, a cross per row and Clear all, tied to the account.
//
// Only what a person PICKED is recorded (a city, country, species, tree or a real
// town), never half-typed text. Signed in only, and on the server only: table
// recent_searches (supabase/recent-searches.sql), the same rows the iPhone and the
// website read. Nothing is kept on the phone beyond this screen's memory (hard
// rule 11), so signed out the section is simply not there. A missing table
// answers 404 or 400: rows stay empty and no section is drawn.

package app.ancienttrees.account

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import org.json.JSONArray
import org.json.JSONObject
import java.net.URLEncoder
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone

class RecentSearches {
    data class Entry(
        /** city | country | species | tree | place */
        val kind: String,
        /** City slug, country name, species name, tree id, or "lat,lng" for a real town. */
        val ref: String,
        val label: String,
        val sub: String,
    ) {
        val id: String get() = "$kind|$ref"
    }

    /** At most five, newest first, none older than 90 days. */
    var rows by mutableStateOf<List<Entry>>(emptyList())
        private set

    suspend fun load(token: String?) {
        if (token.isNullOrEmpty()) { rows = emptyList(); return }
        val since = iso(System.currentTimeMillis() - DAYS * 86_400_000L)
        val path = "/rest/v1/recent_searches?select=kind,key,label,sub" +
            "&searched_at=gte.${enc(since)}&order=searched_at.desc&limit=$LIMIT"
        rows = Supa.rows(path, token).mapNotNull { r ->
            val k = r.optString("kind").ifEmpty { null } ?: return@mapNotNull null
            val ref = r.optString("key").ifEmpty { null } ?: return@mapNotNull null
            Entry(k, ref, r.optString("label"), r.optString("sub"))
        }
    }

    /** The `-recentdemo` launch argument: rows to screenshot the section with. */
    fun demo(entries: List<Entry>) { rows = entries.take(LIMIT) }

    /** A pick: to the top here at once, then upserted with searched_at = now. */
    suspend fun record(e: Entry, token: String?) {
        rows = (listOf(e) + rows.filter { it.id != e.id }).take(LIMIT)
        if (token.isNullOrEmpty()) return
        val row = JSONObject().put("kind", e.kind).put("key", e.ref).put("label", e.label)
            .put("sub", e.sub).put("searched_at", iso(System.currentTimeMillis()))
        Supa.upsert("/rest/v1/recent_searches?on_conflict=user_id,kind,key", token, JSONArray().put(row))
    }

    suspend fun remove(e: Entry, token: String?) {
        rows = rows.filter { it.id != e.id }
        if (token.isNullOrEmpty()) return
        Supa.delete("/rest/v1/recent_searches?kind=eq.${enc(e.kind)}&key=eq.${enc(e.ref)}", token)
    }

    suspend fun clear(token: String?) {
        rows = emptyList()
        if (token.isNullOrEmpty()) return
        // RLS limits the delete to this person's own rows; PostgREST refuses a
        // DELETE with no filter, so the filter is one every row meets.
        Supa.delete("/rest/v1/recent_searches?kind=not.is.null", token)
    }

    companion object {
        const val LIMIT = 5
        const val DAYS = 90

        fun enc(s: String): String = URLEncoder.encode(s, "UTF-8").replace("+", "%20")

        fun iso(ms: Long): String = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", Locale.US)
            .apply { timeZone = TimeZone.getTimeZone("UTC") }
            .format(Date(ms))
    }
}
