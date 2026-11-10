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

    suspend fun load() {
        val s = account.fresh() ?: run { forget(); return }
        hearts = Supa.rows("/rest/v1/saves?select=tree_id", s.accessToken)
            .mapNotNull { it.optString("tree_id").ifEmpty { null } }.toSet()
        collected = Supa.rows("/rest/v1/visited?select=tree_id", s.accessToken)
            .mapNotNull { it.optString("tree_id").ifEmpty { null } }.toSet()
    }

    /** Signed out: what this phone showed goes with the account. */
    fun forget() {
        hearts = emptySet()
        collected = emptySet()
    }

    /**
     * Heart on or off. The screen changes at once and the server is asked; if it
     * says no, the heart goes back, because the server is the record.
     */
    suspend fun toggle(treeId: String): Boolean {
        val s = account.fresh() ?: return false
        val on = treeId !in hearts
        hearts = if (on) hearts + treeId else hearts - treeId
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
        if (!ok) hearts = if (on) hearts - treeId else hearts + treeId
        return ok
    }
}
